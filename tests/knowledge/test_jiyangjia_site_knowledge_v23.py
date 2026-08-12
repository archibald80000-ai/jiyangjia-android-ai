from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from scripts.build_jiyangjia_site_knowledge_v23 import build


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "knowledge-public" / "v2.3"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def test_v23_is_complete_and_data_driven() -> None:
    manifest = _load(PACKAGE / "manifest.json")
    documents = _load(PACKAGE / "import_all.json")["documents"]
    catalog = _load(PACKAGE / "catalog.json")
    product_documents = [item for item in documents if item["id"].startswith("site_product_")]

    assert manifest["version"] == "2.3"
    assert manifest["build_strategy"] == "data_driven_from_public_site_products"
    assert len(catalog["products"]) == manifest["new_product_documents"] == 47
    assert len(catalog["source_documents"]) == 26
    assert len(documents) == manifest["documents"] == 251
    assert Counter(item["status"] for item in documents) == Counter({"approved": 227, "draft": 24})
    assert len(product_documents) == 47
    assert all(item["source_uri"].startswith("https://jiyangjia-ai.netlify.app/products/") for item in product_documents)
    assert all("资料待补充】" not in item["text"] for item in product_documents)


def test_v23_batches_sources_and_hashes_match() -> None:
    manifest = _load(PACKAGE / "manifest.json")
    documents = _load(PACKAGE / "import_all.json")["documents"]
    batched = []
    for name in manifest["batches"]:
        batch = _load(PACKAGE / name)["documents"]
        assert len(batch) <= 50
        batched.extend(batch)
    assert batched == documents
    assert len({item["id"] for item in documents}) == len(documents)

    source_map = _load(PACKAGE / "source-map.json")["documents"]
    assert set(source_map) == {item["id"] for item in documents}
    for item in manifest["files"]:
        path = PACKAGE / item["name"]
        assert path.stat().st_size == item["bytes"]
        assert _sha256(path) == item["sha256"]
    for item in manifest["site_files"]:
        path = PACKAGE / item["path"]
        assert path.stat().st_size == item["bytes"]
        assert _sha256(path) == item["sha256"]


def test_v23_builder_accepts_new_products_without_code_changes(tmp_path: Path) -> None:
    source = tmp_path / "site"
    shutil.copytree(PACKAGE / "site", source)
    index_path = source / "knowledge" / "index.json"
    index = _load(index_path)
    index["products"].append(
        {
            "id": "dynamic-test-product",
            "name": "动态测试产品",
            "aliases": ["测试别名"],
            "category": "测试",
            "url": "https://jiyangjia-ai.netlify.app/products/dynamic-test-product/",
            "price": "以门店公告为准",
            "specification": "",
            "short_intro": "用于验证构建器按数据扩展。",
            "status": "公开",
        }
    )
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    output = tmp_path / "output"
    manifest = build(source, ROOT / "knowledge-public" / "v2.2", output)
    documents = _load(output / "import_all.json")["documents"]

    assert manifest["new_product_documents"] == 48
    assert any(item["id"] == "site_product_dynamic-test-product" for item in documents)
    for item in manifest["files"]:
        generated = output / item["name"]
        assert b"\r\n" not in generated.read_bytes()
        assert generated.stat().st_size == item["bytes"]
        assert _sha256(generated) == item["sha256"]


def test_v23_public_package_excludes_secrets_and_runtime_data() -> None:
    forbidden_names = {".env", ".env.local", "knowledge.db", "faiss.index", ".DS_Store"}
    forbidden_content = ("BEGIN PRIVATE KEY", "DOUBAO_API_KEY=", "ARK_API_KEY=")
    for path in PACKAGE.rglob("*"):
        if not path.is_file():
            continue
        assert path.name not in forbidden_names
        if path.suffix.lower() in {".json", ".md", ".html", ".txt", ".js"}:
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            assert all(pattern not in text for pattern in forbidden_content)
