# Reflexion — Cursor Rules / Gemini Context

## Project Philosophy
- Build the IMPRESSIVE thing first, optimize later
- Every feature must be visible in the demo
- Mock before logic — if the UI can't show it, it doesn't matter yet
- Keep compilation errors at zero at all times
- Write tests alongside code, not after

## Coding Standards
- Python: type hints, docstrings, async/await
- TypeScript: strict mode, no `any` types
- Error handling: graceful degradation, never crash
- Naming: descriptive, no abbreviations

## Architecture Decisions
- ADK for agent logic (not LangChain)
- Phoenix for observability (not custom logging)
- SQLite for local state (no external DB needed)
- Next.js for dashboard (fast, good DX)
- Tailwind for styling (rapid iteration)

## What NOT to Do
- Don't use competing AI services (OpenAI, AWS Bedrock) — hackathon rules
- Don't over-engineer — this is a hackathon, not production
- Don't add features that aren't visible in the demo
- Don't skip error handling for demo-critical paths
- Don't use placeholder/mock data that looks fake

## Demo Requirements
- Must work offline (demo mode with pre-recorded traces)
- Must show improvement over time (the core wow moment)
- Must be reproducible (same demo every time)
- Must highlight Arize Phoenix integration visually

## File Organization
```
Reflexion/
├── agent/              # Python ADK agent
│   ├── main.py         # Entry point
│   ├── reflexion.py    # Self-improvement logic
│   ├── tools.py        # Agent tools
│   └── evaluation.py   # LLM-as-a-Judge
├── dashboard/          # Next.js frontend
│   ├── app/            # App router pages
│   ├── components/     # React components
│   └── lib/            # Utilities
├── data/               # SQLite DB, demo data
├── docs/               # Documentation
└── screenshots/        # Demo screenshots
```
