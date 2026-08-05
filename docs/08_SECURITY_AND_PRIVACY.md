# Security and privacy

## Threat boundaries

- Public Android device can be physically accessed.
- Public repository is readable by anyone.
- Provider API keys are high-value secrets.
- Voice data may contain personal information.
- WebRTC and remote control endpoints can be abused if exposed without controls.

## Controls

- Android receives only a scoped device token.
- TLS for all production HTTP/WebSocket traffic.
- Gateway validates store/device identity and rate limits requests.
- LiveTalking control endpoints are private, authenticated through a proxy or network-restricted.
- Raw audio retention defaults to zero.
- Logs mask phone numbers, identifiers and provider payload details.
- Admin mode requires separate authentication.
- Secret scanning and pre-commit checks prevent accidental publication.

## Public repository exclusions

- `.env.local` and secrets.
- Raw store archives and contracts.
- Customer recordings and transcripts.
- Model weights and private avatars.
- Internal IPs, credentials and production database backups.
