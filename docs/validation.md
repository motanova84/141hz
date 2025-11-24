# Validación

QCAL implementa un framework de validación riguroso que garantiza la calidad y corrección de los análisis.

## Metodología de validación

### Niveles de validación

1. **Tests unitarios**: Funciones individuales
2. **Tests de integración**: Pipelines completos
3. **Validación científica**: Controles off-source, time-slides
4. **Validación estadística**: Significancia, p-valores
5. **Revisión por pares**: Pre-registro y replicación

## Tests unitarios

### Estructura de tests

```
tests/
├── test_qcal_module.py       # Tests del módulo principal
├── test_multi_event_analysis.py
├── test_pozo_infinito_cuantico.py
└── ...
```

### Ejecutar tests

```bash
# Todos los tests
pytest

# Tests específicos
pytest tests/test_qcal_module.py

# Con cobertura
pytest --cov=qcal tests/
```

## Validaciones científicas

### 1. Validación de radio cuántico

Verifica la consistencia de las predicciones teóricas:

```bash
python run_all_validations.py --validation radio_cuantico
```

**Criterios de éxito**:
- Desviación < 1% del valor teórico
- p-valor > 0.05 (no rechazo)

### 2. Validación de energía cuántica

Valida cálculos de energía en el pozo cuántico:

```bash
python run_all_validations.py --validation energia_cuantica
```

### 3. Validación de simetría discreta

Verifica simetría gauge en el campo Ψ:

```bash
python run_all_validations.py --validation simetria_discreta
```

## Controles experimentales

### Off-source analysis

Análisis de ventanas temporales sin señal esperada:

```python
# 10,000 ventanas off-source por evento
from controls import offsource_analysis

null_distribution = offsource_analysis(
    event='GW150914',
    detector='H1',
    n_windows=10000
)
```

**Objetivo**: Caracterizar distribución nula bajo H₀.

### Time-slides

Desplazamiento temporal entre detectores:

```python
from controls import time_slides

significance = time_slides(
    events=['GW150914', 'GW151226'],
    detectors=['H1', 'L1'],
    n_slides=100
)
```

**Objetivo**: Estimar tasa de coincidencias accidentales.

### Leave-one-out cross-validation

```python
from bayes import leave_one_out

loo_results = leave_one_out(event_list)
```

**Objetivo**: Verificar robustez del análisis Bayesiano.

## Análisis Bayesiano multi-evento

### Modelo jerárquico

```python
from bayes.hierarchical_model import bayes_factor

# Lista de SNRs de múltiples eventos
snr_list = [12.5, 8.3, 15.1, 6.7, ...]

# Calcular Bayes Factor
bf, diagnostics = bayes_factor(snr_list)
print(f"Bayes Factor: {bf:.2f}")
print(f"log₁₀(BF): {np.log10(bf):.2f}")
```

**Interpretación** (escala de Kass-Raftery):
- log₁₀(BF) < 0.5: No evidencia
- 0.5 < log₁₀(BF) < 1: Evidencia débil
- 1 < log₁₀(BF) < 2: Evidencia fuerte
- log₁₀(BF) > 2: Evidencia decisiva

### Parámetros globales

- **π**: Fracción de eventos con señal (prior: Beta(1,1))
- **μ, σ**: Media y desviación de SNR (priors normales)

Ver [hierarchical_model.py](../bayes/hierarchical_model.py) para detalles.

## CI/CD

### Workflows automáticos

#### `.github/workflows/ci.yml`
Tests básicos en cada commit:
```yaml
- Lint (flake8)
- Tests unitarios (pytest)
- Cobertura de código
```

#### `.github/workflows/analyze.yml`
Análisis completo cada 4 horas:
```yaml
- Descarga de datos GWOSC
- Análisis espectral
- Generación de artefactos
```

#### `.github/workflows/scientific-validation.yml`
Validaciones científicas programadas:
```yaml
- Radio cuántico
- Energía cuántica
- Simetría discreta
```

### Badges de estado

![CI](https://github.com/motanova84/141hz/workflows/CI/badge.svg)
![Tests](https://github.com/motanova84/141hz/workflows/Tests/badge.svg)

Ver [.github/workflows/](../.github/workflows/) para todos los workflows.

## Pre-registro

### Blind pre-registration

El proyecto sigue un protocolo de pre-registro ciego:

1. **Análisis pre-registrado** en [PREREGISTRATION.md](../PREREGISTRATION.md)
2. **Parámetros fijos** en [analysis_plan.json](../analysis_plan.json)
3. **Criterios de éxito** definidos a priori
4. **Falsificación posible**: Condiciones de rechazo claras

### Criterios de éxito

**Hipótesis nula (H₀)**: No hay señal coherente a 141.7 Hz

**Criterio de rechazo de H₀**:
- SNR > 5σ en ≥3 eventos
- Consistencia multi-detector (H1/L1)
- Bayes Factor > 100
- Controles off-source: p < 0.01

## Exclusión de líneas instrumentales

Frecuencias conocidas se excluyen del análisis:

```csv
# controls/lines_exclusion.csv
frequency,source,detector
60.0,power_grid,H1
120.0,power_grid_2nd_harmonic,H1
500.0,calibration_line,H1
```

Ver [lines_exclusion.csv](../controls/lines_exclusion.csv) completo.

## Antenna pattern consistency

Verifica consistencia con el patrón de antena de LIGO:

```python
from notebooks import antenna_pattern

# Calcula F+ y Fx para una dirección del cielo
f_plus, f_cross = antenna_pattern(ra, dec, psi, detector='H1')

# Compara con amplitudes observadas
ratio_predicted = f_plus / f_cross
ratio_observed = A_plus / A_cross

assert np.isclose(ratio_predicted, ratio_observed, rtol=0.1)
```

Ver [antenna_pattern.ipynb](../notebooks/antenna_pattern.ipynb).

## Estadística de validación

### p-valores y significancia

```python
from scipy import stats

# Test de Kolmogorov-Smirnov
ks_stat, p_value = stats.kstest(observed, null_distribution)

# Test χ²
chi2, p_value = stats.chisquare(observed, expected)
```

### Corrección por múltiples pruebas

Aplicamos corrección de Bonferroni:

```python
alpha_corrected = 0.05 / n_tests
```

## Replicabilidad

### Datos públicos

Todos los análisis usan datos públicos de GWOSC:
- [https://www.gw-openscience.org/](https://www.gw-openscience.org/)

### Código abierto

Todo el código es open source (MIT License):
- [https://github.com/motanova84/141hz](https://github.com/motanova84/141hz)

### Documentación completa

Cada script incluye docstrings y ejemplos de uso.

## Reportes de validación

Los resultados de validación se publican como GitHub Issues:
- [Validation Reports](https://github.com/motanova84/141hz/labels/validation)

## Ver también

- [CLI](cli.md): Cómo ejecutar análisis
- [Reproducibilidad](reproducibilidad.md): Gestión de entornos
- [PREREGISTRATION.md](../PREREGISTRATION.md): Protocolo de pre-registro
- [DISCOVERY_STANDARDS.md](../DISCOVERY_STANDARDS.md): Estándares de descubrimiento
- Criterio: umbral **5σ** en banda 141.7 Hz
- Métricas: `mean_snr`, distribución por evento
- Artefactos subidos en CI: `coverage.xml`, `sbom.json`, figuras y tablas
# QCAL Validation Protocols

## Overview

QCAL employs a rigorous three-pillar validation framework to ensure scientific reproducibility and falsifiability. All detections must pass multiple independent criteria to be considered valid.

## The Three Pillars

### 1. Quantum Radio (r_ψ)

**Definition**: The ratio between coherent energy and vacuum energy at f₀ = 141.7001 Hz.

**Formula**:
```
r_ψ = E_coherent / E_vacuum
```

**Validation Criteria**:
- r_ψ > 1.0 (coherent energy exceeds vacuum fluctuations)
- Statistical significance: p < 0.05
- Consistency across detectors (< 20% variation)

**Implementation**:
```python
from qcal import compute_quantum_radio

r_psi, p_value = compute_quantum_radio(psd, f0=141.7001, bandwidth=2.0)
valid = (r_psi > 1.0) and (p_value < 0.05)
```

**Physical Interpretation**: 
r_ψ > 1.0 indicates a coherent signal above quantum vacuum noise, suggesting a real physical source rather than random fluctuation.

### 2. Quantum Energy (E_cuántica)

**Definition**: Energy density at the fundamental frequency.

**Formula**:
```
E_cuántica = ∫_{f₀-Δf}^{f₀+Δf} S(f) df
```

where S(f) is the power spectral density.

**Validation Criteria**:
- E_cuántica > threshold (detector-dependent)
- SNR > 5.0
- Δf tolerance: |f_peak - f₀| < 1.0 Hz

**Implementation**:
```python
from qcal import compute_quantum_energy

E_q, snr, delta_f = compute_quantum_energy(
    psd, f0=141.7001, bandwidth=2.0, detector='H1'
)
valid = (snr > 5.0) and (abs(delta_f) < 1.0)
```

**Physical Interpretation**:
High quantum energy at f₀ indicates a persistent spectral feature that cannot be explained by transient noise or instrumental artifacts.

### 3. Discrete Symmetry

**Definition**: Phase coherence between multiple detectors.

**Formula**:
```
S_discrete = Σᵢⱼ cos(φᵢ - φⱼ) / N_pairs
```

where φᵢ is the phase at detector i.

**Validation Criteria**:
- S_discrete > 0.5 (high phase coherence)
- At least 2 detectors required
- Time-delay consistency with detector geometry

**Implementation**:
```python
from qcal import compute_discrete_symmetry

S, phases, consistency = compute_discrete_symmetry(
    psds={'H1': psd_h1, 'L1': psd_l1, 'V1': psd_v1},
    f0=141.7001
)
valid = (S > 0.5) and consistency
```

**Physical Interpretation**:
Phase coherence across widely separated detectors rules out local instrumental effects and supports a gravitational wave origin.

## Falsification Criteria

QCAL is designed to be **falsifiable**. A detection is rejected if:

1. **Any pillar fails**: All three criteria must pass
2. **Inconsistent across detectors**: >30% variation in measured f₀
3. **Time-domain artifacts**: Glitches or non-stationarity detected
4. **Statistical insignificance**: Combined p-value > 0.05
5. **Off-source contamination**: Similar features in off-source data

### Falsification Tests

```python
# Example falsification workflow
from qcal import run_falsification_tests

results = run_falsification_tests(
    event='GW150914',
    detector='H1',
    f0=141.7001,
    tests=['glitch', 'stationarity', 'off_source', 'consistency']
)

if results['falsified']:
    print(f"Detection REJECTED: {results['reason']}")
    print(f"Failed tests: {results['failed_tests']}")
else:
    print("Detection VALIDATED")
```

## Export Formats

### Tables

Results are exported in multiple table formats:

#### LaTeX
```latex
\begin{table}[h]
\centering
\caption{GWTC-1 Validation Results}
\begin{tabular}{lcccccc}
\hline
Event & Detector & $f_0$ (Hz) & SNR & $r_\psi$ & $E_q$ & Valid \\
\hline
GW150914 & H1 & 141.65 & 23.5 & 1.45 & 2.1e-20 & Yes \\
GW151226 & H1 & 141.72 & 18.3 & 1.32 & 1.8e-20 & Yes \\
...
\hline
\end{tabular}
\end{table}
```

#### CSV
```csv
event,detector,f_peak,snr,r_psi,e_cuantica,validated
GW150914,H1,141.65,23.5,1.45,2.1e-20,true
GW151226,H1,141.72,18.3,1.32,1.8e-20,true
```

#### Markdown
```markdown
| Event | Detector | f₀ (Hz) | SNR | r_ψ | E_q | Valid |
|-------|----------|---------|-----|-----|-----|-------|
| GW150914 | H1 | 141.65 | 23.5 | 1.45 | 2.1e-20 | ✓ |
| GW151226 | H1 | 141.72 | 18.3 | 1.32 | 1.8e-20 | ✓ |
```

### Figures

QCAL generates publication-quality figures:

1. **PSD Plots**: Power spectral density with f₀ band highlighted
2. **SNR vs Event**: Bar chart of SNR across events
3. **Frequency Distribution**: Histogram of detected frequencies
4. **Multi-Detector Comparison**: Overlay plots for H1, L1, V1
5. **Validation Matrix**: Heatmap of validation criteria

```python
from qcal import export_figures

export_figures(
    results='artifacts/summary.json',
    outdir='figures/',
    formats=['png', 'pdf', 'svg'],
    dpi=300
)
```

## Comparative Analysis

### Cross-Catalog Comparison

Compare results across different catalogs:

```python
from qcal import compare_catalogs

comparison = compare_catalogs(
    catalogs=['GWTC-1', 'GWTC-2', 'O4'],
    detector='H1',
    f0=141.7001
)

print(f"Detection rate: {comparison['detection_rate']}")
print(f"Mean SNR: {comparison['mean_snr']}")
print(f"Consistency score: {comparison['consistency']}")
```

### Multi-Detector Coherence

Validate coherence across detector network:

```python
from qcal import multi_detector_coherence

coherence = multi_detector_coherence(
    event='GW150914',
    detectors=['H1', 'L1', 'V1'],
    f0=141.7001
)

print(f"Network coherence: {coherence['score']:.3f}")
print(f"Phase consistency: {coherence['phase_rms']:.3f} rad")
print(f"Significance: {coherence['sigma']:.1f}σ")
```

## Statistical Rigor

### Confidence Intervals

All measurements include 95% confidence intervals:

```python
from qcal import compute_with_ci

f_peak, (f_low, f_high) = compute_with_ci(
    psd, f0=141.7001, confidence=0.95
)
print(f"f_peak = {f_peak:.4f} Hz ({f_low:.4f}, {f_high:.4f})")
```

### Bayesian Analysis

Optional Bayesian inference for robust parameter estimation:

```python
from qcal import bayesian_analysis

posterior = bayesian_analysis(
    psd, f0_prior=(141.0, 142.0, 'uniform'),
    snr_prior=(1.0, 50.0, 'log-uniform')
)

print(f"f₀ posterior: {posterior['f0_mean']:.4f} ± {posterior['f0_std']:.4f}")
print(f"Bayes factor: {posterior['log_bf']:.1f}")
```

### Multiple Testing Correction

Bonferroni correction for multiple comparisons:

```python
from qcal import bonferroni_correction

p_values = [0.01, 0.02, 0.03, 0.001, 0.05]  # 5 tests
alpha = 0.05
corrected = bonferroni_correction(p_values, alpha)

print(f"Adjusted threshold: {corrected['alpha_adj']:.4f}")
print(f"Significant tests: {corrected['significant']}")
```

## Reproducibility

### Version Control

All analysis includes version information:

```json
{
  "qcal_version": "1.0.0",
  "python_version": "3.11.5",
  "numpy_version": "1.24.3",
  "gwpy_version": "3.0.7",
  "git_commit": "a1b2c3d",
  "analysis_date": "2025-01-15T10:30:00Z"
}
```

### Random Seeds

Fixed random seeds for reproducibility:

```python
import numpy as np
np.random.seed(141700)  # Based on f₀ = 141.700 Hz
```

### Data Provenance

Track data sources and processing steps:

```json
{
  "data_source": "GWOSC",
  "data_version": "V3",
  "download_date": "2025-01-15",
  "processing_steps": [
    "bandpass_filter: 100-1000 Hz",
    "whitening: True",
    "psd_method: welch",
    "window: hann"
  ]
}
```

## Quality Assurance

### Automated Checks

```bash
# Run full validation suite
qcal validate --input results/ --checks all

# Checks include:
# - Data integrity
# - Statistical significance
# - Multi-detector consistency
# - Time-domain quality
# - Falsification tests
```

### Peer Review

Results include detailed logs for peer review:

- Raw PSD data (HDF5 format)
- Processing parameters (JSON)
- Validation criteria results (JSON)
- Figures (PNG, PDF, SVG)
- Analysis notebook (Jupyter)

## References

1. **Statistical Methods**: Bonferroni correction, Bayesian inference
2. **GW Analysis**: GWOSC tutorials, GWpy documentation
3. **QCAL Theory**: DOI [10.5281/zenodo.17445017](https://doi.org/10.5281/zenodo.17445017)

## See Also

- [Overview](overview.md) - QCAL architecture
- [CLI](cli.md) - Command-line interface
- [Roadmap](roadmap.md) - Future development
