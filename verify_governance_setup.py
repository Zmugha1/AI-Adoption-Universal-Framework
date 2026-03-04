#!/usr/bin/env python3
"""
Verify AI Governance Framework setup matches the Cursor prompt expectations.
Run: python verify_governance_setup.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add repo to path
sys.path.insert(0, str(Path(__file__).parent))

# Set env for testing
os.environ["GOVERNANCE_REPO_PATH"] = str(Path(__file__).parent)
os.environ["GOVERNANCE_ROLE"] = "novice"
os.environ["GOVERNANCE_MENTOR"] = ""

from mcp_server import (
    _check_zoning_permission,
    _get_tribal_knowledge,
    _calculate_entropy,
    _get_ai_context,
    _get_current_role,
)


async def main():
    print("=" * 60)
    print("AI Governance Framework - Setup Verification")
    print("=" * 60)

    # Test 1: get_current_role
    print("\n[Test 1] get_current_role")
    result = await _get_current_role({})
    print(json.dumps(result, indent=2))
    assert "role" in result and result["role"] == "novice"
    print("  OK")

    # Test 2: RED Zone - Novice blocked
    print("\n[Test 2] check_zoning_permission - RED, novice (blocked)")
    result = await _check_zoning_permission({
        "file_path": "src/payment/gateway.ts",
        "role": "novice",
    })
    print(f"  Zone: {result['zone']}, Allowed: {result['allowed']}")
    assert result["zone"] == "Red"
    assert result["allowed"] is False
    print("  OK")

    # Test 3: RED Zone - Champion allowed
    print("\n[Test 3] check_zoning_permission - RED, champion (allowed)")
    result = await _check_zoning_permission({
        "file_path": "src/payment/gateway.ts",
        "role": "champion",
    })
    print(f"  Zone: {result['zone']}, Allowed: {result['allowed']}")
    assert result["zone"] == "Red"
    assert result["allowed"] is True
    print("  OK")

    # Test 4: YELLOW Zone - Novice without mentor blocked
    print("\n[Test 4] check_zoning_permission - YELLOW, novice, no mentor (blocked)")
    result = await _check_zoning_permission({
        "file_path": "src/api/users/controller.ts",
        "role": "novice",
        "has_mentor": False,
    })
    print(f"  Zone: {result['zone']}, Allowed: {result['allowed']}")
    assert result["zone"] == "Yellow"
    assert result["allowed"] is False
    print("  OK")

    # Test 5: YELLOW Zone - Novice with mentor allowed
    print("\n[Test 5] check_zoning_permission - YELLOW, novice, has mentor (allowed)")
    result = await _check_zoning_permission({
        "file_path": "src/api/users/controller.ts",
        "role": "novice",
        "has_mentor": True,
    })
    print(f"  Zone: {result['zone']}, Allowed: {result['allowed']}")
    assert result["zone"] == "Yellow"
    assert result["allowed"] is True
    print("  OK")

    # Test 6: GREEN Zone - Full autonomy
    print("\n[Test 6] check_zoning_permission - GREEN, novice (allowed)")
    result = await _check_zoning_permission({
        "file_path": "tests/utils/helpers.test.ts",
        "role": "novice",
    })
    print(f"  Zone: {result['zone']}, Allowed: {result['allowed']}")
    assert result["zone"] == "Green"
    assert result["allowed"] is True
    print("  OK")

    # Test 7: get_tribal_knowledge - api-design
    print("\n[Test 7] get_tribal_knowledge - api-design")
    result = await _get_tribal_knowledge({"domain": "api-design"})
    assert "vtco_data" in result or "message" in result
    print(f"  Champion: {result.get('champion_owner', 'N/A')}")
    print("  OK")

    # Test 8: get_tribal_knowledge - database
    print("\n[Test 8] get_tribal_knowledge - database")
    result = await _get_tribal_knowledge({"domain": "database"})
    assert "vtco_data" in result or "message" in result
    print("  OK")

    # Test 9: calculate_entropy
    print("\n[Test 9] calculate_entropy")
    result = await _calculate_entropy({
        "bloat_percent": 4.2,
        "rework_percent": 18.0,
        "revert_percent": 2.3,
        "premature_acceptance_percent": 15.6,
    })
    print(f"  Entropy: {result['entropy_score']}, Maturity: {result['maturity_level']}")
    assert result["maturity_level"] == "M4"
    print("  OK")

    # Test 10: get_ai_context - RED
    print("\n[Test 10] get_ai_context - src/payment/gateway.ts (RED)")
    result = await _get_ai_context({"file_path": "src/payment/gateway.ts"})
    print(f"  Zone: {result['zone']}, Can Implement: {result['can_implement']}")
    assert result["zone"] == "Red"
    assert result["can_implement"] is False
    print("  OK")

    # Test 11: get_ai_context - GREEN
    print("\n[Test 11] get_ai_context - tests/utils/helpers.test.ts (GREEN)")
    result = await _get_ai_context({"file_path": "tests/utils/helpers.test.ts"})
    print(f"  Zone: {result['zone']}, Auto-Approve: {result['auto_approve']}")
    assert result["zone"] == "Green"
    assert result["auto_approve"] is True
    print("  OK")

    print("\n" + "=" * 60)
    print("All verification tests PASSED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
