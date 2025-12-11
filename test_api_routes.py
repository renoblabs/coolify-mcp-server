import os
import requests
import json

BASE_URL = "https://cloud.therink.io/api/v1"
TOKEN = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"
UUID = "tkcwcwwwgcsgwco8g0wkc840"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def test_route(method, endpoint, name):
    print(f"\n--- Testing {name} ({method} {endpoint}) ---")
    try:
        url = f"{BASE_URL}{endpoint}"
        resp = requests.request(method, url, headers=headers)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("Success!")
            try:
                print(str(resp.json())[:200] + "...")
            except:
                print(resp.text[:200])
        else:
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Exception: {e}")

# Test Environment
test_route("GET", f"/applications/{UUID}/envs", "Get Envs (Correct Path?)")
test_route("GET", f"/applications/{UUID}/environment", "Get Envs (Current Path)")

# Test Deploy (Using GET/POST on /deploy endpoint)
# Note: we won't actually force a build unless we must, but hitting the endpoint to see if it exists (method not allowed or 200)
test_route("GET", f"/deploy?uuid={UUID}", "Deploy via GET /deploy")
