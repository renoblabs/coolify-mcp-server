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
import logging
import sys
import signal
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.requests import Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("coolify-mcp-server")

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
    logger.warning("=" * 80)
    logger.warning("🔐 GENERATED NEW MCP AUTH TOKEN (SAVE THIS!):")
    logger.warning(f"   {MCP_AUTH_TOKEN}")
    logger.warning("=" * 80)
    logger.warning(f"Save with: doppler secrets set MCP_AUTH_TOKEN=\"{MCP_AUTH_TOKEN}\"")
    logger.warning("=" * 80)

# Optional: Support for switching between local and tunnel URLs
if os.getenv("USE_TUNNEL", "false").lower() == "true":
    COOLIFY_BASE_URL = os.getenv("COOLIFY_TUNNEL_URL", "https://cloud.therink.io")

async def make_coolify_request(method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
    """Make authenticated request to Coolify API with proper error handling"""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    if not API_TOKEN:
        error_msg = "COOLIFY_API_TOKEN not configured"
        logger.error(error_msg)
        return {"error": error_msg, "success": False}

    headers["Authorization"] = f"Bearer {API_TOKEN}"
    url = f"{COOLIFY_BASE_URL}/api/v1{endpoint}"

    async with httpx.AsyncClient() as client:
        try:
            logger.debug(f"{method} {url}")
            response = await client.request(method, url, headers=headers, json=data, timeout=30)

            # Handle different response status codes
            if response.status_code >= 400:
                error_msg = f"Coolify API error: {response.status_code}"
                logger.error(f"{error_msg} - {response.text[:200]}")
                return {
                    "error": error_msg,
                    "status_code": response.status_code,
                    "success": False,
                    "details": response.text[:500] if response.text else None
                }

            # Parse JSON response
            if response.text:
                try:
                    return response.json()
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON response from Coolify: {e}")
                    return {"error": "Invalid JSON response", "success": False}

            return {"success": True}

        except httpx.TimeoutException as e:
            error_msg = f"Coolify API timeout after 30s"
            logger.error(error_msg)
            return {"error": error_msg, "success": False}
        except httpx.ConnectError as e:
            error_msg = f"Cannot connect to Coolify at {COOLIFY_BASE_URL}"
            logger.error(f"{error_msg}: {str(e)}")
            return {"error": error_msg, "success": False}
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.exception(f"Error in Coolify request: {e}")
            return {"error": error_msg, "success": False}

# ==================== AUTHENTICATION ====================

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce Bearer token authentication for HTTP/SSE endpoints"""

    async def dispatch(self, request: Request, call_next):
        # Skip auth for health check endpoint
        if request.url.path in ["/health", "/healthz"]:
            return await call_next(request)

        # Skip auth if no token configured (development mode)
        if not MCP_AUTH_TOKEN:
            logger.warning("⚠️  No MCP_AUTH_TOKEN configured - running in INSECURE mode!")
            return await call_next(request)

        # Extract Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            logger.warning(f"Authentication failed: No Authorization header from {request.client.host}")
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Authentication required",
                    "message": "Missing Authorization header. Use: Authorization: Bearer YOUR_TOKEN"
                }
            )

        # Verify Bearer token format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            logger.warning(f"Authentication failed: Invalid format from {request.client.host}")
            return JSONResponse(
                status_code=401,
                content={
                    "error": "Invalid authentication format",
                    "message": "Use: Authorization: Bearer YOUR_TOKEN"
                }
            )

        token = parts[1]

        # Verify token
        if token != MCP_AUTH_TOKEN:
            logger.warning(f"Authentication failed: Invalid token from {request.client.host}")
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Authentication failed",
                    "message": "Invalid authentication token"
                }
            )

        # Token valid, proceed with request
        logger.debug(f"✓ Authenticated request from {request.client.host}")
        return await call_next(request)

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
    # Get existing environment variables
    existing = await make_coolify_request("GET", f"/applications/{app_uuid}/environment")

    # Handle errors from fetching existing vars
    if "error" in existing:
        logger.error(f"Failed to fetch existing env vars for {app_uuid}: {existing.get('error')}")
        return existing

    # Merge with existing variables if present
    if "data" in existing and isinstance(existing["data"], dict):
        current_vars = existing["data"].copy()
        current_vars.update(env_vars)
        env_vars = current_vars
        logger.debug(f"Merged {len(env_vars)} environment variables")
    else:
        logger.warning(f"No existing env vars found, creating new set")

    # Update the environment variables
    result = await make_coolify_request(
        "PUT",
        f"/applications/{app_uuid}/environment",
        {"environment": env_vars}
    )

    if "error" not in result:
        logger.info(f"Successfully updated environment for {app_uuid}")

    return result

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
        logger.error(f"Failed to get server resources for {server_uuid}: {server_info.get('error')}")
        return server_info

    # Validate response structure
    if "data" not in server_info or not isinstance(server_info["data"], dict):
        error_msg = "Invalid server response format"
        logger.error(f"{error_msg}: {server_info}")
        return {"error": error_msg, "success": False}

    data = server_info["data"]

    # Extract resource information with validation
    resources = {
        "server_uuid": server_uuid,
        "server_name": data.get("name", "Unknown"),
        "status": data.get("status", "unknown"),
        "resources": data.get("resources", {}),
        "available": data.get("status") == "reachable"
    }

    logger.debug(f"Retrieved resources for {resources['server_name']}: {resources['status']}")
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

# ==================== GRACEFUL SHUTDOWN ====================

shutdown_event = asyncio.Event()

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_event.set()

# ==================== MAIN ENTRY POINT ====================

if __name__ == "__main__":
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Coolify MCP Server")
    parser.add_argument(
        "--mode",
        choices=["stdio", "http", "sse"],
        default="http",
        help="Transport mode: stdio (local IPC), http/sse (remote access)"
    )
    parser.add_argument(
        "--host",
        default=MCP_HOST,
        help=f"Host to bind to (default: {MCP_HOST})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=MCP_PORT,
        help=f"Port to bind to (default: {MCP_PORT})"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )

    args = parser.parse_args()

    # Update logging level if debug mode
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Display startup information
    auth_status = "✅ Enabled" if MCP_AUTH_TOKEN else "⚠️  DISABLED (INSECURE)"

    if args.mode == "stdio":
        # STDIO mode for local IDEs (Claude Desktop, Factory Bridge)
        logger.info("=" * 80)
        logger.info("🚀 Coolify MCP Server - STDIO MODE")
        logger.info("=" * 80)
        logger.info("Transport: Standard Input/Output (JSON-RPC)")
        logger.info("Use case: Local IDE integration (Claude Desktop, Factory Bridge)")
        logger.info(f"Auth: {auth_status}")
        logger.info("=" * 80)

        try:
            app.run()
        except KeyboardInterrupt:
            logger.info("Shutdown requested, exiting...")
        except Exception as e:
            logger.exception(f"Fatal error in STDIO mode: {e}")
            sys.exit(1)

    else:
        # HTTP/SSE mode for remote access
        logger.info("=" * 80)
        logger.info("🚀 Coolify MCP Server - HTTP/SSE MODE")
        logger.info("=" * 80)
        logger.info(f"Host: {args.host}")
        logger.info(f"Port: {args.port}")
        logger.info(f"Auth: {auth_status}")
        logger.info(f"Local URL: http://localhost:{args.port}")
        logger.info(f"Health Check: http://localhost:{args.port}/health")
        logger.info("=" * 80)
        logger.info("📱 Use case: Mobile AI apps, remote access, web integrations")
        logger.info("🔧 Tools available: 18 (Coolify + Cloudflare + Multi-server)")
        logger.info("=" * 80)

        async def run_server():
            """Run the HTTP server with authentication middleware"""
            try:
                logger.info("🔐 Authentication middleware: " + ("Enabled" if MCP_AUTH_TOKEN else "Disabled"))

                # Prepare middleware in Starlette format: (class, args, kwargs)
                middleware_list = []
                if MCP_AUTH_TOKEN:
                    middleware_list.append((AuthMiddleware, [], {}))

                # Run HTTP server with authentication middleware
                # FastMCP 2.x supports middleware parameter
                await app.run_http_async(
                    host=args.host,
                    port=args.port,
                    transport="sse",  # Use SSE transport for MCP protocol
                    middleware=middleware_list,
                    show_banner=False  # We already showed our custom banner
                )
            except KeyboardInterrupt:
                logger.info("Shutdown requested, exiting...")
            except Exception as e:
                logger.exception(f"Fatal error in HTTP mode: {e}")
                raise

        try:
            asyncio.run(run_server())
        except KeyboardInterrupt:
            logger.info("Shutdown complete")
        except Exception as e:
            logger.exception(f"Server failed: {e}")
            sys.exit(1)
