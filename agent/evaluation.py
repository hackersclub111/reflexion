"""LLM-as-a-Judge evaluation pipeline for Reflexion."""

import json
from datetime import datetime
from typing import Optional

from google import genai


EVALUATION_CRITERIA = {
    "accuracy": "Is the information provided factually correct and reliable?",
    "helpfulness": "Does the response directly address the user's needs?",
    "completeness": "Does the response cover all aspects of the question?",
    "efficiency": "Is the response concise without sacrificing quality?",
    "clarity": "Is the response well-structured and easy to understand?",
}


async def evaluate_response(
    query: str,
    response: str,
    criteria: Optional[list[str]] = None,
    model: str = "gemini-2.5-pro",
) -> dict:
    """Evaluate an agent response using LLM-as-a-Judge.

    Args:
        query: The original user query.
        response: The agent's response to evaluate.
        criteria: List of criteria to evaluate (defaults to all).
        model: The Gemini model to use for evaluation.

    Returns:
        Dictionary with scores and reasoning for each criterion.
    """
    if criteria is None:
        criteria = list(EVALUATION_CRITERIA.keys())

    criteria_text = "\n".join(
        f"- {c}: {EVALUATION_CRITERIA[c]}" for c in criteria if c in EVALUATION_CRITERIA
    )

    prompt = f"""You are an expert evaluator. Score the following response on each criterion from 0.0 to 1.0.

USER QUERY: {query}

AGENT RESPONSE: {response}

EVALUATION CRITERIA:
{criteria_text}

Respond in JSON format:
{{
    "scores": {{
        "criterion_name": {{"score": 0.0-1.0, "reasoning": "brief explanation"}}
    }},
    "overall_score": 0.0-1.0,
    "summary": "one sentence overall assessment"
}}"""

    try:
        client = genai.Client()
        result = client.models.generate_content(
            model=model,
            contents=prompt,
            config={"temperature": 0.1},
        )

        # Parse JSON from response
        text = result.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        evaluation = json.loads(text)
        evaluation["evaluated_at"] = datetime.now().isoformat()
        evaluation["model"] = model
        return evaluation

    except Exception as e:
        # Fallback: return default scores
        return {
            "scores": {
                c: {"score": 0.5, "reasoning": "Evaluation unavailable"} for c in criteria
            },
            "overall_score": 0.5,
            "summary": f"Evaluation failed: {str(e)}",
            "evaluated_at": datetime.now().isoformat(),
            "model": model,
            "error": str(e),
        }


def calculate_improvement_delta(before: dict, after: dict) -> dict:
    """Calculate the improvement between two evaluations.

    Args:
        before: Evaluation scores before improvement.
        after: Evaluation scores after improvement.

    Returns:
        Dictionary with delta scores and percentage improvements.
    """
    before_scores = before.get("scores", {})
    after_scores = after.get("scores", {})

    deltas = {}
    for criterion in before_scores:
        if criterion in after_scores:
            b = before_scores[criterion].get("score", 0)
            a = after_scores[criterion].get("score", 0)
            delta = a - b
            pct = (delta / b * 100) if b > 0 else 0
            deltas[criterion] = {
                "before": b,
                "after": a,
                "delta": round(delta, 3),
                "percent_change": round(pct, 1),
            }

    overall_before = before.get("overall_score", 0)
    overall_after = after.get("overall_score", 0)
    overall_delta = overall_after - overall_before

    return {
        "criteria_deltas": deltas,
        "overall_before": overall_before,
        "overall_after": overall_after,
        "overall_delta": round(overall_delta, 3),
        "overall_percent_change": round(
            (overall_delta / overall_before * 100) if overall_before > 0 else 0, 1
        ),
        "calculated_at": datetime.now().isoformat(),
    }
