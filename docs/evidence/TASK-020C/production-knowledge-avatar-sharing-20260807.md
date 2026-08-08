# TASK-020C production knowledge and avatar sharing evidence

Executed: 2026-08-07 America/Chicago (`20260808T031244Z` UTC runtime stamp)

## Decision

`PARTIAL / BLOCKED_BY_TENCENT_WEBBLOCK_ICP`.

The production data and avatar publication are complete. Public sharing is still externally blocked, so this task does not claim that an off-server browser can open the canonical HTTPS URL yet.

## Production knowledge location

Host paths in the active release:

- SQLite: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/knowledge/jiyangjia.db`
- FAISS: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/knowledge/faiss.index`
- Admin SQLite: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/admin/admin.db`
- Assets: `/opt/jiyangjia-ai/releases/release-task015b-realtime-20260807T095914Z/var/assets/`

Container paths are `/app/var/knowledge/jiyangjia.db`, `/app/var/knowledge/faiss.index`, `/app/var/admin/admin.db` and `/app/var/assets/`.

Final status: 41 approved, 24 draft, 0 rejected, 65 chunks, 65 embeddings and 65 FAISS vectors at 2048 dimensions. Doubao Embedding is ready.

The read-only status URL is `https://ai-jiyangjia.cloud/api/v1/knowledge/status`; it becomes publicly usable only after the Tencent webblock/ICP gate is released.

## Avatar publication

User-approved source:

- `E:\work\ai-kefu\资料库\人像背景.MOV`
- 103,491,758 bytes
- SHA-256 `01C87F208A9E81CE83425F35B9778904F7769E7BBD7AA6171FA41473F7118622`
- HEVC 1728x3072 at 60 fps with AAC, 21.283 seconds

The production admin accepts MP4, not MOV. The exact approved source was therefore represented by the existing browser/Android-compatible derivative rather than uploading the MOV container itself:

- H.264, 1080x1920, yuv420p, silent, 21.300 seconds
- 7,930,361 bytes
- SHA-256 `7B19190A3A13A149780B3D9FC371D296EF356C92A8F8744119E573F673221AEB`
- Production ID `asset_6a549a648fe647f1`
- Production URL `/api/v1/assets/asset_6a549a648fe647f1`

The same-source JPG background is 1080x1920, 239,140 bytes, SHA-256 `430DF518D6796F9AA5FAB2018A08D39F169D696227B6D43CB02D1CBE42EB073A`, production ID `asset_0f04a1bf5a0b4237`.

Both assets were downloaded back through the production Gateway. Their downloaded hashes and sizes matched the local derivatives exactly.

## Display Profile

- ID: `display-1080x1920`
- Size/orientation: 1080x1920 portrait
- Scale mode: fit
- Video: `asset_6a549a648fe647f1`
- Background: `asset_0f04a1bf5a0b4237`
- Subtitle: 36 px; left/right 8%, bottom 16%
- Consult button: `(0.5, 0.9)`
- Default/active: true

## Backup and code correction

Rollback backup:

`/opt/jiyangjia-ai/backups/task020c-avatar-20260808T031244Z`

It contains the pre-publication admin/assets trees, pre-publication manifest/Profile and the previous `knowledge.py` and `transcript_normalization.py` files.

The active release initially returned private Windows source paths because it did not contain the TASK-020B source sanitizer. The two narrow files were backed up, synchronized and the Gateway was force-recreated. Final state is `running/healthy`.

## Real production dialogue

- request ID: `task020c-production-final`
- knowledge status: matched
- source IDs: `faq_brand_001`, `faq_boundary_009`
- source URIs: `knowledge://faq_brand_001`, `knowledge://faq_boundary_009`
- private source path leaked: false
- TTS: Doubao `audio/mpeg`
- audio ID: `aud_b454a5e653d64fc6a192cc57f1ff04dc`
- audio: 128,685 bytes
- audio SHA-256: `042CC93B88EF8FFC0155409A29F7DDE2E7E661B0249B5658D59575520A4D87D7`

All ASR/TTS/LLM/Embedding readiness gates reported ready after recreation.

## Sharing status

Server-local Nginx/TLS using the canonical hostname:

- `/health`: 200
- `/demo/kiosk`: 200
- `/api/v1/knowledge/status`: 200

External probe:

- `http://ai-jiyangjia.cloud`: 308 to HTTPS
- `https://ai-jiyangjia.cloud`: connection reset, curl exit 35

Target share URLs are therefore configured but not yet publicly usable:

- `https://ai-jiyangjia.cloud/demo/kiosk`
- `https://ai-jiyangjia.cloud/api/v1/knowledge/status`
- `https://ai-jiyangjia.cloud/api/v1/assets/manifest`
- `https://ai-jiyangjia.cloud/api/v1/display/profile`

The admin URL and `ADMIN_TOKEN` are private and must not be shared. Do not weaken the HTTP-to-HTTPS policy or expose Gateway port 8080 to bypass the external gate.

## Repository verification

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest -q
powershell -ExecutionPolicy Bypass -File scripts\verify_repository.ps1
```

Result: 89 passed with one third-party FAISS/NumPy deprecation warning; repository verification PASS.
