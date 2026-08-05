# 项目长期记忆入口

本文件是所有 Codex / Agent 会话的稳定入口。详细记忆拆分在 `memory/` 目录，任何会话不得只依赖聊天上下文。

## 永久核心事实

- 项目是积养家门店 Android 12 大屏 AI 语音客服与数字人终端。
- 本地开发目录为 `E:\work\安卓大屏AI语音客服系统`。
- 原始资料在 `E:\work\积养家`，当前不做复杂知识库，仅按需人工挑选少量已确认资料。
- 当前前端设备是 Android 12，不运行 Windows EXE、Python、CUDA 或本地大模型。
- 现有腾讯云为 8 核 CPU、4 GB 内存、10 Mbps、无 GPU。
- 前期以 LiveTalking 能力复现与集成为主。
- 必须同时保留 `idle_video` 无 GPU降级模式和 `livetalking_webrtc` 实时数字人模式。
- 所有真实密钥都在本地或服务器私密配置中，公共仓库不包含真实值。

## 会话恢复顺序

1. `memory/CORE_FACTS.md`
2. `memory/DECISIONS.md`
3. `memory/CURRENT_STATE.md`
4. `memory/HANDOFF.md`
5. `PROJECT_STATE.md`
6. 当前任务文件

## 更新纪律

- 稳定产品事实写入 `CORE_FACTS.md`。
- 已批准的架构选择写入 `DECISIONS.md` 并关联 ADR。
- 本轮真实完成/阻塞写入 `CURRENT_STATE.md`。
- 下一位 Agent 需要知道的命令、路径和未完成点写入 `HANDOFF.md`。
- 不把临时想法、密钥或未经验证的成功结论写入记忆。
