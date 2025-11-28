#!/bin/bash
# Quick Audit Script - Run this first on your dev box
# This is a quick check before running the full cleanup.sh

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Coolify MCP Server - Quick Audit                         ║"
echo "╔════════════════════════════════════════════════════════════╝"
echo ""

echo "📍 Current Location:"
echo "   Hostname: $(hostname)"
echo "   User: $(whoami)"
echo "   IP: $(hostname -I | awk '{print $1}')"
echo ""

echo "🔍 [1/6] Checking port 8765..."
if lsof -i :8765 > /dev/null 2>&1; then
    echo "   ⚠️  Port 8765 is IN USE:"
    lsof -i :8765 | grep -v COMMAND | while read line; do
        echo "      $line"
    done
else
    echo "   ✅ Port 8765 is FREE"
fi
echo ""

echo "🔍 [2/6] Checking for Python MCP processes..."
if pgrep -f "python.*server" > /dev/null; then
    echo "   ⚠️  Found Python server processes:"
    ps aux | grep "python.*server" | grep -v grep | while read line; do
        echo "      $(echo $line | awk '{print $2, $11, $12, $13}')"
    done
else
    echo "   ✅ No Python server processes found"
fi
echo ""

echo "🔍 [3/6] Checking for systemd services..."
if systemctl list-unit-files 2>/dev/null | grep -q "coolify-mcp"; then
    echo "   ⚠️  Found systemd service(s):"
    systemctl list-unit-files | grep coolify | while read line; do
        echo "      $line"
    done
    echo ""
    echo "   Status:"
    systemctl status coolify-mcp-server --no-pager 2>/dev/null | head -5 | while read line; do
        echo "      $line"
    done
else
    echo "   ✅ No systemd services found"
fi
echo ""

echo "🔍 [4/6] Checking for MCP server directories..."
FOUND=0
for dir in ~/coolify-mcp-server ~/coolify-mcp ~/mcp-server /opt/coolify-mcp-server; do
    if [ -d "$dir" ]; then
        echo "   📁 Found: $dir"
        if [ -f "$dir/.env" ]; then
            echo "      └─ Contains .env file (has configuration)"
        fi
        if [ -d "$dir/venv" ]; then
            echo "      └─ Contains venv/"
        fi
        if [ -f "$dir/server.py" ]; then
            echo "      └─ Contains server.py"
        fi
        FOUND=1
    fi
done
if [ $FOUND -eq 0 ]; then
    echo "   ✅ No previous installations found"
fi
echo ""

echo "🔍 [5/6] Checking Python environment..."
if command -v python3 &> /dev/null; then
    echo "   ✅ Python: $(python3 --version)"
    if python3 -c "import fastmcp" 2>/dev/null; then
        echo "   ✅ fastmcp is installed"
    else
        echo "   ⚠️  fastmcp not installed (will be installed during deploy)"
    fi
else
    echo "   ❌ Python 3 not found!"
fi
echo ""

echo "🔍 [6/6] Checking firewall..."
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status 2>/dev/null | grep "8765" || echo "")
    if [ -n "$UFW_STATUS" ]; then
        echo "   ⚠️  Port 8765 has firewall rules:"
        echo "$UFW_STATUS" | while read line; do
            echo "      $line"
        done
    else
        echo "   ℹ️  No firewall rules for port 8765 (will need to add)"
    fi
else
    echo "   ℹ️  UFW not installed"
fi
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Summary                                                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Review the findings above"
echo "  2. If you see important configs, back them up:"
echo "     cp ~/coolify-mcp-server/.env ~/coolify-mcp-server/.env.backup"
echo ""
echo "  3. Run full cleanup (when ready):"
echo "     ./cleanup.sh"
echo ""
echo "  4. Or proceed with manual review/cleanup"
echo ""
