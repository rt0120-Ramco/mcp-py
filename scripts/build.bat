@echo off
REM Cross-platform build script launcher for Windows
REM This script calls the appropriate build method

echo ==========================================
echo FastMCP Multi-Tool Server Build Launcher
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Using Python build script for cross-platform compatibility...
echo.

REM Run the Python build script
python scripts\build.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed. Trying Windows-specific build script...
    echo.
    call scripts\windows\build.bat
)

echo.
echo Build process completed.
pause