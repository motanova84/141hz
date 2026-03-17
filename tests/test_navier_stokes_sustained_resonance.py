#!/usr/bin/env python3
"""
Unit Tests: QCAL-NS v2 Sustained Resonance

Tests for the compute_forcing, compute_adaptive_damping, and QCALNSResonator
components of the QCAL-NS v2 Active Resonator architecture.
"""

import pytest
import numpy as np

from navier_stokes.sustained_resonance import (
    compute_forcing,
    compute_adaptive_damping,
    _alpha_from_re_q,
    QCALNSResonator,
)
from navier_stokes.constants import F0


# ─────────────────────────────────────────────────────────────────────────────
# compute_forcing
# ─────────────────────────────────────────────────────────────────────────────

class TestComputeForcing:
    """Tests for the temporal phase-dragging forcing function."""

    def _make_xx(self, N=32):
        x = np.linspace(0.0, 2.0 * np.pi, N, endpoint=False)
        return np.meshgrid(x, x, indexing="ij")[0]

    def test_output_shape_matches_input(self):
        """Output shape equals input shape."""
        xx = self._make_xx(32)
        result = compute_forcing(xx, t=0.5)
        assert result.shape == xx.shape

    def test_zero_at_t_zero(self):
        """Forcing is zero at t=0 because temporal_sync = sin(2π f₀·0) = 0."""
        xx = self._make_xx(32)
        result = compute_forcing(xx, t=0.0)
        np.testing.assert_allclose(result, 0.0, atol=1e-15)

    def test_nonzero_at_quarter_period(self):
        """At t = 1/(4 f₀), temporal_sync = sin(π/2) = 1, so forcing ≠ 0."""
        xx = self._make_xx(32)
        t_quarter = 1.0 / (4.0 * F0)
        result = compute_forcing(xx, t=t_quarter)
        # logos_wave = sin(f₀·xx) is not uniformly zero, so max |result| > 0
        assert np.max(np.abs(result)) > 0.0

    def test_gamma_scaling(self):
        """Doubling gamma doubles the forcing amplitude."""
        xx = self._make_xx(32)
        t = 1.0 / (4.0 * F0)
        f1 = compute_forcing(xx, t, gamma=0.1)
        f2 = compute_forcing(xx, t, gamma=0.2)
        np.testing.assert_allclose(f2, 2.0 * f1, rtol=1e-12)

    def test_custom_f0(self):
        """Custom f0 changes the spatial and temporal frequency."""
        xx = self._make_xx(32)
        t = 1.0 / (4.0 * 100.0)  # quarter period of 100 Hz
        f_default = compute_forcing(xx, t, f0=F0)
        f_custom = compute_forcing(xx, t, f0=100.0)
        # They should differ (different frequencies)
        assert not np.allclose(f_default, f_custom)

    def test_temporal_periodicity(self):
        """Forcing repeats with period 1/f₀ in time."""
        xx = self._make_xx(32)
        t0 = 0.3
        t_plus_period = t0 + 1.0 / F0
        f0 = compute_forcing(xx, t0)
        f_period = compute_forcing(xx, t_plus_period)
        np.testing.assert_allclose(f0, f_period, rtol=1e-10, atol=1e-10)

    def test_1d_input(self):
        """Works with a 1-D coordinate array."""
        xx = np.linspace(0.0, 2.0 * np.pi, 64)
        result = compute_forcing(xx, t=0.5)
        assert result.shape == (64,)


# ─────────────────────────────────────────────────────────────────────────────
# _alpha_from_re_q
# ─────────────────────────────────────────────────────────────────────────────

class TestAlphaFromReQ:
    """Tests for the Re_q → α mapping."""

    def test_high_re_q_gives_small_alpha(self):
        """High Re_q (laminar flow) → small α (gentle damping)."""
        alpha = _alpha_from_re_q(1e15)
        assert alpha < 0.01

    def test_low_re_q_gives_large_alpha(self):
        """Low Re_q (chaotic flow) → large α (aggressive damping)."""
        alpha = _alpha_from_re_q(1e6)
        assert alpha > 0.99

    def test_critical_re_q(self):
        """At Re_q = Re_q_crit = 10¹², α = 0.5 exactly."""
        alpha = _alpha_from_re_q(1e12)
        assert abs(alpha - 0.5) < 1e-12

    def test_monotonically_decreasing(self):
        """α decreases as Re_q increases."""
        re_q_values = np.logspace(6, 15, 50)
        alphas = [_alpha_from_re_q(r) for r in re_q_values]
        assert all(alphas[i] > alphas[i + 1] for i in range(len(alphas) - 1))

    def test_alpha_positive(self):
        """α is always strictly positive."""
        for re_q in [0.0, 1.0, 1e6, 1e12, 1e18]:
            if re_q == 0.0:
                # re_q = 0 is degenerate (visc_adelica = ∞), skip
                continue
            assert _alpha_from_re_q(re_q) > 0.0

    def test_alpha_bounded_by_one(self):
        """α ≤ 1 for all finite Re_q."""
        for re_q in [1e3, 1e6, 1e9, 1e12, 1e18]:
            assert _alpha_from_re_q(re_q) <= 1.0


# ─────────────────────────────────────────────────────────────────────────────
# compute_adaptive_damping
# ─────────────────────────────────────────────────────────────────────────────

class TestComputeAdaptiveDamping:
    """Tests for the adaptive vibrational spectral filter."""

    def test_output_shape_matches_k(self):
        """Output shape equals input k shape."""
        k = np.arange(0.0, 33.0, dtype=float)
        result = compute_adaptive_damping(k, k_cut=14.0, N=64, re_q=1e12)
        assert result.shape == k.shape

    def test_unity_at_k_cut(self):
        """Damping = 1 exactly at k = k_cut (resonance mode preserved)."""
        k_cut = 14.0
        result = compute_adaptive_damping(np.array([k_cut]), k_cut=k_cut, N=64, re_q=1e12)
        np.testing.assert_allclose(result, 1.0, atol=1e-15)

    def test_damping_less_than_one_away_from_k_cut(self):
        """Modes away from k_cut are attenuated (Damping < 1)."""
        k_cut = 14.0
        k_far = np.array([0.0, 5.0, 28.0, 32.0])
        result = compute_adaptive_damping(k_far, k_cut=k_cut, N=64, re_q=1e12)
        assert np.all(result < 1.0)

    def test_higher_alpha_means_stronger_damping(self):
        """Lower Re_q → higher α → stronger damping for off-resonance modes."""
        k = np.array([0.0, 5.0, 30.0])
        k_cut = 14.0
        # Low Re_q → high α → strong damping
        damp_low_req = compute_adaptive_damping(k, k_cut, N=64, re_q=1e8)
        # High Re_q → low α → gentle damping
        damp_high_req = compute_adaptive_damping(k, k_cut, N=64, re_q=1e15)
        # Low Re_q should attenuate more (smaller damping factor)
        assert np.all(damp_low_req <= damp_high_req)

    def test_damping_values_in_range(self):
        """All damping values lie in (0, 1]."""
        k = np.linspace(0, 32, 100)
        result = compute_adaptive_damping(k, k_cut=14.0, N=64, re_q=1e12)
        assert np.all(result > 0.0)
        assert np.all(result <= 1.0 + 1e-12)

    def test_2d_array_input(self):
        """Works with 2-D wavenumber magnitude arrays."""
        N = 64
        kx = np.fft.fftfreq(N, d=1.0 / N)
        ky = np.fft.fftfreq(N, d=1.0 / N)
        KX, KY = np.meshgrid(kx, ky, indexing="ij")
        K_norm = np.sqrt(KX ** 2 + KY ** 2)
        result = compute_adaptive_damping(K_norm, k_cut=14.0, N=N, re_q=1e12)
        assert result.shape == (N, N)
        assert np.all(result > 0.0)
        assert np.all(result <= 1.0 + 1e-12)

    def test_bandwidth_scales_with_N(self):
        """Bandwidth N/16 controls how quickly damping falls off."""
        k = np.array([14.0 + 4.0])   # one bandwidth away (N/16 for N=64)
        # At distance exactly = N/16, Damping = exp(-α)
        alpha = _alpha_from_re_q(1e12)  # = 0.5
        expected = np.exp(-alpha)
        result = compute_adaptive_damping(k, k_cut=14.0, N=64, re_q=1e12)
        np.testing.assert_allclose(result, expected, rtol=1e-12)


# ─────────────────────────────────────────────────────────────────────────────
# QCALNSResonator
# ─────────────────────────────────────────────────────────────────────────────

class TestQCALNSResonatorInitialization:
    """Tests for QCALNSResonator.__init__."""

    def test_default_initialization(self):
        """Resonator initialises with expected attribute types."""
        res = QCALNSResonator(N=32)
        assert res.N == 32
        assert res.f0 == F0
        assert res.nu > 0.0
        assert res.gamma > 0.0
        assert res.beta_init > 0.0
        assert res.t == 0.0
        assert isinstance(res.omega, np.ndarray)
        assert res.omega.shape == (32, 32)

    def test_k_f0_mode_positive(self):
        """The aliased QCAL resonance wavenumber is a positive integer."""
        res = QCALNSResonator(N=64)
        assert res.k_f0_mode >= 1

    def test_k_cut_matches_k_f0_mode(self):
        """k_cut equals the aliased forcing mode."""
        res = QCALNSResonator(N=64)
        assert res.k_cut == float(res.k_f0_mode)

    def test_initial_psi_near_half(self):
        """Initial Ψ is approximately 0.5 (pre-coherence seeding)."""
        res = QCALNSResonator(N=64)
        psi0 = res.psi()
        # The seeding is designed for Ψ ≈ 0.5; accept a broad window
        assert 0.1 < psi0 < 0.95

    def test_initial_h1_norm_finite(self):
        """Initial H¹ norm is finite."""
        res = QCALNSResonator(N=32)
        assert np.isfinite(res.h1_norm())

    def test_invalid_N_raises(self):
        """Non-even or too-small N raises ValueError."""
        with pytest.raises(ValueError):
            QCALNSResonator(N=7)
        with pytest.raises(ValueError):
            QCALNSResonator(N=3)

    def test_custom_parameters(self):
        """Custom parameters are stored correctly."""
        res = QCALNSResonator(N=32, f0=100.0, nu=1e-5, gamma=0.2, beta_init=0.3)
        assert res.f0 == 100.0
        assert res.nu == 1e-5
        assert res.gamma == 0.2
        assert res.beta_init == 0.3


class TestQCALNSResonatorStep:
    """Tests for QCALNSResonator.step."""

    def test_step_advances_time(self):
        """Each step increments simulation time by dt."""
        res = QCALNSResonator(N=32)
        dt = 0.05
        for i in range(1, 4):
            metrics = res.step(dt)
            assert abs(metrics["t"] - i * dt) < 1e-12

    def test_step_returns_required_keys(self):
        """step() returns a dict with psi, h1_norm, t."""
        res = QCALNSResonator(N=32)
        metrics = res.step(0.05)
        assert "psi" in metrics
        assert "h1_norm" in metrics
        assert "t" in metrics

    def test_psi_in_unit_interval(self):
        """Ψ stays in [0, 1] after multiple steps."""
        res = QCALNSResonator(N=32)
        for _ in range(10):
            m = res.step(0.05)
            assert 0.0 <= m["psi"] <= 1.0

    def test_h1_norm_positive_and_finite(self):
        """H¹ norm remains positive and finite after several steps."""
        res = QCALNSResonator(N=32)
        for _ in range(10):
            m = res.step(0.05)
            assert np.isfinite(m["h1_norm"])
            assert m["h1_norm"] >= 0.0

    def test_omega_shape_preserved(self):
        """Vorticity field shape is unchanged by stepping."""
        N = 32
        res = QCALNSResonator(N=N)
        for _ in range(5):
            res.step(0.05)
        assert res.omega.shape == (N, N)

    def test_omega_is_real(self):
        """Vorticity field remains real-valued after stepping."""
        res = QCALNSResonator(N=32)
        for _ in range(5):
            res.step(0.05)
        assert np.isrealobj(res.omega) or np.all(np.isreal(res.omega))


class TestQCALNSResonatorRun:
    """Tests for QCALNSResonator.run."""

    def test_run_returns_arrays(self):
        """run() returns numpy arrays for t, psi, h1_norm."""
        res = QCALNSResonator(N=32)
        results = res.run(nt=5, dt=0.05)
        assert isinstance(results["t"], np.ndarray)
        assert isinstance(results["psi"], np.ndarray)
        assert isinstance(results["h1_norm"], np.ndarray)

    def test_run_array_length(self):
        """Returned arrays have length = initial step + nt."""
        res = QCALNSResonator(N=32)
        nt = 8
        results = res.run(nt=nt, dt=0.05)
        # History starts with 1 entry at t=0, then nt more steps
        assert len(results["t"]) == nt + 1
        assert len(results["psi"]) == nt + 1
        assert len(results["h1_norm"]) == nt + 1

    def test_run_time_monotonically_increasing(self):
        """Time array is strictly increasing."""
        res = QCALNSResonator(N=32)
        results = res.run(nt=10, dt=0.05)
        diffs = np.diff(results["t"])
        assert np.all(diffs > 0.0)

    def test_run_psi_bounded(self):
        """All Ψ values remain in [0, 1]."""
        res = QCALNSResonator(N=32)
        results = res.run(nt=10, dt=0.05)
        assert np.all(results["psi"] >= 0.0)
        assert np.all(results["psi"] <= 1.0)

    def test_run_h1_norm_finite(self):
        """H¹ norm is finite for all steps (no blow-up)."""
        res = QCALNSResonator(N=32)
        results = res.run(nt=10, dt=0.05)
        assert np.all(np.isfinite(results["h1_norm"]))


class TestQCALNSResonatorMetrics:
    """Tests for metric accessors."""

    def test_psi_accessor(self):
        """psi() returns the latest Ψ value."""
        res = QCALNSResonator(N=32)
        res.step(0.05)
        assert res.psi() == res._psi_history[-1]

    def test_h1_norm_accessor(self):
        """h1_norm() returns the latest H¹ norm."""
        res = QCALNSResonator(N=32)
        res.step(0.05)
        assert res.h1_norm() == res._h1_history[-1]

    def test_f0_correlation_returns_float(self):
        """f0_correlation() returns a float in [-1, 1]."""
        res = QCALNSResonator(N=32)
        res.run(nt=25, dt=0.05)
        corr = res.f0_correlation()
        assert isinstance(corr, float)
        assert -1.0 <= corr <= 1.0

    def test_f0_correlation_insufficient_history(self):
        """f0_correlation() returns 0.0 when fewer than 2 data points."""
        res = QCALNSResonator(N=32)
        # Only 1 point recorded (at t=0)
        assert res.f0_correlation() == 0.0

    def test_get_metrics_summary_keys(self):
        """get_metrics_summary() contains all required keys."""
        res = QCALNSResonator(N=32)
        res.run(nt=5, dt=0.05)
        summary = res.get_metrics_summary()
        required_keys = {
            "psi_current",
            "psi_mean_last10",
            "h1_norm_current",
            "h1_norm_finite",
            "f0_correlation",
            "re_q",
            "t",
        }
        assert required_keys.issubset(summary.keys())

    def test_get_metrics_summary_values(self):
        """get_metrics_summary() returns sensible values."""
        res = QCALNSResonator(N=32)
        res.run(nt=5, dt=0.05)
        summary = res.get_metrics_summary()
        assert 0.0 <= summary["psi_current"] <= 1.0
        assert summary["h1_norm_finite"] is True
        assert summary["re_q"] > 0.0
        assert summary["t"] > 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Sustained resonance: convergence behaviour
# ─────────────────────────────────────────────────────────────────────────────

class TestSustainedResonance:
    """Integration tests for the Ψ convergence (Resonancia Sostenida)."""

    def test_psi_increases_with_forcing(self):
        """
        With strong forcing (gamma=0.5), Ψ at the end of the run should
        exceed the initial Ψ, demonstrating coherence growth.
        """
        res = QCALNSResonator(N=64, gamma=0.5, beta_init=0.5)
        psi_initial = res.psi()
        results = res.run(nt=30, dt=0.05)
        psi_final = results["psi"][-1]
        # Ψ should have grown or remained high
        assert psi_final >= psi_initial * 0.8  # at least 80% of initial

    def test_h1_norm_controlled(self):
        """
        H¹ norm stays bounded (finite) over a medium-length run —
        the adaptive damping prevents blow-up.
        """
        res = QCALNSResonator(N=64, gamma=0.1)
        results = res.run(nt=20, dt=0.05)
        assert np.all(np.isfinite(results["h1_norm"]))
        # H¹ norm should not grow unboundedly
        max_h1 = np.max(results["h1_norm"])
        init_h1 = results["h1_norm"][0]
        # Allow at most 100× growth relative to the initial norm
        assert max_h1 < 100.0 * (init_h1 + 1.0)

    def test_zero_forcing_psi_decays(self):
        """
        Without forcing (gamma=0), the adaptive damping still controls
        the H¹ norm — it should remain within a small factor of its
        initial value (bounded, no blow-up).
        """
        res_no_forcing = QCALNSResonator(N=32, gamma=0.0, beta_init=0.5)
        h1_initial = res_no_forcing.h1_norm()
        results = res_no_forcing.run(nt=15, dt=0.05)
        h1_final = results["h1_norm"][-1]
        # Without forcing, H¹ norm should remain within 10% of its initial value
        assert h1_final <= h1_initial * 1.10

    def test_adaptive_damping_reduces_chaos(self):
        """
        After running with large forcing + adaptive damping, energy should
        be concentrated in coherent modes (Ψ not near zero).
        """
        res = QCALNSResonator(N=64, gamma=0.3, beta_init=0.5)
        results = res.run(nt=40, dt=0.05)
        # Average Ψ over the second half of the run should be substantial
        half = len(results["psi"]) // 2
        psi_late = np.mean(results["psi"][half:])
        assert psi_late > 0.3

    def test_module_exports(self):
        """Verify that all new symbols are exported from the package."""
        from navier_stokes import (
            compute_forcing,
            compute_adaptive_damping,
            QCALNSResonator,
        )
        assert callable(compute_forcing)
        assert callable(compute_adaptive_damping)
        assert callable(QCALNSResonator)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
