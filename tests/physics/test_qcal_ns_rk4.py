"""
Tests for physics.qcal_ns_rk4 — Protocolo LÁSER NOÉTICO v1.0

183 pruebas que cubren las 8 clases y ambas funciones de la API pública.
Invariantes clave verificados:
  - Ψ_spec ≥ 0,888
  - error_espectral < 1e-6
  - superradiante = True
  - plateau_alcanzado = True
  - psi_total ≈ 0,956
"""

import math
import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.qcal_ns_rk4 import (
    # Constants
    LAMBDA_1,
    F_HRV,
    N_MICROTUBULOS,
    N_SQUARED,
    G_NORM_RK4,
    RENDIMIENTO_CUANTICO,
    F0_HZ,
    GAMMA_1_RIEMANN,
    PSI_MINIMA,
    # Classes
    ResultadoLaserNoetico,
    MallaEspectral,
    FiltroVibracional,
    IntegradorRK4,
    EspectroEnergia,
    ForzadoEspectralNoetico,
    TerminoSuperradiante,
    CoherenciaBiologica,
    # Public API
    generate_upe_signature,
    qcal_ns_rk4_activar,
)


# ============================================================================
# TestResultadoLaserNoetico – 10 tests
# ============================================================================

class TestResultadoLaserNoetico(unittest.TestCase):
    """Tests for ResultadoLaserNoetico dataclass."""

    def setUp(self):
        self.r = ResultadoLaserNoetico(
            psi_spec=0.891,
            psi_dyn=0.9999,
            psi_upe=0.9782,
            psi_total=0.956,
            error_espectral=9.82e-7,
            superradiante=True,
            plateau_alcanzado=True,
            rendimiento_cuantico=1000.0,
            aprobado=True,
        )

    def test_psi_spec_value(self):
        """psi_spec must equal 0.891."""
        self.assertAlmostEqual(self.r.psi_spec, 0.891, places=3)

    def test_psi_dyn_near_one(self):
        """psi_dyn must be > 0.99."""
        self.assertGreater(self.r.psi_dyn, 0.99)

    def test_psi_upe_range(self):
        """psi_upe must be in [0, 1]."""
        self.assertGreaterEqual(self.r.psi_upe, 0.0)
        self.assertLessEqual(self.r.psi_upe, 1.0)

    def test_psi_total_value(self):
        """psi_total must equal 0.956."""
        self.assertAlmostEqual(self.r.psi_total, 0.956, places=3)

    def test_error_espectral_small(self):
        """error_espectral must be < 1e-6."""
        self.assertLess(self.r.error_espectral, 1.0e-6)

    def test_superradiante_true(self):
        """superradiante must be True."""
        self.assertTrue(self.r.superradiante)

    def test_plateau_alcanzado_true(self):
        """plateau_alcanzado must be True."""
        self.assertTrue(self.r.plateau_alcanzado)

    def test_rendimiento_cuantico_value(self):
        """rendimiento_cuantico must equal 1000.0."""
        self.assertAlmostEqual(self.r.rendimiento_cuantico, 1000.0, places=1)

    def test_aprobado_true(self):
        """aprobado must be True."""
        self.assertTrue(self.r.aprobado)

    def test_dataclass_fields_accessible(self):
        """All nine fields must be accessible by name."""
        fields = [
            "psi_spec", "psi_dyn", "psi_upe", "psi_total",
            "error_espectral", "superradiante", "plateau_alcanzado",
            "rendimiento_cuantico", "aprobado",
        ]
        for f in fields:
            self.assertTrue(hasattr(self.r, f), f"Missing field: {f}")


# ============================================================================
# TestMallaEspectral – 20 tests
# ============================================================================

class TestMallaEspectral(unittest.TestCase):
    """Tests for MallaEspectral class."""

    def setUp(self):
        self.m = MallaEspectral()

    def test_centro_default(self):
        """Default centro must equal LAMBDA_1."""
        self.assertAlmostEqual(self.m.centro, LAMBDA_1, places=6)

    def test_frecuencias_length(self):
        """frecuencias must have n_puntos elements."""
        self.assertEqual(len(self.m.frecuencias), 1000)

    def test_frecuencias_ndarray(self):
        """frecuencias must be a numpy ndarray."""
        self.assertIsInstance(self.m.frecuencias, np.ndarray)

    def test_frecuencias_min(self):
        """Minimum frequency must equal LAMBDA_1 - delta_hz."""
        self.assertAlmostEqual(self.m.frecuencias[0], LAMBDA_1 - 50.0, places=4)

    def test_frecuencias_max(self):
        """Maximum frequency must equal LAMBDA_1 + delta_hz."""
        self.assertAlmostEqual(self.m.frecuencias[-1], LAMBDA_1 + 50.0, places=4)

    def test_ancho_hz_default(self):
        """Default ancho_hz must equal 100 Hz."""
        self.assertAlmostEqual(self.m.ancho_hz, 100.0, places=6)

    def test_delta_hz_default(self):
        """Default delta_hz must equal 50 Hz."""
        self.assertAlmostEqual(self.m.delta_hz, 50.0, places=6)

    def test_n_puntos_default(self):
        """Default n_puntos must equal 1000."""
        self.assertEqual(self.m.n_puntos, 1000)

    def test_contiene_centro(self):
        """Centro frequency must be contained in the grid."""
        self.assertTrue(self.m.contiene(LAMBDA_1))

    def test_contiene_min(self):
        """Lower bound must be contained."""
        self.assertTrue(self.m.contiene(LAMBDA_1 - 50.0))

    def test_contiene_max(self):
        """Upper bound must be contained."""
        self.assertTrue(self.m.contiene(LAMBDA_1 + 50.0))

    def test_no_contiene_exterior(self):
        """Frequency outside range must not be contained."""
        self.assertFalse(self.m.contiene(LAMBDA_1 - 51.0))
        self.assertFalse(self.m.contiene(LAMBDA_1 + 51.0))

    def test_indice_central_near_middle(self):
        """Central index must be near n_puntos/2."""
        idx = self.m.indice_central()
        self.assertGreater(idx, 400)
        self.assertLess(idx, 600)

    def test_indice_central_points_to_lambda1(self):
        """Frequency at central index must be close to LAMBDA_1."""
        idx = self.m.indice_central()
        self.assertAlmostEqual(self.m.frecuencias[idx], LAMBDA_1, delta=0.2)

    def test_resolucion_hz(self):
        """Resolution must equal ancho/(n_puntos-1)."""
        expected = 100.0 / 999
        self.assertAlmostEqual(self.m.resolucion_hz(), expected, places=8)

    def test_custom_n_puntos(self):
        """Custom n_puntos must be respected."""
        m2 = MallaEspectral(n_puntos=500)
        self.assertEqual(len(m2.frecuencias), 500)

    def test_custom_delta_hz(self):
        """Custom delta_hz must be respected."""
        m2 = MallaEspectral(delta_hz=25.0)
        self.assertAlmostEqual(m2.ancho_hz, 50.0, places=6)

    def test_frecuencias_monotonic(self):
        """Frequencies must be strictly monotonically increasing."""
        diff = np.diff(self.m.frecuencias)
        self.assertTrue(np.all(diff > 0))

    def test_invalid_n_puntos_raises(self):
        """n_puntos < 2 must raise ValueError."""
        with self.assertRaises(ValueError):
            MallaEspectral(n_puntos=1)

    def test_invalid_delta_hz_raises(self):
        """Negative delta_hz must raise ValueError."""
        with self.assertRaises(ValueError):
            MallaEspectral(delta_hz=-10.0)


# ============================================================================
# TestFiltroVibracional – 20 tests
# ============================================================================

class TestFiltroVibracional(unittest.TestCase):
    """Tests for FiltroVibracional class."""

    def setUp(self):
        self.f = FiltroVibracional()
        self.m = MallaEspectral()

    def test_psi_spec_default(self):
        """Default psi_spec must equal 0.891."""
        self.assertAlmostEqual(self.f.psi_spec, 0.891, places=6)

    def test_psi_spec_above_minimum(self):
        """psi_spec must be >= PSI_MINIMA (0.888)."""
        self.assertGreaterEqual(self.f.psi_spec, PSI_MINIMA)

    def test_aprobado_true(self):
        """Default filter must be aprobado."""
        self.assertTrue(self.f.aprobado)

    def test_gamma_s_positive(self):
        """gamma_s must be positive."""
        self.assertGreater(self.f.gamma_s, 0.0)

    def test_gamma_s_formula(self):
        """gamma_s must equal (1 - 0.891) * pi * F_HRV."""
        expected = 0.109 * math.pi * F_HRV
        self.assertAlmostEqual(self.f.gamma_s, expected, places=10)

    def test_kuramoto_formula_exact(self):
        """Kuramoto formula: 1 - 2*gamma_s/(2*pi*F_HRV) = psi_spec."""
        computed = 1.0 - 2.0 * self.f.gamma_s / (2.0 * math.pi * self.f.f_hrv)
        self.assertAlmostEqual(computed, self.f.psi_spec, places=12)

    def test_lorentziano_centro(self):
        """Lorentzian at center must equal 1/(pi*gamma_s)."""
        val = self.f.lorentziano(LAMBDA_1, f0=LAMBDA_1)
        expected = 1.0 / (math.pi * self.f.gamma_s)
        self.assertAlmostEqual(val, expected, places=6)

    def test_lorentziano_positive(self):
        """Lorentzian must be positive everywhere."""
        for f_test in [LAMBDA_1 - 10, LAMBDA_1, LAMBDA_1 + 10]:
            self.assertGreater(self.f.lorentziano(f_test), 0.0)

    def test_lorentziano_symmetric(self):
        """Lorentzian must be symmetric around center."""
        val_left = self.f.lorentziano(LAMBDA_1 - 5.0, f0=LAMBDA_1)
        val_right = self.f.lorentziano(LAMBDA_1 + 5.0, f0=LAMBDA_1)
        self.assertAlmostEqual(val_left, val_right, places=12)

    def test_lorentziano_decays_with_distance(self):
        """Lorentzian must decrease as |f - f0| increases."""
        v_center = self.f.lorentziano(LAMBDA_1, f0=LAMBDA_1)
        v_near = self.f.lorentziano(LAMBDA_1 + 1.0, f0=LAMBDA_1)
        v_far = self.f.lorentziano(LAMBDA_1 + 10.0, f0=LAMBDA_1)
        self.assertGreater(v_center, v_near)
        self.assertGreater(v_near, v_far)

    def test_amplitud_pico(self):
        """Amplitude peak must equal 1/(pi*gamma_s)."""
        expected = 1.0 / (math.pi * self.f.gamma_s)
        self.assertAlmostEqual(self.f.amplitud_pico(), expected, places=6)

    def test_aplicar_returns_ndarray(self):
        """aplicar must return a numpy ndarray."""
        result = self.f.aplicar(self.m)
        self.assertIsInstance(result, np.ndarray)

    def test_aplicar_same_length_as_malla(self):
        """aplicar must return array with same length as malla."""
        result = self.f.aplicar(self.m)
        self.assertEqual(len(result), self.m.n_puntos)

    def test_aplicar_all_positive(self):
        """All filter values must be positive."""
        result = self.f.aplicar(self.m)
        self.assertTrue(np.all(result > 0))

    def test_aplicar_max_at_center(self):
        """Maximum filter value must occur at or near the center index."""
        result = self.f.aplicar(self.m)
        max_idx = int(np.argmax(result))
        center_idx = self.m.indice_central()
        self.assertAlmostEqual(max_idx, center_idx, delta=5)

    def test_custom_gamma_s(self):
        """Custom gamma_s must set psi_spec accordingly."""
        gamma_s_custom = 0.005
        f2 = FiltroVibracional(gamma_s=gamma_s_custom)
        expected_psi = 1.0 - 2.0 * gamma_s_custom / (2.0 * math.pi * F_HRV)
        self.assertAlmostEqual(f2.psi_spec, expected_psi, places=10)

    def test_f_hrv_stored(self):
        """f_hrv must be stored correctly."""
        self.assertAlmostEqual(self.f.f_hrv, F_HRV, places=10)

    def test_negative_gamma_s_raises(self):
        """Negative gamma_s must raise ValueError."""
        with self.assertRaises(ValueError):
            FiltroVibracional(gamma_s=-0.01)

    def test_zero_f_hrv_raises(self):
        """Zero f_hrv must raise ValueError."""
        with self.assertRaises(ValueError):
            FiltroVibracional(f_hrv=0.0)

    def test_repr_contains_psi_spec(self):
        """repr must mention psi_spec."""
        r = repr(self.f)
        self.assertIn("psi_spec", r)


# ============================================================================
# TestIntegradorRK4 – 20 tests
# ============================================================================

class TestIntegradorRK4(unittest.TestCase):
    """Tests for IntegradorRK4 class."""

    def setUp(self):
        self.rk4 = IntegradorRK4()
        self.t, self.psi = self.rk4.integrar()

    def test_t_array_length(self):
        """t array must have n_pasos+1 elements."""
        n_pasos = int(round(self.rk4.t_final / self.rk4.dt))
        self.assertEqual(len(self.t), n_pasos + 1)

    def test_psi_array_length(self):
        """psi array must have same length as t array."""
        self.assertEqual(len(self.psi), len(self.t))

    def test_t_starts_at_zero(self):
        """t must start at 0."""
        self.assertAlmostEqual(self.t[0], 0.0, places=10)

    def test_t_ends_at_t_final(self):
        """t must end at t_final."""
        self.assertAlmostEqual(self.t[-1], self.rk4.t_final, delta=0.01)

    def test_psi_initial_condition(self):
        """First psi must equal psi_0."""
        self.assertAlmostEqual(self.psi[0], self.rk4.psi_0, places=10)

    def test_psi_monotonically_increasing(self):
        """psi must be monotonically non-decreasing (logistic growth)."""
        diff = np.diff(self.psi)
        self.assertTrue(np.all(diff >= -1e-10))

    def test_psi_bounded_above(self):
        """psi must never exceed 1.0 (equilibrium)."""
        self.assertTrue(np.all(self.psi <= 1.0 + 1e-9))

    def test_psi_bounded_below(self):
        """psi must always be >= 0."""
        self.assertTrue(np.all(self.psi >= 0.0))

    def test_psi_final_near_one(self):
        """Final psi must be very close to 1.0."""
        self.assertGreater(self.rk4.psi_final, 0.999)

    def test_plateau_alcanzado_true(self):
        """plateau_alcanzado must be True with default parameters."""
        self.assertTrue(self.rk4.plateau_alcanzado)

    def test_psi_plateau_above_threshold(self):
        """psi_plateau must be > 0.999."""
        self.assertGreater(self.rk4.psi_plateau, 0.999)

    def test_g_norm_default(self):
        """Default g_norm must equal G_NORM_RK4."""
        self.assertAlmostEqual(self.rk4.g_norm, G_NORM_RK4, places=10)

    def test_alpha_default(self):
        """Default alpha must equal 0.1."""
        self.assertAlmostEqual(self.rk4.alpha, 0.1, places=10)

    def test_derivada_at_psi_one(self):
        """Derivative at psi=1 must equal 0 (equilibrium)."""
        deriv = self.rk4._derivada(0.0, 1.0)
        self.assertAlmostEqual(deriv, 0.0, places=12)

    def test_derivada_at_psi_zero(self):
        """Derivative at psi=0 must equal alpha (positive drive)."""
        deriv = self.rk4._derivada(0.0, 0.0)
        self.assertAlmostEqual(deriv, self.rk4.alpha, places=12)

    def test_rk4_paso_preserves_bounds(self):
        """A single RK4 step from psi=0.5 must stay in [0.45, 1.0]."""
        psi_next = self.rk4._rk4_paso(0.0, 0.5, self.rk4.dt)
        self.assertGreaterEqual(psi_next, 0.45)
        self.assertLessEqual(psi_next, 1.0)

    def test_invalid_alpha_raises(self):
        """Non-positive alpha must raise ValueError."""
        with self.assertRaises(ValueError):
            IntegradorRK4(alpha=0.0)

    def test_invalid_psi_0_raises(self):
        """psi_0 outside [0,1] must raise ValueError."""
        with self.assertRaises(ValueError):
            IntegradorRK4(psi_0=1.5)

    def test_invalid_dt_raises(self):
        """Non-positive dt must raise ValueError."""
        with self.assertRaises(ValueError):
            IntegradorRK4(dt=0.0)

    def test_repr_contains_g_norm(self):
        """repr must mention g_norm."""
        self.assertIn("g_norm", repr(self.rk4))


# ============================================================================
# TestEspectroEnergia – 15 tests
# ============================================================================

class TestEspectroEnergia(unittest.TestCase):
    """Tests for EspectroEnergia class."""

    def setUp(self):
        self.e = EspectroEnergia()

    def test_error_espectral_magnitude(self):
        """error_espectral must be approximately 9.82e-7."""
        self.assertAlmostEqual(self.e.error_espectral, 9.82e-7, delta=1e-9)

    def test_error_espectral_below_tolerance(self):
        """error_espectral must be < 1e-6."""
        self.assertLess(self.e.error_espectral, 1.0e-6)

    def test_verificado_true(self):
        """verificado must be True for default parameters."""
        self.assertTrue(self.e.verificado)

    def test_etiqueta_qed_riemann(self):
        """etiqueta must be 'QED-RIEMANN-VERIFICADO'."""
        self.assertEqual(self.e.etiqueta, "QED-RIEMANN-VERIFICADO")

    def test_gamma_1_f0_near_lambda_1(self):
        """gamma_1 * f0 must be very close to LAMBDA_1."""
        self.assertAlmostEqual(self.e.gamma_1_f0, LAMBDA_1, delta=0.005)

    def test_gamma_1_f0_formula(self):
        """gamma_1_f0 must equal GAMMA_1_RIEMANN * F0_HZ."""
        expected = GAMMA_1_RIEMANN * F0_HZ
        self.assertAlmostEqual(self.e.gamma_1_f0, expected, places=6)

    def test_lambda_1_stored(self):
        """lambda_1 must be stored correctly."""
        self.assertAlmostEqual(self.e.lambda_1, LAMBDA_1, places=6)

    def test_gamma_1_stored(self):
        """gamma_1 must be stored correctly."""
        self.assertAlmostEqual(self.e.gamma_1, GAMMA_1_RIEMANN, places=12)

    def test_f0_stored(self):
        """f0 must be stored correctly."""
        self.assertAlmostEqual(self.e.f0, F0_HZ, places=6)

    def test_error_formula_manual(self):
        """Manual computation of error must match property."""
        ref = GAMMA_1_RIEMANN * F0_HZ
        expected_err = abs(LAMBDA_1 - ref) / ref
        self.assertAlmostEqual(self.e.error_espectral, expected_err, places=15)

    def test_custom_lambda_above_tolerance(self):
        """Deliberately wrong lambda_1 must fail verificado."""
        e2 = EspectroEnergia(lambda_1=2003.0)
        self.assertFalse(e2.verificado)
        self.assertEqual(e2.etiqueta, "FALLA-ESPECTRAL")

    def test_error_nonnegative(self):
        """error_espectral must be non-negative."""
        self.assertGreaterEqual(self.e.error_espectral, 0.0)

    def test_invalid_lambda_raises(self):
        """Non-positive lambda_1 must raise ValueError."""
        with self.assertRaises(ValueError):
            EspectroEnergia(lambda_1=0.0)

    def test_invalid_gamma_raises(self):
        """Non-positive gamma_1 must raise ValueError."""
        with self.assertRaises(ValueError):
            EspectroEnergia(gamma_1=-1.0)

    def test_invalid_f0_raises(self):
        """Non-positive f0 must raise ValueError."""
        with self.assertRaises(ValueError):
            EspectroEnergia(f0=0.0)


# ============================================================================
# TestForzadoEspectralNoetico – 15 tests
# ============================================================================

class TestForzadoEspectralNoetico(unittest.TestCase):
    """Tests for ForzadoEspectralNoetico class."""

    def setUp(self):
        self.fn = ForzadoEspectralNoetico()

    def test_frecuencia_portadora_default(self):
        """Default carrier frequency must equal LAMBDA_1."""
        self.assertAlmostEqual(self.fn.frecuencia_portadora, LAMBDA_1, places=6)

    def test_frecuencia_modulacion_default(self):
        """Default modulation frequency must equal F_HRV."""
        self.assertAlmostEqual(self.fn.frecuencia_modulacion, F_HRV, places=10)

    def test_amplitud_base_default(self):
        """Default amplitud_base must equal 1.0."""
        self.assertAlmostEqual(self.fn.amplitud_base, 1.0, places=10)

    def test_amplitud_pico_double(self):
        """amplitud_pico must equal 2 * amplitud_base."""
        self.assertAlmostEqual(self.fn.amplitud_pico, 2.0 * self.fn.amplitud_base, places=10)

    def test_evaluar_scalar(self):
        """evaluar at t=0 must return a numeric value."""
        val = self.fn.evaluar(0.0)
        # At t=0: cos(0)=1 and (1+cos(0))=2, so F(0) = 1.0 * 2 * 1 = 2.0
        self.assertAlmostEqual(float(val), 2.0, places=6)

    def test_evaluar_array(self):
        """evaluar with ndarray input must return an ndarray of same shape."""
        t = np.linspace(0, 10, 100)
        result = self.fn.evaluar(t)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, t.shape)

    def test_evaluar_bounded(self):
        """Forcing amplitude must be bounded by [-2*amplitud, +2*amplitud]."""
        t = np.linspace(0, 100, 10000)
        result = self.fn.evaluar(t)
        self.assertLessEqual(np.max(np.abs(result)), 2.0 + 1e-9)

    def test_evaluar_zero_mean(self):
        """Mean of forcing over many HRV cycles must be ~0 (carrier averages to 0)."""
        # Integrate over several full HRV cycles (integer number)
        t = np.linspace(0, 100.0, 1_000_000)
        result = self.fn.evaluar(t)
        mean_val = float(np.mean(result))
        self.assertAlmostEqual(mean_val, 0.0, delta=0.01)

    def test_evaluar_max_at_t0(self):
        """At t=0, both carrier and modulation are maximum, giving max amplitude."""
        val = float(self.fn.evaluar(0.0))
        self.assertAlmostEqual(val, 2.0 * self.fn.amplitud_base, places=6)

    def test_custom_amplitud(self):
        """Custom amplitud must scale the output."""
        fn2 = ForzadoEspectralNoetico(amplitud=0.5)
        val0 = float(fn2.evaluar(0.0))
        self.assertAlmostEqual(val0, 1.0, places=6)

    def test_invalid_lambda_raises(self):
        """Non-positive lambda_1 must raise ValueError."""
        with self.assertRaises(ValueError):
            ForzadoEspectralNoetico(lambda_1=0.0)

    def test_invalid_f_hrv_raises(self):
        """Non-positive f_hrv must raise ValueError."""
        with self.assertRaises(ValueError):
            ForzadoEspectralNoetico(f_hrv=-0.1)

    def test_invalid_amplitud_raises(self):
        """Non-positive amplitud must raise ValueError."""
        with self.assertRaises(ValueError):
            ForzadoEspectralNoetico(amplitud=0.0)

    def test_repr_contains_lambda(self):
        """repr must mention lambda_1."""
        self.assertIn("lambda_1", repr(self.fn))

    def test_evaluar_float64_dtype(self):
        """Output array must have float64 dtype."""
        t = np.linspace(0, 1, 100)
        result = self.fn.evaluar(t)
        self.assertEqual(result.dtype, np.float64)


# ============================================================================
# TestTerminoSuperradiante – 20 tests
# ============================================================================

class TestTerminoSuperradiante(unittest.TestCase):
    """Tests for TerminoSuperradiante class."""

    def setUp(self):
        self.ts = TerminoSuperradiante()

    def test_n_default(self):
        """Default n must equal N_MICROTUBULOS."""
        self.assertEqual(self.ts.n, N_MICROTUBULOS)

    def test_n_squared_value(self):
        """n_squared must equal N_MICROTUBULOS^2 = 10^26."""
        expected = float(N_MICROTUBULOS) ** 2
        self.assertAlmostEqual(self.ts.n_squared, expected, delta=1.0)

    def test_n_squared_equals_n_squared_constant(self):
        """n_squared must equal the module constant N_SQUARED."""
        self.assertAlmostEqual(self.ts.n_squared, N_SQUARED, delta=1.0)

    def test_ganancia_equals_n_squared(self):
        """ganancia must equal n_squared."""
        self.assertAlmostEqual(self.ts.ganancia, self.ts.n_squared, delta=1.0)

    def test_rendimiento_cuantico_default(self):
        """Default rendimiento_cuantico must equal RENDIMIENTO_CUANTICO (1000.0)."""
        self.assertAlmostEqual(self.ts.rendimiento_cuantico, RENDIMIENTO_CUANTICO, places=3)

    def test_superradiante_true_for_large_n(self):
        """superradiante must be True for N = 10^13."""
        self.assertTrue(self.ts.superradiante)

    def test_superradiante_false_for_small_n(self):
        """superradiante must be False for N below threshold."""
        ts_small = TerminoSuperradiante(n=100)
        self.assertFalse(ts_small.superradiante)

    def test_escalar_multiplies_by_n_squared(self):
        """escalar must multiply input by n_squared."""
        amplitud = 1.0
        result = self.ts.escalar(amplitud)
        self.assertAlmostEqual(result, self.ts.n_squared, delta=1.0)

    def test_escalar_zero(self):
        """escalar(0) must return 0."""
        self.assertAlmostEqual(self.ts.escalar(0.0), 0.0, places=10)

    def test_escalar_negative(self):
        """escalar(-1.0) must return -n_squared."""
        self.assertAlmostEqual(self.ts.escalar(-1.0), -self.ts.n_squared, delta=1.0)

    def test_n_squared_magnitude(self):
        """n_squared must be in the range [1e25, 1e27]."""
        self.assertGreater(self.ts.n_squared, 1e25)
        self.assertLess(self.ts.n_squared, 1e27)

    def test_rendimiento_cuantico_superradiante_above_1(self):
        """rendimiento_cuantico in superradiant regime must be >> 1."""
        self.assertGreater(self.ts.rendimiento_cuantico, 1.0)

    def test_custom_n(self):
        """Custom n must be stored correctly."""
        ts2 = TerminoSuperradiante(n=int(1e10))
        self.assertEqual(ts2.n, int(1e10))

    def test_custom_rendimiento(self):
        """Custom rendimiento must be stored correctly."""
        ts2 = TerminoSuperradiante(rendimiento=500.0)
        self.assertAlmostEqual(ts2.rendimiento_cuantico, 500.0, places=3)

    def test_invalid_n_raises(self):
        """Non-positive n must raise ValueError."""
        with self.assertRaises(ValueError):
            TerminoSuperradiante(n=0)

    def test_invalid_rendimiento_raises(self):
        """Non-positive rendimiento must raise ValueError."""
        with self.assertRaises(ValueError):
            TerminoSuperradiante(rendimiento=0.0)

    def test_n_squared_is_float(self):
        """n_squared must be a Python float."""
        self.assertIsInstance(self.ts.n_squared, float)

    def test_ganancia_is_float(self):
        """ganancia must be a Python float."""
        self.assertIsInstance(self.ts.ganancia, float)

    def test_superradiante_threshold_boundary(self):
        """N exactly at threshold must be superradiante."""
        ts_boundary = TerminoSuperradiante(n=int(1e6))
        self.assertTrue(ts_boundary.superradiante)

    def test_repr_contains_n_squared(self):
        """repr must mention n_squared."""
        self.assertIn("n_squared", repr(self.ts))


# ============================================================================
# TestCoherenciaBiologica – 15 tests
# ============================================================================

class TestCoherenciaBiologica(unittest.TestCase):
    """Tests for CoherenciaBiologica class."""

    def setUp(self):
        self.cb = CoherenciaBiologica(psi_spec=0.891, psi_dyn=1.0)

    def test_psi_spec_stored(self):
        """psi_spec must be stored correctly."""
        self.assertAlmostEqual(self.cb.psi_spec, 0.891, places=6)

    def test_psi_dyn_stored(self):
        """psi_dyn must be stored correctly."""
        self.assertAlmostEqual(self.cb.psi_dyn, 1.0, places=6)

    def test_psi_upe_auto_computed(self):
        """psi_upe must be auto-computed as 1 - (1-psi_spec)*2*F_HRV."""
        expected = 1.0 - (1.0 - 0.891) * 2.0 * F_HRV
        self.assertAlmostEqual(self.cb.psi_upe, expected, places=10)

    def test_psi_upe_default_value(self):
        """Auto-computed psi_upe must equal 0.9782."""
        self.assertAlmostEqual(self.cb.psi_upe, 0.9782, places=4)

    def test_psi_total_formula(self):
        """psi_total must equal (psi_spec + psi_dyn + psi_upe) / 3."""
        expected = (self.cb.psi_spec + self.cb.psi_dyn + self.cb.psi_upe) / 3.0
        self.assertAlmostEqual(self.cb.psi_total, expected, places=10)

    def test_psi_total_near_target(self):
        """psi_total must round to 0.956."""
        self.assertAlmostEqual(round(self.cb.psi_total, 3), 0.956, places=3)

    def test_psi_total_above_minimum(self):
        """psi_total must be >= PSI_MINIMA."""
        self.assertGreaterEqual(self.cb.psi_total, PSI_MINIMA)

    def test_aprobado_true(self):
        """Default CoherenciaBiologica must be aprobado."""
        self.assertTrue(self.cb.aprobado)

    def test_aprobado_false_for_low_coherence(self):
        """Low psi values must result in aprobado=False."""
        cb_low = CoherenciaBiologica(psi_spec=0.7, psi_dyn=0.7, psi_upe=0.7)
        self.assertFalse(cb_low.aprobado)

    def test_componentes_dict_keys(self):
        """componentes dict must have psi_spec, psi_dyn, psi_upe keys."""
        comp = self.cb.componentes
        self.assertIn("psi_spec", comp)
        self.assertIn("psi_dyn", comp)
        self.assertIn("psi_upe", comp)

    def test_componentes_values_match(self):
        """componentes values must match stored attributes."""
        comp = self.cb.componentes
        self.assertAlmostEqual(comp["psi_spec"], self.cb.psi_spec, places=10)
        self.assertAlmostEqual(comp["psi_dyn"], self.cb.psi_dyn, places=10)
        self.assertAlmostEqual(comp["psi_upe"], self.cb.psi_upe, places=10)

    def test_custom_psi_upe(self):
        """Custom psi_upe must be stored correctly."""
        cb2 = CoherenciaBiologica(psi_spec=0.891, psi_dyn=1.0, psi_upe=0.9)
        self.assertAlmostEqual(cb2.psi_upe, 0.9, places=10)

    def test_invalid_psi_spec_raises(self):
        """psi_spec outside [0,1] must raise ValueError."""
        with self.assertRaises(ValueError):
            CoherenciaBiologica(psi_spec=1.5, psi_dyn=1.0)

    def test_invalid_psi_dyn_raises(self):
        """psi_dyn outside [0,1] must raise ValueError."""
        with self.assertRaises(ValueError):
            CoherenciaBiologica(psi_spec=0.9, psi_dyn=-0.1)

    def test_invalid_psi_upe_raises(self):
        """psi_upe outside [0,1] must raise ValueError."""
        with self.assertRaises(ValueError):
            CoherenciaBiologica(psi_spec=0.9, psi_dyn=1.0, psi_upe=1.5)


# ============================================================================
# TestGenerateUpeSignature – 18 tests
# ============================================================================

class TestGenerateUpeSignature(unittest.TestCase):
    """Tests for generate_upe_signature function."""

    def setUp(self):
        self.t = np.linspace(0, 1, 10000)
        self.sig = generate_upe_signature(self.t, [LAMBDA_1])

    def test_output_shape(self):
        """Output must have shape (10000,)."""
        self.assertEqual(self.sig.shape, (10000,))

    def test_output_dtype(self):
        """Output must have float64 dtype."""
        self.assertEqual(self.sig.dtype, np.float64)

    def test_amplitude_proportional_to_n_squared(self):
        """Maximum amplitude must be approximately N² * 2 = 2e26."""
        self.assertAlmostEqual(np.max(self.sig), 2.0 * N_SQUARED, delta=0.01 * N_SQUARED)

    def test_amplitude_min_near_negative_n_squared(self):
        """Minimum amplitude must be approximately -2*N_SQUARED."""
        self.assertAlmostEqual(np.min(self.sig), -2.0 * N_SQUARED, delta=0.01 * N_SQUARED)

    def test_zero_mean_over_full_period(self):
        """Mean signal over many carrier cycles must be ~0."""
        t_long = np.linspace(0, 100.0, 1_000_000)
        sig_long = generate_upe_signature(t_long, [LAMBDA_1])
        mean_val = float(np.mean(sig_long))
        self.assertAlmostEqual(mean_val / N_SQUARED, 0.0, delta=0.01)

    def test_multiple_lambdas_additive(self):
        """Output for [L1, L2] must equal sum of outputs for [L1] and [L2]."""
        LAMBDA_2 = LAMBDA_1 + 10.0
        sig_both = generate_upe_signature(self.t, [LAMBDA_1, LAMBDA_2])
        sig_l1 = generate_upe_signature(self.t, [LAMBDA_1])
        sig_l2 = generate_upe_signature(self.t, [LAMBDA_2])
        np.testing.assert_array_almost_equal(sig_both, sig_l1 + sig_l2)

    def test_empty_lambdas_returns_zeros(self):
        """Empty lambdas list must return zero array."""
        sig_empty = generate_upe_signature(self.t, [])
        np.testing.assert_array_equal(sig_empty, np.zeros_like(self.t))

    def test_custom_hrv_freq(self):
        """Custom hrv_freq must be used in AM modulation."""
        hrv2 = 0.2
        sig2 = generate_upe_signature(self.t, [LAMBDA_1], hrv_freq=hrv2)
        self.assertEqual(sig2.shape, self.t.shape)

    def test_output_is_1d(self):
        """Output must be 1-dimensional."""
        self.assertEqual(self.sig.ndim, 1)

    def test_at_t_zero_maximum_amplitude(self):
        """At t=0, (1+cos(0))*cos(0)=2, so sig[0] = 2*N_SQUARED."""
        t_single = np.array([0.0])
        sig_single = generate_upe_signature(t_single, [LAMBDA_1])
        self.assertAlmostEqual(float(sig_single[0]), 2.0 * N_SQUARED, delta=1.0)

    def test_input_unchanged(self):
        """Input array t must not be modified."""
        t_copy = self.t.copy()
        _ = generate_upe_signature(self.t, [LAMBDA_1])
        np.testing.assert_array_equal(self.t, t_copy)

    def test_output_is_new_array(self):
        """Output must be a new array, not a view of t."""
        sig = generate_upe_signature(self.t, [LAMBDA_1])
        self.assertIsNot(sig, self.t)

    def test_single_sample(self):
        """Single-sample input must return shape (1,)."""
        sig = generate_upe_signature(np.array([0.0]), [LAMBDA_1])
        self.assertEqual(sig.shape, (1,))

    def test_large_t_array(self):
        """Output shape must match input for large arrays."""
        t_large = np.linspace(0, 100, 100_000)
        sig_large = generate_upe_signature(t_large, [LAMBDA_1])
        self.assertEqual(sig_large.shape, t_large.shape)

    def test_default_hrv_freq(self):
        """Default hrv_freq must equal F_HRV = 0.1 Hz."""
        sig_default = generate_upe_signature(self.t, [LAMBDA_1])
        sig_explicit = generate_upe_signature(self.t, [LAMBDA_1], hrv_freq=F_HRV)
        np.testing.assert_array_equal(sig_default, sig_explicit)

    def test_amplitude_scales_with_n_squared(self):
        """Amplitude magnitude must scale with N²."""
        self.assertGreater(np.max(np.abs(self.sig)), 0.5 * N_SQUARED)

    def test_hrv_modulation_period_visible(self):
        """Envelope HRV peaks when cos(2*pi*F_HRV*t)=1 (at t=0 and t=1/F_HRV)."""
        # At t=0: HRV modulation = 1+cos(0)=2 and carrier cos(0)=1 → max amplitude
        t_zero = np.array([0.0])
        sig_zero = generate_upe_signature(t_zero, [LAMBDA_1])
        self.assertAlmostEqual(float(sig_zero[0]), 2.0 * N_SQUARED, delta=1.0)
        # At t=1/F_HRV the HRV modulation factor is again 2 (peak),
        # but the carrier phase is arbitrary → maximum over a short carrier window
        t_peak = np.linspace(1.0 / F_HRV, 1.0 / F_HRV + 0.001, 1000)
        sig_peak = generate_upe_signature(t_peak, [LAMBDA_1])
        # The envelope peak must reach 2*N_SQUARED within this short window
        self.assertAlmostEqual(np.max(sig_peak), 2.0 * N_SQUARED, delta=0.01 * N_SQUARED)

    def test_half_hrv_period_zero_amplitude(self):
        """At t=1/(2*F_HRV)=5s, cos(2*pi*F_HRV*t)=-1, modulation=0, sig=0."""
        # At t = 1/(2*F_HRV) = 1/(2*0.1) = 5s, cos(2*pi*F_HRV*t) = cos(pi) = -1 → (1-1)*cos(2*pi*λ*t) = 0
        t_half = np.array([0.5 / F_HRV])
        sig_half = generate_upe_signature(t_half, [LAMBDA_1])
        self.assertAlmostEqual(float(sig_half[0]), 0.0, delta=1.0)


# ============================================================================
# TestQcalNsRk4Activar – 20 tests
# ============================================================================

class TestQcalNsRk4Activar(unittest.TestCase):
    """Tests for qcal_ns_rk4_activar public API function."""

    @classmethod
    def setUpClass(cls):
        """Run activation once for all tests in this class."""
        cls.resultado = qcal_ns_rk4_activar()

    def test_returns_resultado_type(self):
        """Return type must be ResultadoLaserNoetico."""
        self.assertIsInstance(self.resultado, ResultadoLaserNoetico)

    def test_psi_spec_value(self):
        """psi_spec must equal 0.891."""
        self.assertAlmostEqual(self.resultado.psi_spec, 0.891, places=6)

    def test_psi_spec_above_minimum(self):
        """psi_spec must be >= PSI_MINIMA = 0.888."""
        self.assertGreaterEqual(self.resultado.psi_spec, PSI_MINIMA)

    def test_psi_dyn_near_one(self):
        """psi_dyn must be > 0.999 (plateau reached)."""
        self.assertGreater(self.resultado.psi_dyn, 0.999)

    def test_psi_upe_formula(self):
        """psi_upe must equal 1 - (1-psi_spec)*2*F_HRV."""
        expected = 1.0 - (1.0 - self.resultado.psi_spec) * 2.0 * F_HRV
        self.assertAlmostEqual(self.resultado.psi_upe, expected, places=6)

    def test_psi_total_value(self):
        """psi_total must round to 0.956."""
        self.assertAlmostEqual(self.resultado.psi_total, 0.956, places=3)

    def test_psi_total_above_minimum(self):
        """psi_total must be >= PSI_MINIMA."""
        self.assertGreaterEqual(self.resultado.psi_total, PSI_MINIMA)

    def test_error_espectral_magnitude(self):
        """error_espectral must be approximately 9.82e-7."""
        self.assertAlmostEqual(self.resultado.error_espectral, 9.82e-7, delta=5e-9)

    def test_error_espectral_below_1e6(self):
        """error_espectral must be < 1e-6 (QED-RIEMANN verified)."""
        self.assertLess(self.resultado.error_espectral, 1.0e-6)

    def test_superradiante_true(self):
        """superradiante must be True."""
        self.assertTrue(self.resultado.superradiante)

    def test_plateau_alcanzado_true(self):
        """plateau_alcanzado must be True."""
        self.assertTrue(self.resultado.plateau_alcanzado)

    def test_rendimiento_cuantico_value(self):
        """rendimiento_cuantico must equal 1000.0."""
        self.assertAlmostEqual(self.resultado.rendimiento_cuantico, 1000.0, places=1)

    def test_aprobado_true(self):
        """aprobado must be True."""
        self.assertTrue(self.resultado.aprobado)

    def test_idempotent_multiple_calls(self):
        """Multiple calls must return consistent psi_spec."""
        r2 = qcal_ns_rk4_activar()
        self.assertAlmostEqual(r2.psi_spec, self.resultado.psi_spec, places=10)

    def test_psi_total_components_consistent(self):
        """psi_total must be consistent with (spec+dyn+upe)/3."""
        expected = (
            self.resultado.psi_spec
            + self.resultado.psi_dyn
            + self.resultado.psi_upe
        ) / 3.0
        # psi_total is rounded to 3 decimal places
        self.assertAlmostEqual(self.resultado.psi_total, round(expected, 3), places=3)

    def test_psi_spec_invariant(self):
        """Key invariant: Ψ_spec = 0.891 ≥ 0.888."""
        self.assertGreaterEqual(self.resultado.psi_spec, 0.888)
        self.assertAlmostEqual(self.resultado.psi_spec, 0.891, places=3)

    def test_error_espectral_invariant(self):
        """Key invariant: error_espectral < 1e-6."""
        self.assertLess(self.resultado.error_espectral, 1e-6)

    def test_superradiante_invariant(self):
        """Key invariant: superradiante = True."""
        self.assertTrue(self.resultado.superradiante)

    def test_plateau_alcanzado_invariant(self):
        """Key invariant: plateau_alcanzado = True."""
        self.assertTrue(self.resultado.plateau_alcanzado)

    def test_rendimiento_cuantico_invariant(self):
        """Key invariant: rendimiento_cuantico = 1000.0."""
        self.assertEqual(self.resultado.rendimiento_cuantico, RENDIMIENTO_CUANTICO)


# ============================================================================
# TestConstants – 10 tests
# ============================================================================

class TestConstants(unittest.TestCase):
    """Tests for module-level constants."""

    def test_lambda_1_value(self):
        """LAMBDA_1 must equal 2002.89 Hz."""
        self.assertAlmostEqual(LAMBDA_1, 2002.89, places=2)

    def test_f_hrv_value(self):
        """F_HRV must equal 0.1 Hz (6 bpm)."""
        self.assertAlmostEqual(F_HRV, 0.1, places=4)

    def test_n_microtubulos_value(self):
        """N_MICROTUBULOS must equal 10^13."""
        self.assertEqual(N_MICROTUBULOS, int(1e13))

    def test_n_squared_value(self):
        """N_SQUARED must equal 10^26."""
        self.assertAlmostEqual(N_SQUARED, 1.0e26, delta=1.0)

    def test_g_norm_rk4_value(self):
        """G_NORM_RK4 must equal 10.0."""
        self.assertAlmostEqual(G_NORM_RK4, 10.0, places=10)

    def test_rendimiento_cuantico_value(self):
        """RENDIMIENTO_CUANTICO must equal 1000.0."""
        self.assertAlmostEqual(RENDIMIENTO_CUANTICO, 1000.0, places=3)

    def test_f0_hz_value(self):
        """F0_HZ must equal 141.7001 Hz."""
        self.assertAlmostEqual(F0_HZ, 141.7001, places=4)

    def test_gamma_1_riemann_value(self):
        """GAMMA_1_RIEMANN must be approximately 14.13473 (first Riemann zero)."""
        self.assertAlmostEqual(GAMMA_1_RIEMANN, 14.134725141734693, places=9)

    def test_psi_minima_value(self):
        """PSI_MINIMA must equal 0.888."""
        self.assertAlmostEqual(PSI_MINIMA, 0.888, places=3)

    def test_n_squared_equals_n_microtubulos_squared(self):
        """N_SQUARED must equal float(N_MICROTUBULOS)**2."""
        self.assertAlmostEqual(N_SQUARED, float(N_MICROTUBULOS) ** 2, delta=1.0)


if __name__ == "__main__":
    unittest.main()
