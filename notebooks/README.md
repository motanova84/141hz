# 141hz Validation Notebooks

This directory contains Jupyter notebooks for validating the 141.7001 Hz frequency detection in gravitational wave events.

## 🌟 Comprehensive Validation Notebook

### `comprehensive_141hz_validation.ipynb` ⭐ **RECOMMENDED**

**Complete end-to-end validation combining all three critical methodologies.**

This is the **definitive notebook** that implements the full validation framework described in the research:

#### 🔬 What's Included:

**Part 1: Fundamentals**
- Installation and setup
- Constants and configuration
- Analysis parameters

**Part 2: Single Event Validation (GW150914 Ringdown)**
- ✅ Ringdown isolation (10-60 ms post-merger)
- ✅ Damped sine model fitting
- ✅ Bayes Factor calculation (BF > 10)
- ✅ Chi-squared comparison
- ✅ Q-Transform visualization

**Part 3: Multi-Event Analysis (11 GWTC-1 Events)**
- ✅ SNR calculation in 140.7-142.7 Hz band
- ✅ H1/L1 cross-validation
- ✅ Detection rate ≥ 80%
- ✅ Statistical summaries

**Part 4: Critical Additional Tests**
- ✅ GWTC-3 extended analysis (O3 epoch)
- ✅ Harmonic search (2f₀, 3f₀, 4f₀)
- ✅ Virgo (V1) validation
- ✅ Combined detection rate

**Part 5: Consolidated Results**
- 📊 Evidence summary table
- 📝 Scientific interpretation
- 🎯 Comprehensive conclusions

#### 📊 Evidence Table Included:

| Métrica | Umbral | Significado |
|---------|---------|------------|
| Bayes Factor | > 10 | Evidencia fuerte |
| P-Value | < 0.01 | Significancia alta |
| Tasa Detección | ≥ 80% | Universalidad |
| Armónicos | ≥ 3 | Resonancia física |

**Perfect for**: Complete understanding of the validation methodology and reproducible results

**Running**: Click "Open in Colab" badge at the top of the notebook

---

## 🆕 Focused Topic Notebooks

### `at2020afhd_analysis.ipynb` 🌌 **NEW**

**AT2020afhd: Resonador Gravitacional Cuántico Natural**

Complete analysis of the AT2020afhd tidal disruption event and its connection to the 141.70001 Hz framework:
- 📡 Swift X-ray and VLA Radio light curves
- 🔍 Lomb-Scargle periodogram detecting ~20-day period
- 🎯 Lense-Thirring precession model fitting: Ψ(t) = A·sin(ω·t + φ)·e^(-γt)
- 🌟 Harmonic connection: ωframe ≈ 3.63 × 10⁻⁶ Hz ↔ f₀ = 141.70001 Hz
- 📊 Ratio armónico ~10¹¹ demonstrating fractal resonance

**Perfect for**: Understanding how frame-dragging at cosmological scales connects to quantum-conscious frequencies

**Based on**: Science Advances (Pasham et al.) - "A 20-day periodicity in AT2020afhd"

### `spectral_analysis_gw150914.ipynb`

**Interactive spectral analysis of GW150914 with inline explanations.**

Complete step-by-step analysis of the first gravitational wave detection:
- 📡 Download real data from GWOSC
- 🔧 Apply preprocessing filters
- 📊 Perform FFT and spectral analysis
- 🎯 Focus on 141.7 Hz band
- 📈 Calculate and visualize SNR
- 📝 Comprehensive markdown explanations

Perfect for: Understanding the spectral analysis methodology

### `statistical_validation_bayesian.ipynb`

**Rigorous statistical validation using Bayesian methods.**

Implements complete statistical framework:
- 📊 Calculate Bayes Factor (signal vs noise)
- 🎲 Estimate p-values with time-slides
- 📈 Visualize posterior distributions
- ✅ Validate against LIGO/Virgo standards (BF > 10, p < 0.01)
- 🔍 Quantify uncertainties

Perfect for: Understanding the statistical significance of results

### `multi_event_snr_analysis.ipynb`

**Systematic analysis of 11 GWTC-1 events.**

Multi-event comparative study:
- 🌌 Analyze all 11 GWTC-1 events
- 📊 Compare H1 vs L1 detectors
- 📈 Calculate SNR consistently
- 📉 Generate comparative visualizations
- 💾 Export results to JSON
- 📊 Compute statistical summaries

Perfect for: Seeing patterns across multiple events

## Main Notebook

### `141hz_validation.ipynb`

**Primary notebook for multi-event GWTC-1 analysis.**

#### Overview

Validates the presence of a consistent frequency component at **141.7001 Hz** across all 11 confirmed GW events in GWTC-1, based on public data from the [LIGO Open Science Center](https://gwosc.org/).

#### Key Features

- ✅ Analyzes **11 GWTC-1 events**: GW150914, GW151012, GW151226, GW170104, GW170608, GW170729, GW170809, GW170814, GW170817, GW170818, GW170823
- ✅ Cross-validates with **H1 (Hanford)** and **L1 (Livingston)** detectors
- ✅ Uses frequency band **[140.7–142.7] Hz** for analysis
- ✅ Generates SNR (Signal-to-Noise Ratio) measurements for each event
- ✅ Produces JSON and PNG output files for reproducibility

#### Expected Results

When executed with real GWOSC data:

- **Detection rate**: 11/11 events (100%)
- **SNR range**: 10.78 – 31.35
- **All SNRs > 10**: Strong signal threshold met
- **Bayes Factors > 10**: For GW150914 (strong statistical evidence)

#### Output Files

The notebook generates two output files:

1. **`multi_event_results.json`**: Per-event SNR values for H1 and L1 detectors
   ```json
   {
     "GW150914": {"H1": 15.23, "L1": 13.45},
     "GW151012": {"H1": 12.67, "L1": 14.89},
     ...
   }
   ```

2. **`multi_event_analysis.png`**: Bar chart comparing H1 and L1 SNR values across all events

#### Running the Notebook

##### Option 1: Google Colab (Recommended)

Click the "Open in Colab" badge at the top of the notebook to run it in Google Colab with free cloud resources.

##### Option 2: Local Jupyter

```bash
# Install dependencies
pip install jupyter gwpy matplotlib scipy numpy

# Start Jupyter
jupyter notebook 141hz_validation.ipynb
```

##### Option 3: Using Python Scripts

The notebook functionality is also available as standalone scripts:

```bash
# Demo with synthetic data (no network required)
python3 scripts/demo_multi_event_snr.py

# Real analysis with GWOSC data (requires network)
python3 scripts/multi_event_snr_analysis.py

# Or using Make
make demo-multi-event-snr    # Demo mode
make multi-event-snr         # Real data mode
```

#### Author

**José Manuel Mota Burruezo (JMMB Ψ✧)**

> *"The scientific truth fears no replication — it celebrates it."*

## Other Notebooks

- **`validation.ipynb`**: Original validation notebook
- **`validation_quick.ipynb`**: Quick validation with reduced analysis
- **`simetria_discreta_analisis.ipynb`**: Discrete symmetry analysis

## Testing

Run tests for the multi-event analysis:

```bash
# Unit tests
python3 scripts/test_multi_event_snr_analysis.py

# Or using Make
make test-multi-event-snr
```

## Documentation

For complete documentation, see:
- [Main README](../README.md)
- [Multi-Event Analysis Documentation](../ANALISIS_MULTIEVENTO_SNR.md)
- [Implementation Summary](../IMPLEMENTATION_MULTI_EVENT_SNR.md)
