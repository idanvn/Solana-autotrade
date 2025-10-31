# 🚀 Start SOL Trading Bot in Docker
# Usage: .\docker_start.ps1

Write-Host "🐋 Starting SOL Trading Bot in Docker..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
try {
    docker version | Out-Null
}
catch {
    Write-Host "❌ Docker is not running!" -ForegroundColor Red
    Write-Host "💡 Please start Docker Desktop first." -ForegroundColor Yellow
    exit 1
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "💡 Create .env file with your RPC_URL and WALLET_PRIVATE_KEY_JSON" -ForegroundColor Yellow
    exit 1
}

# Create logs directory if not exists
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "📁 Created logs directory" -ForegroundColor Green
}

# Create data directory if not exists
if (-not (Test-Path "data")) {
    New-Item -ItemType Directory -Path "data" | Out-Null
    Write-Host "📁 Created data directory" -ForegroundColor Green
}

Write-Host "🔨 Building Docker image..." -ForegroundColor Yellow
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Build successful!" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Starting container..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Bot started successfully!" -ForegroundColor Green
Write-Host ""

# Wait a moment for container to initialize
Start-Sleep -Seconds 2

# Show status
Write-Host "📊 Container Status:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "📋 Useful Commands:" -ForegroundColor Yellow
Write-Host "   View logs:      docker-compose logs -f" -ForegroundColor White
Write-Host "   Stop bot:       docker-compose down" -ForegroundColor White
Write-Host "   Restart:        docker-compose restart" -ForegroundColor White
Write-Host "   Check status:   docker-compose ps" -ForegroundColor White
Write-Host ""

Write-Host "👀 Showing recent logs (Ctrl+C to exit)..." -ForegroundColor Cyan
Write-Host "=" * 70
Start-Sleep -Seconds 3
docker-compose logs -f --tail=50
