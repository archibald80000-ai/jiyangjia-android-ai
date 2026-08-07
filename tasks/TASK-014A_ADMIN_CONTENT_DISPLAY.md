# TASK-014A: Admin content and display profile skeleton

- **Status:** PLANNED
- **Priority:** P1
- **Dependencies:** TASK-014
- **Branch:** `task/TASK-014-tencent-gateway-deployment` (scope prep; implementation on `task/TASK-014A_*` in next task branch)
- **Owner:** Codex / assigned developer

## Objective

在不引入完整 CMS 的前提下，先交付**轻量后台骨架**，支持任务 014A 的配置、审核和发布链路。

目标页（MVP）：

- 系统状态
- 知识库
- 数字人素材
- Display Profile（大屏显示配置）

## Scope (skeleton-only)

- 定义接口协议、数据模型和状态机，不接入复杂 RBAC 或第三方可视化平台。
- 后端主路径保留现有：
  - `GET /api/v1/readiness`
  - `/api/v1/knowledge/*`
  - `POST /api/v1/dialogue/*`
- 同步时机：在完成本任务文档/合同后由 `TASK-015` 前继续推进真实实现，不提前扩展为全量后台。

## Delivery target

1. 增加后台骨架文档与最小契约：
   - 页面路由与字段定义（4 页）
   - `avatar`、`knowledge_upload_run`、`display_profile` 数据模型
   - 审核与发布流（`draft -> preview -> approve -> publish`）
2. 先提交配置/审批骨架，不实现大规模 CRUD 逻辑。
3. 给出可落地到 `main` 的状态文档与 evidence 清单。

## 非目标

- 不引入 Dify、LangFlow、Flowise。
- 不实现完整 CMS（权限系统、审核计费、发布工作流引擎、在线视频编辑）。
- 不接入实时口型（LiveTalking/Wav2Lip/MuseTalk）主链路。

## 页面路由与职责（骨架）

### `/admin/system`

- 展示：
  - Gateway readiness
  - Provider 配置状态
  - `knowledge_store` 状态（approved/draft/rejected、chunk、faiss vector 数）
  - 最近一次失败 `code` 与 `failed_stage`（如有）
- 依赖读取：
  - `GET /api/v1/readiness`
  - `GET /api/v1/knowledge/status`

### `/admin/knowledge`

- 展示：
  - 知识文件上传草稿列表（`draft`）
  - 解析预览结果（`preview`）
  - 审核/发布动作（`approve`、`publish`）
- 接口草案：
  - `GET /api/v1/admin/knowledge`
  - `POST /api/v1/admin/knowledge/upload`
  - `POST /api/v1/admin/knowledge/{run_id}/preview`
  - `POST /api/v1/admin/knowledge/{run_id}/approve`
  - `POST /api/v1/admin/knowledge/{run_id}/publish`

### `/admin/avatar`

- 展示与维护：
  - 预定义静态人物视频 / 图片素材
  - 版本号、文件来源、`sha256`、有效期
  - 草稿与已审核状态
- 接口草案：
  - `GET /api/v1/admin/avatar`
  - `POST /api/v1/admin/avatar`
  - `PUT /api/v1/admin/avatar/{avatar_id}`
  - `POST /api/v1/admin/avatar/{avatar_id}/approve`

### `/admin/display`

- 展示与维护：
  - Display Profile（多分辨率）
  - 角色定位/比例
  - 字幕安全区、字体、按钮坐标
  - 默认页配置
- 接口草案：
  - `GET /api/v1/admin/display`
  - `POST /api/v1/admin/display`
  - `PUT /api/v1/admin/display/{profile_id}`
  - `POST /api/v1/admin/display/{profile_id}/set-default`

## 数据模型（最小）

### `avatar`

- `avatar_id TEXT PK`
- `name TEXT`
- `type TEXT CHECK(type IN ('video','image'))`
- `uri TEXT`
- `sha256 TEXT`
- `version INTEGER`
- `status TEXT CHECK(status IN ('draft','preview','approved','rejected'))`
- `source TEXT`（manual/ops/reviewed）
- `effective_from DATETIME`
- `effective_to DATETIME NULL`
- `created_at DATETIME`
- `updated_at DATETIME`

### `knowledge_upload_run`

- `run_id TEXT PK`
- `document_uri TEXT`
- `document_title TEXT`
- `status TEXT CHECK(status IN ('draft','preview','approve','publish','failed'))`
- `source_type TEXT CHECK(source_type IN ('upload','api','manual'))`
- `chunk_count INTEGER`
- `vector_count INTEGER`
- `error_message TEXT NULL`
- `created_at DATETIME`
- `updated_at DATETIME`

### `display_profile`

- `profile_id TEXT PK`
- `resolution_width INTEGER`
- `resolution_height INTEGER`
- `orientation TEXT CHECK(orientation IN ('landscape','portrait'))`
- `fit_mode TEXT CHECK(fit_mode IN ('fit','fill','crop'))`
- `character_anchor_x REAL`
- `character_anchor_y REAL`
- `character_scale REAL`
- `subtitle_safe_area JSON`
- `subtitle_font_px INTEGER`
- `button_positions JSON`
- `is_default BOOLEAN`
- `status TEXT CHECK(status IN ('draft','approved','rejected'))`
- `created_at DATETIME`
- `updated_at DATETIME`

## 流程定义

- 知识流：`draft -> preview -> approve -> publish`
- 素材流：`draft -> approved/rejected`
- 显示流：`draft -> approved`，后由 `set-default` 生效
- 任何流的失败记录写入 `error_message`（用于后台状态页展示）

## Display Profile 示例枚举（MVP）

- `1920x1080`
- `3840x2160`
- `1280x720`
- `1080x1920`
- 自定义（`width`/`height` 任意正整数）

每个 Profile 包含：

- `orientation`
- `fit/fill/crop`
- 人物锚点（`x`,`y`,`scale`）
- 字幕安全区（`left/right/top/bottom`）
- 字幕字号
- 按钮坐标

示例（`docs/evidence/TASK-014/task014a-skeleton-contract-20260807.json`）：

```json
{
  "profiles": [
    {
      "profile_id": "kiosk-1080p-landscape",
      "resolution": {"w": 1920, "h": 1080},
      "orientation": "landscape",
      "fit_mode": "fit",
      "character_anchor": {"x": 0.42, "y": 0.62, "scale": 0.62},
      "subtitle_safe_area": {"left": 0.06, "right": 0.06, "top": 0.88, "bottom": 0.03},
      "subtitle_font_px": 36,
      "button_positions": {
        "start": [0.80, 0.85],
        "cancel": [0.05, 0.85],
        "help": [0.05, 0.05]
      },
      "status": "approved",
      "is_default": true
    }
  ]
}
```

## 验收指标（本任务骨架级）

- 任务文档与 `tasks/index.yaml` 更新完成。
- `tasks/TASK-014A_ADMIN_CONTENT_DISPLAY.md` 包含 4 页定义、数据模型、状态流与 API 草案。
- `memory/PENDING_INPUTS.md` 保留未闭环项（机型分辨率、权限边界、素材归档）。
- 仅保留轻量后台骨架，不进行生产级 UI/CMS 落地。
- 真实生产代码需在后续 `TASK-014A` 实施分支继续，不提前在本任务混入复杂 CRUD。

## References

- `memory/CURRENT_STATE.md`
- `memory/HANDOFF.md`
- `tasks/index.yaml`
- `PROJECT_STATE.md`
- `docs/evidence/TASK-014/`（收口后接口链路凭据）
