#!/usr/bin/env python3
"""Test connection to MCP server from Google Antigravity perspective"""
import requests
import json
import sys
import io

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Your configuration from .mcp.json
MCP_URL = "https://mcp.therink.io/sse"
AUTH_TOKEN = "E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo="

print("=" * 70)
print("Testing MCP Server Connection for Google Antigravity")
print("=" * 70)
print(f"URL: {MCP_URL}")
print(f"Auth Token: {AUTH_TOKEN[:20]}...")
print()

# Test 1: Basic connectivity
print("Test 1: Basic HTTP connectivity to server")
try:
    response = requests.get("https://mcp.therink.io/", timeout=10)
    print(f"✅ Server is reachable: {response.status_code}")
    if response.text:
        print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"❌ Server unreachable: {e}")
    exit(1)

print()

# Test 2: SSE endpoint with auth
print("Test 2: SSE endpoint with authentication")
headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Accept": "text/event-stream"
}
try:
    response = requests.get(MCP_URL, headers=headers, timeout=10, stream=True)
    print(f"✅ SSE endpoint accessible: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
    
    # Try to read first event
    print("\n   First events from SSE stream:")
    count = 0
    for line in response.iter_lines(decode_unicode=True):
        if line:
            print(f"   {line[:100]}")
            count += 1
            if count >= 5:
                break
                
except Exception as e:
    print(f"❌ SSE endpoint failed: {e}")

print()

# Test 3: Health check
print("Test 3: Health check endpoint")
try:
    response = requests.get("https://mcp.therink.io/health", timeout=10)
    print(f"✅ Health check: {response.status_code}")
    if response.text:
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"⚠️  Health endpoint: {e}")

print()
print("=" * 70)
print("Connection test complete!")
print()
print("If tests passed, Google Antigravity should be able to connect.")
print("If not, check:")
print("1. Is server.py running on dev box?")
print("2. Is Cloudflare tunnel active?")
print("3. Is firewall allowing connections?")
print("=" * 70)
