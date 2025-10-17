#!/bin/bash
# Comprehensive packaging script for FastMCP Multi-Tool Server (Linux/macOS)
# Creates distributable packages for Unix-like systems

set -e  # Exit on any error

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

echo "=========================================="
echo "FastMCP Multi-Tool Server Package Creator"
echo "=========================================="
echo "Working directory: $(pwd)"
echo

# Set variables
PACKAGE_NAME="FastMCP-Multi-Tool-Server"
VERSION="1.0.0"
DIST_DIR="package_dist"
ARCHIVE_NAME="${PACKAGE_NAME}-v${VERSION}-Linux"

# Clean up previous packaging
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

echo "Step 1: Building Python package..."
chmod +x scripts/unix/build.sh
scripts/unix/build.sh
if [[ $? -ne 0 ]]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo
echo "Step 2: Creating standalone package directory..."
mkdir -p "$DIST_DIR/$PACKAGE_NAME"

# Copy essential files
echo "Copying project files..."
cp server.py "$DIST_DIR/$PACKAGE_NAME/"
cp requirements.txt "$DIST_DIR/$PACKAGE_NAME/"
cp README.md "$DIST_DIR/$PACKAGE_NAME/"
cp PROJECT_SUMMARY.md "$DIST_DIR/$PACKAGE_NAME/"
cp demo.py "$DIST_DIR/$PACKAGE_NAME/"
cp test_server.py "$DIST_DIR/$PACKAGE_NAME/"

# Copy Linux scripts
cp scripts/unix/build.sh "$DIST_DIR/$PACKAGE_NAME/"
chmod +x "$DIST_DIR/$PACKAGE_NAME/build.sh"

# Copy distribution files
echo "Copying built packages..."
cp -r dist "$DIST_DIR/$PACKAGE_NAME/"

# Create environment template
echo "Creating .env template..."
cat > "$DIST_DIR/$PACKAGE_NAME/.env.example" << 'EOF'
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

# Create installation script
echo "Creating Linux installer script..."
cat > "$DIST_DIR/$PACKAGE_NAME/install.sh" << 'EOF'
#!/bin/bash
# FastMCP Multi-Tool Server Installer for Linux/macOS

set -e

echo "========================================"
echo "FastMCP Multi-Tool Server Installer"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python3"
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

echo
echo "Creating virtual environment..."
$PYTHON_CMD -m venv .venv
if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing FastMCP server..."
pip install dist/fastmcp_multi_tool_server-*.whl
if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to install FastMCP server"
    exit 1
fi

echo
echo "Installation completed successfully!"
echo
echo "To start the server:"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Run: python server.py"
echo
echo "For Claude Desktop integration:"
echo "1. Copy claude_desktop_config.json content"
echo "2. Add to your Claude Desktop config file"
echo "3. Update paths to match your installation directory"
echo
echo "Configuration file locations:"
echo "- macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "- Linux: ~/.config/Claude/claude_desktop_config.json"
echo
EOF

chmod +x "$DIST_DIR/$PACKAGE_NAME/install.sh"

# Create startup script
echo "Creating startup script..."
cat > "$DIST_DIR/$PACKAGE_NAME/start_server.sh" << 'EOF'
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

chmod +x "$DIST_DIR/$PACKAGE_NAME/start_server.sh"

# Create Claude Desktop config template
echo "Creating Claude Desktop configuration template..."
cat > "$DIST_DIR/$PACKAGE_NAME/claude_desktop_config.json" << 'EOF'
{
  "mcpServers": {
    "fastmcp-multi-tool": {
      "command": "python",
      "args": ["[UPDATE_THIS_PATH]/server.py"],
      "cwd": "[UPDATE_THIS_PATH]"
    }
  }
}
EOF

# Create usage instructions
echo "Creating usage instructions..."
cat > "$DIST_DIR/$PACKAGE_NAME/QUICK_START.md" << 'EOF'
# FastMCP Multi-Tool Server - Quick Start Guide (Linux/macOS)

## Installation

1. Run `./install.sh` to set up the environment and install the server
2. Copy `.env.example` to `.env` and configure if needed

## Running the Server

### Option 1: Using the startup script
```bash
./start_server.sh
```

### Option 2: Manual start
```bash
source .venv/bin/activate
python server.py
```

## Claude Desktop Integration

1. Open the Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the configuration from `claude_desktop_config.json`

3. Update the paths in the configuration to match your installation directory

## Available Tools

The server provides 10 comprehensive tools:
- **Time & Date**: get_current_time
- **Weather**: get_weather (requires API key)
- **File Operations**: create_file, read_file, list_directory, create_temporary_file
- **Search & Analysis**: search_files, calculate_expression
- **System Operations**: execute_command, get_system_info

## Testing

```bash
source .venv/bin/activate
python demo.py          # Test the server tools
python test_server.py   # Run comprehensive tests
```

## Dependencies

The installer will automatically install all required dependencies:
- fastmcp
- requests
- python-dotenv
- pydantic
- psutil

## Support

Visit: https://github.com/rt0120-Ramco/mcp-py

## Troubleshooting

### Permission Issues
Make sure scripts are executable:
```bash
chmod +x install.sh start_server.sh build.sh
```

### Python Version Issues
Ensure you have Python 3.8 or higher:
```bash
python3 --version
```

### Virtual Environment Issues
If the virtual environment fails to create, install venv:
```bash
# Ubuntu/Debian
sudo apt install python3-venv

# CentOS/RHEL
sudo yum install python3-devel
```
EOF

echo
echo "Step 3: Creating tarball archive..."
cd "$DIST_DIR"
tar -czf "${ARCHIVE_NAME}.tar.gz" "$PACKAGE_NAME"
cd ..

echo
echo "=========================================="
echo "Packaging completed successfully!"
echo "=========================================="
echo
echo "Created package: $DIST_DIR/${ARCHIVE_NAME}.tar.gz"
echo "Package size:"
ls -lh "$DIST_DIR/${ARCHIVE_NAME}.tar.gz"
echo
echo "Package contents:"
echo "- Standalone installation"
echo "- Python wheel package"
echo "- Complete documentation"
echo "- Linux/macOS shell scripts"
echo "- Claude Desktop configuration template"
echo
echo "The package is ready for distribution!"
echo
echo "To extract and install:"
echo "  tar -xzf $DIST_DIR/${ARCHIVE_NAME}.tar.gz"
echo "  cd $PACKAGE_NAME"
echo "  ./install.sh"
echo