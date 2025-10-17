#!/usr/bin/env python3
"""
Cross-platform build script for FastMCP Multi-Tool Server
This script works on Windows, Linux, and macOS
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, shell=False):
    """Run a command and handle errors"""
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, shell=shell)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed: {e.cmd}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def get_python_command():
    """Get the appropriate Python command for this system"""
    for cmd in ['python3', 'python']:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return cmd
        except FileNotFoundError:
            continue
    
    print("ERROR: Python not found in PATH")
    sys.exit(1)

def check_virtual_env():
    """Check if we're in a virtual environment or create one"""
    if os.environ.get('VIRTUAL_ENV'):
        print(f"Using existing virtual environment: {os.environ['VIRTUAL_ENV']}")
        return True
    
    if os.path.exists('.venv'):
        print("Found existing virtual environment in .venv")
        activate_venv()
        return True
    
    return False

def activate_venv():
    """Activate the virtual environment"""
    system = platform.system().lower()
    
    if system == 'windows':
        activate_script = os.path.join('.venv', 'Scripts', 'activate.bat')
        if os.path.exists(activate_script):
            # Note: We can't actually activate in the same process on Windows
            # The calling script should handle activation
            print("Virtual environment found. Please run from activated environment.")
    else:
        activate_script = os.path.join('.venv', 'bin', 'activate')
        if os.path.exists(activate_script):
            # Note: We can't actually activate in the same process
            # The calling script should handle activation
            print("Virtual environment found. Please run: source .venv/bin/activate")

def create_virtual_env():
    """Create a new virtual environment"""
    python_cmd = get_python_command()
    
    print("Creating virtual environment...")
    run_command([python_cmd, '-m', 'venv', '.venv'])
    
    print("Virtual environment created successfully!")
    print("To use it:")
    
    system = platform.system().lower()
    if system == 'windows':
        print("  .venv\\Scripts\\activate")
    else:
        print("  source .venv/bin/activate")

def install_build_tools():
    """Install required build tools"""
    python_cmd = get_python_command()
    
    print("Installing/upgrading build tools...")
    run_command([python_cmd, '-m', 'pip', 'install', '--upgrade', 'pip'])
    run_command([python_cmd, '-m', 'pip', 'install', '--upgrade', 'setuptools', 'wheel', 'build'])

def install_dependencies():
    """Install project dependencies"""
    python_cmd = get_python_command()
    
    if os.path.exists('requirements.txt'):
        print("Installing project dependencies...")
        run_command([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    else:
        print("No requirements.txt found, skipping dependency installation")

def clean_build_artifacts():
    """Clean previous build artifacts"""
    print("Cleaning previous build artifacts...")
    
    import shutil
    
    directories_to_clean = ['build', 'dist', '*.egg-info', '__pycache__']
    
    for pattern in directories_to_clean:
        if '*' in pattern:
            # Handle glob patterns
            import glob
            for path in glob.glob(pattern):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        else:
            if os.path.exists(pattern):
                if os.path.isdir(pattern):
                    shutil.rmtree(pattern)
                else:
                    os.remove(pattern)

def build_package():
    """Build the package"""
    python_cmd = get_python_command()
    
    print("Building source distribution...")
    run_command([python_cmd, '-m', 'build', '--sdist'])
    
    print("Building wheel distribution...")
    run_command([python_cmd, '-m', 'build', '--wheel'])

def main():
    """Main build function"""
    print("=" * 50)
    print("FastMCP Multi-Tool Server Build Script")
    print("=" * 50)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    
    # Change to project root directory if we're in scripts directory
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if 'scripts' in script_dir:
        project_root = os.path.join(script_dir, '..')
        os.chdir(project_root)
        print(f"Changed to project root: {os.getcwd()}")
    
    print()
    
    # Check Python
    python_cmd = get_python_command()
    version_output = subprocess.run([python_cmd, '--version'], capture_output=True, text=True)
    print(f"Python: {version_output.stdout.strip()}")
    
    # Check if we need to create or use virtual environment
    if not check_virtual_env():
        response = input("No virtual environment found. Create one? [Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            create_virtual_env()
            print("\nPlease activate the virtual environment and run this script again:")
            system = platform.system().lower()
            if system == 'windows':
                print("  .venv\\Scripts\\activate")
                print("  python scripts/build.py")
            else:
                print("  source .venv/bin/activate")
                print("  python scripts/build.py")
            return
    
    try:
        # Install build tools
        install_build_tools()
        
        # Install dependencies
        install_dependencies()
        
        # Clean previous builds
        clean_build_artifacts()
        
        # Build the package
        build_package()
        
        print()
        print("=" * 50)
        print("Build completed successfully!")
        print("=" * 50)
        print()
        print("Build artifacts created in 'dist' folder:")
        
        if os.path.exists('dist'):
            for file in os.listdir('dist'):
                file_path = os.path.join('dist', file)
                size = os.path.getsize(file_path)
                print(f"  {file} ({size:,} bytes)")
        
        print()
        print("To install locally:")
        print(f"  {python_cmd} -m pip install dist/*.whl")
        print()
        print("To create distribution package:")
        print(f"  {python_cmd} scripts/packaging/package_universal.py")
        
    except Exception as e:
        print(f"ERROR: Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()