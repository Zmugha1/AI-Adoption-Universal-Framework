"""Experiment Tracker - GREEN zone experiment management."""
import streamlit as st
import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
EXPERIMENTS_DIR = APP_DIR / "experiments"

st.title("🟢 Experiment Tracker")
st.caption("GREEN zone experiment management")

# List experiments
if EXPERIMENTS_DIR.exists():
    experiments = [d.name for d in EXPERIMENTS_DIR.iterdir() if d.is_dir()]
else:
    experiments = []
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)

st.subheader("Your Experiments")
if experiments:
    for exp in experiments:
        manifest_path = EXPERIMENTS_DIR / exp / "manifest.json"
        if manifest_path.exists():
            data = json.loads(manifest_path.read_text())
            st.write(f"- **{data.get('name', exp)}** — {data.get('description', '')}")
        else:
            st.write(f"- {exp}")
else:
    st.info("No experiments yet. Create one below.")

st.subheader("Create New Experiment")
with st.form("create_experiment"):
    name = st.text_input("Experiment name")
    desc = st.text_area("Description", placeholder="What are you exploring?")
    if st.form_submit_button("Create"):
        if name:
            try:
                import requests
                r = requests.post("http://localhost:8000/init-experiment", json={"name": name, "description": desc})
                if r.ok:
                    st.success(f"Created: {r.json().get('path', '')}")
                    st.rerun()
                else:
                    raise ConnectionError("Server error")
            except Exception:
                # Fallback: create locally without MCP server
                import json
                from datetime import datetime
                exp_dir = EXPERIMENTS_DIR / name.replace(" ", "_").lower()
                exp_dir.mkdir(parents=True, exist_ok=True)
                manifest = {"name": name, "description": desc, "zone": "green", "created": datetime.now().isoformat()}
                (exp_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
                nb = {"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4}
                (exp_dir / "notebook.ipynb").write_text(json.dumps(nb))
                st.success(f"Created: {exp_dir}")
                st.rerun()
        else:
            st.warning("Enter a name")
