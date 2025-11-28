# Quick Start Guide - Coolify MCP Server

Get up and running in 5 minutes! This guide shows you the fastest path to connecting your AI client to Coolify.

## 🎯 Prerequisites

- Python 3.8+ installed
- A Coolify instance (local or remote)
- An MCP-compatible AI client (Antigravity, Claude Desktop, Cline, etc.)

## 📋 Step-by-Step Setup

### Step 1: Clone & Install (2 minutes)

```bash
# Clone the repository
git clone https://github.com/renoblabs/coolify-mcp-server.git
cd coolify-mcp-server

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get Your Coolify API Token (1 minute)

1. Open your Coolify web interface
2. Go to **Security** → **API Tokens**
3. Click **Create Token**
4. Copy the token (starts with a number like `3|abc123...`)

### Step 3: Test the Connection (1 minute)

Create a test file `test_config.py`:

```python
import os
os.environ["COOLIFY_BASE_URL"] = "https://your-coolify-url.com"  # Change this
os.environ["COOLIFY_API_TOKEN"] = "your-token-here"  # Change this

# Now run verify_connection.py
```

Or just edit `verify_connection.py` directly with your URL and token, then run:

```bash
python verify_connection.py
```

You should see:
```
Connecting to server...
Connected! Found 17 tools.
- get_server_info
- list_applications
...
```

✅ **If you see this, your connection works!**

### Step 4: Configure Your AI Client (1 minute)

Choose your client:

<details>
<summary><b>Antigravity (Google AI Studio)</b></summary>

**Windows:**
1. Find the full path to `server_stdio.py`:
   ```powershell
   cd coolify-mcp-server
   pwd  # Copy this path
   ```
   Example: `C:\Users\YourName\coolify-mcp-server`

2. Create `mcp_config.json` in your project folder:
   ```json
   {
       "mcpServers": {
           "coolify": {
               "command": "python",
               "args": [
                   "C:\\Users\\YourName\\coolify-mcp-server\\server_stdio.py"
               ],
               "env": {
                   "COOLIFY_BASE_URL": "https://your-coolify-url.com",
                   "COOLIFY_API_TOKEN": "your-token-here"
               }
           }
       }
   }
   ```

3. In Antigravity, add this MCP server configuration
4. Restart Antigravity

**Mac/Linux:**
```json
{
    "mcpServers": {
        "coolify": {
            "command": "python3",
            "args": [
                "/home/username/coolify-mcp-server/server_stdio.py"
            ],
            "env": {
                "COOLIFY_BASE_URL": "https://your-coolify-url.com",
                "COOLIFY_API_TOKEN": "your-token-here"
            }
        }
    }
}
```

</details>

<details>
<summary><b>Claude Desktop</b></summary>

**Mac:**
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "coolify": {
      "command": "python3",
      "args": ["/absolute/path/to/coolify-mcp-server/server_stdio.py"],
      "env": {
        "COOLIFY_BASE_URL": "https://your-coolify-url.com",
        "COOLIFY_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Windows:**
Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "coolify": {
      "command": "python",
      "args": ["C:\\Users\\YourName\\coolify-mcp-server\\server_stdio.py"],
      "env": {
        "COOLIFY_BASE_URL": "https://your-coolify-url.com",
        "COOLIFY_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

Restart Claude Desktop.

</details>

<details>
<summary><b>Cline (VS Code)</b></summary>

1. Open VS Code
2. Install the Cline extension
3. Open Cline settings (JSON)
4. Add:

```json
{
  "mcpServers": {
    "coolify": {
      "command": "python",
      "args": ["/absolute/path/to/coolify-mcp-server/server_stdio.py"],
      "env": {
        "COOLIFY_BASE_URL": "https://your-coolify-url.com",
        "COOLIFY_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

Reload VS Code.

</details>

### Step 5: Test It! (30 seconds)

In your AI client, try:

```
"List my Coolify applications"
```

You should see a list of your apps! 🎉

## 🎯 What You Can Do Now

Try these commands:

```
"Show me all my Coolify applications"
"What's the status of my apps?"
"Deploy the app called 'my-app'"
"Show me the logs for my-api"
"What servers do I have?"
"Restart the openhands application"
```

## 🚨 Troubleshooting

### "Server not found" or "Connection failed"

**Check 1:** Is the path absolute?
```bash
# Windows - Get absolute path
cd coolify-mcp-server
pwd

# Mac/Linux
cd coolify-mcp-server
pwd
```

**Check 2:** Can you run it manually?
```bash
python server_stdio.py
# Should wait for input (Ctrl+C to exit)
```

**Check 3:** Is Python in your PATH?
```bash
python --version
# Should show Python 3.8+
```

### "Authentication failed" or "401"

**Check 1:** Is your token correct?
```bash
# Test with curl
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://your-coolify-url.com/api/v1/applications
```

**Check 2:** Did you replace the placeholder values?
- `https://your-coolify-url.com` → Your actual Coolify URL
- `your-token-here` → Your actual API token

### "All connection attempts failed"

**Check 1:** Can you reach Coolify?
```bash
curl https://your-coolify-url.com
```

**Check 2:** Is the URL correct?
- Include `https://` or `http://`
- No trailing slash
- Example: `https://cloud.therink.io` ✅
- Example: `cloud.therink.io/` ❌

### Tools not showing up

1. **Restart your AI client completely** (not just reload)
2. Check the MCP config is valid JSON (use a JSON validator)
3. Look for errors in your AI client's logs
4. Run `python verify_connection.py` to test the connection

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [MCP_CLIENT_CONFIGS.md](MCP_CLIENT_CONFIGS.md) for client-specific tips
- Explore [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for remote access

## 💬 Need Help?

- [Open an issue](https://github.com/renoblabs/coolify-mcp-server/issues)
- Check existing issues for solutions
- Join the Coolify community

---

**You're all set! Start deploying with AI! 🚀**
