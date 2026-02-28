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

# ---------------------------------------------------------------------------
# Metrics Reference Guide (Educational Dropdown)
# ---------------------------------------------------------------------------
st.header("Metrics Reference Guide", divider=True)
st.caption("Understanding what the numbers mean")

with st.expander("Metrics Definitions & Calculations Reference", expanded=False):
    metric = st.selectbox(
        "Select metric for detailed explanation:",
        [
            "Entropy Index",
            "Adoption Rate",
            "Maturity Level",
            "Champion Coverage",
            "Rework Rate",
            "Velocity (PRs/Week)",
            "Premature Acceptance",
            "Complexity Score",
            "Code Bloat",
            "Red Zone Violations",
        ],
        key="metric_ref",
    )

    # Metric detail cards
    if metric == "Entropy Index":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            ### Entropy Index (The Primary Health Metric)
            
            **Definition**: A composite score measuring organizational chaos in AI adoption. Higher = more chaos/technical debt.
            
            **Formula**:  
            `(Code Bloat % × 0.25) + (Rework Rate % × 0.25) + (Revert Frequency % × 0.20) + (Premature Acceptance % × 0.30)`
            
            **Weights Explanation**:
            - Premature acceptance weighted highest (30%) because accepting bad AI suggestions creates cascading debt
            - Bloat and Rework equal (25% each) as primary waste indicators
            - Reverts (20%) as volatility measure
            
            **Data Source**: Git commit history (non-gameable), PR metadata, MCP violation logs  
            **Update Frequency**: Real-time (per commit) with 7-day rolling average
            
            *"This is your 'blood pressure' for AI adoption. It aggregates multiple failure modes into one trend line."*
            """)
            st.info("**Why these weights?** Premature acceptance creates cascading debt (highest weight). Reverts indicate volatility (lowest but significant).")
        with col2:
            st.metric("Your Current", "68/100", delta="M2 - Shallow", delta_color="inverse")
            st.markdown(f"""
            **Thresholds:**
            - M4 (Excellent): < 15
            - M3 (Good): 15-30
            - M2 (Warning): 30-50
            - M1 (Critical): 50-70
            - Danger: > 70
            """)

    elif metric == "Adoption Rate":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Adoption Rate
            
            **Definition**: Percentage of development team actively using AI tools daily/weekly.
            
            **Formula**: `(Active AI Users / Total Developers) × 100`
            
            **Active Definition**: Minimum 10 AI interactions per week (suggestions requested, not just IDE installed).
            
            **Data Source**: IDE telemetry (Cursor/Copilot analytics), MCP interaction logs  
            **Update Frequency**: Weekly
            
            **Caution**: High adoption without governance (M2) is dangerous - like high speed without brakes.
            """)
        with col2:
            st.metric("Your Current", "22%", delta="M2 - Shallow", delta_color="inverse")
            st.markdown("""
            **Thresholds:**
            - M4: 85-100%
            - M3: 70-85%
            - M2: 20-70% (you are here)
            - M1: < 20%
            """)

    elif metric == "Maturity Level":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Maturity Level (M1-M4 Classification)
            
            **Definition**: Stage of AI governance sophistication based on entropy and process maturity.
            
            **Calculation Logic**:
            - **M1 (Chaos)**: Entropy > 70 OR no governance framework
            - **M2 (Shallow)**: Entropy 50-70 AND tools deployed but governance gaps
            - **M3 (Agentic)**: Entropy 30-50 AND MCP enforcement active AND champion program documented
            - **M4 (Autonomous)**: Entropy < 15 AND self-optimizing system with <5% rework
            
            **Assessment Method**: 30-question comprehensive survey + git-based entropy calculation  
            **Upgrade Criteria**: Must maintain lower entropy for 30 days + champion sign-off
            """)
        with col2:
            st.metric("Your Current", "M2", delta="Shallow")
            st.markdown("**Data Source**: Composite of entropy score + organizational checklist")

    elif metric == "Champion Coverage":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Champion Coverage
            
            **Definition**: Percentage of critical domains with documented expert ownership (VTCO authorship).
            
            **Formula**: `(Domains with VTCO Docs / Total Critical Domains) × 100`
            
            **Critical Domains**: Red Zone areas (Payment, Security, Database, Compliance, Production Config).
            
            **Data Source**: `.ai-governance/tribal-knowledge/*.yaml` files  
            **Update Frequency**: Per VTCO document creation
            
            **Why 0% is Critical**: Identified champions without documented knowledge means expertise walks out the door when they leave.
            """)
        with col2:
            st.metric("Your Current", "0%", delta="Danger", delta_color="inverse")
            st.markdown("""
            **Thresholds:**
            - Excellent: 100%
            - At Risk: 60-99%
            - Danger: < 60%
            """)

    elif metric == "Rework Rate":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Rework Rate
            
            **Definition**: Percentage of AI-generated code requiring significant revision after initial acceptance.
            
            **Formula**: `(Lines Reworked / Total AI-Generated Lines) × 100`
            
            **"Significant" Definition**: > 20% of lines changed OR architectural pattern changed OR rejected entirely.
            
            **Data Source**: Git diff analysis (changelogs), PR review comments marked "rework"
            
            **Leading Indicator**: Rework predicts entropy 2-3 weeks ahead.
            """)
        with col2:
            st.metric("Your Current", "34%", delta="M2 - Waste", delta_color="inverse")
            st.markdown("""
            **Thresholds:**
            - M4: < 10%
            - M3: 10-20%
            - M2: 20-35% (you are here)
            - M1: > 35%
            """)

    elif metric == "Velocity (PRs/Week)":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Velocity (PRs/Week)
            
            **Definition**: Rate of code integration, measuring throughput.
            
            **Formula**: `Merged Pull Requests / Time Period (7 days)`
            
            **Important Distinction**: Measures sustainable pace, not heroics (excludes >16 hour days).
            
            **Data Source**: GitHub/GitLab API (PR merge events)
            
            **Paradox**: Velocity often decreases initially when implementing governance (M2 to M3), then exceeds baseline (M3 to M4).
            """)
        with col2:
            st.metric("Your Current", "47", delta="Target 74", delta_color="inverse")
            st.markdown("""
            **Thresholds:**
            - M4: 70+ PRs/week
            - M3: 50-70 (target)
            - M2: 30-50 (you are here)
            - M1: < 30
            """)

    elif metric == "Premature Acceptance":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Premature Acceptance Rate
            
            **Definition**: AI suggestions accepted without adequate review, leading to later defects.
            
            **Formula**: `(Accepted Without Review / Total AI Suggestions) × 100`
            
            **"Without Review"**: No human eyes, direct commit, or "LGTM" without reading.
            
            **Data Source**: IDE telemetry (acceptance timestamps vs. time-to-next-action), MCP logs
            
            **High Impact**: This is the strongest predictor of production incidents.
            """)
        with col2:
            st.metric("Your Current", "41%", delta="M2 - Risk", delta_color="inverse")
            st.markdown("""
            **Thresholds:**
            - M4: < 5%
            - M3: 5-15%
            - M2: 15-40% (you are here)
            - M1: > 40%
            """)

    elif metric == "Complexity Score":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Complexity Score (Cyclomatic)
            
            **Definition**: Code intricacy measured by decision paths (if/else, loops, switches).
            
            **Formula**: Standard cyclomatic complexity: `1 + (number of decision points)`
            
            **Decision Points**: if, while, for, case, catch, &&, ||, ternary operators.
            
            **Data Source**: Static analysis tools (radon for Python, eslint for JS), MCP parsing
            
            **ZPD Connection**: Used to match task difficulty to developer skill level.
            """)
        with col2:
            st.markdown("""
            **Thresholds:**
            - Low (Green): 1-5 (Novice max)
            - Medium (Yellow): 6-10
            - High (Orange): 11-15
            - Very High (Red): 16-20
            - Refactor: > 20
            """)

    elif metric == "Code Bloat":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Code Bloat Percentage
            
            **Definition**: Unnecessary code generated by AI that increases maintenance burden.
            
            **Formula**: `(Lines of Boilerplate or Redundant Code / Total Lines) × 100`
            
            **Examples**: Unused imports, over-engineered abstractions, commented-out AI attempts left in code, duplicate error handling.
            
            **Detection**: MCP pattern matching for common AI "over-generation" patterns
            
            **Cost**: Every line of code is a liability; bloat compounds technical debt silently.
            """)
        with col2:
            st.markdown("""
            **Thresholds:**
            - Clean: < 5%
            - Acceptable: 5-15%
            - Bloated: 15-30%
            - Unmaintainable: > 30%
            """)

    elif metric == "Red Zone Violations":
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Red Zone Violations (Monthly Count)
            
            **Definition**: Unauthorized edits to critical infrastructure without champion approval.
            
            **Formula**: Raw count of MCP-blocked edits in Red Zone domains.
            
            **Severity Levels**:
            - **Attempted**: Blocked by MCP (counted here)
            - **Successful**: Champion approved (legitimate)
            - **Emergency**: Override used (logged separately)
            
            **Data Source**: MCP violation logs
            
            **Trend Direction**: Decreasing violations is GOOD (governance working, not "people behaving badly").
            """)
        with col2:
            st.metric("Your Current", "23/month", delta="M2 - Uncontrolled", delta_color="inverse")
            st.markdown("""
            **Thresholds:**
            - M4: < 5/month
            - M3: 5-15/month
            - M2: 15-30/month (you are here)
            - M1: > 30/month
            """)

    # Educational sections
    st.divider()
    st.subheader("How to Read Your Dashboard")
    st.markdown("""
    - **Green arrows (down)** on entropy/rework = good (decreasing)
    - **Green arrows (up)** on adoption/velocity = good (increasing)
    - Champion coverage should trend toward 100%
    - Red Zone violations should trend toward 0 (but never exactly 0 - that means no one is trying anything)
    """)

    st.subheader("The M2 Paradox")
    st.warning("""
    At M2 (current state), you'll see: **High entropy (68)** | **Low adoption (22%)** | **High rework (34%)**
    
    This is the "worst of both worlds" - enough AI usage to cause chaos, not enough to benefit from scale.
    """)

    st.subheader("Leading vs Lagging Indicators")
    st.markdown("""
    - **Leading** (predict future): Premature Acceptance, Complexity Score
    - **Lagging** (confirm past): Entropy Index, Rework Rate
    - **Real-time**: Red Zone Violations (immediate governance feedback)
    """)

    # Entropy Simulator
    st.divider()
    st.subheader("Entropy Simulator")
    st.caption("Adjust the sliders to see how each component affects your entropy score")
    sim_col1, sim_col2, sim_col3, sim_col4 = st.columns(4)
    with sim_col1:
        bloat = st.slider("Bloat %", 0, 100, 10, key="sim_bloat")
    with sim_col2:
        rework = st.slider("Rework %", 0, 100, 34, key="sim_rework")
    with sim_col3:
        reverts = st.slider("Reverts %", 0, 100, 15, key="sim_reverts")
    with sim_col4:
        premature = st.slider("Premature Acceptance %", 0, 100, 41, key="sim_premature")

    calculated_entropy = round((bloat * 0.25) + (rework * 0.25) + (reverts * 0.20) + (premature * 0.30), 1)
    sim_result_col1, sim_result_col2 = st.columns([1, 2])
    with sim_result_col1:
        st.metric("Calculated Entropy", f"{calculated_entropy}/100", delta=None)
        if calculated_entropy < 15:
            st.success("M4 Ready")
        elif calculated_entropy < 30:
            st.success("M3 Ready")
        elif calculated_entropy < 50:
            st.info("M2 - Shallow")
        else:
            st.error("M1 - Chaos")
    with sim_result_col2:
        st.caption("Formula: (Bloat×0.25) + (Rework×0.25) + (Reverts×0.20) + (Premature×0.30)")

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
