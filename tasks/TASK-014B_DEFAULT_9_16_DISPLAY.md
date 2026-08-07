# TASK-014B - 默认 9:16 展示适配

- **Status:** DONE
- **Priority:** P1
- **Dependencies:** TASK-014A DONE
- **Scope:** Display defaults only; no knowledge, deployment or repository-cleanup changes

## Goal

Make `1080x1920 portrait` the default presentation for the Gateway, admin display form and Android kiosk while retaining all alternate Display Profiles.

## Acceptance

- Fresh and existing admin databases resolve `display-1080x1920` as the migrated default.
- A later administrator-selected default survives process restart.
- `GET /api/v1/display/profile` without query parameters returns the portrait profile.
- The admin new-profile form starts at `1080x1920 portrait`.
- Android Manifest and activity runtime orientation both use portrait.
- Gateway tests and Android build checks pass.

## Exclusions

- No production deployment.
- No knowledge-base modification.
- No Android physical-device acceptance.
- No formal avatar/background media approval.

## Verification (2026-08-07)

- `python -m pytest tests/admin/test_admin_content_display.py -q`: `11 passed`.
- `python -m pytest tests -q`: `56 passed`.
- Gradle `testDebugUnitTest lintDebug assembleDebug`: `BUILD SUCCESSFUL`.
- Debug APK: `android-app/app/build/outputs/apk/debug/app-debug.apk`, 863175 bytes, SHA-256 `C4213EC72364E12C02BD57191B3DCDA600FD291D0E7B7C320BF054E18A248965`.
- APK manifest inspection reports `screenOrientation=1` (`portrait`).
- Android physical-device behavior remains unverified.
