'use client';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

interface QualityChartProps {
  trend: Array<{
    trace_id: string;
    quality_score: number;
    latency_ms: number;
    total_tokens: number;
    session_id: string;
  }>;
}

export function QualityChart({ trend }: QualityChartProps) {
  const data = trend.map((t, i) => ({
    name: `Trace ${i + 1}`,
    score: t.quality_score,
    latency: t.latency_ms / 1000,
    session: t.session_id,
  }));

  return (
    <div className="glass rounded-xl p-6">
      <h2 className="text-lg font-semibold text-slate-800 mb-1">Quality Score Trend</h2>
      <p className="text-sm text-slate-500 mb-6">How the agent improved over time</p>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
          <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
          <YAxis domain={[0, 1]} stroke="#94a3b8" fontSize={12} />
          <Tooltip
            contentStyle={{
              background: 'rgba(255,255,255,0.95)',
              border: '1px solid #e2e8f0',
              borderRadius: '8px',
            }}
          />
          <ReferenceLine y={0.6} stroke="#f59e0b" strokeDasharray="5 5" label="Target" />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#0ea5e9"
            strokeWidth={3}
            dot={{ fill: '#0ea5e9', strokeWidth: 2, r: 6 }}
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>

      <div className="mt-4 flex items-center gap-4 text-sm text-slate-500">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-sky-500"></div>
          Quality Score
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-0.5 bg-amber-500 border-dashed"></div>
          Target (0.6)
        </div>
      </div>
    </div>
  );
}
