# Scripts

- `check_prerequisites.ps1`: safe environment inventory.
- `bootstrap_livetalking.ps1`: deterministic upstream checkout.
- `verify_repository.ps1`: validate required files and refuse common sensitive/binary tracked content.
- `publish_public_repo.ps1`: create/push the public GitHub repository from an authenticated Windows environment.
- `create_github_issues.ps1`: create task issues after repository publication.

Scripts never print secret values and should stop on unexpected tracked changes.
