# ADR-0014: Canonical Production Domain

- Status: Accepted; public rollout blocked
- Date: 2026-08-07

## Decision

Use `https://ai-jiyangjia.cloud` as the only canonical production Gateway origin for Android, API documentation and operator links. Keep the IP TLS virtual host temporarily for rollback diagnostics, but do not use the IP HTTP endpoint in production Android configuration.

## Rationale

A stable HTTPS hostname decouples APK configuration from server IP changes and is required for secure content sync, WebSocket ASR and signed release delivery.

## Current rollout gate

DNS and server-side TLS are configured, but Tencent currently intercepts public domain traffic with a DNSPod webblock page. Public rollout and certificate renewal acceptance remain blocked until ICP/domain access onboarding is released.
