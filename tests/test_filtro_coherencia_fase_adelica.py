"""
Tests para physics.filtro_coherencia_fase_adelica — Filtro de Coherencia de
Fase Adélica (FCFA) para la red IRS-Luna a f₀ = 141.7001 Hz.

Cubre:
- Constantes físicas del protocolo
- ParametrosFCFA: validación de parámetros
- KernelRechazoRuido: Paso A (filtro de muesca adaptativo)
- CorreccionDopplerSidereo: corrección de frecuencia orbital
- IntegracionFaseCoherente: STFT + potencia en f₀
- FiltroCoherenciaFaseAdelica: pipeline completo
- API pública: aplicar_filtro_fcfa, estimar_ganancia_snr
"""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.filtro_coherencia_fase_adelica import (
    # Constantes
    V_SEISMICA_LUNAR,
    L_BRAZO_M,
    DELTA_T_SISMICO_S,
    DELTA_T_LUZ_S,
    N_BRAZOS,
    T_ORBITAL_LUNAR_S,
    SNR_CRUDO,
    SNR_FILTRADO_SISMICO,
    SNR_CORRELACION_3_BRAZOS,
    SNR_INTEGRACION_48H,
    T_INTEGRACION_DESCUBRIMIENTO_H,
    UMBRAL_DETECCION_3SIGMA,
    UMBRAL_DESCUBRIMIENTO_5SIGMA,
    # Clases
    ParametrosFCFA,
    ResultadoFCFA,
    KernelRechazoRuido,
    CorreccionDopplerSidereo,
    IntegracionFaseCoherente,
    FiltroCoherenciaFaseAdelica,
    # API pública
    aplicar_filtro_fcfa,
    estimar_ganancia_snr,
)
from qcal.constants import F0_HZ, C


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FS_TEST = 1024.0  # Hz — suficiente para f₀ = 141.7001 Hz
N_SAMPLES = 2048  # 2 s a 1024 Hz


def _generar_senal_f0(n: int = N_SAMPLES, fs: float = FS_TEST, snr: float = 10.0) -> np.ndarray:
    """Genera señal sintética con tono en f₀ y ruido blanco gaussiano."""
    t = np.arange(n) / fs
    señal = np.sin(2 * np.pi * F0_HZ * t)
    ruido = np.random.default_rng(42).standard_normal(n) / snr
    return señal + ruido


def _generar_senal_ruido_puro(n: int = N_SAMPLES) -> np.ndarray:
    """Genera ruido blanco gaussiano puro (sin tono en f₀)."""
    return np.random.default_rng(7).standard_normal(n)


# ===========================================================================
# 1. CONSTANTES FÍSICAS
# ===========================================================================


class TestConstantesFisicas(unittest.TestCase):
    """Verifica los valores de las constantes del protocolo IRS-Luna."""

    def test_velocidad_seismica_lunar(self):
        """v_s lunar debe ser 2000 m/s (≈ 2 km/s)."""
        self.assertAlmostEqual(V_SEISMICA_LUNAR, 2000.0, places=1)

    def test_longitud_brazo(self):
        """Longitud del brazo IRS-Luna debe ser 100 km."""
        self.assertAlmostEqual(L_BRAZO_M, 1.0e5, places=0)

    def test_delta_t_sismico(self):
        """Δt_sísmico = L/v_s ≈ 50 s."""
        esperado = L_BRAZO_M / V_SEISMICA_LUNAR
        self.assertAlmostEqual(DELTA_T_SISMICO_S, esperado, places=6)
        self.assertAlmostEqual(DELTA_T_SISMICO_S, 50.0, places=1)

    def test_delta_t_luz(self):
        """Δt_luz = L/c ≈ 3,34e-4 s (≈ 0,0003 s)."""
        esperado = L_BRAZO_M / C
        self.assertAlmostEqual(DELTA_T_LUZ_S, esperado, places=15)
        self.assertLess(DELTA_T_LUZ_S, 1e-3)
        self.assertGreater(DELTA_T_LUZ_S, 1e-4)

    def test_separacion_temporal_modos(self):
        """El retraso sísmico debe ser mucho mayor que el de luz (>1000×)."""
        ratio = DELTA_T_SISMICO_S / DELTA_T_LUZ_S
        self.assertGreater(ratio, 1000.0)

    def test_n_brazos(self):
        self.assertEqual(N_BRAZOS, 3)

    def test_snr_tabla_progresiva(self):
        """La SNR debe crecer monótonamente a lo largo del pipeline."""
        self.assertLess(SNR_CRUDO, SNR_FILTRADO_SISMICO)
        self.assertLess(SNR_FILTRADO_SISMICO, SNR_CORRELACION_3_BRAZOS)
        self.assertLess(SNR_CORRELACION_3_BRAZOS, SNR_INTEGRACION_48H)

    def test_snr_valores_especificos(self):
        """SNR del protocolo: 0,001 / 0,8 / 15 / 120."""
        self.assertAlmostEqual(SNR_CRUDO, 0.001, places=6)
        self.assertAlmostEqual(SNR_FILTRADO_SISMICO, 0.8, places=6)
        self.assertAlmostEqual(SNR_CORRELACION_3_BRAZOS, 15.0, places=6)
        self.assertAlmostEqual(SNR_INTEGRACION_48H, 120.0, places=6)

    def test_umbral_deteccion(self):
        self.assertAlmostEqual(UMBRAL_DETECCION_3SIGMA, 3.0, places=6)

    def test_umbral_descubrimiento(self):
        self.assertAlmostEqual(UMBRAL_DESCUBRIMIENTO_5SIGMA, 5.0, places=6)

    def test_t_integracion_48h(self):
        self.assertAlmostEqual(T_INTEGRACION_DESCUBRIMIENTO_H, 48.0, places=6)

    def test_f0_parametros_por_defecto_igual_a_qcal(self):
        """ParametrosFCFA debe usar F0_HZ de qcal.constants como valor por defecto."""
        p = ParametrosFCFA()
        self.assertAlmostEqual(p.f0, F0_HZ, places=6)


# ===========================================================================
# 2. ParametrosFCFA
# ===========================================================================


class TestParametrosFCFA(unittest.TestCase):
    """Valida la configuración del filtro."""

    def test_valores_por_defecto(self):
        p = ParametrosFCFA()
        self.assertAlmostEqual(p.f0, F0_HZ, places=6)
        self.assertAlmostEqual(p.fs, 1024.0, places=6)
        self.assertAlmostEqual(p.v_seismica, V_SEISMICA_LUNAR, places=1)
        self.assertAlmostEqual(p.longitud_brazo, L_BRAZO_M, places=0)
        self.assertEqual(p.n_brazos, N_BRAZOS)
        self.assertEqual(p.nperseg, 512)
        self.assertAlmostEqual(p.t_integracion_h, T_INTEGRACION_DESCUBRIMIENTO_H, places=6)

    def test_noverlap_por_defecto(self):
        """noverlap None → se establece a nperseg // 2."""
        p = ParametrosFCFA(nperseg=512, noverlap=None)
        self.assertEqual(p.noverlap, 256)

    def test_noverlap_explicito(self):
        p = ParametrosFCFA(nperseg=512, noverlap=128)
        self.assertEqual(p.noverlap, 128)

    def test_error_f0_negativa(self):
        with self.assertRaises(ValueError):
            ParametrosFCFA(f0=-1.0)

    def test_error_f0_cero(self):
        with self.assertRaises(ValueError):
            ParametrosFCFA(f0=0.0)

    def test_error_fs_negativa(self):
        with self.assertRaises(ValueError):
            ParametrosFCFA(fs=-100.0)

    def test_error_nyquist(self):
        """fs < 2·f₀ debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            ParametrosFCFA(f0=141.7001, fs=200.0)

    def test_error_n_brazos_cero(self):
        with self.assertRaises(ValueError):
            ParametrosFCFA(n_brazos=0)

    def test_error_t_integracion_negativa(self):
        with self.assertRaises(ValueError):
            ParametrosFCFA(t_integracion_h=-1.0)

    def test_configuracion_personalizada(self):
        p = ParametrosFCFA(fs=4096.0, n_brazos=7, t_integracion_h=24.0)
        self.assertAlmostEqual(p.fs, 4096.0, places=6)
        self.assertEqual(p.n_brazos, 7)
        self.assertAlmostEqual(p.t_integracion_h, 24.0, places=6)


# ===========================================================================
# 3. KernelRechazoRuido
# ===========================================================================


class TestKernelRechazoRuido(unittest.TestCase):
    """Valida el Paso A: kernel de rechazo de ruido sísmico."""

    def setUp(self):
        self.params = ParametrosFCFA(fs=FS_TEST)
        self.kernel = KernelRechazoRuido(self.params)
        np.random.seed(0)

    def test_construccion(self):
        self.assertAlmostEqual(
            self.kernel._delta_t_sismico,
            L_BRAZO_M / V_SEISMICA_LUNAR,
            places=6,
        )
        self.assertAlmostEqual(
            self.kernel._delta_t_luz,
            L_BRAZO_M / C,
            places=15,
        )

    def test_aplicar_conserva_longitud(self):
        """La señal filtrada debe tener la misma longitud que la de entrada."""
        senal = _generar_senal_f0()
        limpia = self.kernel.aplicar(senal)
        self.assertEqual(len(limpia), len(senal))

    def test_aplicar_devuelve_ndarray(self):
        senal = _generar_senal_f0()
        limpia = self.kernel.aplicar(senal)
        self.assertIsInstance(limpia, np.ndarray)

    def test_aplicar_senal_vacia_lanza_error(self):
        with self.assertRaises(ValueError):
            self.kernel.aplicar(np.array([]))

    def test_estimar_espectro_longitudes(self):
        """PSD de salida debe tener N//2+1 componentes."""
        senal = _generar_senal_f0()
        s_moon, s_total = self.kernel.estimar_espectro_sismico(senal)
        esperado = len(senal) // 2 + 1
        self.assertEqual(len(s_moon), esperado)
        self.assertEqual(len(s_total), esperado)

    def test_s_total_no_negativa(self):
        senal = _generar_senal_f0()
        _, s_total = self.kernel.estimar_espectro_sismico(senal)
        self.assertTrue(np.all(s_total >= 0.0))

    def test_s_moon_entre_0_y_s_total(self):
        senal = _generar_senal_f0()
        s_moon, s_total = self.kernel.estimar_espectro_sismico(senal)
        self.assertTrue(np.all(s_moon >= 0.0))
        # s_moon no debe exceder s_total en ningún bin
        self.assertTrue(np.all(s_moon <= s_total + 1e-12))

    def test_senal_dc_pasa_sin_distorsion_severa(self):
        """Una señal DC no debe ser aniquilada por el filtro."""
        senal_dc = np.ones(N_SAMPLES)
        limpia = self.kernel.aplicar(senal_dc)
        # La media de la señal limpiada debe ser positiva y razonable
        self.assertGreater(np.mean(np.abs(limpia)), 0.0)

    def test_aplicar_tonos_distintos_de_f0(self):
        """El kernel no debe amplificar la señal más allá de la energía de entrada."""
        senal = _generar_senal_f0()
        limpia = self.kernel.aplicar(senal)
        energia_in = np.sum(senal ** 2)
        energia_out = np.sum(limpia ** 2)
        self.assertLessEqual(energia_out, energia_in * 1.1)  # tolerancia 10%


# ===========================================================================
# 4. CorreccionDopplerSidereo
# ===========================================================================


class TestCorreccionDopplerSidereo(unittest.TestCase):
    """Valida el modelo de corrección Doppler por movimiento orbital de la Luna."""

    def setUp(self):
        self.doppler = CorreccionDopplerSidereo(f0=F0_HZ)

    def test_construccion_f0(self):
        self.assertAlmostEqual(self.doppler.f0, F0_HZ, places=6)

    def test_error_f0_negativa(self):
        with self.assertRaises(ValueError):
            CorreccionDopplerSidereo(f0=-141.0)

    def test_velocidad_proyectada_escalar(self):
        """v_proj en t=0 debe ser ≈ +V_ORBITAL_LUNA."""
        v = self.doppler.velocidad_proyectada(np.array([0.0]))
        self.assertAlmostEqual(v[0], CorreccionDopplerSidereo.V_ORBITAL_LUNA, places=1)

    def test_velocidad_proyectada_amplitud(self):
        """La amplitud de v_proj no debe superar V_ORBITAL_LUNA."""
        t = np.linspace(0, T_ORBITAL_LUNAR_S, 1000)
        v = self.doppler.velocidad_proyectada(t)
        self.assertLessEqual(np.max(np.abs(v)), CorreccionDopplerSidereo.V_ORBITAL_LUNA + 1.0)

    def test_frecuencia_objetivo_cerca_de_f0(self):
        """f_target debe estar muy próxima a f₀ (desviación Doppler ≪ 1 Hz)."""
        t = np.linspace(0, 1000, 100)
        f_target = self.doppler.frecuencia_objetivo(t)
        desviacion_max = np.max(np.abs(f_target - F0_HZ))
        # v_Luna ≈ 1022 m/s → Δf = f₀ · v/c ≈ 141.7 × 1022/3e8 ≈ 4.8e-4 Hz
        self.assertLess(desviacion_max, 0.01)

    def test_frecuencia_objetivo_simetria(self):
        """La media temporal de f_target debe ser ≈ f₀ (movimiento circular)."""
        t = np.linspace(0, T_ORBITAL_LUNAR_S, 10000)
        f_target = self.doppler.frecuencia_objetivo(t)
        self.assertAlmostEqual(np.mean(f_target), F0_HZ, places=3)

    def test_frecuencia_objetivo_es_ndarray(self):
        t = np.array([0.0, 1.0, 2.0])
        f = self.doppler.frecuencia_objetivo(t)
        self.assertIsInstance(f, np.ndarray)
        self.assertEqual(len(f), 3)

    def test_v_orbital_luna_positiva(self):
        self.assertGreater(CorreccionDopplerSidereo.V_ORBITAL_LUNA, 0.0)


# ===========================================================================
# 5. IntegracionFaseCoherente
# ===========================================================================


class TestIntegracionFaseCoherente(unittest.TestCase):
    """Valida el Paso B: STFT con compensación Doppler."""

    def setUp(self):
        self.params = ParametrosFCFA(fs=FS_TEST, nperseg=256, noverlap=128)
        self.stft_int = IntegracionFaseCoherente(self.params)

    def test_construccion(self):
        self.assertIsInstance(self.stft_int.doppler, CorreccionDopplerSidereo)

    def test_calcular_devuelve_cuatro_elementos(self):
        senal = _generar_senal_f0(fs=FS_TEST)
        resultado = self.stft_int.calcular(senal)
        self.assertEqual(len(resultado), 4)

    def test_freqs_stft_positivas(self):
        senal = _generar_senal_f0(fs=FS_TEST)
        freqs, t_stft, f_doppler, potencia = self.stft_int.calcular(senal)
        self.assertTrue(np.all(freqs >= 0.0))

    def test_f_doppler_cercana_a_f0(self):
        senal = _generar_senal_f0(fs=FS_TEST)
        _, _, f_doppler, _ = self.stft_int.calcular(senal)
        desviacion = np.max(np.abs(f_doppler - F0_HZ))
        self.assertLess(desviacion, 0.01)

    def test_potencia_f0_positiva(self):
        senal = _generar_senal_f0(fs=FS_TEST, snr=5.0)
        _, _, _, potencia = self.stft_int.calcular(senal)
        self.assertGreater(potencia, 0.0)

    def test_potencia_mayor_con_tono(self):
        """Señal con tono en f₀ debe tener más potencia que ruido puro."""
        senal_f0 = _generar_senal_f0(fs=FS_TEST, snr=20.0)
        senal_ruido = _generar_senal_ruido_puro()
        _, _, _, p_f0 = self.stft_int.calcular(senal_f0)
        _, _, _, p_ruido = self.stft_int.calcular(senal_ruido)
        self.assertGreater(p_f0, p_ruido)

    def test_t_stft_monotona(self):
        senal = _generar_senal_f0(fs=FS_TEST)
        _, t_stft, _, _ = self.stft_int.calcular(senal)
        self.assertTrue(np.all(np.diff(t_stft) > 0))

    def test_t_offset_desplaza_tiempos(self):
        senal = _generar_senal_f0(fs=FS_TEST)
        _, t0, _, _ = self.stft_int.calcular(senal, t_offset=0.0)
        _, t1, _, _ = self.stft_int.calcular(senal, t_offset=100.0)
        np.testing.assert_allclose(t1 - t0, 100.0, atol=1e-10)


# ===========================================================================
# 6. FiltroCoherenciaFaseAdelica
# ===========================================================================


class TestFiltroCoherenciaFaseAdelica(unittest.TestCase):
    """Valida el pipeline completo del FCFA."""

    def setUp(self):
        self.params = ParametrosFCFA(fs=FS_TEST, nperseg=256, n_brazos=3, t_integracion_h=48.0)
        self.fcfa = FiltroCoherenciaFaseAdelica(self.params)

    def test_construccion_por_defecto(self):
        fcfa = FiltroCoherenciaFaseAdelica()
        self.assertIsInstance(fcfa.params, ParametrosFCFA)

    def test_procesar_devuelve_resultado_fcfa(self):
        senal = _generar_senal_f0()
        res = self.fcfa.procesar(senal)
        self.assertIsInstance(res, ResultadoFCFA)

    def test_resultado_fs(self):
        senal = _generar_senal_f0()
        res = self.fcfa.procesar(senal)
        self.assertAlmostEqual(res.fs, FS_TEST, places=6)

    def test_senal_limpia_misma_longitud(self):
        senal = _generar_senal_f0()
        res = self.fcfa.procesar(senal)
        self.assertEqual(len(res.senal_limpia), len(senal))

    def test_f_doppler_no_vacio(self):
        senal = _generar_senal_f0()
        res = self.fcfa.procesar(senal)
        self.assertGreater(len(res.f_doppler), 0)

    def test_potencia_f0_no_negativa(self):
        senal = _generar_senal_f0()
        res = self.fcfa.procesar(senal)
        self.assertGreaterEqual(res.potencia_f0, 0.0)

    def test_snr_estimada_positiva(self):
        senal = _generar_senal_f0()
        res = self.fcfa.procesar(senal)
        self.assertGreater(res.snr_estimada, 0.0)

    def test_etapa_deteccion_string(self):
        senal = _generar_senal_f0()
        res = self.fcfa.procesar(senal)
        self.assertIsInstance(res.etapa_deteccion, str)
        self.assertGreater(len(res.etapa_deteccion), 0)

    def test_senal_vacia_lanza_error(self):
        with self.assertRaises(ValueError):
            self.fcfa.procesar(np.array([]))

    def test_t_stft_es_ndarray(self):
        senal = _generar_senal_f0()
        res = self.fcfa.procesar(senal)
        self.assertIsInstance(res.t_stft, np.ndarray)

    def test_clasificar_etapa_descubrimiento(self):
        etapa = FiltroCoherenciaFaseAdelica._clasificar_etapa(SNR_INTEGRACION_48H)
        self.assertIn("Descubrimiento", etapa)

    def test_clasificar_etapa_deteccion_clara(self):
        etapa = FiltroCoherenciaFaseAdelica._clasificar_etapa(SNR_CORRELACION_3_BRAZOS)
        self.assertIn("Detección Clara", etapa)

    def test_clasificar_etapa_emergencia(self):
        etapa = FiltroCoherenciaFaseAdelica._clasificar_etapa(SNR_FILTRADO_SISMICO)
        self.assertIn("Emergencia", etapa)

    def test_clasificar_etapa_enterrada(self):
        etapa = FiltroCoherenciaFaseAdelica._clasificar_etapa(SNR_CRUDO)
        self.assertIn("enterrada", etapa)

    def test_snr_crece_con_mas_brazos(self):
        """Mayor número de brazos → mayor SNR estimada."""
        senal = _generar_senal_f0()

        params_3 = ParametrosFCFA(fs=FS_TEST, nperseg=256, n_brazos=3, t_integracion_h=48.0)
        params_7 = ParametrosFCFA(fs=FS_TEST, nperseg=256, n_brazos=7, t_integracion_h=48.0)
        res_3 = FiltroCoherenciaFaseAdelica(params_3).procesar(senal)
        res_7 = FiltroCoherenciaFaseAdelica(params_7).procesar(senal)
        self.assertGreater(res_7.snr_estimada, res_3.snr_estimada)

    def test_snr_crece_con_mas_integracion(self):
        """Mayor tiempo de integración → mayor SNR estimada."""
        senal = _generar_senal_f0()

        params_24h = ParametrosFCFA(fs=FS_TEST, nperseg=256, n_brazos=3, t_integracion_h=24.0)
        params_48h = ParametrosFCFA(fs=FS_TEST, nperseg=256, n_brazos=3, t_integracion_h=48.0)
        res_24 = FiltroCoherenciaFaseAdelica(params_24h).procesar(senal)
        res_48 = FiltroCoherenciaFaseAdelica(params_48h).procesar(senal)
        self.assertGreater(res_48.snr_estimada, res_24.snr_estimada)


# ===========================================================================
# 7. API PÚBLICA
# ===========================================================================


class TestAplicarFiltroFCFA(unittest.TestCase):
    """Valida la función de conveniencia aplicar_filtro_fcfa."""

    def test_retorna_resultado_fcfa(self):
        senal = _generar_senal_f0()
        res = aplicar_filtro_fcfa(senal, fs=FS_TEST)
        self.assertIsInstance(res, ResultadoFCFA)

    def test_n_brazos_default(self):
        senal = _generar_senal_f0()
        res = aplicar_filtro_fcfa(senal, fs=FS_TEST)
        self.assertGreater(res.snr_estimada, 0.0)

    def test_n_brazos_personalizado(self):
        senal = _generar_senal_f0()
        res_3 = aplicar_filtro_fcfa(senal, fs=FS_TEST, n_brazos=3)
        res_7 = aplicar_filtro_fcfa(senal, fs=FS_TEST, n_brazos=7)
        self.assertGreater(res_7.snr_estimada, res_3.snr_estimada)

    def test_t_offset_funciona(self):
        senal = _generar_senal_f0()
        res = aplicar_filtro_fcfa(senal, fs=FS_TEST, t_offset=1000.0)
        self.assertIsInstance(res, ResultadoFCFA)

    def test_resultado_consistente_con_senal_repetida(self):
        """La misma señal con los mismos parámetros debe dar el mismo resultado."""
        senal = _generar_senal_f0()
        res1 = aplicar_filtro_fcfa(senal, fs=FS_TEST, n_brazos=3, t_integracion_h=48.0)
        res2 = aplicar_filtro_fcfa(senal, fs=FS_TEST, n_brazos=3, t_integracion_h=48.0)
        np.testing.assert_allclose(res1.senal_limpia, res2.senal_limpia)
        self.assertAlmostEqual(res1.snr_estimada, res2.snr_estimada, places=10)


class TestEstimarGananciaSNR(unittest.TestCase):
    """Valida la función estimar_ganancia_snr."""

    def test_retorna_dict_con_claves(self):
        resultado = estimar_ganancia_snr()
        self.assertIn("crudo", resultado)
        self.assertIn("filtrado_sismico", resultado)
        self.assertIn("correlacion_brazos", resultado)
        self.assertIn("integracion_final", resultado)

    def test_snr_crudo(self):
        resultado = estimar_ganancia_snr()
        self.assertAlmostEqual(resultado["crudo"], SNR_CRUDO, places=6)

    def test_snr_filtrado_sismico(self):
        resultado = estimar_ganancia_snr()
        self.assertAlmostEqual(resultado["filtrado_sismico"], SNR_FILTRADO_SISMICO, places=6)

    def test_snr_progresiva(self):
        """Las etapas deben ser monótonamente crecientes."""
        r = estimar_ganancia_snr(n_brazos=3, t_integracion_h=48.0)
        self.assertLess(r["crudo"], r["filtrado_sismico"])
        self.assertLess(r["filtrado_sismico"], r["correlacion_brazos"])
        self.assertLess(r["correlacion_brazos"], r["integracion_final"])

    def test_mas_brazos_mas_snr_correlacion(self):
        r3 = estimar_ganancia_snr(n_brazos=3)
        r7 = estimar_ganancia_snr(n_brazos=7)
        self.assertGreater(r7["correlacion_brazos"], r3["correlacion_brazos"])

    def test_mas_integracion_mas_snr_final(self):
        r24 = estimar_ganancia_snr(t_integracion_h=24.0)
        r48 = estimar_ganancia_snr(t_integracion_h=48.0)
        self.assertGreater(r48["integracion_final"], r24["integracion_final"])

    def test_error_n_brazos_cero(self):
        with self.assertRaises(ValueError):
            estimar_ganancia_snr(n_brazos=0)

    def test_error_t_integracion_negativa(self):
        with self.assertRaises(ValueError):
            estimar_ganancia_snr(t_integracion_h=-1.0)

    def test_snr_integracion_48h_3_brazos(self):
        """Con parámetros de referencia, la SNR final debe coincidir con SNR_INTEGRACION_48H."""
        r = estimar_ganancia_snr(n_brazos=3, t_integracion_h=48.0)
        self.assertAlmostEqual(r["integracion_final"], SNR_INTEGRACION_48H, places=6)

    def test_snr_correlacion_3_brazos_referencia(self):
        """Con 3 brazos, la SNR de correlación debe coincidir con SNR_CORRELACION_3_BRAZOS."""
        r = estimar_ganancia_snr(n_brazos=3, t_integracion_h=48.0)
        self.assertAlmostEqual(r["correlacion_brazos"], SNR_CORRELACION_3_BRAZOS, places=6)

    def test_todos_los_valores_positivos(self):
        r = estimar_ganancia_snr()
        for k, v in r.items():
            self.assertGreater(v, 0.0, msg=f"SNR '{k}' debe ser positiva")


# ===========================================================================
# 8. INTEGRACIÓN: Pipeline completo con señal sintética
# ===========================================================================


class TestPipelineCompleto(unittest.TestCase):
    """Test de integración del pipeline FCFA completo."""

    def test_pipeline_extremo_a_extremo(self):
        """
        El pipeline completo debe:
        1. Aceptar una señal cruda con tono en f₀.
        2. Producir una señal limpia de la misma longitud.
        3. Devolver una SNR estimada positiva.
        4. Devolver una etapa de detección no vacía.
        """
        np.random.seed(42)
        n = 4096
        fs = 1024.0
        t = np.arange(n) / fs
        # Señal: tono en f₀ + ruido blanco moderado
        senal = np.sin(2 * np.pi * F0_HZ * t) + 0.5 * np.random.randn(n)

        res = aplicar_filtro_fcfa(senal, fs=fs, n_brazos=3, t_integracion_h=48.0)

        self.assertEqual(len(res.senal_limpia), n)
        self.assertGreater(res.snr_estimada, 0.0)
        self.assertIsInstance(res.etapa_deteccion, str)
        self.assertGreater(len(res.f_doppler), 0)

    def test_pipeline_con_ruido_puro(self):
        """El filtro no debe fallar con señal de sólo ruido."""
        senal = np.random.default_rng(99).standard_normal(N_SAMPLES)
        res = aplicar_filtro_fcfa(senal, fs=FS_TEST)
        self.assertEqual(len(res.senal_limpia), N_SAMPLES)
        self.assertGreaterEqual(res.potencia_f0, 0.0)

    def test_tabla_snr_ganancias_referenciales(self):
        """Los valores nominales del protocolo deben cumplirse con parámetros estándar."""
        r = estimar_ganancia_snr(n_brazos=3, t_integracion_h=48.0)
        self.assertAlmostEqual(r["crudo"], 0.001, places=4)
        self.assertAlmostEqual(r["filtrado_sismico"], 0.8, places=4)
        self.assertAlmostEqual(r["correlacion_brazos"], 15.0, places=4)
        self.assertAlmostEqual(r["integracion_final"], 120.0, places=4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
