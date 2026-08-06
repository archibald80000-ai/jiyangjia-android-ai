# ADR-0007: Existing Tencent server is gateway-only

- Status: Accepted
- Date: 2026-08-05

## Decision

Use the Tencent Cloud no-GPU server for gateway, API calls, mini knowledge and logs. Do not host LiveTalking inference there. The observed 2026-08-06 allocation is 2 CPU cores, about 1.9Gi RAM, 50G disk and 10 Mbps bandwidth.

## Reason

Real-time model inference requires compatible GPU resources and the current memory budget is better reserved for a lightweight service layer.
