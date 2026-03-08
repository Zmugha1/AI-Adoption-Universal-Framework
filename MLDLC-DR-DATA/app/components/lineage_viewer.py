"""Lineage viewer component for Streamlit dashboard."""
import streamlit as st
import json
from pathlib import Path

LINEAGE_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "lineage"


def render_lineage(entity_id: str | None = None) -> None:
    """Render lineage view."""
    if not LINEAGE_PATH.exists():
        st.info("No lineage records yet")
        return
    records = list(LINEAGE_PATH.glob("*.json"))
    if not records:
        st.info("No lineage records yet")
        return
    for f in records[:20]:
        try:
            with open(f, encoding="utf-8") as fp:
                rec = json.load(fp)
            if entity_id and entity_id not in str(rec):
                continue
            st.json(rec)
