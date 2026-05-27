'use client';

interface ImprovementTimelineProps {
  improvements: Array<{
    id: string;
    type: string;
    description: string;
    before_score: number;
    after_score: number;
    applied: boolean;
    created_at: string;
  }>;
}

export function ImprovementTimeline({ improvements }: ImprovementTimelineProps) {
  return (
    <div className="glass rounded-xl p-6 h-full">
      <h2 className="text-lg font-semibold text-slate-800 mb-1">Improvement Timeline</h2>
      <p className="text-sm text-slate-500 mb-6">Self-generated improvements</p>

      <div className="space-y-4">
        {improvements.map((imp, i) => (
          <div key={imp.id} className="relative pl-6">
            {/* Timeline line */}
            {i < improvements.length - 1 && (
              <div className="absolute left-2 top-8 bottom-0 w-0.5 bg-slate-200"></div>
            )}
            {/* Dot */}
            <div className={`absolute left-0 top-2 w-4 h-4 rounded-full border-2 ${
              imp.applied ? 'bg-green-500 border-green-300' : 'bg-amber-500 border-amber-300'
            }`}></div>

            <div className="bg-white rounded-lg p-4 shadow-sm border border-slate-100">
              <div className="flex items-center gap-2 mb-2">
                <span className="px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs font-medium">
                  {imp.type.replace('_', ' ')}
                </span>
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                  imp.applied ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'
                }`}>
                  {imp.applied ? 'Applied' : 'Pending'}
                </span>
              </div>

              <p className="text-sm text-slate-700 mb-3">{imp.description}</p>

              <div className="flex items-center gap-4 text-xs">
                <div>
                  <span className="text-slate-400">Before:</span>
                  <span className="ml-1 font-medium text-red-600">{imp.before_score.toFixed(2)}</span>
                </div>
                <div className="text-slate-300">→</div>
                <div>
                  <span className="text-slate-400">After:</span>
                  <span className="ml-1 font-medium text-green-600">{imp.after_score.toFixed(2)}</span>
                </div>
                <div className="ml-auto">
                  <span className="text-green-600 font-medium">
                    +{((imp.after_score - imp.before_score) / imp.before_score * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}

        {improvements.length === 0 && (
          <div className="text-center text-slate-400 py-8">
            <p>No improvements yet.</p>
            <p className="text-sm mt-1">The agent will generate improvements as it runs.</p>
          </div>
        )}
      </div>
    </div>
  );
}
