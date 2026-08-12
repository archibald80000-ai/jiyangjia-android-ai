# 积养家公开知识库 v2.3

这是当前积养家 Android 大屏 AI 客服使用的公开知识版本，可供员工浏览、培训、内容复核和 Gateway 导入。知识来自用户授权公开的“Netlify 直接上传包 V2.1 原页整合培训版”，原始目录保持只读。

公开站点：<https://jiyangjia-ai.netlify.app/>

## 当前内容

- 完整知识：251 条，其中 227 approved、24 draft。
- 继承 v2.2：204 条，不删除或覆盖旧 FAQ。
- 新增产品：47 条，由 `site/knowledge/index.json` 的 `products[]` 自动生成。
- 产品目录：[`catalog.json`](catalog.json)。
- 来源文档：26 份。
- 公开站点镜像：[`site/`](site/)，135 个文件。
- 文件清单和 SHA-256：[`manifest.json`](manifest.json)。
- 知识到来源映射：[`source-map.json`](source-map.json)。
- 141 条产品检索测试：[`test_questions.json`](test_questions.json)。

## 员工如何查阅

1. 在 [`catalog.json`](catalog.json) 按产品名称查看产品目录。
2. 在 [`import_all.json`](import_all.json) 查看完整问法、回答正文、审核状态和来源 URL。
3. 在 [`site/`](site/) 打开原始培训页面，核对产品故事、规格、价格和食用方式。
4. `approved` 可作为当前对外口径；`draft` 只供内部复核，不能作为顾客答案。

## 为什么不是写死的 RAG

产品清单不再写进业务代码。构建脚本读取公开站点的结构化 `products[]`，自动生成产品知识、问法、批次和来源映射。Gateway 对未知产品问法先查询当前 approved 语料；当 SQLite/FTS 有强匹配时，再进入 FAISS Top-K 检索。因此新增产品通常只需更新公开数据包并重新索引，不需要修改 Python 关键词表。

显式通用知识问题仍不会被强行拉入积养家知识库，资料未命中时继续安全转人工。

## Gateway 导入

生产导入前必须备份 SQLite 和 FAISS，并确认 Embedding Provider 为真实 Doubao。按 [`manifest.json`](manifest.json) 的 `batches` 顺序依次导入：

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\import_knowledge_package.py `
  --base-url https://ai-jiyangjia.cloud `
  --package-dir knowledge-public\v2.3
```

不要把 `import_all.json` 和分批文件重复导入。`import_all.json` 仅用于浏览、校验和离线交换。

## 验收状态

- 真实 Doubao Embedding：387 个 2048 维向量。
- 141 条产品问法 Top-3：141/141。
- sources 完整率：100%。
- draft 泄露：0。
- 生产数据：227 approved、24 draft。
- 证据：[`TASK-020G`](../../docs/evidence/TASK-020G/public-site-knowledge-v23-acceptance-20260812.md)。

资料公开不代表 AI 可以自由补写。未收录的产地、配料、价格、活动、库存、认证、疗效或研究结论不得自行生成；包装实时信息和门店实时情况应咨询工作人员。
