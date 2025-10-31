# 🏥 Docker Health Check
# Quick check if everything is ready for Docker deployment

Write-Host "🏥 SOL Trading Bot - Docker Readiness Check" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

$allGood = $true

# 1. Check Docker
Write-Host "1️⃣ Checking Docker..." -NoNewline
try {
    docker version | Out-Null
    Write-Host " ✅" -ForegroundColor Green
}
catch {
    Write-Host " ❌ Docker not running!" -ForegroundColor Red
    Write-Host "   💡 Start Docker Desktop" -ForegroundColor Yellow
    $allGood = $false
}

# 2. Check .env
Write-Host "2️⃣ Checking .env file..." -NoNewline
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "RPC_URL=" -and $envContent -match "WALLET_PRIVATE_KEY_JSON=") {
        Write-Host " ✅" -ForegroundColor Green
    }
    else {
        Write-Host " ⚠️ Missing variables" -ForegroundColor Yellow
        $allGood = $false
    }
}
else {
    Write-Host " ❌ Not found!" -ForegroundColor Red
    $allGood = $false
}

# 3. Check Dockerfile
Write-Host "3️⃣ Checking Dockerfile..." -NoNewline
if (Test-Path "Dockerfile") {
    Write-Host " ✅" -ForegroundColor Green
}
else {
    Write-Host " ❌" -ForegroundColor Red
    $allGood = $false
}

# 4. Check docker-compose.yml
Write-Host "4️⃣ Checking docker-compose.yml..." -NoNewline
if (Test-Path "docker-compose.yml") {
    Write-Host " ✅" -ForegroundColor Green
}
else {
    Write-Host " ❌" -ForegroundColor Red
    $allGood = $false
}

# 5. Check requirements.txt
Write-Host "5️⃣ Checking requirements.txt..." -NoNewline
if (Test-Path "requirements.txt") {
    Write-Host " ✅" -ForegroundColor Green
}
else {
    Write-Host " ❌" -ForegroundColor Red
    $allGood = $false
}

# 6. Check backend code
Write-Host "6️⃣ Checking backend code..." -NoNewline
if ((Test-Path "backend\core\wallet_manager.py") -and 
    (Test-Path "backend\core\dynamic_price_feed.py")) {
    Write-Host " ✅" -ForegroundColor Green
}
else {
    Write-Host " ❌" -ForegroundColor Red
    $allGood = $false
}

# 7. Check scripts
Write-Host "7️⃣ Checking scripts..." -NoNewline
if (Test-Path "scripts\run_live_bot.py") {
    Write-Host " ✅" -ForegroundColor Green
}
else {
    Write-Host " ❌" -ForegroundColor Red
    $allGood = $false
}

# 8. Create logs directory if needed
Write-Host "8️⃣ Checking logs directory..." -NoNewline
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host " ✅ Created" -ForegroundColor Green
}
else {
    Write-Host " ✅" -ForegroundColor Green
}

# 9. Create data directory if needed
Write-Host "9️⃣ Checking data directory..." -NoNewline
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
    Write-Host " ✅ Created" -ForegroundColor Green
}
else {
    Write-Host " ✅" -ForegroundColor Green
}

Write-Host ""
Write-Host "=" * 70

if ($allGood) {
    Write-Host "🎉 All checks passed! Ready for Docker!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 To start the bot, run:" -ForegroundColor Cyan
    Write-Host "   .\docker_start.ps1" -ForegroundColor White
}
else {
    Write-Host "⚠️ Some checks failed. Fix the issues above." -ForegroundColor Yellow
}
