from __future__ import annotations

import hmac
import tempfile
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any, Callable, Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from .admin_store import AdminContentStore
from .admin_ui import admin_page
from .config import Settings
from .knowledge import KnowledgeDocument, SQLiteKnowledgeStore, chunk_text, parse_selected_knowledge_path


KNOWLEDGE_EXTENSIONS = {".pdf", ".docx", ".md", ".txt"}
ASSET_TYPES = {
    ".mp4": ("video", "video/mp4"),
    ".jpg": ("image", "image/jpeg"),
    ".jpeg": ("image", "image/jpeg"),
    ".png": ("image", "image/png"),
}


class DisplayProfilePayload(BaseModel):
    profile_name: str = Field(min_length=1, max_length=100)
    width_px: int = Field(ge=320, le=7680)
    height_px: int = Field(ge=320, le=7680)
    orientation: Literal["landscape", "portrait"]
    scale_mode: Literal["fit", "fill", "crop"] = "fit"
    character_anchor_x: float = Field(default=0.5, ge=0, le=1)
    character_anchor_y: float = Field(default=0.5, ge=0, le=1)
    character_scale: float = Field(default=1, ge=0.1, le=5)
    subtitle_safe_area: dict[str, float] = Field(default_factory=lambda: {"left": 0.08, "right": 0.08, "bottom": 0.08})
    subtitle_font_px: int = Field(default=52, ge=12, le=240)
    button_positions: dict[str, Any] = Field(default_factory=lambda: {"consult": {"x": 0.5, "y": 0.88}})
    avatar_id: str | None = None
    background_id: str | None = None
    status: Literal["draft", "active", "archived"] = "active"


def create_admin_router(
    *,
    settings: Settings,
    knowledge_store: SQLiteKnowledgeStore,
    admin_store: AdminContentStore,
    embedding_provider: Any,
    provider_status: Callable[[], dict[str, dict[str, Any]]],
    embedding_error: Callable[[], Any],
) -> APIRouter:
    router = APIRouter()

    def require_admin(request: Request) -> None:
        expected = settings.admin_token
        production = settings.app_env.strip().lower() in {"prod", "production"}
        if production and not expected:
            raise HTTPException(status_code=503, detail={"code": "ADMIN_TOKEN_NOT_CONFIGURED", "message": "生产管理口令尚未配置。"})
        if expected:
            supplied = request.headers.get("X-Admin-Token", "")
            if not supplied or not hmac.compare_digest(supplied, expected):
                raise HTTPException(status_code=401, detail={"code": "ADMIN_UNAUTHORIZED", "message": "管理口令无效。"})

    admin_guard = Depends(require_admin)

    @router.get("/admin/{section}", response_class=HTMLResponse)
    def admin_ui(section: Literal["system", "knowledge", "avatar", "display"]) -> str:
        return admin_page(section)

    @router.get("/api/v1/admin/system/status", dependencies=[admin_guard])
    def system_status(request: Request) -> dict[str, Any]:
        return {
            "request_id": _request_id(request),
            "gateway": {"status": "healthy", "version": settings.app_version, "environment": settings.app_env},
            "providers": provider_status(),
            "knowledge": knowledge_store.status(),
            "content": admin_store.counts(),
            "manifest": admin_store.manifest(),
            "display_profile": admin_store.default_display_profile(),
            "last_failure": None,
            "admin_auth": {"required": bool(settings.admin_token) or settings.app_env.lower() in {"prod", "production"}, "configured": bool(settings.admin_token)},
        }

    @router.get("/api/v1/admin/knowledge", dependencies=[admin_guard])
    def list_knowledge(request: Request) -> dict[str, Any]:
        return {
            "request_id": _request_id(request),
            "runs": admin_store.list_knowledge_runs(),
            "documents": knowledge_store.list_documents(),
            "status": knowledge_store.status(),
        }

    @router.post("/api/v1/admin/knowledge/upload", dependencies=[admin_guard])
    async def upload_knowledge(request: Request, file: UploadFile = File(...)) -> dict[str, Any]:
        filename = file.filename or "upload.bin"
        suffix = Path(filename).suffix.lower()
        if suffix not in KNOWLEDGE_EXTENSIONS:
            raise _bad_request("UNSUPPORTED_KNOWLEDGE_FILE", "仅支持 PDF、DOCX、Markdown 和 TXT。")
        content = await _read_limited(file, settings.max_knowledge_upload_bytes)
        if not content:
            raise _bad_request("EMPTY_KNOWLEDGE_FILE", "上传文件为空。")
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(dir=settings.admin_upload_dir, suffix=suffix, delete=False) as staged:
                staged.write(content)
                temp_path = Path(staged.name)
            parsed = parse_selected_knowledge_path(temp_path, default_status="draft")
            if not parsed or not any(doc.text.strip() for doc in parsed):
                raise ValueError("文件没有可发布的文本内容")
            docs = [asdict(doc) for doc in parsed]
            run = admin_store.create_knowledge_run(filename, content, docs, sum(len(chunk_text(doc.text)) for doc in parsed))
            normalized = _run_documents(run)
            knowledge_store.upsert_many(normalized)
            return {"request_id": _request_id(request), "run": _public_run(run)}
        except HTTPException:
            raise
        except Exception as exc:
            raise _bad_request("KNOWLEDGE_PARSE_FAILED", f"文件解析失败：{str(exc)[:160]}") from exc
        finally:
            if temp_path:
                temp_path.unlink(missing_ok=True)

    @router.post("/api/v1/admin/knowledge/{run_id}/preview", dependencies=[admin_guard])
    def preview_knowledge(run_id: str, request: Request) -> dict[str, Any]:
        run = _require_run(admin_store, run_id)
        run = admin_store.update_knowledge_run(run_id, "preview") or run
        preview = []
        for doc in _run_documents(run):
            for index, text in enumerate(chunk_text(doc.text)):
                preview.append({"doc_id": doc.doc_id, "title": doc.title, "chunk_index": index, "excerpt": text[:500], "source": doc.source_uri})
        return {"request_id": _request_id(request), "run": _public_run(run), "preview": preview}

    @router.post("/api/v1/admin/knowledge/{run_id}/approve", dependencies=[admin_guard])
    def approve_knowledge(run_id: str, request: Request) -> dict[str, Any]:
        run = _require_run(admin_store, run_id)
        if run["status"] in {"rejected", "published"}:
            raise _conflict("INVALID_KNOWLEDGE_TRANSITION", "当前状态不能审核通过。")
        updated = admin_store.update_knowledge_run(run_id, "approved") or run
        return {"request_id": _request_id(request), "run": _public_run(updated)}

    @router.post("/api/v1/admin/knowledge/{run_id}/reject", dependencies=[admin_guard])
    def reject_knowledge(run_id: str, request: Request) -> dict[str, Any]:
        run = _require_run(admin_store, run_id)
        if run["status"] == "published":
            raise _conflict("PUBLISHED_KNOWLEDGE_IMMUTABLE", "已发布批次不能直接驳回。")
        docs = _run_documents(run)
        knowledge_store.set_documents_status([doc.doc_id for doc in docs], "rejected")
        updated = admin_store.update_knowledge_run(run_id, "rejected") or run
        return {"request_id": _request_id(request), "run": _public_run(updated)}

    @router.post("/api/v1/admin/knowledge/{run_id}/publish", dependencies=[admin_guard])
    async def publish_knowledge(run_id: str, request: Request) -> dict[str, Any]:
        run = _require_run(admin_store, run_id)
        if run["status"] != "approved":
            raise _conflict("KNOWLEDGE_NOT_APPROVED", "知识批次必须先审核通过。")
        configuration_error = embedding_error()
        if configuration_error is not None:
            raise HTTPException(status_code=503, detail={"code": "BLOCKED_PROVIDER_CREDENTIALS", "failed_stage": "embedding_provider_config", "message": "Embedding Provider 尚未配置。"})
        documents = [
            KnowledgeDocument(**{**asdict(doc), "status": "approved", "reviewed_by": "admin", "reviewed_at": None})
            for doc in _run_documents(run)
        ]
        try:
            result = await knowledge_store.index_documents(documents, embedding_provider, _request_id(request))
        except Exception as exc:
            knowledge_store.set_documents_status([doc.doc_id for doc in documents], "draft")
            admin_store.update_knowledge_run(run_id, "failed", error_message=str(exc)[:200])
            raise HTTPException(status_code=502, detail={"code": "KNOWLEDGE_PUBLISH_FAILED", "failed_stage": "embedding", "message": "知识发布失败。"}) from exc
        updated = admin_store.update_knowledge_run(run_id, "published", vector_count=int(result["chunks"])) or run
        return {"request_id": _request_id(request), "run": _public_run(updated), "index": result}

    @router.get("/api/v1/admin/avatar", dependencies=[admin_guard])
    def list_avatar(request: Request) -> dict[str, Any]:
        return {"request_id": _request_id(request), "assets": admin_store.list_assets(), "manifest": admin_store.manifest()}

    @router.post("/api/v1/admin/avatar", dependencies=[admin_guard])
    async def upload_avatar(
        request: Request,
        file: UploadFile = File(...),
        name: str = Form(...),
        version: str = Form(...),
        asset_type: Literal["video", "image"] = Form(...),
    ) -> dict[str, Any]:
        suffix = Path(file.filename or "").suffix.lower()
        expected = ASSET_TYPES.get(suffix)
        if not expected or expected[0] != asset_type:
            raise _bad_request("UNSUPPORTED_ASSET_FILE", "视频仅支持 MP4，背景仅支持 JPG 或 PNG。")
        content = await _read_limited(file, settings.max_asset_upload_bytes)
        if not content:
            raise _bad_request("EMPTY_ASSET_FILE", "上传素材为空。")
        if not _valid_asset_signature(suffix, content):
            raise _bad_request("INVALID_ASSET_CONTENT", "文件内容与 MP4/JPG/PNG 类型不匹配。")
        if not name.strip() or not version.strip():
            raise _bad_request("INVALID_ASSET_METADATA", "素材名称和版本不能为空。")
        asset = admin_store.add_asset(
            filename=file.filename or f"asset{suffix}", content=content, name=name.strip(),
            version=version.strip(), asset_type=asset_type, content_type=expected[1],
        )
        return {"request_id": _request_id(request), "asset": asset}

    @router.post("/api/v1/admin/avatar/{avatar_id}/publish", dependencies=[admin_guard])
    def publish_avatar(avatar_id: str, request: Request) -> dict[str, Any]:
        asset = admin_store.publish_asset(avatar_id)
        if not asset:
            raise _not_found("ASSET_NOT_FOUND", "素材不存在。")
        return {"request_id": _request_id(request), "asset": asset, "manifest": admin_store.manifest()}

    @router.post("/api/v1/admin/avatar/{avatar_id}/rollback", dependencies=[admin_guard])
    def rollback_avatar(avatar_id: str, request: Request) -> dict[str, Any]:
        asset = admin_store.publish_asset(avatar_id)
        if not asset:
            raise _not_found("ASSET_NOT_FOUND", "回滚版本不存在。")
        return {"request_id": _request_id(request), "asset": asset, "manifest": admin_store.manifest()}

    @router.delete("/api/v1/admin/avatar/{avatar_id}/delete", dependencies=[admin_guard])
    def delete_avatar(avatar_id: str, request: Request) -> dict[str, Any]:
        if not admin_store.delete_asset(avatar_id):
            raise _conflict("ASSET_DELETE_BLOCKED", "素材不存在或当前版本已发布。")
        return {"request_id": _request_id(request), "deleted": avatar_id}

    @router.get("/api/v1/admin/avatar/{avatar_id}/file", dependencies=[admin_guard])
    def preview_avatar_file(avatar_id: str) -> FileResponse:
        return _asset_response(admin_store, avatar_id)

    @router.get("/api/v1/admin/display", dependencies=[admin_guard])
    def list_display(request: Request) -> dict[str, Any]:
        return {"request_id": _request_id(request), "profiles": admin_store.list_display_profiles()}

    @router.post("/api/v1/admin/display", dependencies=[admin_guard])
    def create_display(body: DisplayProfilePayload, request: Request) -> dict[str, Any]:
        _validate_display_assets(admin_store, body)
        return {"request_id": _request_id(request), "profile": admin_store.save_display_profile(body.model_dump())}

    @router.put("/api/v1/admin/display/{profile_id}", dependencies=[admin_guard])
    def update_display(profile_id: str, body: DisplayProfilePayload, request: Request) -> dict[str, Any]:
        if not admin_store.get_display_profile(profile_id):
            raise _not_found("DISPLAY_PROFILE_NOT_FOUND", "显示配置不存在。")
        _validate_display_assets(admin_store, body)
        return {"request_id": _request_id(request), "profile": admin_store.save_display_profile(body.model_dump(), profile_id=profile_id)}

    @router.post("/api/v1/admin/display/{profile_id}/set-default", dependencies=[admin_guard])
    def set_default_display(profile_id: str, request: Request) -> dict[str, Any]:
        profile = admin_store.set_default_profile(profile_id)
        if not profile:
            raise _not_found("DISPLAY_PROFILE_NOT_FOUND", "显示配置不存在。")
        return {"request_id": _request_id(request), "profile": profile}

    @router.get("/api/v1/assets/manifest")
    def assets_manifest(request: Request) -> dict[str, Any]:
        return {"request_id": _request_id(request), **admin_store.manifest()}

    @router.get("/api/v1/assets/{avatar_id}")
    def asset_file(avatar_id: str) -> FileResponse:
        asset = admin_store.get_asset(avatar_id, include_path=True)
        if not asset or asset["status"] != "published":
            raise _not_found("ASSET_NOT_FOUND", "素材不存在。")
        return _asset_response(admin_store, avatar_id)

    @router.get("/api/v1/display/profile")
    def display_profile(
        request: Request,
        width: int = Query(ge=320, le=7680),
        height: int = Query(ge=320, le=7680),
        orientation: Literal["landscape", "portrait"] | None = None,
    ) -> dict[str, Any]:
        return {"request_id": _request_id(request), "profile": admin_store.match_display_profile(width, height, orientation)}

    return router


async def _read_limited(upload: UploadFile, limit: int) -> bytes:
    content = await upload.read(limit + 1)
    if len(content) > limit:
        raise HTTPException(status_code=413, detail={"code": "UPLOAD_TOO_LARGE", "message": "上传文件超过大小限制。"})
    return content


def _run_documents(run: dict[str, Any]) -> list[KnowledgeDocument]:
    return [KnowledgeDocument(**item) for item in run.get("documents", [])]


def _public_run(run: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in run.items() if key != "documents"}


def _require_run(store: AdminContentStore, run_id: str) -> dict[str, Any]:
    run = store.get_knowledge_run(run_id)
    if not run:
        raise _not_found("KNOWLEDGE_RUN_NOT_FOUND", "知识上传批次不存在。")
    return run


def _request_id(request: Request) -> str:
    return str(getattr(request.state, "request_id", None) or request.headers.get("X-Request-Id") or uuid.uuid4())


def _bad_request(code: str, message: str) -> HTTPException:
    return HTTPException(status_code=422, detail={"code": code, "message": message})


def _not_found(code: str, message: str) -> HTTPException:
    return HTTPException(status_code=404, detail={"code": code, "message": message})


def _conflict(code: str, message: str) -> HTTPException:
    return HTTPException(status_code=409, detail={"code": code, "message": message})


def _asset_response(store: AdminContentStore, avatar_id: str) -> FileResponse:
    asset = store.get_asset(avatar_id, include_path=True)
    if not asset:
        raise _not_found("ASSET_NOT_FOUND", "素材不存在。")
    path = Path(str(asset["file_path"]))
    if not path.is_file():
        raise _not_found("ASSET_FILE_MISSING", "素材文件不存在。")
    return FileResponse(path, media_type=str(asset["content_type"]), filename=path.name)


def _valid_asset_signature(suffix: str, content: bytes) -> bool:
    if suffix == ".mp4":
        return len(content) >= 12 and b"ftyp" in content[:32]
    if suffix == ".png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix in {".jpg", ".jpeg"}:
        return content.startswith(b"\xff\xd8\xff")
    return False


def _validate_display_assets(store: AdminContentStore, body: DisplayProfilePayload) -> None:
    for asset_id, expected_type, field_name in (
        (body.avatar_id, "video", "待机视频"),
        (body.background_id, "image", "背景图片"),
    ):
        if not asset_id:
            continue
        asset = store.get_asset(asset_id)
        if not asset or asset["asset_type"] != expected_type:
            raise _bad_request("DISPLAY_ASSET_INVALID", f"{field_name}不存在或类型不正确。")
        if asset["status"] != "published":
            raise _bad_request("DISPLAY_ASSET_NOT_PUBLISHED", f"{field_name}必须先发布才能绑定。")
