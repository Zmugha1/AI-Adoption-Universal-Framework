"""Zone Dashboard - Detect file zones & validate compliance."""
import streamlit as st
import sys
from pathlib import Path

# Add parent for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mcp.server import detect_zone, validate_code, _load_zone_rules

st.title("🟢 Zone Dashboard")
st.caption("Detect file zones and validate compliance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Zone Detection")
    file_path = st.text_input("File path", placeholder="e.g. notebooks/explore_iris.ipynb")
    if file_path:
        zone = detect_zone(file_path)
        rules = _load_zone_rules()
        info = rules.get("zones", {}).get(zone.lower(), {})
        color = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(zone.lower(), "🟢")
        st.success(f"{color} **{zone}** Zone")
        st.write(info.get("description", ""))
        st.write("**Cursor mode:**", info.get("cursor_mode", "—"))

with col2:
    st.subheader("Code Validation")
    zone_val = st.selectbox("Zone", ["GREEN", "YELLOW", "RED"])
    code = st.text_area("Paste code to validate", height=150, placeholder="# Your ML code here...")
    if st.button("Validate"):
        if code:
            result = validate_code(code, zone_val)
            if result["valid"]:
                st.success("✅ Code passes zone rules")
            else:
                st.error("❌ Violations found")
                for v in result["violations"]:
                    st.write(f"- {v}")
                if result["suggestions"]:
                    st.info("**Suggestions:** " + "; ".join(result["suggestions"]))
        else:
            st.warning("Paste code first")
