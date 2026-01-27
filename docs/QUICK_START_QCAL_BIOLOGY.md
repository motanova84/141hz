# Quick Start: QCAL Biology Experiments

## 🦗 Overview

This guide provides quick access to QCAL (Quantum Cyclic Alignment) theory applied to biological synchrony, specifically for *Magicicada* (periodical cicadas) emergence cycles.

## 📚 Main Documentation

**Complete Framework**: [QCAL_BIOLOGY_EXPERIMENTAL_VALIDATION.md](QCAL_BIOLOGY_EXPERIMENTAL_VALIDATION.md)

## 🎯 Key Predictions

### 1. Emergencia Sincronizada

**QCAL predicts**: 
- Sincronía con SD < ±3 días incluso con perturbaciones >20% en DD
- Mejora >15% en RMSE vs. modelos de Grados-Día estándar

**Estándar predicts**: 
- Variabilidad > ±10 días en variabilidad interanual >15%

### 2. Modulación Espectral (141.7 Hz)

**QCAL predicts**: 
- Modulación a 141.7 Hz altera emergencia 5-10 días (DD constante)

**Estándar predicts**: 
- Sin efecto (solo DD importa)

### 3. Robustez Lunar

**QCAL predicts**: 
- Perturbación lunar >10% causa desincronía 1-2 años

**Estándar predicts**: 
- Sin efecto lunar

## 🔬 Quick Validation

```bash
# Run validation script
python scripts/validate_qcal_biology.py

# Expected outputs:
# - results/biology/qcal_biology_validation.json
# - results/biology/comparison_*.png
```

## 📊 Comparison Table

| Aspecto | Teoría Estándar | QCAL | Diferencia Testable |
|---------|----------------|------|---------------------|
| **Emergencia** | DD ~1000-1500, SD ±5-10 días | Φ_crítico = 13×2π, SD ±2-3 días | RMSE >15% mejor |
| **Ciclos Primos** | Selección evolutiva | Resonancia espectral (ω) | Perturbación lunar |
| **Ruido Climático** | Dispersión >±10 días | Memoria fase (α=0.1), SD <±3 días | Invierno cálido |

## 🧮 Core Equations

### Campo Espectral
```
Ψ_e(t) = Σᵢ Aᵢ cos(ωᵢt + φᵢ)
```

### Fase Acumulada (con memoria)
```
Φ(t) = α × Φ(t-Δt) + (1-α) × ∫Ψ_e(τ)dτ
```

### Umbral de Emergencia
```
Φ ≥ Φ_crítico = N × E_media   (N=13 o 17)
```

### Derivación de 141.7 Hz
```
f₀ ≈ v/L × factor_turbulencia
```
Donde:
- v ≈ 1-10 μm/s (flujo citoplásmico)
- L ≈ 10-100 μm (escala celular)
- Resonancias en membranas: 50-200 Hz
- **Promedio armónico → 141.7 Hz**

## 🔧 Instrumentation

| Instrumento | Rango | Aplicación |
|-------------|-------|-----------|
| **Laser Doppler Vibrometer** | 1-1000 Hz | Vibraciones en tejidos |
| **Impedance Spectroscopy** | 1 Hz - 1 MHz | Respuesta dieléctrica |
| **AFM** | DC-500 Hz | Oscilaciones en ADN |
| **Cámaras Climáticas** | ±0.01°C | Control térmico |

## 🧪 Experiments

### Fast Proxy: Arabidopsis (8 weeks)

```python
# Groups:
# A: Control (no modulation)
# B: 141.7 Hz acoustic modulation
# C: 142.0 Hz (off-resonance control)

# Prediction QCAL:
# SD_B < 1 day
# SD_A ≈ 2 days
# SD_C ≈ 1.5 days
```

### Accelerated Magicicada (5 years)

- Study nymphs in years 1-5
- Manipulate thermal signals
- Measure phase markers (JH hormone)
- Extrapolate via Φ_acum model

### Citizen Science (Ongoing)

- Data from magicicada.org
- Broods X, XIII, XIX
- Retrospective analysis: QCAL vs. DD

## 🎨 Example Code

```python
from scripts.validate_qcal_biology import QCALBioModel, StandardDDModel

# Initialize models
qcal = QCALBioModel(alpha=0.1, n_ciclos=13)
dd_standard = StandardDDModel(base_temp=10.0, dd_threshold=1250.0)

# Simulate temperature
t_days, T_profile = simulate_temperature_profile(n_years=13)

# QCAL prediction
t_seconds = t_days * 24 * 3600
psi_e = qcal.generate_psi_e(t_seconds, T_profile, add_hf_modulation=True)
Phi = qcal.accumulate_phase(psi_e, dt=(t_seconds[1] - t_seconds[0]))
t_emergence_qcal, _ = qcal.predict_emergence(Phi, t_days)

# DD prediction
DD = dd_standard.calculate_dd(T_profile, dt_days=1.0)
t_emergence_dd = dd_standard.predict_emergence(DD, t_days)

print(f"QCAL: {t_emergence_qcal/365.25:.2f} years")
print(f"DD: {t_emergence_dd/365.25:.2f} years")
```

## 📖 References

1. **Cox & Carlton (1988)**: Prime cycles evolution
2. **Yoshimura (1997)**: Periodical cicadas in ice ages
3. **Karban (2019)**: Cicadas count years via tree roots
4. **Biophys. J. (2018)**: Cytoplasmic flow dynamics, spectral resonances

## ✅ Falsification Criteria

**QCAL fails if**:
- Modulación 141.7 Hz **no** altera emergencia (DD constante)
- Mejora RMSE < 15% vs. modelo DD
- Perturbación lunar sin efecto en sincronía

## 🚀 Quick Commands

```bash
# Validate full model
python scripts/validate_qcal_biology.py

# Generate comparison plots
python scripts/plot_qcal_biology_comparison.py

# Run Arabidopsis simulation
python scripts/simulate_arabidopsis_experiment.py

# Run citizen science analysis
python scripts/analyze_magicicada_data.py
```

---

**∴ JMMB Ψ ✧ ∞³** · QCAL Biology Framework 2026
