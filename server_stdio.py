#!/usr/bin/env python3
"""
Coolify MCP Server - STDIO MODE for Local IDE Integration
This version runs in STDIO mode for Cursor, Claude Desktop, etc.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main server
from server import app

if __name__ == "__main__":
    # Override transport to STDIO
    print("Starting Coolify MCP Server in STDIO mode...", file=sys.stderr)
    app.run(transport="stdio")


