"""Core self-improvement engine for Reflexion agent."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from .evaluation import evaluate_response, calculate_improvement_delta
from .tools import analyze_trace_performance, generate_improvement


DB_PATH = Path(__file__).parent.parent / "data" / "reflexion.db"


def get_db() -> sqlite3.Connection:
    """Get database connection, creating tables if needed."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            task_description TEXT,
            status TEXT DEFAULT 'running',
            total_duration_ms INTEGER,
            improvement_count INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS traces (
            id TEXT PRIMARY KEY,
            session_id TEXT REFERENCES sessions(id),
            trace_id TEXT,
            span_count INTEGER,
            total_tokens INTEGER,
            latency_ms INTEGER,
            quality_score REAL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS improvements (
            id TEXT PRIMARY KEY,
            session_id TEXT REFERENCES sessions(id),
            created_at TEXT NOT NULL,
            type TEXT,
            description TEXT,
            before_score REAL,
            after_score REAL,
            applied INTEGER DEFAULT 0
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS evaluations (
            id TEXT PRIMARY KEY,
            trace_id TEXT REFERENCES traces(id),
            criterion TEXT,
            score REAL,
            reasoning TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


class ReflexionEngine:
    """Manages the self-improvement loop for the agent."""

    def __init__(self, session_id: Optional[str] = None):
        self.conn = get_db()
        if session_id:
            self.session_id = session_id
        else:
            self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.conn.execute(
                "INSERT INTO sessions (id, created_at, status) VALUES (?, ?, ?)",
                (self.session_id, datetime.now().isoformat(), "active"),
            )
            self.conn.commit()

    async def record_trace(
        self,
        query: str,
        response: str,
        trace_id: str,
        total_tokens: int,
        latency_ms: int,
    ) -> dict:
        """Record a trace and evaluate the response.

        Args:
            query: The user's query.
            response: The agent's response.
            trace_id: Phoenix trace ID.
            total_tokens: Total tokens used.
            latency_ms: End-to-end latency.

        Returns:
            Evaluation results with quality score.
        """
        # Evaluate response quality
        evaluation = await evaluate_response(query, response)
        quality_score = evaluation.get("overall_score", 0.5)

        # Store trace
        import uuid
        trace_pk = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO traces (id, session_id, trace_id, span_count, total_tokens, latency_ms, quality_score) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (trace_pk, self.session_id, trace_id, 0, total_tokens, latency_ms, quality_score),
        )

        # Store evaluations
        for criterion, data in evaluation.get("scores", {}).items():
            self.conn.execute(
                "INSERT INTO evaluations (id, trace_id, criterion, score, reasoning, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (str(uuid.uuid4()), trace_pk, criterion, data.get("score", 0), data.get("reasoning", ""), datetime.now().isoformat()),
            )

        self.conn.commit()
        return {"quality_score": quality_score, "evaluation": evaluation, "trace_id": trace_pk}

    async def analyze_and_improve(self) -> Optional[dict]:
        """Analyze recent traces and generate improvements.

        Returns:
            Improvement details if any issues found, None otherwise.
        """
        # Get recent traces for this session
        traces = self.conn.execute(
            "SELECT * FROM traces WHERE session_id = ? ORDER BY id DESC LIMIT 5",
            (self.session_id,),
        ).fetchall()

        if not traces:
            return None

        # Analyze performance
        avg_quality = sum(t["quality_score"] for t in traces) / len(traces)
        avg_latency = sum(t["latency_ms"] for t in traces) / len(traces)
        avg_tokens = sum(t["total_tokens"] for t in traces) / len(traces)

        trace_summary = {
            "total_tokens": int(avg_tokens),
            "latency_ms": int(avg_latency),
            "quality_score": avg_quality,
            "tool_calls": [],
        }

        analysis = analyze_trace_performance(json.dumps(trace_summary))
        analysis_data = json.loads(analysis)

        if analysis_data.get("overall_health") == "good":
            return None

        # Generate improvement
        improvement_json = generate_improvement(
            analysis, "Default system prompt for research tasks"
        )
        improvement = json.loads(improvement_json)

        # Store improvement
        import uuid
        imp_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO improvements (id, session_id, created_at, type, description, before_score, applied) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (imp_id, self.session_id, datetime.now().isoformat(), improvement.get("type"), improvement.get("description"), avg_quality, 0),
        )
        self.conn.commit()

        improvement["id"] = imp_id
        improvement["before_score"] = avg_quality
        return improvement

    def get_improvement_history(self) -> list[dict]:
        """Get all improvements for this session."""
        rows = self.conn.execute(
            "SELECT * FROM improvements WHERE session_id = ? ORDER BY created_at",
            (self.session_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_quality_trend(self) -> list[dict]:
        """Get quality score trend over time."""
        rows = self.conn.execute(
            "SELECT trace_id, quality_score, latency_ms, total_tokens FROM traces WHERE session_id = ? ORDER BY id",
            (self.session_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def get_session_stats(self) -> dict:
        """Get overall session statistics."""
        traces = self.conn.execute(
            "SELECT COUNT(*) as count, AVG(quality_score) as avg_quality, AVG(latency_ms) as avg_latency FROM traces WHERE session_id = ?",
            (self.session_id,),
        ).fetchone()

        improvements = self.conn.execute(
            "SELECT COUNT(*) as count FROM improvements WHERE session_id = ?",
            (self.session_id,),
        ).fetchone()

        return {
            "session_id": self.session_id,
            "total_traces": traces["count"] or 0,
            "avg_quality": round(traces["avg_quality"] or 0, 3),
            "avg_latency_ms": round(traces["avg_latency"] or 0, 1),
            "total_improvements": improvements["count"] or 0,
        }

    def close(self):
        """Close database connection."""
        self.conn.close()
