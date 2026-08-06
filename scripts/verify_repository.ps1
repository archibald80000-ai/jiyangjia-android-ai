$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root

$required = @(
    "README.md", "AGENTS.md", "MEMORY.md", "PROJECT_STATE.md",
    "ROADMAP.md", "TASKS.md", "CODEX_START_HERE.md",
    "PROJECT_MANIFEST.json", "VERSION", "CHANGELOG.md",
    "tasks/index.yaml", "config/upstream-lock.json", ".env.example", ".gitignore",
    ".github/CODEOWNERS", ".github/PULL_REQUEST_TEMPLATE.md",
    "android-app/README.md", "gateway/README.md", "integration/README.md",
    "knowledge-test/README.md", "memory/CORE_FACTS.md", "docs/README.md"
)
foreach ($file in $required) {
    if (-not (Test-Path $file)) { throw "Missing required file: $file" }
}

$requiredDirs = @(
    ".codex", ".github", "android-app", "assets", "config", "deploy",
    "docs", "gateway", "integration", "knowledge-test", "memory",
    "scripts", "tasks", "tests", "third_party"
)
foreach ($dir in $requiredDirs) {
    if (-not (Test-Path $dir -PathType Container)) { throw "Missing required directory: $dir" }
}

python -m json.tool config/upstream-lock.json | Out-Null
python -m json.tool PROJECT_MANIFEST.json | Out-Null
python -m json.tool knowledge-test/test_questions.example.json | Out-Null

if (Test-Path ".git") {
    $trackedSensitive = git ls-files | Select-String -Pattern '(^|/)(\.env|\.env\.local|.*\.pem|.*\.key|.*\.p12|.*\.pfx|.*\.jks|.*\.keystore)$'
    if ($trackedSensitive) { throw "Tracked sensitive filename detected." }

    $trackedBinary = git ls-files | Select-String -Pattern '\.(apk|aab|pth|pt|ckpt|onnx|wav|mp3|mp4|db|sqlite3)$'
    if ($trackedBinary) { throw "Tracked binary/model/audio/data file requires explicit review." }

    $origin = $null
    try { $origin = git remote get-url origin 2>$null } catch {}
    if ($origin -and $origin -notmatch 'archibald80000-ai/jiyangjia-android-ai(\.git)?$') {
        throw "Origin remote points to unexpected repository: $origin"
    }
}

Write-Host "Repository verification: PASS"
