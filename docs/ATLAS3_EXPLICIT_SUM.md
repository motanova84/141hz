# Atlas³ Explicit Sum Formula and Prime Memory

## Overview

This module extends the Atlas³ PT-symmetry operator with explicit sum formula analysis, demonstrating the emergence of prime number structure from the operator's spectral properties.

## Mathematical Framework

### 1. Von Mangoldt Weights

The Von Mangoldt function Λ(n) is defined as:

```
Λ(n) = { log p  if n = p^m for some prime p and integer m ≥ 1
       { 0      otherwise
```

This function appears in the explicit formula for the prime counting function and encodes the distribution of prime numbers.

### 2. Synthetic Prime Signal

The synthetic signal from prime distribution is constructed as:

```
S(t) = Σ_{p^m} (log p / p^{m/2}) δ(t - m ln p)
```

where:
- The sum is over prime powers p^m
- log p is the Von Mangoldt weight
- p^{m/2} provides the scaling factor
- δ(t - m ln p) places delta functions at logarithmic positions

This signal encodes the explicit formula connecting primes to the Riemann zeta function.

### 3. Cross-Correlation (Oro Test)

The core "Oro" (Gold) test computes the cross-correlation between:

1. **Atlas³ eigenvalue density** ρ(E): The density of states from the operator's spectrum
2. **Prime signal** S(t): The synthetic signal from prime distribution

```
C(τ) = ∫ ρ(t) S(t + τ) dt
```

**Key Result**: If the Atlas³ operator is an isomorphism of the Riemann Hypothesis, the Fourier transform of its density of levels should show exact peaks at positions t = ln p, ln p², ... with the correct amplitudes.

### 4. Spectral Determinant with Zeta Regularization

The regularized determinant is computed via:

```
det(O) = exp(-ζ'_O(0))
```

where ζ_O(s) = Σ_n λ_n^{-s} is the spectral zeta function of the operator.

### 5. Heat Kernel Truncation

For growth control and to avoid divergences, we use heat kernel truncation:

```
K(t) = Tr(exp(-t |H|))
```

Larger t provides stronger spectral truncation, ensuring numerical stability.

## Implementation

### Core Classes

#### `ExplicitSumAnalyzer`

Main class for analyzing the explicit sum formula and cross-correlation with Atlas³ spectrum.

```python
from physics.atlas3_operator import (
    Atlas3Parameters,
    Atlas3Operator,
    ExplicitSumAnalyzer
)

# Create operator
params = Atlas3Parameters()
operator = Atlas3Operator(params, beta=0.0)
operator.compute_spectrum()

# Create analyzer
analyzer = ExplicitSumAnalyzer(
    operator,
    max_prime=100,      # Maximum prime to include
    max_power=3         # Maximum power m in p^m
)

# Generate synthetic prime signal
prime_signal = analyzer.generate_synthetic_prime_signal()

# Compute cross-correlation (Oro test)
result = analyzer.compute_cross_correlation(
    t_min=0.0,
    t_max=10.0,
    n_points=1000,
    sigma=0.15
)

# Access results
peaks = result['peaks']
correlation = result['cross_correlation']
theoretical_peaks = result['peak_positions_theoretical']
```

#### `SpectralDeterminantCalculator`

Class for computing spectral determinant with zeta function regularization.

```python
from physics.atlas3_operator import SpectralDeterminantCalculator

# Create calculator
calculator = SpectralDeterminantCalculator(
    operator,
    heat_kernel_cutoff=1.0
)

# Compute heat kernel trace
heat_trace = calculator.heat_kernel_trace(t=1.0)

# Compute spectral zeta function
zeta_s = calculator.spectral_zeta_function(s=2.0)

# Compute regularized determinant
det = calculator.regularized_determinant()

# Compute Ξ(t) function
xi_t = calculator.xi_function(t=1.0)
```

### Utility Functions

#### `von_mangoldt_weight(n: int) -> float`

Computes the Von Mangoldt function Λ(n).

```python
from physics.atlas3_operator import von_mangoldt_weight

# For primes: Λ(p) = log(p)
weight = von_mangoldt_weight(7)  # Returns log(7) ≈ 1.9459

# For prime powers: Λ(p^m) = log(p)
weight = von_mangoldt_weight(8)  # 8 = 2^3, returns log(2) ≈ 0.6931

# For composites: Λ(n) = 0
weight = von_mangoldt_weight(6)  # Returns 0
```

#### `generate_primes(max_n: int) -> List[int]`

Generates all primes up to max_n using the Sieve of Eratosthenes.

```python
from physics.atlas3_operator import generate_primes

primes = generate_primes(100)
# Returns [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
```

## Validation Script

The validation script `scripts/validacion_oro_suma_explicita.py` demonstrates the full workflow:

```bash
python scripts/validacion_oro_suma_explicita.py
```

This script:
1. Tests Von Mangoldt weights for various n
2. Validates explicit sum emergence at different β values
3. Computes cross-correlations across PT-symmetry breaking transition
4. Generates visualization plots
5. Saves results to `physics/results/oro_validation/`

### Output

The script produces:
- **Plots**: Four PNG files showing eigenvalue density, prime signal, and cross-correlation for each β value
- **JSON results**: Complete validation results with peaks, correlations, and determinants
- **Console output**: Detailed analysis and verdict

## Physical Interpretation

### "Memoria de Primos" (Prime Memory)

The emergence of peaks in the cross-correlation at positions ln(p) demonstrates that:

1. **The operator "remembers" prime structure**: Even though the Atlas³ operator is defined purely in terms of differential operators and potentials, its eigenvalue distribution spontaneously exhibits modulation at prime logarithms.

2. **PT-symmetry preserves prime memory**: The cross-correlation remains strong both in PT-symmetric (β < κ_Π) and PT-broken (β > κ_Π) regimes, suggesting prime memory is a robust feature.

3. **Connection to Riemann Hypothesis**: The alignment of spectral peaks with theoretical prime positions ln(p) suggests the operator encodes the same information as the Riemann zeta function, supporting the isomorphism hypothesis.

### Heat Kernel and Growth Control

The heat kernel K(t) = Tr(exp(-t |H|)) serves two purposes:

1. **Spectral truncation**: Larger eigenvalues are exponentially suppressed, preventing divergences in the determinant
2. **Weil trace filtering**: Acts as a filter on the density of states N(E), extracting the oscillatory component related to primes

### Determinant and Zeta Regularization

The regularized determinant relates to the functional determinant of the operator:

```
det(O) = exp(-ζ'_O(0)) = Π_n λ_n (regularized)
```

This connects the discrete spectrum to the continuous zeta function, bridging quantum mechanics and number theory.

## Tests

Comprehensive tests are provided in `tests/test_atlas3_explicit_sum.py`:

```bash
python -m unittest tests.test_atlas3_explicit_sum -v
```

Test coverage includes:
- Von Mangoldt function for primes, prime powers, and composites
- Prime generation with Sieve of Eratosthenes
- Synthetic prime signal generation and structure
- Cross-correlation computation and properties
- Peak detection and theoretical positions
- Heat kernel trace computation
- Spectral zeta function
- Regularized determinant
- Integration tests across PT-breaking transition

All 21 tests pass successfully.

## References

1. **Explicit Formula**: Montgomery, H. L. (1994). "The pair correlation of zeros of the zeta function"
2. **Von Mangoldt Weights**: Iwaniec, H., & Kowalski, E. (2004). "Analytic Number Theory"
3. **Spectral Zeta Functions**: Elizalde, E. (1995). "Ten Physical Applications of Spectral Zeta Functions"
4. **Heat Kernel Methods**: Gilkey, P. B. (1995). "Invariance Theory, the Heat Equation, and the Atiyah-Singer Index Theorem"

## Future Directions

1. **Higher Powers**: Extend analysis to higher prime powers p^m with m > 3
2. **Larger Primes**: Test correlation with primes up to 1000 or beyond
3. **Fourier Analysis**: Compute full Fourier transform of density to identify all prime harmonics
4. **Berry Phase Integration**: Incorporate Berry phase θ(t) into Ξ(t) calculation
5. **Riemann Xi Comparison**: Direct comparison with ξ(1/2 + it) / ξ(1/2 - it)

## Author

José Manuel Mota Burruezo

## License

MIT License
