# TASK-020F 爱野食材公开知识库 v2.2 验收

日期：2026-08-09

## 结论

TASK-020F 的知识整理、真实 Embedding 隔离验收和腾讯云生产发布通过。知识状态为 204 条文档，其中 180 approved、24 draft；FAISS 为 340 个 2048 维向量。生产 Top-3 检索 240/240，通过率和 sources 完整率均为 100%，draft 泄露为 0。

公网 `https://ai-jiyangjia.cloud/health` 仍在到达 Nginx 前被腾讯云域名访问管控重置。该问题属于既有 TASK-014H，不影响服务器内 Gateway、生产知识数据和本次 SSH 隧道验收，但外部 Demo 仍不可用。

## 公开来源与知识包

- 原始目录只读：`E:\work\贝贝灵科技\0807-产品手册与网站展示\爱野食材(1)\爱野食材`。
- 25 个根目录 HTML 已逐字节归档到 `knowledge-public/v2.2/sources/aiye-foods/`。
- `manifest.json` 保存每个源文件的字节数和 SHA-256。
- 排除了 `.DS_Store`、`.workbuddy/`、密钥、数据库、FAISS、录音和服务器备份。
- v2.1 的 65 条记录全部保留；新增 139 条 `aiye_` 记录全部为用户确认的 approved。
- 覆盖 24 个节气、19 味药食同源食材、11 个大有谷 SKU 和 1 个大有谷产品目录。
- 完整包 204 条；实际导入使用 5 个动态批次，数量为 50、50、50、50、4，未提交 `import_all.json` 到 Gateway API。

## 本地隔离验收

- Gateway：`127.0.0.1:8092`。
- 数据：忽略目录 `var/task020f/20260809T083154Z/candidate/`。
- Provider：Doubao ASR、Doubao TTS、DeepSeek LLM、Doubao Embedding。
- 检索：240/240，Top-3 100%，sources 100%，draft 泄露 0。
- FAISS：340 vectors，2048 dimensions。
- 文本对话：6/6 matched，均返回 request_id、approved sources、audio_id 和可下载 `audio/mpeg`。
- 音频对话：使用豆包 TTS 合成的短商品问答作为输入；Doubao ASR -> RAG -> DeepSeek LLM -> Doubao TTS 通过。这是合成语音，不是 Android 或真人麦克风证据。

## 生产发布

- 生产主机：`120.53.86.89`。
- 实际数据库：`/opt/jiyangjia-ai/current/var/knowledge/jiyangjia.db`。
- 实际索引：`/opt/jiyangjia-ai/current/var/knowledge/faiss.index`。
- 发布前状态：41 approved、24 draft、65 vectors、2048 dimensions。
- 回滚备份：`/opt/jiyangjia-ai/backups/task020f-20260809T035803Z`。
- 备份数据库 SHA-256：`0a92df50797aa9abeb021ce6626e8787d949c190036c7097ad0e9b10b379fc76`。
- 备份 FAISS SHA-256：`d3f43449155d04f333032601ad58d5cb7e8b5d3c5c67f1e6ce034ad4d648ed40`。
- 发布后数据库 SHA-256：`f241605e10cd68d648f6b8896fd8573f91f96c02c403eeaf198a05c7b7e8a0bd`。
- 发布后 FAISS SHA-256：`b08be7d6f9b5cf8c1847fe9c90e284209b50dc0f1a385c8a039f9303f63ba161`。
- 容器：`jiyangjia-gateway` running/healthy，8080 仅绑定 `127.0.0.1`。
- Provider readiness：ASR/TTS/LLM/Embedding 均 ready；未打印密钥值。

生产完整验收结果：

- 导入：5/5 批次成功。
- 最终状态：180 approved、24 draft、340 chunks/embeddings/vectors、2048 dimensions。
- 检索：240/240，平均 151.9 ms，最大 1018.2 ms。
- 文本对话：6/6 matched。
- 音频对话：HTTP 200，ASR 转录后 matched，返回 3 个 approved sources 和 52,845-byte `audio/mpeg`。

代表性请求：

| 问题 | request_id | sources | audio_id | 耗时 |
| --- | --- | --- | --- | --- |
| 飞鸡蛋品牌故事 | `task020f-dialogue-01` | 3 | `aud_47c9d095f1b84187ac46f01d1e58fbc1` | 10174.1 ms |
| 福人五常大米规格价格 | `task020f-dialogue-02` | 3 | `aud_2c08c9bf46b04ff59f9e166bce5b6542` | 2370.5 ms |
| 立秋养生茶 | `task020f-dialogue-03` | 2 | `aud_82db000f6cbc457689dab85e05836a49` | 4022.6 ms |
| 生姜特点 | `task020f-dialogue-04` | 3 | `aud_411884eb32ae46a4815fa0ff40ec347a` | 5551.0 ms |
| 金华古法酱油工艺 | `task020f-dialogue-05` | 3 | `aud_36e263055e4140939147cb37bf91f1dc` | 6868.3 ms |
| 大有谷产品目录 | `task020f-dialogue-06` | 1 | `aud_463c8939a7da45488780def611e48dc8` | 4942.9 ms |
| 合成语音回灌 | `task020f-dialogue-audio-01` | 3 | `aud_47b98d1a244147ada383e9d8dbf867c0` | 3539.8 ms |

## 健康表述加固

人工复核发现首轮生姜回答把资料健康表述扩写成了确定性措辞。`GROUNDING_SYSTEM_PROMPT` 已加固为：健康、营养和传统食养内容必须明确归因于资料或传统说法，不得扩写为疗效、治疗建议或诊断。

加固后生产抽查：

- `task020f-health-audit-01`：生姜回答明确使用“资料里说”，无 `管用/能治疗/能治好/治愈/保证疗效` 命中，3 个 approved sources，TTS 成功。
- `task020f-health-audit-02`：立秋茶回答明确使用“按咱们积养家的资料”，2 个 approved sources，TTS 成功。

加固后追加全量对话复跑遇到一次可重试 502；此前完整生产验收和两条加固后抽查均已通过。该偶发 Provider 稳定性风险保留记录，不冒充零故障。

## 实际测试

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\knowledge\test_aiye_knowledge_v22.py tests\knowledge\test_lightweight_rag.py -q
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\llm\test_openai_compatible_providers.py tests\knowledge\test_aiye_knowledge_v22.py tests\knowledge\test_lightweight_rag.py -q
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\run_task020f_acceptance.py --base-url http://127.0.0.1:18092 --package-dir knowledge-public\v2.2 --output var\task020f\20260809T083154Z\production-acceptance.json
```

结果：静态知识测试 23 passed；LLM/知识组合测试 36 passed；生产完整验收 `ok=true`。

## 回滚

如生产数据回归，停止 Gateway 写入后，从 `/opt/jiyangjia-ai/backups/task020f-20260809T035803Z/knowledge/` 将数据库和索引复制到同目录临时文件，核对 SHA-256，再使用同文件系统原子 `mv` 替换活动文件，最后只重建 Gateway 并复核 readiness/status。不得直接覆盖正在写入的 SQLite/FAISS。
