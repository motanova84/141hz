#!/usr/bin/env python3
"""
Tests para el Experimento del Coliseo Estadístico: SNR vs Ψ Noética
===================================================================

Valida la implementación del experimento que compara el SNR estándar de
potencia contra la métrica Ψ Noética de coherencia cruzada bajo f₀ = 141.7001 Hz.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import sys
import os
import unittest
import numpy as np

# Añadir el directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from snr_vs_psi_comparison import (
    F0,
    SAMPLE_RATE,
    generar_senal_decayente,
    generar_ruido_coloreado,
    calcular_snr_potencia,
    calcular_psi_noetica,
    calcular_curva_roc,
    ejecutar_zona,
    ejecutar_coliseo,
    tabla_comparativa,
    ResultadoROC,
    ResultadoZona,
)


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


if __name__ == '__main__':
    unittest.main(verbosity=2)
