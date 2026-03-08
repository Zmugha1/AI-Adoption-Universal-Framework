"""Risk matrix component for Streamlit dashboard."""
import streamlit as st
import json
from pathlib import Path

GOV_PATH = Path(__file__).resolve().parent.parent.parent / "governance" / "risk_matrix.json"


def render_risk_matrix() -> None:
    """Render risk matrix from governance config."""
    if not GOV_PATH.exists():
        st.warning("Risk matrix not found")
        return
    with open(GOV_PATH, encoding="utf-8") as f:
        data = json.load(f)
    for level, config in data.get("risk_levels", {}).items():
        with st.expander(f"{level} - {config.get('name', '')}"):
            st.write("**Requirements:**", config.get("requirements", []))
            st.write("**Characteristics:**", config.get("characteristics", []))
