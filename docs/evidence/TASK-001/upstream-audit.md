# TASK-001 upstream audit

- Date: 2026-08-06
- Branch: `task/TASK-001-livetalking-upstream-audit`
- Upstream: `https://github.com/lipku/LiveTalking.git`
- Locked commit: `c963ad409c556918b7d23999bf87c47a7c05c932`
- Status: `DONE`

## Scope executed

- Re-ran deterministic bootstrap using the documented process-scoped Git HTTP/1.1 config.
- Verified `third_party/LiveTalking` is a real ignored Git checkout at the locked commit.
- Read upstream README, README-EN, LICENSE, API docs, config, app entry, route/session/WebRTC/avatar/TTS/LLM/plugin files relevant to this project.
- Created a project-facing upstream architecture, endpoint, asset, extension and compliance audit.
- Did not install model weights, run the service, run Wav2Lip, make paid API calls or edit upstream source.

## Verification commands

| Command | Result | Evidence |
|---|---|---|
| `powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap_livetalking.ps1` with process-scoped `http.version=HTTP/1.1` | Exit 0; locked checkout ready | `checkout-verification.txt` |
| `git -C third_party\LiveTalking rev-parse HEAD` | `c963ad409c556918b7d23999bf87c47a7c05c932` | `checkout-verification.txt` |
| `git -C third_party\LiveTalking status --short --branch` | `## HEAD (no branch)` with no changes | `checkout-verification.txt` |
| `git -C third_party\LiveTalking remote -v` | origin fetch/push is `https://github.com/lipku/LiveTalking.git` | `checkout-verification.txt` |
| Static source scan | Routes, plugin registrations, CLI args, env var names and requirements recorded | `static-source-signals.txt` |
| Special route scan | `/whep`, `/api/asr`, avatar route setup and static web route recorded | `special-route-signals.txt` |

## Upstream architecture summary

LiveTalking is an aiohttp + aiortc server. `app.py` parses config, loads the selected avatar model, initializes `session_manager`, creates `RTCManager`, registers `/offer`, `/record/{sessionid}`, generic routes, WHEP and static web pages, then listens on `0.0.0.0:<listenport>`.

Core layers:

- `server/rtc_manager.py`: creates WebRTC peer connections, answers JSON `/offer` and WHEP `/whep`, adds audio/video tracks from `HumanPlayer`, uses the configured STUN server and removes sessions on failed/closed connections.
- `server/session_manager.py`: singleton session registry, UUID session creation, maximum session gate, session builder hook and removal.
- `server/routes.py`: text/audio/control/admin/SSE routes against an existing avatar session.
- `avatars/base_avatar.py`: shared queueing, custom action state, TTS dispatch, audio file chunking, speaking state, recording and output push logic.
- `avatars/*_avatar.py`: model-specific loaders and inference for `wav2lip`, `musetalk` and `ultralight`.
- `registry.py`: plugin registry for `stt`, `llm`, `tts`, `avatar` and `output`.
- `streamout/*`: WebRTC, RTMP and virtual camera output implementations.

## Supported endpoints at locked commit

Business/control endpoints:

- `POST /offer`: JSON SDP offer, returns SDP answer and `sessionid`.
- `POST /whep`: WHEP-style `application/sdp`, returns SDP answer with `X-Session-ID`.
- `POST /human`: text drive, `type=echo` or `type=chat`, optional interrupt and TTS passthrough.
- `POST /humanaudio`: multipart audio upload for direct audio drive.
- `POST /interrupt_talk`: flushes TTS/ASR queues for a session.
- `POST /is_speaking`: returns current speaking state.
- `POST /record`: `start_record` / `end_record`.
- `GET /record/{sessionid}`: downloads generated MP4 if present.
- `POST /set_audiotype`: sets custom action/audio state.
- `GET /sse?sessionid=...`: Server-Sent Events from avatar session queues.

Admin/avatar/local routes:

- `GET /api/admin/config`
- `GET /api/admin/sessions`
- `POST /api/avatar/task`
- `GET /api/avatar/task/{task_id}`
- `DELETE /api/avatar/task/{task_id}`
- `GET /api/avatar/tasks`
- Conditional `GET /api/asr` WebSocket route only when `funasr` is importable.
- Static web files from `web/`, including `index.html`, `webrtcapi.html`, `webrtcapi-asr.html`, `avatar.html` and admin pages.

## Model and asset requirements

README quick start for Wav2Lip requires:

- `models/wav2lip.pth`, renamed from `wav2lip256.pth`.
- `data/avatars/wav2lip256_avatar1/`, extracted from `wav2lip256_avatar1.tar.gz`.

Code paths confirm:

- `app.py` loads Wav2Lip model from `./models/wav2lip.pth`.
- Wav2Lip, MuseTalk and Ultralight avatar loaders expect prepared folders under `./data/avatars/<avatar_id>`.
- Avatar generation writes uploaded temp files under `./data/tmp` and output under `./data/avatars`.
- Recording writes generated MP4 output under `data/record`.

TASK-001 did not verify the presence, license, hash or runtime usability of any model weight or avatar asset. That remains TASK-002/TASK-003 work.

## Network and runtime requirements

From README/config/source:

- Default HTTP listen port: `8010`.
- README says WebRTC deployment needs TCP `8010` and wide UDP availability.
- Default transport is `webrtc`; supported transports include `rtcpush`, `webrtc`, `rtmp` and `virtualcam`.
- Default STUN: `stun:stun.freeswitch.org:3478`.
- WHEP endpoint is registered manually after CORS setup and also handles `OPTIONS`.
- RTCPush default push URL points to an SRS-style WHIP endpoint.

These are upstream requirements only. Store-network WebRTC, TURN and firewall behavior are not verified.

## Provider and plugin observations

Plugin mechanism:

- `registry.py` supports `register`, `create` and `list_plugins`.
- Avatar plugins registered: `wav2lip`, `musetalk`, `ultralight`.
- TTS plugins found: `edgetts`, `gpt-sovits`, `cosyvoice`, `fishtts`, `tencent`, `doubao`, `azuretts`, `qwentts`, `omnitts`, `xtts`.

Relevant credential environment variable names observed:

- LLM/Qwen: `DASHSCOPE_API_KEY`.
- Doubao TTS: `DOUBAO_APPID`, `DOUBAO_TOKEN`.
- Tencent TTS: `TENCENT_APPID`, `TENCENT_SECRET_KEY`, `TENCENT_SECRET_ID`.
- Azure TTS: `AZURE_SPEECH_KEY`, `AZURE_TTS_REGION`.

No credential values were read or printed. These upstream provider plugins do not replace this project's Gateway Provider Adapter plan; the project still keeps ASR/LLM/TTS business calls server-side behind gateway adapters.

## Compliance and license notes

- Upstream repository code includes Apache License 2.0.
- README states that videos developed and published from this project on platforms such as Bilibili, WeChat Channels and Douyin must include a LiveTalking watermark/logo.
- README points to external model/avatar downloads. Code license does not prove model weight, avatar, voice, source video or likeness commercial rights.
- Public repo must not commit upstream model weights, private avatars, generated recordings or raw business/customer data.
- If any upstream source patch becomes unavoidable, project policy requires an adapter-first attempt and a patch ledger under `integration/livetalking_patches/`.

## Fit with this project

Good fit:

- WHEP/WebRTC and JSON `/offer` are present for Android WebView/WebRTC integration.
- `/human`, `/humanaudio`, `/interrupt_talk`, `/is_speaking`, `/record`, `/set_audiotype` and `/sse` match the planned TASK-004 contract surface.
- `wav2lip` is available and can be kept as the first baseline model.
- Registry/plugin design supports adapter-based integration without editing upstream.

Gaps or differences:

- LiveTalking's built-in LLM/TTS plugins can call providers directly; this project must route business ASR/LLM/TTS through the gateway instead of treating LiveTalking as the business brain.
- Upstream lacks our desired request_id/auth/rate-limit/error envelope; project adapter code must add correlation and safety.
- Upstream admin/avatar routes are unaudited for production exposure and should not be public on the store network.
- Default WebRTC NAT behavior relies on STUN/wide UDP; project deployment still needs TURN/firewall evidence.
- Recording writes MP4 files server-side; project privacy policy defaults to no raw customer retention.
- Local ASR endpoint can lazily download/load SenseVoice/FunASR models and is not part of early project scope.

## No upstream source changes

TASK-001 did not modify the ignored upstream checkout. Final required command:

```powershell
git -C third_party\LiveTalking status --short --branch
```

returned detached `HEAD` with no changed files.

## Next task

Proceed to `TASK-002_LIVETALKING_ENVIRONMENT.md` only after closing this task. TASK-002 should build an isolated LiveTalking runtime environment and record Python/FFmpeg/GPU/CUDA/PyTorch facts. Do not claim model or WebRTC success until TASK-003 evidence exists.
