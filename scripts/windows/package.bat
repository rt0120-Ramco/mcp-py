@echo off
REM Comprehensive packaging script for FastMCP Multi-Tool Server
REM Creates distributable packages for Windows users

echo ==========================================
echo FastMCP Multi-Tool Server Package Creator
echo ==========================================
echo.

REM Change to project root directory
cd /d "%~dp0..\.."

REM Set variables
set PACKAGE_NAME=FastMCP-Multi-Tool-Server
set VERSION=1.0.0
set DIST_DIR=package_dist
set ARCHIVE_NAME=%PACKAGE_NAME%-v%VERSION%-Windows

REM Clean up previous packaging
if exist %DIST_DIR% rmdir /s /q %DIST_DIR%
mkdir %DIST_DIR%

echo Step 1: Building Python package...
call scripts\windows\build.bat
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo Step 2: Creating standalone package directory...
mkdir %DIST_DIR%\%PACKAGE_NAME%

REM Copy essential files
echo Copying project files...
copy server.py %DIST_DIR%\%PACKAGE_NAME%\
copy requirements.txt %DIST_DIR%\%PACKAGE_NAME%\
copy README.md %DIST_DIR%\%PACKAGE_NAME%\
copy PROJECT_SUMMARY.md %DIST_DIR%\%PACKAGE_NAME%\
copy demo.py %DIST_DIR%\%PACKAGE_NAME%\
copy test_server.py %DIST_DIR%\%PACKAGE_NAME%\
copy scripts\windows\setup.bat %DIST_DIR%\%PACKAGE_NAME%\
copy scripts\windows\start_server.bat %DIST_DIR%\%PACKAGE_NAME%\

REM Copy distribution files
echo Copying built packages...
xcopy dist\* %DIST_DIR%\%PACKAGE_NAME%\dist\ /E /I

REM Create environment template
echo Creating .env template...
echo # FastMCP Multi-Tool Server Environment Configuration > %DIST_DIR%\%PACKAGE_NAME%\.env.example
echo # >> %DIST_DIR%\%PACKAGE_NAME%\.env.example
echo # Weather API Configuration (Optional) >> %DIST_DIR%\%PACKAGE_NAME%\.env.example
echo # Get your free API key from: https://openweathermap.org/api >> %DIST_DIR%\%PACKAGE_NAME%\.env.example
echo #OPENWEATHER_API_KEY=your_api_key_here >> %DIST_DIR%\%PACKAGE_NAME%\.env.example
echo # >> %DIST_DIR%\%PACKAGE_NAME%\.env.example
echo # Server Configuration (Optional) >> %DIST_DIR%\%PACKAGE_NAME%\.env.example
echo #MCP_SERVER_NAME=FastMCP-Multi-Tool-Server >> %DIST_DIR%\%PACKAGE_NAME%\.env.example
echo #MCP_SERVER_VERSION=1.0.0 >> %DIST_DIR%\%PACKAGE_NAME%\.env.example

REM Create installation script
echo Creating Windows installer script...
(
echo @echo off
echo echo ========================================
echo echo FastMCP Multi-Tool Server Installer
echo echo ========================================
echo echo.
echo.
echo echo Installing FastMCP Multi-Tool Server...
echo python --version ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo ERROR: Python is not installed or not in PATH
echo     echo Please install Python 3.8 or higher from https://python.org
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo Python found:
echo python --version
echo.
echo echo Creating virtual environment...
echo python -m venv .venv
echo if errorlevel 1 ^(
echo     echo ERROR: Failed to create virtual environment
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo Activating virtual environment...
echo call .venv\Scripts\activate.bat
echo.
echo echo Installing FastMCP server...
echo pip install dist\fastmcp_multi_tool_server-1.0.0-py3-none-any.whl
echo if errorlevel 1 ^(
echo     echo ERROR: Failed to install FastMCP server
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo Installation completed successfully!
echo echo.
echo echo To start the server, run: start_server.bat
echo echo.
echo echo For Claude Desktop integration:
echo echo 1. Copy claude_desktop_config.json content
echo echo 2. Add to your Claude Desktop config file
echo echo 3. Update paths to match your installation directory
echo echo.
echo pause
) > %DIST_DIR%\%PACKAGE_NAME%\install.bat

REM Create Claude Desktop config template
echo Creating Claude Desktop configuration template...
(
echo {
echo   "mcpServers": {
echo     "fastmcp-multi-tool": {
echo       "command": "python",
echo       "args": ["[UPDATE_THIS_PATH]/server.py"],
echo       "cwd": "[UPDATE_THIS_PATH]"
echo     }
echo   }
echo }
) > %DIST_DIR%\%PACKAGE_NAME%\claude_desktop_config.json

REM Create usage instructions
echo Creating usage instructions...
(
echo # FastMCP Multi-Tool Server - Quick Start Guide
echo.
echo ## Installation
echo.
echo 1. Run `install.bat` to set up the environment and install the server
echo 2. Copy `.env.example` to `.env` and configure if needed
echo.
echo ## Running the Server
echo.
echo 1. Run `start_server.bat` to start the MCP server
echo 2. The server will be available for Claude Desktop integration
echo.
echo ## Claude Desktop Integration
echo.
echo 1. Open the Claude Desktop configuration file:
echo    - Windows: `%%APPDATA%%\Claude\claude_desktop_config.json`
echo.
echo 2. Add the configuration from `claude_desktop_config.json`
echo.
echo 3. Update the paths in the configuration to match your installation directory
echo.
echo ## Available Tools
echo.
echo The server provides 10 comprehensive tools:
echo - Time ^& Date: get_current_time
echo - Weather: get_weather ^(requires API key^)
echo - File Operations: create_file, read_file, list_directory, create_temporary_file
echo - Search ^& Analysis: search_files, calculate_expression
echo - System Operations: execute_command, get_system_info
echo.
echo ## Testing
echo.
echo Run `python demo.py` to test the server tools
echo Run `python test_server.py` for comprehensive testing
echo.
echo ## Support
echo.
echo Visit: https://github.com/rt0120-Ramco/mcp-py
) > %DIST_DIR%\%PACKAGE_NAME%\QUICK_START.md

echo.
echo Step 3: Creating ZIP archive...
powershell -command "Compress-Archive -Path '%DIST_DIR%\%PACKAGE_NAME%' -DestinationPath '%DIST_DIR%\%ARCHIVE_NAME%.zip' -Force"

echo.
echo ==========================================
echo Packaging completed successfully!
echo ==========================================
echo.
echo Created package: %DIST_DIR%\%ARCHIVE_NAME%.zip
echo Package size: 
dir %DIST_DIR%\%ARCHIVE_NAME%.zip
echo.
echo Package contents:
echo - Standalone installation
echo - Python wheel package
echo - Complete documentation
echo - Windows batch scripts
echo - Claude Desktop configuration template
echo.
echo The package is ready for distribution!
echo.
pause