"""
Tests for physics.masa_tejido_cosmico — Masa del Tejido Cósmico ∴MTQ∞³

Pruebas que cubren las 8 clases y la función de la API pública:
  - ConstantesMasaTejido    – constantes físicas y sello ∴MTQ∞³
  - MasaTejido              – m_ψ = h·f₀/c², régimen DM bosónico
  - AcoplamientoSwampland   – λ ≈ m_ψ/M_P, superfluidez garantizada
  - AutointeraccionOscura   – σ/m, verificación vs. Bullet Cluster
  - SuperradianciaQCAL      – M_opt, condición α < 1
  - SuperfluidezCosmologica – ξ, λ_dB, escalas macroscópicas
  - CoherenciaTejido        – Ψ_global ≥ 0.888
  - SistemaMasaTejidoCosmico – orquestador
  - masa_tejido_cosmico_activar() – API pública

Invariantes clave verificados (problema original):
  - m_ψ ≈ 5.86×10⁻¹³ eV                  (régimen DM bosónico ligero)
  - λ ≈ 4.8×10⁻⁴¹                        (acoplamiento Swampland)
  - σ/m ≈ 7.91×10⁻⁴⁷ cm²/g             (46 OM bajo Bullet Cluster)
  - ξ ≈ 337 km                            (longitud de coherencia Compton)
  - λ_dB ≈ 2.1×10⁸ m                     (longitud de de Broglie)
  - M_opt ≈ 228 M☉                        (masa óptima BH superradiante)
  - α ≈ 1.0                               (parámetro gravitacional óptimo)
  - Ψ_global ≈ 0.9981 ≥ 0.888            (coherencia global del tejido)
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.masa_tejido_cosmico import (
    # Module-level constants
    _F0,
    _H,
    _HBAR,
    _C,
    _EV_TO_J,
    _G,
    _M_SOL_KG,
    _M_PLANCK_EV,
    _V_DM_MS,
    _DM_BOSON_MIN_EV,
    _DM_BOSON_MAX_EV,
    _BULLET_CLUSTER_LIMIT_CM2_G,
    _M_PSI_KG,
    _M_PSI_EV,
    _LAMBDA_SWAMPLAND,
    _SIGMA_SOBRE_M_CGS,
    _XI_COMPTON_M,
    _LAMBDA_DB_M,
    _M_BH_OPT_KG,
    _M_BH_OPT_SOL,
    _ALPHA_GRAV,
    # Classes
    ConstantesMasaTejido,
    MasaTejido,
    AcoplamientoSwampland,
    AutointeraccionOscura,
    SuperradianciaQCAL,
    SuperfluidezCosmologica,
    CoherenciaTejido,
    SistemaMasaTejidoCosmico,
    ResultadoMasaTejido,
    # Public API
    masa_tejido_cosmico_activar,
)


# ============================================================================
# TestModuleConstants – 20 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests for module-level constants."""

    def test_f0_value(self):
        """_F0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_h_planck_value(self):
        """_H must equal CODATA 2018 Planck constant."""
        self.assertAlmostEqual(_H, 6.62607015e-34, places=42)

    def test_hbar_equals_h_over_2pi(self):
        """_HBAR must equal _H / (2π)."""
        self.assertAlmostEqual(_HBAR, _H / (2.0 * math.pi), places=44)

    def test_c_value(self):
        """_C must be exact speed of light."""
        self.assertEqual(_C, 299_792_458.0)

    def test_ev_to_j_value(self):
        """_EV_TO_J must equal exact CODATA eV."""
        self.assertAlmostEqual(_EV_TO_J, 1.602176634e-19, places=28)

    def test_g_newton_order(self):
        """_G must be ~6.674×10⁻¹¹."""
        self.assertAlmostEqual(_G, 6.67430e-11, delta=1e-13)

    def test_m_sol_kg_order(self):
        """_M_SOL_KG must be ~1.989×10³⁰ kg."""
        self.assertAlmostEqual(_M_SOL_KG, 1.989e30, delta=1e27)

    def test_m_planck_eV_order(self):
        """_M_PLANCK_EV must be ~1.22×10²⁸ eV."""
        self.assertAlmostEqual(_M_PLANCK_EV, 1.22e28, delta=1e26)

    def test_v_dm_ms(self):
        """_V_DM_MS must be 300,000 m/s."""
        self.assertEqual(_V_DM_MS, 300_000.0)

    def test_dm_boson_range(self):
        """DM bosonic range must span from 10⁻²² to 10⁻¹⁰ eV."""
        self.assertEqual(_DM_BOSON_MIN_EV, 1.0e-22)
        self.assertEqual(_DM_BOSON_MAX_EV, 1.0e-10)

    def test_bullet_cluster_limit(self):
        """Bullet Cluster limit must be 1 cm²/g."""
        self.assertEqual(_BULLET_CLUSTER_LIMIT_CM2_G, 1.0)

    def test_m_psi_kg_order(self):
        """_M_PSI_KG must be ~1.04×10⁻⁴⁸ kg."""
        self.assertGreater(_M_PSI_KG, 1.04e-48)
        self.assertLess(_M_PSI_KG, 1.05e-48)

    def test_m_psi_eV_order(self):
        """_M_PSI_EV must be ~5.8–5.9×10⁻¹³ eV."""
        self.assertGreater(_M_PSI_EV, 5.8e-13)
        self.assertLess(_M_PSI_EV, 5.9e-13)

    def test_lambda_swampland_order(self):
        """_LAMBDA_SWAMPLAND must be ~4–6×10⁻⁴¹."""
        self.assertGreater(_LAMBDA_SWAMPLAND, 4.0e-41)
        self.assertLess(_LAMBDA_SWAMPLAND, 6.0e-41)

    def test_sigma_sobre_m_cgs_order(self):
        """_SIGMA_SOBRE_M_CGS must be < 1 cm²/g."""
        self.assertLess(_SIGMA_SOBRE_M_CGS, 1.0)
        self.assertGreater(_SIGMA_SOBRE_M_CGS, 0.0)

    def test_xi_compton_m_order(self):
        """_XI_COMPTON_M must be ~336,700 m (≈ 337 km)."""
        self.assertGreater(_XI_COMPTON_M, 335_000.0)
        self.assertLess(_XI_COMPTON_M, 338_000.0)

    def test_lambda_db_m_order(self):
        """_LAMBDA_DB_M must be > 10⁸ m."""
        self.assertGreater(_LAMBDA_DB_M, 1.0e8)

    def test_m_bh_opt_solar_order(self):
        """_M_BH_OPT_SOL must be ~200–260 M☉."""
        self.assertGreater(_M_BH_OPT_SOL, 200.0)
        self.assertLess(_M_BH_OPT_SOL, 260.0)

    def test_alpha_grav_near_unity(self):
        """_ALPHA_GRAV must be ≈ 1.0 at M_opt."""
        self.assertAlmostEqual(_ALPHA_GRAV, 1.0, places=4)

    def test_m_psi_consistency(self):
        """m_ψ = h·f₀/c² must be internally consistent."""
        m_expected = _H * _F0 / (_C ** 2)
        self.assertAlmostEqual(_M_PSI_KG, m_expected, places=55)


# ============================================================================
# TestConstantesMasaTejido – 5 tests
# ============================================================================

class TestConstantesMasaTejido(unittest.TestCase):
    """Tests for ConstantesMasaTejido dataclass."""

    def setUp(self):
        self.c = ConstantesMasaTejido()

    def test_default_f0(self):
        """Default f0 must be 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_sello_contains_mtq(self):
        """Sello must contain ∴MTQ∞³."""
        self.assertIn("∴MTQ∞³", self.c.sello())

    def test_sello_contains_ram(self):
        """Sello must contain RAM identifier."""
        self.assertIn("RAM-XLI-2026-MASA-TEJIDO-COSMICO", self.c.sello())

    def test_sello_contains_f0(self):
        """Sello must mention the base frequency."""
        sello = self.c.sello()
        self.assertIn("141.7001", sello)

    def test_repr_contains_sello(self):
        """repr must mention ∴MTQ∞³."""
        self.assertIn("∴MTQ∞³", repr(self.c))


# ============================================================================
# TestMasaTejido – 10 tests
# ============================================================================

class TestMasaTejido(unittest.TestCase):
    """Tests for MasaTejido class."""

    def setUp(self):
        self.mt = MasaTejido()

    def test_masa_kg_order(self):
        """masa_kg() must be ~1.04×10⁻⁴⁸ kg."""
        m = self.mt.masa_kg()
        self.assertGreater(m, 1.04e-48)
        self.assertLess(m, 1.05e-48)

    def test_masa_eV_order(self):
        """masa_eV() must be ~5.8–5.9×10⁻¹³ eV."""
        m = self.mt.masa_eV()
        self.assertGreater(m, 5.8e-13)
        self.assertLess(m, 5.9e-13)

    def test_masa_eV_specific_value(self):
        """masa_eV() must be close to 5.86×10⁻¹³ eV."""
        m = self.mt.masa_eV()
        self.assertAlmostEqual(m, 5.86e-13, delta=1e-14)

    def test_en_regimen_dm_bosonico(self):
        """m_ψ must be in the DM bosonic regime."""
        self.assertTrue(self.mt.en_regimen_dm_bosonico())

    def test_en_regimen_dm_consistency(self):
        """en_regimen_dm_bosonico checks against module constants."""
        m = self.mt.masa_eV()
        self.assertGreater(m, _DM_BOSON_MIN_EV)
        self.assertLess(m, _DM_BOSON_MAX_EV)

    def test_coherencia_masa_high(self):
        """Ψ_masa must be ≥ 0.99 (mass in optimal DM range)."""
        psi = self.mt.coherencia_masa()
        self.assertGreater(psi, 0.99)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_masa_expected(self):
        """Ψ_masa must be ≈ 0.9956 as given in problem statement."""
        psi = self.mt.coherencia_masa()
        self.assertAlmostEqual(psi, 0.9956, delta=0.002)

    def test_masa_formula_consistency(self):
        """masa_kg × c² / ev_to_j must equal masa_eV."""
        m_kg = self.mt.masa_kg()
        m_eV_from_kg = m_kg * (_C ** 2) / _EV_TO_J
        self.assertAlmostEqual(m_eV_from_kg, self.mt.masa_eV(), places=25)

    def test_custom_f0(self):
        """Custom f0 should change the mass proportionally."""
        mt2 = MasaTejido(f0=283.4002)  # 2× f₀
        self.assertAlmostEqual(mt2.masa_kg(), 2.0 * self.mt.masa_kg(), places=55)

    def test_repr_contains_eV(self):
        """repr must mention eV."""
        self.assertIn("eV", repr(self.mt))


# ============================================================================
# TestAcoplamientoSwampland – 10 tests
# ============================================================================

class TestAcoplamientoSwampland(unittest.TestCase):
    """Tests for AcoplamientoSwampland class."""

    def setUp(self):
        self.sw = AcoplamientoSwampland()

    def test_lambda_order(self):
        """λ must be ~4–6×10⁻⁴¹."""
        lam = self.sw.lambda_acoplamiento()
        self.assertGreater(lam, 4.0e-41)
        self.assertLess(lam, 6.0e-41)

    def test_lambda_specific_value(self):
        """λ must be close to 4.8×10⁻⁴¹."""
        lam = self.sw.lambda_acoplamiento()
        self.assertAlmostEqual(lam, 4.8e-41, delta=5e-42)

    def test_es_repulsivo(self):
        """λ must be > 0 (repulsive)."""
        self.assertTrue(self.sw.es_repulsivo())

    def test_eft_valida(self):
        """λ must be < 10⁻¹⁰ (EFT perturbative validity)."""
        self.assertTrue(self.sw.eft_valida())

    def test_superfluidez_garantizada(self):
        """λ must be < 10⁻³⁰ (superfluid regime guaranteed)."""
        self.assertTrue(self.sw.superfluidez_garantizada())

    def test_coherencia_lambda_high(self):
        """Ψ_lambda must be ≥ 0.999."""
        psi = self.sw.coherencia_lambda()
        self.assertGreater(psi, 0.999)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_lambda_expected(self):
        """Ψ_lambda must equal 0.9998 as per problem statement."""
        psi = self.sw.coherencia_lambda()
        self.assertAlmostEqual(psi, 0.9998, delta=0.0001)

    def test_lambda_formula_consistency(self):
        """λ = m_ψ / M_P must be consistent with module constants."""
        lam_expected = _M_PSI_EV / _M_PLANCK_EV
        self.assertAlmostEqual(self.sw.lambda_acoplamiento(), lam_expected, places=55)

    def test_eft_invalid_for_large_coupling(self):
        """Large λ must fail EFT validity check."""
        sw_large = AcoplamientoSwampland(m_psi_eV=1e20, m_planck_eV=1e22)
        self.assertFalse(sw_large.eft_valida())

    def test_repr_contains_lambda(self):
        """repr must mention λ."""
        self.assertIn("λ", repr(self.sw))


# ============================================================================
# TestAutointeraccionOscura – 10 tests
# ============================================================================

class TestAutointeraccionOscura(unittest.TestCase):
    """Tests for AutointeraccionOscura class."""

    def setUp(self):
        self.ao = AutointeraccionOscura()

    def test_sigma_SI_positive(self):
        """σ/m in SI units must be positive."""
        self.assertGreater(self.ao.sigma_sobre_m_SI(), 0.0)

    def test_sigma_SI_very_small(self):
        """σ/m in SI must be extremely small."""
        self.assertLess(self.ao.sigma_sobre_m_SI(), 1.0e-40)

    def test_sigma_CGS_order(self):
        """σ/m in cm²/g must be ~7.9×10⁻⁴⁷."""
        sigma = self.ao.sigma_sobre_m_CGS()
        self.assertGreater(sigma, 1.0e-50)
        self.assertLess(sigma, 1.0e-40)

    def test_sigma_CGS_vs_SI(self):
        """σ/m in cm²/g must equal σ/m in m²/kg × 10."""
        sigma_si = self.ao.sigma_sobre_m_SI()
        sigma_cgs = self.ao.sigma_sobre_m_CGS()
        self.assertAlmostEqual(sigma_cgs, sigma_si * 10.0, places=55)

    def test_bajo_limite_bullet_cluster(self):
        """σ/m must be below the Bullet Cluster limit (< 1 cm²/g)."""
        self.assertTrue(self.ao.bajo_limite_bullet_cluster())

    def test_ordenes_magnitud_below_limit(self):
        """Margin vs. Bullet Cluster must be > 40 orders of magnitude."""
        ordenes = self.ao.ordenes_magnitud_bajo_limite()
        self.assertGreater(ordenes, 40.0)

    def test_coherencia_sigma_high(self):
        """Ψ_sigma must be ≥ 0.999."""
        psi = self.ao.coherencia_sigma()
        self.assertGreater(psi, 0.999)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_sigma_expected(self):
        """Ψ_sigma must be ≈ 0.9998 as per problem statement."""
        psi = self.ao.coherencia_sigma()
        self.assertAlmostEqual(psi, 0.9998, delta=0.0001)

    def test_above_limit_gives_zero_coherencia(self):
        """When σ/m > Bullet Cluster limit, coherencia must be 0."""
        # m_psi_kg = 1e-50, lambda = 1 gives σ/m ≈ 3.9×10⁴⁰ cm²/g >> 1
        ao_over = AutointeraccionOscura(
            m_psi_kg=1.0e-50, lambda_acop=1.0
        )
        self.assertFalse(ao_over.bajo_limite_bullet_cluster())
        self.assertEqual(ao_over.coherencia_sigma(), 0.0)

    def test_repr_contains_sigma(self):
        """repr must mention σ/m."""
        self.assertIn("σ/m", repr(self.ao))


# ============================================================================
# TestSuperradianciaQCAL – 10 tests
# ============================================================================

class TestSuperradianciaQCAL(unittest.TestCase):
    """Tests for SuperradianciaQCAL class."""

    def setUp(self):
        self.sr = SuperradianciaQCAL()

    def test_masa_bh_optima_kg_positive(self):
        """M_opt in kg must be positive."""
        self.assertGreater(self.sr.masa_bh_optima_kg(), 0.0)

    def test_masa_bh_optima_kg_order(self):
        """M_opt in kg must be ~4.5×10³² kg."""
        m = self.sr.masa_bh_optima_kg()
        self.assertGreater(m, 4.0e32)
        self.assertLess(m, 5.0e32)

    def test_masa_bh_optima_solar_range(self):
        """M_opt must be ~200–260 M☉."""
        m_sol = self.sr.masa_bh_optima_solar()
        self.assertGreater(m_sol, 200.0)
        self.assertLess(m_sol, 260.0)

    def test_masa_bh_optima_solar_expected(self):
        """M_opt must be close to 228 M☉ as per problem statement."""
        m_sol = self.sr.masa_bh_optima_solar()
        self.assertAlmostEqual(m_sol, 228.0, delta=5.0)

    def test_parametro_gravitacional_at_mopt(self):
        """α at M_opt must be ≈ 1.0."""
        alpha = self.sr.parametro_gravitacional()
        self.assertAlmostEqual(alpha, 1.0, delta=0.01)

    def test_parametro_gravitacional_custom(self):
        """α must scale linearly with BH mass."""
        m_half = self.sr.masa_bh_optima_kg() / 2.0
        alpha_half = self.sr.parametro_gravitacional(m_bh_kg=m_half)
        self.assertAlmostEqual(alpha_half, 0.5, delta=0.01)

    def test_condicion_superradiante(self):
        """Superradiant condition must be verified at M_opt."""
        self.assertTrue(self.sr.condicion_superradiante_verificada())

    def test_coherencia_superfluido_range(self):
        """Ψ_superfluido must be > 0.99 and ≤ 1.0."""
        psi = self.sr.coherencia_superfluido()
        self.assertGreater(psi, 0.99)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_superfluido_expected(self):
        """Ψ_superfluido must be ≈ 0.9970 as per problem statement."""
        psi = self.sr.coherencia_superfluido()
        self.assertAlmostEqual(psi, 0.997, delta=0.001)

    def test_repr_contains_m_sol(self):
        """repr must mention M☉."""
        self.assertIn("M☉", repr(self.sr))


# ============================================================================
# TestSuperfluidezCosmologica – 10 tests
# ============================================================================

class TestSuperfluidezCosmologica(unittest.TestCase):
    """Tests for SuperfluidezCosmologica class."""

    def setUp(self):
        self.sf = SuperfluidezCosmologica()

    def test_xi_compton_m_order(self):
        """ξ_Compton must be ~336,700 m."""
        xi = self.sf.xi_compton_m()
        self.assertGreater(xi, 335_000.0)
        self.assertLess(xi, 338_000.0)

    def test_xi_compton_km_expected(self):
        """ξ_Compton in km must be ≈ 337 km."""
        xi_km = self.sf.xi_compton_km()
        self.assertAlmostEqual(xi_km, 337.0, delta=1.0)

    def test_xi_compton_consistency(self):
        """ξ_km must equal ξ_m / 1000."""
        self.assertAlmostEqual(
            self.sf.xi_compton_km(),
            self.sf.xi_compton_m() / 1_000.0,
            places=10,
        )

    def test_xi_equals_hbar_over_mpsi_c(self):
        """ξ = ℏ/(m_ψ·c) must be consistent."""
        xi_expected = _HBAR / (_M_PSI_KG * _C)
        self.assertAlmostEqual(self.sf.xi_compton_m(), xi_expected, places=5)

    def test_lambda_debroglie_order(self):
        """λ_dB must be > 10⁸ m."""
        ldb = self.sf.lambda_debroglie_m()
        self.assertGreater(ldb, 1.0e8)

    def test_lambda_debroglie_expected(self):
        """λ_dB must be ≈ 2.1×10⁸ – 4×10⁸ m."""
        ldb = self.sf.lambda_debroglie_m()
        self.assertGreater(ldb, 1.0e8)
        self.assertLess(ldb, 1.0e10)

    def test_escalas_macroscopicas(self):
        """Both ξ and λ_dB must be macroscopic."""
        self.assertTrue(self.sf.escalas_macroscopicas())

    def test_coherencia_superfluidez_high(self):
        """Ψ_superfluidez must be ≥ 0.99."""
        psi = self.sf.coherencia_superfluidez()
        self.assertGreater(psi, 0.99)
        self.assertLessEqual(psi, 1.0)

    def test_coherencia_superfluidez_expected(self):
        """Ψ_superfluidez must be ≈ 0.997 (macroscopic scale)."""
        psi = self.sf.coherencia_superfluidez()
        self.assertGreater(psi, 0.995)

    def test_repr_contains_km(self):
        """repr must mention km."""
        self.assertIn("km", repr(self.sf))


# ============================================================================
# TestCoherenciaTejido – 10 tests
# ============================================================================

class TestCoherenciaTejido(unittest.TestCase):
    """Tests for CoherenciaTejido class."""

    def setUp(self):
        self.ct = CoherenciaTejido(
            psi_masa=0.9956,
            psi_lambda=0.9998,
            psi_sigma=0.9998,
            psi_superfluido=0.9970,
        )

    def test_psi_global_formula(self):
        """Ψ_global must be the 4th geometric mean."""
        expected = (0.9956 * 0.9998 * 0.9998 * 0.9970) ** (1.0 / 4.0)
        self.assertAlmostEqual(self.ct.psi_global(), expected, places=10)

    def test_psi_global_above_threshold(self):
        """Ψ_global must be ≥ 0.888."""
        self.assertGreater(self.ct.psi_global(), 0.888)

    def test_psi_global_expected(self):
        """Ψ_global must be ≈ 0.9981 as per problem statement."""
        self.assertAlmostEqual(self.ct.psi_global(), 0.9981, delta=0.001)

    def test_sobre_umbral_true(self):
        """sobre_umbral() must be True for valid coherences."""
        self.assertTrue(self.ct.sobre_umbral())

    def test_sobre_umbral_false_for_low_psi(self):
        """sobre_umbral() must be False for Ψ_global < 0.888."""
        ct_low = CoherenciaTejido(
            psi_masa=0.1, psi_lambda=0.1, psi_sigma=0.1, psi_superfluido=0.1
        )
        self.assertFalse(ct_low.sobre_umbral())

    def test_estado_contains_tejido(self):
        """estado() must mention TEJIDO."""
        self.assertIn("TEJIDO", self.ct.estado())

    def test_estado_contains_mtq(self):
        """estado() must contain ∴MTQ∞³."""
        self.assertIn("∴MTQ∞³", self.ct.estado())

    def test_psi_global_zero_for_negative_product(self):
        """psi_global() must return 0 for negative input."""
        ct_neg = CoherenciaTejido(
            psi_masa=-0.5, psi_lambda=0.9, psi_sigma=0.9, psi_superfluido=0.9
        )
        self.assertEqual(ct_neg.psi_global(), 0.0)

    def test_psi_global_one_for_all_ones(self):
        """Ψ_global = 1 when all components are 1."""
        ct_one = CoherenciaTejido(
            psi_masa=1.0, psi_lambda=1.0, psi_sigma=1.0, psi_superfluido=1.0
        )
        self.assertAlmostEqual(ct_one.psi_global(), 1.0, places=10)

    def test_repr_contains_psi_global(self):
        """repr must mention Ψ_global."""
        self.assertIn("Ψ_global", repr(self.ct))


# ============================================================================
# TestSistemaMasaTejidoCosmico – 15 tests
# ============================================================================

class TestSistemaMasaTejidoCosmico(unittest.TestCase):
    """Tests for SistemaMasaTejidoCosmico orchestrator."""

    def setUp(self):
        self.sistema = SistemaMasaTejidoCosmico()
        self.resultado = self.sistema.activar()

    def test_resultado_is_dataclass(self):
        """activar() must return a ResultadoMasaTejido instance."""
        self.assertIsInstance(self.resultado, ResultadoMasaTejido)

    def test_f0_hz(self):
        """Result f0_hz must be 141.7001."""
        self.assertAlmostEqual(self.resultado.f0_hz, 141.7001, places=4)

    def test_m_psi_eV(self):
        """Result m_psi_eV must be ~5.86×10⁻¹³ eV."""
        self.assertGreater(self.resultado.m_psi_eV, 5.8e-13)
        self.assertLess(self.resultado.m_psi_eV, 5.9e-13)

    def test_en_regimen_dm(self):
        """Result en_regimen_dm must be True."""
        self.assertTrue(self.resultado.en_regimen_dm)

    def test_lambda_swampland(self):
        """Result lambda_swampland must be ~4–6×10⁻⁴¹."""
        self.assertGreater(self.resultado.lambda_swampland, 4.0e-41)
        self.assertLess(self.resultado.lambda_swampland, 6.0e-41)

    def test_bajo_bullet_cluster(self):
        """Result bajo_bullet_cluster must be True."""
        self.assertTrue(self.resultado.bajo_bullet_cluster)

    def test_xi_compton_km(self):
        """Result xi_compton_km must be ~337 km."""
        self.assertAlmostEqual(self.resultado.xi_compton_km, 337.0, delta=2.0)

    def test_m_bh_optima_solar(self):
        """Result m_bh_optima_solar must be ~228 M☉."""
        self.assertAlmostEqual(self.resultado.m_bh_optima_solar, 228.0, delta=5.0)

    def test_superfluidez_garantizada(self):
        """Result superfluidez_garantizada must be True."""
        self.assertTrue(self.resultado.superfluidez_garantizada)

    def test_psi_global_above_threshold(self):
        """Result psi_global must be ≥ 0.888."""
        self.assertGreater(self.resultado.psi_global, 0.888)

    def test_psi_global_expected(self):
        """Result psi_global must be ≈ 0.9981."""
        self.assertAlmostEqual(self.resultado.psi_global, 0.9981, delta=0.001)

    def test_sobre_umbral(self):
        """Result sobre_umbral must be True."""
        self.assertTrue(self.resultado.sobre_umbral)

    def test_mensaje_contains_tejido(self):
        """Result mensaje must mention TEJIDO."""
        self.assertIn("TEJIDO", self.resultado.mensaje)

    def test_custom_f0(self):
        """Sistema with custom f0 should propagate to result."""
        s2 = SistemaMasaTejidoCosmico(f0=283.4002)
        r2 = s2.activar()
        self.assertAlmostEqual(r2.f0_hz, 283.4002, places=4)

    def test_repr_contains_mtq(self):
        """repr must mention ∴MTQ∞³."""
        self.assertIn("∴MTQ∞³", repr(self.sistema))


# ============================================================================
# TestMasaTejidoCosmicActivar – 20 tests (Public API)
# ============================================================================

class TestMasaTejidoCosmicActivar(unittest.TestCase):
    """Tests for the public API masa_tejido_cosmico_activar()."""

    def setUp(self):
        self.result = masa_tejido_cosmico_activar()

    def test_returns_dict(self):
        """API must return a dict."""
        self.assertIsInstance(self.result, dict)

    def test_all_keys_present(self):
        """All 19 expected keys must be present."""
        expected_keys = {
            "f0_hz", "m_psi_kg", "m_psi_eV", "en_regimen_dm",
            "lambda_swampland", "sigma_sobre_m_CGS", "bajo_bullet_cluster",
            "xi_compton_km", "lambda_debroglie_m", "m_bh_optima_solar",
            "alpha_gravitacional", "superfluidez_garantizada",
            "psi_masa", "psi_lambda", "psi_sigma", "psi_superfluido",
            "psi_global", "sobre_umbral", "mensaje",
        }
        self.assertEqual(set(self.result.keys()), expected_keys)

    def test_f0_hz(self):
        """f0_hz must be 141.7001."""
        self.assertAlmostEqual(self.result["f0_hz"], 141.7001, places=4)

    def test_m_psi_kg_order(self):
        """m_psi_kg must be ~1.04×10⁻⁴⁸ kg."""
        m = self.result["m_psi_kg"]
        self.assertGreater(m, 1.04e-48)
        self.assertLess(m, 1.05e-48)

    def test_m_psi_eV_order(self):
        """m_psi_eV must be ~5.8–5.9×10⁻¹³ eV."""
        m = self.result["m_psi_eV"]
        self.assertGreater(m, 5.8e-13)
        self.assertLess(m, 5.9e-13)

    def test_en_regimen_dm(self):
        """en_regimen_dm must be True."""
        self.assertTrue(self.result["en_regimen_dm"])

    def test_lambda_swampland_order(self):
        """lambda_swampland must be ~4–6×10⁻⁴¹."""
        lam = self.result["lambda_swampland"]
        self.assertGreater(lam, 4.0e-41)
        self.assertLess(lam, 6.0e-41)

    def test_sigma_CGS_below_bullet(self):
        """sigma_sobre_m_CGS must be < 1 cm²/g."""
        self.assertLess(self.result["sigma_sobre_m_CGS"], 1.0)

    def test_bajo_bullet_cluster(self):
        """bajo_bullet_cluster must be True."""
        self.assertTrue(self.result["bajo_bullet_cluster"])

    def test_xi_compton_km(self):
        """xi_compton_km must be ≈ 337 km."""
        self.assertAlmostEqual(self.result["xi_compton_km"], 337.0, delta=2.0)

    def test_lambda_debroglie_m_order(self):
        """lambda_debroglie_m must be > 10⁸ m."""
        self.assertGreater(self.result["lambda_debroglie_m"], 1.0e8)

    def test_m_bh_optima_solar(self):
        """m_bh_optima_solar must be ≈ 228 M☉."""
        self.assertAlmostEqual(self.result["m_bh_optima_solar"], 228.0, delta=5.0)

    def test_alpha_gravitacional_near_unity(self):
        """alpha_gravitacional must be ≈ 1.0."""
        self.assertAlmostEqual(self.result["alpha_gravitacional"], 1.0, delta=0.01)

    def test_superfluidez_garantizada(self):
        """superfluidez_garantizada must be True."""
        self.assertTrue(self.result["superfluidez_garantizada"])

    def test_psi_masa_high(self):
        """psi_masa must be ≥ 0.99."""
        self.assertGreater(self.result["psi_masa"], 0.99)

    def test_psi_lambda(self):
        """psi_lambda must be ≈ 0.9998."""
        self.assertAlmostEqual(self.result["psi_lambda"], 0.9998, delta=0.0001)

    def test_psi_sigma(self):
        """psi_sigma must be ≈ 0.9998."""
        self.assertAlmostEqual(self.result["psi_sigma"], 0.9998, delta=0.0001)

    def test_psi_superfluido(self):
        """psi_superfluido must be ≈ 0.997."""
        self.assertAlmostEqual(self.result["psi_superfluido"], 0.997, delta=0.001)

    def test_psi_global_above_threshold(self):
        """psi_global must be ≥ 0.888."""
        self.assertGreater(self.result["psi_global"], 0.888)

    def test_psi_global_expected(self):
        """psi_global must be ≈ 0.9981."""
        self.assertAlmostEqual(self.result["psi_global"], 0.9981, delta=0.001)

    def test_sobre_umbral(self):
        """sobre_umbral must be True."""
        self.assertTrue(self.result["sobre_umbral"])

    def test_mensaje_is_string(self):
        """mensaje must be a non-empty string."""
        self.assertIsInstance(self.result["mensaje"], str)
        self.assertGreater(len(self.result["mensaje"]), 0)

    def test_custom_f0_propagates(self):
        """Custom f0 must propagate to all results."""
        result2 = masa_tejido_cosmico_activar(f0=283.4002)
        self.assertAlmostEqual(result2["f0_hz"], 283.4002, places=4)
        self.assertAlmostEqual(result2["m_psi_eV"], 2.0 * self.result["m_psi_eV"], delta=1e-14)

    def test_invalid_f0_raises_value_error(self):
        """f0 ≤ 0 must raise ValueError."""
        with self.assertRaises(ValueError):
            masa_tejido_cosmico_activar(f0=0.0)

    def test_negative_f0_raises_value_error(self):
        """Negative f0 must raise ValueError."""
        with self.assertRaises(ValueError):
            masa_tejido_cosmico_activar(f0=-1.0)


# ============================================================================
# TestPhysicalConsistency – integration / cross-checks
# ============================================================================

class TestPhysicalConsistency(unittest.TestCase):
    """Cross-consistency tests between classes."""

    def setUp(self):
        self.result = masa_tejido_cosmico_activar()

    def test_hbar_over_m_c_equals_xi(self):
        """ξ = ℏ/(m_ψ·c) must match module constant."""
        xi_expected = _HBAR / (_M_PSI_KG * _C)
        xi_km_expected = xi_expected / 1_000.0
        self.assertAlmostEqual(self.result["xi_compton_km"], xi_km_expected, delta=0.01)

    def test_hbar_over_m_v_equals_lambda_db(self):
        """λ_dB = ℏ/(m_ψ·v) must match module constant."""
        ldb_expected = _HBAR / (_M_PSI_KG * _V_DM_MS)
        self.assertAlmostEqual(
            self.result["lambda_debroglie_m"], ldb_expected, delta=1.0
        )

    def test_lambda_db_much_larger_than_xi(self):
        """λ_dB >> ξ because v_DM << c."""
        ratio = self.result["lambda_debroglie_m"] / (self.result["xi_compton_km"] * 1000.0)
        self.assertGreater(ratio, 100.0)

    def test_m_psi_eV_times_ev_to_j_equals_energy(self):
        """m_ψ·c² in eV must equal h·f₀/eV."""
        energy_eV = self.result["m_psi_eV"]
        energy_from_planck = _H * _F0 / _EV_TO_J
        self.assertAlmostEqual(energy_eV, energy_from_planck, delta=1e-16)

    def test_alpha_near_1_at_mopt(self):
        """α = G·M_opt·m_ψ/(ℏ·c) ≈ 1.0 by construction."""
        alpha = self.result["alpha_gravitacional"]
        self.assertAlmostEqual(alpha, 1.0, delta=0.01)

    def test_psi_global_geometric_mean(self):
        """psi_global = (psi_masa·psi_lambda·psi_sigma·psi_sup)^(1/4)."""
        p = (
            self.result["psi_masa"]
            * self.result["psi_lambda"]
            * self.result["psi_sigma"]
            * self.result["psi_superfluido"]
        ) ** (1.0 / 4.0)
        self.assertAlmostEqual(self.result["psi_global"], p, places=10)


# ============================================================================
# Entry point
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
