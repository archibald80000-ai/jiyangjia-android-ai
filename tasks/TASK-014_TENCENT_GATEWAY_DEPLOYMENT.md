# TASK-014: Deploy the lightweight gateway to Tencent Cloud

- **Status:** DONE
- **Priority:** P1
- **Dependencies:** TASK-013
- **Branch:** `task/TASK-014-tencent-gateway-deployment`
- **Owner:** Codex / assigned developer

## Objective

Deploy and validate the lightweight production gateway on Tencent Cloud with the real Provider chain.

## Preconditions

- TASK-013 local/backend E2E complete and Android device verification deferred
- Server access is authorized
- `/opt/jiyangjia-ai/secrets/.env.local` available

## Scope and allowed changes

- `deploy/`
- gateway deployment config
- `docs/evidence/TASK-014/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents, or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- GPU inference on the CPU-only Tencent Cloud server

## Detailed execution

1. Audit OS/network/service baseline and backup availability.
2. Reconfigure deployment to use `../secrets/.env.local` in `docker-compose` and restart/recreate containers.
3. Verify provider readiness and provider config via `scripts/check_provider_env.py --require-real-mvp`.
4. Run the complete MVP API acceptance set.
5. Record rollback point and operational notes.

## Required evidence

- Exact commands, versions, exit codes/results and timestamps.
- Evidence for env-file chain and provider readiness.
- Changed files and `git diff --stat`.
- Evidence log paths for endpoint acceptance and audio fetch.
- Real-world failures and retry notes (if any).

## Acceptance criteria

- [x] Deployment config uses `/opt/jiyangjia-ai/secrets/.env.local` and `0o600` mode
- [x] `/health` reachable
- [x] `/api/v1/health` reachable
- [x] `/api/v1/readiness` ready=true
- [x] `/api/v1/client/config` 可访问
- [x] `/api/v1/knowledge/status`、`/api/v1/knowledge/index`、`/api/v1/knowledge/search` 通过
- [x] `/api/v1/dialogue/text` 与 `/api/v1/dialogue/audio` 可返回 real chain 结果（以有效语音输入为准）
- [x] `/api/v1/audio/{audio_id}` 可下载 `audio/mpeg`

## Close-out

- [x] Set status to `DONE`.
- [x] Add evidence links/results to this task.
- [x] Update `PROJECT_STATE.md`。
- [x] Update `memory/CURRENT_STATE.md`。
- [x] Update `memory/HANDOFF.md`。
- [ ] Update assumptions/open questions and add ADR if needed.
- [x] Recommend exactly one next task.

## Reconciliation evidence（final）

- Result: `DONE`
- Evidence:
  - `docs/evidence/TASK-014/task014-provider-env-check-after-recreate-20260807.json`
  - `docs/evidence/TASK-014/task014-acceptance-summary-20260807-0943.json`
  - `docs/evidence/TASK-014/task014-dialogue-audio-retry-20260807-0944.json`
  - `docs/evidence/TASK-014/task014-remote-acceptance-final-after-recreate.json`
  - `docs/evidence/TASK-014/task014-remote-acceptance-final-20260807.json`
- Server: Tencent Cloud IP-only test host `120.53.86.89`, Ubuntu `24.04.4 LTS`, 2-core/1.9Gi/50G, CPU-only.
- Provider file chain: `/opt/jiyangjia-ai/secrets/.env.local` exists, readable, expected mode `0o600`.
- `docker-compose.yml` points to `../secrets/.env.local`.
- `/api/v1/readiness` shows ASR/TTS/LLM/Embedding both configured and ready.
- `dialogue/audio` 在有效语音输入下可完成 real chain；空白/无效音频样本会返回 `ASR_NO_TEXT`。`audio fetch` 可返回 `audio/mpeg`，在成功场景中返回 `request_id` 与 `sources`。
- `TASK-014A_ADMIN_CONTENT_DISPLAY.md` is the next single next task.
