# TASK-003: Run the first Wav2Lip WebRTC/WHEP baseline

- **Status:** BLOCKED
- **Priority:** P0
- **Dependencies:** TASK-002
- **Branch:** `task/TASK-003-wav2lip-webrtc-baseline`
- **Owner:** Codex / assigned developer

## Objective

Run the first Wav2Lip WebRTC/WHEP baseline.

## Preconditions

- TASK-002 is DONE or PARTIAL with a usable runtime
- Wav2Lip model and Avatar requirements are understood

## Scope and allowed changes

- `Local ignored model/avatar directories`
- `scripts/start_livetalking.ps1`
- `scripts/inspect_livetalking_assets.ps1`
- `docs/evidence/TASK-003/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- MuseTalk
- Multi-concurrency
- Production deployment

## Detailed execution

1. Check required model and Avatar files by exact path and non-zero size; record source and checksum when available.
2. If assets are missing, stop before fake startup and produce exact manual download/placement instructions.
3. Launch LiveTalking with Wav2Lip and WebRTC/WHEP using the locked checkout; capture full sanitized startup log and PID/stop procedure.
4. Open the official page and establish one stream. Record browser/client, session ID format, audio/video outcome and network ports.
5. Capture `inferfps`/`finalfps` only from real logs and run a minimum stability interval appropriate to the environment.
6. Do not start MuseTalk or alter core upstream code.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
Get-ChildItem third_party/LiveTalking/models -ErrorAction SilentlyContinue
```
```powershell
Get-ChildItem third_party/LiveTalking/data/avatars -ErrorAction SilentlyContinue
```
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_livetalking.ps1
```
```powershell
Invoke-WebRequest http://127.0.0.1:8010/index.html -UseBasicParsing
```

## Required deliverables

- [x] scripts/start_livetalking.ps1
- [x] scripts/inspect_livetalking_assets.ps1
- [x] docs/evidence/TASK-003/wav2lip-baseline.md
- [x] Startup/stream logs or exact BLOCKED evidence

## Acceptance criteria

- [x] Required weights/avatar locations verified
- [x] Service starts or exact blocker is captured
- [ ] Web page and WHEP/WebRTC result recorded
- [x] Real FPS only reported from logs

## Stop / blocked conditions

- A destructive change, secret exposure, uncontrolled paid call or public network exposure would be required.
- A dependency is absent and cannot be safely installed inside the authorized scope.
- Real hardware/model/provider evidence is required but unavailable.
- Existing unrelated changes make safe staging impossible.

When blocked, complete all safe analysis, save sanitized evidence, set status to `BLOCKED` or `PARTIAL`, and state the exact unblock action.

## Required evidence

- Exact commands, versions, exit codes/results and timestamps.
- Changed files and `git diff --stat`.
- Sanitized logs/screenshots where meaningful.
- Artifact paths and SHA-256 for APK/packages.
- Hardware/environment details for device/GPU claims.
- Failed cases, untested paths and cost-bearing calls.

TASK-003 evidence:

- `docs/evidence/TASK-003/wav2lip-baseline.md`
- `docs/evidence/TASK-003/initial-asset-and-env-check.txt`
- `docs/evidence/TASK-003/gdown-install.txt`
- `docs/evidence/TASK-003/gdrive-download.txt`
- `docs/evidence/TASK-003/gdrive-download-retry.txt`
- `docs/evidence/TASK-003/asset-source-reachability.txt`
- `docs/evidence/TASK-003/quark-page-probe.txt`
- `docs/evidence/TASK-003/asset-unblock-followup-local-search.txt`
- `docs/evidence/TASK-003/asset-unblock-followup-web-search.md`
- `docs/evidence/TASK-003/pip-check-after-gdown.txt`
- `docs/evidence/TASK-003/task003-final-verification.txt`
- `docs/evidence/TASK-003/task003-followup-final-verification.txt`
- `docs/evidence/TASK-003/task003-third-blocked-audit.txt`
- `docs/evidence/TASK-003/quark-public-api-probe.txt`
- `docs/evidence/TASK-003/quark-public-api-folder-list.txt`
- `docs/evidence/TASK-003/quark-page-script-urls.txt`
- `docs/evidence/TASK-003/quark-share-download-url-probe.txt`
- `docs/evidence/TASK-003/quark-download-endpoint-error-details.txt`
- `docs/evidence/TASK-003/quark-desktop-ua-download-url-probe.txt`
- `docs/evidence/TASK-003/quark-file-download-desktop-ua-probe.txt`
- `docs/evidence/TASK-003/quark-batch-download-probe.txt`
- `docs/evidence/TASK-003/gdrive-official-source-retry-20260806.txt`
- `docs/evidence/TASK-003/gdrive-official-source-retry-supported-args-20260806.txt`
- `docs/evidence/TASK-003/asset-unblock-downloads-exact-search-20260806.txt`
- `docs/evidence/TASK-003/start-script-asset-preflight-20260806.txt`
- `docs/evidence/TASK-003/start-script-help-skip-asset-check-20260806.txt`
- `docs/evidence/TASK-003/task003-asset-unblock-attempt-final-verification-20260806.txt`
- `docs/evidence/TASK-003/quark-windows-package-public-list-20260806.txt`
- `docs/evidence/TASK-003/quark-windows-package-targeted-asset-list-20260806.txt`
- `docs/evidence/TASK-003/quark-windows-package-download-probe-20260806.txt`
- `docs/evidence/TASK-003/quark-windows-package-avatar-tree-20260806.txt`
- `docs/evidence/TASK-003/quark-avatar-small-download-header-probe-20260806.txt`
- `docs/evidence/TASK-003/quark-download-url-shape-20260806.txt`
- `docs/evidence/TASK-003/quark-client-local-capability-20260806.txt`
- `docs/evidence/TASK-003/task003-official-package-attempt-final-verification-20260806.txt`
- `docs/evidence/TASK-003/asset-unblock-quark-download-dir-search-20260806.txt`
- `docs/evidence/TASK-003/start-script-prepare-assets-mode-verification-20260806.txt`
- `docs/evidence/TASK-003/task003-prepare-assets-mode-final-verification-20260806.txt`
- `docs/evidence/TASK-003/asset-unblock-size-and-structure-search-20260806.txt`
- `docs/evidence/TASK-003/task003-size-structure-search-final-verification-20260806.txt`
- `docs/evidence/TASK-003/asset-inspector-verification-20260806.txt`
- `docs/evidence/TASK-003/task003-asset-inspector-final-verification-20260806.txt`

Blocked result:

- `third_party\LiveTalking\models\wav2lip.pth` is missing.
- `third_party\LiveTalking\avatars\wav2lip\face_detection\detection\sfd\s3fd.pth` is missing.
- `third_party\LiveTalking\data\avatars\wav2lip256_avatar1\` is missing.
- Google Drive official source was unreachable from this machine.
- Quark official source can be listed through public share APIs and currently exposes `wav2lip256_avatar1.zip`, `s3fd.pth` and `wav2lip256.pth`, but unauthenticated download URL creation returns code `23018 download file size limit`.
- Quark Windows integrated package share can also be listed and contains `models/wav2lip.pth`, `_internal/.../s3fd.pth` and expanded `data/avatars/wav2lip256_avatar1`; large files still hit `23018`, and small signed download URLs return HTTP `412` through CLI GET.
- Follow-up exact local filename search in safe roots found no existing copies of the required assets.
- Candidate local Quark/download directories were searched by exact filename on 2026-08-06; no existing local copies were found.
- Selected non-sensitive local roots were searched by exact official file sizes and `wav2lip256_avatar1` directory structure on 2026-08-06; no candidate assets were found.
- Follow-up public web search found repeated upstream source references but no verified official direct download URL.
- LiveTalking service startup was intentionally not attempted without the required model/avatar assets.
- `scripts/start_livetalking.ps1` now performs asset preflight and stops before model loading when required Wav2Lip assets are missing.
- `scripts/start_livetalking.ps1` also supports explicit local preparation via `-PrepareAssets -AssetSourcePath <downloaded_official_source>` after a user/authorized client has downloaded the official assets.
- `scripts/inspect_livetalking_assets.ps1` verifies a downloaded source before preparation and rejects same-name model/S3FD dummy files by default when official sizes do not match.

## Rollback

Restore the previous task commit/config, stop task processes, and remove only task-created local runtime files. Never touch `E:\work\积养家`, unrelated work or user secrets.

## Close-out

- [x] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [x] Add evidence links/results to this task.
- [x] Update `PROJECT_STATE.md`.
- [x] Update `memory/CURRENT_STATE.md`.
- [x] Replace `memory/HANDOFF.md` with current facts.
- [x] Update assumptions/open questions; no new ADR required.
- [x] Recommend exactly one next task: unblock and rerun `TASK-003_WAV2LIP_WEBRTC_BASELINE.md` after placing official Wav2Lip model/S3FD/avatar assets.
