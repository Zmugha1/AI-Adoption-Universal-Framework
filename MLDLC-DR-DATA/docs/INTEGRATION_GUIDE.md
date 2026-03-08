# How to Add Documentation to Your Streamlit App

## Quick Integration Steps

### Step 1: Documentation Page Location

The documentation page is at `app/pages/6_Documentation.py`. Streamlit automatically adds it to the sidebar when using the native multi-page structure.

### Step 2: Run Your App

```bash
cd MLDLC-DR-DATA
streamlit run app/main.py
```

Access documentation at: `http://localhost:8501/6_Documentation`

### Step 3: Alternative - Pages Directory

If using Streamlit's native multi-page structure, ensure:

```
MLDLC-DR-DATA/
├── app/
│   ├── main.py
│   └── pages/
│       └── 6_Documentation.py
```

When running from project root, use:

```bash
streamlit run app/main.py
```

Streamlit discovers pages in `pages/` relative to the script location.

---

## What the Documentation Page Shows

| Tab | Content |
|-----|---------|
| 🏠 Overview | Framework introduction, core components, architecture |
| 🎯 VTCO | Complete VTCO methodology guide with step-by-step examples |
| ⚠️ Risk | RED/YELLOW/GREEN risk matrix with requirements |
| 📋 Schemas | Schema validation guide with examples |
| 🔗 Lineage | Lineage tracking with code examples |
| 📜 Audit | Audit logging requirements and examples |
| 🔧 Tools | Complete MCP tools reference table |
| 💻 Cursor | How Cursor integrates with MLDLC |
| 🚀 Quick Start | Step-by-step setup guide |
| ❓ FAQ | Common questions and answers |

---

## Usage Flow

```
1. User opens Streamlit app
   ↓
2. Clicks "Documentation" in sidebar
   ↓
3. Reads about VTCO methodology
   ↓
4. Understands risk classification
   ↓
5. Learns how to use MCP tools
   ↓
6. Returns to Dashboard to apply knowledge
```

---

## Customization

To customize the documentation for your specific needs:

1. **Update schema list** in the Schemas tab
2. **Add your own FAQs** in the FAQ tab
3. **Modify risk matrix** display if your matrix differs
4. **Add your logo** in the header section
