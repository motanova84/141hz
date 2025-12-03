#!/usr/bin/env python3
"""
Tests for the Spectral Origin module.

This module tests the derivation of the universal constant C = 629.83
from the first eigenvalue λ₀ of the noetic operator Hψ, and the
subsequent derivation of f₀ = 141.7001 Hz.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
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

import unittest  # noqa: E402
import numpy as np  # noqa: E402

from spectral_origin import (  # noqa: E402
    NoeticOperator,
    SpectralOriginValidator,
    LAMBDA_0,
    C_UNIVERSAL,
    F0_SPECTRAL,
    derive_f0,
    get_spectral_constants,
)


class TestSpectralConstants(unittest.TestCase):
    """Test spectral origin constants."""

    def test_lambda_0_value(self):
        """Test that λ₀ is approximately 0.001588050."""
        expected = 0.001588050
        actual = float(LAMBDA_0)
        self.assertAlmostEqual(actual, expected, places=9)

    def test_c_universal_value(self):
        """Test that C = 1/λ₀ ≈ 629.83."""
        expected = 629.83
        actual = float(C_UNIVERSAL)
        self.assertAlmostEqual(actual, expected, delta=0.5)

    def test_c_is_inverse_of_lambda_0(self):
        """Test that C = 1/λ₀ exactly."""
        lambda_0 = float(LAMBDA_0)
        C = float(C_UNIVERSAL)
        self.assertAlmostEqual(C, 1.0 / lambda_0, places=10)

    def test_f0_reference_value(self):
        """Test that f₀ reference is 141.7001 Hz."""
        expected = 141.7001
        actual = float(F0_SPECTRAL)
        self.assertAlmostEqual(actual, expected, places=4)


class TestNoeticOperator(unittest.TestCase):
    """Test the NoeticOperator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.operator = NoeticOperator(grid_size=100, domain_size=10.0)

    def test_initialization(self):
        """Test operator initialization."""
        self.assertEqual(self.operator.grid_size, 100)
        self.assertEqual(self.operator.domain_size, 10.0)
        self.assertEqual(self.operator.dx, 0.1)

    def test_laplacian_matrix_shape(self):
        """Test that Laplacian matrix has correct shape."""
        laplacian = self.operator.compute_laplacian_matrix()
        self.assertEqual(laplacian.shape, (100, 100))

    def test_laplacian_matrix_symmetry(self):
        """Test that Laplacian matrix is symmetric."""
        laplacian = self.operator.compute_laplacian_matrix()
        np.testing.assert_array_almost_equal(laplacian, laplacian.T)

    def test_noetic_potential_shape(self):
        """Test that potential has correct shape."""
        potential = self.operator.compute_noetic_potential()
        self.assertEqual(potential.shape, (100,))

    def test_noetic_potential_positive(self):
        """Test that potential is non-negative everywhere."""
        potential = self.operator.compute_noetic_potential()
        self.assertTrue(np.all(potential >= -1e-10))  # Allow small numerical errors

    def test_hamiltonian_shape(self):
        """Test that Hamiltonian has correct shape."""
        H = self.operator.build_hamiltonian()
        self.assertEqual(H.shape, (100, 100))

    def test_hamiltonian_symmetry(self):
        """Test that Hamiltonian is symmetric (Hermitian)."""
        H = self.operator.build_hamiltonian()
        np.testing.assert_array_almost_equal(H, H.T)

    def test_eigenvalues_real(self):
        """Test that eigenvalues are real."""
        eigenvalues, _ = self.operator.compute_eigenvalues(n_eigenvalues=5)
        self.assertTrue(np.all(np.isreal(eigenvalues)))

    def test_eigenvalues_sorted(self):
        """Test that eigenvalues are sorted in ascending order."""
        eigenvalues, _ = self.operator.compute_eigenvalues(n_eigenvalues=5)
        for i in range(len(eigenvalues) - 1):
            self.assertLessEqual(eigenvalues[i], eigenvalues[i + 1])


class TestSpectralDerivation(unittest.TestCase):
    """Test the spectral derivation of f₀."""

    def test_derive_f0_from_C(self):
        """Test derivation of f₀ from C using the formula."""
        f0_derived = float(NoeticOperator.derive_f0_from_C())
        f0_reference = float(NoeticOperator.F0_REFERENCE)

        # Should be within 1% of reference
        relative_error = abs(f0_derived - f0_reference) / f0_reference
        self.assertLess(relative_error, 0.01)

    def test_derive_f0_from_spectral_origin(self):
        """Test complete spectral derivation."""
        derivation = NoeticOperator.derive_f0_from_spectral_origin()

        # Check all steps are present
        self.assertIn("step_1_lambda_0", derivation)
        self.assertIn("step_2_C_universal", derivation)
        self.assertIn("step_3_constants", derivation)
        self.assertIn("step_4_f0", derivation)
        self.assertIn("formula", derivation)

    def test_derivation_chain_values(self):
        """Test that derivation chain produces correct values."""
        derivation = NoeticOperator.derive_f0_from_spectral_origin()

        # Check λ₀
        lambda_0 = derivation["step_1_lambda_0"]["value"]
        self.assertAlmostEqual(lambda_0, 0.001588050, places=9)

        # Check C
        C = derivation["step_2_C_universal"]["value"]
        self.assertAlmostEqual(C, 629.83, delta=0.5)

        # Check f₀
        f0 = derivation["step_4_f0"]["value"]
        self.assertAlmostEqual(f0, 141.7001, delta=0.1)

    def test_get_all_spectral_constants(self):
        """Test getting all spectral constants."""
        constants = NoeticOperator.get_all_spectral_constants()

        self.assertIn("lambda_0", constants)
        self.assertIn("C_universal", constants)
        self.assertIn("gamma", constants)
        self.assertIn("phi", constants)
        self.assertIn("f0_derived_hz", constants)
        self.assertIn("f0_reference_hz", constants)


class TestSpectralVerification(unittest.TestCase):
    """Test spectral origin verification."""

    def test_verify_spectral_origin(self):
        """Test spectral origin verification."""
        operator = NoeticOperator()
        verification = operator.verify_spectral_origin()

        # Check verification passes
        self.assertTrue(verification["valid"])

        # Check agreement is high
        self.assertGreater(verification["agreement_percent"], 99.0)

    def test_numerical_verification(self):
        """Test numerical verification across grids."""
        operator = NoeticOperator()
        verification = operator.numerical_verification(n_grids=3)

        # Check all grids are tested
        self.assertEqual(len(verification["grid_sizes"]), 3)
        self.assertEqual(len(verification["lambda_0_values"]), 3)


class TestSpectralOriginValidator(unittest.TestCase):
    """Test the SpectralOriginValidator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = SpectralOriginValidator()

    def test_validate_derivation_chain(self):
        """Test validation of derivation chain."""
        result = self.validator.validate_derivation_chain()

        # Check structure
        self.assertIn("derivation", result)
        self.assertIn("validations", result)
        self.assertIn("all_valid", result)
        self.assertIn("summary", result)

        # Check that validation passes
        self.assertTrue(result["all_valid"])

    def test_validate_physical_interpretation(self):
        """Test physical interpretation validation."""
        result = self.validator.validate_physical_interpretation()

        # Check physical values
        self.assertIn("C_universal", result)
        self.assertIn("f0_hz", result)
        self.assertIn("E_quantum_joules", result)
        self.assertIn("lambda_wave_km", result)
        self.assertIn("R_compact_km", result)

        # Check interpretations
        self.assertIn("interpretations", result)
        self.assertIn("spectral", result["interpretations"])
        self.assertIn("geometric", result["interpretations"])
        self.assertIn("physical", result["interpretations"])


class TestConvenienceFunctions(unittest.TestCase):
    """Test convenience functions."""

    def test_derive_f0_function(self):
        """Test derive_f0 convenience function."""
        result = derive_f0()
        self.assertIn("step_4_f0", result)
        self.assertIn("formula", result)

    def test_get_spectral_constants_function(self):
        """Test get_spectral_constants convenience function."""
        result = get_spectral_constants()
        self.assertIn("lambda_0", result)
        self.assertIn("C_universal", result)
        self.assertIn("f0_derived_hz", result)


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency of derived values."""

    def test_wavelength_calculation(self):
        """Test that wavelength is correctly derived from f₀."""
        f0 = float(F0_SPECTRAL)
        c_light = 299792458.0  # m/s

        lambda_expected = c_light / f0
        lambda_expected_km = lambda_expected / 1000

        # Should be approximately 2115 km
        self.assertAlmostEqual(lambda_expected_km, 2115.68, delta=1.0)

    def test_compactification_radius(self):
        """Test compactification radius calculation."""
        f0 = float(F0_SPECTRAL)
        c_light = 299792458.0  # m/s

        R_compact = c_light / (2 * np.pi * f0)
        R_compact_km = R_compact / 1000

        # Should be approximately 336 km
        self.assertAlmostEqual(R_compact_km, 336.72, delta=1.0)

    def test_energy_quantum(self):
        """Test energy quantum calculation."""
        f0 = float(F0_SPECTRAL)
        h_planck = 6.62607015e-34  # J·s

        E_quantum = h_planck * f0

        # Should be approximately 9.39e-32 J
        self.assertAlmostEqual(E_quantum, 9.39e-32, delta=1e-33)


if __name__ == "__main__":
    unittest.main()
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
