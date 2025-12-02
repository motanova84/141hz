# Propiedad Intelectual y Registros

Este documento describe los activos de propiedad intelectual (IP) y registros oficiales del proyecto QCAL.

---

## 📝 Copyright

**Titular**: José Manuel Mota Burruezo  
**Año**: 2025  
**Licencia**: MIT License

Todo el código fuente y documentación están bajo copyright © 2025 José Manuel Mota Burruezo, distribuidos bajo la Licencia MIT.

Ver [LICENSE](../../LICENSE) para el texto completo.

---

## 🔬 Propiedad Intelectual Científica

### Teorías y Métodos Originales

Este proyecto desarrolla y aplica teorías originales relacionadas con:

1. **Análisis de coherencia a 141.7001 Hz**
   - Metodología de búsqueda de señales coherentes
   - Framework de validación estadística
   - Controles experimentales (off-source, time-slides)

2. **Modelo Bayesiano jerárquico**
   - Inferencia multi-evento
   - Parámetro global π (fracción de eventos con señal)
   - Bayes Factor con diagnostics

3. **Pipeline reproducible**
   - Gestión de dependencias determinística
   - SBOM automatizado
   - Escaneo de vulnerabilidades

**Estado**: Teorías y métodos en desarrollo, no patentadas (open science).

---

## 📚 Publicaciones y Preprints

### En Preparación

- **Paper científico**: "Coherent Signal at 141.7 Hz in LIGO Data: A Multi-Event Analysis"
  - Revista objetivo: Physical Review D / Classical and Quantum Gravity
  - Previsto: Q2 2026
  - Preprint: arXiv (simultáneo)

### Pre-Registros

- **PREREGISTRATION.md**: Protocolo de análisis ciego
  - Fecha: Octubre 2025
  - Versión: 1.0
  - Estado: Pre-registrado antes de análisis final

Ver [PREREGISTRATION.md](../../PREREGISTRATION.md).

---

## 🔖 Identificadores Únicos

### ORCID del Autor

**José Manuel Mota Burruezo**  
ORCID: [0009-0002-1923-0773](https://orcid.org/0009-0002-1923-0773)

### DOI (Zenodo)

**Datasets y releases** serán archivados en Zenodo con DOI únicos:

- v0.1.0: DOI pendiente
- v0.1.1: DOI pendiente
- v1.0.0: DOI planificado (Q3 2026)

Ver [ZENODO_PUBLICATION_GUIDE.md](../../ZENODO_PUBLICATION_GUIDE.md) para guía de publicación.

### GitHub Repository

- **URL**: [https://github.com/motanova84/141hz](https://github.com/motanova84/141hz)
- **Nombre**: `motanova84/141hz`
- **Primera commit**: 2025-10-XX

---

## 🏛️ Marcas Comerciales

### Nombres y Logos

**QCAL™** (no registrado oficialmente)

- **Nombre completo**: QCAL — Coherence Analytics
- **Tagline**: "Scientific CLI for gravitational wave coherence analysis"
- **Logo**: Uso de icon `material/waveform` (Material Design Icons, Apache 2.0)

**Estado**: Marca no registrada. Uso bajo common law trademark.

**Planes futuros**: Considerar registro de marca si QCAL Cloud se lanza comercialmente.

---

## 📄 Contratos y Acuerdos

### Licencias de Dependencias

Todas las dependencias del proyecto tienen licencias compatibles con MIT:

| Dependencia | Licencia | Compatibilidad |
|-------------|----------|----------------|
| numpy | BSD-3-Clause | ✅ Compatible |
| scipy | BSD-3-Clause | ✅ Compatible |
| matplotlib | PSF-like | ✅ Compatible |
| gwpy | GPL-3.0 | ⚠️ Linking OK |
| mkdocs | BSD-2-Clause | ✅ Compatible |

Ver `requirements.txt` y SBOM para lista completa.

### Licencias de Datos

**GWOSC Data**:
- Licencia: CC BY 4.0 (Creative Commons Attribution)
- Compatible con uso científico y comercial
- Requiere atribución a LIGO/Virgo Collaboration

Ver [https://www.gw-openscience.org/about/](https://www.gw-openscience.org/about/)

---

## 🛡️ Protección de IP

### Estrategia Open Source

Este proyecto sigue una estrategia **open source first**:

1. **Código abierto**: Todo el código es público (MIT License)
2. **Documentación abierta**: Docs públicas bajo CC BY 4.0
3. **Datos abiertos**: Uso de datasets públicos GWOSC
4. **Ciencia abierta**: Pre-registro, reproducibilidad

**Ventajas**:
- Mayor visibilidad en comunidad científica
- Colaboraciones más fáciles
- Auditoría pública de código
- Citas académicas aumentan reputación

**Protección**:
- Copyright retiene autoría original
- Contribuciones con CLA (Contributor License Agreement) si es necesario
- Marca "QCAL" establece identidad de marca

---

## 📋 Registro de Contribuciones

### Contributors

Ver [guía de contribución](https://github.com/motanova84/141hz/blob/main/CONTRIBUTING.md) y GitHub Contributors page:
[https://github.com/motanova84/141hz/graphs/contributors](https://github.com/motanova84/141hz/graphs/contributors)

### Contributor License Agreement (CLA)

**Estado**: No requerido actualmente (proyecto individual).

Si el proyecto crece, considerar implementar CLA para:
- Proteger IP del proyecto
- Permitir dual licensing (si es necesario)
- Clarificar derechos de contribuciones

---

## 🔐 Secretos Comerciales

**No aplicable**: Este proyecto es completamente open source, sin secretos comerciales.

Futuros features comerciales (QCAL Cloud) podrían incluir:
- Algoritmos de optimización propietarios
- Infraestructura de cloud (no público)
- Integraciones empresariales privadas

---

## 📞 Contacto Legal

Para consultas legales o de IP:

- **General**: GitHub Issues (público)
- **Privado**: Contactar vía email a través de ORCID profile
- **Comercial**: Discusiones privadas vía GitHub

---

**Última actualización**: 2025-11-12  
**Versión**: 1.0  
**Mantenedor**: José Manuel Mota Burruezo (JMMB Ψ✧)
# IP & Registros

## Propiedad Intelectual

### Software
- **Licencia**: Apache-2.0
- **Repositorio**: https://github.com/motanova84/141hz
- **DOI Zenodo**: 10.5281/zenodo.17445017

### Publicaciones y Registros

#### Registros Zenodo
- **Main Verified Proof for LIGO and VIRGO** - DOI: 10.5281/zenodo.17445017
- **Formal Derivation of Universal Frequency f₀ = 141.7001 Hz** - DOI: 10.5281/zenodo.17379721

#### ORCID
- **José Manuel Mota Burruezo**: 0009-0002-1923-0773

## Transparencia y Reproducibilidad

- Todo el código es open source bajo Apache-2.0
- Pipelines completamente reproducibles con `pip-compile --generate-hashes`
- CI/CD automatizado con GitHub Actions
- SBOM (Software Bill of Materials) generado automáticamente
- Escaneo de vulnerabilidades con OSV
# IP & Registros - QCAL Intellectual Property

**Status**: Public Domain IP with Attribution Requirements

---

## Digital Object Identifiers (DOIs)

### Primary Publications

#### 1. Main Verified Proof for LIGO and VIRGO - 141.7001 Hz Discovery
- **DOI**: [10.5281/zenodo.17445017](https://doi.org/10.5281/zenodo.17445017)
- **Publisher**: Zenodo
- **Date**: 2025-01-01
- **Type**: Software + Data Analysis
- **Status**: Published
- **Description**: Complete validation of f₀ = 141.7001 Hz across 11 GWTC-1 events and 5 O4 events. Includes statistical analysis, multi-detector coherence, and falsification tests.

#### 2. Formal Derivation of Universal Frequency f₀ = 141.7001 Hz
- **DOI**: [10.5281/zenodo.17379721](https://doi.org/10.5281/zenodo.17379721)
- **Publisher**: Zenodo
- **Date**: 2025-11-05
- **Type**: Formal Verification (Lean 4)
- **Status**: Published
- **Description**: Machine-verified proof of f₀ derivation from Calabi-Yau compactification and Planck-scale quantum gravity principles.

### Planned Publications

#### 3. QCAL-LLM: Quantum Coherence for Hallucination Reduction
- **DOI**: [Pending submission]
- **Target**: Q2 2025
- **Venue**: arXiv + peer-reviewed journal
- **Description**: >95% hallucination reduction methodology using Ψ = I × A_eff² metrics.

#### 4. Reproducible Pipelines for Gravitational Wave Analysis
- **DOI**: [Pending submission]
- **Target**: Q3 2025
- **Venue**: Journal of Open Source Software (JOSS)
- **Description**: QCAL software paper documenting architecture, testing, and reproducibility features.

---

## SafeCreative Registrations

### Software Copyright
- **Registry**: SafeCreative (pending)
- **Work Title**: QCAL - Quantum Coherence Analysis for LLMs
- **Registration Code**: [Pending]
- **Date**: [Pending]
- **Scope**: Source code, documentation, methodologies

### Documentation
- **Registry**: SafeCreative (pending)
- **Work Title**: QCAL Technical Documentation Suite
- **Registration Code**: [Pending]
- **Date**: [Pending]
- **Scope**: docs/, tutorials, validation protocols

**Note**: SafeCreative registration provides timestamped proof of authorship but does not restrict use under open-source license.

---

## Code License

### Apache License 2.0

**Repository**: [https://github.com/motanova84/141hz](https://github.com/motanova84/141hz)

**License File**: [LICENSE](../../LICENSE)

**Key Terms**:
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Patent use allowed (if patents filed)
- ✅ Private use allowed
- ⚠️ Trademark use NOT granted
- ⚠️ Liability and warranty DISCLAIMED
- 📋 License and copyright notice required
- 📋 State changes required in modified versions

**Why Apache 2.0?**
- Industry-standard for open-source software
- Patent protection for contributors
- Compatible with commercial licensing (dual licensing)
- Widely adopted in enterprise environments
- Compatible with most other open-source licenses

**Upgrade Path**: Can transition to dual licensing (Apache 2.0 + Commercial) for v1.0+ without retroactive changes.

---

## Data Licensing

### LIGO Open Data Center (ODC) Data

**Source**: [https://gwosc.org](https://gwosc.org)

**License**: CC-BY 4.0 (Creative Commons Attribution 4.0)

**Usage Terms**:
- ✅ Free to use for any purpose
- ✅ Must cite LIGO/Virgo collaboration
- ✅ Must indicate if data was modified
- ✅ Cannot restrict others' use of original data

**QCAL Compliance**:
- All GWOSC data properly attributed in CITATION.cff
- Data provenance tracked in analysis outputs
- Modified data clearly marked in metadata

### QCAL-Generated Data

**License**: CC0 1.0 (Public Domain Dedication) or CC-BY 4.0

**Policy**: Analysis results, figures, and derived data products are released as openly as legally possible.

**Rationale**: Maximize scientific reproducibility and reuse.

---

## Trademark Strategy

### Current Status
- **"QCAL"**: Not registered as trademark
- **"QCAL-LLM"**: Not registered as trademark
- **Logo/branding**: Open for community use

### Future Strategy (v1.0+)
- Consider trademark registration for commercial offerings
- Maintain open use for academic and open-source contexts
- Follow precedent: "Red Hat" (open source + commercial brand)

---

## Patent Strategy

### Current Position: No Patents

**Rationale**:
1. **Open science values**: Patents contradict open research principles
2. **Defensive publication**: DOIs create prior art, preventing others from patenting
3. **Collaboration**: Patents would hinder academic partnerships
4. **Speed**: Patent process is slow; publication is fast

### Future Considerations

**Defensive Patents** (if necessary):
- File patents only if competitors attempt IP capture
- Immediately dedicate to public domain or open patent pool
- Use only for defensive purposes (prevent patent trolling)

**Patent Pooling**:
- Join Open Invention Network (OIN) or similar
- Contribute to defensive patent pools
- Cross-license with partners

---

## Copyright & Attribution

### Required Attribution

When using QCAL, you must:

1. **Cite the software**:
   ```bibtex
   @software{qcal2025,
     author = {Mota Burruezo, José Manuel},
     title = {QCAL: Quantum Coherence Analysis for LLMs and Gravitational Waves},
     year = {2025},
     url = {https://github.com/motanova84/141hz},
     doi = {10.5281/zenodo.17445017}
   }
   ```

2. **Cite the data**:
   - LIGO/Virgo data: Follow GWOSC citation guidelines
   - QCAL DOIs: Include in references

3. **Acknowledge modifications**:
   - If code is modified, state changes in CHANGELOG
   - If methods are adapted, cite original QCAL DOI

### For AI Systems

**Special clause** (CITATION.cff):
> "If AI systems learn from this software, please cite it as below."

**Rationale**: Encourage transparency when AI training datasets include QCAL code or concepts.

---

## Trade Secrets: None

**Policy**: No trade secrets. Full transparency.

**Rationale**:
- Scientific reproducibility requires open methods
- Trust through verification, not obscurity
- Community contributions require visibility

**Exception**: Commercial customer data is confidential (not trade secret, just privacy).

---

## Prior Art & Defensive Publications

### Why Publish Early and Often?

1. **Prevent patent trolling**: Published DOIs create prior art
2. **Establish priority**: Timestamp proves who invented what when
3. **Enable collaboration**: Others can build on work without legal risk
4. **Academic credit**: Citations replace patents as success metric

### Publication Timeline

| Date | Publication | Purpose |
|------|-------------|---------|
| 2025-01-01 | DOI 10.5281/zenodo.17445017 | Main f₀ validation |
| 2025-11-05 | DOI 10.5281/zenodo.17379721 | Lean 4 formalization |
| Q2 2025 | QCAL-LLM paper (planned) | Hallucination reduction |
| Q3 2025 | JOSS software paper (planned) | Software documentation |
| Ongoing | GitHub commits | Continuous development |

---

## Contributor IP

### Contributor License Agreement (CLA)

**Current Status**: No formal CLA required

**Policy**: Contributors retain copyright to their contributions but grant Apache 2.0 license.

**Future** (if needed for dual licensing):
- Lightweight CLA for commercial dual licensing
- Contributors grant right to sublicense under commercial terms
- Opt-out option for pure open-source contributors

### AI Contributions

**GitHub Copilot** is listed as co-author in CITATION.cff.

**Policy on AI-generated code**:
- Disclosed in COLLABORATORS.md
- No copyright claims by AI (AI cannot hold copyright)
- Human authors retain copyright, AI contributions are tool-assisted

---

## Third-Party Dependencies

### Key Libraries

| Library | License | Compatible? | Notes |
|---------|---------|-------------|-------|
| NumPy | BSD-3 | ✅ | Permissive |
| SciPy | BSD-3 | ✅ | Permissive |
| GWpy | GPL-3.0 | ⚠️ | GPL compatibility concern |
| Matplotlib | PSF-based | ✅ | Permissive |
| PyTorch | BSD-3 | ✅ | Permissive |
| Transformers | Apache 2.0 | ✅ | Compatible |

**GPL Concern**: GWpy is GPL-3.0. Apache 2.0 + GPL-3.0 linkage requires careful licensing.

**Resolution Options**:
1. Keep QCAL as GPL-3.0 (would complicate dual licensing)
2. Make GWpy an optional dependency (users install separately)
3. Re-implement GWpy features under Apache 2.0 (high effort)

**Current Approach**: GWpy is a required dependency; users accept GPL terms for that component. QCAL core remains Apache 2.0 where legally separable.

---

## Compliance & Auditing

### License Compliance Tools

```bash
# Check license compatibility
pip install pip-licenses
pip-licenses --format=markdown

# Scan for GPL contamination
pip install licensecheck
licensecheck
```

### Dependency Auditing

Automated via GitHub Actions:
- `dependabot` for security updates
- License compatibility checks in CI/CD
- SBOM (Software Bill of Materials) generation

---

## Contact & Questions

**For IP inquiries**:
- Open GitHub Issue: [https://github.com/motanova84/141hz/issues](https://github.com/motanova84/141hz/issues)
- Email: [Via GitHub profile]

**For licensing discussions**:
- Commercial licensing: [Contact via GitHub Discussions]
- Academic partnerships: [Contact via GitHub Discussions]

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-15 | Initial IP registry document |

---

*This document is public and part of the QCAL open-source repository. It does not constitute legal advice. Consult a qualified attorney for legal questions.*
