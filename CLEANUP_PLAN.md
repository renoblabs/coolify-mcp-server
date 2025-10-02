# Repository Cleanup & Simplification Plan

## Goal
Streamline the repo for its core purpose: **Remote MCP server for on-the-go Coolify management**

## Current Structure Issues
- Too many Python files (3 main servers: local, remote, complete_automation)
- 7 test files (some redundant/outdated)
- 2 comprehensive docs that overlap (README + AUTOMATION_GUIDE)
- Config files with hardcoded tokens (MOBILE_APP_CONFIG, REMOTE_ACCESS_SETUP)
- Reliability report as loose HTML file

## Proposed Simplified Structure

```
coolify-mcp-server/
├── server.py                    # Main remote MCP server (renamed from coolify_mcp_server_remote.py)
├── requirements.txt             # Dependencies
├── .env.example                 # Example environment variables
├── README.md                    # Single comprehensive guide
├── start.sh                     # Simple startup script
│
├── tests/                       # Organized test files
│   ├── test_server.py          # Main server tests
│   ├── test_coolify_api.py     # Coolify API tests
│   └── test_cloudflare.py      # CF automation tests
│
├── examples/                    # Config templates (no secrets)
│   ├── mcp_config.json.example
│   └── mobile_app_config.json.example
│
└── docs/                        # Additional documentation
    ├── AUTOMATION_GUIDE.md
    ├── troubleshooting.md
    └── reports/
        └── reliability-droid-report.html
```

## Files to Keep (Essential)
- ✅ `coolify_mcp_server_remote.py` → rename to `server.py` (main server)
- ✅ `requirements.txt`
- ✅ `.env.example`
- ✅ `.gitignore`
- ✅ `README.md` (rewrite for simplicity)

## Files to Archive/Move
- 📁 `complete_automation.py` → `examples/standalone_automation.py`
- 📁 `fix_tunnel_routes.py` → `examples/fix_tunnel_routes.py`
- 📁 `AUTOMATION_GUIDE.md` → `docs/AUTOMATION_GUIDE.md`
- 📁 `reliability-droid-report.html` → `docs/reports/`
- 📁 `test_*.py` → `tests/` directory

## Files to Remove (Redundant/Deprecated)
- ❌ `coolify_mcp_server.py` (local STDIO - use remote version for everything)
- ❌ `mcp_config.json` (create example version instead)
- ❌ `MOBILE_APP_CONFIG.json` (has tokens - create example)
- ❌ `REMOTE_ACCESS_SETUP.md` (has tokens - merge into README)
- ❌ `setup.sh` (simplify into one start script)
- ❌ `start_with_doppler.sh` (merge into single start script)

## New Files to Create
- ✅ `server.py` (single unified server with both STDIO and HTTP modes)
- ✅ `start.sh` (one script: `doppler run -- python server.py`)
- ✅ `examples/mcp_config.json.example` (template without tokens)
- ✅ `examples/mobile_app_config.json.example` (template without tokens)
- ✅ Simple `README.md` (quick start focused)

## Benefits
1. **Single server file** instead of 3 different versions
2. **Organized structure** with tests/, docs/, examples/ directories
3. **No hardcoded secrets** - all examples use placeholders
4. **Easier onboarding** - one README, one start script
5. **Cleaner git history** - removed deprecated experiments

## Implementation Steps
1. Create new directory structure
2. Create unified `server.py` with mode selection
3. Move files to appropriate directories
4. Create example configs without tokens
5. Rewrite README for simplicity
6. Update .gitignore
7. Test the simplified setup
8. Commit and PR
