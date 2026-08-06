# TASK-005: Create the Android 12 landscape kiosk shell and local idle video

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-000
- **Branch:** `task/TASK-005-android-kiosk-shell`
- **Owner:** Codex / assigned developer

## Objective

Create the Android 12 landscape kiosk shell with local idle character video for the Phase 1 MVP.

## Preconditions

- TASK-000 is DONE
- JDK/Android SDK/Gradle availability is known

## Scope and allowed changes

- `android-app/`
- `docs/evidence/TASK-005/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- USB audio selection
- Real provider integration
- LiveTalking/WebRTC digital-human mode

## Detailed execution

1. Create one Android application with package ID and versioning documented.
2. Use Kotlin and a landscape immersive kiosk shell. Implement UI states and a hidden/protected development configuration entry.
3. Implement local idle character video or rights-clear fallback visual that does not depend on network.
4. Add network permission, but do not embed provider secrets or production credentials.
5. Create unit/smoke tests for state and configuration parsing.
6. Run Gradle build and record the actual APK path and SHA-256. If SDK components are missing, document exact requirements and complete safe project generation.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
java -version
```
```powershell
adb version
```
```powershell
.\android-app\gradlew.bat -p android-app tasks
```
```powershell
.\android-app\gradlew.bat -p android-app assembleDebug
```
```powershell
Get-FileHash android-app\app\build\outputs\apk\debug\app-debug.apk -Algorithm SHA256
```

## Required deliverables

- [ ] Buildable Android project
- [ ] Local idle-video/fallback display
- [ ] Actual debug APK when environment permits
- [ ] docs/evidence/TASK-005/android-shell.md

## Acceptance criteria

- [ ] Gradle project builds
- [ ] APK actually generated
- [ ] Immersive landscape UI
- [ ] Local idle character video/fallback visible without network
- [ ] Config screen and health state
- [ ] No provider secrets in APK

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
