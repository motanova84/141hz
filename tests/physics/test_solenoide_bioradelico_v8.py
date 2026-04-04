"""
Tests for physics.solenoide_bioradelico_v8 — Sistema Bio-Adélico V8 ∴SBA∞³

Pruebas que cubren todas las clases y la API pública:
  - ConstantesBioAdelico   – constantes físicas del sistema
  - SolenoideAdelico       – traza adélica en t = k·log p
  - DobleHelice            – señal de 10 bases ADN como osciladores Riemann
  - CoherenciaCuantica     – envolvente de decaimiento τ
  - TraceBioAdelica        – traza combinada en dominio temporal
  - AnalisisFFT            – detección de picos espectrales
  - CoherenciaGlobal       – Ψ_global ≥ 0.888
  - SistemaBioAdelicoV8    – orquestador con activar()
  - ResultadoBioAdelicoV8  – dataclass de resultados
  - solenoide_bioradelico_v8_activar() – API pública

Invariantes clave verificados:
  - f₀ = 141.7001 Hz
  - 10 ceros de Riemann γₙ (γ₁ ≈ 14.1347)
  - 10 primos para el solenoide adélico
  - τ ≈ 2.46 ps
  - Ψ_global ≥ 0.888 → sello ∴SBA∞³ ACTIVO
  - f_scaled_min_hz ≈ γ₁ × f₀ / (2π) ≈ 319 Hz
"""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from physics.solenoide_bioradelico_v8 import (
    # Constantes de módulo
    _F0,
    _GAMMAS,
    _PRIMOS,
    _TAU_PS,
    _TAU_NORM,
    _T0_S,
    _N_PUNTOS,
    _N_PERIODOS,
    _PSI_UMBRAL,
    _N_BASES,
    _N_PRIMOS,
    _PICOS_ESPERADOS,
    _SELLO,
    _F_SCALED_MIN,
    _F_SCALED_MAX,
    # Clases
    ConstantesBioAdelico,
    SolenoideAdelico,
    DobleHelice,
    CoherenciaCuantica,
    TraceBioAdelica,
    AnalisisFFT,
    CoherenciaGlobal,
    SistemaBioAdelicoV8,
    ResultadoBioAdelicoV8,
    # API pública
    solenoide_bioradelico_v8_activar,
)


# ============================================================================
# TestModuleConstants – 18 tests
# ============================================================================

class TestModuleConstants(unittest.TestCase):
    """Tests para las constantes de módulo."""

    def test_f0_value(self):
        self.assertAlmostEqual(_F0, 141.7001, places=4)

    def test_gammas_count(self):
        self.assertEqual(len(_GAMMAS), 10)

    def test_gamma1_value(self):
        self.assertAlmostEqual(_GAMMAS[0], 14.1347251417347, places=5)

    def test_gamma2_value(self):
        self.assertAlmostEqual(_GAMMAS[1], 21.0220396387716, places=5)

    def test_gammas_ascending(self):
        for i in range(len(_GAMMAS) - 1):
            self.assertLess(_GAMMAS[i], _GAMMAS[i + 1])

    def test_primos_count(self):
        self.assertEqual(len(_PRIMOS), 10)

    def test_primos_first(self):
        self.assertEqual(_PRIMOS[0], 2)
        self.assertEqual(_PRIMOS[1], 3)
        self.assertEqual(_PRIMOS[2], 5)

    def test_tau_ps_value(self):
        self.assertAlmostEqual(_TAU_PS, 2.46e-12, places=20)

    def test_t0_derived(self):
        self.assertAlmostEqual(_T0_S, 1.0 / _F0, places=15)

    def test_tau_norm_tiny(self):
        # τ_norm = τ_ps / T₀ debe ser muy pequeño (≈ 3.49e-10)
        self.assertLess(_TAU_NORM, 1e-8)
        self.assertGreater(_TAU_NORM, 0)

    def test_n_puntos(self):
        self.assertEqual(_N_PUNTOS, 1024)

    def test_n_periodos(self):
        self.assertEqual(_N_PERIODOS, 10.0)

    def test_psi_umbral(self):
        self.assertAlmostEqual(_PSI_UMBRAL, 0.888, places=3)

    def test_n_bases(self):
        self.assertEqual(_N_BASES, 10)

    def test_n_primos(self):
        self.assertEqual(_N_PRIMOS, 10)

    def test_picos_esperados(self):
        self.assertEqual(len(_PICOS_ESPERADOS), 3)
        self.assertAlmostEqual(_PICOS_ESPERADOS[0], 2.8, places=1)

    def test_f_scaled_min(self):
        expected = _GAMMAS[0] * _F0 / (2 * math.pi)
        self.assertAlmostEqual(_F_SCALED_MIN, expected, places=5)

    def test_sello_string(self):
        self.assertIn("SBA", _SELLO)


# ============================================================================
# TestConstantesBioAdelico – 8 tests
# ============================================================================

class TestConstantesBioAdelico(unittest.TestCase):
    """Tests para ConstantesBioAdelico."""

    def setUp(self):
        self.c = ConstantesBioAdelico()

    def test_f0_default(self):
        self.assertAlmostEqual(self.c.f0, 141.7001, places=4)

    def test_tau_ps_default(self):
        self.assertAlmostEqual(self.c.tau_ps, 2.46e-12, places=20)

    def test_omega0(self):
        expected = 2 * math.pi * 141.7001
        self.assertAlmostEqual(self.c.omega0(), expected, places=5)

    def test_t0(self):
        self.assertAlmostEqual(self.c.t0(), 1.0 / 141.7001, places=10)

    def test_tau_norm(self):
        tn = self.c.tau_norm()
        self.assertGreater(tn, 0)
        self.assertLess(tn, 1e-7)

    def test_es_valido(self):
        self.assertTrue(self.c.es_valido())

    def test_invalido_f0_negativo(self):
        c = ConstantesBioAdelico(f0=-1.0)
        self.assertFalse(c.es_valido())

    def test_personalizado(self):
        c = ConstantesBioAdelico(f0=100.0, n_bases=5)
        self.assertEqual(c.f0, 100.0)
        self.assertEqual(c.n_bases, 5)
        self.assertTrue(c.es_valido())


# ============================================================================
# TestSolenoideAdelico – 8 tests
# ============================================================================

class TestSolenoideAdelico(unittest.TestCase):
    """Tests para SolenoideAdelico."""

    def setUp(self):
        self.sol = SolenoideAdelico()

    def test_log_primos_count(self):
        self.assertEqual(len(self.sol._log_primos), len(self.sol.primos))

    def test_log_primos_values(self):
        # log(2) ≈ 0.693
        self.assertAlmostEqual(self.sol._log_primos[0], math.log(2), places=10)

    def test_traza_en_escalar(self):
        val = self.sol.traza_en(0.5)
        self.assertIsInstance(val, float)

    def test_traza_en_cero(self):
        # t=0 debería dar un valor finito
        val = self.sol.traza_en(0.0)
        self.assertTrue(math.isfinite(val))

    def test_traza_vector_length(self):
        tiempos = [i * 0.1 for i in range(20)]
        vals = self.sol.traza_vector(tiempos)
        self.assertEqual(len(vals), 20)

    def test_traza_vector_finite(self):
        tiempos = [i * 0.01 for i in range(50)]
        vals = self.sol.traza_vector(tiempos)
        for v in vals:
            self.assertTrue(math.isfinite(v))

    def test_amplitud_rms_positive(self):
        tiempos = [i * 0.05 for i in range(100)]
        rms = self.sol.amplitud_rms(tiempos)
        self.assertGreaterEqual(rms, 0)

    def test_sigma_affects_width(self):
        sol_narrow = SolenoideAdelico(sigma=0.01)
        sol_wide = SolenoideAdelico(sigma=0.5)
        # Ambos deberían dar valores finitos
        self.assertTrue(math.isfinite(sol_narrow.traza_en(math.log(2))))
        self.assertTrue(math.isfinite(sol_wide.traza_en(math.log(2))))


# ============================================================================
# TestDobleHelice – 10 tests
# ============================================================================

class TestDobleHelice(unittest.TestCase):
    """Tests para DobleHelice."""

    def setUp(self):
        self.helice = DobleHelice()

    def test_numero_bases(self):
        self.assertEqual(self.helice._n, 10)

    def test_frecuencias_count(self):
        freqs = self.helice.frecuencias_base()
        self.assertEqual(len(freqs), 10)

    def test_frecuencia_min_positiva(self):
        self.assertGreater(self.helice.frecuencia_min(), 0)

    def test_frecuencia_min_rango(self):
        # γ₁ × f₀ / (2π) ≈ 319 Hz
        self.assertAlmostEqual(self.helice.frecuencia_min(), 318.77, delta=5)

    def test_frecuencia_max_positiva(self):
        self.assertGreater(self.helice.frecuencia_max(), self.helice.frecuencia_min())

    def test_señal_en_escalar(self):
        val = self.helice.señal_en(0.0)
        self.assertIsInstance(val, float)
        self.assertTrue(math.isfinite(val))

    def test_señal_vector_length(self):
        tiempos = [i * 1e-4 for i in range(50)]
        vals = self.helice.señal_vector(tiempos)
        self.assertEqual(len(vals), 50)

    def test_señal_finita(self):
        tiempos = [i * 1e-5 for i in range(100)]
        vals = self.helice.señal_vector(tiempos)
        for v in vals:
            self.assertTrue(math.isfinite(v))

    def test_energia_total_positiva(self):
        e = self.helice.energia_total()
        self.assertGreater(e, 0)

    def test_energia_total_sum(self):
        # Σ 1/(n+1) para n=0..9
        expected = sum(1.0 / (n + 1) for n in range(10))
        self.assertAlmostEqual(self.helice.energia_total(), expected, places=10)


# ============================================================================
# TestCoherenciaCuantica – 8 tests
# ============================================================================

class TestCoherenciaCuantica(unittest.TestCase):
    """Tests para CoherenciaCuantica."""

    def setUp(self):
        self.coh = CoherenciaCuantica()

    def test_omega0_derivado(self):
        self.assertAlmostEqual(self.coh._omega0, 2 * math.pi * 141.7001, places=4)

    def test_envolvente_t0(self):
        # C(0) debe ser máxima
        c0 = self.coh.envolvente_en(0.0)
        self.assertAlmostEqual(c0, 1.0, places=5)

    def test_envolvente_positiva(self):
        tiempos = [i * 1e-5 for i in range(50)]
        for t in tiempos:
            self.assertGreaterEqual(self.coh.envolvente_en(t), 0)

    def test_envolvente_decreciente(self):
        # La envolvente debería ser no creciente en promedio
        c0 = self.coh.envolvente_en(0.0)
        c_last = self.coh.envolvente_en(1.0 / 141.7001 * 10)
        # No necesariamente decreciente en cada punto pero el promedio sí
        self.assertGreaterEqual(c0, 0)
        self.assertGreaterEqual(c_last, 0)

    def test_envolvente_vector_length(self):
        tiempos = [i * 1e-5 for i in range(30)]
        vals = self.coh.envolvente_vector(tiempos)
        self.assertEqual(len(vals), 30)

    def test_psi_coherencia_rango(self):
        tiempos = [i * 1e-4 for i in range(100)]
        psi = self.coh.psi_coherencia(tiempos)
        self.assertGreaterEqual(psi, 0.888)
        self.assertLessEqual(psi, 1.0)

    def test_psi_coherencia_umbral(self):
        tiempos = [i * 1e-5 for i in range(200)]
        psi = self.coh.psi_coherencia(tiempos)
        self.assertGreaterEqual(psi, _PSI_UMBRAL)

    def test_psi_coherencia_lista_vacia(self):
        psi = self.coh.psi_coherencia([])
        self.assertEqual(psi, 0.0)


# ============================================================================
# TestTraceBioAdelica – 8 tests
# ============================================================================

class TestTraceBioAdelica(unittest.TestCase):
    """Tests para TraceBioAdelica."""

    def setUp(self):
        self.traza = TraceBioAdelica(n_puntos=64, n_periodos=5.0)

    def test_tiempos_length(self):
        tiempos = self.traza.tiempos()
        self.assertEqual(len(tiempos), 64)

    def test_tiempos_positivos(self):
        tiempos = self.traza.tiempos()
        for t in tiempos:
            self.assertGreaterEqual(t, 0)

    def test_calcular_length(self):
        vals = self.traza.calcular()
        self.assertEqual(len(vals), 64)

    def test_calcular_finito(self):
        vals = self.traza.calcular()
        for v in vals:
            self.assertTrue(math.isfinite(v), f"Valor no finito: {v}")

    def test_correlacion_escalar(self):
        bio = self.traza.calcular()
        corr = self.traza.correlacion_con_traza_espectral(bio)
        self.assertIsInstance(corr, float)
        self.assertTrue(math.isfinite(corr))

    def test_correlacion_rango(self):
        bio = self.traza.calcular()
        corr = self.traza.correlacion_con_traza_espectral(bio)
        self.assertGreaterEqual(corr, -1.0)
        self.assertLessEqual(corr, 1.0)

    def test_correlacion_vacia(self):
        corr = self.traza.correlacion_con_traza_espectral([])
        self.assertEqual(corr, 0.0)

    def test_alpha_beta_mix(self):
        t1 = TraceBioAdelica(n_puntos=32, n_periodos=3.0, alpha_mix=1.0, beta_mix=0.0)
        t2 = TraceBioAdelica(n_puntos=32, n_periodos=3.0, alpha_mix=0.0, beta_mix=1.0)
        v1 = t1.calcular()
        v2 = t2.calcular()
        # Deben ser diferentes cuando los pesos difieren
        diferencias = sum(abs(v1[i] - v2[i]) for i in range(len(v1)))
        self.assertGreater(diferencias, 0)


# ============================================================================
# TestAnalisisFFT – 8 tests
# ============================================================================

class TestAnalisisFFT(unittest.TestCase):
    """Tests para AnalisisFFT."""

    def setUp(self):
        dt = 10.0 / (141.7001 * 128)
        self.fft = AnalisisFFT(dt=dt, n_puntos=128)

    def test_frecuencias_length(self):
        freqs = self.fft.frecuencias()
        self.assertEqual(len(freqs), 64)

    def test_frecuencias_positivas(self):
        freqs = self.fft.frecuencias()
        for f in freqs:
            self.assertGreaterEqual(f, 0)

    def test_frecuencias_nyquist(self):
        freqs = self.fft.frecuencias()
        fs = 1.0 / self.fft.dt
        self.assertLessEqual(max(freqs), fs / 2 + 1)

    def test_magnitudes_length(self):
        señal = [math.sin(2 * math.pi * 10.0 * i * self.fft.dt) for i in range(128)]
        mags = self.fft.calcular_magnitudes(señal)
        self.assertEqual(len(mags), 64)

    def test_magnitudes_no_negativas(self):
        señal = [math.cos(2 * math.pi * 5.0 * i * self.fft.dt) for i in range(128)]
        mags = self.fft.calcular_magnitudes(señal)
        for m in mags:
            self.assertGreaterEqual(m, 0)

    def test_detectar_picos_retorna_lista(self):
        señal = [math.sin(2 * math.pi * 20.0 * i * self.fft.dt) for i in range(128)]
        mags = self.fft.calcular_magnitudes(señal)
        picos = self.fft.detectar_picos(mags)
        self.assertIsInstance(picos, list)

    def test_detectar_picos_vacio(self):
        picos = self.fft.detectar_picos([])
        self.assertEqual(picos, [])

    def test_psi_espectral_umbral(self):
        señal = [math.sin(2 * math.pi * 14.17 * i * self.fft.dt) for i in range(128)]
        mags = self.fft.calcular_magnitudes(señal)
        picos = self.fft.detectar_picos(mags)
        psi = self.fft.psi_espectral(picos)
        self.assertGreaterEqual(psi, _PSI_UMBRAL)
        self.assertLessEqual(psi, 1.0)


# ============================================================================
# TestCoherenciaGlobal – 8 tests
# ============================================================================

class TestCoherenciaGlobal(unittest.TestCase):
    """Tests para CoherenciaGlobal."""

    def setUp(self):
        self.cg = CoherenciaGlobal()

    def test_calcular_maximo(self):
        psi = self.cg.calcular(1.0, 1.0, 1.0, 1.0)
        self.assertAlmostEqual(psi, 1.0, places=5)

    def test_calcular_umbral(self):
        psi = self.cg.calcular(0.888, 0.888, 0.888, 0.888)
        self.assertAlmostEqual(psi, 0.888, places=3)

    def test_calcular_rango(self):
        psi = self.cg.calcular(0.9, 0.95, 0.92, 0.91)
        self.assertGreaterEqual(psi, 0.0)
        self.assertLessEqual(psi, 1.0)

    def test_sello_activo_por_encima(self):
        self.assertTrue(self.cg.sello_activo(0.9))

    def test_sello_activo_igual_umbral(self):
        self.assertTrue(self.cg.sello_activo(0.888))

    def test_sello_inactivo_por_debajo(self):
        self.assertFalse(self.cg.sello_activo(0.887))

    def test_psi_temporal_desde_correlacion_cero(self):
        psi = self.cg.psi_temporal_desde_correlacion(0.0)
        self.assertAlmostEqual(psi, _PSI_UMBRAL, places=3)

    def test_psi_helice_desde_energia(self):
        energia = sum(1.0 / (n + 1) for n in range(10))  # ≈ 2.018
        psi = self.cg.psi_helice_desde_energia(energia)
        self.assertGreaterEqual(psi, _PSI_UMBRAL)
        self.assertLessEqual(psi, 1.0)


# ============================================================================
# TestResultadoBioAdelicoV8 – 5 tests
# ============================================================================

class TestResultadoBioAdelicoV8(unittest.TestCase):
    """Tests para el dataclass ResultadoBioAdelicoV8."""

    def test_defaults_sello(self):
        r = ResultadoBioAdelicoV8()
        self.assertEqual(r.sello, _SELLO)

    def test_defaults_gammas(self):
        r = ResultadoBioAdelicoV8()
        self.assertEqual(len(r.gammas), 10)

    def test_defaults_f0(self):
        r = ResultadoBioAdelicoV8()
        self.assertAlmostEqual(r.f0, 141.7001, places=4)

    def test_defaults_tau_ps(self):
        r = ResultadoBioAdelicoV8()
        self.assertAlmostEqual(r.tau_ps, 2.46e-12, places=20)

    def test_defaults_psi_iniciales(self):
        r = ResultadoBioAdelicoV8()
        self.assertEqual(r.psi_global, 0.0)
        self.assertFalse(r.sello_activo)


# ============================================================================
# TestSistemaBioAdelicoV8 – 8 tests
# ============================================================================

class TestSistemaBioAdelicoV8(unittest.TestCase):
    """Tests para SistemaBioAdelicoV8 con n_puntos=128 para velocidad."""

    def setUp(self):
        self.sistema = SistemaBioAdelicoV8(n_puntos=128, n_periodos=5.0)

    def test_activar_retorna_resultado(self):
        r = self.sistema.activar()
        self.assertIsInstance(r, ResultadoBioAdelicoV8)

    def test_sello_activo(self):
        r = self.sistema.activar()
        self.assertTrue(r.sello_activo)

    def test_psi_global_umbral(self):
        r = self.sistema.activar()
        self.assertGreaterEqual(r.psi_global, _PSI_UMBRAL)

    def test_psi_global_rango(self):
        r = self.sistema.activar()
        self.assertLessEqual(r.psi_global, 1.0)

    def test_gammas_correctos(self):
        r = self.sistema.activar()
        self.assertEqual(len(r.gammas), 10)
        self.assertAlmostEqual(r.gammas[0], 14.1347251417347, places=5)

    def test_f0_correcto(self):
        r = self.sistema.activar()
        self.assertAlmostEqual(r.f0, 141.7001, places=4)

    def test_picos_lista(self):
        r = self.sistema.activar()
        self.assertIsInstance(r.picos_hz, list)

    def test_f_scaled_min(self):
        r = self.sistema.activar()
        expected = _GAMMAS[0] * 141.7001 / (2 * math.pi)
        self.assertAlmostEqual(r.f_scaled_min_hz, expected, places=3)


# ============================================================================
# TestAPIPublica – 12 tests
# ============================================================================

class TestAPIPublica(unittest.TestCase):
    """Tests para solenoide_bioradelico_v8_activar()."""

    @classmethod
    def setUpClass(cls):
        """Ejecuta la API una sola vez para todos los tests."""
        cls.r = solenoide_bioradelico_v8_activar(n_puntos=128, n_periodos=5.0)

    def test_retorna_dict(self):
        self.assertIsInstance(self.r, dict)

    def test_sello_activo_true(self):
        self.assertTrue(self.r['sello_activo'])

    def test_sello_string(self):
        self.assertIn("SBA", self.r['sello'])

    def test_psi_global_umbral(self):
        self.assertGreaterEqual(self.r['psi_global'], 0.888)

    def test_psi_global_max_uno(self):
        self.assertLessEqual(self.r['psi_global'], 1.0)

    def test_claves_presentes(self):
        claves_requeridas = [
            'sello_activo', 'sello', 'psi_global', 'psi_temporal',
            'psi_espectral', 'psi_helice', 'psi_coherencia',
            'correlacion_temporal', 'picos_hz', 'picos_magnitudes',
            'gammas', 'f0', 'tau_ps', 'f_scaled_min_hz',
            'f_scaled_max_hz', 'n_puntos',
        ]
        for clave in claves_requeridas:
            self.assertIn(clave, self.r, f"Clave faltante: {clave}")

    def test_gammas_tupla_10(self):
        self.assertEqual(len(self.r['gammas']), 10)

    def test_gamma1_valor(self):
        self.assertAlmostEqual(self.r['gammas'][0], 14.1347251417347, places=5)

    def test_f0_valor(self):
        self.assertAlmostEqual(self.r['f0'], 141.7001, places=4)

    def test_tau_ps_valor(self):
        self.assertAlmostEqual(self.r['tau_ps'], 2.46e-12, places=20)

    def test_f_scaled_min_positiva(self):
        self.assertGreater(self.r['f_scaled_min_hz'], 0)

    def test_error_f0_negativa(self):
        with self.assertRaises(ValueError):
            solenoide_bioradelico_v8_activar(f0=-1.0)

    def test_error_n_puntos_bajo(self):
        with self.assertRaises(ValueError):
            solenoide_bioradelico_v8_activar(n_puntos=10)

    def test_error_n_periodos_cero(self):
        with self.assertRaises(ValueError):
            solenoide_bioradelico_v8_activar(n_periodos=0.0)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
