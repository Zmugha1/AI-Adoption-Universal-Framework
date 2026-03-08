"""
MLDLC Documentation Page
Comprehensive guide for using the MLDLC framework
"""
import json
import streamlit as st
from pathlib import Path

# Project root (MLDLC-DR-DATA)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

st.set_page_config(
    page_title="MLDLC Documentation",
    page_icon="📖",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .doc-header { font-size: 2.5rem; font-weight: bold; color: #1f77b4; margin-bottom: 1rem; }
    .doc-section { font-size: 1.5rem; font-weight: bold; color: #2c3e50; margin-top: 2rem; margin-bottom: 1rem; border-bottom: 2px solid #3498db; padding-bottom: 0.5rem; }
    .doc-subsection { font-size: 1.2rem; font-weight: bold; color: #34495e; margin-top: 1.5rem; margin-bottom: 0.5rem; }
    .info-box { background-color: #e8f4f8; border-left: 4px solid #3498db; padding: 1rem; margin: 1rem 0; border-radius: 0 4px 4px 0; }
    .warning-box { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 1rem; margin: 1rem 0; border-radius: 0 4px 4px 0; }
    .success-box { background-color: #d4edda; border-left: 4px solid #28a745; padding: 1rem; margin: 1rem 0; border-radius: 0 4px 4px 0; }
    .step-number { display: inline-block; width: 30px; height: 30px; background-color: #3498db; color: white; border-radius: 50%; text-align: center; line-height: 30px; font-weight: bold; margin-right: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="doc-header">📖 MLDLC Documentation</div>', unsafe_allow_html=True)
st.markdown("""
Complete guide for using the **Machine Learning Development Lifecycle (MLDLC)** 
Governance Framework at **DR Data Decision Intelligence**.
""")

# Table of Contents
st.sidebar.title("📑 Quick Navigation")
for s in ["🏠 Overview", "🎯 VTCO", "⚠️ Risk", "📋 Schemas", "🔗 Lineage", "📜 Audit", "🔧 Tools", "💻 Cursor", "🚀 Quick Start", "❓ FAQ"]:
    st.sidebar.markdown(f"- {s}")

tabs = st.tabs(["🏠 Overview", "🎯 VTCO", "⚠️ Risk", "📋 Schemas", "🔗 Lineage", "📜 Audit", "🔧 Tools", "💻 Cursor", "🚀 Quick Start", "❓ FAQ"])

# TAB 1: OVERVIEW
with tabs[0]:
    st.markdown('<div class="doc-section">🏠 MLDLC Framework Overview</div>', unsafe_allow_html=True)
    st.markdown("""
    The **MLDLC Governance Framework** ensures all machine learning and data initiatives 
    at DR Data Decision Intelligence are:
    - ✅ **Transparent** - Every decision is explainable
    - ✅ **Explainable** - Clear reasoning for all actions
    - ✅ **Auditable** - Complete decision trail
    - ✅ **Traceable** - Full data lineage
    """)
    st.markdown('<div class="doc-subsection">Core Components</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🎯 VTCO** | **⚠️ Risk Matrix** | **📋 Schema Validation**")
    with col2:
        st.markdown("**🔗 Lineage** | **📜 Audit** | **🔧 MCP Integration**")
    st.markdown('<div class="doc-subsection">Architecture</div>', unsafe_allow_html=True)
    st.code("VTCO → Risk Matrix → Schema Validation → Lineage → Audit", language="text")

# TAB 2: VTCO
with tabs[1]:
    st.markdown('<div class="doc-section">🎯 VTCO Methodology</div>', unsafe_allow_html=True)
    st.markdown("**VTCO** = **V**erb → **T**ask → **C**onstraint → **O**utcome")
    st.markdown("| Element | Example |")
    st.markdown("|---------|---------|")
    st.markdown("| **VERB** | Create, Update, Delete, Analyze, Validate, Deploy |")
    st.markdown("| **TASK** | Data preprocessing pipeline for churn model |")
    st.markdown("| **CONSTRAINT** | Handle missing values, validate schema, log lineage |")
    st.markdown("| **OUTCOME** | Clean dataset with documented transformations |")
    st.code("""
Tool: mldlc-vtco/define_vtco
Parameters:
  verb: "Create"
  task: "Data preprocessing pipeline"
  constraints: ["Handle missing values", "Validate schema"]
  expected_outcome: "Clean dataset with lineage"
""")

# TAB 3: RISK
with tabs[2]:
    st.markdown('<div class="doc-section">⚠️ Risk Matrix</div>', unsafe_allow_html=True)
    risk_path = BASE_DIR / "governance" / "risk_matrix.json"
    if risk_path.exists():
        with open(risk_path) as f:
            rm = json.load(f)
        for level, d in rm.get("risk_levels", {}).items():
            color = d.get("color", "#808080")
            st.markdown(f"""<div style="background-color:{color};color:white;padding:1rem;border-radius:8px;margin:1rem 0;">
                <h3>{level} - {d.get('name','')}</h3>
                <p><strong>Score:</strong> {d.get('score_range','N/A')}</p>
                <p><strong>Requirements:</strong> {', '.join(d.get('requirements',[])[:2])}...</p>
            </div>""", unsafe_allow_html=True)
    st.code("""
Tool: mldlc-vtco/assess_risk
Parameters:
  description: "Deploy new model"
  scope: "production"
  data_sensitivity: "high"
  financial_impact: "high"
  customer_impact: "high"
""")

# TAB 4: SCHEMAS
with tabs[3]:
    st.markdown('<div class="doc-section">📋 Schema Validation</div>', unsafe_allow_html=True)
    schemas = {"dataset_v1": "Dataset metadata", "model_v1": "Model metrics", "experiment_v1": "Experiment config", "deployment_v1": "Deployment metadata", "lineage_v1": "Lineage record"}
    for name, desc in schemas.items():
        exists = (BASE_DIR / "schemas" / f"{name}.schema.json").exists()
        st.markdown(f"**{'✅' if exists else '⚠️'} {name}** - {desc}")
    st.code("""
Tool: mldlc-vtco/validate_artifact
Parameters:
  artifact_type: "dataset"
  artifact_data: {name, version, source, schema_version}
  strict_mode: true
""")

# TAB 5: LINEAGE
with tabs[4]:
    st.markdown('<div class="doc-section">🔗 Lineage Tracking</div>', unsafe_allow_html=True)
    st.markdown("Every transformation MUST record: source entities, transformation, destination, context, timestamp.")
    st.code("""
Tool: mldlc-lineage/record_lineage
Parameters:
  source_entities: ["dataset:raw:v1"]
  transformation: "Join and aggregate"
  destination_entity: "dataset:features:v1"
  context: "Creating features for model"
""")

# TAB 6: AUDIT
with tabs[5]:
    st.markdown('<div class="doc-section">📜 Audit Trail</div>', unsafe_allow_html=True)
    st.markdown("Events logged: vtco_defined, risk_assessed, schema_validated, lineage_recorded, decision_made")
    st.code("""
Tool: mldlc-vtco/log_audit_event
Parameters:
  event_type: "decision_made"
  event_data: {decision, approver}
  reasoning: "Why this occurred"
""")
    st.markdown('<div class="warning-box">**⚠️** ALL governance decisions MUST be logged.</div>', unsafe_allow_html=True)

# TAB 7: TOOLS
with tabs[6]:
    st.markdown('<div class="doc-section">🔧 MCP Tools Reference</div>', unsafe_allow_html=True)
    st.markdown("| Tool | Purpose |")
    st.markdown("|------|---------|")
    st.markdown("| define_vtco | Create VTCO task |")
    st.markdown("| assess_risk | Classify risk |")
    st.markdown("| validate_artifact | Validate schema |")
    st.markdown("| record_lineage | Record transformation |")
    st.markdown("| get_lineage | Query lineage |")
    st.markdown("| log_audit_event | Log audit event |")

# TAB 8: CURSOR
with tabs[7]:
    st.markdown('<div class="doc-section">💻 Cursor Integration</div>', unsafe_allow_html=True)
    st.markdown("""
    1. **.cursor/mcp.json** - MCP server config
    2. **.cursor/rules/*.mdc** - AI behavior rules
    
    Cursor automatically enforces VTCO, risk assessment, schema validation, lineage, and audit.
    """)
    st.markdown("| Rule | Purpose |")
    st.markdown("|------|---------|")
    st.markdown("| 00-always.mdc | Foundation |")
    st.markdown("| 01-vtco-methodology.mdc | VTCO enforcement |")
    st.markdown("| 02-risk-matrix.mdc | Risk classification |")
    st.markdown("| 03-schema-validation.mdc | Schema compliance |")
    st.markdown("| 04-lineage-tracking.mdc | Lineage |")
    st.markdown("| 05-audit-requirements.mdc | Audit logging |")

# TAB 9: QUICK START
with tabs[8]:
    st.markdown('<div class="doc-section">🚀 Quick Start</div>', unsafe_allow_html=True)
    st.code("""
pip install -r requirements.txt
cp .env.example .env
python run_mcp_stdio.py          # Terminal 1 - MCP for Cursor
streamlit run app/main.py        # Terminal 2 - Dashboard
""")
    st.markdown("Dashboard: http://localhost:8501")

# TAB 10: FAQ
with tabs[9]:
    st.markdown('<div class="doc-section">❓ FAQ</div>', unsafe_allow_html=True)
    faqs = [
        ("What if I skip VTCO?", "Cursor rules remind you. Audit log will show missing definitions."),
        ("Can I override RED risk?", "No. RED requires explicit approval from CTO/DPO/Legal."),
        ("Where are audit logs?", "data/audit/audit.jsonl"),
        ("Can I use without Cursor?", "Yes. MCP tools work via stdio; HTTP server can be added."),
    ]
    for q, a in faqs:
        with st.expander(f"**Q: {q}**"):
            st.markdown(f"**A:** {a}")

st.markdown("---")
st.markdown("**MLDLC Governance Framework** | DR Data Decision Intelligence | Transparent | Explainable | Auditable | Traceable")
