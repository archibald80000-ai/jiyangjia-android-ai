# Codex 开始执行

请在 Windows 上打开：

`E:\work\ai-kefu\jiyangjia-ai`

然后把以下内容作为新 Codex 会话的第一条指令：

```text
你现在负责 jiyangjia-android-ai 项目，优先执行当前授权任务：TASK-014A_ADMIN_CONTENT_DISPLAY。

先读取：
1. AGENTS.md
2. MEMORY.md
3. PROJECT_STATE.md
4. memory/CURRENT_STATE.md
5. memory/HANDOFF.md
6. memory/PENDING_INPUTS.md
7. tasks/TASK-014A_ADMIN_CONTENT_DISPLAY.md

固定项目目录：E:\work\ai-kefu\jiyangjia-ai
原始资料目录：E:\work\积养家（默认只读，不扫描、不上传、不修改）

严格遵守单任务原则。开始前报告当前目录、分支、已有改动、工具环境、准备修改文件、测试命令和风险。先完成骨架/架构文档更新，再推进轻量实现。

不得读取或输出 .env.local 的值；只能报告需要的变量名是否配置。不得提交密钥、模型权重、人物素材、录音或原始业务资料。

完成后更新任务状态、PROJECT_STATE.md、memory/CURRENT_STATE.md 和 memory/HANDOFF.md，并给出真实命令、结果、日志路径、阻塞和下一任务建议。
```

请先根据 TASKS.md 的当前顺序执行 `TASK-014A`，暂不跨任务。后续 `TASK-015` 需要真机验收，不与文档骨架并行执行。
