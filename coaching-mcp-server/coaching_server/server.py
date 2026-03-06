#!/usr/bin/env python3
"""
Coaching MCP Server - Teaches WHY, validates against industry standards.
Runs on port 8001.
"""
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

APP_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = APP_DIR / "knowledge"
PROMPTS_DIR = APP_DIR / "prompts"

app = FastAPI(title="Coaching MCP Server", version="1.0.0")

# ---------------------------------------------------------------------------
# Load knowledge
# ---------------------------------------------------------------------------
EXPLANATIONS_DIR = KNOWLEDGE_DIR / "explanations"
DIAGNOSTICS_DIR = KNOWLEDGE_DIR / "diagnostics"
ANTI_PATTERNS_DIR = KNOWLEDGE_DIR / "anti_patterns"


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def get_explanation(topic: str) -> dict | None:
    """Load explanation for topic."""
    path = EXPLANATIONS_DIR / f"{topic}.yaml"
    return _load_yaml(path) if path.exists() else None


def list_explanations() -> list[str]:
    """List available explanation topics."""
    if not EXPLANATIONS_DIR.exists():
        return []
    return [p.stem for p in EXPLANATIONS_DIR.glob("*.yaml")]


def get_diagnostic(symptom: str) -> dict | None:
    """Load diagnostic for symptom."""
    path = DIAGNOSTICS_DIR / f"{symptom}.yaml"
    return _load_yaml(path) if path.exists() else None


def list_diagnostics() -> list[str]:
    """List available diagnostics."""
    if not DIAGNOSTICS_DIR.exists():
        return []
    return [p.stem for p in DIAGNOSTICS_DIR.glob("*.yaml")]


def get_anti_pattern(name: str) -> dict | None:
    """Load anti-pattern."""
    path = ANTI_PATTERNS_DIR / f"{name}.yaml"
    return _load_yaml(path) if path.exists() else None


def list_anti_patterns() -> list[str]:
    """List available anti-patterns."""
    if not ANTI_PATTERNS_DIR.exists():
        return []
    return [p.stem for p in ANTI_PATTERNS_DIR.glob("*.yaml")]


def load_coaching_prompts() -> dict:
    """Load coaching prompt library."""
    path = PROMPTS_DIR / "coaching_prompts.yaml"
    return _load_yaml(path)


# ---------------------------------------------------------------------------
# Code validation (production readiness)
# ---------------------------------------------------------------------------
def validate_code(code: str) -> dict[str, Any]:
    """Validate code for production readiness. Returns issues and strengths."""
    issues = []
    strengths = []

    # Check random_state
    if "train_test_split" in code and "random_state" not in code:
        issues.append({"severity": "HIGH", "rule": "random_state", "message": "train_test_split missing random_state"})
    if "random_state" in code:
        strengths.append("random_state present for reproducibility")

    # Check Pipeline
    if ("fit_transform" in code or "fit(" in code) and "Pipeline" not in code and "pipeline" not in code.lower():
        if "StandardScaler" in code or "SimpleImputer" in code:
            issues.append({
                "severity": "CRITICAL",
                "rule": "pipeline",
                "message": "Preprocessing outside Pipeline - data leakage risk"
            })
    elif "Pipeline" in code or "pipeline" in code:
        strengths.append("Using Pipeline - reduces leakage risk")

    # Check MLflow / tracking
    if "mlflow" not in code.lower() and "log_" not in code.lower() and "wandb" not in code.lower():
        issues.append({
            "severity": "WARNING",
            "rule": "experiment_tracking",
            "message": "No MLflow or experiment tracking detected"
        })
    else:
        strengths.append("Experiment tracking present")

    return {
        "valid": len([i for i in issues if i["severity"] in ("CRITICAL", "HIGH")]) == 0,
        "issues": issues,
        "strengths": strengths,
    }


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
class ExplainRequest(BaseModel):
    topic: str
    depth: str = "detailed"
    include_code_examples: bool = True
    include_references: bool = True


class ValidateCodeRequest(BaseModel):
    code: str


class DiagnosticRequest(BaseModel):
    symptom: str


class AntiPatternRequest(BaseModel):
    name: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/explain")
def api_explain(req: ExplainRequest) -> dict:
    """Get WHY explanation for a topic."""
    data = get_explanation(req.topic)
    if not data:
        raise HTTPException(404, f"Unknown topic: {req.topic}")

    response = {
        "topic": req.topic,
        "title": data.get("title", ""),
        "why_it_matters": data.get("why_it_matters", ""),
        "detailed_explanation": data.get("detailed_explanation", "") if req.depth == "detailed" else "",
        "common_misconceptions": data.get("common_misconceptions", []),
        "alternatives": data.get("alternatives", []),
        "validation_checklist": data.get("validation_checklist", []),
    }
    if req.include_code_examples:
        response["wrong_code"] = data.get("wrong_code", "")
        response["correct_code"] = data.get("correct_code", "")
    if req.include_references:
        response["references"] = data.get("references", [])

    return response


@app.get("/explain/topics")
def api_list_explain_topics() -> dict:
    """List available explanation topics."""
    return {"topics": list_explanations()}


@app.post("/validate-code")
def api_validate_code(req: ValidateCodeRequest) -> dict:
    """Validate code for production readiness."""
    return validate_code(req.code)


@app.post("/diagnose")
def api_diagnose(req: DiagnosticRequest) -> dict:
    """Get diagnostic workflow for a symptom."""
    data = get_diagnostic(req.symptom)
    if not data:
        raise HTTPException(404, f"Unknown symptom: {req.symptom}")
    return data


@app.get("/diagnose/symptoms")
def api_list_diagnose_symptoms() -> dict:
    """List available diagnostic symptoms."""
    return {"symptoms": list_diagnostics()}


@app.post("/anti-pattern")
def api_anti_pattern(req: AntiPatternRequest) -> dict:
    """Get anti-pattern details."""
    data = get_anti_pattern(req.name)
    if not data:
        raise HTTPException(404, f"Unknown anti-pattern: {req.name}")
    return data


@app.get("/anti-patterns")
def api_list_anti_patterns() -> dict:
    """List available anti-patterns."""
    return {"anti_patterns": list_anti_patterns()}


@app.get("/prompts")
def api_get_prompts(category: str | None = None) -> dict:
    """Get coaching prompts, optionally filtered by category."""
    data = load_coaching_prompts()
    categories = data.get("categories", {})
    if category:
        return {"category": category, "prompts": categories.get(category, [])}
    return {"categories": list(categories.keys()), "prompts": categories}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "coaching-mcp"}


# ---------------------------------------------------------------------------
# Run: uvicorn coaching_server.server:app --reload --port 8001
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
