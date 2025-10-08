# Credentials for Dev Box Setup

Copy these values when prompted by Droid on the dev box:

## Doppler Secrets to Set:

COOLIFY_API_TOKEN (run on main box to get):
```
doppler secrets get COOLIFY_API_TOKEN --plain
```

CLOUDFLARE_API_TOKEN:
```
doppler secrets get CLOUDFLARE_API_TOKEN --plain
```

CLOUDFLARE_ZONE_ID:
```
doppler secrets get CLOUDFLARE_ZONE_ID --plain
```

CLOUDFLARE_TUNNEL_ID:
```
doppler secrets get CLOUDFLARE_TUNNEL_ID --plain
```

MCP_AUTH_TOKEN:
```
Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY
```

BASE_DOMAIN:
```
therink.io
```

USE_TUNNEL:
```
true
```

COOLIFY_TUNNEL_URL:
```
https://cloud.therink.io
```

---

## Quick Command to Get All Values (run on main box):

```powershell
doppler run -- powershell -Command "
Write-Host 'COOLIFY_API_TOKEN=' -NoNewline; doppler secrets get COOLIFY_API_TOKEN --plain
Write-Host 'CLOUDFLARE_API_TOKEN=' -NoNewline; doppler secrets get CLOUDFLARE_API_TOKEN --plain  
Write-Host 'CLOUDFLARE_ZONE_ID=' -NoNewline; doppler secrets get CLOUDFLARE_ZONE_ID --plain
Write-Host 'CLOUDFLARE_TUNNEL_ID=' -NoNewline; doppler secrets get CLOUDFLARE_TUNNEL_ID --plain
Write-Host 'MCP_AUTH_TOKEN=Qw2xK-YhJO5Bp7XfvLZDVjH1kF3GxmnRn7UyQNzM_EY'
Write-Host 'BASE_DOMAIN=therink.io'
Write-Host 'USE_TUNNEL=true'
Write-Host 'COOLIFY_TUNNEL_URL=https://cloud.therink.io'
"
```

Copy the output and paste it when setting up on dev box!
