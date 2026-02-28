import streamlit as st
import pandas as pd

st.set_page_config(page_title="Framework Details", page_icon="📚")

st.title("Framework Components")

# Maturity Model Deep Dive
st.header("M1-M4 Maturity Model", divider=True)

maturity_data = {
    "Level": ["M1 Chaos", "M2 Shallow", "M3 Agentic", "M4 Autonomous"],
    "Color": ["Gray", "Orange", "Blue", "Gold"],
    "Adoption": ["0-15%", "20-40%", "60-85%", "85%+"],
    "Entropy": ["Unknown/75+", "60-75", "30-45", "<20"],
    "Key Problem": ["No licenses/usage", "Licenses but no governance", "High adoption needs guardrails", "Mature optimization"],
    "Consultant Role": ["Assess + Champion ID", "Workshop + MCP Setup", "Calibrate + Optimize", "Quarterly check-in only"],
    "MCP Role": ["Audit mode only", "Zone enforcement active", "Full SMART goals", "Predictive modeling"],
    "Champion Role": ["Identified but no authority", "Documentation begins", "Full authority established", "Strategic oversight"]
}

st.dataframe(pd.DataFrame(maturity_data), use_container_width=True)

# Zoning Matrix
st.header("SDLC Zoning Matrix", divider=True)

zone_data = {
    "Workflow Phase": ["Requirements", "Design", "Implementation", "Testing", "Deployment", "Monitoring"],
    "Sample Task": ["Security compliance", "Database schema", "CRUD operations", "Unit tests", "Production release", "Alert tuning"],
    "Zone": ["🔴 Red", "🔴 Red", "🟢 Green", "🟢 Green", "🔴 Red", "🔴 Red"],
    "JTA Elements": ["Critical thinking", "Pattern recognition", "Tool proficiency", "Attention to detail", "Risk assessment", "Impact analysis"],
    "VTCO Doc": ["Verb: Elicit", "Verb: Architect", "Verb: Implement", "Verb: Validate", "Verb: Release", "Verb: Tune"],
    "Who Decides": ["Champion", "Champion", "Developer (Green)", "Developer (Green)", "Champion", "Champion"],
    "MCP Enforces": ["Block edits", "Block edits", "Complexity limit", "Coverage check", "Block edits", "Block edits"]
}

st.dataframe(pd.DataFrame(zone_data), use_container_width=True)

# Role Skills Matrix
st.header("Role-Based Skills & SMART Goals", divider=True)

skills_data = {
    "Role": ["Novice", "Intermediate", "Expert", "Champion"],
    "Zone Permissions": ["Green full, Yellow mentored, Red read-only", "Green/Yellow full, Red suggest", "All zones draft proposals", "All zones owns Red decisions"],
    "SMART Goal Example": ["10 Green tasks, complexity <5 in 4 weeks", "Zero reverts 30 days, 1 Yellow validation", "Mentor 2 Novices, draft Red proposal", "Document 3 VTCOs, enable 2 promotions"],
    "MCP Scaffolding": ["Maximum: Explain every line", "Moderate: Key decisions only", "Minimal: Architecture focus", "Consultative: Strategic oversight"],
    "Promotion Criteria": ["10 PRs under complexity 5", "0 reverts, mentor approval", "Successful mentees", "Tribal knowledge documented"]
}

st.dataframe(pd.DataFrame(skills_data), use_container_width=True)

# MCP Configuration
st.header("MCP Server Configuration", divider=True)

st.markdown("""
```yaml
# .ai-governance/mcp-server/config.yml
mcp_server:
  version: 1.0
  
  assessment_integration:
    source: "./assessment-results/baseline.json"
    auto_configure_zones: true
    auto_configure_skills: true
  
  zoning:
    red_zone_paths: ["src/payment/**", "src/security/**"]
    yellow_zone_paths: ["src/api/**", "tests/integration/**"]
    green_zone_paths: ["src/utils/**", "tests/unit/**"]
    
  skill_matrix:
    profiles_path: "./skill-matrix/profiles.yml"
    auto_promote: true
    promotion_criteria:
      complexity_threshold: 5
      revert_rate_max: 0.05
      
  entropy_tracking:
    enabled: true
    metrics: ["bloat", "rework", "reverts", "premature_acceptance"]
```
""")

st.info("""
**MCP Limitations & Champion Agency:**

The MCP server CANNOT:
- Know business priority (champions decide "this hotfix is worth it")
- Write tribal knowledge (champions author VTCO)
- Judge promotion readiness (champions validate)
- Build trust with resistant developers (champions mentor)
- Override emergencies (champions have governance override)

The MCP server CAN:
- Block unauthorized Red Zone edits
- Adjust AI verbosity by skill level
- Count entropy metrics automatically
- Remind of constraints at moment of need
- Enforce complexity limits
""")
