from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from lxml import html


VERSION = "2.4"
BATCH_SIZE = 50
SOURCE_SPECS = (
    {
        "name": "积养家七膳煨汤｜七款汤膳故事.html",
        "slug": "qishan-seven",
        "archive": "qishan-seven-soup-stories.html",
        "prefix": "soup_story_qishan_seven",
    },
    {
        "name": "积养家瓦罐六膳｜六款瓦罐汤故事.html",
        "slug": "waguan-six",
        "archive": "waguan-six-soup-stories.html",
        "prefix": "soup_story_waguan_six",
    },
)


def _read_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected an object in {path}")
    return payload


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path.write_bytes(content.encode("utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _clean(value: object) -> str:
    return " ".join(str(value or "").split()).strip()


def _class_xpath(name: str) -> str:
    return f"contains(concat(' ', normalize-space(@class), ' '), ' {name} ')"


def _text(node: object, xpath: str) -> str:
    values = node.xpath(xpath)
    parts: list[str] = []
    for value in values:
        if isinstance(value, str):
            parts.append(value)
        else:
            parts.extend(value.itertext())
    return _clean(" ".join(parts))


def _find_sources(source_root: Path) -> list[tuple[dict[str, str], Path]]:
    found: list[tuple[dict[str, str], Path]] = []
    for spec in SOURCE_SPECS:
        matches = [path for path in source_root.rglob(spec["name"]) if path.is_file()]
        if len(matches) != 1:
            raise ValueError(f"expected one source named {spec['name']}, found {len(matches)}")
        found.append((spec, matches[0]))
    return found


def _parse_source(spec: dict[str, str], source: Path) -> tuple[list[dict[str, object]], dict[str, object]]:
    root = html.fromstring(source.read_bytes())
    title = _text(root, "//title/text()")
    intro = _text(root, f"//*[ {_class_xpath('cover-intro')} ]//text()")
    notice = _text(root, f"//*[ {_class_xpath('notice')} ]//text()")
    articles = root.xpath(f"//article[{_class_xpath('soup')}]")
    if not articles:
        raise ValueError(f"no soup articles found in {source}")

    source_uri = f"knowledge://soup-story-v2.4/{spec['slug']}"
    article_documents: list[dict[str, object]] = []
    soup_titles: list[str] = []
    sections: list[dict[str, object]] = []
    for index, article in enumerate(articles, 1):
        soup_title = _text(article, ".//h3//text()")
        subtitle = _text(article, f".//*[{_class_xpath('soup-title')}]/p//text()")
        description = _text(article, "./p[1]//text()")
        facts = _text(article, f".//*[{_class_xpath('facts')}]//text()")
        steps = [
            _clean(" ".join(item.itertext()))
            for item in article.xpath(".//details//li")
            if _clean(" ".join(item.itertext()))
        ]
        story = _text(article, f".//*[{_class_xpath('story')}]//text()")
        scene = _text(article, f".//*[{_class_xpath('scene')}]//text()")
        pending = _text(article, f".//*[{_class_xpath('pending')}]//text()")
        questions = (
            f"{soup_title}是什么？",
            f"{soup_title}有哪些食材？",
            f"{soup_title}怎么做？",
            f"{soup_title}是什么口感？",
            f"讲讲{soup_title}的故事。",
        )
        lines = [
            *questions,
            f"系列资料：{title}",
            f"汤品名称：{soup_title}",
            f"特点：{subtitle}",
            f"资料介绍：{description}",
            f"配方与风味：{facts}",
            *( ["制作步骤：" + " ".join(f"{step_index}. {step}" for step_index, step in enumerate(steps, 1))] if steps else [] ),
            f"故事：{story}",
            f"员工介绍与注意事项：{scene}",
            *( [f"待确认事项：{pending}"] if pending else [] ),
            "审核状态：本资料尚需核对最终菜单、名称和特殊人群合规口径，当前仅作内部复核，不进入顾客 approved 检索。",
        ]
        document_id = f"{spec['prefix']}_{index:02d}"
        document_text = "\n".join(line for line in lines if line.strip())
        if len(document_text) > 5000:
            raise ValueError(f"document too long: {document_id}")
        article_documents.append(
            {
                "id": document_id,
                "title": soup_title,
                "text": document_text,
                "status": "draft",
                "source_uri": f"{source_uri}#{article.get('id') or index}",
                "source_type": "html",
            }
        )
        soup_titles.append(soup_title)
        sections.append(
            {
                "document_id": document_id,
                "section_id": article.get("id") or str(index),
                "title": soup_title,
                "pending": pending,
            }
        )

    collection_id = f"{spec['prefix']}_collection"
    collection_text = "\n".join(
        (
            f"{title}是什么？",
            f"{title}包含哪些汤？",
            f"请介绍{title}。",
            f"系列名称：{title}",
            f"系列介绍：{intro}",
            "汤品目录：" + "、".join(soup_titles),
            f"统一食用提示：{notice}",
            "审核状态：页面标注需核对最终菜单；系列与单品当前均为 draft，不进入顾客 approved 检索。",
        )
    )
    collection = {
        "id": collection_id,
        "title": title,
        "text": collection_text,
        "status": "draft",
        "source_uri": source_uri,
        "source_type": "html",
    }
    metadata = {
        "slug": spec["slug"],
        "original_name": source.name,
        "archive": f"sources/{spec['archive']}",
        "title": title,
        "source_sha256": _sha256(source),
        "source_bytes": source.stat().st_size,
        "collection_id": collection_id,
        "sections": sections,
    }
    return [collection, *article_documents], metadata


def build(source_root: Path, base_package: Path, output_dir: Path) -> dict[str, object]:
    base_documents = _read_json(base_package / "import_all.json").get("documents")
    if not isinstance(base_documents, list):
        raise ValueError("base package must contain documents[]")
    output_dir.mkdir(parents=True, exist_ok=True)
    for stale in output_dir.glob("import_batch_*.json"):
        stale.unlink()
    for stale in output_dir.glob("import_delta_*.json"):
        stale.unlink()

    source_dir = output_dir / "sources"
    if source_dir.exists():
        shutil.rmtree(source_dir)
    source_dir.mkdir(parents=True)

    new_documents: list[dict[str, object]] = []
    source_records: list[dict[str, object]] = []
    for spec, source in _find_sources(source_root):
        documents, metadata = _parse_source(spec, source)
        target = source_dir / spec["archive"]
        shutil.copy2(source, target)
        if _sha256(target) != metadata["source_sha256"]:
            raise ValueError(f"source copy mismatch: {source.name}")
        metadata["archive_sha256"] = _sha256(target)
        new_documents.extend(documents)
        source_records.append(metadata)

    documents = [*base_documents, *new_documents]
    ids = [str(item["id"]) for item in documents]
    if len(ids) != len(set(ids)):
        raise ValueError("document ids are not unique")
    _write_json(output_dir / "import_all.json", {"version": VERSION, "status": "review_required", "documents": documents})

    batch_names: list[str] = []
    for offset in range(0, len(documents), BATCH_SIZE):
        name = f"import_batch_{offset // BATCH_SIZE + 1:02d}.json"
        batch_names.append(name)
        _write_json(
            output_dir / name,
            {"version": VERSION, "batch": offset // BATCH_SIZE + 1, "documents": documents[offset : offset + BATCH_SIZE]},
        )

    delta_batch_names: list[str] = []
    for offset in range(0, len(new_documents), BATCH_SIZE):
        name = f"import_delta_{offset // BATCH_SIZE + 1:02d}.json"
        delta_batch_names.append(name)
        _write_json(
            output_dir / name,
            {"version": VERSION, "batch": offset // BATCH_SIZE + 1, "documents": new_documents[offset : offset + BATCH_SIZE]},
        )

    source_map = dict(_read_json(base_package / "source-map.json").get("documents") or {})
    for source_record in source_records:
        for section in source_record["sections"]:
            source_map[section["document_id"]] = {
                "source_file": source_record["archive"],
                "source_sha256": source_record["source_sha256"],
                "section_id": section["section_id"],
                "section_title": section["title"],
            }
        source_map[source_record["collection_id"]] = {
            "source_file": source_record["archive"],
            "source_sha256": source_record["source_sha256"],
            "section_id": "page",
            "section_title": source_record["title"],
        }
    _write_json(output_dir / "source-map.json", {"version": VERSION, "documents": source_map})
    _write_json(output_dir / "catalog.json", {"version": VERSION, "review_status": "draft", "sources": source_records})

    cases = []
    for document in new_documents:
        questions = [line for line in str(document["text"]).splitlines()[:5] if line.endswith("？")]
        for index, question in enumerate(questions[:3], 1):
            cases.append(
                {
                    "id": f"{document['id']}_{index:02d}",
                    "question": question,
                    "draft_id": document["id"],
                    "public_must_exclude": True,
                    "source_uri": document["source_uri"],
                }
            )
    _write_json(output_dir / "test_questions.json", {"version": VERSION, "cases": cases})

    package_files = [
        "import_all.json",
        *batch_names,
        *delta_batch_names,
        "source-map.json",
        "catalog.json",
        "test_questions.json",
    ]
    statuses = Counter(str(item["status"]) for item in documents)
    manifest = {
        "schema_version": 2,
        "package": "jiyangjia-public-knowledge-v2.4",
        "version": VERSION,
        "base_version": "2.3",
        "documents": len(documents),
        "base_documents": len(base_documents),
        "new_documents": len(new_documents),
        "statuses": dict(sorted(statuses.items())),
        "review_status": "DRAFT_REVIEW_REQUIRED",
        "batch_size": BATCH_SIZE,
        "batches": batch_names,
        "delta_batches": delta_batch_names,
        "sources": source_records,
        "files": [
            {"name": name, "bytes": (output_dir / name).stat().st_size, "sha256": _sha256(output_dir / name)}
            for name in package_files
        ],
    }
    _write_json(output_dir / "manifest.json", manifest)
    readme = (
        "# 积养家公开知识库 v2.4\n\n"
        "本版本保留 v2.3 全部知识，并新增两份经用户授权的汤膳故事 HTML。\n\n"
        f"- 完整知识：{len(documents)} 条。\n"
        f"- 新增汤膳资料：{len(new_documents)} 条，全部为 `draft`。\n"
        "- 新增内容在最终菜单、名称和特殊人群合规口径确认前，不进入顾客回答。\n"
        "- 两份原始 HTML 按原字节归档在 `sources/`，SHA-256 见 `manifest.json`。\n"
        "- 全新 Gateway 按 `batches` 导入；从 v2.3 升级只按 `delta_batches` 导入。\n"
        "- 不要把 `import_all.json` 与批次文件重复提交。\n"
    )
    (output_dir / "README.md").write_bytes(readme.encode("utf-8"))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--base-package", type=Path, default=Path("knowledge-public/v2.3"))
    parser.add_argument("--output-dir", type=Path, default=Path("knowledge-public/v2.4"))
    args = parser.parse_args()
    manifest = build(args.source_root.resolve(), args.base_package.resolve(), args.output_dir.resolve())
    print(json.dumps({"version": manifest["version"], "documents": manifest["documents"], "new_documents": manifest["new_documents"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
