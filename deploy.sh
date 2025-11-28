#!/bin/bash
# Coolify MCP Server - Deployment Script for Dev Box

set -e

echo "=================================================="
echo "Coolify MCP Server - Deployment Script"
echo "=================================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get current user and directory
CURRENT_USER=$(whoami)
INSTALL_DIR=$(pwd)

echo "Installation Details:"
echo "  User: $CURRENT_USER"
echo "  Directory: $INSTALL_DIR"
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found: Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
else
    echo ""
    echo "  ✓ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo ""
echo "Installing dependencies..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "  ✓ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo -e "${RED}IMPORTANT: Edit .env and add your Coolify API token!${NC}"
    echo "  nano .env"
    echo ""
else
    echo ""
    echo "  ✓ .env file exists"
fi

# Create systemd service file
echo ""
echo "Creating systemd service file..."
SERVICE_FILE="coolify-mcp-server.service"
TEMP_SERVICE="/tmp/coolify-mcp-server.service"

sed "s|YOUR_USERNAME|$CURRENT_USER|g" "$SERVICE_FILE" > "$TEMP_SERVICE"
sed -i "s|/home/YOUR_USERNAME/coolify-mcp-server|$INSTALL_DIR|g" "$TEMP_SERVICE"

echo ""
echo "Service file created. To install:"
echo ""
echo -e "${GREEN}sudo cp $TEMP_SERVICE /etc/systemd/system/coolify-mcp-server.service${NC}"
echo -e "${GREEN}sudo systemctl daemon-reload${NC}"
echo -e "${GREEN}sudo systemctl enable coolify-mcp-server${NC}"
echo -e "${GREEN}sudo systemctl start coolify-mcp-server${NC}"
echo ""

# Test the server
echo ""
read -p "Do you want to test the server now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting server in test mode (Ctrl+C to stop)..."
    echo "=================================================="
    python server.py
fi

echo ""
echo "=================================================="
echo "Deployment Complete!"
echo "=================================================="
echo ""
echo "Next Steps:"
echo "  1. Edit .env with your Coolify API token"
echo "  2. Install systemd service (commands above)"
echo "  3. Configure client on your main rig"
echo ""
echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
echo ""
