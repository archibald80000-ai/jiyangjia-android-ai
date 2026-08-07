# TASK-014A Admin Content and Display Architecture

Updated: 2026-08-07

## Scope

TASK-014A adds a small operational layer to the existing FastAPI Gateway. It does not add Dify, a CMS, RBAC, multi-tenancy, LiveTalking, or automatic source-directory scanning.

```text
Admin browser
  -> /admin/system | knowledge | avatar | display
  -> /api/v1/admin/* (ADMIN_TOKEN in production)
  -> AdminContentStore (SQLite)
       -> knowledge upload run metadata
       -> avatar/background versions
       -> display profiles

Knowledge publish
  -> existing parser/chunker
  -> existing SQLiteKnowledgeStore
  -> existing Embedding Provider
  -> existing FTS5 + FAISS

Android/public client
  -> /api/v1/assets/manifest
  -> /api/v1/assets/{published_asset_id}
  -> /api/v1/display/profile?width=&height=&orientation=
```

## Knowledge State Machine

```text
upload -> parsed -> preview -> approved -> published
                    \-> rejected
approved -> embedding/index failure -> failed
```

- Uploaded documents are inserted into the knowledge store as `draft`.
- `approve` records human approval but does not make content customer-visible.
- `publish` is the only transition that changes documents to `approved` and runs Embedding/FAISS indexing.
- Customer search continues to allow only `approved`; `draft` and `rejected` remain excluded.
- Published sources use `admin://knowledge/{run_id}/{filename}` and never expose a server filesystem path.

## Asset Release Model

- Accepted types are MP4 video and JPG/PNG image.
- Each upload receives an opaque ID, version, SHA-256 and server-side path.
- Draft preview uses an authenticated admin endpoint.
- The public asset endpoint serves only `published` records.
- Publishing a version demotes the prior version of the same type to `approved`.
- Rollback republishes a selected earlier version and regenerates `manifest.json`.

Runtime files remain outside Git:

- `var/admin/admin.db`
- `var/knowledge/uploads/`
- `var/assets/`

## Display Profiles

Four profiles are seeded: 1080x1920, 1920x1080, 3840x2160 and 1280x720. The 1080x1920 portrait profile is the product default; an idempotent one-time migration applies it to existing admin databases without overriding later administrator choices on every restart. Custom profiles use normalized anchors (0 to 1), bounded character scale, subtitle safe-area JSON, button positions, and optional asset bindings.

Matching order:

1. exact width, height and orientation;
2. nearest active profile of the same orientation;
3. default profile.

This contract lets Android select and cache a profile without rebuilding the APK for each screen.

## Security and Recovery

- Production admin API fails closed when `ADMIN_TOKEN` is missing.
- The token is accepted only through `X-Admin-Token`; it is never returned by an API or bundled into page source.
- Upload sizes and file extensions are bounded.
- Draft asset bytes are not public.
- MP4/JPG/PNG uploads must match their file signatures; Display Profiles may bind only published assets of the correct type.
- SQLite, FAISS, uploads, media and secrets are ignored by Git.
- Recovery consists of restoring `var/admin`, `var/knowledge` and `var/assets` from the same backup point, then recreating the Gateway container.

## Deferred

- Production deployment of TASK-014A;
- business-owned FAQ and media approval;
- Android consumption and device-resolution validation;
- complex identity, audit ledger, alerting and media transcoding.
