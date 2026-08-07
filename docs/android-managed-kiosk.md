# Android fully managed kiosk provisioning

True Lock Task is available only after the application is provisioned as Device Owner. Immersive full screen on an unmanaged device is reported as `limited_unmanaged` and is not acceptance evidence.

## Factory / development provisioning

1. Factory-reset the Android 12 device or create a clean Android 12 AVD with no accounts and no work profile.
2. Install the APK before adding accounts.
3. For a debug APK run:

```powershell
adb install -r android-app\app\build\outputs\apk\debug\app-debug.apk
adb shell dpm set-device-owner ai.jiyangjia.kiosk.debug/ai.jiyangjia.kiosk.KioskDeviceAdminReceiver
adb reboot
```

For a release build the component package is `ai.jiyangjia.kiosk/ai.jiyangjia.kiosk.KioskDeviceAdminReceiver`.

Verify after boot; do not infer the result from a successful provisioning command:

```powershell
adb shell dumpsys device_policy
adb shell dumpsys activity activities
adb shell am get-current-user
```

The application diagnostics must report `owner=true`, `permitted=true`, `locked=true` and `Kiosk=managed_locked`. Verify Home, Overview and notification access manually.

## QR provisioning

The enrollment QR must identify `ai.jiyangjia.kiosk/ai.jiyangjia.kiosk.KioskDeviceAdminReceiver`, a trusted HTTPS APK download URL and the release APK checksum. Generate the final QR only from the approved release manifest; do not commit a token, Wi-Fi password, private URL or placeholder checksum.

## Boot and recovery behavior

- `BOOT_COMPLETED` launches the kiosk and clears all in-memory dialogue/generation state.
- TASK-014C restores the last active private bundle before any network call and then performs an immediate foreground synchronization.
- An incomplete staging bundle is never activated. A failed decoder may restore `previous`.
- If OEM background-start policy blocks the receiver, record the firmware policy as a TASK-015 blocker; do not describe it as a successful boot recovery.

## Removing management

- Development-only Device Owners created from a test-only build may be removable with the platform `dpm remove-active-admin` command.
- A production fully managed Device Owner should be removed through the approved enterprise deprovisioning flow; when that is unavailable, factory reset is the recovery path.
- Before reset, retain only approved logs and record the active release/bundle versions. Never export credentials or private recordings.
