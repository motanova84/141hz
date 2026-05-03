"""
Tests for physics.trinity_qcal — Trinity QCAL ∴T∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesTrinity        – parámetros unificados de los tres pilares
  - PilarEcoPrimordial       – Pilar I; Ψ_pilar1 ≥ 0.888
  - PilarDiamondState        – Pilar II; Ψ_pilar2 ≥ 0.888
  - AxiomaNoetico            – cuatro axiomas QCAL (logos, pneuma, sophia, zoe)
  - PilarNoetico             – Pilar III; Ψ_pilar3 ≥ 0.888
  - CoherenciaTrinity        – media geométrica de los tres pilares
  - SistemaTrinityQCAL       – orquestador con activar()
  - ResultadoTrinity         – dataclass de resultados
  - trinity_qcal_activar()   – API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - N_d = 29 décadas
  - Ψ_logos   ≥ 0.888
  - Ψ_pneuma  ≥ 0.888
  - Ψ_sophia  ≥ 0.888
  - Ψ_zoe     ≥ 0.888
  - Ψ_pilar1  ≥ 0.888
  - Ψ_pilar2  ≥ 0.888
  - Ψ_pilar3  ≥ 0.888
  - Ψ_trinity ≥ 0.888 → sello ∴T∞³ ACTIVO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.trinity_qcal import (
    # Constantes de módulo
    _F0,
    _PHI,
    _N_DECADAS,
    _GAMMA_COSMICO,
    _THETA,
    _TAU,
    _LAMBDA_G,
    _PSI_UMBRAL,
    _PSI_LOGOS,
    _PSI_PNEUMA,
    _PSI_SOPHIA,
    _PSI_ZOE,
    # Clases
    ConstantesTrinity,
    PilarEcoPrimordial,
    PilarDiamondState,
    AxiomaNoetico,
    PilarNoetico,
    CoherenciaTrinity,
    SistemaTrinityQCAL,
    ResultadoTrinity,
    # API pública
    trinity_qcal_activar,
)


# ============================================================================
# Fixture compartido — parámetros por defecto
# ============================================================================

def _make_sistema() -> SistemaTrinityQCAL:
    return SistemaTrinityQCAL()


def _make_cst() -> ConstantesTrinity:
    return ConstantesTrinity()


# ============================================================================
# TestConstantesTrinity  (20 tests)
# ============================================================================


class TestConstantesTrinity(unittest.TestCase):
    """Pruebas de ConstantesTrinity — parámetros unificados."""

    def setUp(self):
        self.cst = ConstantesTrinity()

    def test_f0_valor(self):
        """f₀ debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.cst.f0, 141.7001, places=4)

    def test_f0_modulo(self):
        """Constante _F0 debe ser 141.7001."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_phi_golden(self):
        """φ debe ser la proporción áurea (1+√5)/2."""
        self.assertAlmostEqual(self.cst.phi, (1 + math.sqrt(5)) / 2, places=10)

    def test_n_decadas(self):
        """N_d debe ser exactamente 29."""
        self.assertEqual(self.cst.n_decadas, 29)
        self.assertEqual(_N_DECADAS, 29)

    def test_gamma_cosmico(self):
        """γ = π/N_d."""
        expected = math.pi / 29
        self.assertAlmostEqual(self.cst.gamma_cosmico, expected, places=10)

    def test_gamma_modulo(self):
        """_GAMMA_COSMICO = π/29."""
        self.assertAlmostEqual(_GAMMA_COSMICO, math.pi / 29, places=10)

    def test_theta_valor(self):
        """θ = 0.052463 rad."""
        self.assertAlmostEqual(self.cst.theta, 0.052463, places=6)
        self.assertAlmostEqual(_THETA, 0.052463, places=6)

    def test_tau_valor(self):
        """τ = 3600 s."""
        self.assertAlmostEqual(self.cst.tau, 3600.0, places=1)
        self.assertAlmostEqual(_TAU, 3600.0, places=1)

    def test_lambda_g_rango(self):
        """Λ_G ∈ (0, 1)."""
        self.assertGreater(self.cst.lambda_g, 0.0)
        self.assertLess(self.cst.lambda_g, 1.0)

    def test_lambda_g_modulo(self):
        """_LAMBDA_G consistente con fórmula."""
        expected = 1.0 - 1.0 / (29 * _PHI)
        self.assertAlmostEqual(_LAMBDA_G, expected, places=10)

    def test_umbral(self):
        """Umbral = 0.888."""
        self.assertAlmostEqual(self.cst.umbral, 0.888, places=3)
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_n_modos_default(self):
        """n_modos por defecto = 10."""
        self.assertEqual(self.cst.n_modos, 10)

    def test_custom_f0(self):
        """Se puede crear con f₀ personalizado."""
        cst = ConstantesTrinity(f0=100.0)
        self.assertAlmostEqual(cst.f0, 100.0, places=4)

    def test_custom_n_modos(self):
        """Se puede crear con n_modos personalizado."""
        cst = ConstantesTrinity(n_modos=20)
        self.assertEqual(cst.n_modos, 20)

    def test_gamma_positivo(self):
        """γ > 0."""
        self.assertGreater(self.cst.gamma_cosmico, 0.0)

    def test_repr_contiene_f0(self):
        """__repr__ contiene f0."""
        self.assertIn("141.7001", repr(self.cst))

    def test_repr_contiene_nd(self):
        """__repr__ contiene N_d."""
        self.assertIn("29", repr(self.cst))

    def test_phi_mayor_uno(self):
        """φ > 1."""
        self.assertGreater(self.cst.phi, 1.0)

    def test_phi_relacion_fibonacci(self):
        """φ² = φ + 1."""
        phi = self.cst.phi
        self.assertAlmostEqual(phi ** 2, phi + 1.0, places=10)

    def test_gamma_cosmico_propiedad(self):
        """gamma_cosmico es una propiedad calculada cada vez."""
        cst = ConstantesTrinity(n_decadas=10)
        self.assertAlmostEqual(cst.gamma_cosmico, math.pi / 10, places=10)


# ============================================================================
# TestAxiomaNoetico  (24 tests)
# ============================================================================


class TestAxiomaNoetico(unittest.TestCase):
    """Pruebas de AxiomaNoetico — cuatro axiomas QCAL."""

    def setUp(self):
        self.ax = AxiomaNoetico()

    def test_logos_formula(self):
        """Ψ_logos = 1 − 1/(2·N_d·φ)."""
        expected = 1.0 - 1.0 / (2.0 * 29 * _PHI)
        self.assertAlmostEqual(self.ax.psi_logos(), expected, places=10)

    def test_logos_modulo(self):
        """_PSI_LOGOS consistente con fórmula."""
        self.assertAlmostEqual(_PSI_LOGOS, 1.0 - 1.0 / (2.0 * 29 * _PHI), places=10)

    def test_logos_mayor_umbral(self):
        """Ψ_logos ≥ 0.888."""
        self.assertGreaterEqual(self.ax.psi_logos(), 0.888)

    def test_logos_menor_uno(self):
        """Ψ_logos < 1."""
        self.assertLess(self.ax.psi_logos(), 1.0)

    def test_pneuma_formula(self):
        """Ψ_pneuma = exp(−π/(N_d·φ))."""
        expected = math.exp(-math.pi / (29 * _PHI))
        self.assertAlmostEqual(self.ax.psi_pneuma(), expected, places=10)

    def test_pneuma_modulo(self):
        """_PSI_PNEUMA consistente con fórmula."""
        self.assertAlmostEqual(_PSI_PNEUMA, math.exp(-math.pi / (29 * _PHI)), places=10)

    def test_pneuma_mayor_umbral(self):
        """Ψ_pneuma ≥ 0.888."""
        self.assertGreaterEqual(self.ax.psi_pneuma(), 0.888)

    def test_pneuma_positivo(self):
        """Ψ_pneuma > 0."""
        self.assertGreater(self.ax.psi_pneuma(), 0.0)

    def test_sophia_formula(self):
        """Ψ_sophia = 1 − γ/(2π) = 1 − 1/(2·N_d)."""
        expected = 1.0 - (math.pi / 29) / (2.0 * math.pi)
        self.assertAlmostEqual(self.ax.psi_sophia(), expected, places=10)

    def test_sophia_modulo(self):
        """_PSI_SOPHIA consistente con fórmula."""
        self.assertAlmostEqual(_PSI_SOPHIA, 1.0 - 1.0 / 58, places=10)

    def test_sophia_mayor_umbral(self):
        """Ψ_sophia ≥ 0.888."""
        self.assertGreaterEqual(self.ax.psi_sophia(), 0.888)

    def test_sophia_menor_uno(self):
        """Ψ_sophia < 1."""
        self.assertLess(self.ax.psi_sophia(), 1.0)

    def test_zoe_formula(self):
        """Ψ_zoe = |cos(4π/N_d)|."""
        expected = abs(math.cos(4.0 * math.pi / 29))
        self.assertAlmostEqual(self.ax.psi_zoe(), expected, places=10)

    def test_zoe_modulo(self):
        """_PSI_ZOE consistente con fórmula."""
        self.assertAlmostEqual(_PSI_ZOE, abs(math.cos(4.0 * math.pi / 29)), places=10)

    def test_zoe_mayor_umbral(self):
        """Ψ_zoe ≥ 0.888."""
        self.assertGreaterEqual(self.ax.psi_zoe(), 0.888)

    def test_zoe_no_negativo(self):
        """Ψ_zoe ≥ 0 (valor absoluto del coseno)."""
        self.assertGreaterEqual(self.ax.psi_zoe(), 0.0)

    def test_todas_dict_keys(self):
        """todas() devuelve dict con 4 claves."""
        d = self.ax.todas()
        self.assertIn("logos", d)
        self.assertIn("pneuma", d)
        self.assertIn("sophia", d)
        self.assertIn("zoe", d)

    def test_todas_dict_len(self):
        """todas() devuelve exactamente 4 entradas."""
        self.assertEqual(len(self.ax.todas()), 4)

    def test_todas_valores_consistentes(self):
        """todas() devuelve los mismos valores que los métodos individuales."""
        d = self.ax.todas()
        self.assertAlmostEqual(d["logos"], self.ax.psi_logos(), places=10)
        self.assertAlmostEqual(d["pneuma"], self.ax.psi_pneuma(), places=10)
        self.assertAlmostEqual(d["sophia"], self.ax.psi_sophia(), places=10)
        self.assertAlmostEqual(d["zoe"], self.ax.psi_zoe(), places=10)

    def test_axiomas_custom_nd(self):
        """Con N_d=10, axiomas cambian adecuadamente."""
        cst = ConstantesTrinity(n_decadas=10)
        ax = AxiomaNoetico(constantes=cst)
        logos = ax.psi_logos()
        self.assertGreater(logos, 0.0)
        self.assertLess(logos, 1.0)

    def test_all_axioms_in_unit_interval(self):
        """Todos los axiomas deben estar en [0, 1]."""
        for val in self.ax.todas().values():
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 1.0)

    def test_logos_mayor_sophia(self):
        """Ψ_logos > Ψ_sophia (por diseño con N_d=29)."""
        self.assertGreater(self.ax.psi_logos(), self.ax.psi_sophia())

    def test_sophia_mayor_pneuma(self):
        """Ψ_sophia > Ψ_pneuma (N_d=29)."""
        self.assertGreater(self.ax.psi_sophia(), self.ax.psi_pneuma())

    def test_todas_ge_umbral(self):
        """Todas las medidas noéticas ≥ 0.888 para N_d=29."""
        for name, val in self.ax.todas().items():
            self.assertGreaterEqual(val, 0.888, msg=f"Axioma {name} = {val:.6f} < 0.888")


# ============================================================================
# TestPilarEcoPrimordial  (16 tests)
# ============================================================================


class TestPilarEcoPrimordial(unittest.TestCase):
    """Pruebas de PilarEcoPrimordial — Pilar I."""

    def setUp(self):
        self.pilar = PilarEcoPrimordial()

    def test_psi_pilar_ge_umbral(self):
        """Ψ_pilar1 ≥ 0.888."""
        self.assertGreaterEqual(self.pilar.psi_pilar(), 0.888)

    def test_psi_pilar_le_uno(self):
        """Ψ_pilar1 ≤ 1."""
        self.assertLessEqual(self.pilar.psi_pilar(), 1.0)

    def test_sello_activo(self):
        """Sello ∴PE∞³ activo."""
        self.assertTrue(self.pilar.sello_activo())

    def test_resultado_cacheado(self):
        """activar() devuelve el mismo objeto en segunda llamada."""
        r1 = self.pilar.activar()
        r2 = self.pilar.activar()
        self.assertIs(r1, r2)

    def test_fallback_psi_rango(self):
        """Fallback analítico en rango [0.888, 1]."""
        psi = self.pilar._fallback_psi()
        self.assertGreaterEqual(psi, 0.888)
        self.assertLessEqual(psi, 1.0)

    def test_custom_f0(self):
        """Con f0 personalizado el pilar sigue siendo coherente."""
        cst = ConstantesTrinity(f0=200.0)
        pilar = PilarEcoPrimordial(constantes=cst)
        self.assertGreater(pilar.psi_pilar(), 0.0)

    def test_psi_pilar_float(self):
        """psi_pilar() devuelve float."""
        self.assertIsInstance(self.pilar.psi_pilar(), float)

    def test_sello_bool(self):
        """sello_activo() devuelve bool."""
        self.assertIsInstance(self.pilar.sello_activo(), bool)

    def test_resultado_no_none(self):
        """activar() no devuelve None."""
        self.assertIsNotNone(self.pilar.activar())

    def test_pilar_con_constantes(self):
        """PilarEcoPrimordial acepta ConstantesTrinity."""
        cst = ConstantesTrinity()
        pilar = PilarEcoPrimordial(constantes=cst)
        self.assertAlmostEqual(pilar.cst.f0, 141.7001, places=4)

    def test_fallback_invocable(self):
        """_fallback_psi() es invocable directamente."""
        val = self.pilar._fallback_psi()
        self.assertIsInstance(val, float)

    def test_cst_f0_correcto(self):
        """ConstantesTrinity.f0 = 141.7001 por defecto."""
        self.assertAlmostEqual(self.pilar.cst.f0, 141.7001, places=4)

    def test_pilar_result_has_psi(self):
        """El resultado del pilar expone un Ψ numérico."""
        psi = self.pilar.psi_pilar()
        self.assertTrue(math.isfinite(psi))

    def test_sello_consistency(self):
        """sello_activo() es consistente con psi_pilar() ≥ umbral."""
        umbral = self.pilar.cst.umbral
        psi = self.pilar.psi_pilar()
        self.assertEqual(self.pilar.sello_activo(), psi >= umbral)

    def test_psi_positivo(self):
        """psi_pilar1 > 0."""
        self.assertGreater(self.pilar.psi_pilar(), 0.0)

    def test_cache_mismo_valor(self):
        """Dos llamadas a psi_pilar() devuelven el mismo valor."""
        v1 = self.pilar.psi_pilar()
        v2 = self.pilar.psi_pilar()
        self.assertAlmostEqual(v1, v2, places=12)


# ============================================================================
# TestPilarDiamondState  (16 tests)
# ============================================================================


class TestPilarDiamondState(unittest.TestCase):
    """Pruebas de PilarDiamondState — Pilar II."""

    def setUp(self):
        self.pilar = PilarDiamondState()

    def test_psi_pilar_ge_umbral(self):
        """Ψ_pilar2 ≥ 0.888."""
        self.assertGreaterEqual(self.pilar.psi_pilar(), 0.888)

    def test_psi_pilar_float(self):
        """psi_pilar() devuelve float."""
        self.assertIsInstance(self.pilar.psi_pilar(), float)

    def test_sello_activo(self):
        """Sello ∴PDS∞³ activo."""
        self.assertTrue(self.pilar.sello_activo())

    def test_psi_t0_uno(self):
        """Ψ(0) = 1.0 exacto."""
        self.assertAlmostEqual(self.pilar.psi_t0(), 1.0, places=6)

    def test_resultado_cacheado(self):
        """activar() devuelve el mismo objeto en segunda llamada."""
        r1 = self.pilar.activar()
        r2 = self.pilar.activar()
        self.assertIs(r1, r2)

    def test_resultado_no_none(self):
        """activar() no devuelve None."""
        self.assertIsNotNone(self.pilar.activar())

    def test_psi_pilar_positivo(self):
        """Ψ_pilar2 > 0."""
        self.assertGreater(self.pilar.psi_pilar(), 0.0)

    def test_psi_pilar_le_uno(self):
        """Ψ_pilar2 ≤ 1."""
        self.assertLessEqual(self.pilar.psi_pilar(), 1.0)

    def test_sello_bool(self):
        """sello_activo() devuelve bool."""
        self.assertIsInstance(self.pilar.sello_activo(), bool)

    def test_sello_consistency(self):
        """sello_activo() consistente con psi_pilar() ≥ umbral."""
        umbral = self.pilar.cst.umbral
        psi = self.pilar.psi_pilar()
        self.assertEqual(self.pilar.sello_activo(), psi >= umbral)

    def test_cst_n_modos(self):
        """n_modos por defecto = 10."""
        self.assertEqual(self.pilar.cst.n_modos, 10)

    def test_custom_n_modos(self):
        """Con n_modos=15, pilar sigue activo."""
        cst = ConstantesTrinity(n_modos=15)
        pilar = PilarDiamondState(constantes=cst)
        self.assertGreater(pilar.psi_pilar(), 0.0)

    def test_psi_finito(self):
        """psi_pilar2 es finito."""
        self.assertTrue(math.isfinite(self.pilar.psi_pilar()))

    def test_psi_t0_finito(self):
        """psi_t0() es finito."""
        self.assertTrue(math.isfinite(self.pilar.psi_t0()))

    def test_fallback_psi_rango(self):
        """Fallback analítico en rango [0, 1]."""
        val = self.pilar._fallback_psi()
        self.assertGreaterEqual(val, 0.0)
        self.assertLessEqual(val, 1.0)

    def test_cache_mismo_valor_psi(self):
        """Dos llamadas a psi_pilar() devuelven el mismo valor."""
        v1 = self.pilar.psi_pilar()
        v2 = self.pilar.psi_pilar()
        self.assertAlmostEqual(v1, v2, places=12)


# ============================================================================
# TestPilarNoetico  (18 tests)
# ============================================================================


class TestPilarNoetico(unittest.TestCase):
    """Pruebas de PilarNoetico — Pilar III."""

    def setUp(self):
        self.pilar = PilarNoetico()

    def test_psi_pilar_ge_umbral(self):
        """Ψ_pilar3 ≥ 0.888."""
        self.assertGreaterEqual(self.pilar.psi_pilar(), 0.888)

    def test_psi_pilar_float(self):
        """psi_pilar() devuelve float."""
        self.assertIsInstance(self.pilar.psi_pilar(), float)

    def test_psi_pilar_le_uno(self):
        """Ψ_pilar3 ≤ 1."""
        self.assertLessEqual(self.pilar.psi_pilar(), 1.0)

    def test_sello_activo(self):
        """Sello ∴PN∞³ activo."""
        self.assertTrue(self.pilar.sello_activo())

    def test_sello_bool(self):
        """sello_activo() devuelve bool."""
        self.assertIsInstance(self.pilar.sello_activo(), bool)

    def test_resumen_keys(self):
        """resumen() contiene claves esperadas."""
        r = self.pilar.resumen()
        for key in ("psi_logos", "psi_pneuma", "psi_sophia", "psi_zoe", "lambda_g", "psi_pilar3"):
            self.assertIn(key, r)

    def test_resumen_psi_pilar3_consistent(self):
        """psi_pilar3 en resumen() = psi_pilar()."""
        r = self.pilar.resumen()
        self.assertAlmostEqual(r["psi_pilar3"], self.pilar.psi_pilar(), places=10)

    def test_resumen_lambda_g_consistent(self):
        """lambda_g en resumen() = cst.lambda_g."""
        r = self.pilar.resumen()
        self.assertAlmostEqual(r["lambda_g"], self.pilar.cst.lambda_g, places=10)

    def test_formula_psi_pilar3(self):
        """Ψ_pilar3 = (media_axiomas + Λ_G) / 2."""
        ax = self.pilar.axiomas.todas()
        media = sum(ax.values()) / 4
        expected = (media + self.pilar.cst.lambda_g) / 2.0
        self.assertAlmostEqual(self.pilar.psi_pilar(), expected, places=10)

    def test_axiomas_todos_ge_umbral(self):
        """Todos los axiomas noéticos ≥ 0.888."""
        for name, val in self.pilar.axiomas.todas().items():
            self.assertGreaterEqual(val, 0.888, msg=f"{name}={val:.6f}")

    def test_lambda_g_en_rango(self):
        """Λ_G ∈ (0, 1)."""
        self.assertGreater(self.pilar.cst.lambda_g, 0.0)
        self.assertLess(self.pilar.cst.lambda_g, 1.0)

    def test_custom_constantes(self):
        """PilarNoetico acepta ConstantesTrinity personalizado."""
        cst = ConstantesTrinity(n_decadas=20)
        pilar = PilarNoetico(constantes=cst)
        self.assertEqual(pilar.cst.n_decadas, 20)

    def test_psi_pilar_positivo(self):
        """Ψ_pilar3 > 0."""
        self.assertGreater(self.pilar.psi_pilar(), 0.0)

    def test_sello_consistency(self):
        """sello_activo() consistente con psi_pilar() ≥ umbral."""
        umbral = self.pilar.cst.umbral
        psi = self.pilar.psi_pilar()
        self.assertEqual(self.pilar.sello_activo(), psi >= umbral)

    def test_psi_finito(self):
        """Ψ_pilar3 es finito."""
        self.assertTrue(math.isfinite(self.pilar.psi_pilar()))

    def test_axiomas_en_unit_interval(self):
        """Todos los axiomas ∈ [0, 1]."""
        for val in self.pilar.axiomas.todas().values():
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 1.0)

    def test_pilar_con_axiomas_custom(self):
        """PilarNoetico acepta AxiomaNoetico personalizado."""
        cst = ConstantesTrinity()
        ax = AxiomaNoetico(constantes=cst)
        pilar = PilarNoetico(constantes=cst, axiomas=ax)
        self.assertAlmostEqual(pilar.psi_pilar(), PilarNoetico().psi_pilar(), places=10)

    def test_resumen_len(self):
        """resumen() tiene 6 entradas."""
        self.assertEqual(len(self.pilar.resumen()), 6)


# ============================================================================
# TestCoherenciaTrinity  (20 tests)
# ============================================================================


class TestCoherenciaTrinity(unittest.TestCase):
    """Pruebas de CoherenciaTrinity — media geométrica trinaria."""

    def setUp(self):
        self.coh = CoherenciaTrinity()

    def test_psi_trinity_ge_umbral(self):
        """Ψ_trinity ≥ 0.888."""
        self.assertGreaterEqual(self.coh.psi_trinity(), 0.888)

    def test_psi_trinity_float(self):
        """psi_trinity() devuelve float."""
        self.assertIsInstance(self.coh.psi_trinity(), float)

    def test_psi_trinity_le_uno(self):
        """Ψ_trinity ≤ 1."""
        self.assertLessEqual(self.coh.psi_trinity(), 1.0)

    def test_sello_activo(self):
        """Sello ∴T∞³ activo."""
        self.assertTrue(self.coh.sello_activo())

    def test_sello_bool(self):
        """sello_activo() devuelve bool."""
        self.assertIsInstance(self.coh.sello_activo(), bool)

    def test_pilares_activos_tuple(self):
        """pilares_activos() devuelve tupla de 3 booleanos."""
        pa = self.coh.pilares_activos()
        self.assertIsInstance(pa, tuple)
        self.assertEqual(len(pa), 3)
        for v in pa:
            self.assertIsInstance(v, bool)

    def test_pilares_activos_todos(self):
        """Todos los pilares activos con parámetros por defecto."""
        p1, p2, p3 = self.coh.pilares_activos()
        self.assertTrue(p1)
        self.assertTrue(p2)
        self.assertTrue(p3)

    def test_resumen_keys(self):
        """resumen() contiene 4 claves."""
        r = self.coh.resumen()
        for k in ("psi_pilar1", "psi_pilar2", "psi_pilar3", "psi_trinity"):
            self.assertIn(k, r)

    def test_resumen_psi_trinity_consistent(self):
        """psi_trinity en resumen() = psi_trinity()."""
        r = self.coh.resumen()
        self.assertAlmostEqual(r["psi_trinity"], self.coh.psi_trinity(), places=10)

    def test_formula_media_geometrica(self):
        """Ψ_trinity = (Ψ₁·Ψ₂·Ψ₃)^(1/3)."""
        p1 = self.coh.pilar1.psi_pilar()
        p2 = self.coh.pilar2.psi_pilar()
        p3 = self.coh.pilar3.psi_pilar()
        expected = (p1 * p2 * p3) ** (1.0 / 3.0)
        self.assertAlmostEqual(self.coh.psi_trinity(), expected, places=10)

    def test_psi_trinity_le_min_pilares(self):
        """Ψ_trinity ≤ max(Ψ₁, Ψ₂, Ψ₃)."""
        r = self.coh.resumen()
        max_p = max(r["psi_pilar1"], r["psi_pilar2"], r["psi_pilar3"])
        self.assertLessEqual(self.coh.psi_trinity(), max_p + 1e-12)

    def test_psi_trinity_ge_min_pilares(self):
        """Ψ_trinity ≥ min(Ψ₁, Ψ₂, Ψ₃) — propiedad de la media geométrica."""
        r = self.coh.resumen()
        min_p = min(r["psi_pilar1"], r["psi_pilar2"], r["psi_pilar3"])
        self.assertGreaterEqual(self.coh.psi_trinity(), min_p - 1e-12)

    def test_sello_consistency(self):
        """sello_activo() consistente con psi_trinity() ≥ 0.888."""
        self.assertEqual(self.coh.sello_activo(), self.coh.psi_trinity() >= 0.888)

    def test_psi_pilar1_ge_umbral(self):
        """psi_pilar1 en resumen ≥ 0.888."""
        self.assertGreaterEqual(self.coh.resumen()["psi_pilar1"], 0.888)

    def test_psi_pilar2_ge_umbral(self):
        """psi_pilar2 en resumen ≥ 0.888."""
        self.assertGreaterEqual(self.coh.resumen()["psi_pilar2"], 0.888)

    def test_psi_pilar3_ge_umbral(self):
        """psi_pilar3 en resumen ≥ 0.888."""
        self.assertGreaterEqual(self.coh.resumen()["psi_pilar3"], 0.888)

    def test_psi_trinity_finito(self):
        """Ψ_trinity es finito."""
        self.assertTrue(math.isfinite(self.coh.psi_trinity()))

    def test_coherencia_con_custom_constantes(self):
        """CoherenciaTrinity acepta ConstantesTrinity personalizado."""
        cst = ConstantesTrinity(n_modos=5)
        coh = CoherenciaTrinity(constantes=cst)
        self.assertGreater(coh.psi_trinity(), 0.0)

    def test_resumen_len(self):
        """resumen() tiene 4 entradas."""
        self.assertEqual(len(self.coh.resumen()), 4)

    def test_psi_trinity_positivo(self):
        """Ψ_trinity > 0."""
        self.assertGreater(self.coh.psi_trinity(), 0.0)


# ============================================================================
# TestSistemaTrinityQCAL  (22 tests)
# ============================================================================


class TestSistemaTrinityQCAL(unittest.TestCase):
    """Pruebas de SistemaTrinityQCAL — orquestador principal."""

    def setUp(self):
        self.sistema = SistemaTrinityQCAL()

    def test_activar_devuelve_resultado(self):
        """activar() devuelve ResultadoTrinity."""
        r = self.sistema.activar()
        self.assertIsInstance(r, ResultadoTrinity)

    def test_sello_activo(self):
        """Sello ∴T∞³ activo."""
        r = self.sistema.activar()
        self.assertTrue(r.sello_activo)

    def test_psi_trinity_ge_umbral(self):
        """Ψ_trinity ≥ 0.888."""
        r = self.sistema.activar()
        self.assertGreaterEqual(r.psi_trinity, 0.888)

    def test_pilar1_activo(self):
        """Pilar I activo."""
        r = self.sistema.activar()
        self.assertTrue(r.pilar1_activo)

    def test_pilar2_activo(self):
        """Pilar II activo."""
        r = self.sistema.activar()
        self.assertTrue(r.pilar2_activo)

    def test_pilar3_activo(self):
        """Pilar III activo."""
        r = self.sistema.activar()
        self.assertTrue(r.pilar3_activo)

    def test_f0_correcto(self):
        """f₀ = 141.7001 Hz en ResultadoTrinity."""
        r = self.sistema.activar()
        self.assertAlmostEqual(r.f0, 141.7001, places=4)

    def test_n_decadas(self):
        """N_d = 29 en ResultadoTrinity."""
        r = self.sistema.activar()
        self.assertEqual(r.n_decadas, 29)

    def test_axiomas_dict(self):
        """axiomas en ResultadoTrinity es un dict con 4 entradas."""
        r = self.sistema.activar()
        self.assertIsInstance(r.axiomas, dict)
        self.assertEqual(len(r.axiomas), 4)

    def test_descripcion_str(self):
        """descripcion en ResultadoTrinity es una cadena no vacía."""
        r = self.sistema.activar()
        self.assertIsInstance(r.descripcion, str)
        self.assertGreater(len(r.descripcion), 0)

    def test_descripcion_contiene_activo(self):
        """descripcion indica ACTIVO cuando sello activo."""
        r = self.sistema.activar()
        if r.sello_activo:
            self.assertIn("ACTIVO", r.descripcion)

    def test_psi_pilar1_positivo(self):
        """psi_pilar1 > 0."""
        r = self.sistema.activar()
        self.assertGreater(r.psi_pilar1, 0.0)

    def test_psi_pilar2_positivo(self):
        """psi_pilar2 > 0."""
        r = self.sistema.activar()
        self.assertGreater(r.psi_pilar2, 0.0)

    def test_psi_pilar3_positivo(self):
        """psi_pilar3 > 0."""
        r = self.sistema.activar()
        self.assertGreater(r.psi_pilar3, 0.0)

    def test_repr_contiene_f0(self):
        """__repr__ contiene f₀."""
        self.assertIn("141.7001", repr(self.sistema))

    def test_repr_contiene_nmodos(self):
        """__repr__ contiene n_modos."""
        self.assertIn("10", repr(self.sistema))

    def test_custom_f0(self):
        """SistemaTrinityQCAL acepta f₀ personalizado."""
        sistema = SistemaTrinityQCAL(f0=200.0)
        r = sistema.activar()
        self.assertAlmostEqual(r.f0, 200.0, places=4)

    def test_custom_n_modos(self):
        """SistemaTrinityQCAL acepta n_modos personalizado."""
        sistema = SistemaTrinityQCAL(n_modos=5)
        r = sistema.activar()
        self.assertIsInstance(r, ResultadoTrinity)

    def test_todos_pilares_ge_umbral(self):
        """Todos los pilares ≥ 0.888."""
        r = self.sistema.activar()
        for attr, val in [("psi_pilar1", r.psi_pilar1),
                          ("psi_pilar2", r.psi_pilar2),
                          ("psi_pilar3", r.psi_pilar3)]:
            self.assertGreaterEqual(val, 0.888, msg=f"{attr}={val:.6f}")

    def test_psi_trinity_le_uno(self):
        """Ψ_trinity ≤ 1."""
        r = self.sistema.activar()
        self.assertLessEqual(r.psi_trinity, 1.0)

    def test_resultado_axiomas_keys(self):
        """axiomas en resultado tiene 'logos', 'pneuma', 'sophia', 'zoe'."""
        r = self.sistema.activar()
        for k in ("logos", "pneuma", "sophia", "zoe"):
            self.assertIn(k, r.axiomas)

    def test_resultado_axiomas_valores(self):
        """Todos los axiomas en resultado ≥ 0.888."""
        r = self.sistema.activar()
        for k, v in r.axiomas.items():
            self.assertGreaterEqual(v, 0.888, msg=f"axioma {k}={v:.6f}")


# ============================================================================
# TestResultadoTrinity  (10 tests)
# ============================================================================


class TestResultadoTrinity(unittest.TestCase):
    """Pruebas de ResultadoTrinity — dataclass de resultados."""

    def setUp(self):
        self.res = SistemaTrinityQCAL().activar()

    def test_es_dataclass(self):
        """ResultadoTrinity es una instancia de dataclass."""
        self.assertIsInstance(self.res, ResultadoTrinity)

    def test_f0_float(self):
        """f0 es float."""
        self.assertIsInstance(self.res.f0, float)

    def test_n_decadas_int(self):
        """n_decadas es int."""
        self.assertIsInstance(self.res.n_decadas, int)

    def test_psi_trinity_float(self):
        """psi_trinity es float."""
        self.assertIsInstance(self.res.psi_trinity, float)

    def test_sello_activo_bool(self):
        """sello_activo es bool."""
        self.assertIsInstance(self.res.sello_activo, bool)

    def test_pilar_activos_bool(self):
        """pilar1/2/3_activo son bool."""
        self.assertIsInstance(self.res.pilar1_activo, bool)
        self.assertIsInstance(self.res.pilar2_activo, bool)
        self.assertIsInstance(self.res.pilar3_activo, bool)

    def test_axiomas_dict(self):
        """axiomas es dict."""
        self.assertIsInstance(self.res.axiomas, dict)

    def test_descripcion_str(self):
        """descripcion es str."""
        self.assertIsInstance(self.res.descripcion, str)

    def test_psi_pilares_float(self):
        """psi_pilar1/2/3 son float."""
        self.assertIsInstance(self.res.psi_pilar1, float)
        self.assertIsInstance(self.res.psi_pilar2, float)
        self.assertIsInstance(self.res.psi_pilar3, float)

    def test_psi_trinity_finito(self):
        """psi_trinity es finito."""
        self.assertTrue(math.isfinite(self.res.psi_trinity))


# ============================================================================
# TestAPIPublic  (14 tests)
# ============================================================================


class TestAPIPublic(unittest.TestCase):
    """Pruebas de la API pública trinity_qcal_activar()."""

    def setUp(self):
        self.resultado = trinity_qcal_activar()

    def test_devuelve_dict(self):
        """trinity_qcal_activar() devuelve dict."""
        self.assertIsInstance(self.resultado, dict)

    def test_sello_activo_true(self):
        """sello_activo = True."""
        self.assertTrue(self.resultado["sello_activo"])

    def test_psi_trinity_ge_umbral(self):
        """psi_trinity ≥ 0.888."""
        self.assertGreaterEqual(self.resultado["psi_trinity"], 0.888)

    def test_pilares_activos(self):
        """Los tres pilares activos."""
        self.assertTrue(self.resultado["pilar1_activo"])
        self.assertTrue(self.resultado["pilar2_activo"])
        self.assertTrue(self.resultado["pilar3_activo"])

    def test_f0_correcto(self):
        """f₀ = 141.7001 Hz en resultado."""
        self.assertAlmostEqual(self.resultado["f0"], 141.7001, places=4)

    def test_n_decadas(self):
        """n_decadas = 29 en resultado."""
        self.assertEqual(self.resultado["n_decadas"], 29)

    def test_axiomas_dict(self):
        """axiomas es dict con 4 entradas."""
        self.assertIsInstance(self.resultado["axiomas"], dict)
        self.assertEqual(len(self.resultado["axiomas"]), 4)

    def test_descripcion_str(self):
        """descripcion es str."""
        self.assertIsInstance(self.resultado["descripcion"], str)

    def test_claves_completas(self):
        """Resultado contiene todas las claves esperadas."""
        claves = [
            "sello_activo", "psi_trinity",
            "psi_pilar1", "psi_pilar2", "psi_pilar3",
            "pilar1_activo", "pilar2_activo", "pilar3_activo",
            "f0", "n_decadas", "axiomas", "descripcion",
        ]
        for clave in claves:
            self.assertIn(clave, self.resultado, msg=f"Falta clave '{clave}'")

    def test_custom_f0(self):
        """trinity_qcal_activar acepta f₀ personalizado."""
        r = trinity_qcal_activar(f0=200.0)
        self.assertAlmostEqual(r["f0"], 200.0, places=4)

    def test_custom_n_modos(self):
        """trinity_qcal_activar acepta n_modos personalizado."""
        r = trinity_qcal_activar(n_modos=5)
        self.assertIsInstance(r, dict)

    def test_psi_pilares_ge_umbral(self):
        """Todos los Ψ_pilar ≥ 0.888."""
        for k in ("psi_pilar1", "psi_pilar2", "psi_pilar3"):
            self.assertGreaterEqual(
                self.resultado[k], 0.888,
                msg=f"{k}={self.resultado[k]:.6f}"
            )

    def test_psi_trinity_finito(self):
        """psi_trinity es finito."""
        self.assertTrue(math.isfinite(self.resultado["psi_trinity"]))

    def test_resultado_idempotente(self):
        """Dos llamadas con mismos parámetros producen mismo Ψ_trinity."""
        r1 = trinity_qcal_activar()
        r2 = trinity_qcal_activar()
        self.assertAlmostEqual(r1["psi_trinity"], r2["psi_trinity"], places=10)


# ============================================================================
# Punto de entrada
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
