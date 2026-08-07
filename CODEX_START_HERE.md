# Codex 开始执行

请在 Windows 上打开：

`E:\work\ai-kefu\jiyangjia-ai`

然后把以下内容作为新 Codex 会话的第一条指令：

```text
你现在负责 jiyangjia-android-ai 项目，主线仓库基线为 main 分支，当前已通过主分支整理。

先读取：
1. AGENTS.md
2. MEMORY.md
3. PROJECT_STATE.md
4. memory/CURRENT_STATE.md
5. memory/HANDOFF.md
6. memory/PENDING_INPUTS.md
7. tasks/index.yaml
8. TASKS.md
9. tasks/TASK-015_ANDROID_DEVICE_ACCEPTANCE.md（当前待办）

固定项目目录：E:\work\ai-kefu\jiyangjia-ai
原始资料目录：E:\work\积养家（默认只读，不扫描、不上传、不修改）

严格遵守单任务原则。开始前先报告当前目录、分支、已有改动、工具环境、准备修改文件、测试命令和风险。先完成仓库结构与文档同步，再推进实现。

不得读取或输出 .env.local 的值；只能报告变量是否 configured / missing；
不得提交密钥、模型权重、人物素材、原始业务资料、录音或 APK。
```

当前执行优先级：

- `main`：当前官方基线，`main` 与 `origin/main` 已同步；
- `TASK-014A`：已在本轮完成且为可追溯文档，禁止重复实现；
- 下一任务：`TASK-015_ANDROID_DEVICE_ACCEPTANCE.md`（仅在真实 Android 12 设备与批准素材/配置齐备后执行）。

测试与交接：

- 输出前统一给出真实命令、真实结果（含失败码）与日志路径；
- 不做 Android 真机硬件验收时需明确写明 BLOCKED；
- 更新文件建议使用：
  - `PROJECT_STATE.md`
  - `TASKS.md`
  - `tasks/index.yaml`
  - `memory/CURRENT_STATE.md`
  - `memory/HANDOFF.md`
  - `memory/PENDING_INPUTS.md`
