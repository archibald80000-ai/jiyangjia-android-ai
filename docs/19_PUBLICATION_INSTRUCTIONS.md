# Publish the bootstrap repository

Target: `https://github.com/archibald80000-ai/jiyangjia-ai-kiosk` as a public repository.

## Safe publication from Windows

1. Install Git and GitHub CLI.
2. Authenticate with `gh auth login`.
3. Place this framework in `E:\work\安卓大屏AI语音客服系统`.
4. Review `.env.local` is ignored and not tracked.
5. Initialize/commit the confirmed framework.
6. Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\publish_public_repo.ps1
```

The script refuses publication when common secret file names are tracked, creates the public repository only if absent, checks visibility and pushes `main`.

## After publication

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\create_github_issues.ps1
```

This creates labels and one issue per task. Review the public repository once more for private data before inviting other devices or contributors.
