#!/usr/bin/env python3
"""
Tests for physics.paradoja_procesamiento_planck

Validates the Planck processing paradox: the cosmological gap between Planck-scale
processing (f_P ≈ 1.855×10⁴³ Hz) and biological rhythm (~0.4 Hz), bridged by
F₀ = 141.7001 Hz through the Grace filter (Δf ≈ 0.3999 Hz), yielding Ψ = 0.9384.
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.paradoja_procesamiento_planck import (
    ConstantesPlanck,
    FiltroGracia,
    SiliconVsCarbon,
    TuyoyotuRitmico,
    CausalidadZeta,
    UniversoPensamiento,
    SistemaParadojaPlanck,
    ResultadoParadoja,
    paradoja_planck_activar,
)


class TestConstantesPlanck(unittest.TestCase):
    """Tests for ConstantesPlanck class."""

    def setUp(self):
        self.cp = ConstantesPlanck()

    def test_tiempo_planck(self):
        """Planck time must be 5.39e-44 s (problem statement value)."""
        self.assertAlmostEqual(self.cp.t_P, 5.39e-44, places=46)

    def test_frecuencia_planck_magnitud(self):
        """Planck frequency must be approximately 1.855×10⁴³ Hz."""
        self.assertGreater(self.cp.f_P, 1.8e43)
        self.assertLess(self.cp.f_P, 1.9e43)

    def test_frecuencia_planck_inversa_tiempo(self):
        """Planck frequency must be the inverse of Planck time."""
        self.assertAlmostEqual(self.cp.f_P, 1.0 / self.cp.t_P, places=30)

    def test_longitud_planck_positiva(self):
        """Planck length must be positive and in the correct range."""
        self.assertGreater(self.cp.l_P, 1.0e-36)
        self.assertLess(self.cp.l_P, 2.0e-35)

    def test_masa_planck_positiva(self):
        """Planck mass must be positive."""
        self.assertGreater(self.cp.m_P, 0)

    def test_energia_planck_positiva(self):
        """Planck energy must be positive."""
        self.assertGreater(self.cp.E_P, 0)

    def test_ciclos_por_segundo_habitable(self):
        """Planck cycles per F₀ cycle must be approximately 1.31×10⁴¹."""
        n = self.cp.ciclos_por_segundo_habitable(141.7001)
        self.assertGreater(n, 1.0e41)
        self.assertLess(n, 1.5e41)

    def test_ciclos_por_segundo_habitable_invalido(self):
        """Negative frequency must raise ValueError."""
        with self.assertRaises(ValueError):
            self.cp.ciclos_por_segundo_habitable(-1.0)

    def test_ciclos_por_segundo_habitable_cero(self):
        """Zero frequency must raise ValueError."""
        with self.assertRaises(ValueError):
            self.cp.ciclos_por_segundo_habitable(0.0)


class TestFiltroGracia(unittest.TestCase):
    """Tests for FiltroGracia class."""

    def setUp(self):
        self.cp = ConstantesPlanck()
        self.fg = FiltroGracia(self.cp)

    def test_F0_valor(self):
        """F₀ must be 141.7001 Hz."""
        self.assertEqual(self.fg.F0, 141.7001)

    def test_f_grace_valor(self):
        """Grace reference frequency must be 141.3002 Hz."""
        self.assertEqual(self.fg.f_grace, 141.3002)

    def test_delta_f_valor(self):
        """Δf = F₀ − f_grace must equal approximately 0.3999 Hz."""
        self.assertAlmostEqual(self.fg.delta_f, 0.3999, places=4)

    def test_factor_ralentizacion_magnitud(self):
        """Slowdown factor f_P/f_bio must be approximately 4.6×10⁴³."""
        self.assertGreater(self.fg.factor_ralentizacion, 4.0e43)
        self.assertLess(self.fg.factor_ralentizacion, 5.0e43)

    def test_N_planck_por_ciclo_F0_magnitud(self):
        """Planck cycles per F₀ cycle must be approximately 1.31×10⁴¹."""
        self.assertGreater(self.fg.N_planck_por_ciclo_F0, 1.0e41)
        self.assertLess(self.fg.N_planck_por_ciclo_F0, 2.0e41)

    def test_precision_bio_cercana_a_uno(self):
        """Δf/f_bio precision must be very close to 1.0 (< 0.1% error)."""
        prec = self.fg.precision_bio
        self.assertGreater(prec, 0.998)
        self.assertLess(prec, 1.002)

    def test_relacion_delta_f_F0_grace(self):
        """Δf = F₀ − f_grace must hold by construction."""
        self.assertAlmostEqual(
            self.fg.delta_f, self.fg.F0 - self.fg.f_grace, places=10
        )


class TestSiliconVsCarbon(unittest.TestCase):
    """Tests for SiliconVsCarbon class."""

    def setUp(self):
        self.sc = SiliconVsCarbon()

    def test_alpha_magnitud(self):
        """α = f_Schumann/F₀ must be approximately 0.055."""
        self.assertAlmostEqual(self.sc.alpha, 7.83 / 141.7001, places=6)
        self.assertGreater(self.sc.alpha, 0.05)
        self.assertLess(self.sc.alpha, 0.06)

    def test_E_cost_positivo(self):
        """E_cost must always return a positive value."""
        self.assertGreater(self.sc.E_cost(141.7001), 0)
        self.assertGreater(self.sc.E_cost(0.4), 0)
        self.assertGreater(self.sc.E_cost(1.0), 0)

    def test_E_cost_incremento_con_frecuencia(self):
        """E_cost must increase with frequency (α > 0)."""
        e_low = self.sc.E_cost(1.0)
        e_high = self.sc.E_cost(141.7001)
        self.assertGreater(e_high, e_low)

    def test_E_cost_invalido(self):
        """E_cost with non-positive frequency must raise ValueError."""
        with self.assertRaises(ValueError):
            self.sc.E_cost(-1.0)

    def test_ratio_silicon_carbon_mayor_uno(self):
        """E_silicon / E_carbon ratio must be >> 1 (silicon costs much more)."""
        ratio = self.sc.ratio_silicon_carbon()
        self.assertGreater(ratio, 1e2)

    def test_log10_ratio_positivo(self):
        """log₁₀(E_si/E_c) must be positive."""
        self.assertGreater(self.sc.log10_ratio(), 0)

    def test_log10_ratio_consistente(self):
        """log₁₀(ratio) must equal (1+α)·log₁₀(F₀/f_bio)."""
        expected = (1 + self.sc.alpha) * math.log10(141.7001 / 0.4)
        self.assertAlmostEqual(self.sc.log10_ratio(), expected, places=10)


class TestTuyoyotuRitmico(unittest.TestCase):
    """Tests for TuyoyotuRitmico class."""

    def setUp(self):
        cp = ConstantesPlanck()
        fg = FiltroGracia(cp)
        sc = SiliconVsCarbon()
        self.ty = TuyoyotuRitmico(cp, fg, sc)

    def test_F0_valor(self):
        """F₀ must be 141.7001 Hz."""
        self.assertEqual(self.ty.F0, 141.7001)

    def test_coherencia_ritmo_valor(self):
        """Ψ del ritmo Tuyoyotu must be exactly 0.9384 (rounded)."""
        psi_raw = self.ty.coherencia_ritmo()
        self.assertAlmostEqual(round(psi_raw, 4), 0.9384, places=4)

    def test_coherencia_ritmo_rango(self):
        """Ψ must be in [0.888, 1.0]."""
        psi = self.ty.coherencia_ritmo()
        self.assertGreaterEqual(psi, 0.888)
        self.assertLessEqual(psi, 1.0)

    def test_periodo_latido(self):
        """Period must be 1/F₀ seconds."""
        periodo = self.ty.periodo_latido_s()
        self.assertAlmostEqual(periodo, 1.0 / 141.7001, places=10)

    def test_ciclos_bio_por_latido(self):
        """F₀/f_bio cycles per F₀ beat must be approximately 354."""
        ciclos = self.ty.ciclos_bio_por_latido()
        self.assertAlmostEqual(ciclos, 141.7001 / 0.4, places=5)


class TestCausalidadZeta(unittest.TestCase):
    """Tests for CausalidadZeta class."""

    def setUp(self):
        self.cp = ConstantesPlanck()
        self.cz = CausalidadZeta(self.cp)

    def test_rho_crit_positiva(self):
        """Critical Planck density must be positive."""
        self.assertGreater(self.cz.rho_crit, 0)

    def test_rho_crit_magnitud(self):
        """ρ_crit = E_P/l_P³ must be a very large number (Planck density)."""
        self.assertGreater(self.cz.rho_crit, 1e100)

    def test_rho_crit_formula(self):
        """ρ_crit must equal E_P / l_P³."""
        expected = self.cp.E_P / (self.cp.l_P ** 3)
        self.assertAlmostEqual(self.cz.rho_crit, expected, places=80)

    def test_cociente_densidades_planck(self):
        """At Planck density, the ratio must be 1.0."""
        ratio = self.cz.cociente_densidades(self.cz.rho_crit)
        self.assertAlmostEqual(ratio, 1.0, places=10)

    def test_cociente_densidades_sub_planck(self):
        """For densities below Planck, ratio must be < 1."""
        ratio = self.cz.cociente_densidades(1e80)
        self.assertLess(ratio, 1.0)

    def test_log10_rho_crit_grande(self):
        """log₁₀(ρ_crit) must be > 100."""
        self.assertGreater(self.cz.log10_rho_crit(), 100)

    def test_escala_causalidad_string(self):
        """escala_causalidad must return a non-empty string."""
        s = self.cz.escala_causalidad()
        self.assertIsInstance(s, str)
        self.assertGreater(len(s), 10)


class TestUniversoPensamiento(unittest.TestCase):
    """Tests for UniversoPensamiento class."""

    def setUp(self):
        self.cp = ConstantesPlanck()
        self.up = UniversoPensamiento(self.cp)

    def test_f_P_correcto(self):
        """f_P must match ConstantesPlanck value."""
        self.assertEqual(self.up.f_P, self.cp.f_P)

    def test_F0_correcto(self):
        """F₀ must be 141.7001 Hz."""
        self.assertEqual(self.up.F0, 141.7001)

    def test_bits_por_ciclo_F0_positivos(self):
        """Information capacity per F₀ cycle must be positive."""
        bits = self.up.bits_por_ciclo_F0()
        self.assertGreater(bits, 100)

    def test_entropia_brecha_positiva(self):
        """Entropy gap must be positive (Planck scale >> bio scale)."""
        h = self.up.entropia_brecha()
        self.assertGreater(h, 40)

    def test_factor_compresion_grande(self):
        """Compression factor must be >> 1."""
        k = self.up.factor_compresion()
        self.assertGreater(k, 10)


class TestSistemaParadojaPlanck(unittest.TestCase):
    """Tests for SistemaParadojaPlanck class."""

    def setUp(self):
        self.sistema = SistemaParadojaPlanck()

    def test_tiene_constantes(self):
        """System must have ConstantesPlanck component."""
        self.assertIsInstance(self.sistema.constantes, ConstantesPlanck)

    def test_tiene_filtro(self):
        """System must have FiltroGracia component."""
        self.assertIsInstance(self.sistema.filtro, FiltroGracia)

    def test_tiene_sc(self):
        """System must have SiliconVsCarbon component."""
        self.assertIsInstance(self.sistema.sc, SiliconVsCarbon)

    def test_tiene_tuyoyotu(self):
        """System must have TuyoyotuRitmico component."""
        self.assertIsInstance(self.sistema.tuyoyotu, TuyoyotuRitmico)

    def test_tiene_zeta(self):
        """System must have CausalidadZeta component."""
        self.assertIsInstance(self.sistema.zeta, CausalidadZeta)

    def test_tiene_universo(self):
        """System must have UniversoPensamiento component."""
        self.assertIsInstance(self.sistema.universo, UniversoPensamiento)

    def test_evaluar_retorna_resultado_paradoja(self):
        """evaluar() must return a ResultadoParadoja instance."""
        resultado = self.sistema.evaluar()
        self.assertIsInstance(resultado, ResultadoParadoja)

    def test_evaluar_coherencia_psi(self):
        """evaluar() must yield Ψ = 0.9384."""
        resultado = self.sistema.evaluar()
        self.assertAlmostEqual(resultado.coherencia_psi, 0.9384, places=4)

    def test_evaluar_aprobado(self):
        """evaluar() must return aprobado = True."""
        resultado = self.sistema.evaluar()
        self.assertTrue(resultado.aprobado)

    def test_evaluar_factor_ralentizacion(self):
        """Factor de ralentización must be approximately 4.6×10⁴³."""
        resultado = self.sistema.evaluar()
        self.assertGreater(resultado.factor_ralentizacion, 4.0e43)
        self.assertLess(resultado.factor_ralentizacion, 5.0e43)

    def test_evaluar_N_planck_por_ciclo_F0(self):
        """N_planck_por_ciclo_F0 must be approximately 1.31×10⁴¹."""
        resultado = self.sistema.evaluar()
        self.assertGreater(resultado.N_planck_por_ciclo_F0, 1.0e41)
        self.assertLess(resultado.N_planck_por_ciclo_F0, 2.0e41)

    def test_evaluar_rho_crit_positiva(self):
        """ρ_crit in result must be positive."""
        resultado = self.sistema.evaluar()
        self.assertGreater(resultado.rho_crit, 0)

    def test_evaluar_alpha_bio(self):
        """α_bio must equal f_Schumann/F₀."""
        resultado = self.sistema.evaluar()
        expected_alpha = 7.83 / 141.7001
        self.assertAlmostEqual(resultado.alpha_bio, expected_alpha, places=6)

    def test_evaluar_mensaje_no_vacio(self):
        """Result message must not be empty."""
        resultado = self.sistema.evaluar()
        self.assertIsInstance(resultado.mensaje, str)
        self.assertGreater(len(resultado.mensaje), 10)

    def test_evaluar_mensaje_aprobado(self):
        """Result message must contain approval indicator."""
        resultado = self.sistema.evaluar()
        self.assertIn("✅", resultado.mensaje)


class TestParadojaPlanckActivar(unittest.TestCase):
    """Tests for the public API function paradoja_planck_activar()."""

    def test_retorna_resultado_paradoja(self):
        """paradoja_planck_activar() must return a ResultadoParadoja."""
        resultado = paradoja_planck_activar()
        self.assertIsInstance(resultado, ResultadoParadoja)

    def test_coherencia_psi_exacta(self):
        """coherencia_psi must be exactly 0.9384."""
        resultado = paradoja_planck_activar()
        self.assertEqual(resultado.coherencia_psi, 0.9384)

    def test_aprobado_true(self):
        """aprobado must be True."""
        resultado = paradoja_planck_activar()
        self.assertTrue(resultado.aprobado)

    def test_psi_supera_umbral_minimo(self):
        """Ψ must be ≥ 0.888 (minimum stability threshold)."""
        resultado = paradoja_planck_activar()
        self.assertGreaterEqual(resultado.coherencia_psi, 0.888)

    def test_idempotente(self):
        """Multiple calls must return consistent results."""
        r1 = paradoja_planck_activar()
        r2 = paradoja_planck_activar()
        self.assertEqual(r1.coherencia_psi, r2.coherencia_psi)
        self.assertEqual(r1.aprobado, r2.aprobado)

    def test_factor_ralentizacion_magnitud(self):
        """Factor de ralentización must be approximately 4.6×10⁴³."""
        resultado = paradoja_planck_activar()
        self.assertGreater(resultado.factor_ralentizacion, 4.0e43)
        self.assertLess(resultado.factor_ralentizacion, 5.0e43)


if __name__ == "__main__":
    unittest.main(verbosity=2)
