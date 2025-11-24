# Release Notes

## Version History

### v2.0.0 (2025-10-30) - Pre-Registration & Formalization Release

**Major Changes:**

#### 1. RH (Riemann Hypothesis) - Adelic System
- ✅ **Axioms → Theorems**: Replaced axioms with proper theorem statements
  - Theorem (D ≡ Ξ): Hadamard factorization, Paley-Wiener control, normalization
  - Theorem (Zeros on critical line): Self-adjoint operator, kernel positivity
  - Lemma (Trivial zeros excluded): Gamma factor separation
- ✅ **Lean Formalization**: Created `formalization/lean/RiemannAdelic/axiom_purge.lean`
  - Skeleton theorems with proof strategy outlined
  - CI workflow for axiom checking (`lean-ci.yml`)
- ✅ **Documentation**: Updated references to U1/U2 hypotheses (uniform convergence)

#### 2. 141.7001 Hz GW Analysis - Pre-Registration Protocol
- ✅ **Blind Pre-Registration**: Added `PREREGISTRATION.md`
  - Predefined frequency: 141.7001 Hz (±0.3 Hz)
  - Analysis window: t0 ± 0.25 s
  - PSD method: Welch (Nfft=16384, 50% overlap)
  - Statistical framework: Hierarchical Bayesian
- ✅ **Analysis Plan**: Created `analysis_plan.json` with complete parameters
  - Time windows, spectral analysis, validation controls
  - Success and falsification criteria
  - Reproducibility parameters
- ✅ **Control Infrastructure**:
  - `controls/lines_exclusion.csv`: Instrumental line exclusions (60 Hz harmonics, violin modes, calibration lines)
  - `bayes/hierarchical_model.py`: Hierarchical Bayesian inference with π_global parameter
  - `notebooks/antenna_pattern.ipynb`: Antenna pattern consistency checker
- ✅ **Validation Targets**:
  - Off-source null distribution (10^4 windows)
  - Time-slides (200 per detector pair, ±50 ms)
  - Leave-one-out robustness tests
  - Multi-detector coherence checks

#### 3. P≠NP - Anti-Barriers Documentation
- ✅ **Anti-Barriers Analysis**: Created `docs/PNP_ANTI_BARRIERS.md`
  - Non-relativization: SILB depends on graph structure, not oracle access
  - Non-naturality: Predicates not constructible in P-time, not dense over {0,1}^n
  - Non-algebrization: Separator topology breaks under polynomial extensions
- ✅ **Lean Stubs**: Formalization skeletons
  - `formal/Treewidth/SeparatorInfo.lean`: SILB lemma
  - `formal/Lifting/Gadgets.lean`: Gadget validity
  - `formal/LowerBounds/Circuits.lean`: Circuit lower bound theorem
- ✅ **Technical Route**: Treewidth → Communication → Lifting → Circuit bounds

#### 4. Navier-Stokes - Documentation (Placeholder)
- 📝 **Note**: This repository focuses on 141.7 Hz GW analysis
- 📝 NS changes should be implemented in `3D-Navier-Stokes` repository:
  - Functional spaces (L²_σ, H¹, Leray-Hopf solutions)
  - Energy inequality and BKM criterion
  - Theorem: Misalignment δ* → global regularity
  - Lean formalization: `FunctionalSpaces.lean`

#### 5. Editorial & Traceability
- ✅ **Makefile**: Added targets for reproducible builds
  - `make pdf-docs`: LaTeX documentation building
  - `make lock-env`: Environment version locking
  - `make bayes-analysis`: Hierarchical Bayesian analysis
  - `make antenna-check`: Antenna pattern verification
- ✅ **ENV.lock**: Environment snapshot for reproducibility
- ✅ **CI Workflow**: Lean axiom checking workflow
- 📝 **Bibliography**: TODO - migrate to biblatex/biber (LaTeX-based projects)

---

### v1.x (Previous Releases)

See [CHANGELOG.md](CHANGELOG.md) for complete version history of pre-registration releases.

---

## Migration Guide

### For Users
- Update your local environment: `make setup`
- Lock your environment: `make lock-env`
- Run pre-registered analysis: `make bayes-analysis`

### For Developers
- Review pre-registration protocol: `PREREGISTRATION.md`
- Check analysis parameters: `analysis_plan.json`
- Add instrumental lines: `controls/lines_exclusion.csv`
- Extend Bayesian model: `bayes/hierarchical_model.py`

### For Reviewers
- Pre-registration ensures analysis parameters were fixed before unblinding
- Hierarchical model prevents multiple testing issues
- Controls for instrumental artifacts are documented
- Off-source and time-slide validation provides null distribution

---

## Breaking Changes

None - this is an additive release focused on documentation and pre-registration.

---

## Known Issues

1. Lean formalization is skeletal (proof stubs only)
2. Antenna pattern calculation uses simplified formulas (should use LALSuite)
3. BibTeX references not yet migrated to biblatex
4. NS-related changes pending in separate repository

---

## Future Roadmap

### v2.1 - Lean Proof Development
- [ ] Complete Hadamard factorization in Lean
- [ ] Prove relative determinant bounds
- [ ] Formalize kernel positivity argument
- [ ] Verify zero extra axioms with `lake exe print-axioms`

### v2.2 - Full Off-Source Analysis
- [ ] Implement 10^4 off-source window analysis
- [ ] Complete time-slide validation
- [ ] Add leave-one-out cross-validation
- [ ] Generate Bayes Factor comparison plots

### v2.3 - Advanced Antenna Patterns
- [ ] Integrate LALSuite for exact F+/Fx calculation
- [ ] Marginalize over GWOSC posterior samples
- [ ] Add χ² test for astrophysical consistency
- [ ] Visualize on Mollweide projection

### v3.0 - Multi-Repository Integration
- [ ] Sync with jmmotaburr-riemann-adelic repo
- [ ] Sync with 3D-Navier-Stokes repo
- [ ] Unified bibliography across projects
- [ ] Cross-repository CI/CD coordination

---

## Contributors

See [COLLABORATORS.md](COLLABORATORS.md) for full list of contributors.

**Principal Investigator**: José Manuel Mota Burruezo (JMMB Ψ✧)

---

## License

MIT License - See [LICENSE](LICENSE) for details.

---

## Citation

If you use this work, please cite:

```bibtex
@software{mota2025_141hz_prereg,
  author = {Mota Burruezo, José Manuel},
  title = {141.7001 Hz GW Analysis: Pre-Registration and Validation Framework},
  year = {2025},
  version = {2.0.0},
  url = {https://github.com/motanova84/141hz},
  doi = {10.5281/zenodo.17379721}
}
```

---

**Date**: October 30, 2025  
**Status**: Released  
**Next Review**: TBD
