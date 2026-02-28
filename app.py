import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Universal AI Governance Framework",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'assessment_data' not in st.session_state:
    st.session_state.assessment_data = None

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "1. Framework & Architecture",
    "2. Baseline Assessment (M2)", 
    "3. Scaling Ready (M3)"
])

# Maturity Colors (distinct from zoning)
MATURITY_COLORS = {
    "M1": "#808080",  # Gray
    "M2": "#FF8C00",  # Orange
    "M3": "#0066CC",  # Blue  
    "M4": "#D4AF37"   # Gold
}

# Zoning Colors (distinct from maturity)
ZONE_COLORS = {
    "Red": "#DC143C",
    "Yellow": "#FFD700", 
    "Green": "#228B22"
}

# Role Colors
ROLE_COLORS = {
    "Consultant": "#4169E1",  # Royal Blue
    "MCP": "#708090",         # Slate Gray
    "Champion": "#DAA520"     # Goldenrod
}

if page == "1. Framework & Architecture":
    st.title("Universal AI Governance Framework")
    st.subheader("Progressive Adoption & Entropy Management")
    
    # AI Readiness Assessment Section
    st.header("AI Readiness Assessment", divider=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Organization Profile")
        industry = st.selectbox("Industry", 
            ["Healthcare", "Finance", "Technology", "Manufacturing", "Retail", "Other"])
        team_size = st.select_slider("Team Size", 
            options=["10-50", "51-100", "101-500", "500+"])
        current_tool = st.selectbox("Current AI Tool",
            ["None", "ChatGPT/Claude Web", "GitHub Copilot", "Cursor", "Multiple", "Custom"])
    
    with col2:
        st.subheader("Current Maturity")
        current_adoption = st.select_slider("Current Adoption Rate",
            options=["0-15% (M1)", "16-35% (M2)", "36-60% (M3)", "61%+ (M4)"])
        governance = st.selectbox("Governance Structure",
            ["None", "Informal", "Documented but Unenforced", "Enforced via Tools"])
        champion_program = st.selectbox("Champion Program",
            ["None", "Identified but Inactive", "Active but Unstructured", "Structured with Authority"])
    
    if st.button("Generate Maturity Score", type="primary"):
        # Simple logic to determine maturity
        if "M1" in current_adoption or governance == "None":
            maturity = "M1"
            color = MATURITY_COLORS["M1"]
            constraint = "Governance Gap"
        elif "M2" in current_adoption or governance == "Informal":
            maturity = "M2"
            color = MATURITY_COLORS["M2"]
            constraint = "Adoption Gap"
        elif champion_program == "Structured with Authority":
            maturity = "M3"
            color = MATURITY_COLORS["M3"]
            constraint = "Optimization Ready"
        else:
            maturity = "M3"
            color = MATURITY_COLORS["M3"]
            constraint = "Skill Gap"
        
        st.session_state.assessment_data = {
            "maturity": maturity,
            "industry": industry,
            "team_size": team_size
        }
        
        st.success(f"Assessment Complete!")
        
        # Display result card
        st.markdown(f"""
        <div style='background-color: {color}20; padding: 20px; border-radius: 10px; border-left: 5px solid {color};'>
            <h3 style='color: {color}; margin: 0;'>Maturity Level: {maturity}</h3>
            <p><strong>Primary Constraint:</strong> {constraint}</p>
            <p><strong>Next Step:</strong> {"Champion workshop to establish governance" if maturity in ["M1", "M2"] else "MCP configuration and scaling"}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("? How this scoring works"):
            st.write("Maturity is determined by adoption rate, governance structure, and champion authority. Workforce development principles inform the assessment—focusing on capability building, not just tool deployment.")

    # The Three Roles Section
    st.header("The Three Roles Architecture", divider=True)
    
    role_col1, role_col2, role_col3 = st.columns(3)
    
    with role_col1:
        st.markdown(f"""
        <div style='background-color: {ROLE_COLORS["Consultant"]}20; padding: 15px; border-radius: 10px; height: 400px;'>
            <h4 style='color: {ROLE_COLORS["Consultant"]};'>🎯 AI Training Consultant</h4>
            <p><strong>You/The Consultant</strong></p>
            <hr>
            <p><strong>What You Do:</strong></p>
            <ul>
                <li>Assess M1-M4 maturity</li>
                <li>Architect zone structure</li>
                <li>Facilitate champion workshops</li>
                <li>Configure MCP server</li>
                <li>Train champions (teach the teachers)</li>
                <li>Build entropy dashboards</li>
                <li>EXIT at M3/M4</li>
            </ul>
            <p><strong>What You DON'T Do:</strong></p>
            <ul>
                <li>❌ Write production code</li>
                <li>❌ Make architectural decisions</li>
                <li>❌ Stay forever</li>
            </ul>
            <p><em>"I build the system that protects your experts, then I leave."</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("? Consultant Role Details"):
            st.write("The consultant brings methodology, MCP configuration, and change management. Sets up the system in 2-3 weeks, then fades to quarterly check-ins. Lean consulting: maximum impact, minimum footprint.")
    
    with role_col2:
        st.markdown(f"""
        <div style='background-color: {ROLE_COLORS["MCP"]}20; padding: 15px; border-radius: 10px; height: 400px;'>
            <h4 style='color: {ROLE_COLORS["MCP"]};'>🤖 MCP Server</h4>
            <p><strong>The Technical Enforcer</strong></p>
            <hr>
            <p><strong>What It Does:</strong></p>
            <ul>
                <li>Guards Red Zone files (blocks unauthorized edits)</li>
                <li>Scaffolds based on skill (Novice=verbose, Expert=terse)</li>
                <li>Counts entropy metrics automatically</li>
                <li>Reminds of VTCO constraints</li>
                <li>Blocks commits violating rules</li>
            </ul>
            <p><strong>What It CANNOT Do:</strong></p>
            <ul>
                <li>❌ Know business priority</li>
                <li>❌ Write tribal knowledge</li>
                <li>❌ Judge promotion readiness</li>
                <li>❌ Build trust with humans</li>
                <li>❌ Override emergencies</li>
            </ul>
            <p><em>"Not a data center. One Python file. The 'server' just means it responds to Cursor/Copilot requests."</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("? MCP Server Reality"):
            st.write("The Model Context Protocol is like a USB-C port for AI. Standardized, lightweight, local. The MCP server is a Python script running on the developer's machine—not cloud infrastructure. It exposes 'tools' that AI assistants call to check zones, validate code, and log metrics.")
    
    with role_col3:
        st.markdown(f"""
        <div style='background-color: {ROLE_COLORS["Champion"]}20; padding: 15px; border-radius: 10px; height: 400px;'>
            <h4 style='color: {ROLE_COLORS["Champion"]};'>👑 Champion</h4>
            <p><strong>The Human Expert</strong></p>
            <hr>
            <p><strong>What They Own:</strong></p>
            <ul>
                <li>Red Zone Decisions (veto power)</li>
                <li>Tribal Knowledge (VTCO docs)</li>
                <li>Skill Assessment (Novice vs Expert)</li>
                <li>Mentoring (human coaching)</li>
                <li>Governance Override (emergency judgment)</li>
                <li>Pattern Definition ("our way")</li>
            </ul>
            <p><strong>What They DON'T Do:</strong></p>
            <ul>
                <li>❌ Manual enforcement (MCP blocks automatically)</li>
                <li>❌ 20-page docs (VTCO is structured YAML)</li>
                <li>❌ Review boilerplate (Green Zone is automated)</li>
            </ul>
            <p><em>"The most expensive expertise. Amplified, not replaced. Protected from becoming a bottleneck."</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("? Champion Protection"):
            st.write("Champions are protected from burnout by MCP automation (filters noise) and by the framework (only true Red Zone decisions reach them). Their authority is formalized via CODEOWNERS and governance charter—executive-backed, not 'extra duties as assigned'.")

    # Protection Architecture
    st.header("Protection Architecture", divider=True)
    
    protect_col1, protect_col2, protect_col3 = st.columns(3)
    
    with protect_col1:
        st.info("**🛡️ Protecting Human Coding Architecture**\n\n*Threat:* AI generates inconsistent patterns\n\n*Solution:* Consultant maps sacred architecture → MCP enforces patterns → Champion defines 'our way'\n\n*Result:* Architecture persists despite AI automation")
    
    with protect_col2:
        st.info("**🧠 Protecting Tribal Knowledge**\n\n*Threat:* Experts leave, knowledge evaporates\n\n*Solution:* Consultant extracts via workshop → MCP surfaces at moment of need → Champion updates\n\n*Result:* Knowledge lives in repo, not heads")
    
    with protect_col3:
        st.info("**⚖️ Protecting Champion Expert Judgment**\n\n*Threat:* Champions burned out, become bottlenecks\n\n*Solution:* Consultant gives authority + time protection → MCP filters noise → Champion decides only judgment calls\n\n*Result:* Champions enable scale; AI handles toil")

elif page == "2. Baseline Assessment (M2)":
    st.title("Current State: M2 (Shallow Adoption)")
    st.markdown(f"<h4 style='color: {MATURITY_COLORS['M2']};'>🟠 The M2 Trap: Activity Without Governance</h4>", unsafe_allow_html=True)
    
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
        "Status": ["🟠 Gap", "🟠 High", "🟠 Below", "🟠 High", "🟠 Risk", "🟠 Uncontrolled", "🟠 At Risk"]
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

else:  # Page 3
    st.title("Target State: M3 (Agentic with Guardrails)")
    st.markdown(f"<h4 style='color: {MATURITY_COLORS['M3']};'>🔵 Velocity with Stability: The Three Roles Working</h4>", unsafe_allow_html=True)
    
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
        "Improvement": ["+60% 🟢", "-54% 🟢", "+57% 🟢", "-59% 🟢", "-80% 🟢", "-91% 🟢", "+45% 🟢"]
    }
    
    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True)
    
    # Three Roles Evidence
    st.header("Three Roles Evidence", divider=True)
    
    role_evidence = st.columns(3)
    
    with role_evidence[0]:
        st.success("""
        **🎯 Consultant (Week 0-8)**
        - Assessment completed
        - Workshop facilitated
        - MCP configured
        - Champions trained
        - **EXIT ready** (handoff complete)
        """)
    
    with role_evidence[1]:
        st.success("""
        **🤖 MCP Server (Running)**
        - Red Zone: 23→2 violations (91% reduction)
        - Auto-enforcement active
        - Entropy logging: 68→31
        - Scaffolding: Adjusting by skill
        """)
    
    with role_evidence[2]:
        st.success("""
        **👑 Champions (Enabled)**
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
        st.success("🟢 M3 ACHIEVED: Ready for M4 (Autonomous) - Consultant can exit")
    elif entropy < 45:
        st.warning("🟡 M3 TRANSITION: Stabilizing governance")
    else:
        st.error("🔴 M2 CHAOS: Needs Consultant + MCP + Champion alignment")
