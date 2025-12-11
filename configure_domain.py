import os
import requests
import json
import time

BASE_URL = "https://cloud.therink.io/api/v1"
TOKEN = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"
APP_UUID = "qs4s84ss04cgggocck0owc8k"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def patch_req(endpoint, data):
    print(f"\n--- PATCH {endpoint} ---")
    resp = requests.patch(f"{BASE_URL}{endpoint}", headers=headers, json=data)
    print(f"Status: {resp.status_code}")
    print(resp.text[:200])
    return resp.json() if resp.status_code in [200, 201] else None

print("Configuring Domain: https://reops.therink.io")

# Use PATCH /applications/{uuid} to set fqdn
# Note: coolify expects "fqdn" field in body usually, or "domains"
payload = {
    "name": "Real Estate Tool (Antigravity)",
    "fqdn": "https://reops.therink.io",
    "ports_exposes": "3000"
}

update = patch_req(f"/applications/{APP_UUID}", payload)

if update:
    print("✅ Domain updated successfully!")
    print("Triggering new deployment info update...")
    # Trigger restart to pick up proxy config
    restart = requests.post(f"{BASE_URL}/applications/{APP_UUID}/restart", headers=headers)
    print(f"Restart Trigger: {restart.status_code}")
else:
    print("❌ Failed to update domain.")
