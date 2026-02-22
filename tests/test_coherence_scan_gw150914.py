#!/usr/bin/env python3
"""
Tests para coherence_scan_gw150914.py
======================================

Valida el pipeline de escaneo de coherencia H1-L1 en GW150914 que
implementa la métrica Noēsis Ψ = I(f₀) · A_eff².

Estructura:
  - TestCoherenceScanConstants  : constantes del módulo
  - TestPreprocessing           : blanqueo y paso de banda
  - TestSpectralMetrics         : I(f₀) y A_eff
  - TestPsiMetric               : métrica Ψ completa
  - TestCoherenceScanPipeline   : pipeline run_coherence_scan end-to-end
  - TestIntegration             : verificación de separación on/off-source

Autor: Sistema QCAL ∞³
"""

import unittest
import numpy as np
import sys
import os

# ---------------------------------------------------------------------------
# Añadir el directorio de scripts al path para importar el módulo
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, 'scripts')
sys.path.insert(0, SCRIPTS_DIR)

import coherence_scan_gw150914 as cs


# ---------------------------------------------------------------------------
# Helpers de datos de prueba
# ---------------------------------------------------------------------------

def _pure_noise(n: int = 4096, seed: int = 0) -> np.ndarray:
    """Ruido gaussiano puro sin señal coherente."""
    rng = np.random.default_rng(seed)
    return rng.standard_normal(n) * 1e-23


def _coherent_signal(
    n: int = 4096,
    sample_rate: int = 4096,
    f0: float = cs.F0_QCAL,
    amplitude: float = 5e-22,
    seed: int = 42,
) -> np.ndarray:
    """
    Señal coherente: ruido gaussiano + tono sinusoidal en f0.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(n) / sample_rate
    noise = rng.standard_normal(n) * 1e-24
    tone = amplitude * np.sin(2 * np.pi * f0 * t)
    return noise + tone


# ---------------------------------------------------------------------------
# Tests de constantes del módulo
# ---------------------------------------------------------------------------

class TestCoherenceScanConstants(unittest.TestCase):
    """Verifica que las constantes públicas del módulo están definidas."""

    def test_gps_time(self):
        """GPS time de GW150914 debe ser 1126259462.4."""
        self.assertAlmostEqual(cs.GW150914_GPS, 1126259462.4, places=1)

    def test_f0_qcal(self):
        """Frecuencia objetivo f₀ = 141.7001 Hz."""
        self.assertAlmostEqual(cs.F0_QCAL, 141.7001, places=4)

    def test_sample_rate(self):
        """Tasa de muestreo = 4096 Hz."""
        self.assertEqual(cs.SAMPLE_RATE, 4096)

    def test_on_source_window(self):
        """Ventana On-Source: [-0.1, +0.1] s."""
        self.assertAlmostEqual(cs.ON_SOURCE_WINDOW[0], -0.1, places=3)
        self.assertAlmostEqual(cs.ON_SOURCE_WINDOW[1], +0.1, places=3)

    def test_off_source_window(self):
        """Ventana Off-Source: [-2.1, -1.9] s."""
        self.assertAlmostEqual(cs.OFF_SOURCE_WINDOW[0], -2.1, places=3)
        self.assertAlmostEqual(cs.OFF_SOURCE_WINDOW[1], -1.9, places=3)

    def test_bandpass_range(self):
        """Paso de banda: 130 – 160 Hz."""
        self.assertLess(cs.BANDPASS_LOW, cs.F0_QCAL)
        self.assertGreater(cs.BANDPASS_HIGH, cs.F0_QCAL)


# ---------------------------------------------------------------------------
# Tests de preprocesado
# ---------------------------------------------------------------------------

class TestPreprocessing(unittest.TestCase):
    """Verifica las funciones de blanqueo y paso de banda."""

    def setUp(self):
        n = 4 * cs.SAMPLE_RATE  # 4 segundos
        self.raw = _pure_noise(n=n, seed=7)

    def test_whiten_same_length(self):
        """La señal blanqueada debe tener la misma longitud que la entrada."""
        w = cs.whiten(self.raw)
        self.assertEqual(len(w), len(self.raw))

    def test_whiten_reduces_spectral_variation(self):
        """
        El blanqueo debe reducir la varianza relativa del espectro de potencia.
        La amplitud espectral debe ser más uniforme tras el blanqueo.
        """
        n = len(self.raw)
        amp_raw = np.abs(np.fft.rfft(self.raw)) / n
        w = cs.whiten(self.raw)
        amp_w = np.abs(np.fft.rfft(w)) / n

        # Coeficiente de variación debe disminuir
        cv_raw = np.std(amp_raw) / (np.mean(amp_raw) + 1e-30)
        cv_white = np.std(amp_w) / (np.mean(amp_w) + 1e-30)
        self.assertLess(cv_white, cv_raw,
                        "Blanqueo debe reducir la variación espectral relativa")

    def test_bandpass_same_length(self):
        """El filtro paso de banda no debe cambiar la longitud."""
        bp = cs.bandpass(self.raw)
        self.assertEqual(len(bp), len(self.raw))

    def test_bandpass_suppresses_out_of_band(self):
        """El paso de banda debe suprimir frecuencias fuera de banda."""
        sample_rate = cs.SAMPLE_RATE
        n = 4 * sample_rate
        t = np.arange(n) / sample_rate

        # Señal fuera de banda a 50 Hz
        out_of_band = np.sin(2 * np.pi * 50.0 * t)
        filtered = cs.bandpass(out_of_band)

        # La energía debe reducirse drásticamente
        energy_in = np.sum(out_of_band ** 2)
        energy_out = np.sum(filtered ** 2)
        self.assertLess(energy_out, 0.01 * energy_in,
                        "Señal fuera de banda debe ser suprimida (>99%)")

    def test_preprocess_pipeline(self):
        """preprocess debe devolver un array de la misma longitud."""
        proc = cs.preprocess(self.raw)
        self.assertEqual(len(proc), len(self.raw))
        self.assertFalse(np.all(proc == 0), "La señal preprocesada no debe ser cero")


# ---------------------------------------------------------------------------
# Tests de métricas espectrales
# ---------------------------------------------------------------------------

class TestSpectralMetrics(unittest.TestCase):
    """Verifica spectral_intensity y effective_coherence."""

    def setUp(self):
        self.sample_rate = cs.SAMPLE_RATE
        self.n = 2 * self.sample_rate  # 2 segundos

    # -- spectral_intensity --------------------------------------------------

    def test_intensity_positive(self):
        """I(f₀) debe ser positivo para cualquier señal no nula."""
        data = _pure_noise(self.n)
        i = cs.spectral_intensity(data)
        self.assertGreater(i, 0.0)

    def test_intensity_larger_with_tone(self):
        """I(f₀) debe ser mayor cuando hay un tono en f₀."""
        noise = _pure_noise(self.n, seed=1)
        signal = _coherent_signal(self.n, self.sample_rate, cs.F0_QCAL,
                                   amplitude=1e-20, seed=1)
        i_noise = cs.spectral_intensity(noise)
        i_signal = cs.spectral_intensity(signal)
        self.assertGreater(i_signal, i_noise,
                           "I(f₀) debe crecer con la amplitud de la señal")

    def test_intensity_scales_with_amplitude(self):
        """I(f₀) debe escalar con el cuadrado de la amplitud."""
        t = np.arange(self.n) / self.sample_rate
        amp1, amp2 = 1e-22, 2e-22
        s1 = amp1 * np.sin(2 * np.pi * cs.F0_QCAL * t)
        s2 = amp2 * np.sin(2 * np.pi * cs.F0_QCAL * t)
        i1 = cs.spectral_intensity(s1)
        i2 = cs.spectral_intensity(s2)
        self.assertAlmostEqual(i2 / i1, 4.0, delta=0.5,
                               msg="I escala con A²")

    # -- effective_coherence -------------------------------------------------

    def test_coherence_identical_signals(self):
        """
        Señales idénticas en H1 y L1 deben dar A_eff ≈ 1.
        """
        data = _coherent_signal(self.n, self.sample_rate)
        a_eff = cs.effective_coherence(data, data)
        self.assertGreater(a_eff, 0.95,
                           "Señales idénticas deben tener coherencia ≈ 1")

    def test_coherence_independent_noise(self):
        """
        Ruidos independientes deben dar coherencia baja.
        """
        h1 = _pure_noise(self.n, seed=10)
        l1 = _pure_noise(self.n, seed=20)
        a_eff = cs.effective_coherence(h1, l1)
        self.assertLess(a_eff, 0.5,
                        "Ruidos independientes deben tener coherencia baja")

    def test_coherence_range(self):
        """A_eff debe estar en [0, 1]."""
        h1 = _pure_noise(self.n, seed=30)
        l1 = _pure_noise(self.n, seed=40)
        a_eff = cs.effective_coherence(h1, l1)
        self.assertGreaterEqual(a_eff, 0.0)
        self.assertLessEqual(a_eff, 1.0)

    def test_coherence_partial(self):
        """
        Una mezcla de señal coherente + ruido debe dar coherencia intermedia.
        """
        t = np.arange(self.n) / self.sample_rate
        tone = 1e-22 * np.sin(2 * np.pi * cs.F0_QCAL * t)
        rng = np.random.default_rng(99)
        noise_h1 = rng.standard_normal(self.n) * 5e-22
        noise_l1 = rng.standard_normal(self.n) * 5e-22
        h1 = tone + noise_h1
        l1 = tone + noise_l1
        a_eff = cs.effective_coherence(h1, l1)
        self.assertGreater(a_eff, 0.0)
        self.assertLess(a_eff, 1.0)


# ---------------------------------------------------------------------------
# Tests de la métrica Ψ
# ---------------------------------------------------------------------------

class TestPsiMetric(unittest.TestCase):
    """Verifica la función compute_psi."""

    def setUp(self):
        self.sample_rate = cs.SAMPLE_RATE
        self.n = 2 * self.sample_rate

    def test_psi_coherent_greater_than_noise(self):
        """
        Ψ debe ser mayor para señales coherentes que para ruido puro.
        """
        # Ruido puro (off-source)
        h1_noise = _pure_noise(self.n, seed=1)
        l1_noise = _pure_noise(self.n, seed=2)
        psi_off, _, _ = cs.compute_psi(h1_noise, l1_noise)

        # Señal coherente (on-source)
        h1_on = _coherent_signal(self.n, self.sample_rate, amplitude=1e-20, seed=5)
        l1_on = _coherent_signal(self.n, self.sample_rate, amplitude=1e-20, seed=5)
        psi_on, _, _ = cs.compute_psi(h1_on, l1_on)

        self.assertGreater(psi_on, psi_off,
                           "Ψ_on debe ser mayor que Ψ_off para señal coherente")

    def test_psi_formula(self):
        """Ψ debe ser exactamente I(f₀) · A_eff²."""
        h1 = _coherent_signal(self.n, self.sample_rate, seed=7)
        l1 = _coherent_signal(self.n, self.sample_rate, seed=7)
        psi, intensity, a_eff = cs.compute_psi(h1, l1)
        expected = intensity * a_eff ** 2
        self.assertAlmostEqual(psi, expected, places=30,
                               msg="Ψ = I(f₀) · A_eff²")

    def test_psi_non_negative(self):
        """Ψ debe ser siempre ≥ 0."""
        h1 = _pure_noise(self.n, seed=50)
        l1 = _pure_noise(self.n, seed=51)
        psi, _, _ = cs.compute_psi(h1, l1)
        self.assertGreaterEqual(psi, 0.0)


# ---------------------------------------------------------------------------
# Tests del pipeline completo
# ---------------------------------------------------------------------------

class TestCoherenceScanPipeline(unittest.TestCase):
    """Verifica run_coherence_scan con datos simulados."""

    @classmethod
    def setUpClass(cls):
        """Forzar modo offline/simulado para evitar descargas reales en tests."""
        cls._orig_gwpy_available = getattr(cs, "GWPY_AVAILABLE", None)
        cs.GWPY_AVAILABLE = False

    @classmethod
    def tearDownClass(cls):
        """Restaurar el estado original de GWPY_AVAILABLE tras los tests."""
        if cls._orig_gwpy_available is None:
            # El atributo no existía originalmente
            if hasattr(cs, "GWPY_AVAILABLE"):
                delattr(cs, "GWPY_AVAILABLE")
        else:
            cs.GWPY_AVAILABLE = cls._orig_gwpy_available
    def test_run_returns_dict(self):
        """run_coherence_scan debe devolver un diccionario."""
        results = cs.run_coherence_scan(verbose=False)
        self.assertIsInstance(results, dict)

    def test_run_keys_present(self):
        """El resultado debe contener todas las claves esperadas."""
        results = cs.run_coherence_scan(verbose=False)
        for key in ('off_source', 'on_source', 'ratio_psi', 'f0', 'gps_t0'):
            self.assertIn(key, results, f"Clave '{key}' debe estar en los resultados")

    def test_run_sub_keys(self):
        """Cada segmento debe contener 'psi', 'intensity' y 'a_eff'."""
        results = cs.run_coherence_scan(verbose=False)
        for segment in ('off_source', 'on_source'):
            for sub in ('psi', 'intensity', 'a_eff'):
                self.assertIn(sub, results[segment],
                              f"'{segment}' debe contener '{sub}'")

    def test_run_psi_positive(self):
        """Ψ debe ser positivo en ambas ventanas."""
        results = cs.run_coherence_scan(verbose=False)
        self.assertGreater(results['off_source']['psi'], 0.0)
        self.assertGreater(results['on_source']['psi'], 0.0)

    def test_run_a_eff_range(self):
        """A_eff debe estar en [0, 1] en ambas ventanas."""
        results = cs.run_coherence_scan(verbose=False)
        for seg in ('off_source', 'on_source'):
            a = results[seg]['a_eff']
            self.assertGreaterEqual(a, 0.0, f"A_eff de {seg} debe ser ≥ 0")
            self.assertLessEqual(a, 1.0, f"A_eff de {seg} debe ser ≤ 1")

    def test_run_f0_preserved(self):
        """El resultado debe reflejar la f₀ usada."""
        results = cs.run_coherence_scan(f0=cs.F0_QCAL, verbose=False)
        self.assertAlmostEqual(results['f0'], cs.F0_QCAL, places=4)

    def test_run_gps_preserved(self):
        """El resultado debe reflejar el GPS time usado."""
        results = cs.run_coherence_scan(gps_t0=cs.GW150914_GPS, verbose=False)
        self.assertAlmostEqual(results['gps_t0'], cs.GW150914_GPS, places=1)


# ---------------------------------------------------------------------------
# Tests de integración: separación on/off-source
# ---------------------------------------------------------------------------

class TestIntegration(unittest.TestCase):
    """
    Verifica la separación estadística on/off-source descrita en el
    enunciado del experimento.

    Con datos simulados (sin señal real de GWOSC) la separación no es
    tan dramática como con datos reales, pero la arquitectura del pipeline
    debe producir resultados coherentes y reproducibles.
    """

    def test_ratio_positive(self):
        """El ratio Ψ_on / Ψ_off debe ser finito y positivo."""
        results = cs.run_coherence_scan(verbose=False)
        ratio = results['ratio_psi']
        self.assertGreater(ratio, 0.0, "Ratio Ψ_on/Ψ_off debe ser positivo")
        self.assertFalse(np.isinf(ratio), "Ratio no debe ser infinito")

    def test_reproducibility(self):
        """
        Dos ejecuciones consecutivas con los mismos parámetros deben
        producir resultados idénticos (la simulación es determinista).
        """
        r1 = cs.run_coherence_scan(verbose=False)
        r2 = cs.run_coherence_scan(verbose=False)
        self.assertAlmostEqual(r1['off_source']['psi'], r2['off_source']['psi'],
                               places=30, msg="Ψ_off debe ser reproducible")
        self.assertAlmostEqual(r1['on_source']['psi'], r2['on_source']['psi'],
                               places=30, msg="Ψ_on debe ser reproducible")

    def test_extract_window_correct_length(self):
        """extract_window debe devolver un array con el número correcto de muestras."""
        sample_rate = cs.SAMPLE_RATE
        t0 = cs.GW150914_GPS
        margin = 4.0
        t_start = t0 + cs.OFF_SOURCE_WINDOW[0] - margin
        total_duration = (t0 + cs.ON_SOURCE_WINDOW[1] + margin) - t_start
        n_total = int(total_duration * sample_rate)
        dummy = np.zeros(n_total)

        win = cs.ON_SOURCE_WINDOW
        extracted = cs.extract_window(dummy, t0, t_start, win, sample_rate)
        expected_n = int((win[1] - win[0]) * sample_rate)
        self.assertEqual(len(extracted), expected_n,
                         "extract_window debe devolver la longitud correcta")

    def test_simulate_fallback(self):
        """_simulate_strain debe devolver datos con amplitud realista."""
        data = cs._simulate_strain('H1', duration=0.2)
        # Amplitud máxima debe estar en el rango de ruido de LIGO (~10^{-23})
        self.assertLess(np.max(np.abs(data)), 1e-20,
                        "Datos simulados deben tener amplitud < 10^{-20}")
        self.assertGreater(np.max(np.abs(data)), 0.0,
                           "Datos simulados no deben ser todos ceros")


if __name__ == '__main__':
    unittest.main(verbosity=2)
