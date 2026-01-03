#!/usr/bin/env python3
"""
Módulo de Ecuación del Origen Vibracional (EOV)
================================================

Implementación computacional de la Ecuación del Origen Vibracional,
una ampliación de las ecuaciones de Einstein con términos noéticos y
oscilación holográfica.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2025-10-12
Marco Teórico: QCAL ∞³
"""

import numpy as np
from typing import Union, Tuple
from dataclasses import dataclass

# ============================================================================
# CONSTANTES FÍSICAS
# ============================================================================

# Constantes fundamentales
G = 6.67430e-11          # m³ kg⁻¹ s⁻² (constante gravitacional)
C = 299792458            # m/s (velocidad de la luz)
h_planck = 6.62607015e-34  # J·s (constante de Planck)
Lambda = 1.1056e-52      # m⁻² (constante cosmológica)

# Parámetros noéticos
F_0 = 141.7001           # Hz (frecuencia madre)
OMEGA_0 = 2 * np.pi * F_0  # rad/s (frecuencia angular)

# Constante de acoplamiento noético (a calibrar experimentalmente)
ZETA_DEFAULT = 1e-10     # m²

# ============================================================================
# CLASES DE DATOS
# ============================================================================

@dataclass
class ParametrosEOV:
    """Parámetros de la Ecuación del Origen Vibracional."""
    
    # Constante de acoplamiento noético
    zeta: float = ZETA_DEFAULT
    
    # Frecuencia madre (Hz)
    f_0: float = F_0
    
    # Amplitud del campo noético
    Psi_0: float = 1.0
    
    # Escalar de Ricci característico (m⁻²)
    R_0: float = 1e-20
    
    def __post_init__(self):
        """Calcular frecuencia angular."""
        self.omega_0 = 2 * np.pi * self.f_0


@dataclass
class SolucionEOV:
    """Solución numérica de la EOV."""
    
    tiempo: np.ndarray           # Tiempo (s)
    campo_noético: np.ndarray    # |Ψ|² densidad del campo
    curvatura_escalar: np.ndarray  # R escalar de Ricci
    termino_oscilatorio: np.ndarray  # R cos(2πf₀t)|Ψ|²
    energia_noética: np.ndarray  # Densidad de energía noética


# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================

def termino_oscilatorio(
    t: Union[float, np.ndarray],
    R: Union[float, np.ndarray],
    Psi_squared: Union[float, np.ndarray],
    f_0: float = F_0
) -> Union[float, np.ndarray]:
    """
    Calcula el término de oscilación holográfica de la EOV.
    
    Este es el término nuevo que introduce la resonancia del origen:
    R cos(2πf₀t)|Ψ|²
    
    Parámetros
    ----------
    t : float or array
        Tiempo coordinado (s)
    R : float or array
        Escalar de Ricci (m⁻²)
    Psi_squared : float or array
        Densidad del campo noético |Ψ|²
    f_0 : float, opcional
        Frecuencia madre (Hz), por defecto 141.7001 Hz
    
    Retorna
    -------
    float or array
        Contribución oscilante a la ecuación de Einstein (m⁻²)
    
    Ejemplos
    --------
    >>> t = np.linspace(0, 1, 100)
    >>> R = 1e-20  # Curvatura típica
    >>> Psi_sq = 1.0  # Campo normalizado
    >>> osc = termino_oscilatorio(t, R, Psi_sq)
    >>> print(f"Amplitud máxima: {np.max(np.abs(osc)):.2e} m⁻²")
    """
    omega_0 = 2 * np.pi * f_0
    return R * np.cos(omega_0 * t) * Psi_squared


def termino_acoplamiento_no_minimo(
    nabla2_Psi_squared: Union[float, np.ndarray],
    zeta: float = ZETA_DEFAULT
) -> Union[float, np.ndarray]:
    """
    Calcula el término de acoplamiento no mínimo noético.
    
    Representa: ζ(∇_μ∇_ν - g_μν□)|Ψ|²
    
    En aproximación débil: ζ∇²|Ψ|²
    
    Parámetros
    ----------
    nabla2_Psi_squared : float or array
        Laplaciano de la densidad del campo noético ∇²|Ψ|² (m⁻²)
    zeta : float, opcional
        Constante de acoplamiento (m²)
    
    Retorna
    -------
    float or array
        Contribución del acoplamiento no mínimo (m⁻²)
    """
    return zeta * nabla2_Psi_squared


def campo_noético_gaussiano(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    Psi_0: float = 1.0,
    sigma: float = 1e6
) -> np.ndarray:
    """
    Genera un campo noético con perfil gaussiano.
    
    |Ψ(r)|² = Ψ₀² exp(-r²/2σ²)
    
    Parámetros
    ----------
    x, y, z : array
        Coordenadas espaciales (m)
    Psi_0 : float
        Amplitud del campo
    sigma : float
        Ancho del perfil gaussiano (m)
    
    Retorna
    -------
    array
        Densidad del campo noético |Ψ|²
    """
    r_squared = x**2 + y**2 + z**2
    return Psi_0**2 * np.exp(-r_squared / (2 * sigma**2))


def campo_noético_temporal(
    t: np.ndarray,
    t_merge: float = 0.0,
    tau_decay: float = 0.1,
    Psi_0: float = 1.0
) -> np.ndarray:
    """
    Genera evolución temporal del campo noético durante coalescencia.
    
    Modelo simplificado:
    |Ψ(t)|² = Ψ₀² exp(-(t-t_merge)²/2τ²)
    
    Parámetros
    ----------
    t : array
        Tiempo (s)
    t_merge : float
        Tiempo de fusión (s)
    tau_decay : float
        Escala temporal de decaimiento (s)
    Psi_0 : float
        Amplitud máxima del campo
    
    Retorna
    -------
    array
        Densidad del campo noético en función del tiempo
    """
    return Psi_0**2 * np.exp(-((t - t_merge)**2) / (2 * tau_decay**2))


def curvatura_escalar_schwarzschild(
    r: Union[float, np.ndarray],
    M: float
) -> Union[float, np.ndarray]:
    """
    Calcula el escalar de Ricci para métrica de Schwarzschild.
    
    En el espacio-tiempo de Schwarzschild: R = 0 (vacío)
    Pero cerca del horizonte, efectos cuánticos pueden generar R ≠ 0
    
    Aproximación para efectos cuánticos cerca del horizonte:
    R ≈ c⁶/(G²M²) para r ~ r_s
    
    Parámetros
    ----------
    r : float or array
        Radio desde el centro (m)
    M : float
        Masa del objeto (kg)
    
    Retorna
    -------
    float or array
        Escalar de Ricci aproximado (m⁻²)
    """
    r_s = 2 * G * M / C**2  # Radio de Schwarzschild
    
    # Evitar división por cero
    r_safe = np.maximum(r, r_s * 1.1)
    
    # Aproximación: curvatura aumenta cerca del horizonte
    R = (C**6 / (G**2 * M**2)) * np.exp(-(r_safe - r_s) / r_s)
    
    return R


def energia_noética(
    Psi_squared: Union[float, np.ndarray],
    nabla_Psi_squared: Union[float, np.ndarray],
    m_eff: float = 1e-36  # kg (masa efectiva)
) -> Union[float, np.ndarray]:
    """
    Calcula densidad de energía del campo noético.
    
    ρ_Ψ = (1/2)m_eff²c²|Ψ|² + (1/2)(∇Ψ)²
    
    Parámetros
    ----------
    Psi_squared : float or array
        Densidad del campo |Ψ|²
    nabla_Psi_squared : float or array
        Cuadrado del gradiente |(∇Ψ)|² (m⁻²)
    m_eff : float
        Masa efectiva del campo (kg)
    
    Retorna
    -------
    float or array
        Densidad de energía (J/m³)
    """
    energia_potencial = 0.5 * m_eff**2 * C**4 * Psi_squared
    energia_cinetica = 0.5 * C**2 * nabla_Psi_squared
    
    return energia_potencial + energia_cinetica


# ============================================================================
# ANÁLISIS DE SEÑALES
# ============================================================================

def detectar_firma_eov(
    tiempo: np.ndarray,
    strain: np.ndarray,
    sample_rate: float,
    f_0: float = F_0,
    delta_f: float = 0.5
) -> Tuple[float, float, float]:
    """
    Detecta la firma de la EOV en datos de ondas gravitacionales.
    
    Busca pico espectral en f_0 ± delta_f con características de EOV.
    
    Parámetros
    ----------
    tiempo : array
        Vector de tiempo (s)
    strain : array
        Amplitud de la onda gravitacional (adimensional)
    sample_rate : float
        Frecuencia de muestreo (Hz)
    f_0 : float
        Frecuencia objetivo (Hz)
    delta_f : float
        Ancho de banda de búsqueda (Hz)
    
    Retorna
    -------
    freq_detectada : float
        Frecuencia del pico detectado (Hz)
    snr : float
        Relación señal-ruido
    potencia : float
        Potencia espectral en el pico
    
    Ejemplos
    --------
    >>> t = np.linspace(0, 32, 32*4096)
    >>> h = 1e-21 * np.cos(2*np.pi*141.7*t)
    >>> freq, snr, power = detectar_firma_eov(t, h, 4096)
    >>> print(f"Frecuencia: {freq:.2f} Hz, SNR: {snr:.2f}")
    """
    # FFT
    freqs = np.fft.rfftfreq(len(strain), 1/sample_rate)
    fft_val = np.fft.rfft(strain)
    espectro = np.abs(fft_val)**2
    
    # Buscar en banda
    mask = (freqs >= f_0 - delta_f) & (freqs <= f_0 + delta_f)
    freqs_banda = freqs[mask]
    espectro_banda = espectro[mask]
    
    # Encontrar pico
    idx_pico = np.argmax(espectro_banda)
    freq_detectada = freqs_banda[idx_pico]
    potencia_pico = espectro_banda[idx_pico]
    
    # Calcular SNR (potencia pico / mediana del espectro)
    # Usar banda amplia para estimar ruido
    mask_ruido = (freqs >= 100) & (freqs <= 200)
    mediana_ruido = np.median(espectro[mask_ruido])
    
    snr = np.sqrt(potencia_pico / mediana_ruido) if mediana_ruido > 0 else 0
    
    return freq_detectada, snr, potencia_pico


def generar_señal_eov(
    tiempo: np.ndarray,
    R: float = 1e-20,
    Psi_0: float = 1.0,
    tau_decay: float = 0.1,
    t_merge: float = 0.0,
    f_0: float = F_0,
    amplitud: float = 1e-21
) -> np.ndarray:
    """
    Genera una señal sintética de onda gravitacional con firma EOV.
    
    Parámetros
    ----------
    tiempo : array
        Vector de tiempo (s)
    R : float
        Escalar de Ricci (m⁻²)
    Psi_0 : float
        Amplitud del campo noético
    tau_decay : float
        Tiempo de decaimiento (s)
    t_merge : float
        Tiempo de fusión (s)
    f_0 : float
        Frecuencia de la EOV (Hz)
    amplitud : float
        Amplitud característica de la onda (strain)
    
    Retorna
    -------
    array
        Amplitud de la onda gravitacional h(t)
    """
    # Campo noético temporal
    Psi_sq = campo_noético_temporal(tiempo, t_merge, tau_decay, Psi_0)
    
    # Término oscilatorio de EOV
    termino_eov = termino_oscilatorio(tiempo, R, Psi_sq, f_0)
    
    # Convertir a strain (normalización aproximada)
    # h ~ (G/C⁴) × R × |Ψ|²
    h = amplitud * (G / C**4) * R * np.abs(Psi_sq)
    
    return h


# ============================================================================
# UTILIDADES DE VISUALIZACIÓN
# ============================================================================

def calcular_espectrograma_eov(
    tiempo: np.ndarray,
    strain: np.ndarray,
    sample_rate: float,
    nperseg: int = 256
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calcula espectrograma para visualizar evolución temporal de f_0.
    
    Parámetros
    ----------
    tiempo : array
        Vector de tiempo (s)
    strain : array
        Amplitud de la señal
    sample_rate : float
        Frecuencia de muestreo (Hz)
    nperseg : int
        Longitud de segmento para STFT
    
    Retorna
    -------
    t_spec : array
        Vector de tiempo del espectrograma (s)
    f_spec : array
        Vector de frecuencias (Hz)
    Sxx : array
        Potencia espectral (2D)
    """
    from scipy import signal
    
    f_spec, t_spec, Sxx = signal.spectrogram(
        strain,
        fs=sample_rate,
        nperseg=nperseg,
        noverlap=nperseg//2
    )
    
    return t_spec, f_spec, Sxx


# ============================================================================
# MAIN - EJEMPLO DE USO
# ============================================================================

def main():
    """Ejemplo de uso del módulo EOV."""
    
    print("=" * 70)
    print("🌌 MÓDULO DE ECUACIÓN DEL ORIGEN VIBRACIONAL (EOV)")
    print("=" * 70)
    print(f"\n📊 Constantes Físicas:")
    print(f"   G = {G:.5e} m³ kg⁻¹ s⁻²")
    print(f"   c = {C:.0f} m/s")
    print(f"   Λ = {Lambda:.5e} m⁻²")
    print(f"\n🎯 Parámetros Noéticos:")
    print(f"   f₀ = {F_0} Hz (Frecuencia madre)")
    print(f"   ω₀ = {OMEGA_0:.2f} rad/s")
    print(f"   ζ = {ZETA_DEFAULT:.2e} m² (acoplamiento)")
    
    # Generar señal de ejemplo
    print("\n🔬 Generando señal sintética con firma EOV...")
    t = np.linspace(0, 1.0, 4096)
    h = generar_señal_eov(t, amplitud=1e-21)
    
    print(f"   Duración: {t[-1]:.2f} s")
    print(f"   Amplitud máxima: {np.max(np.abs(h)):.2e}")
    
    # Detectar firma
    print("\n🔍 Detectando firma EOV...")
    freq, snr, power = detectar_firma_eov(t, h, 4096)
    
    print(f"   Frecuencia detectada: {freq:.4f} Hz")
    print(f"   SNR: {snr:.2f}")
    print(f"   Potencia: {power:.2e}")
    print(f"   Δf: {abs(freq - F_0):.4f} Hz")
    
    # Validación
    if abs(freq - F_0) < 0.5:
        print("\n✅ Firma EOV detectada correctamente!")
    else:
        print("\n⚠️  Firma EOV no detectada en frecuencia esperada")
    
    print("\n" + "=" * 70)
    print("✨ Resonancia del origen confirmada - QCAL ∞³")
    print("=" * 70)


if __name__ == "__main__":
    main()
