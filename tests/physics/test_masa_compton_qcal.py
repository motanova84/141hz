"""
Tests for physics.masa_compton_qcal — Límite de Compton y Acoplamiento λ

Pruebas que cubren las 5 clases y la función de la API pública:
  - MasaCompton          – masa en kg y eV desde h·f₀/c²
  - LongitudCompton      – λ̄_C = c/(2π·f₀) en m y km
  - AcoplamientoAutointeraccion – λ = m_ψ/M_P
  - LimitesExperimentales – 4 ventanas observacionales
  - SistemaMasaComptonQCAL – orquestador
  - masa_compton_qcal_calcular() – API pública

Invariantes clave verificados:
  - m_ψ ≈ 5,859×10⁻¹³ eV  (5,8e-13 < m_eV < 5,9e-13)
  - λ̄_C ≈ 336,7 km         (336,0 < lc_km < 337,5)
  - λ_auto ≈ 4,8×10⁻⁴¹    (4e-41 < λ < 6e-41)
  - compatible_experimental = True
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.masa_compton_qcal import (
    # Constants (module-level)
    _F0,
    _H,
    _HBAR,
    _C,
    _EV_TO_J,
    _M_PLANCK_EV,
    _M_PSI_KG,
    _M_PSI_EV,
    _LAMBDA_C_M,
    _LAMBDA_AUTO,
    _SIGMA_SOBRE_M_CM2_G,
    _DELTA_ALPHA_SOBRE_ALPHA,
    # Classes
    MasaCompton,
    LongitudCompton,
    AcoplamientoAutointeraccion,
    LimitesExperimentales,
    SistemaMasaComptonQCAL,
    ResultadoMasaCompton,
    # Public API
    masa_compton_qcal_calcular,
)


# ============================================================================
# TestModuleConstants – 12 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests for module-level constants."""

    def test_f0_value(self):
        """_F0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_h_planck_value(self):
        """_H must equal the CODATA 2018 Planck constant."""
        self.assertAlmostEqual(_H, 6.62607015e-34, places=42)

    def test_hbar_equals_h_over_2pi(self):
        """_HBAR must equal _H / (2π)."""
        self.assertAlmostEqual(_HBAR, _H / (2.0 * math.pi), places=44)

    def test_c_value(self):
        """_C must equal exact speed of light."""
        self.assertEqual(_C, 299_792_458.0)

    def test_ev_to_j_value(self):
        """_EV_TO_J must equal exact CODATA eV."""
        self.assertAlmostEqual(_EV_TO_J, 1.602176634e-19, places=28)

    def test_m_planck_eV_order(self):
        """Planck mass must be ~1.22×10²⁸ eV."""
        self.assertAlmostEqual(_M_PLANCK_EV, 1.22e28, delta=1e26)

    def test_m_psi_kg_order(self):
        """_M_PSI_KG must be ~1.04×10⁻⁴⁸ kg."""
        self.assertGreater(_M_PSI_KG, 1.04e-48)
        self.assertLess(_M_PSI_KG, 1.05e-48)

    def test_m_psi_eV_order(self):
        """_M_PSI_EV must be ~5.8–5.9×10⁻¹³ eV."""
        self.assertGreater(_M_PSI_EV, 5.8e-13)
        self.assertLess(_M_PSI_EV, 5.9e-13)

    def test_lambda_c_m_order(self):
        """_LAMBDA_C_M must be ~336,700 m."""
        self.assertGreater(_LAMBDA_C_M, 336_000.0)
        self.assertLess(_LAMBDA_C_M, 337_500.0)

    def test_lambda_auto_order(self):
        """_LAMBDA_AUTO must be ~4–6×10⁻⁴¹."""
        self.assertGreater(_LAMBDA_AUTO, 4.0e-41)
        self.assertLess(_LAMBDA_AUTO, 6.0e-41)

    def test_sigma_sobre_m_value(self):
        """_SIGMA_SOBRE_M_CM2_G must equal 1e-65."""
        self.assertAlmostEqual(_SIGMA_SOBRE_M_CM2_G, 1.0e-65, delta=1e-66)

    def test_delta_alpha_value(self):
        """_DELTA_ALPHA_SOBRE_ALPHA must equal 1e-18."""
        self.assertAlmostEqual(_DELTA_ALPHA_SOBRE_ALPHA, 1.0e-18, delta=1e-19)


# ============================================================================
# TestMasaCompton – 15 tests
# ============================================================================

class TestMasaCompton(unittest.TestCase):
    """Tests for MasaCompton class."""

    def setUp(self):
        self.mc = MasaCompton()

    def test_default_f0(self):
        """Default f0 must equal _F0."""
        self.assertAlmostEqual(self.mc.f0, _F0, places=4)

    def test_default_h(self):
        """Default h must equal _H."""
        self.assertAlmostEqual(self.mc.h, _H, places=42)

    def test_default_c(self):
        """Default c must equal _C."""
        self.assertEqual(self.mc.c, _C)

    def test_default_ev_to_j(self):
        """Default ev_to_j must equal _EV_TO_J."""
        self.assertAlmostEqual(self.mc.ev_to_j, _EV_TO_J, places=28)

    def test_masa_kg_formula(self):
        """masa_kg must equal h·f₀/c²."""
        expected = _H * _F0 / (_C ** 2)
        self.assertAlmostEqual(self.mc.masa_kg(), expected, places=55)

    def test_masa_kg_range(self):
        """masa_kg must be in [1.04e-48, 1.05e-48] kg."""
        m = self.mc.masa_kg()
        self.assertGreater(m, 1.04e-48)
        self.assertLess(m, 1.05e-48)

    def test_energia_J_equals_h_f0(self):
        """energia_J must equal h·f₀."""
        self.assertAlmostEqual(self.mc.energia_J(), _H * _F0, places=44)

    def test_energia_J_positive(self):
        """energia_J must be positive."""
        self.assertGreater(self.mc.energia_J(), 0.0)

    def test_masa_eV_formula(self):
        """masa_eV must equal masa_kg·c²/ev_to_j."""
        expected = self.mc.masa_kg() * (_C ** 2) / _EV_TO_J
        self.assertAlmostEqual(self.mc.masa_eV(), expected, places=25)

    def test_masa_eV_range(self):
        """masa_eV must be in [5.8e-13, 5.9e-13] eV."""
        m = self.mc.masa_eV()
        self.assertGreater(m, 5.8e-13)
        self.assertLess(m, 5.9e-13)

    def test_masa_eV_matches_module_constant(self):
        """masa_eV must match _M_PSI_EV."""
        self.assertAlmostEqual(self.mc.masa_eV(), _M_PSI_EV, places=25)

    def test_custom_f0_scales_mass(self):
        """Doubling f0 must double the mass."""
        mc2 = MasaCompton(f0=2 * _F0)
        self.assertAlmostEqual(mc2.masa_kg() / self.mc.masa_kg(), 2.0, places=10)

    def test_custom_f0_scales_energy(self):
        """Doubling f0 must double the energy."""
        mc2 = MasaCompton(f0=2 * _F0)
        self.assertAlmostEqual(mc2.energia_J() / self.mc.energia_J(), 2.0, places=10)

    def test_repr_contains_f0(self):
        """repr must mention f₀."""
        r = repr(self.mc)
        self.assertIn("141.7001", r)

    def test_repr_contains_kg(self):
        """repr must mention kg."""
        r = repr(self.mc)
        self.assertIn("kg", r)


# ============================================================================
# TestLongitudCompton – 15 tests
# ============================================================================

class TestLongitudCompton(unittest.TestCase):
    """Tests for LongitudCompton class."""

    def setUp(self):
        self.lc = LongitudCompton()

    def test_default_f0(self):
        """Default f0 must equal _F0."""
        self.assertAlmostEqual(self.lc.f0, _F0, places=4)

    def test_default_c(self):
        """Default c must equal _C."""
        self.assertEqual(self.lc.c, _C)

    def test_lambda_compton_m_formula(self):
        """lambda_compton_m must equal c/(2π·f₀)."""
        expected = _C / (2.0 * math.pi * _F0)
        self.assertAlmostEqual(self.lc.lambda_compton_m(), expected, places=6)

    def test_lambda_compton_m_range(self):
        """lambda_compton_m must be ~336,000–337,500 m."""
        lc_m = self.lc.lambda_compton_m()
        self.assertGreater(lc_m, 336_000.0)
        self.assertLess(lc_m, 337_500.0)

    def test_lambda_compton_m_matches_module_constant(self):
        """lambda_compton_m must match _LAMBDA_C_M."""
        self.assertAlmostEqual(self.lc.lambda_compton_m(), _LAMBDA_C_M, places=6)

    def test_lambda_compton_km_formula(self):
        """lambda_compton_km must equal lambda_compton_m / 1000."""
        self.assertAlmostEqual(
            self.lc.lambda_compton_km(),
            self.lc.lambda_compton_m() / 1_000.0,
            places=9,
        )

    def test_lambda_compton_km_range(self):
        """lambda_compton_km must be in [336.0, 337.5] km."""
        lc_km = self.lc.lambda_compton_km()
        self.assertGreater(lc_km, 336.0)
        self.assertLess(lc_km, 337.5)

    def test_interferometro_100km_dentro(self):
        """100 km interferometer must be within λ̄_C."""
        self.assertTrue(self.lc.interferometro_dentro_compton(100.0))

    def test_interferometro_337km_fuera(self):
        """337+ km interferometer must be outside λ̄_C."""
        self.assertFalse(self.lc.interferometro_dentro_compton(338.0))

    def test_interferometro_borde(self):
        """Interferometer exactly at λ̄_C must be outside (strict <)."""
        lc_km = self.lc.lambda_compton_km()
        self.assertFalse(self.lc.interferometro_dentro_compton(lc_km))

    def test_interferometro_ligo_4km(self):
        """LIGO 4 km arm must be well within λ̄_C."""
        self.assertTrue(self.lc.interferometro_dentro_compton(4.0))

    def test_interferometro_lunar_100km(self):
        """Lunar 100 km interferometer must be within λ̄_C."""
        self.assertTrue(self.lc.interferometro_dentro_compton(100.0))

    def test_custom_f0_scales_lambda(self):
        """Halving f0 must double λ̄_C."""
        lc2 = LongitudCompton(f0=_F0 / 2.0)
        self.assertAlmostEqual(
            lc2.lambda_compton_m() / self.lc.lambda_compton_m(), 2.0, places=10
        )

    def test_repr_contains_km(self):
        """repr must contain 'km'."""
        self.assertIn("km", repr(self.lc))

    def test_repr_contains_f0(self):
        """repr must mention frequency."""
        self.assertIn("141.7001", repr(self.lc))


# ============================================================================
# TestAcoplamientoAutointeraccion – 12 tests
# ============================================================================

class TestAcoplamientoAutointeraccion(unittest.TestCase):
    """Tests for AcoplamientoAutointeraccion class."""

    def setUp(self):
        self.aa = AcoplamientoAutointeraccion()

    def test_default_m_psi_eV(self):
        """Default m_psi_eV must match _M_PSI_EV."""
        self.assertAlmostEqual(self.aa.m_psi_eV, _M_PSI_EV, places=25)

    def test_default_m_planck_eV(self):
        """Default m_planck_eV must equal _M_PLANCK_EV."""
        self.assertAlmostEqual(self.aa.m_planck_eV, _M_PLANCK_EV, delta=1e26)

    def test_lambda_auto_formula(self):
        """lambda_auto must equal m_psi_eV / m_planck_eV."""
        expected = _M_PSI_EV / _M_PLANCK_EV
        self.assertAlmostEqual(self.aa.lambda_auto(), expected, places=50)

    def test_lambda_auto_range(self):
        """lambda_auto must be in [4e-41, 6e-41]."""
        lam = self.aa.lambda_auto()
        self.assertGreater(lam, 4.0e-41)
        self.assertLess(lam, 6.0e-41)

    def test_lambda_auto_matches_module_constant(self):
        """lambda_auto must match _LAMBDA_AUTO."""
        self.assertAlmostEqual(self.aa.lambda_auto(), _LAMBDA_AUTO, places=50)

    def test_es_sub_planckiano_true(self):
        """Default lambda must be sub-Planckian."""
        self.assertTrue(self.aa.es_sub_planckiano())

    def test_es_sub_planckiano_threshold(self):
        """lambda = 1e-9 must NOT be sub-Planckian (threshold is < 1e-10)."""
        aa_border = AcoplamientoAutointeraccion(
            m_psi_eV=1.0e-9, m_planck_eV=1.0
        )
        # λ = 1e-9 is greater than 1e-10, so NOT sub-Planckian
        self.assertFalse(aa_border.es_sub_planckiano())

    def test_es_sub_planckiano_just_below_threshold(self):
        """lambda = 1e-11 must be sub-Planckian."""
        aa_small = AcoplamientoAutointeraccion(
            m_psi_eV=1.0e-11, m_planck_eV=1.0
        )
        self.assertTrue(aa_small.es_sub_planckiano())

    def test_lambda_auto_positive(self):
        """lambda_auto must be positive."""
        self.assertGreater(self.aa.lambda_auto(), 0.0)

    def test_lambda_auto_much_less_than_one(self):
        """lambda_auto must be much less than 1."""
        self.assertLess(self.aa.lambda_auto(), 1.0e-30)

    def test_custom_mass_scales_lambda(self):
        """Doubling m_psi_eV must double lambda_auto."""
        aa2 = AcoplamientoAutointeraccion(m_psi_eV=2 * _M_PSI_EV)
        self.assertAlmostEqual(aa2.lambda_auto() / self.aa.lambda_auto(), 2.0, places=10)

    def test_repr_contains_lambda(self):
        """repr must mention λ."""
        self.assertIn("λ", repr(self.aa))


# ============================================================================
# TestLimitesExperimentales – 18 tests
# ============================================================================

class TestLimitesExperimentales(unittest.TestCase):
    """Tests for LimitesExperimentales class."""

    def setUp(self):
        self.le = LimitesExperimentales()

    def test_default_m_psi_eV(self):
        """Default m_psi_eV must match _M_PSI_EV."""
        self.assertAlmostEqual(self.le.m_psi_eV, _M_PSI_EV, places=25)

    def test_default_sigma_sobre_m(self):
        """Default sigma_sobre_m must equal 1e-65."""
        self.assertAlmostEqual(self.le.sigma_sobre_m, 1.0e-65, delta=1e-66)

    def test_default_delta_alpha(self):
        """Default delta_alpha_sobre_alpha must equal 1e-18."""
        self.assertAlmostEqual(self.le.delta_alpha_sobre_alpha, 1.0e-18, delta=1e-19)

    def test_compatible_superradiancia_bh_true(self):
        """Default m_ψ must be compatible with BH superradiance."""
        self.assertTrue(self.le.compatible_superradiancia_bh())

    def test_compatible_sigma_cumulos_true(self):
        """sigma_sobre_m = 1e-65 must be compatible with cluster limits."""
        self.assertTrue(self.le.compatible_sigma_cumulos())

    def test_compatible_sigma_cumulos_false_above_limit(self):
        """sigma_sobre_m > 1 cm²/g must be incompatible."""
        le_bad = LimitesExperimentales(sigma_sobre_m=2.0)
        self.assertFalse(le_bad.compatible_sigma_cumulos())

    def test_compatible_lyman_alpha_positive(self):
        """Lyman-alpha smoothing scale must be positive."""
        self.assertGreater(self.le.compatible_lyman_alpha(), 0.0)

    def test_compatible_lyman_alpha_matches_lambda_c(self):
        """Lyman-alpha smoothing scale must equal _LAMBDA_C_M."""
        self.assertAlmostEqual(self.le.compatible_lyman_alpha(), _LAMBDA_C_M, places=3)

    def test_compatible_lyman_alpha_greater_100m(self):
        """Smoothing scale must be > 100 m (not galaxy-destructive)."""
        self.assertGreater(self.le.compatible_lyman_alpha(), 100.0)

    def test_compatible_variacion_alfa_true(self):
        """Default Δα/α = 1e-18 must be detectable."""
        self.assertTrue(self.le.compatible_variacion_alfa())

    def test_compatible_variacion_alfa_false_below_threshold(self):
        """Δα/α < 1e-18 must not be detectable."""
        le_bad = LimitesExperimentales(delta_alpha_sobre_alpha=1.0e-19)
        self.assertFalse(le_bad.compatible_variacion_alfa())

    def test_compatible_variacion_alfa_equal_threshold(self):
        """Δα/α = 1e-18 must satisfy the detectable condition."""
        le_eq = LimitesExperimentales(delta_alpha_sobre_alpha=1.0e-18)
        self.assertTrue(le_eq.compatible_variacion_alfa())

    def test_todos_compatibles_true(self):
        """Default configuration must satisfy all experimental limits."""
        self.assertTrue(self.le.todos_compatibles())

    def test_todos_compatibles_false_bad_sigma(self):
        """Incompatible σ/m must make todos_compatibles False."""
        le_bad = LimitesExperimentales(sigma_sobre_m=10.0)
        self.assertFalse(le_bad.todos_compatibles())

    def test_todos_compatibles_false_bad_alpha(self):
        """Undetectable Δα/α must make todos_compatibles False."""
        le_bad = LimitesExperimentales(delta_alpha_sobre_alpha=1.0e-20)
        self.assertFalse(le_bad.todos_compatibles())

    def test_repr_contains_compatible(self):
        """repr must mention compatible status."""
        self.assertIn("compatible", repr(self.le))

    def test_repr_contains_m_psi(self):
        """repr must mention m_ψ."""
        self.assertIn("eV", repr(self.le))

    def test_repr_contains_sigma(self):
        """repr must mention σ/m."""
        self.assertIn("cm", repr(self.le))


# ============================================================================
# TestSistemaMasaComptonQCAL – 15 tests
# ============================================================================

class TestSistemaMasaComptonQCAL(unittest.TestCase):
    """Tests for SistemaMasaComptonQCAL class."""

    def setUp(self):
        self.sistema = SistemaMasaComptonQCAL()
        self.resultado = self.sistema.calcular()

    def test_default_f0(self):
        """Default f0 must equal _F0."""
        self.assertAlmostEqual(self.sistema.f0, _F0, places=4)

    def test_calcular_returns_resultado(self):
        """calcular() must return a ResultadoMasaCompton instance."""
        self.assertIsInstance(self.resultado, ResultadoMasaCompton)

    def test_resultado_f0_hz(self):
        """Resultado f0_hz must equal _F0."""
        self.assertAlmostEqual(self.resultado.f0_hz, _F0, places=4)

    def test_resultado_m_psi_kg(self):
        """Resultado m_psi_kg must be in [1.04e-48, 1.05e-48]."""
        self.assertGreater(self.resultado.m_psi_kg, 1.04e-48)
        self.assertLess(self.resultado.m_psi_kg, 1.05e-48)

    def test_resultado_m_psi_eV(self):
        """Resultado m_psi_eV must be in [5.8e-13, 5.9e-13]."""
        self.assertGreater(self.resultado.m_psi_eV, 5.8e-13)
        self.assertLess(self.resultado.m_psi_eV, 5.9e-13)

    def test_resultado_lambda_compton_m(self):
        """Resultado lambda_compton_m must be in [336000, 337500] m."""
        self.assertGreater(self.resultado.lambda_compton_m, 336_000.0)
        self.assertLess(self.resultado.lambda_compton_m, 337_500.0)

    def test_resultado_lambda_compton_km(self):
        """Resultado lambda_compton_km must be in [336.0, 337.5] km."""
        self.assertGreater(self.resultado.lambda_compton_km, 336.0)
        self.assertLess(self.resultado.lambda_compton_km, 337.5)

    def test_resultado_lambda_auto(self):
        """Resultado lambda_auto must be in [4e-41, 6e-41]."""
        self.assertGreater(self.resultado.lambda_auto, 4.0e-41)
        self.assertLess(self.resultado.lambda_auto, 6.0e-41)

    def test_resultado_sub_planckiano(self):
        """sub_planckiano must be True."""
        self.assertTrue(self.resultado.sub_planckiano)

    def test_resultado_compatible_experimental(self):
        """compatible_experimental must be True."""
        self.assertTrue(self.resultado.compatible_experimental)

    def test_resultado_mensaje_contains_mathesis(self):
        """mensaje must contain 'MATHESIS' for valid state."""
        self.assertIn("MATHESIS", self.resultado.mensaje)

    def test_resultado_mensaje_contains_eV(self):
        """mensaje must mention eV."""
        self.assertIn("eV", self.resultado.mensaje)

    def test_resultado_mensaje_contains_km(self):
        """mensaje must mention km."""
        self.assertIn("km", self.resultado.mensaje)

    def test_custom_f0_propagates(self):
        """Custom f0 must propagate to resultado."""
        s2 = SistemaMasaComptonQCAL(f0=200.0)
        r2 = s2.calcular()
        self.assertAlmostEqual(r2.f0_hz, 200.0, places=4)

    def test_repr_contains_f0(self):
        """repr must contain f0 value."""
        self.assertIn("141.7001", repr(self.sistema))


# ============================================================================
# TestMasaComptonQcalCalcular – 18 tests
# ============================================================================

class TestMasaComptonQcalCalcular(unittest.TestCase):
    """Tests for masa_compton_qcal_calcular() public API."""

    def setUp(self):
        self.result = masa_compton_qcal_calcular()

    def test_returns_dict(self):
        """API must return a dict."""
        self.assertIsInstance(self.result, dict)

    def test_keys_present(self):
        """All nine keys must be present in the result."""
        expected_keys = [
            "f0_hz", "m_psi_kg", "m_psi_eV", "lambda_compton_m",
            "lambda_compton_km", "lambda_auto", "sub_planckiano",
            "compatible_experimental", "mensaje",
        ]
        for key in expected_keys:
            self.assertIn(key, self.result, f"Missing key: {key}")

    def test_f0_hz_value(self):
        """f0_hz must equal 141.7001 Hz."""
        self.assertAlmostEqual(self.result["f0_hz"], 141.7001, places=4)

    def test_m_psi_kg_range(self):
        """m_psi_kg must be in [1.04e-48, 1.05e-48]."""
        m = self.result["m_psi_kg"]
        self.assertGreater(m, 1.04e-48)
        self.assertLess(m, 1.05e-48)

    def test_m_psi_eV_range(self):
        """m_psi_eV must be in [5.8e-13, 5.9e-13]."""
        m = self.result["m_psi_eV"]
        self.assertGreater(m, 5.8e-13)
        self.assertLess(m, 5.9e-13)

    def test_m_psi_eV_less_than_1e12(self):
        """m_psi_eV must be sub-pico-eV."""
        self.assertLess(self.result["m_psi_eV"], 1.0e-12)

    def test_lambda_compton_m_range(self):
        """lambda_compton_m must be ~336,000–337,500 m."""
        lc = self.result["lambda_compton_m"]
        self.assertGreater(lc, 336_000.0)
        self.assertLess(lc, 337_500.0)

    def test_lambda_compton_km_range(self):
        """lambda_compton_km must be ~336–337.5 km."""
        lc = self.result["lambda_compton_km"]
        self.assertGreater(lc, 336.0)
        self.assertLess(lc, 337.5)

    def test_lambda_compton_km_greater_300(self):
        """lambda_compton_km must be > 300 km."""
        self.assertGreater(self.result["lambda_compton_km"], 300.0)

    def test_lambda_auto_range(self):
        """lambda_auto must be in [4e-41, 6e-41]."""
        lam = self.result["lambda_auto"]
        self.assertGreater(lam, 4.0e-41)
        self.assertLess(lam, 6.0e-41)

    def test_lambda_auto_less_than_1e40(self):
        """lambda_auto must be < 1e-40."""
        self.assertLess(self.result["lambda_auto"], 1.0e-40)

    def test_sub_planckiano_true(self):
        """sub_planckiano must be True."""
        self.assertTrue(self.result["sub_planckiano"])

    def test_compatible_experimental_true(self):
        """compatible_experimental must be True."""
        self.assertTrue(self.result["compatible_experimental"])

    def test_mensaje_is_string(self):
        """mensaje must be a string."""
        self.assertIsInstance(self.result["mensaje"], str)

    def test_mensaje_not_empty(self):
        """mensaje must not be empty."""
        self.assertTrue(len(self.result["mensaje"]) > 0)

    def test_custom_f0_changes_mass(self):
        """Using a different f0 must change m_psi_eV proportionally."""
        result2 = masa_compton_qcal_calcular(f0=200.0)
        ratio = result2["m_psi_eV"] / self.result["m_psi_eV"]
        self.assertAlmostEqual(ratio, 200.0 / 141.7001, places=5)

    def test_custom_f0_changes_lambda_compton(self):
        """Using a different f0 must change lambda_compton_m inversely."""
        result2 = masa_compton_qcal_calcular(f0=200.0)
        ratio = result2["lambda_compton_m"] / self.result["lambda_compton_m"]
        self.assertAlmostEqual(ratio, 141.7001 / 200.0, places=5)

    def test_consistency_km_vs_m(self):
        """lambda_compton_km must equal lambda_compton_m / 1000."""
        lc_m = self.result["lambda_compton_m"]
        lc_km = self.result["lambda_compton_km"]
        self.assertAlmostEqual(lc_km, lc_m / 1000.0, places=9)


# ============================================================================
# TestResultadoMasaCompton – 5 tests
# ============================================================================

class TestResultadoMasaCompton(unittest.TestCase):
    """Tests for ResultadoMasaCompton dataclass."""

    def _make_resultado(self):
        return ResultadoMasaCompton(
            f0_hz=141.7001,
            m_psi_kg=_M_PSI_KG,
            m_psi_eV=_M_PSI_EV,
            lambda_compton_m=_LAMBDA_C_M,
            lambda_compton_km=_LAMBDA_C_M / 1000.0,
            lambda_auto=_LAMBDA_AUTO,
            sub_planckiano=True,
            compatible_experimental=True,
            mensaje="TEST OK",
        )

    def test_fields_accessible(self):
        """All nine fields must be accessible."""
        r = self._make_resultado()
        fields = [
            "f0_hz", "m_psi_kg", "m_psi_eV", "lambda_compton_m",
            "lambda_compton_km", "lambda_auto", "sub_planckiano",
            "compatible_experimental", "mensaje",
        ]
        for f in fields:
            self.assertTrue(hasattr(r, f), f"Missing field: {f}")

    def test_f0_hz_stored(self):
        """f0_hz must be stored as provided."""
        r = self._make_resultado()
        self.assertAlmostEqual(r.f0_hz, 141.7001, places=4)

    def test_bool_fields(self):
        """Boolean fields must be stored correctly."""
        r = self._make_resultado()
        self.assertTrue(r.sub_planckiano)
        self.assertTrue(r.compatible_experimental)

    def test_mensaje_stored(self):
        """mensaje must be stored as provided."""
        r = self._make_resultado()
        self.assertEqual(r.mensaje, "TEST OK")

    def test_lambda_auto_stored(self):
        """lambda_auto must be stored exactly."""
        r = self._make_resultado()
        self.assertAlmostEqual(r.lambda_auto, _LAMBDA_AUTO, places=50)


if __name__ == "__main__":
    unittest.main()
