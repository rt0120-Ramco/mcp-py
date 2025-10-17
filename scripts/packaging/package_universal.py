#!/usr/bin/env python3
"""
Cross-platform packaging script for FastMCP Multi-Tool Server
Works on Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import shutil
import zipfile
import tarfile
import platform
from pathlib import Path

def run_command(cmd, shell=False):
    """Run a command and handle errors"""
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, shell=shell)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed: {e.cmd}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def get_python_command():
    """Get the appropriate Python command for this system"""
    for cmd in ['python3', 'python']:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return cmd
        except FileNotFoundError:
            continue
    
    print("ERROR: Python not found in PATH")
    sys.exit(1)

def build_package():
    """Build the Python package"""
    print("Building Python package...")
    python_cmd = get_python_command()
    
    # Install build tools
    run_command([python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel', 'build'])
    
    # Clean previous builds
    for path in ['build', 'dist', '*.egg-info']:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    # Build source and wheel distributions
    run_command([python_cmd, '-m', 'build', '--sdist'])
    run_command([python_cmd, '-m', 'build', '--wheel'])
    
    print("✓ Package built successfully")

def create_package_structure(dist_dir, package_name):
    """Create the package directory structure"""
    package_dir = os.path.join(dist_dir, package_name)
    
    # Clean and create directories
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(package_dir)
    
    # Copy essential files
    files_to_copy = [
        'server.py', 'requirements.txt', 'README.md', 'PROJECT_SUMMARY.md',
        'demo.py', 'test_server.py', 'setup.py', 'MANIFEST.in'
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
    
    # Copy distribution files
    if os.path.exists('dist'):
        shutil.copytree('dist', os.path.join(package_dir, 'dist'))
    
    return package_dir

def create_cross_platform_scripts(package_dir):
    """Create installation and startup scripts for all platforms"""
    
    # Create .env.example
    env_content = """# FastMCP Multi-Tool Server Environment Configuration
#
# Weather API Configuration (Optional)
# Get your free API key from: https://openweathermap.org/api
#OPENWEATHER_API_KEY=your_api_key_here
#
# Server Configuration (Optional)
#MCP_SERVER_NAME=FastMCP-Multi-Tool-Server
#MCP_SERVER_VERSION=1.0.0
"""
    with open(os.path.join(package_dir, '.env.example'), 'w') as f:
        f.write(env_content)
    
    # Windows installation script
    install_bat = """@echo off
echo ========================================
echo FastMCP Multi-Tool Server Installer
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found:
python --version

echo.
echo Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\\Scripts\\activate.bat

echo Installing FastMCP server...
pip install dist\\fastmcp_multi_tool_server-*.whl
if errorlevel 1 (
    echo ERROR: Failed to install FastMCP server
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo To start the server, run: start_server.bat
pause
"""
    
    # Windows startup script
    start_bat = """@echo off
echo Starting FastMCP Multi-Tool Server...

if not exist .venv (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first
    pause
    exit /b 1
)

call .venv\\Scripts\\activate.bat
echo FastMCP Multi-Tool Server is starting...
echo Press Ctrl+C to stop the server
python server.py
"""
    
    # Linux/macOS installation script
    install_sh = """#!/bin/bash
set -e

echo "========================================"
echo "FastMCP Multi-Tool Server Installer"
echo "========================================"

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python)
echo "Using: $($PYTHON_CMD --version)"

echo "Creating virtual environment..."
$PYTHON_CMD -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing FastMCP server..."
pip install dist/fastmcp_multi_tool_server-*.whl

echo "Installation completed successfully!"
echo "To start: ./start_server.sh"
"""
    
    # Linux/macOS startup script
    start_sh = """#!/bin/bash
echo "Starting FastMCP Multi-Tool Server..."

if [[ ! -d ".venv" ]]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./install.sh first"
    exit 1
fi

source .venv/bin/activate
echo "FastMCP Multi-Tool Server is starting..."
echo "Press Ctrl+C to stop"
python server.py
"""
    
    # Write all scripts
    scripts = [
        ('install.bat', install_bat),
        ('start_server.bat', start_bat),
        ('install.sh', install_sh),
        ('start_server.sh', start_sh)
    ]
    
    for filename, content in scripts:
        script_path = os.path.join(package_dir, filename)
        with open(script_path, 'w', newline='\n' if filename.endswith('.sh') else '\r\n') as f:
            f.write(content)
        
        # Make shell scripts executable on Unix systems
        if filename.endswith('.sh') and os.name != 'nt':
            os.chmod(script_path, 0o755)

def create_documentation(package_dir):
    """Create comprehensive documentation"""
    
    quick_start = """# FastMCP Multi-Tool Server - Quick Start Guide

## Installation

### Windows
1. Run `install.bat`
2. Start with `start_server.bat`

### Linux/macOS
1. Run `./install.sh`
2. Start with `./start_server.sh`

## Claude Desktop Integration

Add to your Claude Desktop config file:

**Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fastmcp-multi-tool": {
      "command": "python",
      "args": ["[UPDATE_THIS_PATH]/server.py"],
      "cwd": "[UPDATE_THIS_PATH]"
    }
  }
}
```

## Available Tools

1. **get_current_time** - Current date and time
2. **get_weather** - Weather information (requires API key)
3. **create_file** - Create new files
4. **read_file** - Read file contents
5. **list_directory** - List directory contents
6. **execute_command** - Safe command execution
7. **search_files** - Text search in files
8. **calculate_expression** - Mathematical calculations
9. **get_system_info** - System information
10. **create_temporary_file** - Create temporary files

## Testing

```bash
# Windows
.venv\\Scripts\\activate
python demo.py

# Linux/macOS
source .venv/bin/activate
python demo.py
```

## Support

GitHub: https://github.com/rt0120-Ramco/mcp-py
"""
    
    with open(os.path.join(package_dir, 'QUICK_START.md'), 'w') as f:
        f.write(quick_start)

def create_archives(dist_dir, package_name):
    """Create platform-specific archives"""
    system = platform.system().lower()
    
    if system == 'windows':
        # Create ZIP for Windows
        zip_name = f"{package_name}-v1.0.0-Windows.zip"
        zip_path = os.path.join(dist_dir, zip_name)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            package_path = os.path.join(dist_dir, package_name)
            for root, dirs, files in os.walk(package_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, dist_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✓ Created Windows package: {zip_path}")
    
    else:
        # Create TAR.GZ for Linux/macOS
        tar_name = f"{package_name}-v1.0.0-Unix.tar.gz"
        tar_path = os.path.join(dist_dir, tar_name)
        
        with tarfile.open(tar_path, 'w:gz') as tar:
            package_path = os.path.join(dist_dir, package_name)
            tar.add(package_path, arcname=package_name)
        
        print(f"✓ Created Unix package: {tar_path}")

def main():
    """Main packaging function"""
    print("=" * 50)
    print("FastMCP Multi-Tool Server Cross-Platform Packager")
    print("=" * 50)
    print()
    
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    os.chdir(project_root)
    print(f"Working directory: {os.getcwd()}")
    print()
    
    # Configuration
    package_name = "FastMCP-Multi-Tool-Server"
    dist_dir = "package_dist"
    
    try:
        # Step 1: Build the Python package
        build_package()
        
        # Step 2: Create package structure
        print("Creating package structure...")
        package_dir = create_package_structure(dist_dir, package_name)
        
        # Step 3: Create cross-platform scripts
        print("Creating installation scripts...")
        create_cross_platform_scripts(package_dir)
        
        # Step 4: Create documentation
        print("Creating documentation...")
        create_documentation(package_dir)
        
        # Step 5: Create archives
        print("Creating distribution archives...")
        create_archives(dist_dir, package_name)
        
        print()
        print("=" * 50)
        print("Packaging completed successfully!")
        print("=" * 50)
        print()
        print(f"Package directory: {package_dir}")
        print("Distribution files created in:", dist_dir)
        print()
        
        # List created files
        for item in os.listdir(dist_dir):
            item_path = os.path.join(dist_dir, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                print(f"  {item} ({size:,} bytes)")
        
        print()
        print("Ready for distribution!")
        
    except Exception as e:
        print(f"ERROR: Packaging failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()