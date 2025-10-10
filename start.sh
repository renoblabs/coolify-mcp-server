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

echo "🌐 Starting in REMOTE mode (HTTP/SSE)"
echo "Server will be available at: http://localhost:8765"
echo ""
doppler run -- python run_server.py
