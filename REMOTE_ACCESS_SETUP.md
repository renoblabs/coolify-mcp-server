# Remote MCP Server Setup Guide 🌐

This guide will help you set up your Coolify MCP server for remote access from mobile AI apps or any external client.

## 🎯 Overview

Your MCP server now has **two modes**:
1. **Local STDIO Mode** (`coolify_mcp_server.py`) - For Factory Bridge, Claude Desktop, JetBrains
2. **Remote HTTP Mode** (`coolify_mcp_server_remote.py`) - For mobile AI apps, remote access

## 🚀 Quick Start - Remote Server

### Step 1: Start the Remote Server

```bash
cd coolify-mcp-server
.\coolify_mcp_env\Scripts\activate
doppler run -- python coolify_mcp_server_remote.py
```

You'll see:
```
╭────────────────────────────────────────────────────────╮
│           Coolify MCP Server - REMOTE MODE             │
├────────────────────────────────────────────────────────┤
│  🌐 Starting HTTP/WebSocket server...                  │
│  📍 Host: 0.0.0.0                                      │
│  🔌 Port: 8765                                         │
│  🔐 Auth: Enabled                                      │
│                                                        │
│  Local:  http://localhost:8765                         │
│  Remote: Configure via Cloudflare tunnel              │
╰────────────────────────────────────────────────────────╯
```

### Step 2: Test Local Access

```bash
# In another terminal, test the server:
curl -H "Authorization: Bearer YOUR_MCP_AUTH_TOKEN" http://localhost:8765/health
```

## 🔒 Authentication

Your server is protected with token authentication:
- **Token**: `Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY`
- **Header**: `Authorization: Bearer <token>`

⚠️ **Keep this token secure!** Anyone with this token can access your Coolify infrastructure.

## 🌍 Expose via Cloudflare Tunnel

To make your MCP server accessible from anywhere, add it to your Cloudflare tunnel:

### Option 1: Add to Existing Tunnel Config

Edit your `config.yml` for cloudflared:

```yaml
tunnel: d5d71027-31d6-443a-b2d9-fdd016e720cc
credentials-file: /path/to/credentials.json

ingress:
  # Add this new entry for MCP server
  - hostname: mcp.therink.io
    service: http://localhost:8765
  
  # Your existing services...
  - hostname: cloud.therink.io
    service: http://localhost:8000
  
  - service: http_status:404
```

### Option 2: Use Cloudflare Dashboard

1. Go to [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Navigate to: Access → Tunnels → Your Tunnel (RenobCloud)
3. Click "Configure" → "Public Hostname"
4. Add new public hostname:
   - **Subdomain**: `mcp`
   - **Domain**: `therink.io`
   - **Service**: `http://localhost:8765`

### Option 3: Create DNS Record

Since you already have the tunnel running:

```bash
# Create DNS record pointing to your tunnel
doppler run -- python -c "
import cloudflare
import os

cf = cloudflare.Cloudflare(api_token=os.getenv('CLOUDFLARE_API_TOKEN'))
zone_id = os.getenv('CLOUDFLARE_ZONE_ID')

result = cf.dns.records.create(
    zone_id=zone_id,
    type='CNAME',
    name='mcp.therink.io',
    content='cloud.therink.io',  # Points to your existing tunnel
    ttl=1
)
print(f'Created: mcp.therink.io -> cloud.therink.io')
"
```

## 📱 Mobile AI App Configuration

Once your tunnel is configured, use these settings in your mobile AI app:

### MCP Server Settings
```json
{
  "name": "Coolify Assistant",
  "endpoint": "https://mcp.therink.io",
  "transport": "http",
  "auth": {
    "type": "bearer",
    "token": "Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY"
  }
}
```

### Alternative WebSocket Connection
```json
{
  "name": "Coolify Assistant",
  "endpoint": "wss://mcp.therink.io/ws",
  "transport": "websocket",
  "auth": {
    "type": "bearer",
    "token": "Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY"
  }
}
```

## 🧪 Testing Remote Access

### Test from anywhere:
```bash
# Test server info
curl -H "Authorization: Bearer Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY" \
     https://mcp.therink.io/tools

# Test a tool
curl -X POST \
     -H "Authorization: Bearer Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY" \
     -H "Content-Type: application/json" \
     -d '{"tool": "list_applications"}' \
     https://mcp.therink.io/execute
```

## 🔧 Configuration Options

### Environment Variables (via Doppler)
```bash
# Auth & Port
MCP_AUTH_TOKEN=Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY
MCP_PORT=8765
MCP_HOST=0.0.0.0  # Listen on all interfaces

# Existing Coolify settings work as-is
USE_TUNNEL=true
COOLIFY_API_TOKEN=...
CLOUDFLARE_API_TOKEN=...
# etc.
```

### Change Port or Auth Token
```bash
# Generate new token
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update in Doppler
doppler secrets set MCP_AUTH_TOKEN="new-token-here"
doppler secrets set MCP_PORT="9000"  # Different port if needed
```

## 🚦 Running Both Servers

You can run both local and remote servers simultaneously:

### Terminal 1 - Local STDIO (for Factory/Claude)
```bash
doppler run -- python coolify_mcp_server.py
```

### Terminal 2 - Remote HTTP (for mobile)
```bash
doppler run -- python coolify_mcp_server_remote.py
```

They use different transports so won't conflict!

## 🔐 Security Considerations

1. **Token Security**: Never commit the auth token to git
2. **HTTPS Only**: Always use Cloudflare tunnel for remote access (provides HTTPS)
3. **Firewall**: Don't expose port 8765 directly to internet (use tunnel instead)
4. **Rotate Tokens**: Change auth token periodically
5. **Monitor Access**: Check Cloudflare Analytics for unusual access patterns

## 📊 Available Tools (Same as Local)

All 12 tools are available remotely:
- `get_server_info()` - Server information
- `list_applications()` - List Coolify apps
- `get_application_details()` - App details
- `deploy_application()` - Deploy apps
- `get_application_environment()` - Get env vars
- `update_application_environment()` - Update env vars
- `get_application_logs()` - View logs
- `restart_application()` - Restart apps
- `stop_application()` - Stop apps
- `create_dns_record()` - Create DNS
- `automate_service_deployment()` - Full automation
- `diagnose_tunnel_issues()` - Diagnostics

## ⚠️ Troubleshooting

### Server won't start
- Check if port 8765 is already in use: `netstat -an | findstr 8765`
- Try a different port: `doppler secrets set MCP_PORT="9000"`

### Can't connect from mobile
- Verify tunnel is running: `cloudflared tunnel info`
- Check DNS: `nslookup mcp.therink.io`
- Test locally first: `curl http://localhost:8765/health`

### Authentication errors
- Verify token matches in Doppler and mobile app
- Check header format: `Authorization: Bearer <token>`
- Token should not have quotes in the header

### Tools not working
- Ensure USE_TUNNEL=true in Doppler
- Check Coolify API token is valid
- Verify Cloudflare credentials

## 🎯 Next Steps

1. ✅ Start remote server locally
2. ✅ Configure Cloudflare tunnel
3. ✅ Create DNS record (mcp.therink.io)
4. ✅ Test with curl
5. ✅ Configure mobile AI app
6. ✅ Enjoy remote Coolify management!

---

**Your MCP server is now ready for remote access!** 🚀

Access it from anywhere at: `https://mcp.therink.io` (once tunnel is configured)