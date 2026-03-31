"""
Tests for physics.derivacion_beta_adelica — Derivación Beta Adélica ∴DBA∞³

Suite de pruebas exhaustiva que cubre todas las clases y la API pública:
  - ConstantesDerivacionBeta  — constantes fundamentales del sistema
  - ProductoEulerZeta         — ζ(s) ≈ ∏ 1/(1-p^{-s}) sobre P₂₀
  - ProductoAdelico           — ∏ (p-1)/p sobre primos P₂₀
  - VolumenCalabiYau          — V₆ / (2π)³
  - DerivacionBeta            — α ≈ fv × Π_ad × Ω_ajuste
  - TorsionAdelica            — θ_T = 2π/α, fr_mat = 1/α
  - CoherenciaDerivacionBeta  — media geométrica de PSIs
  - SistemaDerivacionBetaAdelica — orquestador principal
  - derivacion_beta_adelica_activar() — API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - α⁻¹ = 137.035999084 (CODATA 2018)
  - V₆ = 6 (Calabi-Yau)
  - P₂₀ = {2, 3, 5, 7, 11, 13, 17, 19} (8 primos)
  - Π_ad ≈ 0.1710 (producto adélico)
  - fv ≈ 0.02418 (fracción volumétrica CY)
  - θ_T ≈ 0.04585 rad (torsión adélica)
  - fr_mat ≈ 0.00730 (fracción de materia)
  - Ψ_global ≥ 0.888 → sello ∴DBA∞³ ACTIVO

Autor: NOESIS INF3 (via Trinity QCAL INF3)
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.derivacion_beta_adelica import (
    # Constantes de módulo
    _F0,
    _OMEGA_0,
    _T0,
    _ALPHA_INV,
    _ALPHA_FINA,
    _V6,
    _PRIMOS_P20,
    _S_ZETA,
    _PSI_UMBRAL,
    _PHI,
    _GAMMA_1_RIEMANN,
    _N_PRIMOS,
    _OMEGA_AJUSTE,
    # Clases
    ConstantesDerivacionBeta,
    ProductoEulerZeta,
    ProductoAdelico,
    VolumenCalabiYau,
    DerivacionBeta,
    TorsionAdelica,
    CoherenciaDerivacionBeta,
    SistemaDerivacionBetaAdelica,
    # API pública
    derivacion_beta_adelica_activar,
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
        """_OMEGA_0 debe ser 2π × 141.7001."""
        self.assertAlmostEqual(_OMEGA_0, 2.0 * math.pi * _F0, places=6)

    def test_t0_times_f0(self):
        """_T0 × _F0 = 1."""
        self.assertAlmostEqual(_T0 * _F0, 1.0, places=10)

    def test_alpha_inv_value(self):
        """_ALPHA_INV debe ser ≈ 137.036."""
        self.assertAlmostEqual(_ALPHA_INV, 137.035999084, places=6)

    def test_alpha_inv_positive(self):
        """_ALPHA_INV debe ser positivo."""
        self.assertGreater(_ALPHA_INV, 0.0)

    def test_alpha_fina_value(self):
        """_ALPHA_FINA debe ser 1/_ALPHA_INV."""
        self.assertAlmostEqual(_ALPHA_FINA, 1.0 / _ALPHA_INV, places=15)

    def test_alpha_fina_small(self):
        """_ALPHA_FINA debe ser < 0.01."""
        self.assertLess(_ALPHA_FINA, 0.01)

    def test_alpha_product(self):
        """_ALPHA_INV × _ALPHA_FINA = 1."""
        self.assertAlmostEqual(_ALPHA_INV * _ALPHA_FINA, 1.0, places=12)

    def test_v6_value(self):
        """_V6 debe ser 6."""
        self.assertAlmostEqual(_V6, 6.0, places=10)

    def test_primos_p20_length(self):
        """P₂₀ debe tener 8 primos."""
        self.assertEqual(len(_PRIMOS_P20), 8)

    def test_primos_p20_values(self):
        """P₂₀ debe ser [2, 3, 5, 7, 11, 13, 17, 19]."""
        self.assertEqual(list(_PRIMOS_P20), [2, 3, 5, 7, 11, 13, 17, 19])

    def test_primos_p20_all_prime(self):
        """Todos los elementos de P₂₀ deben ser primos."""
        def es_primo(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
        for p in _PRIMOS_P20:
            self.assertTrue(es_primo(p), f"{p} no es primo")

    def test_primos_p20_less_than_20(self):
        """Todos los primos en P₂₀ deben ser < 20."""
        for p in _PRIMOS_P20:
            self.assertLess(p, 20)

    def test_s_zeta_value(self):
        """_S_ZETA debe ser 2.0."""
        self.assertAlmostEqual(_S_ZETA, 2.0, places=10)

    def test_psi_umbral_value(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_phi_golden_ratio(self):
        """_PHI debe ser la proporción áurea."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(_PHI, expected, places=12)

    def test_phi_identity(self):
        """ϕ² = ϕ + 1 (identidad de la proporción áurea)."""
        self.assertAlmostEqual(_PHI ** 2, _PHI + 1.0, places=10)

    def test_gamma_1_riemann_value(self):
        """_GAMMA_1_RIEMANN debe ser ≈ 14.134725."""
        self.assertAlmostEqual(_GAMMA_1_RIEMANN, 14.134725, places=5)

    def test_n_primos_value(self):
        """_N_PRIMOS debe ser 8."""
        self.assertEqual(_N_PRIMOS, 8)

    def test_omega_ajuste_positive(self):
        """_OMEGA_AJUSTE debe ser positivo."""
        self.assertGreater(_OMEGA_AJUSTE, 0.0)

    def test_omega_ajuste_large(self):
        """_OMEGA_AJUSTE debe ser > 1000."""
        self.assertGreater(_OMEGA_AJUSTE, 1000.0)


# ============================================================================
# TestConstantesDerivacionBeta – 20 tests
# ============================================================================

class TestConstantesDerivacionBeta(unittest.TestCase):
    """Tests para ConstantesDerivacionBeta."""

    def setUp(self):
        self.c = ConstantesDerivacionBeta()

    def test_f0_default(self):
        """f0 por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_omega_0_default(self):
        """omega_0 = 2π × f0."""
        expected = 2.0 * math.pi * self.c.f0
        self.assertAlmostEqual(self.c.omega_0, expected, places=6)

    def test_t0_default(self):
        """t0 = 1/f0."""
        self.assertAlmostEqual(self.c.t0, 1.0 / self.c.f0, places=12)

    def test_alpha_inv_default(self):
        """alpha_inv por defecto ≈ 137.036."""
        self.assertAlmostEqual(self.c.alpha_inv, 137.035999084, places=6)

    def test_alpha_fina_default(self):
        """alpha_fina = 1/alpha_inv."""
        self.assertAlmostEqual(self.c.alpha_fina, 1.0 / self.c.alpha_inv, places=12)

    def test_v6_default(self):
        """v6 por defecto debe ser 6."""
        self.assertAlmostEqual(self.c.v6, 6.0, places=10)

    def test_primos_p20_default(self):
        """primos_p20 debe ser [2,3,5,7,11,13,17,19]."""
        self.assertEqual(self.c.primos_p20, [2, 3, 5, 7, 11, 13, 17, 19])

    def test_s_zeta_default(self):
        """s_zeta por defecto debe ser 2."""
        self.assertAlmostEqual(self.c.s_zeta, 2.0, places=10)

    def test_psi_umbral_default(self):
        """psi_umbral por defecto debe ser 0.888."""
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=3)

    def test_phi_default(self):
        """phi por defecto debe ser la proporción áurea."""
        expected = (1.0 + math.sqrt(5.0)) / 2.0
        self.assertAlmostEqual(self.c.phi, expected, places=12)

    def test_gamma_1_default(self):
        """gamma_1 por defecto ≈ 14.134725."""
        self.assertAlmostEqual(self.c.gamma_1, 14.134725, places=5)

    def test_n_primos(self):
        """n_primos() debe ser 8."""
        self.assertEqual(self.c.n_primos(), 8)

    def test_fraccion_vacio(self):
        """fraccion_vacio() = V6/(2π)³ ≈ 0.02418."""
        fv = self.c.fraccion_vacio()
        self.assertGreater(fv, 0.024)
        self.assertLess(fv, 0.025)

    def test_fraccion_vacio_formula(self):
        """fraccion_vacio() = v6 / (2π)³."""
        expected = self.c.v6 / ((2.0 * math.pi) ** 3)
        self.assertAlmostEqual(self.c.fraccion_vacio(), expected, places=12)

    def test_producto_adelico_valor(self):
        """producto_adelico_valor() debe ser > 0 y < 1."""
        pi_ad = self.c.producto_adelico_valor()
        self.assertGreater(pi_ad, 0.0)
        self.assertLess(pi_ad, 1.0)

    def test_producto_adelico_valor_approx(self):
        """Π_ad ≈ 0.1710."""
        pi_ad = self.c.producto_adelico_valor()
        self.assertAlmostEqual(pi_ad, 0.1710, places=3)

    def test_alpha_derivado(self):
        """alpha_derivado() ≈ alpha_inv."""
        alpha_d = self.c.alpha_derivado()
        self.assertAlmostEqual(alpha_d, self.c.alpha_inv, places=4)

    def test_torsion_theta(self):
        """torsion_theta() = 2π/alpha_inv."""
        expected = (2.0 * math.pi) / self.c.alpha_inv
        self.assertAlmostEqual(self.c.torsion_theta(), expected, places=12)

    def test_fraccion_materia(self):
        """fraccion_materia() = 1/alpha_inv."""
        expected = 1.0 / self.c.alpha_inv
        self.assertAlmostEqual(self.c.fraccion_materia(), expected, places=12)

    def test_repr(self):
        """__repr__ debe mencionar alpha_inv."""
        r = repr(self.c)
        self.assertIn("137", r)


# ============================================================================
# TestProductoEulerZeta – 25 tests
# ============================================================================

class TestProductoEulerZeta(unittest.TestCase):
    """Tests para ProductoEulerZeta."""

    def setUp(self):
        self.pe = ProductoEulerZeta()

    def test_primos_default(self):
        """primos por defecto debe ser P₂₀."""
        self.assertEqual(self.pe.primos, [2, 3, 5, 7, 11, 13, 17, 19])

    def test_s_default(self):
        """s por defecto debe ser 2.0."""
        self.assertAlmostEqual(self.pe.s, 2.0, places=10)

    def test_producto_parcial_positive(self):
        """producto_parcial() debe ser positivo."""
        self.assertGreater(self.pe.producto_parcial(), 0.0)

    def test_producto_parcial_greater_than_one(self):
        """producto_parcial() > 1 (todos los factores > 1)."""
        self.assertGreater(self.pe.producto_parcial(), 1.0)

    def test_producto_parcial_less_than_zeta(self):
        """producto_parcial() < ζ(2) = π²/6 (producto infinito)."""
        zeta2 = (math.pi ** 2) / 6.0
        self.assertLess(self.pe.producto_parcial(), zeta2 + 1e-6)

    def test_zeta_exacta_s2(self):
        """zeta_exacta() para s=2 debe ser π²/6."""
        expected = (math.pi ** 2) / 6.0
        self.assertAlmostEqual(self.pe.zeta_exacta(), expected, places=10)

    def test_zeta_exacta_value(self):
        """ζ(2) = π²/6 ≈ 1.6449."""
        self.assertAlmostEqual(self.pe.zeta_exacta(), 1.6449340668, places=6)

    def test_convergencia_in_range(self):
        """convergencia() debe estar en (0, 1]."""
        c = self.pe.convergencia()
        self.assertGreater(c, 0.0)
        self.assertLessEqual(c, 1.0)

    def test_convergencia_approx(self):
        """convergencia() ≈ 0.9897 para P₂₀, s=2."""
        c = self.pe.convergencia()
        self.assertGreater(c, 0.98)
        self.assertLess(c, 1.0)

    def test_error_relativo_small(self):
        """error_relativo() debe ser < 0.02."""
        self.assertLess(self.pe.error_relativo(), 0.02)

    def test_error_relativo_positive(self):
        """error_relativo() debe ser ≥ 0."""
        self.assertGreaterEqual(self.pe.error_relativo(), 0.0)

    def test_terminos_length(self):
        """terminos() debe tener 8 elementos."""
        t = self.pe.terminos()
        self.assertEqual(len(t), 8)

    def test_terminos_first_prime(self):
        """Primer término es para p=2: 1/(1-1/4) = 4/3."""
        t = self.pe.terminos()
        p, val = t[0]
        self.assertEqual(p, 2)
        self.assertAlmostEqual(val, 4.0 / 3.0, places=10)

    def test_terminos_all_greater_one(self):
        """Todos los términos deben ser > 1."""
        for p, val in self.pe.terminos():
            self.assertGreater(val, 1.0, f"Término p={p} no es > 1")

    def test_producto_acumulado_length(self):
        """producto_acumulado() debe tener 8 elementos."""
        ac = self.pe.producto_acumulado()
        self.assertEqual(len(ac), 8)

    def test_producto_acumulado_increasing(self):
        """El producto acumulado debe ser creciente."""
        ac = self.pe.producto_acumulado()
        valores = [v for _, v in ac]
        for i in range(1, len(valores)):
            self.assertGreater(valores[i], valores[i - 1])

    def test_producto_acumulado_last_equals_parcial(self):
        """El último valor del acumulado = producto_parcial()."""
        ac = self.pe.producto_acumulado()
        _, ultimo = ac[-1]
        self.assertAlmostEqual(ultimo, self.pe.producto_parcial(), places=12)

    def test_psi_euler_in_range(self):
        """psi_euler() debe estar en (0, 1]."""
        psi = self.pe.psi_euler()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_euler_high(self):
        """psi_euler() debe ser > 0.95 (alta convergencia)."""
        self.assertGreater(self.pe.psi_euler(), 0.95)

    def test_psi_euler_equals_convergencia(self):
        """psi_euler() = convergencia()."""
        self.assertAlmostEqual(self.pe.psi_euler(), self.pe.convergencia(), places=12)

    def test_custom_s(self):
        """Con s=3, el producto parcial debe ser diferente."""
        pe3 = ProductoEulerZeta(s=3.0)
        self.assertNotAlmostEqual(
            pe3.producto_parcial(), self.pe.producto_parcial(), places=3
        )

    def test_single_prime(self):
        """Con un solo primo p=2, s=2: producto = 4/3."""
        pe_single = ProductoEulerZeta(primos=[2], s=2.0)
        self.assertAlmostEqual(pe_single.producto_parcial(), 4.0 / 3.0, places=10)

    def test_repr_contains_convergencia(self):
        """__repr__ debe mencionar convergencia."""
        r = repr(self.pe)
        self.assertIn("convergencia", r)

    def test_repr_contains_s(self):
        """__repr__ debe mencionar s."""
        r = repr(self.pe)
        self.assertIn("s=2", r)

    def test_producto_parcial_approx_value(self):
        """producto_parcial() ≈ 1.6281 para P₂₀, s=2."""
        self.assertAlmostEqual(self.pe.producto_parcial(), 1.6280, places=3)


# ============================================================================
# TestProductoAdelico – 25 tests
# ============================================================================

class TestProductoAdelico(unittest.TestCase):
    """Tests para ProductoAdelico."""

    def setUp(self):
        self.pa = ProductoAdelico()

    def test_primos_default(self):
        """primos por defecto debe ser P₂₀."""
        self.assertEqual(self.pa.primos, [2, 3, 5, 7, 11, 13, 17, 19])

    def test_calcular_positive(self):
        """calcular() debe ser positivo."""
        self.assertGreater(self.pa.calcular(), 0.0)

    def test_calcular_less_than_one(self):
        """calcular() < 1 (todos los factores < 1)."""
        self.assertLess(self.pa.calcular(), 1.0)

    def test_calcular_approx(self):
        """Π_ad ≈ 0.1710 para P₂₀."""
        self.assertAlmostEqual(self.pa.calcular(), 0.1710, places=3)

    def test_calcular_exact(self):
        """Π_ad calculado manualmente."""
        expected = 1
        for p in [2, 3, 5, 7, 11, 13, 17, 19]:
            expected *= (p - 1) / p
        self.assertAlmostEqual(self.pa.calcular(), expected, places=15)

    def test_densidad_vacio_equals_calcular(self):
        """densidad_vacio() = calcular()."""
        self.assertAlmostEqual(
            self.pa.densidad_vacio(), self.pa.calcular(), places=15
        )

    def test_fraccion_coprimos_equals_calcular(self):
        """fraccion_coprimos() = calcular()."""
        self.assertAlmostEqual(
            self.pa.fraccion_coprimos(), self.pa.calcular(), places=15
        )

    def test_complemento_densidad(self):
        """complemento_densidad() = 1 - calcular()."""
        expected = 1.0 - self.pa.calcular()
        self.assertAlmostEqual(self.pa.complemento_densidad(), expected, places=15)

    def test_complemento_in_range(self):
        """complemento_densidad() ∈ (0, 1)."""
        c = self.pa.complemento_densidad()
        self.assertGreater(c, 0.0)
        self.assertLess(c, 1.0)

    def test_terminos_length(self):
        """terminos() debe tener 8 elementos."""
        t = self.pa.terminos()
        self.assertEqual(len(t), 8)

    def test_terminos_first(self):
        """Primer término: p=2, valor=1/2."""
        t = self.pa.terminos()
        p, val = t[0]
        self.assertEqual(p, 2)
        self.assertAlmostEqual(val, 0.5, places=10)

    def test_terminos_all_in_range(self):
        """Todos los factores (p-1)/p ∈ (0, 1)."""
        for p, val in self.pa.terminos():
            self.assertGreater(val, 0.0)
            self.assertLess(val, 1.0)

    def test_producto_acumulado_length(self):
        """producto_acumulado() debe tener 8 elementos."""
        ac = self.pa.producto_acumulado()
        self.assertEqual(len(ac), 8)

    def test_producto_acumulado_decreasing(self):
        """El producto acumulado debe ser decreciente."""
        ac = self.pa.producto_acumulado()
        valores = [v for _, v in ac]
        for i in range(1, len(valores)):
            self.assertLess(valores[i], valores[i - 1])

    def test_producto_acumulado_last_equals_calcular(self):
        """El último valor del acumulado = calcular()."""
        ac = self.pa.producto_acumulado()
        _, ultimo = ac[-1]
        self.assertAlmostEqual(ultimo, self.pa.calcular(), places=12)

    def test_log_producto_negative(self):
        """log_producto() debe ser negativo."""
        self.assertLess(self.pa.log_producto(), 0.0)

    def test_log_producto_equals_log_calcular(self):
        """log_producto() = log(calcular())."""
        self.assertAlmostEqual(
            self.pa.log_producto(), math.log(self.pa.calcular()), places=12
        )

    def test_psi_adelico_in_range(self):
        """psi_adelico() debe estar en [0, 1]."""
        psi = self.pa.psi_adelico()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_adelico_high(self):
        """psi_adelico() debe ser > 0.99."""
        self.assertGreater(self.pa.psi_adelico(), 0.99)

    def test_psi_adelico_formula(self):
        """psi_adelico() = 1 - exp(-1/Π_ad)."""
        pi_ad = self.pa.calcular()
        expected = 1.0 - math.exp(-1.0 / pi_ad)
        self.assertAlmostEqual(self.pa.psi_adelico(), expected, places=12)

    def test_single_prime_p2(self):
        """Con solo p=2: Π_ad = 1/2 = 0.5."""
        pa_single = ProductoAdelico(primos=[2])
        self.assertAlmostEqual(pa_single.calcular(), 0.5, places=10)

    def test_product_p2_p3(self):
        """Con p=2,3: Π_ad = 1/2 × 2/3 = 1/3."""
        pa23 = ProductoAdelico(primos=[2, 3])
        self.assertAlmostEqual(pa23.calcular(), 1.0 / 3.0, places=12)

    def test_repr_contains_pi_ad(self):
        """__repr__ debe contener Pi_ad."""
        self.assertIn("Pi_ad", repr(self.pa))

    def test_repr_contains_psi(self):
        """__repr__ debe contener Psi_ad."""
        self.assertIn("Psi_ad", repr(self.pa))

    def test_calcular_less_than_half(self):
        """Π_ad < 0.5 (comienza con factor 1/2)."""
        self.assertLess(self.pa.calcular(), 0.5)


# ============================================================================
# TestVolumenCalabiYau – 20 tests
# ============================================================================

class TestVolumenCalabiYau(unittest.TestCase):
    """Tests para VolumenCalabiYau."""

    def setUp(self):
        self.vc = VolumenCalabiYau()

    def test_v6_default(self):
        """v6 por defecto debe ser 6."""
        self.assertAlmostEqual(self.vc.v6, 6.0, places=10)

    def test_fraccion_volumetrica_positive(self):
        """fraccion_volumetrica() debe ser positiva."""
        self.assertGreater(self.vc.fraccion_volumetrica(), 0.0)

    def test_fraccion_volumetrica_less_than_one(self):
        """fv < 1 (V₆ < (2π)³)."""
        self.assertLess(self.vc.fraccion_volumetrica(), 1.0)

    def test_fraccion_volumetrica_approx(self):
        """fv ≈ 0.02418."""
        self.assertAlmostEqual(self.vc.fraccion_volumetrica(), 0.02418, places=4)

    def test_fraccion_volumetrica_formula(self):
        """fv = V6/(2π)³."""
        expected = self.vc.v6 / ((2.0 * math.pi) ** 3)
        self.assertAlmostEqual(self.vc.fraccion_volumetrica(), expected, places=15)

    def test_factor_normalizacion_approx(self):
        """(2π)³ ≈ 248.05."""
        self.assertAlmostEqual(self.vc.factor_normalizacion(), 248.05, places=1)

    def test_factor_normalizacion_formula(self):
        """factor_normalizacion() = (2π)³."""
        expected = (2.0 * math.pi) ** 3
        self.assertAlmostEqual(self.vc.factor_normalizacion(), expected, places=10)

    def test_fv_times_factor_equals_v6(self):
        """fv × (2π)³ = V₆."""
        fv = self.vc.fraccion_volumetrica()
        norm = self.vc.factor_normalizacion()
        self.assertAlmostEqual(fv * norm, self.vc.v6, places=12)

    def test_volumen_esferico_6d_positive(self):
        """Volumen de la bola 6D debe ser positivo."""
        self.assertGreater(self.vc.volumen_esferico_6d(), 0.0)

    def test_volumen_esferico_6d_formula(self):
        """V₆_bola = π³/6."""
        expected = (math.pi ** 3) / 6.0
        self.assertAlmostEqual(self.vc.volumen_esferico_6d(), expected, places=10)

    def test_ratio_cy_esferico_positive(self):
        """ratio_cy_esferico() debe ser positivo."""
        self.assertGreater(self.vc.ratio_cy_esferico(), 0.0)

    def test_ratio_cy_esferico_approx(self):
        """V₆_CY/V₆_bola ≈ 1.161."""
        ratio = self.vc.ratio_cy_esferico()
        self.assertAlmostEqual(ratio, self.vc.v6 / self.vc.volumen_esferico_6d(), places=10)

    def test_contribucion_alpha_equals_fv(self):
        """contribucion_alpha() = fraccion_volumetrica()."""
        self.assertAlmostEqual(
            self.vc.contribucion_alpha(), self.vc.fraccion_volumetrica(), places=15
        )

    def test_psi_calabi_in_range(self):
        """psi_calabi() ∈ [0, 1]."""
        psi = self.vc.psi_calabi()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_calabi_high(self):
        """psi_calabi() > 0.9 (alta coherencia geométrica)."""
        self.assertGreater(self.vc.psi_calabi(), 0.9)

    def test_psi_calabi_formula(self):
        """psi_calabi() = 1 - exp(-alpha_inv × fv)."""
        fv = self.vc.fraccion_volumetrica()
        expected = 1.0 - math.exp(-_ALPHA_INV * fv)
        self.assertAlmostEqual(self.vc.psi_calabi(), expected, places=12)

    def test_custom_v6(self):
        """Con V₆=3, fv = 3/(2π)³."""
        vc3 = VolumenCalabiYau(v6=3.0)
        expected = 3.0 / ((2.0 * math.pi) ** 3)
        self.assertAlmostEqual(vc3.fraccion_volumetrica(), expected, places=15)

    def test_repr_contains_v6(self):
        """__repr__ debe mencionar V6."""
        r = repr(self.vc)
        self.assertIn("V6=6", r)

    def test_repr_contains_fv(self):
        """__repr__ debe mencionar fv."""
        r = repr(self.vc)
        self.assertIn("fv=", r)

    def test_psi_calabi_approx_value(self):
        """psi_calabi() ≈ 0.963."""
        self.assertAlmostEqual(self.vc.psi_calabi(), 0.963, places=2)


# ============================================================================
# TestDerivacionBeta – 20 tests
# ============================================================================

class TestDerivacionBeta(unittest.TestCase):
    """Tests para DerivacionBeta."""

    def setUp(self):
        self.db = DerivacionBeta()

    def test_omega_ajuste_default(self):
        """omega_ajuste por defecto debe ser _OMEGA_AJUSTE."""
        self.assertAlmostEqual(self.db.omega_ajuste, _OMEGA_AJUSTE, places=6)

    def test_alpha_experimental_default(self):
        """alpha_experimental por defecto ≈ 137.036."""
        self.assertAlmostEqual(
            self.db.alpha_experimental, 137.035999084, places=6
        )

    def test_alpha_derivado_approx(self):
        """alpha_derivado() ≈ 137.036."""
        self.assertAlmostEqual(self.db.alpha_derivado(), 137.036, places=3)

    def test_alpha_derivado_close_to_experimental(self):
        """alpha_derivado() debe ser muy cercano a alpha_experimental."""
        self.assertAlmostEqual(
            self.db.alpha_derivado(), self.db.alpha_experimental, places=4
        )

    def test_alpha_derivado_formula(self):
        """alpha_derivado() = fv × pi_ad × omega."""
        fv = self.db.vol_calabi.fraccion_volumetrica()
        pi_ad = self.db.prod_adelico.calcular()
        expected = fv * pi_ad * self.db.omega_ajuste
        self.assertAlmostEqual(self.db.alpha_derivado(), expected, places=12)

    def test_error_relativo_tiny(self):
        """error_relativo() debe ser casi 0 (ajuste exacto)."""
        self.assertLess(self.db.error_relativo(), 1e-10)

    def test_error_relativo_nonneg(self):
        """error_relativo() >= 0."""
        self.assertGreaterEqual(self.db.error_relativo(), 0.0)

    def test_precision_relativa_close_to_one(self):
        """precision_relativa() ≈ 1.0."""
        self.assertAlmostEqual(self.db.precision_relativa(), 1.0, places=8)

    def test_precision_relativa_in_range(self):
        """precision_relativa() ∈ [0, 1]."""
        p = self.db.precision_relativa()
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_raiz_euler_zeta_approx(self):
        """raiz_euler_zeta() ≈ 1.6281."""
        self.assertAlmostEqual(self.db.raiz_euler_zeta(), 1.6280, places=3)

    def test_raiz_euler_zeta_positive(self):
        """raiz_euler_zeta() > 1."""
        self.assertGreater(self.db.raiz_euler_zeta(), 1.0)

    def test_resumen_ingredientes_keys(self):
        """resumen_ingredientes() debe tener las claves correctas."""
        r = self.db.resumen_ingredientes()
        for key in ["fv", "pi_ad", "omega_ajuste", "alpha_d", "alpha_exp", "error_relativo"]:
            self.assertIn(key, r)

    def test_resumen_ingredientes_fv_approx(self):
        """fv en el resumen ≈ 0.02418."""
        r = self.db.resumen_ingredientes()
        self.assertAlmostEqual(r["fv"], 0.02418, places=4)

    def test_resumen_ingredientes_pi_ad_approx(self):
        """pi_ad en el resumen ≈ 0.1710."""
        r = self.db.resumen_ingredientes()
        self.assertAlmostEqual(r["pi_ad"], 0.1710, places=3)

    def test_psi_beta_in_range(self):
        """psi_beta() ∈ [0, 1]."""
        psi = self.db.psi_beta()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_beta_high(self):
        """psi_beta() > 0.99."""
        self.assertGreater(self.db.psi_beta(), 0.99)

    def test_psi_beta_formula(self):
        """psi_beta() = 1 - exp(-alpha_inv / (2π²))."""
        expected = 1.0 - math.exp(
            -self.db.alpha_experimental / (2.0 * math.pi ** 2)
        )
        self.assertAlmostEqual(self.db.psi_beta(), expected, places=12)

    def test_repr_contains_alpha_d(self):
        """__repr__ debe mencionar alpha_d."""
        r = repr(self.db)
        self.assertIn("alpha_d", r)

    def test_repr_contains_error(self):
        """__repr__ debe mencionar error."""
        r = repr(self.db)
        self.assertIn("error", r)

    def test_alpha_range(self):
        """alpha_derivado() debe estar entre 137 y 138."""
        alpha = self.db.alpha_derivado()
        self.assertGreater(alpha, 137.0)
        self.assertLess(alpha, 138.0)


# ============================================================================
# TestTorsionAdelica – 20 tests
# ============================================================================

class TestTorsionAdelica(unittest.TestCase):
    """Tests para TorsionAdelica."""

    def setUp(self):
        self.ta = TorsionAdelica()

    def test_alpha_inv_default(self):
        """alpha_inv por defecto ≈ 137.036."""
        self.assertAlmostEqual(self.ta.alpha_inv, 137.035999084, places=6)

    def test_f0_default(self):
        """f0 por defecto = 141.7001 Hz."""
        self.assertAlmostEqual(self.ta.f0, 141.7001, places=4)

    def test_theta_torsion_positive(self):
        """theta_torsion() debe ser positivo."""
        self.assertGreater(self.ta.theta_torsion(), 0.0)

    def test_theta_torsion_formula(self):
        """theta_torsion() = 2π / alpha_inv."""
        expected = (2.0 * math.pi) / self.ta.alpha_inv
        self.assertAlmostEqual(self.ta.theta_torsion(), expected, places=12)

    def test_theta_torsion_approx(self):
        """θ_T ≈ 0.04585 rad."""
        self.assertAlmostEqual(self.ta.theta_torsion(), 0.04585, places=4)

    def test_theta_torsion_small(self):
        """θ_T < 0.1 rad (ángulo pequeño)."""
        self.assertLess(self.ta.theta_torsion(), 0.1)

    def test_fraccion_materia_formula(self):
        """fraccion_materia() = 1/alpha_inv."""
        expected = 1.0 / self.ta.alpha_inv
        self.assertAlmostEqual(self.ta.fraccion_materia(), expected, places=12)

    def test_fraccion_materia_approx(self):
        """fr_mat ≈ 0.00730."""
        self.assertAlmostEqual(self.ta.fraccion_materia(), 0.00730, places=4)

    def test_fraccion_materia_small(self):
        """fr_mat < 0.01."""
        self.assertLess(self.ta.fraccion_materia(), 0.01)

    def test_angulo_grados_positive(self):
        """angulo_grados() debe ser positivo."""
        self.assertGreater(self.ta.angulo_grados(), 0.0)

    def test_angulo_grados_formula(self):
        """angulo_grados() = θ_T × 180/π."""
        expected = math.degrees(self.ta.theta_torsion())
        self.assertAlmostEqual(self.ta.angulo_grados(), expected, places=10)

    def test_angulo_grados_approx(self):
        """θ_T en grados ≈ 2.627°."""
        self.assertAlmostEqual(self.ta.angulo_grados(), 2.627, places=2)

    def test_frecuencia_torsion_hz_positive(self):
        """frecuencia_torsion_hz() debe ser positiva."""
        self.assertGreater(self.ta.frecuencia_torsion_hz(), 0.0)

    def test_frecuencia_torsion_hz_formula(self):
        """frecuencia_torsion_hz() = f0 × theta_T."""
        expected = self.ta.f0 * self.ta.theta_torsion()
        self.assertAlmostEqual(self.ta.frecuencia_torsion_hz(), expected, places=12)

    def test_longitud_fibra_positive(self):
        """longitud_fibra_m() debe ser positiva."""
        self.assertGreater(self.ta.longitud_fibra_m(), 0.0)

    def test_acoplamiento_qcal_positive(self):
        """acoplamiento_qcal() debe ser positivo."""
        self.assertGreater(self.ta.acoplamiento_qcal(), 0.0)

    def test_acoplamiento_qcal_formula(self):
        """acoplamiento_qcal() = f0 / alpha_inv."""
        expected = self.ta.f0 / self.ta.alpha_inv
        self.assertAlmostEqual(self.ta.acoplamiento_qcal(), expected, places=12)

    def test_psi_torsion_in_range(self):
        """psi_torsion() ∈ [0, 1]."""
        psi = self.ta.psi_torsion()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_torsion_high(self):
        """psi_torsion() > 0.99."""
        self.assertGreater(self.ta.psi_torsion(), 0.99)

    def test_psi_torsion_formula(self):
        """psi_torsion() = 1 - fraccion_materia()."""
        expected = 1.0 - self.ta.fraccion_materia()
        self.assertAlmostEqual(self.ta.psi_torsion(), expected, places=12)

    def test_repr_contains_theta(self):
        """__repr__ debe mencionar theta_T."""
        self.assertIn("theta_T", repr(self.ta))

    def test_repr_contains_fr_mat(self):
        """__repr__ debe mencionar fr_mat."""
        self.assertIn("fr_mat", repr(self.ta))


# ============================================================================
# TestCoherenciaDerivacionBeta – 25 tests
# ============================================================================

class TestCoherenciaDerivacionBeta(unittest.TestCase):
    """Tests para CoherenciaDerivacionBeta."""

    def setUp(self):
        self.coh = CoherenciaDerivacionBeta()

    def test_psi_umbral_default(self):
        """psi_umbral por defecto debe ser 0.888."""
        self.assertAlmostEqual(self.coh.psi_umbral, 0.888, places=3)

    def test_psi_euler_in_range(self):
        """psi_euler() ∈ (0, 1]."""
        psi = self.coh.psi_euler()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_euler_high(self):
        """psi_euler() > 0.95."""
        self.assertGreater(self.coh.psi_euler(), 0.95)

    def test_psi_adelico_in_range(self):
        """psi_adelico() ∈ [0, 1]."""
        psi = self.coh.psi_adelico()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_adelico_high(self):
        """psi_adelico() > 0.99."""
        self.assertGreater(self.coh.psi_adelico(), 0.99)

    def test_psi_calabi_in_range(self):
        """psi_calabi() ∈ [0, 1]."""
        psi = self.coh.psi_calabi()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_calabi_high(self):
        """psi_calabi() > 0.9."""
        self.assertGreater(self.coh.psi_calabi(), 0.9)

    def test_psi_beta_in_range(self):
        """psi_beta() ∈ [0, 1]."""
        psi = self.coh.psi_beta()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_beta_high(self):
        """psi_beta() > 0.99."""
        self.assertGreater(self.coh.psi_beta(), 0.99)

    def test_psi_torsion_in_range(self):
        """psi_torsion() ∈ [0, 1]."""
        psi = self.coh.psi_torsion()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_torsion_high(self):
        """psi_torsion() > 0.99."""
        self.assertGreater(self.coh.psi_torsion(), 0.99)

    def test_coherencias_individuales_keys(self):
        """coherencias_individuales() debe tener 5 claves."""
        c = self.coh.coherencias_individuales()
        expected_keys = {
            "psi_euler", "psi_adelico", "psi_calabi", "psi_beta", "psi_torsion"
        }
        self.assertEqual(set(c.keys()), expected_keys)

    def test_coherencias_individuales_all_in_range(self):
        """Todas las coherencias individuales ∈ [0, 1]."""
        c = self.coh.coherencias_individuales()
        for k, v in c.items():
            self.assertGreaterEqual(v, 0.0, f"{k} < 0")
            self.assertLessEqual(v, 1.0, f"{k} > 1")

    def test_psi_global_in_range(self):
        """psi_global() ∈ [0, 1]."""
        psi = self.coh.psi_global()
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_global_above_threshold(self):
        """psi_global() ≥ 0.888 (sello activo)."""
        self.assertGreaterEqual(self.coh.psi_global(), 0.888)

    def test_psi_global_geometric_mean(self):
        """psi_global() = media geométrica de las 5 coherencias."""
        c = self.coh.coherencias_individuales()
        producto = (
            c["psi_euler"] * c["psi_adelico"] * c["psi_calabi"]
            * c["psi_beta"] * c["psi_torsion"]
        )
        expected = producto ** 0.2
        self.assertAlmostEqual(self.coh.psi_global(), expected, places=12)

    def test_sello_activo(self):
        """sello_activo() debe ser True."""
        self.assertTrue(self.coh.sello_activo())

    def test_sello_activo_logic(self):
        """sello_activo() = (psi_global >= psi_umbral)."""
        psi_g = self.coh.psi_global()
        umbral = self.coh.psi_umbral
        expected = psi_g >= umbral
        self.assertEqual(self.coh.sello_activo(), expected)

    def test_validar_keys(self):
        """validar() debe tener las claves esperadas."""
        v = self.coh.validar()
        for key in ["coherencias", "psi_global", "psi_umbral", "sello_activo", "diferencia_umbral"]:
            self.assertIn(key, v)

    def test_validar_sello_activo(self):
        """validar()['sello_activo'] debe ser True."""
        v = self.coh.validar()
        self.assertTrue(v["sello_activo"])

    def test_validar_diferencia_umbral_positive(self):
        """validar()['diferencia_umbral'] debe ser > 0."""
        v = self.coh.validar()
        self.assertGreater(v["diferencia_umbral"], 0.0)

    def test_certificacion_auron_activo(self):
        """certificacion_auron() debe contener ACTIVO."""
        cert = self.coh.certificacion_auron()
        self.assertIn("ACTIVO", cert)

    def test_certificacion_auron_sello(self):
        """certificacion_auron() debe contener ∴DBA∞³."""
        cert = self.coh.certificacion_auron()
        self.assertIn("∴DBA∞³", cert)

    def test_certificacion_auron_ram(self):
        """certificacion_auron() debe contener el RAM."""
        cert = self.coh.certificacion_auron()
        self.assertIn("RAM-LI-2026-DERIVACION-BETA-ADELICA", cert)

    def test_repr_contains_psi_global(self):
        """__repr__ debe mencionar Ψ_global."""
        r = repr(self.coh)
        self.assertIn("Ψ_global", r)


# ============================================================================
# TestSistemaDerivacionBetaAdelica – 25 tests
# ============================================================================

class TestSistemaDerivacionBetaAdelica(unittest.TestCase):
    """Tests para SistemaDerivacionBetaAdelica."""

    def setUp(self):
        self.sistema = SistemaDerivacionBetaAdelica()
        self.resultado = self.sistema.activar()

    def test_activar_returns_dict(self):
        """activar() debe devolver un dict."""
        self.assertIsInstance(self.resultado, dict)

    def test_sello_value(self):
        """sello debe ser '∴DBA∞³'."""
        self.assertEqual(self.resultado["sello"], "∴DBA∞³")

    def test_ram_value(self):
        """ram debe contener el identificador correcto."""
        self.assertEqual(
            self.resultado["ram"], "RAM-LI-2026-DERIVACION-BETA-ADELICA"
        )

    def test_version_value(self):
        """version debe ser '1.0.0'."""
        self.assertEqual(self.resultado["version"], "1.0.0")

    def test_f0_hz(self):
        """f0_hz debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.resultado["f0_hz"], 141.7001, places=4)

    def test_alpha_inv(self):
        """alpha_inv ≈ 137.036."""
        self.assertAlmostEqual(self.resultado["alpha_inv"], 137.036, places=3)

    def test_alpha_fina_small(self):
        """alpha_fina < 0.01."""
        self.assertLess(self.resultado["alpha_fina"], 0.01)

    def test_v6_value(self):
        """v6 = 6."""
        self.assertAlmostEqual(self.resultado["v6"], 6.0, places=10)

    def test_n_primos(self):
        """n_primos = 8."""
        self.assertEqual(self.resultado["n_primos"], 8)

    def test_zeta_parcial_positive(self):
        """zeta_parcial > 1."""
        self.assertGreater(self.resultado["zeta_parcial"], 1.0)

    def test_zeta_exacta_approx(self):
        """zeta_exacta ≈ π²/6 ≈ 1.6449."""
        self.assertAlmostEqual(
            self.resultado["zeta_exacta"], (math.pi ** 2) / 6.0, places=6
        )

    def test_convergencia_euler_in_range(self):
        """convergencia_euler ∈ (0, 1]."""
        c = self.resultado["convergencia_euler"]
        self.assertGreater(c, 0.0)
        self.assertLessEqual(c, 1.0)

    def test_pi_ad_approx(self):
        """pi_ad ≈ 0.1710."""
        self.assertAlmostEqual(self.resultado["pi_ad"], 0.1710, places=3)

    def test_fv_approx(self):
        """fv ≈ 0.02418."""
        self.assertAlmostEqual(self.resultado["fv"], 0.02418, places=4)

    def test_alpha_derivado_approx(self):
        """alpha_derivado ≈ 137.036."""
        self.assertAlmostEqual(self.resultado["alpha_derivado"], 137.036, places=3)

    def test_omega_ajuste_positive(self):
        """omega_ajuste > 0."""
        self.assertGreater(self.resultado["omega_ajuste"], 0.0)

    def test_error_relativo_tiny(self):
        """error_relativo ≈ 0 (ajuste exacto)."""
        self.assertLess(self.resultado["error_relativo"], 1e-10)

    def test_theta_torsion_rad_positive(self):
        """theta_torsion_rad > 0."""
        self.assertGreater(self.resultado["theta_torsion_rad"], 0.0)

    def test_theta_torsion_deg_positive(self):
        """theta_torsion_deg > 0."""
        self.assertGreater(self.resultado["theta_torsion_deg"], 0.0)

    def test_fraccion_materia(self):
        """fraccion_materia ≈ 0.0073."""
        self.assertAlmostEqual(self.resultado["fraccion_materia"], 0.0073, places=3)

    def test_coherencias_dict(self):
        """coherencias debe ser un dict con 5 claves."""
        c = self.resultado["coherencias"]
        self.assertIsInstance(c, dict)
        self.assertEqual(len(c), 5)

    def test_psi_global_above_threshold(self):
        """psi_global ≥ 0.888."""
        self.assertGreaterEqual(self.resultado["psi_global"], 0.888)

    def test_psi_umbral_value(self):
        """psi_umbral = 0.888."""
        self.assertAlmostEqual(self.resultado["psi_umbral"], 0.888, places=3)

    def test_sello_activo_true(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.resultado["sello_activo"])

    def test_certificacion_contains_activo(self):
        """certificacion debe mencionar ACTIVO."""
        self.assertIn("ACTIVO", self.resultado["certificacion"])

    def test_resumen_returns_string(self):
        """resumen() debe devolver una cadena."""
        self.assertIsInstance(self.sistema.resumen(), str)

    def test_resumen_contains_sello(self):
        """resumen() debe mencionar ∴DBA∞³."""
        self.assertIn("∴DBA∞³", self.sistema.resumen())

    def test_repr_contains_alpha_inv(self):
        """__repr__ debe mencionar α⁻¹."""
        r = repr(self.sistema)
        self.assertIn("137", r)

    def test_post_init_coherencia(self):
        """coherencia debe ser inicializado por __post_init__."""
        self.assertIsInstance(self.sistema.coherencia, CoherenciaDerivacionBeta)


# ============================================================================
# TestAPIPublica – 15 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para la API pública derivacion_beta_adelica_activar()."""

    def setUp(self):
        self.r = derivacion_beta_adelica_activar()

    def test_returns_dict(self):
        """derivacion_beta_adelica_activar() debe devolver un dict."""
        self.assertIsInstance(self.r, dict)

    def test_sello_activo(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.r["sello_activo"])

    def test_sello_value(self):
        """sello debe ser '∴DBA∞³'."""
        self.assertEqual(self.r["sello"], "∴DBA∞³")

    def test_psi_global_above_threshold(self):
        """psi_global ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_global"], 0.888)

    def test_alpha_derivado_close(self):
        """alpha_derivado ≈ 137.036."""
        self.assertAlmostEqual(self.r["alpha_derivado"], 137.036, places=3)

    def test_f0_hz_value(self):
        """f0_hz = 141.7001 Hz."""
        self.assertAlmostEqual(self.r["f0_hz"], 141.7001, places=4)

    def test_ram_correct(self):
        """ram debe ser el identificador correcto."""
        self.assertEqual(self.r["ram"], "RAM-LI-2026-DERIVACION-BETA-ADELICA")

    def test_pi_ad_value(self):
        """pi_ad (Π_ad) debe estar en (0, 1)."""
        self.assertGreater(self.r["pi_ad"], 0.0)
        self.assertLess(self.r["pi_ad"], 1.0)

    def test_fv_value(self):
        """fv = V₆/(2π)³ debe ser > 0 y < 1."""
        self.assertGreater(self.r["fv"], 0.0)
        self.assertLess(self.r["fv"], 1.0)

    def test_theta_torsion_positive(self):
        """theta_torsion_rad > 0."""
        self.assertGreater(self.r["theta_torsion_rad"], 0.0)

    def test_fraccion_materia_small(self):
        """fraccion_materia < 0.01."""
        self.assertLess(self.r["fraccion_materia"], 0.01)

    def test_coherencias_all_valid(self):
        """Todas las coherencias individuales ∈ [0, 1]."""
        for k, v in self.r["coherencias"].items():
            self.assertGreaterEqual(v, 0.0, f"{k} < 0")
            self.assertLessEqual(v, 1.0, f"{k} > 1")

    def test_idempotencia(self):
        """Dos llamadas consecutivas dan el mismo psi_global."""
        r2 = derivacion_beta_adelica_activar()
        self.assertAlmostEqual(
            self.r["psi_global"], r2["psi_global"], places=15
        )

    def test_alpha_fina_inverse(self):
        """alpha_fina × alpha_inv ≈ 1."""
        self.assertAlmostEqual(
            self.r["alpha_fina"] * self.r["alpha_inv"], 1.0, places=12
        )

    def test_certificacion_present(self):
        """certificacion debe estar en el resultado."""
        self.assertIn("certificacion", self.r)
        self.assertIsInstance(self.r["certificacion"], str)


if __name__ == "__main__":
    unittest.main()
