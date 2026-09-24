# GitHub Token 需要从环境变量传入，不要硬编码在脚本中
# 用法: $env:GH_TOKEN='your_token'; powershell -ExecutionPolicy Bypass -File scripts\daily_check.ps1

if (-not $env:GH_TOKEN) {
    Write-Host "[ERROR] 请先设置 GH_TOKEN 环境变量"
    exit 1
}

Write-Host "=== GitHub Repo Info ==="
gh repo view wyjing333-dev/promptblocks --json stargazerCount,forkCount,issues,description
Write-Host ""
Write-Host "=== Issue List ==="
gh issue list --repo wyjing333-dev/promptblocks --state open --limit 20
Write-Host ""
Write-Host "=== Traffic Views ==="
gh api repos/wyjing333-dev/promptblocks/traffic/views
Write-Host ""
Write-Host "=== Traffic Clones ==="
gh api repos/wyjing333-dev/promptblocks/traffic/clones
