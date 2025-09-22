#!/bin/bash
set -e

echo "🚀 Setting up Coolify MCP Server..."

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Install it with: sudo apt update && sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv coolify_mcp_env
source coolify_mcp_env/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get your Coolify API token:"
echo "   - Go to http://localhost:8000/security/api-tokens"
echo "   - Create a new API token"
echo "   - Copy the token"
echo ""
echo "2. Choose your secrets management:"
echo ""
echo "   Option A - Doppler (Recommended):"
echo "   - Install Doppler CLI: curl -Ls https://cli.doppler.com/install.sh | sh"
echo "   - Setup project: doppler setup"
echo "   - Add secrets: doppler secrets set COOLIFY_API_TOKEN=\"your_token\""
echo "   - Run with: ./start_with_doppler.sh"
echo ""
echo "   Option B - Local .env file:"
echo "   - Create .env file with your API token"
echo "   - Run with: source coolify_mcp_env/bin/activate && python coolify_mcp_server.py"