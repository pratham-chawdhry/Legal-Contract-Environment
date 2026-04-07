from __future__ import annotations
import os
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Body
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

_sessions: Dict[str, LegalContractEnv] = {}

current_session_id: Optional[str] = None


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
def reset(req: Optional[ResetRequest] = Body(default=None)):
    global current_session_id

    task_id = req.task_id if req else "easy"
    max_steps = req.max_steps if req else 30

    env = LegalContractEnv(task_id=task_id, max_steps=max_steps)
    session_id = f"{task_id}_{id(env)}"
    _sessions[session_id] = env
    current_session_id = session_id

    obs = env.reset()
    return obs.model_dump()


@app.post("/step")
def step(body: Dict[str, Any] = Body(...)):
    global current_session_id

    session_id = body.pop("session_id", None) or current_session_id
    if session_id is None:
        raise HTTPException(status_code=400, detail="Call /reset first")

    env = _sessions.get(session_id)
    if env is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    try:
        action = ContractAction(**body)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid action: {e}")

    result = env.step(action)

    return {
        "observation": result.observation.model_dump(),
        "reward": result.reward,
        "done": result.done,
    }


@app.get("/state")
def state():
    global current_session_id

    if current_session_id is None:
        return {"status": "not_initialized"}

    env = _sessions.get(current_session_id)
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


def main():
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run("server.app:app", host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()