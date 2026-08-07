# TASK-014A — 轻量管理后台、知识库上传与数字人显示配置

## 目标

在不引入 Dify、CMS 或大型前端框架的前提下，为现有 Android 大屏 AI 语音客服补一个可由非开发人员使用的轻量管理后台。

本任务只负责“管理层”，必须复用已经完成的 TASK-012 SQLite/FTS5/FAISS/Embedding RAG 和现有 Gateway，不重写知识引擎。

## 范围 A：知识库管理

实现浏览器后台：

- 上传 PDF / DOCX / Markdown / TXT；
- 新文件默认 `draft`；
- 自动解析、切片并展示 chunk 数量和内容预览；
- 人工执行 `approved / rejected`；
- 只有 `approved` 内容可进入客户正式检索；
- 支持删除、重新解析、重新切片、重新 Embedding、重新构建 FAISS；
- 支持搜索测试与问答测试，并展示命中的 chunk、source、request_id；
- 原始业务文件、SQLite、FAISS 索引不得提交 GitHub。

推荐流程：

`上传 -> draft -> parse -> chunk -> preview -> approve -> embedding -> FAISS -> publish`

## 范围 B：数字人/待机素材管理

Phase 1 仍然不做 LiveTalking 实时口型。数字人形象使用待机视频。

持久化目录建议：

`/opt/jiyangjia-ai/var/assets/`

支持：

- MP4 待机人物视频上传；
- JPG/PNG 背景上传；
- 素材名称、版本、SHA-256、创建时间、发布状态；
- 浏览器预览；
- 发布、回滚、删除未发布素材；
- 第一优先模式 `composite_video`：人物和背景直接合成一个 MP4；
- 预留 `video_with_background`：人物视频与背景分层，但不作为本任务强制上线门禁。

新增公开客户端 manifest，例如：

- `GET /api/v1/assets/manifest`

Android 根据 manifest 检查版本、下载并缓存当前发布素材；网络不可用时继续使用最后一个有效本地版本。

## 范围 C：Display Profile / 多尺寸大屏

禁止因不同屏幕尺寸重新打 APK。

后台可配置：

- `profile_name`
- `width_px`
- `height_px`
- `orientation`: landscape / portrait
- `scale_mode`: fit / fill / crop
- 人物位置与缩放
- 字幕安全区与字号
- 按钮位置
- 绑定的待机视频/背景版本

内置至少：

- 1920x1080
- 3840x2160
- 1280x720
- 1080x1920
- 自定义宽高

Android 启动后读取真实屏幕尺寸，从 `/api/v1/client/config` 或独立 display-profile API 获取最匹配配置，并缓存最后有效配置。

## 范围 D：后台页面

只做四页：

1. 系统状态：Gateway、ASR、LLM、TTS、Embedding、RAG、当前素材版本；
2. 知识库：上传、文档列表、chunk 预览、审核、索引、搜索测试；
3. 数字人形象：视频/背景上传、预览、版本、发布/回滚；
4. 大屏配置：分辨率、方向、缩放、人物位置、字幕安全区、素材绑定和预览。

管理 API 统一放在 `/api/v1/admin/*`。

Phase 1 管理鉴权允许使用单一 `ADMIN_TOKEN`，但 token 只能在服务端环境变量中，不得进入前端 bundle、APK 或 Git。

## 持久化边界

建议固定：

- `/opt/jiyangjia-ai/var/knowledge/`：SQLite / FAISS；
- `/opt/jiyangjia-ai/var/assets/`：数字人/背景素材；
- `/opt/jiyangjia-ai/secrets/.env.local`：Provider 与 Admin 密钥；
- Git 仓库：只保存代码、schema、示例和文档。

## 验收门禁

必须真实验证：

- PDF/DOCX/MD/TXT 上传与解析；
- chunk 生成和预览；
- draft 不进入客户正式检索；
- approved 后可检索且 sources 正确；
- MP4 上传、预览、发布和回滚；
- manifest 返回当前发布版本与 SHA-256；
- 4 个预设分辨率和自定义分辨率保存/读取；
- Android 客户端契约能获取匹配 Display Profile；
- 服务重启后知识、素材和 Profile 不丢失；
- 未泄露 API Key / ADMIN_TOKEN / 原始业务资料。

## 非目标

- Dify / LangFlow / Flowise；
- 复杂 RBAC、企业 IAM；
- 多租户；
- 大型 CMS；
- LiveTalking / Wav2Lip / MuseTalk；
- 自动扫描 `E:\work\积养家`；
- 未审核资料自动发布。

## 依赖与顺序

- 依赖 TASK-012 已完成的 RAG；
- 可以先完成本地代码和自动化测试；
- 当前 TASK-014 Provider env 链仍需单独收口；
- TASK-015 真机验收前应至少完成本任务的客户端配置契约和一个发布素材样例。

## 完成后更新

- `PROJECT_STATE.md`
- `TASKS.md`
- `tasks/index.yaml`
- `memory/CURRENT_STATE.md`
- `memory/HANDOFF.md`
- `memory/PENDING_INPUTS.md`
