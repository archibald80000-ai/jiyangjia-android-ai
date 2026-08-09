from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from urllib.parse import quote


PACKAGE_FILES = ("import_all.json", "import_batch_01.json", "import_batch_02.json")
VALID_STATUSES = {"approved", "draft", "rejected"}


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict) or not isinstance(payload.get("documents"), list):
        raise ValueError(f"invalid knowledge package: {path}")
    return payload


def _public_document(document: dict) -> dict:
    required = {"id", "title", "text", "status", "source_uri"}
    missing = sorted(required - document.keys())
    if missing:
        raise ValueError(f"document is missing fields: {', '.join(missing)}")
    doc_id = str(document["id"]).strip()
    status = str(document["status"]).strip()
    if not doc_id or status not in VALID_STATUSES:
        raise ValueError(f"invalid document id/status: {doc_id!r}/{status!r}")
    return {
        **document,
        "source_uri": f"knowledge://{quote(doc_id, safe='-._~')}",
    }


def _canonical(document: dict) -> str:
    return json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_package(source_dir: Path, output_dir: Path) -> dict:
    source_payloads = {name: _load(source_dir / name) for name in PACKAGE_FILES}
    public_payloads: dict[str, dict] = {}

    for name, payload in source_payloads.items():
        documents = [_public_document(item) for item in payload["documents"]]
        ids = [item["id"] for item in documents]
        if len(ids) != len(set(ids)):
            raise ValueError(f"duplicate document ids in {name}")
        public_payloads[name] = {**payload, "documents": documents}

    all_documents = public_payloads["import_all.json"]["documents"]
    batch_documents = (
        public_payloads["import_batch_01.json"]["documents"]
        + public_payloads["import_batch_02.json"]["documents"]
    )
    if sorted(map(_canonical, all_documents)) != sorted(map(_canonical, batch_documents)):
        raise ValueError("batch union does not equal import_all.json")

    output_dir.mkdir(parents=True, exist_ok=True)
    file_records = []
    for name in PACKAGE_FILES:
        target = output_dir / name
        target.write_bytes((json.dumps(public_payloads[name], ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        content = target.read_bytes()
        statuses = Counter(item["status"] for item in public_payloads[name]["documents"])
        file_records.append(
            {
                "name": name,
                "documents": len(public_payloads[name]["documents"]),
                "statuses": dict(sorted(statuses.items())),
                "sha256": hashlib.sha256(content).hexdigest().upper(),
            }
        )

    all_statuses = Counter(item["status"] for item in all_documents)
    manifest = {
        "schema_version": 1,
        "package": "jiyangjia-digital-human-knowledge-v2.1",
        "source_authorization": "public_marketing_and_employee_learning",
        "documents": len(all_documents),
        "statuses": dict(sorted(all_statuses.items())),
        "source_uri_policy": "knowledge://<document_id>",
        "files": file_records,
    }
    (output_dir / "manifest.json").write_bytes(
        (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the public Jiyangjia knowledge import package.")
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("knowledge-public/v2.1"))
    args = parser.parse_args()
    manifest = build_package(args.source_dir, args.output_dir)
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
