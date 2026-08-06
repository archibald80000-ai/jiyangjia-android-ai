# TASK-014 Gateway 部署报告（重部署对齐）

日期：2026-08-06

## 一、已完成内容
- 已按 `docs/evidence/TASK-014/server-redeployment-request-20260806.md` 完成重部署：`/opt/jiyangjia-ai/backups/pre-task014-20260806-185559.tgz` 已备份旧部署。
- 已运行 `/opt/jiyangjia-ai/docker/docker-compose.yml` 并拉起 `jiyangjia-gateway`（`Up ... (healthy)`）。
- Nginx 反代可用，HTTP 外部访问通过 `120.53.86.89/health`。
- 关键目录已就位：`/opt/jiyangjia-ai/gateway`, `/opt/jiyangjia-ai/docker`, `/opt/jiyangjia-ai/logs`, `/opt/jiyangjia-ai/var/knowledge`。
- 知识库文件存在：`/opt/jiyangjia-ai/var/knowledge/jiyangjia.db`、`/opt/jiyangjia-ai/var/knowledge/faiss.index`。
- 容器日志轮转与系统日志策略已配置：Docker daemon `log-driver=json-file`、`max-size=10m`、`max-file=5`。
- 容器重启自恢复验证通过：`docker restart jiyangjia-gateway` 后可恢复 `healthy`，`/health` 200。

## 二、安装与版本
- 目标提交：`f3b406ca28222937a6f4c93bac524c48f0b95544`（显示短 SHA `f3b406c`）。
- `.env.local` 目标服务器位置：`/opt/jiyangjia-ai/secrets/.env.local`；旧的 `/opt/jiyangjia-ai/.env.local` 不应作为容器 env_file 使用。
- 运行目录 `/opt/jiyangjia-ai/gateway` 为部署副本（无 `.git`），代码元数据在 `/opt/jiyangjia-ai/releases/release-20260806-185559`：
  - remote: `https://github.com/archibald80000-ai/jiyangjia-android-ai.git`
  - branch: detached at `f3b406c`

## 三、真实接口验证（截至本轮）
- GET `/health`：200
- GET `/api/v1/health`：200
- GET `/api/v1/client/config`：200
- POST `/api/v1/knowledge/index`：200（`request_id` 存在）
- POST `/api/v1/knowledge/search`：200（`request_id`、`sources` 存在）
- GET `/api/v1/knowledge/status`：200（`embedding_ready: false`）
- POST `/api/v1/dialogue/text`：503（`BLOCKED_PROVIDER_CREDENTIALS`）
- POST `/api/v1/dialogue/audio`：503（参数修正后）
- GET `/api/v1/audio/{audio_id}`：未取到 `audio_id`（因 `dialogue` 阶段未放行）
- 外部访问 `/api/v1/health`：200

## 四、环境变量状态（仅状态）
- ASR/Doubao：`DOUBAO_ASR_APP_ID` / `DOUBAO_ASR_ACCESS_TOKEN` / `DOUBAO_ASR_API_KEY` / `DOUBAO_ASR_RESOURCE_ID`：`missing`
- TTS/Doubao：`DOUBAO_TTS_APP_ID` / `DOUBAO_TTS_ACCESS_TOKEN` / `DOUBAO_TTS_API_KEY` / `DOUBAO_TTS_SPEAKER` / `DOUBAO_TTS_RESOURCE_ID`：`missing`
- LLM：`DOUBAO_MODEL` / `DOUBAO_API_KEY`：`missing`
- Embedding：`DOUBAO_EMBEDDING_API_KEY` / `DOUBAO_EMBEDDING_MODEL`：`missing`
- 通用兼容：`OPENAI_COMPATIBLE_*` 系列：`missing`
- Knowledge 路径：`JIYANGJIA_KNOWLEDGE_DB_PATH` / `JIYANGJIA_KNOWLEDGE_FAISS_PATH`：`missing`（回退默认）

## 五、未完成项
- 未提供真实 Provider 凭据，不具备 `/api/v1/dialogue/text` 与 `/api/v1/dialogue/audio` 的真实端到端成功路径。
- 未完成 HTTPS/TLS 与 API 鉴权加固（当前仍为 IP + HTTP）。

## 六、建议
- 补齐 `/opt/jiyangjia-ai/secrets/.env.local` 中的 DOUBAO/Ark/OpenAI-compatible 凭据（按安全位保存，权限 `600`），并确认 Compose `env_file` 指向该路径。
- 先运行 `scripts/check_provider_env.py --env-file /opt/jiyangjia-ai/secrets/.env.local --compose-file /opt/jiyangjia-ai/docker/docker-compose.yml --require-real-mvp`，通过后再重启容器。
- 重启容器后复测 8 项 API，记录 `request_id/sources/audio_id`。
- 完成后将状态更新为 `TASK-014 DONE`，并进入 `TASK-015_ANDROID_DEVICE_ACCEPTANCE.md`。
