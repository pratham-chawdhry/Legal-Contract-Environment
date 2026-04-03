"""
server.py — FastAPI server exposing the OpenEnv API.
"""
from __future__ import annotations
import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.environment import LegalContractEnv
from src.models import ContractAction

app = FastAPI(
    title="Legal Contract Review — OpenEnv",
    description="AI agent environment for reviewing legal contracts.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store (single session for simplicity)
_sessions: Dict[str, LegalContractEnv] = {}


class ResetRequest(BaseModel):
    task_id: str = "easy"
    max_steps: int = 30


class StepRequest(BaseModel):
    session_id: str
    action: Dict[str, Any]


@app.get("/")
def root():
    return {"status": "ok", "env": "legal-contract-review", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
def reset(req: ResetRequest):
    env = LegalContractEnv(task_id=req.task_id, max_steps=req.max_steps)
    session_id = f"{req.task_id}_{id(env)}"
    _sessions[session_id] = env
    obs = env.reset()
    return {"session_id": session_id, "observation": obs.model_dump()}


@app.post("/step")
def step(req: StepRequest):
    env = _sessions.get(req.session_id)
    if env is None:
        raise HTTPException(status_code=404, detail="Session not found. Call /reset first.")
    try:
        action = ContractAction(**req.action)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid action: {e}")
    result = env.step(action)
    return result.model_dump()


@app.get("/state")
def state(session_id: str):
    env = _sessions.get(session_id)
    if env is None:
        raise HTTPException(status_code=404, detail="Session not found.")
    return env.state()


@app.get("/tasks")
def list_tasks():
    return {
        "tasks": [
            {"task_id": "easy",   "difficulty": "easy",   "description": "1-page NDA review"},
            {"task_id": "medium", "difficulty": "medium", "description": "8-page SaaS agreement"},
            {"task_id": "hard",   "difficulty": "hard",   "description": "20-page M&A term sheet"},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run("src.server:app", host="0.0.0.0", port=port, reload=False)
