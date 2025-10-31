# Stop the SOL trading bot
# Usage: .\stop_bot.ps1

$PidFile = "D:\Projects\Solana_autotrade\bot_pid.txt"

if (Test-Path $PidFile) {
    $ProcessId = Get-Content $PidFile
    
    Write-Host "🛑 Stopping bot (Process ID: $ProcessId)..." -ForegroundColor Yellow
    
    try {
        Stop-Process -Id $ProcessId -Force
        Write-Host "✅ Bot stopped successfully!" -ForegroundColor Green
        Remove-Item $PidFile
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
        Write-Host "💡 Bot might already be stopped." -ForegroundColor Cyan
    }
}
else {
    Write-Host "⚠️ No bot_pid.txt found. Is the bot running?" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To check running Python processes:" -ForegroundColor Cyan
    Write-Host '   Get-Process python' -ForegroundColor White
}
