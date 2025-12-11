import os
import requests
import json

BASE_URL = "https://cloud.therink.io/api/v1"
TOKEN = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def check_endpoint(endpoint, name):
    print(f"\n--- Checking {name} ({endpoint}) ---")
    try:
        url = f"{BASE_URL}{endpoint}"
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            try:
                data = resp.json()
                print(json.dumps(data, indent=2)[:500] + "..." if len(json.dumps(data)) > 500 else json.dumps(data, indent=2))
                return data
            except:
                print("Response not JSON")
                print(resp.text[:200])
        elif resp.status_code == 403 or resp.status_code == 401:
             print("Access Denied (Did you enable scope?)")
        else:
             print(f"Error: {resp.text[:200]}")
    except Exception as e:
        print(f"Exception: {e}")

# 1. Check Server Resources (Main Server)
# We know uuid from previous list: p4kssssswg8kw8c0ookwg4k8
SERVER_UUID = "p4kssssswg8kw8c0ookwg4k8"
check_endpoint(f"/servers/{SERVER_UUID}", "Main Server Details")
check_endpoint(f"/servers/{SERVER_UUID}/resources", "Main Server Resources")

# 2. Check Settings (Probing common v4 endpoints)
check_endpoint("/settings", "System Settings")
check_endpoint("/notifications", "Notification Settings")
check_endpoint("/security", "Security Settings")

# 3. Check for failed deployments/items
check_endpoint("/deployments", "Recent Deployments")
