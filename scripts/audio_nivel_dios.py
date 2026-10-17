"""
Audio Nivel Dios — Síntesis binaural QCAL 141.70001 Hz
=======================================================

Síntesis de audio binaural en Python puro, SIN dependencia de scipy.

Características:
  Canal L : 141.70001 Hz
  Canal R : 141.71001 Hz
  Δf      : 0.010 Hz — latido binaural (banda theta)
  AM multi-fase : 0.1 Hz / 0.01 Hz / 4.2 Hz
  Armónicos 2× / 3× / 4× a −35 dB (≈ factor 0.01778)

API pública
-----------
  generar_audio_nivel_dios(duracion_s) → (ndarray float32 [N, 2], int sr)
  guardar_audio_wav(stereo, sr, ruta)

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENCIA: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
import os
import struct
import wave
from typing import Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

SAMPLE_RATE = 44100          # Hz
F_LEFT_HZ = 141.70001        # Hz — canal L
F_RIGHT_HZ = 141.71001       # Hz — canal R
DELTA_F_HZ = F_RIGHT_HZ - F_LEFT_HZ   # 0.010 Hz binaural beat

# Modulación de amplitud multi-fase (Hz)
AM_FREQS_HZ = (0.1, 0.01, 4.2)
AM_DEPTH = 0.25              # profundidad AM (±25 %)

# Armónicos adicionales
HARMONICS = (2, 3, 4)
HARMONIC_GAIN_DB = -35.0
HARMONIC_GAIN_LIN = 10 ** (HARMONIC_GAIN_DB / 20.0)  # ≈ 0.017783

# Headroom para evitar clipping
HEADROOM_DB = -3.0
HEADROOM_LIN = 10 ** (HEADROOM_DB / 20.0)


# ---------------------------------------------------------------------------
# Generación
# ---------------------------------------------------------------------------

def _generar_canal(
    freq_hz: float,
    duracion_s: float,
    sr: int,
    am_freqs: Tuple[float, ...] = AM_FREQS_HZ,
    am_depth: float = AM_DEPTH,
    harmonics: Tuple[int, ...] = HARMONICS,
    harmonic_gain: float = HARMONIC_GAIN_LIN,
) -> np.ndarray:
    """
    Genera un array float64 con la señal de un canal mono.

    La señal incluye:
    - Portadora fundamental a ``freq_hz``
    - AM multi-fase con tres frecuencias de modulación
    - Armónicos 2×, 3×, 4× a ``harmonic_gain`` lineal
    """
    n_muestras = int(sr * duracion_s)
    t = np.arange(n_muestras) / sr

    # Portadora
    portadora = np.sin(2.0 * math.pi * freq_hz * t)

    # Modulación AM multi-fase
    am = np.ones(n_muestras)
    fase_inicial = 0.0
    for f_am in am_freqs:
        am += am_depth * np.sin(2.0 * math.pi * f_am * t + fase_inicial)
        fase_inicial += math.pi / len(am_freqs)
    # Normalizar al rango original: la suma de todos los términos AM es
    # am = 1 + Σ(am_depth * sin(...)), con máximo = 1 + len(am_freqs)*am_depth
    # Dividir por ese máximo asegura que am ∈ [0, 1] siempre.
    am /= (1.0 + len(am_freqs) * am_depth)

    senal = portadora * am

    # Armónicos
    for h in harmonics:
        senal += harmonic_gain * np.sin(2.0 * math.pi * freq_hz * h * t)

    return senal


def generar_audio_nivel_dios(
    duracion_s: float = 10.0,
    sr: int = SAMPLE_RATE,
) -> Tuple[np.ndarray, int]:
    """
    Genera el audio binaural "Nivel Dios" QCAL 141.70001 Hz.

    Parameters
    ----------
    duracion_s : float
        Duración en segundos (por defecto 10).
    sr : int
        Frecuencia de muestreo (por defecto 44100 Hz).

    Returns
    -------
    stereo : np.ndarray, shape (N, 2), dtype float32
        Array estéreo normalizado. Canal 0 = L (141.70001 Hz),
        Canal 1 = R (141.71001 Hz).
    sr : int
        Frecuencia de muestreo.
    """
    canal_l = _generar_canal(F_LEFT_HZ, duracion_s, sr)
    canal_r = _generar_canal(F_RIGHT_HZ, duracion_s, sr)

    stereo = np.stack([canal_l, canal_r], axis=1)

    # Normalizar y aplicar headroom
    pico = np.max(np.abs(stereo))
    if pico > 0:
        stereo = stereo / pico * HEADROOM_LIN

    return stereo.astype(np.float32), sr


# ---------------------------------------------------------------------------
# Escritura WAV (sin scipy) usando el módulo estándar ``wave``
# ---------------------------------------------------------------------------

def guardar_audio_wav(
    stereo: np.ndarray,
    sr: int,
    ruta: str,
) -> str:
    """
    Escribe un archivo WAV PCM de 16 bits estéreo.

    Utiliza únicamente módulos de la biblioteca estándar de Python
    (``wave`` + ``struct``). NO requiere scipy.

    Parameters
    ----------
    stereo : np.ndarray, shape (N, 2), dtype float32
        Array estéreo en rango [-1, 1].
    sr : int
        Frecuencia de muestreo.
    ruta : str
        Ruta de salida del archivo WAV.

    Returns
    -------
    str
        Ruta absoluta del archivo guardado.
    """
    if stereo.ndim != 2 or stereo.shape[1] != 2:
        raise ValueError("stereo debe tener forma (N, 2)")

    directorio = os.path.dirname(os.path.abspath(ruta))
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    # Convertir float32 → int16
    pcm_int16 = np.clip(stereo * 32767.0, -32768, 32767).astype(np.int16)

    n_muestras = pcm_int16.shape[0]
    n_canales = 2
    sampwidth = 2   # bytes por muestra (int16)

    with wave.open(ruta, "wb") as wf:
        wf.setnchannels(n_canales)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sr)
        # Intercalar muestras L/R
        datos = pcm_int16.tobytes()
        wf.writeframes(datos)

    return os.path.abspath(ruta)


def leer_parametros_wav(ruta: str) -> dict:
    """
    Lee los parámetros de cabecera de un archivo WAV.

    Parameters
    ----------
    ruta : str
        Ruta al archivo WAV.

    Returns
    -------
    dict con keys: nchannels, sampwidth, framerate, nframes, comptype, compname
    """
    with wave.open(ruta, "rb") as wf:
        return {
            "nchannels": wf.getnchannels(),
            "sampwidth": wf.getsampwidth(),
            "framerate": wf.getframerate(),
            "nframes": wf.getnframes(),
            "comptype": wf.getcomptype(),
            "compname": wf.getcompname(),
        }


if __name__ == "__main__":
    os.makedirs("audio", exist_ok=True)
    stereo, sr = generar_audio_nivel_dios(duracion_s=10)
    ruta = guardar_audio_wav(stereo, sr, "audio/NivelDios_demo.wav")
    print(f"Audio guardado: {ruta}")
    print(f"Shape: {stereo.shape}, dtype: {stereo.dtype}, sr: {sr} Hz")
    print(f"L = {F_LEFT_HZ} Hz, R = {F_RIGHT_HZ} Hz, Δf = {DELTA_F_HZ:.3f} Hz (binaural theta)")
    params = leer_parametros_wav(ruta)
    print(f"WAV params: {params}")
