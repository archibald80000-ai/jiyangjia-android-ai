# TASK-010: Implement Mock then Doubao ASR adapters

- **Status:** DONE
- **Priority:** P0
- **Dependencies:** TASK-009
- **Branch:** `task/TASK-010-asr-providers`
- **Owner:** Codex / assigned developer

## Objective

Implement Mock then Doubao ASR adapters.

## Preconditions

- TASK-009 is DONE
- TASK-007 and TASK-008 are DONE/PARTIAL with usable audio and gateway contracts

## Scope and allowed changes

- `gateway/provider adapters`
- `integration/asr/`
- `tests/asr/`
- `docs/evidence/TASK-010/`
- `state/memory/task files`

Do not modify unrelated modules, user source documents or secrets. Changes outside these paths require a new approved task or ADR.

## Non-goals

- Always-on streaming before batch path works

## Detailed execution

1. Define accepted audio types, duration/size limits and normalization path.
2. Implement Mock ASR first and prove the dialogue endpoint can consume it.
3. Research the current official Doubao ASR API, then implement one bounded batch/file path before streaming.
4. Add conversion, timeout, finite retry, charge protection and sanitized errors.
5. Test known rights-cleared audio and compare transcript manually; do not call real device streaming complete.

## Verification commands

Commands are starting points; record exact environment-specific variants and results. Do not fabricate missing tools or paths.

```powershell
python -m pytest tests/asr -q
```
```powershell
python scripts/test_asr_provider.py --provider mock --file <sample>
```
```powershell
python scripts/test_asr_provider.py --provider doubao --file <sample>
```

## Required deliverables

- [x] Mock and verified real ASR path when credentials permit
- [x] Format/error tests
- [x] Transcript quality report

## Acceptance criteria

- [x] Audio contract defined
- [x] Mock pass
- [x] Doubao current API verified
- [x] Format conversion tested
- [x] Timeout/error/cost guard

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

## Rollback

Restore the previous task commit/config, stop task processes, and remove only task-created local runtime files. Never touch `E:\work\积养家`, unrelated work or user secrets.

## Close-out

- [x] Set status to `DONE`, `PARTIAL` or `BLOCKED`.
- [x] Add evidence links/results to this task.
- [x] Update `PROJECT_STATE.md`.
- [x] Update `memory/CURRENT_STATE.md`.
- [x] Replace `memory/HANDOFF.md` with current facts.
- [x] Update assumptions/open questions and add ADR if needed.
- [x] Recommend exactly one next task.

## TASK-010 Result

- Doubao/Volcengine ASR adapter is implemented behind the common ASR Provider interface.
- Implementation follows the official big-model WebSocket protocol and uses a bounded Gateway file/bytes-to-chunks path, not Android always-on streaming.
- Non-WAV/PCM input is normalized through ffmpeg to 16 kHz mono PCM WAV before ASR.
- CLI helper exists: `scripts/test_asr_provider.py`.
- Unit and regression tests passed: `python -m pytest tests\asr tests\gateway tests\tts -q` -> 16 passed.
- Mock ASR CLI returned deterministic mock transcript.
- External private-env config preflight returned configured app/access auth; values were not printed.
- Real Doubao ASR call succeeded on generated TTS smoke audio:
  - MP3 input SHA-256 `981F9001284C1C5057B7737318E444393A527C56070F9F3805551C8392F85BF8`
  - normalized WAV SHA-256 `7605E6D543E89A289A64E1C097DC494CB7879DA6B64E6A3E02A36428C17FE3CC`
  - observed transcript `您好，欢迎来到机养家。`
- Known quality note: expected `积养家`, observed `机养家`; domain vocabulary/post-ASR correction or RAG grounding should handle this later.
- Evidence: `docs/evidence/TASK-010/asr-provider.md`.
