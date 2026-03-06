"""Why Explainer - Understand WHY patterns exist."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from coaching_server.server import get_explanation, list_explanations

st.title("📚 Why Explainer")
st.caption("Understand WHY patterns exist")

topic = st.selectbox("Topic", list_explanations() or ["random_state", "pipelines", "cross_validation", "experiment_tracking"])
if st.button("Explain"):
    try:
        import requests
        r = requests.post("http://localhost:8001/explain", json={
            "topic": topic,
            "depth": "detailed",
            "include_code_examples": True,
            "include_references": True
        })
        if r.ok:
            d = r.json()
            st.success(f"🎯 **{d.get('title', '')}**")
            st.write("**Why it matters:**")
            st.write(d.get("why_it_matters", ""))
            st.write("**Detailed explanation:**")
            st.write(d.get("detailed_explanation", ""))
            if d.get("common_misconceptions"):
                st.write("**⚠️ Common misconceptions:**")
                for m in d["common_misconceptions"]:
                    st.write(f"- {m}")
            if d.get("wrong_code"):
                st.write("**❌ Wrong:**")
                st.code(d["wrong_code"], language="python")
            if d.get("correct_code"):
                st.write("**✅ Correct:**")
                st.code(d["correct_code"], language="python")
            if d.get("references"):
                st.write("**📚 References:**")
                for ref in d["references"]:
                    st.write(f"- {ref.get('source', '')} (credibility: {'⭐' * ref.get('credibility', 0)})")
        else:
            st.warning("MCP server not running. Start: uvicorn coaching_server.server:app --port 8001")
    except Exception as e:
        # Fallback: load locally
        data = get_explanation(topic)
        if data:
            st.success(f"🎯 **{data.get('title', '')}**")
            st.write("**Why it matters:**", data.get("why_it_matters", ""))
            st.write("**Detailed:**", data.get("detailed_explanation", ""))
            if data.get("wrong_code"):
                st.code(data["wrong_code"], language="python")
            if data.get("correct_code"):
                st.code(data["correct_code"], language="python")
        else:
            st.error(f"Topic not found: {topic}")
