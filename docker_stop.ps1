# 🛑 Stop SOL Trading Bot Docker Container
# Usage: .\docker_stop.ps1

Write-Host "🛑 Stopping SOL Trading Bot..." -ForegroundColor Yellow

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Bot stopped successfully!" -ForegroundColor Green
}
else {
    Write-Host "⚠️ Error stopping bot" -ForegroundColor Red
}

Write-Host ""
Write-Host "📊 Remaining containers:" -ForegroundColor Cyan
docker ps -a | Select-String "sol"
