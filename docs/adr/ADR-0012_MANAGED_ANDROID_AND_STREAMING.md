# ADR-0012: Managed Android Client and Streaming Dialogue

- Status: Accepted
- Date: 2026-08-07

## Decision

Implement remote content/profile synchronization, deterministic profile rendering and Gateway-proxied streaming ASR before Android physical-device acceptance. Keep Provider credentials on the Gateway and preserve local media plus multipart WAV fallback.

Use Android fully managed Device Owner mode for true Lock Task and silent updates when the target hardware permits provisioning. Unmanaged installations remain supported as a limited fallback but cannot be described as locked or silently updatable.

## Consequences

- TASK-015 depends on TASK-014C through TASK-014G rather than beginning immediately.
- Production requires trusted HTTPS, a device provisioning decision and release signing-key custody.
- Automatic content changes become recoverable through checksum validation, atomic activation and a last-known-good cache.
- Streaming failures do not remove the current whole-WAV dialogue path.
