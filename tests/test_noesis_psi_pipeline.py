#!/usr/bin/env python3
"""
Tests para scripts/noesis_psi_pipeline.py
==========================================
Valida las funciones del pipeline de análisis Noésico PSI.

Uso:
    pytest tests/test_noesis_psi_pipeline.py -v
    python tests/test_noesis_psi_pipeline.py
"""

import sys
import os
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

# Importar módulo a testear
try:
    from scripts.noesis_psi_pipeline import (
        bandpass_noesis,
        compute_psi_windows,
        generate_resilience_curve,
        bin_results,
        run_pipeline,
        F0, FS, BW, N_BINS,
    )
except ImportError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
    from noesis_psi_pipeline import (
        bandpass_noesis,
        compute_psi_windows,
        generate_resilience_curve,
        bin_results,
        run_pipeline,
        F0, FS, BW, N_BINS,
    )


# ---------------------------------------------------------------------------
# Constantes de referencia
# ---------------------------------------------------------------------------
FS_TEST = 4096
F0_TEST = 141.7001
DURATION_SHORT = 4  # s — señal corta para tests rápidos


class TestConstants:
    """Verifica que las constantes principales sean correctas."""

    def test_f0_value(self):
        assert F0 == 141.7001

    def test_fs_value(self):
        assert FS == 4096

    def test_bw_positive(self):
        assert BW > 0

    def test_n_bins_positive(self):
        assert N_BINS > 0


class TestBandpassNoesis:
    """Pruebas unitarias para la función de filtrado."""

    def setup_method(self):
        n = int(DURATION_SHORT * FS_TEST)
        t = np.arange(n) / FS_TEST
        rng = np.random.default_rng(0)
        self.signal_on = np.sin(2 * np.pi * F0_TEST * t)          # en banda
        self.signal_off = np.sin(2 * np.pi * 500.0 * t)            # fuera de banda
        self.noise = rng.normal(0, 0.1, n)

    def test_output_shape(self):
        """La salida tiene el mismo tamaño que la entrada."""
        out = bandpass_noesis(self.signal_on)
        assert out.shape == self.signal_on.shape

    def test_passes_f0(self):
        """La señal en f₀ pasa el filtro con amplitud significativa."""
        out = bandpass_noesis(self.signal_on)
        assert np.std(out) > 0.1

    def test_attenuates_out_of_band(self):
        """Una señal fuera de banda es fuertemente atenuada."""
        out = bandpass_noesis(self.signal_off)
        assert np.std(out) < 0.05 * np.std(self.signal_off)

    def test_custom_parameters(self):
        """Acepta fs, f0 y bw personalizados."""
        out = bandpass_noesis(self.signal_on, fs=FS_TEST, f0=F0_TEST, bw=2.0)
        assert out.shape == self.signal_on.shape


class TestComputePsiWindows:
    """Pruebas para el cálculo de Ψ por ventana."""

    def setup_method(self):
        n = int(DURATION_SHORT * FS_TEST)
        t = np.arange(n) / FS_TEST
        rng = np.random.default_rng(1)
        sig = np.sin(2 * np.pi * F0_TEST * t)
        noise = rng.normal(0, 0.2, n)
        self.canal1 = bandpass_noesis(sig + noise)
        self.canal2 = bandpass_noesis(sig + rng.normal(0, 0.2, n))

    def test_returns_list(self):
        psi = compute_psi_windows(self.canal1, self.canal2)
        assert isinstance(psi, list)

    def test_non_empty(self):
        psi = compute_psi_windows(self.canal1, self.canal2)
        assert len(psi) > 0

    def test_non_negative(self):
        """PSD × Coherencia ≥ 0 siempre."""
        psi = compute_psi_windows(self.canal1, self.canal2)
        assert all(v >= 0.0 for v in psi)

    def test_coherent_signal_higher_psi(self):
        """Canales coherentes producen Ψ mayor que canales no correlacionados."""
        n = int(DURATION_SHORT * FS_TEST)
        t = np.arange(n) / FS_TEST
        rng = np.random.default_rng(2)

        sig = np.sin(2 * np.pi * F0_TEST * t)
        c1 = bandpass_noesis(sig + rng.normal(0, 0.05, n))
        c2_coherent = bandpass_noesis(sig + rng.normal(0, 0.05, n))
        c2_incoherent = bandpass_noesis(rng.normal(0, 1.0, n))

        psi_coh = np.mean(compute_psi_windows(c1, c2_coherent))
        psi_inc = np.mean(compute_psi_windows(c1, c2_incoherent))
        assert psi_coh > psi_inc


class TestGenerateResilienceCurve:
    """Pruebas para la generación de la curva de resiliencia."""

    def setup_method(self):
        # Usar duración ≥ 3 × ventana (2 s) para garantizar al menos una ventana
        self.snr_values = np.array([0.5, 1.0, 2.0, 5.0])
        self.rng = np.random.default_rng(42)
        self.duration_s = 8  # s — suficiente para varias ventanas de 2 s

    def test_returns_dataframe(self):
        df = generate_resilience_curve(
            duration_s=self.duration_s, snr_values=self.snr_values, rng=self.rng
        )
        assert isinstance(df, pd.DataFrame)

    def test_columns_present(self):
        df = generate_resilience_curve(
            duration_s=self.duration_s, snr_values=self.snr_values, rng=self.rng
        )
        for col in ['snr', 'psi_mean', 'psi_std', 'psi_median', 'n_windows']:
            assert col in df.columns, f"Columna faltante: {col}"

    def test_monotonic_tendency(self):
        """Ψ medio debe crecer con el SNR — verificado con rango amplio."""
        snr_wide = np.array([0.1, 0.5, 2.0, 10.0])
        rng = np.random.default_rng(7)
        df = generate_resilience_curve(
            duration_s=self.duration_s, snr_values=snr_wide, rng=rng
        )
        # El SNR más alto debe producir mayor Ψ que el SNR más bajo
        low_snr_psi = df[df['snr'] == df['snr'].min()]['psi_mean'].values[0]
        high_snr_psi = df[df['snr'] == df['snr'].max()]['psi_mean'].values[0]
        assert high_snr_psi > low_snr_psi

    def test_psi_non_negative(self):
        df = generate_resilience_curve(
            duration_s=self.duration_s, snr_values=self.snr_values, rng=self.rng
        )
        assert (df['psi_mean'] >= 0).all()


class TestBinResults:
    """Pruebas para la función de binning."""

    def setup_method(self):
        snr = np.logspace(-1, 1, 30)
        psi = snr ** 2 * 1e-6
        self.df = pd.DataFrame({'snr': snr, 'psi_mean': psi})

    def test_returns_dataframe(self):
        df_b = bin_results(self.df)
        assert isinstance(df_b, pd.DataFrame)

    def test_expected_columns(self):
        df_b = bin_results(self.df)
        for col in ['snr_center', 'psi_mean_bin', 'psi_std_bin']:
            assert col in df_b.columns

    def test_fewer_rows_than_input(self):
        df_b = bin_results(self.df, n_bins=N_BINS)
        assert len(df_b) <= N_BINS

    def test_no_nan_in_mean(self):
        df_b = bin_results(self.df)
        assert not df_b['psi_mean_bin'].isna().any()


class TestRunPipeline:
    """Pruebas de integración para el pipeline completo."""

    def test_pipeline_creates_files(self):
        """El pipeline genera el CSV y el PNG en el directorio indicado."""
        with tempfile.TemporaryDirectory() as tmp:
            results = run_pipeline(output_dir=tmp)
            assert Path(results['csv']).exists(), "CSV no generado"
            assert Path(results['plot']).exists(), "PNG no generado"

    def test_pipeline_returns_dict(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = run_pipeline(output_dir=tmp)
            assert isinstance(results, dict)
            for key in ['csv', 'plot', 'snr_survival', 'psi_max', 'n_snr_points']:
                assert key in results, f"Clave faltante: {key}"

    def test_csv_has_correct_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = run_pipeline(output_dir=tmp)
            df = pd.read_csv(results['csv'])
            for col in ['snr', 'psi_mean', 'psi_std', 'psi_median', 'n_windows']:
                assert col in df.columns, f"Columna faltante en CSV: {col}"

    def test_snr_survival_positive(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = run_pipeline(output_dir=tmp)
            assert results['snr_survival'] > 0

    def test_psi_max_positive(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = run_pipeline(output_dir=tmp)
            assert results['psi_max'] > 0

# ---------------------------------------------------------------------------
# Ejecución directa
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(pytest.main([__file__, '-v']))
