"""
Tests for physics.rutas_convergencia — Las 3 Rutas de Convergencia Física (RCF∞³)

Pruebas que cubren las 8 clases y la API pública:
  - ConstantesRutas           – constantes físicas compartidas
  - RutaHolografica           – Ruta A: c/(2π·√(λ_p·R_dS))/N₇ ≈ 40,91 Hz
  - RutaTopologica            – Ruta B: 1,67·t_energy/H ≈ 50,54 Hz
  - RutaMasaEfectiva          – Ruta C: m_ψ·c²/H ≈ 141,34 Hz
  - CoherenciaConvergencia    – Ψ_global ≥ 0,888
  - ResultadoRuta             – dataclass de resultado individual
  - SistemaRutasConvergencia  – orquestador
  - ResultadoConvergencia     – dataclass del resultado completo
  - rutas_convergencia_calcular() – API pública

Invariantes clave verificados:
  - f_A ≈ 40,91 Hz   (38 < f_A < 44)
  - f_B ≈ 50,54 Hz   (48 < f_B < 54)
  - f_C ≈ 141,34 Hz  (139 < f_C < 143)
  - Ψ_A = 0,9469  Ψ_B = 0,9819  Ψ_C = 0,9993
  - Ψ_global ≥ 0,888
  - f_C es la más próxima a F₀
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.rutas_convergencia import (
    # Constantes de módulo
    _F0,
    _H,
    _HBAR,
    _C,
    _LAMBDA_P_M,
    _R_DS_M,
    _LAMBDA_COSM,
    _N_SITES,
    _N7,
    _GAP_FACTOR,
    _PSI_A,
    _PSI_B,
    _PSI_C,
    _PSI_UMBRAL,
    _SIN_PI7,
    _COS_PI7,
    _SIN_2PI7,
    _COS_2PI7,
    _F_RAW_A,
    # Clases
    ConstantesRutas,
    RutaHolografica,
    RutaTopologica,
    RutaMasaEfectiva,
    CoherenciaConvergencia,
    ResultadoRuta,
    SistemaRutasConvergencia,
    ResultadoConvergencia,
    # API pública
    rutas_convergencia_calcular,
)


# ============================================================================
# TestModuleConstants – constantes de módulo
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests for module-level constants."""

    def test_f0_value(self):
        """_F0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_h_planck_value(self):
        """_H must equal CODATA 2018 Planck constant."""
        self.assertAlmostEqual(_H, 6.62607015e-34, places=15)

    def test_hbar_equals_h_over_2pi(self):
        """_HBAR must equal _H / (2π)."""
        self.assertAlmostEqual(_HBAR, _H / (2.0 * math.pi), places=15)

    def test_c_exact(self):
        """_C must equal the exact speed of light."""
        self.assertEqual(_C, 299_792_458.0)

    def test_lambda_p_order_of_magnitude(self):
        """Proton Compton wavelength must be ~1.3e-15 m (femtometre scale)."""
        self.assertGreater(_LAMBDA_P_M, 1.0e-15)
        self.assertLess(_LAMBDA_P_M, 2.0e-15)

    def test_r_ds_order_of_magnitude(self):
        """De Sitter radius must be ~1.65e26 m."""
        self.assertGreater(_R_DS_M, 1.0e26)
        self.assertLess(_R_DS_M, 2.0e26)

    def test_r_ds_from_lambda_cosm(self):
        """R_dS must equal sqrt(3/Λ)."""
        expected = math.sqrt(3.0 / _LAMBDA_COSM)
        self.assertAlmostEqual(_R_DS_M, expected, places=10)

    def test_n_sites_is_7(self):
        """N_SITES must equal 7 (heptagonal ring)."""
        self.assertEqual(_N_SITES, 7)

    def test_n7_is_2_5(self):
        """N₇ must equal 2.5 = 5/2."""
        self.assertAlmostEqual(_N7, 2.5, places=10)

    def test_gap_factor(self):
        """GAP_FACTOR must equal 1.67 (many-body optical gap)."""
        self.assertAlmostEqual(_GAP_FACTOR, 1.67, places=10)

    def test_psi_a_value(self):
        """Ψ_A must equal 0.9469."""
        self.assertAlmostEqual(_PSI_A, 0.9469, places=4)

    def test_psi_b_value(self):
        """Ψ_B must equal 0.9819."""
        self.assertAlmostEqual(_PSI_B, 0.9819, places=4)

    def test_psi_c_value(self):
        """Ψ_C must equal 0.9993."""
        self.assertAlmostEqual(_PSI_C, 0.9993, places=4)

    def test_psi_umbral(self):
        """QCAL coherence threshold must equal 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_psi_ordering(self):
        """Coherences must satisfy Ψ_A < Ψ_B < Ψ_C."""
        self.assertLess(_PSI_A, _PSI_B)
        self.assertLess(_PSI_B, _PSI_C)

    def test_all_psi_above_umbral(self):
        """All individual coherences must exceed the QCAL threshold."""
        for psi in (_PSI_A, _PSI_B, _PSI_C):
            self.assertGreaterEqual(psi, _PSI_UMBRAL)

    def test_sin_pi7(self):
        """_SIN_PI7 must equal sin(π/7)."""
        self.assertAlmostEqual(_SIN_PI7, math.sin(math.pi / 7), places=12)

    def test_cos_pi7(self):
        """_COS_PI7 must equal cos(π/7)."""
        self.assertAlmostEqual(_COS_PI7, math.cos(math.pi / 7), places=12)

    def test_sin_2pi7(self):
        """_SIN_2PI7 must equal sin(2π/7)."""
        self.assertAlmostEqual(_SIN_2PI7, math.sin(2.0 * math.pi / 7), places=12)

    def test_cos_2pi7(self):
        """_COS_2PI7 must equal cos(2π/7)."""
        self.assertAlmostEqual(_COS_2PI7, math.cos(2.0 * math.pi / 7), places=12)

    def test_sin_cos_identity(self):
        """sin²(π/7) + cos²(π/7) must equal 1 (Pythagorean identity)."""
        self.assertAlmostEqual(_SIN_PI7 ** 2 + _COS_PI7 ** 2, 1.0, places=12)

    def test_f_raw_a_formula(self):
        """_F_RAW_A must equal c/(2π·√(λ_p·R_dS))."""
        expected = _C / (2.0 * math.pi * math.sqrt(_LAMBDA_P_M * _R_DS_M))
        self.assertAlmostEqual(_F_RAW_A, expected, places=6)

    def test_f_raw_a_range(self):
        """Holographic raw frequency must be between 90 and 120 Hz."""
        self.assertGreater(_F_RAW_A, 90.0)
        self.assertLess(_F_RAW_A, 120.0)


# ============================================================================
# TestConstantesRutas – Clase 1
# ============================================================================

class TestConstantesRutas(unittest.TestCase):
    """Tests for ConstantesRutas dataclass."""

    def setUp(self):
        self.c = ConstantesRutas()

    def test_default_f0(self):
        """Default f0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_default_h(self):
        """Default h must equal CODATA Planck constant."""
        self.assertAlmostEqual(self.c.h, 6.62607015e-34, places=15)

    def test_default_c(self):
        """Default c must equal exact speed of light."""
        self.assertEqual(self.c.c, 299_792_458.0)

    def test_lambda_p_m_value(self):
        """Proton Compton wavelength must be h/(m_p*c)."""
        m_p = 1.67262192369e-27  # kg
        expected = 6.62607015e-34 / (m_p * 299_792_458.0)
        self.assertAlmostEqual(self.c.lambda_p_m, expected, places=25)

    def test_r_ds_m_value(self):
        """De Sitter radius must be sqrt(3/Lambda_cosm)."""
        expected = math.sqrt(3.0 / 1.1056e-52)
        self.assertAlmostEqual(self.c.r_ds_m, expected, places=10)

    def test_n7_value(self):
        """N₇ must be 2.5."""
        self.assertAlmostEqual(self.c.n7, 2.5, places=10)

    def test_n_sites_value(self):
        """N_SITES must be 7."""
        self.assertEqual(self.c.n_sites, 7)

    def test_gap_factor_value(self):
        """GAP_FACTOR must be 1.67."""
        self.assertAlmostEqual(self.c.gap_factor, 1.67, places=10)

    def test_f_raw_holografica(self):
        """f_raw_holografica() must compute c/(2π·√(λ_p·R_dS))."""
        expected = self.c.c / (
            2.0 * math.pi * math.sqrt(self.c.lambda_p_m * self.c.r_ds_m)
        )
        self.assertAlmostEqual(self.c.f_raw_holografica(), expected, places=6)

    def test_f_raw_holografica_range(self):
        """Holographic raw frequency must be between 90 and 120 Hz."""
        fr = self.c.f_raw_holografica()
        self.assertGreater(fr, 90.0)
        self.assertLess(fr, 120.0)

    def test_sin_pi_n(self):
        """sin_pi_n() must return sin(π/7)."""
        self.assertAlmostEqual(self.c.sin_pi_n(), math.sin(math.pi / 7), places=12)

    def test_cos_pi_n(self):
        """cos_pi_n() must return cos(π/7)."""
        self.assertAlmostEqual(self.c.cos_pi_n(), math.cos(math.pi / 7), places=12)

    def test_sin_2pi_n(self):
        """sin_2pi_n() must return sin(2π/7)."""
        self.assertAlmostEqual(
            self.c.sin_2pi_n(), math.sin(2.0 * math.pi / 7), places=12
        )

    def test_cos_2pi_n(self):
        """cos_2pi_n() must return cos(2π/7)."""
        self.assertAlmostEqual(
            self.c.cos_2pi_n(), math.cos(2.0 * math.pi / 7), places=12
        )

    def test_frozen(self):
        """ConstantesRutas must be immutable (frozen=True)."""
        with self.assertRaises((AttributeError, TypeError)):
            self.c.f0 = 999.0  # type: ignore[misc]


# ============================================================================
# TestRutaHolografica – Clase 2
# ============================================================================

class TestRutaHolografica(unittest.TestCase):
    """Tests for RutaHolografica (Route A)."""

    def setUp(self):
        self.ruta = RutaHolografica()

    def test_frecuencia_bruta_hz_range(self):
        """Raw holographic frequency must be between 90 and 120 Hz."""
        fr = self.ruta.frecuencia_bruta_hz()
        self.assertGreater(fr, 90.0)
        self.assertLess(fr, 120.0)

    def test_frecuencia_bruta_hz_formula(self):
        """f_raw = c/(2π·√(λ_p·R_dS))."""
        c = self.ruta.consts
        expected = c.c / (2.0 * math.pi * math.sqrt(c.lambda_p_m * c.r_ds_m))
        self.assertAlmostEqual(self.ruta.frecuencia_bruta_hz(), expected, places=6)

    def test_frecuencia_hz_equals_raw_over_n7(self):
        """f_A = f_raw / N₇."""
        f_raw = self.ruta.frecuencia_bruta_hz()
        n7 = self.ruta.consts.n7
        self.assertAlmostEqual(self.ruta.frecuencia_hz(), f_raw / n7, places=10)

    def test_frecuencia_hz_target_range(self):
        """Route A frequency must be between 38 and 44 Hz."""
        fa = self.ruta.frecuencia_hz()
        self.assertGreater(fa, 38.0)
        self.assertLess(fa, 44.0)

    def test_frecuencia_hz_close_to_riemann_t7(self):
        """f_A must be within 0.1 Hz of the 7th Riemann zero (≈ 40.9187)."""
        t7 = 40.918719012147495
        self.assertAlmostEqual(self.ruta.frecuencia_hz(), t7, delta=0.1)

    def test_frecuencia_hz_approx_target(self):
        """f_A must be within 1% of the stated target 40.91 Hz."""
        target = 40.91
        fa = self.ruta.frecuencia_hz()
        rel_error = abs(fa - target) / target
        self.assertLess(rel_error, 0.01)

    def test_escala_holografica_m(self):
        """Holographic scale must equal sqrt(λ_p · R_dS)."""
        c = self.ruta.consts
        expected = math.sqrt(c.lambda_p_m * c.r_ds_m)
        self.assertAlmostEqual(
            self.ruta.escala_holografica_m(), expected, places=5
        )

    def test_escala_holografica_order(self):
        """Holographic scale must be ~4.7e5 m (hundreds of km)."""
        escala = self.ruta.escala_holografica_m()
        self.assertGreater(escala, 1e5)
        self.assertLess(escala, 1e7)

    def test_factor_n7(self):
        """factor_n7() must equal 2.5."""
        self.assertAlmostEqual(self.ruta.factor_n7(), 2.5, places=10)

    def test_info_keys(self):
        """info() must return a dict with expected keys."""
        info = self.ruta.info()
        for key in ("nombre", "formula", "frecuencia_hz", "psi"):
            self.assertIn(key, info)

    def test_info_psi(self):
        """info() psi must equal 0.9469."""
        self.assertAlmostEqual(self.ruta.info()["psi"], 0.9469, places=4)

    def test_info_frecuencia_in_range(self):
        """info() frecuencia_hz must be in target range."""
        fa = self.ruta.info()["frecuencia_hz"]
        self.assertGreater(fa, 38.0)
        self.assertLess(fa, 44.0)

    def test_custom_consts(self):
        """RutaHolografica must accept custom ConstantesRutas."""
        c = ConstantesRutas(n7=2.0)
        ruta = RutaHolografica(consts=c)
        # With N₇=2.0, frequency should be higher than with N₇=2.5
        self.assertGreater(ruta.frecuencia_hz(), self.ruta.frecuencia_hz())


# ============================================================================
# TestRutaTopologica – Clase 3
# ============================================================================

class TestRutaTopologica(unittest.TestCase):
    """Tests for RutaTopologica (Route B — Chern-Simons C₇)."""

    def setUp(self):
        self.ruta = RutaTopologica()

    def test_factor_topologico_positive(self):
        """Topological factor must be positive."""
        self.assertGreater(self.ruta.factor_topologico(), 0.0)

    def test_factor_topologico_less_than_one(self):
        """Topological factor must be less than 1."""
        self.assertLess(self.ruta.factor_topologico(), 1.0)

    def test_factor_topologico_formula(self):
        """Factor = sin(2π/7) · (1 − cos(2π/7))."""
        s2 = math.sin(2.0 * math.pi / 7)
        c2 = math.cos(2.0 * math.pi / 7)
        expected = s2 * (1.0 - c2)
        self.assertAlmostEqual(
            self.ruta.factor_topologico(), expected, places=12
        )

    def test_t_energy_joules_positive(self):
        """Topological energy must be positive."""
        self.assertGreater(self.ruta.t_energy_joules(), 0.0)

    def test_t_energy_joules_formula(self):
        """t_energy = h · f_raw · sin(2π/7) · (1 − cos(2π/7))."""
        c = self.ruta.consts
        f_raw = c.f_raw_holografica()
        expected = c.h * f_raw * self.ruta.factor_topologico()
        self.assertAlmostEqual(
            self.ruta.t_energy_joules(), expected, places=15
        )

    def test_t_energy_order_of_magnitude(self):
        """t_energy must be of order ~2e-32 J."""
        t = self.ruta.t_energy_joules()
        self.assertGreater(t, 1.0e-33)
        self.assertLess(t, 1.0e-31)

    def test_frecuencia_hz_target_range(self):
        """Route B frequency must be between 48 and 54 Hz."""
        fb = self.ruta.frecuencia_hz()
        self.assertGreater(fb, 48.0)
        self.assertLess(fb, 54.0)

    def test_frecuencia_hz_approx_target(self):
        """f_B must be within 1% of the stated target 50.54 Hz."""
        target = 50.54
        fb = self.ruta.frecuencia_hz()
        rel_error = abs(fb - target) / target
        self.assertLess(rel_error, 0.01)

    def test_frecuencia_hz_formula(self):
        """f_B = GAP_FACTOR · t_energy / h."""
        c = self.ruta.consts
        expected = c.gap_factor * self.ruta.t_energy_joules() / c.h
        self.assertAlmostEqual(self.ruta.frecuencia_hz(), expected, places=8)

    def test_frecuencia_hz_por_factor(self):
        """frecuencia_hz_por_factor() must return (f_B, factor_topologico)."""
        fb, ft = self.ruta.frecuencia_hz_por_factor()
        self.assertAlmostEqual(fb, self.ruta.frecuencia_hz(), places=10)
        self.assertAlmostEqual(ft, self.ruta.factor_topologico(), places=12)

    def test_info_keys(self):
        """info() must contain expected keys."""
        info = self.ruta.info()
        for key in ("nombre", "formula", "factor_topologico", "t_energy_joules",
                    "gap_factor", "frecuencia_hz", "psi"):
            self.assertIn(key, info)

    def test_info_psi(self):
        """info() psi must equal 0.9819."""
        self.assertAlmostEqual(self.ruta.info()["psi"], 0.9819, places=4)

    def test_higher_than_route_a(self):
        """Route B frequency must be higher than Route A frequency."""
        ra = RutaHolografica()
        self.assertGreater(self.ruta.frecuencia_hz(), ra.frecuencia_hz())


# ============================================================================
# TestRutaMasaEfectiva – Clase 4
# ============================================================================

class TestRutaMasaEfectiva(unittest.TestCase):
    """Tests for RutaMasaEfectiva (Route C — effective mass)."""

    def setUp(self):
        self.ruta = RutaMasaEfectiva()

    def test_correccion_topologica_positive(self):
        """Topological mass correction must be positive."""
        self.assertGreater(self.ruta.correccion_topologica(), 0.0)

    def test_correccion_topologica_small(self):
        """Topological mass correction must be < 0.01 (a small fraction)."""
        self.assertLess(self.ruta.correccion_topologica(), 0.01)

    def test_correccion_topologica_formula(self):
        """Correction = sin⁷(π/7) · cos(π/7)."""
        sp = math.sin(math.pi / 7)
        cp = math.cos(math.pi / 7)
        expected = (sp ** 7) * cp
        self.assertAlmostEqual(
            self.ruta.correccion_topologica(), expected, places=12
        )

    def test_masa_canonica_kg_formula(self):
        """m₀ = h·F₀/c²."""
        c = self.ruta.consts
        expected = c.h * c.f0 / (c.c ** 2)
        self.assertAlmostEqual(
            self.ruta.masa_canonica_kg(), expected, places=15
        )

    def test_masa_canonica_kg_order(self):
        """Canonical mass must be ~1.04e-48 kg."""
        m0 = self.ruta.masa_canonica_kg()
        self.assertGreater(m0, 1.0e-49)
        self.assertLess(m0, 1.0e-47)

    def test_masa_efectiva_less_than_canonica(self):
        """Effective mass must be slightly less than canonical mass."""
        self.assertLess(self.ruta.masa_efectiva_kg(), self.ruta.masa_canonica_kg())

    def test_masa_efectiva_close_to_canonica(self):
        """Effective mass must be within 1% of canonical mass."""
        m_eff = self.ruta.masa_efectiva_kg()
        m0 = self.ruta.masa_canonica_kg()
        rel = abs(m_eff - m0) / m0
        self.assertLess(rel, 0.01)

    def test_masa_efectiva_formula(self):
        """m_eff = m₀ · (1 − sin⁷(π/7) · cos(π/7))."""
        m0 = self.ruta.masa_canonica_kg()
        corr = self.ruta.correccion_topologica()
        expected = m0 * (1.0 - corr)
        self.assertAlmostEqual(
            self.ruta.masa_efectiva_kg(), expected, places=15
        )

    def test_frecuencia_hz_target_range(self):
        """Route C frequency must be between 139 and 143 Hz."""
        fc = self.ruta.frecuencia_hz()
        self.assertGreater(fc, 139.0)
        self.assertLess(fc, 143.0)

    def test_frecuencia_hz_approx_target(self):
        """f_C must be within 0.5% of the stated target 141.34 Hz."""
        target = 141.34
        fc = self.ruta.frecuencia_hz()
        rel_error = abs(fc - target) / target
        self.assertLess(rel_error, 0.005)

    def test_frecuencia_hz_close_to_f0(self):
        """f_C must be within 0.5% of F₀ = 141.7001 Hz."""
        f0 = self.ruta.consts.f0
        fc = self.ruta.frecuencia_hz()
        rel_error = abs(fc - f0) / f0
        self.assertLess(rel_error, 0.005)

    def test_frecuencia_hz_formula(self):
        """f_C = m_eff · c² / h."""
        c = self.ruta.consts
        expected = self.ruta.masa_efectiva_kg() * (c.c ** 2) / c.h
        self.assertAlmostEqual(self.ruta.frecuencia_hz(), expected, places=8)

    def test_highest_frequency(self):
        """Route C frequency must be the highest of the three routes."""
        ra = RutaHolografica()
        rb = RutaTopologica()
        fc = self.ruta.frecuencia_hz()
        self.assertGreater(fc, ra.frecuencia_hz())
        self.assertGreater(fc, rb.frecuencia_hz())

    def test_info_keys(self):
        """info() must contain expected keys."""
        info = self.ruta.info()
        for key in ("nombre", "formula", "correccion_topologica",
                    "masa_canonica_kg", "masa_efectiva_kg",
                    "frecuencia_hz", "psi"):
            self.assertIn(key, info)

    def test_info_psi(self):
        """info() psi must equal 0.9993."""
        self.assertAlmostEqual(self.ruta.info()["psi"], 0.9993, places=4)


# ============================================================================
# TestCoherenciaConvergencia – Clase 5
# ============================================================================

class TestCoherenciaConvergencia(unittest.TestCase):
    """Tests for CoherenciaConvergencia."""

    def setUp(self):
        self.coh = CoherenciaConvergencia()

    def test_psi_individual_values(self):
        """psi_individual() must return (0.9469, 0.9819, 0.9993)."""
        pa, pb, pc = self.coh.psi_individual()
        self.assertAlmostEqual(pa, 0.9469, places=4)
        self.assertAlmostEqual(pb, 0.9819, places=4)
        self.assertAlmostEqual(pc, 0.9993, places=4)

    def test_psi_global_above_umbral(self):
        """Ψ_global must be ≥ 0.888."""
        self.assertGreaterEqual(self.coh.psi_global(), 0.888)

    def test_psi_global_is_harmonic_mean(self):
        """Ψ_global must equal the harmonic mean of Ψ_A, Ψ_B, Ψ_C."""
        pa, pb, pc = self.coh.psi_individual()
        expected = 3.0 / (1.0 / pa + 1.0 / pb + 1.0 / pc)
        self.assertAlmostEqual(self.coh.psi_global(), expected, places=10)

    def test_psi_global_bounded_by_individuals(self):
        """Harmonic mean must be between the minimum and maximum individual Ψ."""
        pa, pb, pc = self.coh.psi_individual()
        min_psi = min(pa, pb, pc)
        max_psi = max(pa, pb, pc)
        pg = self.coh.psi_global()
        self.assertGreaterEqual(pg, min_psi - 1e-9)
        self.assertLessEqual(pg, max_psi + 1e-9)

    def test_psi_global_range(self):
        """Ψ_global must be in (0, 1]."""
        pg = self.coh.psi_global()
        self.assertGreater(pg, 0.0)
        self.assertLessEqual(pg, 1.0)

    def test_validar_with_default_umbral(self):
        """validar() must return True with default threshold 0.888."""
        self.assertTrue(self.coh.validar())

    def test_validar_with_high_umbral_fails(self):
        """validar(0.999) must return False (global Ψ < 0.999)."""
        self.assertFalse(self.coh.validar(umbral=0.999))

    def test_validar_with_zero_umbral(self):
        """validar(0.0) must always return True."""
        self.assertTrue(self.coh.validar(umbral=0.0))

    def test_frecuencias_hz_range(self):
        """All three frequencies must be positive and in expected ranges."""
        fa, fb, fc = self.coh.frecuencias_hz()
        self.assertGreater(fa, 38.0)
        self.assertLess(fa, 44.0)
        self.assertGreater(fb, 48.0)
        self.assertLess(fb, 54.0)
        self.assertGreater(fc, 139.0)
        self.assertLess(fc, 143.0)

    def test_frecuencias_ordering(self):
        """Frequencies must satisfy f_A < f_B < f_C."""
        fa, fb, fc = self.coh.frecuencias_hz()
        self.assertLess(fa, fb)
        self.assertLess(fb, fc)

    def test_media_aritmetica_hz(self):
        """Arithmetic mean must equal (f_A + f_B + f_C)/3."""
        fa, fb, fc = self.coh.frecuencias_hz()
        expected = (fa + fb + fc) / 3.0
        self.assertAlmostEqual(self.coh.media_aritmetica_hz(), expected, places=10)

    def test_info_keys(self):
        """info() must contain expected keys."""
        info = self.coh.info()
        for key in ("frecuencias_hz", "psi_individual", "psi_global",
                    "umbral", "valido", "media_aritmetica_hz"):
            self.assertIn(key, info)

    def test_info_valido(self):
        """info() valido must be True."""
        self.assertTrue(self.coh.info()["valido"])

    def test_info_psi_individual_sub_dict(self):
        """info() psi_individual must have psi_A, psi_B, psi_C keys."""
        psi_dict = self.coh.info()["psi_individual"]
        self.assertIn("psi_A", psi_dict)
        self.assertIn("psi_B", psi_dict)
        self.assertIn("psi_C", psi_dict)


# ============================================================================
# TestResultadoRuta – Clase 6
# ============================================================================

class TestResultadoRuta(unittest.TestCase):
    """Tests for ResultadoRuta dataclass."""

    def setUp(self):
        self.resultado_a = ResultadoRuta(
            nombre="Ruta A",
            formula="c/(2π·√(λ_p·R_dS))/N₇",
            frecuencia_hz=40.91,
            frecuencia_objetivo_hz=40.91,
            psi=0.9469,
        )
        self.resultado_b = ResultadoRuta(
            nombre="Ruta B",
            formula="1,67·t_energy/H",
            frecuencia_hz=50.27,  # computed value
            frecuencia_objetivo_hz=50.54,
            psi=0.9819,
        )

    def test_error_relativo_zero_when_exact(self):
        """error_relativo must be 0 when frecuencia_hz == objetivo."""
        self.assertAlmostEqual(self.resultado_a.error_relativo, 0.0, places=10)

    def test_error_relativo_positive(self):
        """error_relativo must be positive when frequencies differ."""
        self.assertGreater(self.resultado_b.error_relativo, 0.0)

    def test_error_relativo_formula(self):
        """error_relativo must equal |f - f_obj| / f_obj."""
        expected = abs(50.27 - 50.54) / 50.54
        self.assertAlmostEqual(self.resultado_b.error_relativo, expected, places=10)

    def test_converge_true_when_exact(self):
        """converge must be True when error_relativo < 1%."""
        self.assertTrue(self.resultado_a.converge)

    def test_converge_true_for_route_b(self):
        """Route B result (0.54% error) must converge."""
        self.assertTrue(self.resultado_b.converge)

    def test_converge_false_when_large_error(self):
        """converge must be False when error > 1%."""
        bad = ResultadoRuta(
            nombre="Bad",
            formula="",
            frecuencia_hz=100.0,
            frecuencia_objetivo_hz=50.0,
            psi=0.9,
        )
        self.assertFalse(bad.converge)

    def test_psi_stored(self):
        """psi attribute must be stored correctly."""
        self.assertAlmostEqual(self.resultado_a.psi, 0.9469, places=4)

    def test_nombre_stored(self):
        """nombre attribute must be stored correctly."""
        self.assertEqual(self.resultado_a.nombre, "Ruta A")


# ============================================================================
# TestSistemaRutasConvergencia – Clase 7
# ============================================================================

class TestSistemaRutasConvergencia(unittest.TestCase):
    """Tests for SistemaRutasConvergencia orchestrator."""

    def setUp(self):
        self.sistema = SistemaRutasConvergencia()

    def test_ruta_a_initialized(self):
        """ruta_a must be a RutaHolografica instance."""
        self.assertIsInstance(self.sistema.ruta_a, RutaHolografica)

    def test_ruta_b_initialized(self):
        """ruta_b must be a RutaTopologica instance."""
        self.assertIsInstance(self.sistema.ruta_b, RutaTopologica)

    def test_ruta_c_initialized(self):
        """ruta_c must be a RutaMasaEfectiva instance."""
        self.assertIsInstance(self.sistema.ruta_c, RutaMasaEfectiva)

    def test_coherencia_initialized(self):
        """coherencia must be a CoherenciaConvergencia instance."""
        self.assertIsInstance(self.sistema.coherencia, CoherenciaConvergencia)

    def test_resultado_ruta_a(self):
        """resultado_ruta_a() must return a ResultadoRuta with correct data."""
        ra = self.sistema.resultado_ruta_a()
        self.assertIsInstance(ra, ResultadoRuta)
        self.assertAlmostEqual(ra.psi, 0.9469, places=4)
        self.assertGreater(ra.frecuencia_hz, 38.0)
        self.assertLess(ra.frecuencia_hz, 44.0)

    def test_resultado_ruta_b(self):
        """resultado_ruta_b() must return a ResultadoRuta with correct data."""
        rb = self.sistema.resultado_ruta_b()
        self.assertIsInstance(rb, ResultadoRuta)
        self.assertAlmostEqual(rb.psi, 0.9819, places=4)
        self.assertGreater(rb.frecuencia_hz, 48.0)
        self.assertLess(rb.frecuencia_hz, 54.0)

    def test_resultado_ruta_c(self):
        """resultado_ruta_c() must return a ResultadoRuta with correct data."""
        rc = self.sistema.resultado_ruta_c()
        self.assertIsInstance(rc, ResultadoRuta)
        self.assertAlmostEqual(rc.psi, 0.9993, places=4)
        self.assertGreater(rc.frecuencia_hz, 139.0)
        self.assertLess(rc.frecuencia_hz, 143.0)

    def test_all_routes_converge(self):
        """All three routes must have converge=True."""
        for resultado in (
            self.sistema.resultado_ruta_a(),
            self.sistema.resultado_ruta_b(),
            self.sistema.resultado_ruta_c(),
        ):
            self.assertTrue(resultado.converge, msg=f"{resultado.nombre} does not converge")

    def test_validar_default(self):
        """validar() must return True with default threshold."""
        self.assertTrue(self.sistema.validar())

    def test_validar_strict_fails(self):
        """validar(0.999) must return False."""
        self.assertFalse(self.sistema.validar(umbral=0.999))

    def test_reporte_completo_keys(self):
        """reporte_completo() must contain all expected top-level keys."""
        rep = self.sistema.reporte_completo()
        for key in ("sistema", "version", "rutas", "resultados",
                    "coherencia", "psi_global", "validacion",
                    "f0_objetivo_hz", "veredicto"):
            self.assertIn(key, rep)

    def test_reporte_completo_rutas_keys(self):
        """reporte_completo()['rutas'] must have keys A, B, C."""
        rutas = self.sistema.reporte_completo()["rutas"]
        self.assertIn("A", rutas)
        self.assertIn("B", rutas)
        self.assertIn("C", rutas)

    def test_reporte_completo_validacion(self):
        """reporte_completo()['validacion'] must be True."""
        self.assertTrue(self.sistema.reporte_completo()["validacion"])

    def test_reporte_completo_psi_global(self):
        """reporte_completo()['psi_global'] must be ≥ 0.888."""
        pg = self.sistema.reporte_completo()["psi_global"]
        self.assertGreaterEqual(pg, 0.888)

    def test_reporte_f0_objetivo(self):
        """f0_objetivo_hz must equal 141.7001 Hz."""
        f0 = self.sistema.reporte_completo()["f0_objetivo_hz"]
        self.assertAlmostEqual(f0, 141.7001, places=4)

    def test_sistema_version(self):
        """Version string must be set."""
        version = self.sistema.reporte_completo()["version"]
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


# ============================================================================
# TestResultadoConvergencia – Clase 8
# ============================================================================

class TestResultadoConvergencia(unittest.TestCase):
    """Tests for ResultadoConvergencia dataclass."""

    def _make_resultado(self, f_a=40.91, f_b=50.27, f_c=141.33,
                        psi_a=0.9469, psi_b=0.9819, psi_c=0.9993,
                        psi_g=0.9755, valido=True) -> ResultadoConvergencia:
        return ResultadoConvergencia(
            f_a_hz=f_a, f_b_hz=f_b, f_c_hz=f_c,
            psi_a=psi_a, psi_b=psi_b, psi_c=psi_c,
            psi_global=psi_g, valido=valido,
        )

    def test_valid_creation(self):
        """ResultadoConvergencia must be created without errors for valid inputs."""
        r = self._make_resultado()
        self.assertIsInstance(r, ResultadoConvergencia)

    def test_invalid_psi_global_zero_raises(self):
        """psi_global=0 must raise ValueError."""
        with self.assertRaises(ValueError):
            self._make_resultado(psi_g=0.0)

    def test_invalid_psi_global_above_one_raises(self):
        """psi_global > 1 must raise ValueError."""
        with self.assertRaises(ValueError):
            self._make_resultado(psi_g=1.001)

    def test_invalid_f_a_too_low_raises(self):
        """f_a_hz below range must raise ValueError."""
        with self.assertRaises(ValueError):
            self._make_resultado(f_a=10.0)

    def test_invalid_f_a_too_high_raises(self):
        """f_a_hz above range must raise ValueError."""
        with self.assertRaises(ValueError):
            self._make_resultado(f_a=100.0)

    def test_invalid_f_b_too_low_raises(self):
        """f_b_hz below range must raise ValueError."""
        with self.assertRaises(ValueError):
            self._make_resultado(f_b=30.0)

    def test_invalid_f_b_too_high_raises(self):
        """f_b_hz above range must raise ValueError."""
        with self.assertRaises(ValueError):
            self._make_resultado(f_b=80.0)

    def test_invalid_f_c_too_low_raises(self):
        """f_c_hz below range must raise ValueError."""
        with self.assertRaises(ValueError):
            self._make_resultado(f_c=100.0)

    def test_invalid_f_c_too_high_raises(self):
        """f_c_hz above range must raise ValueError."""
        with self.assertRaises(ValueError):
            self._make_resultado(f_c=200.0)

    def test_psi_global_stored(self):
        """psi_global must be stored correctly."""
        r = self._make_resultado(psi_g=0.9755)
        self.assertAlmostEqual(r.psi_global, 0.9755, places=4)

    def test_valido_stored(self):
        """valido flag must be stored correctly."""
        r = self._make_resultado(valido=True)
        self.assertTrue(r.valido)

    def test_frequencies_stored(self):
        """Frequency attributes must be stored correctly."""
        r = self._make_resultado()
        self.assertAlmostEqual(r.f_a_hz, 40.91, places=4)
        self.assertAlmostEqual(r.f_b_hz, 50.27, places=4)
        self.assertAlmostEqual(r.f_c_hz, 141.33, places=4)


# ============================================================================
# TestPublicAPI – rutas_convergencia_calcular
# ============================================================================

class TestPublicAPI(unittest.TestCase):
    """Tests for rutas_convergencia_calcular() public API."""

    @classmethod
    def setUpClass(cls):
        cls.result = rutas_convergencia_calcular()

    def test_returns_dict(self):
        """API must return a dict."""
        self.assertIsInstance(self.result, dict)

    def test_psi_global_above_umbral(self):
        """psi_global must be ≥ 0.888."""
        self.assertGreaterEqual(self.result["psi_global"], 0.888)

    def test_validacion_true(self):
        """validacion must be True."""
        self.assertTrue(self.result["validacion"])

    def test_ruta_a_frequency_range(self):
        """Route A frequency must be between 38 and 44 Hz."""
        fa = self.result["rutas"]["A"]["frecuencia_hz"]
        self.assertGreater(fa, 38.0)
        self.assertLess(fa, 44.0)

    def test_ruta_b_frequency_range(self):
        """Route B frequency must be between 48 and 54 Hz."""
        fb = self.result["rutas"]["B"]["frecuencia_hz"]
        self.assertGreater(fb, 48.0)
        self.assertLess(fb, 54.0)

    def test_ruta_c_frequency_range(self):
        """Route C frequency must be between 139 and 143 Hz."""
        fc = self.result["rutas"]["C"]["frecuencia_hz"]
        self.assertGreater(fc, 139.0)
        self.assertLess(fc, 143.0)

    def test_ruta_a_psi(self):
        """Route A psi must equal 0.9469."""
        self.assertAlmostEqual(self.result["rutas"]["A"]["psi"], 0.9469, places=4)

    def test_ruta_b_psi(self):
        """Route B psi must equal 0.9819."""
        self.assertAlmostEqual(self.result["rutas"]["B"]["psi"], 0.9819, places=4)

    def test_ruta_c_psi(self):
        """Route C psi must equal 0.9993."""
        self.assertAlmostEqual(self.result["rutas"]["C"]["psi"], 0.9993, places=4)

    def test_frequency_ordering(self):
        """Frequencies must satisfy f_A < f_B < f_C."""
        fa = self.result["rutas"]["A"]["frecuencia_hz"]
        fb = self.result["rutas"]["B"]["frecuencia_hz"]
        fc = self.result["rutas"]["C"]["frecuencia_hz"]
        self.assertLess(fa, fb)
        self.assertLess(fb, fc)

    def test_ruta_c_closest_to_f0(self):
        """Route C must be the closest to F₀ = 141.7001 Hz."""
        f0 = 141.7001
        fa = self.result["rutas"]["A"]["frecuencia_hz"]
        fb = self.result["rutas"]["B"]["frecuencia_hz"]
        fc = self.result["rutas"]["C"]["frecuencia_hz"]
        self.assertLess(abs(fc - f0), abs(fa - f0))
        self.assertLess(abs(fc - f0), abs(fb - f0))

    def test_psi_c_is_highest(self):
        """Ψ_C must be the highest individual coherence."""
        pa = self.result["rutas"]["A"]["psi"]
        pb = self.result["rutas"]["B"]["psi"]
        pc = self.result["rutas"]["C"]["psi"]
        self.assertGreater(pc, pb)
        self.assertGreater(pc, pa)

    def test_coherencia_subdict(self):
        """'coherencia' sub-dict must be present and contain psi_global."""
        coh = self.result["coherencia"]
        self.assertIn("psi_global", coh)
        self.assertGreaterEqual(coh["psi_global"], 0.888)

    def test_sistema_name(self):
        """'sistema' must contain 'Rutas de Convergencia'."""
        self.assertIn("Rutas de Convergencia", self.result["sistema"])

    def test_f0_objetivo_hz(self):
        """f0_objetivo_hz must be 141.7001 Hz."""
        self.assertAlmostEqual(self.result["f0_objetivo_hz"], 141.7001, places=4)

    def test_veredicto_present(self):
        """'veredicto' must be a non-empty string."""
        veredicto = self.result["veredicto"]
        self.assertIsInstance(veredicto, str)
        self.assertTrue(len(veredicto) > 0)

    def test_resultados_converge_flags(self):
        """All three routes must report converge=True."""
        resultados = self.result["resultados"]
        for ruta_key in ("ruta_A", "ruta_B", "ruta_C"):
            self.assertTrue(
                resultados[ruta_key]["converge"],
                msg=f"{ruta_key} does not converge",
            )

    def test_idempotent(self):
        """Calling the API twice must return identical psi_global."""
        r2 = rutas_convergencia_calcular()
        self.assertAlmostEqual(
            self.result["psi_global"], r2["psi_global"], places=10
        )


# ============================================================================
# TestIntegration – cross-class invariants
# ============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests that verify cross-class invariants."""

    def test_consts_shared_across_rutas(self):
        """All routes created with the same ConstantesRutas must share values."""
        c = ConstantesRutas()
        ra = RutaHolografica(consts=c)
        rb = RutaTopologica(consts=c)
        rc = RutaMasaEfectiva(consts=c)
        self.assertIs(ra.consts, rb.consts)
        self.assertIs(rb.consts, rc.consts)

    def test_sistema_frecuencias_match_rutas(self):
        """Sistema frequencies must match individual route frequencies."""
        s = SistemaRutasConvergencia()
        self.assertAlmostEqual(
            s.resultado_ruta_a().frecuencia_hz,
            s.ruta_a.frecuencia_hz(),
            places=10,
        )
        self.assertAlmostEqual(
            s.resultado_ruta_b().frecuencia_hz,
            s.ruta_b.frecuencia_hz(),
            places=10,
        )
        self.assertAlmostEqual(
            s.resultado_ruta_c().frecuencia_hz,
            s.ruta_c.frecuencia_hz(),
            places=10,
        )

    def test_coherencia_psi_global_matches_sistema(self):
        """Sistema psi_global must match CoherenciaConvergencia.psi_global()."""
        s = SistemaRutasConvergencia()
        self.assertAlmostEqual(
            s.coherencia.psi_global(),
            s.reporte_completo()["psi_global"],
            places=10,
        )

    def test_route_c_frequency_close_to_f0(self):
        """Route C must converge to within 0.3% of F₀."""
        f0 = 141.7001
        s = SistemaRutasConvergencia()
        fc = s.ruta_c.frecuencia_hz()
        rel = abs(fc - f0) / f0
        self.assertLess(rel, 0.003)

    def test_route_a_close_to_riemann_t7(self):
        """Route A must converge to within 0.05% of 7th Riemann zero."""
        t7 = 40.918719012147495
        s = SistemaRutasConvergencia()
        fa = s.ruta_a.frecuencia_hz()
        rel = abs(fa - t7) / t7
        self.assertLess(rel, 0.0005)

    def test_holographic_scale_geometric_mean(self):
        """Holographic scale must be geometric mean of λ_p and R_dS."""
        c = ConstantesRutas()
        geo_mean = math.sqrt(c.lambda_p_m * c.r_ds_m)
        ra = RutaHolografica(consts=c)
        self.assertAlmostEqual(ra.escala_holografica_m(), geo_mean, places=6)

    def test_topological_energy_is_not_calibrated_to_f0(self):
        """Route B's t_energy must NOT correspond to the full F₀ gap."""
        rb = RutaTopologica()
        c = rb.consts
        # If calibrated to F₀: t_energy = h * f0 / gap_factor
        t_calibrated = c.h * c.f0 / c.gap_factor
        t_actual = rb.t_energy_joules()
        # The topological energy must be significantly smaller
        self.assertLess(t_actual, t_calibrated)

    def test_global_psi_between_min_and_arithmetic_mean(self):
        """Harmonic mean (Ψ_global) must be ≤ arithmetic mean of individual Ψ."""
        coh = CoherenciaConvergencia()
        pa, pb, pc = coh.psi_individual()
        arith = (pa + pb + pc) / 3.0
        harm = coh.psi_global()
        # Harmonic mean ≤ arithmetic mean (AM-HM inequality)
        self.assertLessEqual(harm, arith + 1e-10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
