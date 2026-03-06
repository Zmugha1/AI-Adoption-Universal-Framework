"""Anti-Patterns - Common pitfalls and how to avoid."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from coaching_server.server import get_anti_pattern, list_anti_patterns

st.title("⚠️ Anti-Patterns")
st.caption("Common pitfalls and how to avoid")

patterns = list_anti_patterns() or ["data_leakage", "missing_random_state"]
pattern = st.selectbox("Anti-pattern", patterns)

data = get_anti_pattern(pattern)
if data:
    st.subheader(data.get("title", ""))
    st.error(f"**Impact:** {data.get('impact', '')}")
    st.write("**❌ Wrong:**")
    st.code(data.get("wrong_code", ""), language="python")
    st.write("**✅ Correct:**")
    st.code(data.get("correct_code", ""), language="python")
    st.write("**Detection:**")
    for m in data.get("detection_methods", []):
        st.write(f"- {m}")
    st.write("**Prevention:**")
    for m in data.get("prevention_checklist", []):
        st.write(f"- [ ] {m}")
