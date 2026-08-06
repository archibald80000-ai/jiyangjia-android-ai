# TASK-013: Connect Android, gateway, providers and both display modes

- **Status:** PARTIAL
- **Priority:** P0
- **Dependencies:** TASK-012
- **Branch:** `task/TASK-013-end-to-end-dialogue`
- **Owner:** Codex / assigned developer

## Objective

Connect Android, gateway, providers and the idle-video voice FAQ mode.

## Preconditions

- TASK-005/007/008/009/010/011/012 satisfy their required interfaces

## Scope and allowed changes

- `android-app/`
- `gateway/`
- `integration/`
- `tests/e2e/`
- `docs/evidence/TASK-013/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Production scale

## Detailed execution

1. Connect one interaction request across Android/gateway/ASR/knowledge-or-LLM/TTS and playback.
2. Propagate one request ID through every component and state transition.
3. Validate idle-video voice mode.
4. Test interrupt/cancel, provider timeout and network loss.
5. Run 30 controlled cycles and report failures, latency breakdown and fallback count.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python -m pytest tests/e2e -q
```
```powershell
.\android-app\gradlew.bat -p android-app connectedDebugAndroidTest
```

## Required deliverables

- [x] End-to-end demonstrable loop in local Android code and Gateway tests
- [x] 30-cycle stability/latency report
- [x] Fallback evidence for service/network/audio errors

## Acceptance criteria

- [x] Audio -> ASR -> answer -> TTS -> audio fetch works through Gateway with Mock and real Providers
- [x] Android code path records PCM, uploads WAV, downloads generated TTS audio, plays encoded audio and returns to idle-video fallback
- [x] Request ID correlation
- [x] 30-cycle stability test
- [ ] Android 12 real-device install, recording, playback and subtitle validation

## Stop / blocked conditions

- A destructive change, secret exposure, uncontrolled paid call or public network exposure would be required.
- A dependency is absent and cannot be safely installed inside the authorized scope.
- Real hardware/model/provider evidence is required but unavailable.
- Existing unrelated changes make safe staging impossible.

When blocked, complete all safe analysis, save sanitized evidence, set status to `BLOCKED` or `PARTIAL`, and state the exact unblock action.

## Required evidence

- Exact commands, versions, exit codes/results and timestamps.
- Changed files and `git diff --stat`.
- Sanitized logs/screenshots where meaningful.
- Artifact paths and SHA-256 for APK/packages.
- Hardware/environment details for device/GPU claims.
- Failed cases, untested paths and cost-bearing calls.

## Rollback

Restore the previous task commit/config, stop task processes, and remove only task-created local runtime files. Never touch `E:\work\积养家`, unrelated work or user secrets.

## Close-out

- [x] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [x] Add evidence links/results to this task.
- [x] Update `PROJECT_STATE.md`.
- [x] Update `memory/CURRENT_STATE.md`.
- [x] Replace `memory/HANDOFF.md` with current facts.
- [x] Update assumptions/open questions and add ADR if needed.
- [x] Recommend exactly one next task.

## Completion evidence

- Branch: `task/TASK-013-end-to-end-dialogue`
- Result: `PARTIAL`
- Commit: pending at close-out

Implemented:

- Android `GatewayClient` submits recorded PCM as WAV multipart to `/api/v1/dialogue/audio`.
- Android downloads generated `/api/v1/audio/{audio_id}` bytes, displays transcript/answer/source diagnostics and plays encoded TTS audio through `MediaPlayer`.
- Android state machine now covers `UPLOADING`, `WAITING_FOR_RESPONSE`, `PLAYING_ANSWER`, cancel and service error recovery.
- Local E2E tests cover Mock ASR -> RAG -> LLM -> TTS -> audio fetch with sources and request IDs.
- A 30-cycle Mock Gateway stability report passed 30/30 cycles with zero fallback.
- One real private-env Gateway smoke call passed through Doubao ASR, Doubao/Ark Embedding, Doubao/Ark LLM and Doubao TTS.

Evidence files:

- `docs/evidence/TASK-013/end-to-end-dialogue.md`
- `docs/evidence/TASK-013/task013-30cycle-pytest-report.json`
- `docs/evidence/TASK-013/task013-pytest-e2e-20260806.txt`
- `docs/evidence/TASK-013/task013-pytest-backend-full-20260806.txt`
- `docs/evidence/TASK-013/task013-android-unit-final-20260806.txt`
- `docs/evidence/TASK-013/task013-android-assemble-final-20260806.txt`
- `docs/evidence/TASK-013/task013-android-lint-final-20260806.txt`
- `docs/evidence/TASK-013/task013-apk-verification-20260806.txt`
- `docs/evidence/TASK-013/task013-adb-devices-20260806.txt`
- `docs/evidence/TASK-013/task013-connected-debug-android-test-20260806.txt`

Verified results:

- `python -m pytest tests\e2e -q`: 3 passed.
- `python -m pytest tests\e2e tests\knowledge tests\gateway tests\llm tests\asr tests\tts -q`: 37 passed.
- `.\android-app\gradlew.bat -p android-app --no-daemon testDebugUnitTest`: BUILD SUCCESSFUL.
- `.\android-app\gradlew.bat -p android-app --no-daemon assembleDebug`: BUILD SUCCESSFUL.
- `.\android-app\gradlew.bat -p android-app --no-daemon lintDebug`: BUILD SUCCESSFUL.
- APK: `android-app\app\build\outputs\apk\debug\app-debug.apk`, size `862144` bytes, SHA-256 `263B1FA8E8DB2198E93B4E4FFC85E715CEE2556E0511C67B002D7E588C76BC8E`.
- `adb devices -l`: no attached devices. `connectedDebugAndroidTest` built successfully but did not prove real-device execution.

Known issues:

- Android real-device recording/playback/subtitle behavior is unverified because no Android device was attached.
- Real ASR still has business-name homophone variation; this run recognized `积养家` as `季养家`.

Next action: execute exactly one next task, `TASK-014_TENCENT_GATEWAY_DEPLOYMENT.md`.
