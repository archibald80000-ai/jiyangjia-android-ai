# 积养家公开知识资料

本目录保存经用户明确授权公开的积养家数字人客服知识包，用于员工学习、对外宣发口径复核和 Gateway 导入。

## 当前发布

GitHub 员工分享地址：<https://github.com/archibald80000-ai/jiyangjia-android-ai/tree/main/knowledge-public/v2.3>

- [v2.3 当前正式公开知识库](v2.3/README.md)
- [v2.3 完整知识内容](v2.3/import_all.json)
- [v2.3 产品目录](v2.3/catalog.json)
- [v2.3 原始公开培训站点](v2.3/site/)
- [v2.3 Manifest 与 SHA-256](v2.3/manifest.json)

- [v2.2 爱野食材正式知识库](v2.2/README.md)
- [v2.2 完整知识内容](v2.2/import_all.json)
- [v2.2 产品目录](v2.2/catalog.json)
- [v2.2 原始公开 HTML](v2.2/sources/aiye-foods/)
- [v2.2 Manifest 与 SHA-256](v2.2/manifest.json)

- [v2.1 完整导入包](v2.1/import_all.json)
- [v2.1 第一批](v2.1/import_batch_01.json)
- [v2.1 第二批](v2.1/import_batch_02.json)
- [v2.1 Manifest](v2.1/manifest.json)

当前 v2.3 完整包包含 251 条：227 approved、24 draft；其中保留 v2.2 的全部 204 条，并从公开培训站点结构化产品目录新增 47 条 approved 产品知识。`draft` 仅供内部确认，不得直接作为顾客答案。

公开副本保留原始 ID、标题、正文和状态，只将工作站绝对路径标准化为 `knowledge://<document_id>`。原始目录 `E:\work\积养家\数字人知识库\08_导入包` 仍保持只读。

## 重新生成

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe scripts\build_public_knowledge_package.py `
  --source-dir "E:\work\积养家\数字人知识库\08_导入包" `
  --output-dir knowledge-public\v2.1
```

## 员工下载与学习

员工可以直接在 GitHub 中浏览 `import_all.json`，也可以下载本目录用于学习统一口径。每条记录包含标题、对外问法、回答正文、审核状态和稳定来源 ID。

- `approved`：当前可用于顾客问答和对外口径学习。
- `draft`：尚待人工确认，只能学习和复核，不能作为正式顾客答案。
- `source_uri`：公开副本统一为 `knowledge://<document_id>`，不依赖某台电脑的路径。

## 导入 Gateway

当前 `POST /api/v1/knowledge/index` 单次最多接收 50 条，因此 65 条完整包只能用于浏览、校验和离线交换；实际导入必须依次提交两个批次：

```powershell
$baseUrl = "http://127.0.0.1:8090"

Invoke-RestMethod -Method Post `
  -Uri "$baseUrl/api/v1/knowledge/index" `
  -ContentType "application/json; charset=utf-8" `
  -InFile "knowledge-public\v2.1\import_batch_01.json"

Invoke-RestMethod -Method Post `
  -Uri "$baseUrl/api/v1/knowledge/index" `
  -ContentType "application/json; charset=utf-8" `
  -InFile "knowledge-public\v2.1\import_batch_02.json"
```

不要再提交 `import_all.json`，也不要把完整包和两个批次重复导入，否则会重复执行 Embedding upsert。生产导入前必须先备份 SQLite 与 FAISS，并确认使用真实 Embedding Provider。

导入后必须检查：

```text
GET /api/v1/knowledge/status
POST /api/v1/knowledge/search
```

生产发布仍遵守 `approved` 可回答、`draft` 不泄露、风险问题转人工的规则。
