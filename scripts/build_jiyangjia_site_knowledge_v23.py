from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path


VERSION = "2.3"
BATCH_SIZE = 50
EXCLUDED_NAMES = {".DS_Store", ".env", ".env.local", "knowledge.db", "faiss.index"}
EXCLUDED_PARTS = {".git", ".workbuddy", "__pycache__"}


def _read_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected an object in {path}")
    return payload


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _copy_public_site(source_dir: Path, target_dir: Path) -> list[dict[str, object]]:
    if target_dir.exists():
        shutil.rmtree(target_dir)
    records: list[dict[str, object]] = []
    for source in sorted(path for path in source_dir.rglob("*") if path.is_file()):
        relative = source.relative_to(source_dir)
        if source.name in EXCLUDED_NAMES or EXCLUDED_PARTS.intersection(relative.parts):
            continue
        target = target_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        records.append(
            {
                "path": target.relative_to(target_dir.parent).as_posix(),
                "bytes": target.stat().st_size,
                "sha256": _sha256(target),
            }
        )
    return records


def _clean(value: object) -> str:
    return " ".join(str(value or "").split()).strip()


def _confirmed(value: object) -> str:
    text = _clean(value)
    return "" if not text or "待补" in text else text


def _product_document(product: dict[str, object], canonical_origin: str) -> dict[str, object]:
    product_id = _clean(product.get("id"))
    name = _clean(product.get("name"))
    if not product_id or not name:
        raise ValueError("every product requires id and name")
    aliases = [_clean(item) for item in product.get("aliases", []) if _clean(item)]
    source_url = _clean(product.get("url")) or f"{canonical_origin.rstrip('/')}/products/{product_id}/"
    questions = [
        f"{name}是什么？",
        f"{name}多少钱？",
        f"{name}是什么规格？",
        f"请详细介绍{name}。",
    ]
    lines = [
        *questions,
        f"产品名称：{name}",
        *( [f"别名：{'、'.join(aliases)}"] if aliases else [] ),
        *( [f"分类：{_clean(product.get('category'))}"] if _clean(product.get("category")) else [] ),
        *( [f"产品介绍：{_clean(product.get('short_intro'))}"] if _clean(product.get("short_intro")) else [] ),
        *( [f"公开售价：{_confirmed(product.get('price'))}"] if _confirmed(product.get("price")) else [] ),
        *( [f"规格：{_confirmed(product.get('specification'))}"] if _confirmed(product.get("specification")) else [] ),
    ]
    if "待补" in _clean(product.get("status")):
        lines.append("资料边界：公开页面未列明的信息请咨询门店工作人员，不得自行补充。")
    text = "\n".join(lines)
    if len(text) > 5000:
        raise ValueError(f"product document too long: {product_id}")
    return {
        "id": f"site_product_{product_id}",
        "title": name,
        "text": text,
        "status": "approved",
        "source_uri": source_url,
    }


def build(source_dir: Path, base_package: Path, output_dir: Path) -> dict[str, object]:
    index = _read_json(source_dir / "knowledge" / "index.json")
    if _clean(index.get("version")) != "2.1":
        raise ValueError("unsupported public site knowledge version")
    products = index.get("products")
    if not isinstance(products, list) or not products:
        raise ValueError("knowledge/index.json must contain products[]")
    product_ids = [_clean(item.get("id")) for item in products if isinstance(item, dict)]
    if len(product_ids) != len(products) or len(product_ids) != len(set(product_ids)):
        raise ValueError("product ids must be present and unique")

    base = _read_json(base_package / "import_all.json")
    base_documents = base.get("documents")
    if not isinstance(base_documents, list):
        raise ValueError("base package must contain documents[]")
    canonical_origin = _clean(index.get("canonical_origin")) or "https://jiyangjia-ai.netlify.app"
    product_documents = [_product_document(item, canonical_origin) for item in products]
    documents = [*base_documents, *product_documents]
    document_ids = [str(item["id"]) for item in documents]
    if len(document_ids) != len(set(document_ids)):
        raise ValueError("generated document ids are not unique")

    output_dir.mkdir(parents=True, exist_ok=True)
    for stale in output_dir.glob("import_batch_*.json"):
        stale.unlink()
    site_files = _copy_public_site(source_dir, output_dir / "site")
    _write_json(output_dir / "import_all.json", {"version": VERSION, "status": "ready", "documents": documents})

    batch_names: list[str] = []
    for offset in range(0, len(documents), BATCH_SIZE):
        batch_name = f"import_batch_{offset // BATCH_SIZE + 1:02d}.json"
        batch_names.append(batch_name)
        _write_json(
            output_dir / batch_name,
            {"version": VERSION, "batch": offset // BATCH_SIZE + 1, "documents": documents[offset : offset + BATCH_SIZE]},
        )

    base_source_map_path = base_package / "source-map.json"
    source_map = _read_json(base_source_map_path).get("documents", {}) if base_source_map_path.exists() else {}
    for product, document in zip(products, product_documents):
        source_map[document["id"]] = {
            "source_file": "site/knowledge/index.json",
            "source_url": document["source_uri"],
            "source_product_id": product["id"],
            "source_version": index["version"],
        }
    _write_json(output_dir / "source-map.json", {"version": VERSION, "documents": source_map})
    _write_json(
        output_dir / "catalog.json",
        {
            "version": VERSION,
            "canonical_origin": canonical_origin,
            "products": products,
            "source_documents": index.get("source_documents", []),
        },
    )
    cases = []
    for product, document in zip(products, product_documents):
        for suffix, question in (
            ("intro", f"{product['name']}是什么？"),
            ("price", f"{product['name']}多少钱？"),
            ("detail", f"详细介绍一下{product['name']}。"),
        ):
            cases.append(
                {
                    "id": f"{document['id']}_{suffix}",
                    "question": question,
                    "expected_any": [document["id"]],
                    "source_uri": document["source_uri"],
                }
            )
    _write_json(output_dir / "test_questions.json", {"version": VERSION, "cases": cases})

    package_files = ["import_all.json", *batch_names, "source-map.json", "catalog.json", "test_questions.json"]
    statuses = Counter(str(item["status"]) for item in documents)
    manifest = {
        "schema_version": 2,
        "package": "jiyangjia-public-knowledge-v2.3",
        "version": VERSION,
        "source_version": index["version"],
        "source_updated_at": index.get("updated_at"),
        "canonical_origin": canonical_origin,
        "build_strategy": "data_driven_from_public_site_products",
        "documents": len(documents),
        "base_documents": len(base_documents),
        "new_product_documents": len(product_documents),
        "statuses": dict(sorted(statuses.items())),
        "batch_size": BATCH_SIZE,
        "batches": batch_names,
        "site_files": site_files,
        "files": [
            {"name": name, "bytes": (output_dir / name).stat().st_size, "sha256": _sha256(output_dir / name)}
            for name in package_files
        ],
    }
    _write_json(output_dir / "manifest.json", manifest)
    (output_dir / "README.md").write_text(
        "# 积养家公开知识库 v2.3\n\n"
        "本包由公开发布站点 `knowledge/index.json` 数据驱动生成，不在代码中手写产品清单。\n\n"
        f"- 完整知识：{len(documents)} 条（新增公开产品卡 {len(product_documents)} 条）\n"
        f"- 产品目录：{len(products)} 个\n"
        f"- 来源文档：{len(index.get('source_documents', []))} 份\n"
        f"- 公开镜像：`site/`（{len(site_files)} 个文件）\n"
        "- Gateway 导入：按 `manifest.json` 的 `batches` 顺序导入，不要再重复导入 `import_all.json`。\n"
        "- 安全边界：资料待补、诊疗承诺、未发布库存和活动不得由 AI 自行补写。\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--base-package", type=Path, default=Path("knowledge-public/v2.2"))
    parser.add_argument("--output-dir", type=Path, default=Path("knowledge-public/v2.3"))
    args = parser.parse_args()
    manifest = build(args.source_dir.resolve(), args.base_package.resolve(), args.output_dir.resolve())
    print(json.dumps({"version": manifest["version"], "documents": manifest["documents"], "products": manifest["new_product_documents"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
