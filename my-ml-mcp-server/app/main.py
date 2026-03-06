"""
Personal ML MCP Server - Streamlit Dashboard
Run with: streamlit run app/main.py
"""
import runpy
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Personal ML Governance",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
PAGES = {
    "1. Zone Dashboard": "01_Zone_Dashboard",
    "2. Experiment Tracker": "02_Experiment_Tracker",
    "3. Pattern Enforcer": "03_Pattern_Enforcer",
    "4. Production Guard": "04_Production_Guard",
    "5. Knowledge Graph": "05_Knowledge_Graph",
    "6. MLflow Integration": "06_MLflow_Integration",
    "7. Prompt Library": "07_Prompt_Library",
}

page = st.sidebar.radio("Navigate", list(PAGES.keys()))
module = PAGES[page]
app_dir = Path(__file__).parent
page_path = app_dir / f"{module}.py"

if page_path.exists():
    runpy.run_path(str(page_path), run_name="__main__")
else:
    st.error(f"Page not found: {page_path}")
