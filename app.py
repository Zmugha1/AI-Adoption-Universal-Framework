"""
Universal AI Governance Framework
Run with: streamlit run app.py
"""
import streamlit as st
import runpy
from pathlib import Path

from shared import render_sidebar

st.set_page_config(
    page_title="Universal AI Governance Framework",
    page_icon="●",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar: Navigation, Demo, App (read nav from query params for deep links)
nav_param = st.query_params.get("nav", "1")
nav_index = max(0, min(2, int(nav_param) - 1)) if nav_param.isdigit() else 0
page = render_sidebar(use_nav_radio=True, nav_index=nav_index)

# Load the selected page
nav_dir = Path(__file__).parent / "nav_pages"
if page == "1. Framework & Architecture":
    runpy.run_path(str(nav_dir / "framework_architecture.py"), run_name="__main__")
elif page == "2. Baseline Assessment (M2)":
    runpy.run_path(str(nav_dir / "baseline_assessment.py"), run_name="__main__")
else:
    runpy.run_path(str(nav_dir / "scaling_ready.py"), run_name="__main__")
