# ADR-0018: Public Resource Access Gate

- Status: Accepted and operational
- Date: 2026-08-12

## Context

The public digital-human page must remain immediately usable for voice and text consultation, while the navigation entries for the knowledge center and public materials need a lightweight shared-password gate. The underlying external resources remain public and are outside this Gateway's authorization boundary.

## Decision

Use a server-side entry gate with these constraints:

- Store only a PBKDF2-SHA256 password hash and an independent random HMAC signing secret in the server-only secrets file.
- Issue a signed 24-hour cookie with `HttpOnly`, `Secure` and `SameSite=Strict`.
- Fail closed when configuration is missing and apply a five-failure, 15-minute per-IP limiter.
- Redirect only to server-defined allowlisted destinations.
- Keep the virtual human, voice, text and APK entry points public.
- Keep `/demo/kiosk` navigation-free.
- Do not use browser storage for the password or session.

## Consequences

- This prevents casual access through the public navigation but is not access control for the original external resources.
- Revoking the session secret invalidates all active gate sessions.
- A full private-document requirement would need authentication and authorization at each underlying resource host.
