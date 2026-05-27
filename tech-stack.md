# Reflexion — Tech Stack

## Core Framework
| Component | Technology | Why |
|-----------|-----------|-----|
| Agent Framework | Google ADK (Agent Development Kit) | Required for hackathon, best Gemini integration |
| LLM | Gemini 3 via Google Cloud | Required by hackathon rules |
| Agent Builder | Google Cloud Agent Builder | Required by hackathon rules |
| Observability | Arize Phoenix Cloud | Partner integration (Arize track) |
| MCP Integration | Phoenix MCP Server | Runtime self-introspection |

## Backend
| Component | Technology | Why |
|-----------|-----------|-----|
| Language | Python 3.10+ | ADK requirement, starter kit language |
| Package Manager | uv | Fast, used by starter kit |
| API Server | FastAPI | Lightweight, async, modern |
| Database | SQLite (local) | Simple, no external deps needed |
| Agent Runtime | ADK Runner | Official Google agent execution |

## Frontend
| Component | Technology | Why |
|-----------|-----------|-----|
| Framework | Next.js 14 (App Router) | Fast to build, great DX |
| UI Library | Tailwind CSS + shadcn/ui | Rapid styling, professional look |
| Charts | Recharts | Lightweight, React-native |
| State | React hooks | Simple, no extra deps |

## Observability Stack
| Component | Technology | Why |
|-----------|-----------|-----|
| Tracing | OpenTelemetry via OpenInference | Arize standard, auto-instrumentation |
| Trace Storage | Phoenix Cloud (free tier) | Hosted, no setup needed |
| Self-Introspection | Phoenix MCP Server | Runtime trace querying |
| Evaluations | LLM-as-a-Judge via Phoenix | Quality scoring |

## Development Tools
| Component | Technology | Why |
|-----------|-----------|-----|
| Version Control | Git + GitHub | Required for submission |
| IDE | Cursor / Gemini CLI | AI-assisted development |
| Deployment | Google Cloud Run | Required for hosted URL |
| CI/CD | GitHub Actions | Automated testing/deployment |

## Verified APIs (from source code, not docs)
- **Google ADK**: `google.adk` — Agent Development Kit Python package
- **Phoenix OTel**: `phoenix.otel.register()` — Auto-instrumentation
- **Phoenix MCP**: `@arizeai/phoenix-mcp` — npx-based MCP server
- **Gemini API**: `google.genai` or `vertexai` — LLM access
- **OpenInference**: `openinference-instrumentation-google-adk` — ADK tracing

## Dependency Lock
- `pyproject.toml` for Python deps
- `package.json` for Next.js deps
- `uv.lock` for Python lockfile
- `package-lock.json` for Node lockfile
