# Repository Structure and Boundaries

生成时间：2026-08-07

本仓库使用“代码与配置入仓、运行时数据不入仓、证据可追溯”的结构。

## 源码与配置

- `android-app/`
  Android 12 大屏客户端（Kotlin）。APK 与日志文件不入库，产物在本地构建目录生成。
- `gateway/`
  FastAPI 网关、路由、Provider 适配、知识与管理接口。
- `integration/`
  现阶段仅保留接口说明与桥接策略，避免重复实现。
- `config/`
  示例配置、上游版本锁、非机密运行配置模板。
- `deploy/`
  部署所需 compose 与 nginx 配置（不含密钥）。
- `scripts/`
  环境检查、Provider 检查、启动和仓库验证脚本。
- `tests/`
  网关、知识库、管理后台与 Android 相关自动化测试。
- `tasks/`
  `TASK-xxx` 任务文档与执行次序。
- `docs/`
  架构、接口、测试、部署、证据、风险与里程碑说明。
- `memory/`
  项目状态、交接与待办，用于会话持续性。
- `assets/`
  资源说明与示例，不上传原始业务素材。业务素材通过 `/var/assets`（运行时）维护。
- `knowledge-test/`
  受控示例知识与测试素材。

## 忽略与边界

以下内容不应进入源码提交（默认由 `.gitignore`/运行时路径管理）：

- 密钥/证书：`.env.local`, `.env.*.local`, `secrets/`, `*.key`, `*.pem`, `*.p12`, `*.pfx`, `*.keystore`, `*.jks`
- 运行时数据库与索引：`*.db`, `*.sqlite`, `*.sqlite3`, `*.index`, `*.faiss`
- 音视频与录音：`*.wav`, `*.mp3`, `*.aac`, `*.m4a`, `*.pcm`, `*.mp4`, `recordings/`
- 构建产物与缓存：`build/`, `.gradle/`, `*.apk`, `*.aab`, `var/`, `logs/`, `tmp/`, `temp/`
- 原始业务资料：`knowledge-source-private/`、`E:\work\积养家` 外部目录（默认只读）
- 供应商返回体与未清洗上传素材：`provider-*`、`uploads/`

## 目录映射说明

- Android 源码入口：`android-app/`
- Gateway 入口：`gateway/app/main.py`
- 管理后台入口：`gateway/app/admin_ui.py`
- 管理 API：`gateway/app/admin_routes.py`
- 任务入口：`tasks/index.yaml`
- 主验收入口：`docs/testing/MVP_ACCEPTANCE.md`

## 清理建议（本轮未执行删除）

1. 将 `main` 与 `origin/main` 的结构差异归零（已在本轮核验前完成）。
2. 统一 `tasks/index.yaml` 的 `current` 到 `TASK-015`（已完成）。
3. 保持 `task/TASK-014A-admin-content-display` 分支仅作历史工作分支，待归档后保留不删除。
