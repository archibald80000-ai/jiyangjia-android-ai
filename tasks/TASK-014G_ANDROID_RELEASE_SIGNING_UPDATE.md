# TASK-014G - Android Release Signing and Controlled Update

- **Status:** PARTIAL
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

## Implementation result (2026-08-07)

- Release Gradle tasks fail during configuration unless a positive controlled `versionCode`, version name and all four external signing values are present. Release package remains `ai.jiyangjia.kiosk`.
- Gateway `/api/v1/client/release` fails closed until complete trusted-HTTPS metadata exists and emits a strong ETag when configured.
- Android downloads to private temporary storage, bounds declared size, checks SHA-256, package, exact/newer version and both manifest/installed certificate digests before committing PackageInstaller.
- Device Owner sessions request silent installation; unmanaged `STATUS_PENDING_USER_ACTION` launches the system confirmation intent.
- Unit tests reject wrong hash, package, lower version and certificate. Gateway tests cover unavailable and ETag-aware release manifests.
- A disposable test certificate built and verified a release APK with v1/v2/v3 signatures, package `ai.jiyangjia.kiosk`, versionCode `900001`; the keystore and APK were deleted and are not formal release artifacts.
- Formal signing identity/custody, trusted APK URL and managed-device N→N+1/N+2 installation are absent. Status remains `PARTIAL` and release acceptance is blocked.
