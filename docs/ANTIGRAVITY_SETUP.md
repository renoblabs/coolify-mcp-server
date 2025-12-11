# Google Antigravity Setup

This guide documents the specific configuration required for **Google Antigravity (Deepmind)** agents to connect to the Coolify MCP server.

## Why Local STDIO?

For local development on the same machine as the agent:
1.  **Reliability**: Avoids network hops and potential cloud tunnel issues.
2.  **Speed**: Instant tool execution.
3.  **Simplicity**: Uses the local Python environment directly.

## Configuration Steps

### 1. Find your Python Path

The agent runs in a restricted Windows environment. You **MUST** use the absolute path to your Python executable. 

Run this in PowerShell to find it:
```powershell
Get-Command python | Select-Object -ExpandProperty Source
```
*Example Output:* `C:\Users\19057\AppData\Local\Programs\Python\Python313\python.exe`

### 2. Configure `mcp_config.json`

Locate your agent's config file (typically `mcp_config.json` in the workspace root or provided by the environment).

```json
{
    "mcpServers": {
        "coolify": {
            "command": "C:\\ABSOLUTE\\PATH\\TO\\python.exe",
            "args": [
                "C:\\Users\\YOUR_USER\\coolify-mcp-server\\server_stdio.py"
            ],
            "cwd": "C:\\Users\\YOUR_USER\\coolify-mcp-server",
            "env": {
                "COOLIFY_BASE_URL": "https://cloud.therink.io"
                // API Token is usually injected or managed by the agent, 
                // but can be added here if needed:
                // "COOLIFY_API_TOKEN": "your-token" 
            }
        }
    }
}
```

### 3. Verify Connection

1.  **Install Dependencies**: Ensure `pip install -r requirements.txt` is run.
2.  **Run Verification Script**: Use the included `verify_apps.py` script to test the connection manually if the agent struggles to list tools.
    ```powershell
    python verify_apps.py
    ```

## Troubleshooting

-   **"EOF" Errors**: Usually means invalid JSON or `server_stdio.py` crashed. Check `cwd` path.
-   **"Unauthorized"**: Verify `COOLIFY_API_TOKEN` is correct in `.env` or passed in `env` config.
-   **"Module not found"**: Ensure `pip install` was run *using the same python executable* as in the config.
