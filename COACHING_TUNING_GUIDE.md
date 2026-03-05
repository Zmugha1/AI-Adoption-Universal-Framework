# Coaching Interaction Logging & Tuning Guide

## How It Works

### 1. Interaction Flow

```
Developer asks question
        │
        ▼
┌───────────────────────┐
│ check_zoning_permission│  ──► coaching_request (file_path, role, zone, query, intent)
└───────────────────────┘
        │
        ▼
┌───────────────────────┐
│ get_tribal_knowledge   │  ──► pattern_referenced (domain, pattern, zone)
└───────────────────────┘
        │
        ▼
┌───────────────────────┐
│ AI provides coaching   │  ──► coaching_provided (coaching_type, patterns, lines_generated)
└───────────────────────┘
        │
        ▼
┌───────────────────────┐
│ Developer responds     │  ──► coaching_accepted | coaching_modified | coaching_rejected
└───────────────────────┘
```

### 2. What Gets Logged

| Event | Data Captured |
|-------|---------------|
| **coaching_request** | file_path, zone, developer_role, query (anonymized), intent, has_mentor |
| **pattern_referenced** | domain, pattern name, zone, developer_role |
| **coaching_provided** | file_path, zone, coaching_type, patterns_referenced, code_generated, lines_generated, validation_checklist |
| **coaching_accepted** | file_path, outcome, lines_accepted, lines_modified, time_to_decision_seconds, mentor_consulted |
| **coaching_modified** | same as accepted |
| **coaching_rejected** | same as accepted |

### 3. How to Test

```bash
# Generate sample coaching interactions
python test_coaching_interactions.py

# Analyze metrics and get tuning insights
python analyze_coaching_metrics.py
```

### 4. Metrics for Tuning

| Metric | What It Tells You | Tuning Action |
|--------|-------------------|---------------|
| **Acceptance rate** | % of suggestions kept | Low → reduce verbosity, improve pattern relevance |
| **Rejection rate** | % of suggestions discarded | High → check if coaching type matches intent |
| **Pattern usage** | Which VTCOs are accessed | Underused → surface earlier; overused → may be redundant |
| **Zone distribution** | Red vs Yellow vs Green activity | Red-heavy → ensure suggest_only is clear |
| **Mentor involvement** | Outcomes with mentor_consulted | Track novice progression |
| **Lines generated** | Code output volume | High in Red zone → may be over-generating |
| **Intent vs outcome** | code_generation vs explanation | Mismatch → improve intent inference |

### 5. Tuning Levers

1. **Verbosity by role** (governance_rules.yaml)
   - `novice: verbosity: maximum` → reduce if acceptance drops
   - `expert: verbosity: minimal` → increase if rejection rises

2. **Pattern surfacing**
   - Log when `get_tribal_knowledge` is called
   - If pattern_referenced is low for Yellow zone → AI may not be fetching patterns

3. **Intent inference** (mcp_server.py `_infer_intent`)
   - Add keywords for better classification
   - Use intent to adjust coaching_type (explanation vs code_generation)

4. **Outcome logging**
   - Currently manual: AI layer must call `log_coaching_outcome()` when user accepts/modifies/rejects
   - Future: Integrate with Cursor/IDE to detect edit events

### 6. Log Location

- **Path:** `.ai-governance/coaching_log.jsonl`
- **Format:** JSON Lines (one JSON object per line)
- **Gitignored:** Yes (runtime data)

### 7. Sample Log Entry

```json
{
  "timestamp": "2026-03-04T22:53:27.385086Z",
  "event_type": "coaching_request",
  "session_id": "73c78edd",
  "governance_context": {
    "role": "novice",
    "mentor": null,
    "repo_path": "/path/to/repo"
  },
  "data": {
    "file_path": "src/api/auth/login.py",
    "zone": "Yellow",
    "developer_role": "Novice",
    "query": "[anonymized]",
    "intent": "code_generation",
    "has_mentor": true
  }
}
```
