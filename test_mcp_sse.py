#!/usr/bin/env python3
"""
Test Coolify MCP Server with SSE transport
"""

import asyncio
import json
import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MCP_HOST = "localhost"
MCP_PORT = int(os.getenv("MCP_PORT", "8765"))
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN")
BASE_URL = f"http://{MCP_HOST}:{MCP_PORT}"

async def test_mcp_sse():
    """Test MCP SSE transport"""
    print("🧪 Testing Coolify MCP Server (SSE Transport)")
    print("=" * 60)
    print(f"Server: {BASE_URL}/sse")
    print(f"Auth Token: {MCP_AUTH_TOKEN[:10]}...")
    print()
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Step 1: Connect to SSE endpoint to get session
            print("1. Connecting to SSE endpoint...")
            headers = {
                "Accept": "text/event-stream",
                "Authorization": f"Bearer {MCP_AUTH_TOKEN}"
            }
            
            async with client.stream("GET", f"{BASE_URL}/sse", headers=headers) as response:
                if response.status_code != 200:
                    print(f"   ❌ SSE connection failed: {response.status_code}")
                    return
                
                # Read the first event to get the session endpoint
                session_endpoint = None
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        session_endpoint = line[6:]  # Remove "data: " prefix
                        break
                
                if not session_endpoint:
                    print("   ❌ No session endpoint received")
                    return
                
                print(f"   ✅ Session endpoint: {session_endpoint}")
                
                # Step 2: Test MCP tools/list on the session endpoint
                print("\n2. Testing MCP tools/list...")
                session_url = f"{BASE_URL}{session_endpoint}"
                
                mcp_headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {MCP_AUTH_TOKEN}"
                }
                
                tools_message = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list",
                    "params": {}
                }
                
                tools_response = await client.post(
                    session_url,
                    json=tools_message,
                    headers=mcp_headers
                )
                
                if tools_response.status_code in [200, 202]:
                    if tools_response.status_code == 202:
                        print("   ✅ Request accepted, listening for SSE response...")
                        return  # Exit the current stream context
                    else:
                        # Direct JSON response
                        tools_data = tools_response.json()
                        if "result" in tools_data and "tools" in tools_data["result"]:
                            tools = tools_data["result"]["tools"]
                            print(f"   ✅ Found {len(tools)} tools:")
                            for tool in tools[:5]:  # Show first 5 tools
                                print(f"      - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
                            if len(tools) > 5:
                                print(f"      ... and {len(tools) - 5} more")
                        else:
                            print(f"   ❌ Unexpected response format: {tools_data}")
                else:
                    print(f"   ❌ Tools request failed: {tools_response.status_code}")
                    print(f"      Response: {tools_response.text}")
                
                return  # Exit after testing
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_sse())