#!/usr/bin/env python3
"""Test creating a DNS record"""

import os
import cloudflare
from dotenv import load_dotenv

load_dotenv()

def test_dns_creation():
    """Test creating a test DNS record"""
    CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
    CF_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
    BASE_DOMAIN = os.getenv("BASE_DOMAIN", "therink.io")
    
    try:
        cf = cloudflare.Cloudflare(api_token=CF_API_TOKEN)
        
        # Create a test DNS record
        subdomain = "test-automation"
        full_domain = f"{subdomain}.{BASE_DOMAIN}"
        target = "cloud.therink.io"
        
        print(f"Creating DNS record: {full_domain} -> {target}")
        
        result = cf.dns.records.create(
            zone_id=CF_ZONE_ID,
            name=full_domain,
            type="CNAME",
            content=target,
            ttl=1
        )
        
        print(f"SUCCESS: Created DNS record!")
        print(f"  Domain: {full_domain}")
        print(f"  Target: {target}")
        print(f"  Record ID: {result.id}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing DNS Record Creation...")
    print()
    test_dns_creation()