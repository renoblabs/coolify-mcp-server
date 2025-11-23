#!/usr/bin/env python3
"""
Test FastMCP basic functionality
"""

import asyncio
from fastmcp import FastMCP

# Create a simple FastMCP app
app = FastMCP("test-server")

@app.tool()
def test_tool() -> str:
    """A simple test tool"""
    return "Hello from test tool!"

async def test_basic():
    print("Testing FastMCP basic functionality...")
    
    # Check available attributes
    print(f"FastMCP attributes: {[attr for attr in dir(app) if not attr.startswith('_')]}")
    
    # Try to get the HTTP app
    http_app = getattr(app, 'http_app', None)
    if http_app:
        print("✅ http_app found")
    else:
        print("❌ http_app not found")
    
    # Try to get the SSE app
    sse_app = getattr(app, 'sse_app', None)
    if sse_app:
        print("✅ sse_app found")
    else:
        print("❌ sse_app not found")
    
    # Try to get streamable HTTP app
    streamable_app = getattr(app, 'streamable_http_app', None)
    if streamable_app:
        print("✅ streamable_http_app found")
    else:
        print("❌ streamable_http_app not found")

if __name__ == "__main__":
    asyncio.run(test_basic())