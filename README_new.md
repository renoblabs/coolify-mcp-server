# Coolify MCP Server 🚀

AI-powered assistant for managing Coolify deployments and Cloudflare automation through Model Context Protocol (MCP).

## 🎯 Overview

This MCP server provides **complete automation** for self-hosted services using:
- **Coolify** - Self-hosted PaaS for easy deployments
- **Cloudflare** - DNS management and tunnel configuration
- **MCP** - AI agent integration via Factory Bridge or Claude Desktop
- **Doppler** - Secure secrets management

No more spending hours configuring Cloudflare tunnels and Coolify domains manually!

## ✨ Features

### 🚀 MCP Server Tools Available

#### Coolify Management
- ✅ `list_applications()` - List all applications in Coolify
- ✅ `get_application_details(app_uuid)` - Get detailed app information
- ✅ `deploy_application(app_uuid)` - Deploy/redeploy applications
- ✅ `get_application_environment(app_uuid)` - Get environment variables
- ✅ `update_application_environment(app_uuid, env_vars)` - Update env vars
- ✅ `get_application_logs(app_uuid, lines)` - Retrieve application logs
- ✅ `restart_application(app_uuid)` - Restart applications
- ✅ `stop_application(app_uuid)` - Stop applications

#### Cloudflare Automation
- ✅ `create_dns_record(subdomain, target, record_type)` - Create DNS records
- ✅ `automate_service_deployment(service_name, subdomain, app_uuid, port)` - Full automation!

#### Diagnostics
- ✅ `diagnose_tunnel_issues(app_uuid)` - Diagnose CF tunnel vs localhost issues

### 🎯 What This Solves

- **Automatic DNS Configuration** - Create subdomains like `supabase.therink.io` automatically
- **Environment Variable Management** - Fix localhost references automatically
- **Tunnel Integration** - Seamless Cloudflare tunnel configuration
- **One-Command Deployments** - Deploy services with a single AI command
- **Smart Diagnostics** - Automatically detect and fix common issues

## 🏗️ Architecture

```
Internet → Cloudflare DNS → CF Tunnel → Dev Box → Coolify → Services
          (subdomain.io)   (cloud.io)   (local)   (8000)   (3000+)
```

### Key Components
1. **DNS**: `supabase.therink.io` → `cloud.therink.io` (CNAME)
2. **Tunnel**: `cloud.therink.io` → `192.168.x.x:8000` (your dev box)
3. **Coolify**: Routes requests to appropriate services/ports
4. **Services**: Individual apps (Supabase, n8n, etc.) on specific ports

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Coolify instance running (local or remote)
- Cloudflare account with configured tunnel
- Doppler account (or use .env file)

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/renoblabs/coolify-mcp-server.git
cd coolify-mcp-server

# Create virtual environment
python -m venv coolify_mcp_env

# Activate environment
# Windows:
coolify_mcp_env\Scripts\activate
# Linux/Mac:
source coolify_mcp_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Secrets

#### Option A: Using Doppler (Recommended)
```bash
# Install Doppler CLI
curl -Ls https://cli.doppler.com/install.sh | sh

# Setup project
doppler login
doppler setup

# Set required secrets
doppler secrets set COOLIFY_API_TOKEN="your-coolify-token"
doppler secrets set COOLIFY_BASE_URL="http://localhost:8000"
doppler secrets set COOLIFY_TUNNEL_URL="https://cloud.therink.io"
doppler secrets set USE_TUNNEL="true"
doppler secrets set CLOUDFLARE_API_TOKEN="your-cf-token"
doppler secrets set CLOUDFLARE_ZONE_ID="your-zone-id"
doppler secrets set CLOUDFLARE_TUNNEL_ID="your-tunnel-id"
doppler secrets set BASE_DOMAIN="therink.io"
```

#### Option B: Using .env file
Create a `.env` file in the project root:
```env
COOLIFY_API_TOKEN=your-coolify-token
COOLIFY_BASE_URL=http://localhost:8000
COOLIFY_TUNNEL_URL=https://cloud.therink.io
USE_TUNNEL=true
CLOUDFLARE_API_TOKEN=your-cf-token
CLOUDFLARE_ZONE_ID=your-zone-id
CLOUDFLARE_TUNNEL_ID=your-tunnel-id
BASE_DOMAIN=therink.io
```

### 3. Test the Setup

```bash
# Test with Doppler
doppler run -- python coolify_mcp_server.py

# Or without Doppler
python coolify_mcp_server.py
```

You should see:
```
╭────────────────────────────────────────────────────────╮
│                    FastMCP  2.0                        │
│                                                        │
│  🖥️  Server name:     Coolify Assistant                │
│  📦 Transport:       STDIO                            │
│                                                        │
│  🏎️  FastMCP version: 2.12.4                           │
│  🤝 MCP SDK version: 1.15.0                           │
╰────────────────────────────────────────────────────────╯
```

## 🤖 AI Client Integration

### Factory Bridge (Windows)

1. Create MCP configuration at `%APPDATA%\Factory Bridge\mcp.json`:

```json
{
  "mcpServers": {
    "coolify": {
      "command": "doppler",
      "args": ["run", "--", "python", "C:/path/to/coolify_mcp_server.py"]
    }
  }
}
```

2. Restart Factory Bridge
3. Connect in Factory session: Click "Connect" → "Local Machine"

### Claude Desktop

Add to Claude's MCP settings:

```json
{
  "mcpServers": {
    "coolify": {
      "command": "doppler",
      "args": ["run", "--", "python", "/full/path/to/coolify_mcp_server.py"]
    }
  }
}
```

### VS Code (Continue/Codeium)

Update your extension's MCP configuration similarly.

## 💬 Example AI Commands

Once connected, you can ask your AI assistant:

- **"List all my Coolify applications"**
- **"Deploy app xyz123 with subdomain myapp.therink.io"**
- **"Fix localhost references in app xyz123's environment"**
- **"Diagnose why my app works locally but not through the tunnel"**
- **"Create DNS record for api.therink.io pointing to cloud.therink.io"**
- **"Show logs for the failing application"**
- **"Automate deployment of Supabase with subdomain supabase.therink.io"**

## 🧪 Testing

### Run Test Suite
```bash
# Test Coolify connection via tunnel
doppler run -- python test_tunnel.py

# Test DNS record creation
doppler run -- python test_dns_create.py

# Test complete automation pipeline
doppler run -- python test_complete_automation.py

# Test Cloudflare connectivity
doppler run -- python test_cf_automation.py
```

### Validation Checklist
- [ ] MCP server starts without errors
- [ ] Coolify API responds (Status 200)
- [ ] Can list applications
- [ ] Can create DNS records in Cloudflare
- [ ] Environment variables update correctly
- [ ] Deployments trigger successfully

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `COOLIFY_API_TOKEN` | Your Coolify API token | Required |
| `COOLIFY_BASE_URL` | Local Coolify URL | `http://localhost:8000` |
| `COOLIFY_TUNNEL_URL` | Cloudflare tunnel URL | Required if USE_TUNNEL=true |
| `USE_TUNNEL` | Use tunnel instead of local | `false` |
| `CLOUDFLARE_API_TOKEN` | CF API token | Required for DNS |
| `CLOUDFLARE_ZONE_ID` | Your CF Zone ID | Required for DNS |
| `CLOUDFLARE_TUNNEL_ID` | Your tunnel ID | Optional |
| `BASE_DOMAIN` | Your base domain | `therink.io` |

### URL Switching

Easily switch between local and tunnel access:
```bash
# For local development
doppler secrets set USE_TUNNEL="false"

# For remote access via tunnel
doppler secrets set USE_TUNNEL="true"
```

## ⚠️ Troubleshooting

### MCP Server Appears to Hang
**Issue**: Server starts but seems unresponsive
**Solution**: This is normal STDIO behavior - the server is waiting for JSON-RPC input from the AI client

### Missing Cloudflare Tools
**Issue**: `create_dns_record` not available
**Solution**: Ensure you're using the latest version with integrated CF tools

### Authentication Errors
**Issue**: 401 Unauthorized from Coolify
**Solution**: Verify your API token is correct in Doppler/env file

### DNS Records Not Accessible
**Issue**: DNS created but service unreachable
**Solution**: Add public hostname route in CF tunnel configuration

### Unicode/Encoding Errors
**Issue**: Emoji characters cause issues on Windows
**Solution**: The server uses UTF-8 encoding by default

## 📚 Documentation

### API References
- [Coolify API Documentation](https://coolify.io/docs/api)
- [Cloudflare API Documentation](https://developers.cloudflare.com/api/)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Factory Bridge Guide](https://docs.factory.ai/user-guides/factory-bridge/)

### Project Structure
```
coolify-mcp-server/
├── coolify_mcp_server.py    # Main MCP server with all tools
├── requirements.txt          # Python dependencies
├── test_*.py                # Test scripts for validation
├── .env.example             # Example environment configuration
├── README.md               # This file
└── reliability-droid-report.html  # Investigation report
```

## 🚀 Automation Vision

The end goal is **zero-manual deployment**:
1. **Developer commits code** → GitHub
2. **AI agent triggers deployment** → Coolify
3. **Automation creates DNS + tunnel routes** → Cloudflare
4. **Service is live** → `service.therink.io`

**Current Status**: ~85% complete
- ✅ DNS automation working
- ✅ Coolify API integration complete
- ✅ Environment variable management
- ✅ MCP server stable
- 🔄 Tunnel route automation (manual config still needed)

## 🤝 Contributing

This tool was born from frustration with manual configuration. PRs welcome for:
- Additional Coolify API endpoints
- Enhanced tunnel route automation
- More AI client integrations
- Better error handling and recovery
- Service-specific templates

## 📝 License

MIT - Use it, improve it, and save yourself hours of configuration time!

## 🙏 Acknowledgments

Built with:
- [FastMCP](https://github.com/gofastmcp/fastmcp) - MCP implementation
- [Coolify](https://coolify.io) - Self-hosted PaaS
- [Cloudflare](https://cloudflare.com) - DNS and tunnels
- [Doppler](https://doppler.com) - Secrets management

---

**Don't waste 9 hours configuring services manually - let the AI handle it!** 🤖✨