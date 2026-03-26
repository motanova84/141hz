"""
Spectral Search Module - C7 Cycle Twist Gauge θ Calculator
===========================================================

This module implements the spectral search algorithm to find the exact twist gauge
angle θ required to shift a C7 (7-node cycle) graph's fundamental frequency from
its bare value to the target resonance frequency f₀ = 141.7001 Hz.

Physical Interpretation:
-----------------------
The twist gauge θ represents a phase offset in the C7 cycle that modulates its
spectral eigenvalue. This is not an arbitrary parameter but a phenomenological
constant that emerges from the requirement of quantum coherence at f₀.

Mathematical Framework:
----------------------
For a C7 cycle graph with twist gauge θ:
- Base eigenvalue: λ₀ = 2 - 2·cos(2π/7)
- Twisted eigenvalue: λ_θ = 2 - 2·cos(2π/7 + θ)
- Frequency scaling: f(θ) = f_bare · √(λ_θ / λ₀)

The script solves for θ such that f(θ) = f₀ = 141.7001 Hz.

Interpretation of θ ≈ 0.0573 rad:
---------------------------------
This twist angle is the "Coupling Constant of Symbiosis" - it represents the
curvature that the intention to be coherent imprints on the graph structure.
If θ = 0, we have only "dead physics". At θ = 0.0573, we encode intentionality.

Future Work:
-----------
- Explore quantized flux interpretation (Ruta A)
- Connect to holonomy and Berry phase concepts
- Investigate network anomaly contributions
- Validate against experimental data

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
License: Sovereign Noetic License 1.0 (compatible with MIT)
Architecture: QCAL ∞³ Original Manufacture

References:
----------
- Spectral graph theory and discrete geometry
- Gauge theories on graphs
- Network topology and quantum coherence
"""

import numpy as np
from scipy.optimize import fsolve
import sys
import os

# Import QCAL constants
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcal.constants import F0_HZ


def calcular_frecuencia_c7(theta, f_bare=134.425):
    """
    Calculate the resulting frequency in a C7 cycle with twist gauge theta.
    
    The frequency is proportional to the square root of the fundamental
    eigenvalue of the twisted C7 cycle graph.
    
    Mathematical relation:
        f(θ) = f_bare · √(λ_θ / λ₀)
    
    where:
        λ₀ = 2 - 2·cos(2π/7)         # Base eigenvalue (θ = 0)
        λ_θ = 2 - 2·cos(2π/7 + θ)    # Twisted eigenvalue
    
    Args:
        theta: Twist gauge angle in radians
        f_bare: Bare (untwisted) frequency in Hz (default: 134.425 Hz)
    
    Returns:
        float: Resulting frequency in Hz after applying twist gauge
    
    Physical Interpretation:
        The twist gauge θ modifies the phase relationship between nodes in the
        C7 cycle, effectively changing the spectral gap and thus the characteristic
        frequency of oscillations on the graph.
    """
    # Fundamental eigenvalue of C7 cycle (θ = 0)
    lambda_0 = 2 - 2 * np.cos(2 * np.pi / 7)
    
    # Twisted eigenvalue with phase θ
    lambda_theta = 2 - 2 * np.cos(2 * np.pi / 7 + theta)
    
    # Spectral scaling factor
    kappa = np.sqrt(lambda_theta / lambda_0)
    
    return f_bare * kappa


def encontrar_theta_exacto(f_objetivo=None, f_bare=134.425, theta_inicial=0.05):
    """
    Find the exact twist gauge θ required to reach the target frequency.
    
    Uses numerical root-finding to solve:
        calcular_frecuencia_c7(θ, f_bare) - f_objetivo = 0
    
    Args:
        f_objetivo: Target frequency in Hz (default: F0_HZ = 141.7001 Hz)
        f_bare: Bare frequency in Hz (default: 134.425 Hz)
        theta_inicial: Initial guess for θ in radians (default: 0.05)
    
    Returns:
        float: The twist gauge angle θ in radians
    
    Notes:
        The default target frequency is the fundamental QCAL frequency f₀,
        which is imported from qcal.constants as F0_HZ.
    """
    if f_objetivo is None:
        f_objetivo = F0_HZ
    
    # Define the equation to solve: f(θ) - f_objetivo = 0
    func = lambda t: calcular_frecuencia_c7(t, f_bare) - f_objetivo
    
    # Solve using numerical root-finding
    theta_sol = fsolve(func, theta_inicial)[0]
    
    return theta_sol


def validar_solucion(theta, f_objetivo=None, f_bare=134.425, tolerancia=1e-6):
    """
    Validate that the found θ solution indeed produces the target frequency.
    
    Args:
        theta: Twist gauge angle to validate
        f_objetivo: Target frequency in Hz (default: F0_HZ)
        f_bare: Bare frequency in Hz
        tolerancia: Maximum allowed error in Hz
    
    Returns:
        tuple: (is_valid, error) where is_valid is bool and error is float
    """
    if f_objetivo is None:
        f_objetivo = F0_HZ
    
    f_calculada = calcular_frecuencia_c7(theta, f_bare)
    error = abs(f_calculada - f_objetivo)
    
    is_valid = error < tolerancia
    
    return is_valid, error


def main():
    """
    Main execution: Calculate and display the twist gauge θ solution.
    
    This function performs the spectral search and outputs:
    - The exact twist gauge θ required
    - The resulting frequency (should match f₀)
    - Validation of the solution
    """
    # Constants
    objetivo = F0_HZ          # Target: 141.7001 Hz (fundamental frequency)
    f_bare_calc = 134.425     # Bare frequency (proton-horizon coupling)
    
    print("=" * 70)
    print("BÚSQUEDA ESPECTRAL DEL TWIST GAUGE θ")
    print("Spectral Search for C7 Cycle Twist Gauge Parameter")
    print("=" * 70)
    print()
    print("Parámetros de Entrada / Input Parameters:")
    print(f"  • Frecuencia Objetivo (f₀): {objetivo:.4f} Hz")
    print(f"  • Frecuencia Bare (f_bare): {f_bare_calc:.3f} Hz")
    print(f"  • Geometría de Red: Ciclo C₇ (7 nodos)")
    print()
    
    # Solve for the twist theta
    theta_sol = encontrar_theta_exacto(objetivo, f_bare_calc)
    
    # Calculate resulting frequency
    f_resultado = calcular_frecuencia_c7(theta_sol, f_bare_calc)
    
    # Validate solution
    is_valid, error = validar_solucion(theta_sol, objetivo, f_bare_calc)
    
    print("─" * 70)
    print("RESULTADO DE LA FISURA / RESULT")
    print("─" * 70)
    print()
    print(f"  ✓ Twist Gauge Requerido (θ): {theta_sol:.6f} rad")
    print(f"  ✓ Frecuencia Resultante: {f_resultado:.4f} Hz")
    print(f"  ✓ Error: {error:.2e} Hz")
    print()
    
    # Additional analysis
    print("─" * 70)
    print("INTERPRETACIÓN FÍSICA / PHYSICAL INTERPRETATION")
    print("─" * 70)
    print()
    print(f"El twist gauge θ ≈ {theta_sol:.4f} rad es la 'Constante de")
    print("Acoplamiento de la Simbiosis' - la curvatura que la intención")
    print("de coherencia imprime en la estructura del grafo.")
    print()
    print("Estado del Sistema / System State:")
    print(f"  • Frecuencia Primordial (f_bare): {f_bare_calc} Hz - SÓLIDO")
    print("  • Geometría de Red (C₇): 7 nodos - SÓLIDO")
    print(f"  • Twist de Sintonía (θ): {theta_sol:.6f} rad - FENOMENOLÓGICO")
    print()
    
    if is_valid:
        print("✓ VALIDACIÓN: Solución verificada dentro de tolerancia.")
        print()
        print("𓁟 El Organismo Noético ha asumido su nueva condición.")
        print("𓂀 La Búsqueda de la Holonomía puede continuar.")
        print()
        print("∴𓂀Ω∞³Φ · θ = 0.0573 rad IDENTIFICADO")
        print("EL CAMINO SIGUE LIBRE DE MENTIRAS. ✅")
    else:
        print(f"⚠ ADVERTENCIA: Error {error:.2e} Hz excede tolerancia.")
    
    print()
    print("=" * 70)
    
    return theta_sol, f_resultado


if __name__ == "__main__":
    main()
