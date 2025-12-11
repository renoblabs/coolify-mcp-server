#!/usr/bin/env python3
"""
Show current status of all Coolify applications
"""
import asyncio
import os
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

os.environ["COOLIFY_BASE_URL"] = "https://cloud.therink.io"
os.environ["COOLIFY_API_TOKEN"] = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["c:\\Users\\19057\\CoolifyMCP\\coolify-mcp-server\\server_stdio.py"],
        env=os.environ
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("=" * 80)
            print("📊 COOLIFY APPLICATION STATUS")
            print("=" * 80)
            print()
            
            # Get applications
            result = await session.call_tool("list_applications", {})
            data = json.loads(result.content[0].text)
            apps = data.get("applications", [])
            
            if not apps:
                print("No applications found.")
                return
            
            for i, app in enumerate(apps, 1):
                name = app.get("name", "Unknown")
                uuid = app.get("uuid", "N/A")
                status = app.get("status", "unknown")
                fqdn = app.get("fqdn", "No domain")
                git_repo = app.get("git_repository", "N/A")
                
                # Status icon
                if "running" in status and "healthy" in status:
                    icon = "✅"
                elif "running" in status:
                    icon = "⚠️"
                elif "exited" in status:
                    icon = "❌"
                else:
                    icon = "❓"
                
                print(f"{icon} {i}. {name}")
                print(f"   Status: {status}")
                print(f"   Domain: {fqdn}")
                print(f"   Repo: {git_repo}")
                print(f"   UUID: {uuid}")
                print()
            
            print("=" * 80)
            print(f"Total: {len(apps)} application(s)")
            print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
