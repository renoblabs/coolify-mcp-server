#!/usr/bin/env python3
"""
Coolify MCP Server - AI Assistant for Coolify Management
Provides tools for managing Coolify applications, deployments, and configurations
With integrated Cloudflare automation capabilities
"""

from fastmcp import FastMCP
import httpx
import json
import os
from typing import Dict, List, Optional, Any
import asyncio
from dotenv import load_dotenv
import cloudflare

# Load environment variables from .env file
load_dotenv()

app = FastMCP("Coolify Assistant")

# Configuration - using Doppler for secrets
COOLIFY_BASE_URL = os.getenv("COOLIFY_BASE_URL", "http://localhost:8000")
API_TOKEN = os.getenv("COOLIFY_API_TOKEN")

# Cloudflare configuration
CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CF_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")  # For therink.io domain
CF_TUNNEL_ID = os.getenv("CLOUDFLARE_TUNNEL_ID")  # Your tunnel ID
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "therink.io")

# Optional: Support for switching between local and tunnel URLs
if os.getenv("USE_TUNNEL", "false").lower() == "true":
    COOLIFY_BASE_URL = os.getenv("COOLIFY_TUNNEL_URL", "https://cloud.therink.io")

async def make_coolify_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
    """Make authenticated request to Coolify API"""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    if API_TOKEN:
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    
    url = f"{COOLIFY_BASE_URL}/api/v1{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, headers=headers, json=data, timeout=30)
            return response.json() if response.text else {}
        except Exception as e:
            return {"error": str(e)}

# ==================== COOLIFY MANAGEMENT TOOLS ====================

@app.tool()
async def list_applications() -> Dict:
    """List all applications in Coolify"""
    return await make_coolify_request("GET", "/applications")

@app.tool()
async def get_application_details(app_uuid: str) -> Dict:
    """Get detailed information about a specific application
    
    Args:
        app_uuid: The UUID of the application
    """
    return await make_coolify_request("GET", f"/applications/{app_uuid}")

@app.tool()
async def deploy_application(app_uuid: str, force_rebuild: bool = False) -> Dict:
    """Deploy an application
    
    Args:
        app_uuid: The UUID of the application to deploy
        force_rebuild: Whether to force rebuild the application
    """
    data = {"force_rebuild": force_rebuild}
    return await make_coolify_request("POST", f"/applications/{app_uuid}/deploy", data)

@app.tool()
async def get_application_environment(app_uuid: str) -> Dict:
    """Get environment variables for an application
    
    Args:
        app_uuid: The UUID of the application
    """
    return await make_coolify_request("GET", f"/applications/{app_uuid}/environment")

@app.tool()
async def update_application_environment(app_uuid: str, env_vars: Dict[str, str]) -> Dict:
    """Update environment variables for an application
    
    Args:
        app_uuid: The UUID of the application
        env_vars: Dictionary of environment variables to set/update
    """
    # Get existing env vars first
    existing = await make_coolify_request("GET", f"/applications/{app_uuid}/environment")
    
    # Merge with new vars
    if "data" in existing:
        current_vars = existing.get("data", {})
        current_vars.update(env_vars)
        env_vars = current_vars
    
    return await make_coolify_request("PUT", f"/applications/{app_uuid}/environment", {"environment": env_vars})

@app.tool()
async def get_application_logs(app_uuid: str, lines: int = 100) -> Dict:
    """Get logs for an application
    
    Args:
        app_uuid: The UUID of the application
        lines: Number of log lines to retrieve (default: 100)
    """
    return await make_coolify_request("GET", f"/applications/{app_uuid}/logs?lines={lines}")

@app.tool()
async def restart_application(app_uuid: str) -> Dict:
    """Restart an application
    
    Args:
        app_uuid: The UUID of the application to restart
    """
    return await make_coolify_request("POST", f"/applications/{app_uuid}/restart")

@app.tool()
async def stop_application(app_uuid: str) -> Dict:
    """Stop an application
    
    Args:
        app_uuid: The UUID of the application to stop
    """
    return await make_coolify_request("POST", f"/applications/{app_uuid}/stop")

# ==================== CLOUDFLARE AUTOMATION TOOLS ====================

@app.tool()
async def create_dns_record(subdomain: str, target: str = "cloud.therink.io", 
                           record_type: str = "CNAME") -> Dict:
    """Create a DNS record in Cloudflare for a subdomain
    
    Args:
        subdomain: The subdomain to create (e.g., 'supabase')
        target: The target domain/IP (default: 'cloud.therink.io')
        record_type: DNS record type (CNAME, A, etc.)
    """
    if not CF_API_TOKEN or not CF_ZONE_ID:
        return {"error": "Cloudflare API token and Zone ID required"}
    
    try:
        cf = cloudflare.Cloudflare(api_token=CF_API_TOKEN)
        full_domain = f"{subdomain}.{BASE_DOMAIN}"
        
        # Create DNS record
        result = cf.dns.records.create(
            zone_id=CF_ZONE_ID,
            type=record_type,
            name=full_domain,
            content=target,
            ttl=1  # Automatic TTL
        )
        
        return {
            "success": True,
            "message": f"Created {record_type} record: {full_domain} -> {target}",
            "record_id": result.id,
            "full_domain": full_domain
        }
    except Exception as e:
        return {"error": f"Failed to create DNS record: {str(e)}"}

@app.tool() 
async def automate_service_deployment(service_name: str, subdomain: str, 
                                     app_uuid: str, port: int = 8000) -> Dict:
    """FULLY AUTOMATE service deployment with CF tunnel and DNS
    
    Args:
        service_name: Name of the service (e.g., 'Supabase')
        subdomain: Desired subdomain (e.g., 'supabase')
        app_uuid: Coolify application UUID
        port: Local port the service runs on
    """
    results = {
        "service": service_name,
        "subdomain": subdomain,
        "steps": [],
        "errors": []
    }
    
    full_domain = f"{subdomain}.{BASE_DOMAIN}"
    
    try:
        # Step 1: Create DNS record
        dns_result = await create_dns_record(subdomain)
        if dns_result.get("success"):
            results["steps"].append(f"✅ Created DNS record: {full_domain}")
        else:
            results["errors"].append(f"❌ DNS creation failed: {dns_result.get('error')}")
        
        # Step 2: Update application environment if needed
        try:
            env_vars = await get_application_environment(app_uuid)
            updated_env = {}
            
            # Replace localhost references with the new domain
            for key, value in env_vars.get("data", {}).items():
                if isinstance(value, str):
                    if "localhost:8000" in value:
                        updated_env[key] = value.replace("localhost:8000", f"https://{full_domain}")
                    elif "http://localhost" in value:
                        updated_env[key] = value.replace("http://localhost", f"https://{full_domain}")
            
            if updated_env:
                update_result = await update_application_environment(app_uuid, updated_env)
                results["steps"].append(f"✅ Updated {len(updated_env)} environment variables")
                results["updated_vars"] = updated_env
        except Exception as e:
            results["errors"].append(f"❌ Environment update failed: {str(e)}")
        
        # Step 3: Trigger deployment
        try:
            deploy_result = await deploy_application(app_uuid)
            if not deploy_result.get("error"):
                results["steps"].append("✅ Triggered application deployment")
            else:
                results["errors"].append(f"❌ Deployment failed: {deploy_result.get('message')}")
        except Exception as e:
            results["errors"].append(f"❌ Deployment trigger failed: {str(e)}")
        
        # Summary
        results["success"] = len(results["errors"]) == 0
        results["summary"] = f"""
🚀 {service_name} Deployment Summary:
📍 Domain: https://{full_domain}
🔗 Coolify App: {app_uuid}
⚡ Port: {port}

{len(results['steps'])} steps completed
{len(results['errors'])} errors occurred

{'✅ FULLY AUTOMATED!' if results['success'] else '⚠️  Manual intervention needed'}

Next: Add this to your tunnel config:
  - hostname: {full_domain}
    service: http://localhost:{port}
        """
        
        return results
        
    except Exception as e:
        results["errors"].append(f"❌ Automation failed: {str(e)}")
        results["success"] = False
        return results

# ==================== DIAGNOSTIC TOOLS ====================

@app.tool()
async def diagnose_tunnel_issues(app_uuid: str) -> Dict:
    """Diagnose common CloudFlare tunnel vs localhost issues
    
    Args:
        app_uuid: The UUID of the application to diagnose
    """
    issues = []
    recommendations = []
    
    # Get application details and environment
    app_details = await get_application_details(app_uuid)
    env_vars = await get_application_environment(app_uuid)
    
    if "data" in env_vars:
        env_data = env_vars["data"]
        
        # Check for localhost references
        localhost_refs = []
        for key, value in env_data.items():
            if isinstance(value, str) and ("localhost" in value or "127.0.0.1" in value):
                localhost_refs.append(f"{key}: {value}")
        
        if localhost_refs:
            issues.append("🚨 Found localhost references in environment variables")
            recommendations.append("Replace localhost URLs with your tunnel domain (e.g., https://cloud.therink.io)")
            recommendations.append(f"Affected variables: {', '.join([ref.split(':')[0] for ref in localhost_refs])}")
    
    # Check application status
    if "data" in app_details:
        status = app_details["data"].get("status", "unknown")
        if status != "running":
            issues.append(f"⚠️  Application is not running (status: {status})")
            recommendations.append("Deploy or restart the application")
    
    return {
        "issues": issues,
        "recommendations": recommendations,
        "has_issues": len(issues) > 0
    }

# Main entry point
if __name__ == "__main__":
    import sys
    app.run(transport="stdio")