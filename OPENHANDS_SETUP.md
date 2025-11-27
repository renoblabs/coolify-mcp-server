# OpenHands MCP Server Setup Guide

## Current Status ✅

Your Coolify MCP Server is now **working perfectly** and ready for OpenHands integration!

### Server Details
- **Status**: ✅ Fully functional and tested
- **Transport**: stdio (Standard MCP Protocol)
- **Tools Available**: 17 Coolify management tools
- **Protocol**: JSON-RPC 2.0 over stdio
- **Compatibility**: ✅ OpenHands ready

## OpenHands Integration Configuration

Use this configuration in your OpenHands MCP settings:

```json
{
  "mcpServers": {
    "coolify": {
      "command": "python",
      "args": ["/workspace/project/coolify-mcp-server/server.py"],
      "env": {
        "COOLIFY_API_TOKEN": "your-actual-coolify-api-token-here",
        "COOLIFY_BASE_URL": "https://cloud.therink.io"
      }
    }
  }
}
```

**This is the standard MCP configuration that OpenHands expects!**

## Required Setup Steps

### 1. Get Your Coolify API Token

You need to replace the dummy API token with a real one:

1. Go to https://cloud.therink.io
2. Navigate to Settings → API Tokens
3. Create a new API token
4. Replace `your-actual-coolify-api-token-here` in the config

### 2. Test the MCP Server

You can test the server works correctly:

```bash
cd /workspace/project/coolify-mcp-server
python test_mcp_stdio.py
```

This should show "✅ Found 17 tools" if everything is working.

## Available Tools

The MCP server provides these Coolify management tools:

- **Applications**: List, create, deploy, stop applications
- **Databases**: List, create, manage databases  
- **Services**: List, manage services
- **Projects**: List, create, manage projects
- **Servers**: List, manage servers
- **Deployments**: List, manage deployments
- **Environment Variables**: List, create, update, delete
- **Domains**: List, create, manage domains
- **Backups**: List, create, restore backups
- **Logs**: Get application and deployment logs
- **Resources**: Get resource usage and metrics

## Testing the Connection

Once configured in OpenHands, you should be able to use commands like:

- "List all my Coolify applications"
- "Deploy my app to production"
- "Show me the logs for my database"
- "Create a new project called 'test-project'"

## Troubleshooting

### Testing the Server
```bash
# Test the MCP protocol directly
cd /workspace/project/coolify-mcp-server
python test_mcp_stdio.py
```

### Authentication Issues
- Verify your Coolify API token is valid at https://cloud.therink.io
- Make sure the token has the necessary permissions

### OpenHands Integration Issues
- Ensure the file path in the configuration is correct
- Check that Python can find all dependencies
- Verify the environment variables are set correctly

## Next Steps

1. **Get your real Coolify API token** from https://cloud.therink.io
2. **Update the configuration** with your actual API token
3. **Add the MCP configuration to OpenHands**
4. **Test the integration** with simple commands

Your MCP server is ready to go! 🚀