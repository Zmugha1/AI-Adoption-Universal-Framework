"""Shared constants and config for the framework demo."""
import streamlit as st


def render_sidebar(use_nav_radio=True, nav_index=0):
    """Render the unified sidebar (Navigation, Demo, App) on every page.
    use_nav_radio: True on app.py (radio for nav selection), False on pages (links instead).
    nav_index: When use_nav_radio, which option to select by default (0, 1, or 2).
    """
    NAV_OPTIONS = [
        "1. Framework & Architecture",
        "2. Baseline Assessment (M2)",
        "3. Scaling Ready (M3)",
        "4. Implementation Playbook"
    ]
    # Section 1: Navigation
    st.sidebar.title("Navigation")
    if use_nav_radio:
        nav = st.sidebar.radio("Go to", NAV_OPTIONS, index=min(nav_index, 3))
    else:
        nav = None
        st.sidebar.page_link("app.py", label="1. Framework & Architecture", query_params={"nav": "1"})
        st.sidebar.page_link("app.py", label="2. Baseline Assessment (M2)", query_params={"nav": "2"})
        st.sidebar.page_link("app.py", label="3. Scaling Ready (M3)", query_params={"nav": "3"})
        st.sidebar.page_link("app.py", label="4. Implementation Playbook", query_params={"nav": "4"})

    # Section 2: Demo
    st.sidebar.divider()
    st.sidebar.subheader("Demo")
    st.sidebar.page_link("pages/1_Framework_Details.py", label="Framework Details", icon=":material/architecture:")
    st.sidebar.page_link("pages/2_Consultant_Workflow.py", label="Consultant Workflow", icon=":material/work:")
    st.sidebar.page_link("pages/3_Developer_Experience.py", label="Developer Experience", icon=":material/code:")
    st.sidebar.page_link("pages/4_Zone_Testing.py", label="Zone Testing & Novice Simulator", icon=":material/science:")
    st.sidebar.page_link("pages/5_Implementation_Playbook.py", label="8-Week Implementation Playbook", icon=":material/assignment:")

    # Section 3: App
    st.sidebar.divider()
    st.sidebar.subheader("App")
    st.sidebar.page_link("app.py", label="Home", icon=":material/home:")

    return nav


MATURITY_COLORS = {
    "M1": "#808080",
    "M2": "#FF8C00",
    "M3": "#0066CC",
    "M4": "#D4AF37"
}
ZONE_COLORS = {
    "Red": "#DC143C",
    "Yellow": "#FFD700",
    "Green": "#228B22"
}
ROLE_COLORS = {
    "Consultant": "#4169E1",
    "MCP": "#708090",
    "Champion": "#DAA520"
}
