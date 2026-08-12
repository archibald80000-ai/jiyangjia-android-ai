from __future__ import annotations

import asyncio
from datetime import datetime, timezone
import json
import logging
import uuid
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, Query, Request, Response, UploadFile, WebSocket, WebSocketDisconnect

from .admin_routes import create_admin_router
from .admin_store import AdminContentStore
from .asr import DoubaoASRConfig, DoubaoASRProvider
from .audio_store import InMemoryAudioStore
from .config import load_settings
from .knowledge import KnowledgeDocument, SAFE_TRANSFER_TEXT, SQLiteKnowledgeStore
from .kiosk_demo import router as kiosk_demo_router
from .http_cache import conditional_json, payload_digest
from .llm import (
    OpenAICompatibleChatConfig,
    OpenAICompatibleEmbeddingConfig,
    OpenAICompatibleEmbeddingProvider,
    OpenAICompatibleLLMProvider,
)
from .providers import MockASRProvider, MockEmbeddingProvider, MockLLMProvider, MockTTSProvider
from .public_access import create_public_access_router
from .schemas import DialogueResponse, DialogueTextRequest, KnowledgeIndexRequest, KnowledgeSearchRequest
from .transcript_normalization import normalize_transcript_text
from .streaming_asr import (
    FRAME_BYTES,
    MAX_PCM_BYTES,
    DoubaoStreamingASRProvider,
    MockStreamingASRProvider,
    WebRtcVadState,
    pcm_to_wav,
)
from .tts import DoubaoTTSConfig, DoubaoTTSProvider, ProviderCallError, ProviderConfigurationError


settings = load_settings()
logger = logging.getLogger("jiyangjia.gateway")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
STREAM_PROGRESS_INTERVAL_SECONDS = 15.0

app = FastAPI(title=settings.app_name, version=settings.app_version)
knowledge_store = SQLiteKnowledgeStore(settings.knowledge_db_path, faiss_index_path=settings.knowledge_faiss_path)
admin_store = AdminContentStore(settings.admin_db_path, upload_dir=settings.admin_upload_dir, asset_dir=settings.asset_dir)
audio_store = InMemoryAudioStore()
asr_provider = MockASRProvider()
llm_provider = MockLLMProvider()
tts_provider = MockTTSProvider()
embedding_provider = MockEmbeddingProvider()
streaming_asr_provider = MockStreamingASRProvider()
tts_configuration_error: ProviderConfigurationError | None = None
asr_configuration_error: ProviderConfigurationError | None = None
llm_configuration_error: ProviderConfigurationError | None = None
embedding_configuration_error: ProviderConfigurationError | None = None

if settings.asr_provider == "doubao":
    try:
        asr_provider = DoubaoASRProvider(DoubaoASRConfig.from_settings(settings))
        streaming_asr_provider = DoubaoStreamingASRProvider(asr_provider, settings.doubao_streaming_asr_endpoint)
    except ProviderConfigurationError as exc:
        asr_configuration_error = exc

if settings.tts_provider == "doubao":
    try:
        tts_provider = DoubaoTTSProvider(DoubaoTTSConfig.from_settings(settings))
    except ProviderConfigurationError as exc:
        tts_configuration_error = exc

if settings.llm_provider in {"deepseek", "doubao", "ark", "volcengine", "openai-compatible", "compatible"}:
    try:
        llm_provider = OpenAICompatibleLLMProvider(OpenAICompatibleChatConfig.from_settings(settings, settings.llm_provider))
    except ProviderConfigurationError as exc:
        llm_configuration_error = exc

if settings.embedding_provider in {"doubao", "ark", "volcengine", "openai-compatible", "compatible"}:
    try:
        embedding_provider = OpenAICompatibleEmbeddingProvider(OpenAICompatibleEmbeddingConfig.from_settings(settings, settings.embedding_provider))
    except ProviderConfigurationError as exc:
        embedding_configuration_error = exc


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _request_id(request: Request, body_request_id: str | None = None) -> str:
    return body_request_id or request.headers.get("X-Request-Id") or str(uuid.uuid4())


def _session_id(provided: str | None) -> str:
    return provided or f"sess_{uuid.uuid4().hex[:16]}"


def _safe_log(event: str, request_id: str, session_id: str = "-", **extra: Any) -> None:
    payload = {
        "event": event,
        "request_id": request_id,
        "session_id": session_id,
        **extra,
    }
    logger.info(payload)


def _normalize_transcript_payload(transcript: dict[str, object]) -> dict[str, object]:
    raw_text = str(transcript.get("text") or "")
    normalized = normalize_transcript_text(raw_text)
    if not normalized.changed:
        return transcript
    updated = dict(transcript)
    updated["raw_text"] = raw_text
    updated["text"] = normalized.text
    updated["normalization"] = {
        "changed": True,
        "replacements": normalized.replacements,
    }
    return updated


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    if "Cache-Control" not in response.headers:
        response.headers["Cache-Control"] = "no-store"
    return response


def _health_payload() -> dict[str, Any]:
    return {
        "ok": True,
        "service": settings.app_name,
        "version": settings.app_version,
        "checked_at": _now(),
        "providers": {
            "asr": settings.asr_provider,
            "tts": settings.tts_provider,
            "llm": settings.llm_provider,
            "embedding": settings.embedding_provider,
            "knowledge": settings.knowledge_provider,
        },
        "checks": {"gateway": "healthy", "knowledge_store": "ready"},
    }


@app.get("/health")
def root_health() -> dict[str, Any]:
    return _health_payload()


@app.get("/api/v1/health")
def api_health() -> dict[str, Any]:
    return _health_payload()


@app.get("/api/v1/readiness")
def readiness() -> dict[str, Any]:
    provider_checks = _provider_readiness()
    ready_for_dialogue = all(check["ready"] for check in provider_checks.values())
    return {
        "request_id": str(uuid.uuid4()),
        "ready": ready_for_dialogue,
        "status": "ready" if ready_for_dialogue else "blocked_provider_credentials",
        "providers": provider_checks,
        "knowledge": knowledge_store.status(),
    }


def _client_config_payload() -> dict[str, Any]:
    default_profile = admin_store.default_display_profile()
    return {
        "schema_version": 1,
        "config_version": settings.app_version,
        "refresh_interval_seconds": 60,
        "minimum_version_code": 1,
        "display_mode": settings.display_mode,
        "max_record_seconds": settings.max_record_seconds,
        "max_upload_bytes": settings.max_upload_bytes,
        "accepted_audio_types": list(settings.accepted_audio_types),
        "subtitle_max_chars": settings.subtitle_max_chars,
        "idle_video_version": "local",
        "assets_manifest": "/api/v1/assets/manifest",
        "release_manifest": "/api/v1/client/release",
        "display_profile": default_profile,
        "api": {
            "dialogue_text": "/api/v1/dialogue/text",
            "dialogue_audio": "/api/v1/dialogue/audio",
            "dialogue_stream": "/api/v1/dialogue/stream",
            "audio_base": "/api/v1/audio/",
            "display_profile": "/api/v1/display/profile",
            "assets_manifest": "/api/v1/assets/manifest",
        },
    }


@app.get("/api/v1/client/config")
def client_config(request: Request) -> Response:
    return conditional_json(request, _client_config_payload())


@app.get("/api/v1/client/bootstrap")
def client_bootstrap(
    request: Request,
    width: int = Query(default=1080, ge=320, le=7680),
    height: int = Query(default=1920, ge=320, le=7680),
    orientation: str | None = Query(default=None),
    version_code: int = Query(default=1, ge=1),
) -> Response:
    resolved_orientation = orientation if orientation in {"portrait", "landscape"} else ("landscape" if width >= height else "portrait")
    base_payload = {
        "schema_version": 1,
        "config": _client_config_payload(),
        "display_profile": admin_store.match_display_profile(width, height, resolved_orientation),
        "assets_manifest": admin_store.manifest(),
        "client": {
            "width_px": width,
            "height_px": height,
            "orientation": resolved_orientation,
            "version_code": version_code,
            "update_required": version_code < 1,
        },
    }
    digest = payload_digest(base_payload)
    payload = {"bundle_version": digest, **base_payload}
    return conditional_json(request, payload, etag=f'"{digest}"')


@app.get("/api/v1/client/release")
def client_release(request: Request) -> Response:
    payload = {
        "package": settings.android_release_package,
        "version_code": settings.android_release_version_code,
        "version_name": settings.android_release_version_name,
        "apk_url": settings.android_release_apk_url,
        "size_bytes": settings.android_release_size_bytes,
        "sha256": settings.android_release_sha256.upper(),
        "signing_certificate_sha256": settings.android_release_certificate_sha256.upper(),
        "release_notes": settings.android_release_notes,
    }
    required = ("version_code", "version_name", "apk_url", "size_bytes", "sha256", "signing_certificate_sha256")
    missing = [name for name in required if not payload[name]]
    if missing or not str(payload["apk_url"]).startswith("https://"):
        raise HTTPException(
            status_code=503,
            detail={"code": "RELEASE_NOT_CONFIGURED", "missing": missing, "message_for_user": "当前没有可用的受控升级。"},
        )
    return conditional_json(request, payload)


@app.post("/api/v1/dialogue/text", response_model=DialogueResponse)
async def dialogue_text(request: Request, body: DialogueTextRequest) -> DialogueResponse:
    request_id = _request_id(request, body.request_id)
    session_id = _session_id(body.session_id)
    question = body.text.strip()
    if not question:
        raise HTTPException(status_code=400, detail={"code": "INVALID_TEXT", "message_for_user": "请重新说一遍。"})
    return await _run_dialogue(question, request_id, session_id, transcript_provider="text")


@app.post("/api/v1/dialogue/audio", response_model=DialogueResponse)
async def dialogue_audio(
    request: Request,
    session_id: str | None = Form(default=None),
    request_id: str | None = Form(default=None),
    duration_ms: int = Form(default=0),
    sample_rate: int | None = Form(default=None),
    input_device: str | None = Form(default=None),
    audio: UploadFile = File(...),
) -> DialogueResponse:
    rid = _request_id(request, request_id)
    sid = _session_id(session_id)
    content_type = audio.content_type or "application/octet-stream"
    if content_type not in settings.accepted_audio_types:
        raise HTTPException(status_code=422, detail={"code": "UNSUPPORTED_AUDIO", "message_for_user": "当前录音格式不支持，请重试。"})
    content = await audio.read()
    if len(content) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail={"code": "AUDIO_TOO_LARGE", "message_for_user": "录音太长，请缩短后重试。"})
    if asr_configuration_error is not None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "BLOCKED_PROVIDER_CREDENTIALS",
                "failed_stage": "asr_provider_config",
                "message_for_user": "语音识别还没有配置完成，请联系工作人员。",
                "missing": asr_configuration_error.missing,
            },
        )
    try:
        transcript = await asr_provider.transcribe(content, content_type, rid)
    except ProviderCallError as exc:
        raise HTTPException(
            status_code=502 if exc.retryable else 400,
            detail={
                "code": exc.code,
                "message_for_user": "语音识别暂时不可用，请稍后再试。",
                "retryable": exc.retryable,
            },
        ) from exc
    transcript = _normalize_transcript_payload(transcript)
    _safe_log("dialogue_audio.received", rid, sid, bytes=len(content), duration_ms=duration_ms, sample_rate=sample_rate, input_device=input_device)
    return await _run_dialogue(str(transcript["text"]), rid, sid, transcript_provider=str(transcript["provider"]), transcript=transcript)


@app.websocket("/api/v1/dialogue/stream")
async def dialogue_stream(websocket: WebSocket) -> None:
    await websocket.accept()
    rid = str(uuid.uuid4())
    sid = _session_id(None)
    stream = None
    pcm = bytearray()
    vad = WebRtcVadState()
    fallback_used = False
    try:
        first = await websocket.receive_json()
        if first.get("type") != "start":
            await _ws_event(websocket, "error", rid, code="START_REQUIRED", message="start event required")
            return
        rid = str(first.get("request_id") or rid)
        sid = _session_id(first.get("session_id"))
        raw_generation = first.get("generation")
        if isinstance(raw_generation, bool) or not isinstance(raw_generation, int) or raw_generation < 0:
            await _ws_event(
                websocket,
                "error",
                rid,
                code="INVALID_START",
                message="invalid stream start event",
            )
            return
        generation = raw_generation
        try:
            stream = await asyncio.wait_for(
                streaming_asr_provider.open_stream(rid),
                timeout=settings.doubao_asr_timeout_seconds,
            )
        except Exception as exc:
            _safe_log("dialogue_stream.provider_open_failed", rid, sid, error=exc.__class__.__name__)
            await _ws_event(websocket, "stage", rid, stage="buffered_fallback", generation=generation)
        await _ws_event(websocket, "ready", rid, sample_rate=16_000, frame_bytes=FRAME_BYTES, generation=generation)

        should_finish = False
        while not should_finish:
            message = await websocket.receive()
            if message.get("type") == "websocket.disconnect":
                return
            if message.get("text") is not None:
                control = json.loads(message["text"])
                if control.get("request_id") not in {None, rid}:
                    continue
                if control.get("type") == "cancel":
                    await _ws_event(websocket, "stage", rid, stage="cancelled", generation=generation)
                    return
                if control.get("type") == "stop":
                    should_finish = True
                    continue
                continue
            frame = message.get("bytes") or b""
            if len(frame) != FRAME_BYTES:
                await _ws_event(websocket, "error", rid, code="BAD_PCM_FRAME", message=f"expected {FRAME_BYTES} bytes")
                return
            if len(pcm) + len(frame) > MAX_PCM_BYTES:
                await _ws_event(websocket, "error", rid, code="AUDIO_TOO_LARGE", message="PCM buffer exceeds 1 MiB")
                return
            pcm.extend(frame)
            event = vad.accept(frame)
            if stream is not None:
                try:
                    for partial in await stream.push(frame):
                        await _ws_event(websocket, "partial_transcript", rid, text=partial, generation=generation)
                except Exception as exc:
                    _safe_log("dialogue_stream.provider_failed", rid, sid, error=exc.__class__.__name__)
                    await stream.close()
                    stream = None
                    await _ws_event(websocket, "stage", rid, stage="buffered_fallback", generation=generation)
            if event.speech_started:
                await _ws_event(websocket, "speech_started", rid, generation=generation)
            if event.no_speech_timeout:
                await _ws_event(websocket, "error", rid, code="NO_SPEECH_TIMEOUT", message="no speech detected")
                return
            if event.speech_ended or event.max_duration:
                await _ws_event(websocket, "speech_ended", rid, reason="silence" if event.speech_ended else "max_duration", generation=generation)
                should_finish = True

        if not vad.started:
            await _ws_event(websocket, "error", rid, code="NO_SPEECH", message="no speech detected")
            return
        await _ws_event(websocket, "stage", rid, stage="asr_finalizing", generation=generation)
        try:
            if stream is None:
                raise ProviderCallError("STREAM_INTERRUPTED", "streaming provider unavailable", retryable=True)
            transcript = await asyncio.wait_for(stream.finish(), timeout=settings.doubao_asr_timeout_seconds)
        except Exception as exc:
            if fallback_used or not pcm:
                raise
            fallback_used = True
            _safe_log("dialogue_stream.wav_fallback", rid, sid, bytes=len(pcm), cause=exc.__class__.__name__)
            transcript = await asr_provider.transcribe(pcm_to_wav(bytes(pcm)), "audio/wav", rid)
        transcript = _normalize_transcript_payload(transcript)
        await _ws_event(websocket, "final_transcript", rid, transcript=transcript, fallback_used=fallback_used, generation=generation)
        await _ws_event(websocket, "stage", rid, stage="answering", generation=generation)
        dialogue_task = asyncio.create_task(
            _run_dialogue(str(transcript["text"]), rid, sid, str(transcript["provider"]), transcript)
        )
        try:
            while not dialogue_task.done():
                done, _ = await asyncio.wait(
                    {dialogue_task},
                    timeout=STREAM_PROGRESS_INTERVAL_SECONDS,
                )
                if dialogue_task in done:
                    break
                await _ws_event(
                    websocket,
                    "stage",
                    rid,
                    stage="answering",
                    heartbeat=True,
                    generation=generation,
                )
            result = await dialogue_task
        finally:
            if not dialogue_task.done():
                dialogue_task.cancel()
        payload = result.model_dump(mode="json")
        await _ws_event(websocket, "answer", rid, answer=payload["answer"], knowledge=payload["knowledge"], sources=payload["sources"], generation=generation)
        await _ws_event(websocket, "tts_ready", rid, tts=payload["tts"], generation=generation)
    except WebSocketDisconnect:
        _safe_log("dialogue_stream.disconnected", rid, sid, bytes=len(pcm))
    except Exception as exc:
        _safe_log("dialogue_stream.failed", rid, sid, error=exc.__class__.__name__, bytes=len(pcm))
        try:
            detail = exc.detail if isinstance(exc, HTTPException) else {}
            code = detail.get("code", "STREAM_FAILED") if isinstance(detail, dict) else "STREAM_FAILED"
            await _ws_event(websocket, "error", rid, code=code, message="stream dialogue failed")
        except Exception:
            pass
    finally:
        if stream is not None:
            await stream.close()


async def _ws_event(websocket: WebSocket, event_type: str, request_id: str, **payload: Any) -> None:
    await websocket.send_json({"type": event_type, "request_id": request_id, **payload})


@app.post("/api/v1/knowledge/index")
async def knowledge_index(body: KnowledgeIndexRequest, request: Request) -> dict[str, Any]:
    rid = _request_id(request)
    if embedding_configuration_error is not None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "BLOCKED_PROVIDER_CREDENTIALS",
                "failed_stage": "embedding_provider_config",
                "message_for_user": "知识检索还没有配置完成，请联系工作人员。",
                "missing": embedding_configuration_error.missing,
            },
        )
    documents = [
        KnowledgeDocument(
            doc_id=item.id,
            title=item.title,
            text=item.text,
            status=item.status,
            source_uri=item.source_uri,
        )
        for item in body.documents
    ]
    result = await knowledge_store.index_documents(documents, embedding_provider, rid)
    _safe_log("knowledge.index", rid, documents=result["documents"], chunks=result["chunks"])
    return {"request_id": rid, "indexed": result["documents"], "chunks": result["chunks"], "status": result["status"]}


@app.post("/api/v1/knowledge/search")
async def knowledge_search(body: KnowledgeSearchRequest, request: Request) -> dict[str, Any]:
    rid = _request_id(request, body.request_id)
    if embedding_configuration_error is not None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "BLOCKED_PROVIDER_CREDENTIALS",
                "failed_stage": "embedding_provider_config",
                "message_for_user": "知识检索还没有配置完成，请联系工作人员。",
                "missing": embedding_configuration_error.missing,
            },
        )
    policy = knowledge_store.classify_query(body.query)
    if policy["action"] != "search":
        return {
            "request_id": rid,
            "status": "safe_transfer",
            "matches": [],
            "sources": [],
            "policy": policy,
        }
    matches = await knowledge_store.search(body.query, embedding_provider, rid, top_k=body.top_k, include_draft=body.include_draft)
    return {
        "request_id": rid,
        "status": "matched" if matches else "no_match",
        "matches": matches,
        "sources": [match["source"] for match in matches],
    }


@app.get("/api/v1/knowledge/status")
def knowledge_status(request: Request) -> dict[str, Any]:
    knowledge_status_payload = knowledge_store.status()
    return {
        "request_id": _request_id(request),
        "provider": settings.knowledge_provider,
        "embedding_provider": settings.embedding_provider,
        "embedding_ready": embedding_configuration_error is None,
        "embedding_missing": embedding_configuration_error.missing if embedding_configuration_error else [],
        "vector_index": knowledge_status_payload["faiss"],
        "documents": knowledge_status_payload["documents"],
        "chunks": knowledge_status_payload["chunks"],
        "embeddings": knowledge_status_payload["embeddings"],
        "latest_run": knowledge_status_payload["latest_run"],
    }


@app.get("/api/v1/audio/{audio_id}")
def get_audio(audio_id: str, request: Request) -> Response:
    blob = audio_store.get(audio_id)
    if not blob:
        raise HTTPException(status_code=404, detail={"code": "AUDIO_NOT_FOUND", "message_for_user": "语音文件已过期，请重新咨询。"})
    return Response(content=blob.content, media_type=blob.content_type, headers={"X-Request-Id": _request_id(request)})


async def _run_dialogue(
    question: str,
    request_id: str,
    session_id: str,
    transcript_provider: str,
    transcript: dict[str, Any] | None = None,
) -> DialogueResponse:
    policy = knowledge_store.classify_query(question)
    if policy["action"] != "search":
        return await _run_policy_transfer(question, request_id, session_id, transcript_provider, transcript, str(policy.get("category") or "policy"))
    if embedding_configuration_error is not None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "BLOCKED_PROVIDER_CREDENTIALS",
                "failed_stage": "embedding_provider_config",
                "message_for_user": "知识检索还没有配置完成，请联系工作人员。",
                "missing": embedding_configuration_error.missing,
            },
        )
    matches = await knowledge_store.search(question, embedding_provider, request_id, top_k=3)
    if llm_configuration_error is not None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "BLOCKED_PROVIDER_CREDENTIALS",
                "failed_stage": "llm_provider_config",
                "message_for_user": "问答服务还没有配置完成，请联系工作人员。",
                "missing": llm_configuration_error.missing,
            },
        )
    try:
        llm = await llm_provider.chat([{"role": "user", "content": question}], matches, request_id)
    except ProviderCallError as exc:
        raise HTTPException(
            status_code=502 if exc.retryable else 400,
            detail={
                "code": exc.code,
                "message_for_user": "问答服务暂时不可用，请联系工作人员。",
                "retryable": exc.retryable,
            },
        ) from exc
    if tts_configuration_error is not None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "BLOCKED_PROVIDER_CREDENTIALS",
                "failed_stage": "tts_provider_config",
                "message_for_user": "语音服务还没有配置完成，请联系工作人员。",
                "missing": tts_configuration_error.missing,
            },
        )
    try:
        tts = await tts_provider.synthesize(str(llm["text"]), voice_id=None, request_id=request_id)
    except ProviderCallError as exc:
        raise HTTPException(
            status_code=502 if exc.retryable else 400,
            detail={
                "code": exc.code,
                "message_for_user": "语音服务暂时不可用，请稍后再试。",
                "retryable": exc.retryable,
            },
        ) from exc
    blob = audio_store.put(bytes(tts["content"]), str(tts["content_type"]))
    sources = [match["source"] | {"id": match["id"], "title": match["title"], "status": match["status"]} for match in matches]
    _safe_log("dialogue.completed", request_id, session_id, provider=transcript_provider, matched=len(matches), audio_id=blob.audio_id)
    return DialogueResponse(
        request_id=request_id,
        session_id=session_id,
        transcript=transcript or {"text": question, "provider": transcript_provider, "language": "zh-CN", "confidence": 1.0},
        knowledge={"status": "matched" if matches else "no_match", "matches": matches, "provider": settings.knowledge_provider},
        answer={"text": llm["text"], "provider": llm["provider"], "source": llm["source"], "subtitles": llm["subtitles"]},
        tts={"provider": tts["provider"], "content_type": tts["content_type"], "audio_id": blob.audio_id, "duration_ms": tts["duration_ms"]},
        sources=sources,
    )


async def _run_policy_transfer(
    question: str,
    request_id: str,
    session_id: str,
    transcript_provider: str,
    transcript: dict[str, Any] | None,
    category: str,
) -> DialogueResponse:
    if tts_configuration_error is not None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "BLOCKED_PROVIDER_CREDENTIALS",
                "failed_stage": "tts_provider_config",
                "message_for_user": "语音服务还没有配置完成，请联系工作人员。",
                "missing": tts_configuration_error.missing,
            },
        )
    try:
        tts = await tts_provider.synthesize(SAFE_TRANSFER_TEXT, voice_id=None, request_id=request_id)
    except ProviderCallError as exc:
        raise HTTPException(
            status_code=502 if exc.retryable else 400,
            detail={
                "code": exc.code,
                "message_for_user": "语音服务暂时不可用，请稍后再试。",
                "retryable": exc.retryable,
            },
        ) from exc
    blob = audio_store.put(bytes(tts["content"]), str(tts["content_type"]))
    _safe_log("dialogue.safe_transfer", request_id, session_id, provider=transcript_provider, category=category, audio_id=blob.audio_id)
    return DialogueResponse(
        request_id=request_id,
        session_id=session_id,
        transcript=transcript or {"text": question, "provider": transcript_provider, "language": "zh-CN", "confidence": 1.0},
        knowledge={"status": "safe_transfer", "matches": [], "provider": settings.knowledge_provider, "category": category},
        answer={"text": SAFE_TRANSFER_TEXT, "provider": "policy", "source": "safe_transfer", "subtitles": [SAFE_TRANSFER_TEXT]},
        tts={"provider": tts["provider"], "content_type": tts["content_type"], "audio_id": blob.audio_id, "duration_ms": tts["duration_ms"]},
        sources=[],
    )


def _provider_readiness() -> dict[str, dict[str, Any]]:
    return {
        "asr": _provider_check(settings.asr_provider, asr_configuration_error),
        "tts": _provider_check(settings.tts_provider, tts_configuration_error),
        "llm": _provider_check(settings.llm_provider, llm_configuration_error),
        "embedding": _provider_check(settings.embedding_provider, embedding_configuration_error),
    }


def _provider_check(provider: str, error: ProviderConfigurationError | None) -> dict[str, Any]:
    missing = error.missing if error else []
    return {
        "provider": provider,
        "ready": not missing,
        "missing": missing,
    }


app.include_router(
    create_admin_router(
        settings=settings,
        knowledge_store=knowledge_store,
        admin_store=admin_store,
        embedding_provider=embedding_provider,
        provider_status=_provider_readiness,
        embedding_error=lambda: embedding_configuration_error,
    )
)
app.include_router(kiosk_demo_router)
app.include_router(create_public_access_router(settings))
