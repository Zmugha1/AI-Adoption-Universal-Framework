#!/usr/bin/env python3
"""
Test script: Simulate coaching interactions and generate sample log data.
Run: python test_coaching_interactions.py

Demonstrates:
1. What gets logged at each step
2. The flow: request → pattern lookup → coaching provided → outcome
3. How to generate data for analysis
"""
import asyncio
import os
import sys
from pathlib import Path

# Setup
REPO = Path(__file__).parent
sys.path.insert(0, str(REPO))
os.environ["GOVERNANCE_REPO_PATH"] = str(REPO)

# Clear or use existing log for demo
COACHING_LOG = REPO / ".ai-governance" / "coaching_log.jsonl"


def run_simulation():
    """Simulate a full coaching interaction flow."""
    from mcp_server import (
        _check_zoning_permission,
        _get_tribal_knowledge,
        log_coaching_provided,
        log_coaching_outcome,
        get_session_id,
    )

    print("=" * 60)
    print("COACHING INTERACTION SIMULATION")
    print("=" * 60)

    # Scenario: Novice developer asks about adding auth endpoint
    file_path = "src/api/auth/login.py"
    query = "How do I add a new API endpoint for user authentication?"

    print("\n[1] COACHING REQUEST (check_zoning_permission)")
    print(f"    File: {file_path}")
    print(f"    Query: {query}")
    result = asyncio.run(
        _check_zoning_permission({
            "file_path": file_path,
            "role": "novice",
            "has_mentor": True,
            "query": query,
        })
    )
    print(f"    -> Zone: {result['zone']}, Allowed: {result['allowed']}")
    print(f"    -> Logged: coaching_request")

    print("\n[2] PATTERN LOOKUP (get_tribal_knowledge)")
    print("    Domain: api-design")
    tk = asyncio.run(_get_tribal_knowledge({"domain": "api-design"}))
    print(f"    -> Pattern: {tk.get('vtco_data', {}).get('pattern', 'N/A')}")
    print("    -> Logged: pattern_referenced")

    print("\n[3] PATTERN LOOKUP (get_tribal_knowledge)")
    print("    Domain: security")
    tk2 = asyncio.run(_get_tribal_knowledge({"domain": "security"}))
    print(f"    -> Pattern: {tk2.get('vtco_data', {}).get('pattern', 'N/A')}")
    print("    -> Logged: pattern_referenced")

    print("\n[4] COACHING PROVIDED (log_coaching_provided)")
    log_coaching_provided(
        file_path=file_path,
        coaching_type="explanation",
        patterns_referenced=["api-design", "security"],
        code_generated=True,
        lines_generated=25,
        validation_checklist=True,
    )
    print("    -> Logged: coaching_provided")

    print("\n[5] COACHING OUTCOME (log_coaching_outcome)")
    log_coaching_outcome(
        file_path=file_path,
        outcome="accepted",
        lines_accepted=22,
        lines_modified=3,
        time_to_decision_seconds=45,
        mentor_consulted=True,
    )
    print("    -> Logged: coaching_accepted")

    print("\n[6] ANOTHER SCENARIO: Expert, Green zone, rejected")
    file_path2 = "tests/utils/helpers.test.ts"
    asyncio.run(
        _check_zoning_permission({
            "file_path": file_path2,
            "role": "expert",
            "query": "Generate unit tests for formatDate",
        })
    )
    log_coaching_provided(
        file_path=file_path2,
        coaching_type="code_generation",
        patterns_referenced=[],
        code_generated=True,
        lines_generated=15,
        validation_checklist=False,
    )
    log_coaching_outcome(
        file_path=file_path2,
        outcome="rejected",
        mentor_consulted=False,
    )
    print("    -> Logged: coaching_request, coaching_provided, coaching_rejected")

    print("\n" + "=" * 60)
    print("Simulation complete. Run: python analyze_coaching_metrics.py")
    print("=" * 60)


if __name__ == "__main__":
    run_simulation()
