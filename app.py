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
        st.balloons()

    # THREE ACTORS IN GOVERNANCE (Streamlit-native, no HTML)
    st.header("Three Actors in Governance", divider=True)

    actor_col1, actor_col2, actor_col3 = st.columns([1, 1, 1], gap="large")

    with actor_col1:
        st.subheader("AI Training Consultant")
        st.caption("You/The Consultant")
        st.divider()

        st.write("**What You Do:**")
        st.write("• Assess M1-M4 maturity levels")
        st.write("• Architect zone structure (Red/Yellow/Green)")
        st.write("• Facilitate champion workshops")
        st.write("• Configure MCP server")
        st.write("• Train champions (teach the teachers)")
        st.write("• Build entropy dashboards")
        st.write("• EXIT at M3/M4 (consultant fades)")

        st.write("")
        st.write("**What You DON'T Do:**")
        st.write("• Write production code")
        st.write("• Make architectural decisions")
        st.write("• Enforce rules daily")
        st.write("• Stay forever (lean consulting)")

        st.write("")
        st.info("\"I build the system that protects your experts, then I leave.\"")

        with st.expander("? Consultant Details"):
            st.write("Brings methodology, MCP configuration, and change management. Sets up system in 2-3 weeks, then fades to quarterly check-ins.")

    with actor_col2:
        st.subheader("MCP Server")
        st.caption("The Technical Enforcer")
        st.divider()

        st.write("**What It Does:**")
        st.write("• Guards Red Zone files (blocks unauthorized edits)")
        st.write("• Scaffolds based on skill (Novice=verbose, Expert=terse)")
        st.write("• Counts entropy metrics automatically")
        st.write("• Reminds of VTCO constraints")
        st.write("• Blocks commits violating rules")

        st.write("")
        st.write("**What It CANNOT Do:**")
        st.write("• Know business priority (champions decide this)")
        st.write("• Write tribal knowledge (champions author this)")
        st.write("• Judge promotion readiness (champions assess this)")
        st.write("• Build trust with humans (champions do this)")
        st.write("• Override emergencies (champions govern this)")

        st.write("")
        st.info("\"Not a data center. One Python file. The 'server' just means it responds to Cursor/Copilot requests.\"")

        with st.expander("? MCP Details"):
            st.write("The Model Context Protocol is like USB-C for AI. Lightweight, local, standardized. Exposes 'tools' that AI assistants call to check zones and validate code.")

    with actor_col3:
        st.subheader("Champion")
        st.caption("The Human Expert")
        st.divider()

        st.write("**What They Own:**")
        st.write("• Red Zone Decisions (veto power)")
        st.write("• Tribal Knowledge (VTCO docs)")
        st.write("• Skill Assessment (Novice vs Expert)")
        st.write("• Mentoring (human coaching)")
        st.write("• Governance Override (emergency judgment)")
        st.write("• Pattern Definition (\"our way\")")

        st.write("")
        st.write("**What They DON'T Do:**")
        st.write("• Manual enforcement (MCP blocks automatically)")
        st.write("• 20-page docs (VTCO is structured YAML)")
        st.write("• Review boilerplate (Green Zone is automated)")
        st.write("• 24/7 availability (protected time)")

        st.write("")
        st.info("\"The most expensive expertise. Amplified, not replaced. Protected from becoming a bottleneck.\"")

        with st.expander("? Champion Details"):
            st.write("Protected from burnout by MCP automation. Authority formalized via CODEOWNERS. Only true Red Zone decisions reach them.")

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
            "🔴 RED", "🟡 YELLOW", "🔴 RED", "🟢 GREEN", "🔴 RED", "🟢 GREEN", "🟡 YELLOW",
            "🔴 RED", "🟢 GREEN", "🟡 YELLOW", "🔴 RED", "🟡 YELLOW", "🔴 RED", "🟢 GREEN"
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
            <h4 style='color: #DC143C; margin-top: 0;'>🔴 RED ZONE</h4>
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
            <h4 style='color: #B8860B; margin-top: 0;'>🟡 YELLOW ZONE</h4>
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
            <h4 style='color: #228B22; margin-top: 0;'>🟢 GREEN ZONE</h4>
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
    skills_expander = st.expander("📊 View Complete Skill Matrix & SMART Goals Framework", expanded=True)
    with skills_expander:
        skills_data = {
            "Role Level": ["Novice", "Intermediate", "Expert", "Champion"],
            "Experience": ["0-2 years", "2-5 years", "5+ years", "7+ years + Domain Expertise"],
            "Zone Permissions": [
                "🟢 Green: Full\n🟡 Yellow: With mentor\n🔴 Red: Read-only",
                "🟢 Green: Full\n🟡 Yellow: Full\n🔴 Red: Suggest only",
                "🟢 Green: Full\n🟡 Yellow: Full\n🔴 Red: Draft proposals",
                "🟢 Green: Governs\n🟡 Yellow: Governs\n🔴 Red: Owns decisions"
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
            "Status": ["🟡 On Track", "🟡 On Track", "🟢 Exceeding", "🟡 On Track", "🟢 PROMOTED"]
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
