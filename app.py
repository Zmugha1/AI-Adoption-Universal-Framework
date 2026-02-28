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

# Sidebar Navigation (at top of sidebar)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "1. Framework & Architecture",
    "2. Baseline Assessment (M2)",
    "3. Scaling Ready (M3)"
])

# Load the selected page
nav_dir = Path(__file__).parent / "nav_pages"
if page == "1. Framework & Architecture":
    runpy.run_path(str(nav_dir / "framework_architecture.py"), run_name="__main__")
elif page == "2. Baseline Assessment (M2)":
    runpy.run_path(str(nav_dir / "baseline_assessment.py"), run_name="__main__")
else:
    runpy.run_path(str(nav_dir / "scaling_ready.py"), run_name="__main__")
