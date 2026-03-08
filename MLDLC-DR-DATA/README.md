# MLDLC DR Data Decision Intelligence

**Machine Learning Development Lifecycle Governance Framework**

Transparent | Explainable | Auditable | Traceable

## Overview

This framework establishes comprehensive governance for ML/data initiatives at DR Data Decision Intelligence, integrating:

- **VTCO Methodology**: Verb-Task-Constraint-Outcome structured approach
- **Risk Matrix**: RED/YELLOW/GREEN classification
- **Schema Validation**: JSON schema enforcement
- **Lineage Tracking**: Full data lineage
- **Audit Logging**: Complete audit trail

## Quick Start

### 1. Setup

```bash
cd MLDLC-DR-DATA
pip install -r requirements.txt
cp .env.example .env
```

### 2. Start MCP Server (for Cursor)

```bash
python run_mcp_stdio.py
```

### 3. Start Streamlit Dashboard

```bash
streamlit run app/main.py
```

## Cursor Integration

Add to Cursor MCP settings (Settings → MCP). Use full path to `run_mcp_stdio.py` and set `cwd` to this project directory.

## VTCO Methodology

Every task follows VTCO:

```
VERB:       [Create | Update | Delete | Analyze | Validate | Deploy]
TASK:       [Specific description]
CONSTRAINT: [Limitations and requirements]
OUTCOME:    [Expected result]
```

## Risk Matrix

| Level | Score | Requirements |
|-------|-------|--------------|
| 🔴 RED | 9-12 | Explicit approval, full docs, security review |
| 🟡 YELLOW | 5-8 | Manager review, documentation, testing |
| 🟢 GREEN | 1-4 | Standard process, basic docs |

## MCP Tools

- `define_vtco`: Define VTCO task
- `assess_risk`: Assess risk level
- `validate_artifact`: Validate against schema
- `record_lineage`: Record transformation
- `get_lineage`: Query lineage
- `log_audit_event`: Log audit event

## Structure

```
MLDLC-DR-DATA/
├── .cursor/          # Cursor rules and MCP config
├── app/              # Streamlit dashboard
├── governance/       # Risk matrix, workflows, policies
├── schemas/          # JSON schemas
├── process/          # VTCO definitions
├── mldlc_server/     # MCP server (stdio)
├── data/             # Lineage, audit, cache
└── docs/             # Documentation
```

## License

MIT License - DR Data Decision Intelligence
