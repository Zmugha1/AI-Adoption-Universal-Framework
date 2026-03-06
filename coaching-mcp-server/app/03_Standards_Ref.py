"""Standards Ref - Industry standards and best practices."""
import streamlit as st

st.title("📋 Standards Ref")
st.caption("Industry standards and best practices")

st.write("""
**ML Production Readiness Checklist:**
- [ ] Reproducibility: random_state everywhere
- [ ] No data leakage: Pipeline for preprocessing
- [ ] Experiment tracking: MLflow or equivalent
- [ ] Cross-validation: Report mean ± std
- [ ] Input validation: Pydantic/schema for serving
- [ ] Model versioning: Artifacts stored with run
- [ ] Monitoring: Latency, error rate, drift

**References:**
- [Google ML Rules](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [Scikit-learn Best Practices](https://scikit-learn.org/stable/developers/contributing.html)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
""")
