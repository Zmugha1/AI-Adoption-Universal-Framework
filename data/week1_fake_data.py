"""
Fake Week 1 telemetry data for demo.
Simulates violations.jsonl and scaffolding_effectiveness.jsonl from MCP observation mode.
"""
import random
from datetime import datetime, timedelta

# Seed for reproducible demo
random.seed(42)

ZONES = ["Green", "Yellow", "Red"]
ROLES = ["Novice", "Intermediate", "Expert"]
GREEN_PATHS = ["src/utils/helpers.py", "tests/unit/test_utils.py", "src/models/user.py"]
YELLOW_PATHS = ["src/api/endpoints.py", "tests/integration/test_api.py"]
RED_PATHS = ["src/payment/processor.py", "src/security/auth.py", "migrations/20240115_add_payment.py"]


def generate_violations(n=127):
    """Generate fake violations.jsonl entries."""
    violations = []
    base_time = datetime.now() - timedelta(days=5)

    for i in range(n):
        role = random.choices(ROLES, weights=[0.5, 0.35, 0.15])[0]
        complexity = random.choices([3, 4, 5, 6, 7, 8, 10, 12, 15], weights=[0.1, 0.15, 0.25, 0.2, 0.1, 0.08, 0.06, 0.04, 0.02])[0]

        # Role-zone logic: Novices attempt Red more often (~23 total), 0 false positives
        if role == "Novice":
            zone = random.choices(ZONES, weights=[0.4, 0.25, 0.35])[0]  # ~23 Red attempts
        elif role == "Intermediate":
            zone = random.choices(ZONES, weights=[0.4, 0.45, 0.15])[0]
        else:
            zone = random.choices(ZONES, weights=[0.35, 0.45, 0.2])[0]

        # Green zone: always allowed (0 false positives)
        # Red zone: would_block but enforced=False in Week 1
        allowed = zone == "Green"
        if zone == "Red":
            allowed = False

        path = random.choice(GREEN_PATHS if zone == "Green" else (YELLOW_PATHS if zone == "Yellow" else RED_PATHS))

        # Rework: some files touched 3+ times (for rework metric)
        touch_count = random.choices([1, 2, 3, 4, 5], weights=[0.6, 0.25, 0.08, 0.05, 0.02])[0]
        # Bloat: some accepted with unused code
        has_bloat = random.random() < 0.12 if allowed else False

        violations.append({
            "timestamp": (base_time + timedelta(hours=i * 0.8)).isoformat(),
            "zone": zone,
            "user_role": role,
            "complexity_score": complexity,
            "allowed": allowed,
            "file_path": path,
            "enforced": False,  # Week 1 = observation only
            "touch_count": touch_count,
            "has_bloat": has_bloat,
        })
    return violations


def generate_scaffolding(n=89):
    """Generate fake scaffolding_effectiveness.jsonl entries."""
    scaffolding = []
    base_time = datetime.now() - timedelta(days=5)

    for i in range(n):
        role = random.choices(ROLES, weights=[0.5, 0.35, 0.15])[0]
        # time_to_accept: <5 = premature, >30 = likely read. Target ~45% read rate
        time_to_accept = random.choices(
            [2, 4, 8, 15, 25, 45, 90],
            weights=[0.25, 0.15, 0.15, 0.15, 0.12, 0.12, 0.06]
        )[0]
        lines_explained = random.randint(3, 25)
        modification_required = random.random() < 0.35
        # Revert: deleted within 24h (for revert metric)
        was_reverted = random.random() < 0.08

        scaffolding.append({
            "timestamp": (base_time + timedelta(hours=i * 1.1)).isoformat(),
            "user_role": role,
            "time_to_accept": time_to_accept,
            "lines_explained": lines_explained,
            "modification_required": modification_required,
            "was_reverted": was_reverted,
        })
    return scaffolding
