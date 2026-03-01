"""Implementation Playbook - 8-Week AI Governance Framework (nav page)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.title("8-Week AI Governance Implementation Framework")
st.subheader("Evidence-Based Consulting Delivery")

st.markdown("""
**Engagement Model**: 8-week intensive with quarterly check-ins thereafter  
**Baseline**: M2 (Chaos/Shallow) → **Target**: M3 (Agentic) by Week 4, M4 trajectory by Week 8  
**Core Method**: Structured data collection → Observation calibration → Enforcement optimization → Consultant exit
""")

st.divider()

# Week 0
with st.expander("Week 0: Discovery & Baseline Establishment", expanded=False):
    week0_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Pre-engagement assessment and architecture mapping",
            "AI Readiness Assessment (30 questions) → assessment_baseline.json; Repo file structure → file_structure_inventory.json; Champion interviews → champion_profiles.yaml; Incident history → incident_heatmap.json",
            "assessment_baseline.json, champion_profiles.yaml, file_structure_inventory.json, week0_discovery_report.md",
            "Self-reported entropy: 68/100 (typical M2); Adoption rate: 22%; Champion coverage: 0%; Red Zone candidates from incident analysis",
            "Not deployed",
            "Which 3-5 domains need VTCO first? Initial zone mapping validated? Champion availability confirmed for Week 1?"
        ]
    })
    st.dataframe(week0_data, use_container_width=True, hide_index=True)
    st.info("**Key Questions**: Show me last 3 production incidents... Which folder causes panic if junior edits it?")

st.divider()

# Week 1
with st.expander("Week 1: Silent Observation (The Learning Week)", expanded=False):
    week1_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Deploy MCP in observation mode + Conduct shadow sessions (3 developers, 30 min screen-share each)",
            "violations.jsonl; scaffolding_effectiveness.jsonl; Shadow observation notes; Champion availability assessment",
            "violations.jsonl (100+ entries); week1_telemetry_summary.json; observation_notes.md; calibrated_zone_map.yaml; initial_scaffolding_rules.yaml (Novice 5, Intermediate 10, Expert 15)",
            "Actual file touch patterns; Premature acceptance rate baseline; Rework indicators; Knowledge gap hotspots; True Red Zone identification",
            "ENFORCEMENT_MODE=observation (log only, warn but don't block, maximum scaffolding for all)",
            "Validate complexity caps; Confirm Red Zone paths with champions; Set SMART goal baselines; Go/No-Go: Telemetry logging correctly? Champions available?"
        ]
    })
    st.dataframe(week1_data, use_container_width=True, hide_index=True)
    st.info("**Key Insight**: We don't guess—Week 1 observation validates Week 0 interview assumptions.")

st.divider()

# Week 2
with st.expander("Week 2: The Switch (Critical Enforcement Week) ⚡", expanded=False):
    week2_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Enable enforcement, validate thresholds, real-time calibration",
            "violations.jsonl (enforced: true); Daily developer feedback; entropy_log.jsonl; Champion escalation log",
            "governance_rules.yaml; smart_goals_by_role.json; week2_calibration_report.json; mentor_pair_assignments.json; escalation_procedures.md",
            "False positive rate: <10%; Champion response: <4 hours; Developer velocity: no drop >20%; Entropy: first measurement post-enforcement",
            "ENFORCEMENT_MODE=enforcement (active blocking), complexity caps calibrated from Week 1",
            "Daily calibration: blocks, complexity caps, Yellow Zone, scaffolding levels. **Critical**: <10% false positive + >80% champion availability or extend/revert."
        ]
    })
    st.dataframe(week2_data, use_container_width=True, hide_index=True)
    st.warning("**Evidence-based calibration**: Week 2 thresholds come from Week 1 telemetry, not arbitrary numbers.")

st.divider()

# Week 3
with st.expander("Week 3: VTCO Deep Dive & Role Acceleration", expanded=False):
    week3_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Champion VTCO workshop (2 hours), SMART goal tracking begins, formal mentor pairing",
            "Champion domain expertise interviews; violations.jsonl pattern analysis; scaffolding_adjustments.jsonl; Shadow follow-ups; SMART goal tracking",
            "3-5 vtco_[domain].yaml files; tribal_knowledge_index.json; smart_goals_progress.json; mentoring_log.jsonl; promotion_candidates.json",
            "VTCO coverage: 100% of Red Zones; SMART goal achievement: 60% on track; Auto-promotions: 2+ Novices → Intermediate; Entropy: continuing downward",
            "Full enforcement + VTCO context surfacing (show relevant VTCO when Red Zone blocked)",
            "Promote developers with 5 consecutive Green PRs, 0 reverts; Assign mentors for Yellow Zone; Lock VTCO v1.0; Adjust scaffolding for promoted"
        ]
    })
    st.dataframe(week3_data, use_container_width=True, hide_index=True)
    st.info("**Tribal knowledge protection**: VTCOs drafted Week 1-3, actively governing Week 4+.")

st.divider()

# Week 4
with st.expander("Week 4: Integration & M3 Validation", expanded=False):
    week4_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "VTCO integration into MCP workflows, M3 milestone validation, handoff preparation begins",
            "entropy_log.jsonl (7-day trend); vtco_effectiveness.jsonl; Team satisfaction survey; Velocity metrics",
            "m3_validation_report.json; governance_handoff_package.zip; governance_rules.yaml (optimized); quarterly_checkin_schedule.ics",
            "M3 Checklist: Entropy 68→<50; Adoption 22%→>50%; Champion innovation >50%; Red Zone violations <10/week; VTCO coverage 100%",
            "Optimized enforcement (scaffolding auto-adjusts by role progression)",
            "Confirm M3 achievement or extend; Identify M4 candidates; Plan Week 8 exit"
        ]
    })
    st.dataframe(week4_data, use_container_width=True, hide_index=True)
    st.success("**M3 Milestone**: Entropy <50, Adoption >50%, Champion innovation time >50%.")

st.divider()

# Week 5
with st.expander("Week 5: Autonomy Scaling", expanded=False):
    week5_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Reduce scaffolding for high performers, expand Yellow Zone access, champion-led training",
            "promotion_log.json; entropy_log.jsonl; Self-assessment surveys; Training session attendance",
            "autonomy_metrics.json; reduced_scaffolding_rules.yaml; training_materials/; week5_progress_dashboard.json",
            "70% of team with moderate/minimal scaffolding; Champion innovation >60%; Entropy trending toward 30 (M4); Zero regression",
            "Predictive (suggests promotions, pre-approves routine Green Zone edits)",
            "Which Intermediates ready for Expert (complexity 15)? Which Yellow → Green for high performers?"
        ]
    })
    st.dataframe(week5_data, use_container_width=True, hide_index=True)
    st.info("**Graduated autonomy**: SMART goals Week 3-5 prove scaffolding reduces as competence increases.")

st.divider()

# Week 6
with st.expander("Week 6: Optimization & Edge Cases", expanded=False):
    week6_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Handle edge cases, refine VTCOs based on new patterns, prepare for consultant exit",
            "Edge case log; VTCO update requests; entropy_log.jsonl (volatility check); Regression testing",
            "vtco_v2_updates.yaml; edge_case_playbook.md; optimization_report.json; week6_stability_report.json",
            "Edge cases resolved: <5%; Entropy: stable; Team self-sufficient; Champion confidence in maintaining system",
            "Stable (no major config changes, monitoring only)",
            "Final VTCO updates; Confirm no critical consultant dependencies; Champions can explain zoning to new hires"
        ]
    })
    st.dataframe(week6_data, use_container_width=True, hide_index=True)

st.divider()

# Week 7
with st.expander("Week 7: Exit Preparation", expanded=False):
    week7_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Documentation finalization, runbook testing, champion authority transfer",
            "Documentation completeness audit; Champion self-assessment; Team survey; Runbook testing (new hire simulation)",
            "final_governance_runbook.md; mcp_maintenance_guide.yaml; new_hire_onboarding.json; exit_checklist.json; 8_week_evidence_package.zip",
            "Champions explain zoning to new hires; Team reads MCP logs independently; VTCO update process documented; 7+ days stable autonomous operation",
            "Self-sustaining (consultant not touching config, champions making adjustments)",
            "Exit approval: Champions sign off; Quarterly check-in dates confirmed; Emergency escalation path defined"
        ]
    })
    st.dataframe(week7_data, use_container_width=True, hide_index=True)

st.divider()

# Week 8
with st.expander("Week 8: Consultant Exit", expanded=False):
    week8_data = pd.DataFrame({
        "Category": ["Activity", "Data Inputs", "Deliverables", "Evidence/Metrics", "MCP Mode", "Key Decisions"],
        "Details": [
            "Final handoff, exit presentation, transition to quarterly cadence",
            "Final entropy calculation; Final adoption metrics; 8-week trend analysis; ROI calculation",
            "8_week_impact_report.json; executive_presentation.pptx; quarterly_checkin_schedule.ics; project_closure_documentation.zip",
            "Final State: Entropy <40 sustained; Adoption >70%; Champion coverage 100%; Champion innovation >65%; Red Zone violations <5/week",
            "Self-sustaining (champion-owned, consultant read-only if needed)",
            "Formal consultant exit; Champions own VTCO updates; Quarterly check-ins (Month 3, 6, 9, 12); Emergency contact for critical issues only"
        ]
    })
    st.dataframe(week8_data, use_container_width=True, hide_index=True)
    st.success("**Measurable exit**: Week 8 exit criteria are logged metrics, not feelings.")

st.divider()

# Key Narrative Points
st.header("Key Narrative Points", divider=True)
col1, col2 = st.columns(2)
with col1:
    st.info("**We don't guess**: Week 1 observation validates Week 0 interview assumptions.")
    st.info("**Tribal knowledge protection**: VTCOs drafted Week 1-3, actively governing Week 4+.")
with col2:
    st.info("**Evidence-based calibration**: Week 2 thresholds come from Week 1 telemetry, not arbitrary numbers.")
    st.info("**Graduated autonomy**: SMART goals Week 3-5 prove scaffolding reduces as competence increases.")
st.info("**Measurable exit**: Week 8 exit criteria are logged metrics, not feelings.")

st.divider()

# Data Flow Diagram
st.header("Data Flow Diagram", divider=True)
st.code("""
Week 0-1: Interview Data + MCP Telemetry → Calibrated Zone Map
Week 2-3: Violation Logs + Champion Feedback → Adjusted Thresholds + VTCOs
Week 4+:  Entropy Logs + VTCO Effectiveness → Optimized Governance + M3 Validation
""", language=None)

st.divider()

# File Type Reference
st.header("File Type Reference", divider=True)
file_ref = pd.DataFrame({
    "File Type": ["Assessment Data", "Champion Profiles", "VTCO Docs", "Governance Rules", "Violation Logs", "Entropy Logs", "Progress Reports"],
    "Extension": [".json", ".yaml", ".yaml", ".yaml", ".jsonl", ".jsonl", ".json"],
    "Written By": ["Consultant", "Consultant", "Champions", "Consultant", "MCP Server", "MCP Server", "Python Script"],
    "Read By": ["Python Dashboard", "MCP Server", "MCP Server", "MCP Server", "Consultant", "Python Dashboard", "Client"],
    "Purpose": ["Baseline metrics", "Role assignments", "Tribal knowledge", "Zoning config", "Telemetry", "Health metrics", "Week-by-week status"]
})
st.dataframe(file_ref, use_container_width=True, hide_index=True)

st.divider()

# Download Button
st.header("Export Framework", divider=True)
framework_export = {
    "title": "8-Week AI Governance Implementation Framework",
    "version": "1.0",
    "generated": datetime.now().isoformat(),
    "engagement_model": "8-week intensive with quarterly check-ins",
    "baseline": "M2 (Chaos/Shallow)",
    "target": "M3 (Agentic) by Week 4, M4 trajectory by Week 8",
    "weeks": [
        {"week": 0, "name": "Discovery & Baseline", "mcp_mode": "Not deployed"},
        {"week": 1, "name": "Silent Observation", "mcp_mode": "observation"},
        {"week": 2, "name": "The Switch", "mcp_mode": "enforcement"},
        {"week": 3, "name": "VTCO Deep Dive", "mcp_mode": "enforcement + VTCO"},
        {"week": 4, "name": "M3 Validation", "mcp_mode": "optimized"},
        {"week": 5, "name": "Autonomy Scaling", "mcp_mode": "predictive"},
        {"week": 6, "name": "Optimization", "mcp_mode": "stable"},
        {"week": 7, "name": "Exit Preparation", "mcp_mode": "self-sustaining"},
        {"week": 8, "name": "Consultant Exit", "mcp_mode": "self-sustaining"}
    ],
    "data_flow": {
        "week_0_1": "Interview Data + MCP Telemetry → Calibrated Zone Map",
        "week_2_3": "Violation Logs + Champion Feedback → Adjusted Thresholds + VTCOs",
        "week_4_plus": "Entropy Logs + VTCO Effectiveness → Optimized Governance + M3 Validation"
    },
    "file_types": file_ref.to_dict(orient="records")
}
st.download_button(
    label="📥 Download Full Framework as JSON",
    data=json.dumps(framework_export, indent=2),
    file_name="8_week_implementation_framework.json",
    mime="application/json",
    use_container_width=False
)
