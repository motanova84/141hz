"""
Tests for physics.resonancia_total_v7 — Identidad de Resonancia Total v7.0

Pruebas que cubren las 6 clases y la función de la API pública:
  - CorreccionSchwinger              – (1 + α/2π), corrección QED de primer orden
  - IdentidadResonanciaV70           – fórmula principal v7.0
  - GeometriaHeptagonoHiperbolico    – corrección cos(π/7)
  - FrecuenciaDeBroglieMediaGeometrica – frecuencia de De Broglie media geométrica
  - ImpedanciaHall                   – Z₀ vs h/e² en la red de 7 nodos
  - SistemaResonanciaTotalV7         – orquestador
  - resonancia_total_v7_calcular()   – API pública

Invariantes clave verificados:
  - schwinger_factor = (1 + α/2π) ≈ 1.001161
  - cos(π/7) ≈ 0.9009
  - f_base_ref = 139.764 Hz
  - f_schwinger ≈ 139.926 Hz
  - f_heptagon ≈ 155.307 Hz
  - φ^π ≈ 4.5348
  - m_p/m_e ≈ 1836.15
  - Z₀ ≈ 376.73 Ω, R_K ≈ 25812.8 Ω, ratio_hall_N7 ≈ 9.788
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.resonancia_total_v7 import (
    # Module-level constants
    _F0,
    _C,
    _H,
    _HBAR,
    _ALPHA,
    _PHI,
    _N7,
    _M_PROTON_KG,
    _LAMBDA_PROTON_M,
    _M_ELECTRON_KG,
    _LAMBDA_ELECTRON_M,
    _M_RATIO_P_E,
    _LAMBDA_COSM,
    _L_DESITTER_M,
    _G_NEWTON,
    _L_PLANCK_M,
    _MU0,
    _Z0_OHM,
    _E_CHARGE,
    _R_HALL_OHM,
    _F_BASE_REF_HZ,
    _SCHWINGER_FACTOR,
    _PHI_PI,
    _COS_PI_7,
    _F_BASE_SCHWINGER_HZ,
    _F_BASE_HEPTAGON_HZ,
    _LAMBDA_GEOM_MEAN_M,
    _LOG_COSM_PLANCK,
    _LAMBDA_C_DEBROGLIE_M,
    _F_DEBROGLIE_HZ,
    _F_V70_HZ,
    _HALL_RATIO_N7,
    _RESIDUO_RELATIVO,
    # Classes
    CorreccionSchwinger,
    IdentidadResonanciaV70,
    GeometriaHeptagonoHiperbolico,
    FrecuenciaDeBroglieMediaGeometrica,
    ImpedanciaHall,
    SistemaResonanciaTotalV7,
    ResultadoResonanciaTotalV7,
    # Public API
    resonancia_total_v7_calcular,
)


# ============================================================================
# TestModuleConstants – 22 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests for module-level constants."""

    def test_f0_value(self):
        """_F0 must equal 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_c_value(self):
        """_C must equal exact speed of light."""
        self.assertEqual(_C, 299_792_458.0)

    def test_h_planck_value(self):
        """_H must equal the CODATA 2018 Planck constant."""
        self.assertAlmostEqual(_H, 6.62607015e-34, places=42)

    def test_hbar_equals_h_over_2pi(self):
        """_HBAR must equal _H / (2π)."""
        self.assertAlmostEqual(_HBAR, _H / (2.0 * math.pi), places=44)

    def test_alpha_value(self):
        """Fine structure constant must be ≈ 1/137.036."""
        self.assertAlmostEqual(_ALPHA, 7.2973525693e-3, places=12)
        self.assertAlmostEqual(1.0 / _ALPHA, 137.0, delta=0.1)

    def test_phi_value(self):
        """Golden ratio φ must equal (1+√5)/2 ≈ 1.6180."""
        self.assertAlmostEqual(_PHI, (1.0 + math.sqrt(5.0)) / 2.0, places=14)
        self.assertAlmostEqual(_PHI, 1.6180, delta=0.001)

    def test_n7_value(self):
        """N₇ must equal 7."""
        self.assertEqual(_N7, 7)

    def test_lambda_proton_order(self):
        """Proton Compton wavelength must be ≈ 1.321×10⁻¹⁵ m."""
        self.assertGreater(_LAMBDA_PROTON_M, 1.321e-15)
        self.assertLess(_LAMBDA_PROTON_M, 1.322e-15)

    def test_lambda_electron_order(self):
        """Electron Compton wavelength must be ≈ 2.426×10⁻¹² m."""
        self.assertGreater(_LAMBDA_ELECTRON_M, 2.426e-12)
        self.assertLess(_LAMBDA_ELECTRON_M, 2.427e-12)

    def test_mass_ratio_p_e(self):
        """Proton/electron mass ratio must be ≈ 1836.15."""
        self.assertAlmostEqual(_M_RATIO_P_E, 1836.15, delta=0.01)

    def test_l_desitter_order(self):
        """de Sitter radius must be ≈ 1.64×10²⁶ m."""
        self.assertGreater(_L_DESITTER_M, 1.6e26)
        self.assertLess(_L_DESITTER_M, 1.7e26)

    def test_l_planck_order(self):
        """Planck length must be ≈ 1.616×10⁻³⁵ m."""
        self.assertAlmostEqual(_L_PLANCK_M, 1.61626e-35, delta=1e-38)

    def test_z0_value(self):
        """Impedance of free space must be ≈ 376.73 Ω."""
        self.assertAlmostEqual(_Z0_OHM, 376.73, delta=0.01)

    def test_r_hall_value(self):
        """Quantum Hall resistance must be ≈ 25812.8 Ω."""
        self.assertAlmostEqual(_R_HALL_OHM, 25812.8, delta=0.5)

    def test_schwinger_factor(self):
        """Schwinger factor must be ≈ 1.001161."""
        self.assertAlmostEqual(_SCHWINGER_FACTOR, 1.001161, delta=0.000001)
        self.assertEqual(_SCHWINGER_FACTOR, 1.0 + _ALPHA / (2.0 * math.pi))

    def test_phi_pi_value(self):
        """φ^π must be ≈ 4.5348."""
        self.assertAlmostEqual(_PHI_PI, _PHI ** math.pi, places=12)
        self.assertAlmostEqual(_PHI_PI, 4.5348, delta=0.001)

    def test_cos_pi_7_value(self):
        """cos(π/7) must be ≈ 0.9009."""
        self.assertAlmostEqual(_COS_PI_7, math.cos(math.pi / 7.0), places=12)
        self.assertAlmostEqual(_COS_PI_7, 0.9009, delta=0.001)

    def test_f_base_ref(self):
        """Reference base frequency must be exactly 139.764 Hz."""
        self.assertEqual(_F_BASE_REF_HZ, 139.764)

    def test_f_base_schwinger(self):
        """Schwinger-corrected base frequency must be ≈ 139.926 Hz."""
        self.assertAlmostEqual(_F_BASE_SCHWINGER_HZ, 139.926, delta=0.002)
        self.assertAlmostEqual(
            _F_BASE_SCHWINGER_HZ, _F_BASE_REF_HZ * _SCHWINGER_FACTOR, places=10
        )

    def test_f_base_heptagon(self):
        """Heptagon-corrected frequency must be ≈ 155.307 Hz."""
        self.assertAlmostEqual(_F_BASE_HEPTAGON_HZ, 155.307, delta=0.01)
        self.assertAlmostEqual(
            _F_BASE_HEPTAGON_HZ, _F_BASE_SCHWINGER_HZ / _COS_PI_7, places=10
        )

    def test_residuo_relativo_positive(self):
        """Residual (f₀ - f_schwinger) / f₀ must be positive."""
        self.assertGreater(_RESIDUO_RELATIVO, 0.0)

    def test_hall_ratio_n7_value(self):
        """R_K / (Z₀·N₇) must be ≈ 9.788."""
        self.assertAlmostEqual(_HALL_RATIO_N7, 9.788, delta=0.01)


# ============================================================================
# TestCorreccionSchwinger – 10 tests
# ============================================================================

class TestCorreccionSchwinger(unittest.TestCase):
    """Tests for CorreccionSchwinger class."""

    def setUp(self):
        self.cs = CorreccionSchwinger()

    def test_default_alpha(self):
        """Default alpha must equal module constant."""
        self.assertEqual(self.cs.alpha, _ALPHA)

    def test_factor_value(self):
        """Factor must equal (1 + α/2π) ≈ 1.001161."""
        f = self.cs.factor()
        self.assertAlmostEqual(f, 1.001161, delta=0.000001)

    def test_factor_greater_than_one(self):
        """Schwinger factor must always be greater than 1."""
        self.assertGreater(self.cs.factor(), 1.0)

    def test_correccion_relativa(self):
        """Relative correction must equal α/2π ≈ 1.161×10⁻³."""
        cr = self.cs.correccion_relativa()
        self.assertAlmostEqual(cr, _ALPHA / (2.0 * math.pi), places=14)
        self.assertAlmostEqual(cr, 1.161e-3, delta=0.001e-3)

    def test_factor_equals_one_plus_correccion(self):
        """Factor must equal 1 + correccion_relativa."""
        self.assertAlmostEqual(
            self.cs.factor(), 1.0 + self.cs.correccion_relativa(), places=14
        )

    def test_aplicar_base_frequency(self):
        """Applying to 139.764 Hz must yield ≈ 139.926 Hz."""
        result = self.cs.aplicar(139.764)
        self.assertAlmostEqual(result, 139.926, delta=0.002)

    def test_aplicar_zero(self):
        """Applying to 0 Hz must return 0."""
        self.assertEqual(self.cs.aplicar(0.0), 0.0)

    def test_aplicar_f0(self):
        """Applying to f₀ must return f₀ × factor."""
        result = self.cs.aplicar(_F0)
        self.assertAlmostEqual(result, _F0 * self.cs.factor(), places=10)

    def test_custom_alpha(self):
        """Custom alpha must change factor correctly."""
        cs_custom = CorreccionSchwinger(alpha=0.01)
        expected = 1.0 + 0.01 / (2.0 * math.pi)
        self.assertAlmostEqual(cs_custom.factor(), expected, places=14)

    def test_repr_contains_factor(self):
        """Repr must mention the factor value."""
        r = repr(self.cs)
        self.assertIn("1+α/2π", r)


# ============================================================================
# TestIdentidadResonanciaV70 – 12 tests
# ============================================================================

class TestIdentidadResonanciaV70(unittest.TestCase):
    """Tests for IdentidadResonanciaV70 class."""

    def setUp(self):
        self.v7 = IdentidadResonanciaV70()

    def test_default_alpha(self):
        """Default alpha must equal module constant."""
        self.assertEqual(self.v7.alpha, _ALPHA)

    def test_default_phi(self):
        """Default phi must equal module constant."""
        self.assertEqual(self.v7.phi, _PHI)

    def test_default_n7(self):
        """Default n7 must equal 7."""
        self.assertEqual(self.v7.n7, _N7)

    def test_phi_pi_value(self):
        """φ^π must be ≈ 4.5348."""
        self.assertAlmostEqual(self.v7.phi_pi(), 4.5348, delta=0.001)

    def test_phi_pi_positive(self):
        """φ^π must be positive."""
        self.assertGreater(self.v7.phi_pi(), 0.0)

    def test_termino_geometrico_positive(self):
        """Geometric term c/(2π√(λ_p·L_Λ)) must be positive."""
        self.assertGreater(self.v7.termino_geometrico_hz(), 0.0)

    def test_factor_espectral_value(self):
        """α·φ^π/N₇ must be ≈ 4.727×10⁻³."""
        fe = self.v7.factor_espectral()
        self.assertAlmostEqual(fe, 4.727e-3, delta=0.01e-3)

    def test_factor_espectral_positive(self):
        """Factor espectral must be positive."""
        self.assertGreater(self.v7.factor_espectral(), 0.0)

    def test_frecuencia_base_positive(self):
        """Base frequency (no Schwinger) must be positive."""
        self.assertGreater(self.v7.frecuencia_base_hz(), 0.0)

    def test_frecuencia_v7_greater_than_base(self):
        """v7.0 frequency with Schwinger must exceed base."""
        self.assertGreater(self.v7.frecuencia_v7_hz(), self.v7.frecuencia_base_hz())

    def test_frecuencia_v7_positive(self):
        """v7.0 frequency must be positive."""
        self.assertGreater(self.v7.frecuencia_v7_hz(), 0.0)

    def test_frecuencia_v7_consistency(self):
        """v7.0 frequency must equal base × Schwinger factor."""
        schwinger = 1.0 + self.v7.alpha / (2.0 * math.pi)
        expected = self.v7.frecuencia_base_hz() * schwinger
        self.assertAlmostEqual(self.v7.frecuencia_v7_hz(), expected, places=10)


# ============================================================================
# TestGeometriaHeptagonoHiperbolico – 10 tests
# ============================================================================

class TestGeometriaHeptagonoHiperbolico(unittest.TestCase):
    """Tests for GeometriaHeptagonoHiperbolico class."""

    def setUp(self):
        self.ghh = GeometriaHeptagonoHiperbolico()

    def test_default_n7(self):
        """Default n7 must equal 7."""
        self.assertEqual(self.ghh.n7, _N7)

    def test_cos_pi_7_value(self):
        """cos(π/7) must be ≈ 0.9009."""
        self.assertAlmostEqual(self.ghh.cos_pi_n7(), 0.9009, delta=0.001)

    def test_cos_pi_7_exact(self):
        """cos(π/N₇) must equal math.cos(math.pi/7) exactly."""
        self.assertAlmostEqual(
            self.ghh.cos_pi_n7(), math.cos(math.pi / 7.0), places=14
        )

    def test_cos_pi_7_between_zero_and_one(self):
        """cos(π/7) must be between 0 and 1."""
        self.assertGreater(self.ghh.cos_pi_n7(), 0.0)
        self.assertLess(self.ghh.cos_pi_n7(), 1.0)

    def test_area_efectiva_value(self):
        """Effective area N₇·cos(π/N₇) must be ≈ 6.307."""
        self.assertAlmostEqual(self.ghh.area_efectiva(), 6.307, delta=0.001)

    def test_area_efectiva_less_than_n7(self):
        """Effective area must be less than N₇ (since cos < 1)."""
        self.assertLess(self.ghh.area_efectiva(), self.ghh.n7)

    def test_aplicar_correccion_base(self):
        """Applying to 139.926 Hz must yield ≈ 155.307 Hz."""
        result = self.ghh.aplicar_correccion(139.926)
        self.assertAlmostEqual(result, 155.307, delta=0.01)

    def test_aplicar_correccion_increases_frequency(self):
        """Division by cos(π/7) < 1 must increase the frequency."""
        f_in = 100.0
        self.assertGreater(self.ghh.aplicar_correccion(f_in), f_in)

    def test_aplicar_correccion_zero(self):
        """Applying to 0 Hz must return 0."""
        self.assertEqual(self.ghh.aplicar_correccion(0.0), 0.0)

    def test_custom_n7(self):
        """Custom N₇ must use correct cosine."""
        ghh5 = GeometriaHeptagonoHiperbolico(n7=5)
        self.assertAlmostEqual(ghh5.cos_pi_n7(), math.cos(math.pi / 5.0), places=14)


# ============================================================================
# TestFrecuenciaDeBroglieMediaGeometrica – 12 tests
# ============================================================================

class TestFrecuenciaDeBroglieMediaGeometrica(unittest.TestCase):
    """Tests for FrecuenciaDeBroglieMediaGeometrica class."""

    def setUp(self):
        self.fdb = FrecuenciaDeBroglieMediaGeometrica()

    def test_default_lambda_proton(self):
        """Default proton Compton wavelength must equal module constant."""
        self.assertEqual(self.fdb.lambda_proton_m, _LAMBDA_PROTON_M)

    def test_default_lambda_electron(self):
        """Default electron Compton wavelength must equal module constant."""
        self.assertEqual(self.fdb.lambda_electron_m, _LAMBDA_ELECTRON_M)

    def test_media_geometrica_compton_positive(self):
        """Geometric mean of Compton wavelengths must be positive."""
        self.assertGreater(self.fdb.media_geometrica_compton_m(), 0.0)

    def test_media_geometrica_compton_between_lambda_p_and_e(self):
        """Geometric mean must be between λ_p and λ_e."""
        mg = self.fdb.media_geometrica_compton_m()
        self.assertGreater(mg, _LAMBDA_PROTON_M)
        self.assertLess(mg, _LAMBDA_ELECTRON_M)

    def test_factor_logaritmico_positive(self):
        """Logarithmic cosmological factor must be positive."""
        self.assertGreater(self.fdb.factor_logaritmico_cosmologico(), 0.0)

    def test_factor_logaritmico_value(self):
        """Logarithmic factor √(ln(L_Λ/L_P)) must be ≈ 11.85."""
        self.assertAlmostEqual(
            self.fdb.factor_logaritmico_cosmologico(), 11.85, delta=0.1
        )

    def test_lambda_c_debroglie_positive(self):
        """λ̄_C must be positive."""
        self.assertGreater(self.fdb.lambda_c_debroglie_m(), 0.0)

    def test_lambda_c_debroglie_equals_product(self):
        """λ̄_C must equal geometric_mean × log_factor."""
        expected = (
            self.fdb.media_geometrica_compton_m()
            * self.fdb.factor_logaritmico_cosmologico()
        )
        self.assertAlmostEqual(
            self.fdb.lambda_c_debroglie_m(), expected, places=20
        )

    def test_frecuencia_debroglie_positive(self):
        """De Broglie frequency must be positive."""
        self.assertGreater(self.fdb.frecuencia_debroglie_hz(), 0.0)

    def test_frecuencia_debroglie_equals_c_over_lambda(self):
        """f_dB must equal c / λ̄_C."""
        expected = _C / self.fdb.lambda_c_debroglie_m()
        self.assertAlmostEqual(
            self.fdb.frecuencia_debroglie_hz(), expected, places=5
        )

    def test_ratio_masa_proton_electron(self):
        """m_p/m_e ratio must be ≈ 1836.15."""
        ratio = self.fdb.ratio_masa_proton_electron()
        self.assertAlmostEqual(ratio, 1836.15, delta=0.01)

    def test_ratio_masa_equals_lambda_ratio(self):
        """m_p/m_e must equal λ_e/λ_p (inverse Compton wavelength ratio)."""
        expected = _LAMBDA_ELECTRON_M / _LAMBDA_PROTON_M
        self.assertAlmostEqual(
            self.fdb.ratio_masa_proton_electron(), expected, places=10
        )


# ============================================================================
# TestImpedanciaHall – 12 tests
# ============================================================================

class TestImpedanciaHall(unittest.TestCase):
    """Tests for ImpedanciaHall class."""

    def setUp(self):
        self.ih = ImpedanciaHall()

    def test_default_z0(self):
        """Default Z₀ must equal module constant."""
        self.assertEqual(self.ih.z0_ohm, _Z0_OHM)

    def test_default_r_hall(self):
        """Default R_K must equal module constant."""
        self.assertEqual(self.ih.r_hall_ohm, _R_HALL_OHM)

    def test_default_n7(self):
        """Default n7 must equal 7."""
        self.assertEqual(self.ih.n7, _N7)

    def test_z0_value(self):
        """Z₀ = μ₀·c must be ≈ 376.73 Ω."""
        self.assertAlmostEqual(self.ih.z0_ohm, 376.73, delta=0.01)

    def test_r_hall_value(self):
        """R_K = h/e² must be ≈ 25812.8 Ω."""
        self.assertAlmostEqual(self.ih.r_hall_ohm, 25812.8, delta=0.5)

    def test_r_hall_greater_than_z0(self):
        """R_K must be much greater than Z₀."""
        self.assertGreater(self.ih.r_hall_ohm, self.ih.z0_ohm * 10)

    def test_ratio_hall_z0(self):
        """R_K / Z₀ must be ≈ 68.52."""
        self.assertAlmostEqual(self.ih.ratio_hall_z0(), 68.52, delta=0.1)

    def test_ratio_hall_n7_value(self):
        """R_K / (Z₀·N₇) must be ≈ 9.788."""
        self.assertAlmostEqual(self.ih.ratio_hall_n7(), 9.788, delta=0.01)

    def test_ratio_hall_n7_equals_ratio_z0_over_n7(self):
        """ratio_hall_n7 must equal ratio_hall_z0 / N₇."""
        self.assertAlmostEqual(
            self.ih.ratio_hall_n7(),
            self.ih.ratio_hall_z0() / self.ih.n7,
            places=10,
        )

    def test_impedancia_efectiva_red(self):
        """Effective network impedance Z₀·N₇ must be ≈ 2637.1 Ω."""
        self.assertAlmostEqual(self.ih.impedancia_efectiva_red_ohm(), 2637.1, delta=1.0)

    def test_longitud_onda_resonancia(self):
        """Resonance wavelength c/f₀ must be ≈ 2,115,683 m."""
        lam = self.ih.longitud_onda_resonancia_m()
        self.assertAlmostEqual(lam, 2_115_683.0, delta=1.0)

    def test_custom_f0(self):
        """Custom f₀ must change the resonance wavelength."""
        ih2 = ImpedanciaHall(f0=200.0)
        self.assertAlmostEqual(ih2.longitud_onda_resonancia_m(), _C / 200.0, places=5)


# ============================================================================
# TestSistemaResonanciaTotalV7 – 12 tests
# ============================================================================

class TestSistemaResonanciaTotalV7(unittest.TestCase):
    """Tests for SistemaResonanciaTotalV7 orchestrator class."""

    def setUp(self):
        self.sistema = SistemaResonanciaTotalV7()
        self.resultado = self.sistema.calcular()

    def test_default_f0(self):
        """Default f₀ must equal module constant."""
        self.assertEqual(self.sistema.f0, _F0)

    def test_default_f_base_ref(self):
        """Default f_base_ref must equal module constant."""
        self.assertEqual(self.sistema.f_base_ref_hz, _F_BASE_REF_HZ)

    def test_resultado_is_dataclass(self):
        """Calcular must return a ResultadoResonanciaTotalV7 instance."""
        self.assertIsInstance(self.resultado, ResultadoResonanciaTotalV7)

    def test_resultado_f0_hz(self):
        """Result f0_hz must equal the system f₀."""
        self.assertEqual(self.resultado.f0_hz, _F0)

    def test_resultado_schwinger_factor(self):
        """Result schwinger_factor must be ≈ 1.001161."""
        self.assertAlmostEqual(self.resultado.schwinger_factor, 1.001161, delta=0.000001)

    def test_resultado_f_schwinger_hz(self):
        """Result f_schwinger_hz must be ≈ 139.926 Hz."""
        self.assertAlmostEqual(self.resultado.f_schwinger_hz, 139.926, delta=0.002)

    def test_resultado_cos_pi_7(self):
        """Result cos_pi_7 must be ≈ 0.9009."""
        self.assertAlmostEqual(self.resultado.cos_pi_7, 0.9009, delta=0.001)

    def test_resultado_f_heptagon_hz(self):
        """Result f_heptagon_hz must be ≈ 155.307 Hz."""
        self.assertAlmostEqual(self.resultado.f_heptagon_hz, 155.307, delta=0.01)

    def test_resultado_ratio_masa_p_e(self):
        """Result proton/electron mass ratio must be ≈ 1836.15."""
        self.assertAlmostEqual(self.resultado.ratio_masa_p_e, 1836.15, delta=0.01)

    def test_resultado_ratio_hall_n7(self):
        """Result ratio_hall_n7 must be ≈ 9.788."""
        self.assertAlmostEqual(self.resultado.ratio_hall_n7, 9.788, delta=0.01)

    def test_resultado_residuo_relativo_positive(self):
        """Residual (f₀ - f_schwinger)/f₀ must be positive."""
        self.assertGreater(self.resultado.residuo_relativo, 0.0)

    def test_resultado_mensaje_not_empty(self):
        """Result message must be a non-empty string."""
        self.assertIsInstance(self.resultado.mensaje, str)
        self.assertGreater(len(self.resultado.mensaje), 0)


# ============================================================================
# TestResonanciaTotalV7Calcular – 18 tests
# ============================================================================

class TestResonanciaTotalV7Calcular(unittest.TestCase):
    """Tests for the public API function resonancia_total_v7_calcular()."""

    def setUp(self):
        self.result = resonancia_total_v7_calcular()

    def test_returns_dict(self):
        """Function must return a dict."""
        self.assertIsInstance(self.result, dict)

    def test_f0_hz(self):
        """Result f0_hz must equal 141.7001 Hz."""
        self.assertEqual(self.result["f0_hz"], 141.7001)

    def test_f_base_ref_hz(self):
        """Result f_base_ref_hz must equal 139.764 Hz."""
        self.assertEqual(self.result["f_base_ref_hz"], 139.764)

    def test_schwinger_factor(self):
        """Schwinger factor must be ≈ 1.001161."""
        self.assertAlmostEqual(self.result["schwinger_factor"], 1.001161, delta=0.000001)

    def test_f_schwinger_hz(self):
        """Schwinger-corrected frequency must be ≈ 139.926 Hz."""
        self.assertAlmostEqual(self.result["f_schwinger_hz"], 139.926, delta=0.002)

    def test_cos_pi_7(self):
        """cos(π/7) must be ≈ 0.9009."""
        self.assertAlmostEqual(self.result["cos_pi_7"], 0.9009, delta=0.001)

    def test_f_heptagon_hz(self):
        """Heptagon-corrected frequency must be ≈ 155.307 Hz."""
        self.assertAlmostEqual(self.result["f_heptagon_hz"], 155.307, delta=0.01)

    def test_phi_pi(self):
        """φ^π must be ≈ 4.5348."""
        self.assertAlmostEqual(self.result["phi_pi"], 4.5348, delta=0.001)

    def test_factor_espectral(self):
        """α·φ^π/N₇ must be ≈ 4.727×10⁻³."""
        self.assertAlmostEqual(self.result["factor_espectral"], 4.727e-3, delta=0.01e-3)

    def test_f_v70_hz_positive(self):
        """v7.0 formula frequency must be positive."""
        self.assertGreater(self.result["f_v70_hz"], 0.0)

    def test_f_debroglie_hz_positive(self):
        """De Broglie frequency must be positive."""
        self.assertGreater(self.result["f_debroglie_hz"], 0.0)

    def test_lambda_c_debroglie_m_positive(self):
        """Effective Compton wavelength must be positive."""
        self.assertGreater(self.result["lambda_c_debroglie_m"], 0.0)

    def test_ratio_masa_p_e(self):
        """m_p/m_e must be ≈ 1836.15."""
        self.assertAlmostEqual(self.result["ratio_masa_p_e"], 1836.15, delta=0.01)

    def test_z0_ohm(self):
        """Z₀ must be ≈ 376.73 Ω."""
        self.assertAlmostEqual(self.result["z0_ohm"], 376.73, delta=0.01)

    def test_r_hall_ohm(self):
        """R_K must be ≈ 25812.8 Ω."""
        self.assertAlmostEqual(self.result["r_hall_ohm"], 25812.8, delta=0.5)

    def test_ratio_hall_n7(self):
        """R_K/(Z₀·N₇) must be ≈ 9.788."""
        self.assertAlmostEqual(self.result["ratio_hall_n7"], 9.788, delta=0.01)

    def test_residuo_relativo_positive(self):
        """Residual must be positive."""
        self.assertGreater(self.result["residuo_relativo"], 0.0)

    def test_mensaje_is_string(self):
        """Message must be a non-empty string."""
        self.assertIsInstance(self.result["mensaje"], str)
        self.assertGreater(len(self.result["mensaje"]), 0)

    def test_custom_f0(self):
        """Custom f₀ must be reflected in result."""
        r = resonancia_total_v7_calcular(f0=200.0)
        self.assertEqual(r["f0_hz"], 200.0)

    def test_custom_f_base_ref(self):
        """Custom f_base_ref must be reflected in result."""
        r = resonancia_total_v7_calcular(f_base_ref_hz=130.0)
        self.assertEqual(r["f_base_ref_hz"], 130.0)
        self.assertAlmostEqual(
            r["f_schwinger_hz"], 130.0 * (1.0 + _ALPHA / (2.0 * math.pi)), places=5
        )


# ============================================================================
# TestNumericalInvariants – 8 additional cross-check tests
# ============================================================================

class TestNumericalInvariants(unittest.TestCase):
    """Cross-checks between module constants and class outputs."""

    def test_schwinger_class_matches_constant(self):
        """CorreccionSchwinger.factor() must match _SCHWINGER_FACTOR."""
        self.assertAlmostEqual(
            CorreccionSchwinger().factor(), _SCHWINGER_FACTOR, places=14
        )

    def test_cos_pi7_class_matches_constant(self):
        """GeometriaHeptagonoHiperbolico.cos_pi_n7() must match _COS_PI_7."""
        self.assertAlmostEqual(
            GeometriaHeptagonoHiperbolico().cos_pi_n7(), _COS_PI_7, places=14
        )

    def test_phi_pi_class_matches_constant(self):
        """IdentidadResonanciaV70.phi_pi() must match _PHI_PI."""
        self.assertAlmostEqual(
            IdentidadResonanciaV70().phi_pi(), _PHI_PI, places=12
        )

    def test_f_v70_class_matches_constant(self):
        """IdentidadResonanciaV70.frecuencia_v7_hz() must match _F_V70_HZ."""
        self.assertAlmostEqual(
            IdentidadResonanciaV70().frecuencia_v7_hz(), _F_V70_HZ, places=10
        )

    def test_debroglie_lambda_class_matches_constant(self):
        """FrecuenciaDeBroglieMediaGeometrica.lambda_c_debroglie_m() must match constant."""
        self.assertAlmostEqual(
            FrecuenciaDeBroglieMediaGeometrica().lambda_c_debroglie_m(),
            _LAMBDA_C_DEBROGLIE_M,
            places=20,
        )

    def test_debroglie_freq_class_matches_constant(self):
        """FrecuenciaDeBroglieMediaGeometrica.frecuencia_debroglie_hz() must match constant."""
        self.assertAlmostEqual(
            FrecuenciaDeBroglieMediaGeometrica().frecuencia_debroglie_hz(),
            _F_DEBROGLIE_HZ,
            places=5,
        )

    def test_hall_ratio_class_matches_constant(self):
        """ImpedanciaHall.ratio_hall_n7() must match _HALL_RATIO_N7."""
        self.assertAlmostEqual(
            ImpedanciaHall().ratio_hall_n7(), _HALL_RATIO_N7, places=10
        )

    def test_schwinger_applied_matches_f_base_schwinger(self):
        """CorreccionSchwinger.aplicar(_F_BASE_REF_HZ) must match _F_BASE_SCHWINGER_HZ."""
        self.assertAlmostEqual(
            CorreccionSchwinger().aplicar(_F_BASE_REF_HZ),
            _F_BASE_SCHWINGER_HZ,
            places=10,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
