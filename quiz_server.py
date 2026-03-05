#!/usr/bin/env python3
"""
Quiz Server - Unlock YELLOW zone for novice developers.
Run: python quiz_server.py
POST http://localhost:3001/quiz/submit with {"quiz_id":"v1","answers":["b","c","a","d","b"]}
"""
import json
import os
from pathlib import Path

from flask import Flask, request, jsonify

REPO_PATH = Path(os.environ.get("GOVERNANCE_REPO_PATH", "."))
QUIZ_RESULTS_PATH = REPO_PATH / ".ai-governance" / "quiz_results.json"

# Quiz v1: Governance fundamentals (correct: b, c, a, d, b)
QUIZ_V1 = {
    "id": "v1",
    "questions": 5,
    "correct_answers": ["b", "c", "a", "d", "b"],
}

app = Flask(__name__)


def _ensure_gov_dir():
    QUIZ_RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def _load_quiz_results() -> dict:
    if not QUIZ_RESULTS_PATH.exists():
        return {}
    try:
        with open(QUIZ_RESULTS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_quiz_result(quiz_id: str, passed: bool, answers: list) -> None:
    _ensure_gov_dir()
    data = _load_quiz_results()
    data[quiz_id] = {
        "passed": passed,
        "answers": answers,
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    }
    with open(QUIZ_RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@app.route("/quiz/submit", methods=["POST"])
def submit_quiz():
    """Submit quiz answers. Unlocks YELLOW zone if passed."""
    try:
        body = request.get_json(force=True, silent=True) or {}
        quiz_id = body.get("quiz_id", "v1")
        answers = body.get("answers", [])

        if quiz_id != "v1":
            return jsonify({"passed": False, "message": f"Unknown quiz_id: {quiz_id}"}), 400

        correct = QUIZ_V1["correct_answers"]
        if len(answers) != len(correct):
            return jsonify({
                "passed": False,
                "message": f"Expected {len(correct)} answers, got {len(answers)}",
            }), 400

        passed = all(a.lower().strip() == c for a, c in zip(answers, correct))
        _save_quiz_result(quiz_id, passed, answers)

        if passed:
            return jsonify({
                "passed": True,
                "message": "Passed! Unlocked YELLOW zone access",
                "unlocked_zone": "yellow",
            })
        return jsonify({
            "passed": False,
            "message": "Quiz failed. Review governance patterns and try again.",
            "correct_answers": len([1 for a, c in zip(answers, correct) if a.lower().strip() == c]),
            "total": len(correct),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/quiz/status", methods=["GET"])
def quiz_status():
    """Check if YELLOW zone is unlocked."""
    data = _load_quiz_results()
    v1 = data.get("v1", {})
    passed = v1.get("passed", False)
    return jsonify({
        "yellow_zone_unlocked": passed,
        "quiz_v1_passed": passed,
    })


@app.route("/quiz/questions", methods=["GET"])
def quiz_questions():
    """Get quiz questions (for UI)."""
    return jsonify({
        "quiz_id": "v1",
        "questions": [
            {"q": "What zone requires Champion approval?", "options": ["Green", "Yellow", "Red", "All"], "answer": "b"},
            {"q": "Where should tribal knowledge live?", "options": ["Confluence", "In the repo", "Slack", "Email"], "answer": "c"},
            {"q": "What does VTCO stand for?", "options": ["Verb-Task-Constant-Outcome", "Value-Test-Code-Output", "Very-Tight-Change-Order", "None"], "answer": "a"},
            {"q": "Novice in Yellow zone needs:", "options": ["Nothing", "Mentor", "Champion", "Quiz pass or mentor"], "answer": "d"},
            {"q": "Entropy formula includes:", "options": ["Only bloat", "Bloat, rework, reverts, premature", "Only reverts", "Complexity"], "answer": "b"},
        ],
    })


if __name__ == "__main__":
    print("Quiz Server starting on http://localhost:3001")
    print("POST /quiz/submit with {\"quiz_id\":\"v1\",\"answers\":[\"b\",\"c\",\"a\",\"d\",\"b\"]}")
    app.run(host="0.0.0.0", port=3001, debug=False)
