"""
API entry point - FastAPI app with Standard Response Envelope.
Run from project root: uvicorn src.api.main:app --reload
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.users.controller import get_user_by_id

app = FastAPI(title="AI Governance Demo API")


@app.get("/api/users/{user_id}")
async def get_user(user_id: str, request: Request):
    """GET user by ID - returns Standard Response Envelope."""
    request_id = request.headers.get("x-request-id")
    result = get_user_by_id(user_id, request_id)
    status = 200 if result["success"] else 404 if result.get("error", {}).get("code") == "NOT_FOUND" else 400
    return JSONResponse(content=result, status_code=status)
