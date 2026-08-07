from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import uuid
from pathlib import Path
from typing import Any


DEFAULT_DISPLAY_PROFILE_ID = "display-1080x1920"
DISPLAY_DEFAULT_MIGRATION_ID = "20260807_default_display_9_16"

DISPLAY_PRESETS = (
    (DEFAULT_DISPLAY_PROFILE_ID, "竖屏 1080x1920", 1080, 1920, "portrait"),
    ("display-1920x1080", "横屏 1920x1080", 1920, 1080, "landscape"),
    ("display-3840x2160", "横屏 3840x2160", 3840, 2160, "landscape"),
    ("display-1280x720", "横屏 1280x720", 1280, 720, "landscape"),
)


class AdminContentStore:
    def __init__(self, db_path: str, *, upload_dir: str, asset_dir: str) -> None:
        path = Path(db_path)
        if db_path != ":memory:":
            path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self.upload_dir = Path(upload_dir)
        self.asset_dir = Path(asset_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self._init_schema()
        self._seed_display_profiles()
        self._migrate_default_display_profile()

    def _init_schema(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS knowledge_upload_runs (
                run_id TEXT PRIMARY KEY,
                document_uri TEXT NOT NULL,
                document_title TEXT NOT NULL,
                source_type TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('draft','parsed','preview','approved','rejected','published','failed')),
                chunk_count INTEGER NOT NULL DEFAULT 0,
                vector_count INTEGER NOT NULL DEFAULT 0,
                documents_json TEXT NOT NULL DEFAULT '[]',
                error_message TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS avatar_assets (
                avatar_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                asset_type TEXT NOT NULL CHECK(asset_type IN ('video','image')),
                uri TEXT NOT NULL,
                file_path TEXT NOT NULL,
                content_type TEXT NOT NULL,
                sha256 TEXT NOT NULL,
                size_bytes INTEGER NOT NULL DEFAULT 0,
                version TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('draft','preview','approved','published','rejected')),
                source TEXT NOT NULL DEFAULT 'manual_upload',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS display_profiles (
                profile_id TEXT PRIMARY KEY,
                profile_name TEXT NOT NULL,
                width_px INTEGER NOT NULL,
                height_px INTEGER NOT NULL,
                orientation TEXT NOT NULL CHECK(orientation IN ('landscape','portrait')),
                scale_mode TEXT NOT NULL CHECK(scale_mode IN ('fit','fill','crop')),
                character_anchor_x REAL NOT NULL,
                character_anchor_y REAL NOT NULL,
                character_scale REAL NOT NULL,
                subtitle_safe_area_json TEXT NOT NULL,
                subtitle_font_px INTEGER NOT NULL,
                button_positions_json TEXT NOT NULL,
                avatar_id TEXT,
                background_id TEXT,
                is_default INTEGER NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('draft','active','archived')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS admin_migrations (
                migration_id TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        columns = {row[1] for row in self._conn.execute("PRAGMA table_info(avatar_assets)").fetchall()}
        if "size_bytes" not in columns:
            self._conn.execute("ALTER TABLE avatar_assets ADD COLUMN size_bytes INTEGER NOT NULL DEFAULT 0")
        self._conn.commit()
        self._backfill_asset_sizes()

    def _backfill_asset_sizes(self) -> None:
        rows = self._conn.execute("SELECT avatar_id, file_path, size_bytes FROM avatar_assets").fetchall()
        for row in rows:
            if int(row["size_bytes"] or 0) > 0:
                continue
            path = Path(str(row["file_path"]))
            if path.is_file():
                self._conn.execute(
                    "UPDATE avatar_assets SET size_bytes = ? WHERE avatar_id = ?",
                    (path.stat().st_size, row["avatar_id"]),
                )
        self._conn.commit()

    def _seed_display_profiles(self) -> None:
        for profile_id, name, width, height, orientation in DISPLAY_PRESETS:
            self._conn.execute(
                """
                INSERT OR IGNORE INTO display_profiles(
                    profile_id, profile_name, width_px, height_px, orientation,
                    scale_mode, character_anchor_x, character_anchor_y,
                    character_scale, subtitle_safe_area_json, subtitle_font_px,
                    button_positions_json, is_default, status
                ) VALUES (?, ?, ?, ?, ?, 'fit', 0.5, 0.5, 1.0, ?, ?, ?, ?, 'active')
                """,
                (
                    profile_id,
                    name,
                    width,
                    height,
                    orientation,
                    json.dumps({"left": 0.08, "right": 0.08, "bottom": 0.08}, separators=(",", ":")),
                    52 if width >= 1920 else 36,
                    json.dumps({"consult": {"x": 0.5, "y": 0.88}}, separators=(",", ":")),
                    1 if profile_id == DEFAULT_DISPLAY_PROFILE_ID else 0,
                ),
            )
        self._conn.commit()

    def _migrate_default_display_profile(self) -> None:
        with self._conn:
            inserted = self._conn.execute(
                "INSERT OR IGNORE INTO admin_migrations(migration_id) VALUES (?)",
                (DISPLAY_DEFAULT_MIGRATION_ID,),
            )
            if inserted.rowcount == 0:
                return
            self._conn.execute(
                "UPDATE display_profiles SET is_default = CASE WHEN profile_id = ? THEN 1 ELSE 0 END",
                (DEFAULT_DISPLAY_PROFILE_ID,),
            )

    def create_knowledge_run(self, filename: str, content: bytes, documents: list[dict[str, Any]], chunk_count: int) -> dict[str, Any]:
        run_id = f"ku_{uuid.uuid4().hex[:16]}"
        safe_name = _safe_filename(filename)
        target = self.upload_dir / f"{run_id}_{safe_name}"
        target.write_bytes(content)
        source_type = target.suffix.lower().lstrip(".")
        public_uri = f"admin://knowledge/{run_id}/{safe_name}"
        normalized_documents = []
        for index, item in enumerate(documents):
            normalized_documents.append(
                {
                    **item,
                    "doc_id": f"{run_id}_{index:03d}",
                    "status": "draft",
                    "source_uri": public_uri,
                    "source_type": source_type,
                }
            )
        self._conn.execute(
            """
            INSERT INTO knowledge_upload_runs(
                run_id, document_uri, document_title, source_type, status,
                chunk_count, documents_json
            ) VALUES (?, ?, ?, ?, 'parsed', ?, ?)
            """,
            (run_id, public_uri, safe_name, source_type, chunk_count, json.dumps(normalized_documents, ensure_ascii=False)),
        )
        self._conn.commit()
        return self.get_knowledge_run(run_id) or {}

    def list_knowledge_runs(self, limit: int = 100) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            """SELECT run_id, document_uri, document_title, source_type, status,
                      chunk_count, vector_count, error_message, created_at, updated_at
               FROM knowledge_upload_runs ORDER BY created_at DESC LIMIT ?""",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def get_knowledge_run(self, run_id: str, *, include_documents: bool = True) -> dict[str, Any] | None:
        row = self._conn.execute("SELECT * FROM knowledge_upload_runs WHERE run_id = ?", (run_id,)).fetchone()
        if not row:
            return None
        payload = dict(row)
        documents = json.loads(payload.pop("documents_json"))
        if include_documents:
            payload["documents"] = documents
        return payload

    def update_knowledge_run(self, run_id: str, status: str, *, vector_count: int | None = None, error_message: str | None = None) -> dict[str, Any] | None:
        self._conn.execute(
            """
            UPDATE knowledge_upload_runs
            SET status = ?, vector_count = COALESCE(?, vector_count),
                error_message = ?, updated_at = CURRENT_TIMESTAMP
            WHERE run_id = ?
            """,
            (status, vector_count, error_message, run_id),
        )
        self._conn.commit()
        return self.get_knowledge_run(run_id)

    def add_asset(self, *, filename: str, content: bytes, name: str, version: str, asset_type: str, content_type: str) -> dict[str, Any]:
        avatar_id = f"asset_{uuid.uuid4().hex[:16]}"
        safe_name = _safe_filename(filename)
        target = self.asset_dir / f"{avatar_id}_{safe_name}"
        target.write_bytes(content)
        uri = f"/api/v1/assets/{avatar_id}"
        self._conn.execute(
            """
            INSERT INTO avatar_assets(
                avatar_id, name, asset_type, uri, file_path, content_type,
                sha256, size_bytes, version, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'draft')
            """,
            (
                avatar_id,
                name,
                asset_type,
                uri,
                str(target),
                content_type,
                hashlib.sha256(content).hexdigest().upper(),
                len(content),
                version,
            ),
        )
        self._conn.commit()
        return self.get_asset(avatar_id) or {}

    def list_assets(self) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            """SELECT avatar_id, name, asset_type, uri, content_type, sha256, size_bytes,
                      version, status, source, created_at, updated_at
               FROM avatar_assets ORDER BY created_at DESC"""
        ).fetchall()
        return [dict(row) for row in rows]

    def get_asset(self, avatar_id: str, *, include_path: bool = False) -> dict[str, Any] | None:
        row = self._conn.execute("SELECT * FROM avatar_assets WHERE avatar_id = ?", (avatar_id,)).fetchone()
        if not row:
            return None
        payload = dict(row)
        if not include_path:
            payload.pop("file_path", None)
        return payload

    def publish_asset(self, avatar_id: str) -> dict[str, Any] | None:
        asset = self.get_asset(avatar_id, include_path=True)
        if not asset:
            return None
        self._conn.execute(
            "UPDATE avatar_assets SET status = 'approved', updated_at = CURRENT_TIMESTAMP WHERE asset_type = ? AND status = 'published'",
            (asset["asset_type"],),
        )
        self._conn.execute(
            "UPDATE avatar_assets SET status = 'published', updated_at = CURRENT_TIMESTAMP WHERE avatar_id = ?",
            (avatar_id,),
        )
        self._conn.commit()
        self.write_manifest()
        return self.get_asset(avatar_id)

    def delete_asset(self, avatar_id: str) -> bool:
        asset = self.get_asset(avatar_id, include_path=True)
        if not asset or asset["status"] == "published":
            return False
        self._conn.execute("DELETE FROM avatar_assets WHERE avatar_id = ?", (avatar_id,))
        self._conn.commit()
        Path(str(asset["file_path"])).unlink(missing_ok=True)
        return True

    def manifest(self) -> dict[str, Any]:
        rows = self._conn.execute(
            """SELECT avatar_id, name, asset_type, uri, content_type, sha256, size_bytes,
                      version, updated_at
               FROM avatar_assets WHERE status = 'published' ORDER BY asset_type"""
        ).fetchall()
        assets = {}
        for row in rows:
            item = dict(row)
            item["url"] = item.pop("uri")
            assets[row["asset_type"]] = item
        return {"mode": "composite_video", "video": assets.get("video"), "background": assets.get("image")}

    def write_manifest(self) -> None:
        target = self.asset_dir / "manifest.json"
        target.write_text(json.dumps(self.manifest(), ensure_ascii=False, indent=2), encoding="utf-8")

    def list_display_profiles(self) -> list[dict[str, Any]]:
        rows = self._conn.execute("SELECT * FROM display_profiles ORDER BY is_default DESC, width_px DESC, profile_id").fetchall()
        return [_display_row(row) for row in rows]

    def get_display_profile(self, profile_id: str) -> dict[str, Any] | None:
        row = self._conn.execute("SELECT * FROM display_profiles WHERE profile_id = ?", (profile_id,)).fetchone()
        return _display_row(row) if row else None

    def default_display_profile(self) -> dict[str, Any] | None:
        row = self._conn.execute(
            "SELECT * FROM display_profiles WHERE is_default = 1 AND status = 'active' LIMIT 1"
        ).fetchone()
        return _display_row(row) if row else None

    def save_display_profile(self, payload: dict[str, Any], *, profile_id: str | None = None) -> dict[str, Any]:
        profile_id = profile_id or f"display_{uuid.uuid4().hex[:16]}"
        values = (
            profile_id,
            payload["profile_name"],
            payload["width_px"],
            payload["height_px"],
            payload["orientation"],
            payload["scale_mode"],
            payload["character_anchor_x"],
            payload["character_anchor_y"],
            payload["character_scale"],
            json.dumps(payload["subtitle_safe_area"], separators=(",", ":")),
            payload["subtitle_font_px"],
            json.dumps(payload["button_positions"], separators=(",", ":")),
            payload.get("avatar_id"),
            payload.get("background_id"),
            payload.get("status", "active"),
        )
        self._conn.execute(
            """
            INSERT INTO display_profiles(
                profile_id, profile_name, width_px, height_px, orientation,
                scale_mode, character_anchor_x, character_anchor_y,
                character_scale, subtitle_safe_area_json, subtitle_font_px,
                button_positions_json, avatar_id, background_id, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(profile_id) DO UPDATE SET
                profile_name=excluded.profile_name, width_px=excluded.width_px,
                height_px=excluded.height_px, orientation=excluded.orientation,
                scale_mode=excluded.scale_mode,
                character_anchor_x=excluded.character_anchor_x,
                character_anchor_y=excluded.character_anchor_y,
                character_scale=excluded.character_scale,
                subtitle_safe_area_json=excluded.subtitle_safe_area_json,
                subtitle_font_px=excluded.subtitle_font_px,
                button_positions_json=excluded.button_positions_json,
                avatar_id=excluded.avatar_id, background_id=excluded.background_id,
                status=excluded.status, updated_at=CURRENT_TIMESTAMP
            """,
            values,
        )
        self._conn.commit()
        return self.get_display_profile(profile_id) or {}

    def set_default_profile(self, profile_id: str) -> dict[str, Any] | None:
        if not self.get_display_profile(profile_id):
            return None
        self._conn.execute("UPDATE display_profiles SET is_default = 0")
        self._conn.execute(
            "UPDATE display_profiles SET is_default = 1, status = 'active', updated_at = CURRENT_TIMESTAMP WHERE profile_id = ?",
            (profile_id,),
        )
        self._conn.commit()
        return self.get_display_profile(profile_id)

    def match_display_profile(self, width: int, height: int, orientation: str | None = None) -> dict[str, Any] | None:
        resolved_orientation = orientation or ("landscape" if width >= height else "portrait")
        row = self._conn.execute(
            """SELECT * FROM display_profiles
               WHERE width_px = ? AND height_px = ? AND orientation = ? AND status = 'active'
               ORDER BY is_default DESC LIMIT 1""",
            (width, height, resolved_orientation),
        ).fetchone()
        if not row:
            row = self._conn.execute(
                """SELECT * FROM display_profiles WHERE orientation = ? AND status = 'active'
                   ORDER BY ABS(width_px - ?) + ABS(height_px - ?), is_default DESC LIMIT 1""",
                (resolved_orientation, width, height),
            ).fetchone()
        if not row:
            row = self._conn.execute("SELECT * FROM display_profiles WHERE is_default = 1 LIMIT 1").fetchone()
        return _display_row(row) if row else None

    def counts(self) -> dict[str, int]:
        return {
            "knowledge_runs": int(self._conn.execute("SELECT COUNT(*) FROM knowledge_upload_runs").fetchone()[0]),
            "assets": int(self._conn.execute("SELECT COUNT(*) FROM avatar_assets").fetchone()[0]),
            "display_profiles": int(self._conn.execute("SELECT COUNT(*) FROM display_profiles").fetchone()[0]),
        }


def _safe_filename(value: str) -> str:
    name = Path(value).name
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return cleaned[:120] or "upload.bin"


def _display_row(row: sqlite3.Row) -> dict[str, Any]:
    payload = dict(row)
    payload["is_default"] = bool(payload["is_default"])
    payload["subtitle_safe_area"] = json.loads(payload.pop("subtitle_safe_area_json"))
    payload["button_positions"] = json.loads(payload.pop("button_positions_json"))
    return payload
