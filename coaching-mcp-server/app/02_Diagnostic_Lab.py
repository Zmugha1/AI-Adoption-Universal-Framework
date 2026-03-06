"""Diagnostic Lab - Systematic debugging workflows."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from coaching_server.server import get_diagnostic, list_diagnostics

st.title("🔬 Diagnostic Lab")
st.caption("Systematic debugging workflows")

symptoms = list_diagnostics() or ["model_underperforming", "overfitting"]
symptom = st.selectbox("Symptom", symptoms)

if st.button("Get diagnostic"):
    data = get_diagnostic(symptom)
    if data:
        st.subheader(data.get("title", ""))
        st.write("**Possible causes:**")
        for c in data.get("possible_causes", []):
            st.write(f"- {c.get('cause', '')} ({c.get('probability', 0)*100:.0f}%): {c.get('description', '')}")
        st.write("**Diagnostic workflow:**")
        for step in data.get("diagnostic_workflow", []):
            with st.expander(f"Step {step.get('step')}: {step.get('name', '')}"):
                for a in step.get("actions", []):
                    st.write(f"- {a}")
                st.caption(f"Tools: {step.get('tools', [])} | Time: {step.get('time_estimate', '')}")
        st.info(f"**When to escalate:** {data.get('when_to_escalate', '')}")
    else:
        st.error("Symptom not found")
