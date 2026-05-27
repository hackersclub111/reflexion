"""Demo data for offline demo mode."""

import json
from datetime import datetime


DEMO_SESSIONS = [
    {
        "id": "demo_session_1",
        "created_at": "2026-05-27T10:00:00",
        "task_description": "Research the latest trends in AI agents",
        "status": "completed",
        "traces": [
            {
                "id": "trace_1_1",
                "query": "What are the latest trends in AI agents?",
                "response": "AI agents are becoming more popular. They use LLMs to reason and plan. Many companies are building agents.",
                "total_tokens": 1250,
                "latency_ms": 2300,
                "quality_score": 0.45,
                "evaluation": {
                    "scores": {
                        "accuracy": {"score": 0.5, "reasoning": "Too generic, lacks specifics"},
                        "helpfulness": {"score": 0.4, "reasoning": "Doesn't provide actionable insights"},
                        "completeness": {"score": 0.3, "reasoning": "Missing key trends and examples"},
                        "efficiency": {"score": 0.6, "reasoning": "Concise but too shallow"},
                        "clarity": {"score": 0.5, "reasoning": "Well-structured but vague"},
                    },
                    "overall_score": 0.45,
                    "summary": "Response is too generic and lacks depth",
                },
            },
            {
                "id": "trace_1_2",
                "query": "Explain how MCP servers work in AI agents",
                "response": "MCP servers provide tools to AI agents. They help agents interact with external services.",
                "total_tokens": 890,
                "latency_ms": 1800,
                "quality_score": 0.52,
                "evaluation": {
                    "scores": {
                        "accuracy": {"score": 0.6, "reasoning": "Correct but incomplete"},
                        "helpfulness": {"score": 0.5, "reasoning": "Basic explanation only"},
                        "completeness": {"score": 0.4, "reasoning": "Missing protocol details"},
                        "efficiency": {"score": 0.6, "reasoning": "Too brief"},
                        "clarity": {"score": 0.5, "reasoning": "Clear but shallow"},
                    },
                    "overall_score": 0.52,
                    "summary": "Explanation is too basic",
                },
            },
        ],
        "improvements": [
            {
                "id": "imp_1_1",
                "type": "prompt_refinement",
                "description": "Add specificity constraint: include examples, statistics, and named entities",
                "before_score": 0.45,
                "after_score": 0.87,
                "applied": True,
                "created_at": "2026-05-27T10:05:00",
            }
        ],
    },
    {
        "id": "demo_session_2",
        "created_at": "2026-05-27T10:15:00",
        "task_description": "Research the latest trends in AI agents (improved)",
        "status": "completed",
        "traces": [
            {
                "id": "trace_2_1",
                "query": "What are the latest trends in AI agents?",
                "response": "Five key trends are reshaping AI agents in 2026:\n\n1. **Multi-Agent Orchestration**: Systems like Google's A2A protocol enable agents to collaborate, with each agent specializing in sub-tasks. Companies like CrewAI and AutoGen report 3x productivity gains.\n\n2. **Self-Improving Agents**: Agents that analyze their own execution traces (via tools like Arize Phoenix) and autonomously refine their strategies. Research shows 20-40% quality improvement over 10 iterations.\n\n3. **MCP-Powered Tool Use**: The Model Context Protocol has become the standard for agent-tool interaction, with 500+ MCP servers now available across GitHub, Slack, databases, and more.\n\n4. **Production Observability**: Tools like Arize Phoenix provide OpenTelemetry-based tracing for agent reasoning, enabling debugging of complex multi-step workflows.\n\n5. **Agentic RAG**: Agents that don't just retrieve documents but reason over them, synthesize across sources, and cite specific passages.",
                "total_tokens": 2100,
                "latency_ms": 950,
                "quality_score": 0.87,
                "evaluation": {
                    "scores": {
                        "accuracy": {"score": 0.9, "reasoning": "Specific, factual, with examples"},
                        "helpfulness": {"score": 0.85, "reasoning": "Directly addresses the question with actionable info"},
                        "completeness": {"score": 0.9, "reasoning": "Covers all major trends with details"},
                        "efficiency": {"score": 0.8, "reasoning": "Well-organized, not wasteful"},
                        "clarity": {"score": 0.9, "reasoning": "Clear structure with bold highlights"},
                    },
                    "overall_score": 0.87,
                    "summary": "Excellent response with specific examples and clear structure",
                },
            },
            {
                "id": "trace_2_2",
                "query": "Explain how MCP servers work in AI agents",
                "response": "MCP (Model Context Protocol) servers are the bridge between AI agents and external tools. Here's the architecture:\n\n**Protocol Layer**: MCP uses JSON-RPC 2.0 over stdio or HTTP. Servers expose tools as callable functions with typed parameters.\n\n**Registration**: Agents register MCP servers in their configuration (e.g., `.gemini/settings.json`). Each server declares its available tools.\n\n**Invocation Flow**:\n1. Agent decides it needs a tool (e.g., 'search database')\n2. Agent sends MCP request with tool name + parameters\n3. MCP server executes the tool (e.g., queries MongoDB)\n4. Server returns structured result\n5. Agent incorporates result into reasoning\n\n**Example**: The Phoenix MCP server (`@arizeai/phoenix-mcp`) exposes tools like `get_traces`, `get_sessions`, `create_evaluation` — letting agents introspect their own performance.\n\n**Security**: MCP servers run in isolated processes. Authentication is handled via API keys or OAuth tokens.",
                "total_tokens": 2800,
                "latency_ms": 1100,
                "quality_score": 0.91,
                "evaluation": {
                    "scores": {
                        "accuracy": {"score": 0.95, "reasoning": "Technically accurate with protocol details"},
                        "helpfulness": {"score": 0.9, "reasoning": "Comprehensive explanation with examples"},
                        "completeness": {"score": 0.9, "reasoning": "Covers architecture, flow, and security"},
                        "efficiency": {"score": 0.85, "reasoning": "Detailed but well-organized"},
                        "clarity": {"score": 0.9, "reasoning": "Clear structure with step-by-step flow"},
                    },
                    "overall_score": 0.91,
                    "summary": "Comprehensive and technically accurate explanation",
                },
            },
        ],
        "improvements": [],
    },
]


def get_demo_sessions() -> list[dict]:
    """Get all demo sessions."""
    return DEMO_SESSIONS


def get_demo_session(session_id: str) -> dict | None:
    """Get a specific demo session."""
    for session in DEMO_SESSIONS:
        if session["id"] == session_id:
            return session
    return None


def get_demo_quality_trend() -> list[dict]:
    """Get quality trend across all demo sessions."""
    trend = []
    for session in DEMO_SESSIONS:
        for trace in session["traces"]:
            trend.append({
                "trace_id": trace["id"],
                "quality_score": trace["quality_score"],
                "latency_ms": trace["latency_ms"],
                "total_tokens": trace["total_tokens"],
                "session_id": session["id"],
            })
    return trend


def get_demo_improvement_summary() -> dict:
    """Get improvement summary across demo sessions."""
    all_traces = []
    all_improvements = []

    for session in DEMO_SESSIONS:
        all_traces.extend(session["traces"])
        all_improvements.extend(session["improvements"])

    scores = [t["quality_score"] for t in all_traces]
    return {
        "total_sessions": len(DEMO_SESSIONS),
        "total_traces": len(all_traces),
        "total_improvements": len(all_improvements),
        "min_score": min(scores),
        "max_score": max(scores),
        "avg_score": sum(scores) / len(scores),
        "improvement_delta": max(scores) - min(scores),
        "improvement_percent": round((max(scores) - min(scores)) / min(scores) * 100, 1),
    }
