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

print(f"--- Verifying App {APP_UUID} ---")
url = f"{BASE_URL}/applications/{APP_UUID}"
resp = requests.get(url, headers=headers)
if resp.status_code == 200:
    data = resp.json()
    status = data.get('status')
    name = data.get('name')
    print(f"Name: {name}")
    print(f"Status: {status}")
    
    # Check logs if running or unhealthy
    if 'running' in status or 'unhealthy' in status or 'exited' in status:
        log_url = f"{BASE_URL}/applications/{APP_UUID}/logs"
        logs = requests.get(log_url, headers=headers)
        if logs.status_code == 200:
            print(f"Logs: {logs.text[:500]}...")
else:
    print(f"Error: {resp.status_code} - {resp.text}")
