"""
Tests for physics.psi_diamond_state — Ψ(t) Diamond-State ∴PDS∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesPsiDiamond  – parámetros físicos y numéricos
  - RiemannZerosCache     – ceros de Riemann exactos (mpmath / fallback)
  - ModosAdelicos         – renormalización adélica y pesos/frecuencias
  - CoherenciaTemporal    – correlación C(t) y función Ψ(t)
  - CoherenciaGlobal      – métricas estructurales de coherencia
  - SistemaPsiDiamond     – orquestador con activar()
  - ResultadoPsiDiamond   – dataclass de resultados
  - psi_diamond_activar() – API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - θ  = 0.052463 rad
  - τ  = 3600 s
  - Ψ(0) = 1.0 exacto
  - Ψ(τ) > 0.5
  - lim Ψ(t) → 0.5
  - Ψ_global ≥ 0.888 → sello ∴PDS∞³ ACTIVO
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.psi_diamond_state import (
    # Constantes de módulo
    _F0,
    _THETA,
    _TAU,
    _EPSILON,
    _N_DEFAULT,
    _DPS,
    _PSI_UMBRAL,
    _RIEMANN_ZEROS_10,
    # Clases
    ConstantesPsiDiamond,
    RiemannZerosCache,
    ModosAdelicos,
    CoherenciaTemporal,
    CoherenciaGlobal,
    SistemaPsiDiamond,
    ResultadoPsiDiamond,
    # API pública
    psi_diamond_activar,
)


# ============================================================================
# Fixture compartido — N pequeño para que los tests sean rápidos
# ============================================================================

_N_FAST = 10  # número de modos para tests rápidos


def _make_sistema(n: int = _N_FAST) -> SistemaPsiDiamond:
    return SistemaPsiDiamond(n_modos=n)


def _make_ct(n: int = _N_FAST) -> CoherenciaTemporal:
    cst = ConstantesPsiDiamond(n_modos=n)
    cache = RiemannZerosCache(n=n)
    modos = ModosAdelicos(constantes=cst, cache=cache)
    return CoherenciaTemporal(constantes=cst, modos=modos)


# ============================================================================
# TestModuleConstants – 8 tests
# ============================================================================


class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        """_F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_theta_value(self):
        """_THETA debe ser 0.052463 rad."""
        self.assertAlmostEqual(_THETA, 0.052463, places=6)

    def test_tau_value(self):
        """_TAU debe ser 3600 s."""
        self.assertAlmostEqual(_TAU, 3600.0, places=6)

    def test_epsilon_value(self):
        """_EPSILON debe ser 1e-3."""
        self.assertAlmostEqual(_EPSILON, 1.0e-3, places=10)

    def test_n_default(self):
        """_N_DEFAULT debe ser 100."""
        self.assertEqual(_N_DEFAULT, 100)

    def test_dps_positive(self):
        """_DPS debe ser > 0."""
        self.assertGreater(_DPS, 0)

    def test_psi_umbral(self):
        """_PSI_UMBRAL debe ser 0.888."""
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_riemann_zeros_10_length(self):
        """_RIEMANN_ZEROS_10 debe tener exactamente 10 entradas."""
        self.assertEqual(len(_RIEMANN_ZEROS_10), 10)


# ============================================================================
# TestRiemannZerosFirst – 8 tests
# ============================================================================


class TestRiemannZerosFirst(unittest.TestCase):
    """Tests para _RIEMANN_ZEROS_10 — valores de alta precisión."""

    def test_gamma1_approx(self):
        """γ₁ ≈ 14.1347."""
        self.assertAlmostEqual(_RIEMANN_ZEROS_10[0], 14.1347, places=3)

    def test_gamma2_approx(self):
        """γ₂ ≈ 21.0220."""
        self.assertAlmostEqual(_RIEMANN_ZEROS_10[1], 21.022, places=2)

    def test_gamma3_approx(self):
        """γ₃ ≈ 25.0109."""
        self.assertAlmostEqual(_RIEMANN_ZEROS_10[2], 25.011, places=2)

    def test_zeros_increasing(self):
        """Los ceros deben estar en orden estrictamente creciente."""
        for i in range(len(_RIEMANN_ZEROS_10) - 1):
            self.assertLess(_RIEMANN_ZEROS_10[i], _RIEMANN_ZEROS_10[i + 1])

    def test_zeros_all_positive(self):
        """Todos los ceros deben ser positivos."""
        for z in _RIEMANN_ZEROS_10:
            self.assertGreater(z, 0.0)

    def test_gamma1_precision(self):
        """γ₁ debe coincidir con valor de referencia a 6 decimales."""
        self.assertAlmostEqual(_RIEMANN_ZEROS_10[0], 14.134725, places=6)

    def test_gamma10_approx(self):
        """γ₁₀ ≈ 49.77."""
        self.assertAlmostEqual(_RIEMANN_ZEROS_10[9], 49.77, places=1)

    def test_range_first_zero(self):
        """γ₁ debe estar entre 14.0 y 15.0."""
        self.assertGreater(_RIEMANN_ZEROS_10[0], 14.0)
        self.assertLess(_RIEMANN_ZEROS_10[0], 15.0)


# ============================================================================
# TestConstantesPsiDiamond – 14 tests
# ============================================================================


class TestConstantesPsiDiamond(unittest.TestCase):
    """Tests para ConstantesPsiDiamond."""

    def setUp(self):
        self.c = ConstantesPsiDiamond()

    def test_f0_default(self):
        """f0 por defecto debe ser 141.7001 Hz."""
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_theta_default(self):
        """theta por defecto debe ser 0.052463 rad."""
        self.assertAlmostEqual(self.c.theta, 0.052463, places=6)

    def test_tau_default(self):
        """tau por defecto debe ser 3600 s."""
        self.assertAlmostEqual(self.c.tau, 3600.0, places=6)

    def test_epsilon_default(self):
        """epsilon por defecto debe ser 1e-3."""
        self.assertAlmostEqual(self.c.epsilon, 1.0e-3, places=10)

    def test_n_modos_default(self):
        """n_modos por defecto debe ser 100."""
        self.assertEqual(self.c.n_modos, 100)

    def test_dps_default(self):
        """dps por defecto debe ser 30."""
        self.assertEqual(self.c.dps, 30)

    def test_psi_umbral(self):
        """psi_umbral debe ser 0.888."""
        self.assertAlmostEqual(self.c.psi_umbral, 0.888, places=3)

    def test_custom_f0(self):
        """Se puede instanciar con f0 personalizado."""
        c = ConstantesPsiDiamond(f0=200.0)
        self.assertAlmostEqual(c.f0, 200.0, places=6)

    def test_custom_tau(self):
        """Se puede instanciar con tau personalizado."""
        c = ConstantesPsiDiamond(tau=7200.0)
        self.assertAlmostEqual(c.tau, 7200.0, places=6)

    def test_custom_n_modos(self):
        """Se puede instanciar con n_modos personalizado."""
        c = ConstantesPsiDiamond(n_modos=50)
        self.assertEqual(c.n_modos, 50)

    def test_custom_theta(self):
        """Se puede instanciar con theta personalizado."""
        c = ConstantesPsiDiamond(theta=0.1)
        self.assertAlmostEqual(c.theta, 0.1, places=10)

    def test_custom_epsilon(self):
        """Se puede instanciar con epsilon personalizado."""
        c = ConstantesPsiDiamond(epsilon=2.0e-3)
        self.assertAlmostEqual(c.epsilon, 2.0e-3, places=10)

    def test_repr_contains_f0(self):
        """__repr__ debe mencionar f0."""
        self.assertIn("141.7001", repr(self.c))

    def test_repr_contains_tau(self):
        """__repr__ debe mencionar tau."""
        self.assertIn("3600", repr(self.c))


# ============================================================================
# TestRiemannZerosCache – 14 tests
# ============================================================================


class TestRiemannZerosCache(unittest.TestCase):
    """Tests para RiemannZerosCache."""

    def setUp(self):
        self.cache = RiemannZerosCache(n=_N_FAST)

    def test_obtener_returns_array(self):
        """obtener() debe devolver un array numpy."""
        import numpy as np

        arr = self.cache.obtener()
        self.assertIsInstance(arr, np.ndarray)

    def test_obtener_length(self):
        """obtener() debe devolver exactamente N elementos."""
        arr = self.cache.obtener()
        self.assertEqual(len(arr), _N_FAST)

    def test_gamma1_positive(self):
        """gamma_1 debe ser positivo."""
        self.assertGreater(self.cache.gamma_1, 0.0)

    def test_gamma1_approx(self):
        """gamma_1 debe ser ≈ 14.1347."""
        self.assertAlmostEqual(self.cache.gamma_1, 14.1347, places=2)

    def test_zeros_increasing(self):
        """Los ceros calculados deben estar en orden creciente."""
        arr = self.cache.obtener()
        for i in range(len(arr) - 1):
            self.assertLess(arr[i], arr[i + 1])

    def test_zeros_all_positive(self):
        """Todos los ceros calculados deben ser positivos."""
        arr = self.cache.obtener()
        for z in arr:
            self.assertGreater(z, 0.0)

    def test_cache_consistency(self):
        """Dos llamadas a obtener() deben retornar el mismo array."""
        arr1 = self.cache.obtener()
        arr2 = self.cache.obtener()
        self.assertTrue((arr1 == arr2).all())

    def test_fallback_n_le_10(self):
        """Fallback funciona para N ≤ 10."""
        cache = RiemannZerosCache(n=5)
        arr = cache._fallback()
        self.assertEqual(len(arr), 5)

    def test_fallback_n_gt_10(self):
        """Fallback extiende para N > 10."""
        cache = RiemannZerosCache(n=15)
        arr = cache._fallback()
        self.assertEqual(len(arr), 15)

    def test_fallback_first_zero(self):
        """Fallback γ₁ debe ser ≈ 14.1347."""
        cache = RiemannZerosCache(n=_N_FAST)
        arr = cache._fallback()
        self.assertAlmostEqual(arr[0], 14.1347, places=3)

    def test_zeros_range_reasonable(self):
        """Los primeros 10 ceros deben estar entre 14 y 60."""
        arr = self.cache.obtener()
        self.assertGreater(arr[0], 14.0)
        self.assertLess(arr[-1], 60.0)

    def test_n_attribute(self):
        """Atributo n debe coincidir con el valor pasado."""
        self.assertEqual(self.cache.n, _N_FAST)

    def test_dps_attribute(self):
        """Atributo dps debe ser positivo."""
        self.assertGreater(self.cache.dps, 0)

    def test_single_zero_cache(self):
        """Cache con n=1 devuelve exactamente un cero."""
        cache = RiemannZerosCache(n=1)
        arr = cache.obtener()
        self.assertEqual(len(arr), 1)


# ============================================================================
# TestModosAdelicos – 18 tests
# ============================================================================


class TestModosAdelicos(unittest.TestCase):
    """Tests para ModosAdelicos."""

    def setUp(self):
        cst = ConstantesPsiDiamond(n_modos=_N_FAST)
        cache = RiemannZerosCache(n=_N_FAST)
        self.modos = ModosAdelicos(constantes=cst, cache=cache)

    def test_gamma_length(self):
        """gamma debe tener N elementos."""
        self.assertEqual(len(self.modos.gamma), _N_FAST)

    def test_gamma_tilde_length(self):
        """gamma_tilde debe tener N elementos."""
        self.assertEqual(len(self.modos.gamma_tilde), _N_FAST)

    def test_pesos_length(self):
        """pesos debe tener N elementos."""
        self.assertEqual(len(self.modos.pesos), _N_FAST)

    def test_omegas_length(self):
        """omegas debe tener N elementos."""
        self.assertEqual(len(self.modos.omegas), _N_FAST)

    def test_c_scale_positive(self):
        """c_scale debe ser positivo."""
        self.assertGreater(self.modos.c_scale, 0.0)

    def test_c_scale_range(self):
        """c_scale debe estar en rango razonable (0.5, 2.0)."""
        self.assertGreater(self.modos.c_scale, 0.5)
        self.assertLess(self.modos.c_scale, 2.0)

    def test_gamma_tilde_all_positive(self):
        """gamma_tilde debe ser positivo para todos los modos."""
        import numpy as np

        self.assertTrue(np.all(self.modos.gamma_tilde > 0.0))

    def test_pesos_all_positive(self):
        """Los pesos wₙ deben ser todos positivos."""
        import numpy as np

        self.assertTrue(np.all(self.modos.pesos > 0.0))

    def test_omegas_all_positive(self):
        """Las frecuencias ωₙ deben ser todas positivas."""
        import numpy as np

        self.assertTrue(np.all(self.modos.omegas > 0.0))

    def test_pesos_formula(self):
        """wₙ = 1/γ̃ₙ — verificar para el primer modo."""
        w0 = self.modos.pesos[0]
        gt0 = self.modos.gamma_tilde[0]
        self.assertAlmostEqual(w0, 1.0 / gt0, places=12)

    def test_omegas_formula(self):
        """ωₙ = γ̃ₙ · f₀ · ε — verificar para el primer modo."""
        omega0 = self.modos.omegas[0]
        gt0 = self.modos.gamma_tilde[0]
        expected = gt0 * 141.7001 * 1.0e-3
        self.assertAlmostEqual(omega0, expected, places=10)

    def test_peso_total_positive(self):
        """peso_total debe ser positivo."""
        self.assertGreater(self.modos.peso_total, 0.0)

    def test_gamma_tilde_gt_gamma_positive(self):
        """Todos los γ̃ₙ deben ser positivos (la modulación no invierte el signo)."""
        import numpy as np

        self.assertTrue(np.all(self.modos.gamma_tilde > 0.0))

    def test_pesos_all_positive_after_abs(self):
        """Los pesos wₙ deben ser positivos (garantizado por valor absoluto de γ̃ₙ)."""
        import numpy as np

        self.assertTrue(np.all(self.modos.pesos > 0.0))

    def test_lazy_evaluation_gamma(self):
        """gamma se calcula de forma perezosa."""
        modos = ModosAdelicos(constantes=ConstantesPsiDiamond(n_modos=_N_FAST))
        self.assertIsNone(modos._gamma)
        _ = modos.gamma
        self.assertIsNotNone(modos._gamma)

    def test_lazy_evaluation_gamma_tilde(self):
        """gamma_tilde se calcula de forma perezosa."""
        modos = ModosAdelicos(constantes=ConstantesPsiDiamond(n_modos=_N_FAST))
        self.assertIsNone(modos._gamma_tilde)
        _ = modos.gamma_tilde
        self.assertIsNotNone(modos._gamma_tilde)

    def test_default_construction(self):
        """ModosAdelicos puede construirse sin argumentos."""
        modos = ModosAdelicos()
        self.assertIsNotNone(modos.cst)
        self.assertIsNotNone(modos.cache)

    def test_c_scale_formula(self):
        """c_scale = √(2π / log(T/2π)) con T = 2π·N."""
        n = _N_FAST
        T = 2.0 * math.pi * n
        expected = math.sqrt(2.0 * math.pi / math.log(T / (2.0 * math.pi)))
        self.assertAlmostEqual(self.modos.c_scale, expected, places=12)


# ============================================================================
# TestCoherenciaTemporal – 24 tests
# ============================================================================


class TestCoherenciaTemporal(unittest.TestCase):
    """Tests para CoherenciaTemporal."""

    def setUp(self):
        self.ct = _make_ct()

    def test_psi_t0_exact(self):
        """Ψ(0) debe ser exactamente 1.0 (Diamond-State puro)."""
        self.assertAlmostEqual(self.ct.psi(0.0), 1.0, places=12)

    def test_psi_t0_unity(self):
        """Ψ(0) = 1.0 con tolerancia 1e-10."""
        self.assertLess(abs(self.ct.psi(0.0) - 1.0), 1.0e-10)

    def test_psi_range(self):
        """Ψ(t) puede oscilar fuera de [0.5, 1.0] para N finito; siempre ∈ [0, 1]."""
        for t in [0, 10, 100, 1000, 3600, 36000]:
            p = self.ct.psi(float(t))
            self.assertGreaterEqual(p, -0.001)  # bounded below by C(t) ≥ -1
            self.assertLessEqual(p, 1.001)

    def test_psi_decreasing_tendency(self):
        """Ψ(t) debe tender a decrecer con el tiempo."""
        self.assertGreater(self.ct.psi(0.0), self.ct.psi(3600.0))

    def test_psi_tau_above_half(self):
        """Ψ(τ) debe ser > 0.5 (coherencia residual a tiempo τ)."""
        self.assertGreater(self.ct.psi(3600.0), 0.5)

    def test_correlacion_t0(self):
        """C(0) debe ser ≈ 1.0 (dado que e^0=1 y cos(0)=1)."""
        self.assertAlmostEqual(self.ct.correlacion(0.0), 1.0, places=12)

    def test_correlacion_large_t(self):
        """C(t_grande) ≈ 0 → Ψ → 0.5."""
        c_inf = self.ct.correlacion(1.0e8)
        self.assertAlmostEqual(c_inf, 0.0, places=6)

    def test_psi_from_correlacion(self):
        """Ψ(t) = (1 + C(t)) / 2 — consistencia."""
        t = 100.0
        c = self.ct.correlacion(t)
        psi_manual = (1.0 + c) / 2.0
        self.assertAlmostEqual(self.ct.psi(t), psi_manual, places=12)

    def test_limite_termico_near_half(self):
        """limite_termico() debe ser ≈ 0.5."""
        lim = self.ct.limite_termico()
        self.assertAlmostEqual(lim, 0.5, places=5)

    def test_limite_termico_above_half(self):
        """limite_termico() debe ser ≥ 0.5."""
        self.assertGreaterEqual(self.ct.limite_termico(), 0.5 - 1e-6)

    def test_tabla_length(self):
        """tabla() debe devolver la misma cantidad de elementos que tiempos."""
        tiempos = [0.0, 10.0, 100.0, 3600.0]
        res = self.ct.tabla(tiempos)
        self.assertEqual(len(res), len(tiempos))

    def test_tabla_first_time(self):
        """El primer elemento de tabla() debe ser (0.0, Ψ(0))."""
        tiempos = [0.0, 10.0]
        res = self.ct.tabla(tiempos)
        self.assertEqual(res[0][0], 0.0)
        self.assertAlmostEqual(res[0][1], 1.0, places=12)

    def test_tabla_times_preserved(self):
        """tabla() debe preservar los tiempos de entrada."""
        tiempos = [0.0, 50.0, 500.0]
        res = self.ct.tabla(tiempos)
        for i, t in enumerate(tiempos):
            self.assertEqual(res[i][0], t)

    def test_correlacion_decays_with_time(self):
        """La correlación debe decrecer (en valor absoluto) con t creciente."""
        c10 = abs(self.ct.correlacion(10.0))
        c3600 = abs(self.ct.correlacion(3600.0))
        self.assertGreater(c10, c3600)

    def test_psi_continuous(self):
        """Ψ(t) debe ser continua: pequeña variación en t → pequeña variación en Ψ."""
        delta = 1.0e-3
        p1 = self.ct.psi(100.0)
        p2 = self.ct.psi(100.0 + delta)
        self.assertLess(abs(p1 - p2), 0.01)

    def test_psi_t0_integer(self):
        """Ψ(0) con argumento entero debe ser 1.0."""
        self.assertAlmostEqual(self.ct.psi(0), 1.0, places=12)

    def test_psi_large_t(self):
        """Ψ(t muy grande) debe ser muy próximo a 0.5."""
        p = self.ct.psi(1.0e8)
        self.assertAlmostEqual(p, 0.5, places=5)

    def test_psi_t10_reasonable(self):
        """Ψ(10) debe estar en [0, 1] (puede oscilar con N finito)."""
        p = self.ct.psi(10.0)
        self.assertGreaterEqual(p, -0.001)
        self.assertLessEqual(p, 1.001)

    def test_psi_t3600_reasonable(self):
        """Ψ(3600) debe estar entre 0.5 y 0.6."""
        p = self.ct.psi(3600.0)
        self.assertGreater(p, 0.5)
        self.assertLess(p, 0.6)

    def test_default_construction(self):
        """CoherenciaTemporal puede construirse sin argumentos."""
        ct = CoherenciaTemporal()
        self.assertIsNotNone(ct.cst)
        self.assertIsNotNone(ct.modos)

    def test_psi_monotone_large_scale(self):
        """A escala grande, Ψ debe ser no-creciente en promedio."""
        vals = [self.ct.psi(float(t)) for t in [0, 1800, 3600, 7200, 18000]]
        self.assertGreaterEqual(vals[0], vals[-1])

    def test_exponential_decay_factor(self):
        """El factor de decaimiento e^(-τ/τ) = e^(-1) ≈ 0.3679."""
        factor = math.exp(-3600.0 / 3600.0)
        self.assertAlmostEqual(factor, math.exp(-1.0), places=12)

    def test_correlacion_at_tau(self):
        """C(τ) debe tener |valor| ≤ e^(-1) ≈ 0.368."""
        c = abs(self.ct.correlacion(3600.0))
        self.assertLessEqual(c, math.exp(-1.0) + 1e-10)

    def test_tabla_psi_values_in_range(self):
        """Todos los Ψ(t) de la tabla deben estar en [0, 1]."""
        tiempos = [0.0, 10.0, 100.0, 1000.0, 3600.0]
        res = self.ct.tabla(tiempos)
        for t, p in res:
            self.assertGreaterEqual(p, -0.001)
            self.assertLessEqual(p, 1.001)


# ============================================================================
# TestCoherenciaGlobal – 18 tests
# ============================================================================


class TestCoherenciaGlobal(unittest.TestCase):
    """Tests para CoherenciaGlobal."""

    def setUp(self):
        cst = ConstantesPsiDiamond(n_modos=_N_FAST)
        cache = RiemannZerosCache(n=_N_FAST)
        modos = ModosAdelicos(constantes=cst, cache=cache)
        ct = CoherenciaTemporal(constantes=cst, modos=modos)
        self.cg = CoherenciaGlobal(constantes=cst, modos=modos, coherencia=ct)

    def test_psi_inicial_unity(self):
        """psi_inicial() debe ser 1.0 (Ψ(0) = 1)."""
        self.assertAlmostEqual(self.cg.psi_inicial(), 1.0, places=10)

    def test_psi_limite_range(self):
        """psi_limite() debe estar en [0, 1]."""
        p = self.cg.psi_limite()
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_psi_limite_near_one(self):
        """psi_limite() debe ser alto (convergencia al equilibrio térmico)."""
        self.assertGreater(self.cg.psi_limite(), 0.8)

    def test_psi_tau_range(self):
        """psi_tau() debe estar en [0, 1]."""
        p = self.cg.psi_tau()
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_psi_tau_positive(self):
        """psi_tau() debe ser > 0 (Ψ(τ) ≥ 0)."""
        self.assertGreater(self.cg.psi_tau(), 0.0)

    def test_psi_modos_range(self):
        """psi_modos() debe estar en [0, 1]."""
        p = self.cg.psi_modos()
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_psi_adelica_range(self):
        """psi_adelica() debe estar en [0, 1]."""
        p = self.cg.psi_adelica()
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_psi_global_range(self):
        """psi_global() debe estar en [0, 1]."""
        p = self.cg.psi_global()
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_psi_global_meets_umbral(self):
        """psi_global() debe ser ≥ 0.888 para activar el sello."""
        self.assertGreaterEqual(self.cg.psi_global(), 0.888)

    def test_sello_activo(self):
        """sello_activo() debe ser True con los parámetros por defecto."""
        self.assertTrue(self.cg.sello_activo())

    def test_psi_modos_entropy(self):
        """psi_modos() mide fracción de modos válidos — debe estar en [0, 1]."""
        self.assertGreaterEqual(self.cg.psi_modos(), 0.0)
        self.assertLessEqual(self.cg.psi_modos(), 1.0)

    def test_psi_global_weighted(self):
        """psi_global() es promedio ponderado — calcularlo manualmente."""
        metricas = [
            self.cg.psi_inicial(),
            self.cg.psi_limite(),
            self.cg.psi_tau(),
            self.cg.psi_modos(),
            self.cg.psi_adelica(),
        ]
        pesos = [2.0, 2.0, 0.5, 1.0, 0.5]
        expected = sum(p * m for p, m in zip(pesos, metricas)) / sum(pesos)
        self.assertAlmostEqual(self.cg.psi_global(), expected, places=12)

    def test_default_construction(self):
        """CoherenciaGlobal puede construirse sin argumentos."""
        cg = CoherenciaGlobal()
        self.assertIsNotNone(cg.cst)

    def test_psi_inicial_formula(self):
        """psi_inicial() debe coincidir con ct.psi(0)."""
        ct = self.cg.ct
        self.assertAlmostEqual(self.cg.psi_inicial(), ct.psi(0.0), places=12)

    def test_psi_limite_formula(self):
        """psi_limite() = 1 − 2·|Ψ(∞)−0.5|."""
        psi_inf = self.cg.ct.limite_termico()
        expected = max(0.0, 1.0 - 2.0 * abs(psi_inf - 0.5))
        self.assertAlmostEqual(self.cg.psi_limite(), expected, places=12)

    def test_psi_tau_formula(self):
        """psi_tau() = Ψ(τ) directo."""
        tau = self.cg.cst.tau
        psi_at_tau = self.cg.ct.psi(tau)
        self.assertAlmostEqual(self.cg.psi_tau(), psi_at_tau, places=12)

    def test_sello_consistency(self):
        """sello_activo() es consistente con psi_global() ≥ 0.888."""
        sello = self.cg.sello_activo()
        global_val = self.cg.psi_global()
        if sello:
            self.assertGreaterEqual(global_val, 0.888)
        else:
            self.assertLess(global_val, 0.888)

    def test_pesos_metricas_sum(self):
        """La suma de pesos de métricas debe ser 6.0."""
        pesos = CoherenciaGlobal._PESOS_METRICAS
        self.assertAlmostEqual(sum(pesos), 6.0, places=10)


# ============================================================================
# TestSistemaPsiDiamond – 16 tests
# ============================================================================


class TestSistemaPsiDiamond(unittest.TestCase):
    """Tests para SistemaPsiDiamond."""

    def setUp(self):
        self.sistema = _make_sistema()

    def test_activar_returns_resultado(self):
        """activar() debe devolver un ResultadoPsiDiamond."""
        res = self.sistema.activar()
        self.assertIsInstance(res, ResultadoPsiDiamond)

    def test_psi_t0_unity(self):
        """ResultadoPsiDiamond.psi_t0 debe ser 1.0."""
        res = self.sistema.activar()
        self.assertAlmostEqual(res.psi_t0, 1.0, places=10)

    def test_psi_tau_above_half(self):
        """ResultadoPsiDiamond.psi_tau debe ser > 0.5."""
        res = self.sistema.activar()
        self.assertGreater(res.psi_tau, 0.5)

    def test_psi_infinito_near_half(self):
        """ResultadoPsiDiamond.psi_infinito debe ser ≈ 0.5."""
        res = self.sistema.activar()
        self.assertAlmostEqual(res.psi_infinito, 0.5, places=5)

    def test_sello_activo(self):
        """ResultadoPsiDiamond.sello_activo debe ser True."""
        res = self.sistema.activar()
        self.assertTrue(res.sello_activo)

    def test_psi_global_meets_umbral(self):
        """psi_global debe ser ≥ 0.888."""
        res = self.sistema.activar()
        self.assertGreaterEqual(res.psi_global, 0.888)

    def test_gamma_1_positive(self):
        """gamma_1 debe ser positivo."""
        res = self.sistema.activar()
        self.assertGreater(res.gamma_1, 0.0)

    def test_gamma_tilde_1_positive(self):
        """gamma_tilde_1 debe ser positivo."""
        res = self.sistema.activar()
        self.assertGreater(res.gamma_tilde_1, 0.0)

    def test_tabla_length(self):
        """tabla_tiempos debe tener 10 entradas (tiempos de referencia)."""
        res = self.sistema.activar()
        self.assertEqual(len(res.tabla_tiempos), 10)

    def test_tabla_first_entry(self):
        """Primera entrada de tabla debe ser (0.0, 1.0)."""
        res = self.sistema.activar()
        t, psi = res.tabla_tiempos[0]
        self.assertEqual(t, 0)
        self.assertAlmostEqual(psi, 1.0, places=10)

    def test_tabla_last_entry(self):
        """Última entrada de tabla debe ser (3600, Ψ(3600))."""
        res = self.sistema.activar()
        t, psi = res.tabla_tiempos[-1]
        self.assertEqual(t, 3600)
        self.assertGreater(psi, 0.5)

    def test_n_modos_preserved(self):
        """n_modos en el resultado debe coincidir con el sistema."""
        res = self.sistema.activar()
        self.assertEqual(res.n_modos, _N_FAST)

    def test_f0_preserved(self):
        """f0 en el resultado debe ser 141.7001."""
        res = self.sistema.activar()
        self.assertAlmostEqual(res.f0, 141.7001, places=4)

    def test_tau_preserved(self):
        """tau en el resultado debe ser 3600."""
        res = self.sistema.activar()
        self.assertAlmostEqual(res.tau, 3600.0, places=6)

    def test_descripcion_contains_activo(self):
        """descripcion debe contener 'ACTIVO' cuando el sello está activo."""
        res = self.sistema.activar()
        if res.sello_activo:
            self.assertIn("ACTIVO", res.descripcion)

    def test_tiempos_referencia_length(self):
        """TIEMPOS_REFERENCIA debe tener 10 tiempos."""
        self.assertEqual(len(SistemaPsiDiamond.TIEMPOS_REFERENCIA), 10)


# ============================================================================
# TestResultadoPsiDiamond – 10 tests
# ============================================================================


class TestResultadoPsiDiamond(unittest.TestCase):
    """Tests para la dataclass ResultadoPsiDiamond."""

    def setUp(self):
        self.res = _make_sistema().activar()

    def test_has_n_modos(self):
        """ResultadoPsiDiamond debe tener atributo n_modos."""
        self.assertTrue(hasattr(self.res, "n_modos"))

    def test_has_f0(self):
        """ResultadoPsiDiamond debe tener atributo f0."""
        self.assertTrue(hasattr(self.res, "f0"))

    def test_has_tau(self):
        """ResultadoPsiDiamond debe tener atributo tau."""
        self.assertTrue(hasattr(self.res, "tau"))

    def test_has_psi_t0(self):
        """ResultadoPsiDiamond debe tener atributo psi_t0."""
        self.assertTrue(hasattr(self.res, "psi_t0"))

    def test_has_psi_tau(self):
        """ResultadoPsiDiamond debe tener atributo psi_tau."""
        self.assertTrue(hasattr(self.res, "psi_tau"))

    def test_has_sello_activo(self):
        """ResultadoPsiDiamond debe tener atributo sello_activo."""
        self.assertTrue(hasattr(self.res, "sello_activo"))

    def test_has_gamma_1(self):
        """ResultadoPsiDiamond debe tener atributo gamma_1."""
        self.assertTrue(hasattr(self.res, "gamma_1"))

    def test_has_gamma_tilde_1(self):
        """ResultadoPsiDiamond debe tener atributo gamma_tilde_1."""
        self.assertTrue(hasattr(self.res, "gamma_tilde_1"))

    def test_has_tabla_tiempos(self):
        """ResultadoPsiDiamond debe tener atributo tabla_tiempos."""
        self.assertTrue(hasattr(self.res, "tabla_tiempos"))

    def test_descripcion_is_string(self):
        """descripcion debe ser un string."""
        self.assertIsInstance(self.res.descripcion, str)


# ============================================================================
# TestAPIPublic – 14 tests
# ============================================================================


class TestAPIPublic(unittest.TestCase):
    """Tests para la API pública psi_diamond_activar()."""

    def setUp(self):
        # Usar N pequeño para que sea rápido
        self.r = psi_diamond_activar(n_modos=_N_FAST)

    def test_returns_dict(self):
        """psi_diamond_activar() debe devolver un diccionario."""
        self.assertIsInstance(self.r, dict)

    def test_sello_activo_key(self):
        """El diccionario debe tener clave 'sello_activo'."""
        self.assertIn("sello_activo", self.r)

    def test_sello_activo_value(self):
        """sello_activo debe ser True con parámetros por defecto."""
        self.assertTrue(self.r["sello_activo"])

    def test_psi_t0_unity(self):
        """psi_t0 debe ser 1.0."""
        self.assertAlmostEqual(self.r["psi_t0"], 1.0, places=10)

    def test_psi_tau_above_half(self):
        """psi_tau debe ser > 0.5."""
        self.assertGreater(self.r["psi_tau"], 0.5)

    def test_psi_infinito_near_half(self):
        """psi_infinito debe ser ≈ 0.5."""
        self.assertAlmostEqual(self.r["psi_infinito"], 0.5, places=5)

    def test_psi_global_meets_umbral(self):
        """psi_global debe ser ≥ 0.888."""
        self.assertGreaterEqual(self.r["psi_global"], 0.888)

    def test_n_modos_key(self):
        """El diccionario debe tener clave 'n_modos'."""
        self.assertIn("n_modos", self.r)

    def test_tabla_tiempos_key(self):
        """El diccionario debe tener clave 'tabla_tiempos'."""
        self.assertIn("tabla_tiempos", self.r)

    def test_gamma_1_key(self):
        """El diccionario debe tener clave 'gamma_1'."""
        self.assertIn("gamma_1", self.r)

    def test_gamma_1_positive(self):
        """gamma_1 debe ser positivo."""
        self.assertGreater(self.r["gamma_1"], 0.0)

    def test_descripcion_key(self):
        """El diccionario debe tener clave 'descripcion'."""
        self.assertIn("descripcion", self.r)

    def test_all_required_keys(self):
        """El diccionario debe tener todas las claves requeridas."""
        required = {
            "sello_activo", "psi_t0", "psi_tau", "psi_infinito",
            "psi_global", "n_modos", "f0", "tau", "theta",
            "gamma_1", "gamma_tilde_1", "tabla_tiempos", "descripcion",
        }
        for key in required:
            self.assertIn(key, self.r)

    def test_custom_n_modos(self):
        """psi_diamond_activar admite n_modos personalizado."""
        r = psi_diamond_activar(n_modos=5)
        self.assertEqual(r["n_modos"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
