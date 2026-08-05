# ADR-0004: Pinned upstream and adapter-first integration

- Status: Accepted
- Date: 2026-08-05

## Decision

Pull LiveTalking at a locked commit, keep upstream source out of normal project commits, and prefer external clients/adapters over direct core rewrites.

## Reason

This preserves upgradeability, auditability and separation between rendering and business logic.
