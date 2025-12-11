import os
import requests
import json
import time

BASE_URL = "https://cloud.therink.io/api/v1"
TOKEN = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_req(endpoint):
    try:
        url = f"{BASE_URL}{endpoint}"
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return None

print(f"--- SERVER HEALTH ---")
servers = get_req("/servers")
if servers:
    for s in servers:
        print(f"Server: {s.get('name')} ({s.get('uuid')})")
        print(f"  Status: {s.get('settings', {}).get('is_reachable', 'Unknown')}")
        # Try to get resources
        res = get_req(f"/servers/{s.get('uuid')}/resources")
        if res:
             print(f"  Resources: {json.dumps(res)[:100]}...")

print(f"\n--- APPLICATION HEALTH ---")
apps = get_req("/applications")
if apps:
    for a in apps:
        print(f"App: {a.get('name')} ({a.get('uuid')})")
        print(f"  Status: {a.get('status')}")
        print(f"  Description: {a.get('description')}")
        
        # Check logs if running
        if a.get('status') == 'running':
            logs = get_req(f"/applications/{a.get('uuid')}/logs?lines=5")
            # Logs usually return plain text or json wrapper
            print(f"  Recent Logs: {str(logs)[:100].replace(chr(10), ' ')}...")

# Poll brunson deployment
BRUNSON_UUID = "tkcwcwwwgcsgwco8g0wkc840"
print(f"\n--- BRUNSON DEPLOYMENT UPCHECK ---")
brunson = get_req(f"/applications/{BRUNSON_UUID}")
if brunson:
    print(f"Current Status: {brunson.get('status')}")
