#!/usr/bin/env python3
"""
FastMCP Server with Multiple Tools
A comprehensive MCP server with various utility tools
"""

import json
import os
import sys
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from dotenv import load_dotenv

# Import FastMCP
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Multi-Tool MCP Server")

@mcp.tool()
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def get_weather(city: str) -> Dict[str, Any]:
    """
    Get weather information for a city using OpenWeatherMap API.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        Dictionary containing weather information
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY environment variable."}
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "visibility": data.get("visibility", "N/A")
        }
    except requests.RequestException as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}
    except KeyError as e:
        return {"error": f"Unexpected API response format: {str(e)}"}

@mcp.tool()
def create_file(filepath: str, content: str) -> Dict[str, Any]:
    """
    Create a new file with the specified content.
    
    Args:
        filepath: Path where the file should be created
        content: Content to write to the file
        
    Returns:
        Dictionary with operation status and details
    """
    try:
        # Create directory if it doesn't exist
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content to file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return {
            "success": True,
            "message": f"File created successfully at {filepath}",
            "size": len(content),
            "absolute_path": str(path.absolute())
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create file: {str(e)}"
        }

@mcp.tool()
def read_file(filepath: str) -> Dict[str, Any]:
    """
    Read the content of a file.
    
    Args:
        filepath: Path to the file to read
        
    Returns:
        Dictionary with file content or error message
    """
    try:
        path = Path(filepath)
        if not path.exists():
            return {
                "success": False,
                "error": f"File does not exist: {filepath}"
            }
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return {
            "success": True,
            "content": content,
            "size": len(content),
            "absolute_path": str(path.absolute()),
            "last_modified": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to read file: {str(e)}"
        }

@mcp.tool()
def list_directory(directory_path: str) -> Dict[str, Any]:
    """
    List contents of a directory.
    
    Args:
        directory_path: Path to the directory to list
        
    Returns:
        Dictionary with directory contents or error message
    """
    try:
        path = Path(directory_path)
        if not path.exists():
            return {
                "success": False,
                "error": f"Directory does not exist: {directory_path}"
            }
            
        if not path.is_dir():
            return {
                "success": False,
                "error": f"Path is not a directory: {directory_path}"
            }
            
        items = []
        for item in path.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None,
                "last_modified": datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            })
            
        return {
            "success": True,
            "directory": str(path.absolute()),
            "items": sorted(items, key=lambda x: (x["type"], x["name"])),
            "total_items": len(items)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list directory: {str(e)}"
        }

@mcp.tool()
def execute_command(command: str, working_directory: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute a shell command and return the result.
    
    Args:
        command: The command to execute
        working_directory: Optional working directory for the command
        
    Returns:
        Dictionary with command output and execution details
    """
    try:
        # Security check - prevent dangerous commands
        dangerous_commands = ['rm -rf', 'del /f', 'format', 'shutdown', 'reboot']
        if any(dangerous in command.lower() for dangerous in dangerous_commands):
            return {
                "success": False,
                "error": "Command contains potentially dangerous operations and was blocked"
            }
            
        # Set working directory
        cwd = Path(working_directory) if working_directory else Path.cwd()
        
        # Execute command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30  # 30-second timeout
        )
        
        return {
            "success": True,
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "working_directory": str(cwd.absolute())
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to execute command: {str(e)}"
        }

@mcp.tool()
def search_files(directory: str, pattern: str, file_extension: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for files containing a specific pattern.
    
    Args:
        directory: Directory to search in
        pattern: Text pattern to search for
        file_extension: Optional file extension filter (e.g., '.py', '.txt')
        
    Returns:
        Dictionary with search results
    """
    try:
        path = Path(directory)
        if not path.exists():
            return {
                "success": False,
                "error": f"Directory does not exist: {directory}"
            }
            
        matches = []
        
        # Get all files matching extension filter
        if file_extension:
            files = path.rglob(f"*{file_extension}")
        else:
            files = path.rglob("*")
            files = [f for f in files if f.is_file()]
            
        for file_path in files:
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if pattern.lower() in content.lower():
                            # Find line numbers containing the pattern
                            lines = content.split('\n')
                            matching_lines = []
                            for i, line in enumerate(lines, 1):
                                if pattern.lower() in line.lower():
                                    matching_lines.append({
                                        "line_number": i,
                                        "content": line.strip()
                                    })
                                    
                            matches.append({
                                "file": str(file_path.relative_to(path)),
                                "absolute_path": str(file_path.absolute()),
                                "matching_lines": matching_lines[:10]  # Limit to first 10 matches per file
                            })
                except:
                    # Skip files that can't be read (binary files, etc.)
                    continue
                    
        return {
            "success": True,
            "pattern": pattern,
            "directory": str(path.absolute()),
            "file_extension": file_extension,
            "matches": matches,
            "total_files_with_matches": len(matches)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to search files: {str(e)}"
        }

@mcp.tool()
def calculate_expression(expression: str) -> Dict[str, Any]:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
        
    Returns:
        Dictionary with calculation result
    """
    try:
        # Security check - only allow safe mathematical operations
        allowed_chars = set('0123456789+-*/().= ')
        allowed_names = {'abs', 'round', 'min', 'max', 'pow', 'sqrt'}
        
        # Remove spaces and check characters
        clean_expr = expression.replace(' ', '')
        if not all(c in allowed_chars or c.isalnum() for c in clean_expr):
            # Check if it contains only allowed function names
            import re
            tokens = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expression)
            if any(token not in allowed_names for token in tokens):
                return {
                    "success": False,
                    "error": "Expression contains disallowed characters or functions"
                }
        
        # Import math for advanced functions
        import math
        
        # Create a safe namespace for evaluation
        safe_dict = {
            "__builtins__": {},
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "pi": math.pi,
            "e": math.e
        }
        
        result = eval(expression, safe_dict)
        
        return {
            "success": True,
            "expression": expression,
            "result": result,
            "type": type(result).__name__
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to evaluate expression: {str(e)}"
        }

@mcp.tool()
def get_system_info() -> Dict[str, Any]:
    """
    Get system information.
    
    Returns:
        Dictionary with system details
    """
    try:
        import platform
        import psutil
        
        return {
            "success": True,
            "system": platform.system(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": {
                "total": psutil.disk_usage('/').total if platform.system() != 'Windows' else psutil.disk_usage('C:').total,
                "used": psutil.disk_usage('/').used if platform.system() != 'Windows' else psutil.disk_usage('C:').used,
                "free": psutil.disk_usage('/').free if platform.system() != 'Windows' else psutil.disk_usage('C:').free
            }
        }
    except ImportError:
        return {
            "success": False,
            "error": "psutil package required for system info. Install with: pip install psutil"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get system info: {str(e)}"
        }

@mcp.tool()
def create_temporary_file(content: str, suffix: str = ".txt") -> Dict[str, Any]:
    """
    Create a temporary file with the specified content.
    
    Args:
        content: Content to write to the temporary file
        suffix: File extension/suffix for the temporary file
        
    Returns:
        Dictionary with temporary file details
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name
            
        return {
            "success": True,
            "temporary_file_path": tmp_path,
            "content_size": len(content),
            "suffix": suffix,
            "message": "Temporary file created successfully. Remember to delete it when no longer needed."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create temporary file: {str(e)}"
        }

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()