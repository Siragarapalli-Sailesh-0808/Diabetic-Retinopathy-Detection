@echo off
cd /d "%~dp0"
call venv\Scripts\activate.bat
echo.
echo ========================================
echo   DR Detection Backend Server
echo ========================================
echo.
echo Starting server on http://localhost:8000
echo.
python -m uvicorn app.main:app --host localhost --port 8000 --reload
pause
