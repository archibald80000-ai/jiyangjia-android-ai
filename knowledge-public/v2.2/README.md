# 积养家 / 爱野食材知识库 v2.2

本目录是积养家 Android 大屏 AI 客服的公开知识库 v2.2，供员工学习、内容复核、Gateway 导入和数字人演示使用。

## 内容范围

- 完整包：204 条（180 approved、24 draft）。
- 继承 v2.1：65 条（41 approved、24 draft）。
- 爱野食材新增：139 条，由 25 个已授权 HTML 提取，全部由用户确认为人工审核通过的 `approved` 内容。
- 专项覆盖：24 个节气茶配方、19 味药食同源食材、11 个大有谷 SKU。
- 每条新增知识都可以通过 `source-map.json` 追溯到 HTML 文件、章节和 SHA-256。

原始公开页面位于 [`sources/aiye-foods/`](sources/aiye-foods/)。`.DS_Store`、`.workbuddy/`、密钥、数据库、FAISS、录音和服务器备份不在公开包中。

## 文件说明

- [`import_all.json`](import_all.json)：完整浏览和离线交换文件，不直接提交到 Gateway。
- `import_batch_01.json` 起：实际导入批次，每批最多 50 条，必须按编号顺序提交。
- [`manifest.json`](manifest.json)：版本、数量、状态、来源文件和全部 SHA-256。
- [`source-map.json`](source-map.json)：知识 ID 到原始 HTML/章节的映射。
- [`catalog.json`](catalog.json)：产品与专项覆盖目录。
- [`test_questions.json`](test_questions.json)：240 条检索验收问题。
- [`claim-audit.json`](claim-audit.json)：价格和健康表述的来源审校索引。

## 使用边界

资料公开不等于允许 AI 自由补写。数字人只能根据检索到的 approved 原文进行概括，不得补充原文没有的产地、工艺、价格、活动、认证、功效或研究结论。涉及诊断、治疗建议或未收录的实时价格/库存时，应转现场工作人员。

## Gateway 导入

生产导入前必须备份 SQLite 和 FAISS，并确认使用真实 Embedding Provider。按 `manifest.json` 中的批次顺序调用：

```text
POST /api/v1/knowledge/index
GET  /api/v1/knowledge/status
POST /api/v1/knowledge/search
```

不要提交 `import_all.json`，不要把完整包和批次重复导入。

## 2026-08-09 验收

- 本地隔离与腾讯云生产均使用真实 Doubao Embedding，FAISS 为 340 个 2048 维向量。
- Top-3 检索 240/240，sources 完整率 100%，draft 泄露 0。
- 生产知识路径：`/opt/jiyangjia-ai/current/var/knowledge/`。
- 生产回滚：`/opt/jiyangjia-ai/backups/task020f-20260809T035803Z`。
- 证据：[`docs/evidence/TASK-020F/aiye-knowledge-v22-acceptance-20260809.md`](../../docs/evidence/TASK-020F/aiye-knowledge-v22-acceptance-20260809.md)。
