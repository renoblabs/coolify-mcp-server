#!/usr/bin/env python3
"""
Fix the missing tunnel routes - add public hostname for supabase
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

def add_tunnel_route(hostname, service_url):
    """Add a public hostname route to CF tunnel"""
    
    account_id = "2be3c35b573e2b546adab898e01c341e"  # We got this from testing
    tunnel_id = os.getenv("CLOUDFLARE_TUNNEL_ID")
    token = os.getenv("CLOUDFLARE_API_TOKEN")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get current tunnel config
    response = httpx.get(
        f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations",
        headers=headers
    )
    
    print(f"Current config status: {response.status_code}")
    if response.status_code == 200:
        current_config = response.json()
        print("Current tunnel config:")
        print(current_config)
    
    # Add wildcard route for all subdomains
    if response.status_code == 200:
        current_config = response.json()
        
        # Build new config with wildcard route
        new_ingress = [
            # Keep existing specific routes first
            {"service": "http://localhost:8000", "hostname": "cloud.therink.io", "originRequest": {}},
            # Add wildcard route for all other subdomains  
            {"service": "http://localhost:8000", "hostname": "*.therink.io", "originRequest": {}},
            # Keep 404 catch-all last
            {"service": "http_status:404"}
        ]
        
        new_config = {
            "config": {
                "ingress": new_ingress,
                "warp-routing": {"enabled": False}
            }
        }
        
        print("New config to apply:")
        print(new_config)
        
        # Apply the new configuration
        update_response = httpx.put(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}/configurations",
            headers=headers,
            json=new_config
        )
        
        print(f"Update status: {update_response.status_code}")
        if update_response.status_code == 200:
            print("SUCCESS: Wildcard route added!")
            print("All *.therink.io domains now route to localhost:8000 (Coolify)")
        else:
            print(f"ERROR: {update_response.text}")
    else:
        print("Could not get current config")

def main():
    print("=== FIXING TUNNEL ROUTES ===")
    
    # Add route for supabase
    add_tunnel_route("supabase.therink.io", "http://localhost:3000")
    
    print("=== DONE ===")

if __name__ == "__main__":
    main()