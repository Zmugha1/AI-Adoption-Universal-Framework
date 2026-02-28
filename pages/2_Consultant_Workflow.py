import streamlit as st

st.set_page_config(page_title="Consultant Workflow", page_icon="🎯")

st.title("The Lean Consulting Architecture")

st.markdown("""
This framework is designed for **consultant exit**—not permanent dependency.
""")

# Timeline
st.header("Week-by-Week Engagement", divider=True)

timeline_data = [
    {"Week": "0-1", "Consultant": "Assessment + Workshop", "MCP": "Install + Configure", "Champion": "Provide tribal knowledge"},
    {"Week": "2-4", "Consultant": "Train + Dashboard build", "MCP": "Enforce zones", "Champion": "Learn VTCO maintenance"},
    {"Week": "5-8", "Consultant": "Check-in weekly (fade)", "MCP": "Auto-promote novices", "Champion": "Own Red Zone decisions"},
    {"Week": "9-12", "Consultant": "EXIT (quarterly only)", "MCP": "Autonomous enforcement", "Champion": "Full authority + innovation"}
]

for item in timeline_data:
    with st.container():
        cols = st.columns([1, 3, 3, 3])
        cols[0].markdown(f"**{item['Week']}**")
        cols[1].info(f"🎯 {item['Consultant']}")
        cols[2].success(f"🤖 {item['MCP']}")
        cols[3].warning(f"👑 {item['Champion']}")
        st.divider()

# Value Proposition
st.header("Value Proposition", divider=True)

st.markdown("""
**For Headstorm AI Clients:**

1. **Consultant**: Brings methodology, configures MCP, trains champions, exits at Week 8
2. **MCP Server**: One Python file, local execution, enforces governance automatically  
3. **Champions**: Protected from burnout, given authority, enabled to scale expertise

**The Promise:**
- Setup: 2-3 weeks (not months)
- Evidence: Entropy down, Velocity up (measurable Week 4)
- Exit: Self-sustaining system (no permanent consultant dependency)
- Protection: Human architecture, tribal knowledge, and expert judgment preserved

**This is consulting IP—generalizable to any AI use case (coding, content, analysis, customer service) with quantifiable evidence.**
""")
