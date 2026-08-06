# Handoff

## Current task

- Completed task: `TASK-001_LIVETALKING_UPSTREAM_AUDIT.md`
- Status: `DONE`
- Current branch: `task/TASK-001-livetalking-upstream-audit`
- Project path: `E:\work\ai-kefu\jiyangjia-ai`
- Raw materials path: `E:\work\积养家` (read-only; not scanned or modified)

## Read first

1. `CODEX_START_HERE.md`
2. `AGENTS.md`
3. `MEMORY.md`
4. `PROJECT_STATE.md`
5. `docs/22_DELIVERY_BLUEPRINT.md`
6. `docs/03_LIVETALKING_SCOPE.md`
7. `tasks/TASK-002_LIVETALKING_ENVIRONMENT.md`
8. `docs/evidence/TASK-001/upstream-audit.md`

## What is verified

- `third_party/LiveTalking` is a real ignored Git checkout at locked commit `c963ad409c556918b7d23999bf87c47a7c05c932`.
- Upstream remote is `https://github.com/lipku/LiveTalking.git`.
- The ignored upstream checkout remained unmodified during TASK-001.
- LiveTalking source/docs at the locked commit expose `/offer`, `/whep`, `/human`, `/humanaudio`, `/interrupt_talk`, `/is_speaking`, `/record`, `/record/{sessionid}`, `/set_audiotype`, `/sse`, admin routes, avatar task routes and conditional `/api/asr`.
- Default upstream listen port is `8010`; default transport is `webrtc`; default STUN is `stun:stun.freeswitch.org:3478`.
- Wav2Lip requires `models/wav2lip.pth` and prepared avatar assets under `data/avatars/<avatar_id>`.
- Upstream code has Apache-2.0 license text, but model weights, avatars, voices and likeness/source-video rights remain separate unresolved asset obligations.

## What is not verified

- LiveTalking dependency installation and Python runtime compatibility.
- Model weight/avatar presence, hashes, licenses or runtime usability.
- Wav2Lip inference, WebRTC media path, `/offer` or `/whep` runtime success.
- Android APK, USB microphone, speaker routing, Doubao ASR/TTS/LLM and mini FAQ behavior.

## TASK-001 evidence

- `docs/evidence/TASK-001/checkout-verification.txt`
- `docs/evidence/TASK-001/static-source-signals.txt`
- `docs/evidence/TASK-001/special-route-signals.txt`
- `docs/evidence/TASK-001/upstream-audit.md`
- `docs/evidence/TASK-001/task001-final-verification.txt`

## Next action

Start `TASK-002_LIVETALKING_ENVIRONMENT.md` on a new task branch/session:

```powershell
git switch -c task/TASK-002-livetalking-environment
```

TASK-002 should create an isolated reproducible LiveTalking runtime environment and record Python, FFmpeg, CUDA/GPU and PyTorch facts. Do not claim model/WebRTC success until TASK-003.
