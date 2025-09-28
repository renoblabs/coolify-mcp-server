#!/usr/bin/env python3
"""Test different ports for Coolify connection"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

def test_coolify_port(port):
    """Test Coolify connection on specific port"""
    API_TOKEN = os.getenv("COOLIFY_API_TOKEN")
    base_url = f"http://174.88.139.173:{port}"
    
    try:
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json"
        }
        
        with httpx.Client(timeout=10) as client:
            response = client.get(f"{base_url}/api/v1/applications", headers=headers)
            
        print(f"Port {port}: {response.status_code} - {response.reason_phrase}")
        if response.status_code == 200:
            apps = response.json()
            print(f"  SUCCESS: Found {len(apps.get('data', []))} applications")
            return True
        return False
            
    except Exception as e:
        print(f"Port {port}: ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Coolify ports...")
    print()
    
    ports_to_test = [80, 8000, 443, 3000]
    
    for port in ports_to_test:
        test_coolify_port(port)
    
    print()
    print("Also test tunnel mode:")
    print("doppler secrets set USE_TUNNEL=true")