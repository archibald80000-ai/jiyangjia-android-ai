# TASK-014 Current API Upload - 2026-08-07

## Source and release

- GitHub default branch: `main`
- GitHub current commit: `a68f234cb0e565f7692c7453fdb298110e842a63`
- Deployment source: current local working tree, including uncommitted Gateway/admin changes
- Server release: `/opt/jiyangjia-ai/releases/release-20260807-667657`
- Active link: `/opt/jiyangjia-ai/current`
- Container: `jiyangjia-gateway` (`running`)

## Secrets

- Local source: `E:\work\ai-kefu\.env.local`
- Server runtime: `/opt/jiyangjia-ai/secrets/.env.local`
- Server source copy: `/opt/jiyangjia-ai/secrets/source-ai-kefu-20260807-667657.env.local`
- Runtime secret mode: `600`
- DeepSeek key: `configured`
- Runtime LLM provider: `deepseek`
- No secret value was written to this evidence file or Git.

## Verification

- Local Gateway/admin tests: `19 passed, 1 warning`
- `GET /api/v1/health`: `200`
- `GET /api/v1/readiness`: `200`, `ready=true`, LLM=`deepseek`, ready
- Real `POST /api/v1/dialogue/text`: success, answer provider=`deepseek`
- TTS provider: `doubao`
- Generated audio fetch: `200`, `57453` bytes
- Public admin page remains restricted: `403`

## APK download

- URL: `http://120.53.86.89/downloads/jiyangjia-kiosk-debug.apk`
- Size: `863175` bytes
- SHA-256: `C4213EC72364E12C02BD57191B3DCDA600FD291D0E7B7C320BF054E18A248965`
- This is a debug APK and has not completed Android real-device acceptance.
- APK inspection confirms the packaged default is still `127.0.0.1:8080`. The package is downloadable but is not accepted as a remote-server-ready APK.
- Source has been updated for the server default and current HTTP test transport, but rebuilding the updated APK is blocked because an Android SDK is not installed/configured on this workstation. Do not claim that the hosted APK can call the remote HTTP server until it is rebuilt and tested on a device.

## GitHub boundary

- No GitHub commit or push was performed.
- GitHub does not include the current local TASK-014B/Gateway/Android changes.
- Existing suspected credential history must be resolved before any push.
