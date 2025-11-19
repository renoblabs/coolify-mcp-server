# Coolify MCP Server - Complete Setup Guide

This guide will help you set up and configure your Coolify MCP Server to manage your Coolify infrastructure from IDEs like Claude Code, mobile AI apps, and more.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Server](#running-the-server)
6. [IDE Integration](#ide-integration)
7. [Authentication](#authentication)
8. [Testing](#testing)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment variables (copy and edit)
cp .env.example .env
# Edit .env with your Coolify API token and settings

# 3. Start the server
python server.py --mode http

# 4. For Claude Desktop/local IDE integration, use STDIO mode:
python server.py --mode stdio
```

---

## Requirements

### System Requirements
- Python 3.11 or higher
- Linux, macOS, or Windows
- Network access to your Coolify instance

### Python Dependencies
All dependencies are automatically installed from `requirements.txt`:
- `fastmcp>=2.0.0` - MCP protocol implementation
- `httpx>=0.24.0` - Async HTTP client
- `python-dotenv>=1.0.0` - Environment variable loading
- `cloudflare>=2.19.0` - Cloudflare API integration (optional)

### Optional
- Doppler CLI - For secure secrets management (recommended for production)
- Cloudflare account - For DNS automation features

---

## Installation

### 1. Clone or Download the Repository

```bash
git clone <your-repo-url>
cd coolify-mcp-server
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python server.py --help
```

You should see:
```
usage: server.py [-h] [--mode {stdio,http,sse}] [--host HOST] [--port PORT] [--debug]

Coolify MCP Server

options:
  -h, --help            show this help message and exit
  --mode {stdio,http,sse}
                        Transport mode: stdio (local IPC), http/sse (remote access)
  --host HOST           Host to bind to (default: 127.0.0.1)
  --port PORT           Port to bind to (default: 8765)
  --debug               Enable debug logging
```

---

## Configuration

### Option 1: Environment File (.env) - Recommended for Development

1. Copy the example file:
```bash
cp .env.example .env
```

2. Edit `.env` with your values:
```bash
# Required: Your Coolify API token
COOLIFY_API_TOKEN=your_coolify_api_token_here

# Required: Coolify instance URL
COOLIFY_BASE_URL=http://localhost:8000
# OR if using Cloudflare tunnel:
# USE_TUNNEL=true
# COOLIFY_TUNNEL_URL=https://cloud.yourdomainn.com

# Optional: MCP server authentication (auto-generated if not set)
MCP_AUTH_TOKEN=your_secure_token_here

# Optional: Server binding (defaults shown)
MCP_PORT=8765
MCP_HOST=127.0.0.1

# Optional: Cloudflare DNS automation
CLOUDFLARE_API_TOKEN=your_cloudflare_token
CLOUDFLARE_ZONE_ID=your_zone_id
BASE_DOMAIN=yourdomain.com
```

### Option 2: Doppler Secrets - Recommended for Production

1. Install Doppler CLI:
```bash
curl -Ls https://cli.doppler.com/install.sh | sh
```

2. Configure Doppler:
```bash
doppler setup
```

3. Set secrets:
```bash
doppler secrets set COOLIFY_API_TOKEN="your_token"
doppler secrets set COOLIFY_TUNNEL_URL="https://cloud.yourdomain.com"
doppler secrets set MCP_AUTH_TOKEN="your_secure_auth_token"
```

4. Run with Doppler:
```bash
doppler run -- python server.py
# or
./start.sh
```

### Getting Your Coolify API Token

1. Log into your Coolify instance
2. Go to **Security** → **API Tokens**
3. Click **Create New Token**
4. Copy the token and save it in your `.env` file or Doppler

---

## Running the Server

### HTTP/SSE Mode (Remote Access)

For remote access from mobile apps, web clients, or remote IDEs:

```bash
# Using python directly
python server.py --mode http

# Using the start script (supports Doppler)
./start.sh

# Custom host/port
python server.py --mode http --host 0.0.0.0 --port 8765

# Enable debug logging
python server.py --mode http --debug
```

Server will start on: `http://localhost:8765/sse`

### STDIO Mode (Local IDE Integration)

For local IDE integration (Claude Desktop, Factory Bridge):

```bash
# Using python directly
python server.py --mode stdio

# Using the start script
./start.sh --mode stdio
```

### Windows

Use the optimized Windows runner:

```bash
python run_server.py --mode http
```

This automatically configures UTF-8 encoding for proper emoji display.

---

## IDE Integration

### Claude Code

To use with Claude Code, you'll need to configure an MCP connection. The server must be running in HTTP/SSE mode.

1. Start the server:
```bash
python server.py --mode http
```

2. In Claude Code, add an MCP server configuration pointing to:
   - URL: `http://localhost:8765/sse`
   - Authentication: Bearer token (from `MCP_AUTH_TOKEN`)

### Claude Desktop

1. Configure the server to run in STDIO mode

2. Add to your Claude Desktop configuration file:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "coolify": {
      "command": "python",
      "args": ["/path/to/coolify-mcp-server/server.py", "--mode", "stdio"],
      "env": {
        "COOLIFY_API_TOKEN": "your_token",
        "COOLIFY_BASE_URL": "http://localhost:8000"
      }
    }
  }
}
```

### Mobile Apps (GenSpark, Manus, etc.)

1. Start the server in HTTP mode:
```bash
python server.py --mode http --host 0.0.0.0 --port 8765
```

2. Set up Cloudflare tunnel (recommended) or use ngrok for external access

3. Configure the app with:
   - Endpoint: `https://your-tunnel-url/sse`
   - Transport: SSE
   - Authentication: Bearer token

---

## Authentication

### How It Works

The server uses **Bearer token authentication** for HTTP/SSE mode:

1. When you first start the server without `MCP_AUTH_TOKEN` set, it auto-generates one:
```
🔐 GENERATED NEW MCP AUTH TOKEN (SAVE THIS!):
   AbCdEf123456...
```

2. **Save this token** immediately:
```bash
# In .env file
echo "MCP_AUTH_TOKEN=AbCdEf123456..." >> .env

# Or in Doppler
doppler secrets set MCP_AUTH_TOKEN="AbCdEf123456..."
```

3. All HTTP/SSE requests must include the token:
```bash
curl -H "Authorization: Bearer AbCdEf123456..." http://localhost:8765/sse
```

### Testing Authentication

```bash
# Start server
python server.py --mode http --port 8765 &

# Test without auth (should fail with 401)
curl http://localhost:8765/sse
# Response: {"error": "Authentication required"}

# Test with correct token (should succeed with 200)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8765/sse
```

### Security Notes

- **STDIO mode**: No authentication required (local process communication)
- **HTTP mode**: Authentication enforced via Bearer token
- **Production**: Use HTTPS (Cloudflare Tunnel) + strong token
- **Never commit** your `.env` file or tokens to git

---

## Testing

### 1. Test Server Startup

```bash
python server.py --help
```

### 2. Test HTTP Mode

```bash
# Start server
python server.py --mode http --port 8765

# In another terminal, test the endpoint
curl -H "Authorization: Bearer your_token" http://localhost:8765/sse
```

### 3. Run Comprehensive Tests

```bash
# Test Coolify connectivity
python tests/test_tunnel.py

# Test MCP protocol
python tests/test_remote_server.py

# Test Cloudflare integration
python tests/test_cf_automation.py
```

### 4. Test STDIO Mode

```bash
# Start in STDIO mode
python server.py --mode stdio

# The server will wait for JSON-RPC messages on stdin
```

---

## Troubleshooting

### Server Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastmcp'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Error**: `COOLIFY_API_TOKEN not configured`
```bash
# Solution: Set the environment variable
echo "COOLIFY_API_TOKEN=your_token" >> .env
```

### Authentication Failures

**Issue**: Getting 401 Unauthorized
```bash
# Check that you're including the Authorization header
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8765/sse

# Verify token in .env matches what you're using
cat .env | grep MCP_AUTH_TOKEN
```

**Issue**: Getting 403 Forbidden
```bash
# Token format is wrong or token is invalid
# Ensure format is: Authorization: Bearer TOKEN
# No extra spaces, quotes, or special characters
```

### Connection Issues

**Issue**: Cannot connect to Coolify API
```bash
# Test Coolify connectivity
curl -H "Authorization: Bearer YOUR_COOLIFY_TOKEN" \
  http://localhost:8000/api/v1/applications

# Check COOLIFY_BASE_URL in .env
# Check if Coolify is running
```

**Issue**: Tunnel/remote access not working
```bash
# Verify server is listening on correct interface
python server.py --mode http --host 0.0.0.0 --port 8765

# Check firewall rules
# Verify Cloudflare tunnel configuration
```

### Windows-Specific Issues

**Issue**: Encoding errors or broken emoji
```bash
# Use the Windows-optimized runner
python run_server.py --mode http
```

**Issue**: Path issues
```powershell
# Use absolute paths in configuration
python C:\path\to\server.py --mode http
```

---

## Available Tools

Once connected, you'll have access to 18 MCP tools:

### Coolify Management (8 tools)
- `list_applications()` - List all applications
- `get_application_details(app_uuid)` - Get app details
- `deploy_application(app_uuid, force_rebuild)` - Deploy an app
- `get_application_environment(app_uuid)` - Get environment variables
- `update_application_environment(app_uuid, env_vars)` - Update env vars
- `get_application_logs(app_uuid, lines)` - View application logs
- `restart_application(app_uuid)` - Restart an application
- `stop_application(app_uuid)` - Stop an application

### Multi-Server Management (5 tools)
- `list_servers()` - List all deployment destinations
- `get_server_details(server_uuid)` - Get server information
- `get_server_resources(server_uuid)` - Check resource availability
- `deploy_to_server(app_uuid, server_name_or_uuid, force_rebuild)` - Deploy to specific server
- `smart_deploy(service_name, app_uuid, requires_gpu, requires_high_memory, preferred_server)` - Intelligent server selection

### Cloudflare Automation (2 tools)
- `create_dns_record(subdomain, target, record_type)` - Create DNS records
- `automate_service_deployment(service_name, subdomain, app_uuid, port)` - Full automation

### Diagnostics (3 tools)
- `get_server_info()` - MCP server information
- `diagnose_tunnel_issues(app_uuid)` - Debug tunnel problems

---

## Next Steps

1. **Production Deployment**: See `PRODUCTION_DEPLOYMENT.md` for production setup
2. **Cloudflare Setup**: See `CLOUDFLARE_SETUP_INSTRUCTIONS.md` for tunnel configuration
3. **Doppler Secrets**: See `DOPPLER_SECRETS_GUIDE.md` for secure secrets management
4. **Connection Info**: See `MCP_CONNECTION_INFO.md` for mobile app configuration

---

## Support

For issues, questions, or contributions:
- Check the troubleshooting section above
- Review the documentation files in this repository
- Check your Coolify instance logs
- Verify network connectivity

---

## Security Best Practices

1. **Never commit secrets** - Use `.gitignore` for `.env` file
2. **Use strong tokens** - Generate cryptographically secure random tokens
3. **Use HTTPS in production** - Set up Cloudflare Tunnel or reverse proxy
4. **Restrict access** - Use firewall rules to limit access
5. **Rotate tokens** - Periodically change your MCP_AUTH_TOKEN
6. **Monitor logs** - Check for unauthorized access attempts

---

## Version Information

- **Server Version**: 2.0.0
- **MCP Protocol**: 1.0.0
- **FastMCP**: 2.x
- **Transport Modes**: STDIO, HTTP, SSE
- **Authentication**: Bearer token (HTTP/SSE only)
