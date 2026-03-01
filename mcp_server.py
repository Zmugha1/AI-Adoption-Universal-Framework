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
import sys
import uuid
from datetime import datetime
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


# ---------------------------------------------------------------------------
# Tool 1: check_zoning_permission
# ---------------------------------------------------------------------------
async def _check_zoning_permission(args: dict[str, Any]) -> dict[str, Any]:
    file_path = args.get("file_path", "")
    sdlc_phase = args.get("sdlc_phase", "Implementation")
    user_role = args.get("user_role", "Novice")
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
        if needs_mentor:
            constraints.append("Yellow Zone: Novice requires mentor approval")
        if user_role == "Novice" and not allowed:
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
        "required_approver": required_approver,
        "scaffolding_level": scaffolding,
        "constraints": constraints,
        "message": message,
    }

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
    """Run the complete Red Zone blocking demo for interview/demo."""
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
        description="Check if an edit is allowed based on SDLC phase, file path, and user role. Returns zone, constraints, and scaffolding level.",
        inputSchema={
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {"type": "string", "description": "File path (e.g., src/payment/core.py)"},
                "sdlc_phase": {"type": "string", "description": "Requirements|Design|Implementation|Testing|Deployment|Monitoring"},
                "user_role": {"type": "string", "description": "Novice|Intermediate|Expert|Champion"},
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
]

TOOL_HANDLERS = {
    "check_zoning_permission": _check_zoning_permission,
    "get_tribal_knowledge": _get_tribal_knowledge,
    "calculate_entropy": _calculate_entropy,
    "validate_code_patterns": _validate_code_patterns,
    "record_decision": _record_decision,
    "demo_red_zone_scenario": lambda args: _demo_red_zone_scenario(args),
    "get_current_entropy_average": _get_current_entropy_average,
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
