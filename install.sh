#!/bin/bash
# FastMCP Multi-Tool Server Installer for Linux/macOS
# Standalone installer script that can be distributed separately

set -e

echo "========================================"
echo "FastMCP Multi-Tool Server Installer"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    echo
    echo "Installation instructions:"
    echo "Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    echo "CentOS/RHEL:   sudo yum install python3 python3-pip"
    echo "Fedora:        sudo dnf install python3 python3-pip"
    echo "Arch Linux:    sudo pacman -S python python-pip"
    echo "macOS:         brew install python3"
    echo
    exit 1
fi

# Use python3 if available, otherwise python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PIP_CMD=pip3
else
    PYTHON_CMD=python
    PIP_CMD=pip
fi

echo "Python found:"
$PYTHON_CMD --version

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info[0])')
PYTHON_MINOR=$($PYTHON_CMD -c 'import sys; print(sys.version_info[1])')

if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
    echo "ERROR: Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "Python version check passed: $PYTHON_VERSION"

echo
echo "Creating virtual environment..."
$PYTHON_CMD -m venv .venv
if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to create virtual environment"
    echo "You may need to install python3-venv:"
    echo "Ubuntu/Debian: sudo apt install python3-venv"
    echo "CentOS/RHEL:   sudo yum install python3-devel"
    exit 1
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

# Check if we have wheel files to install
if ls dist/fastmcp_multi_tool_server-*.whl 1> /dev/null 2>&1; then
    echo "Installing FastMCP server from wheel..."
    pip install dist/fastmcp_multi_tool_server-*.whl
else
    echo "Installing FastMCP server from requirements..."
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
    else
        echo "Installing from PyPI..."
        pip install fastmcp requests python-dotenv pydantic psutil
    fi
fi

if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to install FastMCP server"
    exit 1
fi

# Create startup script if it doesn't exist
if [[ ! -f "start_server.sh" ]]; then
    echo "Creating startup script..."
    cat > start_server.sh << 'EOF'
#!/bin/bash
# FastMCP Multi-Tool Server Startup Script

echo "Starting FastMCP Multi-Tool Server..."

# Check if virtual environment exists
if [[ ! -d ".venv" ]]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run install.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Start the server
echo "FastMCP Multi-Tool Server is starting..."
echo "Press Ctrl+C to stop the server"
echo
python server.py
EOF
    chmod +x start_server.sh
fi

# Create environment template if it doesn't exist
if [[ ! -f ".env.example" ]] && [[ ! -f ".env" ]]; then
    echo "Creating environment template..."
    cat > .env.example << 'EOF'
# FastMCP Multi-Tool Server Environment Configuration
#
# Weather API Configuration (Optional)
# Get your free API key from: https://openweathermap.org/api
#OPENWEATHER_API_KEY=your_api_key_here
#
# Server Configuration (Optional)
#MCP_SERVER_NAME=FastMCP-Multi-Tool-Server
#MCP_SERVER_VERSION=1.0.0
EOF
fi

echo
echo "========================================"
echo "Installation completed successfully!"
echo "========================================"
echo
echo "Next steps:"
echo "1. (Optional) Copy .env.example to .env and configure"
echo "2. Start the server: ./start_server.sh"
echo "   Or manually: source .venv/bin/activate && python server.py"
echo
echo "For Claude Desktop integration:"
echo "1. Add configuration to Claude Desktop config file:"
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   ~/Library/Application Support/Claude/claude_desktop_config.json"
else
    echo "   ~/.config/Claude/claude_desktop_config.json"
fi
echo "2. Use this configuration (update paths):"
echo '{'
echo '  "mcpServers": {'
echo '    "fastmcp-multi-tool": {'
echo '      "command": "python",'
echo "      \"args\": [\"$(pwd)/server.py\"],"
echo "      \"cwd\": \"$(pwd)\""
echo '    }'
echo '  }'
echo '}'
echo
echo "Test the installation:"
echo "  source .venv/bin/activate"
echo "  python demo.py"
echo