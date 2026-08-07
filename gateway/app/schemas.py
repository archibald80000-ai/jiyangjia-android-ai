from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


KnowledgeStatus = Literal["approved", "draft", "rejected"]


class DialogueTextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    session_id: str | None = None
    request_id: str | None = None


class DialogueResponse(BaseModel):
    request_id: str
    session_id: str
    transcript: dict[str, Any]
    knowledge: dict[str, Any]
    answer: dict[str, Any]
    tts: dict[str, Any]
    sources: list[dict[str, Any]]


class KnowledgeDocumentPayload(BaseModel):
    id: str = Field(min_length=1, max_length=120)
    title: str = Field(min_length=1, max_length=200)
    text: str = Field(min_length=1, max_length=5000)
    status: KnowledgeStatus
    source_uri: str | None = Field(default=None, max_length=500)


class KnowledgeIndexRequest(BaseModel):
    documents: list[KnowledgeDocumentPayload] = Field(default_factory=list, max_length=50)


class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=3, ge=1, le=10)
    include_draft: Literal[False] = False
    request_id: str | None = None
