# ============================================================
# NUROTHON AI SMB - PRODUCTION DEPLOYMENT (Windows)
# ============================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 NUROTHON AI SMB - PRODUCTION DEPLOYMENT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Check if Docker is installed
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose is not installed." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️  .env file not found. Creating from .env.production..." -ForegroundColor Yellow
    Copy-Item .env.production .env
    Write-Host "⚠️  Please edit .env file and update production values!" -ForegroundColor Yellow
    Write-Host "⚠️  Press Enter to continue or Ctrl+C to abort..." -ForegroundColor Yellow
    Read-Host
}

Write-Host "✅ Environment file found" -ForegroundColor Green

# Build and start containers
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "📦 BUILDING DOCKER IMAGES" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

docker-compose -f docker-compose.prod.yml build

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING CONTAINERS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

docker-compose -f docker-compose.prod.yml up -d

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "⏳ WAITING FOR SERVICES TO BE HEALTHY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Wait for services
Write-Host "Waiting for database..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "Waiting for backend..." -ForegroundColor Yellow
$retries = 0
$maxRetries = 30
while ($retries -lt $maxRetries) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ Backend is ready" -ForegroundColor Green
            break
        }
    } catch {
        $retries++
        Start-Sleep -Seconds 3
    }
}

if ($retries -eq $maxRetries) {
    Write-Host "❌ Backend failed to start" -ForegroundColor Red
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
}

Write-Host "Waiting for frontend..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://localhost/" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Frontend is ready" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Frontend may still be starting..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "🎉 DEPLOYMENT SUCCESSFUL!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Service URLs:" -ForegroundColor Cyan
Write-Host "   Frontend:  http://localhost" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host "   Database:  localhost:5432" -ForegroundColor White
Write-Host ""
Write-Host "📝 Useful Commands:" -ForegroundColor Cyan
Write-Host "   View logs:        docker-compose -f docker-compose.prod.yml logs -f" -ForegroundColor White
Write-Host "   Stop services:    docker-compose -f docker-compose.prod.yml down" -ForegroundColor White
Write-Host "   Restart:          docker-compose -f docker-compose.prod.yml restart" -ForegroundColor White
Write-Host "   View status:      docker-compose -f docker-compose.prod.yml ps" -ForegroundColor White
Write-Host ""
Write-Host "🔒 Security Reminder:" -ForegroundColor Yellow
Write-Host "   - Update SECRET_KEY in .env" -ForegroundColor White
Write-Host "   - Update POSTGRES_PASSWORD in .env" -ForegroundColor White
Write-Host "   - Configure ALLOWED_ORIGINS for your domain" -ForegroundColor White
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
