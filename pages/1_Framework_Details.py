import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
from shared import render_sidebar

st.set_page_config(page_title="Framework Details", page_icon="●")
render_sidebar(use_nav_radio=False)

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

st.divider()
st.header("8-Week Implementation Playbook", divider=True)
st.markdown("""
**Consulting Engagement Model**: Evidence-based transition from M2 (Chaos) to M3 (Agentic)  
**Data Sources**: Assessment (Week 0) → Telemetry (Week 1) → Calibration (Week 2) → Optimization (Weeks 3-8)
""")

# Week 0 Expander
with st.expander("Week 0: Discovery & Baseline Establishment", expanded=False):
    week0_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Pre-engagement assessment, architecture mapping, champion identification",
            "30-question AI Readiness Assessment; Repository file structure analysis; Champion sessions (3-5); Incident history review (90 days)",
            "assessment_baseline.json; champion_profiles.yaml; file_structure_inventory.json; incident_heatmap.json; week0_discovery_report.md",
            "Self-reported entropy: 68/100; Adoption rate: 22%; Champion coverage: 0% (identified but not documented); Red Zone candidates identified",
            "Not deployed",
            "Which 3-5 domains need VTCO first (prioritize by incident frequency)? Initial zone mapping validated against assessment data?"
        ]
    }
    st.dataframe(pd.DataFrame(week0_data), use_container_width=True, hide_index=True)
    st.info("**Critical Questions**: Show me last 3 production incidents—which files? Which folder causes panic if junior edits it? Where do you store API keys?")

st.divider()

# Week 1 Expander
with st.expander("Week 1: Silent Observation (The Learning Week)", expanded=False):
    week1_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Deploy MCP observation mode; Shadow sessions (3 developers, 30 min screen-share each)",
            "violations.jsonl (logged but not enforced); scaffolding_effectiveness.jsonl; Shadow observation notes; Champion availability assessment",
            "violations.jsonl (100+ entries); week1_telemetry_summary.json; observation_notes.md; calibrated_zone_map.yaml; initial_scaffolding_rules.yaml",
            "Actual file touch patterns by role; Premature acceptance rate baseline; Rework indicators (files touched 3+ times/day); Knowledge gap hotspots; True Red Zone identification",
            "ENFORCEMENT_MODE=observation (log only, warn but don't block, maximum scaffolding for all)",
            "Validate complexity caps: Novice 5 (adjust based on 80% success/failure); Confirm Red Zone paths with champions; Set SMART goal baselines for Week 3"
        ]
    }
    st.dataframe(pd.DataFrame(week1_data), use_container_width=True, hide_index=True)

st.divider()

# Week 2 Expander
with st.expander("Week 2: The Switch ⚡ (Critical Enforcement Week)", expanded=False):
    week2_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Enable enforcement; Validate thresholds; Real-time calibration; Daily check-ins",
            "violations.jsonl (enforced: true); escalation_log.jsonl; Daily developer feedback; entropy_log.jsonl (first real measurement)",
            "governance_rules.yaml (updated thresholds); smart_goals_by_role.json; week2_calibration_report.json; mentor_pair_assignments.json; escalation_procedures.md",
            "False positive rate: <10% target; True positive rate (Red Zone violations caught/total attempts); Champion response time: <4 hours; Developer velocity (not drop >20%); Entropy: First post-enforcement measurement",
            "ENFORCEMENT_MODE=enforcement (active blocking); Complexity caps: Novice 3-5 (calibrated), Intermediate 10, Expert 15",
            "Day 1: Are blocks happening? Day 2: Adjust caps up/down; Day 3: Widen/narrow Yellow Zone; Day 4: Validate scaffolding levels; Day 5: Confirm Week 3 SMART goals achievable"
        ]
    }
    st.dataframe(pd.DataFrame(week2_data), use_container_width=True, hide_index=True)
    st.warning("**Critical Success Factor**: <10% false positives AND >80% champion availability. If missed, extend Week 2 or revert to observation.")

st.divider()

# Week 3 Expander
with st.expander("Week 3: VTCO Deep Dive & Role Acceleration", expanded=False):
    week3_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Champion VTCO workshop (2 hours); SMART goal tracking begins; Formal mentor pairing active",
            "Champion domain expertise sessions (recorded); violations.jsonl (pattern analysis); scaffolding_adjustments.jsonl; Shadow follow-ups (2 developers); SMART goal daily tracking",
            "3-5 vtco_[domain].yaml files (complete); tribal_knowledge_index.json; smart_goals_progress.json; mentoring_log.jsonl; promotion_candidates.json",
            "VTCO coverage: 100% of Red Zones; SMART goal achievement: 60% on track; Auto-promotions: 2+ Novices → Intermediate; Champion time: Review hours dropping; Entropy: Continuing downward trend",
            "Full enforcement + VTCO context surfacing (Red Zone blocks show relevant tribal knowledge constraints)",
            "Promote developers with 5 consecutive Green PRs + 0 reverts; Assign mentors for Yellow Zone transitions; Lock VTCO documents v1.0; Adjust scaffolding: Maximum → Moderate for promoted roles"
        ]
    }
    st.dataframe(pd.DataFrame(week3_data), use_container_width=True, hide_index=True)

st.divider()

# Week 4 Expander
with st.expander("Week 4: Integration & M3 Validation", expanded=False):
    week4_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "VTCO integration into MCP workflows; M3 milestone validation; Handoff preparation begins",
            "entropy_log.jsonl (7-day trend); vtco_effectiveness.jsonl; Team satisfaction survey; Velocity metrics (PRs/week, rework rate, time-to-merge)",
            "m3_validation_report.json; governance_handoff_package.zip (initial); governance_rules.yaml (optimized); quarterly_checkin_schedule.ics",
            "Entropy: 68 → <50 (M3 achieved); Adoption: 22% → >50%; Champion innovation time: >50% (was 20%); Red Zone violations: <10/week (was 23/month); VTCO coverage: 100%",
            "Optimized enforcement (scaffolding auto-adjusts based on role progression)",
            "Confirm M3 achievement (continue to Week 8) or extend; Identify M4 candidates; Plan Week 8 exit; Schedule Weeks 5-8 as optimization phase"
        ]
    }
    st.dataframe(pd.DataFrame(week4_data), use_container_width=True, hide_index=True)

st.divider()

# Week 5 Expander
with st.expander("Week 5: Autonomy Scaling", expanded=False):
    week5_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Reduce scaffolding for high performers; Expand Yellow Zone access; Champion-led training",
            "promotion_log.json (role advancements); entropy_log.jsonl; Self-assessment surveys; Training session attendance",
            "autonomy_metrics.json; reduced_scaffolding_rules.yaml; training_materials/; week5_progress_dashboard.json",
            "70% of team with moderate/minimal scaffolding (was 100% maximum); Champion innovation time: >60% (target 65% by Week 8); Entropy: Trending toward 30 (M4 trajectory); Zero regression (no increase in rework/violations)",
            "Predictive (suggests promotions based on patterns, pre-approves routine Green Zone)",
            "Which Intermediates ready for Expert complexity (15)? Which Yellow Zones become Green for specific roles? Can we reduce champion escalation requirements?"
        ]
    }
    st.dataframe(pd.DataFrame(week5_data), use_container_width=True, hide_index=True)

st.divider()

# Week 6 Expander
with st.expander("Week 6: Optimization & Edge Cases", expanded=False):
    week6_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Handle edge cases; Refine VTCOs based on new patterns; Prepare for consultant exit",
            "Edge case log; VTCO update requests; entropy_log.jsonl (volatility check); Regression testing",
            "vtco_v2_updates.yaml; edge_case_playbook.md; optimization_report.json; week6_stability_report.json",
            "Edge cases resolved: <5% of violations; Entropy: Stable or slowly decreasing; Team self-sufficient: Daily ops without consultant; Champion confidence: Self-reported ability to maintain",
            "Stable (no major config changes, monitoring only)",
            "Final VTCO updates before handoff; Confirm no critical consultant dependencies; Validate champions can explain zoning to new hires"
        ]
    }
    st.dataframe(pd.DataFrame(week6_data), use_container_width=True, hide_index=True)

st.divider()

# Week 7 Expander
with st.expander("Week 7: Exit Preparation", expanded=False):
    week7_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Documentation finalization; Runbook testing; Champion authority transfer",
            "Documentation completeness audit; Champion self-assessment; Team survey; Runbook testing (new hire simulation)",
            "final_governance_runbook.md; mcp_maintenance_guide.yaml; new_hire_onboarding.json; exit_checklist.json; 8_week_evidence_package.zip",
            "Champions explain zoning to new hires without consultant help; Team reads MCP logs independently; VTCO update process documented and tested; 7+ days stable autonomous operation",
            "Self-sustaining (champions making adjustments, consultant not touching config)",
            "Exit approval: Champions sign off on readiness; Quarterly check-in dates confirmed (Month 3, 6, 9, 12); Emergency escalation path established"
        ]
    }
    st.dataframe(pd.DataFrame(week7_data), use_container_width=True, hide_index=True)

st.divider()

# Week 8 Expander
with st.expander("Week 8: Consultant Exit", expanded=False):
    week8_data = {
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Final handoff; Exit presentation; Transition to quarterly cadence",
            "Final entropy calculation; Final adoption metrics; 8-week trend analysis (Python dashboard); ROI calculation",
            "8_week_impact_report.json; executive_presentation.pptx; quarterly_checkin_schedule.ics; project_closure_documentation.zip; champion_thank_you_certificates.pdf",
            "Entropy: <40 sustained (M3 confirmed, M4 trajectory); Adoption: >70% (up from 22%); Champion coverage: 100%; Champion innovation time: >65% (up from 20%); Red Zone violations: <5/week (down from 23/month); Team autonomous: 7+ days",
            "Self-sustaining (champion-owned, consultant has read-only access if needed)",
            "Formal consultant exit; Champions fully own VTCO updates and threshold adjustments; Quarterly check-ins scheduled (Month 3, 6, 9, 12); Emergency contact for critical issues only"
        ]
    }
    st.dataframe(pd.DataFrame(week8_data), use_container_width=True, hide_index=True)

st.divider()

# Zoning Matrix
st.header("SDLC Zoning Matrix", divider=True)

zone_data = {
    "Workflow Phase": ["Requirements", "Design", "Implementation", "Testing", "Deployment", "Monitoring"],
    "Sample Task": ["Security compliance", "Database schema", "CRUD operations", "Unit tests", "Production release", "Alert tuning"],
    "Zone": ["RED", "RED", "GREEN", "GREEN", "RED", "RED"],
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
