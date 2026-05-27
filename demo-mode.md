# Reflexion — Demo Mode Strategy

## Purpose
Ensure the demo NEVER fails, even if APIs are down or slow.

## Demo Mode Toggle
- **Live Mode**: Real Gemini API, real Phoenix traces, real improvements
- **Demo Mode**: Pre-recorded traces, deterministic responses, offline-capable

## Pre-Recorded Demo Data

### Session 1: "The Failure"
- Task: "Research the latest trends in AI agents"
- Agent response: Generic, shallow, missing key trends
- Quality score: 0.45
- Trace: Shows 3 tool calls, 2 failed, 1 slow (2.3s)

### Session 2: "The Reflection"
- Agent analyzes Session 1 trace via MCP
- Identifies: "My research tool calls are too broad"
- Generates improvement: "Use more specific search queries"
- Shows improvement being applied

### Session 3: "The Success"
- Task: "Research the latest trends in AI agents" (same task)
- Agent response: Detailed, specific, covers all trends
- Quality score: 0.87
- Trace: Shows 5 tool calls, all successful, fast (0.8s avg)
- Improvement: +93% quality, -65% latency

### Session 4: "The Dashboard"
- Show quality trend chart: 0.45 → 0.87
- Show improvement timeline: 1 improvement applied
- Show trace comparison: before vs after
- Show real-time improvement metrics

## Mock Data Strategy
- Store demo traces in `data/demo/` as JSON
- Phoenix MCP queries return cached data in demo mode
- LLM responses are pre-scripted but appear natural
- All timing is realistic (not instant)

## UI Indicators
- Demo mode banner: "DEMO MODE — Pre-recorded data"
- Live mode banner: "LIVE MODE — Real-time agent"
- Toggle button in dashboard header
- Demo mode auto-enabled when APIs are unavailable

## Reliability Checklist
- [ ] Demo works offline (no internet required)
- [ ] Demo works with slow internet (no timeouts)
- [ ] Demo is reproducible (same result every time)
- [ ] Demo highlights all sponsor integrations
- [ ] Demo tells compelling improvement story
- [ ] Demo fits in 3 minutes
- [ ] Demo has clear "wow moment"
