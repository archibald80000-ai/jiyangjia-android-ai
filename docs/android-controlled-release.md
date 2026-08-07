# Android controlled release and rollback

## Signing identity and custody

- The production keystore is created once by the approved release owner and never stored in this repository, an APK, a Gateway response or a build log.
- Keep two encrypted offline backups under two-person custody. Record each custodian, backup date, restore drill and the approved signing-certificate SHA-256 in the release register.
- Commit only the approved public certificate digest through the controlled replacement of `android-app/release/certificate-sha256.example.txt`.
- A lost signing identity prevents ordinary upgrades. Do not silently substitute a test key or create a new production identity.

Release builds require all of these environment variables or Gradle properties:

```text
JIYANGJIA_VERSION_CODE
JIYANGJIA_VERSION_NAME
JIYANGJIA_SIGNING_STORE_FILE
JIYANGJIA_SIGNING_STORE_PASSWORD
JIYANGJIA_SIGNING_KEY_ALIAS
JIYANGJIA_SIGNING_KEY_PASSWORD
```

`versionCode` must be allocated from the release register and be greater than every APK ever distributed for this package. Build, verify and hash with the project-local JDK/SDK:

```powershell
.\gradlew.bat clean assembleRelease
apksigner verify --verbose --print-certs app\build\outputs\apk\release\app-release.apk
Get-FileHash -Algorithm SHA256 app\build\outputs\apk\release\app-release.apk
```

Compare the signer SHA-256 with the approved register before publishing. Publish the APK only to trusted HTTPS, then configure the Gateway release manifest with its exact package, version, size, file hash and certificate hash.

## Installation behavior

The client downloads to app-private temporary storage and rejects a non-HTTPS URL, size mismatch, SHA-256 mismatch, wrong package, non-increasing version or certificate mismatch before opening a PackageInstaller session. A Device Owner requests no-user-action installation. An unmanaged device follows `STATUS_PENDING_USER_ACTION` and displays the Android confirmation UI.

## Rollback

Android package downgrade is not the rollback mechanism. Check out the previous stable source and assets, apply only required compatibility/security fixes, allocate a new version code greater than the failed release, sign with the same production identity, publish it as a new release and retain the incident linkage in release notes.

## Test certificate boundary

TASK-014G used a disposable two-day certificate only to verify that the signing pipeline fails closed and can produce an APK whose v1/v2/v3 signatures verify. The test keystore and APK were deleted. Its certificate digest is not an approved production identity and must never be published.
