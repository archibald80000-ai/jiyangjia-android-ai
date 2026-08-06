# LiveTalking integration scope

## Upstream lock

- Repository: `https://github.com/lipku/LiveTalking.git`
- Commit: `c963ad409c556918b7d23999bf87c47a7c05c932`
- Local path: `third_party/LiveTalking`
- TASK-001 audit evidence: `docs/evidence/TASK-001/upstream-audit.md`

## First capabilities to reproduce

1. WebRTC `/offer` or WHEP `/whep` session establishment.
2. `/human` with `type=echo` before LLM chat mode.
3. `/humanaudio` with known WAV input.
4. `/interrupt_talk`.
5. `/is_speaking`.
6. `/record` start/end and resulting file.
7. `/set_audiotype` with official/sample actions.
8. `/sse` start/end events.
9. Wav2Lip real-time path and actual FPS when GPU exists.

## TASK-001 audited upstream surface

At locked commit `c963ad409c556918b7d23999bf87c47a7c05c932`, source and docs confirm:

- `POST /offer` and `POST /whep` create WebRTC sessions and return a `sessionid` / `X-Session-ID`.
- `POST /human`, `POST /humanaudio`, `POST /interrupt_talk`, `POST /is_speaking`, `POST /record`, `GET /record/{sessionid}`, `POST /set_audiotype` and `GET /sse` exist for session control.
- Admin routes `/api/admin/config` and `/api/admin/sessions` exist and must not be exposed publicly without project auth controls.
- Avatar-generation routes under `/api/avatar/*` exist but are not part of the early Android kiosk path.
- Conditional local ASR WebSocket `/api/asr` exists only when FunASR is importable; this is not the initial project ASR route.
- Default listen port is `8010`; default transport is `webrtc`; default STUN is `stun:stun.freeswitch.org:3478`.
- Wav2Lip expects `models/wav2lip.pth` plus a prepared avatar folder under `data/avatars/<avatar_id>`.

These are static upstream audit facts, not runtime proof. TASK-001 did not install models, start a service, open WebRTC or measure FPS.

## Integration policy

- Prefer external adapter/client code in `integration/livetalking_client`.
- Use `config/upstream-lock.json` to fetch a deterministic commit.
- Do not rewrite upstream APIs in the first cycle.
- If a patch is unavoidable, store it in `integration/livetalking_patches/` with reason, upstream SHA, test and rollback.
- Never commit model weights or private avatar data.

## Project boundary after upstream audit

- LiveTalking remains a renderer/control endpoint, not the ASR/LLM/TTS business authority.
- Project gateway owns request IDs, auth, provider routing, knowledge policy, retention and user-safe errors.
- Built-in upstream Doubao/Qwen/Tencent/Azure plugins are useful references only; real project provider integration remains under TASK-009 to TASK-011.
- Upstream admin, avatar-generation and local ASR routes require explicit exposure decisions before any deployment.

## Fallback

When LiveTalking is unavailable, Android plays local idle video and gateway/Android plays TTS audio directly. The product must remain usable as a voice assistant.

## Performance evidence

Record hardware, driver, CUDA, PyTorch, model, avatar resolution, `inferfps`, `finalfps`, first-frame latency, first-audio latency and a 10-minute stability result. Never copy benchmark claims as local results.
