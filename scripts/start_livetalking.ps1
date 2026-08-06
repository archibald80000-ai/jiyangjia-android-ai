param(
  [string]$EnvPath = ".venv\livetalking-task002",
  [string]$Model = "wav2lip",
  [string]$AvatarId = "wav2lip256_avatar1",
  [string]$Transport = "webrtc",
  [int]$ListenPort = 8010,
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
