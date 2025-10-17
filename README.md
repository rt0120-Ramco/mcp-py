# FastMCP Multi-Tool Server

A comprehensive Model Context Protocol (MCP) server built with FastMCP that provides various utility tools.

## Features

This MCP server includes the following tools:

### 🕒 Time & Date
- **get_current_time**: Get the current date and time

### 🌤️ Weather
- **get_weather**: Get weather information for any city (requires OpenWeatherMap API key)

### 📁 File Operations
- **create_file**: Create new files with specified content
- **read_file**: Read content from existing files
- **list_directory**: List contents of directories
- **create_temporary_file**: Create temporary files

### 🔍 Search & Analysis
- **search_files**: Search for text patterns in files within a directory
- **calculate_expression**: Safely evaluate mathematical expressions

### 💻 System Operations
- **execute_command**: Execute shell commands safely (with security restrictions)
- **get_system_info**: Get detailed system information (CPU, memory, disk usage)

## Installation

### Quick Setup

**Windows:**
```batch
scripts\build.bat
```

**Linux/macOS:**
```bash
chmod +x scripts/build.sh && scripts/build.sh
```

**Cross-platform (Python):**
```bash
python scripts/build.py
```

### Manual Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Configure environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenWeatherMap API key if needed
```

## Usage

### Running the Server

To run the MCP server:

```bash
python server.py
```

The server will start and listen for MCP connections.

### Configuration with Claude Desktop

To use this server with Claude Desktop, add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "multi-tool-server": {
      "command": "python",
      "args": ["C:/github/mcp-py/server.py"],
      "cwd": "C:/github/mcp-py"
    }
  }
}
```

**Note**: Update the paths to match your actual installation directory.

### Configuration File Location

The Claude Desktop configuration file is typically located at:

- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## Tool Examples

### File Operations
```python
# Create a new file
create_file("./example.txt", "Hello, World!")

# Read a file
read_file("./example.txt")

# List directory contents
list_directory("./")
```

### Weather Information
```python
# Get weather for a city (requires API key)
get_weather("London")
```

### Mathematical Calculations
```python
# Calculate mathematical expressions
calculate_expression("2 + 2 * 3")
calculate_expression("sqrt(16) + pow(2, 3)")
```

### File Search
```python
# Search for text in Python files
search_files("./", "import", ".py")
```

### System Information
```python
# Get system details
get_system_info()
```

### Command Execution
```python
# Execute safe commands
execute_command("echo Hello World")
execute_command("ls -la", "/tmp")  # Unix
execute_command("dir", "C:\\")     # Windows
```

## Security Features

- **Command Filtering**: Dangerous commands are blocked automatically
- **Safe Expression Evaluation**: Mathematical expressions are evaluated in a secure environment
- **Timeout Protection**: Commands have a 30-second timeout limit
- **Path Validation**: File operations validate paths to prevent unauthorized access

## Environment Variables

- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key for weather functionality
- `MCP_SERVER_NAME`: Custom server name (optional)
- `MCP_SERVER_VERSION`: Server version (optional)

## Dependencies

- `fastmcp`: FastMCP framework for MCP server development
- `requests`: HTTP library for API calls
- `python-dotenv`: Environment variable management
- `pydantic`: Data validation and settings management
- `psutil`: System and process utilities

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **Weather Tool Not Working**: Ensure you have a valid OpenWeatherMap API key set in the `.env` file.

3. **Permission Errors**: Make sure the server has appropriate file system permissions for the operations you're trying to perform.

4. **Command Execution Fails**: Some commands may be blocked for security reasons. Check the error message for details.

## Development

To extend this server with additional tools:

1. Add new tool functions using the `@mcp.tool()` decorator
2. Follow the existing pattern for error handling and return formats
3. Update this README with documentation for new tools

## License

This project is open source. Feel free to modify and distribute according to your needs.