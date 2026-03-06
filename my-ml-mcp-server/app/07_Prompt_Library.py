"""Prompt Library - Curated prompts by zone."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mcp.server import load_prompts

st.title("📚 Prompt Library")
st.caption("Curated prompts ready to copy-paste into Cursor")

zone = st.radio("Zone", ["GREEN", "YELLOW", "RED"], horizontal=True)
prompts = load_prompts(zone)

st.subheader(f"{zone} prompts")
for p in prompts:
    with st.expander(p.get("name", "Untitled")):
        st.caption(f"Tags: {', '.join(p.get('tags', []))}")
        st.code(p.get("text", ""), language=None)  # Streamlit code blocks have built-in copy
