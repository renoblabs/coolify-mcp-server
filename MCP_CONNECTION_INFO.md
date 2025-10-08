# MCP Server Connection Information

**Server Started:** October 2, 2025  
**Status:** 🟢 RUNNING

---

## 🔌 Connection Details

### Local Access
- **URL:** `http://localhost:8765`
- **Host:** `0.0.0.0` (all interfaces)
- **Port:** `8765`
- **Transport:** HTTP/SSE (Server-Sent Events)

### Remote Access (via Cloudflare Tunnel)
- **URL:** `https://mcp.therink.io` (configure in Cloudflare)
- **Public Domain:** Point this to `localhost:8765` in your tunnel config

---

## 🔐 Authentication

### Bearer Token
```
Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY
```

**Use in apps:**
- Header: `Authorization: Bearer Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY`

---

## 📱 App Configuration Examples

### For MCP-Compatible Mobile Apps (Genspark, Manus, etc.)

#### Local Testing
```json
{
  "name": "Coolify Assistant",
  "endpoint": "http://localhost:8765",
  "transport": "sse",
  "authentication": {
    "type": "bearer",
    "token": "Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY"
  }
}
```

#### Remote Access (after tunnel setup)
```json
{
  "name": "Coolify Assistant",
  "endpoint": "https://mcp.therink.io",
  "transport": "sse",
  "authentication": {
    "type": "bearer",
    "token": "Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY"
  }
}
```

### For Desktop Apps (Claude Desktop, etc.)

Add to your MCP config file (usually `~/Library/Application Support/Claude/claude_desktop_config.json` on Mac or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "coolify": {
      "url": "http://localhost:8765",
      "transport": "sse",
      "headers": {
        "Authorization": "Bearer Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY"
      }
    }
  }
}
```

### For curl/HTTP Testing

```bash
# List available tools
curl -H "Authorization: Bearer Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY" \
     http://localhost:8765/tools

# Execute a tool
curl -X POST \
     -H "Authorization: Bearer Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY" \
     -H "Content-Type: application/json" \
     -d '{"tool": "list_applications"}' \
     http://localhost:8765/execute
```

---

## 🚀 Available Tools (18 Total)

### Coolify Management
- `list_applications` - List all apps in Coolify
- `get_application_details` - Get details for specific app
- `deploy_application` - Deploy/redeploy an app
- `get_application_environment` - Get environment variables
- `update_application_environment` - Update env vars
- `get_application_logs` - View application logs
- `restart_application` - Restart an app
- `stop_application` - Stop an app

### Multi-Server Management 🆕
- `list_servers` - List all deployment destinations
- `get_server_details` - Get server info and status
- `get_server_resources` - Check CPU/RAM/disk usage
- `deploy_to_server` - Deploy to specific server
- `smart_deploy` - Auto-select best server (GPU-aware!)
- `get_server_info` - MCP server information

### Cloudflare Automation
- `create_dns_record` - Create DNS records
- `automate_service_deployment` - Full deployment automation

### Diagnostics
- `diagnose_tunnel_issues` - Debug tunnel vs localhost issues
- `get_server_info` - Get MCP server status

---

## 🌐 Cloudflare Tunnel Setup (For Remote Access)

Add to your tunnel configuration:

```yaml
ingress:
  - hostname: mcp.therink.io
    service: http://localhost:8765
  - service: http_status:404
```

Or via Cloudflare dashboard:
1. Go to Zero Trust → Access → Tunnels
2. Edit your tunnel
3. Add public hostname:
   - **Subdomain:** `mcp`
   - **Domain:** `therink.io`
   - **Service:** `http://localhost:8765`

---

## 🛠️ Server Management

### Check if Server is Running
```powershell
netstat -an | Select-String "8765"
```

### Stop Server
Close the PowerShell window that opened, or:
```powershell
Get-Process python | Where-Object {$_.WorkingSet -gt 30MB} | Stop-Process
```

### Restart Server
```bash
cd C:\Users\19057\Factory\ProjectsnSessions\coolify-mcp-server
doppler run -- .\coolify_mcp_env\Scripts\python.exe server.py
```

---

## 📊 Server Status

- **Process ID:** Check PowerShell window
- **Memory Usage:** ~50MB
- **Startup Time:** 3-5 seconds
- **API Response Time:** < 1 second

---

## 🔒 Security Notes

- ✅ Bearer token authentication enabled
- ✅ Secrets managed via Doppler (not in code)
- ✅ HTTPS recommended for remote access (via tunnel)
- 🔄 Rotate token regularly: `doppler secrets set MCP_AUTH_TOKEN="$(openssl rand -base64 32)"`

---

## 🎯 Quick Start for Apps

1. **Copy the auth token** above
2. **Use local endpoint** for testing: `http://localhost:8765`
3. **Set transport** to `sse` or `http`
4. **Add Bearer token** to authentication
5. **Test connection** - try calling `get_server_info` tool

---

## 📞 Support

- **Logs:** Check the PowerShell window for real-time logs
- **Errors:** Server errors will appear in the console
- **Tests:** Run `doppler run -- python tests/test_apps.py`

---

**Server is ready! Start configuring your apps!** 🚀
