from __future__ import annotations

from datetime import datetime, timezone
import logging
import uuid
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, Request, Response, UploadFile

from .asr import DoubaoASRConfig, DoubaoASRProvider
from .audio_store import InMemoryAudioStore
from .config import load_settings
from .knowledge import KnowledgeDocument, SQLiteKnowledgeStore
from .llm import (
    OpenAICompatibleChatConfig,
    OpenAICompatibleEmbeddingConfig,
    OpenAICompatibleEmbeddingProvider,
    OpenAICompatibleLLMProvider,
)
from .providers import MockASRProvider, MockEmbeddingProvider, MockLLMProvider, MockTTSProvider
from .schemas import DialogueResponse, DialogueTextRequest, KnowledgeIndexRequest, KnowledgeSearchRequest
from .tts import DoubaoTTSConfig, DoubaoTTSProvider, ProviderCallError, ProviderConfigurationError


settings = load_settings()
logger = logging.getLogger("jiyangjia.gateway")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title=settings.app_name, version=settings.app_version)
knowledge_store = SQLiteKnowledgeStore(settings.knowledge_db_path)
audio_store = InMemoryAudioStore()
asr_provider = MockASRProvider()
llm_provider = MockLLMProvider()
tts_provider = MockTTSProvider()
embedding_provider = MockEmbeddingProvider()
tts_configuration_error: ProviderConfigurationError | None = None
asr_configuration_error: ProviderConfigurationError | None = None
llm_configuration_error: ProviderConfigurationError | None = None
embedding_configuration_error: ProviderConfigurationError | None = None

if settings.asr_provider == "doubao":
    try:
        asr_provider = DoubaoASRProvider(DoubaoASRConfig.from_settings(settings))
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


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
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


@app.get("/api/v1/client/config")
def client_config() -> dict[str, Any]:
    return {
        "display_mode": settings.display_mode,
        "max_record_seconds": settings.max_record_seconds,
        "max_upload_bytes": settings.max_upload_bytes,
        "accepted_audio_types": list(settings.accepted_audio_types),
        "subtitle_max_chars": settings.subtitle_max_chars,
        "idle_video_version": "local",
        "api": {
            "dialogue_text": "/api/v1/dialogue/text",
            "dialogue_audio": "/api/v1/dialogue/audio",
            "audio_base": "/api/v1/audio/",
        },
    }


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
    _safe_log("dialogue_audio.received", rid, sid, bytes=len(content), duration_ms=duration_ms, sample_rate=sample_rate, input_device=input_device)
    return await _run_dialogue(str(transcript["text"]), rid, sid, transcript_provider=str(transcript["provider"]), transcript=transcript)


@app.post("/api/v1/knowledge/index")
async def knowledge_index(body: KnowledgeIndexRequest, request: Request) -> dict[str, Any]:
    rid = _request_id(request)
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
    count = knowledge_store.upsert_many(documents)
    _safe_log("knowledge.index", rid, documents=count)
    return {"request_id": rid, "indexed": count, "status": knowledge_store.status()}


@app.post("/api/v1/knowledge/search")
async def knowledge_search(body: KnowledgeSearchRequest, request: Request) -> dict[str, Any]:
    rid = _request_id(request, body.request_id)
    matches = knowledge_store.search(body.query, top_k=body.top_k, include_draft=body.include_draft)
    return {
        "request_id": rid,
        "status": "matched" if matches else "no_match",
        "matches": matches,
        "sources": [match["source"] for match in matches],
    }


@app.get("/api/v1/knowledge/status")
def knowledge_status(request: Request) -> dict[str, Any]:
    return {
        "request_id": _request_id(request),
        "provider": settings.knowledge_provider,
        "embedding_provider": settings.embedding_provider,
        "embedding_ready": embedding_configuration_error is None,
        "embedding_missing": embedding_configuration_error.missing if embedding_configuration_error else [],
        "vector_index": "deferred_to_TASK-012",
        "documents": knowledge_store.status(),
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
    matches = knowledge_store.search(question, top_k=3)
    if llm_configuration_error is not None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "BLOCKED_PROVIDER_CREDENTIALS",
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
