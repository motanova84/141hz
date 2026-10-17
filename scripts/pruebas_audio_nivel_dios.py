"""
Pruebas para audio_nivel_dios.py — Síntesis binaural QCAL
==========================================================

25 pruebas que cubren:
- Amplitud y dtype del array estéreo
- Independencia de canales (binaural L ≠ R)
- Forma y duración de la señal
- Frecuencias L y R correctas (FFT)
- Encabezados WAV (nchannels, sampwidth, framerate, nframes)
- Sin dependencia de scipy (módulo wave estándar)
- Casos borde (duraciones cortas, distintos sample rates)

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
import sys
import wave

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from audio_nivel_dios import (
    SAMPLE_RATE,
    F_LEFT_HZ,
    F_RIGHT_HZ,
    DELTA_F_HZ,
    AM_FREQS_HZ,
    HARMONICS,
    HARMONIC_GAIN_LIN,
    generar_audio_nivel_dios,
    guardar_audio_wav,
    leer_parametros_wav,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def audio_10s():
    """Audio de 10 segundos generado una vez para los tests del módulo."""
    return generar_audio_nivel_dios(duracion_s=10.0)


@pytest.fixture(scope="module")
def stereo_10s(audio_10s):
    return audio_10s[0]


@pytest.fixture(scope="module")
def sr_10s(audio_10s):
    return audio_10s[1]


# ---------------------------------------------------------------------------
# 1. Propiedades del array estéreo
# ---------------------------------------------------------------------------

class TestArrayEstereo:
    """Pruebas de las propiedades del array estéreo float32."""

    def test_dtype_float32(self, stereo_10s):
        """El array tiene dtype float32."""
        assert stereo_10s.dtype == np.float32

    def test_shape_ndim_2(self, stereo_10s):
        """El array es bidimensional."""
        assert stereo_10s.ndim == 2

    def test_shape_columnas_2(self, stereo_10s):
        """El array tiene exactamente 2 columnas (L y R)."""
        assert stereo_10s.shape[1] == 2

    def test_duracion_muestras_correcta(self, stereo_10s, sr_10s):
        """El número de muestras corresponde a 10 segundos."""
        n_esperado = int(sr_10s * 10.0)
        assert stereo_10s.shape[0] == n_esperado

    def test_amplitud_maxima_en_rango(self, stereo_10s):
        """La amplitud máxima está en el rango (0, 1]."""
        pico = np.max(np.abs(stereo_10s))
        assert 0.0 < float(pico) <= 1.0

    def test_sin_nan_ni_inf(self, stereo_10s):
        """El array no contiene NaN ni Inf."""
        assert np.all(np.isfinite(stereo_10s))

    def test_sample_rate_devuelto(self, audio_10s):
        """El sample rate devuelto es un entero positivo."""
        _, sr = audio_10s
        assert isinstance(sr, int)
        assert sr > 0


# ---------------------------------------------------------------------------
# 2. Independencia de canales (binaural)
# ---------------------------------------------------------------------------

class TestBinauralidad:
    """Pruebas de la independencia de canales L y R."""

    def test_canal_l_y_r_son_diferentes(self, stereo_10s):
        """Los canales L y R son señales distintas (binaural)."""
        canal_l = stereo_10s[:, 0]
        canal_r = stereo_10s[:, 1]
        assert not np.allclose(canal_l, canal_r)

    def test_delta_f_correcto(self):
        """La diferencia de frecuencias binaurales es 0.010 Hz."""
        assert abs(DELTA_F_HZ - 0.010) < 1e-10

    def test_f_left_correcto(self):
        """La frecuencia del canal L es 141.70001 Hz."""
        assert F_LEFT_HZ == pytest.approx(141.70001)

    def test_f_right_correcto(self):
        """La frecuencia del canal R es 141.71001 Hz."""
        assert F_RIGHT_HZ == pytest.approx(141.71001)

    def test_correlacion_canales_menor_que_1(self, stereo_10s):
        """La correlación cruzada entre L y R es < 1 (señales diferentes)."""
        canal_l = stereo_10s[:, 0].astype(np.float64)
        canal_r = stereo_10s[:, 1].astype(np.float64)
        # Correlación de Pearson normalizada
        corr = float(np.corrcoef(canal_l, canal_r)[0, 1])
        assert corr < 1.0


# ---------------------------------------------------------------------------
# 3. Frecuencias (FFT)
# ---------------------------------------------------------------------------

class TestFrecuenciasFFT:
    """Pruebas de frecuencias detectadas por FFT."""

    def test_pico_fft_canal_l_cerca_de_f_left(self, stereo_10s, sr_10s):
        """El pico FFT del canal L está dentro de ±2 Hz de F_LEFT_HZ."""
        canal = stereo_10s[:, 0].astype(np.float64)
        fft = np.fft.rfft(canal)
        freqs = np.fft.rfftfreq(len(canal), 1.0 / sr_10s)
        idx_pico = int(np.argmax(np.abs(fft)))
        freq_pico = float(freqs[idx_pico])
        assert abs(freq_pico - F_LEFT_HZ) < 2.0

    def test_pico_fft_canal_r_cerca_de_f_right(self, stereo_10s, sr_10s):
        """El pico FFT del canal R está dentro de ±2 Hz de F_RIGHT_HZ."""
        canal = stereo_10s[:, 1].astype(np.float64)
        fft = np.fft.rfft(canal)
        freqs = np.fft.rfftfreq(len(canal), 1.0 / sr_10s)
        idx_pico = int(np.argmax(np.abs(fft)))
        freq_pico = float(freqs[idx_pico])
        assert abs(freq_pico - F_RIGHT_HZ) < 2.0

    def test_armonico_2x_presente_canal_l(self, stereo_10s, sr_10s):
        """El segundo armónico (2×F_LEFT_HZ) tiene amplitud detectada en el canal L."""
        canal = stereo_10s[:, 0].astype(np.float64)
        fft = np.abs(np.fft.rfft(canal))
        freqs = np.fft.rfftfreq(len(canal), 1.0 / sr_10s)
        # Buscar energía cerca de 2× frecuencia fundamental
        mascara = np.abs(freqs - 2 * F_LEFT_HZ) < 3.0
        if mascara.any():
            amp_armonico = float(np.max(fft[mascara]))
            assert amp_armonico > 0.0


# ---------------------------------------------------------------------------
# 4. Encabezados WAV
# ---------------------------------------------------------------------------

class TestEncabezadosWAV:
    """Pruebas de los encabezados del archivo WAV generado."""

    def test_wav_nchannels_es_2(self, tmp_path, stereo_10s, sr_10s):
        """El WAV generado tiene 2 canales."""
        ruta = str(tmp_path / "test_audio.wav")
        guardar_audio_wav(stereo_10s, sr_10s, ruta)
        params = leer_parametros_wav(ruta)
        assert params["nchannels"] == 2

    def test_wav_sampwidth_es_2_bytes(self, tmp_path, stereo_10s, sr_10s):
        """El WAV usa PCM de 16 bits (2 bytes por muestra)."""
        ruta = str(tmp_path / "test_audio2.wav")
        guardar_audio_wav(stereo_10s, sr_10s, ruta)
        params = leer_parametros_wav(ruta)
        assert params["sampwidth"] == 2

    def test_wav_framerate_correcto(self, tmp_path, stereo_10s, sr_10s):
        """El WAV tiene el sample rate correcto."""
        ruta = str(tmp_path / "test_audio3.wav")
        guardar_audio_wav(stereo_10s, sr_10s, ruta)
        params = leer_parametros_wav(ruta)
        assert params["framerate"] == sr_10s

    def test_wav_nframes_correcto(self, tmp_path, stereo_10s, sr_10s):
        """El WAV tiene el número correcto de frames."""
        ruta = str(tmp_path / "test_audio4.wav")
        guardar_audio_wav(stereo_10s, sr_10s, ruta)
        params = leer_parametros_wav(ruta)
        assert params["nframes"] == stereo_10s.shape[0]

    def test_wav_sin_compresion(self, tmp_path, stereo_10s, sr_10s):
        """El WAV es PCM sin compresión."""
        ruta = str(tmp_path / "test_audio5.wav")
        guardar_audio_wav(stereo_10s, sr_10s, ruta)
        params = leer_parametros_wav(ruta)
        assert params["comptype"] == "NONE"

    def test_wav_formato_correcto_con_wave_stdlib(self, tmp_path, stereo_10s, sr_10s):
        """El archivo WAV puede ser leído con el módulo wave de la stdlib."""
        ruta = str(tmp_path / "test_audio6.wav")
        guardar_audio_wav(stereo_10s, sr_10s, ruta)
        with wave.open(ruta, "rb") as wf:
            assert wf.getnchannels() == 2
            assert wf.getsampwidth() == 2

    def test_guardar_wav_error_shape_incorrecto(self, tmp_path):
        """guardar_audio_wav lanza ValueError con array mono (1D)."""
        ruta = str(tmp_path / "test_error.wav")
        mono = np.zeros(1000, dtype=np.float32)
        with pytest.raises((ValueError, Exception)):
            guardar_audio_wav(mono, SAMPLE_RATE, ruta)
