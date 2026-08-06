# TASK-003 asset unblock follow-up web search

- Date: 2026-08-06
- Branch: `task/TASK-003-wav2lip-webrtc-baseline`
- Status impact: TASK-003 remains `BLOCKED`

## Search scope

Queries used:

- `"wav2lip256_avatar1.tar.gz"`
- `"wav2lip256.pth" "LiveTalking"`
- `"1FOC_MD6wdogyyX_7V1d4NDIO7P9NlSAJ"`

## Findings

Public search results found repeated references to the same upstream asset instructions, but did not expose a verified official direct download URL suitable for non-interactive local download in this environment.

Relevant public references:

- LiveTalking upstream GitHub: `https://github.com/lipku/LiveTalking`
- LiveTalking ReadTheDocs quickstart: `https://livetalking-doc.readthedocs.io/zh-cn/latest/quickstart.html`
- LiveTalking ReadTheDocs usage: `https://livetalking-doc.readthedocs.io/en/latest/usage.html`
- Linly-Talker-Stream quick download note: `https://github.com/Kedreamix/Linly-Talker-Stream`
- Other mirrors/posts found in search results repeated the same Quark and Google Drive links instead of providing a verified official direct asset URL.

## Conclusion

TASK-003 remains blocked on asset acquisition. The safe unblock path is still to obtain `wav2lip256.pth` and `wav2lip256_avatar1.tar.gz` from the official README sources through an authorized interactive download or an available network path, then place and hash them before retrying service startup.
