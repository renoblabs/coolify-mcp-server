#!/usr/bin/env python3
"""
Coolify MCP Server - STDIO MODE for Local IDE Integration

This wrapper runs the Coolify MCP server in STDIO mode for use with
desktop IDEs like Claude Desktop, Cursor, and other MCP clients that
spawn local subprocess servers.

Usage:
    python server_stdio.py

The server will:
- Run in STDIO mode (communicates via stdin/stdout)
- Load credentials from .env file or environment variables
- Connect to your Coolify instance remotely
- Provide all Coolify automation tools to your IDE
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the FastMCP app from server.py
from server import app

if __name__ == "__main__":
    # Log to stderr (stdout is used for MCP protocol)
    print("Starting Coolify MCP Server in STDIO mode...", file=sys.stderr)
    print("This server will communicate via stdin/stdout with your IDE", file=sys.stderr)

    # Run in STDIO mode
    app.run(transport="stdio")
