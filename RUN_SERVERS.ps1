# Simple server startup script
Write-Host @"
================================
   DR Detection System
================================
"@ -ForegroundColor Cyan

# Kill existing servers
Get-Process python,node -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

$projectDir = "c:\Users\NAGA PRASAD\Downloads\GAN-Driven_ Diabetic_Retinopathy_Detection"

# Start backend
Write-Host "`nStarting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd '$projectDir\backend'; .\venv\Scripts\Activate.ps1; Write-Host '=== BACKEND SERVER ===' -ForegroundColor Green; Write-Host 'Starting on http://localhost:8000' -ForegroundColor Cyan; Write-Host 'Keep this window open!`n' -ForegroundColor Yellow; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

Write-Host "Waiting for backend to load ML models..." -ForegroundColor Gray
Start-Sleep -Seconds 20

# Start frontend
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList `
    "-NoExit", `
    "-Command", `
    "cd '$projectDir\frontend'; Write-Host '=== FRONTEND SERVER ===' -ForegroundColor Green; Write-Host 'Starting on http://localhost:3000' -ForegroundColor Cyan; Write-Host 'Keep this window open!`n' -ForegroundColor Yellow; npm start"

Start-Sleep -Seconds 5

Write-Host @"

================================
   Servers Starting!
================================
 Backend:  http://localhost:8000
 Frontend: http://localhost:3000

 Demo Login:
   Email:    demo@demo.com
   Password: Demo@123

 Keep the server windows open!
================================

"@ -ForegroundColor Green

Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
