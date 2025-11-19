#!/bin/bash

# Startup script for Coolify MCP Server
# Uses Doppler for secrets management (optional)

set -e

echo "🚀 Starting Coolify MCP Server..."
echo ""

# Check if doppler is installed and configured
USE_DOPPLER=false
if command -v doppler &> /dev/null; then
    if doppler secrets get COOLIFY_API_TOKEN &> /dev/null 2>&1; then
        USE_DOPPLER=true
        echo "✓ Using Doppler for secrets management"
    else
        echo "⚠️  Doppler installed but not configured for this directory"
        echo "   Run: doppler setup"
        echo "   Falling back to .env file (if present)"
    fi
else
    echo "ℹ️  Doppler not found - using .env file for configuration"
    echo "   To use Doppler: curl -Ls https://cli.doppler.com/install.sh | sh"
fi

echo ""

# Parse all command line arguments
ARGS=()
MODE="http"

for arg in "$@"; do
    case $arg in
        --mode=*)
            MODE="${arg#*=}"
            ARGS+=("--mode" "$MODE")
            ;;
        --mode)
            shift
            MODE="$1"
            ARGS+=("--mode" "$MODE")
            ;;
        stdio)
            MODE="stdio"
            ARGS+=("--mode" "stdio")
            ;;
        *)
            ARGS+=("$arg")
            ;;
    esac
done

# Display mode
if [ "$MODE" = "stdio" ]; then
    echo "📡 Starting in STDIO mode (for Claude Desktop/Factory Bridge)"
else
    echo "🌐 Starting in HTTP/SSE mode (for remote access)"
    echo "   Server will be available at: http://localhost:8765"
fi

echo ""

# Run the server
if [ "$USE_DOPPLER" = true ]; then
    doppler run -- python server.py "${ARGS[@]}"
else
    python server.py "${ARGS[@]}"
fi
