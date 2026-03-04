#!/usr/bin/env python3
"""
AI Adoption Universal Framework - MCP Server

Local Python-based MCP server for Cursor IDE integration.
Implements the "Technical Enforcer" role: enforces governance rules,
manages zoning, and tracks entropy metrics.

Run with: python mcp_server.py
Configure in Cursor: Add to MCP settings (mcp_config.json).
"""

from __future__ import annotations

import fnmatch
import json
import logging
import os
import subprocess
import sys
import uuid
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import anyio
import yaml
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from entropy_tracker import (
    calculate_entropy,
    get_current_average,
    get_maturity_level,
    get_trend,
    load_entropy_thresholds,
    log_entropy,
)
from zoning_enforcer import (
    determine_zone,
    get_max_complexity,
    get_scaffolding_level,
    is_role_allowed_in_zone,
    load_governance_rules,
    novice_requires_mentor,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_PATH = Path(os.environ.get("GOVERNANCE_REPO_PATH", "."))
GOV_DIR = REPO_PATH / ".ai-governance"
ENTROPY_LOG = GOV_DIR / "entropy_log.jsonl"
VIOLATIONS_LOG = GOV_DIR / "violations.jsonl"
TRIBAL_KNOWLEDGE_DIR = GOV_DIR / "tribal-knowledge"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
GOVERNANCE_ROLE = os.environ.get("GOVERNANCE_ROLE", "novice")
GOVERNANCE_MENTOR = os.environ.get("GOVERNANCE_MENTOR", "")

# Log to stderr (stdio transport uses stdin/stdout for MCP protocol)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("ai-governance-mcp")

# Observation mode: if governance_rules.yaml missing, log only (no blocking)
OBSERVATION_MODE = False


def _ensure_gov_dir() -> None:
    """Ensure .ai-governance directory exists."""
    GOV_DIR.mkdir(parents=True, exist_ok=True)
    TRIBAL_KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)


def _get_rules() -> dict[str, Any] | None:
    """Load governance rules. Sets OBSERVATION_MODE if missing."""
    global OBSERVATION_MODE
    rules = load_governance_rules(REPO_PATH)
    if rules is None:
        OBSERVATION_MODE = True
        logger.warning("Running in OBSERVATION MODE: governance_rules.yaml not found")
    return rules


def _normalize_role(role: str) -> str:
    """Normalize role for case-insensitive matching (novice -> Novice)."""
    if not role:
        return "Novice"
    r = role.strip().lower()
    return {"novice": "Novice", "intermediate": "Intermediate", "expert": "Expert", "champion": "Champion"}.get(r, role.strip().capitalize())


# ---------------------------------------------------------------------------
# Tool 1: check_zoning_permission
# ---------------------------------------------------------------------------
async def _check_zoning_permission(args: dict[str, Any]) -> dict[str, Any]:
    file_path = args.get("file_path", "")
    sdlc_phase = args.get("sdlc_phase", "Implementation")
    user_role = _normalize_role(args.get("role") or args.get("user_role") or GOVERNANCE_ROLE)
    has_mentor = args.get("has_mentor") if "has_mentor" in args else (bool(GOVERNANCE_MENTOR))
    change_type = args.get("change_type", "bug_fix")
    complexity_score = int(args.get("complexity_score", 5))

    rules = _get_rules()
    if rules is None:
        return {
            "allowed": True,
            "zone": "Yellow",
            "required_approver": None,
            "scaffolding_level": "Moderate",
            "constraints": ["Observation mode: governance rules not loaded"],
            "message": "Observation mode: edits allowed but not enforced.",
        }

    zone = determine_zone(file_path, sdlc_phase, rules)
    scaffolding = get_scaffolding_level(user_role, rules)
    max_complexity = get_max_complexity(user_role, rules)
    allowed = is_role_allowed_in_zone(zone, user_role, rules)
    needs_mentor = user_role == "Novice" and novice_requires_mentor(zone, rules)

    required_approver = None
    constraints: list[str] = []
    message = ""

    if zone == "Red":
        if user_role != "Champion":
            allowed = False
            required_approver = "champion_id"
            constraints = ["Red Zone: Champion approval required", "AI behavior: suggest_only"]
            message = "Red Zone: Only Champions may edit. Use suggest-only mode and escalate to Champion."
        else:
            constraints = ["Red Zone: ADR required", "Champion must document rationale"]
            message = "Red Zone: Champion edit allowed. Document decision in ADR."
    elif zone == "Yellow":
        if needs_mentor and not has_mentor:
            allowed = False
            constraints.append("Yellow Zone: Novice requires mentor assignment")
            message = "Yellow Zone: Novice requires mentor. Get validation before proceeding."
        elif needs_mentor and has_mentor:
            allowed = True  # Novice with mentor can proceed in Yellow
            constraints.append("Yellow Zone: Pattern validation required")
            constraints.append("Mentor review required")
            message = "Yellow Zone: Proceed with pattern validation."
        elif user_role == "Novice" and not allowed:
            allowed = False
            message = "Yellow Zone: Novice requires mentor. Get validation before proceeding."
        else:
            constraints.append("Yellow Zone: Pattern validation required")
            message = "Yellow Zone: Proceed with pattern validation."
    else:
        if complexity_score <= 10:
            message = "Green Zone: Auto-approve if tests pass."
        else:
            constraints.append(f"Complexity {complexity_score} exceeds recommended 10 for Green Zone")
            message = "Green Zone: Consider reducing complexity for faster approval."

    if complexity_score > max_complexity:
        allowed = False
        constraints.append(f"Complexity {complexity_score} exceeds role max ({max_complexity})")
        message = f"Complexity exceeds {user_role} limit ({max_complexity}). Reduce or escalate."

    if OBSERVATION_MODE:
        allowed = True
        message = "[Observation] " + message

    # Log violation when blocked (for MCP enforcement audit trail)
    if not allowed:
        _log_violation({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "file_path": file_path,
            "user_role": user_role,
            "zone": zone,
            "reason": message,
        })

    result: dict[str, Any] = {
        "allowed": allowed,
        "zone": zone,
        "role": user_role,
        "required_approver": required_approver,
        "scaffolding_level": scaffolding,
        "constraints": constraints,
        "message": message,
    }
    if zone == "Yellow" and user_role == "Novice":
        result["has_mentor"] = has_mentor

    # Add VTCO context when Red Zone (path-based lookup, not default payment)
    if zone == "Red":
        domain = _find_domain_for_path(file_path)
        if domain:
            vtco = _load_vtco_for_domain(domain)
        elif "migration" in file_path or "schema" in file_path or "migrations" in file_path:
            vtco = _load_vtco_for_domain("production_database")
        else:
            vtco = _load_vtco_for_domain("payment_processing") or _load_vtco_for_domain("production_database")
        if not vtco and ("migration" in file_path or "schema" in file_path):
            vtco = {
                "domain": "production_database",
                "champion_owner": "Senior_Architect_01",
                "constraints": ["No destructive migrations without rollback", "Use pt-online-schema-change for large tables"],
                "ai_behavior": {"reminder": "RED ZONE - requires Champion approval"},
            }
        result["vtco_context"] = vtco

    return result


# ---------------------------------------------------------------------------
# Tool 2: get_tribal_knowledge
# ---------------------------------------------------------------------------
def _load_vtco_for_domain(domain: str) -> dict[str, Any] | None:
    """Load VTCO YAML for domain from tribal-knowledge dir."""
    if not TRIBAL_KNOWLEDGE_DIR.exists():
        return None
    for f in TRIBAL_KNOWLEDGE_DIR.glob("*.yaml"):
        try:
            with open(f, encoding="utf-8") as fp:
                data = yaml.safe_load(fp)
            if data and data.get("domain") == domain:
                return data
        except Exception as e:
            logger.debug("Skip VTCO file %s: %s", f, e)
    return None


def _path_matches_pattern(path: str, pattern: str) -> bool:
    """Match path against glob pattern (e.g. **/payment/**)."""
    norm = path.replace("\\", "/").strip("/")
    pat = pattern.replace("**/", "").replace("/**", "").strip("*")
    if not pat:
        return True
    return pat in norm or fnmatch.fnmatch(norm, "*" + pat + "*")


def _find_domain_for_path(file_path: str) -> str | None:
    """Find domain that matches file path via domain_mapping."""
    if not TRIBAL_KNOWLEDGE_DIR.exists():
        return None
    norm = file_path.replace("\\", "/")
    for f in TRIBAL_KNOWLEDGE_DIR.glob("*.yaml"):
        try:
            with open(f, encoding="utf-8") as fp:
                data = yaml.safe_load(fp)
            if not data:
                continue
            mapping = data.get("domain_mapping", [])
            for pat in mapping:
                if _path_matches_pattern(norm, pat):
                    return data.get("domain")
        except Exception:
            continue
    return None


async def _get_tribal_knowledge(args: dict[str, Any]) -> dict[str, Any]:
    domain = args.get("domain", "")
    file_path = args.get("file_path", "")

    if not domain and file_path:
        domain = _find_domain_for_path(file_path)
    if not domain:
        return {
            "vtco_data": {},
            "ai_behavior": {"allowed": [], "forbidden": [], "reminder": ""},
            "escalation_path": {},
            "champion_owner": "",
            "message": "No tribal knowledge found for domain or file path.",
        }

    vtco = _load_vtco_for_domain(domain)
    if not vtco:
        return {
            "vtco_data": {},
            "ai_behavior": {"allowed": [], "forbidden": [], "reminder": "Tribal knowledge missing. Proceed with caution."},
            "escalation_path": {},
            "champion_owner": "",
            "message": f"No VTCO found for domain '{domain}'. Champion should add .ai-governance/tribal-knowledge/{domain}.yaml",
        }

    ai_behavior = vtco.get("ai_behavior", {})
    if isinstance(ai_behavior, dict):
        allowed = ai_behavior.get("allowed", [])
        forbidden = ai_behavior.get("forbidden", [])
        reminder = ai_behavior.get("reminder", "")
    else:
        allowed, forbidden, reminder = [], [], str(ai_behavior)

    return {
        "vtco_data": {k: v for k, v in vtco.items() if k not in ("ai_behavior",)},
        "ai_behavior": {"allowed": allowed, "forbidden": forbidden, "reminder": reminder},
        "escalation_path": vtco.get("escalation_path", {}),
        "champion_owner": vtco.get("champion_owner", ""),
        "message": "VTCO loaded successfully.",
    }


# ---------------------------------------------------------------------------
# Tool 3: calculate_entropy
# ---------------------------------------------------------------------------
async def _calculate_entropy(args: dict[str, Any]) -> dict[str, Any]:
    bloat = float(args.get("bloat_percent", 0))
    rework = float(args.get("rework_percent", 0))
    revert = float(args.get("revert_percent", 0))
    premature = float(args.get("premature_acceptance_percent", 0))
    timestamp = args.get("timestamp", "")
    commit_hash = args.get("commit_hash", "")

    if not timestamp:
        from datetime import datetime

        timestamp = datetime.utcnow().isoformat() + "Z"

    score = calculate_entropy(bloat, rework, revert, premature)
    thresholds = load_entropy_thresholds(REPO_PATH)
    maturity = get_maturity_level(score, thresholds)
    trend = get_trend(ENTROPY_LOG, score)

    metrics = {"bloat": bloat, "rework": rework, "reverts": revert, "premature": premature}
    logged = log_entropy(
        REPO_PATH,
        metrics,
        score,
        maturity,
        timestamp,
        commit_hash or None,
    )

    return {
        "entropy_score": score,
        "maturity_level": maturity,
        "trend": trend,
        "logged": logged,
        "formula_breakdown": {
            "bloat_contribution": round(bloat * 0.25, 2),
            "rework_contribution": round(rework * 0.25, 2),
            "reverts_contribution": round(revert * 0.20, 2),
            "premature_contribution": round(premature * 0.30, 2),
        },
    }


# ---------------------------------------------------------------------------
# Tool 4: validate_code_patterns
# ---------------------------------------------------------------------------
def _estimate_complexity(code_snippet: str) -> int:
    """Simple heuristic: nesting, conditionals, loops."""
    score = 1
    for line in code_snippet.split("\n"):
        stripped = line.strip()
        if any(kw in stripped for kw in ("if ", "elif ", "else:", "for ", "while ", "try:", "except")):
            score += 2
        if "{" in stripped or "}" in stripped:
            score += 1
    return min(score, 20)


async def _validate_code_patterns(args: dict[str, Any]) -> dict[str, Any]:
    code_snippet = args.get("code_snippet", "")
    language = args.get("language", "python")
    pattern_type = args.get("pattern_type", "structure")

    violations: list[dict[str, Any]] = []
    suggestions: list[str] = []
    complexity = _estimate_complexity(code_snippet)
    auto_approved = False

    # Simple pattern checks
    if "password" in code_snippet.lower() and "=" in code_snippet and "hash" not in code_snippet.lower():
        violations.append({"type": "security", "message": "Potential plaintext password handling"})
        suggestions.append("Use secure hashing (bcrypt, argon2) for passwords")

    if "eval(" in code_snippet or "exec(" in code_snippet:
        violations.append({"type": "security", "message": "eval/exec usage"})
        suggestions.append("Avoid eval/exec; use safe parsing or config")

    if "SELECT *" in code_snippet.upper():
        violations.append({"type": "performance", "message": "SELECT * may fetch unnecessary columns"})
        suggestions.append("Select only required columns")

    if complexity <= 10 and not violations:
        auto_approved = True

    return {
        "violations": violations,
        "suggestions": suggestions,
        "complexity_score": complexity,
        "auto_approved": auto_approved,
    }


# ---------------------------------------------------------------------------
# Tool 5: record_decision
# ---------------------------------------------------------------------------
def _log_violation(entry: dict[str, Any]) -> bool:
    """Append to violations.jsonl."""
    _ensure_gov_dir()
    try:
        with open(VIOLATIONS_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return True
    except OSError as e:
        logger.error("Failed to log violation: %s", e)
        return False


async def _record_decision(args: dict[str, Any]) -> dict[str, Any]:
    decision_type = args.get("decision_type", "red_zone_edit")
    file_path = args.get("file_path", "")
    champion_id = args.get("champion_id", "")
    rationale = args.get("rationale", "")
    constraints = args.get("constraints", [])
    timestamp = args.get("timestamp", "")

    if not timestamp:
        from datetime import datetime

        timestamp = datetime.utcnow().isoformat() + "Z"

    adr_id = f"ADR-{uuid.uuid4().hex[:8].upper()}"
    entry = {
        "adr_id": adr_id,
        "decision_type": decision_type,
        "file_path": file_path,
        "champion_id": champion_id,
        "rationale": rationale,
        "constraints": constraints,
        "timestamp": timestamp,
    }
    logged = _log_violation(entry)
    git_commit_required = decision_type in ("red_zone_edit", "pattern_change", "emergency_override")

    return {
        "adr_id": adr_id,
        "logged": logged,
        "git_commit_required": git_commit_required,
    }


# ---------------------------------------------------------------------------
# Tool 6: demo_red_zone_scenario
# ---------------------------------------------------------------------------
async def _demo_red_zone_scenario(_args: dict[str, Any]) -> dict[str, Any]:
    """Run the complete Red Zone blocking demo."""
    now = datetime.utcnow().isoformat() + "Z"
    adr_id = f"ADR-{datetime.utcnow().strftime('%Y-%m')}-001"
    timeline = [
        {"step": 1, "actor": "Developer (Novice)", "action": "Request: ALTER TABLE users DROP COLUMN email;", "timestamp": now},
        {"step": 2, "actor": "MCP Server", "action": "Zone Detection: File path 'migrations/2026_03_01_alter_users.sql'", "result": "Classified as Design-Database phase -> RED ZONE"},
        {"step": 3, "actor": "MCP Server", "action": "VTCO Lookup: Loaded production_database rules", "result": "Zone: Red, M4 requirement, Champion: Senior_Architect_01"},
        {"step": 4, "actor": "MCP Server", "action": "Permission Check: Novice role attempting Red Zone modification", "result": "BLOCKED - Role insufficient"},
        {"step": 5, "actor": "MCP Server", "action": "Constraint Validation", "violations": ["Destructive operation (DROP) without rollback script", "Column removal violates data retention policy", "Novice cannot modify production schema"]},
        {"step": 6, "actor": "MCP Server", "action": "Educational Intervention", "message": "ALTER TABLE on large tables causes exclusive locks. For the users table (2.3M rows), this would lock for ~4 minutes. Use pt-online-schema-change or soft delete first."},
        {"step": 7, "actor": "MCP Server", "action": "ADR Creation", "adr_id": adr_id, "status": "Pending Senior_Architect_01 approval"},
        {"step": 8, "actor": "Champion (Senior_Architect_01)", "action": "Notification sent", "options": ["Approve with rollback script attached", "Request modification (use soft delete)", "Schedule architecture review"]},
    ]
    return {
        "scenario": "database_schema_change",
        "timeline": timeline,
        "outcome": {
            "production_incident_prevented": True,
            "downtime_avoided": "4 minutes",
            "data_loss_prevented": True,
            "education_delivered": "Developer learned about online schema changes",
        },
        "key_takeaway": "Red Zone protection prevented destructive change and educated developer on safe patterns.",
    }


# ---------------------------------------------------------------------------
# Tool 7: get_current_entropy_average
# ---------------------------------------------------------------------------
async def _get_current_entropy_average(_args: dict[str, Any]) -> dict[str, Any]:
    """Get 7-day rolling average entropy score from log."""
    avg = get_current_average(REPO_PATH, days=7)
    return {"7_day_average": avg, "days": 7}


# ---------------------------------------------------------------------------
# Tool 8: calculate_architectural_drift
# ---------------------------------------------------------------------------
async def _calculate_architectural_drift(args: dict[str, Any]) -> dict[str, Any]:
    """Calculate architectural drift metrics for codebase health."""
    repo_path = Path(args.get("repo_path", str(REPO_PATH)))
    days = int(args.get("days", 90))

    # Cyclical Dependency Index (simplified - based on import density)
    cdi: dict[str, Any]
    try:
        result = subprocess.run(
            ["git", "ls-files", "*.py", "*.ts", "*.js"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        files = [f for f in result.stdout.strip().split("\n") if f]
        high_import_files = 0
        for fpath in files[:50]:  # Sample up to 50 files
            try:
                full_path = repo_path / fpath
                if full_path.exists():
                    content = full_path.read_text(encoding="utf-8", errors="ignore")
                    imports = len(
                        [l for l in content.split("\n") if "import" in l or "from " in l]
                    )
                    if imports > 10:
                        high_import_files += 1
            except OSError:
                pass
        cdi_value = (high_import_files / len(files) * 100) if files else 0
        cdi = {
            "value": round(cdi_value, 2),
            "status": "healthy" if cdi_value < 5 else "warning" if cdi_value < 15 else "critical",
        }
    except (subprocess.TimeoutExpired, Exception) as e:
        cdi = {"value": 0, "status": "error", "error": str(e)}

    # Layer Violation Rate (simplified placeholder)
    lvr: dict[str, Any] = {"value": 2.1, "status": "good"}

    # Churn-Complexity Risk from git
    churn_complexity: dict[str, Any]
    try:
        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        result = subprocess.run(
            ["git", "log", "--since", since, "--numstat", "--pretty=format:"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=15,
        )
        file_churn: dict[str, int] = defaultdict(int)
        for line in result.stdout.split("\n"):
            parts = line.split("\t")
            if len(parts) >= 3:
                try:
                    added = int(parts[0]) if parts[0] != "-" else 0
                    deleted = int(parts[1]) if parts[1] != "-" else 0
                    file_churn[parts[2]] += added + deleted
                except ValueError:
                    pass
        risky_files: list[dict[str, Any]] = []
        for fpath, churn in sorted(file_churn.items(), key=lambda x: x[1], reverse=True)[:10]:
            complexity = 10  # Simplified
            risk = complexity * (churn / 100)
            if risk > 10:
                risky_files.append({"file": fpath, "churn": churn, "risk": round(risk, 2)})
        max_risk = max([f["risk"] for f in risky_files], default=0)
        churn_complexity = {
            "max_risk_score": round(max_risk, 2),
            "status": (
                "low_risk" if max_risk < 100 else "medium_risk" if max_risk < 500 else "high_risk"
            ),
            "risky_files_count": len(risky_files),
            "top_risky_files": risky_files[:5],
        }
    except (subprocess.TimeoutExpired, Exception) as e:
        churn_complexity = {"max_risk_score": 0, "status": "error", "error": str(e)}

    # Bus Factor from git
    bus_factor: dict[str, Any]
    try:
        result = subprocess.run(
            ["git", "log", "--format=%an", "--", "."],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
            timeout=10,
        )
        authors: dict[str, int] = defaultdict(int)
        for author in result.stdout.strip().split("\n"):
            if author:
                authors[author] += 1
        total = sum(authors.values())
        sorted_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
        cumulative = 0
        bf = 0
        for author, count in sorted_authors:
            cumulative += count
            bf += 1
            if cumulative >= total * 0.5:
                break
        bus_factor = {
            "average_bus_factor": bf,
            "total_contributors": len(authors),
            "status": "critical" if bf == 1 else "high" if bf == 2 else "acceptable",
        }
    except (subprocess.TimeoutExpired, Exception) as e:
        bus_factor = {"average_bus_factor": 1, "status": "error", "error": str(e)}

    # Overall health score (0-100)
    cdi_score = max(0, 100 - cdi.get("value", 0) * 5)
    lvr_score = max(0, 100 - lvr.get("value", 0) * 20)
    churn_score = max(0, 100 - churn_complexity.get("max_risk_score", 0) / 10)
    bf_score = min(100, bus_factor.get("average_bus_factor", 1) * 33)
    overall_score = cdi_score * 0.25 + lvr_score * 0.25 + churn_score * 0.30 + bf_score * 0.20

    maturity = (
        "Healthy" if overall_score >= 80 else "Warning" if overall_score >= 60 else "Critical"
    )

    return {
        "overall_score": round(overall_score, 2),
        "maturity": maturity,
        "analysis_period_days": days,
        "metrics": {
            "cyclical_dependency_index": cdi,
            "layer_violation_rate": lvr,
            "churn_complexity": churn_complexity,
            "bus_factor": bus_factor,
        },
        "thresholds": {
            "cyclical_dependency_index": {"healthy": "< 5%", "warning": "5-15%", "critical": "> 15%"},
            "layer_violation_rate": {"good": "< 2%", "drifting": "2-5%", "violated": "> 5%"},
            "churn_complexity": {"low_risk": "< 100", "medium_risk": "100-500", "high_risk": "> 500"},
            "bus_factor": {
                "critical": "1 (immediate knowledge transfer)",
                "high": "2 (pair programming recommended)",
                "acceptable": "3+",
            },
        },
        "timestamp": datetime.now().isoformat(),
    }


# ---------------------------------------------------------------------------
# MCP Server Setup
# ---------------------------------------------------------------------------
app = Server(
    "ai-governance",
    version="1.0.0",
    instructions="AI Adoption Universal Framework - Technical Enforcer. Enforces Red/Yellow/Green zoning, skill scaffolding, entropy tracking, and VTCO tribal knowledge.",
)

TOOL_DEFS = [
    types.Tool(
        name="check_zoning_permission",
        description="Check if an edit is allowed based on file path, role, and mentor status. Returns zone, constraints, and scaffolding level.",
        inputSchema={
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {"type": "string", "description": "File path (e.g., src/payment/gateway.ts)"},
                "role": {"type": "string", "description": "novice|intermediate|expert|champion (default from GOVERNANCE_ROLE)"},
                "has_mentor": {"type": "boolean", "description": "Whether novice has mentor assigned (for Yellow zone)"},
                "sdlc_phase": {"type": "string", "description": "Requirements|Design|Implementation|Testing|Deployment|Monitoring"},
                "user_role": {"type": "string", "description": "Alias for role"},
                "change_type": {"type": "string", "description": "new_feature|bug_fix|refactor|config_change"},
                "complexity_score": {"type": "integer", "description": "1-20 cyclomatic complexity estimate"},
            },
        },
    ),
    types.Tool(
        name="get_tribal_knowledge",
        description="Retrieve VTCO (Verb-Task-Constraint-Outcome) context for a domain or file.",
        inputSchema={
            "type": "object",
            "properties": {
                "domain": {"type": "string", "description": "Domain (e.g., payment_processing)"},
                "file_path": {"type": "string", "description": "Optional file path for auto-lookup"},
            },
        },
    ),
    types.Tool(
        name="calculate_entropy",
        description="Calculate and log entropy score from bloat, rework, reverts, premature acceptance.",
        inputSchema={
            "type": "object",
            "required": ["bloat_percent", "rework_percent", "revert_percent", "premature_acceptance_percent"],
            "properties": {
                "bloat_percent": {"type": "number", "description": "0-100"},
                "rework_percent": {"type": "number", "description": "0-100"},
                "revert_percent": {"type": "number", "description": "0-100"},
                "premature_acceptance_percent": {"type": "number", "description": "0-100"},
                "timestamp": {"type": "string", "description": "ISO format"},
                "commit_hash": {"type": "string", "description": "Optional git commit hash"},
            },
        },
    ),
    types.Tool(
        name="validate_code_patterns",
        description="Check if code follows architectural patterns. Returns violations and suggestions.",
        inputSchema={
            "type": "object",
            "required": ["code_snippet"],
            "properties": {
                "code_snippet": {"type": "string", "description": "Code to validate"},
                "language": {"type": "string", "description": "python|javascript|java|etc"},
                "pattern_type": {"type": "string", "description": "naming|structure|security|performance"},
            },
        },
    ),
    types.Tool(
        name="record_decision",
        description="Log architectural decisions (ADR) and champion approvals.",
        inputSchema={
            "type": "object",
            "required": ["decision_type", "file_path", "champion_id", "rationale"],
            "properties": {
                "decision_type": {"type": "string", "description": "red_zone_edit|pattern_change|emergency_override"},
                "file_path": {"type": "string"},
                "champion_id": {"type": "string"},
                "rationale": {"type": "string"},
                "constraints": {"type": "array", "items": {"type": "string"}},
                "timestamp": {"type": "string", "description": "ISO format"},
            },
        },
    ),
    types.Tool(
        name="demo_red_zone_scenario",
        description="Run demo of Red Zone governance protection (database schema change blocking).",
        inputSchema={
            "type": "object",
            "properties": {
                "scenario_type": {"type": "string", "description": "database_schema_change (default)"},
            },
        },
    ),
    types.Tool(
        name="get_current_entropy_average",
        description="Get 7-day rolling average entropy score from log.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="get_current_role",
        description="Get current governance role and mentor configuration from environment.",
        inputSchema={"type": "object", "properties": {}},
    ),
    types.Tool(
        name="get_ai_context",
        description="Get AI behavior context for a file path (what the AI can/cannot do in that zone).",
        inputSchema={
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {"type": "string", "description": "File path to check (e.g., src/payment/gateway.ts)"},
            },
        },
    ),
    types.Tool(
        name="calculate_architectural_drift",
        description="Calculate architectural drift metrics including cyclical dependencies, layer violations, churn-complexity, and bus factor.",
        inputSchema={
            "type": "object",
            "properties": {
                "repo_path": {"type": "string", "description": "Repository path (default: GOVERNANCE_REPO_PATH)"},
                "days": {"type": "number", "description": "Days of git history to analyze (default: 90)"},
            },
        },
    ),
]

async def _get_current_role(_args: dict[str, Any]) -> dict[str, Any]:
    """Return current role and mentor from environment."""
    return {
        "role": GOVERNANCE_ROLE,
        "mentor": GOVERNANCE_MENTOR or None,
        "can_change_via": "export GOVERNANCE_ROLE=<role>",
        "available_roles": ["novice", "intermediate", "expert", "champion"],
    }


async def _get_ai_context(args: dict[str, Any]) -> dict[str, Any]:
    """Get AI behavior context for a file path."""
    file_path = args.get("file_path", "")
    rules = _get_rules()
    if rules is None:
        return {
            "zone": "Yellow",
            "ai_behavior": "generate_with_validation",
            "can_implement": True,
            "can_suggest": True,
            "auto_approve": False,
            "message": "Observation mode: governance rules not loaded.",
        }
    zone = determine_zone(file_path, None, rules)
    zones = rules.get("zones", {})
    zone_config = zones.get(zone.lower(), {})
    behavior = zone_config.get("ai_behavior", "generate_with_validation") if isinstance(zone_config, dict) else "generate_with_validation"
    contexts = {
        "suggest_only": {
            "can_implement": False,
            "can_suggest": True,
            "auto_approve": False,
            "message": "This is high-risk code (payment processing). I can explain the patterns we use, but a Champion must approve any implementation changes.",
        },
        "generate_with_validation": {
            "can_implement": True,
            "can_suggest": True,
            "auto_approve": False,
            "message": "I'll generate code following our established patterns. Make sure to run tests and get code review.",
        },
        "full_autonomy": {
            "can_implement": True,
            "can_suggest": True,
            "auto_approve": True,
            "message": "This is a safe zone for AI assistance. I'll generate code and tests following our standards with auto-approval if tests pass.",
        },
    }
    ctx = contexts.get(behavior, contexts["generate_with_validation"]).copy()
    ctx["zone"] = zone
    ctx["ai_behavior"] = behavior
    if zone == "Red":
        ctx["message"] = "This is high-risk code (payment processing). I can explain the patterns we use, but a Champion must approve any implementation changes."
        ctx["patterns_i_can_explain"] = [
            "Decimal precision for amounts (never float)",
            "Transaction boundaries",
            "Circuit breaker for external calls",
            "Correlation ID logging",
            "Idempotency key handling",
        ]
    elif zone == "Green":
        ctx["message"] = "This is a safe zone for AI assistance. I'll generate code and tests following our standards with auto-approval if tests pass."
        ctx["i_can_help_with"] = [
            "Comprehensive test generation",
            "Edge case identification",
            "Test refactoring",
            "Documentation updates",
        ]
    return ctx


TOOL_HANDLERS = {
    "check_zoning_permission": _check_zoning_permission,
    "get_tribal_knowledge": _get_tribal_knowledge,
    "calculate_entropy": _calculate_entropy,
    "validate_code_patterns": _validate_code_patterns,
    "record_decision": _record_decision,
    "demo_red_zone_scenario": lambda args: _demo_red_zone_scenario(args),
    "get_current_entropy_average": _get_current_entropy_average,
    "get_current_role": _get_current_role,
    "get_ai_context": _get_ai_context,
    "calculate_architectural_drift": _calculate_architectural_drift,
}


@app.list_tools()
async def handle_list_tools(_request: types.ListToolsRequest | None = None) -> types.ListToolsResult:
    return types.ListToolsResult(tools=TOOL_DEFS)


@app.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> types.CallToolResult | dict[str, Any]:
    if name not in TOOL_HANDLERS:
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))],
            isError=True,
        )
    try:
        result = await TOOL_HANDLERS[name](arguments)
        return result  # SDK serializes dict to content automatically
    except Exception as e:
        logger.exception("Tool %s failed", name)
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=json.dumps({"error": str(e)}))],
            isError=True,
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    _ensure_gov_dir()
    rules = _get_rules()
    if rules:
        logger.info("Governance rules loaded. Zones: %s", list(rules.get("zones", {}).keys()))
    else:
        logger.info("Observation mode: no governance rules")
    logger.info("AI Governance MCP server ready (stdio)")

    async def arun() -> None:
        async with stdio_server() as streams:
            await app.run(streams[0], streams[1], app.create_initialization_options())

    anyio.run(arun)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
