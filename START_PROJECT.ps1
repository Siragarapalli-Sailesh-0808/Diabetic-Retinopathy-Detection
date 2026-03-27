# DR Detection System Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting DR Detection System" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# Stop any existing processes
Write-Host "`nStopping any running instances..." -ForegroundColor Yellow
Get-Process python,node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Get project directory
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Start Backend in new window
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
$backendDir = Join-Path $projectDir "backend"
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$backendDir'; .\venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
) -WindowStyle Normal

# Wait for backend to start
Write-Host "Waiting for backend to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Start Frontend in new window
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
$frontendDir = Join-Path $projectDir "frontend"
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$frontendDir'; npm start"
) -WindowStyle Normal

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Both servers are starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend will be at: http://localhost:8000" -ForegroundColor White
Write-Host "Frontend will be at: http://localhost:3000" -ForegroundColor White
Write-Host "`nLogin Credentials:" -ForegroundColor Yellow
Write-Host "Email: demo@demo.com" -ForegroundColor White
Write-Host "Password: Demo@123" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

# Wait and verify servers
Write-Host "`nVerifying servers..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

try {
    $backend = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "✓ Backend: RUNNING" -ForegroundColor Green
} catch {
    Write-Host "⚠ Backend: Still starting (check backend window)" -ForegroundColor Yellow
}

try {
    $frontend = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
    Write-Host "✓ Frontend: RUNNING" -ForegroundColor Green
} catch {
    Write-Host "⚠ Frontend: Still starting (check frontend window)" -ForegroundColor Yellow
}

Write-Host "`nPress any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
