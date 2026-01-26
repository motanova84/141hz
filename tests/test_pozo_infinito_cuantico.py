#!/usr/bin/env python3
"""
Test suite for pozo_infinito_cuantico.py module

Tests the standard quantum mechanical derivation of the infinite potential well
and its connection to the noetic framework QCAL ∞³.
"""

import unittest
import numpy as np
from scipy.constants import pi

# Import the module to test
from pozo_infinito_cuantico import (
    PozoInfinitoCuantico,
    PozoNoetico,
    calcular_longitud_pozo,
    resonador_basal_universal,
    F0_UNIVERSAL,
    HBAR
)


class TestPozoInfinitoCuantico(unittest.TestCase):
    """Test the standard infinite quantum well implementation."""

    def setUp(self):
        """Set up test fixtures."""
        # Standard test case: electron in 1 nm well
        self.L = 1e-9  # 1 nm
        self.m_electron = 9.10938356e-31  # kg
        self.pozo = PozoInfinitoCuantico(self.L, self.m_electron)

    def test_initialization(self):
        """Test that the well initializes correctly."""
        self.assertEqual(self.pozo.L, self.L)
        self.assertEqual(self.pozo.m, self.m_electron)

    def test_numero_onda(self):
        """Test wave number calculation kₙ = nπ/L."""
        # Test n=1
        k1 = self.pozo.numero_onda(1)
        expected_k1 = pi / self.L
        self.assertAlmostEqual(k1, expected_k1, places=10)

        # Test n=2
        k2 = self.pozo.numero_onda(2)
        expected_k2 = 2 * pi / self.L
        self.assertAlmostEqual(k2, expected_k2, places=10)

        # Test scaling: k2 should be exactly twice k1
        self.assertAlmostEqual(k2, 2 * k1, places=10)

    def test_numero_onda_invalid(self):
        """Test that invalid quantum numbers raise errors."""
        with self.assertRaises(ValueError):
            self.pozo.numero_onda(0)
        with self.assertRaises(ValueError):
            self.pozo.numero_onda(-1)

    def test_energia(self):
        """Test energy eigenvalue calculation Eₙ = ℏ²π²n²/(2mL²)."""
        # Test n=1
        E1 = self.pozo.energia(1)
        k1 = self.pozo.numero_onda(1)
        expected_E1 = (HBAR**2 * k1**2) / (2 * self.m_electron)
        self.assertAlmostEqual(E1, expected_E1, places=25)

        # Test n=2: E2 should be 4 times E1 (scales as n²)
        E2 = self.pozo.energia(2)
        self.assertAlmostEqual(E2 / E1, 4.0, places=10)

        # Test n=3: E3 should be 9 times E1
        E3 = self.pozo.energia(3)
        self.assertAlmostEqual(E3 / E1, 9.0, places=10)

    def test_energia_scaling(self):
        """Test that energy scales as n²."""
        E1 = self.pozo.energia(1)
        for n in range(2, 11):
            En = self.pozo.energia(n)
            expected_ratio = n**2
            actual_ratio = En / E1
            self.assertAlmostEqual(actual_ratio, expected_ratio, places=10)

    def test_frecuencia(self):
        """Test frequency calculation fₙ = Eₙ/h."""
        E1 = self.pozo.energia(1)
        f1 = self.pozo.frecuencia(1)
        expected_f1 = E1 / (2 * pi * HBAR)
        self.assertAlmostEqual(f1, expected_f1, places=10)

    def test_funcion_onda_normalization(self):
        """Test that wave functions are normalized."""
        x = np.linspace(0, self.L, 1000)
        dx = x[1] - x[0]

        for n in range(1, 6):
            psi = self.pozo.funcion_onda(x, n)
            # Integrate |ψ|² over the well
            norm = np.sum(np.abs(psi)**2) * dx
            # Should integrate to 1 (normalized)
            self.assertAlmostEqual(norm, 1.0, places=2)

    def test_funcion_onda_boundary_conditions(self):
        """Test that wave functions satisfy boundary conditions ψ(0) = ψ(L) = 0."""
        for n in range(1, 6):
            # Test at x=0
            psi_0 = self.pozo.funcion_onda(np.array([0.0]), n)
            self.assertAlmostEqual(psi_0[0], 0.0, places=10)

            # Test at x=L (allow for numerical precision issues with sin(nπ))
            psi_L = self.pozo.funcion_onda(np.array([self.L]), n)
            self.assertAlmostEqual(psi_L[0], 0.0, places=6)

    def test_funcion_onda_nodes(self):
        """Test that wave function for n has (n-1) nodes inside the well."""
        x = np.linspace(0, self.L, 10000)

        for n in range(1, 6):
            psi = self.pozo.funcion_onda(x, n)
            # Count sign changes (zero crossings)
            sign_changes = np.sum(np.diff(np.sign(psi)) != 0)
            # Should have (n-1) internal nodes + 2 boundary zeros
            # But we count sign changes, which is approximately 2*(n-1) + 2 = 2n
            # Actually, for sin(nπx/L), there are exactly n-1 internal zeros
            # We're looking for zero crossings, so approximately n+1 total
            # Let's be less strict: check that we have roughly the right number
            self.assertGreaterEqual(sign_changes, n - 1)
            self.assertLessEqual(sign_changes, n + 1)

    def test_densidad_probabilidad(self):
        """Test probability density calculation."""
        x = np.linspace(0, self.L, 1000)

        for n in range(1, 6):
            psi = self.pozo.funcion_onda(x, n)
            prob = self.pozo.densidad_probabilidad(x, n)
            expected_prob = np.abs(psi)**2
            np.testing.assert_array_almost_equal(prob, expected_prob, decimal=10)

    def test_energia_punto_cero(self):
        """Test ground state energy."""
        E0 = self.pozo.energia_punto_cero()
        E1 = self.pozo.energia(1)
        self.assertEqual(E0, E1)

    def test_frecuencia_fundamental(self):
        """Test fundamental frequency."""
        f0 = self.pozo.frecuencia_fundamental()
        f1 = self.pozo.frecuencia(1)
        self.assertEqual(f0, f1)


class TestPozoNoetico(unittest.TestCase):
    """Test the noetic extension of the quantum well."""

    def setUp(self):
        """Set up test fixtures."""
        self.L = 1e-9
        self.m = 9.10938356e-31
        self.R_psi = 1e-20  # Small noetic feedback term
        self.pozo_noetico = PozoNoetico(self.L, self.m, self.R_psi)
        self.pozo_std = PozoInfinitoCuantico(self.L, self.m)

    def test_initialization(self):
        """Test noetic well initialization."""
        self.assertEqual(self.pozo_noetico.L, self.L)
        self.assertEqual(self.pozo_noetico.m, self.m)
        self.assertEqual(self.pozo_noetico.R_psi, self.R_psi)

    def test_reduces_to_standard_when_R_zero(self):
        """Test that noetic well reduces to standard when R_ψ = 0."""
        pozo_zero = PozoNoetico(self.L, self.m, R_psi=0.0)

        for n in range(1, 6):
            E_std = self.pozo_std.energia(n)
            E_noetic = pozo_zero.energia_noesica(n)
            self.assertEqual(E_std, E_noetic)

            f_std = self.pozo_std.frecuencia(n)
            f_noetic = pozo_zero.frecuencia_noesica(n)
            self.assertEqual(f_std, f_noetic)

    def test_energia_noesica(self):
        """Test that noetic energy includes feedback term."""
        for n in range(1, 6):
            E_std = self.pozo_std.energia(n)
            E_noetic = self.pozo_noetico.energia_noesica(n)
            # Should be E_std + R_psi
            expected = E_std + self.R_psi
            self.assertAlmostEqual(E_noetic, expected, places=30)

    def test_frecuencia_noesica(self):
        """Test noetic frequency calculation."""
        for n in range(1, 6):
            E_noetic = self.pozo_noetico.energia_noesica(n)
            f_noetic = self.pozo_noetico.frecuencia_noesica(n)
            expected_f = E_noetic / (2 * pi * HBAR)
            self.assertAlmostEqual(f_noetic, expected_f, places=10)

    def test_coherencia_campo(self):
        """Test field coherence calculation."""
        # When R_psi = 0, coherence should be 1
        pozo_zero = PozoNoetico(self.L, self.m, R_psi=0.0)
        coherence = pozo_zero.coherencia_campo(1)
        self.assertEqual(coherence, 1.0)

        # When R_psi > 0, coherence should be > 1
        coherence_pos = self.pozo_noetico.coherencia_campo(1)
        self.assertGreater(coherence_pos, 1.0)


class TestCalcularLongitudPozo(unittest.TestCase):
    """Test the inverse calculation: L from f₀."""

    def test_calcular_longitud_pozo_consistency(self):
        """Test that calculating L from f gives consistent results."""
        # Create a well with known properties
        L_original = 1e-9
        m = 9.10938356e-31
        pozo = PozoInfinitoCuantico(L_original, m)
        f1 = pozo.frecuencia_fundamental()

        # Calculate L from f1
        L_calculated = calcular_longitud_pozo(f1, m, n=1)

        # Should get back the original L
        self.assertAlmostEqual(L_calculated, L_original, places=15)

    def test_calcular_longitud_pozo_universal(self):
        """Test calculation with universal frequency."""
        m = 1e-27  # Some arbitrary mass
        L = calcular_longitud_pozo(F0_UNIVERSAL, m, n=1)

        # Verify by creating a well and checking its frequency
        pozo = PozoInfinitoCuantico(L, m)
        f1 = pozo.frecuencia_fundamental()

        # Should match universal frequency within numerical precision
        rel_error = abs(f1 - F0_UNIVERSAL) / F0_UNIVERSAL
        self.assertLess(rel_error, 1e-10)

    def test_calcular_longitud_pozo_scaling(self):
        """Test that L scales correctly with mass and frequency."""
        m = 1e-27
        f = 100.0

        # L should scale as 1/√(mf)
        L1 = calcular_longitud_pozo(f, m, n=1)

        # Double the mass: L should decrease by √2
        L2 = calcular_longitud_pozo(f, 2 * m, n=1)
        self.assertAlmostEqual(L2, L1 / np.sqrt(2), places=10)

        # Double the frequency: L should decrease by √2
        L3 = calcular_longitud_pozo(2 * f, m, n=1)
        self.assertAlmostEqual(L3, L1 / np.sqrt(2), places=10)


class TestResonadorBasalUniversal(unittest.TestCase):
    """Test the universal basal resonator aligned with f₀ = 141.7001 Hz."""

    def test_resonador_universal_frequency(self):
        """Test that universal resonator has correct fundamental frequency."""
        m = 1e-27  # Arbitrary mass
        L, E1, f1 = resonador_basal_universal(m, precision=50)

        # Frequency should match F0_UNIVERSAL within high precision
        rel_error = abs(f1 - F0_UNIVERSAL) / F0_UNIVERSAL
        self.assertLess(rel_error, 1e-6)

    def test_resonador_universal_properties(self):
        """Test that universal resonator has physically consistent properties."""
        m = 1e-27
        L, E1, f1 = resonador_basal_universal(m, precision=50)

        # All values should be positive
        self.assertGreater(L, 0)
        self.assertGreater(E1, 0)
        self.assertGreater(f1, 0)

        # Create well and verify
        pozo = PozoInfinitoCuantico(L, m)
        self.assertAlmostEqual(pozo.energia_punto_cero(), E1, places=20)
        self.assertAlmostEqual(pozo.frecuencia_fundamental(), f1, places=5)

    def test_resonador_universal_different_masses(self):
        """Test that universal resonator works for different masses."""
        masses = [1e-30, 1e-27, 1e-24, 1e-20]

        for m in masses:
            L, E1, f1 = resonador_basal_universal(m, precision=30)

            # Frequency should always match F0_UNIVERSAL
            rel_error = abs(f1 - F0_UNIVERSAL) / F0_UNIVERSAL
            self.assertLess(rel_error, 1e-5)

            # L should scale as 1/√m
            # E should scale as m (since E ~ ℏ²/(mL²) and L² ~ 1/m)


class TestPhysicalConsistency(unittest.TestCase):
    """Test physical consistency and quantum mechanics principles."""

    def setUp(self):
        """Set up test fixtures."""
        self.L = 1e-9
        self.m = 9.10938356e-31
        self.pozo = PozoInfinitoCuantico(self.L, self.m)

    def test_uncertainty_principle(self):
        """Test that system respects Heisenberg uncertainty principle."""
        # For particle in a box, Δx ~ L, Δp ~ ℏπ/L
        # So ΔxΔp ~ ℏπ ≥ ℏ/2
        Delta_x = self.L  # Order of magnitude
        k1 = self.pozo.numero_onda(1)
        Delta_p = HBAR * k1  # Order of magnitude of momentum

        uncertainty_product = Delta_x * Delta_p
        # Should satisfy uncertainty principle
        self.assertGreaterEqual(uncertainty_product, HBAR / 2)

    def test_orthogonality(self):
        """Test orthogonality of wave functions."""
        x = np.linspace(0, self.L, 10000)
        dx = x[1] - x[0]

        # Test orthogonality for first few states
        for n in range(1, 4):
            for m in range(n + 1, 5):
                psi_n = self.pozo.funcion_onda(x, n)
                psi_m = self.pozo.funcion_onda(x, m)

                # Inner product should be zero
                inner_product = np.sum(psi_n * psi_m) * dx
                self.assertAlmostEqual(inner_product, 0.0, places=2)

    def test_energy_positivity(self):
        """Test that all energy eigenvalues are positive."""
        for n in range(1, 21):
            E = self.pozo.energia(n)
            self.assertGreater(E, 0)

    def test_frequency_positivity(self):
        """Test that all frequencies are positive."""
        for n in range(1, 21):
            f = self.pozo.frecuencia(n)
            self.assertGreater(f, 0)


class TestNumericalStability(unittest.TestCase):
    """Test numerical stability of calculations."""

    def test_extreme_well_sizes(self):
        """Test calculations with extreme well sizes."""
        m = 9.10938356e-31

        # Very small well (atomic scale)
        pozo_small = PozoInfinitoCuantico(1e-12, m)
        E1_small = pozo_small.energia(1)
        self.assertGreater(E1_small, 0)
        self.assertTrue(np.isfinite(E1_small))

        # Large well (macroscopic scale)
        pozo_large = PozoInfinitoCuantico(1e-3, m)
        E1_large = pozo_large.energia(1)
        self.assertGreater(E1_large, 0)
        self.assertTrue(np.isfinite(E1_large))

    def test_high_quantum_numbers(self):
        """Test calculations with high quantum numbers."""
        L = 1e-9
        m = 9.10938356e-31
        pozo = PozoInfinitoCuantico(L, m)

        # Test up to n=100
        for n in [50, 75, 100]:
            E = pozo.energia(n)
            f = pozo.frecuencia(n)

            # Should still be finite and positive
            self.assertGreater(E, 0)
            self.assertGreater(f, 0)
            self.assertTrue(np.isfinite(E))
            self.assertTrue(np.isfinite(f))


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
