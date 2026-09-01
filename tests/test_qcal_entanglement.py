#!/usr/bin/env python3
"""
Tests for QCAL entanglement dynamics and telemetry persistence.
"""

import zipfile

import numpy as np
import pytest
from scipy.io import wavfile

from src.qcal_entanglement import (
    F0_REFERENCIA_HZ,
    H_PLANCK_SI,
    QCALDeploymentBundle,
    QCALEntanglementEngine,
    QCALTelemetryExporter,
    SPIN_DIMENSION,
    aplicar_itd_padica,
    anclar_resonancia_global,
    calcular_gap_frecuencia_hz,
    construir_hamiltoniano_qcal,
    ejecutar_despliegue_dinamico_qcal,
    ejecutar_barrido_temporal,
    guardar_audio_binaural_wav,
    graficar_telemetria_qcal,
    sintetizar_audio_binaural_qcal,
)


def test_estado_puro_inicial_preserva_pureza_y_entropia():
    """The coherent product state should start pure and unentangled."""
    engine = QCALEntanglementEngine()

    rho_0 = engine.construir_estado_puro_inicial(N_spec=3)
    rho_spin_0 = engine.traza_parcial_spin(rho_0, N_spec=3)

    assert rho_0.shape == (9, 9)
    assert np.isclose(engine.evaluar_pureza(rho_spin_0), 1.0)
    assert np.isclose(engine.entropia_von_neumann(rho_spin_0), 0.0, atol=1e-9)


def test_ajuste_espectral_calibra_gap_fundamental():
    """The spectral gap should match h·f₀ after scaling."""
    engine = QCALEntanglementEngine()

    autovals_joules = engine.ajustar_escala_espectral_qcal(np.array([1.0, 1.5, 2.0]))
    gap = autovals_joules[-1] - autovals_joules[0]

    assert np.isclose(gap, H_PLANCK_SI * F0_REFERENCIA_HZ)


def test_construir_hamiltoniano_genera_gap_positivo():
    """The composed Hamiltonian should remain Hermitian and have a positive gap."""
    engine = QCALEntanglementEngine()
    h_total = construir_hamiltoniano_qcal(engine, np.array([1.0, 1.5, 2.0, 2.5]))

    assert h_total.shape == (12, 12)
    assert np.allclose(h_total, h_total.conj().T)

    energias = np.linalg.eigvalsh(h_total)
    assert energias[-1] > energias[0]


def test_anclar_resonancia_global_fija_gap_objetivo():
    """Anchoring should force the global gap back to the target frequency."""
    engine = QCALEntanglementEngine()
    h_total = construir_hamiltoniano_qcal(engine, np.array([1.0, 1.5, 2.0]), g_int=0.75)

    anchored = anclar_resonancia_global(h_total)

    assert np.isclose(calcular_gap_frecuencia_hz(anchored), F0_REFERENCIA_HZ)


def test_barrido_temporal_persiste_telemetria_y_estados(tmp_path):
    """Temporal sweeps should emit binary snapshots and compressed telemetry."""
    engine = QCALEntanglementEngine()
    exporter = QCALTelemetryExporter(output_dir=tmp_path)
    num_pasos = 10
    guardar_cada = 3

    result = ejecutar_barrido_temporal(
        engine=engine,
        exporter=exporter,
        num_pasos=num_pasos,
        dt=1e-4,
        guardar_cada=guardar_cada,
        anclar_frecuencia=True,
        generar_csv=True,
        generar_figura=True,
    )

    assert result.log_path.exists()
    assert result.csv_path is not None and result.csv_path.exists()
    assert result.figure_path is not None and result.figure_path.exists()
    assert len(result.state_paths) == len(range(0, num_pasos + 1, guardar_cada))
    assert all(path.exists() for path in result.state_paths)
    h_total = construir_hamiltoniano_qcal(engine, np.array([1.0, 1.5, 2.0]))
    assert calcular_gap_frecuencia_hz(h_total) != F0_REFERENCIA_HZ
    assert np.isclose(result.frecuencia_efectiva_hz, F0_REFERENCIA_HZ)
    assert np.allclose(result.frecuencias, np.full_like(result.frecuencias, result.frecuencia_efectiva_hz))
    assert np.all(result.purezas <= 1.0 + 1e-12)
    assert np.all(result.purezas >= (1.0 / 3.0) - 1e-12)
    assert result.entropias[0] <= result.entropias[-1]

    persisted_state = np.load(result.state_paths[0])
    assert persisted_state.shape == (SPIN_DIMENSION, SPIN_DIMENSION)
    assert persisted_state.dtype == np.complex128

    trajectory = np.load(result.log_path)
    assert set(trajectory.files) == {"t", "gamma", "S", "f0"}
    assert trajectory["t"].shape == (num_pasos + 1,)
    assert np.allclose(trajectory["gamma"], result.purezas)

    csv_lines = result.csv_path.read_text(encoding="utf-8").strip().splitlines()
    assert csv_lines[0] == "t_s,S_bits,pureza_gamma"
    assert len(csv_lines) == num_pasos + 2


def test_registro_telemetria_valida_longitudes(tmp_path):
    """Telemetry arrays must all have the same length."""
    exporter = QCALTelemetryExporter(output_dir=tmp_path)

    with pytest.raises(ValueError, match="misma longitud"):
        exporter.registrar_trayectoria_log(
            np.array([0.0, 1.0]),
            np.array([1.0]),
            np.array([0.0, 0.1]),
            np.array([F0_REFERENCIA_HZ, F0_REFERENCIA_HZ]),
        )


def test_ajuste_espectral_rechaza_gap_nulo():
    """The scaling helper should reject degenerate input spectra."""
    engine = QCALEntanglementEngine()

    with pytest.raises(ValueError, match="gap positivo"):
        engine.ajustar_escala_espectral_qcal(np.array([1.0, 1.0, 1.0]))


def test_graficar_telemetria_qcal_guarda_png(tmp_path):
    """Plotting helper should save a PNG without requiring interactive display."""
    output_path = tmp_path / "telemetria.png"
    saved_path = graficar_telemetria_qcal(
        np.array([0.0, 1.0e-4, 2.0e-4]),
        np.array([0.0, 0.1, 0.2]),
        np.array([1.0, 0.95, 0.9]),
        output_path=output_path,
        show=False,
    )

    assert saved_path == output_path
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_aplicar_itd_padica_retrasa_canal_derecho():
    """The right channel should be delayed by the expected number of samples."""
    audio_l = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
    audio_r = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)

    delayed_l, delayed_r, delay_samples = aplicar_itd_padica(
        audio_l,
        audio_r,
        sample_rate=4_000,
        p_izq=2,
        p_der=3,
        retraso_maximo_s=1e-3,
    )

    assert delay_samples == 2
    assert np.array_equal(delayed_l, audio_l)
    assert np.array_equal(delayed_r, np.array([0.0, 0.0, 1.0, 2.0], dtype=np.float32))


def test_aplicar_itd_padica_sin_retraso_para_mismo_primo():
    """Equal p-adic branches should not introduce interaural delay."""
    audio = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    delayed_l, delayed_r, delay_samples = aplicar_itd_padica(audio, audio, p_izq=3, p_der=3)

    assert delay_samples == 0
    assert np.array_equal(delayed_l, audio)
    assert np.array_equal(delayed_r, audio)


def test_sintesis_binaural_y_wav_float32(tmp_path):
    """The binaural renderer should emit float32 stereo audio and a readable WAV."""
    tiempos = np.array([0.0, 0.25, 0.5], dtype=float)
    entropias = np.array([0.0, 0.4, 0.8], dtype=float)
    purezas = np.array([1.0, 0.85, 0.7], dtype=float)

    stereo, sample_rate, itd_samples = sintetizar_audio_binaural_qcal(
        tiempos,
        entropias,
        purezas,
        sample_rate=8_000,
    )

    assert sample_rate == 8_000
    assert stereo.dtype == np.float32
    assert stereo.ndim == 2 and stereo.shape[1] == 2
    assert itd_samples > 0

    wav_path = guardar_audio_binaural_wav(stereo, sample_rate, tmp_path / "binaural.wav")
    read_sr, read_data = wavfile.read(wav_path)
    assert read_sr == sample_rate
    assert read_data.dtype == np.float32
    assert read_data.shape == stereo.shape


def test_ejecutar_despliegue_dinamico_qcal_empaqueta_bundle(tmp_path):
    """Full deployment should generate telemetry, binaural audio, and a zip bundle."""
    deployment = ejecutar_despliegue_dinamico_qcal(
        output_dir=tmp_path,
        num_pasos=12,
        dt=1e-4,
        guardar_cada=4,
        sample_rate=8_000,
    )

    assert isinstance(deployment, QCALDeploymentBundle)
    assert deployment.telemetry.log_path.exists()
    assert deployment.telemetry.csv_path is not None and deployment.telemetry.csv_path.exists()
    assert deployment.binaural.audio_path.exists()
    assert deployment.binaural.diagnostic_path.exists()
    assert deployment.manifest_path.exists()
    assert deployment.bundle_path.exists()

    with zipfile.ZipFile(deployment.bundle_path) as archive:
        names = set(archive.namelist())
    assert "qcal_dynamic_manifest.json" in names
    assert "qcal_binaural_141Hz.wav" in names
    assert "telemetria_qcal.csv" in names
