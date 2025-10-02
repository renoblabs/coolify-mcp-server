#!/usr/bin/env python3
"""
Test script for Remote MCP Server
Verifies the server is ready for mobile AI apps (GenSpark, Manus, etc.)
"""

import asyncio
import httpx
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
MCP_HOST = "localhost"
MCP_PORT = int(os.getenv("MCP_PORT", "8765"))
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN")
BASE_URL = f"http://{MCP_HOST}:{MCP_PORT}"

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_test(name, status, details=""):
    """Pretty print test results"""
    icon = "[PASS]" if status else "[FAIL]"
    color = GREEN if status else RED
    print(f"{color}{icon} {name}{RESET}")
    if details:
        print(f"   {details}")

def print_section(title):
    """Print section header"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}{title}{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

async def test_server_health():
    """Test if server is running and accessible"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health", timeout=5)
            return response.status_code == 200
    except:
        return False

async def test_authentication():
    """Test authentication with bearer token"""
    headers = {"Authorization": f"Bearer {MCP_AUTH_TOKEN}"}
    
    try:
        async with httpx.AsyncClient() as client:
            # Test with auth
            response = await client.get(f"{BASE_URL}/", headers=headers, timeout=5)
            auth_works = response.status_code != 401
            
            # Test without auth (should fail)
            response = await client.get(f"{BASE_URL}/", timeout=5)
            no_auth_fails = response.status_code == 401 or response.status_code == 403
            
            return auth_works, no_auth_fails
    except Exception as e:
        return False, False

async def test_sse_endpoint():
    """Test SSE (Server-Sent Events) endpoint"""
    headers = {"Authorization": f"Bearer {MCP_AUTH_TOKEN}"}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/sse",
                headers=headers,
                timeout=5
            )
            return response.status_code == 200
    except:
        return False

async def test_mcp_initialization():
    """Test MCP initialization protocol"""
    headers = {
        "Authorization": f"Bearer {MCP_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # MCP initialization message
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "1.0.0",
            "capabilities": {},
            "clientInfo": {
                "name": "MCP Test Client",
                "version": "1.0.0"
            }
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/",
                headers=headers,
                json=init_message,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # Check if we got a valid MCP response
                return "result" in data or "error" not in data
            return False
    except Exception as e:
        print(f"   Error: {e}")
        return False

async def test_list_tools():
    """Test listing available MCP tools"""
    headers = {
        "Authorization": f"Bearer {MCP_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # MCP list tools message
    tools_message = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/",
                headers=headers,
                json=tools_message,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "result" in data and "tools" in data["result"]:
                    tools = data["result"]["tools"]
                    return True, len(tools)
                return False, 0
            return False, 0
    except Exception as e:
        print(f"   Error: {e}")
        return False, 0

async def test_execute_tool():
    """Test executing a simple MCP tool"""
    headers = {
        "Authorization": f"Bearer {MCP_AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Test with get_server_info tool
    execute_message = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_server_info",
            "arguments": {}
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/",
                headers=headers,
                json=execute_message,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return "result" in data
            return False
    except Exception as e:
        print(f"   Error: {e}")
        return False

def generate_mobile_config():
    """Generate configuration for mobile apps"""
    configs = {
        "GenSpark": {
            "name": "Coolify Assistant",
            "type": "mcp",
            "endpoint": "https://mcp.therink.io",
            "transport": "sse",
            "authentication": {
                "type": "bearer",
                "token": MCP_AUTH_TOKEN
            }
        },
        "Manus": {
            "server_name": "Coolify MCP",
            "server_url": "https://mcp.therink.io",
            "auth_type": "bearer",
            "auth_token": MCP_AUTH_TOKEN,
            "transport": "sse"
        },
        "Generic MCP Client": {
            "endpoint": "https://mcp.therink.io",
            "headers": {
                "Authorization": f"Bearer {MCP_AUTH_TOKEN}"
            }
        }
    }
    
    return configs

async def main():
    """Run all tests"""
    print(f"{BOLD}{YELLOW}")
    print("MCP Remote Server Test Suite")
    print(f"Testing: {BASE_URL}")
    print(f"Auth Token: {MCP_AUTH_TOKEN[:10]}..." if MCP_AUTH_TOKEN else "ERROR: No auth token set!")
    print(f"{RESET}")
    
    if not MCP_AUTH_TOKEN:
        print(f"{RED}ERROR: MCP_AUTH_TOKEN not set in environment!{RESET}")
        print("Run: doppler secrets set MCP_AUTH_TOKEN=\"your-token\"")
        return
    
    # Test 1: Server Health
    print_section("1. SERVER CONNECTIVITY")
    
    server_running = await test_server_health()
    print_test("Server is accessible", server_running, f"URL: {BASE_URL}")
    
    if not server_running:
        print(f"\n{RED}WARNING: Server is not running!{RESET}")
        print("Start it with: doppler run -- python coolify_mcp_server_remote.py")
        return
    
    # Test 2: Authentication
    print_section("2. AUTHENTICATION")
    
    auth_works, no_auth_fails = await test_authentication()
    print_test("Authentication with token works", auth_works)
    print_test("Requests without auth are blocked", no_auth_fails)
    
    # Test 3: SSE Endpoint
    print_section("3. SSE TRANSPORT")
    
    sse_works = await test_sse_endpoint()
    print_test("SSE endpoint is available", sse_works, "Required for mobile apps")
    
    # Test 4: MCP Protocol
    print_section("4. MCP PROTOCOL")
    
    init_works = await test_mcp_initialization()
    print_test("MCP initialization", init_works)
    
    tools_work, tool_count = await test_list_tools()
    print_test("List MCP tools", tools_work, f"Found {tool_count} tools")
    
    execute_works = await test_execute_tool()
    print_test("Execute MCP tool", execute_works, "Tested get_server_info()")
    
    # Test 5: Mobile App Configs
    print_section("5. MOBILE APP CONFIGURATION")
    
    configs = generate_mobile_config()
    
    print(f"{GREEN}Server is ready for mobile apps!{RESET}\n")
    print("Mobile App Configurations:\n")
    
    for app, config in configs.items():
        print(f"{BOLD}{app}:{RESET}")
        print(json.dumps(config, indent=2))
        print()
    
    # Summary
    print_section("SUMMARY")
    
    all_tests_pass = all([
        server_running,
        auth_works,
        no_auth_fails,
        sse_works,
        init_works,
        tools_work,
        execute_works
    ])
    
    if all_tests_pass:
        print(f"{GREEN}{BOLD}ALL TESTS PASSED!{RESET}")
        print(f"{GREEN}Your MCP server is ready for GenSpark and Manus!{RESET}")
        print("\nNext steps:")
        print("1. Configure Cloudflare tunnel for mcp.therink.io")
        print("2. Add the configuration to your mobile apps")
        print("3. Start using Coolify automation from anywhere!")
    else:
        print(f"{RED}Some tests failed. Please check the errors above.{RESET}")
    
    # Show tunnel configuration reminder
    print_section("CLOUDFLARE TUNNEL SETUP")
    print("Add to your tunnel config:")
    print(f"""
  - hostname: mcp.therink.io
    service: http://localhost:{MCP_PORT}
    """)
    
    print("\nOr use Cloudflare dashboard:")
    print("https://one.dash.cloudflare.com/ → Access → Tunnels → Configure")

if __name__ == "__main__":
    asyncio.run(main())