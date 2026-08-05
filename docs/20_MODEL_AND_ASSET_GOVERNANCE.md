# Model and asset governance

## Registry

Copy `assets/ASSET_REGISTRY.example.yaml` to a private/local registry when real assets are introduced. Public commits may contain metadata only when it does not expose private URLs or personal information.

## Required fields

- Asset ID and type.
- Source and upstream version.
- SHA-256.
- Expected local path.
- Code license and weight/asset license references.
- Commercial-use review.
- Person/voice consent reference when applicable.
- Status: missing, downloaded, verified, rejected, expired.

## Rules

- Never commit model weights or private avatar/voice media.
- Never mark an asset verified without a real hash and usable file.
- Generated content still requires provider-term and likeness review.
- Replacing an asset is a traceable change with regression tests.
