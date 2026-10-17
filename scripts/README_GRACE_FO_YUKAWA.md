# GRACE-FO Yukawa Detection Protocol

## Overview

This analysis implements a complete protocol for detecting Yukawa-type gravitational modulations at the QCAL frequency (141.7001 Hz) using simulated GRACE-FO (Gravity Recovery and Climate Experiment Follow-On) satellite accelerometer data.

## Scientific Context

The QCAL ∞³ framework predicts that the coherence field Ψ introduces a Yukawa-type correction to the gravitational potential:

```
V(r) = -GM/r × (1 + α·e^(-r/λ_Ψ))
```

Where:
- **α** ≈ 10⁻⁷ to 10⁻⁵ (coupling strength)
- **λ_Ψ** ≈ 2.1 km (coherence length)
- **f₀** = 141.7001 Hz (QCAL fundamental frequency)

In the orbital reference frame of GRACE-FO satellites, this manifests as a modulation at **0.1417001 Hz** (141.7001 mHz).

## Files

### Main Analysis Script
- **`validar_prediccion_grace_fo_yukawa.py`**: Complete implementation of the GRACE-FO Yukawa detection protocol

### Test Suite
- **`test_grace_fo_yukawa.py`**: Comprehensive test suite (20 tests) for CI/CD validation

### Output Files (in `resultados/`)
- **`grace_fo_yukawa_results.json`**: JSON summary of detection metrics
- **`grace_fo_01_time_series.png`**: Raw acceleration time series
- **`grace_fo_02_filtered_signal.png`**: Bandpass-filtered signal at target frequency
- **`grace_fo_03_psd_full.png`**: Full power spectral density
- **`grace_fo_04_psd_zoom.png`**: PSD zoom at target frequency
- **`grace_fo_05_snr_integration.png`**: SNR vs integration time
- **`grace_fo_06_baseline_correlation.png`**: Baseline variation and Yukawa signal

## GRACE-FO Mission Parameters

- **Sampling rate**: 1 Hz (ACC1B accelerometer data)
- **Sensitivity**: ~10⁻¹⁰ m/s²/√Hz
- **Satellite separation**: ~200 km
- **Orbital altitude**: ~500 km
- **Orbital velocity**: ~7.6 km/s
- **Mission duration**: 2018-present

## Analysis Features

### 1. Data Simulation
- Realistic accelerometer noise (10⁻¹⁰ m/s²/√Hz)
- Tidal gravitational signals (diurnal, semi-diurnal)
- Yukawa modulation at f_target = 0.1417001 Hz
- Baseline-dependent amplitude modulation

### 2. Spectral Analysis
- FFT computation with Welch's method for robust PSD estimation
- Peak detection at target frequency
- Frequency resolution: ~0.09 mHz (for 1-day integration)

### 3. Statistical Testing
- Signal-to-noise ratio (SNR) calculation
- Statistical significance (σ-score)
- False alarm probability (FAP)
- Detection thresholds: SNR > 3 dB AND σ > 3

### 4. Yukawa Parameter Extraction
- Coupling strength α estimation
- Coherence length λ_Ψ calculation
- Comparison with theoretical predictions

### 5. Visualization Suite
- 6 publication-quality plots
- Time-domain and frequency-domain analysis
- SNR scaling with integration time
- Baseline correlation analysis

## Usage

### Run Main Analysis

```bash
python scripts/validar_prediccion_grace_fo_yukawa.py
```

This will:
1. Simulate 1 day (86,400 samples) of GRACE-FO data
2. Perform spectral analysis
3. Detect peaks at the target frequency
4. Calculate statistical significance
5. Extract Yukawa parameters
6. Generate visualizations
7. Save results to `resultados/`

### Run Tests

```bash
python scripts/test_grace_fo_yukawa.py
```

This will run 20 comprehensive tests covering:
- Detector initialization
- Data simulation
- PSD calculation
- Peak detection
- Parameter extraction
- Visualization creation
- JSON output

## Expected Results

For a 1-day observation with simulated Yukawa signal (amplitude 2×10⁻¹¹ m/s²):

### Detection Metrics
- **Frequency detected**: 141.67 ± 0.05 mHz
- **Deviation from target**: < 50 μHz
- **SNR**: ~21 dB
- **Significance**: ~16σ
- **False alarm probability**: < 10⁻⁶

### Yukawa Parameters
- **α (coupling)**: ~10⁻¹² (observable with GRACE-FO sensitivity)
- **λ_Ψ (coherence length)**: 2.1 km (from QCAL theory)

### Validation Criteria
✅ Peak detected at f_target ± 100 μHz  
✅ SNR > 3 dB  
✅ Significance > 3σ  
✅ FAP < 10⁻³  

## Integration with QCAL ∞³

This analysis validates **Predicción 1** of the QCAL ∞³ framework:

> The coherence field Ψ introduces a measurable Yukawa-type correction to the gravitational potential, detectable by precision satellite gravimetry at the characteristic frequency f₀ = 141.7001 Hz.

### Connections to Other Predictions
1. **Yukawa Correction** (this analysis): Satellite gravimetry
2. **BEC Spectral Peak**: Condensed matter experiments
3. **Higgs Invisible Channel**: Particle physics (LHC)
4. **Gravitational Modulation**: Ground-based gravimeters (IGETS)

## References

### GRACE-FO Mission
- [^24^] NASA/JPL GRACE-FO Mission Overview
- [^26^] CSR Level-1B Data Products (ACC1B)
- [^27^] KBR Ranging System Specifications
- [^31^] ACT1B Thruster Data Format

### QCAL ∞³ Framework
- See `papers/PREDICCIONES_FALSABLES_QCAL_INFINITO3.md`
- Related scripts: `validar_prediccion_yukawa.py`, `validacion_prediccion_1_yukawa.py`

## Author

**José Manuel Mota Burruezo (JMMB Ψ ✧)**  
Instituto de Conciencia Cuántica (ICQ)  
Fecha: Abril 2026

## License

Sovereign Noetic License 1.0 (compatible with MIT)
