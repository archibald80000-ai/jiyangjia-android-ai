from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import quote


VERSION = "2.2"
BATCH_SIZE = 50
MIN_CHUNK_CHARS = 600
MAX_CHUNK_CHARS = 1350

SOURCE_FILES = {
    "24节气养生茶速查表.html": ("solar-term-tea-guide", "24节气养生茶速查表"),
    "茶油品牌故事.html": ("camellia-oil", "茶油品牌故事"),
    "大有谷合作产品手册.html": ("dayougu-products", "大有谷合作产品手册"),
    "二十四节气养生茶品牌故事.html": ("solar-term-tea-story", "二十四节气养生茶品牌故事"),
    "飞鸡蛋品牌故事.html": ("free-range-eggs", "飞鸡蛋品牌故事"),
    "旱地亚麻籽品牌故事.html": ("golden-flaxseed", "旱地亚麻籽品牌故事"),
    "黄芪蜂蜜醋品牌故事.html": ("astragalus-honey-vinegar", "黄芪蜂蜜醋品牌故事"),
    "积养家社区健康臻选计划-拓客活动.html": ("community-health-event", "积养家社区健康臻选计划"),
    "积养家下午茶体验菜单.html": ("afternoon-tea-menu", "积养家下午茶体验菜单"),
    "积养家药食同源食材大全.html": ("food-medicine-ingredients", "积养家药食同源食材大全"),
    "金华古法酱油品牌故事.html": ("jinhua-soy-sauce", "金华古法酱油品牌故事"),
    "金华两头乌火腿品牌故事.html": ("jinhua-liangtouyu-ham", "金华两头乌火腿品牌故事"),
    "金华农家火腿品牌故事.html": ("jinhua-farm-ham", "金华农家火腿品牌故事"),
    "罗埠土酱油礼盒装品牌故事.html": ("luobu-soy-sauce-gift", "罗埠土酱油礼盒品牌故事"),
    "农家古法黄豆酱品牌故事.html": ("farm-soybean-paste", "农家古法黄豆酱品牌故事"),
    "沙漠一号虎坚果油品牌故事.html": ("tiger-nut-oil", "沙漠一号虎坚果油品牌故事"),
    "山西老陈醋品牌故事.html": ("shanxi-aged-vinegar", "山西老陈醋品牌故事"),
    "上珍缘宣莲品牌故事.html": ("xuan-lotus-seed", "上珍缘宣莲品牌故事"),
    "时珍太和圣坊养生茶系列.html": ("shizhen-health-tea", "时珍太和圣坊养生茶系列"),
    "塔牌黄酒品牌故事.html": ("tapai-rice-wine", "塔牌黄酒品牌故事"),
    "藤茶品牌故事.html": ("vine-tea", "藤茶品牌故事"),
    "五指岩鲜姜品牌故事.html": ("wuzhiyan-ginger", "五指岩鲜姜品牌故事"),
    "武当山野山蜂蜜品牌故事.html": ("wudang-wild-honey", "武当山野山蜂蜜品牌故事"),
    "香榧油品牌故事.html": ("torreya-oil", "香榧油品牌故事"),
    "云南文山三七片品牌故事.html": ("wenshan-notoginseng", "云南文山三七片品牌故事"),
}

SOLAR_TERMS = (
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒",
)

INGREDIENTS = (
    "生姜", "黄芪", "党参段", "三七", "茯苓", "当归", "芡实仁", "百合", "无花果", "大玫瑰",
    "铁皮石斛", "麦冬", "九蒸黄精", "老陈皮", "福建莲子", "宁夏枸杞", "山药", "桑葚", "西洋参片",
)

DAYOUGU_SKUS = (
    "福人 · 有机五常大米",
    "尚乾 · 有机五常大米",
    "十年有机小米 · 礼盒装",
    "十年有机小米 · 家庭装",
    "有机鲜食玉米",
    "有机糯玉米",
    "有机杂粮（8品种）",
    "39°有机盐田虾",
    "肉苁蓉奶粉",
    "芥花油（大桶）",
    "芥花油（双瓶）",
)

PRICE_TERMS = ("价格", "零售价", "优惠", "活动", "元/", "¥", "￥")
HEALTH_CLAIM_TERMS = ("治疗", "治愈", "疗效", "抗癌", "降血压", "降血糖", "心肌缺血", "脑缺血", "疾病")


@dataclass(frozen=True)
class Line:
    text: str
    heading: bool = False


class VisibleTextParser(HTMLParser):
    _BLOCKS = {
        "address", "article", "aside", "blockquote", "br", "div", "dl", "dt", "dd", "figcaption", "figure",
        "footer", "form", "header", "hr", "li", "main", "nav", "ol", "p", "section", "table", "tbody", "td",
        "tfoot", "th", "thead", "tr", "ul", "h1", "h2", "h3", "h4", "h5", "h6",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.lines: list[Line] = []
        self._buffer: list[str] = []
        self._skip_depth = 0
        self._heading_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in self._BLOCKS:
            self._flush()
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_depth += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "noscript"}:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return
        if tag in self._BLOCKS:
            self._flush()
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._heading_depth = max(0, self._heading_depth - 1)

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            value = " ".join(data.split())
            if value:
                self._buffer.append(value)

    def close(self) -> None:
        super().close()
        self._flush()

    def _flush(self) -> None:
        value = " ".join(self._buffer).strip()
        self._buffer.clear()
        if not value:
            return
        line = Line(value, self._heading_depth > 0)
        if not self.lines or self.lines[-1] != line:
            self.lines.append(line)


class TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "table":
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self._cell is not None and self._row is not None:
            self._row.append(" ".join(self._cell).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None and self._table is not None:
            if any(self._row):
                self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            value = " ".join(data.split())
            if value:
                self._cell.append(value)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: object) -> None:
    path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _parse_html(path: Path) -> tuple[list[Line], list[list[list[str]]]]:
    raw = path.read_text(encoding="utf-8-sig", errors="strict")
    visible = VisibleTextParser()
    visible.feed(raw)
    visible.close()
    tables = TableParser()
    tables.feed(raw)
    tables.close()
    return visible.lines, tables.tables


def _slug(value: str) -> str:
    aliases = {
        "立春": "lichun", "雨水": "yushui", "惊蛰": "jingzhe", "春分": "chunfen", "清明": "qingming", "谷雨": "guyu",
        "立夏": "lixia", "小满": "xiaoman", "芒种": "mangzhong", "夏至": "xiazhi", "小暑": "xiaoshu", "大暑": "dashu",
        "立秋": "liqiu", "处暑": "chushu", "白露": "bailu", "秋分": "qiufen", "寒露": "hanlu", "霜降": "shuangjiang",
        "立冬": "lidong", "小雪": "xiaoxue", "大雪": "daxue", "冬至": "dongzhi", "小寒": "xiaohan", "大寒": "dahan",
        "生姜": "ginger", "黄芪": "astragalus", "党参段": "codonopsis", "三七": "notoginseng", "茯苓": "poria", "当归": "angelica",
        "芡实仁": "euryale", "百合": "lily-bulb", "无花果": "fig", "大玫瑰": "rose", "铁皮石斛": "dendrobium", "麦冬": "ophiopogon",
        "九蒸黄精": "polygonatum", "老陈皮": "aged-tangerine-peel", "福建莲子": "fujian-lotus-seed", "宁夏枸杞": "ningxia-goji",
        "山药": "yam", "桑葚": "mulberry", "西洋参片": "american-ginseng",
        "福人 · 有机五常大米": "furen-wuchang-rice",
        "尚乾 · 有机五常大米": "shangqian-wuchang-rice",
        "十年有机小米 · 礼盒装": "aohan-millet-gift",
        "十年有机小米 · 家庭装": "aohan-millet-family",
        "有机鲜食玉米": "organic-fresh-corn",
        "有机糯玉米": "organic-waxy-corn",
        "有机杂粮（8品种）": "organic-mixed-grains",
        "39°有机盐田虾": "organic-salt-field-shrimp",
        "肉苁蓉奶粉": "cistanche-milk-powder",
        "芥花油（大桶）": "canola-oil-5l",
        "芥花油（双瓶）": "canola-oil-twin-pack",
    }
    if value in aliases:
        return aliases[value]
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if normalized:
        return normalized
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _document(doc_id: str, title: str, body: str) -> dict:
    text = body.strip()
    if not text or len(text) > 5000:
        raise ValueError(f"invalid text length for {doc_id}: {len(text)}")
    return {
        "id": doc_id,
        "title": title,
        "text": text,
        "status": "approved",
        "source_uri": f"knowledge://{quote(doc_id, safe='-._~')}",
    }


def _chunk_lines(lines: Iterable[Line]) -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    current: list[str] = []
    headings: list[str] = []
    size = 0
    for line in lines:
        value = line.text
        projected = size + len(value) + (1 if current else 0)
        if current and projected > MAX_CHUNK_CHARS and size >= MIN_CHUNK_CHARS:
            chunks.append((" / ".join(headings[-3:]) or "正文", "\n".join(current)))
            current = []
            headings = []
            size = 0
        current.append(value)
        size += len(value) + 1
        if line.heading and value not in headings:
            headings.append(value)
    if current:
        chunks.append((" / ".join(headings[-3:]) or "正文", "\n".join(current)))
    return chunks


def _span(lines: list[Line], labels: tuple[str, ...], index: int) -> str:
    start_label = labels[index]
    start = next((i for i, line in enumerate(lines) if line.text == start_label), None)
    if start is None:
        raise ValueError(f"source item not found: {start_label}")
    end = len(lines)
    if index + 1 < len(labels):
        next_label = labels[index + 1]
        end = next((i for i in range(start + 1, len(lines)) if lines[i].text == next_label), len(lines))
    selected = [line.text for line in lines[start:end]]
    while selected and not re.search(r"[\w\u3400-\u9fff]", selected[-1]):
        selected.pop()
    return "\n".join(selected).strip()


def _questions(
    name: str,
    category: str,
    expected: list[str],
    *,
    source_file: str | None = None,
    match_terms: tuple[str, ...] | None = None,
) -> list[dict]:
    templates = (
        f"{name}是什么？",
        f"请详细讲讲{name}。",
        f"{name}有什么特点？",
    )
    cases = []
    for index, question in enumerate(templates, 1):
        case = {"id": f"{category}-{_slug(name)}-{index:02d}", "question": question, "category": category, "expected_any": expected}
        case["match_terms"] = list(match_terms or (name,))
        if source_file:
            case["source_file"] = source_file
        cases.append(case)
    return cases


def build(source_dir: Path, legacy_path: Path, output_dir: Path) -> dict:
    missing = sorted(set(SOURCE_FILES) - {path.name for path in source_dir.glob("*.html")})
    extras = sorted({path.name for path in source_dir.glob("*.html")} - set(SOURCE_FILES))
    if missing or extras:
        raise ValueError(f"source inventory mismatch; missing={missing}, extras={extras}")

    source_output = output_dir / "sources" / "aiye-foods"
    source_output.mkdir(parents=True, exist_ok=True)
    for stale in source_output.iterdir():
        if stale.is_file() and stale.suffix.lower() != ".html":
            raise ValueError(f"unexpected non-HTML file in public source directory: {stale.name}")

    source_records: list[dict] = []
    parsed: dict[str, tuple[list[Line], list[list[list[str]]]]] = {}
    for filename, (slug, title) in SOURCE_FILES.items():
        source = source_dir / filename
        target = source_output / filename
        if source.resolve() != target.resolve():
            shutil.copy2(source, target)
        if source.read_bytes() != target.read_bytes():
            raise ValueError(f"source copy mismatch: {filename}")
        parsed[filename] = _parse_html(target)
        source_records.append({
            "name": filename,
            "title": title,
            "slug": slug,
            "bytes": target.stat().st_size,
            "sha256": _sha256(target),
            "path": f"sources/aiye-foods/{filename}",
        })

    legacy_payload = _read_json(legacy_path)
    legacy_documents = legacy_payload.get("documents")
    if not isinstance(legacy_documents, list) or len(legacy_documents) != 65:
        raise ValueError("v2.1 legacy package must contain exactly 65 documents")

    new_documents: list[dict] = []
    source_map: dict[str, dict] = {}
    cases: list[dict] = []

    for filename, (slug, title) in SOURCE_FILES.items():
        lines, _tables = parsed[filename]
        chunk_ids: list[str] = []
        for index, (section, body) in enumerate(_chunk_lines(lines), 1):
            doc_id = f"aiye_{slug}_story_{index:02d}"
            aliases = f"{title}\n{title}是什么\n请详细讲讲{title}\n"
            new_documents.append(_document(doc_id, f"{title}（第{index}部分）", aliases + body))
            chunk_ids.append(doc_id)
            source_map[doc_id] = {
                "source_file": f"sources/aiye-foods/{filename}",
                "source_sha256": _sha256(output_dir / "sources" / "aiye-foods" / filename),
                "section": section,
                "kind": "source_story_chunk",
            }
        cases.extend(_questions(title, "source-story", chunk_ids, source_file=f"sources/aiye-foods/{filename}"))

    tea_file = "24节气养生茶速查表.html"
    tea_lines, _ = parsed[tea_file]
    for index, name in enumerate(SOLAR_TERMS):
        doc_id = f"aiye_solar_term_{_slug(name)}"
        body = _span(tea_lines, SOLAR_TERMS, index)
        new_documents.append(_document(doc_id, f"24节气养生茶：{name}", f"{name}喝什么茶\n{name}养生茶配方\n{name}节气怎么喝\n{body}"))
        source_map[doc_id] = {
            "source_file": f"sources/aiye-foods/{tea_file}",
            "source_sha256": _sha256(output_dir / "sources" / "aiye-foods" / tea_file),
            "section": name,
            "kind": "solar_term_recipe",
        }
        cases.extend(_questions(f"{name}养生茶", "solar-term", [doc_id], match_terms=(name,)))

    ingredient_file = "积养家药食同源食材大全.html"
    ingredient_lines, _ = parsed[ingredient_file]
    for index, name in enumerate(INGREDIENTS):
        doc_id = f"aiye_ingredient_{_slug(name)}"
        body = _span(ingredient_lines, INGREDIENTS, index)
        if index == len(INGREDIENTS) - 1:
            marker = body.find("积养家 · 选品哲学")
            if marker >= 0:
                body = body[:marker].rstrip()
        new_documents.append(
            _document(
                doc_id,
                f"药食同源食材：{name}",
                f"{name}是什么\n请详细讲讲{name}\n{name}怎么吃\n{name}有什么特点\n{body}",
            )
        )
        source_map[doc_id] = {
            "source_file": f"sources/aiye-foods/{ingredient_file}",
            "source_sha256": _sha256(output_dir / "sources" / "aiye-foods" / ingredient_file),
            "section": name,
            "kind": "food_medicine_ingredient",
        }
        cases.extend(_questions(name, "ingredient", [doc_id]))

    dayougu_file = "大有谷合作产品手册.html"
    _dayougu_lines, dayougu_tables = parsed[dayougu_file]
    catalog_table = next((table for table in dayougu_tables if table and table[0][:2] == ["品类", "产品名称"]), None)
    if catalog_table is None:
        raise ValueError("大有谷产品总览表未找到")
    rows_by_name = {row[1]: row for row in catalog_table[1:] if len(row) >= 5}
    catalog_id = "aiye_dayougu_catalog"
    catalog_lines = ["大有谷有哪些产品", "大有谷产品目录", "请介绍大有谷全线产品"]
    catalog_lines.extend(
        f"{row[0]}：{row[1]}；规格：{row[2]}；零售价：{row[3]}；发货地：{row[4]}"
        for name in DAYOUGU_SKUS
        for row in [rows_by_name.get(name)]
        if row is not None
    )
    new_documents.append(_document(catalog_id, "大有谷产品目录", "\n".join(catalog_lines)))
    source_map[catalog_id] = {
        "source_file": f"sources/aiye-foods/{dayougu_file}",
        "source_sha256": _sha256(output_dir / "sources" / "aiye-foods" / dayougu_file),
        "section": "全线总览",
        "kind": "dayougu_catalog",
    }
    cases.extend(_questions("大有谷产品目录", "dayougu-catalog", [catalog_id], match_terms=("大有谷",)))
    for name in DAYOUGU_SKUS:
        row = rows_by_name.get(name)
        if row is None:
            raise ValueError(f"大有谷 SKU 未找到: {name}")
        doc_id = f"aiye_dayougu_{_slug(name)}"
        body = "\n".join((f"产品名称：{row[1]}", f"品类：{row[0]}", f"规格：{row[2]}", f"零售价：{row[3]}", f"发货地：{row[4]}"))
        new_documents.append(
            _document(
                doc_id,
                f"大有谷产品：{name}",
                f"{name}是什么\n请详细讲讲{name}\n{name}有什么特点\n{name}多少钱\n{name}什么规格\n{name}从哪里发货\n{body}",
            )
        )
        source_map[doc_id] = {
            "source_file": f"sources/aiye-foods/{dayougu_file}",
            "source_sha256": _sha256(output_dir / "sources" / "aiye-foods" / dayougu_file),
            "section": f"全线总览 / {name}",
            "kind": "dayougu_sku",
        }
        cases.extend(_questions(name, "dayougu-sku", [doc_id]))

    new_ids = [item["id"] for item in new_documents]
    if len(new_ids) != len(set(new_ids)):
        raise ValueError("duplicate new document ids")
    legacy_ids = [str(item["id"]) for item in legacy_documents]
    if set(new_ids) & set(legacy_ids):
        raise ValueError("new document ids overlap v2.1")

    legacy_sha = _sha256(legacy_path)
    for item in legacy_documents:
        source_map[item["id"]] = {
            "source_file": "../v2.1/import_all.json",
            "source_sha256": legacy_sha,
            "section": item["title"],
            "kind": "legacy_v2.1",
        }

    for case in cases:
        source_file = case.get("source_file")
        if source_file:
            case["expected_any"] = sorted(doc_id for doc_id, mapping in source_map.items() if mapping["source_file"] == source_file)
            continue
        match_terms = [str(term) for term in case.get("match_terms") or []]
        matching_ids = []
        for item in new_documents:
            haystack = f"{item['title']}\n{item['text']}"
            if any(term in haystack for term in match_terms):
                matching_ids.append(item["id"])
        if matching_ids:
            case["expected_any"] = sorted(matching_ids)

    all_documents = legacy_documents + new_documents
    output_dir.mkdir(parents=True, exist_ok=True)
    for stale in output_dir.glob("import_batch_*.json"):
        stale.unlink()

    all_payload = {"version": VERSION, "status": "approved_with_legacy_statuses", "documents": all_documents}
    _write_json(output_dir / "import_all.json", all_payload)

    batch_records: list[dict] = []
    for number, offset in enumerate(range(0, len(all_documents), BATCH_SIZE), 1):
        name = f"import_batch_{number:02d}.json"
        batch_documents = all_documents[offset : offset + BATCH_SIZE]
        batch_payload = {"version": VERSION, "status": "approved_with_legacy_statuses", "documents": batch_documents}
        target = output_dir / name
        _write_json(target, batch_payload)
        batch_records.append({
            "name": name,
            "documents": len(batch_documents),
            "statuses": dict(sorted(Counter(item["status"] for item in batch_documents).items())),
            "sha256": _sha256(target),
        })

    _write_json(output_dir / "source-map.json", {"version": VERSION, "documents": source_map})
    _write_json(output_dir / "test_questions.json", {"version": VERSION, "cases": cases})
    catalog = {
        "version": VERSION,
        "source_pages": [{"name": item["name"], "title": item["title"], "slug": item["slug"]} for item in source_records],
        "coverage": {
            "source_pages": len(source_records),
            "solar_terms": list(SOLAR_TERMS),
            "food_medicine_ingredients": list(INGREDIENTS),
            "dayougu_skus": list(DAYOUGU_SKUS),
        },
    }
    _write_json(output_dir / "catalog.json", catalog)

    claim_audit = {
        "version": VERSION,
        "review_basis": "User confirmed all source materials were human-reviewed and approved for public/customer use.",
        "fidelity_policy": "Knowledge text is extracted from the archived HTML. No external facts are added by the builder.",
        "runtime_policy": "The LLM may summarize retrieved approved text but must not invent medical efficacy, diagnosis, price, inventory or activity facts.",
        "independent_external_fact_check": False,
        "pages": [],
    }
    for item in source_records:
        text = "\n".join(line.text for line in parsed[item["name"]][0])
        claim_audit["pages"].append({
            "name": item["name"],
            "sha256": item["sha256"],
            "price_terms": [term for term in PRICE_TERMS if term in text],
            "health_claim_terms": [term for term in HEALTH_CLAIM_TERMS if term in text],
            "status": "approved_by_user",
        })
    _write_json(output_dir / "claim-audit.json", claim_audit)

    manifest = {
        "schema_version": 2,
        "package": "jiyangjia-digital-human-knowledge-v2.2",
        "version": VERSION,
        "source_authorization": "user_confirmed_public_and_human_approved",
        "source_policy": "source-derived-only; no external factual enrichment",
        "documents": len(all_documents),
        "legacy_documents": len(legacy_documents),
        "new_documents": len(new_documents),
        "statuses": dict(sorted(Counter(item["status"] for item in all_documents).items())),
        "new_statuses": dict(sorted(Counter(item["status"] for item in new_documents).items())),
        "coverage": {
            "source_pages": len(source_records),
            "solar_terms": len(SOLAR_TERMS),
            "food_medicine_ingredients": len(INGREDIENTS),
            "dayougu_skus": len(DAYOUGU_SKUS),
            "test_questions": len(cases),
        },
        "source_uri_policy": "knowledge://<document_id>",
        "batch_size": BATCH_SIZE,
        "source_files": source_records,
        "files": [
            {"name": "import_all.json", "documents": len(all_documents), "sha256": _sha256(output_dir / "import_all.json")},
            *batch_records,
            {"name": "source-map.json", "sha256": _sha256(output_dir / "source-map.json")},
            {"name": "catalog.json", "sha256": _sha256(output_dir / "catalog.json")},
            {"name": "test_questions.json", "sha256": _sha256(output_dir / "test_questions.json")},
            {"name": "claim-audit.json", "sha256": _sha256(output_dir / "claim-audit.json")},
        ],
    }
    _write_json(output_dir / "manifest.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public Aiye/Jiyangjia v2.2 knowledge release from authorized HTML sources.")
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--legacy-package", type=Path, default=Path("knowledge-public/v2.1/import_all.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("knowledge-public/v2.2"))
    args = parser.parse_args()
    manifest = build(args.source_dir, args.legacy_package, args.output_dir)
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
