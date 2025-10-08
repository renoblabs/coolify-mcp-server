# Prompt for New Factory Session on Dev Box

**Copy this entire prompt and paste it into Factory chat on your dev box:**

---

I need help setting up the coolify-mcp-server on my dev box (Linux server running Coolify). This is a continuation of work done on my main Windows PC.

## Context:
- I have Coolify running on this dev box (localhost:8000)
- I have a Cloudflare tunnel already configured (tunnel ID: d5d71027-31d6-443a-b2d9-fdd016e720cc)
- My main gaming rig IP is 192.168.2.30 where I was testing the MCP server
- BUT the main rig goes to sleep, so I need the MCP server running HERE on the dev box (24/7 uptime)

## What I Need:
1. Install the coolify-mcp-server from GitHub: https://github.com/renoblabs/coolify-mcp-server
2. Set up Python environment and dependencies
3. Configure Doppler secrets (or .env file) with my Coolify API credentials
4. Start the MCP server on port 8765
5. Update the Cloudflare tunnel config to route:
   - `mcp.therink.io` → `localhost:8765` (MCP server)
   - `cloud.therink.io` → `localhost:8000` (Coolify)
6. Restart the tunnel

## My Credentials (stored in Doppler on main box):
- COOLIFY_API_TOKEN: [I'll provide when needed]
- CLOUDFLARE_API_TOKEN: [I'll provide when needed]
- CLOUDFLARE_ZONE_ID: [I'll provide when needed]
- USE_TUNNEL: true
- COOLIFY_TUNNEL_URL: https://cloud.therink.io

## System Info:
- This is my dev box running Linux
- Coolify is already installed and working
- Cloudflare tunnel is running (need to find config location)
- Factory Bridge should be connected

**Please help me get this set up step-by-step using Bridge commands where possible!**

---

