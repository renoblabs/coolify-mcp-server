#!/usr/bin/env python3
"""
Windows-optimized wrapper to run server.py
Forces UTF-8 encoding and runs the server directly.
"""
import sys
import os
import subprocess

# Force UTF-8 encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    # Set console to UTF-8
    os.system('chcp 65001 > nul')
    print("✓ Windows UTF-8 encoding configured")

# Run server.py with all command line arguments
if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(script_dir, "server.py")

    # Pass through all command line arguments
    args = [sys.executable, server_path] + sys.argv[1:]

    print(f"Starting: {' '.join(args)}")
    print("")

    # Run server.py directly
    try:
        subprocess.run(args, check=True)
    except KeyboardInterrupt:
        print("\nShutdown requested")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"Server exited with error code: {e.returncode}")
        sys.exit(e.returncode)
