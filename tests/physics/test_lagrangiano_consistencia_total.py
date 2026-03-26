"""
Tests for physics.lagrangiano_consistencia_total
=================================================

Pruebas que verifican las 5 clases y las 3 funciones de la API pública
del Lagrangiano de Consistencia Total.

Invariantes clave verificados:
  - m_ψ = h·f₀/c²  ≈ 5.86 × 10⁻¹³ eV
  - λ ≈ m_ψ/M_P    ≈ 4.8 × 10⁻⁴¹
  - Δθ₀ ∝ L, Δθ₀ ∝ g_{aγγ}, Δθ₀ ∝ √ρ_DM
  - δφ_min ∝ 1/√(P·T)
  - SNR = Δθ₀/δφ_min >> 5 para parámetros de referencia
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.lagrangiano_consistencia_total import (
    # Constants
    M_PSI_EV,
    M_PSI_EV_EXPECTED,
    M_PSI_J,
    M_PLANCK_EV,
    LAMBDA_SELF,
    G_AXION_PHOTON_GEV_INV,
    G_AXION_PHOTON_EV_INV,
    RHO_DM_GEV_CM3,
    RHO_DM_J_M3,
    L_IRS_LUNA_KM,
    L_IRS_LUNA_M,
    LAMBDA_LASER_NM,
    DELTA_THETA_0_RAD,
    SNR_5SIGMA,
    P_LASER_W,
    T_INTEGRACION_S,
    F_SIGNAL_HZ,
    G_NEWTON,
    # Classes
    LagrangianoConsistencia,
    CampoTejido,
    BirrefringenciaOscilatoria,
    LimiteRuidoCuantico,
    AnalisisSensibilidad,
    ResultadoDetectabilidad,
    # Public API
    calcular_amplitud_birrefringencia,
    calcular_limite_ruido_cuantico,
    analizar_detectabilidad,
)
from qcal.constants import F0_HZ, H_PLANCK, HBAR, C, EV_TO_J


# ============================================================================
# Tests de constantes
# ============================================================================

class TestConstantes(unittest.TestCase):
    """Verifica los valores de las constantes físicas del módulo."""

    def test_m_psi_ev_approx(self):
        """m_ψ debe estar cerca del valor esperado del problema (5.86×10⁻¹³ eV)."""
        self.assertAlmostEqual(M_PSI_EV / M_PSI_EV_EXPECTED, 1.0, delta=0.01)

    def test_m_psi_ev_from_planck_frequency(self):
        """m_ψ = h·f₀ / e_charge debe dar el valor correcto en eV."""
        expected = H_PLANCK * F0_HZ / EV_TO_J
        self.assertAlmostEqual(M_PSI_EV, expected, places=25)

    def test_m_psi_j_positive(self):
        """m_ψ en julios debe ser positivo."""
        self.assertGreater(M_PSI_J, 0.0)

    def test_m_planck_ev_scale(self):
        """Masa de Planck debe estar en la escala de 10²⁸ eV."""
        self.assertGreater(M_PLANCK_EV, 1.0e27)
        self.assertLess(M_PLANCK_EV, 1.0e29)

    def test_lambda_self_positive(self):
        """La auto-interacción λ debe ser positiva."""
        self.assertGreater(LAMBDA_SELF, 0.0)

    def test_lambda_self_less_than_unity(self):
        """La auto-interacción λ << 1 (régimen perturbativo)."""
        self.assertLess(LAMBDA_SELF, 1.0)

    def test_lambda_self_approx_expected(self):
        """λ ≈ 4.8×10⁻⁴¹ (escala de Planck)."""
        self.assertAlmostEqual(LAMBDA_SELF / 4.8e-41, 1.0, delta=0.01)

    def test_g_axion_photon_reference_value(self):
        """g_{aγγ} de referencia es 10⁻¹² GeV⁻¹."""
        self.assertAlmostEqual(G_AXION_PHOTON_GEV_INV, 1.0e-12, places=20)

    def test_g_axion_photon_ev_inv_conversion(self):
        """g_{aγγ} en eV⁻¹ debe ser 10⁻⁹ veces el valor en GeV⁻¹."""
        expected = G_AXION_PHOTON_GEV_INV * 1.0e-9
        self.assertAlmostEqual(G_AXION_PHOTON_EV_INV, expected, places=30)

    def test_rho_dm_gev_cm3_reference(self):
        """Densidad de materia oscura de referencia = 0.3 GeV/cm³."""
        self.assertAlmostEqual(RHO_DM_GEV_CM3, 0.3, places=10)

    def test_rho_dm_j_m3_conversion(self):
        """Conversión de densidad de MO a J/m³ debe ser positiva y consistente."""
        rho_expected = (0.3 * 1.0e9 * EV_TO_J) / 1.0e-6
        self.assertAlmostEqual(RHO_DM_J_M3, rho_expected, places=10)

    def test_l_irs_luna_km_reference(self):
        """Longitud del brazo IRS-Luna de referencia = 100 km."""
        self.assertAlmostEqual(L_IRS_LUNA_KM, 100.0, places=5)

    def test_l_irs_luna_m_consistency(self):
        """L_IRS_LUNA_M debe ser 1000 × L_IRS_LUNA_KM."""
        self.assertAlmostEqual(L_IRS_LUNA_M, L_IRS_LUNA_KM * 1.0e3, places=5)

    def test_snr_5sigma_value(self):
        """El umbral de detección debe ser 5σ."""
        self.assertAlmostEqual(SNR_5SIGMA, 5.0, places=5)

    def test_delta_theta_0_order_of_magnitude(self):
        """El DELTA_THETA_0_RAD de referencia del problema es 2.4×10⁻¹⁹ rad."""
        self.assertAlmostEqual(DELTA_THETA_0_RAD, 2.4e-19, places=25)

    def test_f_signal_hz_equals_f0(self):
        """La frecuencia de señal debe coincidir con f₀ = 141.7001 Hz."""
        self.assertAlmostEqual(F_SIGNAL_HZ, F0_HZ, places=6)

    def test_g_newton_positive(self):
        """La constante gravitacional de Newton debe ser positiva."""
        self.assertGreater(G_NEWTON, 0.0)


# ============================================================================
# Tests de LagrangianoConsistencia
# ============================================================================

class TestLagrangianoConsistencia(unittest.TestCase):
    """Verifica la clase LagrangianoConsistencia."""

    def setUp(self):
        self.lag = LagrangianoConsistencia()

    def test_consistente_default(self):
        """El Lagrangiano con parámetros por defecto debe ser consistente."""
        self.assertTrue(self.lag.consistente)

    def test_m_psi_ev_matches_constant(self):
        """m_ψ del Lagrangiano debe coincidir con la constante del módulo."""
        self.assertAlmostEqual(self.lag.m_psi_ev, M_PSI_EV, places=20)

    def test_lambda_self_matches_constant(self):
        """λ del Lagrangiano debe coincidir con la constante del módulo."""
        self.assertAlmostEqual(self.lag.lambda_self, LAMBDA_SELF, places=50)

    def test_g_axion_photon_matches_constant(self):
        """g_{aγγ} del Lagrangiano debe coincidir con la constante del módulo."""
        self.assertAlmostEqual(
            self.lag.g_axion_photon_GeV_inv, G_AXION_PHOTON_GEV_INV, places=20
        )

    def test_omega_psi_is_2pi_f0(self):
        """ω_ψ debe ser 2π·f₀."""
        expected = 2.0 * math.pi * F0_HZ
        self.assertAlmostEqual(self.lag.omega_psi_rad_s, expected, places=8)

    def test_m_psi_kg_is_h_f0_over_c2(self):
        """m_ψ en kg debe ser h·f₀/c²."""
        expected = H_PLANCK * F0_HZ / (C ** 2)
        self.assertAlmostEqual(self.lag.m_psi_kg, expected, places=60)

    def test_g_axion_photon_ev_inv_conversion(self):
        """g_{aγγ} en eV⁻¹ debe ser GeV⁻¹ × 10⁻⁹."""
        expected = G_AXION_PHOTON_GEV_INV * 1.0e-9
        self.assertAlmostEqual(self.lag.g_axion_photon_ev_inv, expected, places=30)

    def test_custom_f0_changes_omega(self):
        """Cambiar f₀ debe cambiar ω_ψ proporcionalmente."""
        lag2 = LagrangianoConsistencia(f0_hz=2.0 * F0_HZ)
        self.assertAlmostEqual(lag2.omega_psi_rad_s, 2.0 * self.lag.omega_psi_rad_s, places=6)

    def test_inconsistent_m_psi_detected(self):
        """Un m_ψ incompatible con f₀ debe marcar consistente=False."""
        lag_bad = LagrangianoConsistencia(m_psi_ev=1.0)  # muy diferente de h*f0
        self.assertFalse(lag_bad.consistente)

    def test_negative_g_is_inconsistent(self):
        """Un g_{aγγ} negativo debe marcar consistente=False."""
        lag_neg = LagrangianoConsistencia(g_axion_photon_GeV_inv=-1e-12)
        self.assertFalse(lag_neg.consistente)

    def test_repr_contains_key_info(self):
        """__repr__ debe contener información clave."""
        r = repr(self.lag)
        self.assertIn("consistente=True", r)
        self.assertIn("eV", r)


# ============================================================================
# Tests de CampoTejido
# ============================================================================

class TestCampoTejido(unittest.TestCase):
    """Verifica la clase CampoTejido."""

    def setUp(self):
        self.campo = CampoTejido()

    def test_omega_psi_matches_lagrangiano(self):
        """ω_ψ del campo debe coincidir con el Lagrangiano subyacente."""
        expected = 2.0 * math.pi * F0_HZ
        self.assertAlmostEqual(self.campo.omega_psi, expected, places=8)

    def test_psi0_si_positive(self):
        """La amplitud ψ₀ debe ser positiva."""
        self.assertGreater(self.campo.psi0_SI, 0.0)

    def test_psi0_si_from_density_formula(self):
        """ψ₀ = √(2·ρ_DM) / ω_ψ debe ser consistente con rho_DM."""
        expected = math.sqrt(2.0 * RHO_DM_J_M3) / (2.0 * math.pi * F0_HZ)
        self.assertAlmostEqual(self.campo.psi0_SI, expected, places=15)

    def test_psi_at_t0_equals_psi0(self):
        """ψ(0) debe ser igual a ψ₀ (coseno empieza en 1)."""
        self.assertAlmostEqual(self.campo.psi(0.0), self.campo.psi0_SI, places=15)

    def test_psi_at_quarter_period_zero(self):
        """ψ(T/4) debe ser ~0 (coseno en π/2)."""
        T = 2.0 * math.pi / self.campo.omega_psi
        self.assertAlmostEqual(self.campo.psi(T / 4.0), 0.0, places=10)

    def test_psi_at_half_period_minus_psi0(self):
        """ψ(T/2) debe ser −ψ₀ (coseno en π)."""
        T = 2.0 * math.pi / self.campo.omega_psi
        self.assertAlmostEqual(
            self.campo.psi(T / 2.0), -self.campo.psi0_SI, places=10
        )

    def test_psi_dot_at_t0_zero(self):
        """ψ̇(0) debe ser 0 (seno empieza en 0)."""
        self.assertAlmostEqual(self.campo.psi_dot(0.0), 0.0, places=10)

    def test_psi_dot_at_quarter_period_min(self):
        """ψ̇(T/4) debe ser −ω_ψ·ψ₀ (amplitud máxima negativa)."""
        T = 2.0 * math.pi / self.campo.omega_psi
        expected = -self.campo.omega_psi * self.campo.psi0_SI
        self.assertAlmostEqual(self.campo.psi_dot(T / 4.0), expected, places=10)

    def test_psi_dot_amplitude_equals_omega_psi0(self):
        """La amplitud de ψ̇ debe ser ω_ψ·ψ₀."""
        expected = self.campo.omega_psi * self.campo.psi0_SI
        self.assertAlmostEqual(self.campo.psi_dot_amplitude, expected, places=15)

    def test_psi_squared_plus_psi_dot_squared_constant(self):
        """ψ(t)² + (ψ̇(t)/ω_ψ)² = ψ₀² para todo t (energía conservada)."""
        psi0 = self.campo.psi0_SI
        omega = self.campo.omega_psi
        for t_frac in [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]:
            t = t_frac * 2.0 * math.pi / omega
            psi_sq = self.campo.psi(t) ** 2
            pdot_sq = (self.campo.psi_dot(t) / omega) ** 2
            self.assertAlmostEqual(psi_sq + pdot_sq, psi0 ** 2, places=12)

    def test_higher_density_gives_larger_psi0(self):
        """Mayor densidad de MO → mayor ψ₀."""
        campo2 = CampoTejido(rho_DM_J_m3=4.0 * RHO_DM_J_M3)
        self.assertGreater(campo2.psi0_SI, self.campo.psi0_SI)

    def test_psi0_scales_as_sqrt_density(self):
        """ψ₀ ∝ √ρ_DM."""
        campo2 = CampoTejido(rho_DM_J_m3=4.0 * RHO_DM_J_M3)
        ratio = campo2.psi0_SI / self.campo.psi0_SI
        self.assertAlmostEqual(ratio, 2.0, places=10)

    def test_negative_density_raises(self):
        """Densidad negativa debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            CampoTejido(rho_DM_J_m3=-1.0)

    def test_zero_density_raises(self):
        """Densidad cero debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            CampoTejido(rho_DM_J_m3=0.0)

    def test_repr_contains_key_info(self):
        """__repr__ debe contener ρ_DM y ψ₀."""
        r = repr(self.campo)
        self.assertIn("J/m³", r)
        self.assertIn("ω_ψ", r)


# ============================================================================
# Tests de BirrefringenciaOscilatoria
# ============================================================================

class TestBirrefringenciaOscilatoria(unittest.TestCase):
    """Verifica la clase BirrefringenciaOscilatoria."""

    def setUp(self):
        self.birr = BirrefringenciaOscilatoria()

    def test_delta_theta_0_positive(self):
        """La amplitud Δθ₀ debe ser positiva."""
        self.assertGreater(self.birr.delta_theta_0, 0.0)

    def test_delta_theta_0_small(self):
        """Δθ₀ debe ser mucho menor que 1 rad para los parámetros de referencia."""
        self.assertLess(self.birr.delta_theta_0, 1.0)

    def test_delta_theta_scales_with_L(self):
        """Δθ₀ ∝ L: doblar L debe doblar la amplitud."""
        birr2 = BirrefringenciaOscilatoria(L_m=2.0 * L_IRS_LUNA_M)
        ratio = birr2.delta_theta_0 / self.birr.delta_theta_0
        self.assertAlmostEqual(ratio, 2.0, places=10)

    def test_delta_theta_scales_with_g(self):
        """Δθ₀ ∝ g_{aγγ}: doblar g debe doblar la amplitud."""
        birr2 = BirrefringenciaOscilatoria(
            g_axion_photon_GeV_inv=2.0 * G_AXION_PHOTON_GEV_INV
        )
        ratio = birr2.delta_theta_0 / self.birr.delta_theta_0
        self.assertAlmostEqual(ratio, 2.0, places=10)

    def test_delta_theta_scales_with_sqrt_density(self):
        """Δθ₀ ∝ √ρ_DM: cuadruplicar ρ debe doblar la amplitud."""
        campo2 = CampoTejido(rho_DM_J_m3=4.0 * RHO_DM_J_M3)
        birr2 = BirrefringenciaOscilatoria(campo=campo2)
        ratio = birr2.delta_theta_0 / self.birr.delta_theta_0
        self.assertAlmostEqual(ratio, 2.0, places=10)

    def test_delta_theta_t_at_quarter_period(self):
        """Δθ(T/4) debe ser Δθ₀ (máximo del seno)."""
        omega = self.birr.campo.omega_psi
        T_quarter = math.pi / (2.0 * omega)
        self.assertAlmostEqual(
            self.birr.delta_theta(T_quarter), self.birr.delta_theta_0, places=10
        )

    def test_delta_theta_t_at_t0_zero(self):
        """Δθ(0) = 0 (seno empieza en cero)."""
        self.assertAlmostEqual(self.birr.delta_theta(0.0), 0.0, places=15)

    def test_delta_theta_t_at_half_period_zero(self):
        """Δθ(T/2) ≈ 0 (seno en π)."""
        omega = self.birr.campo.omega_psi
        T_half = math.pi / omega
        self.assertAlmostEqual(self.birr.delta_theta(T_half), 0.0, places=10)

    def test_delta_theta_max_rad_alias(self):
        """delta_theta_max_rad() debe ser igual a delta_theta_0."""
        self.assertAlmostEqual(
            self.birr.delta_theta_max_rad(), self.birr.delta_theta_0, places=15
        )

    def test_delta_n_at_quarter_period(self):
        """δn(T/4) debe tener signo consistente con la birrefringencia."""
        omega = self.birr.campo.omega_psi
        T_quarter = math.pi / (2.0 * omega)
        omega_laser = 2.0 * math.pi * C / (LAMBDA_LASER_NM * 1.0e-9)
        # En T/4 el seno de ψ̇ es negativo → δn es negativo
        self.assertLess(self.birr.delta_n(T_quarter, omega_laser), 0.0)

    def test_delta_n_at_t0_zero(self):
        """δn(0) = 0 ya que ψ̇(0) = 0."""
        omega_laser = 2.0 * math.pi * C / (LAMBDA_LASER_NM * 1.0e-9)
        self.assertAlmostEqual(self.birr.delta_n(0.0, omega_laser), 0.0, places=15)

    def test_delta_n_zero_laser_freq_raises(self):
        """Frecuencia del láser cero debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.birr.delta_n(0.0, omega_laser_rad_s=0.0)

    def test_negative_L_raises(self):
        """Longitud del brazo negativa debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            BirrefringenciaOscilatoria(L_m=-1.0)

    def test_zero_L_raises(self):
        """Longitud del brazo cero debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            BirrefringenciaOscilatoria(L_m=0.0)

    def test_negative_g_raises(self):
        """Acoplamiento negativo debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            BirrefringenciaOscilatoria(g_axion_photon_GeV_inv=-1.0e-12)

    def test_g_si_conversion(self):
        """g_SI debe ser g_GeV_inv / (1e9 × EV_TO_J)."""
        expected = G_AXION_PHOTON_GEV_INV / (1.0e9 * EV_TO_J)
        self.assertAlmostEqual(self.birr.g_SI, expected, places=20)

    def test_repr_contains_delta_theta(self):
        """__repr__ debe contener Δθ₀ y L."""
        r = repr(self.birr)
        self.assertIn("Δθ₀", r)
        self.assertIn("km", r)


# ============================================================================
# Tests de LimiteRuidoCuantico
# ============================================================================

class TestLimiteRuidoCuantico(unittest.TestCase):
    """Verifica la clase LimiteRuidoCuantico."""

    def setUp(self):
        self.ruido = LimiteRuidoCuantico()

    def test_delta_phi_min_positive(self):
        """δφ_min debe ser positivo."""
        self.assertGreater(self.ruido.delta_phi_min, 0.0)

    def test_delta_phi_min_small(self):
        """δφ_min debe ser mucho menor que 1 rad."""
        self.assertLess(self.ruido.delta_phi_min, 1.0)

    def test_omega_laser_formula(self):
        """ω_laser = 2πc/λ_laser debe ser correcto."""
        lambda_m = LAMBDA_LASER_NM * 1.0e-9
        expected = 2.0 * math.pi * C / lambda_m
        self.assertAlmostEqual(self.ruido.omega_laser_rad_s, expected, places=5)

    def test_n_photons_formula(self):
        """N_fotones = P·T / (ℏ·ω_laser) debe ser correcto."""
        expected = (
            P_LASER_W * T_INTEGRACION_S / (HBAR * self.ruido.omega_laser_rad_s)
        )
        self.assertAlmostEqual(self.ruido.n_photons, expected, places=5)

    def test_n_photons_large(self):
        """El número de fotones debe ser muy grande para P=100W, T=10⁶s."""
        self.assertGreater(self.ruido.n_photons, 1.0e20)

    def test_delta_phi_equals_one_over_sqrt_n(self):
        """δφ_min = 1/√N_fotones debe ser verificado."""
        expected = 1.0 / math.sqrt(self.ruido.n_photons)
        self.assertAlmostEqual(self.ruido.delta_phi_min, expected, places=15)

    def test_delta_phi_scales_inversely_with_sqrt_P(self):
        """δφ_min ∝ 1/√P: cuadruplicar P debe halvar δφ_min."""
        ruido2 = LimiteRuidoCuantico(P_watts=4.0 * P_LASER_W)
        ratio = ruido2.delta_phi_min / self.ruido.delta_phi_min
        self.assertAlmostEqual(ratio, 0.5, places=10)

    def test_delta_phi_scales_inversely_with_sqrt_T(self):
        """δφ_min ∝ 1/√T: cuadruplicar T debe halvar δφ_min."""
        ruido2 = LimiteRuidoCuantico(T_seconds=4.0 * T_INTEGRACION_S)
        ratio = ruido2.delta_phi_min / self.ruido.delta_phi_min
        self.assertAlmostEqual(ratio, 0.5, places=10)

    def test_negative_P_raises(self):
        """Potencia negativa debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            LimiteRuidoCuantico(P_watts=-10.0)

    def test_zero_P_raises(self):
        """Potencia cero debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            LimiteRuidoCuantico(P_watts=0.0)

    def test_negative_T_raises(self):
        """Tiempo negativo debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            LimiteRuidoCuantico(T_seconds=-1.0)

    def test_zero_T_raises(self):
        """Tiempo cero debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            LimiteRuidoCuantico(T_seconds=0.0)

    def test_negative_lambda_raises(self):
        """Longitud de onda negativa debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            LimiteRuidoCuantico(lambda_laser_nm=-1064.0)

    def test_shorter_wavelength_larger_noise(self):
        """Láser UV (λ corta) tiene fotones más energéticos (ℏω mayor).
        Dado que δφ_min = √(ℏω/(P·T)), mayor ω implica mayor shot noise."""
        ruido_uv = LimiteRuidoCuantico(lambda_laser_nm=200.0)  # UV: mayor ω
        # Mayor ω_laser → mayor δφ_min = √(ℏω/PT)
        self.assertGreater(ruido_uv.delta_phi_min, self.ruido.delta_phi_min)

    def test_repr_contains_key_info(self):
        """__repr__ debe contener δφ_min y parámetros clave."""
        r = repr(self.ruido)
        self.assertIn("δφ_min", r)
        self.assertIn("W", r)
        self.assertIn("nm", r)


# ============================================================================
# Tests de AnalisisSensibilidad / ResultadoDetectabilidad
# ============================================================================

class TestAnalisisSensibilidad(unittest.TestCase):
    """Verifica la clase AnalisisSensibilidad y el dataclass ResultadoDetectabilidad."""

    def setUp(self):
        self.analisis = AnalisisSensibilidad()
        self.resultado = self.analisis.calcular()

    def test_resultado_is_dataclass(self):
        """calcular() debe retornar un ResultadoDetectabilidad."""
        self.assertIsInstance(self.resultado, ResultadoDetectabilidad)

    def test_delta_theta_0_positive(self):
        """Δθ₀ en el resultado debe ser positivo."""
        self.assertGreater(self.resultado.delta_theta_0_rad, 0.0)

    def test_delta_phi_min_positive(self):
        """δφ_min en el resultado debe ser positivo."""
        self.assertGreater(self.resultado.delta_phi_min_rad, 0.0)

    def test_snr_positive(self):
        """El SNR debe ser positivo."""
        self.assertGreater(self.resultado.snr, 0.0)

    def test_snr_consistent_with_signal_and_noise(self):
        """SNR = Δθ₀ / δφ_min debe ser consistente."""
        expected_snr = (
            self.resultado.delta_theta_0_rad / self.resultado.delta_phi_min_rad
        )
        self.assertAlmostEqual(self.resultado.snr, expected_snr, places=5)

    def test_detectable_5sigma_default(self):
        """Con parámetros de referencia, la señal debe ser detectable a 5σ."""
        self.assertTrue(self.resultado.detectable_5sigma)

    def test_snr_above_5_when_detectable(self):
        """Si detectable_5σ=True, entonces SNR ≥ 5."""
        if self.resultado.detectable_5sigma:
            self.assertGreaterEqual(self.resultado.snr, SNR_5SIGMA)

    def test_margen_factor_consistent(self):
        """El margen de factor = SNR / 5 debe ser consistente."""
        expected = self.resultado.snr / SNR_5SIGMA
        self.assertAlmostEqual(self.resultado.margen_factor, expected, places=8)

    def test_t_5sigma_positive(self):
        """El tiempo para 5σ debe ser positivo."""
        self.assertGreater(self.resultado.t_5sigma_horas, 0.0)

    def test_t_5sigma_scales_with_snr(self):
        """t_5σ = T_ref × (5/SNR)² debe ser proporcional."""
        r = self.resultado
        # If SNR >> 5, t_5sigma_horas = T_INTEGRACION_S/3600 × (5/SNR)²
        T_ref_h = T_INTEGRACION_S / 3600.0
        expected_t = T_ref_h * (SNR_5SIGMA / r.snr) ** 2
        self.assertAlmostEqual(r.t_5sigma_horas, expected_t, places=8)

    def test_f_signal_is_f0(self):
        """La frecuencia de señal en el resultado debe ser f₀."""
        self.assertAlmostEqual(self.resultado.f_signal_hz, F0_HZ, places=6)

    def test_l_km_is_reference(self):
        """L en el resultado debe ser 100 km."""
        self.assertAlmostEqual(self.resultado.L_km, L_IRS_LUNA_KM, places=5)

    def test_g_axion_photon_is_reference(self):
        """g_{aγγ} en el resultado debe ser el valor de referencia."""
        self.assertAlmostEqual(
            self.resultado.g_axion_photon_GeV_inv, G_AXION_PHOTON_GEV_INV, places=20
        )

    def test_resumen_returns_dict(self):
        """resumen() debe retornar un diccionario."""
        r = self.analisis.resumen()
        self.assertIsInstance(r, dict)

    def test_resumen_contains_snr(self):
        """El resumen debe contener la clave 'SNR'."""
        r = self.analisis.resumen()
        self.assertIn("SNR", r)

    def test_resumen_contains_delta_theta(self):
        """El resumen debe contener la clave de Δθ₀."""
        r = self.analisis.resumen()
        self.assertIn("Δθ₀ [rad]", r)

    def test_resumen_snr_matches_calcular(self):
        """El SNR en el resumen debe coincidir con calcular()."""
        r_dict = self.analisis.resumen()
        self.assertAlmostEqual(r_dict["SNR"], self.resultado.snr, places=5)

    def test_not_detectable_with_tiny_g(self):
        """Con g_{aγγ} muy pequeño la señal no debe ser detectable."""
        campo_s = CampoTejido()
        birr_s = BirrefringenciaOscilatoria(
            campo=campo_s, g_axion_photon_GeV_inv=1.0e-30
        )
        ruido_s = LimiteRuidoCuantico()
        analisis_s = AnalisisSensibilidad(birrefringencia=birr_s, ruido=ruido_s)
        r = analisis_s.calcular()
        self.assertFalse(r.detectable_5sigma)

    def test_detectable_with_large_L(self):
        """Con un brazo muy largo la señal debe seguir siendo detectable."""
        birr_l = BirrefringenciaOscilatoria(L_m=1.0e9)
        ruido_s = LimiteRuidoCuantico()
        analisis_l = AnalisisSensibilidad(birrefringencia=birr_l, ruido=ruido_s)
        r = analisis_l.calcular()
        self.assertTrue(r.detectable_5sigma)


# ============================================================================
# Tests de la API pública
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Verifica las tres funciones de la API pública."""

    def test_calcular_amplitud_birrefringencia_default(self):
        """La función de la API debe retornar un valor positivo con parámetros default."""
        result = calcular_amplitud_birrefringencia()
        self.assertGreater(result, 0.0)

    def test_calcular_amplitud_birrefringencia_scales_with_L(self):
        """Doblar L debe doblar Δθ₀."""
        dt1 = calcular_amplitud_birrefringencia(L_km=100.0)
        dt2 = calcular_amplitud_birrefringencia(L_km=200.0)
        self.assertAlmostEqual(dt2 / dt1, 2.0, places=10)

    def test_calcular_amplitud_birrefringencia_scales_with_g(self):
        """Doblar g debe doblar Δθ₀."""
        dt1 = calcular_amplitud_birrefringencia(g_coupling_GeV_inv=1.0e-12)
        dt2 = calcular_amplitud_birrefringencia(g_coupling_GeV_inv=2.0e-12)
        self.assertAlmostEqual(dt2 / dt1, 2.0, places=10)

    def test_calcular_amplitud_birrefringencia_scales_with_rho(self):
        """Cuadruplicar ρ_DM debe doblar Δθ₀."""
        dt1 = calcular_amplitud_birrefringencia(rho_DM_GeV_cm3=0.3)
        dt2 = calcular_amplitud_birrefringencia(rho_DM_GeV_cm3=1.2)
        self.assertAlmostEqual(dt2 / dt1, 2.0, places=10)

    def test_calcular_amplitud_negative_L_raises(self):
        """L negativa debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            calcular_amplitud_birrefringencia(L_km=-100.0)

    def test_calcular_amplitud_zero_g_raises(self):
        """g=0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            calcular_amplitud_birrefringencia(g_coupling_GeV_inv=0.0)

    def test_calcular_amplitud_negative_rho_raises(self):
        """ρ_DM negativa debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            calcular_amplitud_birrefringencia(rho_DM_GeV_cm3=-0.1)

    def test_calcular_limite_ruido_cuantico_default(self):
        """La función de ruido debe retornar un valor positivo con parámetros default."""
        result = calcular_limite_ruido_cuantico()
        self.assertGreater(result, 0.0)

    def test_calcular_limite_ruido_cuantico_scales_with_P(self):
        """Cuadruplicar P debe halvar δφ_min."""
        dphi1 = calcular_limite_ruido_cuantico(P_watts=100.0)
        dphi2 = calcular_limite_ruido_cuantico(P_watts=400.0)
        self.assertAlmostEqual(dphi2 / dphi1, 0.5, places=10)

    def test_calcular_limite_ruido_cuantico_scales_with_T(self):
        """Cuadruplicar T debe halvar δφ_min."""
        dphi1 = calcular_limite_ruido_cuantico(T_seconds=1.0e6)
        dphi2 = calcular_limite_ruido_cuantico(T_seconds=4.0e6)
        self.assertAlmostEqual(dphi2 / dphi1, 0.5, places=10)

    def test_analizar_detectabilidad_returns_dataclass(self):
        """analizar_detectabilidad() debe retornar ResultadoDetectabilidad."""
        r = analizar_detectabilidad()
        self.assertIsInstance(r, ResultadoDetectabilidad)

    def test_analizar_detectabilidad_detectable(self):
        """Con parámetros de referencia la señal debe ser detectable."""
        r = analizar_detectabilidad()
        self.assertTrue(r.detectable_5sigma)

    def test_analizar_detectabilidad_snr_positive(self):
        """El SNR del análisis debe ser positivo."""
        r = analizar_detectabilidad()
        self.assertGreater(r.snr, 0.0)

    def test_analizar_detectabilidad_custom_params(self):
        """analizar_detectabilidad con L pequeña puede no ser detectable."""
        r = analizar_detectabilidad(
            L_km=0.001,
            g_coupling_GeV_inv=1.0e-25,
        )
        self.assertFalse(r.detectable_5sigma)

    def test_analizar_detectabilidad_f_signal(self):
        """La frecuencia de señal debe ser f₀."""
        r = analizar_detectabilidad()
        self.assertAlmostEqual(r.f_signal_hz, F0_HZ, places=6)

    def test_calcular_amplitud_matches_birrefringencia_class(self):
        """La API pública debe dar el mismo resultado que usar las clases directamente."""
        lag = LagrangianoConsistencia()
        campo = CampoTejido(rho_DM_J_m3=RHO_DM_J_M3, lagrangiano=lag)
        birr = BirrefringenciaOscilatoria(
            campo=campo,
            L_m=L_IRS_LUNA_M,
            g_axion_photon_GeV_inv=G_AXION_PHOTON_GEV_INV,
        )
        expected = birr.delta_theta_0
        result = calcular_amplitud_birrefringencia()
        self.assertAlmostEqual(result, expected, places=15)

    def test_calcular_limite_matches_clase(self):
        """La API pública de ruido debe dar el mismo resultado que la clase."""
        ruido = LimiteRuidoCuantico(
            P_watts=P_LASER_W,
            T_seconds=T_INTEGRACION_S,
            lambda_laser_nm=LAMBDA_LASER_NM,
        )
        expected = ruido.delta_phi_min
        result = calcular_limite_ruido_cuantico()
        self.assertAlmostEqual(result, expected, places=15)


# ============================================================================
# Tests de relaciones físicas globales
# ============================================================================

class TestRelacionesFisicas(unittest.TestCase):
    """Verifica relaciones físicas globales entre módulos."""

    def test_m_psi_from_f0(self):
        """m_ψ = h·f₀/c² debe derivarse de f₀."""
        m_derived = H_PLANCK * F0_HZ / (C ** 2)
        m_in_ev = m_derived * (C ** 2) / EV_TO_J
        self.assertAlmostEqual(m_in_ev, M_PSI_EV, places=20)

    def test_lambda_equals_m_psi_over_m_planck(self):
        """λ ≈ m_ψ / M_P debe verificarse."""
        expected_lambda = M_PSI_EV / M_PLANCK_EV
        self.assertAlmostEqual(LAMBDA_SELF, expected_lambda, places=50)

    def test_omega_psi_equals_2pi_f0(self):
        """ω_ψ = 2π·f₀ debe verificarse en el campo."""
        campo = CampoTejido()
        self.assertAlmostEqual(campo.omega_psi, 2.0 * math.pi * F0_HZ, places=8)

    def test_signal_above_shot_noise(self):
        """La señal de birrefringencia debe estar por encima del ruido cuántico."""
        dt = calcular_amplitud_birrefringencia()
        dphi = calcular_limite_ruido_cuantico()
        self.assertGreater(dt, dphi)

    def test_snr_much_greater_than_5(self):
        """Con parámetros de referencia, el SNR debe ser >> 5."""
        r = analizar_detectabilidad()
        self.assertGreater(r.snr, 5.0)

    def test_delta_theta_independent_of_omega_when_density_fixed(self):
        """Δθ₀ es independiente de ω_ψ cuando ρ_DM se fija: ψ₀ ∝ 1/ω_ψ cancela ω_ψ.
        La relación ψ̇₀ = ω_ψ·ψ₀ = √(2ρ_DM) es constante con ρ_DM fija."""
        # Usar un f₀ mayor (campo más rápido → mayor ψ̇ → mayor δn)
        lag_high = LagrangianoConsistencia(f0_hz=2.0 * F0_HZ)
        campo_high = CampoTejido(lagrangiano=lag_high)
        birr_high = BirrefringenciaOscilatoria(campo=campo_high)
        birr_ref = BirrefringenciaOscilatoria()
        # ψ₀ ∝ 1/ω, ψ̇ = ω·ψ₀ = const, Δθ ∝ ψ̇·L/c = const
        # Ratio should be 1.0 since ω_ψ × ψ₀ = √(2ρ_DM) = const
        ratio = birr_high.delta_theta_0 / birr_ref.delta_theta_0
        self.assertAlmostEqual(ratio, 1.0, places=10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
