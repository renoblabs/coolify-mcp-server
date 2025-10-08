#!/usr/bin/env python3
"""Create mcp.therink.io DNS record pointing to cloud.therink.io"""

import os
from dotenv import load_dotenv
import cloudflare

load_dotenv()

CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CF_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "therink.io")

def create_mcp_dns():
    if not CF_API_TOKEN or not CF_ZONE_ID:
        print("[-] Missing Cloudflare credentials")
        return False
    
    try:
        cf = cloudflare.Cloudflare(api_token=CF_API_TOKEN)
        
        # Check if record already exists
        print(f"[*] Checking for existing mcp.{BASE_DOMAIN} record...")
        existing = cf.dns.records.list(zone_id=CF_ZONE_ID, name=f"mcp.{BASE_DOMAIN}")
        
        if existing and len(list(existing)) > 0:
            print(f"[+] DNS record already exists: mcp.{BASE_DOMAIN}")
            for record in existing:
                print(f"    Points to: {record.content}")
            return True
        
        # Create new CNAME record
        print(f"[*] Creating DNS record: mcp.{BASE_DOMAIN} -> cloud.{BASE_DOMAIN}")
        result = cf.dns.records.create(
            zone_id=CF_ZONE_ID,
            type="CNAME",
            name=f"mcp.{BASE_DOMAIN}",
            content=f"cloud.{BASE_DOMAIN}",
            ttl=1,
            proxied=True  # Cloudflare proxy enabled
        )
        
        print(f"[+] SUCCESS! Created DNS record")
        print(f"    Name: mcp.{BASE_DOMAIN}")
        print(f"    Points to: cloud.{BASE_DOMAIN}")
        print(f"    Record ID: {result.id}")
        print(f"\n[+] Your MCP server will be at: https://mcp.{BASE_DOMAIN}")
        print(f"    (Same tunnel as cloud.{BASE_DOMAIN}, just different subdomain)")
        
        return True
        
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MCP DNS Setup")
    print("=" * 60)
    create_mcp_dns()
    print("=" * 60)
