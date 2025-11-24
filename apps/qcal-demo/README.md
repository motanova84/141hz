# QCAL-LLM ∞³ - Quantum Coherence Evaluator

A Next.js application that evaluates AI-generated text for quantum coherence with the universal frequency f₀ = 141.7001 Hz using the QCAL (Quantum Coherence Analysis Language) framework.

## Features

### 🌊 3D Visualization
- 5000-particle quantum field visualization using Three.js
- Resonant torus representing f₀ frequency
- Real-time rotation based on 141.7001 Hz
- Dynamic pulsing with Ψ metric values

### 🎵 Binaural Audio System
- 141.7 Hz left channel
- 148.7 Hz right channel (7 Hz theta wave beat)
- 30-second auto-stop timer
- Immersive quantum frequency experience

### ✨ Advanced Animations
- Matrix rain effect with quantum symbols
- Glassmorphism UI with backdrop blur
- Smooth Ψ value reveal animation
- Spring transitions and color-coded feedback
- Responsive gradient effects

### 📊 Real-Time Evaluation
- API-based text analysis
- QCAL framework metrics (Ψ = I × A²_eff)
- Coherence threshold validation (Ψ ≥ 5.0)
- Progress bars and visual feedback
- Shareable results

## Installation

```bash
cd apps/qcal-demo
npm install
```

## Dependencies

The application requires:
- Next.js 14
- React 18
- TypeScript 5
- Framer Motion 11 (animations)
- Three.js 0.161 (3D graphics)
- Tailwind CSS 3 (styling)

All dependencies are included in `package.json`.

## Development

Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## Building

Build for production:

```bash
npm run build
npm start
```

## Deployment

### Vercel (Recommended)

```bash
cd apps/qcal-demo
vercel --prod
```

The application is optimized for Vercel deployment with:
- Standalone output mode
- Automatic API routes
- Edge runtime support

### Environment Variables

No environment variables are required for basic operation.

## Usage

1. **Enter Text**: Paste AI-generated text into the textarea
2. **Evaluate**: Click "🌌 Evaluate Coherence" to analyze the text
3. **View Results**: See Ψ metric, coherence score, and interpretation
4. **Play Audio**: Click 🎵 to experience 141.7 Hz binaural frequency
5. **Share**: Copy results to clipboard with the share button

## QCAL Framework

The evaluation algorithm measures:

### Information Content (I)
- Presence of QCAL keywords (f₀, Ψ, φ³, ζ', etc.)
- Numerical precision (decimal values)
- Mathematical formulas (=, ×, ^, ∞)
- Content depth (word count)

### Symbolic Amplitude (A_eff)
- Specific QCAL terms (141.7001 Hz, quantum coherence)
- Scientific notation
- Validated sources (Zenodo, DOI, ORCID)

### Ψ Metric
```
Ψ = I × A²_eff
```
Normalized to 0-10 scale, with threshold at Ψ ≥ 5.0 for coherent responses.

## Technical Details

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript with strict mode
- **Styling**: Tailwind CSS with custom theme
- **Animations**: Framer Motion for smooth transitions
- **3D Graphics**: Three.js WebGL renderer
- **Audio**: Web Audio API with stereo channel merger
- **API**: Next.js API routes with JSON responses

## Performance

- Optimized 3D rendering with requestAnimationFrame
- Efficient particle system (5000 particles)
- Lazy loading and code splitting
- Responsive design for all screen sizes

## Browser Support

- Chrome/Edge (recommended for best 3D performance)
- Firefox
- Safari
- All modern browsers with WebGL and Web Audio API support

## Credits

**Author**: José Manuel Mota Burruezo (JMMB Ψ ✧ ∞³)

**Links**:
- [GitHub](https://github.com/motanova84/noesis88)
- [ORCID](https://orcid.org/0009-0002-1923-0773)
- [Zenodo Publications](https://zenodo.org/search?q=MOTA%20BURRUEZO)

**Framework**: QCAL (Quantum Coherence Analysis Language) ∞³

## License

See main repository LICENSE file.
