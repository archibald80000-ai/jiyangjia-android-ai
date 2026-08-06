# Codex 开始执行

请在 Windows 上打开：

`E:\work\ai-kefu\jiyangjia-ai`

然后把以下内容作为新 Codex 会话的第一条指令：

```text
你现在负责 jiyangjia-android-ai 项目，只执行 TASK-000。

先读取：
1. AGENTS.md
2. MEMORY.md
3. PROJECT_STATE.md
4. memory/CORE_FACTS.md
5. memory/DECISIONS.md
6. memory/HANDOFF.md
7. tasks/TASK-000_PROJECT_BOOTSTRAP.md
8. .codex/TASK_EXECUTION_PROMPT.md

固定项目目录：E:\work\ai-kefu\jiyangjia-ai
原始资料目录：E:\work\积养家（默认只读，不扫描、不上传、不修改）

严格遵守单任务原则。开始前报告当前目录、分支、已有改动、工具环境、准备修改文件、测试命令和风险。随后直接完成 TASK-000，不要提前执行 TASK-001 或编写 Android/后端业务代码。

不得读取或输出 .env.local 的值；只能报告需要的变量名是否配置。不得提交密钥、模型权重、人物素材、录音或原始业务资料。

完成后更新任务状态、PROJECT_STATE.md、memory/CURRENT_STATE.md 和 memory/HANDOFF.md，并给出真实命令、结果、日志路径、阻塞和下一任务建议。
```

TASK-000 通过后，再单独开新分支/会话执行 TASK-001。不要把多个任务合并为一条超长提示词。
