"""
MLDLC MCP Server - stdio transport for Cursor integration
Integrates VTCO methodology, Risk Matrix, Schema Validation, and Lineage Tracking
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration - use env or relative to this file
BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMAS_PATH = Path(os.getenv("MLDLC_SCHEMAS_PATH", str(BASE_DIR / "schemas")))
GOVERNANCE_PATH = Path(os.getenv("MLDLC_GOVERNANCE_PATH", str(BASE_DIR / "governance")))
AUDIT_PATH = Path(os.getenv("MLDLC_AUDIT_PATH", str(BASE_DIR / "data" / "audit")))
LINEAGE_PATH = Path(BASE_DIR / "data" / "lineage")

server = Server("mldlc-vtco")


def _log_audit(event_type: str, event_data: dict[str, Any], reasoning: str = "") -> None:
    """Log audit event to file."""
    AUDIT_PATH.mkdir(parents=True, exist_ok=True)
    audit_file = AUDIT_PATH / "audit.jsonl"
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "event_data": event_data,
        "reasoning": reasoning,
    }
    with open(audit_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------
async def _define_vtco(
    verb: str,
    task: str,
    constraints: list[str],
    expected_outcome: str,
    metadata: dict[str, Any] | None = None,
) -> dict:
    vtco_id = hashlib.sha256(f"{verb}:{task}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:12]
    vtco_def = {
        "vtco_id": vtco_id,
        "verb": verb,
        "task": task,
        "constraints": constraints,
        "expected_outcome": expected_outcome,
        "status": "defined",
        "created_at": datetime.utcnow().isoformat(),
        "metadata": metadata or {},
    }
    _log_audit("vtco_defined", vtco_def)
    return {"status": "success", "vtco_id": vtco_id, "definition": vtco_def}


async def _assess_risk(
    description: str,
    scope: str = "development",
    data_sensitivity: str = "low",
    financial_impact: str = "low",
    customer_impact: str = "low",
) -> dict:
    score = 0
    if scope == "production":
        score += 3
    elif scope == "staging":
        score += 2
    else:
        score += 1
    if data_sensitivity == "high":
        score += 3
    elif data_sensitivity == "medium":
        score += 2
    else:
        score += 1
    if financial_impact == "high":
        score += 3
    elif financial_impact == "medium":
        score += 2
    else:
        score += 1
    if customer_impact == "high":
        score += 3
    elif customer_impact == "medium":
        score += 2
    else:
        score += 1

    if score >= 9:
        risk_level = "RED"
        requirements = [
            "Explicit approval required",
            "Full documentation mandatory",
            "Security review required",
            "Rollback plan required",
            "24-hour observation period",
        ]
    elif score >= 5:
        risk_level = "YELLOW"
        requirements = [
            "Manager review required",
            "Documentation recommended",
            "Testing required",
            "Monitoring required",
        ]
    else:
        risk_level = "GREEN"
        requirements = ["Standard process", "Basic documentation", "Self-review acceptable"]

    result = {
        "risk_level": risk_level,
        "risk_score": score,
        "description": description,
        "factors": {
            "scope": scope,
            "data_sensitivity": data_sensitivity,
            "financial_impact": financial_impact,
            "customer_impact": customer_impact,
        },
        "requirements": requirements,
    }
    _log_audit("risk_assessed", result)
    return {"status": "success", "assessment": result}


async def _validate_artifact(
    artifact_type: str,
    artifact_data: dict[str, Any],
    strict_mode: bool = True,
) -> dict:
    schema_file = SCHEMAS_PATH / f"{artifact_type}_v1.schema.json"
    if not schema_file.exists():
        return {
            "status": "error",
            "error_type": "schema_not_found",
            "message": f"Schema not found: {schema_file}",
        }
    with open(schema_file, encoding="utf-8") as f:
        schema = json.load(f)
    errors = []
    warnings = []
    required = schema.get("required", [])
    for field in required:
        if field not in artifact_data:
            errors.append(f"Missing required field: {field}")
    result = {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "schema_type": artifact_type,
        "schema_version": "v1",
    }
    _log_audit("schema_validated", {"artifact_type": artifact_type, "valid": result["valid"]})
    return {
        "status": "success" if result["valid"] else "validation_failed",
        "validation": result,
    }


async def _record_lineage(
    source_entities: list[str],
    transformation: str,
    destination_entity: str,
    context: str,
    code_reference: str | None = None,
) -> dict:
    lineage_id = hashlib.sha256(
        f"{destination_entity}:{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()[:12]
    lineage_record = {
        "lineage_id": lineage_id,
        "source_entities": source_entities,
        "transformation": transformation,
        "destination_entity": destination_entity,
        "context": context,
        "code_reference": code_reference,
        "timestamp": datetime.utcnow().isoformat(),
    }
    LINEAGE_PATH.mkdir(parents=True, exist_ok=True)
    lineage_file = LINEAGE_PATH / f"{lineage_id}.json"
    with open(lineage_file, "w", encoding="utf-8") as f:
        json.dump(lineage_record, f, indent=2)
    _log_audit("lineage_recorded", lineage_record)
    return {"status": "success", "lineage_id": lineage_id, "record": lineage_record}


async def _get_lineage(entity_id: str, direction: str = "both", depth: int = 5) -> dict:
    upstream, downstream = [], []
    if LINEAGE_PATH.exists():
        for f in LINEAGE_PATH.glob("*.json"):
            try:
                with open(f, encoding="utf-8") as fp:
                    rec = json.load(fp)
                if entity_id in rec.get("source_entities", []):
                    downstream.append(rec)
                if rec.get("destination_entity") == entity_id:
                    upstream.append(rec)
            except (json.JSONDecodeError, OSError):
                pass
    return {
        "status": "success",
        "entity_id": entity_id,
        "direction": direction,
        "lineage": {"upstream": upstream[:depth], "downstream": downstream[:depth]},
    }


async def _log_audit_event(event_type: str, event_data: dict[str, Any], reasoning: str) -> dict:
    event_id = hashlib.sha256(
        f"{event_type}:{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()[:12]
    _log_audit(event_type, event_data, reasoning)
    return {"status": "success", "event_id": event_id}


# ---------------------------------------------------------------------------
# MCP Server setup
# ---------------------------------------------------------------------------
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="define_vtco",
            description="Define a VTCO (Verb-Task-Constraint-Outcome) task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "verb": {"type": "string"},
                    "task": {"type": "string"},
                    "constraints": {"type": "array", "items": {"type": "string"}},
                    "expected_outcome": {"type": "string"},
                    "metadata": {"type": "object"},
                },
                "required": ["verb", "task", "constraints", "expected_outcome"],
            },
        ),
        Tool(
            name="assess_risk",
            description="Assess risk level using RED/YELLOW/GREEN matrix.",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "scope": {"type": "string", "enum": ["production", "staging", "development"]},
                    "data_sensitivity": {"type": "string", "enum": ["high", "medium", "low"]},
                    "financial_impact": {"type": "string", "enum": ["high", "medium", "low"]},
                    "customer_impact": {"type": "string", "enum": ["high", "medium", "low"]},
                },
                "required": ["description"],
            },
        ),
        Tool(
            name="validate_artifact",
            description="Validate artifact against JSON schema.",
            inputSchema={
                "type": "object",
                "properties": {
                    "artifact_type": {
                        "type": "string",
                        "enum": ["dataset", "model", "experiment", "deployment"],
                    },
                    "artifact_data": {"type": "object"},
                    "strict_mode": {"type": "boolean"},
                },
                "required": ["artifact_type", "artifact_data"],
            },
        ),
        Tool(
            name="record_lineage",
            description="Record data lineage for a transformation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_entities": {"type": "array", "items": {"type": "string"}},
                    "transformation": {"type": "string"},
                    "destination_entity": {"type": "string"},
                    "context": {"type": "string"},
                    "code_reference": {"type": "string"},
                },
                "required": ["source_entities", "transformation", "destination_entity", "context"],
            },
        ),
        Tool(
            name="get_lineage",
            description="Get lineage for an entity.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entity_id": {"type": "string"},
                    "direction": {"type": "string", "enum": ["upstream", "downstream", "both"]},
                    "depth": {"type": "integer"},
                },
                "required": ["entity_id"],
            },
        ),
        Tool(
            name="log_audit_event",
            description="Log an audit event.",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_type": {"type": "string"},
                    "event_data": {"type": "object"},
                    "reasoning": {"type": "string"},
                },
                "required": ["event_type", "event_data", "reasoning"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        "define_vtco": lambda: _define_vtco(
            arguments["verb"],
            arguments["task"],
            arguments["constraints"],
            arguments["expected_outcome"],
            arguments.get("metadata"),
        ),
        "assess_risk": lambda: _assess_risk(
            arguments["description"],
            arguments.get("scope", "development"),
            arguments.get("data_sensitivity", "low"),
            arguments.get("financial_impact", "low"),
            arguments.get("customer_impact", "low"),
        ),
        "validate_artifact": lambda: _validate_artifact(
            arguments["artifact_type"],
            arguments["artifact_data"],
            arguments.get("strict_mode", True),
        ),
        "record_lineage": lambda: _record_lineage(
            arguments["source_entities"],
            arguments["transformation"],
            arguments["destination_entity"],
            arguments["context"],
            arguments.get("code_reference"),
        ),
        "get_lineage": lambda: _get_lineage(
            arguments["entity_id"],
            arguments.get("direction", "both"),
            arguments.get("depth", 5),
        ),
        "log_audit_event": lambda: _log_audit_event(
            arguments["event_type"],
            arguments["event_data"],
            arguments["reasoning"],
        ),
    }
    if name not in handlers:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]
    result = await handlers[name]()
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


def main() -> int:
    sys.stderr.write("Starting MLDLC VTCO MCP Server...\n")
    sys.stderr.flush()

    async def arun() -> None:
        async with stdio_server() as streams:
            await server.run(streams[0], streams[1], server.create_initialization_options())

    try:
        import anyio
        anyio.run(arun)
    except ImportError:
        import asyncio
        asyncio.run(arun)
    return 0


if __name__ == "__main__":
    sys.exit(main())
