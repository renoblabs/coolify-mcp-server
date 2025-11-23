# Coolify MCP Server 🚀

Remote MCP server for Coolify automation over HTTP/SSE. This codebase currently runs in HTTP/SSE mode (not STDIO). Use an MCP‑compatible client or place it behind a reverse proxy (e.g., Cloudflare Tunnel) for remote access.

## 🎯 What It Does

- **📱 Remote Access**: Control Coolify from mobile AI apps (Claude, ChatGPT, Genspark, etc.)
- **🤖 AI-Powered**: Full MCP integration with 18+ automation tools
- **🌐 DNS Automation**: Auto-create Cloudflare DNS records and tunnel routes
- **🔒 Production Security**: Doppler-managed secrets, Bearer token auth, HTTPS
- **⚡ Multi-Server**: Smart deployment across multiple Coolify servers
- **🛠️ Windows & Linux**: Cross-platform with optimized runners

## ⚡ Quick Start (HTTP/SSE)

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

# 4. Start server
python run_server.py
```

### Windows
```powershell
python run_server.py
```

Server runs at `http://localhost:8765`. Expose it via your reverse proxy or Cloudflare Tunnel as needed.

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

1) Configure your reverse proxy (e.g., Cloudflare Tunnel) to route your hostname to `http://localhost:8765`.

Example (Cloudflare Tunnel):
```yaml
ingress:
  - hostname: mcp.your-domain.com
    service: http://localhost:8765
  - service: http_status:404
```

2) Configure your MCP client using `examples/mobile_app_config.json.example`.

## 📝 Configuration

### Required Secrets (Doppler)
- `COOLIFY_API_TOKEN` - From Coolify → Security → API Tokens
- `COOLIFY_TUNNEL_URL` - Optional; used when `USE_TUNNEL=true`
- `MCP_AUTH_TOKEN` - Bearer token enforced by the server (and recommended at your reverse proxy as well)
- `USE_TUNNEL` - Set to `"true"` to prefer your tunnel URL for Coolify API

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
python run_server.py
```

## 🧪 Testing

```bash
# Verify Remote Server (HTTP/SSE)
python tests/test_remote_server.py

# Test Coolify API access
python tests/test_apps.py

# Test Cloudflare automation
python tests/test_cf_automation.py
```

## 🚀 Usage Examples

Use an MCP-compatible client (mobile/desktop) with `transport: "sse"` and bearer auth at your reverse proxy. See `examples/mobile_app_config.json.example`.

## 📚 Documentation

- **[Automation Guide](docs/AUTOMATION_GUIDE.md)** - Detailed automation workflows
- **[Examples](examples/)** - Config templates and standalone scripts
- **[Tests](tests/)** - Test suite and usage examples

## 🔒 Security

- The server enforces Bearer token authentication (401 without valid `MCP_AUTH_TOKEN`).
- Additionally enforce auth at your reverse proxy (Cloudflare Access or mTLS) for defense in depth.
- Secrets managed via Doppler; no secrets in repository.
- Use HTTPS via Cloudflare Tunnel or your proxy.
- Rotate `MCP_AUTH_TOKEN` regularly.

## 🛠️ Troubleshooting

### Server won't start
```bash
# Check Doppler configuration
doppler secrets

# Verify Python dependencies
pip install -r requirements.txt

# Run the remote server
python run_server.py
```

### Can't connect remotely
```bash
# Verify tunnel/proxy DNS
nslookup mcp.your-domain.com

# Verify the HTTP server is listening
python tests/test_remote_server.py
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
