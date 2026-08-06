param(
  [string]$EnvPath = ".venv\livetalking-task002",
  [string]$Model = "wav2lip",
  [string]$AvatarId = "wav2lip256_avatar1",
  [string]$Transport = "webrtc",
  [int]$ListenPort = 8010,
  [switch]$PrepareAssets,
  [string]$AssetSourcePath = "",
  [switch]$OverwriteAssets,
  [switch]$AllowNonOfficialSizes,
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

$modelTarget = Join-Path $liveTalkingPath "models\wav2lip.pth"
$s3fdTarget = Join-Path $liveTalkingPath "avatars\wav2lip\face_detection\detection\sfd\s3fd.pth"
$avatarTarget = Join-Path $liveTalkingPath "data\avatars\$AvatarId"
$assetStagingRoot = Join-Path $repoRoot ".cache\livetalking-assets"

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

function Find-FirstAssetDirectory {
  param(
    [string]$Root,
    [string]$Name
  )

  $hits = Get-ChildItem -LiteralPath $Root -Recurse -Directory -Filter $Name -ErrorAction SilentlyContinue |
    Where-Object {
      (Test-Path (Join-Path $_.FullName "coords.pkl")) -and
      (Test-Path (Join-Path $_.FullName "full_imgs")) -and
      (Test-Path (Join-Path $_.FullName "face_imgs"))
    } |
    Sort-Object FullName
  if ($hits) {
    return $hits[0]
  }
  return $null
}

function Assert-OfficialSize {
  param(
    [object]$File,
    [long]$ExpectedSize,
    [string]$Label
  )

  if ($AllowNonOfficialSizes) {
    Write-Output "$Label official_size_check=disabled actual_size=$($File.Length)"
    return
  }

  if ([long]$File.Length -ne $ExpectedSize) {
    throw "$Label size mismatch. Expected official size $ExpectedSize bytes, got $($File.Length) bytes at $($File.FullName). Use -AllowNonOfficialSizes only after explicit manual review."
  }
}

function Expand-AvatarArchive {
  param(
    [object]$Archive,
    [string]$AvatarName
  )

  if ($null -eq $Archive) {
    return $null
  }

  $extractRoot = Join-Path $assetStagingRoot "$AvatarName-extracted"
  if (Test-Path -LiteralPath $extractRoot) {
    Remove-Item -LiteralPath $extractRoot -Recurse -Force
  }
  New-Item -ItemType Directory -Force -Path $extractRoot | Out-Null

  $archiveName = $Archive.Name.ToLowerInvariant()
  if ($archiveName.EndsWith(".zip")) {
    Expand-Archive -LiteralPath $Archive.FullName -DestinationPath $extractRoot -Force
  }
  elseif ($archiveName.EndsWith(".tar.gz") -or $archiveName.EndsWith(".tgz")) {
    tar -xzf $Archive.FullName -C $extractRoot
    if ($LASTEXITCODE -ne 0) {
      throw "Failed to extract avatar archive with tar: $($Archive.FullName)"
    }
  }
  else {
    throw "Unsupported avatar archive type: $($Archive.FullName)"
  }

  return Find-FirstAssetDirectory -Root $extractRoot -Name $AvatarName
}

function Copy-RequiredFile {
  param(
    [string]$Source,
    [string]$Destination,
    [string]$Label
  )

  $existing = Get-Item -LiteralPath $Destination -ErrorAction SilentlyContinue
  if ($null -ne $existing -and $existing.Length -gt 0 -and -not $OverwriteAssets) {
    throw "$Label already exists at $Destination. Re-run with -OverwriteAssets only after confirming the source."
  }
  New-Item -ItemType Directory -Force -Path (Split-Path $Destination -Parent) | Out-Null
  Copy-Item -LiteralPath $Source -Destination $Destination -Force:$OverwriteAssets
  $copied = Get-Item -LiteralPath $Destination
  if ($copied.Length -le 0) {
    throw "$Label copy produced an empty file at $Destination."
  }
  $hash = Get-FileHash -LiteralPath $Destination -Algorithm SHA256
  Write-Output "$Label path=$Destination size=$($copied.Length) sha256=$($hash.Hash)"
}

function Copy-RequiredDirectory {
  param(
    [string]$Source,
    [string]$Destination,
    [string]$Label
  )

  $existing = Get-Item -LiteralPath $Destination -ErrorAction SilentlyContinue
  if ($null -ne $existing -and -not $OverwriteAssets) {
    throw "$Label already exists at $Destination. Re-run with -OverwriteAssets only after confirming the source."
  }
  if ($null -ne $existing -and $OverwriteAssets) {
    Remove-Item -LiteralPath $Destination -Recurse -Force
  }
  New-Item -ItemType Directory -Force -Path (Split-Path $Destination -Parent) | Out-Null
  Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
  $files = @(Get-ChildItem -LiteralPath $Destination -Recurse -File -ErrorAction Stop)
  if ($files.Count -eq 0) {
    throw "$Label copy produced an empty directory at $Destination."
  }
  $totalBytes = ($files | Measure-Object -Property Length -Sum).Sum
  Write-Output "$Label path=$Destination files=$($files.Count) bytes=$totalBytes"
  $files |
    Sort-Object FullName |
    Get-FileHash -Algorithm SHA256 |
    ForEach-Object {
      $relativePath = $_.Path.Substring($Destination.Length).TrimStart("\", "/")
      Write-Output "$Label file=$relativePath sha256=$($_.Hash)"
    }
}

if ($PrepareAssets) {
  if ([string]::IsNullOrWhiteSpace($AssetSourcePath)) {
    throw "AssetSourcePath is required when -PrepareAssets is used. Point it to the downloaded official model folder, avatar package extraction, or Windows integrated package root."
  }

  $resolvedAssetSource = Resolve-Path -LiteralPath $AssetSourcePath -ErrorAction Stop
  $sourcePath = $resolvedAssetSource.Path
  Write-Output "Preparing Wav2Lip assets from $sourcePath"
  Write-Output "This command does not download assets or read Quark/Browser login storage."

  $modelSource = Find-FirstAssetFile -Root $sourcePath -Names @("wav2lip.pth", "wav2lip256.pth")
  $s3fdSource = Find-FirstAssetFile -Root $sourcePath -Names @("s3fd.pth")
  $avatarSource = Find-FirstAssetDirectory -Root $sourcePath -Name $AvatarId
  $avatarArchiveSource = Find-FirstAssetFile -Root $sourcePath -Names @("$AvatarId.zip", "$AvatarId.tar.gz", "$AvatarId.tgz")

  $missing = @()
  if ($null -eq $modelSource) { $missing += "wav2lip.pth or wav2lip256.pth" }
  if ($null -eq $s3fdSource) { $missing += "s3fd.pth" }
  if ($null -eq $avatarSource -and $null -eq $avatarArchiveSource) { $missing += "$AvatarId directory with coords.pkl/full_imgs/face_imgs or $AvatarId.zip" }
  if ($missing.Count -gt 0) {
    throw "Asset source is incomplete. Missing: $($missing -join '; ')"
  }

  Assert-OfficialSize -File $modelSource -ExpectedSize $officialSizes.wav2lip_model -Label "wav2lip_model"
  Assert-OfficialSize -File $s3fdSource -ExpectedSize $officialSizes.s3fd_detector -Label "s3fd_detector"
  if ($null -eq $avatarSource) {
    if ($avatarArchiveSource.Name.ToLowerInvariant().EndsWith(".zip")) {
      Assert-OfficialSize -File $avatarArchiveSource -ExpectedSize $officialSizes.avatar_zip -Label "avatar_$AvatarId"
    }
    Write-Output "Expanding avatar archive from $($avatarArchiveSource.FullName)"
    $avatarSource = Expand-AvatarArchive -Archive $avatarArchiveSource -AvatarName $AvatarId
    if ($null -eq $avatarSource) {
      throw "Avatar archive did not contain expanded $AvatarId with coords.pkl/full_imgs/face_imgs."
    }
  }

  Copy-RequiredFile -Source $modelSource.FullName -Destination $modelTarget -Label "wav2lip_model"
  Copy-RequiredFile -Source $s3fdSource.FullName -Destination $s3fdTarget -Label "s3fd_detector"
  Copy-RequiredDirectory -Source $avatarSource.FullName -Destination $avatarTarget -Label "avatar_$AvatarId"
  Write-Output "Asset preparation complete. Re-run without -PrepareAssets to start LiveTalking."
  return
}

if ($Model -eq "wav2lip" -and -not $SkipAssetCheck) {
  $assetChecks = @(
    [pscustomobject]@{
      Kind = "file"
      Path = $modelTarget
      Help = "Copy official wav2lip256.pth here and rename it to wav2lip.pth."
    },
    [pscustomobject]@{
      Kind = "file"
      Path = $s3fdTarget
      Help = "Copy official s3fd.pth to the Wav2Lip SFD detector directory."
    },
    [pscustomobject]@{
      Kind = "directory"
      Path = $avatarTarget
      Help = "Run -PrepareAssets with the official wav2lip256_avatar1 archive or Windows package so coords.pkl/full_imgs/face_imgs are present."
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
    $hasRequiredAvatarFiles = $false
    if ($null -ne $dir -and $dir.PSIsContainer) {
      $hasRequiredAvatarFiles =
        (Test-Path -LiteralPath (Join-Path $check.Path "coords.pkl")) -and
        (Test-Path -LiteralPath (Join-Path $check.Path "full_imgs")) -and
        (Test-Path -LiteralPath (Join-Path $check.Path "face_imgs"))
    }
    if (-not $hasRequiredAvatarFiles) {
      $missing.Add("- Missing or incomplete directory: $($check.Path)`n  $($check.Help)") | Out-Null
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
