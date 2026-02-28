"""
Universal AI Governance Framework
Run with: streamlit run app.py
"""
import streamlit as st
import runpy
from pathlib import Path

st.set_page_config(
    page_title="Universal AI Governance Framework",
    page_icon="●",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Section 1: Navigation (top)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "1. Framework & Architecture",
    "2. Baseline Assessment (M2)",
    "3. Scaling Ready (M3)"
])

# Section 2: Demo
st.sidebar.divider()
st.sidebar.subheader("Demo")
st.sidebar.page_link("pages/1_Framework_Details.py", label="Framework Details", icon=":material/architecture:")
st.sidebar.page_link("pages/2_Consultant_Workflow.py", label="Consultant Workflow", icon=":material/work:")
st.sidebar.page_link("pages/3_Developer_Experience.py", label="Developer Experience", icon=":material/code:")

# Section 3: App (last)
st.sidebar.divider()
st.sidebar.subheader("App")
st.sidebar.page_link("app.py", label="Home", icon=":material/home:")

# Load the selected page
nav_dir = Path(__file__).parent / "nav_pages"
if page == "1. Framework & Architecture":
    runpy.run_path(str(nav_dir / "framework_architecture.py"), run_name="__main__")
elif page == "2. Baseline Assessment (M2)":
    runpy.run_path(str(nav_dir / "baseline_assessment.py"), run_name="__main__")
else:
    runpy.run_path(str(nav_dir / "scaling_ready.py"), run_name="__main__")
