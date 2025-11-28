# IDE Setup Guide - Coolify MCP Server

## ⚠️ Important: Server Must Be Running First!

Before configuring your IDE, start the MCP server:
```bash
cd /home/user/coolify-mcp-server
python server.py
```

Keep this running in a terminal window!

---

## 🎯 Claude Code (CLI/SDK) - RECOMMENDED

Claude Code is already configured! The `.mcp.json` in this directory should work.

**Configuration file:** `/home/user/coolify-mcp-server/.mcp.json`

**Current config:**
```json
{
  "mcpServers": {
    "coolify-server": {
      "type": "sse",
      "url": "http://localhost:8765/sse",
      "headers": {
        "Authorization": "Bearer E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo="
      }
    }
  }
}
```

**Status:** ✅ Server running, config ready

**Test it:**
Just ask Claude: "List my Coolify applications"

---

## 💻 Claude Desktop App

**Config location:** Platform-specific
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

**Recommended config (STDIO - more stable):**
```json
{
  "mcpServers": {
    "coolify": {
      "command": "python",
      "args": ["/home/user/coolify-mcp-server/server.py"],
      "env": {
        "COOLIFY_API_TOKEN": "YOUR_COOLIFY_TOKEN_HERE",
        "COOLIFY_BASE_URL": "http://192.168.2.30:8000"
      }
    }
  }
}
```

**Note:** For STDIO mode, you need to change `server.py` line 605 from:
```python
app.run(transport="sse", host=MCP_HOST, port=MCP_PORT)
```
to:
```python
app.run(transport="stdio")
```

Then restart Claude Desktop.

---

## 🖱️ Cursor IDE

**Status:** ⚠️ Cursor's MCP support is limited/experimental

**Option 1: Try SSE (may not work)**
1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Search for "MCP"
3. If MCP settings exist, add:
   - URL: `http://localhost:8765/sse`
   - Headers: `Authorization: Bearer E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo=`

**Option 2: STDIO (if Cursor supports it)**
Add to Cursor's settings.json:
```json
{
  "mcp.servers": {
    "coolify": {
      "command": "python",
      "args": ["/home/user/coolify-mcp-server/server.py"]
    }
  }
}
```

**Reality:** Cursor might not support MCP servers yet. Consider using Claude Desktop or Claude Code instead.

---

## 🐛 Common Errors & Solutions

### Error: "Received request before initialization was complete"

**Cause:** Client sending requests without proper MCP handshake

**Solution:**
1. Make sure you're using an MCP-compatible client
2. Update your IDE to the latest version
3. Use STDIO transport instead of SSE (more stable)

### Error: "Connection refused" / "Cannot connect"

**Cause:** Server not running

**Solution:**
```bash
# Check if server is running
lsof -i :8765

# If not, start it
cd /home/user/coolify-mcp-server
python server.py
```

### Error: "Unauthorized" / 401

**Cause:** Missing or wrong auth token

**Solution:** Verify the auth token matches in:
- `.env` file: `MCP_AUTH_TOKEN=...`
- IDE config: `"Authorization": "Bearer ..."`

### Error: "Tools not showing up"

**Cause:** Configuration file in wrong location

**Solution:**
1. Check your IDE's MCP config location (see above)
2. Restart your IDE after changing config
3. Check server logs for connection attempts

### Server shows no activity

**Cause:** IDE not finding the config

**Solution:**
1. Place `.mcp.json` in your project root
2. Or use global config location for your IDE
3. Check IDE documentation for MCP setup

---

## 🎯 Recommended Setup (Easiest)

**For Claude Code (what you're using now):**
1. Server is already running ✅
2. Config is already in place ✅
3. Just use it! Try: "List my Coolify applications"

**For Claude Desktop (if you want GUI):**
1. Change server.py to STDIO mode (line 605)
2. Add config to `~/.config/Claude/claude_desktop_config.json`
3. Restart Claude Desktop
4. MCP tools will appear automatically

**For Cursor:**
1. Check if Cursor actually supports MCP (may not yet)
2. If not, use Claude Code or Claude Desktop instead

---

## 📊 Current Status

- ✅ MCP Server: Running on `http://localhost:8765/sse`
- ✅ Auth Token: Configured
- ✅ Claude Code Config: In place (`.mcp.json`)
- ✅ Test: SSE transport working
- ⚠️  Issue: MCP initialization protocol needs proper client support

---

## 🚀 Quick Test

**In Claude Code (this environment):**

"List my Coolify applications"

**If you get an error, share:**
1. The exact error message
2. Which IDE you're using
3. The config file location you're using

Then I can help you fix it!

---

## 💡 Pro Tips

1. **STDIO is more stable than SSE** for desktop apps
2. **Keep server running** in a terminal while using tools
3. **Check logs** if something doesn't work: `tail -f server.log`
4. **One config per IDE** - each IDE has its own format
5. **Restart IDE** after changing MCP configuration

---

Need help? Share your error message and I'll guide you through!
