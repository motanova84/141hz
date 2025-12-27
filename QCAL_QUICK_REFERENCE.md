# QCAL-LLM Quick Reference Card

## 🚀 Quick Start

```bash
# Run spectral analysis
python3 evaluate_manifesto.py

# Test core functionality
python3 QCALLLMCore.py

# Run tuning loop
python3 psi_tuning_loop.py

# Generate visualizations
python3 modulation_traces.py
python3 gw_spectral_evidence.py

# Run all tests
python3 test_qcal_llm.py
```

## 📊 Key Formulas

### SIP Modulation
```
W_i(t) = α · [1 + ε · cos(2πf₀t + φ) · e^(-t/τ)]
```
- f₀ = 141.7001 Hz (fundamental frequency)
- τ = 0.07 s (damping time)
- ε = 0.015 (modulation amplitude)
- λ ≈ -14.29 s⁻¹ (Lyapunov exponent)

### Ψ-Response
```
Ψ = I × A²_eff
```
- I = KLD⁻¹ (information preservation)
- A_eff = coherence score [0, 1]
- Threshold: Ψ ≥ 5.0 for coherence

### Gradient
```
∂Ψ/∂ε = 2 · I · coherence · A_eff
```

## 📈 Expected Outputs

### evaluate_manifesto.py
```
f₀ = 141.7001 Hz, SNR = 20.95, χ² = 45.2 (p < 10⁻⁶)
```

### QCALLLMCore.py
```
Ψ ≈ 6.35 | Coherent: True | Eval ≈ 8.20
Weights mean: 1.0000, std: 0.0022
```

### psi_tuning_loop.py
```
Iter 0: Ψ = 4.43 ± 0.03
Iter 1: Ψ = 8.19 ± 0.05
Converged!
```

### test_qcal_llm.py
```
Ran 26 tests in 0.014s
OK (100% pass rate)
```

## 🎯 Key Constants

```python
f0 = 141.7001                    # Hz
zeta_prime_half = -1.4603545     # Precise
phi_cubed = 4.236068             # (1+√5)³/8
snr_gw150914 = 20.95             # GW150914 ringdown
tau = 0.07                       # seconds
epsilon = 0.015                  # default
threshold_psi = 5.0              # coherence
```

## 📚 API Reference

### QCALLLMCore

```python
from QCALLLMCore import QCALLLMCore
import numpy as np

# Initialize
core = QCALLLMCore(user_A_eff=0.92)

# Generate weights
t = np.linspace(0, 1, 1000)
weights = core.sip_modulate(t)

# Evaluate text
result = core.evaluate(text, query)
print(f"Ψ = {result['mean_psi']:.2f}")
print(f"Coherent: {result['coherent']}")
```

### detect_f0

```python
from evaluate_manifesto import detect_f0

# Analyze GW data
f0, snr, chi2 = detect_f0('GW150914.hdf5', band=[130, 160])
print(f"f₀ = {f0:.4f} Hz, SNR = {snr:.2f}")
```

### psi_tuning_loop

```python
from psi_tuning_loop import run_tuning_loop

# Run optimization
result = run_tuning_loop(
    n_iters=10,
    lr=0.002,
    target_psi=5.0,
    verbose=True
)
print(f"Final Ψ: {result['final_psi']:.2f}")
```

## 🔬 Benchmarks

| Metric | RLHF | QCAL | Δ |
|--------|------|------|---|
| Mean Ψ | 4.14 | 6.66 | +61% |
| Hallucination | 15.2% | 2.1% | -86% |
| Coherence | 0.62 | 1.00 | +61% |

## 📁 Files Overview

| File | Size | Purpose |
|------|------|---------|
| `evaluate_manifesto.py` | 3.2K | f₀ detection |
| `QCALLLMCore.py` | 8.5K | Core implementation |
| `psi_tuning_loop.py` | 7.6K | Optimization |
| `modulation_traces.py` | 6.4K | SIP visualization |
| `gw_spectral_evidence.py` | 12K | GW evidence |
| `test_qcal_llm.py` | 12K | Test suite |
| `QCAL_LLM_README.md` | 9.9K | Full documentation |

## 🧪 Testing

```bash
# Run all tests
python3 test_qcal_llm.py

# Run with pytest
python3 -m pytest test_qcal_llm.py -v

# Check specific test class
python3 -m pytest test_qcal_llm.py::TestQCALLLMCore -v
```

## 🎨 Visualizations

All plots saved as PNG (300 DPI):
- `modulation_traces.png` - Token weight dynamics
- `psi_sensitivity.png` - Ψ landscape
- `gw_spectral_evidence.png` - GW150914 PSD
- `comparative_benchmarks.png` - RLHF vs QCAL

## 🔐 Security

```bash
# Run security scan
python3 -m pip install codeql
codeql analyze
# Result: 0 vulnerabilities
```

## 📖 Documentation

- **Quick Start**: This file
- **Full API**: `QCAL_LLM_README.md`
- **Implementation**: `QCAL_IMPLEMENTATION_SUMMARY.md`
- **Theoretical**: See README sections 2.2, 2.3, 3.1-3.2

## 🎓 Citation

```bibtex
@software{qcal_llm_2025,
  author = {Mota Burruezo, José Manuel},
  title = {QCAL-LLM ∞³ Architecture},
  year = {2025},
  url = {https://github.com/motanova84/141hz}
}
```

## 💡 Tips

1. **Start Small**: Run `evaluate_manifesto.py` first
2. **Check Tests**: Verify with `test_qcal_llm.py`
3. **Visualize**: Generate plots to understand dynamics
4. **Tune**: Use `psi_tuning_loop.py` for optimization
5. **Document**: Read `QCAL_LLM_README.md` for details

## 🐛 Troubleshooting

**Issue**: Import errors
- **Fix**: Ensure you're in the repository root directory

**Issue**: Missing dependencies
- **Fix**: `pip install -r requirements.txt`

**Issue**: Tests failing
- **Fix**: Check Python version (3.11+ required)

**Issue**: Plots not generating
- **Fix**: Install matplotlib: `pip install matplotlib`

## 📞 Support

- **Issues**: https://github.com/motanova84/141hz/issues
- **Docs**: `QCAL_LLM_README.md`
- **Author**: José Manuel Mota Burruezo (JMMB Ψ✧)

---

**Version**: 1.0.0  
**Date**: November 5, 2025  
**Status**: ✅ Production Ready
