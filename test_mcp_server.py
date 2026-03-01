#!/usr/bin/env python3
"""Quick test for MCP server - verifies it starts in stdio mode."""

import subprocess
import sys
from pathlib import Path

def test_mcp_server():
    repo = Path(__file__).parent
    process = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(repo),
    )
    try:
        import time
        time.sleep(1)
        if process.poll() is not None:
            stderr = process.stderr.read()
            print(f"Server exited early: {stderr}")
            return False
        print("MCP server started successfully (stdio mode)")
        return True
    finally:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()

if __name__ == "__main__":
    print("Testing MCP Server...")
    success = test_mcp_server()
    if success:
        print("Server ready for Cursor integration")
    else:
        sys.exit(1)
