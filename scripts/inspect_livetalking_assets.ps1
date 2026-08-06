param(
  [Parameter(Mandatory = $true)]
  [string]$AssetSourcePath,
  [string]$AvatarId = "wav2lip256_avatar1",
  [switch]$AllowNonOfficialSizes
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$sourcePath = (Resolve-Path -LiteralPath $AssetSourcePath -ErrorAction Stop).Path

$officialSizes = @{
  wav2lip_model = 214670409
  s3fd_detector = 89843225
  avatar_zip = 353735616
}

function Find-FirstAssetFile {
  param(
    [string]$Root,
    [string[]]$Names
  )

  foreach ($name in $Names) {
    $hits = Get-ChildItem -LiteralPath $Root -Recurse -File -Filter $name -ErrorAction SilentlyContinue |
      Sort-Object FullName
    if ($hits) {
      return $hits[0]
    }
  }
  return $null
}

function Find-FirstExpandedAvatar {
  param(
    [string]$Root,
    [string]$Name
  )

  $hits = Get-ChildItem -LiteralPath $Root -Recurse -Directory -Filter $Name -ErrorAction SilentlyContinue |
    Where-Object {
      (Test-Path -LiteralPath (Join-Path $_.FullName "coords.pkl")) -and
      (Test-Path -LiteralPath (Join-Path $_.FullName "full_imgs")) -and
      (Test-Path -LiteralPath (Join-Path $_.FullName "face_imgs"))
    } |
    Sort-Object FullName

  if ($hits) {
    return $hits[0]
  }
  return $null
}

function Write-FileFinding {
  param(
    [string]$Label,
    [object]$File,
    [long]$ExpectedSize
  )

  if ($null -eq $File) {
    Write-Output "$Label status=missing"
    $script:ok = $false
    return
  }

  $hash = Get-FileHash -LiteralPath $File.FullName -Algorithm SHA256
  Write-Output "$Label status=found path=$($File.FullName) size=$($File.Length) sha256=$($hash.Hash)"
  if (-not $AllowNonOfficialSizes -and [long]$File.Length -ne $ExpectedSize) {
    Write-Output "$Label status=size_mismatch expected=$ExpectedSize actual=$($File.Length)"
    $script:ok = $false
  }
}

Write-Output "Inspecting LiveTalking Wav2Lip assets under $sourcePath"
Write-Output "This script does not download assets, copy model files, or read browser/Quark login storage."
if ($AllowNonOfficialSizes) {
  Write-Output "Official size checks are disabled by -AllowNonOfficialSizes; use this only for script fixtures or explicit manual review."
}

$modelSource = Find-FirstAssetFile -Root $sourcePath -Names @("wav2lip.pth", "wav2lip256.pth")
$s3fdSource = Find-FirstAssetFile -Root $sourcePath -Names @("s3fd.pth")
$avatarSource = Find-FirstExpandedAvatar -Root $sourcePath -Name $AvatarId
$avatarZipSource = Find-FirstAssetFile -Root $sourcePath -Names @("$AvatarId.zip")

$script:ok = $true

Write-FileFinding -Label "wav2lip_model" -File $modelSource -ExpectedSize $officialSizes.wav2lip_model
Write-FileFinding -Label "s3fd_detector" -File $s3fdSource -ExpectedSize $officialSizes.s3fd_detector

if ($null -ne $avatarSource) {
  $files = @(Get-ChildItem -LiteralPath $avatarSource.FullName -Recurse -File -ErrorAction Stop)
  $totalBytes = ($files | Measure-Object -Property Length -Sum).Sum
  Write-Output "avatar_$AvatarId status=expanded path=$($avatarSource.FullName) files=$($files.Count) bytes=$totalBytes"
}
elseif ($null -ne $avatarZipSource) {
  $hash = Get-FileHash -LiteralPath $avatarZipSource.FullName -Algorithm SHA256
  Write-Output "avatar_$AvatarId status=zip_only path=$($avatarZipSource.FullName) size=$($avatarZipSource.Length) sha256=$($hash.Hash)"
  if (-not $AllowNonOfficialSizes -and [long]$avatarZipSource.Length -ne $officialSizes.avatar_zip) {
    Write-Output "avatar_$AvatarId status=size_mismatch expected=$($officialSizes.avatar_zip) actual=$($avatarZipSource.Length)"
    $script:ok = $false
  }
  Write-Output "avatar_$AvatarId action=expand_zip_before_prepare"
  $script:ok = $false
}
else {
  Write-Output "avatar_$AvatarId status=missing"
  $script:ok = $false
}

if (-not $script:ok) {
  throw "Asset source is not ready for PrepareAssets. Need wav2lip.pth/wav2lip256.pth, s3fd.pth, and expanded $AvatarId with coords.pkl/full_imgs/face_imgs."
}

$relativeLauncher = Join-Path $repoRoot "scripts\start_livetalking.ps1"
Write-Output "Asset source is ready for local preparation."
Write-Output "Prepare command:"
Write-Output "powershell -ExecutionPolicy Bypass -File `"$relativeLauncher`" -PrepareAssets -AssetSourcePath `"$sourcePath`""
