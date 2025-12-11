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
            
            app_uuid = "tkcwcwwwgcsgwco8g0wkc840"
            
            print(f"\n--- Getting Details for {app_uuid} ---")
            result = await session.call_tool("get_application_details", {"app_uuid": app_uuid})
            for content in result.content:
                if content.type == "text":
                    print(content.text)
            
            print(f"\n--- Getting Environment for {app_uuid} ---")
            result_env = await session.call_tool("get_application_environment", {"app_uuid": app_uuid})
            for content in result_env.content:
                if content.type == "text":
                    print(content.text)

if __name__ == "__main__":
    asyncio.run(run())
