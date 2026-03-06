"""Production Guard - RED zone production rules."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mcp.server import validate_code

st.title("🔴 Production Guard")
st.caption("RED zone: deterministic, audit trail, advisory only")

st.write("""
**RED zone rules:**
- Deterministic only
- Input validation mandatory
- Full audit trail
- Cursor: advisory only
""")

code = st.text_area("Paste production/inference code", height=200)
if st.button("Validate"):
    if code:
        result = validate_code(code, "red")
        if result["valid"]:
            st.success("✅ Production-ready")
        else:
            st.error("Violations:")
            for v in result["violations"]:
                st.write(f"- {v}")
            st.info("Suggestions: " + " | ".join(result["suggestions"]))
    else:
        st.warning("Paste code first")

st.divider()
st.subheader("Production checklist")
st.checkbox("Input validation (Pydantic/schema)")
st.checkbox("No randomness in inference path")
st.checkbox("Logging: request id, latency, model version")
st.checkbox("Error handling with safe fallbacks")
st.checkbox("Model card documented")
