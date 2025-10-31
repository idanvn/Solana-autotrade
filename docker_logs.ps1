# 📊 View SOL Trading Bot Logs
# Usage: .\docker_logs.ps1

param(
    [int]$Lines = 100,
    [switch]$Follow
)

Write-Host "📊 SOL Trading Bot Logs" -ForegroundColor Cyan
Write-Host "=" * 70

if ($Follow) {
    Write-Host "👀 Following logs (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose logs -f --tail=$Lines
}
else {
    Write-Host "📄 Last $Lines lines:" -ForegroundColor Yellow
    docker-compose logs --tail=$Lines
}
