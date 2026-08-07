# TASK-014G - Android Release Signing and Controlled Update

- **Status:** PLANNED
- **Priority:** P0
- **Dependencies:** TASK-014F DONE, signing-key custody approved
- **Allowed scope:** Android release build/update modules, server release metadata, scripts, tests and evidence

## Goal

Create reproducible signed release APKs and a checksum/signature-verified update path suitable for the dedicated display.

## Deliverables

- Release signing configuration that reads key path/passwords only from ignored local or CI secrets.
- Signing key backup/custody runbook; no keystore in Git.
- Monotonic `versionCode`, release notes, APK SHA-256 and signing-certificate digest.
- HTTPS release manifest and verified APK download.
- Device Owner silent installation path; system-confirmed installer fallback for unmanaged devices.
- Rollback release procedure using a new higher version code built from prior known-good source.

## Acceptance

- Release APK verifies with `apksigner` and installs over the previous release without data loss.
- Wrong hash, wrong package, lower version and wrong signing certificate are rejected.
- Managed device update succeeds without leaving kiosk mode; unmanaged mode clearly requests system confirmation.
- Signing secrets, APK binaries and private keys remain outside Git.
