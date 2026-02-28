# Universal AI Governance Framework

A consulting methodology for AI adoption that protects human expertise while enabling scale.

## The Three Roles Architecture

**AI Training Consultant** (You)
- Assesses, architects, configures, trains, exits
- Brings methodology + MCP setup + change management
- 8-week engagement, then quarterly check-ins

**MCP Server** (Technical Enforcer)
- Local Python script (not cloud infrastructure)
- Blocks Red Zone edits, scaffolds by skill, logs entropy
- Cannot judge business priority or build human trust

**Champion** (Human Expert)
- Owns Red Zone decisions, authors tribal knowledge (VTCO)
- Assesses skills, mentors transitions, governs emergencies
- Protected from burnout by automation

## Maturity Progression

M1 (Gray) → M2 (Orange) → M3 (Blue) → M4 (Gold)

- M1: Chaos (no governance)
- M2: Shallow (licenses, no governance) ← **Baseline**
- M3: Agentic (governed autonomy) ← **Target**
- M4: Autonomous (self-optimizing)

## Protection Architecture

1. **Human Coding Architecture**: MCP enforces patterns champion defines
2. **Tribal Knowledge**: VTCO format captures expertise in repo
3. **Champion Judgment**: Authority formalized, noise filtered by MCP

## Evidence-Based

- Entropy Formula: (Bloat×0.25) + (Rework×0.25) + (Reverts×0.20) + (Premature×0.30)
- Git-based metrics: Non-gameable, objective
- Week-by-week improvement: Measurable, guaranteed

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## MCP Server (Cursor Integration)

The MCP server enforces governance rules, zoning, and entropy tracking in Cursor IDE.

### Setup

1. Install MCP dependencies:
   ```bash
   pip install -r requirements-mcp.txt
   ```

2. Add to Cursor MCP settings. Copy the `mcp_config.json` content into your Cursor MCP configuration (Settings → MCP). Use the full path to `mcp_server.py` in the `args` if needed:
   ```json
   {
     "mcpServers": {
       "ai-governance": {
         "command": "python",
         "args": ["C:/path/to/ai-governance-demo/mcp_server.py"],
         "env": { "GOVERNANCE_REPO_PATH": "C:/path/to/ai-governance-demo" }
       }
     }
   }
   ```

3. Run the server standalone (stdio):
   ```bash
   python mcp_server.py
   ```

### Tools

- **check_zoning_permission** – Check if an edit is allowed (file path, role, phase)
- **get_tribal_knowledge** – Retrieve VTCO context for a domain
- **calculate_entropy** – Compute and log entropy score
- **validate_code_patterns** – Check code against architectural patterns
- **record_decision** – Log ADR and champion approvals

### Logs

- Entropy: `.ai-governance/entropy_log.jsonl`
- Violations: `.ai-governance/violations.jsonl`
- Tribal knowledge: `.ai-governance/tribal-knowledge/*.yaml`

### Tests

```bash
cd ai-governance-demo
pip install -r requirements-mcp.txt
pytest tests/ -v
```

## For Headstorm AI Interview

February 2026
