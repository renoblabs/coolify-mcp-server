#!/bin/bash
# Quick start script for running with Doppler

echo "🚀 Starting Coolify MCP Server with Doppler..."

# Activate virtual environment
source coolify_mcp_env/bin/activate

# Check if Doppler is installed
if ! command -v doppler &> /dev/null; then
    echo "❌ Doppler CLI not found. Installing..."
    curl -Ls https://cli.doppler.com/install.sh | sh
fi

# Run with Doppler
echo "🔐 Loading secrets from Doppler and starting server..."
doppler run -- python coolify_mcp_server.py