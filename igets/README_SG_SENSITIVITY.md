# Superconducting Gravimeter Sensitivity Analysis

## Overview

This module implements sensitivity analysis for **Superconducting Gravimeters (SG)** to determine optimal observation parameters for detecting gravitational signals at f₀ = 141.7001 Hz in the **testable amplitude range** of **10⁻¹³ - 10⁻¹² g**.

## Specifications

### Superconducting Gravimeter (SG) Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| σ_single | 10⁻¹¹ g | Single-sample noise level @ 1 Hz |
| f_sampling | 1 Hz | Sampling frequency |
| f_target | 141.7001 Hz | Target signal frequency |

## Amplitude Analysis

### Case 1: A = 10⁻¹² g

For an amplitude of **A = 10⁻¹² g** with target **SNR = 5**:

```
σ_required = A / SNR = 10⁻¹² / 5 = 2×10⁻¹³ g

N_samples = (σ_single / σ_required)²
          = (10⁻¹¹ / 2×10⁻¹³)²
          = (50)²
          = 2,500 samples

Time = N_samples / f_sampling
     = 2,500 s
     ≈ 42 minutes ✅
```

**Conclusion**: Highly feasible with short observation time.

### Case 2: A = 10⁻¹³ g

For an amplitude of **A = 10⁻¹³ g** with target **SNR = 5**:

```
σ_required = A / SNR = 10⁻¹³ / 5 = 2×10⁻¹⁴ g

N_samples = (σ_single / σ_required)²
          = (10⁻¹¹ / 2×10⁻¹⁴)²
          = (500)²
          = 250,000 samples

Time = N_samples / f_sampling
     = 2.5×10⁵ s
     ≈ 2.9 days ✅
```

**Conclusion**: Feasible with ~3 days of continuous observation.

## Feasibility with IGETS Network

Both amplitude levels are **FEASIBLE** with the current IGETS network:

| Amplitude | N_samples | Time | Feasibility |
|-----------|-----------|------|-------------|
| 10⁻¹² g | 2,500 | ~42 minutes | ✅ Highly feasible |
| 10⁻¹³ g | 250,000 | ~3 days | ✅ Feasible |

The IGETS network operates continuously and can maintain stable measurements over extended periods, making both observation durations practical.

## Usage

### Basic Analysis

```python
from igets.sg_sensitivity_analysis import SGSensitivityAnalyzer

# Create analyzer with default SG specifications
analyzer = SGSensitivityAnalyzer()

# Analyze specific amplitude
analyzer.print_analysis(amplitude=1e-12, target_snr=5.0)

# Analyze amplitude range
results = analyzer.analyze_amplitude_range(
    amplitude_min=1e-13,
    amplitude_max=1e-12,
    n_points=10,
    target_snr=5.0
)

# Generate sensitivity plots
analyzer.plot_sensitivity_curves(
    amplitude_range=(1e-14, 1e-11),
    target_snr=5.0,
    output_file='sg_sensitivity_curves.png'
)
```

### Command Line

Run the complete analysis:

```bash
cd igets
python3 sg_sensitivity_analysis.py
```

This will:
1. Analyze both test cases (10⁻¹³ and 10⁻¹² g)
2. Generate range analysis
3. Create sensitivity curve plots
4. Save results to `igets_results/`

### Testing

Run the test suite:

```bash
cd igets
python3 test_sg_sensitivity_analysis.py
```

The tests verify:
- Correct noise level calculations
- Sample size requirements matching problem statement
- Observation time calculations
- Feasibility assessments
- Compliance with exact specifications

## Mathematical Background

### Signal-to-Noise Ratio

The SNR for a measurement is defined as:

```
SNR = A / σ
```

where:
- A is the signal amplitude
- σ is the noise level

### Noise Reduction by Averaging

When averaging N independent measurements, the noise decreases as:

```
σ_averaged = σ_single / √N
```

### Required Samples Calculation

To achieve a target SNR with amplitude A:

```
SNR = A / σ_averaged = A / (σ_single / √N)

Solving for N:
N = (σ_single × SNR / A)² = (σ_single / σ_required)²
```

where `σ_required = A / SNR`.

### Observation Time

The observation time is simply:

```
T = N_samples / f_sampling
```

For f_sampling = 1 Hz, T = N_samples (in seconds).

## Integration with IGETS Network

### IGETS Stations

The International Geodynamics and Earth Tide Service (IGETS) operates a global network of superconducting gravimeters at locations including:

- **Cantley, Canada** (45.59°N, 75.87°W)
- **Bad Homburg, Germany** (50.23°N, 8.61°E)
- **Kyoto, Japan** (35.03°N, 135.78°E)
- **Strasbourg, France** (48.62°N, 7.68°E)
- **Membach, Belgium** (50.61°N, 6.01°E)

### Multi-Station Coherence

For robust detection, the analysis should be performed across multiple stations to verify:

1. **Signal consistency**: Same frequency detected at all stations
2. **Phase coherence**: Correlated phase relationships
3. **Global coverage**: Independent confirmation across different locations

See `igets_fft_analysis.py` for multi-station coherence analysis.

## References

1. **Problem Statement**: Amplitude adjustment to testable range
2. **IGETS Network**: http://igets.u-strasbg.fr/
3. **SG Technology**: Superconducting gravimeter specifications
4. **GQN Model**: Gravitational Quantum Noetic framework (PAPER.md)

## Output Files

Running the analysis generates:

- `igets_results/sg_sensitivity_curves.png`: Sensitivity vs amplitude plots
- Console output with detailed calculations
- Test results with verification of problem statement compliance

## Conclusion

The amplitude range **10⁻¹³ - 10⁻¹² g** is fully testable with current IGETS superconducting gravimeter technology. Both limiting cases require reasonable observation times:

- **Upper bound** (10⁻¹² g): 42 minutes
- **Lower bound** (10⁻¹³ g): 3 days

These durations are well within the operational capabilities of the IGETS network, confirming the **feasibility** of experimental detection in this amplitude range.
