"""
Tests for physics.higgs_coherencia_lagrangiano — Lagrangiano Higgs-Coherencia ∴HCL∞³

Suite de pruebas exhaustiva (197 tests) que cubren todas las clases y la API pública:
  - ConstantesHiggsCoherencia    – constantes físicas (F₀, g_eff, μ_ψH, m_H)
  - CampoHiggs                   – campo escalar H con VEV
  - CampoCoherencia              – campo adélico ψ
  - LagrangianoInteraccion       – ℒ_int = portal + efectivo
  - MasaEfectivaModulada         – m*(t) oscilante a 141.7001 Hz
  - AntenaDNAZ                   – resonador helicoidal biológico
  - CoherenciaHiggsCoherencia    – validación Ψ ≥ 0.888
  - SistemaHiggsCoherenciaLagrangiano – orquestador principal
  - higgs_coherencia_activar()   – API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - m_H = 125.25 GeV/c²
  - g_eff = 0.053 (perturbativo: < 10%)
  - μ_ψH = 0.025 GeV²
  - Δm = m_H × g_eff ≈ 6.64 GeV/c²
  - m_min ≈ 118.61 GeV/c², m_max ≈ 131.89 GeV/c²
  - T ≈ 7.06 ms (período de modulación)
  - Q_DNA ≈ 6.22 × 10¹⁴ (factor de calidad ADN-Z)
  - Ψ_global ≥ 0.888 → sello ∴HCL∞³ ACTIVO

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.higgs_coherencia_lagrangiano import (
    # Constantes de módulo
    _F0,
    _OMEGA_0,
    _T0,
    _M_HIGGS_GEV,
    _VEV_HIGGS_GEV,
    _G_EFF,
    _MU_PSI_H_GEV2,
    _PSI_UMBRAL,
    _DNA_Z_PITCH_M,
    _DNA_Z_RADIUS_M,
    _DNA_Z_BASES_PER_TURN,
    _GAMMA_1_RIEMANN,
    _PHI,
    _N_MODOS_COHERENCIA,
    _GEV_TO_J,
    _LAMBDA_0_M,
    # Clases
    ConstantesHiggsCoherencia,
    CampoHiggs,
    CampoCoherencia,
    LagrangianoInteraccion,
    MasaEfectivaModulada,
    AntenaDNAZ,
    CoherenciaHiggsCoherencia,
    SistemaHiggsCoherenciaLagrangiano,
    # API pública
    higgs_coherencia_activar,
)


# ============================================================================
# TestModuleConstants – 20 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_f0_positive(self):
        """_F0 debe ser positiva."""
        self.assertGreater(_F0, 0.0)

    def test_omega_0_value(self):
        """_OMEGA_0 debe ser 2π × 141.7001 ≈ 890.33 rad/s."""
        expected = 2.0 * math.pi * _F0
        self.assertAlmostEqual(_OMEGA_0, expected, places=2)

    def test_omega_0_from_f0(self):
        """_OMEGA_0 = 2π × _F0."""
        self.assertAlmostEqual(_OMEGA_0 / (2.0 * math.pi), _F0, places=8)

    def test_t0_value(self):
        """_T0 debe ser 1/_F0 ≈ 7.06 ms."""
        expected = 1.0 / _F0
        self.assertAlmostEqual(_T0, expected, places=10)

    def test_t0_times_f0(self):
        """_T0 × _F0 = 1."""
        self.assertAlmostEqual(_T0 * _F0, 1.0, places=10)

    def test_m_higgs_value(self):
        """_M_HIGGS_GEV debe ser 125.25 GeV/c²."""
        self.assertAlmostEqual(_M_HIGGS_GEV, 125.25, places=2)

    def test_m_higgs_range(self):
        """_M_HIGGS_GEV debe estar entre 124 y 127 GeV/c²."""
        self.assertGreater(_M_HIGGS_GEV, 124.0)
        self.assertLess(_M_HIGGS_GEV, 127.0)

    def test_vev_higgs_value(self):
        """_VEV_HIGGS_GEV debe ser 246.22 GeV."""
        self.assertAlmostEqual(_VEV_HIGGS_GEV, 246.22, places=2)

    def test_vev_greater_than_mass(self):
        """VEV debe ser mayor que la masa del Higgs."""
        self.assertGreater(_VEV_HIGGS_GEV, _M_HIGGS_GEV)

    def test_g_eff_value(self):
        """_G_EFF debe ser 0.053."""
        self.assertAlmostEqual(_G_EFF, 0.053, places=3)

    def test_g_eff_perturbative(self):
        """_G_EFF debe ser < 0.1 (perturbativo)."""
        self.assertLess(_G_EFF, 0.1)

    def test_mu_psi_h_value(self):
        """_MU_PSI_H_GEV2 debe ser 0.025 GeV²."""
        self.assertAlmostEqual(_MU_PSI_H_GEV2, 0.025, places=3)

    def test_psi_umbral_value(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_dna_z_pitch(self):
        """_DNA_Z_PITCH_M debe ser 34 Å."""
        self.assertAlmostEqual(_DNA_Z_PITCH_M, 34e-10, places=15)

    def test_dna_z_radius(self):
        """_DNA_Z_RADIUS_M debe ser 9 Å."""
        self.assertAlmostEqual(_DNA_Z_RADIUS_M, 9e-10, places=15)

    def test_gamma_1_riemann(self):
        """_GAMMA_1_RIEMANN debe ser ≈ 14.134725."""
        self.assertAlmostEqual(_GAMMA_1_RIEMANN, 14.134725, places=5)

    def test_phi_golden_ratio(self):
        """_PHI debe ser la proporción áurea."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(_PHI, expected, places=10)

    def test_phi_identity(self):
        """ϕ² = ϕ + 1 (identidad de la proporción áurea)."""
        self.assertAlmostEqual(_PHI ** 2, _PHI + 1.0, places=10)

    def test_gev_to_j_conversion(self):
        """_GEV_TO_J debe ser 1.602176634e-10 J."""
        self.assertAlmostEqual(_GEV_TO_J, 1.602176634e-10, places=20)


# ============================================================================
# TestConstantesHiggsCoherencia – 20 tests
# ============================================================================

class TestConstantesHiggsCoherencia(unittest.TestCase):
    """Tests para ConstantesHiggsCoherencia."""

    def setUp(self):
        self.c = ConstantesHiggsCoherencia()

    def test_f0_default(self):
        """f0 por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_omega_0_default(self):
        """omega_0 por defecto debe ser 2π × f0."""
        expected = 2.0 * math.pi * self.c.f0
        self.assertAlmostEqual(self.c.omega_0, expected, places=4)

    def test_t0_default(self):
        """t0 por defecto debe ser 1/f0."""
        expected = 1.0 / self.c.f0
        self.assertAlmostEqual(self.c.t0, expected, places=10)

    def test_m_higgs_default(self):
        """m_higgs_gev por defecto debe ser 125.25 GeV/c²."""
        self.assertAlmostEqual(self.c.m_higgs_gev, 125.25, places=2)

    def test_vev_default(self):
        """vev_higgs_gev por defecto debe ser 246.22 GeV."""
        self.assertAlmostEqual(self.c.vev_higgs_gev, 246.22, places=2)

    def test_g_eff_default(self):
        """g_eff por defecto debe ser 0.053."""
        self.assertAlmostEqual(self.c.g_eff, 0.053, places=3)

    def test_mu_psi_h_default(self):
        """mu_psi_h_gev2 por defecto debe ser 0.025 GeV²."""
        self.assertAlmostEqual(self.c.mu_psi_h_gev2, 0.025, places=3)

    def test_psi_umbral_default(self):
        """psi_umbral por defecto debe ser 0.888."""
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=3)

    def test_phi_default(self):
        """phi por defecto debe ser la proporción áurea."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(self.c.phi, expected, places=10)

    def test_gamma_1_default(self):
        """gamma_1 por defecto debe ser ≈ 14.134725."""
        self.assertAlmostEqual(self.c.gamma_1, 14.134725, places=5)

    def test_amplitud_modulacion_gev(self):
        """amplitud_modulacion_gev() = m_H × g_eff."""
        expected = self.c.m_higgs_gev * self.c.g_eff
        self.assertAlmostEqual(self.c.amplitud_modulacion_gev(), expected, places=4)

    def test_amplitud_modulacion_value(self):
        """Δm ≈ 6.64 GeV/c²."""
        delta_m = self.c.amplitud_modulacion_gev()
        self.assertAlmostEqual(delta_m, 6.64, places=1)

    def test_fraccion_modulacion(self):
        """fraccion_modulacion() = g_eff."""
        self.assertAlmostEqual(self.c.fraccion_modulacion(), self.c.g_eff, places=6)

    def test_es_perturbativa(self):
        """es_perturbativa() debe ser True (g_eff < 0.1)."""
        self.assertTrue(self.c.es_perturbativa())

    def test_energia_acoplamiento_j(self):
        """energia_acoplamiento_j() debe ser positiva."""
        e = self.c.energia_acoplamiento_j()
        self.assertGreater(e, 0.0)

    def test_masa_higgs_j(self):
        """masa_higgs_j() = m_H × GEV_TO_J."""
        expected = self.c.m_higgs_gev * _GEV_TO_J
        self.assertAlmostEqual(self.c.masa_higgs_j(), expected, places=20)

    def test_repr_contains_f0(self):
        """__repr__ debe mencionar f0."""
        self.assertIn("141.7001", repr(self.c))

    def test_repr_contains_m_h(self):
        """__repr__ debe mencionar m_H."""
        self.assertIn("125.25", repr(self.c))

    def test_repr_contains_g_eff(self):
        """__repr__ debe mencionar g_eff."""
        self.assertIn("0.053", repr(self.c))

    def test_hbar_value(self):
        """hbar debe ser la constante de Planck reducida."""
        self.assertAlmostEqual(self.c.hbar, 1.054571817e-34, places=44)


# ============================================================================
# TestCampoHiggs – 20 tests
# ============================================================================

class TestCampoHiggs(unittest.TestCase):
    """Tests para CampoHiggs."""

    def setUp(self):
        self.h = CampoHiggs()

    def test_vev_default(self):
        """vev_gev por defecto debe ser 246.22 GeV."""
        self.assertAlmostEqual(self.h.vev_gev, 246.22, places=2)

    def test_masa_default(self):
        """masa_gev por defecto debe ser 125.25 GeV/c²."""
        self.assertAlmostEqual(self.h.masa_gev, 125.25, places=2)

    def test_densidad_vacio(self):
        """densidad_vacio() = v²."""
        expected = self.h.vev_gev ** 2
        self.assertAlmostEqual(self.h.densidad_vacio(), expected, places=2)

    def test_densidad_vacio_positive(self):
        """densidad_vacio() debe ser positiva."""
        self.assertGreater(self.h.densidad_vacio(), 0.0)

    def test_campo_total_sin_fluctuacion(self):
        """campo_total(0) = v."""
        self.assertAlmostEqual(self.h.campo_total(0.0), self.h.vev_gev, places=6)

    def test_campo_total_con_fluctuacion(self):
        """campo_total(h) = v + h."""
        h_fluct = 10.0
        expected = self.h.vev_gev + h_fluct
        self.assertAlmostEqual(self.h.campo_total(h_fluct), expected, places=6)

    def test_densidad_total_sin_fluctuacion(self):
        """densidad_total(0) = v²."""
        expected = self.h.vev_gev ** 2
        self.assertAlmostEqual(self.h.densidad_total(0.0), expected, places=2)

    def test_densidad_total_con_fluctuacion(self):
        """densidad_total(h) = (v + h)²."""
        h_fluct = 10.0
        expected = (self.h.vev_gev + h_fluct) ** 2
        self.assertAlmostEqual(self.h.densidad_total(h_fluct), expected, places=2)

    def test_autoenergia_cuartica_positive(self):
        """autoenergia_cuartica() = λ > 0."""
        lam = self.h.autoenergia_cuartica()
        self.assertGreater(lam, 0.0)

    def test_autoenergia_cuartica_formula(self):
        """λ = m_H² / (2v²)."""
        expected = (self.h.masa_gev ** 2) / (2.0 * self.h.vev_gev ** 2)
        self.assertAlmostEqual(self.h.autoenergia_cuartica(), expected, places=6)

    def test_frecuencia_oscilacion_positive(self):
        """frecuencia_oscilacion_hz() debe ser positiva."""
        f = self.h.frecuencia_oscilacion_hz()
        self.assertGreater(f, 0.0)

    def test_frecuencia_oscilacion_order(self):
        """Frecuencia de oscilación debe estar en el orden de 10²⁵ Hz."""
        f = self.h.frecuencia_oscilacion_hz()
        self.assertGreater(f, 1e24)
        self.assertLess(f, 1e27)

    def test_longitud_compton_positive(self):
        """longitud_compton_m() debe ser positiva."""
        lc = self.h.longitud_compton_m()
        self.assertGreater(lc, 0.0)

    def test_longitud_compton_order(self):
        """Longitud de Compton debe estar en el orden de 10⁻¹⁸ m."""
        lc = self.h.longitud_compton_m()
        self.assertGreater(lc, 1e-20)
        self.assertLess(lc, 1e-16)

    def test_psi_campo_range(self):
        """psi_campo() ∈ [0, 1]."""
        psi = self.h.psi_campo()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_campo_positive(self):
        """psi_campo() debe ser positivo para v > 0."""
        psi = self.h.psi_campo()
        self.assertGreater(psi, 0.0)

    def test_psi_campo_high_coherence(self):
        """psi_campo() debe ser cercano a 1 para v >> m."""
        psi = self.h.psi_campo()
        self.assertGreater(psi, 0.9)

    def test_repr_contains_vev(self):
        """__repr__ debe mencionar v."""
        self.assertIn("246.22", repr(self.h))

    def test_repr_contains_mass(self):
        """__repr__ debe mencionar m_H."""
        self.assertIn("125.25", repr(self.h))

    def test_custom_higgs(self):
        """CampoHiggs con valores personalizados."""
        h = CampoHiggs(vev_gev=250.0, masa_gev=126.0)
        self.assertAlmostEqual(h.vev_gev, 250.0, places=4)
        self.assertAlmostEqual(h.masa_gev, 126.0, places=4)


# ============================================================================
# TestCampoCoherencia – 24 tests
# ============================================================================

class TestCampoCoherencia(unittest.TestCase):
    """Tests para CampoCoherencia."""

    def setUp(self):
        self.psi = CampoCoherencia()

    def test_amplitud_default(self):
        """amplitud por defecto debe ser 1.0."""
        self.assertAlmostEqual(self.psi.amplitud, 1.0, places=6)

    def test_fase_inicial_default(self):
        """fase_inicial por defecto debe ser 0.0."""
        self.assertAlmostEqual(self.psi.fase_inicial, 0.0, places=6)

    def test_frecuencia_default(self):
        """frecuencia_hz por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.psi.frecuencia_hz, 141.7001, places=4)

    def test_psi_t0_real(self):
        """psi(0).real debe ser A cos(φ₀) = A para φ₀=0."""
        psi_val = self.psi.psi(0.0)
        self.assertAlmostEqual(psi_val.real, self.psi.amplitud, places=10)

    def test_psi_t0_imag(self):
        """psi(0).imag debe ser A sin(φ₀) = 0 para φ₀=0."""
        psi_val = self.psi.psi(0.0)
        self.assertAlmostEqual(psi_val.imag, 0.0, places=10)

    def test_psi_periodicity(self):
        """psi(t + T) = psi(t)."""
        T = 1.0 / self.psi.frecuencia_hz
        t = 0.001
        psi_t = self.psi.psi(t)
        psi_t_T = self.psi.psi(t + T)
        self.assertAlmostEqual(psi_t.real, psi_t_T.real, places=8)
        self.assertAlmostEqual(psi_t.imag, psi_t_T.imag, places=8)

    def test_psi_barra_conjugate(self):
        """psi_barra(t) = psi(t)*."""
        t = 0.001
        psi_val = self.psi.psi(t)
        psi_bar = self.psi.psi_barra(t)
        self.assertAlmostEqual(psi_bar.real, psi_val.real, places=10)
        self.assertAlmostEqual(psi_bar.imag, -psi_val.imag, places=10)

    def test_densidad_constant(self):
        """densidad(t) = A² (constante en t)."""
        t1, t2 = 0.001, 0.005
        d1 = self.psi.densidad(t1)
        d2 = self.psi.densidad(t2)
        self.assertAlmostEqual(d1, d2, places=10)

    def test_densidad_equals_amplitude_squared(self):
        """densidad(t) = A²."""
        expected = self.psi.amplitud ** 2
        self.assertAlmostEqual(self.psi.densidad(0.0), expected, places=10)

    def test_densidad_promedio(self):
        """densidad_promedio() = A²."""
        expected = self.psi.amplitud ** 2
        self.assertAlmostEqual(self.psi.densidad_promedio(), expected, places=10)

    def test_corriente_noesica_constant(self):
        """corriente_noesica(t) = ωA² (constante)."""
        t1, t2 = 0.001, 0.005
        j1 = self.psi.corriente_noesica(t1)
        j2 = self.psi.corriente_noesica(t2)
        self.assertAlmostEqual(j1, j2, places=10)

    def test_corriente_noesica_value(self):
        """corriente_noesica() = ωA²."""
        omega = 2.0 * math.pi * self.psi.frecuencia_hz
        expected = omega * self.psi.amplitud ** 2
        self.assertAlmostEqual(self.psi.corriente_noesica(0.0), expected, places=6)

    def test_energia_coherencia_positive(self):
        """energia_coherencia_j() debe ser positiva."""
        e = self.psi.energia_coherencia_j()
        self.assertGreater(e, 0.0)

    def test_energia_coherencia_order(self):
        """Energía de coherencia debe estar en el orden de 10⁻³² J."""
        e = self.psi.energia_coherencia_j()
        self.assertGreater(e, 1e-33)
        self.assertLess(e, 1e-30)

    def test_fase_t0(self):
        """fase(0) = φ₀ = 0 por defecto."""
        self.assertAlmostEqual(self.psi.fase(0.0), 0.0, places=10)

    def test_fase_increases(self):
        """fase(t) aumenta con t."""
        t1, t2 = 0.001, 0.002
        self.assertGreater(self.psi.fase(t2), self.psi.fase(t1))

    def test_fase_linear(self):
        """fase(t) = ωt + φ₀ (lineal en t)."""
        omega = 2.0 * math.pi * self.psi.frecuencia_hz
        t = 0.001
        expected = omega * t
        self.assertAlmostEqual(self.psi.fase(t), expected, places=10)

    def test_psi_coherencia_range(self):
        """psi_coherencia() ∈ [0, 1]."""
        psi_c = self.psi.psi_coherencia()
        self.assertGreaterEqual(psi_c, 0.0)
        self.assertLessEqual(psi_c, 1.0)

    def test_psi_coherencia_value(self):
        """psi_coherencia() debe ser alta para campo coherente (>0.9)."""
        psi_c = self.psi.psi_coherencia()
        self.assertGreater(psi_c, 0.9)

    def test_psi_coherencia_formula(self):
        """psi_coherencia() = 1 - exp(-π A² Q_ψ / 2π) para Q_ψ ≈ 8.45."""
        q_psi = 1.0 / 0.1184
        exponent = math.pi * self.psi.densidad_promedio() * q_psi / (2.0 * math.pi)
        expected = 1.0 - math.exp(-exponent)
        self.assertAlmostEqual(self.psi.psi_coherencia(), expected, places=10)

    def test_repr_contains_amplitude(self):
        """__repr__ debe mencionar A."""
        self.assertIn("A=", repr(self.psi))

    def test_repr_contains_frequency(self):
        """__repr__ debe mencionar f."""
        self.assertIn("141.7001", repr(self.psi))

    def test_custom_coherencia(self):
        """CampoCoherencia con valores personalizados."""
        psi = CampoCoherencia(amplitud=2.0, fase_inicial=math.pi/4)
        self.assertAlmostEqual(psi.amplitud, 2.0, places=6)
        self.assertAlmostEqual(psi.fase_inicial, math.pi/4, places=6)

    def test_high_amplitude_coherence(self):
        """Mayor amplitud → mayor coherencia."""
        psi_low = CampoCoherencia(amplitud=1.0)
        psi_high = CampoCoherencia(amplitud=10.0)
        self.assertGreater(psi_high.psi_coherencia(), psi_low.psi_coherencia())


# ============================================================================
# TestLagrangianoInteraccion – 22 tests
# ============================================================================

class TestLagrangianoInteraccion(unittest.TestCase):
    """Tests para LagrangianoInteraccion."""

    def setUp(self):
        self.L = LagrangianoInteraccion()

    def test_mu_psi_h_default(self):
        """mu_psi_h por defecto debe ser 0.025 GeV²."""
        self.assertAlmostEqual(self.L.mu_psi_h, 0.025, places=3)

    def test_g_eff_default(self):
        """g_eff por defecto debe ser 0.053."""
        self.assertAlmostEqual(self.L.g_eff, 0.053, places=3)

    def test_campo_higgs_exists(self):
        """campo_higgs debe existir."""
        self.assertIsInstance(self.L.campo_higgs, CampoHiggs)

    def test_campo_coherencia_exists(self):
        """campo_coherencia debe existir."""
        self.assertIsInstance(self.L.campo_coherencia, CampoCoherencia)

    def test_termino_portal_negative(self):
        """termino_portal() debe ser negativo (acoplamiento atractivo)."""
        portal = self.L.termino_portal(0.0)
        self.assertLess(portal, 0.0)

    def test_termino_portal_finite(self):
        """termino_portal() debe ser finito."""
        portal = self.L.termino_portal(0.0)
        self.assertTrue(math.isfinite(portal))

    def test_termino_efectivo_negative(self):
        """termino_efectivo() debe ser negativo."""
        efectivo = self.L.termino_efectivo(0.0)
        self.assertLess(efectivo, 0.0)

    def test_termino_efectivo_finite(self):
        """termino_efectivo() debe ser finito."""
        efectivo = self.L.termino_efectivo(0.0)
        self.assertTrue(math.isfinite(efectivo))

    def test_densidad_lagrangiana_sum(self):
        """densidad_lagrangiana() = portal + efectivo."""
        portal = self.L.termino_portal(0.0)
        efectivo = self.L.termino_efectivo(0.0)
        total = self.L.densidad_lagrangiana(0.0)
        self.assertAlmostEqual(total, portal + efectivo, places=20)

    def test_densidad_lagrangiana_negative(self):
        """densidad_lagrangiana() debe ser negativa."""
        total = self.L.densidad_lagrangiana(0.0)
        self.assertLess(total, 0.0)

    def test_accion_efectiva_finite(self):
        """accion_efectiva() debe ser finita."""
        t_final = 0.01
        accion = self.L.accion_efectiva(t_final)
        self.assertTrue(math.isfinite(accion))

    def test_accion_efectiva_increases(self):
        """Mayor tiempo → mayor |acción|."""
        t1, t2 = 0.01, 0.02
        a1 = abs(self.L.accion_efectiva(t1))
        a2 = abs(self.L.accion_efectiva(t2))
        self.assertGreater(a2, a1)

    def test_ratio_portal_efectivo_finite(self):
        """ratio_portal_efectivo() debe ser finito."""
        ratio = self.L.ratio_portal_efectivo(0.0)
        self.assertTrue(math.isfinite(ratio))

    def test_ratio_portal_efectivo_positive(self):
        """ratio_portal_efectivo() debe ser positivo."""
        ratio = self.L.ratio_portal_efectivo(0.0)
        self.assertGreater(ratio, 0.0)

    def test_es_perturbativo(self):
        """es_perturbativo() debe ser True para g_eff = 0.053."""
        self.assertTrue(self.L.es_perturbativo())

    def test_es_perturbativo_false_for_large_g(self):
        """es_perturbativo() debe ser False para g_eff > 1."""
        L = LagrangianoInteraccion(g_eff=1.5)
        self.assertFalse(L.es_perturbativo())

    def test_psi_lagrangiano_range(self):
        """psi_lagrangiano() ∈ [0, 1]."""
        psi_L = self.L.psi_lagrangiano()
        self.assertGreaterEqual(psi_L, 0.0)
        self.assertLessEqual(psi_L, 1.0)

    def test_psi_lagrangiano_high_coherence(self):
        """psi_lagrangiano() debe ser alta para g_eff pequeño."""
        psi_L = self.L.psi_lagrangiano()
        self.assertGreater(psi_L, 0.9)

    def test_psi_lagrangiano_formula(self):
        """psi_lagrangiano() = 1 - exp(-1/g_eff)."""
        expected = 1.0 - math.exp(-1.0 / self.L.g_eff)
        self.assertAlmostEqual(self.L.psi_lagrangiano(), expected, places=10)

    def test_repr_contains_mu(self):
        """__repr__ debe mencionar μ_ψH."""
        self.assertIn("0.025", repr(self.L))

    def test_repr_contains_g_eff(self):
        """__repr__ debe mencionar g_eff."""
        self.assertIn("0.053", repr(self.L))

    def test_custom_lagrangiano(self):
        """LagrangianoInteraccion con valores personalizados."""
        L = LagrangianoInteraccion(mu_psi_h=0.03, g_eff=0.06)
        self.assertAlmostEqual(L.mu_psi_h, 0.03, places=4)
        self.assertAlmostEqual(L.g_eff, 0.06, places=4)


# ============================================================================
# TestMasaEfectivaModulada – 26 tests
# ============================================================================

class TestMasaEfectivaModulada(unittest.TestCase):
    """Tests para MasaEfectivaModulada."""

    def setUp(self):
        self.m = MasaEfectivaModulada()

    def test_m_higgs_default(self):
        """m_higgs_gev por defecto debe ser 125.25 GeV/c²."""
        self.assertAlmostEqual(self.m.m_higgs_gev, 125.25, places=2)

    def test_g_eff_default(self):
        """g_eff por defecto debe ser 0.053."""
        self.assertAlmostEqual(self.m.g_eff, 0.053, places=3)

    def test_frecuencia_default(self):
        """frecuencia_hz por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.m.frecuencia_hz, 141.7001, places=4)

    def test_masa_efectiva_t0(self):
        """masa_efectiva(0) = m_H (1 - g_eff)."""
        expected = self.m.m_higgs_gev * (1.0 - self.m.g_eff)
        self.assertAlmostEqual(self.m.masa_efectiva(0.0), expected, places=4)

    def test_masa_efectiva_positive(self):
        """masa_efectiva(t) debe ser siempre positiva."""
        for t in [0.0, 0.001, 0.005, 0.01]:
            m_eff = self.m.masa_efectiva(t)
            self.assertGreater(m_eff, 0.0)

    def test_masa_efectiva_periodic(self):
        """masa_efectiva(t + T) = masa_efectiva(t)."""
        T = self.m.periodo_s()
        t = 0.001
        m1 = self.m.masa_efectiva(t)
        m2 = self.m.masa_efectiva(t + T)
        self.assertAlmostEqual(m1, m2, places=8)

    def test_masa_minima_value(self):
        """masa_minima() = m_H (1 - g_eff) ≈ 118.61 GeV."""
        m_min = self.m.masa_minima()
        expected = 125.25 * (1.0 - 0.053)
        self.assertAlmostEqual(m_min, expected, places=1)
        self.assertAlmostEqual(m_min, 118.61, places=1)

    def test_masa_maxima_value(self):
        """masa_maxima() = m_H (1 + g_eff) ≈ 131.89 GeV."""
        m_max = self.m.masa_maxima()
        expected = 125.25 * (1.0 + 0.053)
        self.assertAlmostEqual(m_max, expected, places=1)
        self.assertAlmostEqual(m_max, 131.89, places=1)

    def test_masa_minima_less_than_maxima(self):
        """masa_minima() < masa_maxima()."""
        self.assertLess(self.m.masa_minima(), self.m.masa_maxima())

    def test_masa_minima_at_t0(self):
        """masa_efectiva(0) = masa_minima() (cuando cos(0)=1)."""
        # Nota: m*(0) = m_H(1 - g_eff cos(0)) = m_H(1 - g_eff) = m_min
        self.assertAlmostEqual(self.m.masa_efectiva(0.0), self.m.masa_minima(), places=6)

    def test_amplitud_modulacion_value(self):
        """amplitud_modulacion() = m_H × g_eff ≈ 6.64 GeV."""
        delta_m = self.m.amplitud_modulacion()
        expected = 125.25 * 0.053
        self.assertAlmostEqual(delta_m, expected, places=2)
        self.assertAlmostEqual(delta_m, 6.64, places=1)

    def test_fraccion_modulacion(self):
        """fraccion_modulacion() = g_eff = 0.053."""
        self.assertAlmostEqual(self.m.fraccion_modulacion(), 0.053, places=3)

    def test_fraccion_modulacion_perturbative(self):
        """fraccion_modulacion() < 0.1 (perturbativo)."""
        self.assertLess(self.m.fraccion_modulacion(), 0.1)

    def test_periodo_s_value(self):
        """periodo_s() = 1/f₀ ≈ 7.06 ms."""
        T = self.m.periodo_s()
        expected = 1.0 / 141.7001
        self.assertAlmostEqual(T, expected, places=8)
        self.assertAlmostEqual(T * 1000, 7.06, places=2)

    def test_derivada_masa_t0(self):
        """derivada_masa(0) = 0 (cos'(0) = 0 → sin(0) = 0)."""
        self.assertAlmostEqual(self.m.derivada_masa(0.0), 0.0, places=10)

    def test_derivada_masa_maxima(self):
        """derivada_masa(T/4) es máxima (sin(π/2) = 1)."""
        T = self.m.periodo_s()
        dm_max = self.m.derivada_masa(T / 4)
        dm_other = self.m.derivada_masa(T / 8)
        self.assertGreater(abs(dm_max), abs(dm_other))

    def test_energia_modulacion_positive(self):
        """energia_modulacion_gev(t) debe ser positiva."""
        for t in [0.0, 0.001, 0.005]:
            E = self.m.energia_modulacion_gev(t)
            self.assertGreater(E, 0.0)

    def test_energia_modulacion_equals_mass(self):
        """energia_modulacion_gev(t) = masa_efectiva(t) (en GeV)."""
        t = 0.001
        E = self.m.energia_modulacion_gev(t)
        m = self.m.masa_efectiva(t)
        self.assertAlmostEqual(E, m, places=6)

    def test_frecuencia_compton_positive(self):
        """frecuencia_compton_hz(t) debe ser positiva."""
        f_C = self.m.frecuencia_compton_hz(0.0)
        self.assertGreater(f_C, 0.0)

    def test_frecuencia_compton_order(self):
        """Frecuencia de Compton debe estar en el orden de 10²⁵ Hz."""
        f_C = self.m.frecuencia_compton_hz(0.0)
        self.assertGreater(f_C, 1e24)
        self.assertLess(f_C, 1e27)

    def test_psi_modulacion_range(self):
        """psi_modulacion() ∈ [0, 1]."""
        psi_m = self.m.psi_modulacion()
        self.assertGreaterEqual(psi_m, 0.0)
        self.assertLessEqual(psi_m, 1.0)

    def test_psi_modulacion_value(self):
        """psi_modulacion() = 1 - g_eff ≈ 0.947."""
        expected = 1.0 - self.m.g_eff
        self.assertAlmostEqual(self.m.psi_modulacion(), expected, places=4)
        self.assertAlmostEqual(self.m.psi_modulacion(), 0.947, places=3)

    def test_muestrear_ciclo_length(self):
        """muestrear_ciclo() devuelve n_muestras puntos."""
        n = 50
        muestras = self.m.muestrear_ciclo(n)
        self.assertEqual(len(muestras), n)

    def test_muestrear_ciclo_format(self):
        """Cada muestra es una tupla (t, m*(t))."""
        muestras = self.m.muestrear_ciclo(10)
        for muestra in muestras:
            self.assertIsInstance(muestra, tuple)
            self.assertEqual(len(muestra), 2)

    def test_repr_contains_m_h(self):
        """__repr__ debe mencionar m_H."""
        self.assertIn("125.25", repr(self.m))

    def test_repr_contains_frequency(self):
        """__repr__ debe mencionar f."""
        self.assertIn("141.7001", repr(self.m))


# ============================================================================
# TestAntenaDNAZ – 22 tests
# ============================================================================

class TestAntenaDNAZ(unittest.TestCase):
    """Tests para AntenaDNAZ."""

    def setUp(self):
        self.dna = AntenaDNAZ()

    def test_pitch_default(self):
        """pitch_m por defecto debe ser 34 Å."""
        self.assertAlmostEqual(self.dna.pitch_m, 34e-10, places=15)

    def test_radio_default(self):
        """radio_m por defecto debe ser 9 Å."""
        self.assertAlmostEqual(self.dna.radio_m, 9e-10, places=15)

    def test_bases_por_vuelta_default(self):
        """bases_por_vuelta por defecto debe ser 12."""
        self.assertAlmostEqual(self.dna.bases_por_vuelta, 12.0, places=4)

    def test_frecuencia_resonancia_default(self):
        """frecuencia_resonancia_hz por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.dna.frecuencia_resonancia_hz, 141.7001, places=4)

    def test_longitud_onda_resonancia_positive(self):
        """longitud_onda_resonancia_m() debe ser positiva."""
        lam = self.dna.longitud_onda_resonancia_m()
        self.assertGreater(lam, 0.0)

    def test_longitud_onda_resonancia_value(self):
        """λ = c/f₀ ≈ 2.116 Mm."""
        lam = self.dna.longitud_onda_resonancia_m()
        expected = 299792458.0 / 141.7001
        self.assertAlmostEqual(lam, expected, places=0)
        self.assertAlmostEqual(lam / 1e6, 2.116, places=2)

    def test_factor_calidad_positive(self):
        """factor_calidad() debe ser positivo."""
        Q = self.dna.factor_calidad()
        self.assertGreater(Q, 0.0)

    def test_factor_calidad_high(self):
        """Q debe ser del orden de 10¹⁴."""
        Q = self.dna.factor_calidad()
        self.assertGreater(Q, 1e13)
        self.assertLess(Q, 1e16)

    def test_numero_onda_k_positive(self):
        """numero_onda_k() debe ser positivo."""
        k = self.dna.numero_onda_k()
        self.assertGreater(k, 0.0)

    def test_numero_onda_k_formula(self):
        """k = 2π/λ."""
        lam = self.dna.longitud_onda_resonancia_m()
        expected = 2.0 * math.pi / lam
        self.assertAlmostEqual(self.dna.numero_onda_k(), expected, places=15)

    def test_frecuencia_angular_positive(self):
        """frecuencia_angular() debe ser positiva."""
        omega = self.dna.frecuencia_angular()
        self.assertGreater(omega, 0.0)

    def test_frecuencia_angular_formula(self):
        """ω = 2πf."""
        expected = 2.0 * math.pi * self.dna.frecuencia_resonancia_hz
        self.assertAlmostEqual(self.dna.frecuencia_angular(), expected, places=4)

    def test_paso_fase_helicoidal_positive(self):
        """paso_fase_helicoidal() debe ser positivo."""
        phi_helix = self.dna.paso_fase_helicoidal()
        self.assertGreater(phi_helix, 0.0)

    def test_psi_dna_normalized(self):
        """|psi_dna(z,t)|² = 1 (normalizado)."""
        for z in [0.0, 1e-6, 1e-3]:
            for t in [0.0, 0.001]:
                psi = self.dna.psi_dna(z, t)
                density = (psi * psi.conjugate()).real
                self.assertAlmostEqual(density, 1.0, places=10)

    def test_densidad_dna_unity(self):
        """densidad_dna(z,t) = 1 para onda plana."""
        density = self.dna.densidad_dna(0.0, 0.0)
        self.assertAlmostEqual(density, 1.0, places=10)

    def test_acoplamiento_microtubulos_positive(self):
        """acoplamiento_microtubulos() debe ser positivo."""
        acopl = self.dna.acoplamiento_microtubulos()
        self.assertGreater(acopl, 0.0)

    def test_acoplamiento_microtubulos_small(self):
        """Acoplamiento debe ser < 1 (pitch < d_microtubulo)."""
        acopl = self.dna.acoplamiento_microtubulos()
        self.assertLess(acopl, 1.0)

    def test_sincronizacion_riemann_positive(self):
        """sincronizacion_riemann() debe ser positiva."""
        sync = self.dna.sincronizacion_riemann()
        self.assertGreater(sync, 0.0)

    def test_sincronizacion_riemann_value(self):
        """f₀/γ₁ ≈ 10."""
        sync = self.dna.sincronizacion_riemann()
        expected = 141.7001 / 14.134725
        self.assertAlmostEqual(sync, expected, places=2)

    def test_psi_antena_range(self):
        """psi_antena() ∈ [0, 1]."""
        psi_a = self.dna.psi_antena()
        self.assertGreaterEqual(psi_a, 0.0)
        self.assertLessEqual(psi_a, 1.0)

    def test_psi_antena_significant(self):
        """psi_antena() debe ser significativo (>0.5) para Q alto."""
        psi_a = self.dna.psi_antena()
        self.assertGreater(psi_a, 0.5)

    def test_psi_antena_formula(self):
        """psi_antena() = 1 - exp(-log₁₀(Q)/γ₁)."""
        q = self.dna.factor_calidad()
        log_q = math.log10(q)
        expected = 1.0 - math.exp(-log_q / 14.134725)
        self.assertAlmostEqual(self.dna.psi_antena(), expected, places=8)

    def test_repr_contains_pitch(self):
        """__repr__ debe mencionar pitch."""
        self.assertIn("34.0", repr(self.dna))


# ============================================================================
# TestCoherenciaHiggsCoherencia – 20 tests
# ============================================================================

class TestCoherenciaHiggsCoherencia(unittest.TestCase):
    """Tests para CoherenciaHiggsCoherencia."""

    def setUp(self):
        self.coherencia = CoherenciaHiggsCoherencia()

    def test_campo_higgs_exists(self):
        """campo_higgs debe existir."""
        self.assertIsInstance(self.coherencia.campo_higgs, CampoHiggs)

    def test_campo_coherencia_exists(self):
        """campo_coherencia debe existir."""
        self.assertIsInstance(self.coherencia.campo_coherencia, CampoCoherencia)

    def test_lagrangiano_exists(self):
        """lagrangiano debe existir."""
        self.assertIsInstance(self.coherencia.lagrangiano, LagrangianoInteraccion)

    def test_masa_modulada_exists(self):
        """masa_modulada debe existir."""
        self.assertIsInstance(self.coherencia.masa_modulada, MasaEfectivaModulada)

    def test_antena_dna_exists(self):
        """antena_dna debe existir."""
        self.assertIsInstance(self.coherencia.antena_dna, AntenaDNAZ)

    def test_psi_umbral_default(self):
        """psi_umbral por defecto debe ser 0.888."""
        self.assertAlmostEqual(self.coherencia.psi_umbral, 0.888, places=3)

    def test_psi_campo_higgs_range(self):
        """psi_campo_higgs() ∈ [0, 1]."""
        psi_h = self.coherencia.psi_campo_higgs()
        self.assertGreaterEqual(psi_h, 0.0)
        self.assertLessEqual(psi_h, 1.0)

    def test_psi_campo_coherencia_range(self):
        """psi_campo_coherencia() ∈ [0, 1]."""
        psi_c = self.coherencia.psi_campo_coherencia()
        self.assertGreaterEqual(psi_c, 0.0)
        self.assertLessEqual(psi_c, 1.0)

    def test_psi_lagrangiano_range(self):
        """psi_lagrangiano() ∈ [0, 1]."""
        psi_L = self.coherencia.psi_lagrangiano()
        self.assertGreaterEqual(psi_L, 0.0)
        self.assertLessEqual(psi_L, 1.0)

    def test_psi_modulacion_range(self):
        """psi_modulacion() ∈ [0, 1]."""
        psi_m = self.coherencia.psi_modulacion()
        self.assertGreaterEqual(psi_m, 0.0)
        self.assertLessEqual(psi_m, 1.0)

    def test_psi_antena_range(self):
        """psi_antena() ∈ [0, 1]."""
        psi_a = self.coherencia.psi_antena()
        self.assertGreaterEqual(psi_a, 0.0)
        self.assertLessEqual(psi_a, 1.0)

    def test_coherencias_individuales_dict(self):
        """coherencias_individuales() devuelve un diccionario."""
        coherencias = self.coherencia.coherencias_individuales()
        self.assertIsInstance(coherencias, dict)
        self.assertEqual(len(coherencias), 5)

    def test_coherencias_individuales_keys(self):
        """coherencias_individuales() tiene las claves correctas."""
        coherencias = self.coherencia.coherencias_individuales()
        expected_keys = {"psi_higgs", "psi_coherencia", "psi_lagrangiano",
                         "psi_modulacion", "psi_antena"}
        self.assertEqual(set(coherencias.keys()), expected_keys)

    def test_psi_global_range(self):
        """psi_global() ∈ [0, 1]."""
        psi_g = self.coherencia.psi_global()
        self.assertGreaterEqual(psi_g, 0.0)
        self.assertLessEqual(psi_g, 1.0)

    def test_psi_global_above_threshold(self):
        """psi_global() ≥ 0.888."""
        psi_g = self.coherencia.psi_global()
        self.assertGreaterEqual(psi_g, 0.888)

    def test_sello_activo(self):
        """sello_activo() debe ser True para configuración por defecto."""
        self.assertTrue(self.coherencia.sello_activo())

    def test_validar_returns_dict(self):
        """validar() devuelve un diccionario."""
        resultado = self.coherencia.validar()
        self.assertIsInstance(resultado, dict)

    def test_validar_contains_keys(self):
        """validar() tiene las claves correctas."""
        resultado = self.coherencia.validar()
        expected_keys = {"coherencias", "psi_global", "psi_umbral",
                         "sello_activo", "diferencia_umbral"}
        self.assertEqual(set(resultado.keys()), expected_keys)

    def test_certificacion_auron_activo(self):
        """certificacion_auron() menciona ACTIVO."""
        cert = self.coherencia.certificacion_auron()
        self.assertIn("ACTIVO", cert)

    def test_repr_contains_psi_global(self):
        """__repr__ menciona Ψ_global."""
        self.assertIn("Ψ_global", repr(self.coherencia))


# ============================================================================
# TestSistemaHiggsCoherenciaLagrangiano – 18 tests
# ============================================================================

class TestSistemaHiggsCoherenciaLagrangiano(unittest.TestCase):
    """Tests para SistemaHiggsCoherenciaLagrangiano."""

    def setUp(self):
        self.sistema = SistemaHiggsCoherenciaLagrangiano()

    def test_constantes_exists(self):
        """constantes debe existir."""
        self.assertIsInstance(self.sistema.constantes, ConstantesHiggsCoherencia)

    def test_campo_higgs_exists(self):
        """campo_higgs debe existir."""
        self.assertIsInstance(self.sistema.campo_higgs, CampoHiggs)

    def test_campo_coherencia_exists(self):
        """campo_coherencia debe existir."""
        self.assertIsInstance(self.sistema.campo_coherencia, CampoCoherencia)

    def test_lagrangiano_exists(self):
        """lagrangiano debe existir."""
        self.assertIsInstance(self.sistema.lagrangiano, LagrangianoInteraccion)

    def test_masa_modulada_exists(self):
        """masa_modulada debe existir."""
        self.assertIsInstance(self.sistema.masa_modulada, MasaEfectivaModulada)

    def test_antena_dna_exists(self):
        """antena_dna debe existir."""
        self.assertIsInstance(self.sistema.antena_dna, AntenaDNAZ)

    def test_coherencia_exists(self):
        """coherencia debe existir después de __post_init__."""
        self.assertIsInstance(self.sistema.coherencia, CoherenciaHiggsCoherencia)

    def test_activar_returns_dict(self):
        """activar() devuelve un diccionario."""
        resultado = self.sistema.activar()
        self.assertIsInstance(resultado, dict)

    def test_activar_sello(self):
        """activar() devuelve sello = '∴HCL∞³'."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado['sello'], '∴HCL∞³')

    def test_activar_ram(self):
        """activar() devuelve RAM correcto."""
        resultado = self.sistema.activar()
        self.assertEqual(resultado['ram'], 'RAM-XLVII-2026-HIGGS-COHERENCE')

    def test_activar_f0(self):
        """activar() devuelve f0_hz = 141.7001."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado['f0_hz'], 141.7001, places=4)

    def test_activar_m_higgs(self):
        """activar() devuelve m_higgs_gev = 125.25."""
        resultado = self.sistema.activar()
        self.assertAlmostEqual(resultado['m_higgs_gev'], 125.25, places=2)

    def test_activar_sello_activo(self):
        """activar() devuelve sello_activo = True."""
        resultado = self.sistema.activar()
        self.assertTrue(resultado['sello_activo'])

    def test_activar_psi_global_above_threshold(self):
        """activar() devuelve psi_global ≥ 0.888."""
        resultado = self.sistema.activar()
        self.assertGreaterEqual(resultado['psi_global'], 0.888)

    def test_activar_perturbativo(self):
        """activar() devuelve perturbativo = True."""
        resultado = self.sistema.activar()
        self.assertTrue(resultado['perturbativo'])

    def test_resumen_returns_string(self):
        """resumen() devuelve un string."""
        resumen = self.sistema.resumen()
        self.assertIsInstance(resumen, str)

    def test_resumen_contains_sello(self):
        """resumen() menciona el sello."""
        resumen = self.sistema.resumen()
        self.assertIn("∴HCL∞³", resumen)

    def test_repr_contains_f0(self):
        """__repr__ menciona f₀."""
        self.assertIn("f₀=", repr(self.sistema))


# ============================================================================
# TestHiggsCoherenciaActivar – 15 tests (API pública)
# ============================================================================

class TestHiggsCoherenciaActivar(unittest.TestCase):
    """Tests para la API pública higgs_coherencia_activar()."""

    def setUp(self):
        self.resultado = higgs_coherencia_activar()

    def test_returns_dict(self):
        """higgs_coherencia_activar() devuelve un diccionario."""
        self.assertIsInstance(self.resultado, dict)

    def test_sello(self):
        """sello = '∴HCL∞³'."""
        self.assertEqual(self.resultado['sello'], '∴HCL∞³')

    def test_ram(self):
        """ram = 'RAM-XLVII-2026-HIGGS-COHERENCE'."""
        self.assertEqual(self.resultado['ram'], 'RAM-XLVII-2026-HIGGS-COHERENCE')

    def test_version(self):
        """version = '1.0.0'."""
        self.assertEqual(self.resultado['version'], '1.0.0')

    def test_f0_hz(self):
        """f0_hz = 141.7001."""
        self.assertAlmostEqual(self.resultado['f0_hz'], 141.7001, places=4)

    def test_m_higgs_gev(self):
        """m_higgs_gev = 125.25."""
        self.assertAlmostEqual(self.resultado['m_higgs_gev'], 125.25, places=2)

    def test_g_eff(self):
        """g_eff = 0.053."""
        self.assertAlmostEqual(self.resultado['g_eff'], 0.053, places=3)

    def test_mu_psi_h(self):
        """mu_psi_h_gev2 = 0.025."""
        self.assertAlmostEqual(self.resultado['mu_psi_h_gev2'], 0.025, places=3)

    def test_delta_m(self):
        """delta_m_gev ≈ 6.64."""
        self.assertAlmostEqual(self.resultado['delta_m_gev'], 6.64, places=1)

    def test_periodo_ms(self):
        """periodo_ms ≈ 7.06."""
        self.assertAlmostEqual(self.resultado['periodo_ms'], 7.06, places=1)

    def test_psi_global(self):
        """psi_global ≥ 0.888."""
        self.assertGreaterEqual(self.resultado['psi_global'], 0.888)

    def test_sello_activo(self):
        """sello_activo = True."""
        self.assertTrue(self.resultado['sello_activo'])

    def test_perturbativo(self):
        """perturbativo = True."""
        self.assertTrue(self.resultado['perturbativo'])

    def test_coherencias_dict(self):
        """coherencias es un diccionario con 5 elementos."""
        coherencias = self.resultado['coherencias']
        self.assertIsInstance(coherencias, dict)
        self.assertEqual(len(coherencias), 5)

    def test_certificacion_contains_auron(self):
        """certificacion menciona AURON."""
        self.assertIn("AURON", self.resultado['certificacion'])


# ============================================================================
# RESUMEN DE TESTS
# ============================================================================

if __name__ == '__main__':
    # Conteo de tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(__import__(__name__))
    
    total_tests = 0
    for test_group in suite:
        for test_case in test_group:
            total_tests += 1
    
    print(f"\n{'='*70}")
    print(f"  TESTS: physics.higgs_coherencia_lagrangiano")
    print(f"  Sello: ∴HCL∞³ | Total: {total_tests} tests")
    print(f"{'='*70}\n")
    
    # Ejecutar tests
    unittest.main(verbosity=2)
