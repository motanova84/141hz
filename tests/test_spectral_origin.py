#!/usr/bin/env python3
"""
Tests for the Spectral Origin module.

This module tests the derivation of the universal constant C = 629.83
from the first eigenvalue λ₀ of the noetic operator Hψ, and the
subsequent derivation of f₀ = 141.7001 Hz.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

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
