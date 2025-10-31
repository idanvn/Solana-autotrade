# View bot logs in real-time
# Usage: .\view_logs.ps1

$LogFile = "D:\Projects\Solana_autotrade\bot_log.txt"

if (Test-Path $LogFile) {
    Write-Host "📊 Live Bot Logs (Ctrl+C to exit):" -ForegroundColor Green
    Write-Host "=" * 70
    Get-Content $LogFile -Wait
}
else {
    Write-Host "⚠️ No log file found. Is the bot running?" -ForegroundColor Yellow
    Write-Host "Log file location: $LogFile" -ForegroundColor Cyan
}
