"""
User API Controller - GET user by ID
Follows Standard Response Envelope pattern (api-design VTCO)
"""
from datetime import datetime, timezone
from uuid import uuid4
from typing import Any


def _envelope(success: bool, data: Any = None, error: dict | None = None) -> dict:
    """Standard Response Envelope - requestId mandatory for distributed tracing."""
    return {
        "success": success,
        "data": data,
        "meta": {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "requestId": str(uuid4()),
        },
        "error": error,
    }


def get_user_by_id(user_id: str, request_id: str | None = None) -> dict:
    """
    Get user by ID endpoint handler.
    
    GET /api/users/{user_id}
    
    Returns Standard Response Envelope.
    """
    # Validate input
    if not user_id or not user_id.strip():
        return _envelope(
            success=False,
            error={
                "code": "VALIDATION_ERROR",
                "message": "User ID is required",
                "details": [{"field": "user_id", "message": "Must not be empty"}],
            },
        )

    # TODO: Replace with actual user lookup (repository/service layer)
    # user = user_repository.get_by_id(user_id)
    user = _mock_get_user(user_id)

    if user is None:
        return _envelope(
            success=False,
            error={
                "code": "NOT_FOUND",
                "message": f"User with ID '{user_id}' not found",
                "details": [],
            },
        )

    return _envelope(success=True, data=user)


def _mock_get_user(user_id: str) -> dict | None:
    """Mock user lookup - replace with repository call."""
    # Demo data - in production use UserRepository.get_by_id(user_id)
    mock_users = {
        "1": {"id": "1", "email": "user1@example.com", "name": "Alice"},
        "2": {"id": "2", "email": "user2@example.com", "name": "Bob"},
    }
    return mock_users.get(user_id)
