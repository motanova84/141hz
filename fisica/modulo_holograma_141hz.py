"""
╔════════════════════════════════════════════════════════════════════════════╗
║           MÓDULO DE CODIFICACIÓN HOLOGRÁFICA — 141 Hz QCAL                ║
║        Holographic Encoding Module based on Bekenstein-Hawking             ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Este módulo implementa la codificación holográfica de la frecuencia f₀:

1. Entropía superficial (principio de Bekenstein-Hawking):
   - area_efectiva_holografica: área de Planck efectiva en f₀
   - bits_holograficos_planck: recuento de bits holográficos

2. Espiral polar zeta:
   - espiral_zeta_polar(gamma_n): holograma radial-angular modulado por γₙ

3. Coherencia holográfica Ψ:
   - coherencia_holografica(f): decaimiento gaussiano alrededor de F₀_exacto
     con ancho de banda Δf_vórtice = 0.3999 Hz

4. Simulación de rebote lunar (Si5351 / LoRa):
   - simular_eco_lunar: genera la señal eco del rebote lunar
   - analizar_fft_moonbounce: extrae frecuencia pico, Δf y Ψ_proxy mediante FFT

Utiliza NumPy para una DFT eficiente cuando está disponible,
y recurre a Python puro en caso contrario.
"""

import math
import cmath

try:
    import numpy as np
    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False

from .reloj_universo_f0 import (
    F0_FLOAT,
    F0_EXACT_HZ,
    GAMMA_1,
    DELTA_FASE_ZIUSUDRA,
    FISURA_ZIUSUDRA,
    HBAR,
    C_LUZ,
)

# ============================================================================
# CONSTANTES DEL MÓDULO HOLOGRÁFICO
# ============================================================================

# Longitud de Planck (CODATA 2018)
L_PLANCK = 1.616255e-35  # m

# Constante gravitacional
G_NEWTON = 6.67430e-11  # m³·kg⁻¹·s⁻²

# Ancho de banda del vórtice holográfico (Constante de Ziusudra)
DELTA_F_VORTICE = 0.3999  # Hz — coincide con CONSTANTE_ZIUSUDRA del Pleroma

# Velocidad de la luz (alias local)
_C = C_LUZ

# Radio efectivo del holograma en f₀: R = c / (2π · f₀)
RADIO_EFECTIVO_M = _C / (2.0 * math.pi * F0_FLOAT)

# ============================================================================
# 1. ENTROPÍA SUPERFICIAL / BITS HOLOGRÁFICOS (Bekenstein-Hawking)
# ============================================================================


def area_efectiva_holografica(f_hz: float = F0_FLOAT) -> float:
    """
    Calcula el área de Planck efectiva para una frecuencia f (en Hz).

    A_eff = (c / (2π · f))²  [m²]

    Esta área representa la superficie mínima coherente con la frecuencia dada,
    siguiendo el principio holográfico de Bekenstein-Hawking.

    Args:
        f_hz: Frecuencia en Hz (por defecto f₀ = 141.7001 Hz)

    Returns:
        Área efectiva en m²
    """
    radio = _C / (2.0 * math.pi * f_hz)
    return radio ** 2


def bits_holograficos_planck(area_m2: float) -> float:
    """
    Calcula el número de bits holográficos según el principio de Bekenstein-Hawking.

    S_BH = A / (4 · L_Planck²)

    Cada L_Planck² de área superficial almacena ~ 1/4 bit de información.

    Args:
        area_m2: Área superficial en m²

    Returns:
        Número de bits holográficos (adimensional)
    """
    return area_m2 / (4.0 * L_PLANCK ** 2)


# ============================================================================
# 2. ESPIRAL POLAR ZETA — holograma radial-angular modulado por γₙ
# ============================================================================


def espiral_zeta_polar(gamma_n: float, n_puntos: int = 360) -> list:
    """
    Genera la espiral polar zeta modulada por el n-ésimo cero de Riemann γₙ.

    La espiral está definida en coordenadas polares (r, θ) como:
        r(θ) = exp(γₙ · θ / (2π · 10))
        (x, y) = (r · cos(θ), r · sin(θ))

    Donde la escala 10 normaliza la amplitud de la espiral al rango razonable.

    Args:
        gamma_n: Parte imaginaria del n-ésimo cero no trivial de ζ(s)
        n_puntos: Número de puntos en la espiral (por defecto 360)

    Returns:
        Lista de tuplas (x, y, r, theta) con los puntos de la espiral
    """
    puntos = []
    for i in range(n_puntos):
        theta = 2.0 * math.pi * i / n_puntos
        r = math.exp(gamma_n * theta / (2.0 * math.pi * 10.0))
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        puntos.append((x, y, r, theta))
    return puntos


# ============================================================================
# 3. COHERENCIA HOLOGRÁFICA Ψ — decaimiento gaussiano
# ============================================================================


def coherencia_holografica(f_hz: float,
                            f_centro: float = F0_EXACT_HZ,
                            delta_f: float = DELTA_F_VORTICE) -> float:
    """
    Calcula la coherencia holográfica Ψ con decaimiento gaussiano.

    Ψ(f) = exp(−((f − f_centro) / delta_f)²)

    El máximo Ψ = 1.0 se alcanza en f = f_centro = F0_EXACT_HZ.
    A ±delta_f el valor decae a exp(−1) ≈ 0.368.

    Args:
        f_hz: Frecuencia de evaluación en Hz
        f_centro: Frecuencia central (por defecto F0_EXACT_HZ ≈ 141.70062 Hz)
        delta_f: Ancho de banda del vórtice en Hz (por defecto 0.3999 Hz)

    Returns:
        Coherencia holográfica Ψ ∈ (0, 1]
    """
    if delta_f <= 0:
        raise ValueError("delta_f must be positive")
    return math.exp(-((f_hz - f_centro) / delta_f) ** 2)


# ============================================================================
# 4. SIMULACIÓN DE REBOTE LUNAR (Si5351 / LoRa)
# ============================================================================


def simular_eco_lunar(f_emitida: float = F0_FLOAT,
                      duracion_s: float = 1.0,
                      fs_hz: float = 4096.0,
                      retardo_s: float = 2.56,
                      atenuacion: float = 0.5) -> tuple:
    """
    Simula la señal de eco del rebote lunar de una señal Si5351 / LoRa.

    Modelo simplificado:
        señal_original(t) = sin(2π · f_emitida · t)
        eco(t) = atenuación · sin(2π · f_emitida · (t − retardo_s))
        señal_total(t) = señal_original(t) + eco(t)   para t ≥ retardo_s

    Args:
        f_emitida: Frecuencia de la señal emitida en Hz
        duracion_s: Duración de la señal en segundos
        fs_hz: Frecuencia de muestreo en Hz
        retardo_s: Retardo del eco (retardo de propagación lunar ≈ 2.56 s)
        atenuacion: Factor de atenuación del eco (0 < a ≤ 1)

    Returns:
        Tupla (tiempos, señal_total, señal_original, eco) donde cada elemento
        es una lista de floats.
    """
    if duracion_s <= 0:
        raise ValueError("duracion_s must be positive")
    if fs_hz <= 0:
        raise ValueError("fs_hz must be positive")
    if atenuacion < 0 or atenuacion > 1:
        raise ValueError("atenuacion must be in [0, 1]")

    n_muestras = int(duracion_s * fs_hz)
    tiempos = [i / fs_hz for i in range(n_muestras)]

    if _NUMPY_AVAILABLE:
        t = np.array(tiempos)
        original = np.sin(2.0 * math.pi * f_emitida * t)
        eco = np.zeros(n_muestras)
        n_retardo = int(retardo_s * fs_hz)
        if n_retardo < n_muestras:
            eco[n_retardo:] = atenuacion * np.sin(
                2.0 * math.pi * f_emitida * (t[n_retardo:] - retardo_s)
            )
        total = original + eco
        return (tiempos, total.tolist(), original.tolist(), eco.tolist())
    else:
        original = [math.sin(2.0 * math.pi * f_emitida * t) for t in tiempos]
        n_retardo = int(retardo_s * fs_hz)
        eco = [0.0] * n_muestras
        for i in range(n_retardo, n_muestras):
            eco[i] = atenuacion * math.sin(
                2.0 * math.pi * f_emitida * (tiempos[i] - retardo_s)
            )
        total = [original[i] + eco[i] for i in range(n_muestras)]
        return (tiempos, total, original, eco)


def analizar_fft_moonbounce(señal: list, fs_hz: float = 4096.0) -> dict:
    """
    Analiza la señal de rebote lunar mediante FFT para extraer:
    - Frecuencia pico (Hz)
    - Δf respecto a f₀ exacta
    - Ψ_proxy (coherencia holográfica en la frecuencia pico)

    Usa NumPy FFT si está disponible; si no, implementa una DFT en Python puro
    evaluando únicamente en las frecuencias de interés (alrededor de f₀).

    Args:
        señal: Lista de muestras de la señal temporal
        fs_hz: Frecuencia de muestreo en Hz

    Returns:
        Diccionario con claves:
            'f_pico_hz': frecuencia del pico espectral en Hz
            'delta_f_hz': Δf = f_pico − F0_EXACT_HZ
            'psi_proxy': coherencia holográfica Ψ en f_pico
            'magnitud_pico': magnitud normalizada del pico (0-1)
    """
    n = len(señal)
    if n == 0:
        raise ValueError("señal must not be empty")

    if _NUMPY_AVAILABLE:
        espectro = np.fft.rfft(señal)
        magnitudes = np.abs(espectro)
        freqs = np.fft.rfftfreq(n, d=1.0 / fs_hz)
        idx_pico = int(np.argmax(magnitudes))
        f_pico = float(freqs[idx_pico])
        mag_max = float(magnitudes[idx_pico])
        mag_norm = mag_max / (n / 2.0)
    else:
        # DFT pura en Python: evalúa solo frecuencias cercanas a f₀
        # para mayor eficiencia cuando no hay NumPy
        f_min = max(0.0, F0_FLOAT - 5.0)
        f_max = F0_FLOAT + 5.0
        # Resolución espectral ~ fs_hz / n
        delta_freq = fs_hz / n
        n_bins = int((f_max - f_min) / delta_freq) + 1
        best_mag = -1.0
        f_pico = F0_FLOAT
        for k in range(n_bins):
            freq = f_min + k * delta_freq
            # DFT manual: X(freq) = Σ x[n] · exp(−j 2π freq n / fs)
            re = sum(señal[i] * math.cos(2.0 * math.pi * freq * i / fs_hz)
                     for i in range(n))
            im = sum(-señal[i] * math.sin(2.0 * math.pi * freq * i / fs_hz)
                     for i in range(n))
            mag = math.sqrt(re ** 2 + im ** 2)
            if mag > best_mag:
                best_mag = mag
                f_pico = freq
        mag_norm = best_mag / (n / 2.0)

    delta_f = f_pico - F0_EXACT_HZ
    psi_proxy = coherencia_holografica(f_pico)

    return {
        'f_pico_hz': f_pico,
        'delta_f_hz': delta_f,
        'psi_proxy': psi_proxy,
        'magnitud_pico': mag_norm,
    }


# ============================================================================
# FUNCIÓN DE RESUMEN
# ============================================================================


def mostrar_resumen_holograma():
    """Muestra un resumen de las constantes y funciones holográficas."""
    print("\n" + "=" * 72)
    print("MÓDULO HOLOGRÁFICO 141 Hz — Bekenstein-Hawking + Espiral Zeta")
    print("=" * 72)
    a_eff = area_efectiva_holografica(F0_FLOAT)
    bits = bits_holograficos_planck(a_eff)
    print(f"  A_eff(f₀)       = {a_eff:.6e} m²")
    print(f"  Bits holográficos = {bits:.6e}")
    print(f"  Radio efectivo   = {RADIO_EFECTIVO_M:.6e} m")
    print(f"  Δf_vórtice       = {DELTA_F_VORTICE} Hz")
    print(f"  Ψ(f₀_exact)     = {coherencia_holografica(F0_EXACT_HZ):.6f}")
    print(f"  Ψ(f₀_operativo) = {coherencia_holografica(F0_FLOAT):.6f}")
    print("=" * 72)


if __name__ == "__main__":
    mostrar_resumen_holograma()
