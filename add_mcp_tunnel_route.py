#!/usr/bin/env python3
"""
Add MCP server route to Cloudflare tunnel via API
Run with: doppler run -- python add_mcp_tunnel_route.py
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# Configuration
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")  # You may need to add this to Doppler
CLOUDFLARE_TUNNEL_ID = os.getenv("CLOUDFLARE_TUNNEL_ID")
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "therink.io")

def add_tunnel_route():
    """Add mcp.therink.io route to the Cloudflare tunnel"""
    
    if not all([CLOUDFLARE_API_TOKEN, CLOUDFLARE_TUNNEL_ID]):
        print(" Missing required environment variables:")
        print(f"   CLOUDFLARE_API_TOKEN: {'' if CLOUDFLARE_API_TOKEN else ''}")
        print(f"   CLOUDFLARE_TUNNEL_ID: {'' if CLOUDFLARE_TUNNEL_ID else ''}")
        return False
    
    # First, let's get the account ID if not set
    if not CLOUDFLARE_ACCOUNT_ID:
        print("[*] Finding Cloudflare account ID...")
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        try:
            response = httpx.get("https://api.cloudflare.com/v4/accounts", headers=headers)
            accounts = response.json()
            if accounts.get("success") and accounts.get("result"):
                account_id = accounts["result"][0]["id"]
                print(f"[+] Found account ID: {account_id}")
                print(f"    TIP: Add to Doppler: doppler secrets set CLOUDFLARE_ACCOUNT_ID=\"{account_id}\"")
            else:
                print("[-] Could not find account ID")
                print("    Please add it manually to Doppler")
                return False
        except Exception as e:
            print(f"[-] Error getting account ID: {e}")
            return False
    else:
        account_id = CLOUDFLARE_ACCOUNT_ID
    
    # Add the tunnel configuration route
    print(f"\n Adding route: mcp.{BASE_DOMAIN}  http://localhost:8765")
    
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Cloudflare tunnel config endpoint
    url = f"https://api.cloudflare.com/v4/accounts/{account_id}/cfd_tunnel/{CLOUDFLARE_TUNNEL_ID}/configurations"
    
    # Get current config first
    try:
        response = httpx.get(url, headers=headers)
        current_config = response.json()
        
        if not current_config.get("success"):
            print(f" Failed to get current config: {current_config.get('errors')}")
            print("\n  MANUAL SETUP REQUIRED:")
            print("   Go to Cloudflare dashboard  Zero Trust  Access  Tunnels")
            print(f"   Add public hostname: mcp.{BASE_DOMAIN}  http://localhost:8765")
            return False
        
        # Build new config with MCP route
        config = current_config.get("result", {}).get("config", {})
        ingress = config.get("ingress", [])
        
        # Check if route already exists
        mcp_hostname = f"mcp.{BASE_DOMAIN}"
        for rule in ingress:
            if rule.get("hostname") == mcp_hostname:
                print(f" Route already exists: {mcp_hostname}")
                return True
        
        # Add new route (before the catch-all)
        new_route = {
            "hostname": mcp_hostname,
            "service": "http://localhost:8765"
        }
        
        # Insert before the last rule (catch-all)
        if ingress:
            ingress.insert(-1, new_route)
        else:
            ingress = [new_route, {"service": "http_status:404"}]
        
        config["ingress"] = ingress
        
        # Update the tunnel configuration
        response = httpx.put(url, headers=headers, json={"config": config})
        result = response.json()
        
        if result.get("success"):
            print(f" Successfully added route!")
            print(f"    Your MCP server is now at: https://{mcp_hostname}")
            print(f"     Allow 30-60 seconds for propagation")
            return True
        else:
            print(f" Failed to update config: {result.get('errors')}")
            return False
            
    except Exception as e:
        print(f" Error: {e}")
        print("\n  MANUAL SETUP REQUIRED:")
        print("   Go to Cloudflare dashboard  Zero Trust  Access  Tunnels")
        print(f"   Add public hostname: mcp.{BASE_DOMAIN}  http://localhost:8765")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Cloudflare Tunnel Route Configuration")
    print("=" * 60)
    success = add_tunnel_route()
    print("=" * 60)
    
    if success:
        print("\n DONE! Your MCP server is accessible remotely!")
    else:
        print("\n Setup incomplete - follow manual instructions above")

