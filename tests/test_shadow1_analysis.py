#!/usr/bin/env python3
"""
Tests for Shadow-1 Subthreshold GW Candidate Analysis
======================================================

Valida el módulo shadow1_analysis que implementa:

1. Factor de Bayes con ln_bayes_factor (canónico) y log10_bayes_factor
2. Masa chirp PN0 con incertidumbre bootstrap
3. Coherencia de fase A_eff = median(sqrt(γ))
4. Control time-slide: A_eff debe caer con desplazamiento temporal
5. Control de banda: ratio A_eff(GW) / A_eff(ctrl)
6. Veredicto de colisión silenciosa: flag + score continuo
7. Módulo EEG es independiente (bajo guard if __name__ == "__main__")
8. bayes_factor_logs en hierarchical_model devuelve ambas representaciones

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
"""

import unittest
import numpy as np
import sys
import os

# Añadir el directorio raíz y 141Hz al path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, '141Hz'))
sys.path.insert(0, REPO_ROOT)

from analysis import shadow1_analysis as s1
from bayes import hierarchical_model as hm


class TestBayesFactorNotation(unittest.TestCase):
    """Verifica que el factor de Bayes tiene notación canónica clara."""

    def test_ln_bayes_factor_is_canonical(self):
        """BayesResult debe tener ln_bayes_factor como campo canónico."""
        res = s1.compute_bayes_factor(snr=5.0)
        self.assertTrue(hasattr(res, 'ln_bayes_factor'),
                        "BayesResult debe exponer ln_bayes_factor (canónico)")
        self.assertTrue(hasattr(res, 'log10_bayes_factor'),
                        "BayesResult debe exponer log10_bayes_factor (referencia)")

    def test_log10_derived_from_ln(self):
        """log10_bayes_factor = ln_bayes_factor / ln(10)."""
        res = s1.compute_bayes_factor(snr=5.0)
        expected = res.ln_bayes_factor / np.log(10.0)
        self.assertAlmostEqual(res.log10_bayes_factor, expected, places=10,
                               msg="log10_bayes_factor debe ser ln_bf / ln(10)")

    def test_bayes_factor_linear_consistent(self):
        """bayes_factor lineal == exp(ln_bayes_factor)."""
        res = s1.compute_bayes_factor(snr=5.0)
        expected_b10 = np.exp(res.ln_bayes_factor)
        self.assertAlmostEqual(res.bayes_factor, expected_b10, places=6,
                               msg="bayes_factor lineal debe ser exp(ln_bayes_factor)")

    def test_disambiguation_example(self):
        """
        Verificar el ejemplo de ambigüedad del docstring:
        ln_bf ≈ 8.3  →  log10_bf ≈ 3.6  (no 8.3)
        """
        # Creamos un resultado artificial con ln_bf = 8.3
        import dataclasses
        dummy = s1.BayesResult(
            ln_bayes_factor=8.3,
            log10_bayes_factor=8.3 / np.log(10.0),
            bayes_factor=np.exp(8.3),
            interpretation="test",
            h0_description="test",
            h1_description="test",
            prior_signal_prob=1e-3,
        )
        # log10(B) debe ser ≈ 3.6, NO 8.3
        self.assertAlmostEqual(dummy.log10_bayes_factor, 3.6, delta=0.1,
                               msg="Si ln_bf=8.3, entonces log10_bf ≈ 3.6")
        # B lineal ≈ 4000, NO 2e8
        self.assertAlmostEqual(dummy.bayes_factor, 4000, delta=200,
                               msg="Si ln_bf=8.3, entonces B≈4000")

    def test_h0_h1_descriptions_present(self):
        """El resultado debe tener descripciones explícitas de H0 y H1."""
        res = s1.compute_bayes_factor(snr=5.0)
        self.assertIsInstance(res.h0_description, str)
        self.assertIsInstance(res.h1_description, str)
        self.assertGreater(len(res.h0_description), 10)
        self.assertGreater(len(res.h1_description), 10)
        # H0 debe mencionar ruido (en español o inglés)
        h0_lower = res.h0_description.lower()
        self.assertTrue('ruido' in h0_lower or 'noise' in h0_lower,
                        "h0_description debe mencionar ruido/noise")

    def test_prior_documented(self):
        """El prior P(H1) debe estar documentado en el resultado."""
        res = s1.compute_bayes_factor(snr=5.0)
        self.assertGreater(res.prior_signal_prob, 0.0)
        self.assertLess(res.prior_signal_prob, 1.0)

    def test_higher_snr_gives_higher_ln_bf(self):
        """Un SNR más alto debe dar un factor de Bayes más alto (H1 más plausible)."""
        res_low = s1.compute_bayes_factor(snr=1.0)
        res_high = s1.compute_bayes_factor(snr=6.0)
        self.assertGreater(res_high.ln_bayes_factor, res_low.ln_bayes_factor)


class TestHierarchicalBayesLogs(unittest.TestCase):
    """Verifica que hierarchical_model.bayes_factor_logs devuelve ambas representaciones."""

    def test_returns_dict_with_required_keys(self):
        """bayes_factor_logs debe retornar un dict con los tres campos."""
        result = hm.bayes_factor_logs([5.0, 6.0, 5.5])
        self.assertIn('bayes_factor', result)
        self.assertIn('ln_bayes_factor', result)
        self.assertIn('log10_bayes_factor', result)

    def test_log10_derived_from_ln(self):
        """log10_bayes_factor = ln_bayes_factor / ln(10)."""
        result = hm.bayes_factor_logs([5.0, 6.0])
        expected = result['ln_bayes_factor'] / np.log(10.0)
        self.assertAlmostEqual(result['log10_bayes_factor'], expected, places=10)

    def test_bayes_factor_linear_consistent(self):
        """bayes_factor == exp(ln_bayes_factor)."""
        result = hm.bayes_factor_logs([5.0, 6.0])
        expected = np.exp(result['ln_bayes_factor'])
        self.assertAlmostEqual(result['bayes_factor'], expected, places=6)

    def test_consistent_with_bayes_factor(self):
        """bayes_factor_logs debe ser consistente con bayes_factor()."""
        snr_list = [4.5, 5.5, 6.0]
        b10_original = hm.bayes_factor(snr_list)
        b10_logs = hm.bayes_factor_logs(snr_list)['bayes_factor']
        self.assertAlmostEqual(b10_original, b10_logs, places=6)


class TestChirpMass(unittest.TestCase):
    """Verifica la estimación de masa chirp con incertidumbre bootstrap."""

    def setUp(self):
        self.rng = np.random.default_rng(seed=42)

    def test_returns_chirp_mass_result(self):
        """chirp_mass_from_frequency_evolution debe retornar ChirpMassResult."""
        res = s1.chirp_mass_from_frequency_evolution(
            f_start=35.0, f_end=150.0, dt=0.4, rng=self.rng
        )
        self.assertIsInstance(res, s1.ChirpMassResult)

    def test_positive_chirp_mass(self):
        """La masa chirp debe ser positiva."""
        res = s1.chirp_mass_from_frequency_evolution(
            f_start=35.0, f_end=150.0, dt=0.4, rng=self.rng
        )
        self.assertGreater(res.chirp_mass_solar, 0.0)

    def test_uncertainty_is_positive(self):
        """La incertidumbre bootstrap debe ser positiva."""
        res = s1.chirp_mass_from_frequency_evolution(
            f_start=35.0, f_end=150.0, dt=0.4, rng=self.rng
        )
        self.assertGreater(res.chirp_mass_uncertainty, 0.0)

    def test_bootstrap_samples_shape(self):
        """Las muestras bootstrap deben tener la forma correcta."""
        n_boot = 100
        res = s1.chirp_mass_from_frequency_evolution(
            f_start=35.0, f_end=150.0, dt=0.4,
            n_bootstrap=n_boot, rng=self.rng
        )
        self.assertEqual(len(res.bootstrap_samples), n_boot)

    def test_warning_present(self):
        """Debe haber una advertencia sobre la limitación de la estimación PN0."""
        res = s1.chirp_mass_from_frequency_evolution(
            f_start=35.0, f_end=150.0, dt=0.4, rng=self.rng
        )
        self.assertIsInstance(res.warning, str)
        self.assertGreater(len(res.warning), 10)

    def test_uncertainty_fraction_reasonable(self):
        """La incertidumbre relativa debe ser razonable (> 0.1%)."""
        res = s1.chirp_mass_from_frequency_evolution(
            f_start=35.0, f_end=150.0, dt=0.4, rng=self.rng
        )
        relative_uncertainty = res.chirp_mass_uncertainty / res.chirp_mass_solar
        self.assertGreater(relative_uncertainty, 0.001,
                           "La incertidumbre relativa debe ser > 0.1%")

    def test_larger_jitter_gives_larger_uncertainty(self):
        """Mayor jitter debe producir mayor incertidumbre bootstrap."""
        rng1 = np.random.default_rng(seed=10)
        rng2 = np.random.default_rng(seed=10)
        res_small = s1.chirp_mass_from_frequency_evolution(
            35.0, 150.0, 0.4, jitter_frac=0.01, rng=rng1
        )
        res_large = s1.chirp_mass_from_frequency_evolution(
            35.0, 150.0, 0.4, jitter_frac=0.10, rng=rng2
        )
        self.assertGreater(res_large.chirp_mass_uncertainty,
                           res_small.chirp_mass_uncertainty)


class TestPhaseCoherence(unittest.TestCase):
    """Verifica el cálculo de A_eff = median(sqrt(γ))."""

    def setUp(self):
        self.rng = np.random.default_rng(seed=141)
        self.fs = 4096.0
        self.N = 4096
        self.f0 = 141.7
        self.bw = 10.0

    def _make_coherent(self, amp_ratio=0.9):
        """Genera datos coherentes en f0."""
        t = np.linspace(0, self.N / self.fs, self.N)
        signal = 1e-21 * np.sin(2 * np.pi * self.f0 * t)
        noise_h1 = self.rng.normal(0, 4e-24, self.N)
        noise_l1 = self.rng.normal(0, 4e-24, self.N)
        return noise_h1 + signal, noise_l1 + signal * amp_ratio

    def _make_incoherent(self):
        """Genera datos puramente de ruido (sin señal coherente)."""
        return self.rng.normal(0, 4e-24, self.N), self.rng.normal(0, 4e-24, self.N)

    def test_returns_coherence_result(self):
        """compute_phase_coherence debe retornar CoherenceResult."""
        h1, l1 = self._make_coherent()
        res = s1.compute_phase_coherence(h1, l1, self.fs, self.f0, self.bw)
        self.assertIsInstance(res, s1.CoherenceResult)

    def test_A_eff_in_range(self):
        """A_eff debe estar en [0, 1]."""
        h1, l1 = self._make_coherent()
        res = s1.compute_phase_coherence(h1, l1, self.fs, self.f0, self.bw)
        self.assertGreaterEqual(res.A_eff, 0.0)
        self.assertLessEqual(res.A_eff, 1.0)

    def test_coherent_higher_than_incoherent(self):
        """Señal coherente debe dar A_eff mayor que ruido puro."""
        h1_coh, l1_coh = self._make_coherent()
        h1_inc, l1_inc = self._make_incoherent()
        res_coh = s1.compute_phase_coherence(h1_coh, l1_coh, self.fs, self.f0, self.bw)
        res_inc = s1.compute_phase_coherence(h1_inc, l1_inc, self.fs, self.f0, self.bw)
        self.assertGreater(res_coh.A_eff, res_inc.A_eff,
                           "Señal coherente debe dar A_eff mayor que ruido puro")


class TestTimeSlidControl(unittest.TestCase):
    """Verifica que A_eff cae con el control de time-slide."""

    def setUp(self):
        self.rng = np.random.default_rng(seed=202)
        self.fs = 4096.0
        self.N = 4096
        self.f0 = 141.7

    def _make_coherent_data(self):
        t = np.linspace(0, self.N / self.fs, self.N)
        signal = 5e-22 * np.sin(2 * np.pi * self.f0 * t)
        h1 = self.rng.normal(0, 4e-24, self.N) + signal
        l1 = self.rng.normal(0, 4e-24, self.N) + signal * 0.9
        return h1, l1

    def test_returns_required_keys(self):
        """time_slide_control debe retornar dict con claves requeridas."""
        h1, l1 = self._make_coherent_data()
        res = s1.time_slide_control(h1, l1, self.fs, self.f0)
        required = {'A_eff_on_source', 'A_eff_time_slide', 'slide_s',
                    'coherence_drop_fraction', 'is_physical'}
        for key in required:
            self.assertIn(key, res, f"Falta clave: {key}")

    def test_slide_values_in_range(self):
        """Los valores de A_eff deben estar en [0, 1]."""
        h1, l1 = self._make_coherent_data()
        res = s1.time_slide_control(h1, l1, self.fs, self.f0)
        self.assertGreaterEqual(res['A_eff_on_source'], 0.0)
        self.assertLessEqual(res['A_eff_on_source'], 1.0)
        self.assertGreaterEqual(res['A_eff_time_slide'], 0.0)
        self.assertLessEqual(res['A_eff_time_slide'], 1.0)

    def test_is_physical_is_bool(self):
        """is_physical debe ser un booleano."""
        h1, l1 = self._make_coherent_data()
        res = s1.time_slide_control(h1, l1, self.fs, self.f0)
        self.assertIsInstance(res['is_physical'], bool)

    def test_slide_with_coherent_signal_drops_A_eff(self):
        """
        Con señal coherente real, A_eff debe caer con time-slide.
        Usa SNR alto y frecuencia alineada con bins de Welch.

        Con nperseg=256 y fs=4096, la resolución es 16 Hz, así que los
        bins están en 0, 16, 32, ..., 96, 112, ...  Se usa f0=96 Hz
        con bandwidth=20 Hz para capturar el bin exactamente.
        """
        rng = np.random.default_rng(seed=999)
        fs = 4096.0
        N = 4096
        # f0=96 Hz: exactamente en un bin de Welch (resolución 16 Hz)
        f0 = 96.0
        bandwidth = 20.0  # captura el bin en 96 Hz
        t = np.linspace(0, N / fs, N)
        # Señal muy fuerte para garantizar coherencia alta
        signal = 1e-18 * np.sin(2 * np.pi * f0 * t)
        h1 = rng.normal(0, 1e-23, N) + signal
        l1 = rng.normal(0, 1e-23, N) + signal

        res = s1.time_slide_control(h1, l1, fs, f0=f0, bandwidth=bandwidth)
        # Con señal fuerte, el slide debe reducir A_eff
        self.assertGreater(res['A_eff_on_source'], 0.0,
                           "A_eff_on_source debe ser > 0 con señal coherente")
        self.assertLess(res['A_eff_time_slide'], res['A_eff_on_source'],
                        "Con señal fuerte, time-slide debe reducir A_eff")


class TestBandCoherenceControl(unittest.TestCase):
    """Verifica el control de banda de frecuencia."""

    def setUp(self):
        self.rng = np.random.default_rng(seed=303)
        self.fs = 4096.0
        self.N = 4096

    def test_returns_required_keys(self):
        """band_coherence_control debe retornar dict con claves requeridas."""
        h1 = self.rng.normal(0, 4e-24, self.N)
        l1 = self.rng.normal(0, 4e-24, self.N)
        res = s1.band_coherence_control(h1, l1, self.fs)
        required = {'A_eff_gw_band', 'A_eff_ctrl_band', 'relative_ratio',
                    'f0', 'f_ctrl', 'is_excess_coherence'}
        for key in required:
            self.assertIn(key, res, f"Falta clave: {key}")

    def test_is_excess_coherence_is_bool(self):
        """is_excess_coherence debe ser un booleano."""
        h1 = self.rng.normal(0, 4e-24, self.N)
        l1 = self.rng.normal(0, 4e-24, self.N)
        res = s1.band_coherence_control(h1, l1, self.fs)
        self.assertIsInstance(res['is_excess_coherence'], bool)

    def test_relative_ratio_positive(self):
        """El ratio A_eff_gw / A_eff_ctrl debe ser positivo."""
        h1 = self.rng.normal(0, 4e-24, self.N)
        l1 = self.rng.normal(0, 4e-24, self.N)
        res = s1.band_coherence_control(h1, l1, self.fs)
        self.assertGreater(res['relative_ratio'], 0.0)

    def test_signal_in_gw_band_increases_ratio(self):
        """Señal solo en banda GW debe dar ratio GW/ctrl > 2 (is_excess=True).

        Con nperseg=256 y fs=4096 Hz, los bins de Welch están en múltiplos
        de 16 Hz.  Se usa f0=144 Hz (bin más cercano a 141.7 Hz) con
        bandwidth=20 Hz para capturar al menos un bin.
        """
        rng = np.random.default_rng(seed=404)
        fs = 4096.0
        N = 4096
        # f0=144 Hz: bin exacto de Welch (múltiplo de 16 Hz)
        f0_gw = 144.0
        t = np.linspace(0, N / fs, N)
        # Señal con SNR moderado: evita leakage severo pero mantiene
        # coherencia alta en GW band y baja en banda de control
        signal = 1e-18 * np.sin(2 * np.pi * f0_gw * t)
        noise_level = 1e-20  # SNR ≈ 100; no tan extremo como 1e5
        h1 = rng.normal(0, noise_level, N) + signal
        l1 = rng.normal(0, noise_level, N) + signal
        res = s1.band_coherence_control(h1, l1, fs,
                                        f0=f0_gw, bandwidth_gw=20.0,
                                        f_ctrl=300.0, bandwidth_ctrl=20.0)
        self.assertTrue(res['is_excess_coherence'],
                        "Señal en banda GW debe dar is_excess_coherence=True")
        self.assertGreater(res['A_eff_gw_band'], res['A_eff_ctrl_band'],
                           "A_eff en banda GW debe superar banda de control")


class TestSilentCollisionVerdict(unittest.TestCase):
    """Verifica el veredicto de colisión silenciosa."""

    def test_returns_silent_collision_result(self):
        """silent_collision_verdict debe retornar SilentCollisionResult."""
        res = s1.silent_collision_verdict(A_eff=0.9, duration=0.1)
        self.assertIsInstance(res, s1.SilentCollisionResult)

    def test_flag_true_when_both_thresholds_met(self):
        """flag_silent_collision debe ser True cuando A_eff ≥ umbral Y duration ≥ umbral."""
        res = s1.silent_collision_verdict(A_eff=0.90, duration=0.10)
        self.assertTrue(res.flag_silent_collision)

    def test_flag_false_when_A_eff_below_threshold(self):
        """flag_silent_collision debe ser False si A_eff < umbral."""
        res = s1.silent_collision_verdict(A_eff=0.50, duration=0.10)
        self.assertFalse(res.flag_silent_collision)

    def test_flag_false_when_duration_below_threshold(self):
        """flag_silent_collision debe ser False si duration < umbral."""
        res = s1.silent_collision_verdict(A_eff=0.90, duration=0.01)
        self.assertFalse(res.flag_silent_collision)

    def test_silent_score_positive(self):
        """silent_score debe ser positivo para A_eff > 0 y duration > 0."""
        res = s1.silent_collision_verdict(A_eff=0.8, duration=0.1)
        self.assertGreater(res.silent_score, 0.0)

    def test_silent_score_monotone_in_A_eff(self):
        """silent_score debe aumentar con A_eff (para duración fija)."""
        duration = 0.1
        scores = [
            s1.silent_collision_verdict(A_eff=a, duration=duration).silent_score
            for a in [0.1, 0.4, 0.7, 0.9]
        ]
        for i in range(len(scores) - 1):
            self.assertLess(scores[i], scores[i + 1],
                            "silent_score debe ser monótono creciente en A_eff")

    def test_silent_score_monotone_in_duration(self):
        """silent_score debe aumentar con duration (para A_eff fija)."""
        A_eff = 0.8
        scores = [
            s1.silent_collision_verdict(A_eff=A_eff, duration=d).silent_score
            for d in [0.05, 0.10, 0.20, 0.50]
        ]
        for i in range(len(scores) - 1):
            self.assertLess(scores[i], scores[i + 1],
                            "silent_score debe ser monótono creciente en duration")

    def test_silent_score_formula(self):
        """Verificar la fórmula: silent_score = A_eff × log1p(duration / threshold)."""
        A_eff = 0.8
        duration = 0.1
        thr = 0.05
        expected = A_eff * np.log1p(duration / thr)
        res = s1.silent_collision_verdict(A_eff=A_eff, duration=duration,
                                          threshold_duration=thr)
        self.assertAlmostEqual(res.silent_score, expected, places=10)

    def test_continuous_score_not_binary(self):
        """El score continuo debe tener múltiples valores distintos."""
        scores = set()
        for a_eff in [0.1, 0.3, 0.5, 0.7, 0.9]:
            for dur in [0.05, 0.1, 0.3, 0.5]:
                sc = s1.silent_collision_verdict(A_eff=a_eff, duration=dur).silent_score
                scores.add(round(sc, 6))
        # Debe haber al menos 10 valores distintos (no binario)
        self.assertGreater(len(scores), 10,
                           "silent_score debe ser continuo, no binario")


class TestEEGModuleIndependence(unittest.TestCase):
    """Verifica que el módulo EEG es independiente del análisis GW."""

    def test_demo_eeg_function_exists(self):
        """demo_eeg debe existir en shadow1_analysis."""
        self.assertTrue(callable(s1.demo_eeg),
                        "demo_eeg debe ser una función callable")

    def test_demo_eeg_runs_without_error(self):
        """demo_eeg debe ejecutarse sin errores."""
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            s1.demo_eeg()

    def test_eeg_not_imported_at_module_level(self):
        """
        shadow1_analysis no debe importar módulos EEG externos a nivel global.
        La función demo_eeg usa solo compute_phase_coherence y numpy.
        """
        # Verificar que shadow1_analysis.py no importa módulos EEG externos
        module_file = s1.__file__
        with open(module_file, 'r') as fh:
            content = fh.read()
        # No debe haber importaciones de paquetes EEG externos a nivel global
        # (mne, pyedflib, etc.)
        for pkg in ['import mne', 'import pyedflib', 'import neo']:
            self.assertNotIn(pkg, content,
                             f"shadow1_analysis no debe importar {pkg} globalmente")


class TestCompleteAnalysis(unittest.TestCase):
    """Test de integración del análisis completo Shadow-1."""

    def test_analizar_shadow1_returns_dict(self):
        """analizar_shadow1 debe retornar un dict con las claves esperadas."""
        result = s1.analizar_shadow1(mostrar_detalles=False)
        required_keys = {'bayes', 'chirp_mass', 'coherence',
                         'time_slide', 'band_control', 'silent_collision'}
        for key in required_keys:
            self.assertIn(key, result, f"Falta clave: {key}")

    def test_analizar_shadow1_bayes_has_canonical_field(self):
        """El resultado del análisis debe tener ln_bayes_factor."""
        result = s1.analizar_shadow1(mostrar_detalles=False)
        self.assertTrue(hasattr(result['bayes'], 'ln_bayes_factor'))

    def test_analizar_shadow1_verdict_has_score(self):
        """El veredicto debe tener silent_score continuo."""
        result = s1.analizar_shadow1(mostrar_detalles=False)
        verdict = result['silent_collision']
        self.assertTrue(hasattr(verdict, 'silent_score'))
        self.assertIsInstance(verdict.silent_score, float)

    def test_analizar_shadow1_with_synthetic_data(self):
        """El análisis debe funcionar con datos sintéticos proporcionados."""
        rng = np.random.default_rng(seed=42)
        N = 4096
        data_h1 = rng.normal(0, 4e-24, N)
        data_l1 = rng.normal(0, 4e-24, N)
        result = s1.analizar_shadow1(data_h1=data_h1, data_l1=data_l1,
                                     mostrar_detalles=False)
        self.assertIn('bayes', result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
