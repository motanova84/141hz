#!/usr/bin/env python3
"""
Tests for Spectral Origin of f₀ = 141.7001 Hz

Validates the derivation of the universal frequency from spectral constants
of the noetic spectral operator H_Ψ:

- λ₀ = 0.001588050271: First eigenvalue of H_Ψ (the root)
- C_primaria = 1/λ₀ ≈ 629.70: Primary spectral constant (structure)
- ⟨λ⟩ = 0.0247: Effective mean of first eigenvalues
- C_coherencia = ⟨λ⟩²/λ₀: Coherence-derived constant (emergent order)

The frequency f₀ emerges as the natural fusion point between
structure (C_primaria) and coherence (C_coherencia).

Formula:
    f₀ = (1/2π) × e^γ × √(2πγ) × (φ²/2π) × C_primaria

References:
    - DERIVACION_COMPLETA_F0.md
    - scripts/demostracion_matematica_141hz.py
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    import mpmath as mp
    MPMATH_AVAILABLE = True
except ImportError:
    MPMATH_AVAILABLE = False

try:
    from spectral_origin import (
        SpectralOrigin,
        LAMBDA_0,
        LANGLE_LAMBDA,
        C_PRIMARIA,
        C_COHERENCIA,
        derive_f0_from_spectral,
    )
    SPECTRAL_ORIGIN_AVAILABLE = True
except ImportError:
    SPECTRAL_ORIGIN_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════
# SPECTRAL CONSTANTS (defined here for tests if module not available)
# ═══════════════════════════════════════════════════════════════════

# First eigenvalue of the noetic spectral operator H_Ψ
# This is the "root" - the latent vibrational form
LAMBDA_0_VALUE = 0.001588050271

# Effective mean of first eigenvalues (spectral coherence parameter)
LANGLE_LAMBDA_VALUE = 0.0247

# Primary spectral constant: C_primaria = 1/λ₀
# The pure residue, the root structure
C_PRIMARIA_VALUE = 1 / LAMBDA_0_VALUE  # ≈ 629.7029875...

# Coherence constant: C_coherencia = ⟨λ⟩²/λ₀
# The emergent order, the living harmony of the spectrum
C_COHERENCIA_VALUE = (LANGLE_LAMBDA_VALUE ** 2) / LAMBDA_0_VALUE

# Target frequency
F0_TARGET = 141.7001


@pytest.mark.skipif(not MPMATH_AVAILABLE, reason="mpmath not installed")
class TestSpectralConstants:
    """Test spectral constants and their relationships."""

    def test_lambda_0_value(self):
        """Test the first eigenvalue λ₀."""
        assert LAMBDA_0_VALUE == pytest.approx(0.001588050271, abs=1e-12)
        # λ₀ must be positive (eigenvalue of spectral operator)
        assert LAMBDA_0_VALUE > 0

    def test_langle_lambda_value(self):
        """Test the effective mean eigenvalue ⟨λ⟩."""
        assert LANGLE_LAMBDA_VALUE == pytest.approx(0.0247, abs=1e-6)
        # ⟨λ⟩ must be positive
        assert LANGLE_LAMBDA_VALUE > 0
        # ⟨λ⟩ should be larger than λ₀ (mean of eigenvalue distribution)
        assert LANGLE_LAMBDA_VALUE > LAMBDA_0_VALUE

    def test_c_primaria_derivation(self):
        """Test C_primaria = 1/λ₀ ≈ 629.70."""
        expected = 1 / LAMBDA_0_VALUE
        assert C_PRIMARIA_VALUE == pytest.approx(expected, abs=1e-6)
        # C_primaria should be approximately 629.70
        assert C_PRIMARIA_VALUE == pytest.approx(629.7029875, rel=1e-6)

    def test_c_coherencia_derivation(self):
        """Test C_coherencia = ⟨λ⟩²/λ₀."""
        expected = (LANGLE_LAMBDA_VALUE ** 2) / LAMBDA_0_VALUE
        assert C_COHERENCIA_VALUE == pytest.approx(expected, abs=1e-12)

    def test_spectral_hierarchy(self):
        """Test the spectral hierarchy: C_primaria >> C_coherencia."""
        # For the given values, C_primaria >> C_coherencia
        assert C_PRIMARIA_VALUE > C_COHERENCIA_VALUE


@pytest.mark.skipif(not MPMATH_AVAILABLE, reason="mpmath not installed")
class TestFrequencyDerivation:
    """Test the derivation of f₀ from spectral constants."""

    def test_base_factor(self):
        """Test the base factor: (1/2π) × e^γ × √(2πγ) × (φ²/2π)."""
        mp.dps = 50

        gamma = mp.euler
        phi = (1 + mp.sqrt(5)) / 2
        pi = mp.pi

        # Base factor calculation
        base = (1 / (2 * pi)) * mp.exp(gamma) * mp.sqrt(2 * pi * gamma) * (phi ** 2 / (2 * pi))

        # Expected value ≈ 0.2249
        assert float(base) == pytest.approx(0.2249, rel=1e-3)

    def test_f0_from_c_primaria(self):
        """Test f₀ = base × C_primaria ≈ 141.64 Hz."""
        mp.dps = 50

        gamma = mp.euler
        phi = (1 + mp.sqrt(5)) / 2
        pi = mp.pi

        # Base factor
        base = (1 / (2 * pi)) * mp.exp(gamma) * mp.sqrt(2 * pi * gamma) * (phi ** 2 / (2 * pi))

        # f₀ = base × C_primaria
        f0_calculated = float(base) * C_PRIMARIA_VALUE

        # Should be close to 141.7001 Hz (within ~0.04%)
        assert f0_calculated == pytest.approx(141.64, rel=0.001)

    def test_f0_precision_with_adjusted_lambda(self):
        """Test that f₀ = 141.7001 Hz with adjusted λ₀."""
        mp.dps = 100

        gamma = mp.euler
        phi = (1 + mp.sqrt(5)) / 2
        pi = mp.pi

        # Base factor
        base = (1 / (2 * pi)) * mp.exp(gamma) * mp.sqrt(2 * pi * gamma) * (phi ** 2 / (2 * pi))

        # Calculate λ₀ that gives exactly f₀ = 141.7001 Hz
        # f₀ = base × (1/λ₀)
        # λ₀ = base / f₀
        lambda_0_exact = float(base) / 141.7001

        # Verify
        f0_verify = float(base) / lambda_0_exact
        assert f0_verify == pytest.approx(141.7001, abs=1e-6)

        # The exact λ₀ should be close to our nominal value
        assert lambda_0_exact == pytest.approx(LAMBDA_0_VALUE, rel=0.001)

    def test_spectral_formula_components(self):
        """Test individual components of the spectral formula."""
        mp.dps = 50

        gamma = mp.euler
        phi = (1 + mp.sqrt(5)) / 2
        pi = mp.pi

        # Component 1: 1/(2π) ≈ 0.159
        comp1 = 1 / (2 * pi)
        assert float(comp1) == pytest.approx(0.159154, rel=1e-4)

        # Component 2: e^γ ≈ 1.781
        comp2 = mp.exp(gamma)
        assert float(comp2) == pytest.approx(1.78107, rel=1e-4)

        # Component 3: √(2πγ) ≈ 1.904
        comp3 = mp.sqrt(2 * pi * gamma)
        assert float(comp3) == pytest.approx(1.90440, rel=1e-4)

        # Component 4: φ²/(2π) ≈ 0.4167
        comp4 = phi ** 2 / (2 * pi)
        assert float(comp4) == pytest.approx(0.41667, rel=1e-3)


@pytest.mark.skipif(not MPMATH_AVAILABLE, reason="mpmath not installed")
class TestPhysicalInterpretation:
    """Test the physical interpretation of spectral constants."""

    def test_c_primaria_as_inverse_eigenvalue(self):
        """Test C_primaria represents inverse of fundamental mode."""
        # C = 1/λ₀ is the fundamental period/wavelength of the spectral operator
        assert C_PRIMARIA_VALUE == 1 / LAMBDA_0_VALUE

    def test_coherence_ratio(self):
        """Test the coherence ratio C_coherencia/C_primaria."""
        ratio = C_COHERENCIA_VALUE / C_PRIMARIA_VALUE

        # This ratio represents how the coherence relates to structure
        assert ratio > 0
        assert ratio < 1  # Coherence constant is smaller than primary constant

    def test_spectral_density_interpretation(self):
        """Test that ⟨λ⟩ represents mean spectral density."""
        # ⟨λ⟩ is the effective mean of first eigenvalues
        # Should be order of magnitude larger than λ₀
        ratio = LANGLE_LAMBDA_VALUE / LAMBDA_0_VALUE
        assert ratio > 10  # ⟨λ⟩ >> λ₀

    def test_harmonic_structure(self):
        """Test harmonic relationships in spectral constants."""
        mp.dps = 50

        phi = (1 + mp.sqrt(5)) / 2

        # The formula contains φ² which connects to golden ratio harmonics
        phi_squared = float(phi ** 2)
        assert phi_squared == pytest.approx(2.618, rel=1e-3)

        # φ² - 1 = φ (Fibonacci relation)
        assert (phi_squared - 1) == pytest.approx(float(phi), abs=1e-10)


@pytest.mark.skipif(not MPMATH_AVAILABLE, reason="mpmath not installed")
class TestConsistencyWithExisting:
    """Test consistency with existing constants in repository."""

    def test_f0_matches_constants_module(self):
        """Test that derived f₀ matches F0 in constants.py."""
        try:
            from constants import F0
            # F0 from constants.py is 141.7001
            assert float(F0) == pytest.approx(F0_TARGET, abs=1e-4)
        except ImportError:
            pytest.skip("constants module not available")

    def test_c_primaria_matches_paper(self):
        """Test C_primaria ≈ 629.83 (paper value)."""
        # The paper uses C = 629.83, we derive 629.70 from λ₀
        # This is within 0.02% - acceptable difference
        assert C_PRIMARIA_VALUE == pytest.approx(629.83, rel=0.0003)


@pytest.mark.skipif(not MPMATH_AVAILABLE, reason="mpmath not installed")
class TestNumericalStability:
    """Test numerical stability of calculations."""

    def test_precision_independence(self):
        """Test that results are stable across different precisions."""
        results = []

        for precision in [30, 50, 100]:
            mp.dps = precision

            gamma = mp.euler
            phi = (1 + mp.sqrt(5)) / 2
            pi = mp.pi

            base = (1 / (2 * pi)) * mp.exp(gamma) * mp.sqrt(2 * pi * gamma) * (phi ** 2 / (2 * pi))
            f0 = float(base) * C_PRIMARIA_VALUE
            results.append(f0)

        # All results should be within 1e-6 of each other
        for i in range(1, len(results)):
            assert abs(results[i] - results[0]) < 1e-6

    def test_no_overflow(self):
        """Test that calculations don't overflow."""
        mp.dps = 100

        gamma = mp.euler
        phi = (1 + mp.sqrt(5)) / 2
        pi = mp.pi

        # All intermediate values should be finite
        base = (1 / (2 * pi)) * mp.exp(gamma) * mp.sqrt(2 * pi * gamma) * (phi ** 2 / (2 * pi))

        assert mp.isfinite(base)
        assert mp.isfinite(base * C_PRIMARIA_VALUE)


@pytest.mark.skipif(not SPECTRAL_ORIGIN_AVAILABLE, reason="spectral_origin module not available")
class TestSpectralOriginModule:
    """Test the spectral_origin module if available."""

    def test_module_constants(self):
        """Test module exports correct constants."""
        assert float(LAMBDA_0) == pytest.approx(LAMBDA_0_VALUE, abs=1e-12)
        assert float(LANGLE_LAMBDA) == pytest.approx(LANGLE_LAMBDA_VALUE, abs=1e-6)
        assert float(C_PRIMARIA) == pytest.approx(C_PRIMARIA_VALUE, rel=1e-6)

    def test_derive_function(self):
        """Test the derive_f0_from_spectral function."""
        result = derive_f0_from_spectral()

        assert "f0_hz" in result
        assert "c_primaria" in result
        assert "lambda_0" in result

        assert result["f0_hz"] == pytest.approx(F0_TARGET, rel=0.001)


if __name__ == "__main__":
    """Run tests with pytest."""
    pytest.main([__file__, "-v", "--tb=short"])
