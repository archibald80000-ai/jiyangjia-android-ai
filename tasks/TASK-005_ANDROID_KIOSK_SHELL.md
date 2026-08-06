# TASK-005: Create the Android 12 landscape kiosk shell and local idle video

- **Status:** DONE
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

- [x] Buildable Android project source scaffold
- [x] Local idle-video/fallback implementation
- [x] Actual debug APK when environment permits
- [x] docs/evidence/TASK-005/android-shell.md

## Acceptance criteria

- [x] Gradle project builds
- [x] APK actually generated
- [x] Immersive landscape UI implemented in source
- [x] Local idle character video/fallback implemented without network
- [x] Config screen and health state implemented in source
- [x] No provider secrets added to APK source

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

## TASK-005 Result

- Source implementation completed for the Android landscape kiosk shell, idle local video resolution and offline fallback visual.
- Official Gradle Wrapper generated for Gradle `8.10.2`.
- Local ignored Android toolchain cache created under `.cache/android-toolchain` with Temurin JDK 17 and Android SDK API 35 components.
- Gradle `tasks`, `testDebugUnitTest assembleDebug` and `lintDebug` completed successfully.
- Debug APK generated at `android-app\app\build\outputs\apk\debug\app-debug.apk`; size `830932` bytes; SHA-256 `AA19DA758C8B319AD33B760127CD82E38385AA6CAF0B796FCB952E5166DE0896`.
- Evidence:
  - `docs/evidence/TASK-005/android-shell.md`
  - `docs/evidence/TASK-005/task005-verification-20260806.txt`
  - `docs/evidence/TASK-005/task005-environment-20260806.txt`
  - `docs/evidence/TASK-005/task005-toolchain-install-20260806.txt`
  - `docs/evidence/TASK-005/task005-gradle-build-20260806.txt`
  - `docs/evidence/TASK-005/task005-lint-20260806.txt`
  - `docs/evidence/TASK-005/task005-final-apk-verification-20260806.txt`
- Android 12 device install/rendering was not verified because no device was connected; `adb devices` returned an empty device list.
- Next unique action: execute TASK-007 Android USB/default microphone and speaker behavior.
