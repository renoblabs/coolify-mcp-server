#!/bin/bash

# Simple startup script for Coolify MCP Server
# Uses Doppler for secrets management

set -e

echo "🚀 Starting Coolify MCP Server..."
echo ""

# Check if doppler is installed
if ! command -v doppler &> /dev/null; then
    echo "❌ Error: Doppler CLI not found"
    echo "Install it: curl -Ls https://cli.doppler.com/install.sh | sh"
    exit 1
fi

# Check if doppler is configured
if ! doppler secrets get COOLIFY_API_TOKEN &> /dev/null; then
    echo "⚠️  Warning: Doppler not configured for this directory"
    echo "Run: doppler setup"
    echo ""
fi

# Default to remote mode, pass --mode=stdio for local STDIO mode
MODE="${1:-remote}"

if [ "$MODE" = "--mode=stdio" ] || [ "$MODE" = "stdio" ]; then
    echo "📡 Starting in STDIO mode (for Factory Bridge/Claude Desktop)"
    doppler run -- python server.py --mode stdio
else
    echo "🌐 Starting in REMOTE mode (for mobile apps)"
    echo "Server will be available at: http://localhost:8765"
    echo ""
    doppler run -- python server.py
fi
