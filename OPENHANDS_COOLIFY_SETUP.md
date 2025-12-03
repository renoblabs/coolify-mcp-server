# 🚀 Coolify Integration for OpenHands - READY TO USE!

Your Coolify server is now connected and ready to use with OpenHands!

## ✅ Connection Status
- **Coolify Server**: https://cloud.therink.io
- **API Token**: Configured and working
- **Applications Found**: 3 applications
- **Integration**: Ready for OpenHands

## 🎯 Your Applications
1. **openhands** (exited:unhealthy) - UUID: cs4k8wcs48c0skgsos0gksk8
2. **renoblabs/-real--estate--analysis--tool** (exited:unhealthy)
3. **renoblabs/-brunson** (exited:unhealthy)

## 🔧 How to Use in OpenHands

### Option 1: Direct Python Integration (Recommended)

You can now use these functions directly in OpenHands:

```python
# Import the integration
from coolify_for_openhands import *

# List all applications
list_apps()

# Deploy an application
deploy_app("openhands")

# Restart an application  
restart_app("openhands")

# Get application logs
get_logs("openhands")

# Get detailed status
get_status("openhands")

# Quick status overview
status()

# OpenHands-specific shortcuts
deploy_openhands()    # Deploy OpenHands specifically
restart_openhands()   # Restart OpenHands specifically
openhands_logs()      # Get OpenHands logs
```

### Option 2: MCP Integration (Alternative)

If you prefer MCP, use this configuration:

```json
{
  "mcpServers": {
    "coolify": {
      "command": "python",
      "args": ["/workspace/project/coolify-mcp-server/server.py"],
      "env": {
        "COOLIFY_API_TOKEN": "5|Zs8nkfu0I6re2WxCiZVmjMgTkXnJsMHVlRyiESgZ4f80dd46",
        "COOLIFY_BASE_URL": "https://cloud.therink.io"
      }
    }
  }
}
```

## 🎮 Example Usage

### Deploy Your OpenHands Application
```python
from coolify_for_openhands import deploy_openhands, openhands_logs

# Deploy OpenHands
deploy_openhands()

# Check the deployment logs
openhands_logs()
```

### Manage All Applications
```python
from coolify_for_openhands import list_apps, deploy_app, restart_app

# See all your apps
list_apps()

# Deploy any app by name
deploy_app("openhands")

# Restart any app
restart_app("renoblabs/-real--estate--analysis--tool")
```

### Monitor Application Status
```python
from coolify_for_openhands import status, get_status, get_logs

# Quick overview of all apps
status()

# Detailed status of specific app
get_status("openhands")

# Get recent logs
get_logs("openhands", lines=50)
```

## 🔍 Available Functions

| Function | Description | Example |
|----------|-------------|---------|
| `list_apps()` | List all applications | `list_apps()` |
| `deploy_app(name)` | Deploy/redeploy app | `deploy_app("openhands")` |
| `restart_app(name)` | Restart application | `restart_app("openhands")` |
| `stop_app(name)` | Stop application | `stop_app("openhands")` |
| `get_logs(name, lines)` | Get application logs | `get_logs("openhands", 100)` |
| `get_status(name)` | Get detailed status | `get_status("openhands")` |
| `status()` | Quick overview | `status()` |
| `deploy_openhands()` | Deploy OpenHands | `deploy_openhands()` |
| `restart_openhands()` | Restart OpenHands | `restart_openhands()` |
| `openhands_logs()` | Get OpenHands logs | `openhands_logs()` |

## 🚨 Important Notes

1. **App Names**: You can use either the full app name or just "openhands" for the OpenHands app
2. **UUIDs**: You can also use UUIDs instead of names if preferred
3. **Status**: All your apps are currently "exited:unhealthy" - you may want to deploy them
4. **Logs**: Use `get_logs()` to monitor deployment progress
5. **Fuzzy Matching**: The system will find apps even with partial names

## 🎯 Quick Start Commands

Try these commands in OpenHands:

```python
# Quick status check
from coolify_for_openhands import status
status()

# Deploy OpenHands
from coolify_for_openhands import deploy_openhands
deploy_openhands()

# Check deployment progress
from coolify_for_openhands import openhands_logs
openhands_logs()
```

## 🔧 Troubleshooting

If you encounter issues:

1. **Connection Problems**: The API token is already configured and tested
2. **App Not Found**: Use `list_apps()` to see exact app names
3. **Deployment Issues**: Check logs with `get_logs(app_name)`
4. **Status Issues**: Use `get_status(app_name)` for detailed info

## 🎉 You're All Set!

Your Coolify integration is ready to use. You can now manage your applications directly from OpenHands using natural language commands or the Python functions above.

**Next Steps:**
1. Try deploying your OpenHands application: `deploy_openhands()`
2. Monitor the deployment: `openhands_logs()`
3. Check status: `status()`

Happy deploying! 🚀