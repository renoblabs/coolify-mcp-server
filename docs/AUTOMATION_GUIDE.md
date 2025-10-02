# Coolify + Cloudflare MCP Automation Guide

## 🎯 Overview

This project provides **complete automation** for self-hosted services using:
- **Coolify** (self-hosted PaaS)
- **Cloudflare Tunnels** (secure external access)
- **MCP (Model Context Protocol)** integration with Factory Bridge
- **Doppler** (secrets management)

## ✅ What's Working

### Core Features
- ✅ **Coolify API Integration** via CF tunnel (`USE_TUNNEL=true`)
- ✅ **Cloudflare DNS Automation** (create records programmatically)
- ✅ **Cloudflare Tunnel API Access** (manage public hostname routes)
- ✅ **MCP Server Integration** (Factory Bridge compatible)
- ✅ **Doppler Secrets Management** (secure credential storage)
- ✅ **Complete Test Suite** (5+ test scripts)

### Automation Capabilities
- **DNS Record Creation**: `subdomain.therink.io` → `cloud.therink.io`
- **Tunnel Route Management**: Cloudflare tunnel public hostnames
- **Service Deployment**: End-to-end automation from code to public URL
- **Environment Management**: Secure secrets via Doppler

## 🔧 Architecture

```
Internet → Cloudflare DNS → CF Tunnel → Dev Box → Coolify → Services
          (subdomain.io)   (cloud.io)   (local)   (8000)   (3000)
```

### Key Components
1. **DNS**: `supabase.therink.io` → `cloud.therink.io` (CNAME)
2. **Tunnel**: `cloud.therink.io` → `192.168.x.x:8000` (your dev box)
3. **Coolify**: Routes requests to appropriate services/ports
4. **Services**: Individual apps (Supabase, etc.) on specific ports

## 🚀 Quick Start

### Prerequisites
- Coolify running on dev box
- Cloudflare tunnel configured (`*.therink.io`)
- Doppler account with project
- Python 3.11+ environment

### Setup Steps
```bash
# 1. Clone repository
git clone https://github.com/renoblabs/coolify-mcp-server
cd coolify-mcp-server

# 2. Create virtual environment
python -m venv coolify_mcp_env
coolify_mcp_env\Scripts\activate  # Windows
# source coolify_mcp_env/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure Doppler secrets
doppler login
doppler setup

# Set required secrets:
doppler secrets set COOLIFY_API_TOKEN="your-coolify-token"
doppler secrets set COOLIFY_TUNNEL_URL="https://cloud.therink.io"
doppler secrets set USE_TUNNEL="true"
doppler secrets set CLOUDFLARE_API_TOKEN="your-cf-token"
doppler secrets set CLOUDFLARE_ZONE_ID="your-zone-id"
doppler secrets set CLOUDFLARE_TUNNEL_ID="your-tunnel-id"
doppler secrets set BASE_DOMAIN="therink.io"

# 5. Test the setup
doppler run -- python test_tunnel.py
doppler run -- python test_complete_automation.py
```

## 🛠️ MCP Integration

### Factory Bridge Configuration
```json
{
  "mcpServers": {
    "coolify-automation": {
      "command": "cmd",
      "args": [
        "/c",
        "cd /d C:\\path\\to\\coolify-mcp-server && .\\coolify_mcp_env\\Scripts\\activate && doppler run -- python coolify_mcp_server.py"
      ],
      "env": {},
      "disabled": false
    }
  }
}
```

Save this to: `%APPDATA%\\Factory Bridge\\mcp.json`

### Available MCP Tools
- `get_applications()` - List Coolify applications
- `deploy_application(app_uuid)` - Trigger deployment
- `get_application_environment(app_uuid)` - Get env vars
- `update_application_environment(app_uuid, vars)` - Update env vars
- `configure_service_subdomain(service, subdomain)` - Configure domains
- `diagnose_tunnel_issues(app_uuid)` - Debug tunnel problems

## 🔍 Testing & Validation

### Test Scripts
- `test_tunnel.py` - Verify Coolify API via tunnel
- `test_dns_create.py` - Test DNS record creation
- `test_complete_automation.py` - Full automation components
- `test_apps.py` - List applications via API
- `test_cf_automation.py` - Cloudflare API connectivity

### Running Tests
```bash
# Test individual components
doppler run -- python test_tunnel.py
doppler run -- python test_dns_create.py

# Test complete automation
doppler run -- python test_complete_automation.py
```

## ⚠️ Known Issues & Solutions

### Issue 1: `USE_TUNNEL=false`
**Problem**: MCP server tries to connect to local Coolify instead of tunnel
**Solution**: `doppler secrets set USE_TUNNEL="true"`

### Issue 2: Missing CF Tunnel Routes
**Problem**: DNS records exist but services not accessible
**Solution**: Add public hostname routes in Cloudflare tunnel config

### Issue 3: MCP Tools Disappearing
**Problem**: `coolify-automation___*` tools become unavailable
**Solution**: Restart MCP server by toggling disabled flag in mcp.json

### Issue 4: Unicode Errors in Tests
**Problem**: Emoji characters cause encoding issues on Windows
**Solution**: Use plain ASCII in test outputs

## 📋 Next Steps (For Knowledge Droid)

### High Priority
1. **Complete Tunnel Route Automation** - Finish the tunnel public hostname API integration
2. **Supabase Deployment Test** - End-to-end test with real service
3. **MCP Server Stability** - Fix connection reliability issues
4. **Documentation Enhancement** - User-friendly setup guide

### Medium Priority
1. **Service Templates** - Pre-configured automation for common services
2. **Monitoring Integration** - Health checks and status monitoring
3. **Error Handling** - Robust error recovery and reporting
4. **Multi-Service Support** - Handle multiple services per project

### Technical Details for Knowledge Droid
- **Cloudflare Account ID**: `2be3c35b573e2b546adab898e01c341e`
- **Tunnel Name**: `RenobCloud`
- **Tunnel ID**: `d5d71027-31d6-443a-b2d9-fdd016e720cc`
- **Base Domain**: `therink.io`
- **Working DNS Records**: `test-automation.therink.io`, `test-fixed.therink.io`, `supabase.therink.io`

## 🔗 Resources

- **Repository**: https://github.com/renoblabs/coolify-mcp-server
- **Coolify API Docs**: https://coolify.io/docs/api
- **Cloudflare API Docs**: https://developers.cloudflare.com/api/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Factory Bridge**: https://docs.factory.ai/user-guides/factory-bridge/

## 💡 Automation Vision

The end goal is **zero-manual deployment**:
1. **Developer commits code** → GitHub
2. **AI agent triggers deployment** → Coolify
3. **Automation creates DNS + tunnel routes** → Cloudflare
4. **Service is live** → `service.therink.io`

**Current Status**: ~80% complete. DNS automation working, tunnel route automation needs completion.