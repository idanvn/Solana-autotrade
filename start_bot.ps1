# Start the SOL trading bot in the background
# Usage: .\start_bot.ps1

$BotPath = "D:\Projects\Solana_autotrade\scripts\run_live_bot.py"
$PythonPath = "D:\Projects\Solana_autotrade\.venv\Scripts\python.exe"
$LogFile = "D:\Projects\Solana_autotrade\bot_log.txt"

Write-Host "🚀 Starting SOL Trading Bot..." -ForegroundColor Green
Write-Host "📝 Log file: $LogFile" -ForegroundColor Cyan

# Start the bot in a new background process
$Process = Start-Process -FilePath $PythonPath `
                         -ArgumentList $BotPath `
                         -RedirectStandardOutput $LogFile `
                         -RedirectStandardError "$LogFile.err" `
                         -PassThru `
                         -WindowStyle Hidden

Write-Host "✅ Bot started! Process ID: $($Process.Id)" -ForegroundColor Green
Write-Host ""
Write-Host "📊 To view live output:" -ForegroundColor Yellow
Write-Host "   Get-Content $LogFile -Wait" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop the bot:" -ForegroundColor Yellow
Write-Host "   Stop-Process -Id $($Process.Id)" -ForegroundColor White
Write-Host ""

# Save process ID
$Process.Id | Out-File "bot_pid.txt"
Write-Host "💾 Process ID saved to bot_pid.txt" -ForegroundColor Cyan
