#!/usr/bin/env python3
"""
Setup helper for Coolify MCP Server
Helps you get your API token and test the connection
"""

import os
import sys
import httpx
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

COOLIFY_URL = "https://cloud.therink.io"

def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step, description):
    print(f"\n{step}. {description}")

async def test_coolify_connection(api_token):
    """Test connection to Coolify API"""
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{COOLIFY_URL}/api/v1/applications", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                app_count = len(data) if isinstance(data, list) else data.get('count', 0)
                print(f"✅ SUCCESS: Connected to Coolify! Found {app_count} applications.")
                return True
            elif response.status_code == 401:
                print("❌ FAILED: Invalid API token (401 Unauthorized)")
                return False
            else:
                print(f"❌ FAILED: HTTP {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ FAILED: Connection error - {e}")
        return False

def main():
    print_header("Coolify MCP Server Setup Helper")
    
    print("This helper will guide you through setting up your Coolify MCP server.")
    print(f"Your Coolify instance: {COOLIFY_URL}")
    
    print_step(1, "Get your Coolify API Token")
    print("   a) Go to https://cloud.therink.io")
    print("   b) Login to your Coolify dashboard")
    print("   c) Go to Settings → Security → API Tokens")
    print("   d) Click 'Create New Token'")
    print("   e) Give it a name like 'MCP Server'")
    print("   f) Copy the generated token")
    
    print_step(2, "Enter your API Token")
    api_token = input("\nPaste your Coolify API token here: ").strip()
    
    if not api_token:
        print("❌ No token provided. Exiting.")
        sys.exit(1)
    
    print_step(3, "Testing connection...")
    success = asyncio.run(test_coolify_connection(api_token))
    
    if success:
        print_step(4, "Updating .env file...")
        
        # Read current .env
        env_path = ".env"
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                content = f.read()
            
            # Replace the API token line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('COOLIFY_API_TOKEN='):
                    lines[i] = f'COOLIFY_API_TOKEN={api_token}'
                    break
            
            # Write back
            with open(env_path, 'w') as f:
                f.write('\n'.join(lines))
            
            print("✅ Updated .env file with your API token")
            
            print_step(5, "Ready to start!")
            print("Your MCP server is now configured. You can start it with:")
            print("   python run_server.py")
            print("\nThe server will run at: http://localhost:8765")
            print(f"MCP Auth Token: {os.getenv('MCP_AUTH_TOKEN', 'DRMRzN0/N8hvgJYhSTKeVET/XFQidMrKj3oJaCewoEc=')}")
            
        else:
            print("❌ .env file not found. Please create it first.")
    else:
        print("\n❌ Setup failed. Please check your API token and try again.")
        print("Make sure you:")
        print("1. Created the token in Coolify Settings → Security → API Tokens")
        print("2. Copied the full token correctly")
        print("3. Your Coolify instance is accessible")

if __name__ == "__main__":
    main()