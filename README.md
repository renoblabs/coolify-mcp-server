# Coolify MCP Server 🚀

**Production-Ready Remote MCP Server for Coolify Automation**

Control your entire Coolify infrastructure remotely through AI assistants, mobile apps, or direct API calls. Fully consolidated and ready for deployment on your Linux dev box at `mcp.therink.io`.

## 🎯 What It Does

- **📱 Remote Access**: Control Coolify from mobile AI apps (Claude, ChatGPT, Genspark, etc.)
- **🤖 AI-Powered**: Full MCP integration with 18+ automation tools
- **🌐 DNS Automation**: Auto-create Cloudflare DNS records and tunnel routes
- **🔒 Production Security**: Doppler-managed secrets, Bearer token auth, HTTPS
- **⚡ Multi-Server**: Smart deployment across multiple Coolify servers
- **🛠️ Windows & Linux**: Cross-platform with optimized runners

## ⚡ Quick Start

### Production Deployment (Linux)
```bash
# 1. Clone repo
git clone https://github.com/renoblabs/coolify-mcp-server.git
cd coolify-mcp-server

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure Doppler secrets
doppler setup
doppler secrets set COOLIFY_API_TOKEN="your-coolify-token"
doppler secrets set COOLIFY_TUNNEL_URL="https://cloud.therink.io"
doppler secrets set MCP_AUTH_TOKEN="$(openssl rand -base64 32)"
doppler secrets set USE_TUNNEL="true"
doppler secrets set CLOUDFLARE_API_TOKEN="your-cf-token"  # Optional
doppler secrets set CLOUDFLARE_ZONE_ID="your-zone-id"      # Optional

# 4. Start server (Linux/Production)
./start.sh
```

### Windows Development
```powershell
# Use the Windows-optimized runner
python run_server.py
```

**Production**: Server runs at `http://localhost:8765` and is exposed at `https://mcp.therink.io`

## 🔧 Available Tools

### Coolify Management
- `list_applications()` - List all apps
- `get_application_details(app_uuid)` - App info
- `deploy_application(app_uuid)` - Deploy/redeploy
- `get_application_environment(app_uuid)` - Get env vars
- `update_application_environment(app_uuid, vars)` - Update env vars
- `get_application_logs(app_uuid, lines)` - View logs
- `restart_application(app_uuid)` - Restart app
- `stop_application(app_uuid)` - Stop app

### 🎯 Multi-Server Management (NEW!)
- `list_servers()` - List all deployment destinations
- `get_server_details(server_uuid)` - Server info with resources
- `get_server_resources(server_uuid)` - CPU/RAM/disk availability
- `deploy_to_server(app_uuid, server_name)` - Deploy to specific server by name
- `smart_deploy(service, app_uuid, requires_gpu, requires_high_memory)` - Auto-select best server

### Cloudflare Automation
- `create_dns_record(subdomain, target)` - Create DNS records
- `automate_service_deployment(service_name, subdomain, app_uuid, port)` - Full automation

### Diagnostics
- `diagnose_tunnel_issues(app_uuid)` - Debug localhost vs tunnel issues
- `get_server_info()` - Server status

## 🌐 Remote Access Setup

### 1. Configure Cloudflare Tunnel

Add to your tunnel config or dashboard:
```yaml
ingress:
  - hostname: mcp.your-domain.com
    service: http://localhost:8765
  - service: http_status:404
```

### 2. Mobile App Configuration

Use `examples/mobile_app_config.json.example` as template:

```json
{
  "name": "Coolify Assistant",
  "endpoint": "https://mcp.your-domain.com",
  "transport": "sse",
  "authentication": {
    "type": "bearer",
    "token": "YOUR_MCP_AUTH_TOKEN"
  }
}
```

## 📝 Configuration

### Required Secrets (Doppler)
- `COOLIFY_API_TOKEN` - From Coolify → Security → API Tokens
- `COOLIFY_TUNNEL_URL` - Your Cloudflare tunnel URL (e.g., `https://cloud.domain.com`)
- `MCP_AUTH_TOKEN` - Random secure token for MCP access
- `USE_TUNNEL` - Set to `"true"` for tunnel access

### Optional Secrets
- `CLOUDFLARE_API_TOKEN` - For DNS automation
- `CLOUDFLARE_ZONE_ID` - Your domain's zone ID
- `CLOUDFLARE_TUNNEL_ID` - For tunnel route automation
- `BASE_DOMAIN` - Your base domain (default: from tunnel URL)
- `MCP_PORT` - Server port (default: 8765)
- `MCP_HOST` - Server host (default: 0.0.0.0)

### Alternative: `.env` File

Copy `.env.example` to `.env` if not using Doppler:
```bash
cp .env.example .env
# Edit .env with your values
python server.py
```

## 🧪 Testing

```bash
# Test Coolify API access
python tests/test_apps.py

# Test Cloudflare automation
python tests/test_cf_automation.py

# Test remote server
python tests/test_remote_server.py
```

## 🚀 Usage Examples

### Multi-Server Deployment
```
AI: "Show me all my servers"
→ Uses list_servers()

AI: "Deploy my Stable Diffusion app to the GPU server"
→ Uses smart_deploy() with requires_gpu=true

AI: "Deploy this lightweight API to the dev box"
→ Uses deploy_to_server(app_uuid, "Dev Box")
```

### Via Mobile AI App
"Deploy my Supabase instance to supabase.mydomain.com"
→ Creates DNS, updates env vars, triggers deployment

### Via curl
```bash
# List applications
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://mcp.your-domain.com/tools

# Execute a tool
curl -X POST \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"tool": "list_applications"}' \
     https://mcp.your-domain.com/execute
```

## 📚 Documentation

- **[Automation Guide](docs/AUTOMATION_GUIDE.md)** - Detailed automation workflows
- **[Examples](examples/)** - Config templates and standalone scripts
- **[Tests](tests/)** - Test suite and usage examples

## 🔒 Security

- ✅ Bearer token authentication
- ✅ Secrets managed via Doppler
- ✅ HTTPS via Cloudflare tunnel
- ✅ No secrets in repository
- 🔄 Rotate `MCP_AUTH_TOKEN` regularly

## 🛠️ Troubleshooting

### Server won't start
```bash
# Check Doppler configuration
doppler secrets

# Verify Python dependencies
pip install -r requirements.txt

# Test with debug logging
doppler run -- python server.py --debug
```

### Can't connect remotely
```bash
# Verify tunnel is running
nslookup mcp.your-domain.com

# Test locally first
curl http://localhost:8765/health

# Check auth token matches
doppler secrets get MCP_AUTH_TOKEN
```

### Tools not working
```bash
# Verify Coolify API token
doppler secrets get COOLIFY_API_TOKEN

# Test Coolify API directly
curl -H "Authorization: Bearer TOKEN" \
     https://your-coolify-url/api/v1/applications
```

## 🤝 Contributing

PRs welcome! This is a practical tool for self-hosted Coolify automation.

## 📄 License

MIT - Use it, improve it, automate all the things!

---

**Quick Links:**
- [Coolify Docs](https://coolify.io/docs)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [Doppler CLI](https://docs.doppler.com/docs/install-cli)
- [Cloudflare Tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)
