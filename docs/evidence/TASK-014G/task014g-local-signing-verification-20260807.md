# TASK-014G local verification — 2026-08-07

## Fail-closed build

Running `gradlew.bat assembleRelease` without release parameters exited 1 during configuration with `Release requires positive JIYANGJIA_VERSION_CODE`.

## Disposable test-only signing pipeline

- Generated an ignored two-day RSA test keystore in `tmp/` without printing its password.
- Built release package `ai.jiyangjia.kiosk`, versionCode `900001`, versionName `0.0.0-task014g-test-only`.
- `apksigner verify --verbose --print-certs` reported `Verifies` and v1/v2/v3 `true`.
- Test-only APK size: `4997277` bytes.
- Test-only APK SHA-256: `1F94FBEC30A119E0617705FE74EC357E043CE4BF1BE8BF2BB8F67AFC29CA3A41`.
- Test-only certificate SHA-256: `F9FD083C9392DD15BBB77E97EE564E59B2F3A8FA505FD792626504DC353CEB64`.
- The disposable keystore and test APK were deleted after verification. This digest is deliberately not copied into the release certificate register.

## Automated checks

- Gateway release-manifest tests: 2 passed.
- Android release-policy tests cover accepted metadata and rejection of wrong hash, package, non-newer version and certificate.
- Debug unit tests, lint and assembly pass; full regression is recorded in TASK-015 evidence.

## Blockers

- No approved production keystore, custodians or restored-backup proof.
- No trusted HTTPS APK publication URL.
- No Android 12 managed device or AVD for N→N+1 silent install, unmanaged confirmation or N+2 rollback.
- Status remains `PARTIAL`.
