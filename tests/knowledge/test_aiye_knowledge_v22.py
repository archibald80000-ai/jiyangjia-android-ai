from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "knowledge-public" / "v2.2"


def _load(name: str) -> dict:
    return json.loads((PACKAGE / name).read_text(encoding="utf-8-sig"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_v22_manifest_and_source_inventory_are_complete() -> None:
    manifest = _load("manifest.json")
    sources = manifest["source_files"]

    assert manifest["version"] == "2.2"
    assert manifest["source_authorization"] == "user_confirmed_public_and_human_approved"
    assert manifest["coverage"]["source_pages"] == 25
    assert manifest["coverage"]["solar_terms"] == 24
    assert manifest["coverage"]["food_medicine_ingredients"] == 19
    assert manifest["coverage"]["dayougu_skus"] == 11
    assert len(sources) == 25

    source_dir = PACKAGE / "sources" / "aiye-foods"
    assert sorted(path.suffix.lower() for path in source_dir.iterdir()) == [".html"] * 25
    assert not (source_dir / ".DS_Store").exists()
    assert not (source_dir / ".workbuddy").exists()
    for item in sources:
        path = PACKAGE / item["path"]
        assert path.is_file()
        assert path.stat().st_size == item["bytes"]
        assert _sha256(path) == item["sha256"]


def test_v22_documents_batches_and_sources_are_consistent() -> None:
    manifest = _load("manifest.json")
    all_documents = _load("import_all.json")["documents"]
    source_map = _load("source-map.json")["documents"]
    batches = []
    for item in manifest["files"]:
        if item["name"].startswith("import_batch_"):
            batch = _load(item["name"])["documents"]
            assert len(batch) <= 50
            batches.extend(batch)

    ids = [item["id"] for item in all_documents]
    new_documents = [item for item in all_documents if item["id"].startswith("aiye_")]
    assert len(ids) == len(set(ids)) == manifest["documents"]
    assert batches == all_documents
    assert set(source_map) == set(ids)
    assert len(new_documents) == manifest["new_documents"]
    assert Counter(item["status"] for item in new_documents) == Counter({"approved": len(new_documents)})
    assert all(0 < len(item["text"]) <= 5000 for item in all_documents)
    assert all(len(item["text"]) <= 1500 for item in new_documents if "_story_" in item["id"])
    assert all(item["source_uri"] == f"knowledge://{item['id']}" for item in all_documents)

    for item in manifest["files"]:
        assert _sha256(PACKAGE / item["name"]) == item["sha256"]


def test_v22_specialized_coverage_and_questions() -> None:
    catalog = _load("catalog.json")["coverage"]
    questions = _load("test_questions.json")["cases"]
    documents = {item["id"] for item in _load("import_all.json")["documents"]}

    assert len(catalog["solar_terms"]) == 24
    assert len(catalog["food_medicine_ingredients"]) == 19
    assert len(catalog["dayougu_skus"]) == 11
    assert len(questions) >= (25 + 24 + 19 + 11) * 3
    assert all(len(case["expected_any"]) >= 1 for case in questions)
    assert all(set(case["expected_any"]) <= documents for case in questions)

    counts = Counter(case["category"] for case in questions)
    assert counts["solar-term"] == 24 * 3
    assert counts["ingredient"] == 19 * 3
    assert counts["dayougu-sku"] == 11 * 3
    assert counts["dayougu-catalog"] == 3
    assert counts["source-story"] == 25 * 3

    audit = _load("claim-audit.json")
    assert audit["independent_external_fact_check"] is False
    assert len(audit["pages"]) == 25
    assert {item["status"] for item in audit["pages"]} == {"approved_by_user"}


def test_v22_public_package_has_no_common_secret_or_private_artifacts() -> None:
    forbidden_names = {".env", ".env.local", "knowledge.db", "faiss.index", ".DS_Store"}
    forbidden_patterns = ("BEGIN PRIVATE KEY", "AKLT", "DOUBAO_API_KEY=", "ARK_API_KEY=")

    for path in PACKAGE.rglob("*"):
        if not path.is_file():
            continue
        assert path.name not in forbidden_names
        if path.suffix.lower() in {".json", ".md", ".html"}:
            text = path.read_text(encoding="utf-8-sig")
            assert all(pattern not in text for pattern in forbidden_patterns)
