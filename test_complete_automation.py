#!/usr/bin/env python3
"""Test complete automation without unicode issues"""

import os
import httpx
import cloudflare
from dotenv import load_dotenv

load_dotenv()

def test_account_id():
    """Test getting account ID"""
    cf = cloudflare.Cloudflare(api_token=os.getenv("CLOUDFLARE_API_TOKEN"))
    zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
    
    try:
        zones = cf.zones.list()
        for zone in zones:
            if zone.id == zone_id:
                print(f"Account ID: {zone.account.id}")
                return zone.account.id
        print("Could not find account ID")
        return None
    except Exception as e:
        print(f"Error getting account ID: {e}")
        return None

def test_tunnel_api():
    """Test tunnel API access"""
    account_id = test_account_id()
    if not account_id:
        return
        
    tunnel_id = os.getenv("CLOUDFLARE_TUNNEL_ID")
    token = os.getenv("CLOUDFLARE_API_TOKEN")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        # Try to get tunnel info
        response = httpx.get(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/cfd_tunnel/{tunnel_id}",
            headers=headers
        )
        
        print(f"Tunnel API Status: {response.status_code}")
        if response.status_code == 200:
            tunnel_data = response.json()
            print(f"Tunnel Name: {tunnel_data.get('result', {}).get('name', 'Unknown')}")
            print("SUCCESS: Tunnel API accessible")
        else:
            print(f"ERROR: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_dns_creation():
    """Test DNS record creation"""
    cf = cloudflare.Cloudflare(api_token=os.getenv("CLOUDFLARE_API_TOKEN"))
    zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
    
    try:
        result = cf.dns.records.create(
            zone_id=zone_id,
            name="test-final.therink.io",
            type="CNAME", 
            content="cloud.therink.io",
            ttl=1
        )
        print("SUCCESS: DNS record created")
        print(f"Record ID: {result.id}")
        return True
    except Exception as e:
        print(f"DNS Error: {e}")
        return False

if __name__ == "__main__":
    print("=== TESTING COMPLETE AUTOMATION COMPONENTS ===")
    print()
    
    print("1. Testing Account ID retrieval...")
    test_account_id()
    print()
    
    print("2. Testing Tunnel API access...")
    test_tunnel_api()
    print()
    
    print("3. Testing DNS creation...")
    test_dns_creation()
    print()
    
    print("=== TEST COMPLETE ===")