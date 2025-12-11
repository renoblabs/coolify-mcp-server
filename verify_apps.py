import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

# Set env vars
os.environ["COOLIFY_BASE_URL"] = "https://cloud.therink.io"
os.environ["COOLIFY_API_TOKEN"] = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"

async def run():
    server_params = StdioServerParameters(
        command="C:\\Users\\19057\\AppData\\Local\\Programs\\Python\\Python313\\python.exe",
        args=["c:\\Users\\19057\\coolify-mcp-server\\server_stdio.py"],
        env=os.environ
    )

    print("Connecting to server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List apps
            print("\nListing applications...")
            result = await session.call_tool("list_applications", {})
            for content in result.content:
                if content.type == "text":
                    apps = json.loads(content.text)
                    if "applications" in apps:
                        for app in apps["applications"]:
                            print(f"Name: {app.get('name')} | Description: {app.get('description')} | UUID: {app.get('uuid')}")
                    else:
                        print(content.text)
                else:
                    print(f"[{content.type} content]")

if __name__ == "__main__":
    asyncio.run(run())
