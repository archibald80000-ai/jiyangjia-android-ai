# Gateway Project State

- 更新时间：2026-08-06
- 当前任务：TASK-014 腾讯云 Gateway 重部署
- 服务器部署目录：`/opt/jiyangjia-ai`
- 代码源：`/opt/jiyangjia-ai/releases/release-20260806-185559`
- 提交：`f3b406c`（目标 `f3b406ca28222937a6f4c93bac524c48f0b95544`）
- 运行目录：`/opt/jiyangjia-ai/gateway`（部署副本，非 `.git`）
- 容器：`jiyangjia-gateway` 健康运行中
- 健康接口：`/health`、`/api/v1/health` 200
- 诊断接口：`/api/v1/readiness` 用于查看 Provider configured/missing 状态，不输出密钥值
- 任务状态：`PARTIAL`（关键 Provider 凭据缺失）
- 未完成：修复 `/opt/jiyangjia-ai/secrets/.env.local` 与 Compose `env_file` 后，完成真实 `/api/v1/dialogue/text`、`/api/v1/dialogue/audio`、`audio_id` 取回
