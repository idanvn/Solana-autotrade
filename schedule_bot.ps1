# Create a Windows Task Scheduler task to run the bot on startup
# Usage: Run PowerShell as Administrator, then: .\schedule_bot.ps1

$TaskName = "SOL_Trading_Bot"
$ScriptPath = "D:\Projects\Solana_autotrade\scripts\run_live_bot.py"
$PythonPath = "D:\Projects\Solana_autotrade\.venv\Scripts\python.exe"
$WorkingDir = "D:\Projects\Solana_autotrade"

Write-Host "🔧 Creating Windows Task Scheduler task..." -ForegroundColor Cyan
Write-Host ""

# Define the action (run Python script)
$Action = New-ScheduledTaskAction -Execute $PythonPath `
                                   -Argument $ScriptPath `
                                   -WorkingDirectory $WorkingDir

# Define the trigger (at startup)
$Trigger = New-ScheduledTaskTrigger -AtStartup

# Define settings
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries `
                                          -DontStopIfGoingOnBatteries `
                                          -StartWhenAvailable `
                                          -RestartCount 3 `
                                          -RestartInterval (New-TimeSpan -Minutes 1)

# Register the task
try {
    Register-ScheduledTask -TaskName $TaskName `
                           -Action $Action `
                           -Trigger $Trigger `
                           -Settings $Settings `
                           -Description "SOL Trading Bot - Auto trading with live prices" `
                           -Force
    
    Write-Host "✅ Task created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Task Details:" -ForegroundColor Yellow
    Write-Host "   Name: $TaskName" -ForegroundColor White
    Write-Host "   Trigger: At system startup" -ForegroundColor White
    Write-Host "   Script: $ScriptPath" -ForegroundColor White
    Write-Host ""
    Write-Host "🎮 Control the task:" -ForegroundColor Yellow
    Write-Host "   Start:  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host "   Stop:   Stop-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host "   Status: Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host "   Remove: Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false" -ForegroundColor White
    Write-Host ""
    Write-Host "⚠️ NOTE: The bot will start automatically when Windows starts!" -ForegroundColor Red
}
catch {
    Write-Host "❌ Error creating task: $_" -ForegroundColor Red
    Write-Host "💡 Make sure you run PowerShell as Administrator!" -ForegroundColor Yellow
}
