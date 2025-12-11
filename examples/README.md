# Example Configurations

This directory contains ready-to-use configuration examples for different MCP clients and use cases.

## 📁 STDIO Mode (Desktop AI Clients)

### Antigravity (Google AI Studio)

**Windows:**
- File: [`antigravity-windows.json`](antigravity-windows.json)
- Usage: Copy and update paths/credentials, then add to Antigravity settings

**Mac/Linux:**
- File: [`antigravity-mac-linux.json`](antigravity-mac-linux.json)
- Usage: Copy and update paths/credentials, then add to Antigravity settings

### Claude Desktop

**Mac:**
- File: [`claude-desktop-mac.json`](claude-desktop-mac.json)
- Location: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Usage: Copy content to the config file, update paths/credentials, restart Claude

**Windows:**
- File: [`claude-desktop-windows.json`](claude-desktop-windows.json)
- Location: `%APPDATA%\Claude\claude_desktop_config.json`
- Usage: Copy content to the config file, update paths/credentials, restart Claude

### Cline / Continue (VS Code)

- File: [`mcp_config.json.example`](mcp_config.json.example)
- Usage: See [MCP_CLIENT_CONFIGS.md](../MCP_CLIENT_CONFIGS.md) for VS Code setup

## 🌐 SSE Mode (Remote/Mobile Access)

### Mobile Apps

- File: [`mobile_app_config.json.example`](mobile_app_config.json.example)
- Usage: For remote access via Cloudflare Tunnel or reverse proxy
- See: [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md)

### Client Setup Script

- File: [`setup-client.sh`](setup-client.sh)
- Usage: Automated setup script for Linux/Mac clients

## 🛠️ Automation Scripts

### Standalone Automation

- File: [`standalone_automation.py`](standalone_automation.py)
- Usage: Python script for automated deployments without MCP client
- Run: `python standalone_automation.py`

### Fix Tunnel Routes

- File: [`fix_tunnel_routes.py`](fix_tunnel_routes.py)
- Usage: Cloudflare tunnel route management
- Requires: Cloudflare API credentials

## 🔧 How to Use These Examples

### 1. Choose Your Client

Pick the example file that matches your AI client and operating system.

### 2. Copy the Configuration

```bash
# For Antigravity on Windows
cp examples/antigravity-windows.json my-config.json

# For Claude Desktop on Mac
cp examples/claude-desktop-mac.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### 3. Update the Values

Edit the file and replace:

- `C:\\Users\\YourUsername\\coolify-mcp-server\\server_stdio.py` → Your actual absolute path
- `https://your-coolify-url.com` → Your Coolify instance URL
- `your-api-token-here` → Your Coolify API token

### 4. Get Absolute Paths

**Windows:**
```powershell
cd coolify-mcp-server
pwd
# Example output: C:\Users\Mark\coolify-mcp-server
```

**Mac/Linux:**
```bash
cd coolify-mcp-server
pwd
# Example output: /home/mark/coolify-mcp-server
```

Then use: `C:\Users\Mark\coolify-mcp-server\server_stdio.py` (Windows) or `/home/mark/coolify-mcp-server/server_stdio.py` (Mac/Linux)

### 5. Restart Your Client

After updating the config, completely restart your AI client (not just reload).

## 🧪 Test Your Configuration

Run the verification script to test your setup:

```bash
# Update verify_connection.py with your credentials first
python verify_connection.py
```

Expected output:
```
Connecting to server...
Connected! Found 17 tools.
- get_server_info
- list_applications
...
```

## 📝 Configuration Template

All STDIO configs follow this pattern:

```json
{
    "mcpServers": {
        "coolify": {
            "command": "python",  // or "python3" on Mac/Linux
            "args": [
                "/absolute/path/to/server_stdio.py"
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
- ✅ Use **absolute paths** (not relative like `./server_stdio.py`)
- ✅ Use `python3` on Mac/Linux, `python` on Windows
- ✅ Include `https://` in your Coolify URL
- ✅ No trailing slash on the URL

## 🚨 Common Issues

### Path not found

**Problem:** `server_stdio.py` not found

**Solution:** Use absolute path. Run `pwd` in the repo directory and copy the full path.

### Python not found

**Problem:** `python: command not found`

**Solution:** 
- Windows: Use `python`
- Mac/Linux: Use `python3`
- Or use full path: `/usr/bin/python3`

### Connection failed

**Problem:** Can't connect to Coolify

**Solution:** 
1. Check `COOLIFY_BASE_URL` is correct
2. Test: `curl https://your-coolify-url.com`
3. Verify API token is valid

## 📚 More Help

- [QUICKSTART.md](../QUICKSTART.md) - Step-by-step setup guide
- [README.md](../README.md) - Full documentation
- [MCP_CLIENT_CONFIGS.md](../MCP_CLIENT_CONFIGS.md) - Client-specific guides

---

**Need help?** [Open an issue](https://github.com/renoblabs/coolify-mcp-server/issues)
