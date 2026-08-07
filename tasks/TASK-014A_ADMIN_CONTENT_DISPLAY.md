# TASK-014A - 轻量管理后台、知识库上传与显示配置

- **Status:** PLANNED
- **Priority:** P1
- **Dependencies:** TASK-012 DONE, TASK-014 DONE
- **Target branch:** `task/TASK-014A-admin-content-display`
- **Owner:** Codex / assigned developer

## 目标

在不引入 Dify、CMS 或大型前端框架的前提下，为现有 Android 大屏 AI 语音客服增加非开发人员可使用的轻量管理层。必须复用 TASK-012 的 SQLite/FTS5/FAISS/Embedding RAG 和现有 Gateway。

本任务首先交付四页可运行骨架、数据模型、API 契约、状态机和持久化验证，不扩张为复杂 CMS。

## 页面范围

### 1. 系统状态 `/admin/system`

- Gateway readiness；
- ASR、TTS、LLM、Embedding 配置状态；
- approved/draft/rejected、chunk 和 FAISS vector 数量；
- 当前发布素材和 Display Profile；
- 最近失败的 `code`、`failed_stage` 和 `request_id`。

### 2. 知识库 `/admin/knowledge`

- 上传 PDF、DOCX、Markdown、TXT；
- 新文件默认 `draft`；
- parse、chunk、preview、approve/reject、embedding、publish；
- 搜索测试和问答测试展示 chunk、source、request_id；
- 只有 `approved` 内容进入顾客检索。

流程：

`upload -> draft -> parse -> chunk -> preview -> approve -> embedding -> FAISS -> publish`

### 3. 数字人形象 `/admin/avatar`

Phase 1 仍使用静态图片或本地待机视频，不做实时口型。

- MP4 待机视频；
- JPG/PNG 背景；
- 浏览器预览；
- 名称、版本、SHA-256、创建时间和发布状态；
- 发布、回滚和删除未发布素材；
- 生成公开客户端 manifest。

推荐模式：`composite_video`。预留 `video_with_background`，但不作为本任务门禁。

### 4. 大屏配置 `/admin/display`

- 1920x1080、3840x2160、1280x720、1080x1920；
- 自定义宽高；
- `orientation`: landscape / portrait；
- `scale_mode`: fit / fill / crop；
- 人物位置与缩放；
- 字幕安全区与字号；
- 按钮位置；
- 绑定待机视频/背景版本。

Android 根据真实屏幕尺寸匹配并缓存 Profile，不因屏幕尺寸重新打 APK。

## 最小管理 API

- `GET /api/v1/admin/system/status`
- `GET /api/v1/admin/knowledge`
- `POST /api/v1/admin/knowledge/upload`
- `POST /api/v1/admin/knowledge/{run_id}/preview`
- `POST /api/v1/admin/knowledge/{run_id}/approve`
- `POST /api/v1/admin/knowledge/{run_id}/reject`
- `POST /api/v1/admin/knowledge/{run_id}/publish`
- `GET /api/v1/admin/avatar`
- `POST /api/v1/admin/avatar`
- `POST /api/v1/admin/avatar/{avatar_id}/publish`
- `POST /api/v1/admin/avatar/{avatar_id}/rollback`
- `GET /api/v1/admin/display`
- `POST /api/v1/admin/display`
- `PUT /api/v1/admin/display/{profile_id}`
- `POST /api/v1/admin/display/{profile_id}/set-default`
- `GET /api/v1/assets/manifest`

## 最小数据模型

### `knowledge_upload_run`

- `run_id`, `document_uri`, `document_title`, `source_type`；
- `status`: draft / parsed / preview / approved / rejected / published / failed；
- `chunk_count`, `vector_count`, `error_message`；
- `created_at`, `updated_at`。

### `avatar_asset`

- `avatar_id`, `name`, `type`: video / image；
- `uri`, `sha256`, `version`；
- `status`: draft / preview / approved / published / rejected；
- `source`, `created_at`, `updated_at`。

### `display_profile`

- `profile_id`, `profile_name`, `width_px`, `height_px`；
- `orientation`, `scale_mode`；
- `character_anchor_x`, `character_anchor_y`, `character_scale`；
- `subtitle_safe_area`, `subtitle_font_px`, `button_positions`；
- `avatar_id`, `background_id`, `is_default`, `status`；
- `created_at`, `updated_at`。

## 持久化边界

- `/opt/jiyangjia-ai/var/knowledge/`: SQLite / FAISS；
- `/opt/jiyangjia-ai/var/assets/`: 视频、图片与 manifest；
- `/opt/jiyangjia-ai/secrets/.env.local`: Provider 与 Admin 密钥；
- Git 仅保存代码、schema、示例和文档。

管理 API 统一放在 `/api/v1/admin/*`。Phase 1 可使用服务端 `ADMIN_TOKEN`，不得进入 APK、前端 bundle 或 Git。

## 验收门禁

- 四页可访问并具有 loading、empty、error 状态；
- PDF/DOCX/MD/TXT 上传、解析、chunk 预览通过；
- draft 不进入顾客检索，approved 后 sources 正确；
- MP4/JPG/PNG 上传、预览、发布和回滚通过；
- manifest 返回当前版本与 SHA-256；
- 四个预设分辨率和自定义 Profile 可保存、匹配和读取；
- 服务重启后知识、素材和 Profile 不丢失；
- 未泄露 API Key、ADMIN_TOKEN、原始资料、SQLite 或 FAISS。

## 非目标

- Dify、LangFlow、Flowise；
- 复杂 RBAC、企业 IAM、多租户；
- 大型 CMS 或在线视频编辑；
- LiveTalking、Wav2Lip、MuseTalk；
- 自动扫描 `E:\work\积养家`；
- 未审核资料自动发布。

## 完成后更新

- `PROJECT_STATE.md`
- `TASKS.md`
- `tasks/index.yaml`
- `memory/CURRENT_STATE.md`
- `memory/HANDOFF.md`
- `memory/PENDING_INPUTS.md`
