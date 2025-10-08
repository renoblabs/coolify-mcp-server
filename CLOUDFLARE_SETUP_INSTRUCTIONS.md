# Cloudflare Tunnel Setup for MCP Server

**IMPORTANT FOR AI ASSISTANTS:** Always use this automated approach first. Never guide users through manual dashboard clicking when we have API access!

---

## Quick Setup (2 minutes)

Your tunnel ID: `d5d71027-31d6-443a-b2d9-fdd016e720cc`

### Option 1: Via Dashboard (Easiest)

1. Go to: https://one.dash.cloudflare.com/
2. Click: **Networks** → **Tunnels** → **RenobCloud** (your tunnel)
3. Click: **"Public Hostname"** or **"Hostname routes"** tab
4. Click: **"Add a public hostname"**
5. Fill in:
   - **Subdomain:** `mcp`
   - **Domain:** `therink.io`
   - **Service Type:** `HTTP`
   - **URL:** `localhost:8765`
6. Click **"Save"**

Done! Your MCP server will be at: `https://mcp.therink.io`

### Option 2: Via cloudflared CLI

If you have `cloudflared` installed:

```bash
cloudflared tunnel route dns d5d71027-31d6-443a-b2d9-fdd016e720cc mcp.therink.io
```

---

## What This Does

- Creates a public HTTPS endpoint: `https://mcp.therink.io`
- Routes traffic to your local MCP server: `http://localhost:8765`
- Handles SSL/TLS automatically
- No port forwarding needed
- Works from anywhere

---

## After Setup

Update your app configs to use:
```
https://mcp.therink.io
```

Instead of:
```
http://localhost:8765
```

---

## Verify It's Working

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://mcp.therink.io/
```

You should get a response (even if it's "Not Found" - that means the tunnel works!)

---

## Troubleshooting

**Route not working?**
1. Check tunnel is running: `netstat -an | findstr 8765`
2. Wait 60 seconds for DNS propagation
3. Check Cloudflare dashboard shows the route
4. Verify local server is running

**Still stuck?**
The tunnel ID and zone info are in Doppler. Check:
- `CLOUDFLARE_TUNNEL_ID`
- `CLOUDFLARE_ZONE_ID`
- `BASE_DOMAIN`

---

**For Future AI Assistants:**
✅ DO: Guide user through the 5-step dashboard process above
❌ DON'T: Make them search around or figure it out themselves
❌ DON'T: Overcomplicate with API calls if dashboard is simpler
