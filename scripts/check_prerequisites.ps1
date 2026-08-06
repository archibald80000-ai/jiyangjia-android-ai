$ErrorActionPreference = "Continue"

Write-Host "== Jiyangjia AI Kiosk prerequisite audit =="
Write-Host "Path: $(Get-Location)"

function Show-Tool($Name, $Command, $CommandArgs) {
    $cmd = Get-Command $Command -ErrorAction SilentlyContinue
    if (-not $cmd) {
        Write-Host "${Name}: MISSING"
        return
    }
    try {
        $output = & $Command @CommandArgs 2>&1 | Select-Object -First 8
        Write-Host "${Name}: FOUND ($($cmd.Source))"
        $output | ForEach-Object { Write-Host "  $_" }
    } catch {
        Write-Host "${Name}: ERROR ($($_.Exception.Message))"
    }
}

Show-Tool "Git" "git" @("--version")
Show-Tool "Python" "python" @("--version")
Show-Tool "Conda" "conda" @("--version")
Show-Tool "FFmpeg" "ffmpeg" @("-version")
Show-Tool "NVIDIA" "nvidia-smi" @()
Show-Tool "Java" "java" @("-version")
Show-Tool "ADB" "adb" @("version")
Show-Tool "Gradle" "gradle" @("--version")
Show-Tool "GitHub CLI" "gh" @("--version")

$envFile = Join-Path (Get-Location) ".env.local"
if (Test-Path $envFile) {
    Write-Host ".env.local: PRESENT (values not read or printed)"
} else {
    Write-Host ".env.local: MISSING"
}

Write-Host "== Git status =="
if (Test-Path ".git") { git status --short --branch } else { Write-Host "Not a Git repository" }
