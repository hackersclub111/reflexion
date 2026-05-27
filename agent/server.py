"""FastAPI server for Reflexion agent and dashboard API."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.main import run_reflexion
from agent.reflexion import ReflexionEngine
from agent.demo_data import (
    get_demo_sessions,
    get_demo_session,
    get_demo_quality_trend,
    get_demo_improvement_summary,
)


app = FastAPI(title="Reflexion API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    session_id: str | None = None


class QueryResponse(BaseModel):
    query: str
    response: str
    session_id: str
    quality_score: float
    evaluation: dict
    improvement: dict | None
    stats: dict


@app.get("/api/health")
async def health():
    return {"status": "ok", "mode": "demo" if os.getenv("DEMO_MODE") == "true" else "live"}


@app.post("/api/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """Run the Reflexion agent on a query."""
    try:
        result = await run_reflexion(request.query, request.session_id)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions")
async def list_sessions():
    """List all sessions (demo mode returns pre-recorded data)."""
    if os.getenv("DEMO_MODE") == "true":
        return {"sessions": get_demo_sessions()}
    engine = ReflexionEngine()
    stats = engine.get_session_stats()
    engine.close()
    return {"sessions": [stats]}


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get a specific session with traces and improvements."""
    if os.getenv("DEMO_MODE") == "true":
        session = get_demo_session(session_id)
        if session:
            return session
        raise HTTPException(status_code=404, detail="Session not found")

    engine = ReflexionEngine(session_id)
    stats = engine.get_session_stats()
    improvements = engine.get_improvement_history()
    trend = engine.get_quality_trend()
    engine.close()
    return {"stats": stats, "improvements": improvements, "trend": trend}


@app.get("/api/quality-trend")
async def quality_trend():
    """Get quality score trend over time."""
    if os.getenv("DEMO_MODE") == "true":
        return {"trend": get_demo_quality_trend()}

    engine = ReflexionEngine()
    trend = engine.get_quality_trend()
    engine.close()
    return {"trend": trend}


@app.get("/api/improvements")
async def list_improvements():
    """List all improvements."""
    if os.getenv("DEMO_MODE") == "true":
        summary = get_demo_improvement_summary()
        return {"summary": summary}

    engine = ReflexionEngine()
    improvements = engine.get_improvement_history()
    stats = engine.get_session_stats()
    engine.close()
    return {"improvements": improvements, "stats": stats}


@app.get("/api/stats")
async def get_stats():
    """Get overall statistics."""
    if os.getenv("DEMO_MODE") == "true":
        return get_demo_improvement_summary()

    engine = ReflexionEngine()
    stats = engine.get_session_stats()
    engine.close()
    return stats


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
