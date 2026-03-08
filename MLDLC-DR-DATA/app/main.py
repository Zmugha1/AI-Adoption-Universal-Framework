"""
MLDLC DR Data - Streamlit Dashboard
Run with: streamlit run app/main.py
"""
import streamlit as st

st.set_page_config(
    page_title="MLDLC DR Data Decision Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
st.sidebar.title("MLDLC Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Documentation"],
    index=0,
)

if page == "Documentation":
    st.switch_page("pages/6_Documentation.py")

st.title("MLDLC DR Data Decision Intelligence")
st.caption("VTCO | Risk Matrix | Schema Validation | Lineage | Audit")

st.markdown("""
## Quick Links

- **VTCO**: Define Verb-Task-Constraint-Outcome for every task
- **Risk Matrix**: RED / YELLOW / GREEN classification
- **Schemas**: Validate datasets, models, experiments, deployments
- **Lineage**: Track data transformations
- **Audit**: Full audit trail in `data/audit/`

## MCP Tools (Cursor)

When this project is open in Cursor with the MCP server configured:

- `define_vtco` - Define VTCO task
- `assess_risk` - Assess risk level
- `validate_artifact` - Validate against schema
- `record_lineage` - Record transformation
- `get_lineage` - Query lineage
- `log_audit_event` - Log audit event

## Documentation

Click **Documentation** in the sidebar for the complete MLDLC guide (VTCO, Risk Matrix, Schemas, Lineage, Audit, MCP Tools, Cursor Integration, FAQ).
""")
