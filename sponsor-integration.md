# Reflexion — Sponsor Integration Plan

## Primary Sponsor: Arize (Phoenix)

### Integration 1: Auto-Instrumentation (Foundation)
- **What**: OpenTelemetry tracing via OpenInference instrumentors
- **How**: `phoenix.otel.register(project_name="reflexion", auto_instrument=True)`
- **Visibility**: Every trace visible in Phoenix Cloud dashboard
- **Demo**: Show live traces appearing in Phoenix during agent execution

### Integration 2: Phoenix MCP Server (Core Differentiator)
- **What**: Runtime self-introspection via MCP protocol
- **How**: Configure `@arizeai/phoenix-mcp` in agent's MCP settings
- **Visibility**: Agent queries its own traces during execution
- **Demo**: Agent says "Let me check my recent performance..." and queries Phoenix

### Integration 3: LLM-as-a-Judge Evaluations (Quality Tracking)
- **What**: Automated quality scoring on every response
- **How**: Phoenix evaluation pipeline with custom criteria
- **Visibility**: Quality scores displayed on dashboard
- **Demo**: Show before/after scores when improvement is applied

### Integration 4: Trace Analysis for Self-Improvement (Intelligence)
- **What**: Agent analyzes its own traces to generate improvements
- **How**: Agent queries Phoenix MCP for recent traces, identifies patterns
- **Visibility**: Improvement suggestions shown in dashboard
- **Demo**: Agent identifies a slow tool call and optimizes its strategy

## Secondary Sponsor: Google Cloud

### Integration 5: Gemini 3 (Brain)
- **What**: Core LLM for reasoning and task execution
- **How**: Google ADK with Gemini 3 model
- **Visibility**: All agent responses powered by Gemini
- **Demo**: Show agent reasoning process

### Integration 6: Google Cloud Agent Builder (Platform)
- **What**: Agent orchestration and deployment
- **How**: Agent Builder for tool management and deployment
- **Visibility**: Hosted agent accessible via web
- **Demo**: Live agent interaction during demo

### Integration 7: Cloud Run (Hosting)
- **What**: Deploy agent and dashboard
- **How**: Docker container on Cloud Run
- **Visibility**: Public URL for judges to test
- **Demo**: Navigate to live URL during demo

## Integration Depth Strategy
- **Shallow (visible)**: Phoenix Cloud dashboard with live traces
- **Medium (functional)**: MCP-powered self-introspection
- **Deep (impressive)**: Self-improvement loop using trace analysis

## Fallback Strategy
- If Phoenix Cloud is down: use local Phoenix instance
- If MCP is slow: cache recent traces locally
- If Cloud Run fails: deploy to Vercel/Netlify as backup
- If Gemini API is slow: implement retry with exponential backoff

## Sponsor Badge Placement
- README: Arize Phoenix badge + Google Cloud badge
- Dashboard: "Powered by Arize Phoenix" footer
- Demo video: Arize + Google Cloud logos in intro/outro
- Devpost: Arize + Google Cloud in "Built With" tags
