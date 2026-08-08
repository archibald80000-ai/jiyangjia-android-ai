import json
from pathlib import Path

from scripts.build_public_knowledge_package import build_package


def _payload(documents: list[dict]) -> dict:
    return {"version": 2, "status": "ready", "documents": documents}


def test_build_package_preserves_content_and_sanitizes_sources(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    documents = [
        {
            "id": "faq_brand_001",
            "title": "品牌介绍",
            "text": "积养家是社区健康生活馆。",
            "status": "approved",
            "source_uri": r"E:\private\brand.md",
        },
        {
            "id": "faq_store_001",
            "title": "营业时间",
            "text": "营业时间待确认。",
            "status": "draft",
            "source_uri": r"E:\private\store.md",
        },
    ]
    (source / "import_all.json").write_text(json.dumps(_payload(documents), ensure_ascii=False), encoding="utf-8")
    (source / "import_batch_01.json").write_text(json.dumps(_payload(documents[:1]), ensure_ascii=False), encoding="utf-8")
    (source / "import_batch_02.json").write_text(json.dumps(_payload(documents[1:]), ensure_ascii=False), encoding="utf-8")

    manifest = build_package(source, output)

    published = json.loads((output / "import_all.json").read_text(encoding="utf-8"))
    assert published["documents"][0]["text"] == documents[0]["text"]
    assert published["documents"][0]["source_uri"] == "knowledge://faq_brand_001"
    assert published["documents"][1]["source_uri"] == "knowledge://faq_store_001"
    assert manifest["documents"] == 2
    assert manifest["statuses"] == {"approved": 1, "draft": 1}
    assert len(manifest["files"]) == 3
