#!/usr/bin/env python3
"""
FastMCP Server Demonstration
Shows how to start the server and list available tools
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main demonstration function."""
    print("🚀 FastMCP Multi-Tool Server")
    print("=" * 50)
    
    try:
        # Import the server module
        import server
        
        print(f"✓ Server initialized: {server.mcp.name}")
        
        # Get the list of available tools
        if hasattr(server.mcp, '_tools'):
            tools = list(server.mcp._tools.keys())
            print(f"\n📋 Available Tools ({len(tools)}):")
            print("-" * 30)
            
            tool_descriptions = {
                'get_current_time': '🕒 Get current date and time',
                'get_weather': '🌤️ Get weather for any city',
                'create_file': '📝 Create new files',
                'read_file': '📖 Read file contents',
                'list_directory': '📁 List directory contents',
                'execute_command': '💻 Execute shell commands safely',
                'search_files': '🔍 Search for text in files',
                'calculate_expression': '🧮 Calculate mathematical expressions',
                'get_system_info': '⚙️ Get system information',
                'create_temporary_file': '📄 Create temporary files'
            }
            
            for i, tool in enumerate(sorted(tools), 1):
                description = tool_descriptions.get(tool, '🔧 Utility tool')
                print(f"{i:2d}. {description}")
                print(f"    Function: {tool}")
        
        print("\n" + "=" * 50)
        print("🎯 How to Use:")
        print("1. Start the server: python server.py")
        print("2. Configure Claude Desktop with the server")
        print("3. Use the tools through Claude's interface")
        
        print("\n📖 Documentation:")
        print("See README.md for detailed setup and usage instructions")
        
        print("\n🔧 Configuration:")
        print("- Environment file: .env")
        print("- Add OpenWeatherMap API key for weather functionality")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading server: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Server is ready to run!")
        print("\nTo start the server now, run:")
        print("python server.py")
    else:
        print("\n❌ Server has issues. Check the error messages above.")
        
    sys.exit(0 if success else 1)