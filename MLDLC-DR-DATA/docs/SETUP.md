# MLDLC DR Data - Setup Guide

## Prerequisites

- Python 3.10+
- pip or uv

## Installation

```bash
cd MLDLC-DR-DATA
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
```

## Cursor Integration

1. Copy the contents of `.cursor/mcp.json` into your Cursor MCP settings (Settings → MCP)
2. Set the `cwd` to the full path of MLDLC-DR-DATA
3. Use `python run_mcp_stdio.py` as the command with cwd set to this project

Example Cursor MCP config:

```json
{
  "mcpServers": {
    "mldlc-vtco": {
      "command": "python",
      "args": ["run_mcp_stdio.py"],
      "cwd": "C:/path/to/MLDLC-DR-DATA",
      "env": {
        "MLDLC_MODE": "development",
        "MLDLC_SCHEMAS_PATH": "./schemas",
        "MLDLC_GOVERNANCE_PATH": "./governance",
        "MLDLC_AUDIT_PATH": "./data/audit"
      }
    }
  }
}
```

## Run Dashboard

```bash
streamlit run app/main.py
```
