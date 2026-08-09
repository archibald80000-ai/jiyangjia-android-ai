from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import time
from pathlib import Path
from typing import Any

import httpx


DIALOGUE_QUESTIONS = (
    "请详细讲讲飞鸡蛋的品牌故事。",
    "福人有机五常大米多少钱，什么规格？",
    "立秋应该喝什么养生茶？",
    "积养家的生姜有什么特点？",
    "金华古法酱油是怎么做的？",
    "大有谷有哪些产品？",
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


async def _post_json(client: httpx.AsyncClient, url: str, payload: dict[str, Any], request_id: str) -> tuple[httpx.Response, float]:
    started = time.perf_counter()
    response = await client.post(url, json=payload, headers={"X-Request-Id": request_id})
    return response, round((time.perf_counter() - started) * 1000, 1)


async def run(
    base_url: str,
    package_dir: Path,
    *,
    skip_import: bool = False,
    skip_search: bool = False,
    skip_dialogue: bool = False,
) -> dict[str, Any]:
    manifest = _load(package_dir / "manifest.json")
    all_documents = _load(package_dir / "import_all.json")["documents"]
    draft_ids = {item["id"] for item in all_documents if item["status"] == "draft"}
    batch_names = [item["name"] for item in manifest["files"] if item["name"].startswith("import_batch_")]
    cases = _load(package_dir / "test_questions.json")["cases"]
    result: dict[str, Any] = {
        "base_url": base_url,
        "manifest": {
            "package": manifest["package"],
            "documents": manifest["documents"],
            "statuses": manifest["statuses"],
            "new_documents": manifest["new_documents"],
        },
        "imports": [],
        "search": {"cases": len(cases), "results": []},
        "dialogues": [],
    }

    timeout = httpx.Timeout(120.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        readiness = await client.get(f"{base_url}/api/v1/readiness")
        result["readiness"] = {"status_code": readiness.status_code, "body": readiness.json()}
        readiness.raise_for_status()
        if not readiness.json().get("ready"):
            raise RuntimeError("Gateway readiness is false")

        if not skip_import:
            for index, batch_name in enumerate(batch_names, 1):
                payload = _load(package_dir / batch_name)
                response, elapsed_ms = await _post_json(
                    client,
                    f"{base_url}/api/v1/knowledge/index",
                    payload,
                    f"task020f-import-{index:02d}",
                )
                record = {"name": batch_name, "status_code": response.status_code, "elapsed_ms": elapsed_ms, "body": response.json()}
                result["imports"].append(record)
                response.raise_for_status()

        status = await client.get(f"{base_url}/api/v1/knowledge/status", headers={"X-Request-Id": "task020f-status"})
        result["knowledge_status"] = {"status_code": status.status_code, "body": status.json()}
        status.raise_for_status()

        passed = 0
        sources_complete = 0
        draft_leaks = 0
        latencies: list[float] = []
        if not skip_search:
            for index, case in enumerate(cases, 1):
                response, elapsed_ms = await _post_json(
                    client,
                    f"{base_url}/api/v1/knowledge/search",
                    {"query": case["question"], "top_k": 3, "include_draft": False, "request_id": f"task020f-search-{index:03d}"},
                    f"task020f-search-{index:03d}",
                )
                body = response.json()
                matches = body.get("matches") or []
                actual_ids = [item.get("id") for item in matches]
                expected = set(case["expected_any"])
                ok = response.status_code == 200 and bool(expected.intersection(actual_ids))
                complete = response.status_code == 200 and bool(matches) and all(
                    str((item.get("source") or {}).get("uri") or "").startswith("knowledge://") for item in matches
                )
                leak_ids = sorted(draft_ids.intersection(actual_ids))
                passed += int(ok)
                sources_complete += int(complete)
                draft_leaks += len(leak_ids)
                latencies.append(elapsed_ms)
                result["search"]["results"].append({
                    "id": case["id"],
                    "question": case["question"],
                    "status_code": response.status_code,
                    "elapsed_ms": elapsed_ms,
                    "expected_any": case["expected_any"],
                    "actual_ids": actual_ids,
                    "ok": ok,
                    "sources_complete": complete,
                    "draft_leaks": leak_ids,
                    "request_id": body.get("request_id"),
                })

        result["search"].update({
            "passed": passed,
            "failed": len(cases) - passed,
            "pass_rate": round(passed / len(cases), 4) if cases and not skip_search else 1.0,
            "sources_complete": sources_complete,
            "sources_complete_rate": round(sources_complete / len(cases), 4) if cases and not skip_search else 1.0,
            "draft_leaks": draft_leaks,
            "latency_ms": {
                "min": min(latencies) if latencies else 0.0,
                "max": max(latencies) if latencies else 0.0,
                "avg": round(sum(latencies) / len(latencies), 1) if latencies else 0.0,
            },
        })

        if skip_dialogue:
            result["ok"] = result["search"]["pass_rate"] >= 0.9 and result["search"]["sources_complete_rate"] == 1.0 and draft_leaks == 0
            return result

        audio_candidate: tuple[bytes, str, str] | None = None
        for index, question in enumerate(DIALOGUE_QUESTIONS, 1):
            response, elapsed_ms = await _post_json(
                client,
                f"{base_url}/api/v1/dialogue/text",
                {"text": question, "session_id": "task020f", "request_id": f"task020f-dialogue-{index:02d}"},
                f"task020f-dialogue-{index:02d}",
            )
            body = response.json()
            tts = body.get("tts") or {}
            sources = body.get("sources") or []
            audio_id = tts.get("audio_id")
            audio_response = await client.get(f"{base_url}/api/v1/audio/{audio_id}") if audio_id else None
            audio_bytes = audio_response.content if audio_response is not None and audio_response.status_code == 200 else b""
            content_type = audio_response.headers.get("content-type", "") if audio_response is not None else ""
            record = {
                "question": question,
                "status_code": response.status_code,
                "elapsed_ms": elapsed_ms,
                "request_id": body.get("request_id"),
                "knowledge_status": (body.get("knowledge") or {}).get("status"),
                "source_ids": [item.get("id") or item.get("chunk_id") for item in sources],
                "sources": sources,
                "answer": (body.get("answer") or {}).get("text"),
                "answer_provider": (body.get("answer") or {}).get("provider"),
                "tts_provider": tts.get("provider"),
                "audio_id": audio_id,
                "audio_status": audio_response.status_code if audio_response is not None else None,
                "audio_content_type": content_type,
                "audio_bytes": len(audio_bytes),
                "audio_sha256": hashlib.sha256(audio_bytes).hexdigest().upper() if audio_bytes else None,
            }
            result["dialogues"].append(record)
            response.raise_for_status()
            if index == 2 and audio_bytes:
                audio_candidate = (audio_bytes, content_type.split(";")[0] or "audio/mpeg", question)

        if audio_candidate is None:
            raise RuntimeError("No TTS audio available for audio dialogue acceptance")
        audio_bytes, audio_type, source_question = audio_candidate
        started = time.perf_counter()
        audio_response = await client.post(
            f"{base_url}/api/v1/dialogue/audio",
            data={"session_id": "task020f-audio", "request_id": "task020f-dialogue-audio-01"},
            files={"audio": ("task020f.mp3", audio_bytes, audio_type)},
        )
        audio_elapsed = round((time.perf_counter() - started) * 1000, 1)
        audio_body = audio_response.json()
        generated_audio_id = (audio_body.get("tts") or {}).get("audio_id")
        generated = await client.get(f"{base_url}/api/v1/audio/{generated_audio_id}") if generated_audio_id else None
        result["audio_dialogue"] = {
            "synthetic_source_question": source_question,
            "status_code": audio_response.status_code,
            "elapsed_ms": audio_elapsed,
            "request_id": audio_body.get("request_id"),
            "transcript": audio_body.get("transcript"),
            "knowledge_status": (audio_body.get("knowledge") or {}).get("status"),
            "sources": audio_body.get("sources") or [],
            "answer_provider": (audio_body.get("answer") or {}).get("provider"),
            "tts_provider": (audio_body.get("tts") or {}).get("provider"),
            "audio_id": generated_audio_id,
            "audio_status": generated.status_code if generated is not None else None,
            "audio_content_type": generated.headers.get("content-type") if generated is not None else None,
            "audio_bytes": len(generated.content) if generated is not None and generated.status_code == 200 else 0,
        }
        audio_response.raise_for_status()

    result["ok"] = (
        result["search"]["pass_rate"] >= 0.9
        and result["search"]["sources_complete_rate"] == 1.0
        and result["search"]["draft_leaks"] == 0
        and all(item["status_code"] == 200 and item["audio_status"] == 200 and item["knowledge_status"] == "matched" and item["sources"] for item in result["dialogues"])
        and result["audio_dialogue"]["status_code"] == 200
        and result["audio_dialogue"]["audio_status"] == 200
        and result["audio_dialogue"]["knowledge_status"] == "matched"
        and bool(result["audio_dialogue"]["sources"])
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run TASK-020F real Gateway import, retrieval and dialogue acceptance.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8092")
    parser.add_argument("--package-dir", type=Path, default=Path("knowledge-public/v2.2"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-import", action="store_true")
    parser.add_argument("--skip-search", action="store_true")
    parser.add_argument("--skip-dialogue", action="store_true")
    args = parser.parse_args()
    result = asyncio.run(
        run(
            args.base_url.rstrip("/"),
            args.package_dir,
            skip_import=args.skip_import,
            skip_search=args.skip_search,
            skip_dialogue=args.skip_dialogue,
        )
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    summary = {
        "ok": result["ok"],
        "documents": result["knowledge_status"]["body"]["documents"],
        "vectors": result["knowledge_status"]["body"]["vector_index"],
        "search": {key: result["search"][key] for key in ("cases", "passed", "failed", "pass_rate", "sources_complete_rate", "draft_leaks", "latency_ms")},
        "dialogues": len(result["dialogues"]),
        "audio_dialogue": (result.get("audio_dialogue") or {}).get("status_code"),
        "output": str(args.output),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
