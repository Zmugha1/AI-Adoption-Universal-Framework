# MCP Server Demo Guide

## Pre-Demo Checklist
- [ ] Run: `python setup_mcp_cursor.py`
- [ ] Verify Cursor shows green dot for "ai-governance" MCP
- [ ] Start Streamlit: `streamlit run app.py`
- [ ] Have Cursor ready in separate window

## Demo Flow (5 minutes)

### 1. Streamlit Assessment (1 min)
- Open http://localhost:8501
- Page 1: Show Maturity Matrix (M2 baseline)
- Scroll to Pre-Project Kickoff section
- "This is the workshop deliverable"

### 2. Cursor Integration (2 min)
- Switch to Cursor
- Open Composer/Chat (Ctrl/Cmd+I)
- Type: `Check if I can edit migrations/schema.sql as a Novice`
- Show the BLOCKED response
- Point out the VTCO context surfaced

### 3. Demo Scenario (1 min)
- Type: `Run the demo_red_zone_scenario`
- Walk through the 8-step timeline
- Highlight: "Production incident prevented, 4min downtime avoided"

### 4. Logs (30 sec)
- Show `.ai-governance/violations.jsonl`
- "Every blocked edit is logged for audit"

### 5. Closing (30 sec)
- "That's the Technical Enforcer protecting the workshop outputs"

## Cursor MCP Test Commands

1. **Zone Check (Green)**:
   ```
   Check zoning for file_path="src/utils/helpers.py", user_role="Novice", complexity_score=2
   ```
   Expected: Green Zone approved

2. **Red Zone Block**:
   ```
   Check zoning for file_path="migrations/dangerous.sql", user_role="Novice"
   ```
   Expected: Blocked with VTCO context

3. **Entropy Calc**:
   ```
   Calculate entropy with bloat_percent=10, rework_percent=15, revert_percent=5, premature_acceptance_percent=8
   ```
   Expected: Score ~9.4, M4 level

4. **Demo Scenario**:
   ```
   Run demo_red_zone_scenario
   ```

## Troubleshooting

**Server not showing in Cursor:**
- Cmd/Ctrl+Shift+P -> "Developer: Reload Window"
- Check View -> Output -> "MCP" channel

**"Python not found":**
- Edit mcp.json to use full Python path
- Find with: `which python` (Mac/Linux) or `where python` (Windows)

**Import errors:**
- Run: `pip install -r requirements-mcp.txt`
