# Coolify MCP Server 🚀

AI-powered assistant for managing Coolify deployments and configurations through Model Context Protocol (MCP).

## What This Does

This MCP server gives you an AI assistant that can:
- **Diagnose CF tunnel vs localhost issues** automatically
- **Deploy applications** with proper subdomain configuration (like `supabase.therink.io`)
- **Manage environment variables** and fix localhost references
- **Monitor logs and application status**
- **Automate the boring config shit** so you can focus on building

No more spending 9 hours configuring Cloudflare tunnels and Coolify domains manually!

## Quick Setup

1. **Clone and setup:**
   ```bash
   git clone https://github.com/renoblabs/coolify-mcp-server.git
   cd coolify-mcp-server
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Get your Coolify API token:**
   - Go to `http://localhost:8000/security/api-tokens`
   - Create a new API token
   - Copy it

3. **Configure secrets with Doppler:**
   ```bash
   # Install Doppler CLI (if not already installed)
   curl -Ls https://cli.doppler.com/install.sh | sh
   
   # Setup Doppler project
   doppler setup
   
   # Add your secrets
   doppler secrets set COOLIFY_API_TOKEN="your_actual_token_here"
   doppler secrets set COOLIFY_BASE_URL="http://localhost:8000"
   doppler secrets set COOLIFY_TUNNEL_URL="https://cloud.therink.io"
   doppler secrets set USE_TUNNEL="false"
   ```

4. **Start the MCP server:**
   ```bash
   ./start_with_doppler.sh
   ```

## AI Client Integration

### VS Code with Continue/Codeium
1. Install Continue or Codeium extension
2. Update your MCP configuration:
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

### Claude Desktop
Add to your Claude Desktop MCP configuration:
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

## Available AI Commands

Once connected, you can ask your AI to:

- `"Check all my applications and their status"`
- `"Deploy my app with subdomain myapp.therink.io"`
- `"Fix all localhost references in my environment variables"`
- `"Diagnose why my app works on localhost but not through CF tunnel"`
- `"Set up Supabase with subdomain supabase.therink.io"`
- `"Show me logs for the failing application"`
- `"Restart all stopped services"`

## Key Features

### 🔍 Tunnel Issue Diagnosis
Automatically finds common CF tunnel problems:
- Hardcoded localhost URLs in environment variables
- HTTP vs HTTPS mismatches
- CORS configuration issues
- Port references that need updating

### 🌐 Subdomain Management
Built-in helpers for your therink.io subdomains:
- Auto-configures services with proper domains
- Updates environment variables
- Handles CF tunnel routing suggestions

### ⚙️ Environment Variable Management
- Bulk update environment variables
- Find and replace localhost references
- Validate configuration against tunnel setup

### 🔄 URL Switching
Easily switch between local and tunnel URLs:
```bash
# For local development
doppler secrets set USE_TUNNEL="false"

# When working remotely via CF tunnel
doppler secrets set USE_TUNNEL="true"
```

## Configuration Options

### Doppler Secrets
- `COOLIFY_API_TOKEN`: Your Coolify API token
- `COOLIFY_BASE_URL`: Base URL (http://localhost:8000)
- `COOLIFY_TUNNEL_URL`: CF tunnel URL (https://cloud.therink.io)
- `USE_TUNNEL`: Switch between local/tunnel (true/false)

### Fallback .env File
If you prefer not to use Doppler, copy `examples/.env.example` to `.env` and configure manually.

## Testing

Test your API connection:
```bash
# Test basic connection
curl -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Accept: application/json" \
     http://localhost:8000/api/v1/applications
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AI Client     │────│  FastMCP Server  │────│   Coolify API   │
│ (VS Code/Claude)│    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌──────────────────┐
                       │ Diagnostic Tools │
                       │ Domain Helpers   │
                       │ CF Tunnel Fixes  │
                       └──────────────────┘
```

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common issues and solutions.

## Contributing

This is a practical tool born from frustration with manual Coolify configuration. PRs welcome for:
- Additional Coolify API endpoints
- Better tunnel diagnostics
- More AI client integrations
- Documentation improvements

## License

MIT - Use it, improve it, don't waste 9 hours on config like we did.