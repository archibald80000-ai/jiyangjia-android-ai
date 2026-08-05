# ADR-0005: Native kiosk shell plus WebView first

- Status: Accepted
- Date: 2026-08-05

## Decision

Use a native Kotlin kiosk shell with WebView/WHEP/WebRTC content for the first Android integration rather than immediately rewriting a full native WebRTC stack.

## Reason

It is the shortest path to reproduce upstream behavior while retaining native control of device audio, fallback and kiosk state.
