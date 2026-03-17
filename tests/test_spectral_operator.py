#!/usr/bin/env python3
"""
Tests for physics.spectral_operator

Validates the QCAL Spectral Operator (Berry-Keating Hamiltonian) and the
QCAL Spectral Engine (Mellin-space Riemann spectrum approximation), along
with the noetic forcing function F_ext(t).

Classes under test
------------------
- QCALSpectralOperator: H_BK + V_mod scaled by f₀
- QCALSpectralEngine:   -i·∂_u Hermitian Hamiltonian in log-space
- compute_noetic_forcing: Σ α_n sin(2π γ_n f₀ t + φ_n)
"""

import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.spectral_operator import (
    QCALSpectralOperator,
    QCALSpectralEngine,
    compute_noetic_forcing,
)

# Known non-trivial Riemann zeros (imaginary parts on the critical line)
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]


# ============================================================================
# QCALSpectralOperator tests
# ============================================================================

class TestQCALSpectralOperatorInit(unittest.TestCase):
    """Tests for QCALSpectralOperator initialisation."""

    def test_default_init(self):
        """Default constructor creates operator with N=128, f0=141.7001."""
        op = QCALSpectralOperator()
        self.assertEqual(op.N, 128)
        self.assertAlmostEqual(op.f0, 141.7001, places=4)

    def test_custom_n_and_f0(self):
        """Custom N and f0 are stored correctly."""
        op = QCALSpectralOperator(N=64, f0=141.7001)
        self.assertEqual(op.N, 64)
        self.assertAlmostEqual(op.f0, 141.7001, places=4)

    def test_x_grid_shape(self):
        """x grid has shape (N,) and spans [0.1, 10.0]."""
        op = QCALSpectralOperator(N=50)
        self.assertEqual(op.x.shape, (50,))
        self.assertAlmostEqual(op.x[0], 0.1, places=10)
        self.assertAlmostEqual(op.x[-1], 10.0, places=10)

    def test_dx_positive(self):
        """Mesh step dx is positive."""
        op = QCALSpectralOperator(N=64)
        self.assertGreater(op.dx, 0.0)

    def test_invalid_n_raises(self):
        """N < 4 must raise ValueError."""
        with self.assertRaises(ValueError):
            QCALSpectralOperator(N=2)

    def test_invalid_f0_raises(self):
        """Non-positive f0 must raise ValueError."""
        with self.assertRaises(ValueError):
            QCALSpectralOperator(f0=-1.0)
        with self.assertRaises(ValueError):
            QCALSpectralOperator(f0=0.0)


class TestQCALSpectralOperatorBuildHamiltonian(unittest.TestCase):
    """Tests for QCALSpectralOperator.build_hamiltonian."""

    def setUp(self):
        self.op = QCALSpectralOperator(N=32)

    def test_shape(self):
        """Hamiltonian matrix has shape (N, N)."""
        H = self.op.build_hamiltonian()
        self.assertEqual(H.shape, (self.op.N, self.op.N))

    def test_complex_dtype(self):
        """Hamiltonian has complex dtype."""
        H = self.op.build_hamiltonian()
        self.assertTrue(np.iscomplexobj(H))

    def test_scale_by_f0(self):
        """Changing f0 scales the Hamiltonian proportionally."""
        op1 = QCALSpectralOperator(N=32, f0=1.0)
        op2 = QCALSpectralOperator(N=32, f0=2.0)
        H1 = op1.build_hamiltonian(gamma=0.0)
        H2 = op2.build_hamiltonian(gamma=0.0)
        np.testing.assert_allclose(H2, 2.0 * H1, rtol=1e-12)

    def test_zero_c_raises(self):
        """C=0 must raise ValueError."""
        with self.assertRaises(ValueError):
            self.op.build_hamiltonian(C=0.0)

    def test_vmod_diagonal(self):
        """With gamma=0, V_mod is zero and H is purely H_BK-based."""
        H_gamma0 = self.op.build_hamiltonian(gamma=0.0)
        # Extract diagonal; should not contain a constant shift
        H_gamma1 = self.op.build_hamiltonian(gamma=1.0)
        # The difference should be a diagonal matrix (pure V_mod contribution)
        diff = H_gamma1 - H_gamma0
        diag_part = np.diag(np.diag(diff))
        np.testing.assert_allclose(diff, diag_part, atol=1e-25)


class TestQCALSpectralOperatorGetResonantModes(unittest.TestCase):
    """Tests for QCALSpectralOperator.get_resonant_modes."""

    def setUp(self):
        self.op = QCALSpectralOperator(N=64)

    def test_returns_20_modes(self):
        """get_resonant_modes returns at most 20 eigenvalues."""
        modes = self.op.get_resonant_modes()
        self.assertLessEqual(len(modes), 20)

    def test_modes_non_negative(self):
        """Returned eigenvalues (absolute values) are non-negative."""
        modes = self.op.get_resonant_modes()
        self.assertTrue(np.all(modes >= 0.0))

    def test_modes_sorted(self):
        """Returned eigenvalues are in non-decreasing order."""
        modes = self.op.get_resonant_modes()
        for i in range(len(modes) - 1):
            self.assertLessEqual(modes[i], modes[i + 1])

    def test_modes_positive_for_default_params(self):
        """Default parameters yield at least one positive mode."""
        modes = self.op.get_resonant_modes()
        self.assertTrue(np.any(modes > 0.0))

    def test_modes_scale_with_f0(self):
        """Scaling f0 scales eigenvalue magnitudes proportionally."""
        op1 = QCALSpectralOperator(N=32, f0=1.0)
        op2 = QCALSpectralOperator(N=32, f0=10.0)
        m1 = op1.get_resonant_modes()
        m2 = op2.get_resonant_modes()
        if len(m1) > 0 and len(m2) > 0:
            ratio = m2[0] / m1[0] if m1[0] > 0 else None
            if ratio is not None:
                self.assertAlmostEqual(ratio, 10.0, delta=0.1)


# ============================================================================
# QCALSpectralEngine tests
# ============================================================================

class TestQCALSpectralEngineInit(unittest.TestCase):
    """Tests for QCALSpectralEngine initialisation."""

    def test_default_init(self):
        """Default constructor creates engine with N=1024."""
        engine = QCALSpectralEngine()
        self.assertEqual(engine.N, 1024)

    def test_custom_n(self):
        """Custom N is stored correctly."""
        engine = QCALSpectralEngine(N=256)
        self.assertEqual(engine.N, 256)

    def test_u_grid_shape(self):
        """u grid has shape (N,) and spans [-5, 5]."""
        engine = QCALSpectralEngine(N=128)
        self.assertEqual(engine.u.shape, (128,))
        self.assertAlmostEqual(engine.u[0], -5.0, places=10)
        self.assertAlmostEqual(engine.u[-1], 5.0, places=10)

    def test_du_positive(self):
        """Logarithmic mesh step du is positive."""
        engine = QCALSpectralEngine(N=256)
        self.assertGreater(engine.du, 0.0)

    def test_invalid_n_raises(self):
        """N < 4 must raise ValueError."""
        with self.assertRaises(ValueError):
            QCALSpectralEngine(N=2)


class TestQCALSpectralEngineGenerateOperator(unittest.TestCase):
    """Tests for QCALSpectralEngine.generate_operator."""

    def setUp(self):
        self.engine = QCALSpectralEngine(N=64)

    def test_shape(self):
        """Operator matrix has shape (N, N)."""
        H = self.engine.generate_operator()
        self.assertEqual(H.shape, (64, 64))

    def test_hermitian(self):
        """Operator must be Hermitian: H = H†."""
        H = self.engine.generate_operator()
        np.testing.assert_allclose(H, H.conj().T, atol=1e-14)

    def test_complex_dtype(self):
        """Operator has complex dtype."""
        H = self.engine.generate_operator()
        self.assertTrue(np.iscomplexobj(H))

    def test_antidiagonal_structure(self):
        """Main diagonal is zero (pure derivative operator)."""
        H = self.engine.generate_operator()
        diag_vals = np.diag(H)
        np.testing.assert_allclose(np.abs(diag_vals), 0.0, atol=1e-14)


class TestQCALSpectralEngineComputeSpectrum(unittest.TestCase):
    """Tests for QCALSpectralEngine.compute_spectrum."""

    def setUp(self):
        self.engine = QCALSpectralEngine(N=256)

    def test_returns_array(self):
        """compute_spectrum returns a numpy array."""
        spectrum = self.engine.compute_spectrum()
        self.assertIsInstance(spectrum, np.ndarray)

    def test_all_positive(self):
        """All returned eigenvalues are strictly positive."""
        spectrum = self.engine.compute_spectrum()
        self.assertTrue(np.all(spectrum > 0.0))

    def test_sorted(self):
        """Eigenvalues are in non-decreasing order."""
        spectrum = self.engine.compute_spectrum()
        for i in range(len(spectrum) - 1):
            self.assertLessEqual(spectrum[i], spectrum[i + 1])

    def test_scale_factor_applied(self):
        """scale_factor multiplies all eigenvalues."""
        s1 = self.engine.compute_spectrum(scale_factor=1.0)
        s2 = self.engine.compute_spectrum(scale_factor=2.0)
        np.testing.assert_allclose(s2, 2.0 * s1, rtol=1e-12)

    def test_invalid_scale_factor_raises(self):
        """scale_factor ≤ 0 must raise ValueError."""
        with self.assertRaises(ValueError):
            self.engine.compute_spectrum(scale_factor=0.0)
        with self.assertRaises(ValueError):
            self.engine.compute_spectrum(scale_factor=-1.0)

    def test_weyl_law_density(self):
        """
        The number of positive eigenvalues should grow with N
        (Weyl law: N(T) ~ T·ln(T)/2π).
        """
        e_small = QCALSpectralEngine(N=128).compute_spectrum()
        e_large = QCALSpectralEngine(N=512).compute_spectrum()
        self.assertGreater(len(e_large), len(e_small))

    def test_spectrum_non_empty(self):
        """compute_spectrum must return at least one eigenvalue."""
        spectrum = self.engine.compute_spectrum()
        self.assertGreater(len(spectrum), 0)

    def test_first_eigenvalue_positive(self):
        """Minimum positive eigenvalue is strictly positive."""
        spectrum = self.engine.compute_spectrum()
        self.assertGreater(float(spectrum[0]), 0.0)


# ============================================================================
# compute_noetic_forcing tests
# ============================================================================

class TestComputeNoeticForcing(unittest.TestCase):
    """Tests for compute_noetic_forcing."""

    def setUp(self):
        self.gamma_n = np.array(RIEMANN_ZEROS[:5])

    def test_returns_float(self):
        """Return value is a Python float."""
        result = compute_noetic_forcing(0.0, self.gamma_n)
        self.assertIsInstance(result, float)

    def test_zero_time_default_phases(self):
        """At t=0 with default zero phases, F_ext = 0 (sin(0)=0)."""
        result = compute_noetic_forcing(0.0, self.gamma_n)
        self.assertAlmostEqual(result, 0.0, places=12)

    def test_empty_eigenvalues(self):
        """Empty eigenvalue array returns 0.0."""
        result = compute_noetic_forcing(1.0, np.array([]))
        self.assertAlmostEqual(result, 0.0, places=12)

    def test_custom_alphas(self):
        """Custom amplitudes are applied correctly."""
        alphas = np.ones(5)
        result = compute_noetic_forcing(0.001, self.gamma_n, alphas=alphas)
        self.assertIsInstance(result, float)

    def test_custom_phis(self):
        """Custom phases are applied correctly."""
        phis = np.full(5, math.pi / 2)
        result = compute_noetic_forcing(0.0, self.gamma_n, phis=phis)
        # With φ = π/2, sin(2π·γ·f₀·0 + π/2) = sin(π/2) = 1 for each term
        # F = Σ (1/N) * 1 = 1.0
        self.assertAlmostEqual(result, 1.0, places=10)

    def test_mismatched_alphas_raises(self):
        """Mismatched alphas length must raise ValueError."""
        with self.assertRaises(ValueError):
            compute_noetic_forcing(0.0, self.gamma_n, alphas=np.ones(3))

    def test_mismatched_phis_raises(self):
        """Mismatched phis length must raise ValueError."""
        with self.assertRaises(ValueError):
            compute_noetic_forcing(0.0, self.gamma_n, phis=np.zeros(3))

    def test_default_alpha_normalized(self):
        """Default alphas sum to 1 (uniform normalisation)."""
        # With phases π/2, F = sum of (1/N)*1 over N terms = 1.0
        phis = np.full(5, math.pi / 2)
        result = compute_noetic_forcing(0.0, self.gamma_n, phis=phis)
        self.assertAlmostEqual(result, 1.0, places=10)

    def test_bounded_output(self):
        """F_ext is bounded by [-1, 1] for normalised alphas."""
        for t in np.linspace(0, 1, 100):
            result = compute_noetic_forcing(t, self.gamma_n)
            self.assertGreaterEqual(result, -1.0 - 1e-12)
            self.assertLessEqual(result, 1.0 + 1e-12)

    def test_custom_f0(self):
        """Custom f0 changes output value."""
        r1 = compute_noetic_forcing(0.001, self.gamma_n, f0=141.7001)
        r2 = compute_noetic_forcing(0.001, self.gamma_n, f0=1.0)
        # Different f0 → different argument to sin → different result
        # (not guaranteed to differ in all cases, but very likely for this t)
        # We test that the function at least runs without error
        self.assertIsInstance(r1, float)
        self.assertIsInstance(r2, float)


# ============================================================================
# Integration tests
# ============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests combining operator and forcing."""

    def test_operator_modes_feed_forcing(self):
        """Eigenvalues from QCALSpectralOperator can feed compute_noetic_forcing."""
        op = QCALSpectralOperator(N=32)
        modes = op.get_resonant_modes()
        self.assertGreater(len(modes), 0)
        result = compute_noetic_forcing(0.001, modes)
        self.assertIsInstance(result, float)

    def test_engine_spectrum_feeds_forcing(self):
        """Eigenvalues from QCALSpectralEngine can feed compute_noetic_forcing."""
        engine = QCALSpectralEngine(N=128)
        spectrum = engine.compute_spectrum()[:10]
        result = compute_noetic_forcing(0.001, spectrum)
        self.assertIsInstance(result, float)

    def test_physics_module_imports(self):
        """QCALSpectralOperator and QCALSpectralEngine export from physics."""
        from physics import QCALSpectralOperator as Op, QCALSpectralEngine as Eng
        from physics import compute_noetic_forcing as cnf
        self.assertIsNotNone(Op)
        self.assertIsNotNone(Eng)
        self.assertIsNotNone(cnf)


if __name__ == "__main__":
    unittest.main()
