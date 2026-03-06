"""
Coaching MCP Server - Streamlit Dashboard
Run with: streamlit run app/main.py
"""
import runpy
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="ML Engineering Coach",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

PAGES = {
    "1. Why Explainer": "01_Why_Explainer",
    "2. Diagnostic Lab": "02_Diagnostic_Lab",
    "3. Standards Ref": "03_Standards_Ref",
    "4. Code Review": "04_Code_Review",
    "5. Tradeoff Analysis": "05_Tradeoff_Analysis",
    "6. Anti-Patterns": "06_Anti_Patterns",
    "7. Production Check": "07_Production_Check",
    "8. Learning Path": "08_Learning_Path",
}

page = st.sidebar.radio("Navigate", list(PAGES.keys()))
module = PAGES[page]
app_dir = Path(__file__).parent
page_path = app_dir / f"{module}.py"

if page_path.exists():
    runpy.run_path(str(page_path), run_name="__main__")
else:
    st.error(f"Page not found: {page_path}")
