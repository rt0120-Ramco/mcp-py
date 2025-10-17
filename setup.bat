@echo off
echo FastMCP Multi-Tool Server Setup
echo ================================

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or later and try again.
    pause
    exit /b 1
)

echo Python found. Setting up virtual environment...

REM Create virtual environment
if not exist ".venv" (
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment and install dependencies
echo Installing dependencies...
".venv\Scripts\pip.exe" install --upgrade pip
".venv\Scripts\pip.exe" install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the server:
echo   1. Run start_server.bat, or
echo   2. Run: python server.py
echo.
echo For Claude Desktop integration:
echo   1. Copy claude_desktop_config.json content
echo   2. Add it to your Claude Desktop config
echo   3. Update paths to match your installation
echo.
echo See README.md for detailed instructions.
echo.

pause