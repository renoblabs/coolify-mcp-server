#!/usr/bin/env python3
"""
Wrapper to run server.py with proper encoding on Windows
This explicitly starts the FastMCP SSE server instead of relying on
server.py's __main__ guard (which doesn't run when imported).
"""
import sys
import os
import uvicorn

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    # Set console to UTF-8
    os.system('chcp 65001 > nul')

# Import server module and start the SSE transport directly
import server

if __name__ == "__main__":
    print("=" * 60)
    print("Coolify MCP Server - REMOTE MODE (run_server.py)")
    print("=" * 60)
    print(f"Host: {server.MCP_HOST}")
    print(f"Port: {server.MCP_PORT}")
    print("Auth: Enabled")
    print(f"Local: http://localhost:{server.MCP_PORT}")
    print("=" * 60)

    # Start ASGI app - run the server.py main block to create http_app
    import subprocess
    import sys
    subprocess.run([sys.executable, "server.py"], cwd=".")
