"""Framework & Architecture page - Comprehensive AI Readiness Assessment and governance framework."""
import sys
from pathlib import Path

# Ensure shared module is importable when run as Streamlit page
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

from shared import MATURITY_COLORS, ZONE_COLORS, ROLE_COLORS

# Initialize session state
if 'assessment_data' not in st.session_state:
    st.session_state.assessment_data = None

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

st.title("Universal AI Governance Framework")
st.subheader("Progressive Adoption & Entropy Management")

# COMPREHENSIVE AI READINESS ASSESSMENT
st.header("Comprehensive AI Readiness Assessment", divider=True)

assess_tabs = st.tabs(["A. Technical Infrastructure", "B. Organizational Maturity", "C. Current State Metrics", "D. Goals & Constraints"])

with assess_tabs[0]:
    st.subheader("A. Technical Infrastructure (5 questions)")
    col1, col2 = st.columns(2)
    with col1:
        q1_ai_tools = st.multiselect(
            "1. Which AI coding/development tools are currently in use?",
            ["None", "GitHub Copilot", "Cursor", "Claude Code", "Amazon CodeWhisperer", "Tabnine", "Custom internal tools", "ChatGPT/Claude web for coding", "Other"],
            default=["Cursor"]
        )
        q2_ide = st.multiselect(
            "2. Which IDEs are primary for your development team?",
            ["VS Code", "IntelliJ IDEA", "PyCharm", "Visual Studio", "Eclipse", "Vim/Neovim", "Cursor", "Windsurf", "Other"]
        )
        q3_cicd = st.selectbox(
            "3. CI/CD Pipeline maturity:",
            ["No automated pipelines", "Basic build automation", "Automated testing + deployment", "Full DevOps with monitoring", "GitOps/Advanced practices"]
        )
    with col2:
        q4_repo = st.selectbox(
            "4. Code repository platform:",
            ["GitHub", "GitLab", "Bitbucket", "Azure DevOps", "Self-hosted Git", "Multiple platforms"]
        )
        q5_languages = st.multiselect(
            "5. Primary programming languages:",
            ["Python", "Java", "JavaScript/TypeScript", "C/C++", "C#", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Other"]
        )

with assess_tabs[1]:
    st.subheader("B. Organizational Maturity (10 questions)")
    col1, col2 = st.columns(2)
    with col1:
        q6_governance = st.select_slider(
            "6. Current AI governance structure:",
            options=["None/Ad-hoc", "Informal guidelines", "Written policy (unenforced)", "Enforced via code review", "Automated enforcement (tools)"]
        )
        q7_champions = st.select_slider(
            "7. Champion/Expert program status:",
            options=["No identified experts", "Experts exist (no formal role)", "Champions identified", "Active champion program", "Structured with authority"]
        )
        q8_documentation = st.selectbox(
            "8. Architectural decision documentation:",
            ["No ADRs", "Some ADRs (inconsistent)", "Standard ADR process", "ADRs + automatic enforcement", "Full governance records"]
        )
        q9_training = st.selectbox(
            "9. AI tool training provided:",
            ["None", "Self-directed learning", "Workshops provided", "Structured onboarding", "Continuous learning program"]
        )
        q10_standards = st.selectbox(
            "10. Code standards enforcement:",
            ["No standards", "Standards documented (voluntary)", "Linting in CI", "Pre-commit hooks", "Full automated enforcement"]
        )
    with col2:
        q11_compliance = st.multiselect(
            "11. Compliance requirements (select all):",
            ["None", "SOC 2", "PCI-DSS", "HIPAA", "GDPR", "FedRAMP", "ISO 27001", "SOX", "Other industry-specific"]
        )
        q12_security = st.selectbox(
            "12. AI-generated code security review:",
            ["No special review", "Informal security checks", "Mandatory security review", "Automated security scanning", "Full SAST/DAST on AI code"]
        )
        q13_ownership = st.selectbox(
            "13. Clear code ownership (CODEOWNERS):",
            ["No ownership defined", "Team-level ownership", "File-level ownership", "Enforced via CODEOWNERS", "Automated + champion assignment"]
        )
        q14_onboarding = st.selectbox(
            "14. New developer onboarding to AI tools:",
            ["No onboarding", "Documentation only", "Mentor pairing", "Structured program", "AI-adaptive onboarding (scaffolding)"]
        )
        q15_feedback = st.selectbox(
            "15. Feedback loop for AI tool improvement:",
            ["No feedback collected", "Informal complaints", "Regular surveys", "Metrics-driven feedback", "Continuous improvement system"]
        )

with assess_tabs[2]:
    st.subheader("C. Current State Metrics (10 questions - self-reported estimates)")
    col1, col2 = st.columns(2)
    with col1:
        q16_adoption = st.slider(
            "16. Estimated AI tool adoption rate (% of team using regularly):",
            0, 100, 22
        )
        q17_acceptance = st.slider(
            "17. AI suggestion acceptance rate (% of suggestions kept):",
            0, 100, 45
        )
        q18_rework = st.slider(
            "18. Estimated rework rate on AI-generated code (% requiring significant revision):",
            0, 100, 34
        )
        q19_bugs = st.slider(
            "19. Production bugs attributed to AI code (per month):",
            0, 50, 5
        )
        q20_velocity = st.slider(
            "20. Current velocity trend over last 3 months:",
            -50, 50, -10,
            help="Negative = slowing down, Positive = speeding up"
        )
    with col2:
        q21_entropy = st.select_slider(
            "21. Perceived code complexity/chaos (Entropy self-assessment):",
            options=["Very clean (10-20)", "Manageable (20-40)", "Moderate concern (40-60)", "Significant drift (60-80)", "Chaos (80-100)"],
            help="Your intuition about technical debt and architectural consistency"
        )
        q22_confidence = st.select_slider(
            "22. Developer confidence in AI-generated code:",
            options=["Very low", "Low", "Moderate", "High", "Very high"]
        )
        q23_champion_time = st.slider(
            "23. % of champion/expert time spent on review/gatekeeping:",
            0, 100, 80
        )
        q24_documentation = st.slider(
            "24. % of critical knowledge documented (vs. in heads):",
            0, 100, 20
        )
        q25_satisfaction = st.select_slider(
            "25. Overall team satisfaction with current AI adoption:",
            options=["Very dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very satisfied"]
        )

with assess_tabs[3]:
    st.subheader("D. Goals & Constraints (5 questions)")
    col1, col2 = st.columns(2)
    with col1:
        q26_timeline = st.selectbox(
            "26. Target timeline for improvement:",
            ["Immediate (0-3 months)", "Short-term (3-6 months)", "Medium-term (6-12 months)", "Long-term (12+ months)"]
        )
        q27_budget = st.selectbox(
            "27. Consulting/training budget availability:",
            ["Minimal (DIY approach)", "Moderate (targeted help)", "Substantial (comprehensive program)", "Enterprise (full transformation)"]
        )
        q28_priority = st.multiselect(
            "28. Top priorities (select top 3):",
            ["Increase adoption rates", "Reduce rework/bugs", "Improve code quality", "Faster onboarding", "Preserve tribal knowledge", "Reduce champion bottleneck", "Compliance/audit readiness", "Developer satisfaction", "Velocity improvement", "Cost reduction"]
        )
    with col2:
        q29_blockers = st.multiselect(
            "29. Perceived blockers to adoption (select all):",
            ["Security concerns", "Quality concerns", "Lack of training", "No governance framework", "Developer resistance", "Tool limitations", "Management buy-in", "Time constraints", "Unclear ROI", "Compliance requirements"]
        )
        q30_success = st.text_area(
            "30. What does 'successful AI adoption' look like for your organization?",
            placeholder="Describe your vision for AI integration in 12 months...",
            height=100
        )

if st.button("Generate Comprehensive Maturity Assessment", type="primary"):
    infra_score = 0
    if len(q1_ai_tools) > 0 and "None" not in q1_ai_tools: infra_score += 5
    if q3_cicd in ["Automated testing + deployment", "Full DevOps with monitoring", "GitOps/Advanced practices"]: infra_score += 5
    if q4_repo in ["GitHub", "GitLab"]: infra_score += 5
    if len(q5_languages) > 0: infra_score += 5

    maturity_score = 0
    if q6_governance != "None/Ad-hoc": maturity_score += 8
    if q7_champions in ["Champions identified", "Active champion program", "Structured with authority"]: maturity_score += 8
    if q8_documentation in ["Standard ADR process", "ADRs + automatic enforcement", "Full governance records"]: maturity_score += 8
    if q9_training in ["Structured onboarding", "Continuous learning program"]: maturity_score += 8
    if q10_standards in ["Linting in CI", "Pre-commit hooks", "Full automated enforcement"]: maturity_score += 8

    current_score = 0
    if q16_adoption > 20: current_score += 6
    if q17_acceptance > 40: current_score += 6
    if q18_rework < 30: current_score += 6
    if q22_confidence in ["High", "Very high"]: current_score += 6
    if q25_satisfaction in ["Satisfied", "Very satisfied"]: current_score += 6

    readiness_score = 0
    if q26_timeline != "Long-term (12+ months)": readiness_score += 3
    if q27_budget in ["Moderate (targeted help)", "Substantial (comprehensive program)", "Enterprise (full transformation)"]: readiness_score += 4
    if len(q28_priority) > 0: readiness_score += 3

    total_score = infra_score + maturity_score + current_score + readiness_score

    if total_score < 25:
        maturity = "M1"
        color = "#808080"
        description = "CHAOS: Early stage, foundation building needed"
        next_steps = "Focus: Champion identification, basic governance structure, initial tooling setup"
    elif total_score < 50:
        maturity = "M2"
        color = "#FF8C00"
        description = "SHALLOW: Tools present but governance gaps"
        next_steps = "Focus: Zoning implementation, champion authority, MCP configuration, entropy tracking"
    elif total_score < 75:
        maturity = "M3"
        color = "#0066CC"
        description = "AGENTIC: Strong governance, scaling phase"
        next_steps = "Focus: Optimization, skill-based scaffolding refinement, predictive metrics"
    else:
        maturity = "M4"
        color = "#D4AF37"
        description = "AUTONOMOUS: Mature, self-optimizing system"
        next_steps = "Focus: Continuous improvement, autonomous optimization, innovation"

    st.session_state.assessment_data = {
        "maturity": maturity,
        "total_score": total_score,
        "infra_score": infra_score,
        "maturity_score": maturity_score,
        "current_score": current_score,
        "readiness_score": readiness_score,
        "responses": {
            "tools": q1_ai_tools,
            "languages": q5_languages,
            "adoption": q16_adoption,
            "rework": q18_rework,
            "entropy_perception": q21_entropy
        }
    }

    st.success("Comprehensive Assessment Complete!")
    result_col1, result_col2 = st.columns([1, 2])
    with result_col1:
        st.markdown(f"""
        <div style='background-color: {color}20; padding: 30px; border-radius: 15px; border-left: 8px solid {color}; text-align: center;'>
            <h2 style='color: {color}; margin: 0; font-size: 3em;'>{maturity}</h2>
            <p style='font-size: 1.2em; font-weight: bold; margin: 10px 0;'>{description}</p>
            <p style='font-size: 2em; margin: 10px 0;'>Score: {total_score}/100</p>
        </div>
        """, unsafe_allow_html=True)
    with result_col2:
        st.markdown("### Assessment Breakdown")
        st.write(f"**Infrastructure Readiness:** {infra_score}/20")
        st.progress(infra_score / 20)
        st.write(f"**Governance Maturity:** {maturity_score}/40")
        st.progress(maturity_score / 40)
        st.write(f"**Current State Health:** {current_score}/30")
        st.progress(current_score / 30)
        st.write(f"**Improvement Readiness:** {readiness_score}/10")
        st.progress(readiness_score / 10)
        st.info(f"**Recommended Next Steps:** {next_steps}")
    st.subheader("Detailed Recommendations")
    if infra_score < 10:
        st.warning("**Infrastructure Priority:** Establish basic CI/CD and consolidate on primary AI tools before governance implementation.")
    if maturity_score < 20:
        st.warning("**Governance Priority:** Identify and empower champions. Begin documentation of critical architectural decisions.")
    if current_score < 15:
        st.warning("**Adoption Priority:** Focus on training and confidence-building before scaling. High rework indicates need for scaffolding.")

# AI ADOPTION MATURITY MATRIX - Insert after assessment results, before Three Actors section
st.divider()
st.header("AI Adoption Maturity Matrix", divider=True)
st.markdown("**Begin with the end in mind:** This framework engineers progression from baseline chaos to autonomous governance through measurable entropy reduction.")

matrix_cols = st.columns(4)

with matrix_cols[0]:
    st.markdown(f"""
    <div style='background-color: {MATURITY_COLORS["M1"]}20; padding: 15px; border-radius: 5px; border-left: 5px solid {MATURITY_COLORS["M1"]}; height: 300px;'>
        <h4 style='color: {MATURITY_COLORS["M1"]}; margin-top: 0;'>M1: Chaos</h4>
        <p><strong>Exploration</strong></p>
        <div style='background-color: {MATURITY_COLORS["M1"]}; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block; margin: 10px 0;'>
            Entropy > 70
        </div>
        <p style='font-style: italic; font-size: 0.9em; margin: 10px 0;'>
            "The Wild West": Copilot writes code that breaks production; no zoning.
        </p>
        <p style='font-weight: bold; margin-top: 15px; font-size: 0.9em;'>
            High Rework & Tech Debt
        </p>
    </div>
    """, unsafe_allow_html=True)

with matrix_cols[1]:
    current_badge = "<div style='position: absolute; top: -10px; right: 10px; background-color: #FF8C00; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; font-weight: bold;'>CURRENT BASELINE</div>"
    st.markdown(f"""
    <div style='background-color: {MATURITY_COLORS["M2"]}20; padding: 15px; border-radius: 5px; border-left: 5px solid {MATURITY_COLORS["M2"]}; height: 300px; position: relative;'>
        {current_badge}
        <h4 style='color: {MATURITY_COLORS["M2"]}; margin-top: 0;'>M2: Shallow</h4>
        <p><strong>Installation</strong></p>
        <div style='background-color: {MATURITY_COLORS["M2"]}; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block; margin: 10px 0;'>
            Entropy 50 - 70
        </div>
        <p style='font-style: italic; font-size: 0.9em; margin: 10px 0;'>
            "Guided Learning": MCP blocks Red Zone edits; basic VTCO in place.
        </p>
        <p style='font-weight: bold; margin-top: 15px; font-size: 0.9em;'>
            Standardized Tooling
        </p>
    </div>
    """, unsafe_allow_html=True)

with matrix_cols[2]:
    target_badge = "<div style='position: absolute; top: -10px; right: 10px; background-color: #0066CC; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; font-weight: bold;'>TARGET STATE</div>"
    st.markdown(f"""
    <div style='background-color: {MATURITY_COLORS["M3"]}20; padding: 15px; border-radius: 5px; border-left: 5px solid {MATURITY_COLORS["M3"]}; height: 300px; position: relative;'>
        {target_badge}
        <h4 style='color: {MATURITY_COLORS["M3"]}; margin-top: 0;'>M3: Agentic</h4>
        <p><strong>Integration</strong></p>
        <div style='background-color: {MATURITY_COLORS["M3"]}; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block; margin: 10px 0;'>
            Entropy 30 - 50
        </div>
        <p style='font-style: italic; font-size: 0.9em; margin: 10px 0;'>
            "The Guardrail": MCP suggests patterns; Entropy logged per commit.
        </p>
        <p style='font-weight: bold; margin-top: 15px; font-size: 0.9em;'>
            106x Faster Lead Time
        </p>
    </div>
    """, unsafe_allow_html=True)

with matrix_cols[3]:
    st.markdown(f"""
    <div style='background-color: {MATURITY_COLORS["M4"]}20; padding: 15px; border-radius: 5px; border-left: 5px solid {MATURITY_COLORS["M4"]}; height: 300px;'>
        <h4 style='color: {MATURITY_COLORS["M4"]}; margin-top: 0;'>M4: Autonomous</h4>
        <p><strong>Optimization</strong></p>
        <div style='background-color: {MATURITY_COLORS["M4"]}; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block; margin: 10px 0;'>
            Entropy < 15
        </div>
        <p style='font-style: italic; font-size: 0.9em; margin: 10px 0;'>
            "Invisible Governance": High-quality code is auto-approved; zero "Bloat."
        </p>
        <p style='font-weight: bold; margin-top: 15px; font-size: 0.9em;'>
            208x More Deployments
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center; color: #666; margin-top: 20px; font-style: italic;'>
    The consulting engagement engineers the transition from M2 (baseline) to M3/M4 (target) through systematic entropy reduction.
</p>
""", unsafe_allow_html=True)
st.divider()

# PRE-PROJECT KICKOFF WORKSHOP SECTION
st.header("Pre-Project Kickoff Workshop", divider=True)
st.markdown("""
**90-Minute Facilitated Session**: From assessment to implementation plan  
**Participants**: SME Champions, Tech Lead, Engineering Manager  
**My Role**: AI Training Consultant guiding the workshop
""")

if 'workshop_phase' not in st.session_state:
    st.session_state.workshop_phase = "assessment_review"

workshop_tabs = st.tabs([
    "1. Assessment Review (15 min)",
    "2. Champion Identification (20 min)",
    "3. Zoning Mapping (15 min)",
    "4. Project Plan Generation"
])

with workshop_tabs[0]:
    st.markdown("""
    ### Current State Validation

    **Facilitator Script**: *"Your assessment shows M2 maturity with 68 entropy. This is typical for teams with AI tools but no governance. Let's validate this matches your experience."*

    **Discussion Points**:
    """)

    col1, col2 = st.columns(2)
    with col1:
        pain_point_1 = st.checkbox("Production incident from AI-generated code in last 3 months")
        pain_point_2 = st.checkbox("Champions spending >50% time on review/gatekeeping")
        pain_point_3 = st.checkbox("Novice developers avoiding AI tools due to fear")

    with col2:
        pain_point_4 = st.checkbox("No documented standards for AI-generated code")
        pain_point_5 = st.checkbox("Rework rate perceived as 'high' by team")

    st.text_area("Key Incidents to Address",
                 placeholder="Describe recent production issues or near-misses related to AI code...",
                 key="workshop_incidents")

    if pain_point_1 or pain_point_2 or pain_point_3:
        st.info("**Workshop Focus**: Governance structure and champion protection priority")

with workshop_tabs[1]:
    st.markdown("""
    ### Champion Mapping

    **Facilitator Script**: *"Champions are not managers—they're the experts everyone already goes to. We're formalizing their authority and protecting their time. Identify 3-5 champions across critical domains."*
    """)

    champion_data = []

    for i in range(1, 4):
        with st.expander(f"Champion {i}", expanded=(i == 1)):
            c_name = st.text_input("Name", key=f"c_name_{i}")
            c_role = st.text_input("Current Role", key=f"c_role_{i}")
            c_domain = st.selectbox("Domain Expertise",
                                   ["Database/Schema", "Security/Auth", "Payment Processing",
                                    "API/Integration", "DevOps/Infrastructure", "Frontend/UX",
                                    "Compliance/Audit"], key=f"c_domain_{i}")
            c_pain = st.text_area("Current Pain Point",
                                 placeholder="E.g., 'Constant interruptions for schema questions'",
                                 key=f"c_pain_{i}")
            c_priority = st.selectbox("First VTCO Priority",
                                     ["Database Schema Changes", "Security Configuration",
                                      "API Design Patterns", "Deployment Procedures",
                                      "Authentication Flows"], key=f"c_priority_{i}")

            if c_name:
                champion_data.append({
                    "name": c_name,
                    "role": c_role,
                    "domain": c_domain,
                    "pain": c_pain,
                    "first_vtco": c_priority
                })

    st.session_state.champion_data = champion_data

with workshop_tabs[2]:
    st.markdown("""
    ### Zoning Workshop

    **Facilitator Script**: *"Map your codebase to Red/Yellow/Green zones. Red = Champion-only (irreversible). Yellow = Validation required. Green = Autonomous execution."*
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Red Zone**")
        st.caption("Champion-only. Irreversible decisions.")
        red_zones = st.text_area("File Patterns",
                                value="migrations/*.sql\nsrc/payment/core.py\nconfig/production.yml\nsrc/security/auth.py",
                                height=150,
                                key="red_zones_input")

    with col2:
        st.markdown("**Yellow Zone**")
        st.caption("Validation required. Pattern matching.")
        yellow_zones = st.text_area("File Patterns",
                                   value="src/api/**/*.py\nsrc/integration/*\nsrc/services/*.py",
                                   height=150,
                                   key="yellow_zones_input")

    with col3:
        st.markdown("**Green Zone**")
        st.caption("Autonomous. Reversible changes.")
        green_zones = st.text_area("File Patterns",
                                  value="src/utils/*\ntests/*\ndocs/*\n*.md",
                                  height=150,
                                  key="green_zones_input")

with workshop_tabs[3]:
    st.markdown("""
    ### Implementation Project Plan

    **Facilitator Script**: *"Based on today's workshop, here's your 8-week roadmap from M2 to M3."*
    """)

    if st.button("Generate Complete Project Plan", type="primary", key="gen_plan"):
        if not st.session_state.get('champion_data'):
            st.warning("Please complete Champion Identification first")
        else:
            start_date = datetime.now()
            week_dates = {
                "Week 1": (start_date + timedelta(days=7)).strftime("%Y-%m-%d"),
                "Week 2": (start_date + timedelta(days=14)).strftime("%Y-%m-%d"),
                "Week 4": (start_date + timedelta(days=28)).strftime("%Y-%m-%d"),
                "Week 6": (start_date + timedelta(days=42)).strftime("%Y-%m-%d"),
                "Week 8": (start_date + timedelta(days=56)).strftime("%Y-%m-%d")
            }

            red_zones_val = st.session_state.get("red_zones_input", "migrations/*.sql\nsrc/payment/core.py")
            yellow_zones_val = st.session_state.get("yellow_zones_input", "src/api/**/*.py\nsrc/integration/*")
            green_zones_val = st.session_state.get("green_zones_input", "src/utils/*\ntests/*")

            project_plan = {
                "project_metadata": {
                    "project_name": "AI Adoption Accelerator",
                    "engagement_type": "8-Week Consulting Engagement",
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "target_maturity": "M3 (Agentic with Guardrails)",
                    "consultant_role": "AI Training Consultant",
                    "deliverable_format": "JSON"
                },
                "current_state_baseline": {
                    "maturity_level": "M2",
                    "maturity_description": "Shallow - Tools present but governance gaps",
                    "entropy_score": 68,
                    "entropy_status": "Above M3 threshold (30)",
                    "key_metrics": {
                        "adoption_rate": "22%",
                        "rework_rate": "34%",
                        "champion_coverage": f"{len(st.session_state.champion_data)} identified, 0 documented",
                        "red_zone_violations": "23/month (uncontrolled)"
                    },
                    "critical_gaps": [
                        "No VTCO documentation",
                        "No zoning enforcement",
                        "Champions burned out (80% review time)",
                        "High premature acceptance (41%)"
                    ]
                },
                "target_state": {
                    "maturity_level": "M3",
                    "maturity_description": "Agentic - Strong governance, scaling phase",
                    "entropy_score": "< 30",
                    "timeline_weeks": 8,
                    "success_criteria": [
                        "Entropy reduced from 68 to < 30",
                        "Red Zone violations < 5/month",
                        "Champion time on innovation > 65%",
                        "100% Red Zone coverage with VTCO docs",
                        "Novice developers autonomous in Green Zone"
                    ],
                    "business_outcomes": {
                        "velocity_improvement": "106x faster lead time (industry benchmark)",
                        "quality_improvement": "59% reduction in rework",
                        "champion_satisfaction": "65% time on innovation vs 20% baseline"
                    }
                },
                "workshop_outputs": {
                    "champions_identified": [
                        {
                            "name": c["name"],
                            "domain": c["domain"],
                            "first_vtco_topic": c["first_vtco"],
                            "pain_to_solve": c["pain"]
                        } for c in st.session_state.champion_data
                    ],
                    "zoning_map": {
                        "red_zone_patterns": [p.strip() for p in red_zones_val.split('\n') if p.strip()],
                        "yellow_zone_patterns": [p.strip() for p in yellow_zones_val.split('\n') if p.strip()],
                        "green_zone_patterns": [p.strip() for p in green_zones_val.split('\n') if p.strip()]
                    },
                    "priority_vtcos": [c["first_vtco"] for c in st.session_state.champion_data]
                },
                "execution_timeline": {
                    "week_1": {
                        "theme": "Foundation",
                        "deliverables": [
                            "Champion VTCO drafting session (2 hours)",
                            "Complete 3-5 VTCO documents (YAML format)",
                            "Validate zoning map with tech leads"
                        ],
                        "milestone": "Tribal knowledge documented",
                        "owner": "Consultant + Champions"
                    },
                    "week_2": {
                        "theme": "Configuration",
                        "deliverables": [
                            "Finalize governance_rules.yaml",
                            "Configure MCP server for Red Zone blocking",
                            "Set up .ai-governance/ directory structure"
                        ],
                        "milestone": "MCP enforcing Red Zone",
                        "owner": "Consultant + Tech Lead",
                        "checkpoint_meeting": week_dates["Week 2"]
                    },
                    "week_4": {
                        "theme": "Deployment",
                        "deliverables": [
                            "MCP server deployed to dev environment",
                            "Yellow Zone pattern validation active",
                            "Entropy logging operational"
                        ],
                        "milestone": "Governance active in development",
                        "owner": "Tech Lead",
                        "checkpoint_meeting": week_dates["Week 4"]
                    },
                    "week_6": {
                        "theme": "Adoption",
                        "deliverables": [
                            "Team training on role-based scaffolding",
                            "Novice mentor pairs assigned",
                            "Skill progression tracking enabled"
                        ],
                        "milestone": "Team operating under new governance",
                        "owner": "Champions + Engineering Manager",
                        "checkpoint_meeting": week_dates["Week 6"]
                    },
                    "week_8": {
                        "theme": "Validation & Exit",
                        "deliverables": [
                            "M3 maturity validation (entropy check)",
                            "Handoff documentation complete",
                            "Quarterly check-in schedule established"
                        ],
                        "milestone": "Consultant exit, team self-sufficient",
                        "owner": "Champions (ongoing)",
                        "checkpoint_meeting": week_dates["Week 8"]
                    }
                },
                "immediate_action_items": [
                    {"task": "Schedule Champion VTCO drafting session", "due": "This week", "owner": "Champions", "deliverable": "3-5 completed VTCO YAML files"},
                    {"task": "Identify 'Code Red' files for immediate protection", "due": "Week 1", "owner": "Tech Lead", "deliverable": "List of files requiring immediate MCP blocking"},
                    {"task": "Set up .ai-governance/ directory in repository", "due": "Week 1", "owner": "DevOps/Tech Lead", "deliverable": "Repository structure ready"},
                    {"task": "Assign mentor pairs for Novice developers", "due": "Week 2", "owner": "Engineering Manager", "deliverable": "Mentor assignments documented"}
                ],
                "risk_mitigation": [
                    {"risk": "Champions unavailable for VTCO drafting", "mitigation": "Break into 30-min sessions, use voice-to-text for speed", "trigger": "Week 1 deliverable at risk"},
                    {"risk": "MCP blocks too aggressively (Yellow/Green overlap)", "mitigation": "Adjust file patterns, add override for emergencies", "trigger": "Developer complaints in Week 2-3"},
                    {"risk": "Adoption drops during transition (M2 to M3 dip)", "mitigation": "Monitor entropy weekly, adjust scaffolding levels", "trigger": "Entropy increases for 2 consecutive weeks"}
                ],
                "deliverables_repository": {
                    "directory_structure": [
                        ".ai-governance/",
                        "  tribal-knowledge/",
                        "    payment_processing.yaml (VTCO)",
                        "    database_schema.yaml (VTCO)",
                        "    [champion_domain].yaml (VTCOs)",
                        "  entropy_log.jsonl",
                        "  violations.jsonl",
                        "  governance_rules.yaml"
                    ],
                    "file_formats": {
                        "vtcos": "YAML (Verb-Task-Constraint-Outcome)",
                        "logs": "JSON Lines (append-only)",
                        "rules": "YAML (zoning and scaffolding config)"
                    }
                }
            }

            st.success("Project Plan Generated from Workshop Data")

            dl_col1, dl_col2 = st.columns(2)

            with dl_col1:
                st.download_button(
                    label="Download Project Plan (JSON)",
                    data=json.dumps(project_plan, indent=2),
                    file_name=f"ai_adoption_project_plan_{start_date.strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True,
                    key="dl_plan"
                )

            with dl_col2:
                first_vtco_topic = st.session_state.champion_data[0]["first_vtco"] if st.session_state.champion_data else "Database Schema Changes"
                first_champion = st.session_state.champion_data[0]["name"] if st.session_state.champion_data else "Champion_Name"
                first_domain = st.session_state.champion_data[0]["domain"] if st.session_state.champion_data else "Database/Schema"

                vtco_template = f"""# VTCO: {first_vtco_topic}
# Generated from Kickoff Workshop
domain: "{first_domain.lower().replace('/', '_')}"
champion_owner: "{first_champion}"
sdlc_phase: "Design-Database"
created_date: "{start_date.strftime('%Y-%m-%d')}"
last_validated: "{start_date.strftime('%Y-%m-%d')}"

vtco_definition:
  verb: "Modify"
  task: "{first_vtco_topic} in production environment"
  constraints:
    technical:
      - "[Constraint from workshop discussion]"
      - "Zero downtime requirement"
      - "Rollback script verified before deployment"
    compliance:
      - "[Compliance requirement identified in workshop]"
    performance:
      - "Query latency p95 < 50ms post-change"
  outcome: "Safe deployment with full audit trail and zero incidents"

governance_rules:
  zone: "Red"
  m_level_requirement: "M4"
  ai_behavior:
    allowed:
      - "Explain risks and alternatives"
      - "Review rollback script syntax"
      - "Suggest testing strategies"
    forbidden:
      - "Generate final deployment commands"
      - "Approve changes without champion sign-off"
      - "Bypass safety constraints"
    on_violation: "Block and trigger ADR (Architectural Decision Record)"
    scaffolding: "Explain architectural implications to requesting developer"

escalation_path:
  if_ai_uncertain: "Flag for {first_champion} review"
  if_constraints_conflict: "Schedule emergency architecture review"
  emergency_contact: "[champion_email@company.com]"
  adr_required: true

ai_reminder: "This is RED ZONE - requires {first_champion} approval. Do not proceed without champion sign-off."
"""

                st.download_button(
                    label="Download VTCO Template (YAML)",
                    data=vtco_template,
                    file_name=f"vtco_{first_domain.lower().replace('/', '_').replace(' ', '_')}.yaml",
                    mime="text/yaml",
                    use_container_width=True,
                    key="dl_vtco"
                )

            st.subheader("Workshop Summary Dashboard")

            sum_col1, sum_col2, sum_col3 = st.columns(3)
            with sum_col1:
                st.metric("Champions Identified", len(st.session_state.champion_data))
                st.metric("Red Zone Patterns", len([p for p in red_zones_val.split('\n') if p.strip()]))
            with sum_col2:
                st.metric("Start Date", start_date.strftime("%b %d"))
                st.metric("Target M3 Date", week_dates["Week 8"])
            with sum_col3:
                st.metric("Current Entropy", "68", delta="-38 to M3")
                st.metric("Consultant Exit", "Week 8")

            champion_names = ", ".join([c["name"] for c in st.session_state.champion_data])
            st.info(f"**Next Step**: Schedule Champion VTCO drafting session with {champion_names} for this week. Goal: Complete {len(st.session_state.champion_data)} VTCO documents.")

st.divider()

# THREE ACTORS IN GOVERNANCE (Demo-Ready Version)
st.header("Three Actors in Governance", divider=True)

st.markdown("*A lean consulting architecture for AI adoption*")

# Actor 1: Zubia (Consultant) - In Expander
with st.expander("**Zubia** — AI Training Consultant (8-week engagement)", expanded=False):
    st.caption("*I set up the system, train your champions, then exit.*")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**What I Do:**")
        st.write("• Assess M1-M4 maturity")
        st.write("• Architect Red/Yellow/Green zones")
        st.write("• Facilitate champion workshop")
        st.write("• Configure MCP server")
        st.write("• Build entropy dashboard")
        st.write("• **EXIT at M3/M4**")

    with col2:
        st.write("**What I DON'T Do:**")
        st.write("• Write your production code")
        st.write("• Make architectural decisions (champions do)")
        st.write("• Enforce daily (MCP does)")
        st.write("• Stay forever (lean consulting)")

    st.info("\"*I build the system that protects your experts, then I leave.*\"")

    st.markdown("""
    <details style='margin-top: 10px;'>
        <summary style='cursor: pointer; font-weight: 500;'>? My Methodology</summary>
        <p style='margin: 8px 0 0 0; font-size: 0.9em;'>Workforce development + ML systems. I bring the governance framework, configure the technical infrastructure, and enable your champions to scale without me.</p>
    </details>
    """, unsafe_allow_html=True)

# Actor 2: MCP Server - In Expander
with st.expander("**MCP Server** — Technical Enforcer (Local Python script)", expanded=False):
    st.caption("*The automation layer—blocks, scaffolds, and measures.*")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**What It Does:**")
        st.write("• Guards Red Zone (blocks edits)")
        st.write("• Scaffolds by skill (Novice=verbose)")
        st.write("• Counts entropy metrics")
        st.write("• Reminds of constraints")
        st.write("• Blocks rule violations")

    with col2:
        st.write("**What It CANNOT Do:**")
        st.write("• Know business priority")
        st.write("• Write tribal knowledge")
        st.write("• Judge promotion readiness")
        st.write("• Build human trust")
        st.write("• Override emergencies")

    st.info("\"*Not a data center. One Python file. USB-C for AI.*\"")

    st.markdown("""
    <details style='margin-top: 10px;'>
        <summary style='cursor: pointer; font-weight: 500;'>? Technical Reality</summary>
        <p style='margin: 8px 0 0 0; font-size: 0.9em;'>The Model Context Protocol is a local script that Cursor/Copilot call for context. It's lightweight, standardized, and runs on the developer's machine—not cloud infrastructure.</p>
    </details>
    """, unsafe_allow_html=True)

# Actor 3: Champion - In Expander
with st.expander("**Champion** — Your Domain Expert (Protected & Enabled)", expanded=False):
    st.caption("*The human authority—owns decisions, mentors, defines patterns.*")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**What They Own:**")
        st.write("• Red Zone decisions (veto power)")
        st.write("• Tribal knowledge (VTCO docs)")
        st.write("• Skill assessment")
        st.write("• Mentoring")
        st.write("• Emergency override")
        st.write("• Pattern definition")

    with col2:
        st.write("**What They DON'T Do:**")
        st.write("• Manual enforcement (MCP blocks)")
        st.write("• 20-page docs (structured YAML)")
        st.write("• Boilerplate review (automated)")
        st.write("• 24/7 availability (protected)")

    st.info("\"*Your most expensive expertise. Amplified, not replaced. Protected from burnout.*\"")

    st.markdown("""
    <details style='margin-top: 10px;'>
        <summary style='cursor: pointer; font-weight: 500;'>? Champion Protection</summary>
        <p style='margin: 8px 0 0 0; font-size: 0.9em;'>MCP filters noise so only true Red Zone decisions reach them. They spend 65% time on innovation (not gatekeeping) by M3.</p>
    </details>
    """, unsafe_allow_html=True)

# Visual Summary (Compact)
st.divider()
st.caption("**The Flow:** Zubia configures → MCP enforces → Champion decides → Team adopts → Entropy drops → Consultant exits")

# Optional: Show interaction diagram in nested expander
with st.expander("View Week-by-Week Engagement Timeline"):
    timeline_data = {
        "Week": ["0-1", "2-4", "5-8", "9-12"],
        "Zubia": ["Assessment + Workshop", "Train + Dashboard", "Check-in (fading)", "EXIT (quarterly only)"],
        "MCP": ["Install + Configure", "Enforce zones", "Auto-promotions", "Autonomous"],
        "Champion": ["Provide knowledge", "Learn VTCO", "Own Red Zone", "Full authority"]
    }
    st.dataframe(pd.DataFrame(timeline_data), use_container_width=True, hide_index=True)

# Protection Architecture - IMPROVED
st.header("Protection Architecture", divider=True)

protect_col1, protect_col2, protect_col3 = st.columns([1, 1, 1], gap="medium")

with protect_col1:
    st.markdown("""
    <div style='background-color: #E3F2FD; padding: 15px; border-radius: 8px; border-left: 4px solid #2196F3; min-height: 280px;'>
        <h4 style='color: #1565C0; margin-top: 0;'>Protecting Human Coding Architecture</h4>
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
        <h4 style='color: #7B1FA2; margin-top: 0;'>Protecting Tribal Knowledge</h4>
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
        <h4 style='color: #EF6C00; margin-top: 0;'>Protecting Champion Expert Judgment</h4>
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

# COMPLETE SDLC ZONING MATRIX
st.header("The Zoning Matrix: SDLC × Risk Levels", divider=True)
st.markdown("""
The Zoning Matrix maps every Software Development Life Cycle (SDLC) phase to a Risk Zone (Red/Yellow/Green)
based on reversibility, compliance requirements, and tribal knowledge intensity.
""")
zoning_data = {
    "SDLC Phase": [
        "Requirements", "Requirements", "Design", "Design", "Implementation", "Implementation", "Implementation",
        "Testing", "Testing", "Testing", "Deployment", "Deployment", "Monitoring", "Monitoring"
    ],
    "Task Example": [
        "Security compliance mapping", "Feature scope definition", "Database schema design", "UI component selection",
        "Business logic (payment)", "CRUD operations", "Integration patterns", "Security pen testing",
        "Unit test generation", "Integration testing", "Production release", "CI/CD configuration",
        "Alert threshold tuning", "Dashboard creation"
    ],
    "Zone": [
        "RED", "YELLOW", "RED", "GREEN", "RED", "GREEN", "YELLOW",
        "RED", "GREEN", "YELLOW", "RED", "YELLOW", "RED", "GREEN"
    ],
    "Risk Rationale": [
        "Compliance violations irreversible", "Scope creep affects timeline", "Schema changes expensive",
        "Components easily reversible", "Financial impact if wrong", "Standard patterns, reversible",
        "Integration failures cascade", "Security breaches catastrophic", "Tests easily regenerated",
        "Requires realistic data", "Production downtime costly", "Pipeline affects all devs",
        "Alert fatigue burns teams", "Dashboards easily modified"
    ],
    "Human Role": [
        "Champion defines threat model", "Tech Lead validates boundaries", "Data Architect designs",
        "Developer reviews brand", "Senior Engineer writes core", "Junior Developer implements",
        "Mid-level validates fit", "Security Champion executes", "Developer reviews coverage",
        "QA Engineer designs scenarios", "DevOps Champion approves", "DevOps Engineer maintains",
        "SRE Champion sets thresholds", "Developer adds metrics"
    ],
    "AI Role": [
        "Suggests frameworks only", "Generates user stories", "Analyzes patterns, warns",
        "Generates component code", "Explains existing code", "Generates boilerplate",
        "Suggests approaches", "Generates test scenarios", "Generates test cases",
        "Generates test data", "Checks logs, suggests rollback", "Suggests optimizations",
        "Analyzes patterns", "Generates queries"
    ],
    "Key Constraints": [
        "PCI-DSS, <100ms latency", "OpenAPI 3.0, backward compatible", "GDPR deletion, 10M+ rows",
        "WCAG 2.1 AA, <50KB", "Thread-safe, 99.99% accurate", "Use BaseController, JWT auth",
        "Circuit breaker, <5s timeout", "Zero critical vulns", ">80% branch coverage",
        "Real DB, <30s execution", "Blue-green, auto-rollback", "Parallel execution, <10min",
        "<2min detection, <5 false pos", "95th percentile view"
    ],
    "MCP Enforcement": [
        "Block edits, require ADR", "Require validation checkpoint", "Block schema changes",
        "Complexity <10 auto-approve", "Block implementation, suggest only", "Auto-approve if tests pass",
        "Pattern match required", "Block without security review", "Auto-generate, coverage check",
        "Require data validation", "Block without approval chain", "Config validation only",
        "Block threshold changes", "Auto-approve"
    ]
}
zoning_df = pd.DataFrame(zoning_data)
st.dataframe(zoning_df, use_container_width=True)
zone_summary_col1, zone_summary_col2, zone_summary_col3 = st.columns(3)
with zone_summary_col1:
    st.markdown("""
    <div style='background-color: #DC143C20; padding: 20px; border-radius: 10px; border-left: 5px solid #DC143C;'>
        <h4 style='color: #DC143C; margin-top: 0;'>RED ZONE</h4>
        <p><strong>Architectural Authority</strong></p>
        <ul>
            <li>Irreversible decisions</li>
            <li>Compliance boundaries</li>
            <li>Tribal knowledge critical</li>
        </ul>
        <p><strong>AI:</strong> Suggest only</p>
        <p><strong>Human:</strong> Champion owns</p>
        <p><strong>MCP:</strong> Blocks unauthorized edits</p>
    </div>
    """, unsafe_allow_html=True)
with zone_summary_col2:
    st.markdown("""
    <div style='background-color: #FFD70020; padding: 20px; border-radius: 10px; border-left: 5px solid #FFD700;'>
        <h4 style='color: #B8860B; margin-top: 0;'>YELLOW ZONE</h4>
        <p><strong>Collaborative Implementation</strong></p>
        <ul>
            <li>Pattern implementation</li>
            <li>Integration points</li>
            <li>Complex features</li>
        </ul>
        <p><strong>AI:</strong> Generate with validation</p>
        <p><strong>Human:</strong> Validate against patterns</p>
        <p><strong>MCP:</strong> Enforces pattern matching</p>
    </div>
    """, unsafe_allow_html=True)
with zone_summary_col3:
    st.markdown("""
    <div style='background-color: #228B2220; padding: 20px; border-radius: 10px; border-left: 5px solid #228B22;'>
        <h4 style='color: #228B22; margin-top: 0;'>GREEN ZONE</h4>
        <p><strong>Autonomous Execution</strong></p>
        <ul>
            <li>Standard tasks</li>
            <li>Boilerplate code</li>
            <li>Reversible changes</li>
        </ul>
        <p><strong>AI:</strong> Full autonomy</p>
        <p><strong>Human:</strong> Monitor, spot-check</p>
        <p><strong>MCP:</strong> Automated CI/CD gates</p>
    </div>
    """, unsafe_allow_html=True)

# ROLE-BASED SKILLS & SMART GOALS
st.header("Role-Based Skills & SMART Goals Architecture", divider=True)
st.markdown("""
The framework adapts AI assistance based on developer capability (ZPD - Zone of Proximal Development)
with time-bound, measurable progression goals.
""")
skills_expander = st.expander("View Complete Skill Matrix & SMART Goals Framework", expanded=True)
with skills_expander:
    skills_data = {
        "Role Level": ["Novice", "Intermediate", "Expert", "Champion"],
        "Experience": ["0-2 years", "2-5 years", "5+ years", "7+ years + Domain Expertise"],
        "Zone Permissions": [
            "Green: Full / Yellow: With mentor / Red: Read-only",
            "Green: Full / Yellow: Full / Red: Suggest only",
            "Green: Full / Yellow: Full / Red: Draft proposals",
            "Green: Governs / Yellow: Governs / Red: Owns decisions"
        ],
        "Current Capabilities": [
            "Learning patterns, needs guidance on all tasks",
            "Solid execution, occasional architectural gaps",
            "Complex problem solving, designs new patterns",
            "Sets standards, owns architecture, defines direction"
        ],
        "SMART Goal Example (4-week)": [
            "Complete 10 Green Zone PRs with avg complexity <5",
            "Zero reverts for 30 days, complete 1 Yellow Zone validation",
            "Mentor 2 Novices through Yellow transitions, draft Red proposal",
            "Document 3 tribal knowledge VTCOs, enable 2 promotions"
        ],
        "Measurable Criteria": [
            "10 PRs merged, complexity ≤5, 0 critical feedback",
            "0 revert commits, 1 Yellow PR approved, mentor sign-off",
            "2 successful mentee promotions, 1 ADR drafted",
            "3 VTCO docs merged, 2 developers promoted to Intermediate"
        ],
        "AI Scaffolding Level": [
            "MAXIMUM: Explain every line, simple patterns only, max complexity 5",
            "MODERATE: Key decisions explained, standard patterns, max complexity 10",
            "MINIMAL: Architecture focus, edge cases only, max complexity 15",
            "CONSULTATIVE: Strategic oversight, innovation focus, no limits"
        ],
        "MCP Configuration": [
            "High verbosity, mandatory explanations, complexity cap 5, mentor required for Yellow",
            "Medium verbosity, pattern validation required, complexity cap 10",
            "Low verbosity, full pattern library, complexity cap 15",
            "Constraint definition authority, entropy monitoring, governance override"
        ],
        "Auto-Promotion Criteria": [
            "10 consecutive PRs under complexity 5, 0 reverts, mentor recommendation",
            "30 days 0 reverts, 3 Yellow Zone validations, peer feedback positive",
            "2 successful mentees, 1 accepted Red Zone proposal, champion nomination",
            "N/A - Champion role requires nomination + documented expertise"
        ],
        "Time to Next Level": ["4-8 weeks typical", "8-16 weeks typical", "16-24 weeks typical", "Ongoing - Continuous improvement"]
    }
    skills_df = pd.DataFrame(skills_data)
    st.dataframe(skills_df, use_container_width=True)
    st.info("""
    **Zone of Proximal Development (ZPD) Connection:**
    - **Novice:** Requires maximum scaffolding (AI explains everything) - they're in ZPD for most tasks
    - **Intermediate:** Moderate scaffolding - can work independently in Green, needs support in Yellow
    - **Expert:** Minimal scaffolding - only architecturally complex tasks are in their ZPD
    - **Champion:** Consultative - their ZPD is strategic; routine work is below their capability

    The MCP server automatically adjusts AI behavior based on role, ensuring optimal challenge without overwhelm.
    """)
    st.subheader("SMART Goals Framework")
    smart_col1, smart_col2 = st.columns(2)
    with smart_col1:
        st.markdown("""
        **S - Specific**
        - Exact task and complexity metric
        - Clear zone permissions
        - Defined deliverable

        **M - Measurable**
        - Git-based metrics (PR count, complexity scores)
        - Revert rate (objective, can't fabricate)
        - Mentor/champion validation (human checkpoint)

        **A - Achievable**
        - Based on current capability assessment
        - Progressive difficulty (4-week sprints)
        - Support resources identified
        """)
    with smart_col2:
        st.markdown("""
        **R - Relevant**
        - Progresses toward next skill level
        - Addresses current pain points
        - Aligns with team needs

        **T - Time-Bound**
        - 4-week sprint cycles
        - Weekly check-ins
        - Clear deadline with consequences

        **Evidence Source:**
        All metrics come from git history (objective), not self-reporting:
        - PR metadata (complexity, review time)
        - Commit history (reverts, rework)
        - MCP logs (zone violations, scaffold effectiveness)
        """)
    progression_data = {
        "Week": ["1", "2", "4", "6", "8"],
        "Goal": [
            "Complete 2 Green PRs, complexity <5",
            "Complete 5 Green PRs, complexity <5",
            "Complete 10 Green PRs, 0 reverts",
            "Attempt 1 Yellow PR with mentor",
            "Complete 1 Yellow validation, promoted to Intermediate"
        ],
        "MCP Scaffold": [
            "Maximum: Explain every line",
            "Maximum: Pattern suggestions",
            "High: Reduce verbosity slightly",
            "Moderate: Mentor checkpoint required",
            "Moderate: Standard Intermediate scaffolding"
        ],
        "Evidence": [
            "2 PRs merged, avg complexity 4.2",
            "5 PRs merged, avg complexity 4.5",
            "10 PRs merged, 0 revert commits",
            "1 Yellow PR opened, mentor assigned",
            "1 Yellow PR approved, auto-promoted by MCP"
        ],
        "Status": ["[On Track]", "[On Track]", "[Exceeding]", "[On Track]", "[PROMOTED]"]
    }
    st.dataframe(pd.DataFrame(progression_data), use_container_width=True)
    st.success("""
    **The Result:** Objective, git-based promotion with full audit trail.
    No manager bias, no gaming the system, clear capability demonstration.
    MCP automatically adjusts scaffolding level upon promotion.
    """)

# VTCO DOCUMENTATION STANDARD
st.header("VTCO: Tribal Knowledge Capture", divider=True)
st.markdown("""
**Verb-Task-Constraint-Outcome** - The structured format for capturing expert knowledge
""")
vtco_example = """
# Example: Payment Processing (Red Zone)
domain: payment_processing
champion_owner: sarah_chen
last_validated: 2026-02-28

vtc_o:
  verb: Architect
  task: Design database schema for payment processing subsystem
  constraints:
    technical:
      - "Normalized to 3NF except performance-critical paths"
      - "Immutable ledger pattern (INSERTS only, no UPDATES)"
      - "AES-256 encryption for PAN data"
    compliance:
      - "PCI-DSS Level 1 (no raw card data in logs)"
      - "GDPR hard-delete capability"
      - "SOX audit trail for adjustments"
    performance:
      - "Query latency p95 <50ms"
      - "Support 10K TPS peak load"
      - "Sharding by merchant_id"
  outcome: |
    ADR-024 approved and documented with:
    1. Schema migration scripts (forward + rollback)
    2. Entity-relationship diagram
    3. Privacy impact assessment
    4. Performance benchmarks
    5. Champion sign-off

ai_behavior:
  allowed: |
    - Suggest indexing strategies
    - Explain normalization tradeoffs
    - Warn on PCI violations in suggested schemas
  forbidden: |
    - Generate final CREATE TABLE statements
    - Select sharding strategy
    - Approve schema changes
  reminder: "This is RED ZONE - requires sarah_chen approval"

escalation_path:
  if_ai_uncertain: "Flag for champion review"
  if_constraints_conflict: "Schedule architecture review board"
  emergency_contact: "sarah_chen@company.com"
"""
st.code(vtco_example, language="yaml")
st.caption("""
VTCO documents live in the repo (`.ai-governance/tribal-knowledge/`),
version-controlled alongside code. Champions update them (5-min updates),
MCP surfaces them at moment of need (file open = context popup).
""")
