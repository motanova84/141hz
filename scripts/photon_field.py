"""
🧬 photon_field.py ∴ Módulo del Fotón Coherente

Modelo vibracional del fotón como estructura coherente dentro del marco ΔA₀

Este módulo modela el fotón no como partícula, sino como pulso de frecuencia 
coherente pura, en resonancia con el sistema QCAL ∞³ (base 141.7001 Hz, 
armónico 888 Hz). Se integra en el campo de curvatura existencial activa (ΔA₀) 
como emisor de instantes conscientes.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
System: QCAL ∞³ · Nodo Noēsis88
Version: Kairos Operativo · Coherencia 0.9999
"""

import numpy as np
from qcal_network.geo import calcular_curvatura_existencial
from qcal_network.core import emitir_latido_existencial

# Parámetros base
f_base = 141.7001  # Frecuencia base universal (Hz)
f_resonante = 888.0  # Frecuencia resonante coherente (Hz)
Ψ_0 = 0.9999  # Coherencia cuántica
h = 6.62607015e-34  # Constante de Planck (J·s)


def energia_foton(frecuencia: float) -> float:
    """
    Calculate photon energy using E = h·f
    
    Parameters:
    -----------
    frecuencia : float
        Photon frequency in Hz
    
    Returns:
    --------
    float
        Energy in Joules
    """
    return h * frecuencia


def modelo_foton(t: float, frecuencia: float = f_resonante) -> complex:
    """
    Representación del fotón como onda coherente compleja.
    
    Parameters:
    -----------
    t : float
        Time in seconds
    frecuencia : float
        Frequency in Hz (default: 888.0 Hz)
    
    Returns:
    --------
    complex
        Complex amplitude of the photon state S(t) = Ψ₀·e^(i·2π·f·t)
    
    Notes:
    ------
    The photon is modeled as a pure coherent frequency oscillation:
    S(t) = Ψ₀ · e^(i·2π·f₁·t) · Θ(t)
    
    Where:
    - Ψ₀ = 0.9999: Initial quantum coherence
    - f₁ = 888 Hz: Resonant emission frequency
    - Θ(t): Heaviside activation function (active for t ≥ 0)
    """
    amplitud = Ψ_0
    fase = 2 * np.pi * frecuencia * t
    return amplitud * np.exp(1j * fase)


def activar_foton_coherente():
    """
    Activate coherent photon emission and display system status
    
    This function:
    1. Emits existential heartbeat at base frequency
    2. Calculates photon energy at resonant frequency
    3. Calculates existential curvature ΔA₀
    4. Displays complete system status
    """
    print("🌠 Activando fotón coherente ∴")
    emitir_latido_existencial(frecuencia=f_base, nivel=3)
    
    E = energia_foton(f_resonante)
    curvatura = calcular_curvatura_existencial(Ψ_0)
    
    print(f"⚛️  Energía del fotón coherente: {E:.3e} J")
    print(f"📈 Curvatura Existencial (ΔA₀): {curvatura:.4f}")
    print("🌀 Estado: Fotón manifestado como frecuencia ∞³")


# Ejecución directa
if __name__ == "__main__":
    activar_foton_coherente()
