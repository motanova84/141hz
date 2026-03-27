"""
Tests for physics.limite_ruido_disparo — Shot Noise Limit y Cooperatividad IRS-Luna

Pruebas que cubren las 5 clases y la función de la API pública:
  - ParametrosLaser           – flujo de fotones, energía por fotón
  - LimiteRuidoDisparo        – δφ_SNL, fotones detectados, brecha en décadas
  - MultiplicadorCooperatividad – G_req, 2F/π, cooperatividad de red, ξ
  - EcuacionViscosidadVacio   – Δf_crítico, umbral de coherencia
  - SistemaIRSLuna            – orquestador
  - ResultadoIRSLuna          – dataclass de resultado
  - limite_ruido_disparo_calcular() – API pública

Invariantes clave verificados:
  - Φ_P ≈ 5,36×10²⁰ /s   (5.3e20 < phi_p < 5.4e20)
  - δφ_SNL ≈ 1,55×10⁻¹³ rad  (1e-13 < snl < 2e-13)
  - G_req > 1×10⁵ (ganancia total requerida positiva y significativa)
  - 0 < ξ < 1              (umbral generoso, sub-unitario)
  - senyal_localizada = True
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.limite_ruido_disparo import (
    # Constantes del módulo
    _F0,
    _H,
    _C,
    _EV_TO_J,
    _P_LASER_W,
    _LAMBDA_LASER_M,
    _PHI_P,
    _ETA,
    _TAU_24H,
    _DELTA_THETA_CELDA,
    _FINEZA_CAVIDAD,
    _N_CELDAS,
    _SNR_OBJETIVO,
    _M_PLANCK_EV,
    _M_PSI_EV,
    _RATIO_MASA_PSI_PLANCK,
    _DELTA_PHI_SNL,
    _G_REQ,
    _FACTOR_FINEZA,
    _COOPERATIVIDAD_RED,
    _XI,
    _DELTA_F_CRITICO,
    _TIEMPO_DETECCION_H,
    _CONFIANZA_SIGMA,
    # Clases
    ParametrosLaser,
    LimiteRuidoDisparo,
    MultiplicadorCooperatividad,
    EcuacionViscosidadVacio,
    SistemaIRSLuna,
    ResultadoIRSLuna,
    # API pública
    limite_ruido_disparo_calcular,
)


# ============================================================================
# TestModuleConstants – 18 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests for module-level constants."""

    def test_f0_value(self):
        """_F0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_h_planck_value(self):
        """_H must be the CODATA 2018 Planck constant."""
        self.assertAlmostEqual(_H, 6.62607015e-34, places=42)

    def test_c_value(self):
        """_C must be the exact speed of light."""
        self.assertEqual(_C, 299_792_458.0)

    def test_ev_to_j(self):
        """_EV_TO_J must be the exact CODATA electronvolt."""
        self.assertAlmostEqual(_EV_TO_J, 1.602176634e-19, places=28)

    def test_laser_power(self):
        """_P_LASER_W must be 100 W."""
        self.assertEqual(_P_LASER_W, 100.0)

    def test_laser_wavelength(self):
        """_LAMBDA_LASER_M must be 1064 nm."""
        self.assertAlmostEqual(_LAMBDA_LASER_M, 1064e-9, places=15)

    def test_phi_p_order_of_magnitude(self):
        """_PHI_P must be between 5.3e20 and 5.4e20 /s."""
        self.assertGreater(_PHI_P, 5.3e20)
        self.assertLess(_PHI_P, 5.4e20)

    def test_phi_p_formula(self):
        """_PHI_P must equal P*lambda/(h*c)."""
        expected = _P_LASER_W * _LAMBDA_LASER_M / (_H * _C)
        self.assertAlmostEqual(_PHI_P, expected, places=5)

    def test_eta_detection(self):
        """_ETA must be 0.9."""
        self.assertAlmostEqual(_ETA, 0.9, places=10)

    def test_tau_24h(self):
        """_TAU_24H must be 86400 s."""
        self.assertEqual(_TAU_24H, 86_400.0)

    def test_delta_theta_celda(self):
        """_DELTA_THETA_CELDA must be 2.4e-19 rad."""
        self.assertAlmostEqual(_DELTA_THETA_CELDA, 2.4e-19, places=27)

    def test_fineza_cavidad(self):
        """_FINEZA_CAVIDAD must be 1e6."""
        self.assertEqual(_FINEZA_CAVIDAD, 1.0e6)

    def test_n_celdas(self):
        """_N_CELDAS must be 297."""
        self.assertEqual(_N_CELDAS, 297)

    def test_snr_objetivo(self):
        """_SNR_OBJETIVO must be 5.0 (5σ)."""
        self.assertEqual(_SNR_OBJETIVO, 5.0)

    def test_m_psi_eV_formula(self):
        """_M_PSI_EV must equal h*f0/eV_to_J."""
        expected = _H * _F0 / _EV_TO_J
        self.assertAlmostEqual(_M_PSI_EV, expected, places=25)

    def test_m_psi_eV_order(self):
        """_M_PSI_EV must be ~5.86e-13 eV."""
        self.assertGreater(_M_PSI_EV, 5.8e-13)
        self.assertLess(_M_PSI_EV, 5.9e-13)

    def test_ratio_masa_positivo(self):
        """_RATIO_MASA_PSI_PLANCK must be positive."""
        self.assertGreater(_RATIO_MASA_PSI_PLANCK, 0.0)

    def test_ratio_masa_sub_planckiano(self):
        """_RATIO_MASA_PSI_PLANCK must be much less than 1."""
        self.assertLess(_RATIO_MASA_PSI_PLANCK, 1.0e-30)


# ============================================================================
# TestDerivedConstants – 10 tests
# ============================================================================

class TestDerivedConstants(unittest.TestCase):
    """Tests for module-level derived constants."""

    def test_delta_phi_snl_formula(self):
        """_DELTA_PHI_SNL must equal 1/sqrt(eta*phi_p*tau)."""
        expected = 1.0 / math.sqrt(_ETA * _PHI_P * _TAU_24H)
        self.assertAlmostEqual(_DELTA_PHI_SNL, expected, places=20)

    def test_delta_phi_snl_order(self):
        """_DELTA_PHI_SNL must be in the range [1e-13, 2e-13] rad."""
        self.assertGreater(_DELTA_PHI_SNL, 1.0e-13)
        self.assertLess(_DELTA_PHI_SNL, 2.0e-13)

    def test_g_req_formula(self):
        """_G_REQ must equal SNR * delta_phi_snl / delta_theta."""
        expected = _SNR_OBJETIVO * _DELTA_PHI_SNL / _DELTA_THETA_CELDA
        self.assertAlmostEqual(_G_REQ, expected, places=5)

    def test_g_req_positive(self):
        """_G_REQ must be positive."""
        self.assertGreater(_G_REQ, 0.0)

    def test_factor_fineza_formula(self):
        """_FACTOR_FINEZA must equal 2F/pi."""
        expected = 2.0 * _FINEZA_CAVIDAD / math.pi
        self.assertAlmostEqual(_FACTOR_FINEZA, expected, places=5)

    def test_factor_fineza_order(self):
        """_FACTOR_FINEZA must be ~6.37e5."""
        self.assertGreater(_FACTOR_FINEZA, 6.3e5)
        self.assertLess(_FACTOR_FINEZA, 6.4e5)

    def test_cooperatividad_red_formula(self):
        """_COOPERATIVIDAD_RED must equal G_req / factor_fineza."""
        expected = _G_REQ / _FACTOR_FINEZA
        self.assertAlmostEqual(_COOPERATIVIDAD_RED, expected, places=5)

    def test_xi_formula(self):
        """_XI must equal cooperatividad_red / n_celdas."""
        expected = _COOPERATIVIDAD_RED / _N_CELDAS
        self.assertAlmostEqual(_XI, expected, places=10)

    def test_xi_sub_unitario(self):
        """_XI must be less than 1 (generoso umbral)."""
        self.assertLess(_XI, 1.0)

    def test_delta_f_critico_formula(self):
        """_DELTA_F_CRITICO must equal xi * f0 * ratio_masa."""
        expected = _XI * _F0 * _RATIO_MASA_PSI_PLANCK
        self.assertAlmostEqual(_DELTA_F_CRITICO, expected, places=50)


# ============================================================================
# TestParametrosLaser – 12 tests
# ============================================================================

class TestParametrosLaser(unittest.TestCase):
    """Tests for ParametrosLaser class."""

    def setUp(self):
        self.pl = ParametrosLaser()

    def test_default_power(self):
        """Default power must be 100 W."""
        self.assertEqual(self.pl.potencia_w, 100.0)

    def test_default_wavelength(self):
        """Default wavelength must be 1064 nm."""
        self.assertAlmostEqual(self.pl.lambda_m, 1064e-9, places=15)

    def test_energia_foton_J_order(self):
        """Photon energy must be ~1.867e-19 J for 1064 nm."""
        e = self.pl.energia_foton_J()
        self.assertGreater(e, 1.86e-19)
        self.assertLess(e, 1.88e-19)

    def test_energia_foton_J_formula(self):
        """Photon energy must equal h*c/lambda."""
        expected = _H * _C / _LAMBDA_LASER_M
        self.assertAlmostEqual(self.pl.energia_foton_J(), expected, places=30)

    def test_energia_foton_eV_order(self):
        """Photon energy must be ~1.165 eV for 1064 nm."""
        e_eV = self.pl.energia_foton_eV()
        self.assertGreater(e_eV, 1.16)
        self.assertLess(e_eV, 1.17)

    def test_energia_foton_eV_from_J(self):
        """energia_foton_eV must equal energia_foton_J / eV_to_J."""
        e_J = self.pl.energia_foton_J()
        self.assertAlmostEqual(self.pl.energia_foton_eV(), e_J / _EV_TO_J, places=10)

    def test_flujo_fotones_order(self):
        """Photon flux must be between 5.3e20 and 5.4e20 /s."""
        phi = self.pl.flujo_fotones()
        self.assertGreater(phi, 5.3e20)
        self.assertLess(phi, 5.4e20)

    def test_flujo_fotones_formula(self):
        """Photon flux must equal P / E_photon."""
        e_J = self.pl.energia_foton_J()
        expected = self.pl.potencia_w / e_J
        self.assertAlmostEqual(self.pl.flujo_fotones(), expected, places=5)

    def test_frecuencia_laser(self):
        """Laser frequency must be c/lambda."""
        f = self.pl.frecuencia_laser_hz()
        expected = _C / _LAMBDA_LASER_M
        self.assertAlmostEqual(f, expected, places=2)

    def test_frecuencia_laser_order(self):
        """Laser frequency must be ~2.82e14 Hz."""
        f = self.pl.frecuencia_laser_hz()
        self.assertGreater(f, 2.8e14)
        self.assertLess(f, 2.9e14)

    def test_custom_power(self):
        """Custom 50 W laser should give half the photon flux."""
        pl_50 = ParametrosLaser(potencia_w=50.0)
        self.assertAlmostEqual(
            pl_50.flujo_fotones(), self.pl.flujo_fotones() / 2.0, places=5
        )

    def test_repr_contains_power(self):
        """repr must mention the power in watts."""
        r = repr(self.pl)
        self.assertIn("100", r)


# ============================================================================
# TestLimiteRuidoDisparo – 15 tests
# ============================================================================

class TestLimiteRuidoDisparo(unittest.TestCase):
    """Tests for LimiteRuidoDisparo class."""

    def setUp(self):
        self.snl = LimiteRuidoDisparo()

    def test_delta_phi_snl_order(self):
        """delta_phi_snl must be between 1e-13 and 2e-13 rad."""
        snl = self.snl.delta_phi_snl()
        self.assertGreater(snl, 1.0e-13)
        self.assertLess(snl, 2.0e-13)

    def test_delta_phi_snl_formula(self):
        """delta_phi_snl must equal 1/sqrt(eta*phi_p*tau)."""
        expected = 1.0 / math.sqrt(_ETA * _PHI_P * _TAU_24H)
        self.assertAlmostEqual(self.snl.delta_phi_snl(), expected, places=20)

    def test_delta_phi_snl_decreases_with_tau(self):
        """Longer integration must reduce delta_phi_snl."""
        snl_short = LimiteRuidoDisparo(tau=_TAU_24H)
        snl_long = LimiteRuidoDisparo(tau=_TAU_24H * 4.0)
        self.assertLess(snl_long.delta_phi_snl(), snl_short.delta_phi_snl())

    def test_delta_phi_snl_scales_as_sqrt_tau(self):
        """delta_phi_snl must scale as 1/sqrt(tau)."""
        snl_1 = LimiteRuidoDisparo(tau=1.0)
        snl_4 = LimiteRuidoDisparo(tau=4.0)
        ratio = snl_4.delta_phi_snl() / snl_1.delta_phi_snl()
        self.assertAlmostEqual(ratio, 0.5, places=10)

    def test_delta_phi_snl_decreases_with_phi(self):
        """Higher photon flux must reduce delta_phi_snl."""
        snl_low = LimiteRuidoDisparo(phi_p=1e18)
        snl_high = LimiteRuidoDisparo(phi_p=1e22)
        self.assertLess(snl_high.delta_phi_snl(), snl_low.delta_phi_snl())

    def test_fotones_detectados_formula(self):
        """fotones_detectados must equal eta*phi_p*tau."""
        expected = _ETA * _PHI_P * _TAU_24H
        self.assertAlmostEqual(self.snl.fotones_detectados(), expected, places=5)

    def test_fotones_detectados_positive(self):
        """fotones_detectados must be positive."""
        self.assertGreater(self.snl.fotones_detectados(), 0.0)

    def test_fotones_detectados_order(self):
        """fotones_detectados must be order 1e25."""
        n = self.snl.fotones_detectados()
        self.assertGreater(n, 1e24)
        self.assertLess(n, 1e26)

    def test_brecha_ordenes_magnitud_positive(self):
        """brecha_ordenes_magnitud must be positive (SNL > signal)."""
        self.assertGreater(self.snl.brecha_ordenes_magnitud(), 0.0)

    def test_brecha_ordenes_magnitud_range(self):
        """Gap must be between 5 and 7 orders of magnitude."""
        brecha = self.snl.brecha_ordenes_magnitud()
        self.assertGreater(brecha, 5.0)
        self.assertLess(brecha, 7.0)

    def test_brecha_formula(self):
        """brecha must equal log10(delta_phi_snl / delta_theta_celda)."""
        expected = math.log10(self.snl.delta_phi_snl() / _DELTA_THETA_CELDA)
        self.assertAlmostEqual(self.snl.brecha_ordenes_magnitud(), expected, places=10)

    def test_snl_sobre_senyal_positive(self):
        """snl_sobre_senyal must be positive."""
        self.assertGreater(self.snl.snl_sobre_senyal(), 0.0)

    def test_snl_sobre_senyal_greater_than_one(self):
        """snl_sobre_senyal must be > 1 (need gain to detect signal)."""
        self.assertGreater(self.snl.snl_sobre_senyal(), 1.0)

    def test_snl_sobre_senyal_formula(self):
        """snl_sobre_senyal must equal delta_phi_snl / delta_theta_celda."""
        expected = self.snl.delta_phi_snl() / _DELTA_THETA_CELDA
        self.assertAlmostEqual(self.snl.snl_sobre_senyal(), expected, places=10)

    def test_repr_contains_eta(self):
        """repr must mention eta."""
        r = repr(self.snl)
        self.assertIn("η", r)


# ============================================================================
# TestMultiplicadorCooperatividad – 18 tests
# ============================================================================

class TestMultiplicadorCooperatividad(unittest.TestCase):
    """Tests for MultiplicadorCooperatividad class."""

    def setUp(self):
        self.mc = MultiplicadorCooperatividad()

    def test_g_req_positive(self):
        """g_req must be positive."""
        self.assertGreater(self.mc.g_req(), 0.0)

    def test_g_req_significant(self):
        """g_req must be at least 1e5 (substantial gain required)."""
        self.assertGreater(self.mc.g_req(), 1.0e5)

    def test_g_req_formula(self):
        """g_req must equal SNR * delta_phi_snl / delta_theta_celda."""
        expected = _SNR_OBJETIVO * _DELTA_PHI_SNL / _DELTA_THETA_CELDA
        self.assertAlmostEqual(self.mc.g_req(), expected, places=5)

    def test_g_req_proportional_to_snr(self):
        """Doubling SNR must double g_req."""
        mc_2 = MultiplicadorCooperatividad(snr_objetivo=10.0)
        self.assertAlmostEqual(mc_2.g_req(), self.mc.g_req() * 2.0, places=5)

    def test_factor_fineza_formula(self):
        """factor_fineza must equal 2*F/pi."""
        expected = 2.0 * _FINEZA_CAVIDAD / math.pi
        self.assertAlmostEqual(self.mc.factor_fineza(), expected, places=5)

    def test_factor_fineza_order(self):
        """factor_fineza must be between 6.3e5 and 6.4e5."""
        ff = self.mc.factor_fineza()
        self.assertGreater(ff, 6.3e5)
        self.assertLess(ff, 6.4e5)

    def test_factor_fineza_proportional_to_F(self):
        """Doubling finesse must double factor_fineza."""
        mc_2 = MultiplicadorCooperatividad(fineza=2.0e6)
        self.assertAlmostEqual(mc_2.factor_fineza(), self.mc.factor_fineza() * 2.0, places=5)

    def test_cooperatividad_red_formula(self):
        """cooperatividad_red must equal g_req / factor_fineza."""
        expected = self.mc.g_req() / self.mc.factor_fineza()
        self.assertAlmostEqual(self.mc.cooperatividad_red(), expected, places=10)

    def test_cooperatividad_red_positive(self):
        """cooperatividad_red must be positive."""
        self.assertGreater(self.mc.cooperatividad_red(), 0.0)

    def test_xi_formula(self):
        """xi must equal cooperatividad_red / n_celdas."""
        expected = self.mc.cooperatividad_red() / _N_CELDAS
        self.assertAlmostEqual(self.mc.xi(), expected, places=15)

    def test_xi_positive(self):
        """xi must be positive."""
        self.assertGreater(self.mc.xi(), 0.0)

    def test_xi_sub_unitario(self):
        """xi must be less than 1 (generous threshold)."""
        self.assertLess(self.mc.xi(), 1.0)

    def test_umbral_generoso_true(self):
        """umbral_generoso must be True for default parameters."""
        self.assertTrue(self.mc.umbral_generoso())

    def test_umbral_generoso_false_when_xi_ge_1(self):
        """umbral_generoso must be False when xi >= 1."""
        mc_tight = MultiplicadorCooperatividad(n_celdas=1)
        if mc_tight.xi() >= 1.0:
            self.assertFalse(mc_tight.umbral_generoso())

    def test_xi_decreases_with_n_celdas(self):
        """More cells must reduce xi (distributed gain)."""
        mc_few = MultiplicadorCooperatividad(n_celdas=10)
        mc_many = MultiplicadorCooperatividad(n_celdas=1000)
        self.assertGreater(mc_few.xi(), mc_many.xi())

    def test_xi_increases_with_snr(self):
        """Higher SNR requirement must increase xi (harder to achieve)."""
        mc_low = MultiplicadorCooperatividad(snr_objetivo=1.0)
        mc_high = MultiplicadorCooperatividad(snr_objetivo=10.0)
        self.assertLess(mc_low.xi(), mc_high.xi())

    def test_xi_decreases_with_fineza(self):
        """Higher cavity finesse must reduce xi (more gain from cavity)."""
        mc_low_f = MultiplicadorCooperatividad(fineza=1.0e4)
        mc_high_f = MultiplicadorCooperatividad(fineza=1.0e6)
        self.assertGreater(mc_low_f.xi(), mc_high_f.xi())

    def test_repr_contains_g_req(self):
        """repr must mention G_req."""
        r = repr(self.mc)
        self.assertIn("G_req", r)


# ============================================================================
# TestEcuacionViscosidadVacio – 12 tests
# ============================================================================

class TestEcuacionViscosidadVacio(unittest.TestCase):
    """Tests for EcuacionViscosidadVacio class."""

    def setUp(self):
        self.evv = EcuacionViscosidadVacio()

    def test_delta_f_critico_positive(self):
        """delta_f_critico must be positive."""
        self.assertGreater(self.evv.delta_f_critico(), 0.0)

    def test_delta_f_critico_formula(self):
        """delta_f_critico must equal xi * f0 * ratio_masa."""
        expected = _XI * _F0 * _RATIO_MASA_PSI_PLANCK
        self.assertAlmostEqual(self.evv.delta_f_critico(), expected, places=50)

    def test_delta_f_critico_tiny(self):
        """delta_f_critico must be extremely small (< 1e-30 Hz)."""
        self.assertLess(self.evv.delta_f_critico(), 1.0e-30)

    def test_delta_f_critico_proportional_to_xi(self):
        """Doubling xi must double delta_f_critico."""
        evv_2 = EcuacionViscosidadVacio(xi=_XI * 2.0)
        self.assertAlmostEqual(evv_2.delta_f_critico(), self.evv.delta_f_critico() * 2.0, places=50)

    def test_umbral_coherencia_satisfecho_zero(self):
        """Zero drift must always satisfy the threshold."""
        self.assertTrue(self.evv.umbral_coherencia_satisfecho(0.0))

    def test_umbral_coherencia_satisfecho_negative(self):
        """Negative drift must satisfy the threshold (drift below zero)."""
        self.assertTrue(self.evv.umbral_coherencia_satisfecho(-1.0))

    def test_umbral_coherencia_not_satisfecho_large(self):
        """Large drift must not satisfy the threshold."""
        self.assertFalse(self.evv.umbral_coherencia_satisfecho(1.0e10))

    def test_ratio_deriva_umbral_zero(self):
        """Zero drift gives ratio 0."""
        self.assertEqual(self.evv.ratio_deriva_umbral(0.0), 0.0)

    def test_ratio_deriva_umbral_at_threshold(self):
        """At the critical frequency, ratio equals 1."""
        self.assertAlmostEqual(
            self.evv.ratio_deriva_umbral(self.evv.delta_f_critico()),
            1.0,
            places=10,
        )

    def test_ratio_deriva_umbral_positive(self):
        """Positive drift gives positive ratio."""
        self.assertGreater(self.evv.ratio_deriva_umbral(1e-50), 0.0)

    def test_custom_xi(self):
        """Custom xi must change delta_f_critico proportionally."""
        xi_custom = 0.1
        evv_custom = EcuacionViscosidadVacio(xi=xi_custom)
        evv_default = EcuacionViscosidadVacio(xi=_XI)
        ratio = evv_custom.delta_f_critico() / evv_default.delta_f_critico()
        self.assertAlmostEqual(ratio, xi_custom / _XI, places=10)

    def test_repr_contains_delta_f(self):
        """repr must mention Δf_crítico."""
        r = repr(self.evv)
        self.assertIn("Δf_crítico", r)


# ============================================================================
# TestSistemaIRSLuna – 12 tests
# ============================================================================

class TestSistemaIRSLuna(unittest.TestCase):
    """Tests for SistemaIRSLuna orchestrator."""

    def setUp(self):
        self.sistema = SistemaIRSLuna()
        self.resultado = self.sistema.calcular()

    def test_calcular_returns_resultado(self):
        """calcular() must return a ResultadoIRSLuna instance."""
        self.assertIsInstance(self.resultado, ResultadoIRSLuna)

    def test_f0_hz(self):
        """Resultado f0_hz must equal 141.7001."""
        self.assertAlmostEqual(self.resultado.f0_hz, 141.7001, places=4)

    def test_phi_p_order(self):
        """Resultado phi_p must be between 5.3e20 and 5.4e20."""
        self.assertGreater(self.resultado.phi_p, 5.3e20)
        self.assertLess(self.resultado.phi_p, 5.4e20)

    def test_delta_phi_snl_positive(self):
        """Resultado delta_phi_snl must be positive."""
        self.assertGreater(self.resultado.delta_phi_snl, 0.0)

    def test_delta_phi_snl_small(self):
        """Resultado delta_phi_snl must be < 1e-12 rad."""
        self.assertLess(self.resultado.delta_phi_snl, 1.0e-12)

    def test_g_req_significant(self):
        """Resultado g_req must be at least 1e5."""
        self.assertGreater(self.resultado.g_req, 1.0e5)

    def test_xi_sub_unitario(self):
        """Resultado xi must be in (0, 1)."""
        self.assertGreater(self.resultado.xi, 0.0)
        self.assertLess(self.resultado.xi, 1.0)

    def test_umbral_generoso(self):
        """Resultado umbral_generoso must be True."""
        self.assertTrue(self.resultado.umbral_generoso)

    def test_senyal_localizada(self):
        """Resultado senyal_localizada must be True."""
        self.assertTrue(self.resultado.senyal_localizada)

    def test_mensaje_contains_senyal(self):
        """mensaje must contain 'SEÑAL LOCALIZADA' or system info."""
        self.assertIsInstance(self.resultado.mensaje, str)
        self.assertGreater(len(self.resultado.mensaje), 0)

    def test_confianza_sigma(self):
        """confianza_sigma must be >= 5.0."""
        self.assertGreaterEqual(self.resultado.confianza_sigma, 5.0)

    def test_tiempo_deteccion_positive(self):
        """tiempo_deteccion_h must be positive."""
        self.assertGreater(self.resultado.tiempo_deteccion_h, 0.0)


# ============================================================================
# TestResultadoIRSLunaDataclass – 8 tests
# ============================================================================

class TestResultadoIRSLunaDataclass(unittest.TestCase):
    """Tests for ResultadoIRSLuna dataclass."""

    def setUp(self):
        self.resultado = SistemaIRSLuna().calcular()

    def test_has_f0_hz(self):
        self.assertTrue(hasattr(self.resultado, "f0_hz"))

    def test_has_phi_p(self):
        self.assertTrue(hasattr(self.resultado, "phi_p"))

    def test_has_delta_phi_snl(self):
        self.assertTrue(hasattr(self.resultado, "delta_phi_snl"))

    def test_has_g_req(self):
        self.assertTrue(hasattr(self.resultado, "g_req"))

    def test_has_xi(self):
        self.assertTrue(hasattr(self.resultado, "xi"))

    def test_has_delta_f_critico(self):
        self.assertTrue(hasattr(self.resultado, "delta_f_critico"))

    def test_has_senyal_localizada(self):
        self.assertTrue(hasattr(self.resultado, "senyal_localizada"))

    def test_has_mensaje(self):
        self.assertTrue(hasattr(self.resultado, "mensaje"))


# ============================================================================
# TestLimiteRuidoDisparoCalcularAPI – 20 tests
# ============================================================================

class TestLimiteRuidoDisparoCalcularAPI(unittest.TestCase):
    """Tests for the public API function limite_ruido_disparo_calcular()."""

    def setUp(self):
        self.result = limite_ruido_disparo_calcular()

    def test_returns_dict(self):
        """API must return a dict."""
        self.assertIsInstance(self.result, dict)

    def test_f0_hz_key(self):
        """Result must contain 'f0_hz' key."""
        self.assertIn("f0_hz", self.result)

    def test_f0_hz_value(self):
        """f0_hz must be 141.7001."""
        self.assertAlmostEqual(self.result["f0_hz"], 141.7001, places=4)

    def test_phi_p_key(self):
        """Result must contain 'phi_p' key."""
        self.assertIn("phi_p", self.result)

    def test_phi_p_range(self):
        """phi_p must be between 5.3e20 and 5.4e20."""
        self.assertGreater(self.result["phi_p"], 5.3e20)
        self.assertLess(self.result["phi_p"], 5.4e20)

    def test_energia_foton_J_key(self):
        """Result must contain 'energia_foton_J' key."""
        self.assertIn("energia_foton_J", self.result)

    def test_energia_foton_eV_key(self):
        """Result must contain 'energia_foton_eV' key."""
        self.assertIn("energia_foton_eV", self.result)

    def test_delta_phi_snl_key(self):
        """Result must contain 'delta_phi_snl' key."""
        self.assertIn("delta_phi_snl", self.result)

    def test_delta_phi_snl_small(self):
        """delta_phi_snl must be < 1e-12 rad."""
        self.assertLess(self.result["delta_phi_snl"], 1.0e-12)

    def test_fotones_detectados_key(self):
        """Result must contain 'fotones_detectados' key."""
        self.assertIn("fotones_detectados", self.result)

    def test_brecha_ordenes_key(self):
        """Result must contain 'brecha_ordenes' key."""
        self.assertIn("brecha_ordenes", self.result)

    def test_g_req_key(self):
        """Result must contain 'g_req' key."""
        self.assertIn("g_req", self.result)

    def test_g_req_positive(self):
        """g_req must be positive."""
        self.assertGreater(self.result["g_req"], 0.0)

    def test_xi_key(self):
        """Result must contain 'xi' key."""
        self.assertIn("xi", self.result)

    def test_xi_range(self):
        """xi must be between 0 and 1."""
        self.assertGreater(self.result["xi"], 0.0)
        self.assertLess(self.result["xi"], 1.0)

    def test_umbral_generoso_key(self):
        """Result must contain 'umbral_generoso' key."""
        self.assertIn("umbral_generoso", self.result)

    def test_umbral_generoso_true(self):
        """umbral_generoso must be True."""
        self.assertTrue(self.result["umbral_generoso"])

    def test_senyal_localizada_key(self):
        """Result must contain 'senyal_localizada' key."""
        self.assertIn("senyal_localizada", self.result)

    def test_senyal_localizada_true(self):
        """senyal_localizada must be True."""
        self.assertTrue(self.result["senyal_localizada"])

    def test_mensaje_key(self):
        """Result must contain 'mensaje' key with non-empty string."""
        self.assertIn("mensaje", self.result)
        self.assertIsInstance(self.result["mensaje"], str)
        self.assertGreater(len(self.result["mensaje"]), 0)


# ============================================================================
# TestAPIParametrizacion – 10 tests
# ============================================================================

class TestAPIParametrizacion(unittest.TestCase):
    """Tests for parameterized API calls."""

    def test_custom_f0(self):
        """Custom f0 must appear in result."""
        result = limite_ruido_disparo_calcular(f0=200.0)
        self.assertAlmostEqual(result["f0_hz"], 200.0, places=4)

    def test_higher_power_gives_more_photons(self):
        """200 W laser must give roughly twice the photon flux."""
        result_100 = limite_ruido_disparo_calcular(potencia_w=100.0)
        result_200 = limite_ruido_disparo_calcular(potencia_w=200.0)
        ratio = result_200["phi_p"] / result_100["phi_p"]
        self.assertAlmostEqual(ratio, 2.0, places=5)

    def test_longer_tau_reduces_snl(self):
        """4x longer integration must halve delta_phi_snl."""
        result_1 = limite_ruido_disparo_calcular(tau=_TAU_24H)
        result_4 = limite_ruido_disparo_calcular(tau=_TAU_24H * 4.0)
        ratio = result_4["delta_phi_snl"] / result_1["delta_phi_snl"]
        self.assertAlmostEqual(ratio, 0.5, places=10)

    def test_higher_snr_increases_g_req(self):
        """Higher SNR must increase g_req proportionally."""
        result_5 = limite_ruido_disparo_calcular(snr_objetivo=5.0)
        result_10 = limite_ruido_disparo_calcular(snr_objetivo=10.0)
        ratio = result_10["g_req"] / result_5["g_req"]
        self.assertAlmostEqual(ratio, 2.0, places=10)

    def test_more_cells_reduces_xi(self):
        """More cells must reduce xi proportionally."""
        result_297 = limite_ruido_disparo_calcular(n_celdas=297)
        result_594 = limite_ruido_disparo_calcular(n_celdas=594)
        ratio = result_594["xi"] / result_297["xi"]
        self.assertAlmostEqual(ratio, 0.5, places=10)

    def test_higher_fineza_reduces_xi(self):
        """Higher finesse must reduce xi (more gain from cavity)."""
        result_low = limite_ruido_disparo_calcular(fineza=1.0e4)
        result_high = limite_ruido_disparo_calcular(fineza=1.0e6)
        self.assertGreater(result_low["xi"], result_high["xi"])

    def test_all_keys_present_custom(self):
        """Custom call must return all expected keys."""
        result = limite_ruido_disparo_calcular(potencia_w=50.0, eta=0.8, tau=3600.0)
        expected_keys = [
            "f0_hz", "phi_p", "energia_foton_J", "energia_foton_eV",
            "delta_phi_snl", "fotones_detectados", "brecha_ordenes",
            "g_req", "factor_fineza", "cooperatividad_red", "xi",
            "umbral_generoso", "delta_f_critico", "tiempo_deteccion_h",
            "confianza_sigma", "senyal_localizada", "mensaje",
        ]
        for key in expected_keys:
            self.assertIn(key, result, f"Key '{key}' missing from result")

    def test_factor_fineza_consistent(self):
        """factor_fineza in result must equal 2F/pi."""
        result = limite_ruido_disparo_calcular(fineza=5.0e5)
        expected = 2.0 * 5.0e5 / math.pi
        self.assertAlmostEqual(result["factor_fineza"], expected, places=5)

    def test_g_req_xi_consistency(self):
        """xi must equal g_req / (factor_fineza * n_celdas)."""
        result = limite_ruido_disparo_calcular()
        expected_xi = result["g_req"] / (result["factor_fineza"] * _N_CELDAS)
        self.assertAlmostEqual(result["xi"], expected_xi, places=10)

    def test_delta_phi_snl_consistency(self):
        """delta_phi_snl^2 * fotones_detectados must equal 1."""
        result = limite_ruido_disparo_calcular()
        product = result["delta_phi_snl"] ** 2 * result["fotones_detectados"]
        self.assertAlmostEqual(product, 1.0, places=5)


if __name__ == "__main__":
    unittest.main()
