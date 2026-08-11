from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import httpx


QUESTIONS = (
    "积养家是什么？",
    "有什么产品？",
    "七膳鸡汤是什么？",
    "门店在哪里？",
    "怎么体验？",
)


async def run(base_url: str) -> dict[str, Any]:
    result: dict[str, Any] = {"base_url": base_url, "dialogues": []}
    audio_seed: bytes | None = None
    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        readiness = await client.get(f"{base_url}/api/v1/readiness")
        readiness.raise_for_status()
        result["readiness"] = readiness.json()

        for index, question in enumerate(QUESTIONS, 1):
            request_id = f"task014h-dialogue-text-{index:02d}"
            started = time.perf_counter()
            response = await client.post(
                f"{base_url}/api/v1/dialogue/text",
                json={"text": question, "session_id": "task014h-demo", "request_id": request_id},
                headers={"X-Request-Id": request_id},
            )
            elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
            body = response.json()
            response.raise_for_status()
            tts = body.get("tts") or {}
            audio_id = tts.get("audio_id")
            audio = await client.get(f"{base_url}/api/v1/audio/{audio_id}") if audio_id else None
            audio_bytes = audio.content if audio is not None and audio.status_code == 200 else b""
            if index == 1:
                audio_seed = audio_bytes
            result["dialogues"].append(
                {
                    "question": question,
                    "status_code": response.status_code,
                    "elapsed_ms": elapsed_ms,
                    "request_id": body.get("request_id"),
                    "knowledge_status": (body.get("knowledge") or {}).get("status"),
                    "source_ids": [item.get("id") or item.get("chunk_id") for item in body.get("sources") or []],
                    "answer": (body.get("answer") or {}).get("text"),
                    "answer_provider": (body.get("answer") or {}).get("provider"),
                    "tts_provider": tts.get("provider"),
                    "audio_id": audio_id,
                    "audio_status": audio.status_code if audio is not None else None,
                    "audio_content_type": audio.headers.get("content-type") if audio is not None else None,
                    "audio_bytes": len(audio_bytes),
                    "audio_sha256": hashlib.sha256(audio_bytes).hexdigest().upper() if audio_bytes else None,
                }
            )

        if not audio_seed:
            raise RuntimeError("No TTS audio was available for WAV dialogue acceptance")
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            raise RuntimeError("ffmpeg is required to create the Android-compatible WAV fixture")
        with tempfile.TemporaryDirectory(prefix="task014h-") as temp_dir:
            source = Path(temp_dir) / "tts-source.mp3"
            wav = Path(temp_dir) / "android-upload.wav"
            source.write_bytes(audio_seed)
            subprocess.run(
                [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(source), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)],
                check=True,
            )
            wav_bytes = wav.read_bytes()

        started = time.perf_counter()
        audio_response = await client.post(
            f"{base_url}/api/v1/dialogue/audio",
            data={"session_id": "task014h-demo-audio", "request_id": "task014h-dialogue-audio-01"},
            files={"audio": ("android-upload.wav", wav_bytes, "audio/wav")},
            headers={"X-Request-Id": "task014h-dialogue-audio-01"},
        )
        audio_elapsed_ms = round((time.perf_counter() - started) * 1000, 1)
        audio_body = audio_response.json()
        audio_response.raise_for_status()
        generated_id = (audio_body.get("tts") or {}).get("audio_id")
        generated = await client.get(f"{base_url}/api/v1/audio/{generated_id}") if generated_id else None
        result["audio_dialogue"] = {
            "status_code": audio_response.status_code,
            "elapsed_ms": audio_elapsed_ms,
            "request_id": audio_body.get("request_id"),
            "upload_content_type": "audio/wav",
            "upload_bytes": len(wav_bytes),
            "transcript": audio_body.get("transcript"),
            "knowledge_status": (audio_body.get("knowledge") or {}).get("status"),
            "source_ids": [item.get("id") or item.get("chunk_id") for item in audio_body.get("sources") or []],
            "answer_provider": (audio_body.get("answer") or {}).get("provider"),
            "tts_provider": (audio_body.get("tts") or {}).get("provider"),
            "audio_id": generated_id,
            "audio_status": generated.status_code if generated is not None else None,
            "audio_content_type": generated.headers.get("content-type") if generated is not None else None,
            "audio_bytes": len(generated.content) if generated is not None and generated.status_code == 200 else 0,
        }

    provider_names = {item["answer_provider"] for item in result["dialogues"]}
    result["ok"] = (
        result["readiness"].get("ready") is True
        and provider_names == {"doubao"}
        and all(
            item["status_code"] == 200
            and item["tts_provider"] == "doubao"
            and item["audio_status"] == 200
            and item["audio_bytes"] > 0
            for item in result["dialogues"]
        )
        and result["audio_dialogue"]["status_code"] == 200
        and result["audio_dialogue"]["answer_provider"] == "doubao"
        and result["audio_dialogue"]["tts_provider"] == "doubao"
        and result["audio_dialogue"]["audio_status"] == 200
        and result["audio_dialogue"]["audio_bytes"] > 0
        and bool(result["audio_dialogue"]["source_ids"])
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run TASK-014H production dialogue and Android WAV acceptance.")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = asyncio.run(run(args.base_url.rstrip("/")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": result["ok"],
                "text_dialogues": len(result["dialogues"]),
                "text_request_ids": [item["request_id"] for item in result["dialogues"]],
                "text_audio_ids": [item["audio_id"] for item in result["dialogues"]],
                "audio_dialogue": result["audio_dialogue"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
