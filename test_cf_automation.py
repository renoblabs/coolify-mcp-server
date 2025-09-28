#!/usr/bin/env python3
"""
Test CF Automation - Quick test of our Cloudflare automation
"""

import os
from dotenv import load_dotenv
import cloudflare

load_dotenv()

def test_cf_connection():
    """Test Cloudflare API connection"""
    CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
    CF_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
    
    if not CF_API_TOKEN or not CF_ZONE_ID:
        print("ERROR: Missing CF credentials in environment")
        return False
    
    try:
        cf = cloudflare.Cloudflare(api_token=CF_API_TOKEN)
        
        # Test: Get zone info
        zone = cf.zones.get(zone_id=CF_ZONE_ID)
        print(f"SUCCESS: Connected to Cloudflare zone: {zone.name}")
        
        # Test: List existing DNS records
        records = cf.dns.records.list(zone_id=CF_ZONE_ID, per_page=5)
        record_count = len(list(records))
        print(f"SUCCESS: Found {record_count} DNS records")
        
        return True
    except Exception as e:
        print(f"ERROR: CF connection failed: {str(e)}")
        return False

def test_coolify_connection():
    """Test Coolify API connection"""
    COOLIFY_BASE_URL = os.getenv("COOLIFY_BASE_URL")
    API_TOKEN = os.getenv("COOLIFY_API_TOKEN")
    
    if not API_TOKEN:
        print("ERROR: Missing Coolify API token")
        return False
    
    try:
        import httpx
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json"
        }
        
        with httpx.Client() as client:
            response = client.get(f"{COOLIFY_BASE_URL}/api/v1/applications", headers=headers)
            
        if response.status_code == 200:
            apps = response.json()
            print(f"SUCCESS: Connected to Coolify: {len(apps.get('data', []))} applications found")
            return True
        else:
            print(f"ERROR: Coolify connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: Coolify connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Automation Setup...")
    print()
    
    cf_ok = test_cf_connection()
    coolify_ok = test_coolify_connection()
    
    print()
    if cf_ok and coolify_ok:
        print("ALL SYSTEMS GO! Ready for full automation!")
    else:
        print("Some connections failed - check your Doppler secrets")