# Cursor AI Governance Framework - Setup Guide

This guide configures Cursor to use the AI Governance Framework with zone-based enforcement.

## 1. MCP Server Configuration

Add the AI Governance MCP server to Cursor:

1. Open **Cursor Settings** → **MCP** (or `~/.cursor/mcp.json`)
2. Add the following configuration (adjust paths for your system):

```json
{
  "mcpServers": {
    "ai-governance": {
      "command": "C:\\Users\\zumah\\AppData\\Local\\Programs\\Python\\Python311\\python.exe",
      "args": ["C:\\Users\\zumah\\ai-governance-demo\\mcp_server.py"],
      "env": {
        "GOVERNANCE_REPO_PATH": "C:\\Users\\zumah\\ai-governance-demo",
        "GOVERNANCE_ROLE": "novice",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

3. **Restart Cursor** to load the MCP server.

## 2. Verify MCP Connection

In Cursor Chat, run:

```
@mcp Initialize the AI Governance MCP server and confirm connection.
```

Expected: `✅ AI Governance MCP Server connected` with tools listed.

## 3. Quick Test Commands

| Command | Purpose |
|---------|---------|
| `@mcp get_current_role` | Check current role |
| `@mcp check_zoning_permission for file "src/payment/gateway.ts" with role "novice"` | RED zone - blocked |
| `@mcp check_zoning_permission for file "src/payment/gateway.ts" with role "champion"` | RED zone - allowed |
| `@mcp check_zoning_permission for file "src/api/users/controller.ts" with role "novice" and has_mentor false` | YELLOW - blocked (no mentor) |
| `@mcp check_zoning_permission for file "src/api/users/controller.ts" with role "novice" and has_mentor true` | YELLOW - allowed |
| `@mcp check_zoning_permission for file "tests/utils/helpers.test.ts" with role "novice"` | GREEN - full autonomy |
| `@mcp get_tribal_knowledge for domain "api-design"` | API design patterns |
| `@mcp get_tribal_knowledge for domain "database"` | Database patterns |
| `@mcp calculate_entropy with bloat_percent 4.2, rework_percent 18.0, revert_percent 2.3, premature_acceptance_percent 15.6` | Entropy score |
| `@mcp get_ai_context for file_path "src/payment/gateway.ts"` | AI behavior for RED zone |

## 4. Role Configuration

Set your role via environment (in MCP config `env`):

- `GOVERNANCE_ROLE`: `novice` | `intermediate` | `expert` | `champion`
- `GOVERNANCE_MENTOR`: Mentor ID (e.g., `Sec-Champ-01`) – required for novices in Yellow zone

## 5. Cursor Rule

The rule at `.cursor/rules/ai-governance-framework.mdc` is set to `alwaysApply: true`, so the AI will follow zone-based behavior in all conversations.

## 6. Run Verification

```bash
python verify_governance_setup.py
```

All 11 tests should pass.
