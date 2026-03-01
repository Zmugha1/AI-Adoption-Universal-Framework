"""
Entropy calculation and logging for the AI Adoption Universal Framework.

Entropy formula: (Bloat×0.25) + (Rework×0.25) + (Reverts×0.20) + (Premature×0.30)
All inputs are 0-100 percentages. Output is 0-100 score.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Weights for entropy calculation (must sum to 1.0)
BLOAT_WEIGHT = 0.25
REWORK_WEIGHT = 0.25
REVERT_WEIGHT = 0.20
PREMATURE_WEIGHT = 0.30

logger = logging.getLogger(__name__)


def calculate_entropy(
    bloat_percent: float,
    rework_percent: float,
    revert_percent: float,
    premature_acceptance_percent: float,
) -> float:
    """
    Calculate entropy score from component metrics.
    Each input should be 0-100. Output is 0-100.
    """
    bloat = max(0, min(100, bloat_percent))
    rework = max(0, min(100, rework_percent))
    revert = max(0, min(100, revert_percent))
    premature = max(0, min(100, premature_acceptance_percent))
    return round(
        (bloat * BLOAT_WEIGHT)
        + (rework * REWORK_WEIGHT)
        + (revert * REVERT_WEIGHT)
        + (premature * PREMATURE_WEIGHT),
        2,
    )


def get_maturity_level(entropy_score: float, thresholds: dict[str, float]) -> str:
    """
    Map entropy score to maturity level (M1-M4).
    Lower entropy = higher maturity.
    """
    if entropy_score >= thresholds.get("m1_chaos", 70):
        return "M1"
    if entropy_score >= thresholds.get("m2_shallow", 50):
        return "M2"
    if entropy_score >= thresholds.get("m3_agentic", 30):
        return "M3"
    return "M4"


def get_trend(entropy_log_path: Path, current_score: float) -> str:
    """
    Compare current score to rolling 7-day average.
    Returns: improving | stable | degrading
    """
    if not entropy_log_path.exists():
        return "stable"
    cutoff = datetime.utcnow() - timedelta(days=7)
    scores: list[float] = []
    try:
        with open(entropy_log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = entry.get("timestamp", "")
                    if ts:
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        if dt.tzinfo:
                            dt = dt.replace(tzinfo=None)
                        if dt >= cutoff:
                            scores.append(entry.get("score", 0))
                except json.JSONDecodeError:
                    continue
    except OSError as e:
        logger.warning("Could not read entropy log for trend: %s", e)
        return "stable"
    if not scores:
        return "stable"
    avg = sum(scores) / len(scores)
    diff = avg - current_score
    if diff > 5:
        return "improving"
    if diff < -5:
        return "degrading"
    return "stable"


def log_entropy(
    repo_path: str | Path,
    metrics: dict[str, float],
    score: float,
    maturity: str,
    timestamp: str,
    commit_hash: str | None = None,
) -> bool:
    """
    Append entropy entry to .ai-governance/entropy_log.jsonl.
    """
    repo = Path(repo_path)
    gov_dir = repo / ".ai-governance"
    gov_dir.mkdir(parents=True, exist_ok=True)
    log_path = gov_dir / "entropy_log.jsonl"
    entry = {
        "timestamp": timestamp,
        "commit_hash": commit_hash or "",
        "metrics": metrics,
        "score": score,
        "maturity": maturity,
    }
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        return True
    except OSError as e:
        logger.error("Failed to log entropy: %s", e)
        return False


def get_current_average(repo_path: str | Path, days: int = 7) -> float | None:
    """Calculate rolling average entropy score from log. Returns None if no data."""
    repo = Path(repo_path)
    log_path = repo / ".ai-governance" / "entropy_log.jsonl"
    if not log_path.exists():
        return None
    cutoff = datetime.utcnow() - timedelta(days=days)
    scores: list[float] = []
    try:
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    ts = entry.get("timestamp", "")
                    if ts:
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        if dt.tzinfo:
                            dt = dt.replace(tzinfo=None)
                        if dt >= cutoff:
                            scores.append(entry.get("score", 0))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return None
    return round(sum(scores) / len(scores), 2) if scores else None


def load_entropy_thresholds(repo_path: str | Path) -> dict[str, float]:
    """Load entropy thresholds from governance_rules.yaml if present."""
    import yaml

    repo = Path(repo_path)
    rules_path = repo / "governance_rules.yaml"
    if not rules_path.exists():
        return {
            "m1_chaos": 70,
            "m2_shallow": 50,
            "m3_agentic": 30,
            "m4_autonomous": 15,
        }
    try:
        with open(rules_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data.get("entropy_thresholds", {}) or {}
    except Exception as e:
        logger.warning("Could not load entropy thresholds: %s", e)
        return {
            "m1_chaos": 70,
            "m2_shallow": 50,
            "m3_agentic": 30,
            "m4_autonomous": 15,
        }
