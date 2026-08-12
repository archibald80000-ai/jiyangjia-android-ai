# TASK-021A Public Resource Access Gate

## Status

`DONE / PRODUCTION_PUBLISHED`

## Goal

Preserve the public virtual-human, real-time voice, text consultation and APK download experience while placing an entry gate in front of the `知识中心` and `公开资料` navigation actions.

## Delivered

- Added `POST /api/v1/public-access/login`, `GET /api/v1/public-access/session` and `POST /api/v1/public-access/logout`.
- Added fixed allowlisted redirects at `GET /access/go/knowledge-center` and `GET /access/go/public-materials`.
- Added PBKDF2-SHA256 password verification, signed HMAC sessions, 24-hour expiry and per-IP failed-login limiting.
- Set the session cookie to `HttpOnly`, `Secure`, `SameSite=Strict` and `Max-Age=86400`.
- Added a responsive desktop dialog and mobile bottom panel without using `localStorage` or `sessionStorage`.
- Kept `/demo/kiosk` free of public navigation and gate UI.
- Integrated the gate with the production grounded-response persona and v2.4 knowledge release.

## Security boundary

- The repository, client HTML, APK and logs contain no plaintext gate password or session secret.
- Production reads the hash and signing secret only from `/opt/jiyangjia-ai/secrets/.env.local` with mode `600`.
- The gate protects navigation entry points only. It does not make the original GitHub or training-site URLs private.
- Redirect destinations are server constants; the client cannot submit an arbitrary URL.

## Acceptance

- Automated Gateway/admin/knowledge/LLM suite: `99 passed`.
- Desktop dialog, mobile bottom panel, keyboard focus/error state and kiosk isolation were checked in a real browser.
- External HTTPS health, readiness, login, session, both redirects, logout and post-logout locking passed.
- Production container is healthy and the gate configuration is `configured` without exposing values.

## Evidence

- `docs/evidence/TASK-021/public-resource-access-gate-20260812.md`
- Server backup: `/opt/jiyangjia-ai/backups/task021-reconcile-20260812T161020Z`
- Deployment backup: `/opt/jiyangjia-ai/backups/task021-integrated-20260812T161522Z`
