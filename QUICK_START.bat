@echo off
echo ========================================
echo  DR Detection - Quick Start
echo ========================================
echo.

REM Kill any stuck processes from before sleep
echo Cleaning up old processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

REM Start Backend
echo Starting Backend Server...
start "DR Backend" powershell -NoExit -Command "cd '%~dp0backend'; .\venv\Scripts\Activate.ps1; Write-Host '=== BACKEND SERVER ===' -ForegroundColor Cyan; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

REM Wait for backend to load
echo Waiting for backend to initialize (15 seconds)...
timeout /t 15 /nobreak >nul

REM Start Frontend
echo Starting Frontend Server...
start "DR Frontend" powershell -NoExit -Command "cd '%~dp0frontend'; Write-Host '=== FRONTEND SERVER ===' -ForegroundColor Cyan; npm start"

echo.
echo ========================================
echo  Servers Starting!
echo ========================================
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo.
echo Login: demo@demo.com / Demo@123
echo ========================================
echo.
echo You can close this window.
echo Keep the Backend and Frontend windows open!
timeout /t 5 /nobreak >nul
