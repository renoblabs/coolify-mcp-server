#!/usr/bin/env python3
import requests
import json
import sys

# Configuration
COOLIFY_BASE_URL = "https://cloud.therink.io"
COOLIFY_API_TOKEN = "2|1AVWKq6jqYmnCH5TFtHnYPrGGC0HuNZGOH2sy3b0deb49e23"
HEADERS = {
    "Authorization": f"Bearer {COOLIFY_API_TOKEN}",
    "Content-Type": "application/json"
}

# Application configuration
APP_CONFIG = {
    "name": "mcp-server",
    "description": "Coolify MCP Server - SSE Endpoint",
    "git_repository": "https://github.com/renoblabs/coolify-mcp-server.git",
    "git_branch": "master",
    "build_pack": "dockerfile",
    "dockerfile_location": "./Dockerfile",
    "ports_exposes": "8765",
    "domains": "mcp.therink.io",
    "environment_variables": {
        "COOLIFY_API_TOKEN": "2|1AVWKq6jqYmnCH5TFtHnYPrGGC0HuNZGOH2sy3b0deb49e23",
        "COOLIFY_BASE_URL": "http://174.88.139.173:8000",
        "USE_TUNNEL": "true",
        "COOLIFY_TUNNEL_URL": "https://cloud.therink.io",
        "CLOUDFLARE_API_TOKEN": "yCqmxrvDB7jHlCp1CpVQolo6BfCH0fNqb0srOkwz",
        "CLOUDFLARE_ZONE_ID": "61a745f1bc21b16569875efe1d02202b",
        "CLOUDFLARE_TUNNEL_ID": "d5d71027-31d6-443a-b2d9-fdd016e720cc",
        "BASE_DOMAIN": "therink.io",
        "MCP_AUTH_TOKEN": "E2L98+RsBfM7vSBNoDvPmdA4iYj1C0FrBqsd14LEQXo=",
        "MCP_PORT": "8765",
        "MCP_HOST": "0.0.0.0"
    }
}

def get_teams():
    """Get list of teams"""
    url = f"{COOLIFY_BASE_URL}/api/v1/teams"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_projects(team_id):
    """Get projects for a team"""
    url = f"{COOLIFY_BASE_URL}/api/v1/teams/{team_id}/projects"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_environments(project_uuid):
    """Get environments for a project"""
    url = f"{COOLIFY_BASE_URL}/api/v1/projects/{project_uuid}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def create_application(project_uuid, environment_name, server_uuid):
    """Create a new application"""
    url = f"{COOLIFY_BASE_URL}/api/v1/applications"
    
    payload = {
        "project_uuid": project_uuid,
        "environment_name": environment_name,
        "server_uuid": server_uuid,
        "type": "public",
        **APP_CONFIG
    }
    
    response = requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    print("🚀 Deploying MCP Server to Coolify...")
    
    try:
        # Step 1: Get teams
        print("\n1️⃣  Fetching teams...")
        teams = get_teams()
        if not teams:
            print("❌ No teams found!")
            sys.exit(1)
        
        team_id = teams[0]['id']
        print(f"✅ Using team: {teams[0]['name']} (ID: {team_id})")
        
        # Step 2: Get projects
        print("\n2️⃣  Fetching projects...")
        projects = get_projects(team_id)
        if not projects:
            print("❌ No projects found!")
            sys.exit(1)
        
        project = projects[0]
        project_uuid = project['uuid']
        print(f"✅ Using project: {project['name']} (UUID: {project_uuid})")
        
        # Step 3: Get environments and server
        print("\n3️⃣  Fetching environments...")
        project_details = get_environments(project_uuid)
        
        if not project_details.get('environments'):
            print("❌ No environments found!")
            sys.exit(1)
        
        env = project_details['environments'][0]
        environment_name = env['name']
        server_uuid = project_details.get('uuid')
        
        print(f"✅ Using environment: {environment_name}")
        
        # Step 4: Create application
        print("\n4️⃣  Creating application...")
        result = create_application(project_uuid, environment_name, server_uuid)
        
        print(f"\n🎉 Successfully created MCP Server application!")
        print(f"📋 Application UUID: {result.get('uuid')}")
        print(f"🌐 Domain: mcp.therink.io")
        print(f"🔗 Access at: {COOLIFY_BASE_URL}")
        
        print("\n⚠️  Next steps:")
        print("1. Go to Coolify UI and start the deployment")
        print("2. Wait for the build to complete")
        print("3. Test the endpoint: curl https://mcp.therink.io/sse")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()
