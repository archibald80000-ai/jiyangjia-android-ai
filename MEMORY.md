# 项目长期记忆入口

本文件是所有 Codex / Agent 会话的稳定入口。详细记忆拆分在 `memory/` 目录，任何会话不得只依赖聊天上下文。

## 永久核心事实

- 项目是积养家门店 Android 12 大屏 AI 语音客服与数字人终端。
- 本地开发目录为 `E:\work\ai-kefu\jiyangjia-ai`。
- 原始资料在 `E:\work\积养家`，当前不批量扫描；知识库改为轻量 RAG，只导入人工确认的小范围 Markdown/TXT/PDF/DOCX 资料。
- 当前前端设备是 Android 12，不运行 Windows EXE、Python、CUDA 或本地大模型。
- 现有腾讯云观测规格为 2 核 CPU、约 1.9Gi 内存、50G 磁盘、10Mbps、无 GPU；2026-08-06 服务器线程只验证到旧 mock Gateway，未部署当前 TASK-013 代码。
- 当前第一阶段以 Android 待机人物视频 + USB/默认麦克风 + FastAPI Gateway + 豆包 ASR/TTS + 方舟/豆包或 OpenAI-Compatible LLM + Embedding API + SQLite/FAISS 轻量 RAG 的语音问答 MVP 为主。
- LiveTalking、Wav2Lip、MuseTalk、实时口型和 WebRTC 数字人移到后续增强阶段；保留扩展接口但不阻塞第一阶段。
- Android 真机验收延后到 TASK-015；不阻塞 TASK-008 到 TASK-014 的本地开发、自动化测试和服务器部署准备。
- 所有真实密钥都在本地或服务器私密配置中，公共仓库不包含真实值。
- TASK-009 已验证真实豆包/火山引擎 TTS：默认使用 V3 单向 HTTP 流式合成，私有外部 env 真实调用生成 MP3；密钥值未打印、未提交。
- TASK-012 已验证轻量 RAG：SQLite 元数据、FTS5、FAISS Top-K、真实豆包/方舟 Embedding、人工确认 FAQ、sources 引用和安全转人工策略均已通过本地/真实向量评估。
- TASK-013 已完成 Android 到 Gateway 语音问答闭环的本地代码与后端验证：Android 录音上传、字幕/source 展示、TTS 音频取回和播放代码已实现，Mock 30-cycle 与真实 Provider Gateway 烟测通过；Android 12 真机验收仍待 TASK-015。
- TASK-013 后续加固了品牌名 ASR 归一化：常见 `ji/yang/jia` 同音漂移会在 Gateway 侧统一为“积养家”，并保留原始 `raw_text`。
- TASK-014 已完成腾讯云 Gateway 收口：生产 Compose 从 `/opt/jiyangjia-ai/secrets/.env.local` 加载真实 Provider，线上容器包含 FFmpeg；文本、Android WAV、MP3 均通过真实 ASR/RAG/LLM/TTS 与音频下载验收。部署测试知识已降为 draft，approved 仅保留 10 条受控 FAQ。
- TASK-014A 已完成本地轻量管理骨架：FastAPI 四页后台、知识审核发布、素材版本/manifest 和 Display Profile 持久化匹配均通过自动化与本地 HTTP 验证；尚未部署生产，也未导入正式资料或素材。

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
