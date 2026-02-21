#!/usr/bin/env python3
"""
Tests para el Experimento del Coliseo Estadístico: SNR vs Ψ Noética
===================================================================

Valida la implementación del experimento que compara el SNR estándar de
potencia contra la métrica Ψ Noética de coherencia cruzada bajo f₀ = 141.7001 Hz.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import os
import importlib.util
import unittest
import numpy as np

# Cargar explícitamente el módulo snr_vs_psi_comparison desde scripts sin modificar sys.path
_scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
_module_path = os.path.join(_scripts_dir, 'snr_vs_psi_comparison.py')
_spec = importlib.util.spec_from_file_location('snr_vs_psi_comparison', _module_path)
snr_vs_psi_comparison = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(snr_vs_psi_comparison)

F0 = snr_vs_psi_comparison.F0
SAMPLE_RATE = snr_vs_psi_comparison.SAMPLE_RATE
generar_senal_decayente = snr_vs_psi_comparison.generar_senal_decayente
generar_ruido_coloreado = snr_vs_psi_comparison.generar_ruido_coloreado
calcular_snr_potencia = snr_vs_psi_comparison.calcular_snr_potencia
calcular_psi_noetica = snr_vs_psi_comparison.calcular_psi_noetica
calcular_curva_roc = snr_vs_psi_comparison.calcular_curva_roc
calcular_separacion_sigma = snr_vs_psi_comparison.calcular_separacion_sigma
ejecutar_zona = snr_vs_psi_comparison.ejecutar_zona
ejecutar_coliseo = snr_vs_psi_comparison.ejecutar_coliseo
tabla_comparativa = snr_vs_psi_comparison.tabla_comparativa
ResultadoROC = snr_vs_psi_comparison.ResultadoROC
ResultadoZona = snr_vs_psi_comparison.ResultadoZona
_coherencia_welch = snr_vs_psi_comparison._coherencia_welch


class TestConstantesYSenal(unittest.TestCase):
    """Tests para constantes globales y generación de señal."""

    def test_f0_valor(self):
        """F0 debe ser 141.7001 Hz."""
        self.assertAlmostEqual(F0, 141.7001, places=4)

    def test_sample_rate_valor(self):
        """SAMPLE_RATE debe ser 4096 Hz."""
        self.assertEqual(SAMPLE_RATE, 4096.0)

    def test_senal_decayente_longitud(self):
        """La señal debe tener la longitud correcta."""
        s = generar_senal_decayente(1.0, duration=1.0, fs=100.0, f0=F0)
        self.assertEqual(len(s), 100)

    def test_senal_decayente_amplitud_inicial(self):
        """La amplitud inicial de la señal debe ser aproximadamente la indicada."""
        amplitud = 2.0
        s = generar_senal_decayente(amplitud, duration=0.5, fs=SAMPLE_RATE, f0=F0)
        # El primer elemento es amplitud * exp(0) * cos(0) = amplitud
        self.assertAlmostEqual(s[0], amplitud, places=1)

    def test_senal_decayente_monotona(self):
        """La envolvente de la señal debe ser decreciente."""
        s = generar_senal_decayente(1.0, duration=1.0, fs=100.0, f0=F0, tau_decay=0.3)
        N = len(s)
        # Comparar envolventes en cuartos del segmento
        e1 = np.max(np.abs(s[:N // 4]))
        e4 = np.max(np.abs(s[3 * N // 4:]))
        self.assertGreater(e1, e4, "La envolvente debe decrecer con el tiempo")

    def test_senal_decayente_frecuencia(self):
        """La señal debe tener energía concentrada alrededor de f0."""
        fs = SAMPLE_RATE
        s = generar_senal_decayente(1.0, duration=1.0, fs=fs, f0=F0)
        freqs = np.fft.rfftfreq(len(s), 1.0 / fs)
        psd = np.abs(np.fft.rfft(s)) ** 2
        idx_pico = np.argmax(psd)
        self.assertAlmostEqual(freqs[idx_pico], F0, delta=2.0,
                               msg="El pico espectral debe estar en f0")


class TestRuido(unittest.TestCase):
    """Tests para la generación de ruido coloreado."""

    def setUp(self):
        self.rng = np.random.default_rng(42)
        self.N = 4096

    def test_ruido_blanco_varianza(self):
        """El ruido blanco debe tener varianza ~1."""
        r = generar_ruido_coloreado(self.N, color='white', rng=self.rng)
        self.assertAlmostEqual(np.std(r), 1.0, delta=0.1)

    def test_ruido_rosa_varianza(self):
        """El ruido rosa debe tener varianza normalizada a ~1."""
        r = generar_ruido_coloreado(self.N, color='pink', rng=self.rng)
        self.assertAlmostEqual(np.std(r), 1.0, delta=0.1)

    def test_ruido_marron_varianza(self):
        """El ruido marrón debe tener varianza normalizada a ~1."""
        r = generar_ruido_coloreado(self.N, color='brown', rng=self.rng)
        self.assertAlmostEqual(np.std(r), 1.0, delta=0.1)

    def test_ruido_color_invalido(self):
        """Un color inválido debe lanzar ValueError."""
        with self.assertRaises(ValueError):
            generar_ruido_coloreado(self.N, color='verde', rng=self.rng)

    def test_ruido_reproducible(self):
        """El ruido debe ser reproducible con la misma semilla."""
        r1 = generar_ruido_coloreado(self.N, color='pink',
                                     rng=np.random.default_rng(99))
        r2 = generar_ruido_coloreado(self.N, color='pink',
                                     rng=np.random.default_rng(99))
        np.testing.assert_array_equal(r1, r2)

    def test_canales_independientes(self):
        """Dos realizaciones con diferente semilla deben ser distintas."""
        r1 = generar_ruido_coloreado(self.N, rng=np.random.default_rng(1))
        r2 = generar_ruido_coloreado(self.N, rng=np.random.default_rng(2))
        self.assertFalse(np.allclose(r1, r2),
                         "Dos semillas distintas deben producir ruido distinto")


class TestSNRPotencia(unittest.TestCase):
    """Tests para el cálculo del SNR estándar de potencia."""

    def setUp(self):
        self.fs = SAMPLE_RATE
        self.duration = 0.5
        self.N = int(self.duration * self.fs)

    def test_snr_positivo(self):
        """El SNR debe ser no-negativo."""
        rng = np.random.default_rng(0)
        x = generar_ruido_coloreado(self.N, rng=rng)
        snr = calcular_snr_potencia(x, f0=F0, fs=self.fs)
        self.assertGreaterEqual(snr, 0.0)

    def test_snr_mayor_con_senal(self):
        """El SNR debe ser mayor cuando hay señal que cuando no la hay."""
        rng = np.random.default_rng(7)
        ruido = generar_ruido_coloreado(self.N, rng=rng)
        senal = generar_senal_decayente(5.0, duration=self.duration,
                                        fs=self.fs, f0=F0)
        snr_con = calcular_snr_potencia(ruido + senal, f0=F0, fs=self.fs)
        snr_sin = calcular_snr_potencia(ruido, f0=F0, fs=self.fs)
        self.assertGreater(snr_con, snr_sin,
                           "SNR con señal fuerte debe superar SNR sin señal")

    def test_snr_crece_con_amplitud(self):
        """El SNR debe crecer al aumentar la amplitud de la señal."""
        rng = np.random.default_rng(11)
        ruido = generar_ruido_coloreado(self.N, rng=rng)
        snrs = []
        for amp in [0.5, 2.0, 10.0]:
            s = generar_senal_decayente(amp, duration=self.duration,
                                        fs=self.fs, f0=F0)
            snrs.append(calcular_snr_potencia(ruido + s, f0=F0, fs=self.fs))
        self.assertLess(snrs[0], snrs[1])
        self.assertLess(snrs[1], snrs[2])


class TestPsiNoetica(unittest.TestCase):
    """Tests para el cálculo de la métrica Ψ Noética."""

    def setUp(self):
        self.fs = SAMPLE_RATE
        self.duration = 0.5
        self.N = int(self.duration * self.fs)

    def test_psi_positiva(self):
        """Ψ debe ser no-negativa."""
        rng_a = np.random.default_rng(20)
        rng_b = np.random.default_rng(21)
        x = generar_ruido_coloreado(self.N, rng=rng_a)
        y = generar_ruido_coloreado(self.N, rng=rng_b)
        psi = calcular_psi_noetica(x, y, f0=F0, fs=self.fs)
        self.assertGreaterEqual(psi, 0.0)

    def test_psi_mayor_con_senal_coherente(self):
        """Ψ debe ser mayor cuando ambos canales comparten una señal coherente."""
        rng_a = np.random.default_rng(30)
        rng_b = np.random.default_rng(31)
        ruido_a = generar_ruido_coloreado(self.N, rng=rng_a)
        ruido_b = generar_ruido_coloreado(self.N, rng=rng_b)
        senal = generar_senal_decayente(3.0, duration=self.duration,
                                        fs=self.fs, f0=F0)

        psi_con = calcular_psi_noetica(senal + ruido_a, senal + ruido_b,
                                       f0=F0, fs=self.fs)
        psi_sin = calcular_psi_noetica(ruido_a, ruido_b, f0=F0, fs=self.fs)
        self.assertGreater(psi_con, psi_sin,
                           "Ψ debe ser mayor con señal coherente compartida")

    def test_psi_acotada(self):
        """Ψ debe ser un valor finito."""
        rng_a = np.random.default_rng(40)
        rng_b = np.random.default_rng(41)
        senal = generar_senal_decayente(1.0, duration=self.duration,
                                        fs=self.fs, f0=F0)
        x = senal + generar_ruido_coloreado(self.N, rng=rng_a)
        y = senal + generar_ruido_coloreado(self.N, rng=rng_b)
        psi = calcular_psi_noetica(x, y, f0=F0, fs=self.fs)
        self.assertTrue(np.isfinite(psi), "Ψ debe ser finita")


class TestCurvaROC(unittest.TestCase):
    """Tests para el cálculo de curvas ROC."""

    def setUp(self):
        rng = np.random.default_rng(50)
        # Generar puntuaciones con separación clara
        self.scores_signal = rng.normal(3.0, 1.0, 100)
        self.scores_noise = rng.normal(1.0, 1.0, 100)

    def test_roc_auc_rango(self):
        """El AUC debe estar en [0, 1]."""
        roc = calcular_curva_roc(self.scores_signal, self.scores_noise)
        self.assertGreaterEqual(roc.auc, 0.0)
        self.assertLessEqual(roc.auc, 1.0)

    def test_roc_auc_bueno_cuando_separacion_grande(self):
        """Con señales bien separadas el AUC debe superar 0.8."""
        roc = calcular_curva_roc(self.scores_signal, self.scores_noise)
        self.assertGreater(roc.auc, 0.8,
                           "AUC debe ser alto con señales bien separadas")

    def test_roc_auc_chance_sin_separacion(self):
        """Sin separación el AUC debe ser cercano a 0.5."""
        rng = np.random.default_rng(55)
        iguales = rng.normal(0.0, 1.0, 200)
        roc = calcular_curva_roc(iguales[:100], iguales[100:])
        self.assertAlmostEqual(roc.auc, 0.5, delta=0.15,
                               msg="AUC debe ser ~0.5 sin separación")

    def test_roc_longitudes_tpr_fpr(self):
        """TPR y FPR deben tener la misma longitud."""
        roc = calcular_curva_roc(self.scores_signal, self.scores_noise)
        self.assertEqual(len(roc.tpr), len(roc.fpr))

    def test_roc_nombre(self):
        """El nombre del ROC debe conservarse."""
        roc = calcular_curva_roc(self.scores_signal, self.scores_noise,
                                 nombre='test_nombre')
        self.assertEqual(roc.nombre, 'test_nombre')


class TestEjecutarZona(unittest.TestCase):
    """Tests para la ejecución del experimento por zona."""

    def setUp(self):
        # Usar n_trials=20 y duration corta para velocidad en tests
        self.kwargs = dict(n_trials=20, duration=0.2, seed=42)

    def test_zona_confort_retorna_resultadozona(self):
        """El resultado debe ser un objeto ResultadoZona."""
        res = ejecutar_zona(15.0, 'Confort', **self.kwargs)
        self.assertIsInstance(res, ResultadoZona)

    def test_zona_tiene_roc(self):
        """El resultado debe incluir curvas ROC para ambas métricas."""
        res = ejecutar_zona(5.0, 'Penumbra', **self.kwargs)
        self.assertIsNotNone(res.roc_snr)
        self.assertIsNotNone(res.roc_psi)
        self.assertIsInstance(res.roc_snr, ResultadoROC)
        self.assertIsInstance(res.roc_psi, ResultadoROC)

    def test_zona_scores_longitud(self):
        """Los arrays de puntuaciones deben tener longitud n_trials."""
        n = 20
        res = ejecutar_zona(3.0, 'Test', n_trials=n, duration=0.2, seed=0)
        self.assertEqual(len(res.snr_scores_senal), n)
        self.assertEqual(len(res.psi_scores_senal), n)
        self.assertEqual(len(res.snr_scores_ruido), n)
        self.assertEqual(len(res.psi_scores_ruido), n)
        self.assertEqual(len(res.psi_ratio_senal), n)
        self.assertEqual(len(res.psi_ratio_ruido), n)

    def test_zona_ratio_positivo(self):
        """Los ratios anti-bias Ψ(f₀)/Ψ(f_control) deben ser positivos."""
        res = ejecutar_zona(5.0, 'Test', n_trials=10, duration=0.2, seed=1)
        self.assertTrue(np.all(res.psi_ratio_senal > 0),
                        "ratios señal deben ser positivos")
        self.assertTrue(np.all(res.psi_ratio_ruido > 0),
                        "ratios ruido deben ser positivos")

    def test_zona_separacion_finita(self):
        """Las separaciones estadísticas deben ser valores finitos."""
        res = ejecutar_zona(5.0, 'Test', **self.kwargs)
        self.assertTrue(np.isfinite(res.separacion_snr_sigma))
        self.assertTrue(np.isfinite(res.separacion_psi_sigma))


class TestColiseoCompleto(unittest.TestCase):
    """Tests de integración para el Coliseo Estadístico completo."""

    @classmethod
    def setUpClass(cls):
        """Ejecutar el experimento completo una sola vez para todos los tests."""
        cls.resultados = ejecutar_coliseo(n_trials=50, duration=0.2, seed=42)

    def test_tres_zonas(self):
        """El experimento debe producir resultados para las tres zonas."""
        self.assertIn('Confort', self.resultados)
        self.assertIn('Penumbra', self.resultados)
        self.assertIn('Noetica', self.resultados)

    def test_zona_confort_auc_excelente(self):
        """En la Zona de Confort, ambas métricas deben tener AUC > 0.9."""
        res = self.resultados['Confort']
        self.assertGreater(res.roc_snr.auc, 0.9,
                           "SNR debe ser excelente en Zona de Confort")
        self.assertGreater(res.roc_psi.auc, 0.9,
                           "Ψ debe ser excelente en Zona de Confort")

    def test_zona_noetica_psi_supera_2sigma(self):
        """En la Zona Noética, Ψ debe mantener ≥ 2σ de separación estadística."""
        res = self.resultados['Noetica']
        self.assertGreaterEqual(
            res.separacion_psi_sigma, 2.0,
            f"Ψ debe mantener ≥ 2σ en Zona Noética (got {res.separacion_psi_sigma:.2f}σ)"
        )

    def test_zona_noetica_psi_auc_mayor_que_snr(self):
        """En la Zona Noética, Ψ debe tener mayor AUC que SNR estándar."""
        res = self.resultados['Noetica']
        self.assertGreater(
            res.roc_psi.auc, res.roc_snr.auc,
            "Ψ debe superar a SNR en AUC en la Zona Noética"
        )

    def test_zona_penumbra_psi_sep_mayor_que_snr(self):
        """En la Zona de Penumbra, Ψ debe tener mayor separación estadística."""
        res = self.resultados['Penumbra']
        self.assertGreater(
            res.separacion_psi_sigma, res.separacion_snr_sigma,
            "Ψ debe tener mayor separación estadística que SNR en Zona de Penumbra"
        )

    def test_tabla_comparativa_formato(self):
        """La tabla comparativa debe generarse sin errores."""
        tabla = tabla_comparativa(self.resultados)
        self.assertIsInstance(tabla, str)
        self.assertIn('COLISEO', tabla)
        self.assertIn(str(F0), tabla)
        self.assertIn('Confort', tabla)
        self.assertIn('Penumbra', tabla)
        self.assertIn('Noetica', tabla)

    def test_reproducibilidad(self):
        """El experimento debe ser reproducible con la misma semilla."""
        res1 = ejecutar_coliseo(n_trials=10, duration=0.2, seed=99)
        res2 = ejecutar_coliseo(n_trials=10, duration=0.2, seed=99)
        np.testing.assert_array_almost_equal(
            res1['Noetica'].snr_scores_senal,
            res2['Noetica'].snr_scores_senal,
            err_msg="Los resultados deben ser reproducibles con la misma semilla"
        )


class TestSeparacionSigma(unittest.TestCase):
    """Tests para la función oficial calcular_separacion_sigma."""

    def test_separacion_cero_distribuciones_iguales(self):
        """Con distribuciones idénticas la separación debe ser cero."""
        rng = np.random.default_rng(60)
        datos = rng.normal(0.0, 1.0, 100)
        sep = calcular_separacion_sigma(datos, datos)
        self.assertAlmostEqual(sep, 0.0, places=5)

    def test_separacion_positiva_cuando_con_mayor(self):
        """La separación debe ser positiva cuando la media de 'con' supera la de 'sin'."""
        rng = np.random.default_rng(61)
        con = rng.normal(3.0, 1.0, 100)
        sin = rng.normal(1.0, 1.0, 100)
        sep = calcular_separacion_sigma(con, sin)
        self.assertGreater(sep, 0.0)

    def test_separacion_crece_con_diferencia_medias(self):
        """La separación debe crecer al aumentar la diferencia de medias."""
        rng = np.random.default_rng(62)
        sin = rng.normal(0.0, 1.0, 200)
        sep1 = calcular_separacion_sigma(rng.normal(1.0, 1.0, 200), sin)
        sep2 = calcular_separacion_sigma(rng.normal(3.0, 1.0, 200), sin)
        self.assertLess(sep1, sep2)


class TestH0Sanity(unittest.TestCase):
    """
    Tests de saneamiento bajo H₀ (hipótesis nula pura).

    Bajo H₀, ambos canales son ruido independiente y no hay señal en ninguno.
    En este caso:
      • AUC de cualquier métrica debe ser ≈ 0.5 (azar).
      • La separación entre 'con ruido' vs 'sin ruido' debe ser ≈ 0.
    """

    @classmethod
    def setUpClass(cls):
        """Crea distribuciones H₀ de SNR y Ψ con ruido puro en ambas hipótesis."""
        n = 200
        fs = SAMPLE_RATE
        N = int(0.2 * fs)
        snr_a, snr_b = [], []
        psi_a, psi_b = [], []

        for i in range(n):
            rng1 = np.random.default_rng(500 + i * 4)
            rng2 = np.random.default_rng(500 + i * 4 + 1)
            rng3 = np.random.default_rng(500 + i * 4 + 2)
            rng4 = np.random.default_rng(500 + i * 4 + 3)

            # Grupo A: dos realizaciones de ruido puro
            xa = generar_ruido_coloreado(N, rng=rng1)
            ya = generar_ruido_coloreado(N, rng=rng2)
            # Grupo B: otras dos realizaciones de ruido puro
            xb = generar_ruido_coloreado(N, rng=rng3)
            yb = generar_ruido_coloreado(N, rng=rng4)

            snr_a.append(calcular_snr_potencia(xa, f0=F0, fs=fs))
            snr_b.append(calcular_snr_potencia(xb, f0=F0, fs=fs))
            psi_a.append(calcular_psi_noetica(xa, ya, f0=F0, fs=fs))
            psi_b.append(calcular_psi_noetica(xb, yb, f0=F0, fs=fs))

        cls.snr_a = np.array(snr_a)
        cls.snr_b = np.array(snr_b)
        cls.psi_a = np.array(psi_a)
        cls.psi_b = np.array(psi_b)

    def test_snr_auc_cerca_de_punto_cinco_bajo_h0(self):
        """SNR bajo H₀ puro: AUC debe ser ≈ 0.5 (no hay información de señal)."""
        roc = calcular_curva_roc(self.snr_a, self.snr_b, nombre='SNR H0')
        self.assertAlmostEqual(roc.auc, 0.5, delta=0.1,
                               msg=f"SNR AUC bajo H₀ puro debe ser ≈ 0.5 (got {roc.auc:.3f})")

    def test_psi_auc_cerca_de_punto_cinco_bajo_h0(self):
        """Ψ bajo H₀ puro: AUC debe ser ≈ 0.5 (sin señal coherente)."""
        roc = calcular_curva_roc(self.psi_a, self.psi_b, nombre='Psi H0')
        self.assertAlmostEqual(roc.auc, 0.5, delta=0.1,
                               msg=f"Ψ AUC bajo H₀ puro debe ser ≈ 0.5 (got {roc.auc:.3f})")

    def test_separacion_sigma_baja_bajo_h0(self):
        """La separación σ entre dos grupos de ruido puro debe ser ≈ 0."""
        sep_snr = calcular_separacion_sigma(self.snr_a, self.snr_b)
        sep_psi = calcular_separacion_sigma(self.psi_a, self.psi_b)
        self.assertLess(abs(sep_snr), 1.5,
                        f"SNR σ-sep bajo H₀ debe ser pequeña (got {sep_snr:.2f})")
        self.assertLess(abs(sep_psi), 1.5,
                        f"Ψ σ-sep bajo H₀ debe ser pequeña (got {sep_psi:.2f})")


class TestFallbackScipy(unittest.TestCase):
    """
    Tests que verifican la ruta fallback (sin SciPy) de calcular_psi_noetica.

    Monkeypatcha SCIPY_AVAILABLE a False para ejercitar la implementación
    manual Welch y verifica que el comportamiento estadístico se conserva.
    """

    def _calc_psi_fallback(self, x, y, f0=F0, fs=SAMPLE_RATE):
        """Invoca Ψ forzando el camino fallback."""
        orig = snr_vs_psi_comparison.SCIPY_AVAILABLE
        snr_vs_psi_comparison.SCIPY_AVAILABLE = False
        try:
            return calcular_psi_noetica(x, y, f0=f0, fs=fs)
        finally:
            snr_vs_psi_comparison.SCIPY_AVAILABLE = orig

    def test_fallback_psi_no_negativa(self):
        """Fallback: Ψ debe ser no-negativa con ruido puro."""
        rng_a = np.random.default_rng(70)
        rng_b = np.random.default_rng(71)
        N = int(0.5 * SAMPLE_RATE)
        x = generar_ruido_coloreado(N, rng=rng_a)
        y = generar_ruido_coloreado(N, rng=rng_b)
        psi = self._calc_psi_fallback(x, y)
        self.assertGreaterEqual(psi, 0.0)

    def test_fallback_psi_mayor_con_senal_coherente(self):
        """Fallback: Ψ con señal coherente debe superar Ψ con solo ruido."""
        rng_a = np.random.default_rng(72)
        rng_b = np.random.default_rng(73)
        N = int(0.5 * SAMPLE_RATE)
        ruido_a = generar_ruido_coloreado(N, rng=rng_a)
        ruido_b = generar_ruido_coloreado(N, rng=rng_b)
        senal = generar_senal_decayente(3.0, duration=0.5, fs=SAMPLE_RATE, f0=F0)

        psi_con = self._calc_psi_fallback(senal + ruido_a, senal + ruido_b)
        psi_sin = self._calc_psi_fallback(ruido_a, ruido_b)
        self.assertGreater(psi_con, psi_sin,
                           "Fallback Ψ con señal coherente debe superar Ψ sin señal")

    def test_fallback_psi_baja_para_ruido_independiente(self):
        """Fallback: con ruido independiente, Ψ debe ser inferior a Ψ con señal."""
        N = int(0.5 * SAMPLE_RATE)
        ruido_a = generar_ruido_coloreado(N, rng=np.random.default_rng(74))
        ruido_b = generar_ruido_coloreado(N, rng=np.random.default_rng(75))
        senal = generar_senal_decayente(5.0, duration=0.5, fs=SAMPLE_RATE, f0=F0)

        psi_senal = self._calc_psi_fallback(senal + ruido_a, senal + ruido_b)
        psi_ruido = self._calc_psi_fallback(ruido_a, ruido_b)
        self.assertGreater(psi_senal, psi_ruido)


if __name__ == '__main__':
    unittest.main(verbosity=2)
