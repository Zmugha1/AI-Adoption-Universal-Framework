import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from shared import render_sidebar

st.set_page_config(page_title="Developer Experience", page_icon="●")
render_sidebar(use_nav_radio=False)

# Color constants
RED = "#DC143C"
YELLOW = "#DAA520"
GREEN = "#228B22"
BLUE = "#0066CC"
ORANGE = "#FF8C00"
GRAY = "#808080"
GOLD = "#DAA520"

def zone_badge(zone, color):
    return f'<span style="background-color: {color}; color: white; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 0.9em;">{zone}</span>'

def maturity_badge(level, color, desc):
    return f'<span style="background-color: {color}; color: white; padding: 4px 12px; border-radius: 4px; font-weight: bold;">{level}</span> <span style="color: {color}; font-weight: 600;">{desc}</span>'

st.title("Developer Experience")
st.subheader("The Novice Journey: Framework Instantiation")
st.caption("Complete visibility into how Zubia (Novice) interacts with the MCP governance layer")

# Create four tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Day 1: Red Zone Protection",
    "Week 1: Green Zone Learning",
    "Week 4: Auto-Promotion",
    "Framework Mechanics"
])

# TAB 1: Day 1 - Complete visibility of protection
with tab1:
    st.header("Day 1: Red Zone Protection")
    st.markdown(zone_badge("RED ZONE", RED), unsafe_allow_html=True)

    st.write("**Scenario:** I (Zubia) join as a Junior Data Scientist. Python background, learning Java. I attempt to open TransactionProcessor.java.")

    # Split view: File tree and MCP response
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Repository Structure")
        st.code("""
src/
├── payment/
│   └── TransactionProcessor.java  [RED ZONE]
│   └── PaymentGateway.java        [RED ZONE]
├── api/
│   └── routes.java                [YELLOW ZONE]
└── utils/
    └── Calculator.java            [GREEN ZONE]
        """, language="text")

        st.write("**My Status:**")
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 12px; border-left: 4px solid {RED}; font-family: monospace;">
        Developer ID: zubia_mughal<br>
        Skill Level: <span style="color: {BLUE}; font-weight: bold;">NOVICE</span><br>
        Mentor: sarah_chen<br>
        Zone Access: <span style="color: {GREEN};">Green: YES</span> |
        <span style="color: {YELLOW};">Yellow: NO</span> |
        <span style="color: {RED};">Red: READ-ONLY</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("MCP Server Response")
        st.error("ACCESS DENIED")
        st.code("""
// MCP Server Tool Call: check_edit_permission
// File: src/payment/TransactionProcessor.java
// Developer: zubia_mughal

{
  "can_edit": false,
  "zone": "red",
  "developer_level": "novice",
  "reason": "RED ZONE: Payment Processing.
             Requires Champion approval.",
  "champion_owner": "sarah_chen",
  "vtc_o_reference": "payment-processing.yml"
}
        """, language="json")

        st.info("""
**Cursor IDE displays:**
"This file is in the RED ZONE - Payment Processing.

You have READ-ONLY access because:
• PCI-DSS compliance requirements
• Your current skill level: Novice
• Champion approval required

Contact: sarah_chen@company.com"
        """)

    # Framework visibility section
    st.divider()
    st.subheader("Framework Visibility: Protection Layer")

    viz_col1, viz_col2, viz_col3 = st.columns(3)

    with viz_col1:
        st.write("**Zubia (Consultant) configured:**")
        st.write("• Zones mapped (payment/ = RED)")
        st.write("• My profile set to Novice")
        st.write("• Champion assigned (Sarah)")
        st.write("• MCP server deployed")

    with viz_col2:
        st.write("**MCP Server enforced:**")
        st.write("• Path pattern match: payment/**")
        st.write("• Skill check: Novice ≠ Red access")
        st.write("• Blocked edit attempt")
        st.write("• Logged telemetry entry")

    with viz_col3:
        st.write("**Champion protected:**")
        st.write("• Payment logic protected")
        st.write("• I learn by reading, not breaking")
        st.write("• Sarah maintains authority")
        st.write("• Zero unauthorized changes")

    st.write("**Result:** I cannot accidentally break payment logic. The MCP server instantiates the protection framework at the moment I open the file.")

# TAB 2: Week 1 - Complete visibility of scaffolding
with tab2:
    st.header("Week 1: Green Zone Learning")
    st.markdown(zone_badge("GREEN ZONE", GREEN), unsafe_allow_html=True)

    st.write("**Assignment:** Write unit tests for Calculator.java. Safe to experiment with scaffolded support.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("MCP Scaffolding Configuration")
        st.code("""
// MCP Server Tool Call: get_scaffolding_level
// Developer: zubia_mughal
// File: tests/unit/CalculatorTest.java

{
  "level": "novice",
  "scaffolding": {
    "verbosity": "MAXIMUM",
    "explanation_style": "tutorial",
    "complexity_limit": 5,
    "examples_provided": true,
    "pattern_hints": true
  },
  "smart_goals": {
    "target_prs": 10,
    "complexity_threshold": 5,
    "current_progress": 3
  }
}
        """, language="json")

        st.write("**AI Behavior Adjusted:**")
        st.markdown(f"""
        <div style="background-color: {GREEN}20; padding: 10px; border-left: 4px solid {GREEN};">
        • Every line explained<br>
        • Complexity capped at 5<br>
        • Patterns matched to examples<br>
        • Tutorial-style comments
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("Generated Code with Scaffolding")
        st.code("""
// AI-GENERATED WITH NOVICE SCAFFOLDING
// File: tests/unit/CalculatorTest.java
// Zone: GREEN | Complexity: 2/5 [PASS]

/**
 * This is a JUnit test class.
 * JUnit is a testing framework for Java.
 * The @Test annotation marks methods as tests.
 */
public class CalculatorTest {

    /**
     * This test checks if addition works.
     * ARRANGE: Create the object we want to test
     * ACT: Call the method we want to verify
     * ASSERT: Check the result is what we expect
     */
    @Test
    public void testAddition() {
        // ARRANGE: Create calculator instance
        Calculator calc = new Calculator();

        // ACT: Call the add method with 2 and 3
        int result = calc.add(2, 3);

        // ASSERT: Verify 2+3 equals 5
        // If this fails, the test will show an error
        assertEquals(5, result);

        // Complexity check: 2 (under limit of 5) [SAFE]
    }

    // MCP VALIDATION: Pattern matches existing tests
    // MCP VALIDATION: Complexity 2 < threshold 5
    // STATUS: Approved for commit
}
        """, language="java")

    # Progress tracking
    st.divider()
    st.subheader("Framework Visibility: Progress Tracking")

    prog_col1, prog_col2, prog_col3 = st.columns(3)

    with prog_col1:
        st.write("**My SMART Goal Progress:**")
        st.metric("PRs Completed", "3 of 10")
        st.metric("Avg Complexity", "4.2", "Under 5.0 limit")
        st.metric("Reverts", "0", "Clean record")

    with prog_col2:
        st.write("**MCP Telemetry Logged:**")
        st.code("""
{
  "timestamp": "2026-03-07T14:23:00Z",
  "developer_id": "zubia_mughal",
  "metric_type": "complexity",
  "value": 4.2,
  "file_path": "tests/unit/CalculatorTest.java",
  "zone": "green"
}
        """, language="json")
        st.caption("Non-gameable git metrics")

    with prog_col3:
        st.write("**Scaffolding Effectiveness:**")
        st.write("• Complexity controlled: 4.2/5.0")
        st.write("• Learning via explanations")
        st.write("• Safe experimentation")
        st.write("• Zero production bugs")

    st.write("**Result:** I learn by doing in the Green Zone, with the AI adjusting to my Novice level (verbose explanations, complexity limits). The MCP server tracks my progress toward the Intermediate promotion criteria.")

# TAB 3: Week 4 - Complete visibility of promotion
with tab3:
    st.header("Week 4: Auto-Promotion to Intermediate")
    st.markdown(maturity_badge("M3", BLUE, "AGENTIC"), unsafe_allow_html=True)

    st.write("**Achievement:** I have completed 10 Green Zone PRs with average complexity 4.2 and zero reverts. The MCP server auto-promotes me.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Promotion Decision Engine")
        st.code("""
// MCP Server Auto-Promotion Check
// Developer: zubia_mughal
// Evaluation Date: 2026-03-28

PROMOTION_CRITERIA = {
  "novice_to_intermediate": {
    "min_prs": 10,
    "max_avg_complexity": 5.0,
    "max_revert_rate": 0.0,
    "mentor_signoff": true
  }
}

ACTUAL_METRICS = {
  "prs_completed": 10,
  "avg_complexity": 4.2,
  "revert_count": 0,
  "mentor_signoff": "sarah_chen"
}

EVALUATION:
PRs completed: 10 >= 10 [PASS]
Avg complexity: 4.2 <= 5.0 [PASS]
Revert rate: 0% <= 0% [PASS]
Mentor signoff: Approved [PASS]

RESULT: AUTO-PROMOTE to INTERMEDIATE
EFFECTIVE: Immediately
NOTIFY: Manager, Champion, Developer
        """, language="text")

        st.success("PROMOTION ACHIEVED")
        st.write("**New Status:** Intermediate")
        st.write("**Unlocked:** Yellow Zone access with validation")
        st.write("**Next Goal:** Complete 1 Yellow Zone validation")

    with col2:
        st.subheader("Evidence-Based Decision")

        evidence_df = pd.DataFrame({
            "Criterion": [
                "Green Zone PRs",
                "Average Complexity",
                "Revert Rate",
                "Code Review Feedback",
                "Mentor Sign-off"
            ],
            "Requirement": [
                "≥ 10",
                "< 5.0",
                "0%",
                "Positive",
                "Required"
            ],
            "Actual": [
                "10",
                "4.2",
                "0%",
                "Good patterns",
                "Sarah Chen"
            ],
            "Status": [
                "PASS",
                "PASS",
                "PASS",
                "PASS",
                "PASS"
            ]
        })

        st.dataframe(evidence_df, use_container_width=True, hide_index=True)

        st.write("**Key Point:** Promotion based on objective git metrics, not manager bias or tenure.")

    # Updated permissions
    st.divider()
    st.subheader("Framework Visibility: Updated Permissions")

    perm_col1, perm_col2 = st.columns(2)

    with perm_col1:
        st.write("**Previous (Novice):**")
        st.write("- Green: Full autonomy")
        st.write("- Yellow: Mentor required")
        st.write("- Red: Read only")
        st.write("- Scaffolding: Maximum")

    with perm_col2:
        st.write("**New (Intermediate):**")
        st.write("- Green: Full autonomy")
        st.write("- Yellow: Generate with validation [NEW]")
        st.write("- Red: Suggest only [NEW]")
        st.write("- Scaffolding: Moderate")

    st.write("**Result:** The MCP server automatically adjusted my permissions when I met the objective criteria. No paperwork, no politics—evidence-based progression.")

# TAB 4: Framework Mechanics - Complete instantiation details
with tab4:
    st.header("Framework Mechanics: Complete Instantiation")
    st.write("Technical visibility into how the three actors interact.")

    # Three columns showing the interaction
    mech_col1, mech_col2, mech_col3 = st.columns(3)

    with mech_col1:
        st.markdown(f"""
        <div style="background-color: {BLUE}20; padding: 15px; border-left: 4px solid {BLUE}; margin-bottom: 10px;">
            <h4 style="color: {BLUE}; margin-top: 0;">Zubia</h4>
            <p style="color: #666; font-size: 0.9em;">AI Training Consultant</p>
            <p><strong>Configures:</strong></p>
            <ul style="margin: 5px 0;">
                <li>zones/config.yml</li>
                <li>skill-matrix/profiles.yml</li>
                <li>smart_goals.yml</li>
                <li>.cursor/mcp.json</li>
            </ul>
            <p><strong>Delivers:</strong></p>
            <ul style="margin: 5px 0;">
                <li>8-week engagement</li>
                <li>Exit at M3</li>
                <li>Quarterly check-ins</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with mech_col2:
        st.markdown(f"""
        <div style="background-color: {GRAY}20; padding: 15px; border-left: 4px solid {GRAY}; margin-bottom: 10px;">
            <h4 style="color: {GRAY}; margin-top: 0;">MCP Server</h4>
            <p style="color: #666; font-size: 0.9em;">Technical Enforcer</p>
            <p><strong>Exposes Tools:</strong></p>
            <ul style="margin: 5px 0;">
                <li>check_edit_permission</li>
                <li>get_scaffolding_level</li>
                <li>get_zone_for_file</li>
                <li>log_entropy_metric</li>
            </ul>
            <p><strong>Enforces:</strong></p>
            <ul style="margin: 5px 0;">
                <li>Zone blocking</li>
                <li>Complexity caps</li>
                <li>Auto-promotion</li>
                <li>Telemetry logging</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with mech_col3:
        st.markdown(f"""
        <div style="background-color: {GOLD}20; padding: 15px; border-left: 4px solid {GOLD}; margin-bottom: 10px;">
            <h4 style="color: {GOLD}; margin-top: 0;">Champion</h4>
            <p style="color: #666; font-size: 0.9em;">Domain Expert</p>
            <p><strong>Owns:</strong></p>
            <ul style="margin: 5px 0;">
                <li>Red Zone decisions</li>
                <li>VTCO documentation</li>
                <li>Skill validation</li>
                <li>Mentoring</li>
            </ul>
            <p><strong>Protected By:</strong></p>
            <ul style="margin: 5px 0;">
                <li>MCP automation</li>
                <li>Time allocation</li>
                <li>Authority formalization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # The instantiation flow
    st.divider()
    st.subheader("Instantiation Timeline")

    timeline_data = pd.DataFrame({
        "Phase": ["Week 0-1", "Week 2-4", "Week 5-8", "Week 9-12"],
        "Zubia (Consultant)": [
            "Assessment + Workshop",
            "Configure MCP + Train",
            "Check-in (fading)",
            "EXIT (quarterly)"
        ],
        "MCP Server": [
            "Install + Load configs",
            "Enforce zones actively",
            "Auto-promotions",
            "Autonomous mode"
        ],
        "Champion": [
            "Define Red Zones + VTCO",
            "Mentor Novices",
            "Validate Yellow Zone",
            "Full authority"
        ],
        "Me (Novice)": [
            "Assessment",
            "Green Zone learning",
            "Promotion to Intermediate",
            "Yellow Zone work"
        ]
    })

    st.dataframe(timeline_data, use_container_width=True, hide_index=True)

    # Technical architecture
    st.divider()
    st.subheader("Technical Architecture")

    arch_col1, arch_col2 = st.columns(2)

    with arch_col1:
        st.write("**MCP Server Flow:**")
        st.code("""
Cursor IDE opens file
    ↓
MCP Tool Call: get_zone_for_file
    ↓
Check: zones/config.yml
    ↓
Match: src/payment/** = RED
    ↓
Check: skill-matrix/profiles.yml
    ↓
Developer: zubia_mughal = NOVICE
    ↓
Decision: RED + NOVICE = BLOCK
    ↓
Return: {
  "can_edit": false,
  "reason": "Requires Champion"
}
        """, language="text")

    with arch_col2:
        st.write("**Scaffolding Adjustment:**")
        st.code("""
Cursor requests code generation
    ↓
MCP Tool Call: get_scaffolding_level
    ↓
Check: zubia_mughal = NOVICE
    ↓
Config: {
  "verbosity": "maximum",
  "complexity_limit": 5
}
    ↓
AI adjusts: Tutorial mode ON
    ↓
Generated code includes:
- Line-by-line comments
- Complexity check
- Pattern explanations
        """, language="text")

    st.write("**Complete Visibility:** Every interaction is logged, every decision is traceable, every promotion is evidence-based.")

st.divider()
st.caption("Universal AI Governance Framework | Complete Instantiation Visibility")
