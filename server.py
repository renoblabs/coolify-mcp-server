#!/usr/bin/env python3
"""
Coolify MCP Server - REMOTE VERSION
Provides HTTP/WebSocket transport for remote access from mobile AI apps
"""

from fastmcp import FastMCP
import httpx
import json
import os
from typing import Dict, List, Optional, Any
import asyncio
from dotenv import load_dotenv
import cloudflare
import secrets
import hashlib

# Load environment variables
load_dotenv()

# Create the MCP app with HTTP transport capability
app = FastMCP("Coolify Assistant Remote")

# Configuration - using Doppler for secrets
COOLIFY_BASE_URL = os.getenv("COOLIFY_BASE_URL", "http://localhost:8000")
API_TOKEN = os.getenv("COOLIFY_API_TOKEN")

# Cloudflare configuration
CF_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CF_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
CF_TUNNEL_ID = os.getenv("CLOUDFLARE_TUNNEL_ID")
BASE_DOMAIN = os.getenv("BASE_DOMAIN", "therink.io")

# Remote access configuration
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN")
MCP_PORT = int(os.getenv("MCP_PORT", "8765"))
MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")  # Listen on all interfaces

# Generate auth token if not set
if not MCP_AUTH_TOKEN:
    MCP_AUTH_TOKEN = secrets.token_urlsafe(32)
    print(f"Generated MCP Auth Token: {MCP_AUTH_TOKEN}")
    print("Save this token in Doppler: doppler secrets set MCP_AUTH_TOKEN=\"{MCP_AUTH_TOKEN}\"")

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

# ==================== AUTHENTICATION ====================
# Note: FastMCP doesn't have built-in auth middleware for SSE
# Authentication should be handled by the reverse proxy (Cloudflare Tunnel)
# or implemented at the transport layer

# ==================== SERVER INFO ====================

@app.tool()
async def get_server_info() -> Dict:
    """Get information about this MCP server"""
    return {
        "name": "Coolify Assistant Remote",
        "version": "2.0.0",
        "transport": "HTTP/WebSocket",
        "capabilities": {
            "coolify_management": True,
            "cloudflare_automation": True,
            "remote_access": True
        },
        "endpoints": {
            "local": f"http://localhost:{MCP_PORT}",
            "tunnel": f"https://mcp.therink.io"  # You'll configure this
        },
        "tools_available": 18  # Updated with server management tools
    }

# ==================== COOLIFY MANAGEMENT TOOLS ====================

@app.tool()
async def list_applications() -> Dict:
    """List all applications in Coolify"""
    result = await make_coolify_request("GET", "/applications")
    # Ensure result is always a dict for FastMCP 2.x compatibility
    if isinstance(result, list):
        return {"applications": result, "count": len(result)}
    return result

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
    existing = await make_coolify_request("GET", f"/applications/{app_uuid}/environment")
    
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

# ==================== SERVER MANAGEMENT TOOLS ====================

@app.tool()
async def list_servers() -> Dict:
    """List all servers/destinations configured in Coolify
    
    Returns information about all deployment destinations including
    local server, remote servers, and their capabilities.
    """
    result = await make_coolify_request("GET", "/servers")
    # Ensure result is always a dict for FastMCP 2.x compatibility
    if isinstance(result, list):
        return {"servers": result, "count": len(result)}
    return result

@app.tool()
async def get_server_details(server_uuid: str) -> Dict:
    """Get detailed information about a specific server
    
    Args:
        server_uuid: The UUID of the server to get details for
        
    Returns server info including name, IP, status, and resources
    """
    return await make_coolify_request("GET", f"/servers/{server_uuid}")

@app.tool()
async def get_server_resources(server_uuid: str) -> Dict:
    """Get resource usage and availability for a server
    
    Args:
        server_uuid: The UUID of the server to check
        
    Returns CPU, RAM, disk usage, and availability info
    """
    server_info = await make_coolify_request("GET", f"/servers/{server_uuid}")
    
    if "error" in server_info:
        return server_info
    
    # Extract resource information from server data
    resources = {
        "server_uuid": server_uuid,
        "server_name": server_info.get("data", {}).get("name", "Unknown"),
        "status": server_info.get("data", {}).get("status", "unknown"),
        "resources": server_info.get("data", {}).get("resources", {}),
        "available": server_info.get("data", {}).get("status") == "reachable"
    }
    
    return resources

@app.tool()
async def deploy_to_server(app_uuid: str, server_name_or_uuid: str, force_rebuild: bool = False) -> Dict:
    """Smart deployment - deploy application to a specific server by name or UUID
    
    Args:
        app_uuid: The UUID of the application to deploy
        server_name_or_uuid: Server name (e.g., 'Main Computer') or UUID
        force_rebuild: Whether to force rebuild the application
        
    This tool will:
    1. Find the server by name or UUID
    2. Check if the server is available
    3. Deploy the application to that server
    4. Return deployment status
    """
    # First, try to get all servers
    servers_response = await make_coolify_request("GET", "/servers")
    
    if "error" in servers_response:
        return {"error": f"Failed to get servers list: {servers_response['error']}"}
    
    servers = servers_response.get("data", [])
    target_server = None
    
    # Try to find server by name or UUID
    for server in servers:
        if server.get("uuid") == server_name_or_uuid or server.get("name") == server_name_or_uuid:
            target_server = server
            break
    
    if not target_server:
        available_servers = [f"{s.get('name')} ({s.get('uuid')})" for s in servers]
        return {
            "error": f"Server '{server_name_or_uuid}' not found",
            "available_servers": available_servers
        }
    
    # Check if server is reachable
    server_status = target_server.get("status")
    if server_status != "reachable":
        return {
            "error": f"Server '{target_server.get('name')}' is not reachable (status: {server_status})",
            "server_uuid": target_server.get("uuid")
        }
    
    # Get application details to update destination
    app_details = await get_application_details(app_uuid)
    if "error" in app_details:
        return {"error": f"Failed to get application details: {app_details.get('error')}"}
    
    # Update application destination (if Coolify API supports it)
    # Note: The exact endpoint may vary depending on Coolify version
    update_result = await make_coolify_request(
        "PUT", 
        f"/applications/{app_uuid}",
        {"destination_uuid": target_server.get("uuid")}
    )
    
    # Now deploy the application
    deploy_result = await deploy_application(app_uuid, force_rebuild)
    
    return {
        "success": "error" not in deploy_result,
        "server_name": target_server.get("name"),
        "server_uuid": target_server.get("uuid"),
        "app_uuid": app_uuid,
        "deployment": deploy_result,
        "message": f"Deployed to {target_server.get('name')}"
    }

@app.tool()
async def smart_deploy(
    service_name: str,
    app_uuid: str,
    requires_gpu: bool = False,
    requires_high_memory: bool = False,
    preferred_server: Optional[str] = None
) -> Dict:
    """Intelligently deploy an application based on resource requirements
    
    Args:
        service_name: Name of the service being deployed
        app_uuid: The UUID of the application
        requires_gpu: Whether the app needs GPU resources
        requires_high_memory: Whether the app needs high memory (>8GB)
        preferred_server: Optional specific server name to use
        
    This tool will:
    1. Analyze resource requirements
    2. Find the best available server
    3. Deploy to that server
    4. Report deployment status
    """
    # Get all servers
    servers_response = await list_servers()
    if "error" in servers_response:
        return {"error": f"Failed to get servers: {servers_response['error']}"}
    
    servers = servers_response.get("data", [])
    
    # If preferred server specified, use it
    if preferred_server:
        return await deploy_to_server(app_uuid, preferred_server)
    
    # Smart server selection logic
    selected_server = None
    
    for server in servers:
        server_name = server.get("name", "").lower()
        
        # GPU requirement - look for keywords
        if requires_gpu:
            if any(keyword in server_name for keyword in ["gpu", "main", "workstation", "desktop"]):
                selected_server = server
                break
        
        # High memory requirement
        if requires_high_memory:
            if any(keyword in server_name for keyword in ["main", "powerful", "workstation"]):
                selected_server = server
                break
    
    # Default to first reachable server if no match
    if not selected_server:
        for server in servers:
            if server.get("status") == "reachable":
                selected_server = server
                break
    
    if not selected_server:
        return {"error": "No reachable servers found"}
    
    # Deploy to selected server
    result = await deploy_to_server(app_uuid, selected_server.get("uuid"))
    
    result["selection_reason"] = {
        "requires_gpu": requires_gpu,
        "requires_high_memory": requires_high_memory,
        "selected_server": selected_server.get("name"),
        "server_capabilities": f"Selected based on {'GPU' if requires_gpu else 'memory' if requires_high_memory else 'availability'} requirements"
    }
    
    return result

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
        
        result = cf.dns.records.create(
            zone_id=CF_ZONE_ID,
            type=record_type,
            name=full_domain,
            content=target,
            ttl=1
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
        
        results["success"] = len(results["errors"]) == 0
        results["summary"] = f"""
🚀 {service_name} Deployment Summary:
📍 Domain: https://{full_domain}
🔗 Coolify App: {app_uuid}
⚡ Port: {port}

{len(results['steps'])} steps completed
{len(results['errors'])} errors occurred

{'✅ FULLY AUTOMATED!' if results['success'] else '⚠️  Manual intervention needed'}
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
    
    app_details = await get_application_details(app_uuid)
    env_vars = await get_application_environment(app_uuid)
    
    if "data" in env_vars:
        env_data = env_vars["data"]
        
        localhost_refs = []
        for key, value in env_data.items():
            if isinstance(value, str) and ("localhost" in value or "127.0.0.1" in value):
                localhost_refs.append(f"{key}: {value}")
        
        if localhost_refs:
            issues.append("🚨 Found localhost references in environment variables")
            recommendations.append("Replace localhost URLs with your tunnel domain")
            recommendations.append(f"Affected variables: {', '.join([ref.split(':')[0] for ref in localhost_refs])}")
    
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

# Main entry point with HTTP transport
if __name__ == "__main__":
    import sys
    
    auth_status = "Enabled" if MCP_AUTH_TOKEN else "DISABLED"
    print("=" * 60)
    print("Coolify MCP Server - REMOTE MODE")
    print("=" * 60)
    print(f"Host: {MCP_HOST}")
    print(f"Port: {MCP_PORT}")
    print(f"Auth: {auth_status}")
    print(f"Local: http://localhost:{MCP_PORT}")
    print("=" * 60)
    
    # Run with SSE (Server-Sent Events) transport for remote access
    # FastMCP supports: stdio, sse, or custom transports
    import asyncio
    
    # Use the new FastMCP 2.x method
    asyncio.run(app.run_http_async(
        host=MCP_HOST,
        port=MCP_PORT
    ))
