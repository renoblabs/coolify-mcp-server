# Direct API Guide - When MCP Won't Cooperate

**TL;DR:** MCP clients can be buggy. If you're frustrated, skip MCP entirely and use the direct API. It works reliably.

## The Reality of MCP (2025)

MCP (Model Context Protocol) is still new. Different clients implement it differently:
- ❌ Cursor: Experimental, often doesn't load servers properly
- ⚠️ Claude Code: Works sometimes, breaks sometimes  
- ⚠️ Claude Desktop: Better support, but still finnicky
- ⚠️ Antigravity: Varies by version

**If you've spent hours debugging MCP and it still won't work - STOP. Use the direct API instead.**

## Option 1: Use the CoolifyAPI Helper

```python
from coolify_api import CoolifyAPI
import os

# Set your credentials
os.environ["COOLIFY_BASE_URL"] = "https://cloud.therink.io"
os.environ["COOLIFY_API_TOKEN"] = "your-token-here"

# Create API client
api = CoolifyAPI()

# List all applications
apps = api.list_applications()
for app in apps:
    print(f"{app['name']}: {app['status']}")

# Start an app
api.start_application("app-uuid-here")

# Get logs
logs = api.get_logs("app-uuid-here")
print(logs)

# Check status
api.print_status()
```

### CLI Usage

```bash
# List all apps
python coolify_api.py

# Start an app
python coolify_api.py start <uuid>

# Stop an app  
python coolify_api.py stop <uuid>

# Restart an app
python coolify_api.py restart <uuid>

# Get logs
python coolify_api.py logs <uuid>
```

## Option 2: Direct HTTP Calls (Works Anywhere)

If you're in an AI IDE like Cursor and MCP tools aren't available, the AI can make HTTP calls directly:

### List Applications
```powershell
$token = "your-coolify-token"
$response = Invoke-RestMethod -Uri "https://cloud.therink.io/api/v1/applications" `
    -Headers @{Authorization="Bearer $token"}
$response | ForEach-Object { Write-Host "$($_.name): $($_.status)" }
```

### Start/Deploy Application
```powershell
$token = "your-coolify-token"
Invoke-RestMethod -Uri "https://cloud.therink.io/api/v1/applications/APP_UUID/start" `
    -Headers @{Authorization="Bearer $token"} -Method Post
```

### Stop Application
```powershell
$token = "your-coolify-token"
Invoke-RestMethod -Uri "https://cloud.therink.io/api/v1/applications/APP_UUID/stop" `
    -Headers @{Authorization="Bearer $token"} -Method Post
```

### Restart Application
```powershell
$token = "your-coolify-token"
Invoke-RestMethod -Uri "https://cloud.therink.io/api/v1/applications/APP_UUID/restart" `
    -Headers @{Authorization="Bearer $token"} -Method Post
```

### Get Application Details
```powershell
$token = "your-coolify-token"
$app = Invoke-RestMethod -Uri "https://cloud.therink.io/api/v1/applications/APP_UUID" `
    -Headers @{Authorization="Bearer $token"}
$app | ConvertTo-Json -Depth 5
```

## Option 3: curl (Universal)

```bash
# List apps
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://cloud.therink.io/api/v1/applications

# Start app
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
     https://cloud.therink.io/api/v1/applications/APP_UUID/start

# Stop app
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
     https://cloud.therink.io/api/v1/applications/APP_UUID/stop

# Get app details
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://cloud.therink.io/api/v1/applications/APP_UUID
```

## Your Credentials (therink.io setup)

```
Coolify URL: https://cloud.therink.io
API Token: Get from Coolify → Security → API Tokens
```

## Why Direct API > MCP (Sometimes)

| Aspect | MCP | Direct API |
|--------|-----|------------|
| Setup | Complex | Simple |
| Reliability | Client-dependent | Always works |
| Debugging | Painful | Easy |
| Speed | Same | Same |
| Works in any IDE | No | Yes |

## When to Use Each

**Use MCP when:**
- Your client supports it well (rare)
- You want natural language integration
- You have time to debug

**Use Direct API when:**
- MCP won't load/work
- You need it to work NOW
- You're in an IDE that doesn't support MCP
- You're frustrated and want something that works

## API Endpoints Reference

| Action | Method | Endpoint |
|--------|--------|----------|
| List apps | GET | `/api/v1/applications` |
| Get app | GET | `/api/v1/applications/{uuid}` |
| Start app | POST | `/api/v1/applications/{uuid}/start` |
| Stop app | POST | `/api/v1/applications/{uuid}/stop` |
| Restart app | POST | `/api/v1/applications/{uuid}/restart` |
| Get logs | GET | `/api/v1/applications/{uuid}/logs?lines=100` |
| Get envs | GET | `/api/v1/applications/{uuid}/envs` |
| List servers | GET | `/api/v1/servers` |
| Get server | GET | `/api/v1/servers/{uuid}` |

## The Bottom Line

Don't waste hours debugging MCP. If it doesn't work in 15 minutes:
1. Use `coolify_api.py` directly
2. Or have your AI make HTTP calls
3. Get your actual work done
4. Fix MCP later when you have time

**Your goal is deploying apps, not fighting protocols.**

