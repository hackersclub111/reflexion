# Reflexion — Database Schema

## Tables

### `sessions`
Tracks each agent interaction session.

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | UUID session identifier |
| created_at | TIMESTAMP | Session start time |
| task_description | TEXT | What the agent was asked to do |
| status | TEXT | 'running', 'completed', 'failed' |
| total_duration_ms | INTEGER | Total session duration |
| improvement_count | INTEGER | Number of improvements applied |

### `traces`
Stores Phoenix trace references for each session.

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | UUID trace identifier |
| session_id | TEXT FK | References sessions.id |
| trace_id | TEXT | Phoenix trace ID |
| span_count | INTEGER | Number of spans in trace |
| total_tokens | INTEGER | Total tokens used |
| latency_ms | INTEGER | End-to-end latency |
| quality_score | FLOAT | LLM-as-a-Judge score (0-1) |

### `improvements`
Tracks self-improvement events.

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | UUID improvement identifier |
| session_id | TEXT FK | References sessions.id |
| created_at | TIMESTAMP | When improvement was generated |
| type | TEXT | 'prompt_refinement', 'tool_strategy', 'parameter_tuning' |
| description | TEXT | Human-readable description |
| before_score | FLOAT | Quality score before improvement |
| after_score | FLOAT | Quality score after improvement |
| applied | BOOLEAN | Whether improvement was applied |

### `evaluations`
Stores evaluation results from LLM-as-a-Judge.

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | UUID evaluation identifier |
| trace_id | TEXT FK | References traces.id |
| criterion | TEXT | What was evaluated |
| score | FLOAT | Score (0-1) |
| reasoning | TEXT | LLM's reasoning for the score |
| created_at | TIMESTAMP | When evaluation was run |

### `improvement_log`
Audit trail of all changes made to the agent.

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT PK | UUID log identifier |
| improvement_id | TEXT FK | References improvements.id |
| action | TEXT | What changed |
| old_value | TEXT | Previous value |
| new_value | TEXT | New value |
| created_at | TIMESTAMP | When change was applied |

## Relationships
- sessions 1:N traces (one session has many traces)
- sessions 1:N improvements (one session generates many improvements)
- traces 1:N evaluations (one trace has many evaluations)
- improvements 1:N improvement_log (one improvement has many log entries)
