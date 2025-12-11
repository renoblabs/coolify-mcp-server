#!/usr/bin/env python3
"""
Interactive GitHub Project Deployment to Coolify
This script helps you deploy GitHub projects to your Coolify instance.
"""
import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Set env vars to match config
os.environ["COOLIFY_BASE_URL"] = "https://cloud.therink.io"
os.environ["COOLIFY_API_TOKEN"] = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"

async def connect_to_mcp():
    """Establish connection to MCP server"""
    server_params = StdioServerParameters(
        command="python",
        args=["c:\\Users\\19057\\CoolifyMCP\\coolify-mcp-server\\server_stdio.py"],
        env=os.environ
    )
    return stdio_client(server_params)

async def list_applications(session):
    """List all existing applications"""
    result = await session.call_tool("list_applications", {})
    return json.loads(result.content[0].text)

async def list_servers(session):
    """List all available servers"""
    result = await session.call_tool("list_servers", {})
    return json.loads(result.content[0].text)

async def deploy_app(session, app_uuid, force_rebuild=False):
    """Deploy an application"""
    result = await session.call_tool("deploy_application", {
        "app_uuid": app_uuid,
        "force_rebuild": force_rebuild
    })
    return json.loads(result.content[0].text)

async def get_app_details(session, app_uuid):
    """Get application details"""
    result = await session.call_tool("get_application_details", {
        "app_uuid": app_uuid
    })
    return json.loads(result.content[0].text)

async def get_app_logs(session, app_uuid, lines=50):
    """Get application logs"""
    result = await session.call_tool("get_application_logs", {
        "app_uuid": app_uuid,
        "lines": lines
    })
    return json.loads(result.content[0].text)

async def main():
    print("=" * 70)
    print("🚀 Coolify GitHub Project Deployment Helper")
    print("=" * 70)
    print()
    
    async with await connect_to_mcp() as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available servers
            print("📡 Checking available deployment servers...")
            servers_data = await list_servers(session)
            servers = servers_data.get("servers", [])
            
            if not servers:
                print("❌ No servers found in Coolify!")
                print("   You need to add a server in Coolify first.")
                return
            
            print(f"✅ Found {len(servers)} server(s):")
            for i, server in enumerate(servers, 1):
                status = server.get("status", "unknown")
                status_icon = "✅" if status == "reachable" else "❌"
                print(f"   {i}. {status_icon} {server.get('name', 'Unknown')} ({server.get('uuid')})")
                print(f"      Status: {status}")
            print()
            
            # List existing applications
            print("📦 Checking existing applications...")
            apps_data = await list_applications(session)
            apps = apps_data.get("applications", [])
            
            if apps:
                print(f"✅ Found {len(apps)} existing application(s):")
                for i, app in enumerate(apps, 1):
                    print(f"   {i}. {app.get('name', 'Unknown')} ({app.get('uuid')})")
                    print(f"      Status: {app.get('status', 'unknown')}")
                print()
                
                # Ask if user wants to deploy existing app
                choice = input("Do you want to deploy an existing app? (y/n): ").strip().lower()
                if choice == 'y':
                    app_num = int(input(f"Enter app number (1-{len(apps)}): ")) - 1
                    if 0 <= app_num < len(apps):
                        selected_app = apps[app_num]
                        app_uuid = selected_app.get("uuid")
                        
                        print(f"\n🔍 Getting details for: {selected_app.get('name')}")
                        details = await get_app_details(session, app_uuid)
                        print(json.dumps(details, indent=2))
                        
                        force = input("\nForce rebuild? (y/n): ").strip().lower() == 'y'
                        
                        print(f"\n🚀 Deploying {selected_app.get('name')}...")
                        deploy_result = await deploy_app(session, app_uuid, force)
                        print(json.dumps(deploy_result, indent=2))
                        
                        print("\n📋 Fetching deployment logs...")
                        await asyncio.sleep(2)  # Wait a bit for logs
                        logs = await get_app_logs(session, app_uuid, 50)
                        print(json.dumps(logs, indent=2))
                        
                        return
            else:
                print("ℹ️  No existing applications found.")
                print()
            
            # Guide for creating new application
            print("=" * 70)
            print("📝 TO DEPLOY A NEW GITHUB PROJECT:")
            print("=" * 70)
            print()
            print("The Coolify API doesn't currently support creating applications via API.")
            print("You need to create the app in the Coolify UI first, then deploy it here.")
            print()
            print("Steps to add a new GitHub project:")
            print("1. Go to https://cloud.therink.io")
            print("2. Click '+ Add' → 'Application'")
            print("3. Select 'Public Repository' or connect your GitHub account")
            print("4. Enter your GitHub repo URL (e.g., https://github.com/username/repo)")
            print("5. Configure build settings (Dockerfile, Nixpacks, etc.)")
            print("6. Set environment variables if needed")
            print("7. Click 'Save'")
            print()
            print("Once created, run this script again to deploy it!")
            print()
            print("=" * 70)
            print("💡 QUICK TIP:")
            print("=" * 70)
            print("If you tell me your GitHub repos, I can help you:")
            print("- Generate Dockerfiles if needed")
            print("- Suggest environment variables")
            print("- Create deployment configurations")
            print("- Automate the deployment process once apps are created")
            print()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Deployment cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
