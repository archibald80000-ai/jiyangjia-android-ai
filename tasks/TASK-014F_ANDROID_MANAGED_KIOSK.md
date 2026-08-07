# TASK-014F - Android Managed Kiosk and Boot Recovery

- **Status:** PARTIAL
- **Priority:** P0
- **Dependencies:** TASK-014C DONE, TASK-014D DONE, TASK-014E DONE
- **Allowed scope:** Android device-admin/home/boot modules, provisioning docs, tests and evidence

## Goal

Make the store display recover after reboot and, where hardware provisioning allows, operate in true Android Lock Task mode.

## Deliverables

- Device Owner/DPC provisioning path and rollback instructions.
- Lock Task allowlisting with explicit runtime diagnostics.
- Persistent Home activity for managed dedicated devices.
- BootReceiver/fallback launch path and watchdog-safe state restoration.
- Clear limited-mode status when Device Owner is unavailable.

## Acceptance

- Managed test device reboots into the kiosk and cannot exit through Home/Overview/notifications.
- Unmanaged device does not falsely report Lock Task and remains manually recoverable.
- Boot with no network shows cached media, then synchronizes after connectivity returns.
- Ten reboot cycles and process-kill recovery complete without losing the active bundle.

## Manual Gate

The device owner confirmed that factory reset/provisioning as a fully managed device is permitted. True Lock Task still requires successful device or AVD provisioning evidence.

## Implementation result (2026-08-07)

- The APK now contains a minimal `DeviceAdminReceiver`, `BOOT_COMPLETED` receiver and Home activity declaration.
- Device Owner configuration allowlists only this package, disables Lock Task features/status bar and assigns persistent Home. Lock Task starts only when `isLockTaskPermitted()` is true and reports success only from `LOCK_TASK_MODE_LOCKED`.
- Unmanaged and partially configured devices explicitly report `limited_unmanaged` rather than true kiosk success.
- Boot starts a fresh Activity, restores TASK-014C cached content and never restores a prior dialogue generation.
- Unit tests, debug assembly and lint pass. Factory/ADB, QR, deprovisioning and recovery procedures are documented.
- No emulator/system image or Android device is installed on this workstation; `adb devices -l` returned no target. Device Owner, reboot and 10-cycle acceptance remain unverified, so status is `PARTIAL`.
