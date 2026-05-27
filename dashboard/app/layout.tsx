import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Reflexion — Self-Improving Agent',
  description: 'A self-improving AI agent powered by Gemini 3 and Arize Phoenix',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen">{children}</body>
    </html>
  );
}
