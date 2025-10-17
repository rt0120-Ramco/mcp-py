#!/usr/bin/env python3
"""Setup script for FastMCP Multi-Tool Server."""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="fastmcp-multi-tool-server",
    version="1.0.0",
    author="JSK",
    author_email="rt0120@ramco.com",
    description="A comprehensive Model Context Protocol (MCP) server built with FastMCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rt0120-Ramco/mcp-py",
    project_urls={
        "Bug Tracker": "https://github.com/rt0120-Ramco/mcp-py/issues",
        "Documentation": "https://github.com/rt0120-Ramco/mcp-py#readme",
        "Source Code": "https://github.com/rt0120-Ramco/mcp-py",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    packages=find_packages(),
    py_modules=["server"],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "weather": [
            "requests>=2.25.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "fastmcp-server=server:main",
            "mcp-multi-tool=server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.md",
            "*.txt",
            "*.json",
            "*.bat",
            "*.env.example",
        ],
    },
    zip_safe=False,
    keywords=[
        "mcp",
        "model-context-protocol",
        "fastmcp",
        "ai",
        "claude",
        "tools",
        "server",
        "utilities",
        "weather",
        "file-operations",
        "system-info",
    ],
    platforms=["any"],
)