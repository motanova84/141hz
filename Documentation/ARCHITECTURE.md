# QC-LLM Architecture Documentation

## Overview

This document describes the modular architecture implemented for establishing 141Hz as a global standard for Quantum Coherence in Language Models (QC-LLM).

## Architecture Phases

### PHASE 1: Modular Architecture ✅ IMPLEMENTED

The project follows a layered architecture pattern:

```
141hz/
├── Core/                      # Mathematical Foundation (Lean 4)
├── API/                       # Public Interfaces
├── Applications/              # Practical Applications  
├── Benchmarks/               # Validation Infrastructure
├── Documentation/            # Comprehensive Docs
├── Tools/                    # Development Tools
├── Examples/                 # Integration Examples
└── Web/                      # Web Interface (future)
```

## Core Modules

### 1. Core/ - Mathematical Foundation

Formal verification in Lean 4:

- **FrequencyDerivation/**
  - `ZetaConnection.lean` - Riemann zeta function ζ'(1/2)
  - `GoldenRatio.lean` - Golden ratio φ and properties
  - `SqrtTwo.lean` - √2 properties and proofs
  - `Main.lean` - Main theorem: f₀ = 141.7001 Hz

- **DimensionalAnalysis/**
  - `PhysicalDimensions.lean` - Physical units and dimensions
  - `RiccatiCorrection.lean` - Dimensional corrections
  - `Consistency.lean` - Dimensional consistency proofs

- **PrimeDistribution/**
  - `Convergence.lean` - Prime series convergence
  - `SpectralEmergence.lean` - Frequency emergence from primes

**Status:** ✅ Core modules implemented with formal proofs

## API Layer

### 2. API/ - Public Interfaces

Three API implementations:

#### REST API (FastAPI)
- **Location:** `API/REST/`
- **Files:** 
  - `main.py` - Original API server
  - `frequency_validator.py` - Enhanced frequency validator
- **Endpoints:**
  - `POST /validate` - Validate text coherence
  - `GET /frequency` - Get f₀ constant
  - `GET /health` - Health check

#### Python Package
- **Location:** `API/Python/qc_llm/`
- **Modules:**
  - `__init__.py` - Main QC_LLM class
  - `validator.py` - CoherenceValidator
  - `metrics.py` - Core metric computations
- **Installation:** `pip install -e API/Python`

#### JavaScript Package
- **Location:** `API/JavaScript/qc-llm-js/`
- **Files:**
  - `src/validator.ts` - TypeScript validator
  - `src/index.ts` - Package entry point
  - `package.json` - NPM configuration
- **Installation:** `npm install qc-llm-js` (after publishing)

**Status:** ✅ All three APIs implemented

## Applications Layer

### 3. Applications/ - Practical Use Cases

#### LLM Applications
- **Location:** `Applications/LLM/`
- **Modules:**
  - `CoherenceMetric.py` - Coherence measurement for LLM evaluation
  - `QuantumAlignment.py` - Text alignment with f₀
  - `RealTimeMonitor.py` - Streaming coherence monitoring

**Usage Example:**
```python
from CoherenceMetric import CoherenceMetric

metric = CoherenceMetric()
score = metric.measure("LLM output text")
print(f"Coherence: {score:.2%}")
```

#### Physics Applications (Planned)
- Navier-Stokes connections
- Fluid dynamics analysis
- Quantum field applications

#### Neuroscience Applications (Planned)
- EEG analysis
- Brain coherence measurement
- Neural synchronization

**Status:** ✅ LLM applications implemented

## Benchmarking Infrastructure

### 4. Benchmarks/ - Validation Framework

#### LLM Comparison
- **Location:** `Benchmarks/LLMComparison/`
- **Module:** `benchmark.py`
- **Features:**
  - Compare multiple LLMs (GPT-4, Claude, etc.)
  - Generate leaderboards
  - Statistical analysis

**Usage:**
```python
from benchmark import LLMBenchmark

benchmark = LLMBenchmark()
results = benchmark.run_benchmark({
    "GPT-4": gpt4_responses,
    "Claude-3.5": claude_responses
})
```

#### Physics Validation (Planned)
- Navier-Stokes validation
- Physical model testing

#### Results Storage
- **Location:** `Benchmarks/Results/`
- **Files:**
  - `metrics.json` - Project metrics
  - `badges.md` - Status badges
  - `leaderboard.md` - LLM leaderboard

**Status:** ✅ Benchmark infrastructure implemented

## Tools & Automation

### 5. Tools/ - Development Tools

#### Validators
- **Location:** `Tools/Validators/`
- **Scripts:**
  - `validate_lean.sh` - Validate Lean 4 formalization
  - `validate_coherence.py` - Test coherence implementation

**Run tests:**
```bash
python3 Tools/Validators/validate_coherence.py
```

#### Generators
- **Location:** `Tools/Generators/`
- **Scripts:**
  - `generate_badges.py` - Generate status badges
  - `generate_metrics.py` - Generate project metrics

**Generate metrics:**
```bash
python3 Tools/Generators/generate_metrics.py
```

#### CI Tools (Planned)
- Automated testing
- Deployment automation
- Quality gates

**Status:** ✅ Core tools implemented

## Examples & Documentation

### 6. Examples/ - Integration Examples

#### LLM Integration
- **Location:** `Examples/LLM_Integration/`
- **Files:**
  - `openai_example.py` - OpenAI integration pattern
  - More examples planned...

#### Real-Time Applications
- **Location:** `Examples/RealTime/`
- **Files:**
  - `streaming_monitor.py` - Streaming coherence monitor

**Status:** ✅ Basic examples implemented

### 7. Documentation/ - Comprehensive Guides

#### Tutorials
- **Location:** `Documentation/Tutorials/`
- **Guides:**
  - `01_getting_started.md` - Quick start guide
  - More tutorials planned...

#### Theory
- **Location:** `Documentation/Theory/`
- Mathematical foundations (planned)
- Physical interpretations (planned)

#### API Documentation
- **Location:** `Documentation/API/`
- Python API docs (planned)
- JavaScript API docs (planned)
- REST API specs (planned)

**Status:** ✅ Basic documentation structure

## Future Phases (from Problem Statement)

### PHASE 2: API Public (Weeks 3-4)
- ✅ REST API implemented
- ✅ Python package implemented
- ✅ JavaScript package implemented
- 🔄 Public deployment pending

### PHASE 3: LLM Integration (Weeks 5-6)
- ✅ OpenAI integration example
- 🔄 Anthropic integration (planned)
- 🔄 Hugging Face integration (planned)

### PHASE 4: Benchmarks & Leaderboard (Weeks 7-8)
- ✅ Benchmark infrastructure
- 🔄 Multi-LLM comparison (needs API keys)
- 🔄 Public leaderboard deployment

## Key Features

### Fundamental Constant
```
f₀ = 141.7001 Hz

Derivation:
  f₀ = √2 × f_ref
  where f_ref = k × |ζ'(1/2)| × φ³
  k ≈ 16.195 (dimensional scale factor)
```

### Coherence Metric
The coherence score combines:
- **Frequency Alignment** (60%): Spectral alignment with f₀
- **Quantum Entropy** (40%): Token diversity and distribution

Range: [0, 1] where:
- > 0.8 = HIGH COHERENCE
- 0.6-0.8 = MODERATE COHERENCE
- 0.4-0.6 = LOW COHERENCE
- < 0.4 = VERY LOW COHERENCE

## Technology Stack

- **Formal Verification:** Lean 4
- **Backend API:** FastAPI (Python)
- **Python Package:** Pure Python 3.8+
- **JavaScript Package:** TypeScript/ES2020
- **Testing:** pytest, jest
- **CI/CD:** GitHub Actions
- **Documentation:** Markdown

## Installation & Usage

### Quick Start

```bash
# Install dependencies
pip install numpy scipy fastapi pydantic uvicorn

# Test Python API
python3 -c "
import sys
sys.path.insert(0, 'API/Python')
from qc_llm import QC_LLM
v = QC_LLM()
print(v.validate('Test text')['coherence'])
"

# Run validators
python3 Tools/Validators/validate_coherence.py

# Generate metrics
python3 Tools/Generators/generate_metrics.py
```

### API Server

```bash
cd API/REST
python3 frequency_validator.py
# Server runs on http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Contributing

See main CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file

## References

- **DOI:** 10.5281/zenodo.17379721
- **Repository:** https://github.com/motanova84/141hz
- **Author:** José Manuel Mota Burruezo (JMMB Ψ ✧ ∞³)
