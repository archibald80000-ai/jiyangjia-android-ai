# 积养家 AI 客服知识库

本目录是正式知识库在 GitHub 仓库中的公开分享入口。

## 当前版本

- 内容版本：积养家数字人知识库 v2.1
- 生产状态：41 approved、24 draft、0 rejected
- 索引状态：65 chunks、65 embeddings、65 个 2048 维 FAISS vectors
- Embedding：Doubao/Volcengine Ark，真实 Provider 已验收
- 客户可检索范围：仅 `approved`
- `draft`：不进入顾客答案
- 来源返回：稳定 `knowledge://<doc_id>` URI，不暴露本机原始资料路径

## GitHub 中包含什么

- [轻量 RAG 架构](../architecture/LIGHTWEIGHT_RAG.md)
- [MVP API 规范](../api/MVP_API_SPEC.md)
- [TASK-020A 正式导入验收](../evidence/TASK-020A/formal-knowledge-import-acceptance-20260807.md)
- [TASK-020B 数字人绑定验收](../evidence/TASK-020B/avatar-knowledge-binding-20260807.md)
- [TASK-020C 生产发布与分享状态](../evidence/TASK-020C/production-knowledge-avatar-sharing-20260807.md)
- [知识导入任务](../../tasks/TASK-020A_FORMAL_KNOWLEDGE_IMPORT_ACCEPTANCE.md)
- [数字人绑定任务](../../tasks/TASK-020B_AVATAR_KNOWLEDGE_BINDING.md)
- [生产发布任务](../../tasks/TASK-020C_PRODUCTION_KNOWLEDGE_AVATAR_SHARE.md)

## 为什么没有直接提交数据库

GitHub 公共仓库不保存以下运行数据和原始业务资料：

- `knowledge.db`
- `faiss.index`
- `import_all.json` 和原始导入批次
- PDF、DOCX、录音、客户资料
- Provider 密钥和 `.env.local`

这些文件包含运行状态、向量或未经公开授权的业务原文。GitHub 只保存代码、接口、公开安全的统计、验收结论和回滚说明。

## 实时接口

备案和腾讯云接入放行后的只读接口：

- 数字人演示：`https://ai-jiyangjia.cloud/demo/kiosk`
- 知识库状态：`https://ai-jiyangjia.cloud/api/v1/knowledge/status`
- 素材清单：`https://ai-jiyangjia.cloud/api/v1/assets/manifest`
- Display Profile：`https://ai-jiyangjia.cloud/api/v1/display/profile`

当前公网 HTTPS 仍被腾讯 Webblock/ICP 门禁重置。服务器内部经正式域名 TLS 已验证为 HTTP 200，但外部放行前不能把这些接口描述为公众可访问。

## 内容更新规则

```text
upload -> draft -> parse -> preview -> approve -> embedding -> publish
```

只有人工复核并发布的 `approved` 内容进入顾客问答。价格、库存、活动、医疗疗效和其他高风险问题必须使用已批准口径，否则转人工。
