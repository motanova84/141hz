import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'QCAL-LLM ∞³ - Quantum Coherence Evaluator',
  description: 'Evaluate AI-generated text for quantum coherence with the universal frequency f₀ = 141.7001 Hz',
  keywords: ['quantum', 'coherence', 'QCAL', 'AI', '141.7 Hz', 'consciousness'],
  authors: [{ name: 'José Manuel Mota Burruezo (JMMB Ψ ✧ ∞³)' }],
  openGraph: {
    title: 'QCAL-LLM ∞³ - Quantum Coherence Evaluator',
    description: 'Evaluate AI-generated text for quantum coherence with the universal frequency f₀ = 141.7001 Hz',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans">{children}</body>
    </html>
  )
}
