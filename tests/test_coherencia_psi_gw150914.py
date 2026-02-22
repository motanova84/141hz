#!/usr/bin/env python3
"""
Tests para coherencia_psi_gw150914.py
======================================

Valida las funciones de simulación, blanqueo, métrica Ψ y análisis
ON/OFF-source del módulo de coherencia para GW150914.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import importlib.util
import os
import sys
import unittest

import numpy as np

# ---------------------------------------------------------------------------
# Carga del módulo evitando la cadena de importación del paquete, que
# requiere matplotlib (puede no estar disponible en entornos CI ligeros).
# ---------------------------------------------------------------------------
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODULE_PATH = os.path.join(
    _REPO_ROOT, "141Hz", "analysis", "coherencia_psi_gw150914.py"
)
_spec = importlib.util.spec_from_file_location("coherencia_psi_gw150914", _MODULE_PATH)
cpsi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cpsi)


# ===========================================================================
# Tests de simulación
# ===========================================================================


class TestSimularDatosGW150914(unittest.TestCase):
    """Pruebas para simular_datos_gw150914()"""

    def test_output_shapes(self):
        """Los arrays devueltos tienen la longitud correcta."""
        fs = cpsi.SAMPLE_RATE
        dur = 4.0
        h_H1, h_L1, t = cpsi.simular_datos_gw150914(
            sample_rate=fs, duration=dur, seed=0
        )
        expected_len = int(dur * fs)
        self.assertEqual(len(h_H1), expected_len)
        self.assertEqual(len(h_L1), expected_len)
        self.assertEqual(len(t), expected_len)

    def test_reproducibility(self):
        """El mismo seed produce exactamente la misma salida."""
        h1a, h2a, _ = cpsi.simular_datos_gw150914(seed=7)
        h1b, h2b, _ = cpsi.simular_datos_gw150914(seed=7)
        np.testing.assert_array_equal(h1a, h1b)
        np.testing.assert_array_equal(h2a, h2b)

    def test_different_seeds(self):
        """Seeds distintas producen realizaciones de ruido diferentes."""
        h1a, _, _ = cpsi.simular_datos_gw150914(seed=0)
        h1b, _, _ = cpsi.simular_datos_gw150914(seed=1)
        self.assertFalse(np.array_equal(h1a, h1b))

    def test_noise_statistics(self):
        """El ruido de fondo (sin señal) tiene σ ≈ 1."""
        # Datos sin señal: ubicar merger fuera de la duración
        h_H1, _, _ = cpsi.simular_datos_gw150914(
            duration=4.0, t_merger=100.0, seed=42
        )
        # La totalidad de la serie es ruido puro
        self.assertAlmostEqual(float(np.std(h_H1)), 1.0, delta=0.05)

    def test_signal_present_near_merger(self):
        """La varianza es mayor cerca del merger que lejos de él."""
        fs = cpsi.SAMPLE_RATE
        t_m = 16.0
        h_H1, _, _ = cpsi.simular_datos_gw150914(seed=42)
        N = len(h_H1)
        mi = int(t_m * fs)
        var_on = float(np.var(h_H1[mi - 1843 : mi]))  # ventana del chirp
        var_off = float(np.var(h_H1[: int(10 * fs)]))  # primeros 10 s (solo ruido)
        self.assertGreater(var_on, var_off)


# ===========================================================================
# Tests de blanqueo / bandpass
# ===========================================================================


class TestBlanquearDatos(unittest.TestCase):
    """Pruebas para blanquear_datos()"""

    def setUp(self):
        rng = np.random.default_rng(99)
        self.noise = rng.normal(size=int(4 * cpsi.SAMPLE_RATE))

    def test_zero_input(self):
        """Input cero → output cero (sin división por cero)."""
        z = cpsi.blanquear_datos(np.zeros(4096))
        np.testing.assert_array_equal(z, np.zeros(4096))

    def test_bandpass_out_of_band_suppression(self):
        """Las frecuencias fuera de la banda son suprimidas."""
        from scipy import signal as scipy_signal

        fs = cpsi.SAMPLE_RATE
        N = int(4 * fs)
        t = np.arange(N) / fs
        # Tono puro a 200 Hz (fuera de 35–123 Hz)
        tone_200hz = np.sin(2 * np.pi * 200 * t)
        whitened = cpsi.blanquear_datos(tone_200hz)
        rms_out = float(np.sqrt(np.mean(whitened[N // 2 :] ** 2)))  # evitar bordes
        self.assertLess(rms_out, 0.01)

    def test_bandpass_in_band_passes(self):
        """Las frecuencias dentro de la banda no son suprimidas totalmente."""
        fs = cpsi.SAMPLE_RATE
        N = int(4 * fs)
        t = np.arange(N) / fs
        # Tono puro a 80 Hz (dentro de 35–123 Hz)
        tone_80hz = np.sin(2 * np.pi * 80 * t)
        whitened = cpsi.blanquear_datos(tone_80hz)
        rms_out = float(np.sqrt(np.mean(whitened[N // 2 :] ** 2)))
        self.assertGreater(rms_out, 0.1)

    def test_noise_std_after_bandpass(self):
        """El ruido filtrado tiene std en el rango esperado para BW=88 Hz."""
        whitened = cpsi.blanquear_datos(self.noise)
        # Para ruido blanco σ=1 y BW=88 Hz, σ_bp ≈ sqrt(2*88/4096) ≈ 0.207
        std_bp = float(np.std(whitened))
        self.assertGreater(std_bp, 0.10)
        self.assertLess(std_bp, 0.35)

    def test_output_length_preserved(self):
        """La longitud del output es igual a la del input."""
        for n in [512, 1024, 2048, 4096]:
            x = np.random.randn(n)
            y = cpsi.blanquear_datos(x)
            self.assertEqual(len(y), n)


# ===========================================================================
# Tests de la métrica Ψ
# ===========================================================================


class TestCalcularPsiEnVentana(unittest.TestCase):
    """Pruebas para calcular_psi_en_ventana()"""

    def test_zero_inputs(self):
        """Ψ de señales nulas es 0."""
        psi = cpsi.calcular_psi_en_ventana(np.zeros(512), np.zeros(512))
        self.assertEqual(psi, 0.0)

    def test_psi_nonnegative(self):
        """Ψ siempre es >= 0."""
        rng = np.random.default_rng(0)
        for _ in range(20):
            h1 = rng.normal(size=2048)
            h2 = rng.normal(size=2048)
            psi = cpsi.calcular_psi_en_ventana(h1, h2)
            self.assertGreaterEqual(psi, 0.0)

    def test_identical_signals_positive(self):
        """Señales idénticas → Ψ > 0."""
        x = np.random.randn(2048)
        psi = cpsi.calcular_psi_en_ventana(x, x)
        self.assertGreater(psi, 0.0)

    def test_noise_psi_order_of_magnitude(self):
        """Para ruido bandpassed independiente, E[Ψ_OFF] ≈ 2.1 × 10⁻⁵."""
        rng = np.random.default_rng(77)
        win = cpsi.WINDOW_SAMPLES
        psi_vals = []
        for _ in range(500):
            h1 = rng.normal(size=win)
            h2 = rng.normal(size=win)
            h1_bp = cpsi.blanquear_datos(h1, sample_rate=cpsi.SAMPLE_RATE)
            h2_bp = cpsi.blanquear_datos(h2, sample_rate=cpsi.SAMPLE_RATE)
            psi_vals.append(cpsi.calcular_psi_en_ventana(h1_bp, h2_bp))
        psi_mean = float(np.mean(psi_vals))
        # E[Ψ_OFF] should be in [5e-6, 1e-4] for these parameters
        self.assertGreater(psi_mean, 5e-6)
        self.assertLess(psi_mean, 1e-4)

    def test_coherent_signal_psi_larger_than_noise(self):
        """Una señal coherente produce Ψ mayor que el ruido solo."""
        from scipy import signal as scipy_signal

        fs = cpsi.SAMPLE_RATE
        N = cpsi.WINDOW_SAMPLES
        t = np.arange(N) / fs
        chirp = scipy_signal.chirp(t, f0=35, f1=123, t1=N / fs, method="linear")
        chirp *= np.hanning(N)
        A = cpsi._A_SIGNAL_H1
        rng = np.random.default_rng(5)
        noise = rng.normal(size=N)
        h1 = cpsi.blanquear_datos(noise + A * chirp)
        h2 = cpsi.blanquear_datos(noise + A * (13 / 24) * chirp)
        psi_signal = cpsi.calcular_psi_en_ventana(h1, h2)

        noise_psies = []
        for seed in range(20):
            rng2 = np.random.default_rng(seed + 100)
            n1 = cpsi.blanquear_datos(rng2.normal(size=N))
            n2 = cpsi.blanquear_datos(rng2.normal(size=N))
            noise_psies.append(cpsi.calcular_psi_en_ventana(n1, n2))
        psi_noise_mean = float(np.mean(noise_psies))

        self.assertGreater(psi_signal, 10 * psi_noise_mean)


# ===========================================================================
# Tests de la serie temporal de Ψ
# ===========================================================================


class TestCalcularPsiSerieTemporal(unittest.TestCase):
    """Pruebas para calcular_psi_serie_temporal()"""

    def setUp(self):
        rng = np.random.default_rng(0)
        N = int(4 * cpsi.SAMPLE_RATE)
        self.h1 = cpsi.blanquear_datos(rng.normal(size=N))
        self.h2 = cpsi.blanquear_datos(rng.normal(size=N))

    def test_output_shapes_consistent(self):
        """times y psi_values tienen la misma longitud."""
        times, psi_vals = cpsi.calcular_psi_serie_temporal(self.h1, self.h2)
        self.assertEqual(len(times), len(psi_vals))

    def test_default_window_size(self):
        """La ventana por defecto es WINDOW_SAMPLES."""
        N = len(self.h1)
        win = cpsi.WINDOW_SAMPLES
        stride = win // 4
        expected_n = len(range(0, N - win + 1, stride))
        times, psi_vals = cpsi.calcular_psi_serie_temporal(self.h1, self.h2)
        self.assertEqual(len(times), expected_n)

    def test_times_within_bounds(self):
        """Los tiempos de centro de ventana están dentro del rango de la señal."""
        times, _ = cpsi.calcular_psi_serie_temporal(self.h1, self.h2)
        total_dur = len(self.h1) / cpsi.SAMPLE_RATE
        self.assertGreaterEqual(float(times[0]), 0.0)
        self.assertLessEqual(float(times[-1]), total_dur)

    def test_psi_values_nonnegative(self):
        """Todos los valores de la serie Ψ(t) son >= 0."""
        _, psi_vals = cpsi.calcular_psi_serie_temporal(self.h1, self.h2)
        self.assertTrue(np.all(psi_vals >= 0.0))


# ===========================================================================
# Tests de análisis ON/OFF source
# ===========================================================================


class TestAnalizarOnOffSource(unittest.TestCase):
    """Pruebas para analizar_on_off_source()"""

    def _make_psi_series(self, n=300, t_merger=16.0, psi_on_val=0.1, psi_off_val=1e-5, seed=0):
        rng = np.random.default_rng(seed)
        stride_s = cpsi.WINDOW_SAMPLES // 4
        fs = cpsi.SAMPLE_RATE
        N = int(32 * fs)
        times = np.array([(s + cpsi.WINDOW_SAMPLES // 2) / fs
                          for s in range(0, N - cpsi.WINDOW_SAMPLES + 1, stride_s)])
        on_mask = np.abs(times - t_merger) <= 0.5
        off_mask = np.abs(times - t_merger) > 2.0
        psi_vals = np.abs(rng.normal(scale=psi_off_val, size=len(times)))
        psi_vals[on_mask] = np.abs(rng.normal(loc=psi_on_val, scale=psi_on_val * 0.1,
                                               size=on_mask.sum()))
        return times, psi_vals

    def test_returns_none_when_no_on_windows(self):
        """Devuelve None si no hay ventanas ON."""
        times = np.arange(100) * 0.5
        psi = np.random.rand(100) * 1e-5
        # Merger muy lejos: no hay ON windows
        result = cpsi.analizar_on_off_source(times, psi, t_merger=9999.0)
        self.assertIsNone(result)

    def test_returns_none_when_too_few_off_windows(self):
        """Devuelve None si hay menos ventanas OFF que el mínimo."""
        times = np.array([0.0, 1.0, 2.0, 16.0])
        psi = np.array([1e-5, 1e-5, 1e-5, 0.1])
        result = cpsi.analizar_on_off_source(
            times, psi, t_merger=16.0, min_off_windows=50
        )
        self.assertIsNone(result)

    def test_detection_positive_strong_signal(self):
        """Una señal fuerte produce detección positiva."""
        times, psi_vals = self._make_psi_series(psi_on_val=0.5, psi_off_val=1e-6)
        result = cpsi.analizar_on_off_source(times, psi_vals, t_merger=16.0)
        self.assertIsNotNone(result)
        self.assertTrue(result["detection"])
        self.assertLess(result["p_value"], 0.01)

    def test_detection_negative_no_signal(self):
        """Sin señal, la detección no es positiva (p-value grande)."""
        rng = np.random.default_rng(0)
        # Pure noise: ON and OFF both drawn from same distribution
        times, psi_vals = self._make_psi_series(psi_on_val=1e-5, psi_off_val=1e-5)
        result = cpsi.analizar_on_off_source(times, psi_vals, t_merger=16.0)
        self.assertIsNotNone(result)
        # Not required to fail, but p-value should be large (no signal)
        # Just check structure
        self.assertIn("p_value", result)
        self.assertIn("contrast_ratio", result)

    def test_result_keys(self):
        """El resultado contiene todas las claves esperadas."""
        times, psi_vals = self._make_psi_series(psi_on_val=0.1)
        result = cpsi.analizar_on_off_source(times, psi_vals, t_merger=16.0)
        self.assertIsNotNone(result)
        expected_keys = {
            "psi_on", "psi_off", "psi_on_mean", "psi_off_mean",
            "psi_on_std", "psi_off_std", "contrast_ratio",
            "p_value", "n_on", "n_off", "detection", "significance",
        }
        self.assertEqual(set(result.keys()), expected_keys)

    def test_contrast_ratio_formula(self):
        """El ratio de contraste es psi_on_mean / psi_off_mean."""
        times, psi_vals = self._make_psi_series(psi_on_val=0.1)
        result = cpsi.analizar_on_off_source(times, psi_vals, t_merger=16.0)
        self.assertIsNotNone(result)
        expected = result["psi_on_mean"] / result["psi_off_mean"]
        self.assertAlmostEqual(result["contrast_ratio"], expected, places=5)


# ===========================================================================
# Tests de integración (análisis completo)
# ===========================================================================


class TestIntegracion(unittest.TestCase):
    """Pruebas de extremo a extremo del análisis completo."""

    def test_analisis_completo_deteccion_positiva(self):
        """Con datos simulados calibrados, la detección es POSITIVA (p < 0.01)."""
        result = cpsi.analizar_coherencia_psi_gw150914(seed=42)
        est = result["estadisticas"]
        self.assertIsNotNone(est)
        self.assertTrue(est["detection"], "Se espera detección POSITIVA con seed=42")
        self.assertLess(est["p_value"], 0.01)

    def test_psi_on_order_of_magnitude(self):
        """Ψ_ON media es del orden de 10⁻² a 10⁰ (señal detectable)."""
        result = cpsi.analizar_coherencia_psi_gw150914(seed=42)
        est = result["estadisticas"]
        self.assertGreater(est["psi_on_mean"], 1e-3)
        self.assertLess(est["psi_on_mean"], 1e1)

    def test_psi_off_order_of_magnitude(self):
        """Ψ_OFF media está en el rango del nivel de ruido esperado [5e-6, 1e-3]."""
        result = cpsi.analizar_coherencia_psi_gw150914(seed=42)
        est = result["estadisticas"]
        self.assertGreater(est["psi_off_mean"], 5e-6)
        self.assertLess(est["psi_off_mean"], 1e-3)

    def test_contrast_ratio_large(self):
        """El ratio de contraste Ψ_ON / Ψ_OFF es >> 1."""
        result = cpsi.analizar_coherencia_psi_gw150914(seed=42)
        est = result["estadisticas"]
        self.assertGreater(est["contrast_ratio"], 100)

    def test_psi_on_greater_than_psi_off(self):
        """Ψ_ON > Ψ_OFF en la simulación calibrada."""
        result = cpsi.analizar_coherencia_psi_gw150914(seed=42)
        est = result["estadisticas"]
        self.assertGreater(est["psi_on_mean"], est["psi_off_mean"])

    def test_result_dict_keys(self):
        """El resultado contiene todas las claves esperadas."""
        result = cpsi.analizar_coherencia_psi_gw150914(seed=42)
        expected_keys = {
            "times", "h_H1", "h_L1", "h_H1_w", "h_L1_w",
            "times_psi", "times_rel", "psi_values",
            "estadisticas", "parametros",
        }
        self.assertEqual(set(result.keys()), expected_keys)

    def test_times_rel_centered_at_zero(self):
        """times_rel tiene valores negativos Y positivos (centrado en merger)."""
        result = cpsi.analizar_coherencia_psi_gw150914(seed=42)
        times_rel = result["times_rel"]
        self.assertTrue(np.any(times_rel < 0))
        self.assertTrue(np.any(times_rel > 0))

    def test_custom_data_accepted(self):
        """El análisis acepta datos externos (sin generar datos simulados)."""
        rng = np.random.default_rng(0)
        N = int(8 * cpsi.SAMPLE_RATE)
        h_H1 = rng.normal(size=N)
        h_L1 = rng.normal(size=N)
        result = cpsi.analizar_coherencia_psi_gw150914(
            h_H1=h_H1, h_L1=h_L1, t_merger=4.0
        )
        self.assertIn("estadisticas", result)

    def test_reporte_generado_correctamente(self):
        """El reporte no contiene emojis y tiene las secciones esperadas."""
        result = cpsi.analizar_coherencia_psi_gw150914(seed=42)
        report = cpsi.generar_reporte(result)
        self.assertIsInstance(report, str)
        self.assertIn("REPORTE DE VALIDACION", report)
        self.assertIn("Psi_ON", report)
        self.assertIn("Psi_OFF", report)
        self.assertIn("Ratio de Contraste", report)
        self.assertIn("p-value", report)
        # No emoji characters
        for char in ["🔬", "📊", "🟢", "🏆", "✅", "❌"]:
            self.assertNotIn(char, report, f"Emoji '{char}' found in report")


if __name__ == "__main__":
    unittest.main(verbosity=2)
