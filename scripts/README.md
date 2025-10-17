# Build and Packaging Scripts

This directory contains all the build and packaging scripts for the FastMCP Multi-Tool Server project, organized by platform and purpose.

## Directory Structure

```
scripts/
├── README.md              # This file
├── build.py               # Cross-platform build script (Python)
├── build.bat              # Cross-platform build script (Windows)
├── build.sh               # Cross-platform build script (Unix)
├── windows/               # Windows-specific scripts
│   ├── build.bat          # Windows build script
│   ├── package.bat        # Windows packaging script
│   ├── setup.bat          # Windows setup script
│   └── start_server.bat   # Windows server startup script
├── unix/                  # Unix-like systems (Linux/macOS)
│   ├── build.sh           # Unix build script
│   ├── install.sh         # Unix installation script
│   └── package.sh         # Unix packaging script
└── packaging/             # Cross-platform packaging tools
    └── package_universal.py  # Universal packaging script
```

## Usage

### Quick Build (Any Platform)

**Python (Recommended - Cross-platform):**
```bash
python scripts/build.py
```

**Windows:**
```batch
scripts\build.bat
```

**Linux/macOS:**
```bash
chmod +x scripts/build.sh && scripts/build.sh
```

### Platform-Specific Building

**Windows Only:**
```batch
scripts\windows\build.bat
```

**Unix Only:**
```bash
chmod +x scripts/unix/build.sh && scripts/unix/build.sh
```

### Packaging

**Universal Packaging (Creates packages for all platforms):**
```bash
python scripts/packaging/package_universal.py
```

**Windows Packaging:**
```batch
scripts\windows\package.bat
```

**Unix Packaging:**
```bash
chmod +x scripts/unix/package.sh && scripts/unix/package.sh
```

## Script Descriptions

### Cross-Platform Scripts

- **`build.py`** - Python-based build script that works on all platforms
- **`build.bat`** - Cross-platform build script for Windows users
- **`build.sh`** - Cross-platform build script for Unix users

### Windows Scripts (`windows/`)

- **`build.bat`** - Windows-specific build script
- **`package.bat`** - Creates Windows distribution package
- **`setup.bat`** - Initial setup script for development
- **`start_server.bat`** - Starts the MCP server on Windows

### Unix Scripts (`unix/`)

- **`build.sh`** - Unix-specific build script
- **`install.sh`** - Installation script for end users
- **`package.sh`** - Creates Unix distribution package

### Packaging Scripts (`packaging/`)

- **`package_universal.py`** - Cross-platform packaging script that creates distributions for all supported platforms

## Best Practices

1. **Use the cross-platform scripts first** - They handle platform detection automatically
2. **Platform-specific scripts** are for when you need platform-specific behavior
3. **Always make shell scripts executable** on Unix systems: `chmod +x script.sh`
4. **Test on target platforms** before distributing packages

## Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment support (`venv` module)

For packaging:
- `setuptools`
- `wheel`
- `build`
- `twine` (for PyPI uploads)

## Distribution

The packaging scripts create distribution-ready archives:
- **Windows**: ZIP files with batch scripts
- **Unix**: TAR.GZ files with shell scripts
- **Cross-platform**: Python wheel packages for pip installation

## Troubleshooting

### Permission Issues (Unix)
```bash
chmod +x scripts/unix/*.sh
chmod +x scripts/*.sh
```

### Python Path Issues
Make sure Python is in your PATH or use the full path:
```bash
/usr/bin/python3 scripts/build.py
```

### Virtual Environment Issues
Some systems require explicit venv installation:
```bash
# Ubuntu/Debian
sudo apt install python3-venv

# CentOS/RHEL
sudo yum install python3-devel
```