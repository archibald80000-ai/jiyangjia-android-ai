param(
    [string]$Repository = "archibald80000-ai/jiyangjia-ai-kiosk",
    [string]$Description = "Android 12 store AI voice kiosk and LiveTalking digital-human integration"
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required. Install it and run: gh auth login"
}

gh auth status

powershell -ExecutionPolicy Bypass -File .\scripts\verify_repository.ps1

$forbidden = git ls-files | Select-String -Pattern '(^|/)(\.env|\.env\.local|.*\.pem|.*\.key|.*\.p12|.*\.pfx)$'
if ($forbidden) { throw "Refusing publication: a sensitive file name is tracked." }

if (-not (Test-Path ".git")) {
    git init -b main
    git config user.name | Out-Null
}

$status = git status --porcelain
if ($status) {
    Write-Host "Uncommitted changes exist. Review and commit only confirmed files before publishing:"
    git status --short
    throw "Working tree must be clean before publication."
}

$existing = $null
try { $existing = gh repo view $Repository --json nameWithOwner,visibility 2>$null | ConvertFrom-Json } catch {}

if ($existing) {
    if ($existing.visibility -ne "PUBLIC") { throw "Repository exists but is not public." }
    Write-Host "Repository already exists: $($existing.nameWithOwner)"
} else {
    gh repo create $Repository --public --description $Description --source . --remote origin
    gh repo edit $Repository --enable-issues --enable-wiki=false --enable-projects=true
    gh repo edit $Repository --add-topic android --add-topic ai --add-topic digital-human --add-topic livetalking --add-topic kiosk --add-topic voice-assistant
}

$remote = git remote get-url origin
Write-Host "Origin: $remote"
git push -u origin main
Write-Host "Published: https://github.com/$Repository"
