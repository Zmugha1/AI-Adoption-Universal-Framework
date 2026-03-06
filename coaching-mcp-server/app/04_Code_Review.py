"""Code Review - AI-powered production readiness check."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from coaching_server.server import validate_code

st.title("🔍 Code Review")
st.caption("Production readiness check")

code = st.text_area("Paste code to review", height=250, placeholder="# Your ML code here...")
if st.button("Review"):
    if code:
        result = validate_code(code)
        if result["valid"]:
            st.success("✅ No critical issues")
        else:
            st.error("Issues found:")
            for i in result["issues"]:
                st.write(f"- **{i['severity']}**: {i['message']}")
        if result.get("strengths"):
            st.info("**Strengths:** " + "; ".join(result["strengths"]))
    else:
        st.warning("Paste code first")
