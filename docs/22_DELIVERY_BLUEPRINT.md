# Delivery blueprint

This document is the controller view for turning the current framework into a sustainable, verifiable and deployable Android 12 store AI voice service project.

## North star

Deliver a store-facing Android 12 large-screen APK that can:

1. stay visually alive with a local idle human video;
2. receive bounded customer speech through USB or default microphone input;
3. send audio to a lightweight gateway with one `request_id`;
4. answer through Mock, reviewed FAQ, LLM and provider adapters in that order;
5. synthesize and play speech through speakers;
6. optionally route the same answer to a pinned LiveTalking WebRTC/WHEP digital-human renderer;
7. recover to `idle_video` when network, provider or LiveTalking rendering fails.

## System contracts

### Android client

- Owns kiosk UI, landscape immersive mode, local idle video, audio device selection, recording, playback, client status and non-secret configuration.
- Does not store provider API keys, raw business material, model weights or private avatar assets.
- Emits state transitions and selected device information with the active `request_id`.

### Gateway

- Owns session creation, device authentication, provider routing, answer policy, mini FAQ, logging, retention and provider error mapping.
- Runs within the 8 vCPU / 4 GB / 10 Mbps Tencent Cloud budget until measurements justify a change.
- Exposes stable `/api/v1/**` contracts and short-lived authenticated audio resources.

### LiveTalking node

- Remains a pinned upstream rendering engine controlled through adapter/client code.
- Is not the source of business truth and is not required for `idle_video` voice service.
- Requires real model, avatar, GPU, WebRTC and FPS evidence before any "works" claim.

## State machine

```text
INITIALIZING
  -> IDLE
  -> LISTENING
  -> RECOGNIZING
  -> THINKING
  -> SPEAKING
  -> IDLE

Any active state
  -> NETWORK_ERROR | DEVICE_ERROR | SERVER_ERROR | PROVIDER_ERROR | RENDERER_ERROR
  -> FALLBACK_IDLE_VIDEO
  -> IDLE
```

No state may produce a blank screen, leak diagnostics to customers or require app reinstall as the normal recovery path.

## Task dependency gates

| Gate | Tasks | Exit condition | Next route |
|---|---|---|---|
| G0 bootstrap | TASK-000 | Fixed path, branch, repository structure, secrets, config examples and upstream bootstrap are verified or blockers recorded | TASK-001 only after bootstrap gates pass |
| G1 upstream | TASK-001 to TASK-004 | Locked LiveTalking checkout, runtime, Wav2Lip baseline and core APIs are evidenced | Android shell work may begin |
| G2 kiosk | TASK-005 to TASK-007 | APK builds, display modes work, USB/default audio behavior is measured | Gateway/provider loop can consume real device constraints |
| G3 service | TASK-008 to TASK-012 | Gateway contracts, Mock, TTS, ASR, LLM and mini FAQ pass tests with cost guards | End-to-end loop |
| G4 pilot loop | TASK-013 | Android to gateway to answer to TTS/playback works for controlled cycles with request correlation | Deployment hardening |
| G5 deployment | TASK-014 to TASK-015 | Tencent gateway and real Android device pass security, recovery and long-run checks | Expansion decisions |
| G6 expansion | TASK-016 to TASK-017 | Wav2Lip pilot evidence exists before MuseTalk/formal knowledge work | Adopt, defer or reject by evidence |

## Verification ladder

Claims must climb this ladder and state the highest rung actually reached:

1. `DOCUMENTED`: design, contract or task exists.
2. `STATIC_VERIFIED`: repository, schema, secret and syntax checks pass.
3. `LOCAL_MOCK`: deterministic tests pass without hardware, paid APIs or GPU.
4. `LOCAL_REAL`: real local tool/provider/model/device evidence exists.
5. `DEVICE_REAL`: Android 12 physical device evidence exists.
6. `CLOUD_REAL`: Tencent Cloud or provider evidence exists with sanitized logs.
7. `PILOT_READY`: 30-cycle and recovery checks pass with known residual risks.

Mock, static or partial evidence must never be described as device, provider, APK, GPU or production success.

## Acceptance spine

Every task close-out must include:

- exact commands and exit results;
- evidence paths under `docs/evidence/TASK-###/`;
- changed files and whether they are within task scope;
- secret/model/audio/data tracking checks when relevant;
- untested paths and blockers;
- rollback instructions;
- exactly one recommended next task or unblock action.

## Rollback strategy

- Keep one task per branch.
- Commit only task-scoped files after reviewing `git diff`.
- For generated local runtime files, remove only the files created by the task.
- For upstream changes, prefer adapter code; any patch needs a patch ledger entry, tests and removal condition.
- For deployment, record previous service config, process state, backup path and health check before changing production.

## Long-term route

```text
TASK-000 bootstrap evidence
-> TASK-001 locked upstream audit
-> TASK-002 isolated LiveTalking runtime
-> TASK-003 Wav2Lip WebRTC/WHEP baseline
-> TASK-004 LiveTalking API contracts
-> TASK-005 Android landscape shell and APK
-> TASK-006 idle_video / livetalking_webrtc display modes
-> TASK-007 USB/default audio validation
-> TASK-008 lightweight gateway contracts
-> TASK-009 TTS providers
-> TASK-010 ASR providers
-> TASK-011 LLM router
-> TASK-012 reviewed mini FAQ
-> TASK-013 end-to-end dialogue loop
-> TASK-014 Tencent Cloud gateway deployment
-> TASK-015 Android 12 device acceptance
-> TASK-016 MuseTalk evaluation after pilot
-> TASK-017 formal knowledge base after pilot
```

The route is intentionally conservative: visible and audible `idle_video` voice service is the reliability baseline; LiveTalking, MuseTalk and formal knowledge expansion are upgrades that must earn their place with evidence.
