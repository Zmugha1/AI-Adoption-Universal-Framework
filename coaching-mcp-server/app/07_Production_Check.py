"""Production Check - Pre-deployment validation."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from coaching_server.server import validate_code

st.title("🚀 Production Check")
st.caption("Pre-deployment validation")

code = st.text_area("Paste your ML code before deployment", height=300)
if st.button("Check"):
    if code:
        result = validate_code(code)
        if result["valid"]:
            st.success("✅ Passes production readiness checks")
        else:
            critical = [i for i in result["issues"] if i["severity"] in ("CRITICAL", "HIGH")]
            if critical:
                st.error("**Block deployment:**")
                for i in critical:
                    st.write(f"- {i['message']}")
            for i in result["issues"]:
                if i["severity"] == "WARNING":
                    st.warning(i["message"])
        if result.get("strengths"):
            st.success("**Strengths:** " + "; ".join(result["strengths"]))
    else:
        st.warning("Paste code first")
