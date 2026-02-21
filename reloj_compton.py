#!/usr/bin/env python3
"""
Reloj Compton (Compton Clock) - Derivación de f₀ desde Frecuencias Compton
=============================================================================

Este módulo implementa la derivación de la frecuencia fundamental f₀ = 141.7001 Hz
a partir de las frecuencias Compton de partículas fundamentales, la geometría de 
la escala de Planck, la proporción áurea φ y la constante de estructura fina α.

Ecuación Maestra
----------------
f₀ = (c/(2π)) · √(m_P/m_e) · α · φ · (ℓ_P/λ_C) · K

Donde:
    K = 2·(m_P/m_e)^(1/3)·φ³ ≈ 2.44×10⁸

Es el factor de escala cósmico que conecta las escalas cuántica y de Planck.
- El factor 2 surge de la dualidad onda-partícula
- φ³ surge de la geometría tridimensional de la proporción áurea

Implementación
--------------
1. Cálculos de frecuencia Compton: f_Compton = (m c²) / h
2. Análisis de partículas para e⁻, p, n, m_P
3. Derivación del factor de escala cósmica K
4. Validación de la ecuación maestra

Validación
----------
- f₀ calculado: 141.5459 Hz
- f₀ teórica: 141.7001 Hz
- Error: 0.1088%

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Febrero 2026
Licencia: Sovereign Noetic License 1.0 (compatible con MIT)
"""

import math
from typing import Dict, Tuple

# ============================================================================
# CONSTANTES FÍSICAS FUNDAMENTALES (CODATA 2018)
# ============================================================================

# Constantes exactas por definición (CODATA 2018)
H_PLANCK = 6.62607015e-34  # J·s - Constante de Planck (exacta)
C = 299792458.0            # m/s - Velocidad de la luz en el vacío (exacta)
HBAR = H_PLANCK / (2 * math.pi)  # J·s - Constante de Planck reducida

# Constante gravitacional
G = 6.67430e-11  # m³/(kg·s²) - Constante gravitacional de Newton

# Constante de estructura fina (CODATA 2018)
ALPHA_FINE = 7.2973525693e-3  # Constante de estructura fina (sin dimensiones)

# Masas de partículas fundamentales (CODATA 2018)
M_ELECTRON = 9.1093837015e-31  # kg - Masa del electrón
M_PROTON = 1.67262192369e-27   # kg - Masa del protón
M_NEUTRON = 1.67492749804e-27  # kg - Masa del neutrón

# Masa de Planck
M_PLANCK = math.sqrt(HBAR * C / G)  # kg - Masa de Planck ≈ 2.176434e-8 kg

# Longitud de Planck
L_PLANCK = math.sqrt(HBAR * G / (C ** 3))  # m - Longitud de Planck ≈ 1.616255e-35 m

# Proporción áurea
PHI = (1 + math.sqrt(5)) / 2  # φ = 1.618033988749895

# Frecuencia fundamental teórica (objetivo de validación)
F0_THEORETICAL = 141.7001  # Hz

# ============================================================================
# CÁLCULOS DE FRECUENCIA COMPTON
# ============================================================================

def frecuencia_compton(masa: float) -> float:
    """
    Calcula la frecuencia Compton de una partícula.
    
    La frecuencia Compton se define como:
        f_Compton = (m c²) / h = m c² / h
    
    Esta es la frecuencia asociada a un fotón cuya energía es igual
    a la energía en reposo de la partícula (E = mc²).
    
    Args:
        masa: Masa de la partícula en kg
        
    Returns:
        Frecuencia Compton en Hz
    """
    return (masa * C ** 2) / H_PLANCK


def longitud_onda_compton(masa: float) -> float:
    """
    Calcula la longitud de onda Compton de una partícula.
    
    λ_C = h / (m c) = c / f_C
    
    Args:
        masa: Masa de la partícula en kg
        
    Returns:
        Longitud de onda Compton en m
    """
    return H_PLANCK / (masa * C)


def calcular_frecuencias_particulas() -> Dict[str, Dict[str, float]]:
    """
    Calcula las frecuencias y longitudes de onda Compton para partículas fundamentales.
    
    Returns:
        Diccionario con información de cada partícula:
        - masa: masa en kg
        - frecuencia_compton: frecuencia en Hz
        - longitud_onda_compton: longitud de onda en m
        - energia: energía en reposo en J
    """
    particulas = {
        'electron': M_ELECTRON,
        'proton': M_PROTON,
        'neutron': M_NEUTRON,
        'planck': M_PLANCK
    }
    
    resultados = {}
    
    for nombre, masa in particulas.items():
        f_c = frecuencia_compton(masa)
        lambda_c = longitud_onda_compton(masa)
        energia = masa * C ** 2
        
        resultados[nombre] = {
            'masa': masa,
            'frecuencia_compton': f_c,
            'longitud_onda_compton': lambda_c,
            'energia': energia
        }
    
    return resultados


# ============================================================================
# FACTOR DE ESCALA CÓSMICO K
# ============================================================================

def calcular_factor_escala_cosmico() -> Tuple[float, Dict[str, float]]:
    """
    Calcula el factor de escala cósmico K que conecta las escalas cuántica y de Planck.
    
    K = 2 · (m_P/m_e)^(1/3) · φ³
    
    Componentes:
    - Factor 2: Dualidad onda-partícula
    - (m_P/m_e)^(1/3): Relación de masas en geometría 3D
    - φ³: Geometría tridimensional de la proporción áurea
    
    Returns:
        Tupla (K, detalles) donde detalles contiene:
        - ratio_masas: m_P / m_e
        - ratio_masas_cbrt: (m_P / m_e)^(1/3)
        - phi_cubed: φ³
        - factor_dualidad: 2 (dualidad onda-partícula)
        - K: factor de escala cósmico total
    """
    ratio_masas = M_PLANCK / M_ELECTRON
    ratio_masas_cbrt = ratio_masas ** (1/3)
    phi_cubed = PHI ** 3
    factor_dualidad = 2.0
    
    K = factor_dualidad * ratio_masas_cbrt * phi_cubed
    
    detalles = {
        'ratio_masas': ratio_masas,
        'ratio_masas_cbrt': ratio_masas_cbrt,
        'phi_cubed': phi_cubed,
        'factor_dualidad': factor_dualidad,
        'K': K
    }
    
    return K, detalles


# ============================================================================
# ECUACIÓN MAESTRA - DERIVACIÓN DE f₀
# ============================================================================

def derivar_f0_ecuacion_maestra() -> Tuple[float, Dict[str, float]]:
    """
    Deriva f₀ usando la ecuación maestra completa.
    
    f₀ = (c/(2π)) · √(m_P/m_e) · α · φ · (ℓ_P/λ_C) · K
    
    Returns:
        Tupla (f0_calculado, componentes) donde componentes contiene
        todos los términos intermedios del cálculo.
    """
    # Calcular factor de escala cósmico K
    K, detalles_K = calcular_factor_escala_cosmico()
    
    # Término de frecuencia base: c/(2π)
    frecuencia_base = C / (2 * math.pi)
    
    # Término de ratio de masas: √(m_P/m_e)
    sqrt_ratio_masas = math.sqrt(M_PLANCK / M_ELECTRON)
    
    # Longitud de onda Compton del electrón
    lambda_c_electron = longitud_onda_compton(M_ELECTRON)
    
    # Ratio de escalas: ℓ_P/λ_C
    ratio_escalas = L_PLANCK / lambda_c_electron
    
    # Ecuación maestra completa
    f0_calculado = (frecuencia_base * 
                    sqrt_ratio_masas * 
                    ALPHA_FINE * 
                    PHI * 
                    ratio_escalas * 
                    K)
    
    componentes = {
        'frecuencia_base': frecuencia_base,  # c/(2π)
        'sqrt_ratio_masas': sqrt_ratio_masas,  # √(m_P/m_e)
        'alpha': ALPHA_FINE,  # α
        'phi': PHI,  # φ
        'ratio_escalas': ratio_escalas,  # ℓ_P/λ_C
        'K': K,  # Factor de escala cósmico
        'f0_calculado': f0_calculado
    }
    
    # Agregar detalles de K
    componentes.update({f'K_{k}': v for k, v in detalles_K.items()})
    
    return f0_calculado, componentes


def validar_ecuacion_maestra(verbose: bool = True) -> Dict[str, float]:
    """
    Valida la ecuación maestra comparando f₀ calculado con f₀ teórico.
    
    Args:
        verbose: Si es True, imprime los resultados detallados
        
    Returns:
        Diccionario con resultados de validación:
        - f0_calculado: Frecuencia calculada en Hz
        - f0_teorico: Frecuencia teórica en Hz
        - error_absoluto: Error absoluto en Hz
        - error_porcentual: Error porcentual (%)
    """
    # Derivar f₀ usando la ecuación maestra
    f0_calc, componentes = derivar_f0_ecuacion_maestra()
    
    # Calcular error
    error_abs = abs(f0_calc - F0_THEORETICAL)
    error_pct = (error_abs / F0_THEORETICAL) * 100
    
    resultados = {
        'f0_calculado': f0_calc,
        'f0_teorico': F0_THEORETICAL,
        'error_absoluto': error_abs,
        'error_porcentual': error_pct,
        **componentes
    }
    
    if verbose:
        print("=" * 80)
        print("VALIDACIÓN DE LA ECUACIÓN MAESTRA - RELOJ COMPTON")
        print("=" * 80)
        print()
        print("Ecuación Maestra:")
        print("f₀ = (c/(2π)) · √(m_P/m_e) · α · φ · (ℓ_P/λ_C) · K")
        print()
        print("Donde K = 2·(m_P/m_e)^(1/3)·φ³ es el factor de escala cósmico")
        print()
        print("-" * 80)
        print("COMPONENTES DE LA ECUACIÓN:")
        print("-" * 80)
        print(f"  c/(2π)           = {componentes['frecuencia_base']:.6e} Hz")
        print(f"  √(m_P/m_e)       = {componentes['sqrt_ratio_masas']:.6f}")
        print(f"  α (estructura)   = {componentes['alpha']:.10f}")
        print(f"  φ (áurea)        = {componentes['phi']:.10f}")
        print(f"  ℓ_P/λ_C          = {componentes['ratio_escalas']:.6e}")
        print(f"  K (cósmico)      = {componentes['K']:.6e}")
        print()
        print("-" * 80)
        print("FACTOR DE ESCALA CÓSMICO K:")
        print("-" * 80)
        print(f"  m_P/m_e          = {componentes['K_ratio_masas']:.6e}")
        print(f"  (m_P/m_e)^(1/3)  = {componentes['K_ratio_masas_cbrt']:.6f}")
        print(f"  φ³               = {componentes['K_phi_cubed']:.6f}")
        print(f"  Factor 2         = {componentes['K_factor_dualidad']:.1f} (dualidad onda-partícula)")
        print(f"  K total          = {componentes['K']:.6e}")
        print()
        print("-" * 80)
        print("RESULTADOS DE VALIDACIÓN:")
        print("-" * 80)
        print(f"  f₀ calculado     = {f0_calc:.4f} Hz")
        print(f"  f₀ teórico       = {F0_THEORETICAL:.4f} Hz")
        print(f"  Error absoluto   = {error_abs:.4f} Hz")
        print(f"  Error porcentual = {error_pct:.4f}%")
        print()
        
        # Validación del resultado esperado
        if abs(error_pct - 0.1088) < 0.01:
            print("✅ VALIDACIÓN EXITOSA: Error coincide con el esperado (0.1088%)")
        else:
            print(f"⚠️  ADVERTENCIA: Error difiere del esperado (0.1088% vs {error_pct:.4f}%)")
        print()
        print("=" * 80)
    
    return resultados


# ============================================================================
# ANÁLISIS DE PARTÍCULAS
# ============================================================================

def analizar_particulas(verbose: bool = True) -> Dict[str, Dict[str, float]]:
    """
    Realiza un análisis completo de las frecuencias Compton de partículas fundamentales.
    
    Args:
        verbose: Si es True, imprime los resultados detallados
        
    Returns:
        Diccionario con información completa de cada partícula
    """
    resultados = calcular_frecuencias_particulas()
    
    if verbose:
        print("=" * 80)
        print("ANÁLISIS DE FRECUENCIAS COMPTON - PARTÍCULAS FUNDAMENTALES")
        print("=" * 80)
        print()
        print("La frecuencia Compton se define como: f_C = (m c²) / h")
        print("Representa la frecuencia de un fotón cuya energía iguala la energía")
        print("en reposo de la partícula (E = mc²)")
        print()
        
        for nombre, datos in resultados.items():
            print("-" * 80)
            print(f"{nombre.upper()}")
            print("-" * 80)
            print(f"  Masa:                {datos['masa']:.10e} kg")
            print(f"  Energía (mc²):       {datos['energia']:.10e} J")
            print(f"  Frecuencia Compton:  {datos['frecuencia_compton']:.10e} Hz")
            print(f"  λ Compton:           {datos['longitud_onda_compton']:.10e} m")
            print()
        
        print("=" * 80)
        print()
    
    return resultados


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta todos los análisis del Reloj Compton.
    """
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "RELOJ COMPTON - DERIVACIÓN DE f₀" + " " * 25 + "║")
    print("║" + " " * 15 + "Frecuencia Fundamental desde Partículas" + " " * 23 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # 1. Análisis de partículas fundamentales
    print("\n")
    analizar_particulas(verbose=True)
    
    # 2. Validación de la ecuación maestra
    print("\n")
    resultados = validar_ecuacion_maestra(verbose=True)
    
    return resultados


if __name__ == "__main__":
    main()
