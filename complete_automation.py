#!/usr/bin/env python3
"""
Complete Coolify + Cloudflare Automation
Handles DNS records AND tunnel public hostname routes
"""

import os
import httpx
import cloudflare
from dotenv import load_dotenv
from typing import Dict, Optional

load_dotenv()

class CoolifyCloudflareAutomation:
    def __init__(self):
        self.cf_api_token = os.getenv("CLOUDFLARE_API_TOKEN")
        self.cf_zone_id = os.getenv("CLOUDFLARE_ZONE_ID")
        self.cf_tunnel_id = os.getenv("CLOUDFLARE_TUNNEL_ID")
        self.base_domain = os.getenv("BASE_DOMAIN", "therink.io")
        self.tunnel_domain = os.getenv("COOLIFY_TUNNEL_URL", "https://cloud.therink.io")
        
        if not all([self.cf_api_token, self.cf_zone_id, self.cf_tunnel_id]):
            raise ValueError("Missing required Cloudflare credentials")
            
        self.cf = cloudflare.Cloudflare(api_token=self.cf_api_token)
    
    def create_dns_record(self, subdomain: str, target: str = None) -> Dict:
        """Create DNS record pointing to tunnel"""
        if target is None:
            target = "cloud.therink.io"
            
        full_domain = f"{subdomain}.{self.base_domain}"
        
        try:
            result = self.cf.dns.records.create(
                zone_id=self.cf_zone_id,
                name=full_domain,
                type="CNAME",
                content=target,
                ttl=1
            )
            
            return {
                "success": True,
                "message": f"Created DNS record: {full_domain} -> {target}",
                "record_id": result.id,
                "full_domain": full_domain
            }
        except Exception as e:
            return {"success": False, "error": f"DNS creation failed: {str(e)}"}
    
    def create_tunnel_route(self, subdomain: str, service_url: str = "http://localhost:8000") -> Dict:
        """Create tunnel public hostname route"""
        full_domain = f"{subdomain}.{self.base_domain}"
        
        try:
            # Use Cloudflare API to create tunnel public hostname
            headers = {
                "Authorization": f"Bearer {self.cf_api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "hostname": full_domain,
                "service": service_url
            }
            
            response = httpx.post(
                f"https://api.cloudflare.com/client/v4/accounts/{self._get_account_id()}/cfd_tunnel/{self.cf_tunnel_id}/configurations",
                headers=headers,
                json={"config": {"ingress": [{"hostname": full_domain, "service": service_url}]}}
            )
            
            if response.status_code in [200, 201]:
                return {
                    "success": True,
                    "message": f"Created tunnel route: {full_domain} -> {service_url}",
                    "full_domain": full_domain
                }
            else:
                return {
                    "success": False,
                    "error": f"Tunnel route creation failed: {response.text}"
                }
                
        except Exception as e:
            return {"success": False, "error": f"Tunnel route failed: {str(e)}"}
    
    def _get_account_id(self) -> str:
        """Get Cloudflare account ID"""
        try:
            zones = self.cf.zones.list()
            for zone in zones:
                if zone.id == self.cf_zone_id:
                    return zone.account.id
            raise ValueError("Could not find account ID")
        except Exception as e:
            # Fallback - try to extract from zone info
            return "fallback-account-id"
    
    def automate_full_deployment(self, 
                                service_name: str, 
                                subdomain: str, 
                                service_port: int = 8000,
                                coolify_app_uuid: str = None) -> Dict:
        """
        Complete automation: DNS + Tunnel Route + Optional Coolify Update
        """
        results = {
            "service": service_name,
            "subdomain": subdomain,
            "full_domain": f"{subdomain}.{self.base_domain}",
            "steps": [],
            "errors": []
        }
        
        service_url = f"http://localhost:{service_port}"
        
        # Step 1: Create DNS record
        dns_result = self.create_dns_record(subdomain)
        if dns_result.get("success"):
            results["steps"].append(f"✅ DNS: {dns_result['message']}")
        else:
            results["errors"].append(f"❌ DNS: {dns_result.get('error')}")
        
        # Step 2: Create tunnel route
        tunnel_result = self.create_tunnel_route(subdomain, service_url)
        if tunnel_result.get("success"):
            results["steps"].append(f"✅ Tunnel: {tunnel_result['message']}")
        else:
            results["errors"].append(f"❌ Tunnel: {tunnel_result.get('error')}")
        
        # Step 3: Optional Coolify integration (if UUID provided)
        if coolify_app_uuid:
            results["steps"].append(f"ℹ️ Coolify app UUID provided: {coolify_app_uuid}")
            # TODO: Integrate with Coolify API to update app domains
        
        results["success"] = len(results["errors"]) == 0
        results["summary"] = f"🚀 {service_name} automation {'✅ COMPLETE' if results['success'] else '⚠️ PARTIAL'}"
        
        return results


def main():
    """Test the automation"""
    automation = CoolifyCloudflareAutomation()
    
    # Test complete automation
    result = automation.automate_full_deployment(
        service_name="Test Service",
        subdomain="test-complete",
        service_port=3000
    )
    
    print("=== COMPLETE AUTOMATION TEST ===")
    print(f"Service: {result['service']}")
    print(f"Domain: {result['full_domain']}")
    print(f"Success: {result['success']}")
    print("\nSteps:")
    for step in result['steps']:
        print(f"  {step}")
    if result['errors']:
        print("\nErrors:")
        for error in result['errors']:
            print(f"  {error}")
    print(f"\n{result['summary']}")


if __name__ == "__main__":
    main()