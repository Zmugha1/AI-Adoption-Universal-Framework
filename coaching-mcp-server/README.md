# Coaching MCP Server

Teaches you **WHY**, validates against industry standards, and helps build production-ready ML systems.

## Quick Start

```bash
pip install -r requirements.txt

# Start MCP server (port 8001)
uvicorn coaching_server.server:app --reload --port 8001

# Launch dashboard (separate terminal)
streamlit run app/main.py
```

## What's Included

### Explanation Database (WHY)
- `random_state` — Reproducibility foundation
- `pipelines` — Data leakage prevention
- `cross_validation` — Why single splits lie
- `experiment_tracking` — External ML brain

### Diagnostic Database
- `model_underperforming` — 5-step diagnostic
- `overfitting` — Learning curves → regularization

### Anti-Patterns
- `data_leakage` — Wrong vs correct code
- `missing_random_state` — Reproducibility

### Code Validation
- Missing `random_state` → HIGH
- No Pipeline → CRITICAL (leakage risk)
- No MLflow → WARNING

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/explain` | POST | Get WHY explanation for topic |
| `/explain/topics` | GET | List explanation topics |
| `/validate-code` | POST | Production readiness check |
| `/diagnose` | POST | Diagnostic workflow for symptom |
| `/anti-pattern` | POST | Anti-pattern details |
| `/prompts` | GET | Coaching prompt library |

## Dashboard Pages

1. **Why Explainer** — Understand WHY patterns exist
2. **Diagnostic Lab** — Systematic debugging
3. **Standards Ref** — Industry best practices
4. **Code Review** — AI-powered validation
5. **Tradeoff Analysis** — Alternatives with pros/cons
6. **Anti-Patterns** — Common pitfalls
7. **Production Check** — Pre-deployment validation
8. **Learning Path** — Coaching prompts by category
