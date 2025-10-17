@echo off
REM Build script for FastMCP Multi-Tool Server
REM This script builds the Python package for distribution

echo ========================================
echo FastMCP Multi-Tool Server Build Script
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check if we're in a virtual environment
if defined VIRTUAL_ENV (
    echo Using virtual environment: %VIRTUAL_ENV%
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ERROR: Failed to activate virtual environment
        pause
        exit /b 1
    )
)

echo.
echo Installing/upgrading build tools...
python -m pip install --upgrade pip setuptools wheel build twine
if errorlevel 1 (
    echo ERROR: Failed to install build tools
    pause
    exit /b 1
)

echo.
echo Installing project dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Cleaning previous build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.egg-info rmdir /s /q *.egg-info

echo.
echo Building source distribution...
python -m build --sdist
if errorlevel 1 (
    echo ERROR: Failed to build source distribution
    pause
    exit /b 1
)

echo.
echo Building wheel distribution...
python -m build --wheel
if errorlevel 1 (
    echo ERROR: Failed to build wheel distribution
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo Build artifacts created in 'dist' folder:
dir dist
echo.
echo To install the package locally, run:
echo   pip install dist\fastmcp_multi_tool_server-1.0.0-py3-none-any.whl
echo.
echo To upload to PyPI (requires authentication), run:
echo   twine upload dist/*
echo.
pause