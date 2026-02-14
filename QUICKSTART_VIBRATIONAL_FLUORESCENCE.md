# Quick Start Guide: Vibrational Fluorescence Measurement

## Installation

```bash
pip install -r requirements.txt
```

## 1-Minute Quick Start

```python
from modules.quantum_biology import run_fluorescence_experiment

# Run complete QCAL validation
results = run_fluorescence_experiment(verbose=True)

# Check if QCAL is confirmed
print(f"QCAL Confirmed: {results['summary']['qcal_confirmed']}")
```

## 5-Minute Tutorial

### Basic Experiment

```python
from modules.quantum_biology.core.vibrational_fluorescence import (
    VibrationalFluorescenceSystem,
    FluorescenceConfig
)

# Create system with default parameters
system = VibrationalFluorescenceSystem()

# Generate modulated signal at 2 Hz
t, signal = system.generate_modulated_signal(f_mod=2.0)

# Calculate fluorescence response
fluorescence, metrics = system.calculate_fluorescence_response(2.0)

print(f"Response amplitude: {metrics['delta_f']:.4f}")
print(f"Efficiency η: {metrics['eta']:.4f}")
print(f"SNR: {metrics['snr']:.2f}")
```

### Frequency Sweep

```python
# Perform complete frequency sweep
results = system.perform_frequency_sweep(include_qcal=True)

# Access results
frequencies = results['frequencies']
response_amplitudes = results['delta_f']
efficiencies = results['eta']
phases = results['phase']
```

### Statistical Validation

```python
# Get QCAL and null hypothesis results
results_qcal = system.perform_frequency_sweep(include_qcal=True)
results_null = system.perform_frequency_sweep(include_qcal=False)

# Perform ANOVA statistical test
anova = system.calculate_spectral_anova(results_qcal, results_null)

print(f"F-statistic: {anova['f_statistic']:.2f}")
print(f"p-value: {anova['p_value']:.2e}")
print(f"Decision: {anova['significance']}")
```

### Custom Configuration

```python
# Create custom experimental configuration
config = FluorescenceConfig(
    f0=141.7001,           # Carrier frequency (Hz)
    f_mod_min=0.1,         # Min modulation frequency (Hz)
    f_mod_max=10.0,        # Max modulation frequency (Hz)
    f_mod_steps=100,       # Number of frequency steps
    sampling_rate=10000.0, # Sampling rate (Hz)
    duration=10.0,         # Measurement duration (s)
    psi_critical=0.888,    # QCAL critical threshold
    alpha=0.001            # Statistical significance level
)

system = VibrationalFluorescenceSystem(config)
```

## Run Demo Script

```bash
cd /home/runner/work/141hz/141hz
PYTHONPATH=. python examples/demo_vibrational_fluorescence.py
```

This generates:
- `fluorescence_demo_signals.png` - Modulated carrier signals
- `fluorescence_demo_response.png` - Frequency response analysis
- `fluorescence_demo_timeseries.png` - Time-series measurements
- `fluorescence_demo_coherence.png` - Coherence analysis
- `fluorescence_demo_resonance.png` - Protein domain resonance

## Run Tests

```bash
pytest modules/quantum_biology/tests/test_vibrational_fluorescence.py -v
```

## Key Metrics

| Metric | QCAL Prediction | Null Hypothesis |
|--------|----------------|-----------------|
| Response ratio (141.7/100 Hz) | > 1.5 | ≈ 1.0 |
| Resonance peaks | At f₀/n | No peaks |
| Coherence | > 0.7 | < 0.5 |
| Effect size | > 2.0 | ≈ 1.0 |

## Expected QCAL Resonances

- 141.7 Hz (n=1) - Fundamental
- 70.85 Hz (n=2) - First harmonic
- 47.23 Hz (n=3) - Second harmonic
- 10.9 Hz (n=13) - Magicicada resonance
- 8.3 Hz (n=17) - Magicicada resonance

## For More Information

See: `modules/quantum_biology/VIBRATIONAL_FLUORESCENCE_README.md`
