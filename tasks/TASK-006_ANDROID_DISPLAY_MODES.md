# TASK-006: Implement idle-video and LiveTalking WebView/WHEP modes

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-005
- **Branch:** `task/TASK-006-android-display-modes`
- **Owner:** Codex / assigned developer

## Objective

Implement idle-video and LiveTalking WebView/WHEP modes.

## Preconditions

- TASK-005 is DONE
- A usable LiveTalking test endpoint exists or fallback-only testing is explicitly recorded

## Scope and allowed changes

- `android-app/`
- `docs/evidence/TASK-006/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Native WebRTC rewrite

## Detailed execution

1. Implement local idle-video loop with packaging/provisioning behavior that does not depend on network.
2. Implement LiveTalking WebView/WHEP page mode and required WebView media/microphone permission handling.
3. Load display mode and endpoint from non-secret configuration.
4. Implement health check, reconnect and automatic fallback without blank screen.
5. Test both modes independently and a forced failure transition.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
.\android-app\gradlew.bat -p android-app testDebugUnitTest
```
```powershell
.\android-app\gradlew.bat -p android-app assembleDebug
```
```powershell
adb logcat -c
```
```powershell
adb shell am force-stop <package>
```
```powershell
adb shell monkey -p <package> 1
```

## Required deliverables

- [ ] Dual-mode implementation
- [ ] Fallback/reconnect test evidence
- [ ] Updated APK checksum

## Acceptance criteria

- [ ] Local idle video loop
- [ ] LiveTalking page mode
- [ ] Config switch
- [ ] Service failure fallback
- [ ] Reconnect without blank screen

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

- [ ] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [ ] Add evidence links/results to this task.
- [ ] Update `PROJECT_STATE.md`.
- [ ] Update `memory/CURRENT_STATE.md`.
- [ ] Replace `memory/HANDOFF.md` with current facts.
- [ ] Update assumptions/open questions and add ADR if needed.
- [ ] Recommend exactly one next task.
