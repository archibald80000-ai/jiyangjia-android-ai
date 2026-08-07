# TASK-014A Evidence

Date: 2026-08-07

- `task014a-pytest-20260807.txt`: full regression, 55 passed, including embedding-failure rollback, asset signature/binding validation and UI command contract.
- `task014a-admin-ui-node-check-20260807.txt`: generated admin JavaScript syntax check, exit 0 (no stdout).
- `task014a-local-http-20260807.json`: local Mock Gateway checks for four pages, system status, manifest and display-profile matching; all returned HTTP 200 with request IDs.
- `task014a-valid-file-http-20260807.json`: valid H.264 MP4 and PNG upload/publish/manifest plus Markdown approve/publish/search HTTP workflow. The downloaded preview was verified by ffprobe as H.264 640x360.
- `task014a-real-browser-actions-20260807.json`: real in-app-browser clicks for knowledge, asset, display and system actions after repairing the command dispatcher. Backend states changed and no application console errors were observed.
- `task014a-browser-api-requests-20260807.txt`: 16 corresponding POST/PUT/DELETE access-log entries, all HTTP 200.

Docker Compose parsing was not run because Docker CLI is unavailable on this Windows host. No production deployment, formal business-content import, Android profile consumption or physical-device result is claimed by TASK-014A.
