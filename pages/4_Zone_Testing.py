"""Zone Testing & Novice Simulator - Interactive testing laboratory for AI governance."""
import sys
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from shared import render_sidebar, ZONE_COLORS

st.set_page_config(page_title="Zone Testing & Novice Simulator", page_icon="●")
render_sidebar(use_nav_radio=False)

st.title("Zone Testing & Novice Simulator")
st.subheader("Validate governance rules and experience the Novice journey")
st.markdown("""
Test how the MCP server responds to different file paths, user roles, and complexity levels.
This simulator demonstrates the Three-Actors governance in action.
""")
st.divider()


def _zone_from_path(file_path: str) -> str:
    """Zone detection - matches zoning_enforcer priority: Green > Red > Yellow."""
    path = file_path.replace("\\", "/")

    # 1. GREEN FIRST (explicitly safe)
    if re.search(r"^tests?/|^docs?/|^src/utils/|\.md$|fixtures/|mocks/", path, re.IGNORECASE):
        return "Green"

    # 2. RED (dangerous)
    if re.search(r"migrations?/|schema/|config/production|src/payment/|src/security/|ddl/", path, re.IGNORECASE):
        # Double-check: tests override Red
        if re.search(r"^tests?/", path, re.IGNORECASE):
            return "Green"
        return "Red"

    # 3. YELLOW (medium risk)
    if re.search(r"src/api/|src/services/|src/integration/|lib/", path, re.IGNORECASE):
        return "Yellow"

    return "Yellow"  # Default safe


def detect_zone(file_path: str, complexity: int, role: str) -> dict:
    """
    Simulate MCP zoning logic.
    Returns: zone, zone_color, allowed, scaffolding, required_approver, message
    """
    zone = _zone_from_path(file_path)
    zone_color = ZONE_COLORS[zone]

    allowed = True
    required_approver = None
    scaffolding = "Minimal"
    message = ""

    if zone == "Red":
        if role != "Champion":
            allowed = False
            required_approver = "Senior_Architect_01"
            message = f"BLOCKED: Red Zone requires Champion role. Current role: {role}."
            if role == "Novice":
                message += " Novice users cannot edit production infrastructure."
                scaffolding = "Maximum (Educational)"
        else:
            scaffolding = "Consultative"
            message = "APPROVED: Champion authority recognized."

    elif zone == "Yellow":
        if role == "Novice" and complexity > 5:
            allowed = False
            required_approver = "Mentor_Assigned"
            message = f"BLOCKED: Complexity {complexity} exceeds Novice limit (5). Mentor review required."
            scaffolding = "Maximum"
        elif role == "Novice":
            allowed = True
            message = "APPROVED WITH MENTOR: Yellow Zone requires validation checkpoint."
            scaffolding = "Moderate"
        else:
            message = "APPROVED: Yellow Zone with pattern validation."
            scaffolding = "Moderate"

    else:
        if role == "Novice" and complexity > 5:
            allowed = False
            message = f"BLOCKED: Complexity {complexity} exceeds role limit (5). Simplify or escalate."
            scaffolding = "Maximum"
        else:
            message = "AUTO-APPROVED: Green Zone operation."
            if role == "Novice":
                scaffolding = "Maximum (Explain every line)"
            elif role == "Intermediate":
                scaffolding = "Moderate"
            else:
                scaffolding = "Minimal"

    return {
        "zone": zone,
        "zone_color": zone_color,
        "allowed": allowed,
        "scaffolding": scaffolding,
        "required_approver": required_approver,
        "message": message,
    }


# Initialize session state for scenario results
if "scenario_result" not in st.session_state:
    st.session_state.scenario_result = None
if "last_test_result" not in st.session_state:
    st.session_state.last_test_result = None
if "last_test_path" not in st.session_state:
    st.session_state.last_test_path = ""

# Test Configuration Panel
st.header("Test Configuration", divider=True)
config_col1, config_col2, config_col3 = st.columns(3)

with config_col1:
    test_role = st.selectbox(
        "Test User Role",
        ["Novice", "Intermediate", "Expert", "Champion"],
        index=0,
        help="Novice: 0-2 years, max complexity 5. Champion: Full governance authority.",
    )

with config_col2:
    test_file_path = st.text_input(
        "File Path to Test",
        value="tests/test_utils.py",
        help="Examples: tests/test_utils.py (Green), migrations/schema.sql (Red), src/api/client.py (Yellow)",
    )

with config_col3:
    test_complexity = st.slider(
        "Code Complexity Score",
        1,
        20,
        3,
        help="Cyclomatic complexity: 1-5 (Green), 6-10 (Yellow), 11-20 (Red/Expert)",
    )

# Main Testing Interface
st.header("Live Zone Detection", divider=True)

if st.button("Test This Configuration", type="primary"):
    st.session_state.scenario_result = None
    result = detect_zone(test_file_path, test_complexity, test_role)
    st.session_state.last_test_result = result
    st.session_state.last_test_path = test_file_path

result = st.session_state.last_test_result
display_path = st.session_state.last_test_path or test_file_path
if result is not None:
    zone_col1, zone_col2 = st.columns([1, 2])
    with zone_col1:
        st.markdown(
            f"""
        <div style='background-color: {result['zone_color']}20;
                    border-left: 5px solid {result['zone_color']};
                    padding: 20px;
                    border-radius: 5px;'>
            <h2 style='color: {result['zone_color']}; margin: 0;'>
                {result['zone']} ZONE
            </h2>
            <p style='margin: 10px 0 0 0; font-size: 0.9em;'>
                File: <code>{display_path}</code>
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with zone_col2:
        if result["allowed"]:
            st.success(result["message"])
        else:
            st.error(result["message"])
        st.metric("Scaffolding Level", result["scaffolding"])
        if result["required_approver"]:
            st.warning(f"Escalation required: {result['required_approver']}")

    st.subheader("MCP Server Decision Log")
    role_limits = {"Novice": 5, "Intermediate": 10, "Expert": 15, "Champion": 20}
    log_entries = [
        f"10:00:00 - Zone detection: File path '{display_path}' -> {result['zone']}",
        f"10:00:01 - Role check: {test_role} (Complexity limit: {role_limits.get(test_role, 20)})",
        f"10:00:01 - Permission check: {'ALLOWED' if result['allowed'] else 'BLOCKED'}",
    ]
    if not result["allowed"]:
        log_entries.append("10:00:02 - Violation logged: .ai-governance/violations.jsonl")
        log_entries.append(f"10:00:02 - ADR created: ADR-{datetime.now().strftime('%Y-%m')}-001")
        if result["zone"] == "Red":
            log_entries.append("10:00:03 - Champion notified: Senior_Architect_01")
    for entry in log_entries:
        st.code(entry, language="log")

# Quick Test Scenarios
st.header("Quick Test Scenarios", divider=True)
scenario_cols = st.columns(3)

test_scenarios = {
    "Green Zone Success": {
        "role": "Novice",
        "path": "src/utils/string_helpers.py",
        "complexity": 2,
        "description": "Simple utility function within Novice limits",
    },
    "Yellow Zone Block": {
        "role": "Novice",
        "path": "src/api/payment_client.py",
        "complexity": 8,
        "description": "Novice attempting complex integration logic",
    },
    "Red Zone Block": {
        "role": "Intermediate",
        "path": "migrations/2026_03_01_alter_users.sql",
        "complexity": 3,
        "description": "Non-Champion attempting database schema change",
    },
}

with scenario_cols[0]:
    st.markdown("**Green Zone Test**")
    st.caption("Novice + simple utility")
    if st.button("Run Green Test", key="green"):
        r = detect_zone("src/utils/string_helpers.py", 2, "Novice")
        st.session_state.last_test_result = r
        st.session_state.last_test_path = "src/utils/string_helpers.py"
        st.session_state.scenario_result = "green"
        st.rerun()
    if st.session_state.scenario_result == "green" and st.session_state.last_test_result:
        r = st.session_state.last_test_result
        st.success("Approved - Max scaffolding enabled")
        st.caption(f"Zone: {r['zone']} | Scaffolding: {r['scaffolding']}")

with scenario_cols[1]:
    st.markdown("**Yellow Zone Test**")
    st.caption("Novice + complex API")
    if st.button("Run Yellow Test", key="yellow"):
        r = detect_zone("src/api/client.py", 8, "Novice")
        st.session_state.last_test_result = r
        st.session_state.last_test_path = "src/api/client.py"
        st.session_state.scenario_result = "yellow"
        st.rerun()
    if st.session_state.scenario_result == "yellow" and st.session_state.last_test_result:
        r = st.session_state.last_test_result
        st.error("Blocked - Complexity 8 > Novice limit 5")
        st.info("Mentor auto-assigned for review")

with scenario_cols[2]:
    st.markdown("**Red Zone Test**")
    st.caption("Intermediate + database")
    if st.button("Run Red Test", key="red"):
        r = detect_zone("migrations/schema.sql", 3, "Intermediate")
        st.session_state.last_test_result = r
        st.session_state.last_test_path = "migrations/schema.sql"
        st.session_state.scenario_result = "red"
        st.rerun()
    if st.session_state.scenario_result == "red" and st.session_state.last_test_result:
        r = st.session_state.last_test_result
        st.error("BLOCKED - Red Zone requires Champion")
        st.warning("ADR created, Senior_Architect_01 notified")
        st.code(
            """
VTCO Context Surfaced:
- Domain: production_database
- Constraint: No destructive migrations without rollback
- Champion: Senior_Architect_01
""",
            language="yaml",
        )

# Novice Journey Simulator
st.header("Novice Journey Simulation", divider=True)
st.markdown("See how a Novice progresses through the system over 8 weeks")

week = st.slider("Week", 1, 8, 1)

journey_data = {
    1: {"status": "New Hire", "complexity_limit": 5, "green_prs": 0, "yellow_attempts": 0, "zone": "Green Only"},
    2: {"status": "Learning", "complexity_limit": 5, "green_prs": 3, "yellow_attempts": 1, "zone": "Green Only"},
    3: {"status": "Building Confidence", "complexity_limit": 5, "green_prs": 7, "yellow_attempts": 2, "zone": "Green + Supervised Yellow"},
    4: {"status": "First Promotion", "complexity_limit": 7, "green_prs": 12, "yellow_attempts": 3, "zone": "Green + Yellow (Mentor)"},
    5: {"status": "Intermediate", "complexity_limit": 10, "green_prs": 18, "yellow_attempts": 5, "zone": "Green + Yellow"},
    6: {"status": "Expanding Scope", "complexity_limit": 10, "green_prs": 25, "yellow_attempts": 8, "zone": "Green + Yellow"},
    7: {"status": "Expert Track", "complexity_limit": 12, "green_prs": 35, "yellow_attempts": 12, "zone": "Green + Yellow + Red Drafts"},
    8: {"status": "Promotion Ready", "complexity_limit": 15, "green_prs": 45, "yellow_attempts": 15, "zone": "Expert Level"},
}

current = journey_data[week]

prog_col1, prog_col2, prog_col3 = st.columns(3)
with prog_col1:
    st.metric("Status", current["status"])
    st.metric("Complexity Limit", current["complexity_limit"])
with prog_col2:
    st.metric("Green PRs Completed", current["green_prs"])
    st.metric("Yellow Attempts", current["yellow_attempts"])
with prog_col3:
    st.metric("Current Permissions", current["zone"])

st.progress(week / 8)
st.caption(f"Week {week} of 8 - Entitlement: {current['complexity_limit']} complexity cap")

if week == 4:
    st.success("MCP Auto-Promotion: Complexity limit raised to 7 after 10 successful Green PRs")
elif week == 5:
    st.success("Role Promotion: Intermediate status achieved. Yellow Zone access granted.")
elif week == 8:
    st.balloons()
    st.success("Expert Track: Can draft Red Zone proposals (Champion approval still required)")

# VTCO Context Viewer
st.header("Tribal Knowledge Context", divider=True)

vtco_path = display_path if st.session_state.last_test_result else test_file_path
if "migrations" in vtco_path or "schema" in vtco_path:
    st.info("VTCO Document Auto-Loaded: production_database")
    st.code(
        """
domain: "production_database"
champion_owner: "Senior_Architect_01"

constraints:
  - "No destructive migrations (DROP) without verified rollback"
  - "All new columns NULLABLE initially"
  - "Max execution time: 30 seconds"
  - "Use pt-online-schema-change for tables > 1GB"

ai_behavior:
  allowed: ["Explain locking risks", "Suggest strategies"]
  forbidden: ["Generate ALTER TABLE", "Approve schema changes"]
  reminder: "This is RED ZONE - requires Senior_Architect_01 approval"

escalation_path:
  if_blocked: "File ADR and contact Senior_Architect_01"
""",
        language="yaml",
    )
else:
    st.info("No specific VTCO for this path. General Green Zone policies apply.")

# Educational Sidebar
with st.sidebar:
    st.divider()
    st.header("Testing Guide")
    st.markdown("""
    **Zone Patterns (priority: Green > Red > Yellow):**
    - **Green**: `tests/`, `docs/`, `src/utils/`, `*.md`, `fixtures/`, `mocks/`
    - **Red**: `migrations/`, `schema/`, `config/production`, `src/payment/`, `src/security/`, `ddl/`
    - **Yellow**: `src/api/`, `src/services/`, `src/integration/`, `lib/`

    **Role Limits:**
    - Novice: Complexity <= 5
    - Intermediate: Complexity <= 10
    - Expert: Complexity <= 15
    - Champion: No limit + Red Zone

    **Scaffolding Levels:**
    - Maximum: Explain every line, simple patterns only
    - Moderate: Key decisions explained
    - Minimal: Architecture focus only
    - Consultative: Strategic oversight
    """)
