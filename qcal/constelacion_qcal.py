"""
╔════════════════════════════════════════════════════════════════════════════╗
║               CONSTELACIÓN QCAL Ψ✧ - Quantum Constellation                ║
║          Fotografía del Universo Soñado - Photographic State              ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ CONSTELACIÓN CUÁNTICA FOTOGRAFIADA ⚡

La función de onda total del universo QCAL:

Ψ_total(x,y) = Σ[αₙe^(if₀tₙ) + βₙ(7/8)ⁿζ(1/2+itₙ) + γₙφⁿ𝒦(tₙ) + δₙ𝒩(tₙ)]

Donde cada término codifica un eje de coherencia:
- Dorado: f₀ = 141.7001 Hz (eje del Logos)
- Azul: Riemann + Berry 7/8 (matemático)
- Violeta: NOESIS/AMDA (noético)
- Verde: Fibonacci/φ (kairós)
- Blanco: H-21cm @ 23.257 octavas (logos)

Referencias:
- Riemann Hypothesis: ζ(1/2 + it) = 0
- Berry Phase: Geometric phase in quantum systems
- Golden Ratio: φ = (1 + √5)/2 ≈ 1.618
- Hydrogen Line: f_H = 1420.405751 MHz
"""

import numpy as np
import mpmath
from typing import Tuple, Dict, List, Optional
import math

# Import QCAL constants
try:
    from fisica.reloj_universo_f0 import F0_HZ, C_LUZ, h as PLANCK_H
    from fisica.marco_adelico import FACTOR_SIETE_OCTAVOS, RIEMANN_CEROS
    from fisica.constantes_coherencia import PSI_MINIMO_ESTABLE, PSI_BUENO
except ImportError:
    # Fallback values if imports fail
    F0_HZ = 141.7001
    C_LUZ = 299792458.0
    PLANCK_H = 6.62607015e-34
    FACTOR_SIETE_OCTAVOS = 7.0 / 8.0
    RIEMANN_CEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]
    PSI_MINIMO_ESTABLE = 0.888
    PSI_BUENO = 0.95

# ============================================================================
# CONSTANTES DE LA CONSTELACIÓN
# ============================================================================

# Golden Ratio (φ - Phi)
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618033988749895

# Hydrogen Line frequency (21 cm)
F_HYDROGEN_HZ = 1420.405751e6  # Hz (1420.405751 MHz)

# Octaves between hydrogen and f₀
OCTAVAS_H_F0 = math.log2(F_HYDROGEN_HZ / F0_HZ)  # ≈ 23.257

# Coherence threshold for constellation
PSI_COHERENCIA_ALTA = PSI_BUENO  # Ψ ≥ 0.95


# ============================================================================
# FUNCIÓN DE ONDA TOTAL - Total Wave Function
# ============================================================================

def psi_dorado(n: int, t_n: float) -> complex:
    """
    Eje Dorado (Golden Axis): f₀ = 141.7001 Hz
    
    El eje del Logos, la columna vertebral del universo fotografiado.
    
    Ψ_dorado = αₙ exp(i·f₀·tₙ)
    
    Args:
        n: Index of the term in the series
        t_n: Time parameter (often Riemann zero value)
    
    Returns:
        Complex amplitude for golden axis
    """
    omega_0 = 2 * math.pi * F0_HZ
    alpha_n = 1.0 / math.sqrt(n + 1)  # Normalization factor
    
    # Phase from f₀
    phase = omega_0 * t_n
    
    return alpha_n * np.exp(1j * phase)


def psi_azul(n: int, t_n: float) -> complex:
    """
    Eje Azul Matemático (Blue Mathematical Axis): Riemann + Berry 7/8
    
    Los ceros de Riemann materializados, modulados por el invariante
    topológico de Berry.
    
    Ψ_azul = βₙ (7/8)ⁿ ζ(1/2 + i·tₙ)
    
    Args:
        n: Index of the term in the series
        t_n: Time parameter (Riemann zero imaginary part)
    
    Returns:
        Complex amplitude for blue mathematical axis
    """
    beta_n = 1.0 / (n + 1)  # Normalization factor
    
    # Berry phase factor: (7/8)^n
    berry_factor = FACTOR_SIETE_OCTAVOS ** n
    
    # Riemann zeta on critical line: ζ(1/2 + i·tₙ)
    # Using mpmath for high precision
    s = mpmath.mpc(0.5, t_n)
    zeta_value = complex(mpmath.zeta(s))
    
    return beta_n * berry_factor * zeta_value


def psi_verde(n: int, t_n: float) -> complex:
    """
    Eje Verde Kairós (Green Kairos Axis): Fibonacci/φ
    
    El tiempo cualitativo (kairós) sobre el tiempo cuantitativo (cronos).
    Puntos de bifurcación donde el sistema elige coherencia o entropía.
    
    Ψ_verde = γₙ φⁿ 𝒦(tₙ)
    
    Args:
        n: Index of the term in the series
        t_n: Time parameter
    
    Returns:
        Complex amplitude for green kairos axis
    """
    gamma_n = 1.0 / math.sqrt(n + 2)  # Normalization factor
    
    # Golden ratio power: φⁿ
    phi_power = PHI ** n
    
    # Kairos function: temporal quality modulation
    # Uses sine modulation at f₀ frequency
    kairos = math.cos(2 * math.pi * F0_HZ * t_n / 1000) + \
             1j * math.sin(2 * math.pi * F0_HZ * t_n / 1000)
    
    return gamma_n * phi_power * kairos


def psi_violeta(n: int, t_n: float) -> complex:
    """
    Eje Violeta Noético (Violet Noetic Axis): NOESIS/AMDA
    
    Nodos de consciencia pura. La relación señal/ruido se invierte.
    Información no-local de la Asociación de Memoria y Desarrollo Anímico.
    
    Ψ_noesis = δₙ 𝒩(tₙ)
    
    Args:
        n: Index of the term in the series
        t_n: Time parameter
    
    Returns:
        Complex amplitude for violet noetic axis
    """
    delta_n = 1.0 / (n + 3)  # Normalization factor
    
    # Noetic function: consciousness resonance
    # Modulated by PSI coherence threshold
    noetic_freq = F0_HZ / PSI_MINIMO_ESTABLE  # ≈ 159.57 Hz
    
    noesis = PSI_MINIMO_ESTABLE * np.exp(1j * 2 * math.pi * noetic_freq * t_n / 1000)
    
    return delta_n * noesis


def psi_blanco(n: int, t_n: float) -> complex:
    """
    Eje Blanco Logos (White Logos Axis): H-21cm @ 23.257 octavas
    
    La firma del hidrógeno, elemento primordial, 23.257 octavas por encima
    de la frecuencia del alma. Materia (H) y espíritu (f₀) en armonía.
    
    Modulación adicional sobre todos los ejes.
    
    Args:
        n: Index of the term in the series
        t_n: Time parameter
    
    Returns:
        Complex amplitude for white logos axis (modulation factor)
    """
    # Hydrogen line modulation at octave-reduced frequency
    # f_mod = f_H / 2^23 (bringing it closer to f₀ range)
    f_modulation = F_HYDROGEN_HZ / (2 ** OCTAVAS_H_F0)
    
    # White light: all colors combined
    epsilon_n = 1.0 / (2 ** n)  # Exponential decay
    
    modulation = epsilon_n * np.exp(1j * 2 * math.pi * f_modulation * t_n)
    
    return modulation


def psi_total(x: float, y: float, n_terms: int = 50) -> complex:
    """
    Función de Onda Total del Universo QCAL
    
    Ψ_total(x,y) = Σ[αₙe^(if₀tₙ) + βₙ(7/8)ⁿζ(1/2+itₙ) + γₙφⁿ𝒦(tₙ) + δₙ𝒩(tₙ)]
    
    Cada píxel codifica coherencia:
    - Dorado: f₀ eje
    - Azul: matemático RH Berry 7/8
    - Violeta: noético NOESIS/AMDA
    - Verde: kairós Fibonacci
    - Blanco: logos H-21cm 23.257 octavas
    
    Args:
        x: Spatial coordinate (normalized)
        y: Spatial coordinate (normalized)
        n_terms: Number of terms in the series (default: 50)
    
    Returns:
        Complex wave function value at (x, y)
    """
    # Use Riemann zeros as time parameters
    # Extend beyond known zeros using asymptotic formula if needed
    t_values = []
    
    # Use known Riemann zeros
    for i, t in enumerate(RIEMANN_CEROS[:min(n_terms, len(RIEMANN_CEROS))]):
        t_values.append(t)
    
    # Extend with asymptotic approximation if needed
    if n_terms > len(RIEMANN_CEROS):
        for i in range(len(RIEMANN_CEROS), n_terms):
            # Asymptotic: t_n ≈ 2π(n+1)/log((n+1)/(2πe))
            t_approx = 2 * math.pi * (i + 1) / math.log((i + 1) / (2 * math.pi * math.e))
            t_values.append(t_approx)
    
    # Compute wave function as sum over n
    psi_sum = 0.0 + 0.0j
    
    for n in range(n_terms):
        t_n = t_values[n]
        
        # Spatial modulation: depends on (x, y) position
        spatial_phase = 2 * math.pi * (x * math.cos(t_n) + y * math.sin(t_n))
        spatial_mod = np.exp(1j * spatial_phase)
        
        # Sum all five axes
        term = (psi_dorado(n, t_n) + 
                psi_azul(n, t_n) + 
                psi_verde(n, t_n) + 
                psi_violeta(n, t_n)) * psi_blanco(n, t_n)
        
        psi_sum += term * spatial_mod
    
    return psi_sum / math.sqrt(n_terms)  # Normalize


def coherencia_local(psi: complex) -> float:
    """
    Calcula la coherencia local Ψ de un valor de función de onda.
    
    Ψ = |ψ| / max_esperado
    
    Args:
        psi: Complex wave function value
    
    Returns:
        Local coherence value (0 to 1+)
    """
    return abs(psi)


def calcular_constelacion(
    grid_size: int = 256,
    x_range: Tuple[float, float] = (-2.0, 2.0),
    y_range: Tuple[float, float] = (-2.0, 2.0),
    n_terms: int = 50
) -> Dict[str, np.ndarray]:
    """
    Calcula la constelación QCAL completa en una malla espacial.
    
    Genera el mapa fotográfico del universo soñado por JMMB Ψ✧.
    
    Args:
        grid_size: Number of pixels per dimension
        x_range: (min, max) for x coordinate
        y_range: (min, max) for y coordinate
        n_terms: Number of terms in wave function series
    
    Returns:
        Dictionary with:
            - 'x': x coordinate array
            - 'y': y coordinate array
            - 'psi': Complex wave function values (grid_size x grid_size)
            - 'coherencia': Coherence map (grid_size x grid_size)
            - 'fase': Phase map (grid_size x grid_size)
    """
    print(f"Calculando Constelación QCAL Ψ✧ ({grid_size}x{grid_size} píxeles)...")
    
    # Create spatial grid
    x = np.linspace(x_range[0], x_range[1], grid_size)
    y = np.linspace(y_range[0], y_range[1], grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Initialize arrays
    psi_grid = np.zeros((grid_size, grid_size), dtype=complex)
    coherencia_grid = np.zeros((grid_size, grid_size))
    fase_grid = np.zeros((grid_size, grid_size))
    
    # Calculate wave function at each point
    total_points = grid_size * grid_size
    for i in range(grid_size):
        if i % 16 == 0:
            progress = (i * grid_size) / total_points * 100
            print(f"  Progreso: {progress:.1f}%")
        
        for j in range(grid_size):
            # Normalized coordinates
            x_norm = X[i, j]
            y_norm = Y[i, j]
            
            # Compute wave function
            psi_val = psi_total(x_norm, y_norm, n_terms)
            
            psi_grid[i, j] = psi_val
            coherencia_grid[i, j] = coherencia_local(psi_val)
            fase_grid[i, j] = np.angle(psi_val)
    
    print("  ✓ Constelación calculada")
    
    return {
        'x': x,
        'y': y,
        'X': X,
        'Y': Y,
        'psi': psi_grid,
        'coherencia': coherencia_grid,
        'fase': fase_grid
    }


def analizar_constelacion(constelacion: Dict[str, np.ndarray]) -> Dict[str, float]:
    """
    Analiza las propiedades estadísticas de la constelación.
    
    Args:
        constelacion: Dictionary returned by calcular_constelacion()
    
    Returns:
        Dictionary with analysis metrics:
            - coherencia_media: Average coherence
            - coherencia_max: Maximum coherence
            - coherencia_min: Minimum coherence
            - puntos_interes: Number of high-coherence points (Ψ > 0.95)
            - dimension_fractal: Estimated fractal dimension
    """
    coherencia = constelacion['coherencia']
    
    # Basic statistics
    coherencia_media = np.mean(coherencia)
    coherencia_max = np.max(coherencia)
    coherencia_min = np.min(coherencia)
    
    # Count high-coherence points
    puntos_interes = np.sum(coherencia > PSI_COHERENCIA_ALTA)
    
    # Estimate fractal dimension using box-counting
    # Simplified: ratio of high-coherence points follows power law
    threshold = coherencia_media + 0.5 * (coherencia_max - coherencia_media)
    high_points = coherencia > threshold
    
    # Approximate fractal dimension (should be close to φ ≈ 1.618)
    # This is a simplified estimate
    n_high = np.sum(high_points)
    total = coherencia.size
    if n_high > 0:
        dimension_fractal = math.log(n_high) / math.log(total) * 2
    else:
        dimension_fractal = 1.0
    
    # Clamp to reasonable range around golden ratio
    dimension_fractal = max(1.0, min(2.0, dimension_fractal))
    
    return {
        'coherencia_media': float(coherencia_media),
        'coherencia_max': float(coherencia_max),
        'coherencia_min': float(coherencia_min),
        'puntos_interes': int(puntos_interes),
        'dimension_fractal': float(dimension_fractal)
    }


def punto_ciego_observador(constelacion: Dict[str, np.ndarray]) -> Tuple[float, float]:
    """
    Calcula la posición del observador como "punto ciego" de coherencia.
    
    Según el principio de incertidumbre de QCAL:
        Δx · ΔΨ ≥ 1/f₀
    
    El observador no es un punto, sino una región de coherencia desde
    la cual toda la constelación es visible.
    
    Args:
        constelacion: Dictionary returned by calcular_constelacion()
    
    Returns:
        (x_obs, y_obs): Observer position coordinates
    """
    coherencia = constelacion['coherencia']
    X = constelacion['X']
    Y = constelacion['Y']
    
    # Find center of mass of high-coherence regions
    threshold = PSI_COHERENCIA_ALTA
    mask = coherencia > threshold
    
    if np.sum(mask) > 0:
        x_obs = np.mean(X[mask])
        y_obs = np.mean(Y[mask])
    else:
        # Fallback to geometric center
        x_obs = 0.0
        y_obs = 0.0
    
    return (float(x_obs), float(y_obs))


# ============================================================================
# CERTIFICADO DE LA CONSTELACIÓN
# ============================================================================

def generar_certificado(
    constelacion: Dict[str, np.ndarray],
    fecha: str = "2026-03-08"
) -> Dict:
    """
    Genera el certificado JSON de la constelación QCAL Ψ✧.
    
    Args:
        constelacion: Dictionary returned by calcular_constelacion()
        fecha: Date string (ISO format)
    
    Returns:
        Certificate dictionary ready for JSON serialization
    """
    # Analyze constellation
    analisis = analizar_constelacion(constelacion)
    x_obs, y_obs = punto_ciego_observador(constelacion)
    
    certificado = {
        "constelacion_qcal_psix": {
            "fecha": fecha,
            "sello": "∴𓂀Ω∞³Ψ✧",
            "ejes": {
                "dorado": f"f0 = {F0_HZ} Hz",
                "azul": "Riemann + Berry 7/8",
                "violeta": "NOESIS/AMDA",
                "verde": "Fibonacci (kairós)",
                "blanco": f"H-21cm @ {OCTAVAS_H_F0:.3f} octavas"
            },
            "coherencia_media": round(analisis['coherencia_media'], 3),
            "coherencia_max": round(analisis['coherencia_max'], 3),
            "coherencia_min": round(analisis['coherencia_min'], 3),
            "puntos_de_interes": analisis['puntos_interes'],
            "dimension_fractal": round(analisis['dimension_fractal'], 3),
            "observador_posicion": {
                "x": round(x_obs, 3),
                "y": round(y_obs, 3),
                "interpretacion": "punto_ciego_coherencia"
            },
            "interpretacion": "Fotografía del universo soñado por JMMB Ψ✧",
            "estado": "CONSTELACION_FOTOGRAFIADA"
        }
    }
    
    return certificado


if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           CONSTELACIÓN QCAL Ψ✧ - Demo Calculation                 ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Quick test with small grid
    print("Calculando constelación de prueba (64x64)...")
    constelacion = calcular_constelacion(grid_size=64, n_terms=20)
    
    print("\nAnálisis de la constelación:")
    analisis = analizar_constelacion(constelacion)
    for key, value in analisis.items():
        print(f"  {key}: {value}")
    
    print("\nPosición del observador:")
    x_obs, y_obs = punto_ciego_observador(constelacion)
    print(f"  (x, y) = ({x_obs:.3f}, {y_obs:.3f})")
    
    print("\n✓ Demo completado")
    print("\nPara visualización completa, usar: visualizacion_constelacion.py")
    print("∴𓂀Ω∞³Ψ✧")
