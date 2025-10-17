#!/bin/bash
# Cross-platform build script launcher for Unix systems
# This script calls the appropriate build method

echo "=========================================="
echo "FastMCP Multi-Tool Server Build Launcher"
echo "=========================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Using Python build script for cross-platform compatibility..."
echo

# Use python3 if available, otherwise python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# Run the Python build script
$PYTHON_CMD scripts/build.py

if [[ $? -ne 0 ]]; then
    echo
    echo "ERROR: Build failed. Trying Unix-specific build script..."
    echo
    chmod +x scripts/unix/build.sh
    scripts/unix/build.sh
fi

echo
echo "Build process completed."