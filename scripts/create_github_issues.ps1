param(
    [string]$Repository = "archibald80000-ai/jiyangjia-android-ai"
)

$ErrorActionPreference = "Stop"
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw "gh is required" }
gh auth status

$labels = @(
    "type:task", "type:bug", "type:feature",
    "area:docs", "area:livetalking", "area:android", "area:audio", "area:gateway", "area:knowledge", "area:deploy",
    "priority:p0", "priority:p1", "priority:p2",
    "status:blocked", "status:needs-device", "status:needs-gpu", "status:needs-owner"
)
foreach ($label in $labels) {
    try { gh label create $label --repo $Repository --force | Out-Null } catch { Write-Warning $_ }
}

Get-ChildItem "tasks/TASK-*.md" | Sort-Object Name | ForEach-Object {
    $titleLine = Get-Content $_.FullName | Select-Object -First 1
    $title = $titleLine -replace '^#\s*', ''
    $existing = gh issue list --repo $Repository --search ('"' + $title + '" in:title') --json number,title | ConvertFrom-Json
    if (-not $existing) {
        gh issue create --repo $Repository --title $title --body-file $_.FullName --label "type:task"
    } else {
        Write-Host "Issue already exists for $title"
    }
}
