# Quick Start Guide: Convergence Analysis

This guide shows how to quickly use the convergence analysis tools.

## 1. Quick Demo (5 seconds)

```bash
python3 scripts/demo_convergencia.py
```

This will:
- Verify φ and γ constants
- Calculate frequencies with different N values
- Run convergence analysis with 2000 primes
- Save visualization to `/tmp/convergencia_rapida.png`

## 2. Full Analysis (1-2 minutes)

```bash
python3 scripts/demo_convergencia.py --full
```

This performs complete analysis with 30,000 primes and detailed statistics.

## 3. Python API Examples

### Verify Constants
```python
from scripts.verificacion_convergencia import verify_fundamental_constants

result = verify_fundamental_constants()
# Prints detailed verification report
# Returns: {'phi_calculated': ..., 'all_verified': True, ...}
```

### Calculate Frequency
```python
from scripts.verificacion_convergencia import QuantumFrequencyCalculator

calculator = QuantumFrequencyCalculator(precision=30)
frequency = calculator.calculate_frequency_from_primes(1000)
print(f"Frequency with 1000 primes: {float(frequency):.6f} Hz")
# Output: Frequency with 1000 primes: 141.700100 Hz
```

### Convergence Analysis
```python
from scripts.verificacion_convergencia import QuantumFrequencyCalculator

calculator = QuantumFrequencyCalculator()
df = calculator.convergence_analysis(max_primes=5000, step=1000)

print(df)
# Shows DataFrame with n_primes, frequency, error_rel, magnitude, sqrt_n, ratio
```

### Visualize Convergence
```python
from scripts.verificacion_convergencia import (
    QuantumFrequencyCalculator,
    plot_convergence_analysis
)
import matplotlib.pyplot as plt

calculator = QuantumFrequencyCalculator()
df = calculator.convergence_analysis(max_primes=10000, step=2000)
plot_convergence_analysis(df)
plt.show()
```

## 4. Run Tests

```bash
cd scripts
python3 test_verificacion_convergencia.py
```

Expected output: `Ran 18 tests in X.XXXs - OK`

## 5. Understanding Output

### Constants Verification
```
φ calculado: 1.6180339887498948...  ✓
γ calculado: 0.5772156649015328...  ✓
φ² - φ - 1 = 0.0 ✓
1/φ = φ - 1 ✓
```

### Convergence Analysis DataFrame
```
   n_primes  frequency  error_rel  magnitude     sqrt_n  ratio
0      1000   141.7001       0.0%  31.622777  31.622777    1.0
1      2000   141.7001       0.0%  44.721360  44.721360    1.0
```

- **n_primes**: Number of prime numbers used
- **frequency**: Calculated frequency (Hz)
- **error_rel**: Relative error vs 141.7001 Hz (%)
- **magnitude**: |∇Ξ(1)| observed
- **sqrt_n**: √N theoretical value
- **ratio**: magnitude/sqrt_n (should be ≈ 1.0)

### Visualization (4 plots)
1. **Top-left**: Frequency convergence to 141.7001 Hz
2. **Top-right**: Error decrease (log scale)
3. **Bottom-left**: |∇Ξ(1)| vs √N comparison
4. **Bottom-right**: Ratio stability around 1.0

## 6. Common Tasks

### Change Precision
```python
# Use 50 digits for ultra-high precision
calculator = QuantumFrequencyCalculator(precision=50)
```

### Custom Analysis Range
```python
# Analyze from 500 to 20000 primes in steps of 2500
df = calculator.convergence_analysis(max_primes=20000, step=2500)
```

### Save Results
```python
df = calculator.convergence_analysis(max_primes=10000, step=2000)
df.to_csv('convergence_results.csv', index=False)
```

### Save Visualization
```python
import matplotlib.pyplot as plt

plot_convergence_analysis(df)
plt.savefig('convergence_plot.png', dpi=300, bbox_inches='tight')
plt.close()
```

## 7. Expected Results

For any analysis, you should see:
- ✅ Frequency ≈ 141.7001 Hz (within 0.001%)
- ✅ |∇Ξ(1)|/√N ratio ≈ 1.0 (within 0.01)
- ✅ φ = 1.6180339887... (golden ratio)
- ✅ γ = 0.5772156649... (Euler-Mascheroni)

If results differ significantly, check:
- mpmath version >= 1.3.0
- numpy version >= 1.21.0
- Python version >= 3.8

## 8. Troubleshooting

### Import Error
```bash
pip install numpy matplotlib pandas mpmath sympy
```

### "Module not found"
Make sure you're running from the repository root:
```bash
cd /path/to/141hz
python3 scripts/demo_convergencia.py
```

### Slow Performance
Use quick mode or reduce max_primes:
```python
df = calculator.convergence_analysis(max_primes=2000, step=500)
```

## 9. For More Information

- Full documentation: `scripts/README_VERIFICACION_CONVERGENCIA.md`
- Implementation details: `IMPLEMENTATION_SUMMARY_CONVERGENCIA.md`
- Source code: `scripts/verificacion_convergencia.py`
- Tests: `scripts/test_verificacion_convergencia.py`

## 10. Contributing

To run the full test suite before contributing:
```bash
cd scripts
python3 test_verificacion_convergencia.py
python3 test_protocolos_experimentales.py
```

All tests should pass before submitting changes.
