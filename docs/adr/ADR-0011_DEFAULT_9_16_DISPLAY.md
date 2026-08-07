# ADR-0011: Default 9:16 Portrait Display

- Status: Accepted
- Date: 2026-08-07

## Decision

Use the `1080x1920` portrait Display Profile as the Phase 1 product default across the Gateway public API, admin creation form and Android kiosk orientation. Keep the existing landscape and custom profiles available for explicit device matching.

Existing admin SQLite databases apply the new default through a recorded one-time migration. After that migration, an administrator may select another default and a process restart will preserve the choice.

## Consequences

- A new or unconfigured client resolves to a 9:16 portrait presentation.
- Android uses portrait orientation by default and must be rebuilt before device testing.
- Existing published assets may require portrait-safe framing or replacement; code cannot prove their visual suitability.
- Real-device visual, touch, subtitle-safe-area and media crop acceptance remains part of TASK-015.
