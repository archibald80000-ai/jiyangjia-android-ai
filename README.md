# 积养家 Android 大屏 AI 语音客服系统

> Repository: `jiyangjia-android-ai`
> Workspace: `E:\work\ai-kefu\jiyangjia-ai`
> Target: Android 12 大屏

本仓库作为 Phase 1 正式基线，管理 Android 端、Gateway、任务、文档、证据与交接。
交付目标是“本地待机人物视频 + 轻量知识问答 + Android 音频交互 + 健康的运维边界”，
不在当前基线中承诺实时数字人、GPU 推理或全量业务私有资料上链。

## 项目目标

- 在 Android 12 大屏上交付可观测的语音客服 MVP。
- Gateway 通过 provider adapter 路由 ASR/TTS/LLM/Embedding 调用。
- 采用轻量 RAG（SQLite + FAISS）并使用 `approved` 内容供客户检索。
- 管理后台支持知识内容与显示配置的草稿/发布流程，便于门店内容上线前复核。
- 任务结构与文档可直接交接到 `TASK-015` 的真机验收。

## 当前 MVP 架构

```text
Android 12 Kiosk（android-app）
  -> Gateway（gateway）
    -> ASR Provider（TASK-009）
    -> LLM/Embedding Provider（TASK-011）
    -> 知识库（SQLite + FAISS，TASK-012）
    -> TTS Provider（TASK-009）
    -> Android 显示与字幕回放
```

LiveTalking/Wav2Lip/MuseTalk/WebRTC 数字人、实时口型与 GPU 推理为 **增强阶段**，当前不在第一阶段上线目标。

## 已完成功能

- TASK-005：Android 12 横屏 Kiosk 外壳与本地待机/交互基础能力。
- TASK-007：音频输入输出链路与设备监控能力。
- TASK-008：FastAPI Gateway、基础健康接口、Provider 抽象与对话入口。
- TASK-009/010/011：Doubao ASR/TTS、LLM 和 Embedding 适配器与本地回归基础。
- TASK-012：轻量 RAG 与检索来源返回（含 draft/reject/approved 状态）。
- TASK-013：Android 到 Gateway 对话链路联调（无真机验收）。
- TASK-014：腾讯云部署与 Gateway 生产链路收口（基于任务环境）。
- TASK-014A：四页管理后台（system / knowledge / avatar / display）+发布闭环+路由 API。

## 未完成项（不在本基线宣称范围）

- Android 12 真机验收（TASK-015）。
- 生产环境 ADMIN_TOKEN 与正式内容发布流程。
- LiveTalking 全流程重入与实时口型（增强阶段）。
- 生产监控、告警、CDN/成本保护与长期稳定性验证。

## 仓库结构与边界

```text
android-app/     Android 大屏客户端源码（APK 产物不入库）
gateway/         FastAPI 服务、路由、Provider 适配器
integration/     外部服务适配说明（若新增）
knowledge-test/   受控知识样例（可复用但非正式资料）
config/          示例配置与上游锁版本
deploy/          Docker Compose 与部署说明（不含密钥）
scripts/         校验、发布辅助、Provider 工具脚本
tests/           后端、管理后台、知识链路与 Android 相关测试
tasks/           TASK-000~ 的任务骨架
docs/            架构、接口、部署、验收、证据目录
memory/          会话状态、决策和 Handoff 记录
assets/          人物/背景说明与示例清单（不入库业务素材）
.github/        CI 与 Issue 模板
```

运行时/临时文件边界：

- `var/`, `runtime/`, `logs/`, `tmp/`, `recordings/`, `secrets/`, `data/`, `knowledge-source-private/`
  属于运行时或私有资料，不进入源码提交。

## 本地启动方法

1. 安装环境与依赖（`gateway`）：

```powershell
py -3.10 -m venv .venv\gateway-task008-py310
.\.venv\gateway-task008-py310\Scripts\python.exe -m pip install -r gateway\requirements.txt
```

2. 配置环境变量：

```powershell
Copy-Item .env.example .env.local
# 本文件仅作模板，真实值由本地/服务器机密存储提供
```

3. 运行 Gateway（开发口径）：

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m gateway --host 127.0.0.1 --port 18080
```

4. 打开管理后台（开发默认口令环境）：

- `http://127.0.0.1:18080/admin/system`
- `http://127.0.0.1:18080/admin/knowledge`
- `http://127.0.0.1:18080/admin/avatar`
- `http://127.0.0.1:18080/admin/display`

## 自动化测试方法

- Gateway/管理后台：

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\gateway tests\admin -q
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\admin\test_admin_content_display.py -q
```

- 配置/预检：

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\check_provider_env.py --require-real-mvp
```

## 管理后台入口

- 管理页面：`/admin/system`、`/admin/knowledge`、`/admin/avatar`、`/admin/display`
- 管理 API：`/api/v1/admin/*`（生产要求 `X-Admin-Token`，缺失返回 `503 ADMIN_TOKEN_NOT_CONFIGURED`）
- 客户端接口：`/api/v1/client/config`、`/api/v1/assets/manifest`、`/api/v1/display/profile`

## Gateway API

基础接口来自 [`docs/api/MVP_API_SPEC.md`](docs/api/MVP_API_SPEC.md)：

- `GET /health`
- `GET /api/v1/health`
- `GET /api/v1/readiness`
- `POST /api/v1/dialogue/text`
- `POST /api/v1/dialogue/audio`
- `POST /api/v1/knowledge/index`
- `POST /api/v1/knowledge/search`
- `GET /api/v1/knowledge/status`
- `GET /api/v1/audio/{audio_id}`
- `GET /api/v1/client/config`
- `GET /api/v1/admin/system/status`
- `GET|POST /api/v1/admin/*`

## Android 端位置

`android-app/`
APK 以本地构建产物为准，不提交到 Git；未进行 Android 真机发布验收前仅表示本地构建和单元覆盖情况。

## 环境变量配置方式

- 根模板：`.env.example`（仅变量名与占位符）
- 本地/服务器：`.env.local` 或等效环境变量
- 禁止将真实值写入源码、提交日志或聊天输出。

## 腾讯云部署入口

当前部署入口与说明集中在：

- [`docs/operations/MVP_DEPLOYMENT.md`](docs/operations/MVP_DEPLOYMENT.md)
- `deploy/docker-compose.yml`
- `deploy/` 下的部署素材

## 当前任务与下一任务

- 当前权限内完成基线收口：`main`（`a68f234`）已包含 `TASK-014A` 变更。
- 下一任务仅允许执行：`TASK-015_ANDROID_DEVICE_ACCEPTANCE.md`（需真实 Android 12 设备与批准素材信息）。

## 证据与交接

- 变更和验收证据集中在 `docs/evidence/`。
- 任务状态由 `PROJECT_STATE.md`、`TASKS.md`、`tasks/index.yaml`、`memory/*` 统一维护。

## 免责声明

- 未声明的真机指标（设备、网络、音频硬件）不能在本仓库视为已完成。
- LiveTalking/Wav2Lip/MuseTalk/WebRTC 数字人口型与 GPU 推理保留为增强阶段任务。
