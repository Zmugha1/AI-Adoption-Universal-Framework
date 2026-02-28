"""Unit tests for entropy calculation and logging."""

import json
import tempfile
from pathlib import Path

import pytest

from entropy_tracker import (
    calculate_entropy,
    get_maturity_level,
    get_trend,
    log_entropy,
)


class TestCalculateEntropy:
    """Tests for calculate_entropy formula."""

    def test_formula_weights(self):
        """Weights: Bloat 0.25, Rework 0.25, Revert 0.20, Premature 0.30."""
        # All zeros -> 0
        assert calculate_entropy(0, 0, 0, 0) == 0

        # All 100 -> 100
        assert calculate_entropy(100, 100, 100, 100) == 100

        # Bloat only 100 -> 25
        assert calculate_entropy(100, 0, 0, 0) == 25

        # Rework only 100 -> 25
        assert calculate_entropy(0, 100, 0, 0) == 25

        # Revert only 100 -> 20
        assert calculate_entropy(0, 0, 100, 0) == 20

        # Premature only 100 -> 30
        assert calculate_entropy(0, 0, 0, 100) == 30

    def test_clamping(self):
        """Inputs outside 0-100 are clamped."""
        assert calculate_entropy(-10, 0, 0, 0) == 0
        assert calculate_entropy(150, 0, 0, 0) == 25  # 100*0.25

    def test_rounded_output(self):
        """Output is rounded to 2 decimal places."""
        result = calculate_entropy(33.33, 33.33, 33.33, 33.33)
        assert isinstance(result, float)
        assert round(result, 2) == result


class TestGetMaturityLevel:
    """Tests for maturity level mapping."""

    def test_default_thresholds(self):
        thresholds = {"m1_chaos": 70, "m2_shallow": 50, "m3_agentic": 30, "m4_autonomous": 15}
        assert get_maturity_level(75, thresholds) == "M1"
        assert get_maturity_level(70, thresholds) == "M1"
        assert get_maturity_level(60, thresholds) == "M2"
        assert get_maturity_level(50, thresholds) == "M2"
        assert get_maturity_level(40, thresholds) == "M3"
        assert get_maturity_level(30, thresholds) == "M3"
        assert get_maturity_level(20, thresholds) == "M4"
        assert get_maturity_level(10, thresholds) == "M4"


class TestLogEntropy:
    """Tests for entropy logging."""

    def test_log_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            metrics = {"bloat": 10, "rework": 20, "reverts": 5, "premature": 15}
            ok = log_entropy(path, metrics, 12.5, "M3", "2024-01-15T12:00:00Z", "abc123")
            assert ok
            log_file = path / ".ai-governance" / "entropy_log.jsonl"
            assert log_file.exists()
            lines = log_file.read_text().strip().split("\n")
            assert len(lines) == 1
            entry = json.loads(lines[0])
            assert entry["score"] == 12.5
            assert entry["maturity"] == "M3"
            assert entry["commit_hash"] == "abc123"

    def test_log_append(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            log_entropy(path, {}, 10, "M3", "2024-01-15T12:00:00Z")
            log_entropy(path, {}, 11, "M3", "2024-01-15T13:00:00Z")
            log_file = path / ".ai-governance" / "entropy_log.jsonl"
            lines = log_file.read_text().strip().split("\n")
            assert len(lines) == 2
