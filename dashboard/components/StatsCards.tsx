'use client';

interface StatsCardsProps {
  summary: {
    total_sessions: number;
    total_traces: number;
    total_improvements: number;
    min_score: number;
    max_score: number;
    avg_score: number;
    improvement_delta: number;
    improvement_percent: number;
  };
}

export function StatsCards({ summary }: StatsCardsProps) {
  const cards = [
    {
      label: 'Quality Improvement',
      value: `+${summary.improvement_percent}%`,
      sub: `${summary.min_score.toFixed(2)} → ${summary.max_score.toFixed(2)}`,
      color: 'text-green-600',
      bg: 'bg-green-50',
    },
    {
      label: 'Sessions',
      value: summary.total_sessions,
      sub: `${summary.total_traces} total traces`,
      color: 'text-blue-600',
      bg: 'bg-blue-50',
    },
    {
      label: 'Improvements Applied',
      value: summary.total_improvements,
      sub: 'Self-generated',
      color: 'text-purple-600',
      bg: 'bg-purple-50',
    },
    {
      label: 'Average Score',
      value: summary.avg_score.toFixed(2),
      sub: 'Across all traces',
      color: 'text-amber-600',
      bg: 'bg-amber-50',
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <div key={card.label} className={`${card.bg} rounded-xl p-5 border border-white/50`}>
          <p className="text-sm text-slate-500 mb-1">{card.label}</p>
          <p className={`text-3xl font-bold ${card.color}`}>{card.value}</p>
          <p className="text-xs text-slate-400 mt-1">{card.sub}</p>
        </div>
      ))}
    </div>
  );
}
