# Repository Cleanup Evidence — 2026-08-07

输出日期：2026-08-07

本次整理目标：把仓库主线 `main` 固化为可交接、可继续开发与部署的基线，不新增业务代码。

## 1) Git 状态与分支核验

- 本地分支切换：`main`
- `origin/main` 远端最新提交：`a68f234`
- 本地 `main` 已 fast-forward 到远端 `a68f234`
- 最终 `git fetch origin --prune`：成功；本地 ahead/behind 为 `0/0`
- `TASK-014A-admin-content-display` 代码已在主线，不再要求继续重放开发。
- `main` 与 `origin/task/TASK-014A-admin-content-display`：ahead/behind 为 `0/0`，文件差异为空。
- 新建本次备份标签：`backup-before-repository-cleanup-20260807`
- 任务分支：`task/TASK-014A-admin-content-display` 仍保留（未删除）。

## 2) 文件结构与索引

- 关键目录核验通过：`android-app`, `gateway`, `deploy`, `scripts`, `tests`, `tasks`, `docs`, `memory`
- 当前 Git 跟踪文件数：`489`；远端分支数：`9`；标签数：`6`
- docs 目录内验证目录存在：`docs/architecture`, `docs/api`, `docs/operations`, `docs/testing`, `docs/evidence`, `docs/adr`, `docs/README.md`
- 代码清单中未新增运行时数据目录到源码根下。

## 3) 文档与任务索引一致性

- 更新文件：
  - `README.md`
  - `CODEX_START_HERE.md`
  - `PROJECT_STATE.md`
  - `TASKS.md`
  - `tasks/index.yaml`
  - `memory/CURRENT_STATE.md`
  - `memory/HANDOFF.md`
  - `memory/PENDING_INPUTS.md`
  - `.gitignore`
  - `docs/REPOSITORY_STRUCTURE.md`
  - `docs/evidence/REPOSITORY_CLEANUP/README.md`（本文件）
- 任务状态对齐：
  - `tasks/index.yaml` 当前设为 `TASK-015`
  - `TASKS.md` 明确下一步仅 `TASK-015`
  - `PROJECT_STATE.md`/`memory` 说明 `TASK-014A` 已入主线

## 4) 证据与安全检查

- Gateway + Admin 测试命令（项目 Python 3.10 环境）：
  - `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\gateway tests\admin -q` → `18 passed, 1 warning`
  - `.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\admin\test_admin_content_display.py -q` → `10 passed, 1 warning`
- 配置检查：
  - `.\.venv\gateway-task008-py310\Scripts\python.exe scripts\check_provider_env.py --require-real-mvp` → `missing`（本地未配置 `secrets\.env.local`）
- API 路由存在性检查：
  - 使用 `docs/api/MVP_API_SPEC.md` 要求路由列表完成匹配（返回 `API_ROUTES_OK`）
- 文档链接检查：
  - 关键文档路径均可解析（`DOC_LINKS_OK`）
- `git diff --check` → 通过
- 敏感文件扫描：
  - 当前跟踪文件后缀/目录检查：`safe`
  - AWS Access Key、GitHub Token、私钥头模式：`safe`
  - 通用 `sk-` 凭据形态：`suspicious`
  - 命中文件：`docs/evidence/TASK-014/task014a-skeleton-contract-20260807.json`
  - 最早命中提交：`9363609`；未输出或复制命中值
  - 依据安全门禁，本轮提交与推送停止，需先由仓库所有者确认凭据性质并决定 GitHub 密钥撤销/历史处置方案

## 5) 待清理但未删除列表

- `docs/evidence/TASK-014/` 下若干已生成 `.json/.txt/.bin/.mp3` 证据文件保持本地、未提交；其中二进制音频已由 `.gitignore` 排除，本轮不删除。
- `docs/evidence/TASK-013/task013-30cycle-pytest-report.json` 曾被本轮测试重写时延字段，已恢复，不纳入整理提交。

## 6) 下一步

1. 先确认疑似凭据是否真实；若真实，立即撤销/轮换，并单独批准历史清理方案。在该安全问题解除前不得 push。
2. 安全门禁解除后，再按 `TASK-015_ANDROID_DEVICE_ACCEPTANCE.md` 补齐 Android 真机验收。
