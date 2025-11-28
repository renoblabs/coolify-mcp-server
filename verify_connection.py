import os
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Set env vars to match config
os.environ["COOLIFY_BASE_URL"] = "https://cloud.therink.io"
os.environ["COOLIFY_API_TOKEN"] = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"

async def run():
    server_params = StdioServerParameters(
        command="python",
        args=["c:\\Users\\19057\\CoolifyMCP\\coolify-mcp-server\\server_stdio.py"],
        env=os.environ
    )

    print("Connecting to server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List tools
            tools = await session.list_tools()
            print(f"Connected! Found {len(tools.tools)} tools.")
            for tool in tools.tools:
                print(f"- {tool.name}")

if __name__ == "__main__":
    asyncio.run(run())
