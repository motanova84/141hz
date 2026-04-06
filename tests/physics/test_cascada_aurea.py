"""
Tests for physics.cascada_aurea — Cascada Áurea / Sistema ∴CA∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesCascadaAurea   – constantes físicas y geométricas
  - CompactificacionAurea    – 12 etapas ϕⁿ y número de Lucas L₁₂
  - DescensoPlanck           – descenso logarítmico-áureo y resonancia Riemann
  - MatrizKPi                – operador K_π 7×7, autovalores y brecha espectral
  - ViscosidadEfectiva       – μ_eff = 1/f₀, invariante μ·f₀ = 1
  - FlujoLaminar             – condición Re(s) = ½ y disipación áurea
  - CoherenciaCascada        – promedio ponderado → Ψ_global ≥ 0.888
  - SistemaCascadaAurea      – orquestador con activar()
  - ResultadoCascadaAurea    – dataclass de resultados
  - cascada_aurea_activar()  – API pública
  - Utilidades internas      – _mv, _dot, _norm, _lambda_max_potencia,
                               _lambda_min_shift

Invariantes clave verificados:
  - n_pasos_aureos = 12
  - ϕ¹² ≈ 321.9969 ≈ L₁₂ = 322  (número de Lucas)
  - n_descenso ≈ 196.74 pasos áureos log_ϕ(f_P/f₀)
  - f₀/γ₁ ≈ 10.025  (resonancia con el primer cero de Riemann)
  - gap K_π ≈ 3496.96 Hz ≈ f₀·(ϕ⁷−ϕ³)  (brecha espectral áurea)
  - μ_eff·f₀ = 1.0  (invariante exacto del vacío)
  - Ψ_global ≥ 0.888  → sello ∴CA∞³ ACTIVO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.cascada_aurea import (
    # Constantes de módulo
    _LAMBDA_P,
    _C,
    _F_PLANCK,
    _F0,
    _PHI,
    _N_PASOS,
    _N_GUARDIANES,
    _L12,
    _GAMMA_RIEMANN,
    _N_DESCENSO,
    _OMEGA_TARGET,
    _MU_EFF,
    _PSI_UMBRAL,
    _PHI_N,
    _N_DECADAS,
    # Clases
    ConstantesCascadaAurea,
    CompactificacionAurea,
    DescensoPlanck,
    MatrizKPi,
    ViscosidadEfectiva,
    FlujoLaminar,
    CoherenciaCascada,
    SistemaCascadaAurea,
    ResultadoCascadaAurea,
    # API pública
    cascada_aurea_activar,
    # Utilidades internas
    _mv,
    _dot,
    _norm,
    _lambda_max_potencia,
    _lambda_min_shift,
)


# ============================================================================
# TestModuleConstants – 16 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_lambda_p_order(self):
        """_LAMBDA_P debe ser ≈ 1.616229×10⁻³⁵ m."""
        self.assertAlmostEqual(_LAMBDA_P, 1.616229e-35, places=40)

    def test_c_value(self):
        """_C debe ser 299 792 458 m/s."""
        self.assertEqual(_C, 299792458.0)

    def test_f_planck_derivation(self):
        """_F_PLANCK = c/λ_P debe coincidir con el valor calculado."""
        expected = _C / _LAMBDA_P
        self.assertAlmostEqual(_F_PLANCK, expected, places=0)

    def test_f_planck_order(self):
        """_F_PLANCK debe estar en el orden 10⁴³ Hz."""
        self.assertGreater(_F_PLANCK, 1e42)
        self.assertLess(_F_PLANCK, 1e44)

    def test_phi_value(self):
        """_PHI debe ser la proporción áurea ≈ 1.618034."""
        self.assertAlmostEqual(_PHI, (1.0 + math.sqrt(5.0)) / 2.0, places=10)

    def test_phi_identity(self):
        """ϕ² = ϕ + 1 (identidad de la proporción áurea)."""
        self.assertAlmostEqual(_PHI ** 2, _PHI + 1.0, places=10)

    def test_n_pasos(self):
        """_N_PASOS debe ser 12."""
        self.assertEqual(_N_PASOS, 12)

    def test_n_guardianes(self):
        """_N_GUARDIANES debe ser 7."""
        self.assertEqual(_N_GUARDIANES, 7)

    def test_l12_value(self):
        """_L12 debe ser 322 (número de Lucas L₁₂)."""
        self.assertEqual(_L12, 322)

    def test_gamma_riemann(self):
        """_GAMMA_RIEMANN debe ser ≈ 14.134725."""
        self.assertAlmostEqual(_GAMMA_RIEMANN, 14.134725, places=5)

    def test_n_descenso_positive(self):
        """_N_DESCENSO debe ser positivo y ≈ 196.74."""
        self.assertGreater(_N_DESCENSO, 190.0)
        self.assertLess(_N_DESCENSO, 205.0)

    def test_n_descenso_formula(self):
        """_N_DESCENSO = log_ϕ(f_P/f₀)."""
        expected = math.log(_F_PLANCK / _F0) / math.log(_PHI)
        self.assertAlmostEqual(_N_DESCENSO, expected, places=8)

    def test_omega_target_positive(self):
        """_OMEGA_TARGET debe ser positivo y ≈ 3513.93 Hz."""
        self.assertGreater(_OMEGA_TARGET, 3000.0)
        self.assertLess(_OMEGA_TARGET, 5000.0)

    def test_omega_target_formula(self):
        """_OMEGA_TARGET = f₀·(ϕ⁷−ϕ³)."""
        expected = _F0 * (_PHI ** 7 - _PHI ** 3)
        self.assertAlmostEqual(_OMEGA_TARGET, expected, places=6)

    def test_mu_eff_formula(self):
        """_MU_EFF = 1/f₀."""
        self.assertAlmostEqual(_MU_EFF, 1.0 / _F0, places=10)

    def test_psi_umbral(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_phi_n_length(self):
        """_PHI_N debe tener 12 elementos."""
        self.assertEqual(len(_PHI_N), _N_PASOS)

    def test_phi_n_first(self):
        """El primer elemento de _PHI_N debe ser ϕ¹."""
        self.assertAlmostEqual(_PHI_N[0], _PHI, places=10)

    def test_phi_n_last(self):
        """El último elemento de _PHI_N debe ser ϕ¹²."""
        self.assertAlmostEqual(_PHI_N[-1], _PHI ** 12, places=8)

    def test_n_decadas_consistency(self):
        """_N_DECADAS = ⌊log₁₀(f_P/f₀)⌋."""
        expected = int(math.log10(_F_PLANCK / _F0))
        self.assertEqual(_N_DECADAS, expected)


# ============================================================================
# TestConstantesCascadaAurea – 8 tests
# ============================================================================

class TestConstantesCascadaAurea(unittest.TestCase):
    """Tests para ConstantesCascadaAurea."""

    def setUp(self):
        self.c = ConstantesCascadaAurea()

    def test_f0_default(self):
        """f0 por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_phi_default(self):
        """phi debe ser la proporción áurea."""
        self.assertAlmostEqual(self.c.phi, (1.0 + math.sqrt(5.0)) / 2.0, places=10)

    def test_n_pasos_default(self):
        """n_pasos por defecto debe ser 12."""
        self.assertEqual(self.c.n_pasos, 12)

    def test_n_guardianes_default(self):
        """n_guardianes por defecto debe ser 7."""
        self.assertEqual(self.c.n_guardianes, 7)

    def test_psi_umbral_default(self):
        """psi_umbral por defecto debe ser 0.888."""
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=3)

    def test_ratio_logaritmico(self):
        """ratio_logaritmico() = log₁₀(f_P/f₀) > 40."""
        r = self.c.ratio_logaritmico()
        self.assertGreater(r, 40.0)
        self.assertLess(r, 43.0)

    def test_phi_n_valid_range(self):
        """phi_n(n) para n en [1, 12] debe ser ϕⁿ."""
        for n in range(1, 13):
            expected = self.c.phi ** n
            self.assertAlmostEqual(self.c.phi_n(n), expected, places=8)

    def test_phi_n_invalid_raises(self):
        """phi_n(0) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.c.phi_n(0)

    def test_repr_contains_f0(self):
        """__repr__ debe mencionar f0."""
        self.assertIn("141.7001", repr(self.c))

    def test_mu_eff_default(self):
        """mu_eff por defecto debe ser 1/f₀."""
        self.assertAlmostEqual(self.c.mu_eff, 1.0 / self.c.f0, places=10)


# ============================================================================
# TestCompactificacionAurea – 10 tests
# ============================================================================

class TestCompactificacionAurea(unittest.TestCase):
    """Tests para CompactificacionAurea."""

    def setUp(self):
        self.ca = CompactificacionAurea()

    def test_generaciones_length(self):
        """generaciones() debe retornar 12 valores."""
        self.assertEqual(len(self.ca.generaciones()), 12)

    def test_generaciones_first(self):
        """El primer elemento de generaciones() debe ser ϕ¹."""
        gens = self.ca.generaciones()
        self.assertAlmostEqual(gens[0], _PHI, places=10)

    def test_generaciones_last(self):
        """El último elemento de generaciones() debe ser ϕ¹²."""
        gens = self.ca.generaciones()
        self.assertAlmostEqual(gens[-1], _PHI ** 12, places=8)

    def test_horizonte_value(self):
        """horizonte() debe ser ϕ¹² ≈ 321.997."""
        h = self.ca.horizonte()
        self.assertAlmostEqual(h, _PHI ** 12, places=8)
        self.assertGreater(h, 321.0)
        self.assertLess(h, 323.0)

    def test_error_lucas_small(self):
        """error_lucas() debe ser muy pequeño (< 1e-4)."""
        self.assertLess(self.ca.error_lucas(), 1e-4)

    def test_error_lucas_formula(self):
        """error_lucas() = |ϕ¹² − 322| / 322."""
        expected = abs(_PHI ** 12 - 322) / 322
        self.assertAlmostEqual(self.ca.error_lucas(), expected, places=10)

    def test_psi_compactificacion_range(self):
        """psi_compactificacion() debe estar en (0.999, 1.0]."""
        psi = self.ca.psi_compactificacion()
        self.assertGreater(psi, 0.999)
        self.assertLessEqual(psi, 1.0)

    def test_psi_above_umbral(self):
        """psi_compactificacion() debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.ca.psi_compactificacion(), 0.888)

    def test_identidad_fibonacci_valid(self):
        """identidad_fibonacci(n) debe ser < 1e-10 para todo n."""
        for n in range(1, 11):
            err = self.ca.identidad_fibonacci(n)
            self.assertLess(err, 1e-10, f"Error en n={n}: {err}")

    def test_identidad_fibonacci_invalid_raises(self):
        """identidad_fibonacci(0) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            self.ca.identidad_fibonacci(0)

    def test_repr_contains_phi12(self):
        """__repr__ debe mencionar ϕ¹²."""
        self.assertIn("321.99", repr(self.ca))


# ============================================================================
# TestDescensoPlanck – 10 tests
# ============================================================================

class TestDescensoPlanck(unittest.TestCase):
    """Tests para DescensoPlanck."""

    def setUp(self):
        self.dp = DescensoPlanck()

    def test_n_descenso_range(self):
        """n_descenso() debe estar entre 190 y 205."""
        n = self.dp.n_descenso()
        self.assertGreater(n, 190.0)
        self.assertLess(n, 205.0)

    def test_n_descenso_formula(self):
        """n_descenso() = log_ϕ(f_P/f₀)."""
        expected = math.log(_F_PLANCK / _F0) / math.log(_PHI)
        self.assertAlmostEqual(self.dp.n_descenso(), expected, places=6)

    def test_etapas_por_paso_range(self):
        """etapas_por_paso() debe estar entre 15 y 18."""
        e = self.dp.etapas_por_paso()
        self.assertGreater(e, 15.0)
        self.assertLess(e, 18.0)

    def test_etapas_por_paso_formula(self):
        """etapas_por_paso() = n_descenso() / n_pasos."""
        expected = self.dp.n_descenso() / self.dp.n_pasos
        self.assertAlmostEqual(self.dp.etapas_por_paso(), expected, places=8)

    def test_ratio_riemann_close_to_10(self):
        """ratio_riemann() = f₀/γ₁ debe ser ≈ 10 (error < 1%)."""
        r = self.dp.ratio_riemann()
        self.assertAlmostEqual(r, 10.0, delta=0.1)

    def test_ratio_riemann_formula(self):
        """ratio_riemann() = f₀ / gamma_riemann."""
        expected = _F0 / _GAMMA_RIEMANN
        self.assertAlmostEqual(self.dp.ratio_riemann(), expected, places=8)

    def test_error_riemann_small(self):
        """error_riemann() debe ser < 0.01 (< 1%)."""
        self.assertLess(self.dp.error_riemann(), 0.01)

    def test_error_riemann_formula(self):
        """error_riemann() = |f₀/γ₁ − 10| / 10."""
        expected = abs(_F0 / _GAMMA_RIEMANN - 10.0) / 10.0
        self.assertAlmostEqual(self.dp.error_riemann(), expected, places=8)

    def test_psi_descenso_range(self):
        """psi_descenso() debe estar en (0.99, 1.0]."""
        psi = self.dp.psi_descenso()
        self.assertGreater(psi, 0.99)
        self.assertLessEqual(psi, 1.0)

    def test_psi_above_umbral(self):
        """psi_descenso() debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.dp.psi_descenso(), 0.888)

    def test_repr_contains_descenso(self):
        """__repr__ debe mencionar n_descenso."""
        self.assertIn("196.", repr(self.dp))


# ============================================================================
# TestMatrizKPi – 12 tests
# ============================================================================

class TestMatrizKPi(unittest.TestCase):
    """Tests para MatrizKPi."""

    def setUp(self):
        self.kpi = MatrizKPi()
        self._mat = self.kpi.construir()

    def test_construir_dimensiones(self):
        """construir() debe retornar una matriz 7×7."""
        m = self._mat
        self.assertEqual(len(m), 7)
        for fila in m:
            self.assertEqual(len(fila), 7)

    def test_es_simetrica(self):
        """K_π debe ser simétrica (autoadjunta)."""
        self.assertTrue(self.kpi.es_simetrica())

    def test_diagonal_igual_f0(self):
        """Los elementos diagonales deben ser f₀ = 141.7001 Hz."""
        for i in range(7):
            self.assertAlmostEqual(self._mat[i][i], _F0, places=4)

    def test_traza_formula(self):
        """traza() = N_guardianes · f₀."""
        expected = _N_GUARDIANES * _F0
        self.assertAlmostEqual(self.kpi.traza(), expected, places=4)

    def test_traza_positive(self):
        """traza() debe ser positiva."""
        self.assertGreater(self.kpi.traza(), 0.0)

    def test_lambda_max_positive(self):
        """λ_max de K_π debe ser positivo."""
        self.assertGreater(self.kpi.lambda_max(), 0.0)

    def test_lambda_min_negative(self):
        """λ_min de K_π debe ser negativo (espectro mixto)."""
        self.assertLess(self.kpi.lambda_min(), 0.0)

    def test_gap_espectral_positive(self):
        """gap_espectral() = λ_max − λ_min debe ser positivo."""
        self.assertGreater(self.kpi.gap_espectral(), 0.0)

    def test_gap_espectral_range(self):
        """gap_espectral() debe estar entre 2000 y 6000 Hz."""
        gap = self.kpi.gap_espectral()
        self.assertGreater(gap, 2000.0)
        self.assertLess(gap, 6000.0)

    def test_omega_target_formula(self):
        """omega_target debe ser f₀·(ϕ⁷−ϕ³)."""
        expected = _F0 * (_PHI ** 7 - _PHI ** 3)
        self.assertAlmostEqual(self.kpi.omega_target, expected, places=4)

    def test_psi_kpi_range(self):
        """psi_kpi() debe estar en (0.0, 1.0]."""
        psi = self.kpi.psi_kpi()
        self.assertGreater(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_psi_kpi_above_threshold(self):
        """psi_kpi() debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.kpi.psi_kpi(), 0.888)

    def test_psi_kpi_formula(self):
        """psi_kpi() = 1 − error_omega."""
        gap = self.kpi.gap_espectral()
        expected = max(0.0, 1.0 - abs(gap - self.kpi.omega_target) / self.kpi.omega_target)
        self.assertAlmostEqual(self.kpi.psi_kpi(), expected, places=6)

    def test_repr_contains_traza(self):
        """__repr__ debe mencionar traza."""
        self.assertIn("991.", repr(self.kpi))


# ============================================================================
# TestViscosidadEfectiva – 8 tests
# ============================================================================

class TestViscosidadEfectiva(unittest.TestCase):
    """Tests para ViscosidadEfectiva."""

    def setUp(self):
        self.ve = ViscosidadEfectiva()

    def test_mu_eff_value(self):
        """mu_eff() = 1/f₀."""
        self.assertAlmostEqual(self.ve.mu_eff(), 1.0 / _F0, places=10)

    def test_mu_eff_positive(self):
        """mu_eff() debe ser positivo."""
        self.assertGreater(self.ve.mu_eff(), 0.0)

    def test_producto_invariante_exacto(self):
        """producto_invariante() = μ_eff·f₀ debe ser exactamente 1.0."""
        self.assertAlmostEqual(self.ve.producto_invariante(), 1.0, places=10)

    def test_re_phi_positive(self):
        """re_phi() debe ser positivo para longitud > 0."""
        self.assertGreater(self.ve.re_phi(1.0), 0.0)

    def test_re_phi_formula(self):
        """re_phi(L) = ϕ³ · (L/λ_P)."""
        L = 1.0
        expected = (_PHI ** 3) * (L / _LAMBDA_P)
        self.assertAlmostEqual(self.ve.re_phi(L), expected, places=0)

    def test_re_phi_scales_linearly(self):
        """re_phi(2L) debe ser el doble de re_phi(L)."""
        self.assertAlmostEqual(
            self.ve.re_phi(2.0),
            2.0 * self.ve.re_phi(1.0),
            places=5,
        )

    def test_psi_viscosidad_exacto(self):
        """psi_viscosidad() debe ser 1.0 (invariante exacto)."""
        self.assertAlmostEqual(self.ve.psi_viscosidad(), 1.0, places=10)

    def test_psi_above_umbral(self):
        """psi_viscosidad() debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.ve.psi_viscosidad(), 0.888)

    def test_repr_contains_mu(self):
        """__repr__ debe mencionar μ_eff."""
        self.assertIn("7.05", repr(self.ve))


# ============================================================================
# TestFlujoLaminar – 9 tests
# ============================================================================

class TestFlujoLaminar(unittest.TestCase):
    """Tests para FlujoLaminar."""

    def setUp(self):
        self.fl = FlujoLaminar()

    def test_sigma_critica_default(self):
        """sigma_critica por defecto debe ser 0.5."""
        self.assertAlmostEqual(self.fl.sigma_critica, 0.5, places=10)

    def test_es_laminar_true(self):
        """es_laminar(0.5) debe retornar True."""
        self.assertTrue(self.fl.es_laminar(0.5))

    def test_es_laminar_false(self):
        """es_laminar(0.7) debe retornar False."""
        self.assertFalse(self.fl.es_laminar(0.7))

    def test_disipacion_aurea_positive(self):
        """disipacion_aurea() debe ser positivo."""
        self.assertGreater(self.fl.disipacion_aurea(), 0.0)

    def test_disipacion_aurea_formula(self):
        """disipacion_aurea() = ϕ / (N_pasos + N_guardianes)."""
        expected = _PHI / (_N_PASOS + _N_GUARDIANES)
        self.assertAlmostEqual(self.fl.disipacion_aurea(), expected, places=10)

    def test_coherencia_espectral_value(self):
        """coherencia_espectral() = ½·(1 + cos(π/2)) = 0.5."""
        self.assertAlmostEqual(self.fl.coherencia_espectral(), 0.5, places=10)

    def test_psi_flujo_threshold(self):
        """psi_flujo() debe ser exactamente 0.888."""
        self.assertAlmostEqual(self.fl.psi_flujo(), 0.888, places=3)

    def test_psi_flujo_equals_umbral(self):
        """psi_flujo() debe ser igual a psi_umbral."""
        self.assertAlmostEqual(self.fl.psi_flujo(), self.fl.psi_umbral, places=10)

    def test_psi_above_or_equal_umbral(self):
        """psi_flujo() debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.fl.psi_flujo(), 0.888)

    def test_repr_contains_sigma(self):
        """__repr__ debe mencionar la condición laminar."""
        self.assertIn("laminar=True", repr(self.fl))


# ============================================================================
# TestCoherenciaCascada – 10 tests
# ============================================================================

class TestCoherenciaCascada(unittest.TestCase):
    """Tests para CoherenciaCascada."""

    def _make_coh(self, **kwargs):
        defaults = dict(
            psi_compactificacion=0.999990,
            psi_descenso=0.997504,
            psi_kpi=0.995171,
            psi_viscosidad=1.0,
            psi_flujo=0.888,
        )
        defaults.update(kwargs)
        return CoherenciaCascada(**defaults)

    def test_psi_global_formula(self):
        """psi_global() = promedio ponderado (1,1,1.5,1,1.5)."""
        coh = self._make_coh()
        medidas = [0.999990, 0.997504, 0.995171, 1.0, 0.888]
        pesos = [1.0, 1.0, 1.5, 1.0, 1.5]
        expected = sum(p * m for p, m in zip(pesos, medidas)) / sum(pesos)
        self.assertAlmostEqual(coh.psi_global(), expected, places=6)

    def test_psi_global_above_umbral(self):
        """psi_global() debe ser ≥ 0.888."""
        coh = self._make_coh()
        self.assertGreaterEqual(coh.psi_global(), 0.888)

    def test_sello_activo_true(self):
        """sello_activo() debe ser True cuando Ψ ≥ 0.888."""
        coh = self._make_coh()
        self.assertTrue(coh.sello_activo())

    def test_sello_activo_false(self):
        """sello_activo() debe ser False cuando Ψ < 0.888."""
        coh = CoherenciaCascada(
            psi_compactificacion=0.5,
            psi_descenso=0.5,
            psi_kpi=0.5,
            psi_viscosidad=0.5,
            psi_flujo=0.5,
        )
        self.assertFalse(coh.sello_activo())

    def test_resumen_keys(self):
        """resumen() debe contener todas las claves esperadas."""
        coh = self._make_coh()
        keys = coh.resumen().keys()
        for k in [
            "psi_compactificacion", "psi_descenso", "psi_kpi",
            "psi_viscosidad", "psi_flujo", "psi_global",
        ]:
            self.assertIn(k, keys)

    def test_resumen_values_consistent(self):
        """Los valores en resumen() deben coincidir con los atributos."""
        coh = self._make_coh()
        r = coh.resumen()
        self.assertAlmostEqual(r["psi_kpi"], coh.psi_kpi, places=8)
        self.assertAlmostEqual(r["psi_global"], coh.psi_global(), places=8)

    def test_umbral_default(self):
        """psi_umbral por defecto debe ser 0.888."""
        coh = self._make_coh()
        self.assertAlmostEqual(coh.psi_umbral, 0.888, places=3)

    def test_all_ones_psi_global_one(self):
        """Cuando todas las Ψᵢ = 1.0, psi_global() debe ser 1.0."""
        coh = CoherenciaCascada(
            psi_compactificacion=1.0,
            psi_descenso=1.0,
            psi_kpi=1.0,
            psi_viscosidad=1.0,
            psi_flujo=1.0,
        )
        self.assertAlmostEqual(coh.psi_global(), 1.0, places=10)

    def test_repr_contains_activo(self):
        """__repr__ debe indicar ACTIVO cuando sello está activo."""
        coh = self._make_coh()
        self.assertIn("ACTIVO", repr(coh))

    def test_pesos_sum(self):
        """Los pesos internos deben sumar 6.0."""
        coh = self._make_coh()
        self.assertAlmostEqual(sum(coh._PESOS), 6.0, places=10)


# ============================================================================
# TestSistemaCascadaAurea – 8 tests
# ============================================================================

class TestSistemaCascadaAurea(unittest.TestCase):
    """Tests para SistemaCascadaAurea."""

    def setUp(self):
        self.sistema = SistemaCascadaAurea()

    def test_f0_default(self):
        """f0 del sistema por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.sistema.f0, 141.7001, places=4)

    def test_f_planck_large(self):
        """f_planck del sistema debe ser > 10⁴² Hz."""
        self.assertGreater(self.sistema.f_planck, 1e42)

    def test_invalid_f0_raises(self):
        """SistemaCascadaAurea(f0=0) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            SistemaCascadaAurea(f0=0.0)

    def test_invalid_f0_negative_raises(self):
        """SistemaCascadaAurea(f0=-1) debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            SistemaCascadaAurea(f0=-1.0)

    def test_f_planck_less_than_f0_raises(self):
        """f_planck ≤ f0 debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            SistemaCascadaAurea(f0=200.0, f_planck=100.0)

    def test_activar_returns_resultado(self):
        """activar() debe retornar un ResultadoCascadaAurea."""
        resultado = self.sistema.activar()
        self.assertIsInstance(resultado, ResultadoCascadaAurea)

    def test_sello_activo(self):
        """activar().sello_activo debe ser True."""
        self.assertTrue(self.sistema.activar().sello_activo)

    def test_psi_global_above_umbral(self):
        """activar().psi_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.sistema.activar().psi_global, 0.888)

    def test_repr_contains_f0(self):
        """__repr__ debe mencionar f0."""
        self.assertIn("141.7001", repr(self.sistema))


# ============================================================================
# TestResultadoCascadaAurea – 8 tests
# ============================================================================

class TestResultadoCascadaAurea(unittest.TestCase):
    """Tests para ResultadoCascadaAurea."""

    def setUp(self):
        self.resultado = SistemaCascadaAurea().activar()

    def test_f0_field(self):
        """Campo f0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.resultado.f0, 141.7001, places=4)

    def test_n_pasos_aureos_field(self):
        """Campo n_pasos_aureos debe ser 12."""
        self.assertEqual(self.resultado.n_pasos_aureos, 12)

    def test_n_descenso_field(self):
        """Campo n_descenso debe ser > 190."""
        self.assertGreater(self.resultado.n_descenso, 190.0)

    def test_phi_12_field(self):
        """Campo phi_12 debe ser ≈ 321.997."""
        self.assertAlmostEqual(self.resultado.phi_12, _PHI ** 12, places=4)

    def test_generaciones_phi_length(self):
        """Campo generaciones_phi debe tener 12 elementos."""
        self.assertEqual(len(self.resultado.generaciones_phi), 12)

    def test_gap_espectral_positive(self):
        """Campo gap_espectral debe ser positivo."""
        self.assertGreater(self.resultado.gap_espectral, 0.0)

    def test_mu_eff_field(self):
        """Campo mu_eff debe ser 1/f₀."""
        self.assertAlmostEqual(self.resultado.mu_eff, 1.0 / _F0, places=10)

    def test_sello_activo_field(self):
        """Campo sello_activo debe ser True."""
        self.assertTrue(self.resultado.sello_activo)

    def test_mensaje_nonempty(self):
        """Campo mensaje debe ser una cadena no vacía."""
        self.assertIsInstance(self.resultado.mensaje, str)
        self.assertGreater(len(self.resultado.mensaje), 0)

    def test_mensaje_activo_contiene_sello(self):
        """Cuando sello_activo=True, mensaje debe contener '∴CA∞³'."""
        if self.resultado.sello_activo:
            self.assertIn("∴CA∞³", self.resultado.mensaje)

    def test_psi_global_field(self):
        """Campo psi_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.resultado.psi_global, 0.888)


# ============================================================================
# TestCascadaAureaActivar – 10 tests
# ============================================================================

class TestCascadaAureaActivar(unittest.TestCase):
    """Tests para la API pública cascada_aurea_activar()."""

    def setUp(self):
        self.result = cascada_aurea_activar()

    def test_returns_dict(self):
        """cascada_aurea_activar() debe retornar un dict."""
        self.assertIsInstance(self.result, dict)

    def test_sello_activo(self):
        """sello_activo debe ser True."""
        self.assertTrue(self.result["sello_activo"])

    def test_psi_global_above_umbral(self):
        """psi_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.result["psi_global"], 0.888)

    def test_all_keys_present(self):
        """El resultado debe contener todas las claves esperadas."""
        expected_keys = [
            "f0_hz", "f_planck_hz", "n_pasos_aureos", "n_descenso",
            "n_decadas", "phi_12", "generaciones_phi", "lambda_max_kpi",
            "lambda_min_kpi", "gap_espectral", "omega_target", "mu_eff",
            "psi_compactificacion", "psi_descenso", "psi_kpi",
            "psi_viscosidad", "psi_flujo", "psi_global",
            "sello_activo", "mensaje",
        ]
        for key in expected_keys:
            self.assertIn(key, self.result, f"Clave faltante: {key}")

    def test_f0_hz_value(self):
        """f0_hz debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.result["f0_hz"], 141.7001, places=4)

    def test_n_pasos_aureos_value(self):
        """n_pasos_aureos debe ser 12."""
        self.assertEqual(self.result["n_pasos_aureos"], 12)

    def test_generaciones_phi_count(self):
        """generaciones_phi debe tener 12 elementos."""
        self.assertEqual(len(self.result["generaciones_phi"]), 12)

    def test_psi_viscosidad_uno(self):
        """psi_viscosidad debe ser 1.0 (invariante exacto)."""
        self.assertAlmostEqual(self.result["psi_viscosidad"], 1.0, places=6)

    def test_psi_flujo_threshold(self):
        """psi_flujo debe ser 0.888."""
        self.assertAlmostEqual(self.result["psi_flujo"], 0.888, places=3)

    def test_custom_f0(self):
        """cascada_aurea_activar(f0=100.0) debe funcionar y retornar un dict."""
        r = cascada_aurea_activar(f0=100.0)
        self.assertIsInstance(r, dict)
        self.assertAlmostEqual(r["f0_hz"], 100.0, places=4)

    def test_mensaje_activo(self):
        """mensaje debe contener ACTIVO cuando sello está activo."""
        self.assertIn("ACTIVO", self.result["mensaje"])


# ============================================================================
# TestUtilidades – 8 tests
# ============================================================================

class TestUtilidades(unittest.TestCase):
    """Tests para las utilidades internas de álgebra lineal."""

    def test_mv_identity(self):
        """_mv(I, v) debe retornar v."""
        I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        v = [1.0, 2.0, 3.0]
        result = _mv(I, v)
        for r, expected in zip(result, v):
            self.assertAlmostEqual(r, expected, places=10)

    def test_mv_zero_matrix(self):
        """_mv(0, v) debe retornar el vector cero."""
        Z = [[0, 0], [0, 0]]
        v = [3.0, 4.0]
        result = _mv(Z, v)
        for r in result:
            self.assertAlmostEqual(r, 0.0, places=10)

    def test_dot_orthogonal(self):
        """_dot([1,0], [0,1]) debe ser 0."""
        self.assertAlmostEqual(_dot([1.0, 0.0], [0.0, 1.0]), 0.0, places=10)

    def test_dot_parallel(self):
        """_dot([1,0], [2,0]) debe ser 2."""
        self.assertAlmostEqual(_dot([1.0, 0.0], [2.0, 0.0]), 2.0, places=10)

    def test_norm_unit_vector(self):
        """_norm([1,0,0]) debe ser 1."""
        self.assertAlmostEqual(_norm([1.0, 0.0, 0.0]), 1.0, places=10)

    def test_norm_pythagorean(self):
        """_norm([3,4]) debe ser 5."""
        self.assertAlmostEqual(_norm([3.0, 4.0]), 5.0, places=10)

    def test_lambda_max_diagonal(self):
        """λ_max de una matriz diagonal debe ser el mayor diagonal."""
        mat = [[3.0, 0.0], [0.0, 1.0]]
        lmax = _lambda_max_potencia(mat, 2)
        self.assertAlmostEqual(lmax, 3.0, places=8)

    def test_lambda_min_diagonal(self):
        """λ_min de una matriz diagonal debe ser el menor diagonal."""
        mat = [[3.0, 0.0], [0.0, 1.0]]
        lmin = _lambda_min_shift(mat, 2)
        self.assertAlmostEqual(lmin, 1.0, places=6)


# ============================================================================
# TestIntegracion – 5 tests
# ============================================================================

class TestIntegracion(unittest.TestCase):
    """Tests de integración: coherencia interna del sistema completo."""

    def setUp(self):
        self.sistema = SistemaCascadaAurea()
        self.resultado = self.sistema.activar()

    def test_psi_global_consistency(self):
        """psi_global del resultado debe coincidir con el cálculo manual."""
        pesos = [1.0, 1.0, 1.5, 1.0, 1.5]
        medidas = [
            self.resultado.psi_compactificacion,
            self.resultado.psi_descenso,
            self.resultado.psi_kpi,
            self.resultado.psi_viscosidad,
            self.resultado.psi_flujo,
        ]
        expected = sum(p * m for p, m in zip(pesos, medidas)) / sum(pesos)
        self.assertAlmostEqual(self.resultado.psi_global, expected, places=6)

    def test_todas_psis_en_rango(self):
        """Todas las Ψᵢ deben estar en [0, 1]."""
        for nombre, psi in [
            ("psi_compactificacion", self.resultado.psi_compactificacion),
            ("psi_descenso", self.resultado.psi_descenso),
            ("psi_kpi", self.resultado.psi_kpi),
            ("psi_viscosidad", self.resultado.psi_viscosidad),
            ("psi_flujo", self.resultado.psi_flujo),
        ]:
            self.assertGreaterEqual(psi, 0.0, f"{nombre} < 0")
            self.assertLessEqual(psi, 1.0, f"{nombre} > 1")

    def test_gap_vs_lambda(self):
        """gap_espectral debe ser lambda_max_kpi − lambda_min_kpi."""
        expected = self.resultado.lambda_max_kpi - self.resultado.lambda_min_kpi
        self.assertAlmostEqual(self.resultado.gap_espectral, expected, places=4)

    def test_mu_eff_times_f0(self):
        """mu_eff · f0 debe ser exactamente 1.0."""
        self.assertAlmostEqual(
            self.resultado.mu_eff * self.resultado.f0, 1.0, places=10
        )

    def test_phi_12_vs_generaciones(self):
        """phi_12 debe coincidir con el último elemento de generaciones_phi."""
        self.assertAlmostEqual(
            self.resultado.phi_12,
            self.resultado.generaciones_phi[-1],
            places=8,
        )


if __name__ == "__main__":
    unittest.main()
