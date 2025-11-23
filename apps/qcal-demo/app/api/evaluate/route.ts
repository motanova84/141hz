import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { text } = await request.json()
    
    if (!text || typeof text !== 'string') {
      return NextResponse.json(
        { error: 'Invalid text input' },
        { status: 400 }
      )
    }
    
    // Calculate Ψ (Psi) metric based on QCAL framework
    const psi = calculatePsi(text)
    const coherence = calculateCoherence(text)
    
    return NextResponse.json({
      psi,
      coherence,
      timestamp: new Date().toISOString(),
    })
  } catch (error) {
    console.error('Error evaluating text:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

function calculatePsi(text: string): number {
  // QCAL framework: Ψ = I × A²_eff
  // I: Information content
  // A_eff: Effective symbolic amplitude
  
  const I = calculateInformationContent(text)
  const A_eff = calculateSymbolicAmplitude(text)
  
  const psi = I * (A_eff ** 2)
  
  // Normalize to 0-10 scale
  return Math.min(Math.max(psi, 0), 10)
}

function calculateInformationContent(text: string): number {
  // Check for key QCAL symbols and concepts
  const keywords = [
    '141.7', '141.7001', 'f₀', 'f0',
    'Ψ', 'psi', 'φ³', 'phi',
    "ζ'", 'zeta', 'riemann',
    'coherence', 'coherencia',
    'quantum', 'cuántico', 'cuantico',
    'Hz', 'frequency', 'frecuencia',
    'GW150914', 'LIGO',
    'noetic', 'noésic', 'consciousness'
  ]
  
  let score = 0
  const lowerText = text.toLowerCase()
  
  // Count keyword occurrences
  for (const keyword of keywords) {
    if (lowerText.includes(keyword.toLowerCase())) {
      score += 0.5
    }
  }
  
  // Check for numerical precision (presence of decimal values)
  const decimalPattern = /\b\d+\.\d{2,}\b/g
  const decimals = text.match(decimalPattern)
  if (decimals) {
    score += Math.min(decimals.length * 0.3, 2.0)
  }
  
  // Check for mathematical formulas (presence of =, ×, ^, etc.)
  const mathSymbols = ['=', '×', '^', '∞', '∑', '∫', '∂']
  for (const symbol of mathSymbols) {
    if (text.includes(symbol)) {
      score += 0.2
    }
  }
  
  // Reward longer, more detailed content
  const wordCount = text.split(/\s+/).length
  score += Math.min(wordCount / 100, 2)
  
  return score
}

function calculateSymbolicAmplitude(text: string): number {
  // Measure the density of QCAL-aligned concepts
  const specificTerms = [
    '141.7001 Hz',
    'f₀ = 141.7001',
    'Ψ = I × A²',
    'quantum coherence',
    'universal frequency',
    'gravitational wave',
    'ringdown',
    'QCAL'
  ]
  
  let amplitude = 1.0
  const lowerText = text.toLowerCase()
  
  for (const term of specificTerms) {
    if (lowerText.includes(term.toLowerCase())) {
      amplitude += 0.4
    }
  }
  
  // Check for scientific notation (with length limit to prevent ReDoS)
  if (text.length < 10000 && /\d{1,10}\.?\d{0,10}\s*[eE][+-]?\d{1,5}/.test(text)) {
    amplitude += 0.3
  }
  
  // Check for references to validated sources
  if (lowerText.includes('zenodo') || lowerText.includes('doi') || lowerText.includes('orcid')) {
    amplitude += 0.5
  }
  
  return amplitude
}

function calculateCoherence(text: string): number {
  // Coherence is a normalized measure of alignment with QCAL
  const psi = calculatePsi(text)
  return Math.min(psi / 10, 1.0)
}
