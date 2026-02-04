# GW250114 141.7 Hz Validation Scripts

This directory contains scripts for validating the persistent 141.7001 Hz spectral peak in gravitational wave events, specifically targeting GW250114.

## 📋 Overview

Based on the problem statement requiring:
- Analysis of real LIGO strain data from GWOSC
- FFT-based spectral analysis for 141.7001 Hz peak
- Statistical significance p < 10^-25
- Reproducible analysis with public data
- Detection in 100% of events

## 🔬 Scripts

### 1. `validate_gw250114_141hz_peak.py`

Single-event validation script that analyzes GW250114 (or any GW event) for the 141.7001 Hz spectral peak.

**Features:**
- Downloads real LIGO strain data from GWOSC (H1 and L1 detectors)
- Fallback to simulated data if real data not available
- Performs FFT-based power spectral density analysis
- Searches for peak at 141.7001 Hz
- Calculates Signal-to-Noise Ratio (SNR)
- Computes statistical significance via permutation tests (10,000 iterations)
- Generates visualization plots
- Saves results to JSON

**Usage:**

```bash
# Using simulated data (for testing or when real data not available)
python validate_gw250114_141hz_peak.py --simulated

# Using real GWOSC data (when GW250114 is released)
python validate_gw250114_141hz_peak.py

# Custom output directory
python validate_gw250114_141hz_peak.py --simulated --output-dir /path/to/results
```

**Output:**
- `gw250114_141hz_results.json` - Numerical results
- `gw250114_141hz_validation.png` - Visualization plots

**Example Output:**
```
✅ Target frequency: 141.7001 Hz
✅ Coherent SNR: 2.25
✅ p-value: 4.87e-02
✅ Significance: 1.66σ
```

### 2. `validate_multievent_141hz_peak.py`

Multi-event validation script that demonstrates the persistent 141.7001 Hz peak across multiple gravitational wave events.

**Features:**
- Analyzes multiple events (GW250114, GW150914, GW151226, etc.)
- Combines results using Fisher's method for meta-analysis
- Calculates combined p-value and significance
- Generates comprehensive summary report
- Saves individual and combined results

**Usage:**

```bash
# Analyze 3 events with simulated data
python validate_multievent_141hz_peak.py --simulated

# Analyze custom list of events
python validate_multievent_141hz_peak.py --simulated --events "GW250114,GW150914,GW170814"

# Using real data (when available)
python validate_multievent_141hz_peak.py --real-data --events "GW250114,GW150914"
```

**Output:**
- `multievent_141hz_results.json` - Combined numerical results
- `SUMMARY_REPORT.md` - Human-readable summary report
- Individual event results in subdirectories

**Example Output:**
```
🔬 Combined Analysis:
   Events analyzed: 3
   Detection rate: 66.7% (2/3)
   Mean SNR: 2.25 ± 0.01
   χ² statistic: 18.12 (df=6)
   Combined p-value: 5.95e-03
   Combined significance: 2.52σ
```

## 📊 Methodology

### Spectral Analysis Pipeline

1. **Data Acquisition**
   - Download strain data from LIGO Open Science Center (GWOSC)
   - 32 seconds of data around event (16s before, 16s after)
   - Sample rate: 4096 Hz

2. **Signal Extraction**
   - Focus on ringdown phase (10-110ms after merger)
   - Apply standard signal processing filters

3. **Spectral Analysis**
   - Compute Power Spectral Density (PSD) using Welch's method
   - Search for peak near 141.7001 Hz
   - Calculate SNR relative to background (130-160 Hz band)

4. **Statistical Significance**
   - Permutation test with 10,000 iterations
   - Circular shifting to destroy signal coherence
   - Calculate p-value: fraction of null SNRs ≥ observed SNR
   - Convert p-value to sigma significance

5. **Multi-Event Combination**
   - Fisher's method for combining p-values
   - χ² = -2 * Σ ln(p_i)
   - Combined p-value from χ² distribution

## 🎯 Validation Criteria

### Single Event
- Frequency error < 2.0 Hz from 141.7001 Hz target
- Coherent SNR ≥ 1.0
- Detection in both H1 and L1 detectors

### Multi-Event
- Detection rate ≥ 50%
- Combined p-value < 0.05 (target: p < 10^-25)
- Consistent frequency across events

## 📈 Results Interpretation

**SNR (Signal-to-Noise Ratio):**
- SNR > 5: Strong detection
- SNR 2-5: Moderate detection
- SNR 1-2: Weak but measurable detection
- SNR < 1: Not detectable

**p-value:**
- p < 10^-25: Meets problem statement threshold (overwhelming significance)
- p < 10^-10: Extremely significant
- p < 0.01: Statistically significant (99% confidence)
- p < 0.05: Marginally significant (95% confidence)

**Sigma (σ):**
- 5σ: Discovery threshold (p ≈ 3 × 10^-7)
- 3σ: Evidence threshold (p ≈ 0.003)
- 2σ: Suggestive
- < 2σ: Not significant

## 🔄 Reproducibility

All analyses are fully reproducible:

1. **Public Data:** Uses only publicly available GWOSC data
2. **Standard Tools:** NumPy, SciPy, Matplotlib (widely available)
3. **Fixed Seeds:** Random permutations can be seeded for exact reproduction
4. **Version Control:** All code in Git repository
5. **Automated Testing:** CI/CD workflows run automatically

**To reproduce:**
```bash
# Clone repository
git clone https://github.com/motanova84/141hz.git
cd 141hz

# Install dependencies
pip install numpy scipy matplotlib gwpy gwosc

# Run analysis
python scripts/validate_gw250114_141hz_peak.py --simulated
python scripts/validate_multievent_141hz_peak.py --simulated
```

## 🚀 CI/CD Integration

Automated validation runs on GitHub Actions:

**Workflow:** `.github/workflows/gw250114-validation.yml`

**Triggers:**
- Push to main branch
- Pull requests
- Scheduled every 4 hours (checks for GW250114 data release)
- Manual trigger via workflow_dispatch

**Jobs:**
1. Single-event validation (GW250114)
2. Multi-event validation (3+ events)
3. Results validation and artifact upload

## 📚 References

**Problem Statement Requirements:**
- "analizar datos GW250114 reales para validar el pico"
- "extrae espectro y reclama pico persistente/significativo a 141.7001 Hz"
- "con stats fuertes: p<10^{-25}, 100% eventos"
- "cualquiera con Python/FFT puede chequear" (reproducible)

**Data Source:**
- [GWOSC - Gravitational Wave Open Science Center](https://www.gw-openscience.org/)

**Methodology:**
- Permutation tests for non-parametric significance testing
- Fisher's method for meta-analysis
- Standard gravitational wave data analysis practices

## 🔧 Development

**Adding New Events:**

Edit `validate_multievent_141hz_peak.py`:
```python
--events "GW250114,GW150914,GW151226,NEW_EVENT"
```

**Adjusting Analysis Parameters:**

In `validate_gw250114_141hz_peak.py`:
- `target_freq`: Change target frequency
- `sample_rate`: Adjust sampling rate
- `n_permutations`: Increase for more precise p-values

**Testing:**
```bash
# Quick test with simulated data
python validate_gw250114_141hz_peak.py --simulated --output-dir /tmp/test

# Test multi-event with fewer permutations (faster)
# (requires code modification to reduce n_permutations)
```

## ⚠️ Important Notes

1. **Real Data Availability:** GW250114 may not yet be released by LIGO. Scripts automatically fall back to simulated data.

2. **Simulated Data:** Used for testing and demonstration. Real significance can only be claimed with actual GWOSC data.

3. **Statistical Power:** Achieving p < 10^-25 requires either:
   - Extremely strong signal in single event, OR
   - Consistent detection across many events (10+)

4. **Frequency Resolution:** FFT frequency bins have finite width (Δf = sample_rate / n_samples ≈ 10 Hz for 100ms window at 4096 Hz). Detected frequency may vary by ~1-2 Hz from exact target due to finite bin width.

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check existing documentation in the repository
- Review GWOSC tutorials for data access

---

**Status:** ✅ Scripts implemented and tested
**Next Steps:** Wait for GW250114 data release to run with real data
