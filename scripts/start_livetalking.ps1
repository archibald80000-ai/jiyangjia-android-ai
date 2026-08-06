param(
  [string]$EnvPath = ".venv\livetalking-task002",
  [string]$Model = "wav2lip",
  [string]$AvatarId = "wav2lip256_avatar1",
  [string]$Transport = "webrtc",
  [int]$ListenPort = 8010,
  [switch]$SkipAssetCheck,
  [string[]]$ExtraArgs = @()
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$liveTalkingPath = Join-Path $repoRoot "third_party\LiveTalking"
$resolvedEnvPath = Join-Path $repoRoot $EnvPath

if (-not (Test-Path $liveTalkingPath)) {
  throw "LiveTalking checkout not found at $liveTalkingPath. Run scripts\bootstrap_livetalking.ps1 first."
}

if (-not (Test-Path $resolvedEnvPath)) {
  throw "Conda environment not found at $resolvedEnvPath. Complete TASK-002 environment setup first."
}

if ($Model -eq "wav2lip" -and -not $SkipAssetCheck) {
  $assetChecks = @(
    [pscustomobject]@{
      Kind = "file"
      Path = Join-Path $liveTalkingPath "models\wav2lip.pth"
      Help = "Copy official wav2lip256.pth here and rename it to wav2lip.pth."
    },
    [pscustomobject]@{
      Kind = "file"
      Path = Join-Path $liveTalkingPath "avatars\wav2lip\face_detection\detection\sfd\s3fd.pth"
      Help = "Copy official s3fd.pth to the Wav2Lip SFD detector directory."
    },
    [pscustomobject]@{
      Kind = "directory"
      Path = Join-Path $liveTalkingPath "data\avatars\$AvatarId"
      Help = "Extract the official wav2lip256_avatar1 package so this avatar directory exists and is non-empty."
    }
  )

  $missing = New-Object System.Collections.Generic.List[string]
  foreach ($check in $assetChecks) {
    if ($check.Kind -eq "file") {
      $item = Get-Item -LiteralPath $check.Path -ErrorAction SilentlyContinue
      if ($null -eq $item -or $item.Length -le 0) {
        $missing.Add("- Missing file: $($check.Path)`n  $($check.Help)") | Out-Null
      }
      continue
    }

    $dir = Get-Item -LiteralPath $check.Path -ErrorAction SilentlyContinue
    $hasContent = $false
    if ($null -ne $dir -and $dir.PSIsContainer) {
      $hasContent = $null -ne (Get-ChildItem -LiteralPath $check.Path -Force -ErrorAction SilentlyContinue | Select-Object -First 1)
    }
    if (-not $hasContent) {
      $missing.Add("- Missing or empty directory: $($check.Path)`n  $($check.Help)") | Out-Null
    }
  }

  if ($missing.Count -gt 0) {
    $message = @(
      "Wav2Lip assets are not ready; LiveTalking startup was stopped before model loading.",
      "",
      "Required assets:",
      ($missing -join [Environment]::NewLine),
      "",
      "Official source recorded by LiveTalking docs: https://pan.quark.cn/s/83a750323ef0",
      "Observed public Quark listing on 2026-08-06: s3fd.pth, wav2lip256.pth, wav2lip256_avatar1.zip.",
      "Do not commit these model/avatar files; third_party/LiveTalking is intentionally ignored."
    ) -join [Environment]::NewLine
    throw $message
  }
}

Push-Location $liveTalkingPath
try {
  conda run -p $resolvedEnvPath python app.py `
    --transport $Transport `
    --model $Model `
    --avatar_id $AvatarId `
    --listenport $ListenPort `
    @ExtraArgs
}
finally {
  Pop-Location
}
