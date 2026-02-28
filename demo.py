"""
Universal AI Governance Framework - Demo Entry Point
Navigation at top, Demo pages below. Main app renamed to "Demo".
"""
import streamlit as st

st.set_page_config(
    page_title="Universal AI Governance Framework",
    page_icon="●",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Navigation section first (top), Demo section below
framework_pg = st.Page(
    "nav_pages/framework_architecture.py",
    title="Framework & Architecture",
    default=True
)
baseline_pg = st.Page(
    "nav_pages/baseline_assessment.py",
    title="Baseline Assessment (M2)"
)
scaling_pg = st.Page(
    "nav_pages/scaling_ready.py",
    title="Scaling Ready (M3)"
)

framework_details_pg = st.Page(
    "pages/1_Framework_Details.py",
    title="Framework Details"
)
consultant_pg = st.Page(
    "pages/2_Consultant_Workflow.py",
    title="Consultant Workflow"
)
developer_pg = st.Page(
    "pages/3_Developer_Experience.py",
    title="Developer Experience"
)

pg = st.navigation({
    "Navigation": [framework_pg, baseline_pg, scaling_pg],
    "Demo": [framework_details_pg, consultant_pg, developer_pg]
})
pg.run()
