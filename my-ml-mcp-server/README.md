# Personal ML MCP Server

Zone-based governance for ML development: **GREEN** (experiment) → **YELLOW** (develop) → **RED** (production).

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Start MCP server (FastAPI)
cd my-ml-mcp-server
uvicorn mcp.server:app --reload --port 8000

# Launch dashboard (separate terminal)
streamlit run app/main.py
```

## Zone Rules

| Zone | Purpose | Cursor Mode |
|------|---------|-------------|
| **GREEN** | Experimentation — notebooks, exploration, quick prototypes | Creative |
| **YELLOW** | Development — templates, random_state, MLflow | Pattern-following |
| **RED** | Production — deterministic, validation, audit trail | Advisory only |

## MCP API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/detect-zone` | POST | Auto-detect zone for a file path |
| `/validate-code` | POST | Validate code against zone rules |
| `/suggest-pattern` | POST | Suggest patterns based on task |
| `/init-experiment` | POST | Initialize new experiment |
| `/query-knowledge-graph` | POST | Query personal ML history |
| `/prompts/{zone}` | GET | Get curated prompts for zone |

## Daily Workflow

1. **New idea?** → GREEN zone, use exploration prompts
2. **Pattern emerging?** → Promote to YELLOW, follow templates
3. **Ready for production?** → RED zone, strict validation
4. **Need help?** → Dashboard shows relevant prompts
5. **Want to remember?** → Knowledge graph captures lessons

## Structure

```
my-ml-mcp-server/
├── app/                    # 7 Streamlit dashboard pages
├── mcp/                    # FastAPI MCP server
├── governance/              # Zone rules (YAML)
├── patterns/                # Reusable ML templates
├── prompts/                 # Curated prompt library
└── knowledge_graph/         # Personal ML knowledge
```
