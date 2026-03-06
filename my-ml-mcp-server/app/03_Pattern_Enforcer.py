"""Pattern Enforcer - YELLOW zone pattern compliance."""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mcp.server import validate_code, load_prompts

st.title("🟡 Pattern Enforcer")
st.caption("YELLOW zone: templates, random_state, MLflow")

st.write("""
**YELLOW zone rules:**
- Must use templates
- `random_state=42` required
- MLflow tracking enabled
- Config externalized
""")

code = st.text_area("Paste your training/development code", height=200)
if st.button("Check Compliance"):
    if code:
        result = validate_code(code, "yellow")
        if result["valid"]:
            st.success("✅ Compliance passed")
        else:
            st.error("Violations:")
            for v in result["violations"]:
                st.write(f"- {v}")
            st.info("Suggestions: " + " | ".join(result["suggestions"]))
    else:
        st.warning("Paste code first")

st.divider()
st.subheader("Pattern template")
st.code("""
# patterns/train_template.py
RANDOM_STATE = 42

def train(config):
    model = YourModel(random_state=RANDOM_STATE, **config)
    model.fit(X_train, y_train)
    mlflow.log_params(config)
    mlflow.log_metrics({"accuracy": score})
    mlflow.log_artifact(model_path)
""", language="python")
