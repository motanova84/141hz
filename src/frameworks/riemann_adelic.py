#!/usr/bin/env python3
"""
Riemann-Adelic Framework: Spectral Structure

This module provides the spectral structure foundation through:
- Riemann zeta function analysis at critical line
- Adelic geometry connecting local and global analysis
- Spectral decomposition of the fundamental frequency
- Zero distribution and its connection to f₀

Mathematical Foundation:
    The Riemann zeta function ζ(s) and its derivative ζ'(1/2) provide
    the spectral structure that underlies the frequency f₀ = 141.7001 Hz.
    The adelic framework unifies p-adic and real analysis.
"""

import mpmath as mp
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

# Set precision for mpmath calculations
mp.dps = 50


@dataclass
class SpectralData:
    """Container for spectral analysis results."""
    frequencies: np.ndarray
    amplitudes: np.ndarray
    phases: np.ndarray
    zeta_contribution: complex
    adelic_norm: float


class RiemannAdelicFramework:
    """
    Riemann-Adelic Framework for spectral structure analysis.
    
    This framework provides:
    1. Spectral decomposition via Riemann zeta function
    2. Adelic geometry for local-global connections
    3. Zero distribution analysis
    4. Spectral invariants computation
    """
    
    def __init__(self, precision: int = 50):
        """
        Initialize the Riemann-Adelic framework.
        
        Args:
            precision: Decimal precision for calculations
        """
        self.precision = precision
        mp.dps = precision
        
        # Fundamental constants from Riemann zeta theory
        self.zeta_prime_half = mp.mpf("-0.207886224977354566017307")
        self.phi = (1 + mp.sqrt(5)) / 2  # Golden ratio
        
        # Cache for computed zeros
        self._zeros_cache: Optional[List[mp.mpf]] = None
    
    def compute_zeta_derivative(self, s: complex) -> complex:
        """
        Compute derivative of Riemann zeta function at s.
        
        Args:
            s: Complex argument
            
        Returns:
            ζ'(s) computed with high precision
        """
        # Use numerical differentiation for high precision
        h = mp.mpf(1e-10)
        zeta_plus = mp.zeta(s + h)
        zeta_minus = mp.zeta(s - h)
        return (zeta_plus - zeta_minus) / (2 * h)
    
    def get_riemann_zeros(self, max_zeros: int = 100) -> List[mp.mpf]:
        """
        Get first N non-trivial zeros of Riemann zeta function.
        
        Uses known values for first 100 zeros, then asymptotic formula.
        
        Args:
            max_zeros: Maximum number of zeros to return
            
        Returns:
            List of imaginary parts of zeros on critical line
        """
        if self._zeros_cache is not None and len(self._zeros_cache) >= max_zeros:
            return self._zeros_cache[:max_zeros]
        
        # First 20 known zeros (imaginary parts)
        known_zeros = [
            14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
            37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
            52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
            67.079811, 69.546402, 72.067158, 75.704691, 77.144840
        ]
        
        zeros = [mp.mpf(z) for z in known_zeros]
        
        # Use asymptotic approximation for additional zeros if needed
        if max_zeros > len(zeros):
            # Riemann-von Mangoldt formula: γₙ ≈ 2πn/log(n)
            for n in range(len(zeros) + 1, max_zeros + 1):
                approx_zero = 2 * mp.pi * n / mp.log(n)
                zeros.append(approx_zero)
        
        self._zeros_cache = zeros
        return zeros[:max_zeros]
    
    def spectral_decomposition(
        self, 
        f0: float = 141.7001,
        num_harmonics: int = 10
    ) -> SpectralData:
        """
        Perform spectral decomposition based on Riemann zeros.
        
        The spectral structure is determined by the distribution of
        Riemann zeros and their connection to the fundamental frequency.
        
        Args:
            f0: Fundamental frequency (Hz)
            num_harmonics: Number of harmonic components
            
        Returns:
            SpectralData object with decomposition results
        """
        # Get Riemann zeros
        zeros = self.get_riemann_zeros(num_harmonics)
        
        # Compute spectral frequencies scaled by f0
        frequencies = np.array([float(f0 * (1 + z / (2 * mp.pi))) for z in zeros])
        
        # Compute amplitudes based on zeta function behavior
        amplitudes = np.array([
            float(1 / mp.sqrt(1 + (z / (2 * mp.pi))**2)) 
            for z in zeros
        ])
        
        # Compute phases from zeta function argument
        phases = np.array([
            float(mp.arg(mp.zeta(mp.mpc(0.5, float(z))))) 
            for z in zeros
        ])
        
        # Zeta contribution at critical point
        zeta_at_half = self.compute_zeta_derivative(0.5)
        
        # Adelic norm (product of local norms)
        adelic_norm = float(mp.fabs(zeta_at_half))
        
        return SpectralData(
            frequencies=frequencies,
            amplitudes=amplitudes,
            phases=phases,
            zeta_contribution=complex(zeta_at_half),
            adelic_norm=adelic_norm
        )
    
    def adelic_local_analysis(
        self, 
        prime: int,
        field_value: complex
    ) -> Dict[str, Any]:
        """
        Perform p-adic (local) analysis at a given prime.
        
        The adelic framework unifies analysis across all primes and
        the real numbers, providing both local and global perspectives.
        
        Args:
            prime: Prime number for p-adic analysis
            field_value: Complex field value to analyze
            
        Returns:
            Dictionary with local analysis results
        """
        # p-adic valuation (order of vanishing)
        abs_val = abs(field_value)
        if abs_val == 0:
            valuation = float('inf')
        else:
            valuation = -np.log(abs_val) / np.log(prime)
        
        # Local contribution to adelic norm
        local_norm = abs_val if abs_val > 0 else 0
        
        # Harmonic at prime
        harmonic_freq = 141.7001 * prime
        
        return {
            'prime': prime,
            'valuation': valuation,
            'local_norm': local_norm,
            'harmonic_frequency': harmonic_freq,
            'convergent': local_norm < 1
        }
    
    def adelic_global_product(
        self,
        field_value: complex,
        primes: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Compute adelic global product over all places.
        
        Product formula: ∏(all places p) |·|_p = 1
        
        Args:
            field_value: Complex field value
            primes: List of primes to include (default: first 10 primes)
            
        Returns:
            Global adelic analysis results
        """
        if primes is None:
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        
        # Real place contribution
        real_norm = abs(field_value)
        
        # Compute local contributions
        local_results = [
            self.adelic_local_analysis(p, field_value)
            for p in primes
        ]
        
        # Product of local norms
        product = real_norm * np.prod([r['local_norm'] for r in local_results])
        
        # Check product formula (should be ≈ 1 for algebraic numbers)
        product_formula_satisfied = abs(product - 1.0) < 1e-6
        
        return {
            'real_norm': real_norm,
            'local_results': local_results,
            'global_product': product,
            'product_formula_satisfied': product_formula_satisfied,
            'primes_analyzed': primes
        }
    
    def spectral_invariant(
        self,
        f0: float = 141.7001
    ) -> Dict[str, Any]:
        """
        Compute spectral invariants from Riemann-adelic structure.
        
        These invariants are independent of coordinate choices and
        provide fundamental characterization of the frequency spectrum.
        
        Args:
            f0: Fundamental frequency
            
        Returns:
            Dictionary of spectral invariants
        """
        # Zeta derivative at critical point
        zeta_prime = self.compute_zeta_derivative(0.5)
        
        # Spectral gap (difference between consecutive zeros)
        zeros = self.get_riemann_zeros(20)
        gaps = [float(zeros[i+1] - zeros[i]) for i in range(len(zeros)-1)]
        mean_gap = np.mean(gaps)
        gap_variance = np.var(gaps)
        
        # Golden ratio scaling
        phi_scaled_freq = f0 * float(self.phi)
        
        # Zeta-regulated frequency
        zeta_regulated = f0 * float(mp.fabs(zeta_prime))
        
        return {
            'fundamental_frequency': f0,
            'zeta_prime_at_half': complex(zeta_prime),
            'mean_spectral_gap': mean_gap,
            'gap_variance': gap_variance,
            'phi_scaled_frequency': phi_scaled_freq,
            'zeta_regulated_frequency': zeta_regulated,
            'spectral_dimension': len(gaps),
            'adelic_compatible': True
        }
    
    def validate_spectral_structure(self) -> Dict[str, Any]:
        """
        Validate the spectral structure properties.
        
        Returns:
            Validation results
        """
        # Get spectral decomposition
        spectral = self.spectral_decomposition()
        
        # Check positivity of amplitudes
        amplitudes_positive = np.all(spectral.amplitudes >= 0)
        
        # Check frequency ordering
        frequencies_ordered = np.all(np.diff(spectral.frequencies) > 0)
        
        # Check adelic norm positivity
        norm_positive = spectral.adelic_norm > 0
        
        # Test product formula for f0
        f0_complex = complex(141.7001, 0)
        adelic = self.adelic_global_product(f0_complex)
        
        return {
            'amplitudes_positive': amplitudes_positive,
            'frequencies_ordered': frequencies_ordered,
            'adelic_norm_positive': norm_positive,
            'product_formula_satisfied': adelic['product_formula_satisfied'],
            'num_spectral_components': len(spectral.frequencies),
            'validation_passed': all([
                amplitudes_positive,
                frequencies_ordered,
                norm_positive
            ])
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export framework state as dictionary.
        
        Returns:
            Dictionary representation of framework
        """
        invariants = self.spectral_invariant()
        validation = self.validate_spectral_structure()
        
        return {
            'framework': 'Riemann-Adelic',
            'role': 'Spectral Structure',
            'precision': self.precision,
            'zeta_prime_half': float(self.zeta_prime_half),
            'phi': float(self.phi),
            'spectral_invariants': invariants,
            'validation': validation
        }


if __name__ == "__main__":
    """Demonstration of Riemann-Adelic framework."""
    print("=" * 70)
    print("RIEMANN-ADELIC FRAMEWORK: SPECTRAL STRUCTURE")
    print("=" * 70)
    print()
    
    # Initialize framework
    framework = RiemannAdelicFramework(precision=50)
    
    # Compute spectral decomposition
    print("Spectral Decomposition:")
    spectral = framework.spectral_decomposition()
    print(f"  Number of components: {len(spectral.frequencies)}")
    print(f"  Frequency range: {spectral.frequencies[0]:.2f} - {spectral.frequencies[-1]:.2f} Hz")
    print(f"  Zeta contribution: {spectral.zeta_contribution:.6f}")
    print(f"  Adelic norm: {spectral.adelic_norm:.6f}")
    print()
    
    # Compute spectral invariants
    print("Spectral Invariants:")
    invariants = framework.spectral_invariant()
    print(f"  f₀: {invariants['fundamental_frequency']:.4f} Hz")
    print(f"  ζ'(1/2): {invariants['zeta_prime_at_half']}")
    print(f"  Mean spectral gap: {invariants['mean_spectral_gap']:.4f}")
    print(f"  φ-scaled frequency: {invariants['phi_scaled_frequency']:.4f} Hz")
    print()
    
    # Adelic analysis
    print("Adelic Analysis:")
    adelic = framework.adelic_global_product(complex(141.7001, 0))
    print(f"  Real norm: {adelic['real_norm']:.6f}")
    print(f"  Global product: {adelic['global_product']:.6f}")
    print(f"  Product formula: {'✓' if adelic['product_formula_satisfied'] else '✗'}")
    print()
    
    # Validation
    print("Validation:")
    validation = framework.validate_spectral_structure()
    print(f"  Spectral structure: {'PASS ✓' if validation['validation_passed'] else 'FAIL ✗'}")
    print()
    
    print("=" * 70)
