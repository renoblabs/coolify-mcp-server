#!/usr/bin/env python3
"""Test listing applications"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def test_applications():
    """Test listing applications via tunnel"""
    token = os.getenv("COOLIFY_API_TOKEN")
    base_url = "https://cloud.therink.io"
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = httpx.get(f"{base_url}/api/v1/applications", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            apps = response.json()
            print(f"Found {len(apps)} applications")
            for app in apps:
                name = app.get("name", "Unknown")
                uuid = app.get("uuid", "no-uuid")
                print(f"  - {name} ({uuid})")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    print("Testing Applications via Tunnel...")
    test_applications()