from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gateway.app.config import load_settings
from gateway.app.knowledge import SQLiteKnowledgeStore, parse_selected_knowledge_path
from gateway.app.llm import OpenAICompatibleEmbeddingConfig, OpenAICompatibleEmbeddingProvider
from gateway.app.providers import MockEmbeddingProvider
from gateway.app.tts import ProviderCallError, ProviderConfigurationError


async def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the lightweight RAG layer without scanning raw materials")
    parser.add_argument("--data", default="knowledge-test")
    parser.add_argument("--provider", choices=["mock", "doubao", "ark", "openai-compatible"], default="mock")
    parser.add_argument("--env-file", default=".env.local")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    data_dir = Path(args.data)
    docs_path = data_dir / "faq_mvp_approved.example.json"
    cases_path = data_dir / "test_questions.example.json"
    if not docs_path.exists() or not cases_path.exists():
        print(json.dumps({"ok": False, "code": "MISSING_TEST_DATA", "data": str(data_dir)}, ensure_ascii=False))
        return 2

    try:
        embedding_provider = _embedding_provider(args.provider, args.env_file)
        documents = parse_selected_knowledge_path(docs_path)
        cases = json.loads(cases_path.read_text(encoding="utf-8"))["cases"]
        store = SQLiteKnowledgeStore(":memory:")
        index_result = await store.index_documents(documents, embedding_provider, "eval-rag-index")
        results = []
        passed = 0
        for case in cases:
            question = str(case["question"])
            expected_status = str(case["expected_status"])
            expected_match_id = case.get("expected_match_id")
            policy = store.classify_query(question)
            if policy["action"] != "search":
                actual_status = "safe_transfer"
                matches = []
            else:
                matches = await store.search(question, embedding_provider, f"eval-{case['id']}", top_k=args.top_k)
                actual_status = "matched" if matches else "no_match"
            actual_ids = [match["id"] for match in matches]
            ok = actual_status == expected_status and (not expected_match_id or expected_match_id in actual_ids)
            passed += 1 if ok else 0
            results.append(
                {
                    "id": case["id"],
                    "ok": ok,
                    "expected_status": expected_status,
                    "actual_status": actual_status,
                    "expected_match_id": expected_match_id,
                    "actual_ids": actual_ids,
                    "sources": [match["source"] for match in matches],
                }
            )
    except ProviderConfigurationError as exc:
        print(json.dumps({"ok": False, "code": "BLOCKED_PROVIDER_CREDENTIALS", "missing": exc.missing}, ensure_ascii=False))
        return 2
    except ProviderCallError as exc:
        print(json.dumps({"ok": False, "code": exc.code, "retryable": exc.retryable, "message": str(exc)}, ensure_ascii=False))
        return 3 if exc.retryable else 4

    summary = {
        "ok": passed == len(results),
        "provider": args.provider,
        "documents": index_result["documents"],
        "chunks": index_result["chunks"],
        "cases": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "status": store.status(),
        "results": results,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["ok"] else 1


def _embedding_provider(provider: str, env_file: str):
    if provider == "mock":
        return MockEmbeddingProvider()
    settings = load_settings(env_file=env_file, override_env_file=True)
    return OpenAICompatibleEmbeddingProvider(OpenAICompatibleEmbeddingConfig.from_settings(settings, provider))


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
