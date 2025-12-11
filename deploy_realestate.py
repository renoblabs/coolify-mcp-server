import os
import requests
import json
import time

BASE_URL = "https://cloud.therink.io/api/v1"
TOKEN = "3|3e7fzF0d5C1WT5s0aRa6ini5eLoAodvuwqxzkq1l14ec4cb8"
# Main Server UUID
SERVER_UUID = "p4kssssswg8kw8c0ookwg4k8" 
# GitHub App UUID (from previous audit/logs, usually implies generic public repo capability or existing linked git app)
# Using generic public repo endpoint or creating via project
# NOTE: v4 API usually requires project_uuid and environment_name to create resources.
# Let's try to list projects first to get a valid destination.

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_req(endpoint):
    resp = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
    return resp.json() if resp.status_code == 200 else None

def post_req(endpoint, data):
    resp = requests.post(f"{BASE_URL}{endpoint}", headers=headers, json=data)
    print(f"POST {endpoint}: {resp.status_code}")
    print(resp.text[:200])
    return resp.json() if resp.status_code in [200, 201] else None

print("--- Step 1: Find Destination Project & Environment ---")
projects = get_req("/projects")
if not projects:
    print("❌ Critical: No projects found. Cannot deploy.")
    exit(1)

# Just pick the first project and environment
project = projects[0]
project_uuid = project.get('uuid')
env = get_req(f"/projects/{project_uuid}")['environments'][0]
env_name = env.get('name')
print(f"Target: Project '{project.get('name')}' -> Env '{env_name}'")

print("\n--- Step 2: Create Application ---")
# Endpoint based on API docs for creating public repo app
# usually POST /applications/public 
payload = {
    "project_uuid": project_uuid,
    "environment_name": env_name,
    "server_uuid": SERVER_UUID,
    "git_repository": "https://github.com/renoblabs/Real-Estate-Analysis-Tool",
    "git_branch": "main",
    "build_pack": "nixpacks",
    "ports_exposes": "3000", # Internal port (default for nixpacks usually)
    "name": "Real Estate Tool (Antigravity)"
}

new_app = post_req("/applications/public", payload)

if new_app:
    app_uuid = new_app.get('uuid')
    print(f"\n✅ Created App! UUID: {app_uuid}")
    
    print("\n--- Step 3: Trigger Deployment ---")
    deploy_url = f"/deploy?uuid={app_uuid}&force=false"
    deploy = requests.get(f"{BASE_URL}{deploy_url}", headers=headers)
    print(f"Deploy Trigger: {deploy.status_code}")
    print(f"Response: {deploy.text}")
else:
    print("❌ Failed to create application.")
