#!/usr/bin/env python3
"""
Coaching Metrics Analyzer - Measure and tune coaching effectiveness.

Reads .ai-governance/coaching_log.jsonl and computes:
- Acceptance rate by role, zone, intent
- Pattern usage and effectiveness
- Mentor impact
- Zone-specific success rates

Run: python analyze_coaching_metrics.py
"""
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta

REPO = Path(__file__).parent
COACHING_LOG = REPO / ".ai-governance" / "coaching_log.jsonl"


def load_entries():
    """Load all coaching log entries."""
    if not COACHING_LOG.exists():
        return []
    entries = []
    with open(COACHING_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def analyze(entries: list[dict]) -> dict:
    """Compute coaching metrics for tuning."""
    metrics = {
        "total_events": len(entries),
        "by_event_type": defaultdict(int),
        "by_role": defaultdict(int),
        "by_zone": defaultdict(int),
        "by_intent": defaultdict(int),
        "outcomes": {"accepted": 0, "modified": 0, "rejected": 0},
        "patterns_accessed": defaultdict(int),
        "sessions": set(),
        "mentor_involvement": 0,
        "code_generated_count": 0,
        "total_lines_generated": 0,
    }

    for e in entries:
        event = e.get("event_type", "")
        data = e.get("data", {})
        ctx = e.get("governance_context", {})

        metrics["by_event_type"][event] += 1
        metrics["sessions"].add(e.get("session_id", ""))

        role = data.get("developer_role") or ctx.get("role", "unknown")
        zone = data.get("zone", "unknown")
        intent = data.get("intent") or "unknown"

        if role:
            metrics["by_role"][str(role).lower()] += 1
        if zone:
            metrics["by_zone"][str(zone)] += 1
        if intent:
            metrics["by_intent"][intent] += 1

        if event == "coaching_accepted":
            metrics["outcomes"]["accepted"] += 1
            if data.get("mentor_consulted"):
                metrics["mentor_involvement"] += 1
        elif event == "coaching_modified":
            metrics["outcomes"]["modified"] += 1
        elif event == "coaching_rejected":
            metrics["outcomes"]["rejected"] += 1

        if event == "pattern_referenced":
            domain = data.get("domain", "unknown")
            metrics["patterns_accessed"][domain] += 1

        if event == "coaching_provided":
            if data.get("code_generated"):
                metrics["code_generated_count"] += 1
            metrics["total_lines_generated"] += data.get("lines_generated", 0)

    return metrics


def compute_tuning_insights(metrics: dict) -> list[str]:
    """Generate insights for coaching tuning."""
    insights = []

    total_outcomes = sum(metrics["outcomes"].values())
    if total_outcomes > 0:
        accepted = metrics["outcomes"]["accepted"]
        rejected = metrics["outcomes"]["rejected"]
        acceptance_rate = accepted / total_outcomes * 100
        insights.append(f"Acceptance rate: {acceptance_rate:.1f}% ({accepted}/{total_outcomes})")

        if rejected > accepted and total_outcomes >= 3:
            insights.append("TUNING: High rejection rate - consider reducing verbosity or improving pattern relevance")

    if metrics["by_zone"]:
        red = metrics["by_zone"].get("Red", 0)
        yellow = metrics["by_zone"].get("Yellow", 0)
        green = metrics["by_zone"].get("Green", 0)
        if red > 0:
            insights.append(f"Red zone interactions: {red} - ensure suggest_only is clear")
        if yellow > red + green:
            insights.append("TUNING: Yellow zone dominant - validate pattern_referenced is surfacing at right moment")

    if metrics["patterns_accessed"]:
        top_pattern = max(metrics["patterns_accessed"].items(), key=lambda x: x[1])
        insights.append(f"Most used pattern: {top_pattern[0]} ({top_pattern[1]}x)")

    if metrics["by_role"]:
        novice = metrics["by_role"].get("novice", 0)
        if novice > 0 and metrics["mentor_involvement"] == 0 and metrics["outcomes"]["accepted"] > 0:
            insights.append("TUNING: Novice activity without mentor_involvement logged - add outcome logging")

    return insights


def print_report(metrics: dict, insights: list[str]):
    """Print formatted report."""
    print("\n" + "=" * 60)
    print("COACHING METRICS REPORT")
    print("=" * 60)
    print(f"\nTotal events: {metrics['total_events']}")
    print(f"Unique sessions: {len(metrics['sessions'])}")

    print("\n--- By Event Type ---")
    for event, count in sorted(metrics["by_event_type"].items(), key=lambda x: -x[1]):
        print(f"  {event}: {count}")

    print("\n--- By Role ---")
    for role, count in sorted(metrics["by_role"].items(), key=lambda x: -x[1]):
        print(f"  {role}: {count}")

    print("\n--- By Zone ---")
    for zone, count in sorted(metrics["by_zone"].items(), key=lambda x: -x[1]):
        print(f"  {zone}: {count}")

    print("\n--- Outcomes ---")
    for outcome, count in metrics["outcomes"].items():
        print(f"  {outcome}: {count}")

    print("\n--- Patterns Accessed ---")
    for domain, count in sorted(metrics["patterns_accessed"].items(), key=lambda x: -x[1]):
        print(f"  {domain}: {count}")

    print("\n--- Code Generation ---")
    print(f"  Coaching with code: {metrics['code_generated_count']}")
    print(f"  Total lines generated: {metrics['total_lines_generated']}")

    print("\n--- TUNING INSIGHTS ---")
    for insight in insights:
        print(f"  - {insight}")

    print("\n" + "=" * 60)


def main():
    entries = load_entries()
    if not entries:
        print("No coaching log entries. Run: python test_coaching_interactions.py")
        return

    metrics = analyze(entries)
    insights = compute_tuning_insights(metrics)
    print_report(metrics, insights)


if __name__ == "__main__":
    main()
