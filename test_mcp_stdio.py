#!/usr/bin/env python3
"""Test the MCP server with stdio transport."""

import json
import subprocess
import os

def test_mcp_stdio():
    """Test MCP server with stdio transport."""
    
    # Set environment variables
    env = os.environ.copy()
    env.update({
        'COOLIFY_API_TOKEN': 'dummy-token-for-testing',
        'COOLIFY_BASE_URL': 'https://cloud.therink.io'
    })
    
    # Start the server process
    process = subprocess.Popen(
        ['python', 'server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    
    try:
        # Initialize the MCP session
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {
                        "listChanged": True
                    },
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("Sending initialize request...")
        process.stdin.write(json.dumps(init_request) + '\n')
        process.stdin.flush()
        
        # Read the response
        response_line = process.stdout.readline()
        print(f"Initialize response: {response_line.strip()}")
        
        # Send initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        print("Sending initialized notification...")
        process.stdin.write(json.dumps(initialized_notification) + '\n')
        process.stdin.flush()
        
        # Now test tools/list
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        print("Sending tools/list request...")
        process.stdin.write(json.dumps(tools_request) + '\n')
        process.stdin.flush()
        
        # Read the response
        response_line = process.stdout.readline()
        print(f"Tools response: {response_line.strip()}")
        
        # Parse and display tools
        try:
            response = json.loads(response_line)
            if 'result' in response and 'tools' in response['result']:
                tools = response['result']['tools']
                print(f"\n✅ Found {len(tools)} tools:")
                for tool in tools[:5]:  # Show first 5 tools
                    print(f"  - {tool['name']}: {tool['description']}")
                if len(tools) > 5:
                    print(f"  ... and {len(tools) - 5} more tools")
            else:
                print(f"❌ Unexpected response format: {response}")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse response: {e}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        # Clean up
        process.terminate()
        process.wait()

if __name__ == "__main__":
    test_mcp_stdio()