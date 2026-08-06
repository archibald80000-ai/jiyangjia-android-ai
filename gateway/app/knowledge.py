from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from typing import Iterable


VALID_STATUSES = {"approved", "draft", "rejected"}


@dataclass(frozen=True)
class KnowledgeDocument:
    doc_id: str
    title: str
    text: str
    status: str
    source_uri: str | None = None


class SQLiteKnowledgeStore:
    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_documents (
                doc_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                text TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('approved', 'draft', 'rejected')),
                source_uri TEXT,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._conn.commit()

    def upsert_many(self, documents: Iterable[KnowledgeDocument]) -> int:
        count = 0
        for doc in documents:
            if doc.status not in VALID_STATUSES:
                raise ValueError(f"invalid knowledge status: {doc.status}")
            self._conn.execute(
                """
                INSERT INTO knowledge_documents(doc_id, title, text, status, source_uri)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(doc_id) DO UPDATE SET
                    title=excluded.title,
                    text=excluded.text,
                    status=excluded.status,
                    source_uri=excluded.source_uri,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (doc.doc_id, doc.title, doc.text, doc.status, doc.source_uri),
            )
            count += 1
        self._conn.commit()
        return count

    def status(self) -> dict[str, int]:
        rows = self._conn.execute(
            "SELECT status, COUNT(*) AS count FROM knowledge_documents GROUP BY status"
        ).fetchall()
        result = {"approved": 0, "draft": 0, "rejected": 0}
        result.update({row["status"]: int(row["count"]) for row in rows})
        return result

    def search(self, query: str, top_k: int = 3, include_draft: bool = False) -> list[dict[str, object]]:
        tokens = _tokens(query)
        if not tokens:
            return []
        allowed = ("approved", "draft") if include_draft else ("approved",)
        placeholders = ",".join("?" for _ in allowed)
        rows = self._conn.execute(
            f"SELECT * FROM knowledge_documents WHERE status IN ({placeholders})",
            allowed,
        ).fetchall()
        scored: list[dict[str, object]] = []
        for row in rows:
            haystack = f"{row['title']} {row['text']}".lower()
            score = sum(1 for token in tokens if token in haystack)
            if score:
                scored.append(
                    {
                        "id": row["doc_id"],
                        "title": row["title"],
                        "status": row["status"],
                        "score": score,
                        "confidence": min(0.99, 0.45 + score * 0.15),
                        "source": {"uri": row["source_uri"] or "manual"},
                        "excerpt": row["text"][:160],
                    }
                )
        scored.sort(key=lambda item: (-float(item["confidence"]), str(item["id"])))
        return scored[:top_k]


def _tokens(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    if not normalized:
        return []
    ascii_tokens = re.findall(r"[a-z0-9_]+", normalized)
    chinese_chunks = re.findall(r"[\u4e00-\u9fff]{2,}", normalized)
    bigrams: list[str] = []
    for chunk in chinese_chunks:
        bigrams.extend(chunk[i : i + 2] for i in range(max(0, len(chunk) - 1)))
    return list(dict.fromkeys(ascii_tokens + chinese_chunks + bigrams))
