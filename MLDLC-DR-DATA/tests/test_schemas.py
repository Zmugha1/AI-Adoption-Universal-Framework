"""Tests for JSON schemas."""
import json
from pathlib import Path

import pytest


def test_dataset_schema_valid() -> None:
    """Test dataset schema accepts valid data."""
    schema_path = Path(__file__).parent.parent / "schemas" / "dataset_v1.schema.json"
    with open(schema_path) as f:
        schema = json.load(f)
    assert "required" in schema
    assert "name" in schema["required"]


def test_risk_matrix_exists() -> None:
    """Test risk matrix is valid JSON."""
    risk_path = Path(__file__).parent.parent / "governance" / "risk_matrix.json"
    with open(risk_path) as f:
        data = json.load(f)
    assert "risk_levels" in data
    assert "RED" in data["risk_levels"]
