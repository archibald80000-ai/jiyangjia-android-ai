param(
    [string]$Repository = "archibald80000-ai/jiyangjia-android-ai",
    [string]$Description = "积养家 Android 12 大屏 AI 语音与数字人客服系统"
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
}

gh api -X PATCH "repos/$Repository" `
    -f description="$Description" `
    -F has_issues=true `
    -F has_wiki=false `
    -F has_projects=true | Out-Null

gh api -X PUT "repos/$Repository/topics" `
    -H "Accept: application/vnd.github+json" `
    -f names[]=android `
    -f names[]=ai `
    -f names[]=digital-human `
    -f names[]=livetalking `
    -f names[]=speech-recognition `
    -f names[]=text-to-speech `
    -f names[]=kiosk `
    -f names[]=webrtc | Out-Null

if (-not (git remote | Select-String -Pattern '^origin$')) {
    git remote add origin "https://github.com/$Repository.git"
}

$remote = git remote get-url origin
Write-Host "Origin: $remote"
git push -u origin main
Write-Host "Published: https://github.com/$Repository"
