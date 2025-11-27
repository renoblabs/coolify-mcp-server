# MCP Client Configurations for Coolify Server

This MCP server works with multiple clients. Here are the configurations:

## Claude Desktop (Anthropic)

**Config Location:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
```json
{
  "mcpServers": {
    "coolify": {
      "command": "doppler",
      "args": ["run", "--", "python", "C:\\Users\\19057\\Projects\\coolify-mcp-server\\coolify-mcp-server\\server_stdio.py"],
      "cwd": "C:\\Users\\19057\\Projects\\coolify-mcp-server\\coolify-mcp-server"
    }
  }
}
```

**Or without Doppler (using .env file):**
```json
{
  "mcpServers": {
    "coolify": {
      "command": "python",
      "args": ["C:\\Users\\19057\\Projects\\coolify-mcp-server\\coolify-mcp-server\\server_stdio.py"],
      "cwd": "C:\\Users\\19057\\Projects\\coolify-mcp-server\\coolify-mcp-server"
    }
  }
}
```

## Cursor IDE

**Config Location:** `%APPDATA%\Cursor\User\settings.json`

**Configuration:**
```json
{
  "mcp.servers": {
    "coolify": {
      "command": "doppler",
      "args": ["run", "--", "python", "C:\\Users\\19057\\Projects\\coolify-mcp-server\\coolify-mcp-server\\server_stdio.py"],
      "cwd": "C:\\Users\\19057\\Projects\\coolify-mcp-server\\coolify-mcp-server"
    }
  }
}
```

## JetBrains IDEs (with MCP plugin)

**Configuration:** Similar to Claude Desktop format

## Cline (VS Code Extension)

**Config Location:** VS Code settings or Cline extension settings

**Configuration:**
```json
{
  "mcpServers": {
    "coolify": {
      "command": "doppler",
      "args": ["run", "--", "python", "C:\\Users\\19057\\Projects\\coolify-mcp-server\\coolify-mcp-server\\server_stdio.py"],
      "cwd": "C:\\Users\\19057\\Projects\\coolify-mcp-server\\coolify-mcp-server"
    }
  }
}
```

## Continue.dev

**Configuration:** Add to Continue config file

## Testing the Connection

After configuring any client:

1. **Restart the client completely**
2. **Wait 10-15 seconds** for MCP to initialize
3. **Test with:** "Can you list my Coolify applications?"

## Verifying It Works

You should see 18 tools available:
- list_applications
- get_application_details
- deploy_application
- get_application_environment
- update_application_environment
- get_application_logs
- restart_application
- stop_application
- list_servers
- get_server_details
- get_server_resources
- deploy_to_server
- smart_deploy
- create_dns_record
- automate_service_deployment
- diagnose_tunnel_issues
- get_server_info

## Troubleshooting

### Server Won't Start

1. **Check Python:** `python --version` (need 3.8+)
2. **Check dependencies:** `pip list | grep "fastmcp\|httpx\|cloudflare"`
3. **Check Doppler:** `doppler secrets get COOLIFY_API_TOKEN --plain`
4. **Test manually:** `doppler run -- python server_stdio.py`

### Can't Connect to Coolify

1. **Test API:** 
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" https://cloud.therink.io/api/v1/applications
   ```
2. **Check tunnel is running**
3. **Verify API token is valid**

### Tools Not Appearing

1. **Completely restart the client** (not just reload)
2. **Check client logs** for errors
3. **Verify config file saved correctly**
4. **Make sure path uses double backslashes** on Windows: `C:\\Users\\...`

## Your Specific Setup

- **Coolify URL:** https://cloud.therink.io
- **Auth:** Managed via Doppler
- **Server Path:** `C:\Users\19057\Projects\coolify-mcp-server\coolify-mcp-server`
- **Server File:** `server_stdio.py`

## Alternative: HTTP/SSE Mode (Remote Access)

For mobile apps or remote access, use `server.py` instead:

```bash
doppler run -- python server.py
# Server runs at http://localhost:8765
# Accessible at https://mcp.therink.io (if tunnel configured)
```

Then use the mobile app config from `examples/mobile_app_config.json.example`

---

**Repository:** https://github.com/renoblabs/coolify-mcp-server

**Need help?** Check CURSOR_SETUP.md, QUICKSTART.md, or READY_TO_USE.md

