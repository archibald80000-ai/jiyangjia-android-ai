from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path
from typing import Any

import httpx


SAFE_TRANSFER_IDS = {
    "faq_boundary_002",
    "faq_boundary_005",
    "faq_boundary_006",
    "faq_boundary_007",
    "faq_food_004",
    "faq_service_002",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


async def post(client: httpx.AsyncClient, url: str, payload: dict[str, Any], request_id: str) -> tuple[httpx.Response, float]:
    started = time.perf_counter()
    response = await client.post(url, json=payload, headers={"X-Request-Id": request_id})
    return response, round((time.perf_counter() - started) * 1000, 1)


async def run(base_url: str, package_dir: Path, test_set: Path, *, skip_import: bool) -> dict[str, Any]:
    documents = load_json(package_dir / "import_all.json")["documents"]
    status_by_id = {item["id"]: item["status"] for item in documents}
    draft_ids = {item["id"] for item in documents if item["status"] == "draft"}
    cases = load_json(test_set)["cases"]
    result: dict[str, Any] = {"base_url": base_url, "imports": [], "cases": []}

    async with httpx.AsyncClient(timeout=httpx.Timeout(120.0)) as client:
        readiness = await client.get(f"{base_url}/api/v1/readiness")
        readiness.raise_for_status()
        result["readiness"] = readiness.json()
        if not result["readiness"].get("ready"):
            raise RuntimeError("Gateway readiness is false")

        if not skip_import:
            for number in (1, 2):
                name = f"import_batch_{number:02d}.json"
                response, elapsed_ms = await post(
                    client,
                    f"{base_url}/api/v1/knowledge/index",
                    load_json(package_dir / name),
                    f"task014h-v21-import-{number:02d}",
                )
                body = response.json()
                result["imports"].append(
                    {"name": name, "status_code": response.status_code, "elapsed_ms": elapsed_ms, "body": body}
                )
                response.raise_for_status()

        status = await client.get(f"{base_url}/api/v1/knowledge/status")
        status.raise_for_status()
        result["knowledge_status"] = status.json()

        passed = 0
        matched = 0
        sources_complete = 0
        draft_leaks = 0
        latencies: list[float] = []
        for index, case in enumerate(cases, 1):
            response, elapsed_ms = await post(
                client,
                f"{base_url}/api/v1/knowledge/search",
                {
                    "query": case["question"],
                    "top_k": 3,
                    "include_draft": False,
                    "request_id": f"task014h-v21-search-{index:03d}",
                },
                f"task014h-v21-search-{index:03d}",
            )
            body = response.json()
            matches = body.get("matches") or []
            actual_ids = [item.get("id") for item in matches]
            leaks = sorted(draft_ids.intersection(item for item in actual_ids if item))
            expected_id = case.get("expected_match_id")
            expected_status = case.get("expected_status")
            expected_document_status = status_by_id.get(expected_id)
            if expected_document_status == "approved":
                ok = expected_id in actual_ids
            elif expected_document_status == "draft":
                ok = expected_id not in actual_ids and not leaks
            elif expected_status == "safe_transfer":
                ok = not leaks and (
                    body.get("status") != "matched" or bool(SAFE_TRANSFER_IDS.intersection(actual_ids))
                )
            elif expected_status == "no_match":
                ok = body.get("status") != "matched" and not leaks
            else:
                ok = False
            complete = not matches or all(
                str((item.get("source") or {}).get("uri") or "").startswith("knowledge://") for item in matches
            )
            passed += int(ok)
            matched += int(body.get("status") == "matched")
            sources_complete += int(complete)
            draft_leaks += len(leaks)
            latencies.append(elapsed_ms)
            result["cases"].append(
                {
                    "id": case["id"],
                    "status_code": response.status_code,
                    "request_id": body.get("request_id"),
                    "expected_status": expected_status,
                    "expected_id": expected_id,
                    "actual_ids": actual_ids,
                    "ok": ok,
                    "sources_complete": complete,
                    "draft_leaks": leaks,
                    "elapsed_ms": elapsed_ms,
                }
            )

    documents_by_status = result["knowledge_status"].get("documents") or {}
    vector_index = result["knowledge_status"].get("vector_index") or {}
    summary = {
        "total": len(cases),
        "passed": passed,
        "failed": len(cases) - passed,
        "pass_rate": round(passed / len(cases), 4),
        "matched": matched,
        "sources_complete": sources_complete,
        "sources_complete_rate": round(sources_complete / len(cases), 4),
        "draft_leaks": draft_leaks,
        "latency_ms": {
            "min": min(latencies),
            "max": max(latencies),
            "avg": round(sum(latencies) / len(latencies), 1),
        },
    }
    result["summary"] = summary
    result["ok"] = (
        documents_by_status == {"approved": 41, "draft": 24, "rejected": 0}
        and vector_index.get("ready") is True
        and vector_index.get("vectors") == 65
        and vector_index.get("dimensions") == 2048
        and summary["pass_rate"] >= 0.9
        and summary["sources_complete_rate"] == 1.0
        and summary["draft_leaks"] == 0
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Import and verify the public v2.1 package against a real Gateway.")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--package-dir", type=Path, default=Path("knowledge-public/v2.1"))
    parser.add_argument("--test-set", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--skip-import", action="store_true")
    args = parser.parse_args()
    result = asyncio.run(
        run(args.base_url.rstrip("/"), args.package_dir, args.test_set, skip_import=args.skip_import)
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": result["ok"], "knowledge": result["knowledge_status"], "summary": result["summary"]}, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
