'use client';

import { useState, useEffect } from 'react';
import { QualityChart } from '@/components/QualityChart';
import { ImprovementTimeline } from '@/components/ImprovementTimeline';
import { StatsCards } from '@/components/StatsCards';
import { AgentChat } from '@/components/AgentChat';

const DEMO_DATA = {
  summary: {
    total_sessions: 2,
    total_traces: 4,
    total_improvements: 1,
    min_score: 0.45,
    max_score: 0.91,
    avg_score: 0.6875,
    improvement_delta: 0.46,
    improvement_percent: 102.2,
  },
  trend: [
    { trace_id: 'trace_1_1', quality_score: 0.45, latency_ms: 2300, total_tokens: 1250, session_id: 'Session 1' },
    { trace_id: 'trace_1_2', quality_score: 0.52, latency_ms: 1800, total_tokens: 890, session_id: 'Session 1' },
    { trace_id: 'trace_2_1', quality_score: 0.87, latency_ms: 950, total_tokens: 2100, session_id: 'Session 2' },
    { trace_id: 'trace_2_2', quality_score: 0.91, latency_ms: 1100, total_tokens: 2800, session_id: 'Session 2' },
  ],
  improvements: [
    {
      id: 'imp_1_1',
      type: 'prompt_refinement',
      description: 'Add specificity constraint: include examples, statistics, and named entities',
      before_score: 0.45,
      after_score: 0.87,
      applied: true,
      created_at: '2026-05-27T10:05:00',
    },
  ],
};

export default function Dashboard() {
  const [data, setData] = useState(DEMO_DATA);
  const [mode, setMode] = useState<'demo' | 'live'>('demo');

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="glass sticky top-0 z-50 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold gradient-text">Reflexion</h1>
            <p className="text-sm text-slate-500">Self-Improving Agent Dashboard</p>
          </div>
          <div className="flex items-center gap-4">
            <span className={`px-3 py-1 rounded-full text-xs font-medium ${
              mode === 'demo' ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700'
            }`}>
              {mode === 'demo' ? 'DEMO MODE' : 'LIVE MODE'}
            </span>
            <button
              onClick={() => setMode(mode === 'demo' ? 'live' : 'demo')}
              className="px-4 py-2 text-sm bg-white rounded-lg shadow-sm border hover:bg-slate-50 transition"
            >
              Switch to {mode === 'demo' ? 'Live' : 'Demo'}
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats Cards */}
        <StatsCards summary={data.summary} />

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
          {/* Quality Chart — 2 cols */}
          <div className="lg:col-span-2">
            <QualityChart trend={data.trend} />
          </div>

          {/* Improvement Timeline — 1 col */}
          <div className="lg:col-span-1">
            <ImprovementTimeline improvements={data.improvements} />
          </div>
        </div>

        {/* Agent Chat */}
        <div className="mt-8">
          <AgentChat mode={mode} />
        </div>

        {/* Sponsor Badges */}
        <div className="mt-12 text-center">
          <p className="text-sm text-slate-400 mb-4">Powered by</p>
          <div className="flex items-center justify-center gap-8">
            <div className="flex items-center gap-2 text-slate-600">
              <span className="text-lg font-semibold">Gemini 3</span>
            </div>
            <div className="flex items-center gap-2 text-slate-600">
              <span className="text-lg font-semibold">Google Cloud</span>
            </div>
            <div className="flex items-center gap-2 text-slate-600">
              <span className="text-lg font-semibold">Arize Phoenix</span>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
