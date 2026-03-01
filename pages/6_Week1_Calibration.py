"""
Week 1 Calibration Report - Demo
Evidence-based data pipeline: violations.jsonl + scaffolding_effectiveness.jsonl → calibration dashboard
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json
from shared import render_sidebar
from data.week1_fake_data import generate_violations, generate_scaffolding

st.set_page_config(
    page_title="Week 1 Calibration Report",
    page_icon="📊",
    layout="wide"
)
render_sidebar(use_nav_radio=False)

st.title("Week 1 Calibration Report")
st.subheader("Evidence-Based Consulting: From Observation to Calibration")

# =============================================================================
# Week 1 Insights: Narrative Write-Up
# =============================================================================
with st.expander("📋 Week 1 Insights: From Observation to Action", expanded=True):
    st.markdown("""
    ### The Observation Effect: Data as a Behavioral Mirror

    **Week 0 self-assessment estimated 68 entropy**—typical M2 chaos. **Week 1 actual measurement: 20.4**. A 47.6 point drop without enforcement.

    **Insight**: The Hawthorne effect is real. Developers self-corrected when they knew telemetry was active. The MCP's mere presence—logging but not blocking—changed behavior. This validates our methodology: observation before enforcement prevents false positives and builds trust.

    **Week 2 Decision**: We can proceed with confidence. The baseline was inflated; actual chaos was lower than perceived. Enforcement will land on a team already trending toward discipline.

    ---

    ### Zero False Positives: Zoning Validation Confirmed

    **127 violation events logged. Zero misclassifications.**

    Every Green Zone file allowed. Every Red Zone file correctly flagged. The regex patterns and zone logic (migrations/, payment/, security/) accurately matched the client's risk topology.

    **Insight**: Our Week 0 interview-based zone mapping was correct. Champions identified the right danger zones. The file path architecture aligned with tribal knowledge.

    **Week 2 Decision**: Flip `ENFORCEMENT_MODE` from `observation` to `active`. The system is calibrated. No "learning mode" buffer needed—we're not guessing.

    ---

    ### 16 Red Zone Attempts: The Protection Gap Quantified

    **Novice developers attempted production edits 16 times in 5 days.**

    Database migrations, security configs, payment logic—all caught and warned, not blocked. In the old world, 3-4 of these would have hit production. In Week 2, they become hard blocks with champion escalation.

    **Insight**: Champions are currently firefighting 3+ incidents per week that they don't even know about. The MCP surfaces invisible risk.

    **Week 2 Decision**: Champion notification system goes live. Every Red Zone attempt pings the domain expert in real-time. Champions move from reactive (incident response) to proactive (approval workflow).

    ---

    ### 23.6% Explanation Read Rate: The Education Gap

    **Only 1 in 4 developers read the AI explanations before accepting suggestions.**

    Scaffolding was set to "maximum," but verbosity doesn't guarantee comprehension. Developers click through warnings. This is why entropy remained at 20.4 despite observation—partial understanding, not full learning.

    **Insight**: Information overload creates friction without value. Maximum verbosity → moderate effectiveness.

    **Week 2 Decision**: Change scaffolding to "interactive acknowledgment." Force 3-second delay + "I understand" checkbox before edit. Reduce text, increase engagement. Test if forced pause > verbose explanation.

    ---

    ### 75% Complexity Success: Threshold Validation

    **Novice developers succeeded at complexity 5 tasks 75% of the time.**

    The interview assumption (complexity 5 = Novice limit) held. No need to lower to 3 (too restrictive) or raise to 7 (too risky). The Goldilocks zone is confirmed.

    **Insight**: Skill-based scaffolding works when data-validated. Not patronizing (cap 3) or dangerous (cap 10).

    **Week 2 Decision**: Maintain Novice cap at 5. Set Intermediate at 10, Expert at 15. Complexity gates stay as modeled—no calibration needed here.

    ---

    ### The Week 2 Transition: Data-Driven Enforcement

    **From these 127 data points, the Week 2 configuration emerges:**

    | Metric | Insight | Week 2 Action |
    |--------|---------|---------------|
    | **Entropy 20.4** | Team ready for structure | Enable enforcement |
    | **0% False Positives** | Zoning accurate | No buffer needed |
    | **16 Red Attempts** | Risk is real | Champion alerts active |
    | **23.6% Read Rate** | Education failing | Interactive scaffolding |
    | **75% Success @ 5** | Threshold valid | Keep complexity caps |

    **The consulting narrative**: *"Week 0 was subjective fear. Week 1 was objective telemetry. Week 2 is calibrated enforcement. We're not installing a tool—we're installing a data-driven protection layer validated by their actual behavior."*

    ---

    **Bottom line**: Week 1 proved the framework works before it ever blocked a single edit. That's evidence-based consulting.
    """)

st.divider()

st.markdown("""
Week 0 is subjective assessment. Week 1 is objective telemetry. By Day 4, I have enough signal to tune the enforcement engine.

This demo uses **fake data** to simulate the MCP telemetry pipeline. In production, data comes from `.ai-governance/violations.jsonl` and `scaffolding_effectiveness.jsonl`.
""")

st.divider()

# =============================================================================
# Step 1: Data Ingestion (simulated)
# =============================================================================
with st.expander("Step 1: Data Ingestion (Day 3 of Week 1)", expanded=True):
    st.markdown("*\"By Day 3, the MCP server has generated roughly 100-150 log entries. I pull the raw telemetry files into a Python analysis notebook.\"*")

    violations = generate_violations()
    scaffolding = generate_scaffolding()

    df_violations = pd.DataFrame(violations)
    df_scaffolding = pd.DataFrame(scaffolding)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Violation events loaded", len(df_violations))
        st.dataframe(df_violations.head(10), use_container_width=True, hide_index=True)
    with col2:
        st.metric("Scaffolding interactions loaded", len(df_scaffolding))
        st.dataframe(df_scaffolding.head(10), use_container_width=True, hide_index=True)

st.divider()

# =============================================================================
# Step 2: Pattern Analysis
# =============================================================================
with st.expander("Step 2: Pattern Analysis (Using Cursor as Assistant)", expanded=True):
    st.markdown("*\"I use Cursor as my data analysis partner. I ask it to identify patterns—which roles hit complexity limits, which file paths are attempted but blocked.\"*")

    # Pattern analysis
    false_positives = len(df_violations[(df_violations["zone"] == "Green") & (df_violations["allowed"] == False)])
    novice_red_attempts = len(df_violations[(df_violations["user_role"] == "Novice") & (df_violations["zone"] == "Red")])
    fp_rate = (false_positives / len(df_violations) * 100) if len(df_violations) > 0 else 0

    # Complexity success for Novices at level 5
    novice_at_5 = df_violations[(df_violations["user_role"] == "Novice") & (df_violations["complexity_score"] == 5)]
    complexity_success_5 = (len(novice_at_5[novice_at_5["allowed"] == True]) / len(novice_at_5) * 100) if len(novice_at_5) > 0 else 0

    # Explanation read rate: time_to_accept > 30 seconds = likely read
    read_count = len(df_scaffolding[df_scaffolding["time_to_accept"] >= 30])
    explanation_read_rate = (read_count / len(df_scaffolding) * 100) if len(df_scaffolding) > 0 else 0

    analysis = {
        "false_positives": false_positives,
        "novice_red_attempts": novice_red_attempts,
        "complexity_success_at_5": complexity_success_5,
        "explanation_read_rate": explanation_read_rate,
        "recommended_novice_cap": 5 if complexity_success_5 >= 70 else 3,
    }

    st.json(analysis)

st.divider()

# =============================================================================
# Step 3: Entropy Calculation
# =============================================================================
def calculate_bloat_rate(df):
    accepted = df[df["allowed"] == True]
    if len(accepted) == 0:
        return 0
    return accepted["has_bloat"].sum() / len(accepted) * 100

def calculate_rework_rate(df):
    if len(df) == 0:
        return 0
    return len(df[df["touch_count"] >= 3]) / len(df) * 100

def calculate_revert_rate(df):
    if len(df) == 0:
        return 0
    return df["was_reverted"].sum() / len(df) * 100

def calculate_premature_acceptance(df):
    if len(df) == 0:
        return 0
    return len(df[df["time_to_accept"] < 5]) / len(df) * 100

with st.expander("Step 3: Calculate Calibrated Entropy", expanded=True):
    st.markdown("*\"Now I calculate the actual entropy score from Week 1 data—not the self-reported 68 from the assessment, but the real behavioral metric.\"*")

    week1_metrics = {
        "bloat": calculate_bloat_rate(df_violations),
        "rework": calculate_rework_rate(df_violations),
        "reverts": calculate_revert_rate(df_scaffolding),
        "premature": calculate_premature_acceptance(df_scaffolding),
    }

    entropy_score = (
        week1_metrics["bloat"] * 0.25 +
        week1_metrics["rework"] * 0.25 +
        week1_metrics["reverts"] * 0.20 +
        week1_metrics["premature"] * 0.30
    )
    # Scale to 0-100 range (typical entropy)
    entropy_score = min(100, entropy_score * 1.2)

    st.metric("Week 1 Actual Entropy", f"{entropy_score:.1f}", delta=f"{entropy_score - 68:.1f} vs assessment estimate (68)")
    st.dataframe(pd.DataFrame([week1_metrics]).T.rename(columns={0: "Contribution %"}), use_container_width=True, hide_index=True)

st.divider()

# =============================================================================
# Step 4: Calibration Dashboard
# =============================================================================
st.header("Week 1 Calibration Dashboard", divider=True)
st.markdown("*\"I publish this immediately to Streamlit so the client sees the evidence during our Day 4 calibration workshop. It's not a PowerPoint—it's live data.\"*")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Events Logged", len(df_violations))
    st.metric("Actual Entropy", f"{entropy_score:.1f}", delta=f"{entropy_score - 68:.1f} vs estimate")
with col2:
    st.metric("Novice Red Zone Attempts", novice_red_attempts)
    st.metric("False Positive Rate", f"{fp_rate:.1f}%")
with col3:
    st.metric("Explanation Read Rate", f"{explanation_read_rate:.1f}%")
    st.metric("Recommended Novice Cap", str(analysis["recommended_novice_cap"]))

st.divider()

# Visual pattern analysis
st.subheader("Complexity Distribution by Role")
role_complexity = df_violations.groupby(["user_role", "complexity_score"]).size().unstack(fill_value=0)
st.bar_chart(role_complexity)

st.subheader("Zone Violation Summary")
zone_counts = df_violations["zone"].value_counts()
st.dataframe(zone_counts.rename("Count").to_frame(), use_container_width=True, hide_index=True)

st.divider()

# =============================================================================
# Step 5: Calibration Recommendations
# =============================================================================
st.header("Step 5: Calibration Recommendations (Auto-Generated)", divider=True)
st.markdown("*\"Cursor helps me draft the calibration recommendations based on the data patterns.\"*")

recommendations = {
    "novice_complexity_cap": analysis["recommended_novice_cap"],
    "red_zone_enforcement": "ACTIVE" if fp_rate < 5 else "OBSERVATION",
    "scaffolding_change": "INCREASE_VERBOSITY" if explanation_read_rate < 50 else "MAINTAIN",
    "mentor_assignment": "REQUIRED_FOR_YELLOW",
}

st.json({"recommendations": recommendations})

st.info("""
**Key phrases for the interview:**
- *"I don't guess at thresholds—I observe behavior for a week, then calibrate."*
- *"The MCP logs everything in JSONL format—machine-readable, append-only, auditable."*
- *"Cursor accelerates my analysis—I ask it to find patterns in the telemetry, it writes the pandas code, I validate and deploy."*
- *"Week 1 is 'silent observation'—we're training the model on their actual behavior before we enforce."*
""")
