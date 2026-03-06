#!/usr/bin/env python3
"""
Personal ML MCP Server - FastAPI
Zone-based governance: GREEN (experiment) | YELLOW (develop) | RED (production)
"""
import json
from pathlib import Path
from typing import Any

import fnmatch
import re
import yaml
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

APP_DIR = Path(__file__).resolve().parent.parent
GOVERNANCE_DIR = APP_DIR / "governance"
PROMPTS_DIR = APP_DIR / "prompts"
PATTERNS_DIR = APP_DIR / "patterns"
KNOWLEDGE_DIR = APP_DIR / "knowledge_graph"

app = FastAPI(title="Personal ML MCP Server", version="1.0.0")

# ---------------------------------------------------------------------------
# Load governance
# ---------------------------------------------------------------------------
def _load_zone_rules() -> dict:
    path = GOVERNANCE_DIR / "zone_rules.yaml"
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _normalize_path(p: str) -> str:
    return p.replace("\\", "/").strip("/")


def _glob_match(file_path: str, pattern: str) -> bool:
    norm = _normalize_path(file_path)
    pat = pattern.replace("**/", "*/").replace("/**", "/*")
    if pat.startswith("*"):
        return fnmatch.fnmatch(norm, pat) or fnmatch.fnmatch("/" + norm, "/" + pat)
    return fnmatch.fnmatch(norm, pat)


def _path_matches_any(file_path: str, patterns: list[str]) -> bool:
    for pat in patterns:
        if _glob_match(file_path, pat):
            return True
    return False


def detect_zone(file_path: str) -> str:
    """Auto-detect which zone a file belongs to. Priority: Red > Yellow > Green."""
    rules = _load_zone_rules()
    zones = rules.get("zones", {})
    norm = _normalize_path(file_path)

    for zone_name in ["red", "yellow", "green"]:
        zone = zones.get(zone_name, {})
        patterns = zone.get("file_patterns", [])
        if patterns and _path_matches_any(file_path, patterns):
            return zone_name.upper()

    return "GREEN"  # default: experimentation


def validate_code(code: str, zone: str) -> dict[str, Any]:
    """Validate code against zone rules. Returns violations and suggestions."""
    violations = []
    suggestions = []

    zone_lower = zone.lower()

    if zone_lower == "yellow":
        if "random_state" not in code and "random_state" not in code.lower():
            violations.append("YELLOW zone requires random_state=42 for reproducibility")
            suggestions.append("Add random_state=42 to model/train_test_split/fit calls")
        if "mlflow" not in code.lower() and "log_" not in code.lower():
            violations.append("YELLOW zone should use MLflow or equivalent tracking")
            suggestions.append("Add mlflow.log_params(), mlflow.log_metrics(), mlflow.log_artifact()")

    if zone_lower == "red":
        if "validate" not in code.lower() and "pydantic" not in code.lower() and "schema" not in code.lower():
            violations.append("RED zone requires input validation")
            suggestions.append("Add Pydantic model or schema validation for inputs")
        if "random" in code.lower() and "np.random" not in code.lower():
            violations.append("RED zone should be deterministic in production path")
            suggestions.append("Remove or fix random sampling in inference path")

    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "suggestions": suggestions,
        "zone": zone,
    }


def load_prompts(zone: str) -> list[dict]:
    """Load curated prompts for zone."""
    zone_map = {"green": "green_prompts", "yellow": "yellow_prompts", "red": "red_prompts"}
    fname = zone_map.get(zone.lower(), "green_prompts") + ".yaml"
    path = PROMPTS_DIR / fname
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("prompts", [])


# ---------------------------------------------------------------------------
# Request/Response models
# ---------------------------------------------------------------------------
class DetectZoneRequest(BaseModel):
    file_path: str


class ValidateCodeRequest(BaseModel):
    code: str
    zone: str


class SuggestPatternRequest(BaseModel):
    task: str
    zone: str | None = None


class InitExperimentRequest(BaseModel):
    name: str
    description: str = ""


class QueryKnowledgeRequest(BaseModel):
    query: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.post("/detect-zone")
def api_detect_zone(req: DetectZoneRequest) -> dict:
    """Auto-detect which zone a file belongs to."""
    zone = detect_zone(req.file_path)
    rules = _load_zone_rules()
    zone_info = rules.get("zones", {}).get(zone.lower(), {})
    return {
        "file_path": req.file_path,
        "zone": zone,
        "description": zone_info.get("description", ""),
        "cursor_mode": zone_info.get("cursor_mode", ""),
    }


@app.post("/validate-code")
def api_validate_code(req: ValidateCodeRequest) -> dict:
    """Validate code against zone rules."""
    return validate_code(req.code, req.zone)


@app.post("/suggest-pattern")
def api_suggest_pattern(req: SuggestPatternRequest) -> dict:
    """Suggest patterns based on task."""
    zone = req.zone or "yellow"
    prompts = load_prompts(zone)
    # Simple keyword match for now
    task_lower = req.task.lower()
    relevant = [p for p in prompts if any(t in task_lower for t in p.get("tags", []))]
    if not relevant:
        relevant = prompts[:3]
    return {
        "task": req.task,
        "zone": zone,
        "suggestions": [{"name": p["name"], "text": p["text"][:200] + "..."} for p in relevant],
    }


@app.post("/init-experiment")
def api_init_experiment(req: InitExperimentRequest) -> dict:
    """Initialize new experiment with proper structure."""
    exp_dir = Path(APP_DIR) / "experiments" / req.name.replace(" ", "_").lower()
    exp_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": req.name,
        "description": req.description,
        "zone": "green",
        "created": __import__("datetime").datetime.now().isoformat(),
    }
    (exp_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (exp_dir / "notebook.ipynb").write_text(
        json.dumps({"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4})
    )
    return {
        "status": "created",
        "path": str(exp_dir),
        "manifest": manifest,
    }


@app.post("/query-knowledge-graph")
def api_query_knowledge(req: QueryKnowledgeRequest) -> dict:
    """Query personal ML history."""
    path = KNOWLEDGE_DIR / "experiments.json"
    if not path.exists():
        return {"results": [], "query": req.query}
    data = json.loads(path.read_text())
    # Simple filter for now
    results = [e for e in data if isinstance(e, dict) and req.query.lower() in str(e).lower()]
    return {"results": results[:10], "query": req.query}


@app.get("/prompts/{zone}")
def api_get_prompts(zone: str) -> dict:
    """Get curated prompts for zone."""
    prompts = load_prompts(zone)
    return {"zone": zone.upper(), "prompts": prompts}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "personal-ml-mcp"}


# ---------------------------------------------------------------------------
# Run with: uvicorn mcp.server:app --reload
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
