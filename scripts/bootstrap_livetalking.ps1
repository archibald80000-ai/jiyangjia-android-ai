param(
    [string]$LockFile = "config/upstream-lock.json"
)

$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root

if (-not (Test-Path $LockFile)) { throw "Missing lock file: $LockFile" }
$lock = Get-Content $LockFile -Raw | ConvertFrom-Json
$target = Join-Path $root $lock.local_path

if (Test-Path $target) {
    if (-not (Test-Path (Join-Path $target ".git"))) {
        throw "Target exists but is not a Git checkout: $target"
    }
    Write-Host "Existing checkout found: $target"
    git -C $target status --short --branch
} else {
    New-Item -ItemType Directory -Force (Split-Path $target) | Out-Null
    git clone --no-checkout $lock.repository $target
}

git -C $target fetch origin $lock.commit --depth 1
git -C $target checkout --detach $lock.commit
$actual = (git -C $target rev-parse HEAD).Trim()
if ($actual -ne $lock.commit) { throw "Commit mismatch: $actual" }

Write-Host "LiveTalking locked checkout ready"
Write-Host "Path: $target"
Write-Host "Commit: $actual"
Write-Host "No model weights or avatar packages were downloaded."
