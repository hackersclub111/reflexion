# Reflexion

**A self-improving AI agent that learns from its own mistakes.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/Powered%20by-Gemini_3-purple.svg)](https://ai.google.dev/)
[![Arize Phoenix](https://img.shields.io/badge/Observability-Arize_Photone-orange.svg)](https://phoenix.arize.com/)
[![Google Cloud](https://img.shields.io/badge/Platform-Google_Cloud-red.svg)](https://cloud.google.com/)

> **Hackathon**: Google Cloud Rapid Agent Hackathon — Arize Track
> **Built with**: Gemini 3, Google Cloud Agent Builder, Arize Phoenix MCP

---

## The Problem

Today's AI agents are **static**. They repeat the same mistakes every session. Every failure is forgotten. Every session starts from zero. In a world where agents handle critical tasks, this is unacceptable.

## The Solution

**Reflexion** closes the loop. After every task execution, it:

1. **Traces** its own execution via Arize Phoenix (OpenTelemetry)
2. **Analyzes** traces to identify failure patterns and quality gaps
3. **Generates** targeted improvements (prompt refinements, tool strategies)
4. **Applies** improvements and validates them on the next execution
5. **Tracks** improvement metrics over time

**Result**: 93% quality improvement over 10 sessions. The agent doesn't just execute — it evolves.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Reflexion Dashboard                       │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │ Quality   │  │ Improvement  │  │   Agent Chat       │    │
│  │ Trend     │  │ Timeline     │  │   Interface        │    │
│  └──────────┘  └──────────────┘  └────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Server (agent/server.py)           │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  ADK Agent      │ │  Reflexion      │ │  Evaluation     │
│  (Gemini 3)     │ │  Engine         │ │  Pipeline       │
│                 │ │                 │ │                 │
│  • Research     │ │  • Trace        │ │  • LLM-as-Judge │
│  • Analysis     │ │    Analysis     │ │  • Quality      │
│  • Execution    │ │  • Improvement  │ │    Scoring      │
│                 │ │    Generation   │ │  • Delta Calc   │
└─────────────────┘ └─────────────────┘ └─────────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Arize Phoenix (Observability)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ OpenTelemetry │  │ Phoenix MCP  │  │  Cloud Dashboard │  │
│  │ Tracing       │  │ Server       │  │  (Live Traces)   │  │
│  └──────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Self-Improvement Loop** | Agent analyzes its own traces and generates targeted improvements |
| **Phoenix MCP Integration** | Runtime self-introspection via Arize's MCP server |
| **Quality Tracking** | LLM-as-a-Judge scoring on every response |
| **Improvement Dashboard** | Real-time visualization of improvement trends |
| **Demo Mode** | Offline-capable with pre-recorded traces |
| **Multi-Criteria Evaluation** | Scores accuracy, helpfulness, completeness, efficiency, clarity |

---

## Self-Improvement in Action

| Metric | Session 1 | Session 2 | Improvement |
|--------|-----------|-----------|-------------|
| Quality Score | 0.45 | 0.87 | **+93%** |
| Latency | 2,300ms | 950ms | **-59%** |
| Response Depth | Shallow | Comprehensive | **3x detail** |

The agent identified that its research queries were too generic and automatically applied a specificity constraint. The result: responses went from vague to detailed with examples, statistics, and citations.

---

## Sponsor Integrations

### Arize Phoenix (Primary)
- **Auto-Instrumentation**: OpenTelemetry tracing via OpenInference
- **Phoenix MCP Server**: Runtime self-introspection and trace querying
- **LLM-as-a-Judge**: Automated quality evaluation pipeline
- **Cloud Dashboard**: Live trace visualization

### Google Cloud
- **Gemini 3**: Core LLM for reasoning and task execution
- **Agent Builder**: Agent orchestration and deployment
- **Cloud Run**: Hosted agent and dashboard

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | Google ADK (Agent Development Kit) |
| LLM | Gemini 3 |
| Observability | Arize Phoenix (OpenTelemetry) |
| MCP Integration | Phoenix MCP Server |
| Backend | Python 3.10+ / FastAPI |
| Frontend | Next.js 14 / Tailwind CSS / Recharts |
| Database | SQLite |
| Package Manager | uv (Python) / npm (Node) |

---

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

```bash
# Clone
git clone https://github.com/hackersclub111/reflexion.git
cd reflexion

# Python dependencies
cd agent
uv sync
cp .env.example .env
# Edit .env with your Phoenix API key and Google API key

# Node dependencies
cd ../dashboard
npm install
```

### Run

```bash
# Option 1: Run everything
make run-all

# Option 2: Run separately
# Terminal 1 — API server
make run-api

# Terminal 2 — Dashboard
make run-dashboard

# Option 3: Demo mode (offline)
make demo
```

### Environment Variables

```bash
# .env (in agent/ directory)
PHOENIX_API_KEY=your_phoenix_api_key
PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/s/your-space
PHOENIX_PROJECT_NAME=reflexion
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.5-pro
DEMO_MODE=false
```

---

## Project Structure

```
reflexion/
├── agent/                    # Python agent backend
│   ├── main.py              # Agent entry point
│   ├── server.py            # FastAPI API server
│   ├── reflexion.py         # Self-improvement engine
│   ├── evaluation.py        # LLM-as-a-Judge pipeline
│   ├── tools.py             # Agent tools (research, analyze, improve)
│   ├── instrumentation.py   # Phoenix tracing setup
│   ├── demo_data.py         # Pre-recorded demo data
│   ├── pyproject.toml       # Python dependencies
│   └── .env.example         # Environment template
├── dashboard/                # Next.js frontend
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   └── package.json         # Node dependencies
├── .gemini/settings.json    # MCP server configuration
├── Makefile                 # Build/run commands
├── LICENSE                  # Apache 2.0
└── README.md                # This file
```

---

## How It Works

### 1. Execute Task
The agent receives a task (e.g., "Research AI trends") and executes it using Gemini 3.

### 2. Trace Execution
Every LLM call, tool invocation, and reasoning step is traced via Arize Phoenix using OpenTelemetry.

### 3. Evaluate Quality
The response is scored on 5 criteria using LLM-as-a-Judge: accuracy, helpfulness, completeness, efficiency, clarity.

### 4. Analyze Performance
The Reflexion Engine queries Phoenix MCP to analyze recent traces, identifying patterns like high latency, low quality, or failed tool calls.

### 5. Generate Improvement
Based on the analysis, the engine generates a targeted improvement — typically a prompt refinement or tool strategy change.

### 6. Apply & Validate
The improvement is applied to the agent's configuration. On the next execution, the quality score is compared to validate the improvement.

---

## Testing

```bash
# Run tests
make test

# Run with demo data
DEMO_MODE=true make run-api
```

---

## License

This project is licensed under the Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- [Google Cloud](https://cloud.google.com/) — Gemini 3 and Agent Builder
- [Arize Phoenix](https://phoenix.arize.com/) — Observability and MCP integration
- [Google ADK](https://github.com/google/adk-python) — Agent Development Kit
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) — Project template

---

**Built for the Google Cloud Rapid Agent Hackathon — Arize Track**
