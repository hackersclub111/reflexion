"""Arize Phoenix instrumentation for Reflexion agent."""

import os
from phoenix.otel import register


def setup_phoenix_tracing() -> None:
    """Configure OpenTelemetry tracing with Arize Phoenix."""
    api_key = os.getenv("PHOENIX_API_KEY")
    endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "https://app.phoenix.arize.com")
    project_name = os.getenv("PHOENIX_PROJECT_NAME", "reflexion")

    if api_key:
        os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={api_key}"

    register(
        project_name=project_name,
        endpoint=endpoint,
        auto_instrument=True,
    )
    print(f"[Reflexion] Phoenix tracing enabled — project: {project_name}")
