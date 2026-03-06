"""MLflow Integration - Experiment tracking view."""
import streamlit as st

st.title("📈 MLflow Integration")
st.caption("Experiment tracking view")

st.write("""
**MLflow integration** (YELLOW zone requirement):
- Log params, metrics, artifacts
- Track experiments by name
- Compare runs
""")

st.info("""
To use MLflow:
1. Install: `pip install mlflow`
2. Start UI: `mlflow ui` (default http://localhost:5000)
3. In your training code:
   ```python
   import mlflow
   mlflow.set_experiment("my_project")
   with mlflow.start_run():
       mlflow.log_param("lr", 0.01)
       mlflow.log_metric("accuracy", 0.95)
       mlflow.log_artifact("model.pkl")
   ```
""")

st.subheader("Quick links")
st.markdown("- [MLflow UI](http://localhost:5000) (if running)")
st.markdown("- [MLflow docs](https://mlflow.org/docs/latest/index.html)")
