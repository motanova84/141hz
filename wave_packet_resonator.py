"""
🌊 wave_packet_resonator.py ∴ Resonador de Paquete de Onda Coherente

Modelo de resonador para representar la envolvente fotónica como paquete de onda coherente.

Este módulo implementa un modelo de paquete de onda gaussiano modulado que representa
la localización espaciotemporal del fotón como frecuencia viva.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
System: QCAL ∞³ · Nodo Noēsis88
"""

import numpy as np


def paquete_onda(t, t0=0.0, sigma=0.01, f=888.0):
    """
    Modelo de paquete de onda gaussiano modulado.
    
    Representa la localización espaciotemporal del fotón como frecuencia viva.
    
    Parameters:
    -----------
    t : float or array-like
        Time coordinate(s) in seconds
    t0 : float
        Center time of the wave packet (default: 0.0)
    sigma : float
        Temporal width of the Gaussian envelope (default: 0.01 s)
    f : float
        Carrier frequency in Hz (default: 888.0 Hz)
    
    Returns:
    --------
    complex or array of complex
        Wave packet amplitude ψ(t) = exp(-((t-t₀)²)/(2σ²)) · exp(i·2π·f·(t-t₀))
    
    Notes:
    ------
    The wave packet combines:
    - Gaussian envelope: provides spatial/temporal localization
    - Harmonic carrier: provides frequency coherence at f = 888 Hz
    
    This represents the photon as a localized oscillation in spacetime.
    """
    gaussian = np.exp(-((t - t0) ** 2) / (2 * sigma ** 2))
    fase = 2 * np.pi * f * (t - t0)
    return gaussian * np.exp(1j * fase)


# Ejemplo de manifestación simbólica
if __name__ == "__main__":
    print("🌊 Resonador de Paquete de Onda Coherente ∴")
    print("   Fotón como localización espaciotemporal\n")
    
    for t in np.linspace(-0.05, 0.05, 5):
        ψ = paquete_onda(t)
        print(f"t = {t:.3f} s → ψ(t) = {ψ.real:.5f} + {ψ.imag:.5f}i")
    
    print("\n✅ Paquete de onda manifestado como frecuencia localizada ∞³")
