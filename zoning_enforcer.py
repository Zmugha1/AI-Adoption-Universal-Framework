"""
Zoning enforcement for the AI Adoption Universal Framework.

Maps file paths and SDLC phases to Red/Yellow/Green zones.
Uses governance_rules.yaml and optional CODEOWNERS for Red Zone detection.
"""

from __future__ import annotations

import fnmatch
import logging
import re
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


def _normalize_path(path: str) -> str:
    """Normalize path separators for cross-platform matching."""
    return path.replace("\\", "/").strip("/")


def _glob_match(file_path: str, pattern: str) -> bool:
    """Match file path against glob pattern (e.g. **/payment/**)."""
    norm = _normalize_path(file_path)
    # Convert ** to fnmatch-compatible pattern
    pat = pattern.replace("**/", "*/").replace("/**", "/*")
    if pat.startswith("*"):
        return fnmatch.fnmatch(norm, pat) or fnmatch.fnmatch("/" + norm, "/" + pat)
    return fnmatch.fnmatch(norm, pat)


def _path_matches_any(file_path: str, patterns: list[str]) -> bool:
    """Check if file path matches any of the glob patterns."""
    for pat in patterns:
        if _glob_match(file_path, pat):
            return True
    return False


def _infer_sdlc_phase_from_path(file_path: str, mapping: dict[str, list[str]]) -> str | None:
    """Infer SDLC phase from file path using governance rules mapping."""
    norm = _normalize_path(file_path)
    for phase, patterns in mapping.items():
        if _path_matches_any(norm, patterns):
            return phase
    return None


def load_governance_rules(repo_path: str | Path) -> dict[str, Any] | None:
    """Load governance_rules.yaml. Returns None if missing or invalid."""
    repo = Path(repo_path)
    rules_path = repo / "governance_rules.yaml"
    if not rules_path.exists():
        logger.warning("governance_rules.yaml not found at %s", rules_path)
        return None
    try:
        with open(rules_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error("Failed to load governance_rules.yaml: %s", e)
        return None


def determine_zone(
    file_path: str,
    sdlc_phase: str | None,
    rules: dict[str, Any],
) -> str:
    """
    Determine zone (Red, Yellow, Green) for a file and phase.
    Priority: Green (explicit safe paths) > Red (dangerous) > Phase-based > Yellow default.
    """
    norm = _normalize_path(file_path)

    # 1. EXPLICIT GREEN PATTERNS (checked first - tests, docs, utils are safe)
    green_patterns = rules.get("green_zone_patterns", [])
    if green_patterns and _path_matches_any(file_path, green_patterns):
        logger.info("Zone detection: %s -> Green (explicit green pattern)", file_path)
        return "Green"

    # 2. YELLOW ZONE PATTERNS (medium risk - api, services, integration)
    yellow_patterns = rules.get("yellow_zone_patterns", [])
    if yellow_patterns and _path_matches_any(file_path, yellow_patterns):
        logger.info("Zone detection: %s -> Yellow (explicit yellow pattern)", file_path)
        return "Yellow"

    # 3. RED ZONE PATTERNS (dangerous paths - but tests/ overrides)
    red_zone = rules.get("zones", {}).get("red", {})
    red_patterns = rules.get("red_zone_patterns", [])
    if isinstance(red_zone, dict) and red_zone.get("codeowner_pattern"):
        red_patterns = red_zone["codeowner_pattern"].split()
    if red_patterns and _path_matches_any(file_path, red_patterns):
        # Even if path looks red, test files stay Green
        if _path_matches_any(file_path, ["tests/**", "test/**"]):
            logger.info("Zone detection: %s -> Green (test file overrides red pattern)", file_path)
            return "Green"
        logger.info("Zone detection: %s -> Red (red zone pattern)", file_path)
        return "Red"

    # 4. Phase-based zone lookup
    zones = rules.get("zones", {})
    phase_lower = (sdlc_phase or "").lower()

    for zone_name, zone_config in zones.items():
        if not isinstance(zone_config, dict):
            continue
        phases = zone_config.get("sdlc_phases", [])
        for p in phases:
            if phase_lower in p.lower():
                zone = zone_name.capitalize()
                logger.info("Zone detection: %s -> %s (phase %s matches %s)", file_path, zone, phase_lower or "inferred", p)
                return zone

    # Fallback: use file path mapping
    mapping = rules.get("file_path_mapping", {})
    inferred = _infer_sdlc_phase_from_path(file_path, mapping)
    if inferred:
        for zone_name, zone_config in zones.items():
            if not isinstance(zone_config, dict):
                continue
            phases = zone_config.get("sdlc_phases", [])
            for p in phases:
                if inferred.lower() in p.lower():
                    zone = zone_name.capitalize()
                    logger.info("Zone detection: %s -> %s (inferred phase %s matches %s)", file_path, zone, inferred, p)
                    return zone_name.capitalize()

    # Default to Yellow (safer than Green for unknown)
    logger.info("Zone detection: %s -> Yellow (default)", file_path)
    return "Yellow"


def get_scaffolding_level(role: str, rules: dict[str, Any]) -> str:
    """Map user role to scaffolding verbosity level."""
    scaffolding = rules.get("skill_scaffolding", {})
    role_config = scaffolding.get(role.lower(), {})
    if isinstance(role_config, dict):
        return role_config.get("verbosity", "moderate")
    return "moderate"


def is_role_allowed_in_zone(zone: str, role: str, rules: dict[str, Any]) -> bool:
    """Check if role is allowed to edit in the given zone."""
    zones = rules.get("zones", {})
    zone_config = zones.get(zone.lower(), {})
    if not isinstance(zone_config, dict):
        return False
    allowed = zone_config.get("allowed_roles", [])
    return role in allowed or role in [r.capitalize() for r in allowed]


def novice_requires_mentor(zone: str, rules: dict[str, Any]) -> bool:
    """Check if Novice requires mentor for this zone."""
    zones = rules.get("zones", {})
    zone_config = zones.get(zone.lower(), {})
    if not isinstance(zone_config, dict):
        return False
    return zone_config.get("novice_requires_mentor", False)


def get_max_complexity(role: str, rules: dict[str, Any]) -> int:
    """Get max allowed complexity for role."""
    scaffolding = rules.get("skill_scaffolding", {})
    role_config = scaffolding.get(role.lower(), {})
    if isinstance(role_config, dict):
        return role_config.get("max_complexity", 10)
    return 10
