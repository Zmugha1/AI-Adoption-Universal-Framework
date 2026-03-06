"""Tradeoff Analysis - Decision frameworks with alternatives."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from coaching_server.server import get_explanation, list_explanations

st.title("⚖️ Tradeoff Analysis")
st.caption("Alternatives with pros/cons")

topic = st.selectbox("Topic", list_explanations() or ["random_state", "pipelines", "cross_validation", "experiment_tracking"])
data = get_explanation(topic) if topic else None

if data and data.get("alternatives"):
    st.subheader(f"Alternatives for: {data.get('title', topic)}")
    for alt in data["alternatives"]:
        with st.expander(alt.get("name", "")):
            st.write("**Pros:**", alt.get("pros", ""))
            st.write("**Cons:**", alt.get("cons", ""))
else:
    st.info("Select a topic to see alternatives and tradeoffs.")
