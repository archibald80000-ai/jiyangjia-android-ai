# ADR-0016: Separate phone demo and managed store Android variants

- Status: Accepted
- Date: 2026-08-12

## Context

The public debug APK contained both ordinary launcher behavior and managed-kiosk Home, boot, immersive and Lock Task capabilities. Those capabilities are correct for a provisioned store display but interfere with navigation on an ordinary phone.

## Decision

Build two terminal-mode product flavors from the same Android client. `phoneDemo` is the public, phone-safe experience and retains the current debug package identity for in-place upgrades. `storeKiosk` has a distinct package identity and alone declares Home, boot, Device Admin, package-install, immersive and Lock Task behavior.

The public website links to the phone build by default and labels the store build as managed-device-only. Both flavors keep the same Gateway, media/Profile, streaming dialogue and offline-content implementation.

## Consequences

- An ordinary phone can use Home, recent apps and notifications after upgrading the public APK.
- Managed-kiosk permissions cannot be accidentally activated from the public phone build.
- Store and phone acceptance are recorded separately; phone smoke evidence never completes Android 12 store-screen TASK-015.
- Build, signing and download checks must cover both variants.
