# ADR-0007: Existing Tencent server is gateway-only

- Status: Accepted
- Date: 2026-08-05

## Decision

Use the 8C/4G/10M no-GPU server for gateway, API calls, mini knowledge and logs. Do not host LiveTalking inference there.

## Reason

Real-time model inference requires compatible GPU resources and the current memory budget is better reserved for a lightweight service layer.
