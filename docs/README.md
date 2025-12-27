# Documentation Directory - 141.7001 Hz Gravitational Wave Analysis

This directory contains comprehensive documentation for the 141.7001 Hz gravitational wave analysis project, including tutorials, conceptual guides, technical specifications, and validation frameworks.

## 📚 User Documentation (NEW - v2.5.0)

### Essential Guides for New Users

These documents provide complete, accessible documentation for scientists from all disciplines:

#### **[TUTORIAL_COMPLETO.md](TUTORIAL_COMPLETO.md)**
**Complete Step-by-Step Tutorial** - Start here if you're new to gravitational wave analysis

- ✅ Installation and environment setup
- ✅ Data download from GWOSC
- ✅ Running analyses (basic and advanced)
- ✅ Interpreting results (JSON and graphics)
- ✅ Troubleshooting common issues
- ✅ Next steps for different user profiles

**Target audience:** Scientists with no prior experience in gravitational wave analysis
**Time to complete:** 1-2 hours

#### **[TEORIA_CONCEPTUAL.md](TEORIA_CONCEPTUAL.md)**
**Mathematical and Physical Foundations** - Accessible explanations for all scientists

- 🔢 Mathematical foundations (primes, golden ratio, Riemann zeta)
- ⚛️ Physical interpretation (Calabi-Yau geometry, Ψ field)
- 🌌 Connection to observations (LIGO/Virgo data)
- 📊 Statistical significance and validation
- 💡 Analogies and intuitive explanations

**Target audience:** Scientists from other disciplines wanting to understand the theory
**Reading time:** 45-60 minutes

#### **[FORMATOS_SALIDA.md](FORMATOS_SALIDA.md)**
**Output Formats Reference** - Complete specification for integration

- 📋 JSON schemas (all output types documented)
- 📊 Graphics interpretation (time series, spectra, histograms)
- 🔧 Integration examples (Python, R, Julia)
- 📦 JSON Schema for validation
- 💾 Versioning and compatibility

**Target audience:** Developers and researchers integrating with external tools
**Use case:** API reference, tool development

### Quick Navigation by Purpose

**I'm new to this project →** Start with [TUTORIAL_COMPLETO.md](TUTORIAL_COMPLETO.md)

**I want to understand the theory →** Read [TEORIA_CONCEPTUAL.md](TEORIA_CONCEPTUAL.md)

**I need to integrate the outputs →** Consult [FORMATOS_SALIDA.md](FORMATOS_SALIDA.md)

**I want advanced mathematical details →** See [Pre-Registration Framework](#pre-registration-and-validation-framework-v200) below

---

## Pre-Registration and Validation Framework (v2.0.0)

### `PNP_ANTI_BARRIERS.md`
**P ≠ NP: Anti-Barriers and Treewidth Approach**

Explains why the treewidth-based approach to P ≠ NP avoids the three major barriers in complexity theory:

1. **Non-Relativization**: SILB (Separator-Information Lower Bounds) depends on graph structure, not oracle access
2. **Non-Naturality**: Predicates are sparse, structured, and not efficiently computable
3. **Non-Algebrization**: Separator topology breaks down under polynomial extensions

Includes formalization roadmap in Lean 4.

---

## Related Project Files

### Root Directory Files

- **`PREREGISTRATION.md`**: Blind pre-registration protocol v1.0
  - Predefined analysis parameters (frequency, windows, validation)
  - Success and falsification criteria
  - Timeline and investigator information

- **`analysis_plan.json`**: Complete JSON specification of analysis parameters
  - Time windows, spectral methods, detectors
  - Validation controls (off-source, time-slides, leave-one-out)
  - Statistical inference framework
  - Reproducibility parameters

- **`RELEASE_NOTES.md`**: Version history and migration guide
  - Changelog for v2.0.0
  - Breaking changes (none for this release)
  - Future roadmap

### Code Directories

- **`bayes/`**: Hierarchical Bayesian inference framework
  - `hierarchical_model.py`: Multi-event Bayesian analysis
  - Global parameter π (fraction of events with signal)
  - Bayes Factor computation
  - Posterior distributions and credible intervals

- **`controls/`**: Instrumental and environmental controls
  - `lines_exclusion.csv`: Known instrumental lines to exclude
    - Power grid harmonics (60 Hz family)
    - Violin modes (suspension resonances)
    - Calibration lines (detector-specific)

- **`notebooks/`**: Analysis notebooks
  - `antenna_pattern.ipynb`: Antenna pattern consistency checks
    - F+ and Fx computation
    - Predicted vs observed amplitude ratios
    - Astrophysical consistency validation

### Formalization Directories

- **`formalization/lean/RiemannAdelic/`**: Lean 4 formalization of Riemann Hypothesis work
  - `axiom_purge.lean`: Replacement of axioms with theorems
    - Theorem: D ≡ Ξ (Hadamard factorization, Paley-Wiener bounds)
    - Theorem: All zeros on critical line (self-adjoint operator, kernel positivity)
    - Lemma: Trivial zeros excluded (Gamma factor separation)

- **`formal/`**: Lean 4 formalization of P ≠ NP approach
  - `Treewidth/SeparatorInfo.lean`: SILB lemma
  - `Lifting/Gadgets.lean`: Gadget validity (Ramanujan expanders)
  - `LowerBounds/Circuits.lean`: Circuit lower bound theorem

### Results Directories

- **`results/offsource/`**: Off-source null distribution results
  - README.md with methodology
  - Placeholder for 10,000 window analysis per event
  - Statistical significance testing framework

---

## Documentation Standards

All documentation in this project follows these standards:

1. **Markdown formatting**: GitHub-flavored markdown with math support
2. **Reproducibility**: All parameters and methods are explicitly documented
3. **Version control**: Changes tracked via git with meaningful commit messages
4. **Cross-references**: Documents link to each other and to code
5. **Status indicators**: Clear markers for completed vs pending work

### Math Notation

Mathematical expressions use:
- Inline: `$f_0 = 141.7001$` Hz
- Display: 
  ```
  $$
  BF = \frac{P(D|H_1)}{P(D|H_0)}
  $$
  ```

### Code Blocks

Code examples include language specifiers:
```python
from hierarchical_model import bayes_factor
bf, diagnostics = bayes_factor(snr_list)
```

---

## Contributing

When adding new documentation:

1. Place in appropriate directory (`docs/`, root, or with related code)
2. Update this README with a brief description
3. Follow existing formatting and style conventions
4. Add cross-references to related documents
5. Include date and version information

---

## Review Status

| Document | Review Date | Reviewer | Status |
|----------|-------------|----------|---------|
| PNP_ANTI_BARRIERS.md | 2025-10-30 | JMMB | ✅ Approved |
| PREREGISTRATION.md | 2025-10-30 | JMMB | ✅ Approved |
| analysis_plan.json | 2025-10-30 | JMMB | ✅ Approved |
| RELEASE_NOTES.md | 2025-10-30 | JMMB | ✅ Approved |

---

**Last Updated**: 2025-10-30  
**Version**: 2.0.0  
**Maintainer**: José Manuel Mota Burruezo (JMMB Ψ✧)
