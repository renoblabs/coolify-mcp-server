# Production Deployment Guide

**Target Environment:** Linux Dev Box (the old PC running Coolify)

**Production URL:** `https://mcp.therink.io`

**Goal:** Deploy the Coolify MCP Server for remote access from AI assistants and mobile apps

---

## Quick Info:
- **Main Rig IP:** `192.168.2.30`
- **MCP Server Port:** `8765`
- **Tunnel ID:** `d5d71027-31d6-443a-b2d9-fdd016e720cc`

---

## Step 1: Find Your Tunnel Config

Run this command to find where the tunnel config is:

```bash
find ~ -name "config.yml" -path "*cloudflared*" 2>/dev/null
```

Common locations:
- `~/.cloudflared/config.yml`
- `/etc/cloudflared/config.yml`
- `$HOME/.cloudflared/config.yml`

Once found, note the path!

---

## Step 2: Backup Current Config

```bash
sudo cp ~/.cloudflared/config.yml ~/.cloudflared/config.yml.backup
```

(Replace `~/.cloudflared/config.yml` with your actual path if different)

---

## Step 3: Edit the Config

Open the config file:

```bash
sudo nano ~/.cloudflared/config.yml
```

**Add this section to the `ingress:` block:**

```yaml
ingress:
  - hostname: mcp.therink.io
    service: http://192.168.2.30:8765
  - hostname: cloud.therink.io
    service: http://localhost:8000
  # ... keep any other existing routes ...
  - service: http_status:404  # This should be the LAST line
```

**IMPORTANT:** 
- The catch-all `service: http_status:404` MUST be the last entry
- Make sure indentation matches (use spaces, not tabs)
- Add the mcp route BEFORE the cloud route

---

## Step 4: Verify Config Syntax

Check if the config is valid:

```bash
cloudflared tunnel ingress validate
```

If you get errors, check your spacing/indentation!

---

## Step 5: Restart the Tunnel

### If running as a service:
```bash
sudo systemctl restart cloudflared
sudo systemctl status cloudflared
```

### If running in Docker:
```bash
docker restart cloudflared
# OR
docker-compose restart cloudflared
```

### If running manually:
Find and kill the process, then restart:
```bash
ps aux | grep cloudflared
sudo kill <PID>
# Then restart however you normally start it
```

---

## Step 6: Test It!

From your **main box** (Windows), run:

```powershell
curl https://mcp.therink.io
```

You should get a response from your MCP server (even if it's "Not Found", that means routing works!)

---

## Troubleshooting

**Config file not found?**
- Check if tunnel is running: `ps aux | grep cloudflared`
- Check systemd service: `systemctl status cloudflared`
- Look for Docker: `docker ps | grep cloudflare`

**Tunnel won't restart?**
- Check logs: `journalctl -u cloudflared -f`
- Or Docker logs: `docker logs cloudflared`

**Still not working?**
- Verify main box is reachable from dev box: `ping 192.168.2.30`
- Check MCP server is running on main box
- Check firewall on main box allows port 8765

---

## What This Does

When someone (including you from Genspark) visits:
```
https://mcp.therink.io
```

The Cloudflare tunnel will:
1. Receive the request
2. Forward it to `192.168.2.30:8765` (your main rig)
3. Your MCP server responds
4. Response goes back through the tunnel

---

**Once done, come back to the main box and we'll test it!** 🚀
