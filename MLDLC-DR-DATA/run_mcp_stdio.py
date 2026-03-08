#!/usr/bin/env python3
"""Run MLDLC MCP server (stdio transport for Cursor)."""
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mldlc_server.mcp_server_stdio import main

if __name__ == "__main__":
    sys.exit(main())
