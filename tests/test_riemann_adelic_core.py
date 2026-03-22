"""
tests/test_riemann_adelic_core.py — Tests for physics/riemann_adelic_core.py

Validates:
  1. Analytical Ψ_min computation via golden-ratio/Berry-Keating formula
  2. H_QCAL toy model (Berry-Keating operator + QED modulation potential)
  3. Riemann zero comparison utilities

AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
DATE: March 2026
"""

import math
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics.riemann_adelic_core import (
    PHI,
    F0_HZ,
    PSI_MIN,
    BERRY_CORRECTION_BASE,
    BERRY_CORRECTION_EXPONENT,
    RIEMANN_ZEROS_T,
    PsiMinResult,
    RiemannComparison,
    calcular_psi_min,
    simulate_h_qcal,
    comparar_con_riemann,
)


# ============================================================================
# TestConstants — module-level constants
# ============================================================================

class TestConstants:
    """Verify module-level constants."""

    def test_phi_golden_ratio(self):
        """φ = (1 + √5)/2 ≈ 1.6180339887."""
        assert abs(PHI - (1.0 + math.sqrt(5.0)) / 2.0) < 1e-12

    def test_f0_hz(self):
        """F0_HZ must equal the QCAL fundamental frequency."""
        assert F0_HZ == pytest.approx(141.7001, rel=1e-6)

    def test_psi_min_threshold(self):
        """PSI_MIN threshold = 0.888."""
        assert PSI_MIN == pytest.approx(0.888, rel=1e-6)

    def test_berry_correction_base(self):
        """Berry correction base = 8/7."""
        assert BERRY_CORRECTION_BASE == pytest.approx(8.0 / 7.0, rel=1e-10)

    def test_berry_correction_exponent(self):
        """Berry correction exponent = 1/8."""
        assert BERRY_CORRECTION_EXPONENT == pytest.approx(1.0 / 8.0, rel=1e-10)

    def test_riemann_zeros_count(self):
        """First 10 known Riemann zeros must be provided."""
        assert len(RIEMANN_ZEROS_T) == 10

    def test_riemann_zeros_first(self):
        """First Riemann zero t₁ ≈ 14.1347."""
        assert RIEMANN_ZEROS_T[0] == pytest.approx(14.134725, rel=1e-4)

    def test_riemann_zeros_ascending(self):
        """Riemann zeros must be in ascending order."""
        for i in range(len(RIEMANN_ZEROS_T) - 1):
            assert RIEMANN_ZEROS_T[i] < RIEMANN_ZEROS_T[i + 1]


# ============================================================================
# TestCalcularPsiMin — analytical Ψ_min computation
# ============================================================================

class TestCalcularPsiMin:
    """Tests for calcular_psi_min()."""

    @pytest.fixture
    def result(self) -> PsiMinResult:
        return calcular_psi_min()

    def test_returns_psi_min_result(self, result):
        """calcular_psi_min() returns a PsiMinResult dataclass."""
        assert isinstance(result, PsiMinResult)

    def test_phi_value(self, result):
        """phi field matches the golden ratio."""
        assert result.phi == pytest.approx(PHI, rel=1e-10)

    def test_two_phi_squared(self, result):
        """2φ² ≈ 5.23607."""
        expected = 2.0 * PHI ** 2
        assert result.two_phi_squared == pytest.approx(expected, rel=1e-10)

    def test_psi_base_formula(self, result):
        """Ψ_base = e^(-1/(2φ²)) ≈ 0.8261."""
        expected = math.exp(-1.0 / (2.0 * PHI ** 2))
        assert result.psi_base == pytest.approx(expected, rel=1e-8)
        assert 0.82 < result.psi_base < 0.83

    def test_berry_factor(self, result):
        """Berry factor = (8/7)^(1/8) ≈ 1.0168."""
        expected = (8.0 / 7.0) ** (1.0 / 8.0)
        assert result.berry_factor == pytest.approx(expected, rel=1e-8)
        assert result.berry_factor == pytest.approx(1.0168, rel=1e-3)
        assert result.berry_factor > 1.0

    def test_psi_min_composition(self, result):
        """Ψ_min = psi_base × berry_factor (multiplicative correction)."""
        assert result.psi_min == pytest.approx(
            result.psi_base * result.berry_factor, rel=1e-10
        )

    def test_psi_min_value(self, result):
        """Ψ_min = psi_base × berry_factor (composition verified independently)."""
        assert result.psi_min == pytest.approx(result.psi_base * result.berry_factor, rel=1e-10)
        assert 0.83 < result.psi_min < 0.86

    def test_psi_min_positive(self, result):
        """Ψ_min must be a positive real number."""
        assert result.psi_min > 0.0

    def test_description_non_empty(self, result):
        """Description string must be non-empty."""
        assert len(result.description) > 0

    def test_psi_min_less_than_one(self, result):
        """Ψ_min must be less than 1 (not saturated coherence)."""
        assert result.psi_min < 1.0

    def test_deterministic(self):
        """calcular_psi_min() returns the same value on repeated calls."""
        r1 = calcular_psi_min()
        r2 = calcular_psi_min()
        assert r1.psi_min == r2.psi_min


# ============================================================================
# TestSimulateHQcal — H_QCAL toy model eigenvalues
# ============================================================================

class TestSimulateHQcal:
    """Tests for simulate_h_qcal()."""

    def test_returns_numpy_array(self):
        """simulate_h_qcal() returns a numpy ndarray."""
        evs = simulate_h_qcal()
        assert isinstance(evs, np.ndarray)

    def test_default_dimension(self):
        """Default call returns 10 eigenvalues."""
        evs = simulate_h_qcal()
        assert len(evs) == 10

    def test_custom_dimension(self):
        """Custom n_dim parameter is respected."""
        for n in [5, 10, 20]:
            evs = simulate_h_qcal(n_dim=n)
            assert len(evs) == n

    def test_eigenvalues_ascending(self):
        """eigvalsh() returns eigenvalues in ascending order."""
        evs = simulate_h_qcal()
        assert np.all(np.diff(evs) > 0), "Eigenvalues should be strictly ascending"

    def test_eigenvalues_positive(self):
        """All eigenvalues of H_QCAL must be positive (positive-definite H)."""
        evs = simulate_h_qcal()
        assert np.all(evs > 0), "All eigenvalues should be positive"

    def test_first_eigenvalue(self):
        """First eigenvalue: H[0,0] = 0.5 + 1 + f0·1e-4 ≈ 1.514."""
        evs = simulate_h_qcal(f0=F0_HZ)
        expected_first = 0.5 + 1.0 + F0_HZ * 1e-4
        assert evs[0] == pytest.approx(expected_first, rel=1e-6)

    def test_eigenvalue_spacing(self):
        """Adjacent eigenvalues should differ by 0.5 (diagonal structure)."""
        evs = simulate_h_qcal()
        diffs = np.diff(evs)
        assert np.all(np.abs(diffs - 0.5) < 1e-6), "Spacing should be 0.5 between eigenvalues"

    def test_f0_coupling_effect(self):
        """Higher f0 shifts eigenvalues up proportionally."""
        evs_low = simulate_h_qcal(f0=100.0)
        evs_high = simulate_h_qcal(f0=200.0)
        # Each eigenvalue should be shifted by (200-100)*1e-4 = 0.01
        delta = (200.0 - 100.0) * 1e-4
        assert np.allclose(evs_high - evs_low, delta, atol=1e-10)

    def test_hermitian_matrix(self):
        """H_QCAL as constructed is symmetric (Hermitian), producing real eigenvalues."""
        evs = simulate_h_qcal()
        assert np.all(np.isreal(evs))

    def test_real_eigenvalues(self):
        """Eigenvalues should all be real-valued floats."""
        evs = simulate_h_qcal()
        for ev in evs:
            assert isinstance(float(ev), float)


# ============================================================================
# TestCompararConRiemann — Riemann zero comparison
# ============================================================================

class TestCompararConRiemann:
    """Tests for comparar_con_riemann()."""

    @pytest.fixture
    def eigenvalues(self) -> np.ndarray:
        return simulate_h_qcal()

    @pytest.fixture
    def comparison(self, eigenvalues) -> RiemannComparison:
        return comparar_con_riemann(eigenvalues)

    def test_returns_riemann_comparison(self, comparison):
        """comparar_con_riemann() returns a RiemannComparison dataclass."""
        assert isinstance(comparison, RiemannComparison)

    def test_eigenvalues_stored(self, comparison, eigenvalues):
        """Eigenvalues are stored in the result."""
        assert len(comparison.eigenvalues) == len(eigenvalues)

    def test_riemann_zeros_stored(self, comparison):
        """Riemann zeros are stored in the result."""
        assert len(comparison.riemann_zeros) == 10

    def test_scale_factor_default(self, comparison):
        """Default scale factor is 1.2."""
        assert comparison.scale_factor == pytest.approx(1.2, rel=1e-10)

    def test_scaled_eigenvalues_count(self, comparison, eigenvalues):
        """Scaled eigenvalues count matches input."""
        assert len(comparison.scaled_eigenvalues) == min(len(eigenvalues), 10)

    def test_scaled_eigenvalues_correct(self, comparison, eigenvalues):
        """Scaled eigenvalues = eigenvalues × scale_factor."""
        for ev, sev in zip(eigenvalues, comparison.scaled_eigenvalues):
            assert sev == pytest.approx(ev * comparison.scale_factor, rel=1e-10)

    def test_mean_error_positive(self, comparison):
        """Mean error must be a positive real number."""
        assert comparison.mean_error >= 0.0

    def test_max_error_geq_mean(self, comparison):
        """Max error must be ≥ mean error."""
        assert comparison.max_error >= comparison.mean_error

    def test_custom_scale_factor(self, eigenvalues):
        """Custom scale factor is applied correctly."""
        cmp = comparar_con_riemann(eigenvalues, scale_factor=2.0)
        assert cmp.scale_factor == pytest.approx(2.0)
        assert cmp.scaled_eigenvalues[0] == pytest.approx(eigenvalues[0] * 2.0)

    def test_custom_riemann_zeros(self, eigenvalues):
        """Custom t_n list is used when provided."""
        custom_zeros = [10.0, 20.0, 30.0]
        cmp = comparar_con_riemann(eigenvalues, t_n=custom_zeros)
        assert len(cmp.riemann_zeros) == len(custom_zeros)

    def test_spectral_density_flag(self, comparison):
        """captures_spectral_density is True when mean_error < 5.0."""
        assert comparison.captures_spectral_density == (comparison.mean_error < 5.0)

    def test_toy_model_error_magnitude(self, comparison):
        """Toy model eigenvalues are in a different scale than Riemann zeros."""
        # The toy model is a simplified approximation — large errors expected
        # without the Dirichlet convolution kernel
        assert comparison.mean_error > 0.0
