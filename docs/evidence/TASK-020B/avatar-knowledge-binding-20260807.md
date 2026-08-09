# TASK-020B avatar knowledge binding evidence

Executed: 2026-08-07 America/Chicago (`20260808T025409Z` UTC runtime stamp)

## Decision

`DONE` for the isolated local avatar demo binding.

The accepted TASK-020A candidate is now used by the local `18084` demo together with real Doubao ASR/TTS/LLM/Embedding providers. No Provider value, database, FAISS index, recording, generated audio, MP4/JPG asset or original business document is committed.

## Bound runtime

- Demo URL: `http://127.0.0.1:18084/demo/kiosk`
- Knowledge SQLite: `var/task014a-dev/task020a-candidate-20260808T023610Z/knowledge.db`
- FAISS index: `var/task014a-dev/task020a-candidate-20260808T023610Z/faiss.index`
- Runtime admin SQLite: `var/local-avatar-demo/admin.db`
- Runtime assets: `var/local-avatar-demo/assets/`
- Providers: Doubao ASR, Doubao TTS, Doubao/Ark LLM and Doubao/Ark Embedding
- Provider credentials: loaded from the protected external `E:\work\ai-kefu\.env.local`; values were not printed or copied.

The previous local avatar runtime was backed up before switching:

- `var/local-avatar-demo/backups/task020b-20260808T025409Z/admin.db`
  - 36,864 bytes
  - SHA-256 `00659984C4E7E04C695C80649659279486E9A651099EBFC06F35F4CAE165EA74`
- `var/local-avatar-demo/backups/task020b-20260808T025409Z/knowledge.db`
  - 90,112 bytes
  - SHA-256 `40581C135F66DD58BB9463E0547359A2D2F5E268B3CF5A7EE834E64010D9C500`
- `var/local-avatar-demo/backups/task020b-20260808T025409Z/faiss.index`
  - 8,237 bytes
  - SHA-256 `0874F323AC970BD41EF01D67B0D5B8B2343BC0D64D96E9337E050E67FED718F0`

The preserved TASK-014A demo database remains at `var/task014a-dev/knowledge.db`; it was not overwritten or deleted.

## Readiness and content

After restart:

- `/api/v1/health`: HTTP 200
- `/api/v1/readiness`: `ready`
- `/api/v1/knowledge/status`: 41 approved, 24 draft, 0 rejected, 65 chunks, 65 embeddings
- FAISS: ready, 65 vectors, 2048 dimensions
- Embedding: `doubao`, ready
- Display Profile: `display-1080x1920`, 1080x1920, portrait, fit
- Video: `asset_63dd435b89694958`
- Background: `asset_d777ca4a174b4849`

## Real audio dialogue

The controlled 16 kHz mono PCM WAV asked `积养家是做什么的？`. Real ASR returned `七养家是做什么呢？`; the brand normalizer changed it to `积养家是做什么呢？`.

- `POST /api/v1/dialogue/audio`: HTTP 200
- request ID: `task020b-brand-final`
- knowledge status: `matched`
- approved sources: `faq_brand_001`, `faq_boundary_009`
- public source URIs: `knowledge://faq_brand_001`, `knowledge://faq_boundary_009`
- private local source path leaked: false
- TTS provider: `doubao`
- TTS format: `audio/mpeg`
- audio ID: `aud_fd4892f0c29647bfb4419764880f0007`
- audio fetch: HTTP 200, 140,781 bytes
- audio SHA-256: `AFCFDDD89D794EB97127AC4EB7EC77DC65CDE4F150D71F704ECFABD961D8D42C`

The source contract was hardened so local/file paths are returned as stable `knowledge://<doc_id>` URIs. Public `http`, `https` and stable internal `admin`, `manual`, `knowledge` URIs remain supported.

An additional real WAV asking the draft-only business-hours question returned `no_match` and did not leak draft content. This is the intended customer-safety behavior.

## Browser verification

The real local browser loaded `/demo/kiosk` and observed:

- page title `积养家数字人客服`;
- video decoded at 1080x1920, ready state 4 and playing;
- no horizontal overflow;
- `发送` and `开始咨询` enabled;
- text question `积养家是做什么的？` produced a grounded answer and displayed `品牌定位——积养家是做什么的 / 设备使用方式`;
- after TTS playback, the control returned from `处理中` to `开始咨询` while the video continued playing.

Browser microphone permission was not accepted in this task. The real WAV API test verifies the audio pipeline, not physical microphone capture.

## Automated verification

Focused regression:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest tests\asr\test_transcript_normalization.py tests\knowledge\test_lightweight_rag.py tests\e2e\test_dialogue_loop.py -q
```

Result: 19 passed, one third-party FAISS/NumPy deprecation warning.

The ASR suite now covers the observed `七养家` homophone. The knowledge suite covers preservation of public source schemes and redaction of Windows/file source paths.

Full repository regression:

```powershell
.\.venv\gateway-task008-py310\Scripts\python.exe -m pytest -q
powershell -ExecutionPolicy Bypass -File scripts\verify_repository.ps1
```

Result: 89 passed, one third-party FAISS/NumPy deprecation warning; repository verification PASS. The first full run exposed and then fixed compatibility with published `admin://knowledge/...` source URIs before this final pass.

## Rollback

Stop the isolated `18084` process, point `JIYANGJIA_KNOWLEDGE_DB_PATH` and `JIYANGJIA_KNOWLEDGE_FAISS_PATH` back to copies restored from `var/local-avatar-demo/backups/task020b-20260808T025409Z/`, then restart the same local Gateway. Restore `admin.db` only if the avatar/Profile state also needs rollback.

## Completion boundary

This proves the formal knowledge candidate works in the local AI avatar dialogue demo. It does not publish the candidate to Tencent Cloud, clear the Tencent DNSPod webblock/ICP gate, validate browser microphone permission, install an APK or prove Android 12 USB audio behavior.
