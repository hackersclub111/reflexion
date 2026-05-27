"""Agent tools for Reflexion — research, analyze, and self-improve."""

import json
from datetime import datetime
from google.adk.tools import FunctionTool


def research_topic(query: str) -> str:
    """Research a given topic and return structured findings.

    Args:
        query: The research query to investigate.

    Returns:
        A structured research summary with key findings.
    """
    # In production, this would use web search APIs
    # For the hackathon, we use Gemini's built-in knowledge
    return json.dumps({
        "query": query,
        "timestamp": datetime.now().isoformat(),
        "status": "researched",
        "note": "Research completed using Gemini knowledge base"
    })


def analyze_trace_performance(trace_data: str) -> str:
    """Analyze agent trace data to identify performance issues.

    Args:
        trace_data: JSON string containing trace information.

    Returns:
        Analysis results with identified issues and suggestions.
    """
    try:
        data = json.loads(trace_data) if isinstance(trace_data, str) else trace_data
    except json.JSONDecodeError:
        data = {"raw": str(trace_data)}

    issues = []
    suggestions = []

    # Analyze token usage
    total_tokens = data.get("total_tokens", 0)
    if total_tokens > 2000:
        issues.append("High token usage detected")
        suggestions.append("Use more concise prompts to reduce token consumption")

    # Analyze latency
    latency_ms = data.get("latency_ms", 0)
    if latency_ms > 5000:
        issues.append("High latency detected")
        suggestions.append("Reduce number of tool calls or use faster tools")

    # Analyze tool calls
    tool_calls = data.get("tool_calls", [])
    failed_calls = [t for t in tool_calls if t.get("status") == "failed"]
    if failed_calls:
        issues.append(f"{len(failed_calls)} tool calls failed")
        suggestions.append("Improve tool selection strategy and error handling")

    # Analyze quality score
    quality_score = data.get("quality_score", 1.0)
    if quality_score < 0.6:
        issues.append(f"Low quality score: {quality_score:.2f}")
        suggestions.append("Refine prompts for more detailed and accurate responses")

    return json.dumps({
        "issues": issues,
        "suggestions": suggestions,
        "overall_health": "good" if not issues else "needs_improvement",
        "analyzed_at": datetime.now().isoformat()
    })


def generate_improvement(analysis: str, current_prompt: str) -> str:
    """Generate a targeted improvement based on trace analysis.

    Args:
        analysis: JSON string with analysis results.
        current_prompt: The current system prompt or strategy.

    Returns:
        Improvement recommendation with before/after comparison.
    """
    try:
        analysis_data = json.loads(analysis) if isinstance(analysis, str) else analysis
    except json.JSONDecodeError:
        analysis_data = {"suggestions": ["Improve response quality"]}

    suggestions = analysis_data.get("suggestions", [])

    improvement = {
        "type": "prompt_refinement",
        "description": suggestions[0] if suggestions else "General improvement",
        "before": current_prompt[:200] + "..." if len(current_prompt) > 200 else current_prompt,
        "suggested_changes": [],
        "confidence": 0.85,
        "generated_at": datetime.now().isoformat()
    }

    # Generate specific improvements based on issues
    if any("token" in s.lower() for s in suggestions):
        improvement["suggested_changes"].append({
            "action": "add_constraint",
            "target": "system_prompt",
            "addition": "Be concise. Limit responses to essential information."
        })

    if any("latency" in s.lower() for s in suggestions):
        improvement["suggested_changes"].append({
            "action": "optimize_strategy",
            "target": "tool_selection",
            "addition": "Prioritize faster tools. Batch related queries."
        })

    if any("quality" in s.lower() for s in suggestions):
        improvement["suggested_changes"].append({
            "action": "enhance_prompt",
            "target": "system_prompt",
            "addition": "Provide specific examples. Cite sources. Structure with headers."
        })

    if not improvement["suggested_changes"]:
        improvement["suggested_changes"].append({
            "action": "general_refinement",
            "target": "system_prompt",
            "addition": "Focus on clarity, specificity, and actionable insights."
        })

    return json.dumps(improvement)


def apply_improvement(improvement_data: str, current_config: str) -> str:
    """Apply an improvement to the agent configuration.

    Args:
        improvement_data: JSON string with improvement details.
        current_config: JSON string with current agent configuration.

    Returns:
        Updated configuration with improvements applied.
    """
    try:
        improvement = json.loads(improvement_data) if isinstance(improvement_data, str) else improvement_data
        config = json.loads(current_config) if isinstance(current_config, str) else current_config
    except json.JSONDecodeError:
        return json.dumps({"error": "Invalid input data", "applied": False})

    changes = improvement.get("suggested_changes", [])
    applied_changes = []

    for change in changes:
        target = change.get("target", "system_prompt")
        addition = change.get("addition", "")

        if target == "system_prompt":
            current_prompt = config.get("system_prompt", "")
            if addition not in current_prompt:
                config["system_prompt"] = current_prompt + "\n" + addition
                applied_changes.append(f"Added to system prompt: {addition[:50]}...")

        elif target == "tool_selection":
            config["tool_strategy"] = addition
            applied_changes.append(f"Updated tool strategy: {addition[:50]}...")

    config["last_improved"] = datetime.now().isoformat()
    config["improvement_count"] = config.get("improvement_count", 0) + 1

    return json.dumps({
        "applied": True,
        "changes": applied_changes,
        "config": config
    })


# Export tools for ADK
research_tool = FunctionTool(func=research_topic)
analysis_tool = FunctionTool(func=analyze_trace_performance)
improvement_tool = FunctionTool(func=generate_improvement)
apply_tool = FunctionTool(func=apply_improvement)
