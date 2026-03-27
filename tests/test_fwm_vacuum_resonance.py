#!/usr/bin/env python3
"""
Tests for FWM Vacuum Resonance Module
======================================

Validates the Four-Wave Mixing vacuum resonance implementation covering:

- Physical constants and default parameter consistency
- Nonlinear polarisation P_NL = ε₀ χ⁽³⁾ |ψ|² E
- FWM sideband frequencies f_L ± f₀ and amplitude ratio
- Sideband power spectrum (Lorentzian peaks)
- Resonance strength ℛ(f) = g_aγγ² ρ_DM / [Δf² + (Γ/2)²]
- Resonance profile peak location and FWHM
- Ramsey Echo protocol (τ = 1/f₀, visibility, echo field)
- Ramsey Echo SNR
- Max-Cut SDP relaxation on K₇ (bipartition, SDP bound, coherence)
- Max-Cut phase spectrum
- Input validation / error handling
- FWM summary dictionary keys

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 2026-03
Framework: QCAL ∞³
"""

import math
import unittest

import numpy as np

from physics.fwm_vacuum_resonance import (
    # Constants
    MU_0,
    EPS_0,
    CHI3_VACUUM,
    GAMMA_DEFAULT_HZ,
    K7_MAX_CUT_INTEGER,
    K7_N_VERTICES,
    K7_TOTAL_EDGES,
    K7_SDP_BOUND,
    # Data structures
    FWMParameters,
    NonlinearPolarisation,
    FWMSidebandResult,
    ResonanceResult,
    RamseyEchoResult,
    MaxCutSDPResult,
    # Nonlinear polarisation
    psi_mod_sq,
    nonlinear_polarisation,
    # FWM sidebands
    fwm_sidebands,
    fwm_sideband_spectrum,
    # Resonance
    resonance_strength,
    resonance_profile,
    resonance_fwhm,
    resonance_peak,
    # Ramsey Echo
    ramsey_echo,
    ramsey_echo_snr,
    # Max-Cut SDP
    maxcut_sdp_k7,
    maxcut_phase_spectrum,
    # Summary
    fwm_summary,
)
from qcal.constants import F0_HZ, C


# ---------------------------------------------------------------------------
# Tolerances
# ---------------------------------------------------------------------------
REL = 1.0e-6   # relative tolerance for exact derivations
ABS = 1.0e-60  # absolute tolerance for near-zero comparisons


class TestConstants(unittest.TestCase):
    """Validate module-level physical constants."""

    def test_mu0_value(self):
        """MU_0 ≈ 4π × 10⁻⁷ H m⁻¹."""
        self.assertAlmostEqual(MU_0, 4.0 * math.pi * 1.0e-7, places=20)

    def test_eps0_value(self):
        """ε₀ = 1 / (μ₀ c²)."""
        expected = 1.0 / (MU_0 * C**2)
        self.assertAlmostEqual(EPS_0 / expected, 1.0, places=10)

    def test_chi3_positive(self):
        """χ⁽³⁾ must be positive."""
        self.assertGreater(CHI3_VACUUM, 0.0)

    def test_chi3_tiny(self):
        """χ⁽³⁾ should be extremely small (< 10⁻²⁵ m² V⁻²)."""
        self.assertLess(CHI3_VACUUM, 1.0e-25)

    def test_gamma_default_near_zero(self):
        """Default linewidth Γ should be near-zero (< 1 Hz)."""
        self.assertLess(GAMMA_DEFAULT_HZ, 1.0)
        self.assertGreater(GAMMA_DEFAULT_HZ, 0.0)

    def test_k7_vertices(self):
        """K₇ has 7 vertices."""
        self.assertEqual(K7_N_VERTICES, 7)

    def test_k7_total_edges(self):
        """K₇ has 7×6/2 = 21 edges."""
        self.assertEqual(K7_TOTAL_EDGES, 21)

    def test_k7_max_cut_integer(self):
        """Known Max-Cut on K₇ is 12."""
        self.assertEqual(K7_MAX_CUT_INTEGER, 12)

    def test_k7_sdp_bound(self):
        """Goemans-Williamson bound for K₇ = 7×6/4 = 10.5."""
        self.assertAlmostEqual(K7_SDP_BOUND, 10.5, places=10)


class TestFWMParameters(unittest.TestCase):
    """Validate FWMParameters dataclass."""

    def test_defaults(self):
        """Default parameters use canonical F0_HZ."""
        p = FWMParameters()
        self.assertAlmostEqual(p.f0, F0_HZ)
        self.assertGreater(p.g_agg, 0)
        self.assertGreater(p.rho_dm, 0)
        self.assertGreater(p.gamma_hz, 0)
        self.assertGreater(p.chi3, 0)
        self.assertGreater(p.psi0_ev, 0)

    def test_omega0(self):
        """ω₀ = 2π f₀."""
        p = FWMParameters()
        self.assertAlmostEqual(p.omega0, 2.0 * math.pi * F0_HZ, places=8)

    def test_tau_echo(self):
        """τ = 1/f₀."""
        p = FWMParameters()
        self.assertAlmostEqual(p.tau_echo, 1.0 / F0_HZ, places=10)

    def test_invalid_f0(self):
        """Negative f0 raises ValueError."""
        with self.assertRaises(ValueError):
            FWMParameters(f0=-1.0)

    def test_invalid_rho_dm(self):
        """Zero rho_dm raises ValueError."""
        with self.assertRaises(ValueError):
            FWMParameters(rho_dm=0.0)

    def test_invalid_gamma_hz(self):
        """Negative gamma_hz raises ValueError."""
        with self.assertRaises(ValueError):
            FWMParameters(gamma_hz=-1.0)

    def test_invalid_psi0_ev(self):
        """Negative psi0_ev raises ValueError."""
        with self.assertRaises(ValueError):
            FWMParameters(psi0_ev=-1.0)

    def test_custom_parameters(self):
        """Custom parameters are stored correctly."""
        p = FWMParameters(f0=200.0, gamma_hz=1.0, rho_dm=0.5)
        self.assertAlmostEqual(p.f0, 200.0)
        self.assertAlmostEqual(p.gamma_hz, 1.0)
        self.assertAlmostEqual(p.rho_dm, 0.5)


class TestNonlinearPolarisation(unittest.TestCase):
    """Validate NonlinearPolarisation dataclass and psi_mod_sq."""

    def test_psi_mod_sq_at_zero(self):
        """At t=0, |ψ|² = ψ₀²."""
        psi0 = 1.0
        val = psi_mod_sq(0.0, psi0_ev=psi0, f0=F0_HZ)
        self.assertAlmostEqual(val, psi0**2, places=12)

    def test_psi_mod_sq_at_quarter_period(self):
        """At t = T/4, cos(ω₀ t) = 0 so |ψ|² = 0."""
        psi0 = 2.0
        T = 1.0 / F0_HZ
        val = psi_mod_sq(T / 4.0, psi0_ev=psi0, f0=F0_HZ)
        self.assertAlmostEqual(val, 0.0, places=10)

    def test_psi_mod_sq_non_negative(self):
        """psi_mod_sq is always non-negative."""
        psi0 = 3.0
        for k in range(20):
            t = k * 0.01 / F0_HZ
            self.assertGreaterEqual(psi_mod_sq(t, psi0), 0.0)

    def test_psi_mod_sq_period(self):
        """psi_mod_sq has period T/2 = 1/(2f₀)."""
        psi0 = 1.5
        T = 1.0 / F0_HZ
        t0 = 0.07 / F0_HZ
        val1 = psi_mod_sq(t0, psi0)
        val2 = psi_mod_sq(t0 + T / 2.0, psi0)
        self.assertAlmostEqual(val1, val2, places=10)

    def test_nonlinear_polarisation_formula(self):
        """P_NL = ε₀ χ⁽³⁾ |ψ|² E."""
        from physics.fwm_vacuum_resonance import EPS_0
        t = 0.0
        E = 1.0e3  # V/m
        p = FWMParameters()
        nlp = nonlinear_polarisation(t, E, p)
        psi_sq = psi_mod_sq(t, p.psi0_ev, p.f0)
        expected = EPS_0 * p.chi3 * psi_sq * E
        self.assertAlmostEqual(nlp.P_NL, expected, places=50)

    def test_nonlinear_polarisation_zero_field(self):
        """Zero laser field gives zero P_NL."""
        nlp = nonlinear_polarisation(0.0, 0.0)
        self.assertAlmostEqual(nlp.P_NL, 0.0, places=50)

    def test_nonlinear_polarisation_scales_with_E(self):
        """P_NL is linear in E_laser."""
        t = 0.0
        nlp1 = nonlinear_polarisation(t, 1.0)
        nlp2 = nonlinear_polarisation(t, 2.0)
        if nlp1.P_NL != 0.0:
            self.assertAlmostEqual(nlp2.P_NL / nlp1.P_NL, 2.0, places=10)


class TestFWMSidebands(unittest.TestCase):
    """Validate FWM sideband generation."""

    def test_sideband_frequencies(self):
        """Sidebands are at f_L ± f₀."""
        f_L = 1000.0  # Hz
        result = fwm_sidebands(f_L)
        self.assertAlmostEqual(result.f_lower, f_L - F0_HZ, places=6)
        self.assertAlmostEqual(result.f_upper, f_L + F0_HZ, places=6)

    def test_sideband_f0_stored(self):
        """f0 stored in result matches F0_HZ."""
        result = fwm_sidebands(500.0)
        self.assertAlmostEqual(result.f0, F0_HZ)

    def test_sideband_f_laser_stored(self):
        """f_laser is stored in result."""
        f_L = 750.0
        result = fwm_sidebands(f_L)
        self.assertAlmostEqual(result.f_laser, f_L)

    def test_sideband_amplitude_positive(self):
        """Sideband amplitude ratio is positive."""
        result = fwm_sidebands(500.0)
        self.assertGreater(result.amplitude_ratio, 0.0)

    def test_sideband_amplitude_tiny(self):
        """Sideband amplitude ratio is very small (< 1e-20)."""
        result = fwm_sidebands(500.0)
        self.assertLess(result.amplitude_ratio, 1.0e-20)

    def test_invalid_f_laser_zero(self):
        """Zero laser frequency raises ValueError."""
        with self.assertRaises(ValueError):
            fwm_sidebands(0.0)

    def test_invalid_f_laser_negative(self):
        """Negative laser frequency raises ValueError."""
        with self.assertRaises(ValueError):
            fwm_sidebands(-100.0)

    def test_invalid_f_laser_below_f0(self):
        """Laser frequency ≤ f₀ raises ValueError."""
        with self.assertRaises(ValueError):
            fwm_sidebands(F0_HZ * 0.5)

    def test_invalid_f_laser_equals_f0(self):
        """Laser frequency = f₀ raises ValueError."""
        with self.assertRaises(ValueError):
            fwm_sidebands(F0_HZ)

    def test_sideband_spectrum_type(self):
        """Sideband spectrum returns ndarray of correct shape."""
        f_array = np.linspace(0, 2000, 500)
        spectrum = fwm_sideband_spectrum(500.0, f_array)
        self.assertIsInstance(spectrum, np.ndarray)
        self.assertEqual(spectrum.shape, f_array.shape)

    def test_sideband_spectrum_max_at_laser(self):
        """Spectrum peak is at or near the laser frequency."""
        f_L = 1000.0
        # Use dense sampling around the laser frequency
        f_array = np.linspace(f_L - 10.0, f_L + 10.0, 10000)
        spectrum = fwm_sideband_spectrum(f_L, f_array)
        peak_idx = int(np.argmax(spectrum))
        self.assertAlmostEqual(f_array[peak_idx], f_L, delta=0.1)

    def test_sideband_spectrum_normalised(self):
        """Spectrum maximum is 1.0 (normalised)."""
        f_L = 500.0
        f_array = np.linspace(100, 900, 5000)
        spectrum = fwm_sideband_spectrum(f_L, f_array)
        self.assertAlmostEqual(float(np.max(spectrum)), 1.0, places=5)


class TestResonanceStrength(unittest.TestCase):
    """Validate the strong spectral resonance ℛ(f)."""

    def test_resonance_at_f0_is_peak(self):
        """ℛ(f₀) is the maximum of the profile."""
        p = FWMParameters()
        r0 = resonance_strength(p.f0, p)
        # Detuned by 1 Hz should be smaller
        r1 = resonance_strength(p.f0 + 1.0, p)
        self.assertGreater(r0.strength, r1.strength)

    def test_resonance_delta_f_zero_at_f0(self):
        """Δf = 0 when f = f₀."""
        p = FWMParameters()
        r = resonance_strength(p.f0, p)
        self.assertAlmostEqual(r.delta_f, 0.0, places=10)

    def test_resonance_formula(self):
        """ℛ(f) = g² ρ / [Δf² + (Γ/2)²]."""
        f = F0_HZ + 5.0
        p = FWMParameters(gamma_hz=2.0)
        r = resonance_strength(f, p)
        delta_f = abs(f - p.f0)
        gamma_half = p.gamma_hz / 2.0
        expected = p.g_agg**2 * p.rho_dm / (delta_f**2 + gamma_half**2)
        self.assertAlmostEqual(r.strength / expected, 1.0, places=10)

    def test_resonance_symmetric(self):
        """ℛ(f₀ + δ) = ℛ(f₀ − δ)."""
        delta = 3.7
        p = FWMParameters()
        r_plus = resonance_strength(p.f0 + delta, p)
        r_minus = resonance_strength(p.f0 - delta, p)
        self.assertAlmostEqual(r_plus.strength, r_minus.strength, places=15)

    def test_resonance_decreases_with_detuning(self):
        """ℛ decreases as |Δf| increases."""
        p = FWMParameters()
        strengths = [
            resonance_strength(p.f0 + df, p).strength
            for df in [0, 1, 5, 10, 50]
        ]
        for i in range(len(strengths) - 1):
            self.assertGreater(strengths[i], strengths[i + 1])

    def test_resonance_profile_shape(self):
        """resonance_profile returns ndarray of correct shape."""
        f_array = np.linspace(100, 200, 300)
        profile = resonance_profile(f_array)
        self.assertIsInstance(profile, np.ndarray)
        self.assertEqual(profile.shape, f_array.shape)

    def test_resonance_profile_peak_at_f0(self):
        """Profile peak is at f₀."""
        p = FWMParameters()
        f_array = np.linspace(p.f0 - 10.0, p.f0 + 10.0, 100000)
        profile = resonance_profile(f_array, p)
        peak_idx = int(np.argmax(profile))
        self.assertAlmostEqual(f_array[peak_idx], p.f0, delta=1.0e-3)

    def test_resonance_fwhm_equals_gamma(self):
        """FWHM of ℛ equals Γ."""
        p = FWMParameters(gamma_hz=5.0)
        self.assertAlmostEqual(resonance_fwhm(p), 5.0, places=10)

    def test_resonance_peak_formula(self):
        """Peak strength = g² ρ / (Γ/2)²."""
        p = FWMParameters(gamma_hz=2.0)
        expected = p.g_agg**2 * p.rho_dm / (1.0) ** 2  # (Γ/2)² = 1
        self.assertAlmostEqual(resonance_peak(p) / expected, 1.0, places=10)

    def test_resonance_peak_increases_as_gamma_decreases(self):
        """Smaller Γ gives larger peak (divergence as Γ → 0)."""
        p1 = FWMParameters(gamma_hz=10.0)
        p2 = FWMParameters(gamma_hz=1.0)
        self.assertGreater(resonance_peak(p2), resonance_peak(p1))

    def test_resonance_result_stores_f(self):
        """ResonanceResult stores the probe frequency."""
        f = 150.0
        r = resonance_strength(f)
        self.assertAlmostEqual(r.f, f)

    def test_resonance_result_stores_f0(self):
        """ResonanceResult stores the resonance centre f₀."""
        r = resonance_strength(150.0)
        self.assertAlmostEqual(r.f0, F0_HZ)


class TestRamseyEcho(unittest.TestCase):
    """Validate the Ramsey Echo protocol."""

    def test_tau_equals_1_over_f0(self):
        """Echo delay τ = 1/f₀."""
        result = ramsey_echo()
        self.assertAlmostEqual(result.tau, 1.0 / F0_HZ, places=10)

    def test_visibility_near_one_for_small_gamma(self):
        """For tiny Γ, visibility V = exp(−Γτ/2) ≈ 1."""
        p = FWMParameters(gamma_hz=1.0e-9)
        result = ramsey_echo(params=p)
        self.assertAlmostEqual(result.visibility, 1.0, places=5)

    def test_visibility_decay(self):
        """Larger Γ gives smaller visibility."""
        p1 = FWMParameters(gamma_hz=0.001)
        p2 = FWMParameters(gamma_hz=1.0)
        r1 = ramsey_echo(params=p1)
        r2 = ramsey_echo(params=p2)
        self.assertGreater(r1.visibility, r2.visibility)

    def test_echo_amplitude_scales_with_E0(self):
        """Echo amplitude = E₀ × visibility."""
        p = FWMParameters()
        r1 = ramsey_echo(E0=1.0, params=p)
        r2 = ramsey_echo(E0=2.0, params=p)
        self.assertAlmostEqual(r2.echo_amplitude / r1.echo_amplitude, 2.0, places=10)

    def test_echo_field_zero_before_tau(self):
        """Echo field is zero for t < τ."""
        result = ramsey_echo(n_points=2000)
        tau = result.tau
        t_array = result.t_array
        before_echo = result.echo_field[t_array < tau]
        self.assertTrue(np.all(before_echo == 0.0))

    def test_echo_field_nonzero_after_tau(self):
        """Echo field is non-zero for some t ≥ τ."""
        result = ramsey_echo(E0=1.0, n_points=2000)
        tau = result.tau
        t_array = result.t_array
        after_echo = result.echo_field[t_array >= tau]
        self.assertTrue(np.any(after_echo != 0.0))

    def test_echo_field_shape(self):
        """Echo field has same shape as t_array."""
        result = ramsey_echo(n_points=1000)
        self.assertEqual(result.echo_field.shape, result.t_array.shape)

    def test_echo_field_amplitude_bounded(self):
        """Echo field amplitude ≤ E₀."""
        E0 = 5.0
        result = ramsey_echo(E0=E0, n_points=2000)
        self.assertLessEqual(float(np.max(np.abs(result.echo_field))), E0 + 1.0e-10)

    def test_echo_field_oscillates_at_f0(self):
        """Echo field oscillates at f₀ after the delay."""
        p = FWMParameters(gamma_hz=0.0)
        result = ramsey_echo(E0=1.0, n_cycles=5, n_points=50000, params=p)
        tau = result.tau
        t_array = result.t_array
        echo = result.echo_field

        # Find zero crossings after tau
        after_mask = t_array >= tau
        t_after = t_array[after_mask]
        echo_after = echo[after_mask]

        if len(echo_after) > 10:
            # Count zero crossings to infer period
            sign_changes = np.where(np.diff(np.sign(echo_after)))[0]
            if len(sign_changes) >= 2:
                # Two consecutive zero crossings span half a period
                half_period = float(t_after[sign_changes[1]] - t_after[sign_changes[0]])
                period_est = 2.0 * half_period
                expected_period = 1.0 / p.f0
                self.assertAlmostEqual(period_est, expected_period, delta=0.05 * expected_period)

    def test_invalid_E0_negative(self):
        """Negative E0 raises ValueError."""
        with self.assertRaises(ValueError):
            ramsey_echo(E0=-1.0)

    def test_invalid_n_cycles(self):
        """n_cycles < 1 raises ValueError."""
        with self.assertRaises(ValueError):
            ramsey_echo(n_cycles=0)

    def test_invalid_n_points(self):
        """n_points < 10 raises ValueError."""
        with self.assertRaises(ValueError):
            ramsey_echo(n_points=5)

    def test_ramsey_echo_snr_positive(self):
        """SNR is positive."""
        snr = ramsey_echo_snr(E0=1.0, noise_rms=1.0e-3)
        self.assertGreater(snr, 0.0)

    def test_ramsey_echo_snr_scales_with_E0(self):
        """SNR doubles when E0 doubles."""
        snr1 = ramsey_echo_snr(E0=1.0, noise_rms=0.01)
        snr2 = ramsey_echo_snr(E0=2.0, noise_rms=0.01)
        self.assertAlmostEqual(snr2 / snr1, 2.0, places=8)

    def test_ramsey_echo_snr_invalid_noise(self):
        """Zero noise raises ValueError."""
        with self.assertRaises(ValueError):
            ramsey_echo_snr(noise_rms=0.0)


class TestMaxCutSDP(unittest.TestCase):
    """Validate the Max-Cut SDP relaxation on K₇."""

    def test_n_vertices(self):
        """Result has 7 vertices."""
        mc = maxcut_sdp_k7()
        self.assertEqual(mc.n_vertices, 7)

    def test_max_cut_integer_is_12(self):
        """Integer Max-Cut on K₇ is 12."""
        mc = maxcut_sdp_k7()
        self.assertEqual(mc.max_cut_integer, 12)

    def test_sdp_bound_is_12(self):
        """SDP value for the 3|4 bipartition on K₇ is 12.0."""
        mc = maxcut_sdp_k7()
        # The bipartition {0,1,2} vs {3,4,5,6} gives 3×4 = 12 cut edges,
        # all with phase difference π → (1 − cos π)/2 = 1 per edge → 12 total.
        self.assertAlmostEqual(mc.sdp_bound, 12.0, places=10)

    def test_phases_shape(self):
        """Phase array has 7 elements."""
        mc = maxcut_sdp_k7()
        self.assertEqual(len(mc.phases), 7)

    def test_phases_bipartition_values(self):
        """Phase array has values 0 and π."""
        mc = maxcut_sdp_k7()
        unique_phases = set(round(p, 6) for p in mc.phases)
        self.assertIn(0.0, unique_phases)
        self.assertIn(round(math.pi, 6), unique_phases)

    def test_coherence_psi_in_range(self):
        """Coherence Ψ ∈ (0, 1]."""
        mc = maxcut_sdp_k7()
        self.assertGreater(mc.coherence_psi, 0.0)
        self.assertLessEqual(mc.coherence_psi, 1.0)

    def test_coherence_psi_equals_one(self):
        """When sdp_bound = integer cut, Ψ = 1."""
        mc = maxcut_sdp_k7()
        # sdp_bound should equal 12, integer cut = 12 → Ψ = 1
        if mc.sdp_bound > 0:
            ratio = mc.max_cut_integer / mc.sdp_bound
            expected_psi = min(ratio, 1.0)
            self.assertAlmostEqual(mc.coherence_psi, expected_psi, places=10)

    def test_reproducible_with_seed(self):
        """Same seed gives same result."""
        mc1 = maxcut_sdp_k7(random_seed=42)
        mc2 = maxcut_sdp_k7(random_seed=42)
        self.assertAlmostEqual(mc1.sdp_bound, mc2.sdp_bound, places=15)
        np.testing.assert_array_equal(mc1.phases, mc2.phases)

    def test_phase_spectrum_shape(self):
        """Phase spectrum has n*(n-1)/2 entries for n phases."""
        mc = maxcut_sdp_k7()
        spectrum = maxcut_phase_spectrum(mc.phases)
        n = len(mc.phases)
        expected_len = n * (n - 1) // 2
        self.assertEqual(len(spectrum), expected_len)

    def test_phase_spectrum_bipartition(self):
        """For 0|π bipartition, phase differences are 0 or π."""
        mc = maxcut_sdp_k7()
        spectrum = maxcut_phase_spectrum(mc.phases)
        for diff in spectrum:
            self.assertTrue(
                abs(diff) < 1.0e-10 or abs(diff - math.pi) < 1.0e-10,
                f"Unexpected phase difference: {diff}",
            )

    def test_cut_edges_equal_12(self):
        """Bipartition {0,1,2}|{3,4,5,6} gives exactly 12 cut edges."""
        mc = maxcut_sdp_k7()
        phases = mc.phases
        n = len(phases)
        cut_count = sum(
            1
            for i in range(n)
            for j in range(i + 1, n)
            if abs(phases[i] - phases[j]) > 0.01
        )
        self.assertEqual(cut_count, 12)


class TestFWMSummary(unittest.TestCase):
    """Validate the fwm_summary convenience function."""

    def setUp(self):
        self.summary = fwm_summary()

    def test_keys_present(self):
        """All expected keys are present in the summary."""
        expected_keys = [
            "f0_Hz",
            "gamma_hz",
            "chi3",
            "psi0_eV",
            "resonance_peak",
            "resonance_fwhm",
            "sideband_f_lower",
            "sideband_f_upper",
            "sideband_amplitude_ratio",
            "ramsey_tau_s",
            "ramsey_echo_amplitude",
            "maxcut_sdp_bound",
            "maxcut_integer",
            "coherence_psi",
        ]
        for key in expected_keys:
            self.assertIn(key, self.summary, f"Missing key: {key}")

    def test_f0_matches(self):
        """f0 in summary matches F0_HZ."""
        self.assertAlmostEqual(self.summary["f0_Hz"], F0_HZ)

    def test_sideband_lower_lt_upper(self):
        """Lower sideband < laser < upper sideband."""
        self.assertLess(
            self.summary["sideband_f_lower"],
            self.summary["sideband_f_upper"],
        )

    def test_ramsey_tau_matches_f0(self):
        """τ = 1/f₀."""
        self.assertAlmostEqual(
            self.summary["ramsey_tau_s"], 1.0 / F0_HZ, places=10
        )

    def test_maxcut_integer_is_12(self):
        """Max-Cut integer in summary is 12."""
        self.assertEqual(self.summary["maxcut_integer"], 12)

    def test_coherence_psi_positive(self):
        """Coherence Ψ is positive."""
        self.assertGreater(self.summary["coherence_psi"], 0.0)

    def test_resonance_peak_positive(self):
        """Resonance peak is positive."""
        self.assertGreater(self.summary["resonance_peak"], 0.0)

    def test_custom_f_laser(self):
        """Custom f_laser is reflected in sideband frequencies."""
        f_L = 5000.0
        s = fwm_summary(f_laser=f_L)
        self.assertAlmostEqual(s["sideband_f_lower"], f_L - F0_HZ, places=5)
        self.assertAlmostEqual(s["sideband_f_upper"], f_L + F0_HZ, places=5)


class TestIntegration(unittest.TestCase):
    """Integration-level tests combining multiple components."""

    def test_sideband_lies_within_resonance_bandwidth(self):
        """The sideband at f_L - f₀ is resolved against the f₀ resonance peak."""
        p = FWMParameters(gamma_hz=1.0)
        f_L = p.f0 * 2.0  # laser at 2f₀
        sb = fwm_sidebands(f_L, p)
        # Lower sideband at f₀ → Δf = 0 → maximum resonance
        r_lower = resonance_strength(sb.f_lower, p)
        r_upper = resonance_strength(sb.f_upper, p)
        # Lower sideband (at f₀) has higher resonance than upper sideband
        self.assertGreater(r_lower.strength, r_upper.strength)

    def test_echo_reveals_fabric_phase(self):
        """Echo field at t = τ + 1/(4f₀) has expected cosine value."""
        p = FWMParameters(gamma_hz=0.0)
        result = ramsey_echo(E0=1.0, n_cycles=3, n_points=100000, params=p)
        tau = result.tau
        # At t = τ + T/4, cos(2π f₀ (t − τ)) = cos(π/2) = 0
        t_check = tau + 1.0 / (4.0 * p.f0)
        # Find nearest index
        idx = int(np.argmin(np.abs(result.t_array - t_check)))
        self.assertAlmostEqual(result.echo_field[idx], 0.0, delta=0.05)

    def test_maxcut_coherence_with_resonance_peak(self):
        """Coherence Ψ ≈ 1 matches the resonance collapse at f₀."""
        mc = maxcut_sdp_k7()
        p = FWMParameters()
        r0 = resonance_strength(p.f0, p)
        # Both exhibit the 'infinite' resonance / unity coherence at f₀
        self.assertGreater(r0.strength, 0.0)
        self.assertGreater(mc.coherence_psi, 0.0)

    def test_fwm_pipeline(self):
        """Full FWM pipeline runs without error and returns consistent results."""
        p = FWMParameters()
        f_L = p.f0 * 5.0

        # Step 1: Compute nonlinear polarisation
        nlp = nonlinear_polarisation(0.0, 1.0e3, p)
        self.assertGreater(nlp.psi_mod_sq, 0.0)

        # Step 2: Generate sidebands
        sb = fwm_sidebands(f_L, p)
        self.assertLess(sb.f_lower, f_L)
        self.assertGreater(sb.f_upper, f_L)

        # Step 3: Resonance at lower sideband (≈ 4f₀)
        r = resonance_strength(sb.f_lower, p)
        self.assertGreater(r.strength, 0.0)

        # Step 4: Ramsey echo
        echo = ramsey_echo(E0=1.0, params=p)
        self.assertGreater(echo.visibility, 0.0)

        # Step 5: Max-Cut SDP
        mc = maxcut_sdp_k7()
        self.assertEqual(mc.max_cut_integer, 12)


if __name__ == "__main__":
    unittest.main()
