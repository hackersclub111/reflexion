'use client';

import { useState } from 'react';

interface AgentChatProps {
  mode: 'demo' | 'live';
}

const DEMO_RESPONSES = [
  {
    query: 'What are the latest trends in AI agents?',
    response: `Five key trends are reshaping AI agents in 2026:

**1. Multi-Agent Orchestration**: Systems like Google's A2A protocol enable agents to collaborate, with each agent specializing in sub-tasks. Companies like CrewAI and AutoGen report 3x productivity gains.

**2. Self-Improving Agents**: Agents that analyze their own execution traces (via tools like Arize Phoenix) and autonomously refine their strategies. Research shows 20-40% quality improvement over 10 iterations.

**3. MCP-Powered Tool Use**: The Model Context Protocol has become the standard for agent-tool interaction, with 500+ MCP servers now available across GitHub, Slack, databases, and more.

**4. Production Observability**: Tools like Arize Phoenix provide OpenTelemetry-based tracing for agent reasoning, enabling debugging of complex multi-step workflows.

**5. Agentic RAG**: Agents that don't just retrieve documents but reason over them, synthesize across sources, and cite specific passages.`,
    quality: 0.87,
    improvement: 'Applied: Add specificity constraint with examples and statistics',
  },
];

export function AgentChat({ mode }: AgentChatProps) {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Array<{ role: string; content: string; quality?: number; improvement?: string }>>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMsg = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMsg]);
    setQuery('');
    setLoading(true);

    if (mode === 'demo') {
      // Simulate delay
      await new Promise((r) => setTimeout(r, 1500));
      const demo = DEMO_RESPONSES[0];
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: demo.response,
          quality: demo.quality,
          improvement: demo.improvement,
        },
      ]);
    } else {
      try {
        const res = await fetch('/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query }),
        });
        const data = await res.json();
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: data.response,
            quality: data.quality_score,
            improvement: data.improvement?.description,
          },
        ]);
      } catch {
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: 'Error: Could not reach the agent server.' },
        ]);
      }
    }
    setLoading(false);
  };

  return (
    <div className="glass rounded-xl p-6">
      <h2 className="text-lg font-semibold text-slate-800 mb-1">Try Reflexion</h2>
      <p className="text-sm text-slate-500 mb-6">Ask a question and watch the agent self-improve</p>

      {/* Messages */}
      <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl rounded-xl px-4 py-3 ${
              msg.role === 'user'
                ? 'bg-sky-500 text-white'
                : 'bg-white border border-slate-200'
            }`}>
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              {msg.quality && (
                <div className="mt-3 pt-3 border-t border-slate-100 flex items-center gap-4 text-xs">
                  <span className="text-slate-500">Quality: <span className="font-medium text-sky-600">{msg.quality.toFixed(2)}</span></span>
                  {msg.improvement && (
                    <span className="text-green-600">Improved: {msg.improvement}</span>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 rounded-xl px-4 py-3">
              <div className="flex items-center gap-2 text-sm text-slate-500">
                <div className="w-2 h-2 bg-sky-500 rounded-full animate-pulse"></div>
                Reflexion is thinking...
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask Reflexion anything..."
          className="flex-1 px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 bg-sky-500 text-white rounded-xl font-medium hover:bg-sky-600 transition disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
