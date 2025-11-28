#!/usr/bin/env python3
"""
Deploy a specific Coolify application by name or UUID
Usage: python deploy_app.py <app_name_or_uuid> [--force]
"""
import asyncio
import os
import json
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

os.environ["COOLIFY_BASE_URL"] = "https://cloud.therink.io"
os.environ["COOLIFY_API_TOKEN"] = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"

async def find_app_by_name_or_uuid(session, search_term):
    """Find application by name or UUID"""
    result = await session.call_tool("list_applications", {})
    data = json.loads(result.content[0].text)
    apps = data.get("applications", [])
    
    for app in apps:
        if app.get("uuid") == search_term or app.get("name") == search_term:
            return app
    return None

async def deploy(app_identifier, force_rebuild=False):
    server_params = StdioServerParameters(
        command="python",
        args=["c:\\Users\\19057\\CoolifyMCP\\coolify-mcp-server\\server_stdio.py"],
        env=os.environ
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Find the app
            print(f"🔍 Searching for app: {app_identifier}")
            app = await find_app_by_name_or_uuid(session, app_identifier)
            
            if not app:
                print(f"❌ Application '{app_identifier}' not found!")
                print("\nAvailable apps:")
                result = await session.call_tool("list_applications", {})
                data = json.loads(result.content[0].text)
                for a in data.get("applications", []):
                    print(f"  - {a.get('name')} ({a.get('uuid')})")
                return
            
            app_uuid = app.get("uuid")
            app_name = app.get("name")
            
            print(f"✅ Found: {app_name}")
            print(f"   UUID: {app_uuid}")
            print(f"   Current Status: {app.get('status')}")
            print(f"   Force Rebuild: {force_rebuild}")
            print()
            
            # Deploy
            print("🚀 Starting deployment...")
            result = await session.call_tool("deploy_application", {
                "app_uuid": app_uuid,
                "force_rebuild": force_rebuild
            })
            
            deploy_data = json.loads(result.content[0].text)
            print(json.dumps(deploy_data, indent=2))
            
            # Wait and get logs
            print("\n⏳ Waiting 3 seconds for deployment to start...")
            await asyncio.sleep(3)
            
            print("\n📋 Fetching deployment logs...")
            result = await session.call_tool("get_application_logs", {
                "app_uuid": app_uuid,
                "lines": 50
            })
            
            logs_data = json.loads(result.content[0].text)
            if "logs" in logs_data:
                print("\n" + "=" * 80)
                print("DEPLOYMENT LOGS")
                print("=" * 80)
                print(logs_data.get("logs", "No logs available"))
            else:
                print(json.dumps(logs_data, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy_app.py <app_name_or_uuid> [--force]")
        print("\nExample:")
        print("  python deploy_app.py openhands")
        print("  python deploy_app.py cs4k8wcs48c0skgsos0gksk8 --force")
        sys.exit(1)
    
    app_id = sys.argv[1]
    force = "--force" in sys.argv
    
    asyncio.run(deploy(app_id, force))
