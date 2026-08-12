from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "knowledge-public" / "v2.4"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_v24_preserves_v23_and_adds_draft_soup_stories() -> None:
    base = _load(ROOT / "knowledge-public" / "v2.3" / "import_all.json")["documents"]
    payload = _load(PACKAGE / "import_all.json")
    documents = payload["documents"]
    added = documents[len(base) :]

    assert documents[: len(base)] == base
    assert len(documents) == 266
    assert len(added) == 15
    assert Counter(item["status"] for item in documents) == Counter({"approved": 227, "draft": 39})
    assert all(item["status"] == "draft" for item in added)
    assert len([item for item in added if item["id"].startswith("soup_story_qishan_seven")]) == 8
    assert len([item for item in added if item["id"].startswith("soup_story_waguan_six")]) == 7
    assert any(item["title"] == "古法月子专用乌鸡汤" for item in added)
    assert any(item["title"] == "清润菌菇鸡瓦罐汤" for item in added)


def test_v24_batches_sources_and_hashes_are_complete() -> None:
    manifest = _load(PACKAGE / "manifest.json")
    documents = _load(PACKAGE / "import_all.json")["documents"]
    batched = []
    for name in manifest["batches"]:
        batch = _load(PACKAGE / name)["documents"]
        assert len(batch) <= 50
        batched.extend(batch)
    assert batched == documents
    assert len({item["id"] for item in documents}) == 266

    delta = []
    for name in manifest["delta_batches"]:
        batch = _load(PACKAGE / name)["documents"]
        assert len(batch) <= 50
        delta.extend(batch)
    assert delta == documents[-manifest["new_documents"] :]

    for item in manifest["files"]:
        path = PACKAGE / item["name"]
        assert b"\r\n" not in path.read_bytes()
        assert path.stat().st_size == item["bytes"]
        assert _sha256(path) == item["sha256"]
    for source in manifest["sources"]:
        path = PACKAGE / source["archive"]
        assert path.stat().st_size == source["source_bytes"]
        assert _sha256(path) == source["source_sha256"] == source["archive_sha256"]


def test_v24_source_map_and_public_safety_cases_cover_every_new_document() -> None:
    manifest = _load(PACKAGE / "manifest.json")
    documents = _load(PACKAGE / "import_all.json")["documents"]
    source_map = _load(PACKAGE / "source-map.json")["documents"]
    cases = _load(PACKAGE / "test_questions.json")["cases"]
    added_ids = {item["id"] for item in documents[-manifest["new_documents"] :]}

    assert set(source_map) == {item["id"] for item in documents}
    assert {item["draft_id"] for item in cases} == added_ids
    assert all(item["public_must_exclude"] is True for item in cases)
    assert all(len(item["text"]) <= 5000 for item in documents)
