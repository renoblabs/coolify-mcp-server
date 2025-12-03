#!/usr/bin/env python3
"""
Coolify Direct API Helper
Works without MCP - just direct HTTP calls to the Coolify API.
Use this when MCP clients are being difficult!

Usage:
    from coolify_api import CoolifyAPI
    api = CoolifyAPI("https://cloud.therink.io", "your-token")
    apps = api.list_applications()
"""

import requests
from typing import Dict, List, Optional
import os


class CoolifyAPI:
    """Direct API wrapper for Coolify - no MCP needed!"""
    
    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or os.getenv("COOLIFY_BASE_URL", "https://cloud.therink.io")
        self.token = token or os.getenv("COOLIFY_API_TOKEN")
        
        if not self.token:
            raise ValueError("COOLIFY_API_TOKEN required. Set it as env var or pass to constructor.")
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make API request"""
        url = f"{self.base_url}/api/v1{endpoint}"
        response = requests.request(method, url, headers=self.headers, json=data, timeout=30)
        
        if response.status_code == 404:
            return {"error": "Not found", "status": 404}
        
        response.raise_for_status()
        return response.json() if response.text else {}
    
    # ==================== Applications ====================
    
    def list_applications(self) -> List[Dict]:
        """List all applications"""
        result = self._request("GET", "/applications")
        return result if isinstance(result, list) else result.get("data", result)
    
    def get_application(self, uuid: str) -> Dict:
        """Get application details"""
        return self._request("GET", f"/applications/{uuid}")
    
    def start_application(self, uuid: str) -> Dict:
        """Start/deploy an application"""
        return self._request("POST", f"/applications/{uuid}/start")
    
    def stop_application(self, uuid: str) -> Dict:
        """Stop an application"""
        return self._request("POST", f"/applications/{uuid}/stop")
    
    def restart_application(self, uuid: str) -> Dict:
        """Restart an application"""
        return self._request("POST", f"/applications/{uuid}/restart")
    
    def get_logs(self, uuid: str, lines: int = 100) -> str:
        """Get application logs"""
        return self._request("GET", f"/applications/{uuid}/logs?lines={lines}")
    
    def get_environment(self, uuid: str) -> Dict:
        """Get application environment variables"""
        return self._request("GET", f"/applications/{uuid}/envs")
    
    def update_environment(self, uuid: str, env_vars: Dict[str, str]) -> Dict:
        """Update application environment variables"""
        return self._request("PATCH", f"/applications/{uuid}/envs", {"data": env_vars})
    
    # ==================== Servers ====================
    
    def list_servers(self) -> List[Dict]:
        """List all servers"""
        result = self._request("GET", "/servers")
        return result if isinstance(result, list) else result.get("data", result)
    
    def get_server(self, uuid: str) -> Dict:
        """Get server details"""
        return self._request("GET", f"/servers/{uuid}")
    
    # ==================== Helper Methods ====================
    
    def get_app_by_name(self, name: str) -> Optional[Dict]:
        """Find an application by name (partial match)"""
        apps = self.list_applications()
        for app in apps:
            if name.lower() in app.get("name", "").lower():
                return app
        return None
    
    def print_status(self):
        """Print status of all applications"""
        apps = self.list_applications()
        print("=" * 60)
        print("COOLIFY APPLICATIONS")
        print("=" * 60)
        
        for app in apps:
            name = app.get("name", "Unknown")
            status = app.get("status", "unknown")
            uuid = app.get("uuid", "N/A")
            
            if "running" in status and "healthy" in status:
                icon = "✅"
            elif "running" in status:
                icon = "⚠️ "
            else:
                icon = "❌"
            
            print(f"{icon} {name}")
            print(f"   Status: {status}")
            print(f"   UUID: {uuid}")
            print()
        
        print(f"Total: {len(apps)} applications")
        print("=" * 60)


# Quick CLI usage
if __name__ == "__main__":
    import sys
    
    # Use env vars or defaults for therink.io setup
    api = CoolifyAPI()
    
    if len(sys.argv) < 2:
        api.print_status()
    else:
        cmd = sys.argv[1]
        
        if cmd == "list":
            api.print_status()
        
        elif cmd == "start" and len(sys.argv) > 2:
            result = api.start_application(sys.argv[2])
            print(f"Started: {result}")
        
        elif cmd == "stop" and len(sys.argv) > 2:
            result = api.stop_application(sys.argv[2])
            print(f"Stopped: {result}")
        
        elif cmd == "restart" and len(sys.argv) > 2:
            result = api.restart_application(sys.argv[2])
            print(f"Restarted: {result}")
        
        elif cmd == "logs" and len(sys.argv) > 2:
            logs = api.get_logs(sys.argv[2])
            print(logs)
        
        else:
            print("Usage:")
            print("  python coolify_api.py                    # List all apps")
            print("  python coolify_api.py list               # List all apps")
            print("  python coolify_api.py start <uuid>       # Start app")
            print("  python coolify_api.py stop <uuid>        # Stop app")
            print("  python coolify_api.py restart <uuid>     # Restart app")
            print("  python coolify_api.py logs <uuid>        # Get logs")

