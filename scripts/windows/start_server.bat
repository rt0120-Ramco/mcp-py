@echo off
echo Starting FastMCP Multi-Tool Server...
echo ======================================

REM Try to find project root - check if we're in scripts/windows or project root
if exist "server.py" (
    REM We're in project root or distribution package
    set PROJECT_ROOT=%cd%
) else if exist "..\..\server.py" (
    REM We're in scripts/windows subdirectory
    cd /d "%~dp0..\.."
    set PROJECT_ROOT=%cd%
) else (
    echo ERROR: Cannot find server.py. Please run from project root or ensure server.py exists.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first or install dependencies manually.
    pause
    exit /b 1
)

REM Start the server
echo Starting server from: %PROJECT_ROOT%
".venv\Scripts\python.exe" server.py

pause