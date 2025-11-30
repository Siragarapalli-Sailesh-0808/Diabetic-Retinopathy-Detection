@echo off
echo ========================================
echo Starting DR Detection System
echo ========================================

REM Kill any existing processes
echo Stopping any running instances...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

REM Start Backend in new window
echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d "%~dp0backend" && call venv\Scripts\activate && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

REM Wait for backend to initialize
echo Waiting for backend to start...
timeout /t 15 /nobreak >nul

REM Start Frontend in new window
echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d "%~dp0frontend" && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo ========================================
echo Backend will be at: http://localhost:8000
echo Frontend will be at: http://localhost:3000
echo.
echo Login Credentials:
echo Email: demo@demo.com
echo Password: Demo@123
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul
