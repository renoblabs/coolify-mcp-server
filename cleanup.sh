#!/bin/bash
# Coolify MCP Server - Cleanup & Audit Script
# Run this on your dev box BEFORE deploying to clean up previous attempts

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================================="
echo "Coolify MCP Server - Cleanup & Audit Script"
echo "=========================================================="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${YELLOW}⚠  Running as root. Some checks may not work correctly.${NC}"
    echo ""
fi

echo -e "${BLUE}[1/8] Checking for running Python servers on port 8765...${NC}"
if lsof -i :8765 > /dev/null 2>&1; then
    echo -e "${YELLOW}Found processes using port 8765:${NC}"
    lsof -i :8765 | grep -v COMMAND
    echo ""
    read -p "Kill these processes? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo lsof -ti :8765 | xargs -r sudo kill -9
        echo -e "${GREEN}✓ Processes killed${NC}"
    fi
else
    echo -e "${GREEN}✓ Port 8765 is free${NC}"
fi
echo ""

echo -e "${BLUE}[2/8] Checking for running MCP server processes...${NC}"
if pgrep -f "python.*server.py" > /dev/null; then
    echo -e "${YELLOW}Found MCP server processes:${NC}"
    ps aux | grep "python.*server.py" | grep -v grep
    echo ""
    read -p "Kill these processes? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -9 -f "python.*server.py"
        echo -e "${GREEN}✓ Processes killed${NC}"
    fi
else
    echo -e "${GREEN}✓ No MCP server processes running${NC}"
fi
echo ""

echo -e "${BLUE}[3/8] Checking for systemd service...${NC}"
if systemctl list-unit-files | grep -q "coolify-mcp-server.service"; then
    echo -e "${YELLOW}Found systemd service:${NC}"
    systemctl status coolify-mcp-server.service --no-pager || true
    echo ""
    read -p "Stop and disable service? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo systemctl stop coolify-mcp-server.service 2>/dev/null || true
        sudo systemctl disable coolify-mcp-server.service 2>/dev/null || true
        echo -e "${GREEN}✓ Service stopped and disabled${NC}"
        echo ""
        read -p "Remove service file? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            sudo rm /etc/systemd/system/coolify-mcp-server.service
            sudo systemctl daemon-reload
            echo -e "${GREEN}✓ Service file removed${NC}"
        fi
    fi
else
    echo -e "${GREEN}✓ No systemd service found${NC}"
fi
echo ""

echo -e "${BLUE}[4/8] Checking for previous installations...${NC}"
POSSIBLE_DIRS=(
    "$HOME/coolify-mcp-server"
    "$HOME/coolify-mcp"
    "$HOME/mcp-server"
    "/opt/coolify-mcp-server"
    "/srv/coolify-mcp-server"
)

FOUND_DIRS=()
for dir in "${POSSIBLE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        FOUND_DIRS+=("$dir")
    fi
done

if [ ${#FOUND_DIRS[@]} -gt 0 ]; then
    echo -e "${YELLOW}Found previous installations:${NC}"
    for dir in "${FOUND_DIRS[@]}"; do
        echo "  - $dir"
        if [ -f "$dir/.env" ]; then
            echo "    └─ Contains .env file"
        fi
        if [ -d "$dir/venv" ]; then
            echo "    └─ Contains virtual environment"
        fi
    done
    echo ""
    echo "Review these directories. You may want to:"
    echo "  1. Backup any .env files with important configuration"
    echo "  2. Remove old installations"
    echo ""
    read -p "Show detailed info for these directories? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for dir in "${FOUND_DIRS[@]}"; do
            echo ""
            echo "Directory: $dir"
            ls -lah "$dir" 2>/dev/null | head -20
        done
    fi
else
    echo -e "${GREEN}✓ No previous installations found${NC}"
fi
echo ""

echo -e "${BLUE}[5/8] Checking Python environments...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"

    # Check for fastmcp installation
    if python3 -c "import fastmcp" 2>/dev/null; then
        FASTMCP_VERSION=$(python3 -c "import fastmcp; print(fastmcp.__version__)" 2>/dev/null || echo "unknown")
        echo "  └─ fastmcp installed (version: $FASTMCP_VERSION)"
    else
        echo "  └─ fastmcp not installed globally"
    fi
else
    echo -e "${RED}✗ Python 3 not found!${NC}"
    echo "  Install with: sudo apt install python3 python3-pip python3-venv"
fi
echo ""

echo -e "${BLUE}[6/8] Checking firewall configuration...${NC}"
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status | grep "8765" || echo "")
    if [ -n "$UFW_STATUS" ]; then
        echo -e "${YELLOW}Port 8765 firewall rules:${NC}"
        echo "$UFW_STATUS"
    else
        echo -e "${GREEN}✓ No firewall rules for port 8765${NC}"
        echo "  (You'll need to add this later: sudo ufw allow 8765/tcp)"
    fi
else
    echo -e "${YELLOW}⚠  UFW not installed${NC}"
fi
echo ""

echo -e "${BLUE}[7/8] Checking network connectivity...${NC}"
# Check if this is the dev box or if we need to test remotely
HOSTNAME=$(hostname)
IP_ADDR=$(hostname -I | awk '{print $1}')
echo "  Hostname: $HOSTNAME"
echo "  IP Address: $IP_ADDR"

if [ "$IP_ADDR" = "192.168.2.30" ] || [ "$HOSTNAME" = "devbox" ]; then
    echo -e "${GREEN}✓ This appears to be the dev box${NC}"
else
    echo -e "${YELLOW}⚠  This might not be the dev box (expected 192.168.2.30)${NC}"
fi
echo ""

echo -e "${BLUE}[8/8] Checking for MCP configuration files...${NC}"
MCP_CONFIGS=(
    "$HOME/.config/claude/mcp.json"
    "$HOME/.mcp.json"
    "$(pwd)/.mcp.json"
)

FOUND_CONFIGS=()
for config in "${MCP_CONFIGS[@]}"; do
    if [ -f "$config" ]; then
        FOUND_CONFIGS+=("$config")
    fi
done

if [ ${#FOUND_CONFIGS[@]} -gt 0 ]; then
    echo -e "${YELLOW}Found MCP configuration files:${NC}"
    for config in "${FOUND_CONFIGS[@]}"; do
        echo "  - $config"
    done
    echo ""
    read -p "Show contents? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for config in "${FOUND_CONFIGS[@]}"; do
            echo ""
            echo "=== $config ==="
            cat "$config"
            echo ""
        done
    fi
else
    echo -e "${GREEN}✓ No MCP configuration files found${NC}"
fi
echo ""

echo "=========================================================="
echo "Cleanup Summary"
echo "=========================================================="
echo ""
echo "Review the findings above. Common cleanup actions:"
echo ""
echo "1. Kill running servers:"
echo "   pkill -9 -f 'python.*server.py'"
echo "   sudo lsof -ti :8765 | xargs -r sudo kill -9"
echo ""
echo "2. Remove systemd service:"
echo "   sudo systemctl stop coolify-mcp-server"
echo "   sudo systemctl disable coolify-mcp-server"
echo "   sudo rm /etc/systemd/system/coolify-mcp-server.service"
echo "   sudo systemctl daemon-reload"
echo ""
echo "3. Remove old installations:"
echo "   # Backup .env first if needed!"
echo "   rm -rf ~/coolify-mcp-server"
echo ""
echo "4. Clean firewall rules (if needed):"
echo "   sudo ufw delete allow 8765/tcp"
echo ""
echo "5. Fresh install:"
echo "   git clone https://github.com/renoblabs/coolify-mcp-server.git"
echo "   cd coolify-mcp-server"
echo "   ./deploy.sh"
echo ""
echo "=========================================================="
echo ""

read -p "Do you want to perform automatic cleanup now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${YELLOW}Performing automatic cleanup...${NC}"

    # Stop and remove systemd service
    if systemctl list-unit-files | grep -q "coolify-mcp-server.service"; then
        echo "  → Stopping systemd service..."
        sudo systemctl stop coolify-mcp-server.service 2>/dev/null || true
        sudo systemctl disable coolify-mcp-server.service 2>/dev/null || true
        sudo rm /etc/systemd/system/coolify-mcp-server.service 2>/dev/null || true
        sudo systemctl daemon-reload
        echo -e "    ${GREEN}✓ Systemd service removed${NC}"
    fi

    # Kill running processes
    if pgrep -f "python.*server.py" > /dev/null || lsof -i :8765 > /dev/null 2>&1; then
        echo "  → Killing running processes..."
        pkill -9 -f "python.*server.py" 2>/dev/null || true
        sudo lsof -ti :8765 | xargs -r sudo kill -9 2>/dev/null || true
        sleep 1
        echo -e "    ${GREEN}✓ Processes killed${NC}"
    fi

    echo ""
    echo -e "${GREEN}Cleanup complete!${NC}"
    echo ""
    echo "System is now clean and ready for fresh deployment."
    echo "Run ./deploy.sh to install."
else
    echo ""
    echo "No automatic cleanup performed."
    echo "Review the findings above and clean up manually as needed."
fi

echo ""
echo "=========================================================="
echo "Done!"
echo "=========================================================="
