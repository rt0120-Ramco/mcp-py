#!/bin/bash
# Build script for FastMCP Multi-Tool Server (Linux/macOS)
# This script builds the Python package for distribution

set -e  # Exit on any error

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

echo "========================================"
echo "FastMCP Multi-Tool Server Build Script"
echo "========================================"
echo "Working directory: $(pwd)"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
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

# Check if we're in a virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo "Using virtual environment: $VIRTUAL_ENV"
else
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
    if [[ $? -ne 0 ]]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    
    echo "Activating virtual environment..."
    source .venv/bin/activate
    if [[ $? -ne 0 ]]; then
        echo "ERROR: Failed to activate virtual environment"
        exit 1
    fi
    
    # Update pip and setuptools in the new virtual environment
    python -m pip install --upgrade pip
fi

echo
echo "Installing/upgrading build tools..."
$PIP_CMD install --upgrade pip setuptools wheel build twine
if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to install build tools"
    exit 1
fi

echo
echo "Installing project dependencies..."
$PIP_CMD install -r requirements.txt
if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo
echo "Cleaning previous build artifacts..."
rm -rf build dist *.egg-info

echo
echo "Building source distribution..."
$PYTHON_CMD -m build --sdist
if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to build source distribution"
    exit 1
fi

echo
echo "Building wheel distribution..."
$PYTHON_CMD -m build --wheel
if [[ $? -ne 0 ]]; then
    echo "ERROR: Failed to build wheel distribution"
    exit 1
fi

echo
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo
echo "Build artifacts created in 'dist' folder:"
ls -la dist/
echo
echo "To install the package locally, run:"
echo "  pip install dist/fastmcp_multi_tool_server-*.whl"
echo
echo "To upload to PyPI (requires authentication), run:"
echo "  twine upload dist/*"
echo