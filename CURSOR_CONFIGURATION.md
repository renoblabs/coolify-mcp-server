# Cursor IDE MCP Configuration
# Location: Cursor Settings → MCP Servers

## Option 1: Via Cursor UI
1. Open Cursor Settings (Cmd/Ctrl + ,)
2. Search for "MCP"
3. Add new server with these settings:
   - Name: Coolify
   - URL: http://localhost:8765/sse
   - Type: SSE
   - Headers: {"Authorization": "Bearer E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo="}

## Option 2: Via Config File
Add this to your Cursor settings.json:

```json
{
  "mcp.servers": {
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

## Option 3: Use STDIO Transport (Recommended for Cursor)
Cursor works better with STDIO. Use this config instead:

```json
{
  "mcp.servers": {
    "coolify-server": {
      "command": "python",
      "args": ["/home/user/coolify-mcp-server/server.py"],
      "env": {
        "COOLIFY_API_TOKEN": "your-coolify-api-token",
        "COOLIFY_BASE_URL": "http://192.168.2.30:8000"
      }
    }
  }
}
```

Note: For STDIO, you need to change server.py to run in stdio mode instead of SSE.
