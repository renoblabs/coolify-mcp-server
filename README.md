# Coolify MCP Server 🚀

**Control your Coolify instance from any MCP-compatible AI client** (Claude Desktop, Antigravity, Cline, Continue, etc.)

Deploy, manage, and monitor your applications through natural language commands. Works with both **local STDIO** (desktop AI tools) and **remote SSE** (mobile apps, remote access).

## 🎯 What It Does

- **🤖 AI-Powered Deployments**: Deploy GitHub repos through natural conversation
- **📊 Application Management**: List, deploy, restart, monitor all your Coolify apps
- **🌐 Multi-Server Support**: Smart deployment across multiple servers
- **🔍 Intelligent Debugging**: Get logs, diagnose issues, check health
- **☁️ Cloudflare Integration**: Automated DNS and tunnel management
- **🔒 Secure**: Bearer token auth, HTTPS support, Doppler secrets

## ⚡ Quick Start

### For Desktop AI Tools (Antigravity, Claude Desktop, Cline, etc.)

**1. Clone the repository:**
```bash
git clone https://github.com/renoblabs/coolify-mcp-server.git
cd coolify-mcp-server
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Get your Coolify API token:**
- Go to your Coolify instance → **Security** → **API Tokens**
- Create a new token and copy it

**4. Create your MCP config:**

Create a file (e.g., `mcp_config.json`) with:

```json
{
    "mcpServers": {
        "coolify": {
            "command": "python",
            "args": [
                "/absolute/path/to/coolify-mcp-server/server_stdio.py"
            ],
            "env": {
                "COOLIFY_BASE_URL": "https://your-coolify-url.com",
                "COOLIFY_API_TOKEN": "your-api-token-here"
            }
        }
    }
}
```

**Important:** 
- Use **absolute paths** for the `args` field
- Replace `https://your-coolify-url.com` with your actual Coolify URL
- Replace `your-api-token-here` with your API token from step 3

**5. Configure your AI client:**

<details>
<summary><b>Antigravity (Google AI Studio)</b></summary>

1. Open Antigravity settings
2. Add the MCP server configuration from step 4
3. Restart Antigravity
4. Test: "List my Coolify applications"

</details>

<details>
<summary><b>Claude Desktop</b></summary>

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "coolify": {
      "command": "python",
      "args": ["/absolute/path/to/coolify-mcp-server/server_stdio.py"],
      "env": {
        "COOLIFY_BASE_URL": "https://your-coolify-url.com",
        "COOLIFY_API_TOKEN": "your-token"
      }
    }
  }
}
```

Restart Claude Desktop.

</details>

<details>
<summary><b>Cline / Continue (VS Code)</b></summary>

See [MCP_CLIENT_CONFIGS.md](MCP_CLIENT_CONFIGS.md) for detailed VS Code setup.

</details>

### For Remote/Mobile Access (SSE Mode)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for setting up remote access via Cloudflare Tunnel or reverse proxy.

## 🛠️ Available Tools (17 Total)

### Application Management
- `list_applications` - List all apps with status
- `get_application_details` - Get detailed app info
- `deploy_application` - Deploy/redeploy an app
- `get_application_logs` - View deployment logs
- `restart_application` - Restart an app
- `stop_application` - Stop an app

### Environment & Configuration
- `get_application_environment` - Get environment variables
- `update_application_environment` - Update env vars

### Multi-Server Management
- `list_servers` - List all deployment servers
- `get_server_details` - Get server info
- `get_server_resources` - Check CPU/RAM/disk
- `deploy_to_server` - Deploy to specific server
- `smart_deploy` - Auto-select best server based on requirements

### Cloudflare Automation
- `create_dns_record` - Create DNS records
- `automate_service_deployment` - Full deployment automation

### Diagnostics
- `diagnose_tunnel_issues` - Debug connectivity issues
- `get_server_info` - MCP server status

## 💬 Example Commands

Once connected, you can use natural language:

```
"List all my Coolify applications"
"Deploy the app called 'my-nextjs-app'"
"Show me the logs for my-api"
"What servers do I have available?"
"Deploy my-app to the server called 'production'"
"Restart the openhands application"
```

## 🧰 Helper Scripts

We've included Python scripts for quick testing and automation:

### `verify_connection.py`
Test your MCP connection and list available tools:
```bash
python verify_connection.py
```

### `show_apps.py`
Quick status overview of all applications:
```bash
python show_apps.py
```

### `deploy_app.py`
Deploy a specific app by name or UUID:
```bash
# Deploy by name
python deploy_app.py my-app

# Force rebuild
python deploy_app.py my-app --force
```

### `list_servers.py`
List available deployment servers:
```bash
python list_servers.py
```

## 📝 Configuration Options

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `COOLIFY_BASE_URL` | ✅ Yes | Your Coolify instance URL | `https://coolify.example.com` |
| `COOLIFY_API_TOKEN` | ✅ Yes | API token from Coolify | `3\|abc123...` |
| `MCP_AUTH_TOKEN` | No | Bearer token for SSE mode | Auto-generated if not set |
| `MCP_PORT` | No | Port for SSE server | `8765` (default) |
| `MCP_HOST` | No | Host for SSE server | `0.0.0.0` (default) |
| `CLOUDFLARE_API_TOKEN` | No | For DNS automation | Your CF token |
| `CLOUDFLARE_ZONE_ID` | No | For DNS automation | Your zone ID |

### Using `.env` File

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Using Doppler (Production)

For production deployments, use Doppler for secret management:

```bash
doppler setup
doppler secrets set COOLIFY_API_TOKEN="your-token"
doppler secrets set COOLIFY_BASE_URL="https://your-coolify.com"
```

See [DOPPLER_SECRETS_GUIDE.md](DOPPLER_SECRETS_GUIDE.md) for details.

## 🚀 Deployment Modes

### STDIO Mode (Local Desktop)
- **Use case**: Desktop AI tools (Antigravity, Claude Desktop, Cline)
- **Transport**: Standard input/output
- **Setup**: Add to your AI client's MCP config
- **Security**: Local only, no network exposure

### SSE Mode (Remote/Mobile)
- **Use case**: Mobile apps, remote access, team sharing
- **Transport**: HTTP Server-Sent Events
- **Setup**: Run `python server.py` and expose via reverse proxy
- **Security**: Bearer token auth + HTTPS recommended

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for SSE setup.

## 🔒 Security Best Practices

1. **Never commit secrets** - Use `.env` or Doppler
2. **Use HTTPS** - Always use SSL for remote access
3. **Rotate tokens** - Change API tokens regularly
4. **Restrict access** - Use Cloudflare Access or VPN for remote access
5. **Monitor logs** - Check for unauthorized access attempts

## 🧪 Testing

Test your setup with the verification script:

```bash
python verify_connection.py
```

Expected output:
```
Connecting to server...
Connected! Found 17 tools.
- get_server_info
- list_applications
- deploy_application
...
```

## 📚 Additional Documentation

- **[MCP_CLIENT_CONFIGS.md](MCP_CLIENT_CONFIGS.md)** - Client-specific setup guides
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Remote/SSE deployment
- **[DOPPLER_SECRETS_GUIDE.md](DOPPLER_SECRETS_GUIDE.md)** - Production secrets management
- **[IDE_SETUP_GUIDE.md](IDE_SETUP_GUIDE.md)** - VS Code integration
- **[CLOUDFLARE_SETUP_INSTRUCTIONS.md](CLOUDFLARE_SETUP_INSTRUCTIONS.md)** - DNS automation

## 🛠️ Troubleshooting

### "Connection failed" or "Server not found"

1. Check that `server_stdio.py` path is absolute
2. Verify Python is in your PATH
3. Test manually: `python server_stdio.py` (should wait for input)
4. Check your AI client's MCP logs

### "Authentication failed" or "401 Unauthorized"

1. Verify your `COOLIFY_API_TOKEN` is correct
2. Check token hasn't expired in Coolify
3. Ensure `COOLIFY_BASE_URL` is accessible

### "All connection attempts failed"

1. Verify `COOLIFY_BASE_URL` is reachable
2. Check if Coolify is behind a firewall
3. Test: `curl https://your-coolify-url.com/api/v1/applications -H "Authorization: Bearer YOUR_TOKEN"`

### Tools not showing up

1. Restart your AI client completely
2. Check MCP config syntax (valid JSON)
3. Look for errors in AI client logs
4. Run `python verify_connection.py` to test

## 🤝 Contributing

Contributions welcome! This is a practical tool for the Coolify community.

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Test with `verify_connection.py`
5. Submit a PR

## 📄 License

MIT - Use it, improve it, automate all the things!

---

## 🔗 Quick Links

- [Coolify Documentation](https://coolify.io/docs)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [Antigravity by Google](https://deepmind.google/technologies/gemini/antigravity/)
- [Claude Desktop](https://claude.ai/download)
- [Doppler CLI](https://docs.doppler.com/docs/install-cli)

---

**Made with ❤️ for the Coolify community**

*Having issues? [Open an issue](https://github.com/renoblabs/coolify-mcp-server/issues) or check the docs!*
