# TASK-014F - Android Managed Kiosk and Boot Recovery

- **Status:** PLANNED
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

The device owner must confirm whether factory reset/provisioning as a fully managed device is permitted. Without this approval, true Lock Task cannot be accepted.
