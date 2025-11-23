#!/usr/bin/env python3
"""
Simple test for Coolify MCP Server with SSE transport
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

async def test_mcp_simple():
    """Simple MCP test"""
    print("🧪 Testing Coolify MCP Server (Simple SSE Test)")
    print("=" * 60)
    print(f"Server: {BASE_URL}/sse")
    print()
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            # Step 1: Get session endpoint
            print("1. Getting session endpoint...")
            headers = {
                "Accept": "text/event-stream",
                "Authorization": f"Bearer {MCP_AUTH_TOKEN}"
            }
            
            response = await client.get(f"{BASE_URL}/sse", headers=headers)
            if response.status_code != 200:
                print(f"   ❌ Failed to connect: {response.status_code}")
                return
            
            # Parse the first line to get session endpoint
            lines = response.text.split('\n')
            session_endpoint = None
            for line in lines:
                if line.startswith("data: "):
                    session_endpoint = line[6:]  # Remove "data: " prefix
                    break
            
            if not session_endpoint:
                print("   ❌ No session endpoint found")
                return
            
            print(f"   ✅ Session endpoint: {session_endpoint}")
            
            # Step 2: Send tools/list request
            print("\n2. Sending tools/list request...")
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
            
            print(f"   Status: {tools_response.status_code}")
            print(f"   Response: {tools_response.text[:200]}...")
            
            if tools_response.status_code == 202:
                print("   ✅ Request accepted (SSE mode)")
                print("   💡 In SSE mode, responses come via the event stream")
                print("   💡 OpenHands should connect to the SSE endpoint to receive responses")
            elif tools_response.status_code == 200:
                try:
                    data = tools_response.json()
                    if "result" in data and "tools" in data["result"]:
                        tools = data["result"]["tools"]
                        print(f"   ✅ Found {len(tools)} tools")
                    else:
                        print(f"   ❌ Unexpected format: {data}")
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response")
            else:
                print(f"   ❌ Request failed")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mcp_simple())