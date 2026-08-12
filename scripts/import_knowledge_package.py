from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path


def _request_json(url: str, *, payload: dict | None = None, timeout: float = 180.0) -> dict:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    if not isinstance(body, dict):
        raise ValueError(f"expected an object from {url}")
    return body


def import_package(package_dir: Path, base_url: str) -> dict[str, object]:
    manifest = json.loads((package_dir / "manifest.json").read_text(encoding="utf-8-sig"))
    batches = manifest.get("batches")
    if not isinstance(batches, list) or not batches:
        raise ValueError("manifest requires batches[]")
    results = []
    for name in batches:
        payload = json.loads((package_dir / str(name)).read_text(encoding="utf-8-sig"))
        response = _request_json(f"{base_url.rstrip('/')}/api/v1/knowledge/index", payload=payload)
        results.append(
            {
                "batch": name,
                "request_id": response.get("request_id"),
                "indexed": response.get("indexed"),
                "chunks": response.get("chunks"),
            }
        )
    status = _request_json(f"{base_url.rstrip('/')}/api/v1/knowledge/status")
    return {"version": manifest.get("version"), "batches": results, "status": status}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8080")
    args = parser.parse_args()
    result = import_package(args.package_dir, args.base_url)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
