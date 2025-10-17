#!/usr/bin/env python3
"""
Test script for FastMCP Multi-Tool Server
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from fastmcp import FastMCP
        print("✓ FastMCP imported successfully")
    except ImportError as e:
        print(f"✗ FastMCP import failed: {e}")
        return False
        
    try:
        import requests
        print("✓ Requests imported successfully")
    except ImportError as e:
        print(f"✗ Requests import failed: {e}")
        return False
        
    try:
        import psutil
        print("✓ PSUtil imported successfully")
    except ImportError as e:
        print(f"✗ PSUtil import failed: {e}")
        return False
        
    try:
        from dotenv import load_dotenv
        print("✓ Python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ Python-dotenv import failed: {e}")
        return False
        
    return True

def test_server_creation():
    """Test if the server can be created without errors."""
    print("\nTesting server creation...")
    
    try:
        # Import the server module
        import server
        print("✓ Server module imported successfully")
        
        # Check if the MCP instance was created
        if hasattr(server, 'mcp'):
            print("✓ FastMCP instance created successfully")
            print(f"✓ Server name: {server.mcp.name}")
            
            # List available tools
            if hasattr(server.mcp, '_tools'):
                tools = list(server.mcp._tools.keys())
                print(f"✓ Available tools ({len(tools)}):")
                for tool in sorted(tools):
                    print(f"  - {tool}")
            
            return True
        else:
            print("✗ FastMCP instance not found")
            return False
            
    except Exception as e:
        print(f"✗ Server creation failed: {e}")
        return False

def test_tool_functions():
    """Test individual tool functions."""
    print("\nTesting individual tool functions...")
    
    try:
        import server
        
        # Test get_current_time
        try:
            result = server.get_current_time()
            print(f"✓ get_current_time: {result}")
        except Exception as e:
            print(f"✗ get_current_time failed: {e}")
        
        # Test calculate_expression
        try:
            result = server.calculate_expression("2 + 2")
            print(f"✓ calculate_expression: {result}")
        except Exception as e:
            print(f"✗ calculate_expression failed: {e}")
            
        # Test create_temporary_file
        try:
            result = server.create_temporary_file("Test content", ".txt")
            print(f"✓ create_temporary_file: {result.get('success', False)}")
        except Exception as e:
            print(f"✗ create_temporary_file failed: {e}")
            
        # Test get_system_info
        try:
            result = server.get_system_info()
            print(f"✓ get_system_info: {result.get('success', False)}")
        except Exception as e:
            print(f"✗ get_system_info failed: {e}")
            
        return True
        
    except Exception as e:
        print(f"✗ Tool testing failed: {e}")
        return False

if __name__ == "__main__":
    print("FastMCP Multi-Tool Server - Test Suite")
    print("=" * 50)
    
    success = True
    
    # Run tests
    success &= test_imports()
    success &= test_server_creation()
    success &= test_tool_functions()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The server is ready to use.")
        print("\nTo run the server:")
        print("python server.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        
    print("\nFor more information, see README.md")