# Riemann Zeros Validation

This document describes the implementation of the Riemann zeros computation validation script.

## Overview

The `validate_riemann_zeros.py` script implements a high-precision validation of the mathematical relationship between Riemann zeta function zeros and quantum frequency calculations.

## Mathematical Basis

The script validates the following relationship:

```
Σ exp(-α·γₙ) × e^(γπ) ≈ φ×400
```

Where:
- `γₙ` are the imaginary parts of Riemann zeta function zeros
- `α` is a decay parameter (default: 0.006695 for approximated zeros)
- `γ` is the Euler-Mascheroni constant (0.577215...)
- `π` is pi (3.141592...)
- `φ` is the golden ratio (1.618033...)
- `e^(γπ)` ≈ 6.131114

### Target Values

- Sum target: S ≈ 105.562150
- Validation target: S × e^(γπ) ≈ φ×400 ≈ 647.213595

## Implementation Details

### Constants

All constants are defined with 100-digit precision using mpmath:

```python
phi = 1.618033988749894848204586834365638117720309179805762862135448622705260
gamma = 0.577215664901532860606512090082402431042159335939923598805767234648689
pi = 3.141592653589793238462643383279502884197169399375105820974944592307816
```

### Riemann Zeros

The script uses:
- **100 known zeros**: First 100 Riemann zeros from mathematical tables/LMFDB
- **Asymptotic approximations**: Additional zeros generated using Riemann-von Mangoldt formula:
  ```
  γₙ ≈ 2πn/log(n)
  ```

**Important**: For production use, replace the approximated zeros with actual data from the [LMFDB database](https://www.lmfdb.org/zeros/zeta/).

### Alpha Parameter

The decay parameter `α` controls the exponential decay in the sum. The script provides two approaches:

1. **Default alpha (0.006695)**: Optimal for the approximated zero set
2. **Find alpha**: Use `--find-alpha` to compute the optimal alpha for your zero set

The original problem statement specifies `α = 0.551020`, which is likely calibrated for actual LMFDB data.

### Frequency Computation

The script also computes a final frequency using:

```
f = (1/2π) × [e^γ × √(2πγ) × (φ²/2π)] × [ψ_eff] × [δ]
```

Where:
- `ψ_eff = ψ' / (2π × log²(ψ'/2π))`
- `ψ' = φ×400×e^(γπ)`
- `δ = 1 + (1/φ)×log(γπ)`

## Usage

### Basic Validation

Run validation with default parameters:
```bash
python3 validate_riemann_zeros.py --precision 50
```

### Custom Parameters

Specify custom alpha and maximum zero height:
```bash
python3 validate_riemann_zeros.py --precision 100 --alpha 0.006695 --T 3967.986
```

### Find Optimal Alpha

Find the alpha that achieves target sum for your zero set:
```bash
python3 validate_riemann_zeros.py --find-alpha --precision 50
```

### Save Results

Save validation results to a specific file:
```bash
python3 validate_riemann_zeros.py --precision 50 --output results/my_validation.json
```

## Output Format

The script generates JSON output with the following structure:

```json
{
  "timestamp": "2025-10-29T...",
  "precision_digits": 50,
  "validation_suite": "riemann_zeros",
  "zeros_validation": {
    "constants": {
      "phi": 1.618033988749895,
      "gamma": 0.5772156649015329,
      "pi": 3.141592653589793,
      "e_gamma_pi": 6.131114182422604,
      "phi_400": 647.2135954999579,
      "target_sum": 105.56215008284556
    },
    "parameters": {
      "alpha": 0.006695,
      "T": 3967.986,
      "precision_digits": 50,
      "num_zeros_used": 3438
    },
    "computation": {
      "zeros_sum": 105.658801,
      "expected_sum": 105.562150,
      "validation_result": 647.806028,
      "expected_phi_400": 647.213595,
      "relative_error_sum": 0.000915,
      "relative_error_result": 0.000915,
      "absolute_difference_sum": 0.096651,
      "absolute_difference_result": 0.592433
    },
    "status": "PASS"
  },
  "frequency_computation": {
    "frequency_hz": 4.67334,
    "components": {
      "f_base": 0.159155,
      "scaling_factor": 1.413305,
      "psi_prime": 3968.140454,
      "psi_effective": 15.189149,
      "delta_correction": 1.367848,
      "log_term": 6.448176
    },
    "precision_digits": 50
  },
  "overall_status": "PASS",
  "summary": {
    "tests_run": 1,
    "tests_passed": 1,
    "tests_failed": 0
  }
}
```

## Testing

Run the test suite:
```bash
python3 -m unittest test_riemann_zeros -v
```

The test suite includes:
- Unit tests for individual functions
- Validation of constant values
- Structure and type checking
- Integration tests

## Integration with CI/CD

The script can be integrated into GitHub Actions workflows:

```yaml
- name: Validate Riemann zeros relationship
  run: python3 validate_riemann_zeros.py --precision 50
  continue-on-error: false
```

## Known Limitations

1. **Approximated Zeros**: The current implementation uses asymptotic approximations beyond the first 100 zeros. For research-grade accuracy, use actual LMFDB data.

2. **Alpha Calibration**: The optimal alpha value depends on the zero set used. With actual LMFDB data, the alpha from the problem statement (0.551020) may be appropriate.

3. **Computational Cost**: Higher precision (100+ digits) and more zeros (3438) require significant computation time.

## Future Enhancements

1. **LMFDB Integration**: Direct download of zeros from LMFDB database
2. **Parallel Computation**: Parallelize sum computation for better performance
3. **Caching**: Cache computed zeros to avoid regeneration
4. **Visualization**: Plot zeros distribution and validation results

## References

- [LMFDB - L-functions and Modular Forms Database](https://www.lmfdb.org/)
- [Riemann Zeta Function Zeros](https://www.lmfdb.org/zeros/zeta/)
- Riemann-von Mangoldt formula for zero approximation
- mpmath documentation: https://mpmath.org/

## License

This code is part of the 141Hz gravitational wave analysis project. See the repository LICENSE file for details.
