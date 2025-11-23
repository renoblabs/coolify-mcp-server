#!/usr/bin/env python3
"""
Consolidated MCP Server Test Suite
Tests both HTTP/JSON-RPC and SSE transports
"""

import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MCP_HOST = "localhost"
MCP_PORT = int(os.getenv("MCP_PORT", "8765"))
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN")
BASE_URL = f"http://{MCP_HOST}:{MCP_PORT}"


async def test_http_transport():
    """Test MCP server with HTTP/JSON-RPC transport"""
    print("\n🧪 Testing HTTP/JSON-RPC Transport")
    print("=" * 60)

    headers = {
        "Authorization": f"Bearer {MCP_AUTH_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            # Test 1: List tools
            print("1. Testing tools/list...")
            tools_message = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            }

            response = await client.post(
                f"{BASE_URL}/mcp/",
                headers=headers,
                json=tools_message,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if "result" in data and "tools" in data["result"]:
                    tools = data["result"]["tools"]
                    print(f"   ✅ Found {len(tools)} MCP tools")
                    print(f"   Tools: {', '.join([t['name'] for t in tools[:5]])}{'...' if len(tools) > 5 else ''}")
                else:
                    print(f"   ❌ Unexpected response format: {data}")
                    return False
            else:
                print(f"   ❌ Request failed with status {response.status_code}")
                return False

            # Test 2: Execute a tool
            print("\n2. Testing tool execution (get_server_info)...")
            execute_message = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "get_server_info",
                    "arguments": {}
                }
            }

            response = await client.post(
                f"{BASE_URL}/mcp/",
                headers=headers,
                json=execute_message,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if "result" in data:
                    print("   ✅ Tool execution successful")
                    if isinstance(data["result"], dict) and "content" in data["result"]:
                        content = data["result"]["content"]
                        if isinstance(content, list) and len(content) > 0:
                            server_info = content[0].get("text", "")
                            if server_info:
                                try:
                                    server_data = json.loads(server_info)
                                    print(f"   Server: {server_data.get('name', 'Unknown')}")
                                    print(f"   Version: {server_data.get('version', 'Unknown')}")
                                    print(f"   Tools: {server_data.get('tools_available', 'Unknown')}")
                                except:
                                    print(f"   Response: {server_info[:100]}...")
                    return True
                else:
                    print(f"   ❌ Tool execution failed: {data}")
                    return False
            else:
                print(f"   ❌ Request failed with status {response.status_code}")
                return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


async def test_sse_transport():
    """Test MCP server with SSE transport"""
    print("\n🧪 Testing SSE Transport")
    print("=" * 60)

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
                    return False

                # Read the first event to get the session endpoint
                session_endpoint = None
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        session_endpoint = line[6:]  # Remove "data: " prefix
                        break

                if not session_endpoint:
                    print("   ❌ No session endpoint received")
                    return False

                print(f"   ✅ Session endpoint: {session_endpoint}")

                # Step 2: Test MCP tools/list on the session endpoint
                print("\n2. Testing tools/list...")
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

                if tools_response.status_code == 202:
                    print("   ✅ Request accepted (SSE mode)")
                    print("   💡 Responses will be delivered via SSE stream")
                    return True
                elif tools_response.status_code == 200:
                    tools_data = tools_response.json()
                    if "result" in tools_data and "tools" in tools_data["result"]:
                        tools = tools_data["result"]["tools"]
                        print(f"   ✅ Found {len(tools)} tools:")
                        for tool in tools[:5]:  # Show first 5 tools
                            print(f"      - {tool.get('name', 'Unknown')}")
                        if len(tools) > 5:
                            print(f"      ... and {len(tools) - 5} more")
                        return True
                    else:
                        print(f"   ❌ Unexpected response format: {tools_data}")
                        return False
                else:
                    print(f"   ❌ Tools request failed: {tools_response.status_code}")
                    print(f"      Response: {tools_response.text}")
                    return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


async def main():
    print("🚀 Coolify MCP Server Test Suite")
    print("=" * 60)
    print(f"Server: {BASE_URL}")
    print(f"Auth Token: {MCP_AUTH_TOKEN[:10]}..." if MCP_AUTH_TOKEN else "❌ No auth token!")
    print()

    if not MCP_AUTH_TOKEN:
        print("❌ MCP_AUTH_TOKEN not set in .env file!")
        return

    # Test HTTP transport
    http_ok = await test_http_transport()

    # Test SSE transport
    sse_ok = await test_sse_transport()

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   HTTP/JSON-RPC: {'✅ PASS' if http_ok else '❌ FAIL'}")
    print(f"   SSE Transport: {'✅ PASS' if sse_ok else '❌ FAIL'}")

    if http_ok and sse_ok:
        print("\n🎉 All tests passed! Server is working correctly.")
        print("\nNext steps:")
        print("1. Configure your MCP client with:")
        print(f"   - HTTP: {BASE_URL}/mcp/")
        print(f"   - SSE:  {BASE_URL}/sse")
        print(f"2. Use auth token: {MCP_AUTH_TOKEN}")
    else:
        print("\n⚠️  Some tests failed. Check server logs.")


if __name__ == "__main__":
    asyncio.run(main())
