"""
Week 1→2 Strategic Decision Intelligence
Transforms Week 1 telemetry into actionable Week 2 configurations.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
from shared import render_sidebar

st.set_page_config(page_title="Strategic Planning | Week 1→2", page_icon="🧠", layout="wide")
render_sidebar(use_nav_radio=False)

st.title("Week 1→2 Strategic Decision Intelligence")
st.subheader("From Telemetry to Transformation: Evidence-Based Transition Planning")

st.markdown("""
**Consulting Homework**: Between Week 1 (Observation) and Week 2 (Enforcement)  
**Objective**: Transform 127 data points into calibrated governance configuration  
**Output**: Signed-off `week2_governance_configuration.yaml`
""")

st.divider()

# =============================================================================
# Section 1: Time-to-Maturity Forecasting Model
# =============================================================================
st.header("1. Time-to-Maturity Forecasting Model", divider=True)

forecast_col1, forecast_col2 = st.columns([2, 1])

with forecast_col1:
    st.markdown("### Week 1 Baseline Validation")
    st.info("""
    **Self-Assessment (Week 0)**: Entropy 68, M2 Chaos  
    **Actual Measurement (Week 1)**: Entropy 20.4, M2.3 Stabilizing  
    **Observation Effect**: 47.6 point drop without enforcement
    """)

    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8']
    entropy_projection = [20.4, 28.0, 22.0, 18.0, 15.5, 13.0, 11.5, 10.0]
    adoption_projection = [35, 45, 55, 65, 72, 78, 82, 85]

    forecast_df = pd.DataFrame({
        'Week': weeks,
        'Entropy (Target <30)': entropy_projection,
        'Adoption % (Target >60)': adoption_projection
    })

    st.line_chart(forecast_df.set_index('Week'))
    st.caption("Week 2 entropy spike expected (enforcement friction), then rapid decay")

with forecast_col2:
    st.markdown("### Risk-Adjusted Timeline")

    risk_scenarios = {
        "Scenario": ["Best Case", "Expected", "Risk-Adjusted"],
        "Week 4 M3?": ["Yes (Low friction)", "Yes (Normal)", "No (+1 week)"],
        "Week 8 M4?": ["Yes", "Trajectory set", "M3 sustained only"],
        "Key Risk": ["None", "False positives <10%", "Champion availability <80%"]
    }

    st.dataframe(pd.DataFrame(risk_scenarios), use_container_width=True, hide_index=True)

    st.warning("""
    **Critical Path**: If Week 2 false positives >10% OR champion response >8hrs,
    timeline extends by 1-2 weeks. Monitor daily in Week 2.
    """)

st.divider()

# =============================================================================
# Section 2: Entropy Reduction Driver Analysis
# =============================================================================
st.header("2. Entropy Reduction Driver Analysis", divider=True)

st.markdown("""
**Week 1 Entropy Decomposition**: 20.4 total  
Formula: (Bloat×0.25) + (Rework×0.25) + (Reverts×0.20) + (Premature×0.30)
""")

drivers_data = {
    "Driver": ["Bloat", "Rework", "Reverts", "Premature Acceptance"],
    "Current %": [5.2, 6.8, 3.1, 5.3],
    "Target %": [2.0, 3.5, 2.0, 3.0],
    "Week 2 Scaffolding Fix": [
        "Force lint-check before AI accept",
        "10-min cooling off period before re-edit",
        "Preview impact visualization",
        "3-sec mandatory delay + comprehension check"
    ],
    "Expected Impact": ["-3.2 pts", "-3.3 pts", "-1.1 pts", "-2.3 pts"],
    "Total Entropy Reduction": ["", "", "", "-9.9 pts (Target: 10.4)"]
}

st.dataframe(pd.DataFrame(drivers_data), use_container_width=True, hide_index=True)

st.success("""
**Calibrated Approach**: Week 2 scaffolding targets specific entropy drivers,
not blanket restrictions. Each intervention mapped to metric impact.
""")

st.divider()

# =============================================================================
# Section 3: Adoption Acceleration Psychology
# =============================================================================
st.header("3. Adoption Acceleration: Psychology-Driven Scaffolding", divider=True)

psych_col1, psych_col2 = st.columns(2)

with psych_col1:
    st.markdown("### Week 1 Behavioral Insight")

    insights = {
        "Observed Behavior": [
            "23.6% explanation read rate",
            "Developers click past warnings",
            "Novices fear asking for help",
            "Champion approval = trust signal"
        ],
        "Root Cause": [
            "Information overload",
            "Friction without value",
            "Competence signaling anxiety",
            "Social proof authority"
        ],
        "Week 1 Failure": [
            "Maximum verbosity ignored",
            "Passive warnings ineffective",
            "Isolation in decision-making",
            "Undocumented tribal knowledge"
        ]
    }

    st.dataframe(pd.DataFrame(insights), use_container_width=True, hide_index=True)

with psych_col2:
    st.markdown("### Week 2 Scaffolding Redesign")

    redesign = {
        "Design Principle": [
            "Competence Signaling",
            "Loss Aversion",
            "Champion Halo",
            "Interactive Acknowledgment"
        ],
        "Implementation": [
            "Frame as 'optimization tips' not 'training'",
            "'Protecting your time from rework' messaging",
            "VTCO author prominently displayed",
            "3-sec countdown + 'I understand' checkbox"
        ],
        "Expected Outcome": [
            "40% → 65% engagement",
            "Perceived autonomy preserved",
            "Trust in governance system",
            "Comprehension verified, not assumed"
        ]
    }

    st.dataframe(pd.DataFrame(redesign), use_container_width=True, hide_index=True)

st.divider()

# =============================================================================
# Section 4: Individual Preference Profiling
# =============================================================================
st.header("4. Individual Preference Profiling Survey", divider=True)

st.markdown("""
**Week 1 Day 5 Deployment**: 15-minute developer survey → Personalized scaffolding profiles  
**Goal**: Move from role-based (Novice/Intermediate/Expert) to individual-optimized scaffolding
""")

survey_questions = {
    "Question Category": [
        "Learning Style",
        "Cognitive Load",
        "Risk Tolerance",
        "Help-Seeking Preference",
        "Context Preference"
    ],
    "Question": [
        "When stuck, I prefer: (a) Read docs (b) Watch video (c) Ask colleague (d) Trial/error",
        "Concurrent tasks I handle: (a) 1 (b) 2-3 (c) 4+",
        "Comfort with production edits: (a) Never (b) With approval (c) If tests pass (d) YOLO",
        "I ask for help: (a) Immediately (b) After 30 min (c) After 2 hours (d) Never",
        "I want AI to be: (a) Conservative/safe (b) Balanced (c) Aggressive/innovative (d) Silent"
    ],
    "Maps To": [
        "Scaffolding format: text/visual/interactive/sandbox",
        "Interruption frequency: rare/occasional/frequent",
        "Red Zone override: emergency/standard/pre-approved",
        "Proactive mentor assignment trigger threshold",
        "Complexity cap adjustment: -2/+0/+2/+4 from baseline"
    ],
    "Output File": [
        "individual_profiles.json['learning_format']",
        "individual_profiles.json['interruption_tolerance']",
        "individual_profiles.json['risk_profile']",
        "individual_profiles.json['help_seeking']",
        "individual_profiles.json['complexity_bias']"
    ]
}

st.dataframe(pd.DataFrame(survey_questions), use_container_width=True, hide_index=True)

st.info("""
**Personalization Logic**: Developer UUID → Load profile → Adjust scaffolding dynamically  
**Example**: Developer selects "Watch video" + "Conservative" → Video-format explanations, complexity cap -2 from role baseline
""")

st.divider()

# =============================================================================
# Section 5: Edge Case Identification & Protocols
# =============================================================================
st.header("5. Edge Case Identification & Handling Protocols", divider=True)

edge_cases = {
    "Edge Case": [
        "The 'Gray Zone' File",
        "Emergency Override (2 AM)",
        "Role Transition Confusion",
        "Ghost Champion (departure)",
        "False Positive Spike",
        "Adoption Drop >30%"
    ],
    "Week 1 Signal": [
        "3 developers confused about zone boundary",
        "N/A (not yet enforced)",
        "N/A (promotions not yet active)",
        "N/A (contingency planning)",
        "0% observed (validated)",
        "N/A (monitoring trigger)"
    ],
    "Week 2 Protocol": [
        "Most restrictive wins + explicit messaging",
        "3-Champion Slack approval + auto-ADR + 48hr revoke",
        "'You're now Expert level' confirmation dialog ×3",
        "VTCO complete by Week 3 + second champion shadow",
        "Immediate rollback to observation + pattern review",
        "Revert to Week 1 thresholds + extend timeline"
    ],
    "Owner": [
        "Champion (zone definition)",
        "On-call champion rotation",
        "Engineering Manager",
        "Consultant (succession planning)",
        "Consultant + Tech Lead",
        "Executive sponsor"
    ],
    "Escalation": [
        "Architecture review board",
        "Emergency incident protocol",
        "Peer confirmation required",
        "Hiring freeze + knowledge extraction",
        "Daily war room until resolved",
        "Stakeholder notification"
    ]
}

st.dataframe(pd.DataFrame(edge_cases), use_container_width=True, hide_index=True)

st.divider()

# =============================================================================
# Section 6: Configuration Sign-Off Document
# =============================================================================
st.header("6. Dashboard & MCP Configuration Sign-Off", divider=True)

st.markdown("""
**Document**: `week2_governance_configuration.yaml`  
**Process**: Automated draft → Champion review → Team vote → Digital signature
""")

sign_off_sections = {
    "Configuration Section": [
        "Zone Boundaries",
        "Complexity Caps",
        "Scaffolding Rules",
        "Escalation SLAs",
        "VTCO Authorship",
        "Individual Profiles"
    ],
    "Current Proposal": [
        "Red: migrations/, payment/, security/, config/prod",
        "Novice: 5, Intermediate: 10, Expert: 15, Champion: 20",
        "Mandatory acknowledgment: true, Delay: 3s, Length: moderate",
        "Red Zone: 4hrs, Yellow Zone: 24hrs, After-hours: rotation",
        "3 VTCOs drafted, 2 pending champion validation",
        "Survey deployed Week 1 Day 5, results pending"
    ],
    "Evidence From Week 1": [
        "0% false positives on 127 events",
        "75% success at complexity 5 (Novice)",
        "23.6% read rate (too low, needs interactive)",
        "Champion availability: 100% (observed)",
        "Tribal knowledge extraction: 60% complete",
        "Personalization preference: Not yet measured"
    ],
    "Sign-off Required By": [
        "Champions (domain experts)",
        "Engineering Manager + Champions",
        "Team vote (all developers)",
        "Champions (commitment)",
        "Champions (authority transfer)",
        "Individual developers (opt-in)"
    ],
    "Status": [
        "✅ Approved",
        "✅ Approved",
        "🟡 Pending vote",
        "✅ Committed",
        "🟡 In progress",
        "🟡 Survey deployed"
    ]
}

st.dataframe(pd.DataFrame(sign_off_sections), use_container_width=True, hide_index=True)

week2_yaml = """# week2_governance_configuration.yaml
# Generated from Week 1 telemetry analysis
# Sign-off required before enforcement activation

governance:
  version: "2.0.0"
  effective_date: "2026-03-08"
  based_on_week1_data: true

zones:
  red:
    paths: ["migrations/**", "src/payment/**", "src/security/**", "config/production/**"]
    enforcement: "ACTIVE"
    champion_notification: "immediate"

complexity_caps:
  novice: 5  # Validated: 75% success rate Week 1
  intermediate: 10
  expert: 15
  champion: 20

scaffolding:
  mode: "interactive_acknowledgment"
  mandatory_delay_seconds: 3
  explanation_length: "moderate"
  personalized: true  # Based on individual_profiles.json

escalation:
  red_zone_sla_hours: 4
  yellow_zone_sla_hours: 24
  after_hours_rotation: ["champion_1", "champion_2", "champion_3"]

signatures:
  engineering_manager: ""
  champion_1: ""
  champion_2: ""
  champion_3: ""
  consultant: ""
  date: ""
"""

st.download_button(
    label="Download Week 2 Configuration Template (YAML)",
    data=week2_yaml,
    file_name="week2_governance_configuration.yaml",
    mime="text/yaml"
)

st.divider()

# =============================================================================
# Section 7: VTCO-Driven Scaffolding Architecture
# =============================================================================
st.header("7. VTCO-Driven Scaffolding Architecture", divider=True)

st.markdown("""
**Dynamic Scaffolding**: File path → Load VTCO → Apply context-specific rules
""")

vtco_flow = """
**Example: Database Schema Change (migrations/schema.sql)**

**Path Match**: migrations/**
**VTCO Loaded**: production_database.yaml
**Constraint Check**: "No destructive migrations without rollback"
**Developer Action**: Attempts ALTER TABLE users DROP COLUMN email
**Scaffolding Triggered**:
- Constraint: FAILED
- Rule Applied: when_violated
- Message: "This is a destructive operation. The users table has 2.3M rows.
  Estimated lock time: 4 minutes. Suggested: Use pt-online-schema-change
  or soft delete first. Champion: Senior_Architect_01"
- Format: Video (developer previously selected "Watch video" preference)
- Auto-creates: ADR-2026-031-001
- Escalates: Slack notification to @Senior_Architect_01
"""

st.code(vtco_flow, language=None)

st.info("""
**Learning Loop**: Track which VTCO resources are clicked → Update VTCO effectiveness metrics →
Refine scaffolding rules Week 3
""")

st.divider()

# =============================================================================
# Section 8: Forecasting Dashboard Design
# =============================================================================
st.header("8. Predictive Dashboard & Early Warning System", divider=True)

dashboard_col1, dashboard_col2 = st.columns(2)

with dashboard_col1:
    st.markdown("### Leading Indicators (Predict 1-2 Weeks Ahead)")

    leading = {
        "Metric": [
            "Scaffolding read rate trajectory",
            "File touch frequency trend",
            "Champion response volatility",
            "Complexity success rate slope"
        ],
        "Week 1 Baseline": [
            "23.6%",
            "2.3 touches/file/day",
            "0% (100% availability)",
            "Flat at 75%"
        ],
        "Alert Threshold": [
            "<15% (engagement drop)",
            ">4 touches/file/day (rework spike)",
            ">20% variance (availability risk)",
            "<60% (threshold too high)"
        ],
        "Action Triggered": [
            "Increase scaffolding interactivity",
            "Force cooling-off period",
            "Add backup champion",
            "Lower complexity cap"
        ]
    }

    st.dataframe(pd.DataFrame(leading), use_container_width=True, hide_index=True)

with dashboard_col2:
    st.markdown("### Early Warning System")

    warnings = {
        "Alert Level": ["🟢 Green", "🟡 Yellow", "🔴 Red"],
        "Condition": [
            "All metrics within expected range",
            "1 metric outside threshold",
            "2+ metrics outside OR entropy increases 2 weeks"
        ],
        "Response": [
            "Continue monitoring (weekly)",
            "Consultant check-in call (within 24hrs)",
            "War room + potential rollback to observation"
        ],
        "Notification": [
            "Weekly automated email",
            "Slack DM to consultant + EM",
            "Executive sponsor + all champions"
        ]
    }

    st.dataframe(pd.DataFrame(warnings), use_container_width=True, hide_index=True)

st.divider()

# =============================================================================
# Section 9: Change Management & Communication
# =============================================================================
st.header("9. Change Management & Communication Strategy", divider=True)

change_management = {
    "Stakeholder": ["Developers", "Champions", "Engineering Manager", "Executive Sponsor"],
    "Week 2 Concern": [
        "Loss of autonomy / 'Big Brother'",
        "Time burden / 'More work'",
        "Team velocity / 'Slower delivery'",
        "ROI / 'Is this worth it?'"
    ],
    "Messaging Strategy": [
        "Frame as 'protection from rework' not 'policing'",
        "Frame as 'authority formalization' not 'extra duty'",
        "Show Week 1 velocity data (no drop) + forecast",
        "Show entropy reduction + incident prevention value"
    ],
    "Deliverable": [
        "Interactive demo: 'See how this saves you 2 hours'",
        "VTCO authorship: 'You own the decisions'",
        "Dashboard: 'Data shows no velocity loss'",
        "Business case: '$X saved in prevented incidents'"
    ],
    "Success Metric": [
        ">70% positive sentiment in Week 2 survey",
        "100% champion commitment (signed SLAs)",
        "Velocity maintained (±10%)",
        "Budget approved for Weeks 3-8"
    ]
}

st.dataframe(pd.DataFrame(change_management), use_container_width=True, hide_index=True)

st.divider()
st.success("""
**Consultant's Week 1 Homework Complete**:
127 data points → 6 configuration sections → 1 signed YAML → Week 2 enforcement ready
""")
