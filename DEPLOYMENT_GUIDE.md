# Coolify MCP Server - Dev Box Deployment Guide

## Overview

This guide helps you deploy the Coolify MCP server on your dev box so you can connect to it from your main rig using Claude Code.

## Architecture

```
Main Rig (Claude Code)  ──→  Dev Box (192.168.2.30:8765)  ──→  Coolify API
                         MCP/SSE                           HTTP
```

## Prerequisites

- **Dev Box**: Linux server with Python 3.11+
- **Coolify**: Running and accessible from dev box
- **Network**: Main rig can reach dev box on port 8765

---

## Part 1: Deploy Server on Dev Box

### 1.1 SSH into Your Dev Box

```bash
ssh user@192.168.2.30
```

### 1.2 Clone the Repository

```bash
cd ~
git clone https://github.com/renoblabs/coolify-mcp-server.git
cd coolify-mcp-server
```

### 1.3 Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or use a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 1.4 Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit the configuration
nano .env
```

Update these values in `.env`:

```bash
# Coolify Configuration
COOLIFY_API_TOKEN=your_actual_coolify_api_token_here
COOLIFY_BASE_URL=http://localhost:8000  # Or your Coolify URL
USE_TUNNEL=false

# MCP Server Configuration
MCP_AUTH_TOKEN=E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo=
MCP_PORT=8765
MCP_HOST=0.0.0.0  # Important: Listen on all interfaces
ALLOWED_ORIGINS=*

# Optional: Cloudflare (for DNS automation)
# CLOUDFLARE_API_TOKEN=your_cf_token_here
# CLOUDFLARE_ZONE_ID=your_zone_id_here
```

**Important Notes:**
- Get your Coolify API token from: Coolify → Security → API Tokens
- Keep the `MCP_AUTH_TOKEN` as-is, or generate a new one with: `openssl rand -base64 32`
- `MCP_HOST=0.0.0.0` is crucial - it allows connections from your main rig

### 1.5 Test the Server

```bash
# Start the server manually first to test
python server.py
```

You should see:
```
============================================================
Coolify MCP Server - REMOTE MODE (SSE)
============================================================
Host: 0.0.0.0
Port: 8765
Auth: Enabled
Local: http://localhost:8765
SSE Endpoint: http://localhost:8765/sse
Auth Token: E2L98+RsBfM7vSBNoDvP...
============================================================
```

### 1.6 Test from Main Rig

From your main rig, test the connection:

```bash
# Test health endpoint (no auth required)
curl http://192.168.2.30:8765/health

# Should return: ok
```

If you get a connection error, check:
- Firewall on dev box: `sudo ufw allow 8765/tcp`
- Dev box IP is correct
- Server is running

### 1.7 Set Up Systemd Service (Auto-start)

Create a systemd service so the server starts automatically:

```bash
sudo nano /etc/systemd/system/coolify-mcp-server.service
```

Paste this configuration (adjust paths as needed):

```ini
[Unit]
Description=Coolify MCP Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/coolify-mcp-server
Environment="PATH=/home/your-username/coolify-mcp-server/venv/bin:/usr/local/bin:/usr/bin"
ExecStart=/home/your-username/coolify-mcp-server/venv/bin/python server.py
Restart=always
RestartSec=10

# Load environment variables from .env
EnvironmentFile=/home/your-username/coolify-mcp-server/.env

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable coolify-mcp-server

# Start the service
sudo systemctl start coolify-mcp-server

# Check status
sudo systemctl status coolify-mcp-server

# View logs
sudo journalctl -u coolify-mcp-server -f
```

---

## Part 2: Configure Client on Main Rig

### 2.1 Install Claude Code (if not already installed)

Follow the official installation guide at: https://docs.anthropic.com/claude/docs/claude-code

### 2.2 Configure MCP Server Connection

On your main rig, create or update the MCP configuration:

**Option A: Using Claude Code CLI**

```bash
# Add the MCP server
claude mcp add --transport sse coolify-server http://192.168.2.30:8765/sse \
  --header "Authorization: Bearer E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo="
```

**Option B: Manual Configuration**

Create/edit `~/.config/claude/mcp.json` (or your project's `.mcp.json`):

```json
{
  "mcpServers": {
    "coolify-server": {
      "type": "sse",
      "url": "http://192.168.2.30:8765/sse",
      "headers": {
        "Authorization": "Bearer E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo="
      }
    }
  }
}
```

### 2.3 Test the Connection

In Claude Code, try these commands:

```
List my Coolify applications
```

```
Get Coolify server info
```

If you see your applications, you're all set! 🎉

---

## Part 3: Security Hardening (Optional but Recommended)

### 3.1 Firewall Configuration

Only allow your main rig to access port 8765:

```bash
# On dev box
sudo ufw allow from 192.168.2.0/24 to any port 8765 proto tcp
sudo ufw enable
```

### 3.2 Use HTTPS with Reverse Proxy

For production use, consider putting the MCP server behind nginx with SSL:

```nginx
server {
    listen 443 ssl;
    server_name mcp.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8765;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 3.3 Rotate Auth Token Regularly

Generate a new token and update both:
- `.env` on dev box
- MCP config on main rig

```bash
openssl rand -base64 32
```

---

## Troubleshooting

### Server won't start

```bash
# Check logs
sudo journalctl -u coolify-mcp-server -n 50

# Check if port is in use
sudo lsof -i :8765

# Test manually
cd ~/coolify-mcp-server
source venv/bin/activate
python server.py
```

### Can't connect from main rig

```bash
# Test network connectivity
ping 192.168.2.30

# Test port accessibility
telnet 192.168.2.30 8765

# Check firewall
sudo ufw status
```

### MCP tools not working

```bash
# Verify Coolify API token
curl -H "Authorization: Bearer YOUR_COOLIFY_TOKEN" \
     http://localhost:8000/api/v1/applications

# Check server logs for errors
sudo journalctl -u coolify-mcp-server -f
```

### Authentication errors

- Verify the `MCP_AUTH_TOKEN` matches in:
  - Dev box `.env` file
  - Main rig MCP config
- Make sure the token doesn't have extra spaces or quotes

---

## Available Tools

Once connected, you'll have access to:

- **Application Management**: List, deploy, restart, stop applications
- **Multi-Server**: Deploy to specific servers, smart deployment
- **Environment**: Get/update environment variables
- **Logs**: View application logs
- **Cloudflare**: DNS automation, tunnel management
- **Diagnostics**: Troubleshoot tunnel and deployment issues

---

## Quick Reference

**Dev Box:**
- Server URL: `http://0.0.0.0:8765/sse`
- Service: `sudo systemctl status coolify-mcp-server`
- Logs: `sudo journalctl -u coolify-mcp-server -f`
- Config: `~/coolify-mcp-server/.env`

**Main Rig:**
- MCP Config: `~/.config/claude/mcp.json` or `.mcp.json`
- Connection: `http://192.168.2.30:8765/sse`
- Test: `curl http://192.168.2.30:8765/health`

**Security:**
- Auth Token: `E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo=`
- Change in both `.env` and MCP config if rotated

---

Need help? Open an issue at: https://github.com/renoblabs/coolify-mcp-server/issues
