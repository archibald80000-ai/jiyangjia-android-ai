from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import httpx


def request_json(client: httpx.Client, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    started = time.perf_counter()
    response = client.request(method, path, **kwargs)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    try:
        body: Any = response.json()
    except ValueError:
        body = {"text": response.text[:500]}
    return {
        "method": method,
        "path": path,
        "status": response.status_code,
        "elapsed_ms": elapsed_ms,
        "x_request_id": response.headers.get("x-request-id"),
        "content_type": response.headers.get("content-type"),
        "body": body,
    }


def fetch_audio(client: httpx.Client, audio_id: str) -> dict[str, Any]:
    started = time.perf_counter()
    response = client.get(f"/api/v1/audio/{audio_id}")
    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    return {
        "status": response.status_code,
        "elapsed_ms": elapsed_ms,
        "x_request_id": response.headers.get("x-request-id"),
        "content_type": response.headers.get("content-type"),
        "bytes": len(response.content),
        "sha256": hashlib.sha256(response.content).hexdigest().upper() if response.is_success else None,
    }


def dialogue_audio(client: httpx.Client, audio_path: Path, content_type: str, request_id: str) -> dict[str, Any]:
    with audio_path.open("rb") as stream:
        result = request_json(
            client,
            "POST",
            "/api/v1/dialogue/audio",
            data={
                "session_id": "task014-final",
                "request_id": request_id,
                "duration_ms": "3000",
                "sample_rate": "16000",
                "input_device": "android-usb-or-default",
            },
            files={"audio": (audio_path.name, stream, content_type)},
        )
    body = result.get("body") if isinstance(result.get("body"), dict) else {}
    tts = body.get("tts") if isinstance(body.get("tts"), dict) else {}
    audio_id = str(tts.get("audio_id") or "")
    result["input"] = {
        "name": audio_path.name,
        "content_type": content_type,
        "bytes": audio_path.stat().st_size,
        "sha256": hashlib.sha256(audio_path.read_bytes()).hexdigest().upper(),
    }
    result["audio_fetch"] = fetch_audio(client, audio_id) if audio_id else {"status": 0, "note": "audio_id missing"}
    return result


def dialogue_ok(result: dict[str, Any], *, expect_asr: bool) -> bool:
    body = result.get("body") if isinstance(result.get("body"), dict) else {}
    transcript = body.get("transcript") if isinstance(body.get("transcript"), dict) else {}
    knowledge = body.get("knowledge") if isinstance(body.get("knowledge"), dict) else {}
    answer = body.get("answer") if isinstance(body.get("answer"), dict) else {}
    tts = body.get("tts") if isinstance(body.get("tts"), dict) else {}
    audio_fetch = result.get("audio_fetch") if isinstance(result.get("audio_fetch"), dict) else {}
    return all(
        [
            result.get("status") == 200,
            bool(body.get("request_id")),
            transcript.get("provider") == ("doubao" if expect_asr else "text"),
            knowledge.get("provider") == "sqlite_lightweight",
            answer.get("provider") == "doubao",
            tts.get("provider") == "doubao",
            bool(tts.get("audio_id")),
            bool(body.get("sources")),
            audio_fetch.get("status") == 200,
            audio_fetch.get("content_type", "").startswith("audio/mpeg"),
            int(audio_fetch.get("bytes") or 0) > 0,
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the final TASK-014 production acceptance once.")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--wav", type=Path, required=True)
    parser.add_argument("--mp3", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    for path in (args.wav, args.mp3):
        if not path.is_file():
            raise SystemExit(f"missing input audio: {path}")

    timeout = httpx.Timeout(90.0, connect=10.0)
    with httpx.Client(base_url=args.base_url.rstrip("/"), timeout=timeout) as client:
        checks = {
            "health": request_json(client, "GET", "/health"),
            "api_health": request_json(client, "GET", "/api/v1/health"),
            "readiness": request_json(client, "GET", "/api/v1/readiness"),
            "client_config": request_json(client, "GET", "/api/v1/client/config"),
            "knowledge_status": request_json(client, "GET", "/api/v1/knowledge/status"),
            "knowledge_index": request_json(client, "POST", "/api/v1/knowledge/index", json={"documents": []}),
            "knowledge_search": request_json(
                client,
                "POST",
                "/api/v1/knowledge/search",
                json={"query": "积养家门店的营业时间是什么？", "top_k": 3, "request_id": "task014-final-search"},
            ),
        }
        text_dialogue = request_json(
            client,
            "POST",
            "/api/v1/dialogue/text",
            json={"text": "积养家门店的营业时间是什么？", "session_id": "task014-final", "request_id": "task014-final-text"},
        )
        text_body = text_dialogue.get("body") if isinstance(text_dialogue.get("body"), dict) else {}
        text_tts = text_body.get("tts") if isinstance(text_body.get("tts"), dict) else {}
        text_audio_id = str(text_tts.get("audio_id") or "")
        text_dialogue["audio_fetch"] = fetch_audio(client, text_audio_id) if text_audio_id else {"status": 0, "note": "audio_id missing"}

        wav_dialogue = dialogue_audio(client, args.wav, "audio/wav", "task014-final-wav")
        mp3_dialogue = dialogue_audio(client, args.mp3, "audio/mpeg", "task014-final-mp3")

    readiness_body = checks["readiness"].get("body") if isinstance(checks["readiness"].get("body"), dict) else {}
    knowledge_body = checks["knowledge_status"].get("body") if isinstance(checks["knowledge_status"].get("body"), dict) else {}
    base_ok = all(item["status"] == 200 for item in checks.values())
    providers = readiness_body.get("providers") if isinstance(readiness_body.get("providers"), dict) else {}
    providers_ready = bool(providers) and all(bool(item.get("ready")) for item in providers.values() if isinstance(item, dict))
    approved_clean = (knowledge_body.get("documents") or {}).get("approved") == 10
    result = {
        "task": "TASK-014",
        "base_url": args.base_url,
        "run_epoch": int(time.time()),
        "checks": checks,
        "dialogue_text": text_dialogue,
        "dialogue_wav": wav_dialogue,
        "dialogue_mp3": mp3_dialogue,
        "summary": {
            "base_api_ok": base_ok,
            "providers_ready": providers_ready,
            "approved_knowledge_count_is_10": approved_clean,
            "text_chain_ok": dialogue_ok(text_dialogue, expect_asr=False),
            "wav_chain_ok": dialogue_ok(wav_dialogue, expect_asr=True),
            "mp3_chain_ok": dialogue_ok(mp3_dialogue, expect_asr=True),
        },
    }
    result["summary"]["overall_ok"] = all(result["summary"].values())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0 if result["summary"]["overall_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
