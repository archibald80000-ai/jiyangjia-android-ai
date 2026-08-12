# TASK-020G 积养家公开站点知识库 v2.3 验收

日期：2026-08-12

## 结论

用户授权的 Netlify 直接上传包已按只读来源归档到 `knowledge-public/v2.3/site/`，并以站点 `knowledge/index.json` 的结构化产品数据生成 47 条新增 approved 产品知识。v2.3 保留 v2.2 全部 204 条记录，生产状态现为 251 条文档、387 个知识块和 387 个 2048 维向量。

真实 Doubao Embedding 的 141 条产品问法验收全部 Top-3 命中，sources 完整率 100%，draft 泄露为 0。生产 `dialogue/text` 已通过 RAG、Doubao LLM、Doubao TTS 和音频下载。因此 TASK-020G 为 `DONE / PRODUCTION_PUBLISHED`。

## 公开包

- 只读来源：`E:\work\积养家\积养家知识库\04_数字化系统\00_当前发布版\积养家AI知识库_Netlify直接上传包_V2.1_原页整合培训版`。
- 公开站点：`https://jiyangjia-ai.netlify.app/`，验收时返回 HTTP 200、`text/html`，首页包含“积养家”。
- 仓库位置：`knowledge-public/v2.3/`。
- 公开镜像：135 个文件，总源包约 9.9 MB；每个文件的 SHA-256 均在 `manifest.json`。
- 知识记录：251 条，ID 唯一；227 approved、24 draft；最长正文 1396 字，低于 Gateway 5000 字限制。
- 导入批次：6 批，数量为 50、50、50、50、50、1；实际生产导入未提交 `import_all.json`。

## 灵活 RAG 调整

此前业务域依赖静态词表，新增产品“圣牧有机酸奶”会被归为 general，无法进入业务检索。现在分类逻辑保留显式通用知识意图的隔离，但对未知问法先查询当前 approved SQLite/FTS 语料；强词法命中时按 `dynamic_corpus` 进入业务 RAG。产品新增和改名主要由知识数据驱动，不再要求把每个产品名写进 Python 关键词表。

安全边界未改变：顾客检索仍只返回 approved；draft 不参与答案；未收录实时库存、活动、诊疗承诺和资料外事实不得补写。

## 自动化与真实检索

```text
pytest tests/knowledge/test_lightweight_rag.py tests/knowledge/test_answer_policy.py tests/knowledge/test_jiyangjia_site_knowledge_v23.py tests/knowledge/test_aiye_knowledge_v22.py -q
43 passed

real product search acceptance
provider=doubao
top3=141/141 (100%)
sources=141/141 (100%)
draft_leaks=0
```

代表性公网搜索：

| 问题 | Top-1 | 分数 | 来源 |
| --- | --- | ---: | --- |
| 圣牧有机酸奶是什么？ | `site_product_shengmu-yogurt` | 0.9534 | `https://jiyangjia-ai.netlify.app/products/shengmu-yogurt/` |
| 圣牧有机酸奶多少钱？ | `site_product_shengmu-yogurt` | 0.9521 | 同上 |
| 积养家是什么？ | `faq_brand_002` | 0.7428 | `knowledge://faq_brand_002` |

## 生产发布

- Provider readiness：Doubao ASR、TTS、LLM、Embedding 全部 ready；没有输出密钥值。
- 发布前备份：`/opt/jiyangjia-ai/backups/task-v23-production-20260812-024528`。
- 备份数据库 SHA-256：`9c50aceccac0fc31dd84e40f214c40dc733231ae1a306c904da3bb8af58f3523`。
- 备份 FAISS SHA-256：`13be507240a45f43f331c4c06542faa7b17aa0704159668dda7392d4d11166dc`。
- 发布后数据库：15,208,448 bytes，SHA-256 `07ff788def0950200550c9f055afcf0513379e0204c4c81586def57be9d68fea`。
- 发布后 FAISS：3,170,349 bytes，SHA-256 `9b47c558cbad313b6e63e092d2f4b87cf39a8f6c72290ee756f1609be33b4284`。
- 最终状态：227 approved、24 draft、0 rejected；387 chunks/embeddings/vectors，2048 dimensions。

6 个批次 request ID：

```text
56beedd5-d52f-4b6d-9a77-31967a925193
de287375-6f93-481c-af13-2d0602bb414d
54db32fb-b95a-44e9-9912-7ca365eacf2b
5ca8b788-1ac9-45c6-bee9-dd074a80b85c
ab53cf01-2d23-467a-9bb2-f5f96bd4ecec
caeb7483-1b4f-4fbd-bb02-a21fb4daa423
```

## 真实问答

- 问题：`圣牧有机酸奶是什么？`
- request_id：`6c450e16-3424-4892-9ef9-35b1f1a3c76e`
- RAG 来源：`圣牧有机酸奶`（approved）
- LLM：Doubao
- TTS：Doubao，`audio/mpeg`
- audio_id：`aud_fcfa710c9307447ba05d49a40faee187`
- 音频下载：HTTP 200，172,461 bytes
- 回答内容按来源说明产品类别、68 元/箱、200g×10，并明确配料、糖分、储存和保质期以包装为准。

## 回滚

停止 Gateway 写入后，从上述备份目录恢复 SQLite 与 FAISS 到同目录临时文件，核对 SHA-256，再以同文件系统原子替换活动文件并重建 Gateway。不得直接覆盖正在写入的 SQLite/FAISS。

## 未包含

- `.env.local`、Provider 密钥、SQLite、FAISS、录音和服务器备份均未进入 Git。
- 本任务不等于 Android 12 门店大屏真机验收。
