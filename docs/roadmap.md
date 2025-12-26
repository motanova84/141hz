# Roadmap

Hoja de ruta del proyecto QCAL — Análisis de Coherencia a 141.7 Hz

## v0.2.0 — Q1 2026 (Planificado)

### Análisis Multi-Evento
- [ ] Integración completa de eventos GWTC-2 y GWTC-3
- [ ] Pipeline automatizado para nuevos eventos
- [ ] Dashboard interactivo de resultados

### Mejoras en Validación
- [ ] 10,000 ventanas off-source por evento (automatizado)
- [ ] Time-slides multi-detector (100+ combinaciones)
- [ ] Análisis Bayesiano jerárquico refinado

### Infraestructura
- [ ] API REST para acceso programático
- [ ] Base de datos de resultados (PostgreSQL)
- [ ] Cache de datos GWOSC (reducir descargas)

## v0.3.0 — Q2 2026 (Planificado)

### Detectores adicionales
- [ ] Integración de Virgo (todos los eventos O2+)
- [ ] Integración de KAGRA (eventos O4)
- [ ] Análisis de coherencia 3-4 detectores

### Machine Learning
- [ ] Clasificador de señales vs ruido (CNN)
- [ ] Detección automática de líneas instrumentales
- [ ] Predicción de SNR con redes neuronales

### Visualización
- [ ] Dashboard web interactivo (Dash/Streamlit)
- [ ] Plots 3D de coherencia multi-detector
- [ ] Animaciones de evolución temporal

## v1.0.0 — Q3 2026 (Objetivo)

### Release estable
- [ ] API estable (SemVer)
- [ ] Documentación completa (Sphinx + MkDocs)
- [ ] Tutorial interactivo (Jupyter Book)

### Publicación científica
- [ ] Paper en revista peer-reviewed
- [ ] Preprint en arXiv
- [ ] Datasets en Zenodo con DOI

### Comunidad
- [ ] Guías de contribución detalladas
- [ ] Issues templates
- [ ] Discusiones en GitHub

## Backlog (Ideas futuras)

### Análisis avanzados
- Análisis de armónicos (2×141.7 Hz, 3×141.7 Hz)
- Búsqueda de modulaciones temporales
- Correlación con catálogos astronómicos

### Integraciones
- PyCBC (análisis de ondas gravitacionales)
- LALSuite (LIGO Algorithm Library)
- Bilby (inferencia Bayesiana)

### Formalismos matemáticos
- Lean 4: Formalización completa de teoremas
- Coq: Verificación de algoritmos críticos
- Isabelle/HOL: Pruebas de propiedades estadísticas

### HPC y escalabilidad
- Paralelización con Dask/Ray
- Soporte GPU (CuPy)
- Cluster computing (Slurm)

## Versiones anteriores

### v0.1.1 — 2025-11-11 ✅
- Sitio MkDocs optimizado
- Despliegue automático a gh-pages
- Minificado HTML y sitemap

### v0.1.0 — 2025-11-11 ✅
- CLI inicial `qcal analyze`
- Tests + CI + SBOM + OSV scan
- Documentación con MkDocs Material

## Contribuir al roadmap

¿Tienes ideas para el proyecto? Abre un issue:

- [Feature requests](https://github.com/motanova84/141hz/issues/new?labels=enhancement)
- [Bug reports](https://github.com/motanova84/141hz/issues/new?labels=bug)
- [Discusiones](https://github.com/motanova84/141hz/discussions)

## Prioridades

Las siguientes características tienen alta prioridad:

1. 🔥 **Multi-evento GWTC-2/3**: Ampliar cobertura
2. 🔥 **Validación robusta**: Off-source automatizado
3. 🔥 **API REST**: Acceso programático
4. ⭐ **Dashboard web**: Visualización interactiva
5. ⭐ **Paper científico**: Publicación peer-reviewed

## Financiación

Buscamos financiación para:

- Tiempo de cómputo en clusters HPC
- Revisión y auditoría de código
- Conferencias y presentaciones
- Publicaciones en open access

Ver [dataroom/valuation_onepager.md](dataroom/valuation_onepager.md) para más información.

---

**Última actualización**: 2025-11-12  
**Mantenedor**: José Manuel Mota Burruezo (JMMB Ψ✧)
- **v0.1**: CLI básica + CI + SBOM + docs
- **v0.2**: Paquete PyPI y datasets guiados
- **v0.3**: Pilotos QC-LLM / GW con informes automáticos
# QCAL Development Roadmap

## Overview

This roadmap outlines the planned development of QCAL from the initial CLI release through enterprise-ready features and research integrations.

---

## v0.1 - Basic CLI ✓ (Current)

**Status**: In Development  
**Target**: Q1 2025  
**Branch**: `feat/packaging-ci-repro`

### Features

- [x] Core QCAL module (`qcal/`)
  - [x] Coherence metrics (Ψ = I × A_eff²)
  - [x] Statistical metrics (SNR, KL divergence)
  - [x] Quantum radio, quantum energy, discrete symmetry
- [x] Basic CLI (`qcal` command)
  - [x] `qcal analyze` - Analyze GW catalogs
  - [x] `qcal validate` - Run validation protocols
  - [x] `qcal compare` - Compare results
- [x] Documentation
  - [x] docs/overview.md
  - [x] docs/cli.md
  - [x] docs/validation.md
  - [x] docs/roadmap.md (this file)
- [x] Testing infrastructure
  - [x] pytest configuration
  - [x] Basic unit tests
  - [x] Integration tests
- [x] CI/CD
  - [x] GitHub Actions workflows
  - [x] Automated testing
  - [x] Linting (flake8, black)
- [x] Reproducibility
  - [x] `repro/GWTC-1/` pipeline
  - [x] Versioned dependencies
  - [x] Fixed random seeds

### Deliverables

- Installable Python package (`pip install -e .`)
- Working CLI with basic commands
- Documentation in `docs/`
- CI/CD pipeline passing
- Tagged release: `v0.1.0`

---

## v0.2 - PyPI + Total Reproducibility

**Status**: Planned  
**Target**: Q2 2025

### Features

#### Package Distribution
- [ ] PyPI publication (`pip install qcal`)
- [ ] Conda-forge package
- [ ] Docker images (CPU and GPU)
- [ ] Pre-built wheels for major platforms

#### Enhanced Reproducibility
- [ ] Reproducibility checksum verification
- [ ] Environment snapshot (`qcal env export`)
- [ ] Containerized workflows (Singularity/Apptainer)
- [ ] Automated data versioning (DVC integration)
- [ ] Reproducibility badges for analyses

#### Expanded CLI
- [ ] `qcal export` - Export to LaTeX, PDF, HTML
- [ ] `qcal config` - Configuration management
- [ ] `qcal cache` - Cache management
- [ ] Progress bars and rich terminal UI
- [ ] Interactive mode

#### Performance Optimization
- [ ] GPU acceleration (CuPy)
- [ ] Parallel processing (Dask)
- [ ] Caching of intermediate results
- [ ] Memory-efficient streaming for large datasets

#### Testing & QA
- [ ] 90%+ code coverage
- [ ] Property-based testing (Hypothesis)
- [ ] Benchmarking suite
- [ ] Performance regression tests

### Deliverables

- Published PyPI package
- Docker Hub images
- Comprehensive reproducibility guide
- Performance benchmarks
- Tagged release: `v0.2.0`

---

## v0.3 - QC-LLM/GW Pilots

**Status**: Planned  
**Target**: Q3 2025

### Features

#### QC-LLM Integration
- [ ] Llama 4 Maverick coherence backend
- [ ] QCAL-LLM evaluation pipeline
- [ ] Hallucination detection (>95% reduction)
- [ ] Attention mechanism integration
- [ ] Real-time coherence monitoring

#### GW Analysis Extensions
- [ ] LISA integration (mHz band)
- [ ] DESI correlation analysis
- [ ] IGETS geophysical coupling
- [ ] Multi-messenger astronomy hooks
- [ ] Custom detector support

#### Enterprise Features
- [ ] REST API server
- [ ] Web dashboard
- [ ] User authentication
- [ ] Job queuing system
- [ ] Cloud deployment guides (AWS, GCP, Azure)

#### Pilot Programs
- [ ] QC-LLM pilot with enterprise partners (8-12 weeks)
- [ ] GW research collaborations (LIGO/Virgo)
- [ ] Academic institution partnerships

### Pilot Structure

#### QC-LLM Pilot Brief
See: [docs/dataroom/pilot_briefs/qcllm.md](dataroom/pilot_briefs/qcllm.md)

**Objective**: Demonstrate >95% hallucination reduction in production LLM systems

**Metrics**:
- Hallucination rate reduction
- Response coherence score (Ψ)
- Inference latency overhead
- Integration effort (developer-hours)

**Timeline**: 8-12 weeks
- Week 1-2: Integration and baseline
- Week 3-6: Tuning and optimization
- Week 7-8: Validation and reporting
- Week 9-12: Documentation and handoff

**Deliverables**:
- Technical integration guide
- Performance benchmarks
- Cost-benefit analysis
- Case study report

**Risk Mitigation**:
- Fallback to CPU if GPU unavailable
- Incremental rollout (A/B testing)
- 24/7 monitoring and alerts
- Regular checkpoints and reviews

### Deliverables

- QC-LLM production-ready integration
- Pilot program completion reports
- Enterprise deployment documentation
- Tagged release: `v0.3.0`

---

## v1.0 - Production-Grade System

**Status**: Future  
**Target**: Q4 2025

### Features

- [ ] Stable API (semantic versioning)
- [ ] Comprehensive documentation
- [ ] 95%+ test coverage
- [ ] Security audit completion
- [ ] Scalability testing (1000+ events)
- [ ] Long-term support (LTS) commitment

### Enterprise Features

- [ ] Dual licensing (Apache 2.0 + Commercial)
- [ ] SLA guarantees
- [ ] Priority support
- [ ] Custom feature development
- [ ] White-label options

### Deliverables

- Production-ready v1.0.0 release
- Enterprise licensing options
- Professional support offering
- Tagged release: `v1.0.0`

---

## Future Directions (v2.0+)

### Research Integrations
- [ ] Quantum gravity simulations
- [ ] String theory model testing
- [ ] Calabi-Yau compactification
- [ ] Riemann hypothesis connections
- [ ] Fractal resonance analysis

### Advanced Features
- [ ] Machine learning integration
- [ ] Automated anomaly detection
- [ ] Predictive modeling
- [ ] Real-time streaming analysis
- [ ] Federated learning for privacy

### Ecosystem Growth
- [ ] Plugin architecture
- [ ] Community contributions
- [ ] Third-party integrations
- [ ] Educational materials
- [ ] Conference presentations

---

## Development Principles

### Scientific Rigor
- Peer-reviewed methods
- Open data and code
- Reproducible results
- Falsifiable hypotheses

### Software Quality
- Test-driven development
- Continuous integration
- Code review process
- Documentation-first approach

### Community
- Open source (MIT license)
- Welcoming contributors
- Responsive maintainers
- Regular releases

### Privacy & Ethics
- No telemetry by default (see [PRIVACY.md](../PRIVACY.md))
- Opt-in metrics only
- Data sovereignty
- Transparent practices

---

## Contributing

We welcome contributions at all levels:

1. **Bug reports**: Open issues on GitHub
2. **Feature requests**: Discuss in GitHub Discussions
3. **Code contributions**: Submit pull requests
4. **Documentation**: Improve docs and tutorials
5. **Testing**: Add test cases and benchmarks

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

---

## Funding & Support

### Current Status
- Self-funded open source project
- Community contributions
- Academic research grants

### Future Plans
- Dual licensing (v1.0)
- Enterprise support contracts
- Pilot program revenue
- Research grants and partnerships

See [docs/dataroom/valuation_onepager.md](dataroom/valuation_onepager.md) for investment details.

---

## Questions?

- **GitHub Issues**: [https://github.com/motanova84/141hz/issues](https://github.com/motanova84/141hz/issues)
- **Discussions**: [https://github.com/motanova84/141hz/discussions](https://github.com/motanova84/141hz/discussions)
- **Email**: Contact maintainers (see [COLLABORATORS.md](../COLLABORATORS.md))

---

*Last updated: 2025-01-15*
