"""Learning Path - Personalized skill development."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from coaching_server.server import load_coaching_prompts

st.title("🎓 Learning Path")
st.caption("Coaching prompts for skill development")

data = load_coaching_prompts()
categories = data.get("categories", {})

cat = st.selectbox("Category", list(categories.keys()))
prompts = categories.get(cat, [])

st.subheader(f"{cat} prompts")
for p in prompts:
    with st.expander(p.get("name", "")):
        st.code(p.get("text", ""), language=None)
