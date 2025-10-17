@echo off
echo Starting FastMCP Multi-Tool Server...
echo ======================================

cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first or install dependencies manually.
    pause
    exit /b 1
)

REM Start the server
echo Starting server...
".venv\Scripts\python.exe" server.py

pause