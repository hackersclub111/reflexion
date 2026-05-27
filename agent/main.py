"""Reflexion — Self-improving agent entry point."""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.sessions import Session

from agent.instrumentation import setup_phoenix_tracing
from agent.reflexion import ReflexionEngine
from agent.tools import research_tool, analysis_tool, improvement_tool, apply_tool


SYSTEM_PROMPT = """You are Reflexion, a self-improving AI agent.

Your unique capability: after every task, you analyze your own performance using Arize Phoenix observability and generate targeted improvements.

When given a task:
1. Research and execute the task using your tools
2. After completion, analyze your performance traces
3. Identify any weaknesses or areas for improvement
4. Generate specific improvements and apply them

You are powered by Gemini 3 and observe your own behavior through Arize Phoenix MCP.

Be thorough, specific, and always include examples. Cite sources when possible."""


async def create_agent() -> Agent:
    """Create the Reflexion agent with all tools."""
    agent = Agent(
        name="reflexion",
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-pro"),
        description="A self-improving AI agent powered by Gemini 3 and Arize Phoenix",
        instruction=SYSTEM_PROMPT,
        tools=[research_tool, analysis_tool, improvement_tool, apply_tool],
    )
    return agent


async def run_reflexion(query: str, session_id: str | None = None) -> dict:
    """Run the Reflexion agent on a query with self-improvement.

    Args:
        query: The user's query/task.
        session_id: Optional session ID for continuing a session.

    Returns:
        Dictionary with response, evaluation, and improvement data.
    """
    # Setup Phoenix tracing
    if os.getenv("DEMO_MODE", "false").lower() != "true":
        setup_phoenix_tracing()

    # Initialize engine
    engine = ReflexionEngine(session_id)
    agent = await create_agent()
    runner = InMemoryRunner(agent=agent, app_name="reflexion")

    # Create or get session
    session = await runner.session_service.create_session(
        app_name="reflexion",
        user_id="demo_user",
    )

    # Run agent
    from google.adk.content_types import Content
    user_message = Content(role="user", parts=[{"text": query}])

    response_text = ""
    async for event in runner.run_async(
        user_id="demo_user",
        session_id=session.id,
        new_message=user_message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    response_text += part.text

    # Record trace and evaluate
    import time
    start_time = time.time()
    trace_result = await engine.record_trace(
        query=query,
        response=response_text,
        trace_id=session.id,
        total_tokens=len(response_text.split()) * 2,  # Approximate
        latency_ms=int((time.time() - start_time) * 1000),
    )

    # Analyze and improve
    improvement = await engine.analyze_and_improve()

    result = {
        "query": query,
        "response": response_text,
        "session_id": engine.session_id,
        "quality_score": trace_result["quality_score"],
        "evaluation": trace_result["evaluation"],
        "improvement": improvement,
        "stats": engine.get_session_stats(),
    }

    engine.close()
    return result


async def main():
    """CLI entry point for testing."""
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Research the latest trends in AI agents and their real-world applications"

    print(f"\n{'='*60}")
    print(f"REFLEXION — Self-Improving Agent")
    print(f"{'='*60}")
    print(f"Query: {query}\n")

    result = await run_reflexion(query)

    print(f"\n{'='*60}")
    print(f"RESPONSE")
    print(f"{'='*60}")
    print(result["response"])

    print(f"\n{'='*60}")
    print(f"QUALITY SCORE: {result['quality_score']:.2f}")
    print(f"{'='*60}")

    if result["improvement"]:
        print(f"\n[SELF-IMPROVEMENT] Generated improvement:")
        print(f"  Type: {result['improvement'].get('type')}")
        print(f"  Description: {result['improvement'].get('description')}")
        print(f"  Before Score: {result['improvement'].get('before_score', 0):.2f}")

    print(f"\nSession Stats: {json.dumps(result['stats'], indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
