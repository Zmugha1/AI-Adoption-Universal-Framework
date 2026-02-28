"""Scaling Ready (M3) page - Target state agentic with guardrails."""
import sys
from pathlib import Path

# Ensure shared module is importable when run as Streamlit page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd

from shared import MATURITY_COLORS, ZONE_COLORS, ROLE_COLORS

st.title("Target State: M3 (Agentic with Guardrails)")
st.markdown(f"<h4 style='color: {MATURITY_COLORS['M3']};'>Velocity with Stability: The Three Roles Working</h4>", unsafe_allow_html=True)

# Executive Summary
st.header("Executive Summary", divider=True)

metric_cols = st.columns(4)

with metric_cols[0]:
    st.metric("Maturity Level", "M3 - Agentic", delta="Target Achieved")
with metric_cols[1]:
    st.metric("Adoption Rate", "82%", delta="+60% from M2")
with metric_cols[2]:
    st.metric("Entropy Index", "31/100", delta="-37 from M2")
with metric_cols[3]:
    st.metric("Champion Coverage", "100% documented", delta="Secured")

# Before/After
st.header("Evidence: Before vs After", divider=True)

comparison_data = {
    "Evidence Category": ["Adoption Rate", "Entropy Index", "Velocity (PRs/week)", "Rework Rate", "Premature Acceptance", "Red Violations", "Champion Time on Innovation"],
    "M2 Baseline": ["22%", "68", "47", "34%", "41%", "23/month", "20%"],
    "M3 Achieved": ["82%", "31", "74", "14%", "8%", "2/month", "65%"],
    "Improvement": ["+60%", "-54%", "+57%", "-59%", "-80%", "-91%", "+45%"]
}

st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)

# Three Roles Evidence
st.header("Three Roles Evidence", divider=True)

role_evidence = st.columns(3)

with role_evidence[0]:
    st.success("""
    **Consultant (Week 0-8)**
    - Assessment completed
    - Workshop facilitated
    - MCP configured
    - Champions trained
    - **EXIT ready** (handoff complete)
    """)

with role_evidence[1]:
    st.success("""
    **MCP Server (Running)**
    - Red Zone: 23→2 violations (91% reduction)
    - Auto-enforcement active
    - Entropy logging: 68→31
    - Scaffolding: Adjusting by skill
    """)

with role_evidence[2]:
    st.success("""
    **Champions (Enabled)**
    - 100% tribal knowledge documented
    - Time on innovation: 20%→65%
    - 7 developers mentored to Intermediate
    - Authority protected by CODEOWNERS
    """)

# Interactive Entropy Calculator
st.header("Entropy Impact Simulator", divider=True)

calc_cols = st.columns(4)

with calc_cols[0]:
    bloat = st.slider("Code Bloat %", 0, 50, 10, help="M3 target: <10%")
with calc_cols[1]:
    rework = st.slider("Rework Rate %", 0, 50, 14, help="M3 target: <15%")
with calc_cols[2]:
    reverts = st.slider("Revert Frequency %", 0, 30, 3, help="M3 target: <5%")
with calc_cols[3]:
    premature = st.slider("Premature Acceptance %", 0, 50, 8, help="M3 target: <10%")

entropy = (bloat * 0.25) + (rework * 0.25) + (reverts * 0.20) + (premature * 0.30)

st.metric("Calculated Entropy", f"{entropy:.1f}/100")

if entropy < 30:
    st.success("M3 ACHIEVED: Ready for M4 (Autonomous) - Consultant can exit")
elif entropy < 45:
    st.warning("M3 TRANSITION: Stabilizing governance")
else:
    st.error("M2 CHAOS: Needs Consultant + MCP + Champion alignment")
