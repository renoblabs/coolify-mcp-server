#!/bin/bash
# Setup script for Claude Code MCP client on main rig

set -e

echo "=================================================="
echo "Coolify MCP Client Setup (Main Rig)"
echo "=================================================="
echo ""

# Configuration
DEV_BOX_IP="192.168.2.30"
MCP_PORT="8765"
AUTH_TOKEN="E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Configuration:"
echo "  Dev Box: $DEV_BOX_IP:$MCP_PORT"
echo "  Auth Token: ${AUTH_TOKEN:0:20}..."
echo ""

# Test connection to dev box
echo "Testing connection to dev box..."
if curl -s --connect-timeout 5 "http://$DEV_BOX_IP:$MCP_PORT/health" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ Dev box is reachable${NC}"
else
    echo -e "  ${RED}✗ Cannot reach dev box${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Verify dev box IP: $DEV_BOX_IP"
    echo "  2. Check if MCP server is running on dev box"
    echo "  3. Check firewall: sudo ufw allow 8765/tcp"
    echo "  4. Ping dev box: ping $DEV_BOX_IP"
    echo ""
    exit 1
fi

# Check if Claude Code is installed
echo ""
echo "Checking for Claude Code installation..."
if command -v claude &> /dev/null; then
    echo -e "  ${GREEN}✓ Claude Code is installed${NC}"
    CLAUDE_VERSION=$(claude --version 2>&1 || echo "unknown")
    echo "  Version: $CLAUDE_VERSION"
else
    echo -e "  ${YELLOW}⚠ Claude Code not found${NC}"
    echo ""
    echo "Install Claude Code from:"
    echo "  https://docs.anthropic.com/claude/docs/claude-code"
    echo ""
fi

# Create MCP configuration
echo ""
echo "Creating MCP configuration..."

MCP_CONFIG_DIR="$HOME/.config/claude"
MCP_CONFIG_FILE="$MCP_CONFIG_DIR/mcp.json"

# Create directory if it doesn't exist
mkdir -p "$MCP_CONFIG_DIR"

# Check if config already exists
if [ -f "$MCP_CONFIG_FILE" ]; then
    echo -e "  ${YELLOW}⚠ MCP config already exists${NC}"
    echo "  Location: $MCP_CONFIG_FILE"
    echo ""
    read -p "Do you want to back it up and create a new one? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        BACKUP_FILE="$MCP_CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$MCP_CONFIG_FILE" "$BACKUP_FILE"
        echo "  Backed up to: $BACKUP_FILE"
    else
        echo ""
        echo "Please manually add this to your $MCP_CONFIG_FILE:"
        cat examples/client-config-main-rig.json
        echo ""
        exit 0
    fi
fi

# Create new config
cat > "$MCP_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "coolify-server": {
      "type": "sse",
      "url": "http://$DEV_BOX_IP:$MCP_PORT/sse",
      "headers": {
        "Authorization": "Bearer $AUTH_TOKEN"
      }
    }
  }
}
EOF

echo -e "  ${GREEN}✓ MCP configuration created${NC}"
echo "  Location: $MCP_CONFIG_FILE"

# Test MCP connection
echo ""
echo "Testing MCP server connection..."
if curl -s -H "Authorization: Bearer $AUTH_TOKEN" \
        -H "Accept: text/event-stream" \
        --connect-timeout 5 \
        --max-time 3 \
        "http://$DEV_BOX_IP:$MCP_PORT/sse" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ MCP server is accessible${NC}"
else
    echo -e "  ${YELLOW}⚠ MCP server connection test inconclusive${NC}"
    echo "  (This is normal for SSE endpoints)"
fi

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "You can now use Coolify MCP tools in Claude Code!"
echo ""
echo "Try these commands in Claude Code:"
echo "  • List my Coolify applications"
echo "  • Get Coolify server info"
echo "  • Show application details for <uuid>"
echo ""
echo "Troubleshooting:"
echo "  • Check MCP config: cat $MCP_CONFIG_FILE"
echo "  • Test dev box: curl http://$DEV_BOX_IP:$MCP_PORT/health"
echo "  • View Claude Code logs: claude logs"
echo ""
