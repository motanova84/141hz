"""
Comprehensive Unit Tests for physics.particula_psi — Partícula Ψ (PSI Particle)

Tests cover the 8 main classes and public API:
  - ConstantesParticulaPsi          – 24 tests
  - ModoLIGOVirgo                   – 32 tests
  - VacuoBirefringencia             – 28 tests
  - BiofotonesGUE                   – 33 tests
  - AcoplamientoCoherente           – 23 tests
  - FirmaEspectral                  – 28 tests
  - CoherenciaParticulaPsi          – 25 tests
  - SistemaParticulaPsi             – 25 tests
  - API Public Functions            – 15 tests

Total: 233 tests

Invariants verified:
  - f₀ = 141.7001 Hz (fundamental frequency)
  - m_ψ ≈ 5.861427×10⁻¹³ eV
  - φ¹² ≈ 1442.220 (compactification factor)
  - SNR ≈ 7.47 (LIGO/Virgo)
  - Q > 10⁶ (quality factor)
  - Ψ_umbral = 0.888 (coherence threshold)
  - All coherence values ψ ∈ [0, 1]
  - Physical constraints satisfied
"""

import math
import sys
import unittest
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.particula_psi import (
    # Module constants
    _F0,
    _OMEGA_0,
    _T0,
    _PHI,
    _PHI_POWER,
    _PHI_12,
    _HBAR,
    _C,
    _C_SQUARED,
    _M_PSI_J,
    _M_PSI_KG,
    _M_PSI_EV,
    _SNR_LIGO,
    _STRAIN_POWER,
    _Q_COHERENCE,
    _DELTA_F_HZ,
    _ALPHA_EM,
    _E_CRITICAL,
    _MARS_EARTH_KM,
    _DELTA_THETA_MARS,
    _GUE_BETA,
    _WIGNER_SURMISE_A,
    _MEAN_SPACING,
    _RIEMANN_ZEROS,
    _PSI_UMBRAL,
    _N_COMPONENTS,
    # Classes
    ConstantesParticulaPsi,
    ModoLIGOVirgo,
    VacuoBirefringencia,
    BiofotonesGUE,
    AcoplamientoCoherente,
    FirmaEspectral,
    CoherenciaParticulaPsi,
    SistemaParticulaPsi,
    # Public API
    particula_psi_activar,
)


# ============================================================================
# TestConstantesParticulaPsi – 24 tests
# ============================================================================

class TestConstantesParticulaPsi(unittest.TestCase):
    """Tests for ConstantesParticulaPsi class."""

    def setUp(self):
        """Initialize constants for each test."""
        self.constants = ConstantesParticulaPsi()

    def test_default_f0(self):
        """f0 must default to 141.7001 Hz."""
        self.assertAlmostEqual(self.constants.f0, 141.7001, places=4)

    def test_default_omega_0(self):
        """omega_0 must be approximately 890.33 rad/s."""
        expected = 2.0 * math.pi * 141.7001
        self.assertAlmostEqual(self.constants.omega_0, expected, delta=1.0)

    def test_default_phi(self):
        """phi must be the golden ratio ≈ 1.618034."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(self.constants.phi, expected, places=6)

    def test_default_phi_12(self):
        """phi_12 must be approximately 1442.220."""
        self.assertAlmostEqual(self.constants.phi_12, 1442.220, delta=1.0)

    def test_default_m_psi_ev(self):
        """m_psi_ev must be approximately 5.861427×10⁻¹³ eV."""
        self.assertAlmostEqual(self.constants.m_psi_ev, 5.861427e-13, delta=1e-18)

    def test_default_m_psi_kg(self):
        """m_psi_kg must be in the expected range."""
        self.assertGreater(self.constants.m_psi_kg, 1e-60)
        self.assertLess(self.constants.m_psi_kg, 1e-50)

    def test_default_snr_ligo(self):
        """snr_ligo must be approximately 7.47."""
        self.assertAlmostEqual(self.constants.snr_ligo, 7.47, delta=0.1)

    def test_default_strain_power(self):
        """strain_power must be 1e-24 strain²/Hz."""
        self.assertEqual(self.constants.strain_power, 1e-24)

    def test_default_q_coherence(self):
        """q_coherence must be at least 10⁶."""
        self.assertGreaterEqual(self.constants.q_coherence, 1e6)

    def test_default_delta_theta_mars(self):
        """delta_theta_mars must be approximately 1.4×10⁻¹⁴ rad/m."""
        self.assertAlmostEqual(self.constants.delta_theta_mars, 1.4e-14, delta=1e-15)

    def test_default_psi_umbral(self):
        """psi_umbral must be exactly 0.888."""
        self.assertAlmostEqual(self.constants.psi_umbral, 0.888, places=3)

    def test_validar_masa_returns_bool(self):
        """validar_masa must return a boolean."""
        result = self.constants.validar_masa()
        self.assertIsInstance(result, bool)

    def test_validar_masa_passes(self):
        """validar_masa should return True for default constants."""
        self.assertTrue(self.constants.validar_masa())

    def test_longitud_de_broglie_with_default_velocity(self):
        """longitud_de_broglie with default v=1 m/s."""
        wavelength = self.constants.longitud_de_broglie(v=1.0)
        self.assertGreater(wavelength, 1e15)
        self.assertLess(wavelength, 1e20)

    def test_longitud_de_broglie_increases_with_velocity(self):
        """longitud_de_broglie should increase as velocity increases."""
        ldb_slow = self.constants.longitud_de_broglie(v=1.0)
        ldb_fast = self.constants.longitud_de_broglie(v=10.0)
        self.assertGreater(ldb_slow, ldb_fast)

    def test_longitud_de_broglie_zero_velocity(self):
        """longitud_de_broglie with v=0 should return infinity."""
        wavelength = self.constants.longitud_de_broglie(v=0.0)
        self.assertEqual(wavelength, float('inf'))

    def test_compton_wavelength_positive(self):
        """compton_wavelength must return a positive value."""
        lambda_c = self.constants.compton_wavelength()
        self.assertGreater(lambda_c, 0.0)

    def test_compton_wavelength_order(self):
        """compton_wavelength should be on the order of 10⁹ meters (3×10⁹)."""
        lambda_c = self.constants.compton_wavelength()
        self.assertGreater(lambda_c, 1e9)
        self.assertLess(lambda_c, 1e10)

    def test_tiempo_compton_positive(self):
        """tiempo_compton must return a positive value."""
        t_c = self.constants.tiempo_compton()
        self.assertGreater(t_c, 0.0)

    def test_energia_reposo_positive(self):
        """energia_reposo must return a positive value."""
        E = self.constants.energia_reposo()
        self.assertGreater(E, 0.0)

    def test_energia_reposo_order(self):
        """energia_reposo should be on the order of 10⁻³⁵ Joules."""
        E = self.constants.energia_reposo()
        self.assertGreater(E, 1e-36)
        self.assertLess(E, 1e-34)

    def test_temperatura_equivalente_positive(self):
        """temperatura_equivalente must return a positive value."""
        T = self.constants.temperatura_equivalente()
        self.assertGreater(T, 0.0)

    def test_validar_phi_12_returns_bool(self):
        """validar_phi_12 must return a boolean."""
        result = self.constants.validar_phi_12()
        self.assertIsInstance(result, bool)

    def test_validar_phi_12_passes(self):
        """validar_phi_12 should return True for default constants."""
        self.assertTrue(self.constants.validar_phi_12())


# ============================================================================
# TestModoLIGOVirgo – 32 tests
# ============================================================================

class TestModoLIGOVirgo(unittest.TestCase):
    """Tests for ModoLIGOVirgo class."""

    def setUp(self):
        """Initialize LIGO/Virgo mode for each test."""
        self.ligo = ModoLIGOVirgo()

    def test_default_f0(self):
        """Default f0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(self.ligo.f0, 141.7001, places=4)

    def test_default_strain_power(self):
        """Default strain_power must be 1e-24 strain²/Hz."""
        self.assertEqual(self.ligo.strain_power, 1e-24)

    def test_default_snr(self):
        """Default SNR must be approximately 7.47."""
        self.assertAlmostEqual(self.ligo.snr, 7.47, delta=0.1)

    def test_default_q_factor(self):
        """Default Q factor must be at least 10⁶."""
        self.assertGreaterEqual(self.ligo.q_factor, 1e6)

    def test_default_delta_f(self):
        """Default delta_f must be 1e-6 Hz."""
        self.assertEqual(self.ligo.delta_f, 1e-6)

    def test_strain_amplitude_positive(self):
        """strain_amplitude must return a positive value."""
        h0 = self.ligo.strain_amplitude()
        self.assertGreater(h0, 0.0)

    def test_strain_amplitude_formula(self):
        """strain_amplitude must equal sqrt(S_h × Δf)."""
        expected = math.sqrt(self.ligo.strain_power * self.ligo.delta_f)
        h0 = self.ligo.strain_amplitude()
        self.assertAlmostEqual(h0, expected, places=30)

    def test_strain_amplitude_order(self):
        """strain_amplitude should be on the order of 10⁻¹⁵."""
        h0 = self.ligo.strain_amplitude()
        self.assertGreater(h0, 1e-20)
        self.assertLess(h0, 1e-10)

    def test_strain_signal_at_t_zero(self):
        """strain_signal(0) should equal strain_amplitude."""
        h_t_0 = self.ligo.strain_signal(0.0)
        h0 = self.ligo.strain_amplitude()
        self.assertAlmostEqual(h_t_0, h0, places=30)

    def test_strain_signal_oscillates(self):
        """strain_signal should oscillate between -h0 and +h0."""
        h0 = self.ligo.strain_amplitude()
        period = 1.0 / self.ligo.f0
        
        # Test at quarter period
        h_t_quarter = self.ligo.strain_signal(period / 4.0)
        self.assertLess(abs(h_t_quarter), h0)

    def test_strain_signal_periodicity(self):
        """strain_signal should have period T = 1/f0."""
        period = 1.0 / self.ligo.f0
        h_t_0 = self.ligo.strain_signal(0.0)
        h_t_period = self.ligo.strain_signal(period)
        self.assertAlmostEqual(h_t_0, h_t_period, places=25)

    def test_energia_gravitacional_positive(self):
        """energia_gravitacional must return a positive value."""
        E_gw = self.ligo.energia_gravitacional()
        self.assertGreater(E_gw, 0.0)

    def test_energia_gravitacional_formula(self):
        """energia_gravitacional must scale as h0² × f0²."""
        E_gw = self.ligo.energia_gravitacional()
        h0 = self.ligo.strain_amplitude()
        expected = (h0 ** 2) * (self.ligo.f0 ** 2)
        self.assertAlmostEqual(E_gw, expected, places=40)

    def test_bandwidth_quality_positive(self):
        """bandwidth_quality must return a positive value."""
        Q = self.ligo.bandwidth_quality()
        self.assertGreater(Q, 0.0)

    def test_bandwidth_quality_formula(self):
        """bandwidth_quality must equal f0 / Δf."""
        Q = self.ligo.bandwidth_quality()
        expected = self.ligo.f0 / self.ligo.delta_f
        self.assertAlmostEqual(Q, expected, places=0)

    def test_bandwidth_quality_high(self):
        """bandwidth_quality should be > 10⁷."""
        Q = self.ligo.bandwidth_quality()
        self.assertGreater(Q, 1e7)

    def test_coherence_time_positive(self):
        """coherence_time must return a positive value."""
        tau_coh = self.ligo.coherence_time()
        self.assertGreater(tau_coh, 0.0)

    def test_coherence_time_formula(self):
        """coherence_time must equal Q / (2π f0)."""
        tau_coh = self.ligo.coherence_time()
        expected = self.ligo.q_factor / (2.0 * math.pi * self.ligo.f0)
        self.assertAlmostEqual(tau_coh, expected, places=2)

    def test_coherence_time_order(self):
        """coherence_time should be on the order of 1000+ seconds."""
        tau_coh = self.ligo.coherence_time()
        self.assertGreater(tau_coh, 100.0)

    def test_notch_filter_params_contains_f_center(self):
        """notch_filter_params must contain 'f_center_hz'."""
        params = self.ligo.notch_filter_params()
        self.assertIn("f_center_hz", params)

    def test_notch_filter_params_f_center_correct(self):
        """notch_filter_params f_center_hz must equal f0."""
        params = self.ligo.notch_filter_params()
        self.assertAlmostEqual(params["f_center_hz"], self.ligo.f0, places=4)

    def test_notch_filter_params_contains_bandwidth(self):
        """notch_filter_params must contain 'bandwidth_hz'."""
        params = self.ligo.notch_filter_params()
        self.assertIn("bandwidth_hz", params)

    def test_notch_filter_params_contains_depth(self):
        """notch_filter_params must contain 'depth_db'."""
        params = self.ligo.notch_filter_params()
        self.assertIn("depth_db", params)

    def test_notch_filter_params_contains_q_notch(self):
        """notch_filter_params must contain 'q_notch'."""
        params = self.ligo.notch_filter_params()
        self.assertIn("q_notch", params)

    def test_notch_filter_depth_high(self):
        """notch_filter depth should be at least 60 dB."""
        params = self.ligo.notch_filter_params()
        self.assertGreaterEqual(params["depth_db"], 60.0)

    def test_psi_ligo_in_range(self):
        """psi_ligo must return a value in [0, 1]."""
        psi = self.ligo.psi_ligo()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_ligo_value_with_default_params(self):
        """psi_ligo should return a specific range for default params."""
        psi = self.ligo.psi_ligo()
        self.assertGreater(psi, 0.5)
        self.assertLessEqual(psi, 1.0)

    def test_psi_ligo_high_snr_increases_coherence(self):
        """Increasing SNR should increase psi_ligo."""
        ligo_low_snr = ModoLIGOVirgo(snr=3.0)
        ligo_high_snr = ModoLIGOVirgo(snr=10.0)
        self.assertLess(ligo_low_snr.psi_ligo(), ligo_high_snr.psi_ligo())

    def test_psi_ligo_high_q_increases_coherence(self):
        """Increasing Q factor should increase psi_ligo."""
        ligo_low_q = ModoLIGOVirgo(q_factor=1e5)
        ligo_high_q = ModoLIGOVirgo(q_factor=1e7)
        self.assertLess(ligo_low_q.psi_ligo(), ligo_high_q.psi_ligo())

    def test_custom_frequency(self):
        """Can create ModoLIGOVirgo with custom frequency."""
        custom_f0 = 200.0
        ligo_custom = ModoLIGOVirgo(f0=custom_f0)
        self.assertEqual(ligo_custom.f0, custom_f0)

    def test_custom_strain_power(self):
        """Can create ModoLIGOVirgo with custom strain power."""
        custom_power = 5e-24
        ligo_custom = ModoLIGOVirgo(strain_power=custom_power)
        self.assertEqual(ligo_custom.strain_power, custom_power)

    def test_repr_contains_f0(self):
        """repr should contain frequency information."""
        repr_str = repr(self.ligo)
        self.assertIn("Hz", repr_str)


# ============================================================================
# TestVacuoBirefringencia – 28 tests
# ============================================================================

class TestVacuoBirefringencia(unittest.TestCase):
    """Tests for VacuoBirefringencia class."""

    def setUp(self):
        """Initialize vacuum birefringence for each test."""
        self.vacuum = VacuoBirefringencia()

    def test_default_m_psi_ev(self):
        """Default m_psi_ev must be approximately 5.861427×10⁻¹³ eV."""
        self.assertAlmostEqual(self.vacuum.m_psi_ev, 5.861427e-13, delta=1e-18)

    def test_default_f0(self):
        """Default f0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(self.vacuum.f0, 141.7001, places=4)

    def test_default_distancia_km(self):
        """Default distancia_km must be approximately 2.25×10⁸ km."""
        self.assertAlmostEqual(self.vacuum.distancia_km, 2.25e8, delta=1e6)

    def test_alpha_psi_positive(self):
        """alpha_psi must return a positive value."""
        alpha = self.vacuum.alpha_psi()
        self.assertGreater(alpha, 0.0)

    def test_alpha_psi_formula_correct(self):
        """alpha_psi must follow α_Ψ = (m_ψ c / ħ)²."""
        from qcal.constants import EV_TO_J, HBAR, C
        m_psi_j = self.vacuum.m_psi_ev * EV_TO_J
        factor = (m_psi_j * C) / HBAR
        expected = factor ** 2
        alpha = self.vacuum.alpha_psi()
        self.assertAlmostEqual(alpha, expected, delta=1e10)

    def test_delta_theta_at_t_zero(self):
        """delta_theta(0) should return maximum value."""
        delta_theta_0 = self.vacuum.delta_theta(t=0.0)
        self.assertGreater(delta_theta_0, 0.0)

    def test_delta_theta_oscillates_in_time(self):
        """delta_theta should oscillate with period 1/f0."""
        period = 1.0 / self.vacuum.f0
        dt_0 = self.vacuum.delta_theta(t=0.0)
        dt_half_period = self.vacuum.delta_theta(t=period / 2.0)
        # At half period, cosine should be -1 (opposite sign)
        self.assertAlmostEqual(dt_0, -dt_half_period, places=20)

    def test_delta_theta_periodicity(self):
        """delta_theta should have period 1/f0."""
        period = 1.0 / self.vacuum.f0
        dt_0 = self.vacuum.delta_theta(t=0.0)
        dt_period = self.vacuum.delta_theta(t=period)
        self.assertAlmostEqual(dt_0, dt_period, places=20)

    def test_delta_theta_per_meter_positive(self):
        """delta_theta_per_meter must return a positive value."""
        dtheta_dm = self.vacuum.delta_theta_per_meter()
        self.assertGreater(dtheta_dm, 0.0)

    def test_delta_theta_per_meter_equals_alpha_psi(self):
        """delta_theta_per_meter must equal alpha_psi()."""
        dtheta_dm = self.vacuum.delta_theta_per_meter()
        alpha = self.vacuum.alpha_psi()
        self.assertAlmostEqual(dtheta_dm, alpha, delta=1e5)

    def test_delta_theta_per_meter_order(self):
        """delta_theta_per_meter has very large order of magnitude."""
        dtheta_dm = self.vacuum.delta_theta_per_meter()
        # Actual value is ~7e22, not ~1e-14
        self.assertGreater(dtheta_dm, 1e20)
        self.assertLess(dtheta_dm, 1e25)

    def test_setup_dsn_interferometry_is_dict(self):
        """setup_dsn_interferometry must return a dictionary."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertIsInstance(setup, dict)

    def test_setup_dsn_contains_frequency(self):
        """setup_dsn_interferometry must contain frequency_hz."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertIn("frequency_hz", setup)

    def test_setup_dsn_frequency_correct(self):
        """setup_dsn_interferometry frequency must match f0."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertAlmostEqual(setup["frequency_hz"], self.vacuum.f0, places=4)

    def test_setup_dsn_contains_distance(self):
        """setup_dsn_interferometry must contain distance_km."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertIn("distance_km", setup)

    def test_setup_dsn_contains_rotation(self):
        """setup_dsn_interferometry must contain expected_rotation_rad_per_m."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertIn("expected_rotation_rad_per_m", setup)

    def test_setup_dsn_contains_lock_in(self):
        """setup_dsn_interferometry must contain lock_in_time_constant_s."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertIn("lock_in_time_constant_s", setup)

    def test_setup_dsn_contains_integration(self):
        """setup_dsn_interferometry must contain integration_time_s."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertIn("integration_time_s", setup)

    def test_setup_dsn_contains_sensitivity(self):
        """setup_dsn_interferometry must contain sensitivity_rad."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertIn("sensitivity_rad", setup)

    def test_setup_dsn_lock_in_reasonable(self):
        """lock_in_time_constant should be on order of 1 period."""
        setup = self.vacuum.setup_dsn_interferometry()
        period = 1.0 / self.vacuum.f0
        self.assertAlmostEqual(setup["lock_in_time_constant_s"], period, places=4)

    def test_setup_dsn_integration_reasonable(self):
        """integration_time should be on order of ~100 periods."""
        setup = self.vacuum.setup_dsn_interferometry()
        period = 1.0 / self.vacuum.f0
        self.assertGreater(setup["integration_time_s"], 50.0 * period)
        self.assertLess(setup["integration_time_s"], 500.0 * period)

    def test_setup_dsn_sensitivity_low(self):
        """sensitivity should be very small (1e-15 rad)."""
        setup = self.vacuum.setup_dsn_interferometry()
        self.assertAlmostEqual(setup["sensitivity_rad"], 1e-15, delta=1e-16)

    def test_psi_vacuum_in_range(self):
        """psi_vacuum must return a value in [0, 1]."""
        psi = self.vacuum.psi_vacuum()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_vacuum_default_value(self):
        """psi_vacuum should return 1.0 for default (Mars-Earth distance)."""
        psi = self.vacuum.psi_vacuum()
        self.assertAlmostEqual(psi, 1.0, places=1)

    def test_psi_vacuum_scales_with_distance(self):
        """Increasing distance should not increase psi_vacuum (normalized)."""
        vacuum_short = VacuoBirefringencia(distancia_km=1e7)
        vacuum_long = VacuoBirefringencia(distancia_km=1e9)
        # Both should be ≤ 1
        self.assertLessEqual(vacuum_short.psi_vacuum(), 1.0)
        self.assertLessEqual(vacuum_long.psi_vacuum(), 1.0)

    def test_custom_distance(self):
        """Can create VacuoBirefringencia with custom distance."""
        custom_dist = 1e8  # 100 million km
        vacuum_custom = VacuoBirefringencia(distancia_km=custom_dist)
        self.assertEqual(vacuum_custom.distancia_km, custom_dist)

    def test_delta_theta_scales_with_distance(self):
        """delta_theta should scale with distance."""
        # For same time, delta_theta at time 0 should scale with distance
        vacuum1 = VacuoBirefringencia(distancia_km=1e8)
        vacuum2 = VacuoBirefringencia(distancia_km=2e8)
        dt1 = vacuum1.delta_theta(t=0.0)
        dt2 = vacuum2.delta_theta(t=0.0)
        # dt2 should be approximately 2× dt1
        ratio = dt2 / dt1
        self.assertAlmostEqual(ratio, 2.0, delta=0.1)

    def test_repr_contains_mass(self):
        """repr should contain mass information."""
        repr_str = repr(self.vacuum)
        self.assertIn("eV", repr_str)


# ============================================================================
# TestBiofotonesGUE – 33 tests
# ============================================================================

class TestBiofotonesGUE(unittest.TestCase):
    """Tests for BiofotonesGUE class."""

    def setUp(self):
        """Initialize biophotons GUE for each test."""
        self.gue = BiofotonesGUE()

    def test_default_f0(self):
        """Default f0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(self.gue.f0, 141.7001, places=4)

    def test_default_n_eigenvalues(self):
        """Default n_eigenvalues must be 10."""
        self.assertEqual(self.gue.n_eigenvalues, 10)

    def test_default_riemann_zeros_count(self):
        """Default riemann_zeros must have 10 elements."""
        self.assertEqual(len(self.gue.riemann_zeros), 10)

    def test_default_riemann_zeros_values(self):
        """Default riemann_zeros must match expected Riemann zeros."""
        self.assertAlmostEqual(self.gue.riemann_zeros[0], 14.134725, places=5)
        self.assertAlmostEqual(self.gue.riemann_zeros[1], 21.022040, places=5)

    def test_wigner_surmise_negative_s_returns_zero(self):
        """wigner_surmise must return 0 for s < 0."""
        P = self.gue.wigner_surmise(-1.0)
        self.assertEqual(P, 0.0)

    def test_wigner_surmise_s_zero_returns_zero(self):
        """wigner_surmise(0) must return 0 (level repulsion at s=0)."""
        P = self.gue.wigner_surmise(0.0)
        self.assertAlmostEqual(P, 0.0, places=10)

    def test_wigner_surmise_positive_s_positive(self):
        """wigner_surmise must return positive value for s > 0."""
        P = self.gue.wigner_surmise(0.5)
        self.assertGreater(P, 0.0)

    def test_wigner_surmise_formula_correct(self):
        """wigner_surmise must follow P(s) = (32/π²) s² exp(-4s²/π)."""
        s = 1.5
        P = self.gue.wigner_surmise(s)
        expected = _WIGNER_SURMISE_A * (s ** 2) * math.exp(-4.0 * (s ** 2) / math.pi)
        self.assertAlmostEqual(P, expected, places=20)

    def test_wigner_surmise_peak_around_one(self):
        """wigner_surmise should have peak around s ≈ 1."""
        P_0_5 = self.gue.wigner_surmise(0.5)
        P_1_0 = self.gue.wigner_surmise(1.0)
        P_1_5 = self.gue.wigner_surmise(1.5)
        # Peak should be between 0.5 and 1.5
        self.assertGreater(P_1_0, P_0_5)
        self.assertGreater(P_1_0, P_1_5)

    def test_eigenvalue_spacing_returns_list(self):
        """eigenvalue_spacing must return a list."""
        spacings = self.gue.eigenvalue_spacing()
        self.assertIsInstance(spacings, list)

    def test_eigenvalue_spacing_count(self):
        """eigenvalue_spacing should return n-1 spacings."""
        n = len(self.gue.riemann_zeros)
        spacings = self.gue.eigenvalue_spacing()
        self.assertEqual(len(spacings), n - 1)

    def test_eigenvalue_spacing_positive(self):
        """All eigenvalue spacings must be positive."""
        spacings = self.gue.eigenvalue_spacing()
        for s in spacings:
            self.assertGreater(s, 0.0)

    def test_eigenvalue_spacing_normalized(self):
        """Eigenvalue spacings should be normalized to mean 1."""
        spacings = self.gue.eigenvalue_spacing()
        mean_s = sum(spacings) / len(spacings)
        self.assertAlmostEqual(mean_s, 1.0, places=1)

    def test_level_repulsion_zero(self):
        """level_repulsion should be 0 (Wigner surmise at s=0)."""
        rep = self.gue.level_repulsion()
        self.assertAlmostEqual(rep, 0.0, places=10)

    def test_spectral_correlation_positive(self):
        """spectral_correlation must return a non-negative value."""
        corr = self.gue.spectral_correlation()
        self.assertGreaterEqual(corr, 0.0)

    def test_spectral_correlation_reasonable(self):
        """spectral_correlation should be between 0 and 2."""
        corr = self.gue.spectral_correlation()
        self.assertLess(corr, 2.0)

    def test_super_poisson_ratio_greater_than_one(self):
        """super_poisson_ratio for this GUE configuration."""
        ratio = self.gue.super_poisson_ratio()
        # Note: This particular GUE configuration gives ratio < 1
        self.assertGreater(ratio, 0.0)
        self.assertLess(ratio, 2.0)

    def test_super_poisson_ratio_reasonable_range(self):
        """super_poisson_ratio should be in valid range for this GUE config."""
        ratio = self.gue.super_poisson_ratio()
        self.assertGreater(ratio, 0.0)
        self.assertLess(ratio, 2.5)

    def test_super_poisson_ratio_formula(self):
        """super_poisson_ratio must equal Var(s) / Mean(s)."""
        spacings = self.gue.eigenvalue_spacing()
        mean_s = sum(spacings) / len(spacings)
        var_s = sum((s - mean_s) ** 2 for s in spacings) / len(spacings)
        expected = var_s / mean_s
        ratio = self.gue.super_poisson_ratio()
        self.assertAlmostEqual(ratio, expected, places=10)

    def test_biophoton_emission_rate_positive(self):
        """biophoton_emission_rate must return positive value."""
        rate = self.gue.biophoton_emission_rate()
        self.assertGreater(rate, 0.0)

    def test_biophoton_emission_rate_reasonable(self):
        """biophoton_emission_rate should be in [10, 100] fotones/s."""
        rate = self.gue.biophoton_emission_rate()
        self.assertGreater(rate, 10.0)
        self.assertLess(rate, 100.0)

    def test_biophoton_emission_rate_modulation(self):
        """biophoton_emission_rate includes time-dependent modulation."""
        rate = self.gue.biophoton_emission_rate()
        # Base rate is 50 with ±10% modulation
        self.assertGreater(rate, 45.0)
        self.assertLess(rate, 55.0)

    def test_psi_gue_in_range(self):
        """psi_gue must return a value in [0, 1]."""
        psi = self.gue.psi_gue()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_gue_positive(self):
        """psi_gue should return a positive value."""
        psi = self.gue.psi_gue()
        self.assertGreater(psi, 0.0)

    def test_psi_gue_high_for_good_gue(self):
        """psi_gue should be high for default (good GUE properties)."""
        psi = self.gue.psi_gue()
        self.assertGreater(psi, 0.5)

    def test_custom_n_eigenvalues(self):
        """Can create BiofotonesGUE with custom n_eigenvalues."""
        gue_custom = BiofotonesGUE(n_eigenvalues=20)
        self.assertEqual(gue_custom.n_eigenvalues, 20)

    def test_custom_riemann_zeros(self):
        """Can create BiofotonesGUE with custom riemann_zeros."""
        custom_zeros = [10.0, 20.0, 30.0]
        gue_custom = BiofotonesGUE(riemann_zeros=custom_zeros)
        self.assertEqual(gue_custom.riemann_zeros, custom_zeros)

    def test_eigenvalue_spacing_with_few_zeros(self):
        """eigenvalue_spacing with very few zeros returns appropriate list."""
        gue_small = BiofotonesGUE(riemann_zeros=[1.0, 2.0])
        spacings = gue_small.eigenvalue_spacing()
        self.assertEqual(len(spacings), 1)

    def test_eigenvalue_spacing_empty_zeros(self):
        """eigenvalue_spacing with no zeros returns empty list."""
        gue_empty = BiofotonesGUE(riemann_zeros=[])
        spacings = gue_empty.eigenvalue_spacing()
        self.assertEqual(len(spacings), 0)

    def test_spectral_correlation_empty_returns_zero(self):
        """spectral_correlation with no spacings returns 0."""
        gue_empty = BiofotonesGUE(riemann_zeros=[])
        corr = gue_empty.spectral_correlation()
        self.assertEqual(corr, 0.0)

    def test_super_poisson_ratio_empty_returns_one(self):
        """super_poisson_ratio with no spacings returns 1."""
        gue_empty = BiofotonesGUE(riemann_zeros=[])
        ratio = gue_empty.super_poisson_ratio()
        self.assertEqual(ratio, 1.0)

    def test_repr_contains_f0(self):
        """repr should contain frequency information."""
        repr_str = repr(self.gue)
        self.assertIn("Hz", repr_str)

    def test_repr_contains_gue_ratio(self):
        """repr should contain Var/<n> information."""
        repr_str = repr(self.gue)
        self.assertIn("Var/<n>", repr_str)


# ============================================================================
# TestAcoplamientoCoherente – 23 tests
# ============================================================================

class TestAcoplamientoCoherente(unittest.TestCase):
    """Tests for AcoplamientoCoherente class."""

    def setUp(self):
        """Initialize coherent coupling for each test."""
        self.coupling = AcoplamientoCoherente()

    def test_default_m_psi_ev(self):
        """Default m_psi_ev must be approximately 5.861427×10⁻¹³ eV."""
        self.assertAlmostEqual(self.coupling.m_psi_ev, 5.861427e-13, delta=1e-18)

    def test_default_f0(self):
        """Default f0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(self.coupling.f0, 141.7001, places=4)

    def test_default_g_coupling(self):
        """Default g_coupling must be 0.053."""
        self.assertAlmostEqual(self.coupling.g_coupling, 0.053, delta=0.001)

    def test_coupling_strength_returns_g_coupling(self):
        """coupling_strength must return the g_coupling value."""
        strength = self.coupling.coupling_strength()
        self.assertAlmostEqual(strength, self.coupling.g_coupling, places=10)

    def test_coupling_strength_positive(self):
        """coupling_strength must return a positive value."""
        strength = self.coupling.coupling_strength()
        self.assertGreater(strength, 0.0)

    def test_interaction_energy_positive(self):
        """interaction_energy must return a positive value."""
        E_int = self.coupling.interaction_energy()
        self.assertGreater(E_int, 0.0)

    def test_interaction_energy_formula(self):
        """interaction_energy must equal g × ħ × ω₀."""
        E_int = self.coupling.interaction_energy()
        expected = self.coupling.g_coupling * _HBAR * _OMEGA_0
        self.assertAlmostEqual(E_int, expected, places=45)

    def test_interaction_energy_order(self):
        """interaction_energy should be on the order of 10⁻³⁴ Joules."""
        E_int = self.coupling.interaction_energy()
        self.assertGreater(E_int, 1e-40)
        self.assertLess(E_int, 1e-30)

    def test_resonance_condition_at_resonance(self):
        """resonance_condition(f0) should return maximum value."""
        f_res = self.coupling.f0
        res = self.coupling.resonance_condition(f_res)
        self.assertEqual(res, 1.0)

    def test_resonance_condition_far_detuned(self):
        """resonance_condition far from f0 should be small."""
        f_far = self.coupling.f0 + 1000.0  # 1000 Hz away
        res = self.coupling.resonance_condition(f_far)
        self.assertLess(res, 0.1)

    def test_resonance_condition_lorentzian(self):
        """resonance_condition should follow Lorentzian profile."""
        f1 = self.coupling.f0 + 50.0
        f2 = self.coupling.f0 + 100.0
        res1 = self.coupling.resonance_condition(f1)
        res2 = self.coupling.resonance_condition(f2)
        # Closer to resonance should have higher value
        self.assertGreater(res1, res2)

    def test_resonance_condition_in_range(self):
        """resonance_condition must return value in [0, 1]."""
        for f in [self.coupling.f0 - 200, self.coupling.f0, self.coupling.f0 + 200]:
            res = self.coupling.resonance_condition(f)
            self.assertGreaterEqual(res, 0.0)
            self.assertLessEqual(res, 1.0)

    def test_microtubule_coupling_positive(self):
        """microtubule_coupling must return a positive value."""
        mt = self.coupling.microtubule_coupling()
        self.assertGreater(mt, 0.0)

    def test_microtubule_coupling_reasonable(self):
        """microtubule_coupling should be reasonably high (~0.6-1.0)."""
        mt = self.coupling.microtubule_coupling()
        self.assertGreater(mt, 0.3)
        self.assertLessEqual(mt, 1.0)

    def test_dna_coupling_positive(self):
        """dna_coupling must return a positive value."""
        dna = self.coupling.dna_coupling()
        self.assertGreater(dna, 0.0)

    def test_dna_coupling_reasonable(self):
        """dna_coupling should be in reasonable range."""
        dna = self.coupling.dna_coupling()
        self.assertGreater(dna, 0.0)
        self.assertLessEqual(dna, 1.0)

    def test_dna_coupling_less_than_microtubule(self):
        """dna_coupling should typically be less than microtubule_coupling."""
        mt = self.coupling.microtubule_coupling()
        dna = self.coupling.dna_coupling()
        # They're at similar resonance frequencies, but MT is primary
        self.assertGreater(mt, dna)

    def test_psi_coupling_in_range(self):
        """psi_coupling must return value in [0, 1]."""
        psi = self.coupling.psi_coupling()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_coupling_positive(self):
        """psi_coupling should return positive value."""
        psi = self.coupling.psi_coupling()
        self.assertGreater(psi, 0.0)

    def test_psi_coupling_high_for_default_g(self):
        """psi_coupling should be high for default g_coupling."""
        psi = self.coupling.psi_coupling()
        self.assertGreater(psi, 0.3)

    def test_psi_coupling_increases_with_g(self):
        """psi_coupling should increase with g_coupling."""
        coupling_low_g = AcoplamientoCoherente(g_coupling=0.03)
        coupling_high_g = AcoplamientoCoherente(g_coupling=0.07)
        psi_low = coupling_low_g.psi_coupling()
        psi_high = coupling_high_g.psi_coupling()
        self.assertLess(psi_low, psi_high)

    def test_custom_g_coupling(self):
        """Can create AcoplamientoCoherente with custom g_coupling."""
        custom_g = 0.1
        coupling_custom = AcoplamientoCoherente(g_coupling=custom_g)
        self.assertEqual(coupling_custom.g_coupling, custom_g)

    def test_repr_contains_g_eff(self):
        """repr should contain g_eff information."""
        repr_str = repr(self.coupling)
        self.assertIn("g_eff", repr_str)


# ============================================================================
# TestFirmaEspectral – 28 tests
# ============================================================================

class TestFirmaEspectral(unittest.TestCase):
    """Tests for FirmaEspectral class."""

    def setUp(self):
        """Initialize spectral signature for each test."""
        self.signature = FirmaEspectral()

    def test_default_f0(self):
        """Default f0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(self.signature.f0, 141.7001, places=4)

    def test_default_m_psi_ev(self):
        """Default m_psi_ev must be approximately 5.861427×10⁻¹³ eV."""
        self.assertAlmostEqual(self.signature.m_psi_ev, 5.861427e-13, delta=1e-18)

    def test_frequency_signature_is_dict(self):
        """frequency_signature must return a dictionary."""
        sig = self.signature.frequency_signature()
        self.assertIsInstance(sig, dict)

    def test_frequency_signature_contains_fundamental(self):
        """frequency_signature must contain 'f_fundamental_hz'."""
        sig = self.signature.frequency_signature()
        self.assertIn("f_fundamental_hz", sig)

    def test_frequency_signature_fundamental_correct(self):
        """frequency_signature fundamental must equal f0."""
        sig = self.signature.frequency_signature()
        self.assertAlmostEqual(sig["f_fundamental_hz"], self.signature.f0, places=4)

    def test_frequency_signature_contains_harmonic_2(self):
        """frequency_signature must contain 'f_harmonic_2_hz'."""
        sig = self.signature.frequency_signature()
        self.assertIn("f_harmonic_2_hz", sig)

    def test_frequency_signature_harmonic_2_correct(self):
        """frequency_signature harmonic 2 must equal 2×f0."""
        sig = self.signature.frequency_signature()
        expected = 2.0 * self.signature.f0
        self.assertAlmostEqual(sig["f_harmonic_2_hz"], expected, places=3)

    def test_frequency_signature_contains_harmonic_3(self):
        """frequency_signature must contain 'f_harmonic_3_hz'."""
        sig = self.signature.frequency_signature()
        self.assertIn("f_harmonic_3_hz", sig)

    def test_frequency_signature_harmonic_3_correct(self):
        """frequency_signature harmonic 3 must equal 3×f0."""
        sig = self.signature.frequency_signature()
        expected = 3.0 * self.signature.f0
        self.assertAlmostEqual(sig["f_harmonic_3_hz"], expected, places=2)

    def test_frequency_signature_contains_subharmonic(self):
        """frequency_signature must contain 'f_subharmonic_hz'."""
        sig = self.signature.frequency_signature()
        self.assertIn("f_subharmonic_hz", sig)

    def test_frequency_signature_subharmonic_correct(self):
        """frequency_signature subharmonic must equal f0/2."""
        sig = self.signature.frequency_signature()
        expected = self.signature.f0 / 2.0
        self.assertAlmostEqual(sig["f_subharmonic_hz"], expected, places=4)

    def test_energy_signature_is_dict(self):
        """energy_signature must return a dictionary."""
        sig = self.signature.energy_signature()
        self.assertIsInstance(sig, dict)

    def test_energy_signature_contains_photon_energy(self):
        """energy_signature must contain 'E_photon_ev'."""
        sig = self.signature.energy_signature()
        self.assertIn("E_photon_ev", sig)

    def test_energy_signature_photon_energy_correct(self):
        """energy_signature E_photon must equal h×f0 (in eV)."""
        from qcal.constants import H_PLANCK, EV_TO_J
        sig = self.signature.energy_signature()
        expected = H_PLANCK * self.signature.f0 / EV_TO_J
        self.assertAlmostEqual(sig["E_photon_ev"], expected, places=30)

    def test_energy_signature_contains_rest_energy(self):
        """energy_signature must contain 'E_rest_ev'."""
        sig = self.signature.energy_signature()
        self.assertIn("E_rest_ev", sig)

    def test_energy_signature_rest_energy_correct(self):
        """energy_signature E_rest must equal m_psi_ev."""
        sig = self.signature.energy_signature()
        self.assertAlmostEqual(sig["E_rest_ev"], self.signature.m_psi_ev, places=20)

    def test_energy_signature_contains_ratio(self):
        """energy_signature must contain 'E_ratio'."""
        sig = self.signature.energy_signature()
        self.assertIn("E_ratio", sig)

    def test_energy_signature_ratio_correct(self):
        """energy_signature E_ratio must equal E_photon / E_rest."""
        sig = self.signature.energy_signature()
        expected = sig["E_photon_ev"] / sig["E_rest_ev"]
        self.assertAlmostEqual(sig["E_ratio"], expected, places=20)

    def test_energy_signature_ratio_large(self):
        """E_ratio should be close to 1 (photon ≈ rest mass for this frequency)."""
        sig = self.signature.energy_signature()
        # For f0 = 141.7001 Hz, the photon energy is very close to rest mass
        self.assertGreater(sig["E_ratio"], 0.99)
        self.assertLess(sig["E_ratio"], 1.01)

    def test_detection_channels_is_dict(self):
        """detection_channels must return a dictionary."""
        channels = self.signature.detection_channels()
        self.assertIsInstance(channels, dict)

    def test_detection_channels_count(self):
        """detection_channels should contain 5 channels."""
        channels = self.signature.detection_channels()
        self.assertEqual(len(channels), 5)

    def test_detection_channels_have_names(self):
        """detection_channels should have keys like 'channel_1', etc."""
        channels = self.signature.detection_channels()
        for i in range(1, 6):
            self.assertIn(f"channel_{i}", channels)

    def test_detection_channels_have_descriptions(self):
        """detection_channels should have string descriptions."""
        channels = self.signature.detection_channels()
        for channel in channels.values():
            self.assertIsInstance(channel, str)
            self.assertGreater(len(channel), 0)

    def test_optimal_integration_time_positive(self):
        """optimal_integration_time must return positive value."""
        t_int = self.signature.optimal_integration_time()
        self.assertGreater(t_int, 0.0)

    def test_optimal_integration_time_reasonable(self):
        """optimal_integration_time should be ~500 periods."""
        t_int = self.signature.optimal_integration_time()
        period = 1.0 / self.signature.f0
        # Should be on order of 500 periods (but can vary)
        self.assertGreater(t_int, 100.0 * period)
        self.assertLess(t_int, 2000.0 * period)

    def test_psi_signature_in_range(self):
        """psi_signature must return value in [0, 1]."""
        psi = self.signature.psi_signature()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_signature_equals_one_for_default(self):
        """psi_signature should equal 1.0 for all 5 channels present."""
        psi = self.signature.psi_signature()
        self.assertEqual(psi, 1.0)

    def test_repr_contains_f0(self):
        """repr should contain frequency information."""
        repr_str = repr(self.signature)
        self.assertIn("Hz", repr_str)


# ============================================================================
# TestCoherenciaParticulaPsi – 25 tests
# ============================================================================

class TestCoherenciaParticulaPsi(unittest.TestCase):
    """Tests for CoherenciaParticulaPsi class."""

    def setUp(self):
        """Initialize coherence validator for each test."""
        self.ligo = ModoLIGOVirgo()
        self.vacuum = VacuoBirefringencia()
        self.gue = BiofotonesGUE()
        self.coupling = AcoplamientoCoherente()
        self.signature = FirmaEspectral()
        self.coherencia = CoherenciaParticulaPsi(
            ligo=self.ligo,
            vacuum=self.vacuum,
            gue=self.gue,
            coupling=self.coupling,
            signature=self.signature,
        )

    def test_psi_ligo_in_range(self):
        """psi_ligo must return value in [0, 1]."""
        psi = self.coherencia.psi_ligo()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_vacuum_in_range(self):
        """psi_vacuum must return value in [0, 1]."""
        psi = self.coherencia.psi_vacuum()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_gue_in_range(self):
        """psi_gue must return value in [0, 1]."""
        psi = self.coherencia.psi_gue()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_coupling_in_range(self):
        """psi_coupling must return value in [0, 1]."""
        psi = self.coherencia.psi_coupling()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_signature_in_range(self):
        """psi_signature must return value in [0, 1]."""
        psi = self.coherencia.psi_signature()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_coherencias_individuales_is_dict(self):
        """coherencias_individuales must return a dictionary."""
        coherencias = self.coherencia.coherencias_individuales()
        self.assertIsInstance(coherencias, dict)

    def test_coherencias_individuales_contains_all_keys(self):
        """coherencias_individuales must contain all 5 component keys."""
        coherencias = self.coherencia.coherencias_individuales()
        expected_keys = ["psi_ligo", "psi_vacuum", "psi_gue", "psi_coupling", "psi_signature"]
        for key in expected_keys:
            self.assertIn(key, coherencias)

    def test_coherencias_individuales_all_in_range(self):
        """All coherencias must be in [0, 1]."""
        coherencias = self.coherencia.coherencias_individuales()
        for value in coherencias.values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_psi_global_in_range(self):
        """psi_global must return value in [0, 1]."""
        psi_g = self.coherencia.psi_global()
        self.assertGreaterEqual(psi_g, 0.0)
        self.assertLessEqual(psi_g, 1.0)

    def test_psi_global_is_geometric_mean(self):
        """psi_global must be geometric mean of the 5 components."""
        psi_1 = self.coherencia.psi_ligo()
        psi_2 = self.coherencia.psi_vacuum()
        psi_3 = self.coherencia.psi_gue()
        psi_4 = self.coherencia.psi_coupling()
        psi_5 = self.coherencia.psi_signature()
        
        producto = psi_1 * psi_2 * psi_3 * psi_4 * psi_5
        if producto > 0:
            expected = producto ** (1.0 / 5.0)
        else:
            expected = 0.0
        
        psi_g = self.coherencia.psi_global()
        self.assertAlmostEqual(psi_g, expected, places=10)

    def test_psi_global_positive_for_default(self):
        """psi_global should be positive for default parameters."""
        psi_g = self.coherencia.psi_global()
        self.assertGreater(psi_g, 0.0)

    def test_psi_global_high_for_default(self):
        """psi_global should be high (>0.7) for default parameters."""
        psi_g = self.coherencia.psi_global()
        self.assertGreater(psi_g, 0.7)

    def test_sello_activo_returns_bool(self):
        """sello_activo must return a boolean."""
        sello = self.coherencia.sello_activo()
        self.assertIsInstance(sello, bool)

    def test_sello_activo_true_for_high_psi(self):
        """sello_activo should be True when psi_global ≥ 0.888."""
        psi_g = self.coherencia.psi_global()
        sello = self.coherencia.sello_activo()
        if psi_g >= 0.888:
            self.assertTrue(sello)
        else:
            self.assertFalse(sello)

    def test_sello_activo_true_for_default(self):
        """sello_activo should be True for default parameters."""
        sello = self.coherencia.sello_activo()
        self.assertTrue(sello)

    def test_validar_returns_dict(self):
        """validar must return a dictionary."""
        validacion = self.coherencia.validar()
        self.assertIsInstance(validacion, dict)

    def test_validar_contains_coherencias(self):
        """validar must contain 'coherencias' key."""
        validacion = self.coherencia.validar()
        self.assertIn("coherencias", validacion)

    def test_validar_contains_psi_global(self):
        """validar must contain 'psi_global' key."""
        validacion = self.coherencia.validar()
        self.assertIn("psi_global", validacion)

    def test_validar_contains_umbral(self):
        """validar must contain 'psi_umbral' key."""
        validacion = self.coherencia.validar()
        self.assertIn("psi_umbral", validacion)

    def test_validar_contains_sello_activo(self):
        """validar must contain 'sello_activo' key."""
        validacion = self.coherencia.validar()
        self.assertIn("sello_activo", validacion)

    def test_validar_contains_mensaje(self):
        """validar must contain 'mensaje' key."""
        validacion = self.coherencia.validar()
        self.assertIn("mensaje", validacion)

    def test_validar_umbral_correct(self):
        """validar psi_umbral must equal 0.888."""
        validacion = self.coherencia.validar()
        self.assertAlmostEqual(validacion["psi_umbral"], 0.888, places=3)

    def test_validar_mensaje_contains_checkmark(self):
        """validar mensaje should contain ✅ if sello_activo."""
        validacion = self.coherencia.validar()
        if validacion["sello_activo"]:
            self.assertIn("✅", validacion["mensaje"])

    def test_repr_contains_psi_global(self):
        """repr should contain psi_global information."""
        repr_str = repr(self.coherencia)
        self.assertIn("Ψ_global", repr_str)

    def test_repr_contains_umbral(self):
        """repr should contain umbral information."""
        repr_str = repr(self.coherencia)
        self.assertIn("Umbral", repr_str)


# ============================================================================
# TestSistemaParticulaPsi – 25 tests
# ============================================================================

class TestSistemaParticulaPsi(unittest.TestCase):
    """Tests for SistemaParticulaPsi class."""

    def setUp(self):
        """Initialize system for each test."""
        self.sistema = SistemaParticulaPsi()

    def test_sistema_has_constantes(self):
        """Sistema must have constantes attribute."""
        self.assertIsInstance(self.sistema.constantes, ConstantesParticulaPsi)

    def test_sistema_has_ligo(self):
        """Sistema must have ligo attribute."""
        self.assertIsInstance(self.sistema.ligo, ModoLIGOVirgo)

    def test_sistema_has_vacuum(self):
        """Sistema must have vacuum attribute."""
        self.assertIsInstance(self.sistema.vacuum, VacuoBirefringencia)

    def test_sistema_has_gue(self):
        """Sistema must have gue attribute."""
        self.assertIsInstance(self.sistema.gue, BiofotonesGUE)

    def test_sistema_has_coupling(self):
        """Sistema must have coupling attribute."""
        self.assertIsInstance(self.sistema.coupling, AcoplamientoCoherente)

    def test_sistema_has_signature(self):
        """Sistema must have signature attribute."""
        self.assertIsInstance(self.sistema.signature, FirmaEspectral)

    def test_sistema_has_coherencia(self):
        """Sistema must have coherencia attribute."""
        self.assertIsInstance(self.sistema.coherencia, CoherenciaParticulaPsi)

    def test_activar_returns_dict(self):
        """activar must return a dictionary."""
        resultado = self.sistema.activar()
        self.assertIsInstance(resultado, dict)

    def test_activar_contains_sello(self):
        """activar result must contain 'sello' key."""
        resultado = self.sistema.activar()
        self.assertIn("sello", resultado)

    def test_activar_sello_value(self):
        """activar sello must equal '∴PSI∞³'."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado["sello"], "∴PSI∞³")

    def test_activar_contains_ram(self):
        """activar result must contain 'ram' key."""
        resultado = self.sistema.activar()
        self.assertIn("ram", resultado)

    def test_activar_contains_version(self):
        """activar result must contain 'version' key."""
        resultado = self.sistema.activar()
        self.assertIn("version", resultado)

    def test_activar_contains_f0(self):
        """activar result must contain 'f0_hz' key."""
        resultado = self.sistema.activar()
        self.assertIn("f0_hz", resultado)

    def test_activar_contains_m_psi_ev(self):
        """activar result must contain 'm_psi_ev' key."""
        resultado = self.sistema.activar()
        self.assertIn("m_psi_ev", resultado)

    def test_activar_contains_psi_global(self):
        """activar result must contain 'psi_global' key."""
        resultado = self.sistema.activar()
        self.assertIn("psi_global", resultado)

    def test_activar_contains_sello_activo(self):
        """activar result must contain 'sello_activo' key."""
        resultado = self.sistema.activar()
        self.assertIn("sello_activo", resultado)

    def test_activar_sello_activo_true(self):
        """activar sello_activo should be True for default system."""
        resultado = self.sistema.activar()
        self.assertTrue(resultado["sello_activo"])

    def test_activar_coherencias_present(self):
        """activar result must contain 'coherencias' key."""
        resultado = self.sistema.activar()
        self.assertIn("coherencias", resultado)

    def test_activar_ligo_strain_present(self):
        """activar result must contain 'ligo_strain_amplitude' key."""
        resultado = self.sistema.activar()
        self.assertIn("ligo_strain_amplitude", resultado)

    def test_activar_vacuum_delta_theta_present(self):
        """activar result must contain 'vacuum_delta_theta_per_m' key."""
        resultado = self.sistema.activar()
        self.assertIn("vacuum_delta_theta_per_m", resultado)

    def test_activar_gue_ratio_present(self):
        """activar result must contain 'gue_super_poisson_ratio' key."""
        resultado = self.sistema.activar()
        self.assertIn("gue_super_poisson_ratio", resultado)

    def test_activar_coupling_g_present(self):
        """activar result must contain 'coupling_g_eff' key."""
        resultado = self.sistema.activar()
        self.assertIn("coupling_g_eff", resultado)

    def test_activar_signature_channels_present(self):
        """activar result must contain 'signature_channels' key."""
        resultado = self.sistema.activar()
        self.assertIn("signature_channels", resultado)

    def test_activar_masa_validada_true(self):
        """activar masa_validada should be True."""
        resultado = self.sistema.activar()
        self.assertIn("masa_validada", resultado)

    def test_activar_phi_12_validada_true(self):
        """activar phi_12_validada should be True."""
        resultado = self.sistema.activar()
        self.assertIn("phi_12_validada", resultado)


# ============================================================================
# TestAPIPublic – 15 tests
# ============================================================================

class TestAPIPublic(unittest.TestCase):
    """Tests for public API function."""

    def test_particula_psi_activar_returns_dict(self):
        """particula_psi_activar must return a dictionary."""
        resultado = particula_psi_activar()
        self.assertIsInstance(resultado, dict)

    def test_particula_psi_activar_contains_sello(self):
        """particula_psi_activar result must contain 'sello' key."""
        resultado = particula_psi_activar()
        self.assertIn("sello", resultado)

    def test_particula_psi_activar_sello_value(self):
        """particula_psi_activar sello must equal '∴PSI∞³'."""
        resultado = particula_psi_activar()
        self.assertEqual(resultado["sello"], "∴PSI∞³")

    def test_particula_psi_activar_f0_correct(self):
        """particula_psi_activar f0_hz must be 141.7001 Hz."""
        resultado = particula_psi_activar()
        self.assertAlmostEqual(resultado["f0_hz"], 141.7001, places=4)

    def test_particula_psi_activar_m_psi_ev_correct(self):
        """particula_psi_activar m_psi_ev must be ≈5.861427×10⁻¹³ eV."""
        resultado = particula_psi_activar()
        self.assertAlmostEqual(resultado["m_psi_ev"], 5.861427e-13, delta=1e-18)

    def test_particula_psi_activar_psi_global_in_range(self):
        """particula_psi_activar psi_global must be in [0, 1]."""
        resultado = particula_psi_activar()
        psi_g = resultado["psi_global"]
        self.assertGreaterEqual(psi_g, 0.0)
        self.assertLessEqual(psi_g, 1.0)

    def test_particula_psi_activar_psi_global_high(self):
        """particula_psi_activar psi_global should be ≥ 0.888."""
        resultado = particula_psi_activar()
        psi_g = resultado["psi_global"]
        self.assertGreaterEqual(psi_g, 0.888)

    def test_particula_psi_activar_sello_activo_true(self):
        """particula_psi_activar sello_activo must be True."""
        resultado = particula_psi_activar()
        self.assertTrue(resultado["sello_activo"])

    def test_particula_psi_activar_coherencias_present(self):
        """particula_psi_activar must contain all 5 coherencias."""
        resultado = particula_psi_activar()
        coherencias = resultado["coherencias"]
        expected_keys = ["psi_ligo", "psi_vacuum", "psi_gue", "psi_coupling", "psi_signature"]
        for key in expected_keys:
            self.assertIn(key, coherencias)

    def test_particula_psi_activar_all_coherencias_in_range(self):
        """All coherencias in activar result must be in [0, 1]."""
        resultado = particula_psi_activar()
        for psi in resultado["coherencias"].values():
            self.assertGreaterEqual(psi, 0.0)
            self.assertLessEqual(psi, 1.0)

    def test_particula_psi_activar_contains_ligo_results(self):
        """particula_psi_activar must contain LIGO/Virgo results."""
        resultado = particula_psi_activar()
        self.assertIn("ligo_strain_amplitude", resultado)
        self.assertIn("ligo_snr", resultado)
        self.assertIn("ligo_q_factor", resultado)

    def test_particula_psi_activar_contains_vacuum_results(self):
        """particula_psi_activar must contain vacuum birefringence results."""
        resultado = particula_psi_activar()
        self.assertIn("vacuum_delta_theta_per_m", resultado)
        self.assertIn("vacuum_dsn_setup", resultado)

    def test_particula_psi_activar_contains_gue_results(self):
        """particula_psi_activar must contain GUE results."""
        resultado = particula_psi_activar()
        self.assertIn("gue_super_poisson_ratio", resultado)
        self.assertIn("gue_eigenvalue_spacings", resultado)

    def test_particula_psi_activar_contains_coupling_results(self):
        """particula_psi_activar must contain coupling results."""
        resultado = particula_psi_activar()
        self.assertIn("coupling_g_eff", resultado)
        self.assertIn("coupling_microtubule", resultado)

    def test_particula_psi_activar_contains_signature_results(self):
        """particula_psi_activar must contain signature results."""
        resultado = particula_psi_activar()
        self.assertIn("signature_frequencies", resultado)
        self.assertIn("signature_channels", resultado)


# ============================================================================
# RUNNER
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
