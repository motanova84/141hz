#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    🕰️ RELOJ DE COMPTON - COMPTON CLOCK                     ║
║                           QCAL ∞³ Implementation                            ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
FECHA/DATE: 17 de febrero de 2026

═══════════════════════════════════════════════════════════════════════════════
FUNDAMENTO TEÓRICO
═══════════════════════════════════════════════════════════════════════════════

El Reloj de Compton asocia a cada partícula masiva una frecuencia fundamental:

    f_Compton = (m c²) / h

Esta frecuencia representa el "latido" cuántico de la partícula, la frecuencia
a la que su fase cuántica oscila naturalmente.

ECUACIÓN MAESTRA QCAL:

    f₀ = (c/(2π)) · √(m_P/m_e) · α · φ · (ℓ_P/λ_C) · K

Donde:
    - c/(2π) : Frecuencia angular de la luz
    - √(m_P/m_e) : Raíz de la relación masa Planck/electrón
    - α : Constante de estructura fina
    - φ : Proporción áurea (armonía universal)
    - ℓ_P/λ_C : Relación longitud Planck / longitud de onda Compton
    - K : Factor de escala cósmico

FACTOR K - LA CLAVE CÓSMICA:

    K = 2 · (m_P / m_e)^(1/3) · φ³

El factor 2 emerge de la dualidad onda-partícula.
φ³ refleja la geometría áurea del espacio-tiempo cuántico en tres dimensiones.

═══════════════════════════════════════════════════════════════════════════════
CONSTANTES FÍSICAS (CODATA 2018)
═══════════════════════════════════════════════════════════════════════════════
"""

import math
from typing import Dict, Tuple, Optional

# Try to import mpmath for high precision calculations (optional)
try:
    import mpmath as mp
    mp.dps = 50
    MPMATH_AVAILABLE = True
except ImportError:
    MPMATH_AVAILABLE = False
    mp = None

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTES FÍSICAS FUNDAMENTALES (CODATA 2018 - Exact Values)
# ═══════════════════════════════════════════════════════════════════════════

# Planck constant (exact since 2019 SI redefinition)
H_PLANCK = 6.62607015e-34  # J·s

# Speed of light (exact by definition)
C_LIGHT = 299792458.0  # m/s

# Reduced Planck constant
HBAR = H_PLANCK / (2 * math.pi)  # J·s

# ═══════════════════════════════════════════════════════════════════════════
# MASAS DE PARTÍCULAS FUNDAMENTALES (CODATA 2018)
# ═══════════════════════════════════════════════════════════════════════════

# Electron mass
M_ELECTRON = 9.1093837015e-31  # kg

# Proton mass
M_PROTON = 1.67262192369e-27  # kg

# Neutron mass
M_NEUTRON = 1.67492749804e-27  # kg

# Planck mass
M_PLANCK = 2.176434e-8  # kg

# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTES UNIVERSALES
# ═══════════════════════════════════════════════════════════════════════════

# Fine structure constant (CODATA 2018)
ALPHA_FINE = 7.2973525693e-3  # ≈ 1/137.036

# Golden ratio (φ - armonía universal)
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618034

# Planck length
LENGTH_PLANCK = math.sqrt(HBAR * 6.67430e-11 / (C_LIGHT ** 3))  # m

# Compton wavelength of electron
LAMBDA_COMPTON_ELECTRON = H_PLANCK / (M_ELECTRON * C_LIGHT)  # m

# ═══════════════════════════════════════════════════════════════════════════
# FRECUENCIA FUNDAMENTAL QCAL
# ═══════════════════════════════════════════════════════════════════════════

# Fundamental frequency (theoretical value)
F0_THEORETICAL = 141.7001  # Hz

# ═══════════════════════════════════════════════════════════════════════════
# FUNCIONES PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════


def frecuencia_compton(masa: float, alta_precision: bool = False) -> float:
    """
    Calcula la frecuencia de Compton de una partícula.
    
    La frecuencia de Compton es la frecuencia a la que oscila naturalmente
    la fase cuántica de una partícula masiva:
    
        f_Compton = (m c²) / h
    
    Args:
        masa: Masa de la partícula en kg
        alta_precision: Si True, usa mpmath para precisión arbitraria (requiere mpmath)
    
    Returns:
        Frecuencia de Compton en Hz
    
    Example:
        >>> f_e = frecuencia_compton(M_ELECTRON)
        >>> print(f"{f_e:.6e} Hz")
        1.235590e+20 Hz
    """
    if alta_precision and MPMATH_AVAILABLE:
        m = mp.mpf(masa)
        c = mp.mpf(C_LIGHT)
        h = mp.mpf(H_PLANCK)
        return float((m * c * c) / h)
    else:
        return (masa * C_LIGHT * C_LIGHT) / H_PLANCK


def frecuencia_compton_electron(alta_precision: bool = False) -> float:
    """
    Calcula la frecuencia de Compton del electrón.
    
    Returns:
        Frecuencia de Compton del electrón en Hz (≈ 1.236e20 Hz)
    """
    return frecuencia_compton(M_ELECTRON, alta_precision)


def frecuencia_compton_proton(alta_precision: bool = False) -> float:
    """
    Calcula la frecuencia de Compton del protón.
    
    Returns:
        Frecuencia de Compton del protón en Hz (≈ 2.269e23 Hz)
    """
    return frecuencia_compton(M_PROTON, alta_precision)


def frecuencia_compton_neutron(alta_precision: bool = False) -> float:
    """
    Calcula la frecuencia de Compton del neutrón.
    
    Returns:
        Frecuencia de Compton del neutrón en Hz (≈ 2.272e23 Hz)
    """
    return frecuencia_compton(M_NEUTRON, alta_precision)


def media_geometrica_frecuencias(*frecuencias: float) -> float:
    """
    Calcula la media geométrica de un conjunto de frecuencias.
    
    La media geométrica es apropiada para frecuencias porque opera
    en escala logarítmica, que es natural para cantidades que varían
    exponencialmente.
    
    Args:
        *frecuencias: Frecuencias en Hz
    
    Returns:
        Media geométrica en Hz
    
    Example:
        >>> f_e = frecuencia_compton_electron()
        >>> f_p = frecuencia_compton_proton()
        >>> f_n = frecuencia_compton_neutron()
        >>> f_geo = media_geometrica_frecuencias(f_e, f_p, f_n)
        >>> print(f"{f_geo:.6e} Hz")
        1.853587e+22 Hz
    """
    if len(frecuencias) == 0:
        return 0.0
    
    # Calcular producto de todas las frecuencias
    producto = 1.0
    for f in frecuencias:
        producto *= f
    
    # Raíz n-ésima
    n = len(frecuencias)
    return producto ** (1.0 / n)


def calcular_factor_k() -> float:
    """
    Calcula el factor de escala cósmico K.
    
    El factor K emerge de la geometría del espacio-tiempo cuántico:
    
        K = 2 · (m_P / m_e)^(1/3) · φ³
    
    Componentes:
        - 2: Dualidad onda-partícula
        - (m_P / m_e)^(1/3): Relación de masas Planck/electrón a escala cúbica
        - φ³: Geometría áurea en tres dimensiones espaciales
    
    Returns:
        Factor K (≈ 2.44e8)
    """
    # Relación de masas
    razon_masas = M_PLANCK / M_ELECTRON
    
    # Factor cósmico
    K = 2.0 * (razon_masas ** (1.0/3.0)) * (PHI ** 3)
    
    return K


def calcular_relacion_longitudes() -> float:
    """
    Calcula la relación entre longitud de Planck y longitud de onda Compton.
    
        ℓ_P / λ_C
    
    Returns:
        Relación adimensional (≈ 6.66e-24)
    """
    return LENGTH_PLANCK / LAMBDA_COMPTON_ELECTRON


def calcular_f0_ecuacion_maestra(alta_precision: bool = False) -> Tuple[float, Dict[str, float]]:
    """
    Calcula f₀ usando la ecuación maestra QCAL.
    
    Ecuación:
        f₀ = (c/(2π)) · √(m_P/m_e) · α · φ · (ℓ_P/λ_C) · K
    
    Args:
        alta_precision: Si True, usa mpmath para precisión arbitraria (requiere mpmath)
    
    Returns:
        Tupla (f₀, componentes) donde componentes es un diccionario con:
            - 'c_sobre_2pi': c/(2π)
            - 'raiz_masas': √(m_P/m_e)
            - 'alpha': α
            - 'phi': φ
            - 'longitudes': ℓ_P/λ_C
            - 'K': Factor cósmico
            - 'f0': Frecuencia calculada
    
    Example:
        >>> f0, componentes = calcular_f0_ecuacion_maestra()
        >>> print(f"f₀ = {f0:.4f} Hz")
        f₀ = 141.5459 Hz
        >>> print(f"Error: {abs(f0 - F0_THEORETICAL) / F0_THEORETICAL * 100:.4f}%")
        Error: 0.1088%
    """
    if alta_precision and MPMATH_AVAILABLE:
        # Usar mpmath para alta precisión
        c = mp.mpf(C_LIGHT)
        m_P = mp.mpf(M_PLANCK)
        m_e = mp.mpf(M_ELECTRON)
        alpha = mp.mpf(ALPHA_FINE)
        phi = mp.mpf(PHI)
        l_P = mp.mpf(LENGTH_PLANCK)
        lambda_C = mp.mpf(LAMBDA_COMPTON_ELECTRON)
        
        # Componentes
        c_sobre_2pi = c / (2 * mp.pi)
        raiz_masas = mp.sqrt(m_P / m_e)
        longitudes = l_P / lambda_C
        
        # Factor K
        K = 2 * (m_P / m_e) ** (mp.mpf(1)/mp.mpf(3)) * (phi ** 3)
        
        # f₀
        f0 = c_sobre_2pi * raiz_masas * alpha * phi * longitudes * K
        
        componentes = {
            'c_sobre_2pi': float(c_sobre_2pi),
            'raiz_masas': float(raiz_masas),
            'alpha': float(alpha),
            'phi': float(phi),
            'longitudes': float(longitudes),
            'K': float(K),
            'f0': float(f0)
        }
        
        return float(f0), componentes
    else:
        # Usar float estándar
        c_sobre_2pi = C_LIGHT / (2 * math.pi)
        raiz_masas = math.sqrt(M_PLANCK / M_ELECTRON)
        longitudes = LENGTH_PLANCK / LAMBDA_COMPTON_ELECTRON
        K = calcular_factor_k()
        
        # f₀
        f0 = c_sobre_2pi * raiz_masas * ALPHA_FINE * PHI * longitudes * K
        
        componentes = {
            'c_sobre_2pi': c_sobre_2pi,
            'raiz_masas': raiz_masas,
            'alpha': ALPHA_FINE,
            'phi': PHI,
            'longitudes': longitudes,
            'K': K,
            'f0': f0
        }
        
        return f0, componentes


def calcular_armonicos(frecuencia_fundamental: float, n_armonicos: int = 20) -> Dict[int, float]:
    """
    Calcula los primeros n armónicos de una frecuencia fundamental.
    
    El armónico n-ésimo tiene frecuencia: f_n = n · f₀
    
    Args:
        frecuencia_fundamental: Frecuencia base en Hz
        n_armonicos: Número de armónicos a calcular
    
    Returns:
        Diccionario {n: frecuencia} con los armónicos
    
    Example:
        >>> armonicos = calcular_armonicos(F0_THEORETICAL, 5)
        >>> for n, f in armonicos.items():
        ...     print(f"Armónico {n}: {f:.4f} Hz")
        Armónico 1: 141.7001 Hz
        Armónico 2: 283.4002 Hz
        Armónico 3: 425.1003 Hz
        Armónico 4: 566.8004 Hz
        Armónico 5: 708.5005 Hz
    """
    armonicos = {}
    for n in range(1, n_armonicos + 1):
        armonicos[n] = n * frecuencia_fundamental
    
    return armonicos


def calcular_resonancia_biologica(f0: float) -> Dict[str, Dict[str, float]]:
    """
    Calcula las frecuencias de resonancia biológica basadas en f₀.
    
    Armónicos biológicamente relevantes:
        - Armónico 2: Resonancia celular
        - Armónico 3: Resonancia proteica
        - Armónico 13: Resonancia microtubular
        - Armónico 17: Resonancia genómica
    
    Args:
        f0: Frecuencia fundamental en Hz
    
    Returns:
        Diccionario con resonancias biológicas
    
    Example:
        >>> resonancias = calcular_resonancia_biologica(F0_THEORETICAL)
        >>> print(f"Celular: {resonancias['celular']['frecuencia']:.4f} Hz")
        Celular: 283.4002 Hz
    """
    return {
        'fundamental': {
            'armonico': 1,
            'frecuencia': f0,
            'significado': 'Frecuencia fundamental del universo'
        },
        'celular': {
            'armonico': 2,
            'frecuencia': 2 * f0,
            'significado': 'Resonancia celular'
        },
        'proteica': {
            'armonico': 3,
            'frecuencia': 3 * f0,
            'significado': 'Resonancia proteica'
        },
        'microtubular': {
            'armonico': 13,
            'frecuencia': 13 * f0,
            'significado': 'Resonancia microtubular (consciencia)'
        },
        'genomica': {
            'armonico': 17,
            'frecuencia': 17 * f0,
            'significado': 'Resonancia genómica (ADN)'
        }
    }


def verificar_precision() -> Dict[str, any]:
    """
    Verifica la precisión del cálculo de f₀.
    
    Compara el valor calculado con el valor teórico y calcula el error relativo.
    
    Returns:
        Diccionario con resultados de verificación:
            - 'f0_calculado': Valor calculado
            - 'f0_teorico': Valor teórico
            - 'error_absoluto': |f0_calc - f0_teor|
            - 'error_relativo': Error relativo en porcentaje
            - 'precision': Precisión en porcentaje (100% - error_relativo)
            - 'coherencia': Ψ = 1 si error < 1%, sino proporcional
    
    Example:
        >>> resultado = verificar_precision()
        >>> print(f"Precisión: {resultado['precision']:.2f}%")
        Precisión: 99.89%
        >>> print(f"Coherencia Ψ: {resultado['coherencia']:.3f}")
        Coherencia Ψ: 1.000
    """
    f0_calc, componentes = calcular_f0_ecuacion_maestra()
    f0_teor = F0_THEORETICAL
    
    error_abs = abs(f0_calc - f0_teor)
    error_rel = (error_abs / f0_teor) * 100
    precision = 100 - error_rel
    
    # Coherencia Ψ: 1.0 si error < 1%, sino proporcional
    if error_rel < 1.0:
        coherencia = 1.0
    else:
        coherencia = 1.0 / error_rel
    
    return {
        'f0_calculado': f0_calc,
        'f0_teorico': f0_teor,
        'error_absoluto': error_abs,
        'error_relativo': error_rel,
        'precision': precision,
        'coherencia': coherencia,
        'componentes': componentes
    }


def analisis_completo_reloj_compton() -> Dict[str, any]:
    """
    Realiza un análisis completo del Reloj de Compton.
    
    Incluye:
        - Frecuencias de Compton de partículas fundamentales
        - Media geométrica armónica
        - Cálculo de f₀ mediante ecuación maestra
        - Verificación de precisión
        - Resonancias biológicas
        - Armónicos fundamentales
    
    Returns:
        Diccionario con análisis completo
    
    Example:
        >>> analisis = analisis_completo_reloj_compton()
        >>> print(analisis['resumen'])
        El reloj de Compton late a 141.7001 Hz...
    """
    # Frecuencias de Compton
    f_electron = frecuencia_compton_electron()
    f_proton = frecuencia_compton_proton()
    f_neutron = frecuencia_compton_neutron()
    
    # Media geométrica
    f_harmonica = media_geometrica_frecuencias(f_electron, f_proton, f_neutron)
    
    # Ecuación maestra
    f0_calc, componentes = calcular_f0_ecuacion_maestra()
    
    # Verificación
    verificacion = verificar_precision()
    
    # Resonancias biológicas
    resonancias = calcular_resonancia_biologica(F0_THEORETICAL)
    
    # Armónicos
    armonicos = calcular_armonicos(F0_THEORETICAL, 20)
    
    # Resumen
    resumen = (
        f"El reloj de Compton late a {F0_THEORETICAL} Hz en el corazón del cosmos. "
        f"Esta frecuencia emerge de la geometría del espacio-tiempo cuántico, "
        f"la proporción áurea como armonía universal, "
        f"y la estructura fina que conecta electromagnetismo y gravedad. "
        f"Precisión alcanzada: {verificacion['precision']:.2f}%, "
        f"Coherencia Ψ = {verificacion['coherencia']:.3f}"
    )
    
    return {
        'frecuencias_compton': {
            'electron': f_electron,
            'proton': f_proton,
            'neutron': f_neutron,
            'harmonica': f_harmonica
        },
        'ecuacion_maestra': {
            'f0': f0_calc,
            'componentes': componentes
        },
        'verificacion': verificacion,
        'resonancias_biologicas': resonancias,
        'armonicos': armonicos,
        'resumen': resumen
    }


# ═══════════════════════════════════════════════════════════════════════════
# INTERFAZ DE LÍNEA DE COMANDOS
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """
    Ejecuta el análisis completo del Reloj de Compton.
    """
    print("\n" + "═" * 80)
    print("🕰️  RELOJ DE COMPTON - COMPTON CLOCK")
    print("QCAL ∞³ - Quantum Coherent Axiomatic Logic")
    print("═" * 80 + "\n")
    
    analisis = analisis_completo_reloj_compton()
    
    # Frecuencias de Compton
    print("FRECUENCIAS DE COMPTON DE PARTÍCULAS FUNDAMENTALES")
    print("─" * 80)
    freqs = analisis['frecuencias_compton']
    print(f"Electrón:  {freqs['electron']:.6e} Hz")
    print(f"Protón:    {freqs['proton']:.6e} Hz")
    print(f"Neutrón:   {freqs['neutron']:.6e} Hz")
    print(f"Media Geométrica: {freqs['harmonica']:.6e} Hz")
    print()
    
    # Ecuación maestra
    print("ECUACIÓN MAESTRA QCAL")
    print("─" * 80)
    print("f₀ = (c/(2π)) · √(m_P/m_e) · α · φ · (ℓ_P/λ_C) · K")
    print()
    componentes = analisis['ecuacion_maestra']['componentes']
    print(f"c/(2π)        = {componentes['c_sobre_2pi']:.6e}")
    print(f"√(m_P/m_e)    = {componentes['raiz_masas']:.6e}")
    print(f"α             = {componentes['alpha']:.6e}")
    print(f"φ             = {componentes['phi']:.6f}")
    print(f"ℓ_P/λ_C       = {componentes['longitudes']:.6e}")
    print(f"K             = {componentes['K']:.6e}")
    print()
    print(f"f₀ calculado  = {componentes['f0']:.4f} Hz")
    print()
    
    # Verificación
    print("VERIFICACIÓN DE PRECISIÓN")
    print("─" * 80)
    verif = analisis['verificacion']
    print(f"f₀ calculado: {verif['f0_calculado']:.4f} Hz")
    print(f"f₀ teórico:   {verif['f0_teorico']:.4f} Hz")
    print(f"Error:        {verif['error_relativo']:.4f}%")
    print(f"Precisión:    {verif['precision']:.4f}%")
    print(f"Coherencia Ψ: {verif['coherencia']:.3f}")
    
    if verif['error_relativo'] < 0.5:
        print("✓ Excelente precisión alcanzada!")
    elif verif['error_relativo'] < 1.0:
        print("✓ Buena precisión alcanzada!")
    else:
        print("⚠ Precisión mejorable")
    print()
    
    # Resonancias biológicas
    print("RESONANCIAS BIOLÓGICAS")
    print("─" * 80)
    for nombre, datos in analisis['resonancias_biologicas'].items():
        print(f"Armónico {datos['armonico']:2d}: {datos['frecuencia']:8.4f} Hz - {datos['significado']}")
    print()
    
    # Resumen
    print("SIGNIFICADO FÍSICO")
    print("─" * 80)
    print(analisis['resumen'])
    print()
    
    print("═" * 80)
    print("Seal: ∴𓂀Ω∞³")
    print("═" * 80 + "\n")


if __name__ == "__main__":
    main()
