# Doppler Secrets Setup Guide

## Required Secrets for Coolify MCP Server

Here's what you need to set in Doppler for the MCP server to work:

### Core Coolify Secrets (REQUIRED)
```bash
# Get your Coolify API token from: http://localhost:8000/security/api-tokens
doppler secrets set COOLIFY_API_TOKEN="your-coolify-api-token-here"

# Your Cloudflare tunnel URL for accessing Coolify
doppler secrets set COOLIFY_TUNNEL_URL="https://cloud.therink.io"

# Tell the server to use the tunnel instead of localhost
doppler secrets set USE_TUNNEL="true"
```

### MCP Server Authentication (REQUIRED for remote access)
```bash
# Generate a secure random token for MCP authentication
doppler secrets set MCP_AUTH_TOKEN="$(openssl rand -base64 32)"

# Or if openssl isn't available, use:
# doppler secrets set MCP_AUTH_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
```

### Optional Cloudflare Automation Secrets
Only needed if you want DNS automation features:

```bash
# Cloudflare API Token (from https://dash.cloudflare.com/profile/api-tokens)
doppler secrets set CLOUDFLARE_API_TOKEN="your-cf-api-token"

# Your zone ID (from Cloudflare dashboard for therink.io)
doppler secrets set CLOUDFLARE_ZONE_ID="your-zone-id"

# Your Cloudflare tunnel ID (if doing advanced tunnel automation)
doppler secrets set CLOUDFLARE_TUNNEL_ID="your-tunnel-id"

# Base domain (defaults to therink.io)
doppler secrets set BASE_DOMAIN="therink.io"
```

### Optional MCP Server Configuration
```bash
# Change the port (default: 8765)
doppler secrets set MCP_PORT="8765"

# Change the host (default: 0.0.0.0)
doppler secrets set MCP_HOST="0.0.0.0"
```

## Quick Setup Commands

### Minimal Setup (Just to get started)
```bash
cd /path/to/coolify-mcp-server
doppler setup  # Configure your Doppler project

# Set the 3 essential secrets
doppler secrets set COOLIFY_API_TOKEN="get-from-coolify-ui"
doppler secrets set COOLIFY_TUNNEL_URL="https://cloud.therink.io"
doppler secrets set USE_TUNNEL="true"
doppler secrets set MCP_AUTH_TOKEN="$(openssl rand -base64 32)"
```

### Full Setup (All features)
```bash
# Core Coolify
doppler secrets set COOLIFY_API_TOKEN="your-token"
doppler secrets set COOLIFY_TUNNEL_URL="https://cloud.therink.io"
doppler secrets set USE_TUNNEL="true"

# MCP Auth
doppler secrets set MCP_AUTH_TOKEN="$(openssl rand -base64 32)"

# Cloudflare (optional)
doppler secrets set CLOUDFLARE_API_TOKEN="your-cf-token"
doppler secrets set CLOUDFLARE_ZONE_ID="your-zone-id"
doppler secrets set CLOUDFLARE_TUNNEL_ID="your-tunnel-id"
doppler secrets set BASE_DOMAIN="therink.io"
```

## Verify Your Setup

```bash
# Check what you have set
doppler secrets

# Test specific secrets
doppler secrets get COOLIFY_API_TOKEN
doppler secrets get MCP_AUTH_TOKEN
doppler secrets get USE_TUNNEL

# Start the server (it will show which secrets are missing)
./start.sh
```

## What Each Secret Does

| Secret | Purpose | Required? |
|--------|---------|-----------|
| `COOLIFY_API_TOKEN` | Authenticate with Coolify API | ✅ YES |
| `COOLIFY_TUNNEL_URL` | URL to access Coolify (via tunnel) | ✅ YES |
| `USE_TUNNEL` | Use tunnel instead of localhost | ✅ YES |
| `MCP_AUTH_TOKEN` | Secure your MCP server endpoints | ✅ YES (for remote) |
| `CLOUDFLARE_API_TOKEN` | Create DNS records automatically | ⚠️ Optional |
| `CLOUDFLARE_ZONE_ID` | Which domain to create DNS in | ⚠️ Optional |
| `CLOUDFLARE_TUNNEL_ID` | Advanced tunnel automation | ⚠️ Optional |
| `BASE_DOMAIN` | Your base domain name | ⚠️ Optional |
| `MCP_PORT` | What port to run MCP server on | ⚠️ Optional |
| `MCP_HOST` | What interface to bind to | ⚠️ Optional |

## Getting Your Tokens

### Coolify API Token
1. Open Coolify: http://localhost:8000 (or via tunnel)
2. Go to: Settings → Security → API Tokens
3. Click "New Token"
4. Copy the token immediately (you won't see it again!)

### Cloudflare API Token
1. Go to: https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Use "Edit zone DNS" template
4. Select your zone (therink.io)
5. Copy the token

### Cloudflare Zone ID
1. Go to: https://dash.cloudflare.com
2. Select your domain (therink.io)
3. Zone ID is shown on the right side under "API"

## Troubleshooting

### "MCP_AUTH_TOKEN not set"
This is actually fine for local testing! The server will generate one automatically.
For production/remote access, you should set it explicitly:
```bash
doppler secrets set MCP_AUTH_TOKEN="$(openssl rand -base64 32)"
```

### "COOLIFY_API_TOKEN invalid"
- Make sure you copied the full token
- Check it hasn't expired in Coolify
- Generate a new one if needed

### "Connection refused to Coolify"
- Check `USE_TUNNEL` is set to "true"
- Verify `COOLIFY_TUNNEL_URL` is correct
- Make sure Cloudflare tunnel is running

## Migration from Old Setup

If you had secrets in `.env` files or old config files:

```bash
# Don't do this - old way with secrets in files
# .env file (INSECURE)

# Do this instead - Doppler way
doppler secrets set KEY="value"
```

All the old config files with hardcoded tokens have been removed from the repo.
Use Doppler for everything now!
