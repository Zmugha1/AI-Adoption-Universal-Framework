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

# Custom CSS for better text handling
st.markdown("""
<style>
    .stMarkdown ul {
        margin-bottom: 10px;
    }
    .stMarkdown li {
        margin-bottom: 5px;
        line-height: 1.4;
    }
    .stExpander {
        border: 1px solid #ddd;
        border-radius: 5px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

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

    # Three Roles Section - IMPROVED LAYOUT
    st.header("The Three Roles Architecture", divider=True)

    with st.container():
        role_col1, role_col2, role_col3 = st.columns([1, 1, 1], gap="medium")
        
        with role_col1:
            st.markdown("""
            <div style='background-color: #4169E120; padding: 20px; border-radius: 10px; border-left: 5px solid #4169E1; min-height: 500px;'>
                <h3 style='color: #4169E1; margin-top: 0;'>🎯 AI Training Consultant</h3>
                <p><strong>You/The Consultant</strong></p>
                <hr style='margin: 10px 0;'>
                
                <p><strong>What You Do:</strong></p>
                <ul style='padding-left: 20px;'>
                    <li>Assess M1-M4 maturity</li>
                    <li>Architect zone structure</li>
                    <li>Facilitate champion workshops</li>
                    <li>Configure MCP server</li>
                    <li>Train champions (teach teachers)</li>
                    <li>Build entropy dashboards</li>
                    <li>EXIT at M3/M4</li>
                </ul>
                
                <p style='margin-top: 20px;'><strong>What You DON'T Do:</strong></p>
                <ul style='padding-left: 20px; color: #DC143C;'>
                    <li>❌ Write production code</li>
                    <li>❌ Make architectural decisions</li>
                    <li>❌ Enforce rules daily</li>
                    <li>❌ Stay forever</li>
                </ul>
                
                <p style='margin-top: 20px; font-style: italic; font-size: 0.9em;'>
                "I build the system that protects your experts, then I leave."
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("? Consultant Role Details"):
                st.write("The consultant brings methodology, MCP configuration, and change management expertise. Sets up the system in 2-3 weeks, then fades to quarterly check-ins. Lean consulting: maximum impact, minimum footprint.")
        
        with role_col2:
            st.markdown("""
            <div style='background-color: #70809020; padding: 20px; border-radius: 10px; border-left: 5px solid #708090; min-height: 500px;'>
                <h3 style='color: #708090; margin-top: 0;'>🤖 MCP Server</h3>
                <p><strong>The Technical Enforcer</strong></p>
                <hr style='margin: 10px 0;'>
                
                <p><strong>What It Does:</strong></p>
                <ul style='padding-left: 20px;'>
                    <li>Guards Red Zone files (blocks unauthorized edits)</li>
                    <li>Scaffolds based on skill (Novice=verbose, Expert=terse)</li>
                    <li>Counts entropy metrics automatically</li>
                    <li>Reminds of VTCO constraints</li>
                    <li>Blocks commits violating rules</li>
                </ul>
                
                <p style='margin-top: 20px;'><strong>What It CANNOT Do:</strong></p>
                <ul style='padding-left: 20px; color: #DC143C;'>
                    <li>❌ Know business priority</li>
                    <li>❌ Write tribal knowledge</li>
                    <li>❌ Judge promotion readiness</li>
                    <li>❌ Build trust with humans</li>
                    <li>❌ Override emergencies</li>
                </ul>
                
                <p style='margin-top: 20px; font-style: italic; font-size: 0.9em;'>
                "Not a data center. One Python file. The 'server' just means it responds to requests."
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("? MCP Server Reality"):
                st.write("The Model Context Protocol is like a USB-C port for AI. Standardized, lightweight, local. The MCP server is a Python script running on the developer's machine—not cloud infrastructure. It exposes 'tools' that AI assistants call to check zones, validate code, and log metrics.")
        
        with role_col3:
            st.markdown("""
            <div style='background-color: #DAA52020; padding: 20px; border-radius: 10px; border-left: 5px solid #DAA520; min-height: 500px;'>
                <h3 style='color: #DAA520; margin-top: 0;'>👑 Champion</h3>
                <p><strong>The Human Expert</strong></p>
                <hr style='margin: 10px 0;'>
                
                <p><strong>What They Own:</strong></p>
                <ul style='padding-left: 20px;'>
                    <li>Red Zone Decisions (veto power)</li>
                    <li>Tribal Knowledge (VTCO docs)</li>
                    <li>Skill Assessment (Novice vs Expert)</li>
                    <li>Mentoring (human coaching)</li>
                    <li>Governance Override (emergencies)</li>
                    <li>Pattern Definition ("our way")</li>
                </ul>
                
                <p style='margin-top: 20px;'><strong>What They DON'T Do:</strong></p>
                <ul style='padding-left: 20px; color: #DC143C;'>
                    <li>❌ Manual enforcement (MCP blocks automatically)</li>
                    <li>❌ 20-page docs (VTCO is structured YAML)</li>
                    <li>❌ Review boilerplate (Green Zone automated)</li>
                    <li>❌ 24/7 availability (protected time)</li>
                </ul>
                
                <p style='margin-top: 20px; font-style: italic; font-size: 0.9em;'>
                "The most expensive expertise. Amplified, not replaced. Protected from burnout."
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("? Champion Protection"):
                st.write("Champions are protected from burnout by MCP automation (filters noise) and by the framework (only true Red Zone decisions reach them). Their authority is formalized via CODEOWNERS and governance charter—executive-backed, not 'extra duties as assigned'.")

    # Protection Architecture - IMPROVED
    st.header("Protection Architecture", divider=True)

    protect_col1, protect_col2, protect_col3 = st.columns([1, 1, 1], gap="medium")

    with protect_col1:
        st.markdown("""
        <div style='background-color: #E3F2FD; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3; min-height: 280px;'>
            <h4 style='color: #1565C0; margin-top: 0;'>🛡️ Protecting Human Coding Architecture</h4>
            <p style='font-size: 0.9em;'><strong>Threat:</strong> AI generates inconsistent patterns, technical debt accumulates</p>
            <p style='font-size: 0.9em;'><strong>Solution:</strong></p>
            <ul style='font-size: 0.85em; padding-left: 20px;'>
                <li>Consultant maps sacred architecture</li>
                <li>MCP enforces patterns automatically</li>
                <li>Champion defines "our way"</li>
            </ul>
            <p style='font-size: 0.9em; margin-top: 10px;'><strong>Result:</strong> Architecture persists despite AI automation</p>
        </div>
        """, unsafe_allow_html=True)

    with protect_col2:
        st.markdown("""
        <div style='background-color: #F3E5F5; padding: 15px; border-radius: 8px; border-left: 4px solid #9C27B0; min-height: 280px;'>
            <h4 style='color: #7B1FA2; margin-top: 0;'>🧠 Protecting Tribal Knowledge</h4>
            <p style='font-size: 0.9em;'><strong>Threat:</strong> Experts leave, knowledge evaporates, AI guesses wrong</p>
            <p style='font-size: 0.9em;'><strong>Solution:</strong></p>
            <ul style='font-size: 0.85em; padding-left: 20px;'>
                <li>Consultant extracts via workshop (VTCO)</li>
                <li>MCP surfaces at moment of need</li>
                <li>Champion updates as reality changes</li>
            </ul>
            <p style='font-size: 0.9em; margin-top: 10px;'><strong>Result:</strong> Knowledge lives in repo, not heads</p>
        </div>
        """, unsafe_allow_html=True)

    with protect_col3:
        st.markdown("""
        <div style='background-color: #FFF3E0; padding: 15px; border-radius: 8px; border-left: 4px solid #FF9800; min-height: 280px;'>
            <h4 style='color: #EF6C00; margin-top: 0;'>⚖️ Protecting Champion Expert Judgment</h4>
            <p style='font-size: 0.9em;'><strong>Threat:</strong> Champions burned out, become bottlenecks, lose autonomy</p>
            <p style='font-size: 0.9em;'><strong>Solution:</strong></p>
            <ul style='font-size: 0.85em; padding-left: 20px;'>
                <li>Consultant gives authority + time protection</li>
                <li>MCP filters noise (only exceptions reach them)</li>
                <li>Champion decides only judgment calls</li>
            </ul>
            <p style='font-size: 0.9em; margin-top: 10px;'><strong>Result:</strong> Champions enable scale; AI handles toil</p>
        </div>
        """, unsafe_allow_html=True)

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
