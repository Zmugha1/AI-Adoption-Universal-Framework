"""Baseline Assessment (M2) page - Current state shallow adoption metrics."""
import sys
from pathlib import Path

# Ensure shared module is importable when run as Streamlit page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd

from shared import MATURITY_COLORS, ZONE_COLORS, ROLE_COLORS

st.title("Current State: M2 (Shallow Adoption)")
st.markdown(f"<h4 style='color: {MATURITY_COLORS['M2']};'>The M2 Trap: Activity Without Governance</h4>", unsafe_allow_html=True)

# Executive Summary
st.header("Executive Summary", divider=True)

metric_cols = st.columns(4)

with metric_cols[0]:
    st.metric("Maturity Level", "M2 - Shallow", delta="Assessment Complete")
with metric_cols[1]:
    st.metric("Adoption Rate", "22%", delta="-58% from M3", delta_color="inverse")
with metric_cols[2]:
    st.metric("Entropy Index", "68/100", delta="+38 above target", delta_color="inverse")
with metric_cols[3]:
    st.metric("Champion Coverage", "15 identified, 0 documented", delta="At Risk", delta_color="off")

# Problem Context
st.header("Problem Context", divider=True)

st.write("""
**Acme Corp has AI licenses but no governance:**
- AI usage sporadic (22% adoption) - not enough for competency
- No zoning enforcement - 23 Red Zone violations last month
- No skill-based scaffolding - novices get same AI as experts
- Tribal knowledge evaporating - champions exist but undocumented
""")

# Metrics Table
st.subheader("Evidence Dashboard")

baseline_data = {
    "Metric": ["Adoption Rate", "Entropy Index", "Velocity (PRs/week)", "Rework Rate", "Premature Acceptance", "Red Zone Violations", "Champion Documentation"],
    "Current Value": ["22%", "68", "47", "34%", "41%", "23/month", "0%"],
    "Target (M3)": ["82%", "31", "74", "14%", "8%", "<5/month", "100%"],
    "Status": ["[Gap]", "[High]", "[Below]", "[High]", "[Risk]", "[Uncontrolled]", "[At Risk]"]
}

st.dataframe(pd.DataFrame(baseline_data), use_container_width=True)

# Human-AI Interaction Evidence
st.info("""
**Human-AI Interaction (M2 Chaos):**
- **Scaffolding:** None (one-size-fits-all AI)
- **Trust:** Low (developers fear breaking production)
- **Tribal Knowledge:** Siloed (experts leaving, knowledge lost)
- **Consultant:** Not yet engaged
- **Champion:** Overwhelmed, no authority
""")
