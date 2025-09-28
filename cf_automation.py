# NEW CLOUDFLARE AUTOMATION TOOLS FOR MCP SERVER

@app.tool()
async def create_dns_record(subdomain: str, target: str = "cloud.therink.io", 
                           record_type: str = "CNAME") -> Dict:
    """Create a DNS record in Cloudflare for a subdomain
    
    Args:
        subdomain: The subdomain to create (e.g., 'supabase')
        target: The target domain/IP (default: 'cloud.therink.io')
        record_type: DNS record type (CNAME, A, etc.)
    """
    if not CF_API_TOKEN or not CF_ZONE_ID:
        return {"error": "Cloudflare API token and Zone ID required"}
    
    try:
        cf = CloudFlare.CloudFlare(token=CF_API_TOKEN)
        full_domain = f"{subdomain}.{BASE_DOMAIN}"
        
        # Create DNS record
        dns_record = {
            'name': full_domain,
            'type': record_type,
            'content': target,
            'ttl': 1  # Automatic TTL
        }
        
        result = cf.zones.dns_records.post(CF_ZONE_ID, data=dns_record)
        
        return {
            "success": True,
            "message": f"Created {record_type} record: {full_domain} -> {target}",
            "record_id": result['id'],
            "full_domain": full_domain
        }
    except Exception as e:
        return {"error": f"Failed to create DNS record: {str(e)}"}

@app.tool() 
async def automate_service_deployment(service_name: str, subdomain: str, 
                                     app_uuid: str, port: int = 8000) -> Dict:
    """FULLY AUTOMATE service deployment with CF tunnel and DNS
    
    Args:
        service_name: Name of the service (e.g., 'Supabase')
        subdomain: Desired subdomain (e.g., 'supabase')
        app_uuid: Coolify application UUID
        port: Local port the service runs on
    """
    results = {
        "service": service_name,
        "subdomain": subdomain,
        "steps": [],
        "errors": []
    }
    
    full_domain = f"{subdomain}.{BASE_DOMAIN}"
    
    try:
        # Step 1: Create DNS record
        dns_result = await create_dns_record(subdomain)
        if dns_result.get("success"):
            results["steps"].append(f"✅ Created DNS record: {full_domain}")
        else:
            results["errors"].append(f"❌ DNS creation failed: {dns_result.get('error')}")
        
        # Step 2: Update application environment if needed
        try:
            env_vars = await get_application_environment(app_uuid)
            updated_env = {}
            
            # Replace localhost references with the new domain
            for key, value in env_vars.get("data", {}).items():
                if isinstance(value, str):
                    if "localhost:8000" in value:
                        updated_env[key] = value.replace("localhost:8000", f"https://{full_domain}")
                    elif "http://localhost" in value:
                        updated_env[key] = value.replace("http://localhost", f"https://{full_domain}")
            
            if updated_env:
                update_result = await update_application_environment(app_uuid, updated_env)
                results["steps"].append(f"✅ Updated {len(updated_env)} environment variables")
                results["updated_vars"] = updated_env
        except Exception as e:
            results["errors"].append(f"❌ Environment update failed: {str(e)}")
        
        # Step 3: Trigger deployment
        try:
            deploy_result = await deploy_application(app_uuid)
            if not deploy_result.get("error"):
                results["steps"].append("✅ Triggered application deployment")
            else:
                results["errors"].append(f"❌ Deployment failed: {deploy_result.get('message')}")
        except Exception as e:
            results["errors"].append(f"❌ Deployment trigger failed: {str(e)}")
        
        # Summary
        results["success"] = len(results["errors"]) == 0
        results["summary"] = f"""
🚀 {service_name} Deployment Summary:
📍 Domain: https://{full_domain}
🔗 Coolify App: {app_uuid}
⚡ Port: {port}

{len(results['steps'])} steps completed
{len(results['errors'])} errors occurred

{'✅ FULLY AUTOMATED!' if results['success'] else '⚠️  Manual intervention needed'}

Next: Add this to your tunnel config:
  - hostname: {full_domain}
    service: http://localhost:{port}
        """
        
        return results
        
    except Exception as e:
        results["errors"].append(f"❌ Automation failed: {str(e)}")
        results["success"] = False
        return results