# LiveTalking integration scope

## Upstream lock

- Repository: `https://github.com/lipku/LiveTalking.git`
- Commit: `c963ad409c556918b7d23999bf87c47a7c05c932`
- Local path: `third_party/LiveTalking`

## First capabilities to reproduce

1. WebRTC `/offer` or WHEP `/whep` session establishment.
2. `/human` with `type=echo` before LLM chat mode.
3. `/humanaudio` with known WAV input.
4. `/interrupt_talk`.
5. `/is_speaking`.
6. `/record` start/end and resulting file.
7. `/set_audiotype` with official/sample actions.
8. `/sse` start/end events.
9. Wav2Lip real-time path and actual FPS when GPU exists.

## Integration policy

- Prefer external adapter/client code in `integration/livetalking_client`.
- Use `config/upstream-lock.json` to fetch a deterministic commit.
- Do not rewrite upstream APIs in the first cycle.
- If a patch is unavoidable, store it in `integration/livetalking_patches/` with reason, upstream SHA, test and rollback.
- Never commit model weights or private avatar data.

## Fallback

When LiveTalking is unavailable, Android plays local idle video and gateway/Android plays TTS audio directly. The product must remain usable as a voice assistant.

## Performance evidence

Record hardware, driver, CUDA, PyTorch, model, avatar resolution, `inferfps`, `finalfps`, first-frame latency, first-audio latency and a 10-minute stability result. Never copy benchmark claims as local results.
