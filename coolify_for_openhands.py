#!/usr/bin/env python3
"""
Coolify Integration for OpenHands
Direct API approach - optimized for OpenHands usage

Your Coolify Server: https://cloud.therink.io
Applications Found:
- renoblabs/-real--estate--analysis--tool:main-mo0cccgc8o8o8kw0o4ow4o8w (exited:unhealthy)
- openhands (exited:unhealthy) 
- renoblabs/-brunson:main-vksw48gwcg8g00wc0cgk40sw (exited:unhealthy)
"""

import os
import sys
import requests
from typing import Dict, List, Optional

# Add the coolify-mcp-server to path
sys.path.append('/workspace/project/coolify-mcp-server')

class CoolifyForOpenHands:
    """Coolify integration specifically designed for OpenHands"""
    
    def __init__(self):
        # Your Coolify credentials
        self.base_url = "https://cloud.therink.io"
        self.token = "5|Zs8nkfu0I6re2WxCiZVmjMgTkXnJsMHVlRyiESgZ4f80dd46"
        
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Cache applications for better performance
        self._apps_cache = None
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make API request to Coolify"""
        url = f"{self.base_url}/api/v1{endpoint}"
        
        try:
            response = requests.request(method, url, headers=self.headers, json=data, timeout=30)
            
            if response.status_code == 404:
                return {"error": "Not found", "status": 404}
            
            response.raise_for_status()
            return response.json() if response.text else {}
            
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status": "connection_error"}
    
    def _get_apps(self, refresh=False) -> List[Dict]:
        """Get applications with caching"""
        if self._apps_cache is None or refresh:
            result = self._request("GET", "/applications")
            self._apps_cache = result if isinstance(result, list) else result.get("data", [])
        return self._apps_cache
    
    def _find_app(self, identifier: str) -> Optional[Dict]:
        """Find app by name or UUID"""
        apps = self._get_apps()
        
        for app in apps:
            if (app.get('name') == identifier or 
                app.get('uuid') == identifier or
                identifier.lower() in app.get('name', '').lower()):
                return app
        return None
    
    # ==================== Main Functions ====================
    
    def list_applications(self) -> List[Dict]:
        """List all your Coolify applications"""
        apps = self._get_apps(refresh=True)  # Always refresh for list
        
        print("🚀 Your Coolify Applications")
        print("=" * 60)
        
        if not apps:
            print("❌ No applications found")
            return []
        
        for i, app in enumerate(apps, 1):
            name = app.get('name', 'Unknown')
            status = app.get('status', 'Unknown')
            uuid = app.get('uuid', 'Unknown')
            
            # Status emoji
            status_emoji = {
                'running': '✅',
                'stopped': '⏹️',
                'exited': '❌',
                'restarting': '🔄',
                'starting': '🟡'
            }.get(status.split(':')[0], '❓')
            
            print(f"{i}. {status_emoji} {name}")
            print(f"   Status: {status}")
            print(f"   UUID: {uuid}")
            print()
        
        return apps
    
    def deploy_application(self, app_identifier: str, force_rebuild: bool = False) -> bool:
        """Deploy/redeploy an application"""
        app = self._find_app(app_identifier)
        
        if not app:
            print(f"❌ Application '{app_identifier}' not found")
            self.list_applications()  # Show available apps
            return False
        
        app_name = app.get('name', 'Unknown')
        app_uuid = app.get('uuid')
        
        print(f"🚀 Deploying '{app_name}'...")
        if force_rebuild:
            print("🔨 Force rebuild enabled")
        
        # Prepare deployment data
        data = {"force_rebuild": force_rebuild} if force_rebuild else {}
        
        # Use the /start endpoint which actually works for deployment
        result = self._request("POST", f"/applications/{app_uuid}/start", data)
        
        if "error" in result:
            print(f"❌ Deployment failed: {result['error']}")
            return False
        
        # Check for successful deployment queue
        if "message" in result and "queued" in result["message"].lower():
            deployment_uuid = result.get("deployment_uuid")
            print(f"✅ Deployment started for '{app_name}'")
            if deployment_uuid:
                print(f"📋 Deployment UUID: {deployment_uuid}")
            print("💡 Use get_logs() to monitor the deployment progress")
            return True
        else:
            print(f"✅ Deployment initiated for '{app_name}'")
            print("💡 Use get_logs() to monitor the deployment progress")
            return True
    
    def restart_application(self, app_identifier: str) -> bool:
        """Restart an application"""
        app = self._find_app(app_identifier)
        
        if not app:
            print(f"❌ Application '{app_identifier}' not found")
            return False
        
        app_name = app.get('name', 'Unknown')
        app_uuid = app.get('uuid')
        
        print(f"🔄 Restarting '{app_name}'...")
        
        result = self._request("POST", f"/applications/{app_uuid}/restart")
        
        if "error" in result:
            print(f"❌ Restart failed: {result['error']}")
            return False
        
        print(f"✅ Restart initiated for '{app_name}'")
        return True
    
    def stop_application(self, app_identifier: str) -> bool:
        """Stop an application"""
        app = self._find_app(app_identifier)
        
        if not app:
            print(f"❌ Application '{app_identifier}' not found")
            return False
        
        app_name = app.get('name', 'Unknown')
        app_uuid = app.get('uuid')
        
        print(f"⏹️ Stopping '{app_name}'...")
        
        result = self._request("POST", f"/applications/{app_uuid}/stop")
        
        if "error" in result:
            print(f"❌ Stop failed: {result['error']}")
            return False
        
        print(f"✅ Stop initiated for '{app_name}'")
        return True
    
    def get_application_logs(self, app_identifier: str, lines: int = 100) -> str:
        """Get application logs"""
        app = self._find_app(app_identifier)
        
        if not app:
            print(f"❌ Application '{app_identifier}' not found")
            return ""
        
        app_name = app.get('name', 'Unknown')
        app_uuid = app.get('uuid')
        
        print(f"📄 Getting logs for '{app_name}' (last {lines} lines)...")
        
        result = self._request("GET", f"/applications/{app_uuid}/logs")
        
        if "error" in result:
            print(f"❌ Failed to get logs: {result['error']}")
            return ""
        
        # Extract logs from the response
        logs = result.get('logs', result.get('data', result if isinstance(result, str) else ''))
        
        if logs:
            print("📋 Application Logs:")
            print("-" * 60)
            print(logs)
            print("-" * 60)
        else:
            print("ℹ️ No logs available")
        
        return logs
    
    def get_application_status(self, app_identifier: str) -> Dict:
        """Get detailed application status"""
        app = self._find_app(app_identifier)
        
        if not app:
            print(f"❌ Application '{app_identifier}' not found")
            return {}
        
        app_name = app.get('name', 'Unknown')
        app_uuid = app.get('uuid')
        
        result = self._request("GET", f"/applications/{app_uuid}")
        
        if "error" in result:
            print(f"❌ Failed to get status: {result['error']}")
            return {}
        
        print(f"📊 Status for '{app_name}':")
        print("-" * 40)
        print(f"Name: {result.get('name', 'Unknown')}")
        print(f"Status: {result.get('status', 'Unknown')}")
        print(f"UUID: {result.get('uuid', 'Unknown')}")
        print(f"Repository: {result.get('git_repository', 'N/A')}")
        print(f"Branch: {result.get('git_branch', 'N/A')}")
        
        return result
    
    def quick_status(self) -> None:
        """Show a quick status overview of all applications"""
        apps = self._get_apps(refresh=True)
        
        print("⚡ Quick Status Overview")
        print("=" * 40)
        
        status_counts = {}
        for app in apps:
            status = app.get('status', 'unknown').split(':')[0]
            status_counts[status] = status_counts.get(status, 0) + 1
            
            name = app.get('name', 'Unknown')
            if len(name) > 30:
                name = name[:27] + "..."
            
            status_emoji = {
                'running': '✅',
                'stopped': '⏹️', 
                'exited': '❌',
                'restarting': '🔄',
                'starting': '🟡'
            }.get(status, '❓')
            
            print(f"{status_emoji} {name}")
        
        print("\n📈 Summary:")
        for status, count in status_counts.items():
            print(f"  {status}: {count}")

# ==================== Global Instance & Convenience Functions ====================

# Create global instance for easy access
coolify = CoolifyForOpenHands()

def list_apps():
    """List all Coolify applications"""
    return coolify.list_applications()

def deploy_app(app_name: str, force_rebuild: bool = False):
    """Deploy a Coolify application by name or UUID"""
    return coolify.deploy_application(app_name, force_rebuild)

def restart_app(app_name: str):
    """Restart a Coolify application by name or UUID"""
    return coolify.restart_application(app_name)

def stop_app(app_name: str):
    """Stop a Coolify application by name or UUID"""
    return coolify.stop_application(app_name)

def get_logs(app_name: str, lines: int = 100):
    """Get logs for a Coolify application"""
    return coolify.get_application_logs(app_name, lines)

def get_status(app_name: str):
    """Get detailed status for a Coolify application"""
    return coolify.get_application_status(app_name)

def status():
    """Show quick status overview of all applications"""
    return coolify.quick_status()

# ==================== OpenHands Integration Examples ====================

def deploy_openhands():
    """Deploy the OpenHands application specifically"""
    return deploy_app("openhands")

def restart_openhands():
    """Restart the OpenHands application specifically"""
    return restart_app("openhands")

def openhands_logs():
    """Get OpenHands application logs"""
    return get_logs("openhands")

if __name__ == "__main__":
    print("🧪 Testing Coolify for OpenHands integration...")
    print()
    status()
    print()
    print("💡 Available functions:")
    print("  - list_apps() - List all applications")
    print("  - deploy_app('app-name') - Deploy an application")
    print("  - restart_app('app-name') - Restart an application") 
    print("  - stop_app('app-name') - Stop an application")
    print("  - get_logs('app-name') - Get application logs")
    print("  - get_status('app-name') - Get detailed status")
    print("  - status() - Quick overview")
    print()
    print("🎯 OpenHands specific:")
    print("  - deploy_openhands() - Deploy OpenHands")
    print("  - restart_openhands() - Restart OpenHands")
    print("  - openhands_logs() - Get OpenHands logs")