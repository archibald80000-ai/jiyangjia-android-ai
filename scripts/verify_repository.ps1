$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root

$required = @(
    "README.md", "AGENTS.md", "MEMORY.md", "PROJECT_STATE.md",
    "tasks/index.yaml", "config/upstream-lock.json", ".env.example", ".gitignore"
)
foreach ($file in $required) {
    if (-not (Test-Path $file)) { throw "Missing required file: $file" }
}

python -m json.tool config/upstream-lock.json | Out-Null
python -m json.tool PROJECT_MANIFEST.json | Out-Null
python -m json.tool knowledge-test/test_questions.example.json | Out-Null

if (Test-Path ".git") {
    $trackedSensitive = git ls-files | Select-String -Pattern '(^|/)(\.env|\.env\.local|.*\.pem|.*\.key|.*\.p12|.*\.pfx|.*\.jks|.*\.keystore)$'
    if ($trackedSensitive) { throw "Tracked sensitive filename detected." }

    $trackedBinary = git ls-files | Select-String -Pattern '\.(apk|aab|pth|pt|ckpt|onnx|wav|mp3|mp4|db|sqlite3)$'
    if ($trackedBinary) { throw "Tracked binary/model/audio/data file requires explicit review." }
}

Write-Host "Repository verification: PASS"
