# Reflexion — Product Requirements Document

## Must-Have Features (MVP)

### 1. Self-Improving Agent Core
- ADK-based agent with Gemini 3
- Executes tasks (Q&A, research, analysis)
- Traces all execution via Arize Phoenix (OpenTelemetry)
- After each task: analyzes traces, identifies weaknesses, generates improvements
- Applies improvements to next execution

### 2. Arize Phoenix Integration
- Auto-instrumentation via OpenInference
- All LLM calls, tool calls, and agent reasoning traced
- Traces visible in Phoenix Cloud dashboard
- MCP server configured for runtime self-introspection

### 3. Self-Introspection via MCP
- Agent queries its own traces via Phoenix MCP at runtime
- Identifies: slow tool calls, low-quality responses, token waste
- Generates targeted improvement suggestions
- Applies improvements with before/after comparison

### 4. Improvement Dashboard (Web UI)
- Real-time improvement metrics
- Session history with trace links
- Improvement timeline (what changed, when, impact)
- Quality score trend chart
- Live agent interaction interface

### 5. Evaluation Pipeline
- LLM-as-a-Judge scoring on each response
- Criteria: accuracy, helpfulness, completeness, efficiency
- Scores stored and tracked over time
- Improvement validation (did changes actually help?)

## Nice-to-Have Features

### 6. Multi-Domain Agent
- Multiple task domains: research, coding, analysis
- Domain-specific improvement strategies
- Cross-domain learning transfer

### 7. Improvement History Visualization
- Before/after comparison for each improvement
- Impact analysis (which improvements helped most)
- Regression detection (improvements that made things worse)

### 8. Export/Share
- Export improvement report as PDF
- Share agent improvement journey
- Public improvement leaderboard

## Features We Will NOT Build (Time Constraint)
- User authentication (use demo mode)
- Multi-user support
- Production deployment infrastructure
- Mobile app
- Custom model training

## Success Metrics
- Agent quality score improves by 20%+ over 10 sessions
- At least 5 distinct improvement types demonstrated
- Dashboard shows clear improvement trend
- Demo video tells compelling improvement story
