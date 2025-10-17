# FastMCP Multi-Tool Server Project

## Project Structure

```
c:\github\test-py\
├── server.py                    # Main FastMCP server with 10 tools
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables (template)
├── README.md                   # Detailed documentation
├── demo.py                     # Demonstration script
├── test_server.py              # Test suite
├── claude_desktop_config.json  # Claude Desktop configuration template
├── setup.bat                   # Windows setup script
├── start_server.bat            # Windows server startup script
└── .venv\                      # Python virtual environment
```

## Quick Start

### For Windows Users:
1. Run `setup.bat` to automatically set up the environment
2. Run `start_server.bat` to start the server

### For Manual Setup:
1. Create virtual environment: `python -m venv .venv`
2. Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `python server.py`

## Available Tools

The server includes 10 comprehensive tools:

1. **🕒 get_current_time** - Get current date and time
2. **🌤️ get_weather** - Weather information for any city (requires API key)
3. **📝 create_file** - Create new files with content
4. **📖 read_file** - Read existing file contents
5. **📁 list_directory** - List directory contents with details
6. **💻 execute_command** - Execute shell commands safely
7. **🔍 search_files** - Search for text patterns in files
8. **🧮 calculate_expression** - Mathematical expression calculator
9. **⚙️ get_system_info** - System information (CPU, memory, disk)
10. **📄 create_temporary_file** - Create temporary files

## Integration with Claude Desktop

Copy the configuration from `claude_desktop_config.json` to your Claude Desktop settings:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Update the paths to match your installation directory.

## Security Features

- Command execution filtering (blocks dangerous operations)
- Safe mathematical expression evaluation
- 30-second timeout for commands
- Path validation for file operations

## Optional Configuration

Set `OPENWEATHER_API_KEY` in `.env` file for weather functionality.
Get your free API key at: https://openweathermap.org/api

## Testing

Run `python demo.py` to see available tools and verify setup.
Run `python test_server.py` for comprehensive testing.

## Ready to Use!

Your FastMCP server is ready. Start it with `python server.py` and integrate with Claude Desktop for powerful AI-assisted development!