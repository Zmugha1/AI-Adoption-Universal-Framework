"""Unit tests for zoning enforcement logic."""

import tempfile
from pathlib import Path

import yaml

from zoning_enforcer import (
    determine_zone,
    get_max_complexity,
    get_scaffolding_level,
    is_role_allowed_in_zone,
    load_governance_rules,
    novice_requires_mentor,
)


def _make_rules(overrides: dict | None = None) -> dict:
    base = {
        "zones": {
            "red": {
                "description": "Red zone",
                "sdlc_phases": ["Requirements-Security", "Design-Database"],
                "allowed_roles": ["Champion"],
                "codeowner_pattern": "**/payment/** **/security/**",
            },
            "yellow": {
                "description": "Yellow zone",
                "sdlc_phases": ["Implementation-Integration"],
                "allowed_roles": ["Intermediate", "Expert", "Champion"],
                "novice_requires_mentor": True,
            },
            "green": {
                "description": "Green zone",
                "sdlc_phases": ["Implementation-CRUD", "Testing-Unit"],
                "allowed_roles": ["Novice", "Intermediate", "Expert", "Champion"],
            },
        },
        "red_zone_patterns": ["**/payment/**", "**/security/**"],
        "skill_scaffolding": {
            "novice": {"max_complexity": 5, "verbosity": "maximum"},
            "intermediate": {"max_complexity": 10, "verbosity": "moderate"},
            "expert": {"max_complexity": 15, "verbosity": "minimal"},
            "champion": {"max_complexity": 20, "verbosity": "consultative"},
        },
    }
    if overrides:
        for k, v in overrides.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                base[k].update(v)
            else:
                base[k] = v
    return base


class TestDetermineZone:
    """Tests for zone determination."""

    def test_red_zone_by_path(self):
        rules = _make_rules()
        assert determine_zone("src/payment/core.py", None, rules) == "Red"
        assert determine_zone("src/security/auth.py", None, rules) == "Red"

    def test_yellow_green_by_phase(self):
        rules = _make_rules()
        assert determine_zone("src/api/client.py", "Implementation-Integration", rules) == "Yellow"
        assert determine_zone("src/crud/repo.py", "Implementation-CRUD", rules) == "Green"
        assert determine_zone("tests/unit/test_foo.py", "Testing-Unit", rules) == "Green"


class TestRoleAllowed:
    """Tests for role-based zone access."""

    def test_red_zone_champion_only(self):
        rules = _make_rules()
        assert is_role_allowed_in_zone("Red", "Champion", rules) is True
        assert is_role_allowed_in_zone("Red", "Expert", rules) is False
        assert is_role_allowed_in_zone("Red", "Novice", rules) is False

    def test_green_zone_all_roles(self):
        rules = _make_rules()
        for role in ["Novice", "Intermediate", "Expert", "Champion"]:
            assert is_role_allowed_in_zone("Green", role, rules) is True

    def test_yellow_zone_intermediate_up(self):
        rules = _make_rules()
        assert is_role_allowed_in_zone("Yellow", "Intermediate", rules) is True
        assert is_role_allowed_in_zone("Yellow", "Expert", rules) is True
        assert is_role_allowed_in_zone("Yellow", "Novice", rules) is False


class TestScaffolding:
    """Tests for scaffolding levels."""

    def test_verbosity_by_role(self):
        rules = _make_rules()
        assert get_scaffolding_level("Novice", rules) == "maximum"
        assert get_scaffolding_level("Champion", rules) == "consultative"

    def test_max_complexity_by_role(self):
        rules = _make_rules()
        assert get_max_complexity("Novice", rules) == 5
        assert get_max_complexity("Champion", rules) == 20


class TestNoviceMentor:
    """Tests for novice mentor requirement."""

    def test_yellow_requires_mentor(self):
        rules = _make_rules()
        assert novice_requires_mentor("Yellow", rules) is True

    def test_green_no_mentor(self):
        rules = _make_rules()
        assert novice_requires_mentor("Green", rules) is False


class TestLoadGovernanceRules:
    """Tests for loading rules from file."""

    def test_load_from_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            rules = _make_rules()
            (path / "governance_rules.yaml").write_text(yaml.dump(rules))
            loaded = load_governance_rules(path)
            assert loaded is not None
            assert "zones" in loaded

    def test_missing_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            assert load_governance_rules(Path(tmp)) is None
