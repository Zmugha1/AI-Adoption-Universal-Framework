"""Knowledge Graph - Personal ML knowledge exploration."""
import streamlit as st
import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
KG_PATH = APP_DIR / "knowledge_graph" / "experiments.json"

st.title("📊 Knowledge Graph")
st.caption("Personal ML knowledge and experiment history")

if KG_PATH.exists():
    data = json.loads(KG_PATH.read_text())
    if data:
        st.subheader("Past experiments")
        for item in data:
            if isinstance(item, dict):
                st.json(item)
            else:
                st.write(item)
    else:
        st.info("No experiments recorded yet. Run experiments and they'll appear here.")
else:
    st.info("Knowledge graph is empty. Add experiments to build your ML history.")

st.divider()
st.subheader("Query (when MCP server is running)")
query = st.text_input("Search experiments", placeholder="e.g. iris, accuracy")
if query:
    try:
        import requests
        r = requests.post("http://localhost:8000/query-knowledge-graph", json={"query": query})
        if r.ok:
            results = r.json().get("results", [])
            for r in results:
                st.write(r)
        else:
            st.warning("MCP server not running on port 8000")
    except Exception as e:
        st.warning(f"Could not query: {e}")
