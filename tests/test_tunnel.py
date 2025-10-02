#!/usr/bin/env python3
"""Test Coolify connection via tunnel"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

def test_tunnel_connection():
    """Test Coolify connection via CF tunnel"""
    API_TOKEN = os.getenv("COOLIFY_API_TOKEN")
    tunnel_url = os.getenv("COOLIFY_TUNNEL_URL")
    use_tunnel = os.getenv("USE_TUNNEL", "false").lower() == "true"
    
    print(f"USE_TUNNEL: {use_tunnel}")
    print(f"Tunnel URL: {tunnel_url}")
    
    # Use tunnel URL if enabled
    base_url = tunnel_url if use_tunnel else os.getenv("COOLIFY_BASE_URL")
    
    try:
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json"
        }
        
        print(f"Testing: {base_url}/api/v1/applications")
        
        with httpx.Client(timeout=15) as client:
            response = client.get(f"{base_url}/api/v1/applications", headers=headers)
            
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            apps = response.json()
            if isinstance(apps, list):
                print(f"SUCCESS: Found {len(apps)} applications")
                # Show some app info
                for app in apps[:3]:
                    print(f"  - {app.get('name', 'Unknown')}: {app.get('uuid', 'No UUID')}")
            else:
                print(f"SUCCESS: Found {len(apps.get('data', []))} applications")
                # Show some app info
                for app in apps.get('data', [])[:3]:
                    print(f"  - {app.get('name', 'Unknown')}: {app.get('uuid', 'No UUID')}")
            
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Coolify via CF Tunnel...")
    print()
    test_tunnel_connection()