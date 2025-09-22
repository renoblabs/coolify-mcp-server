#!/usr/bin/env python3
"""
Coolify MCP Server - AI Assistant for Coolify Management
Provides tools for managing Coolify applications, deployments, and configurations
"""

from fastmcp import FastMCP
import httpx
import json
import os
from typing import Dict, List, Optional, Any
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastMCP("Coolify Assistant")

# Configuration - using Doppler for secrets
COOLIFY_BASE_URL = os.getenv("COOLIFY_BASE_URL", "http://localhost:8000")
API_TOKEN = os.getenv("COOLIFY_API_TOKEN")

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
        if method.upper() == "GET":
            response = await client.get(url, headers=headers)
        elif method.upper() == "POST":
            response = await client.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = await client.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    
    if response.status_code >= 400:
        return {
            "error": True,
            "status_code": response.status_code,
            "message": response.text
        }
    
    try:
        return response.json()
    except:
        return {"data": response.text}

@app.tool()
async def get_applications() -> Dict:
    """Get all applications from Coolify"""
    return await make_coolify_request("GET", "/applications")

@app.tool()
async def get_application(app_uuid: str) -> Dict:
    """Get specific application details by UUID"""
    return await make_coolify_request("GET", f"/applications/{app_uuid}")

@app.tool()
async def get_application_logs(app_uuid: str, lines: int = 100) -> Dict:
    """Get recent logs for a Coolify application"""
    return await make_coolify_request("GET", f"/applications/{app_uuid}/logs?lines={lines}")

@app.tool()
async def deploy_application(app_uuid: str) -> Dict:
    """Deploy/redeploy a Coolify application"""
    return await make_coolify_request("POST", f"/applications/{app_uuid}/deploy")

@app.tool()
async def diagnose_tunnel_issues(app_uuid: str) -> Dict:
    """Diagnose common Cloudflare tunnel vs localhost issues
    
    Args:
        app_uuid: Application UUID to diagnose
    """
    # Get app details and environment
    app_details = await get_application(app_uuid)
    app_env = await get_application_environment(app_uuid)
    app_logs = await get_application_logs(app_uuid, 50)
    
    issues = []
    suggestions = []
    
    # Common issues to check for:
    # 1. Hardcoded localhost URLs
    # 2. HTTP vs HTTPS mismatches  
    # 3. CORS configuration
    # 4. Base URL configuration
    
    if "localhost" in str(app_env).lower():
        issues.append("Found localhost references in environment variables")
        suggestions.append("Update environment variables to use your CF tunnel domain")
    
    if "8000" in str(app_env):
        issues.append("Found port 8000 references (likely localhost:8000)")
        suggestions.append("Replace localhost:8000 with cloud.therink.io")
    
    return {
        "application": app_details.get("name", app_uuid),
        "issues_found": issues,
        "suggestions": suggestions,
        "environment_variables": app_env,
        "recent_logs": app_logs
    }

@app.tool()
async def get_application_environment(app_uuid: str) -> Dict:
    """Get environment variables for an application"""
    return await make_coolify_request("GET", f"/applications/{app_uuid}/environment")

@app.tool()
async def update_application_environment(app_uuid: str, environment_variables: Dict[str, str]) -> Dict:
    """Update environment variables for an application"""
    data = {"environment_variables": environment_variables}
    return await make_coolify_request("PUT", f"/applications/{app_uuid}/environment", data)

@app.tool()
async def configure_service_subdomain(service_name: str, subdomain: str, 
                                    base_domain: str = "therink.io") -> Dict:
    """Helper to configure a service with a proper subdomain"""
    full_domain = f"{subdomain}.{base_domain}"
    
    return {
        "message": f"Configuration helper for {service_name} on {full_domain}",
        "suggested_domain": full_domain,
        "next_steps": [
            f"Update service domains to include {full_domain}",
            f"Ensure Cloudflare tunnel routes {subdomain}.{base_domain} correctly",
            "Update any internal service URLs to use the new domain",
            "Test external access via the tunnel"
        ]
    }

if __name__ == "__main__":
    app.run()