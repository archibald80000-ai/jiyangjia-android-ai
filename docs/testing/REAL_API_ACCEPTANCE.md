# Real API Acceptance

Updated: 2026-08-06

## Purpose

This document defines the gate for claiming real provider integration. Passing TASK-008 tests does not mean Doubao, Volcengine Ark, OpenAI-compatible LLM, or embedding APIs are connected.

## Required Providers

- Doubao ASR.
- Doubao TTS.
- Doubao / Volcengine Ark LLM.
- OpenAI-compatible fallback LLM.
- Embedding API.

## Secret Handling

- Secrets are read only from `.env.local` in local development or server environment variables in deployment.
- Secrets are never committed, printed, copied into Android, or returned by diagnostics.
- Status output may only say `configured`, `missing`, or `disabled`.

## Provider Gates

Each real provider task must include:

- current official API documentation source and access date;
- exact environment variables required;
- one small approved integration test;
- request timeout and finite retry;
- sanitized error mapping;
- cost-control notes;
- evidence log with request IDs and no secret values.

## MVP Real API Flow Gate

The real API MVP is accepted only when:

```text
Android/local audio sample
-> Doubao ASR transcript
-> RAG Top-K approved sources
-> Doubao/Ark LLM grounded answer
-> Doubao TTS audio
-> audio_id fetch works
```

Missing credentials must be reported as `BLOCKED_PROVIDER_CREDENTIALS`, not replaced with Mock while claiming real success.
