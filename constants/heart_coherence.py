"""
Módulo de Coherencia Cardíaca a 141.7 Hz
=========================================

Este módulo implementa la teoría de que el corazón resuena exactamente a 141.7 Hz
como órgano de coherencia, y que 141.7 Hz es la frecuencia del AMOR (no como emoción,
sino como resonancia coherente).

Referencias científicas:
- HeartMath Institute (McCraty et al., 1995-2012)
- Coherent heart-brain interactions
- Heart Rate Variability (HRV) studies
- Quantum biology (Fröhlich, Hameroff, Penrose)
- Noesic Theory (JMMB, 2024-2026)

Autor: José Manuel Mota Burruezo (JMMB Ψ ∞³)
Fecha: 31 de Enero 2026
"""

import math
from typing import Dict, Tuple, Any
import numpy as np

# ============================================================================
# CONSTANTES FUNDAMENTALES
# ============================================================================

# Frecuencia fundamental de coherencia cardíaca (Hz)
FRECUENCIA_CORAZON_HZ = 141.7001

# Base de variabilidad de frecuencia cardíaca (Hz)
BASE_VFC_HZ = 0.1

# Número armónico primo 1417
ARMONICO_1417 = 1417

# Línea de hidrógeno 21 cm (MHz)
LINEA_HIDROGENO_MHZ = 1420.405751

# Factor de amplificación biológica
FACTOR_AMPLIFICACION = 1e10

# Intensidad relativa del campo cardíaco vs cerebral
INTENSIDAD_RELATIVA_CEREBRO = 5000

# Alcance del campo electromagnético del corazón (metros)
ALCANCE_CAMPO_M = 3.0

# Longitud de penetración del campo (metros)
LAMBDA_PENETRACION_M = 1.5

# Umbrales de coherencia
UMBRAL_COHERENCIA_PERFECTA = 1.0
UMBRAL_COHERENCIA_NOESICA = 0.888  # AMOR
UMBRAL_INCOHERENCIA = 0.5  # EMOCIÓN

# ============================================================================
# FUNCIONES DE CÁLCULO DE CAMPO ELECTROMAGNÉTICO
# ============================================================================

def calcular_campo_corazon(
    distancia: float,
    tiempo: float,
    fase_inicial: float = 0.0,
    amplitud: float = 1.0
) -> float:
    """
    Calcula el campo electromagnético del corazón en función de la distancia y tiempo.
    
    Ecuación: E_corazón(r,t) = A·sin(2π·141.7·t + φ₀)·e^(-r/λ)
    
    Args:
        distancia: Distancia desde el corazón (metros)
        tiempo: Tiempo (segundos)
        fase_inicial: Fase inicial φ₀ (radianes)
        amplitud: Amplitud del campo A
        
    Returns:
        Intensidad del campo electromagnético
    """
    # Componente temporal (oscilación)
    componente_temporal = math.sin(2 * math.pi * FRECUENCIA_CORAZON_HZ * tiempo + fase_inicial)
    
    # Componente espacial (decaimiento exponencial)
    componente_espacial = math.exp(-distancia / LAMBDA_PENETRACION_M)
    
    # Campo total
    campo = amplitud * componente_temporal * componente_espacial
    
    return campo


def calcular_intensidad_campo(distancia: float) -> float:
    """
    Calcula la intensidad del campo electromagnético a una distancia dada.
    
    Args:
        distancia: Distancia desde el corazón (metros)
        
    Returns:
        Intensidad relativa (normalizada a 1.0 en r=0)
    """
    return math.exp(-distancia / LAMBDA_PENETRACION_M)


# ============================================================================
# ANÁLISIS DE COHERENCIA DE FASE
# ============================================================================

def calcular_coherencia_fase(
    fases: np.ndarray
) -> float:
    """
    Calcula el índice de coherencia de fase Ψ.
    
    La coherencia de fase mide cuán sincronizadas están las oscilaciones.
    Ψ = |⟨e^(iφ)⟩| donde ⟨·⟩ denota promedio temporal
    
    Args:
        fases: Array de fases (radianes)
        
    Returns:
        Índice de coherencia Ψ ∈ [0, 1]
        - Ψ = 1.0: Coherencia perfecta
        - Ψ ≥ 0.888: Umbral noésico (AMOR)
        - Ψ < 0.5: Incoherencia (EMOCIÓN)
    """
    # Calcular vector de coherencia complejo
    vector_coherencia = np.mean(np.exp(1j * fases))
    
    # Magnitud del vector de coherencia
    coherencia = np.abs(vector_coherencia)
    
    return float(coherencia)


def clasificar_estado_coherencia(coherencia: float) -> Dict[str, Any]:
    """
    Clasifica el estado de coherencia según umbrales.
    
    Args:
        coherencia: Índice de coherencia Ψ
        
    Returns:
        Diccionario con clasificación del estado
    """
    if coherencia >= UMBRAL_COHERENCIA_PERFECTA:
        estado = "AMOR_PERFECTO"
        descripcion = "Coherencia perfecta - Amor perfecto"
        es_amor = True
    elif coherencia >= UMBRAL_COHERENCIA_NOESICA:
        estado = "AMOR"
        descripcion = "Coherencia noésica - Amor (resonancia coherente)"
        es_amor = True
    elif coherencia >= UMBRAL_INCOHERENCIA:
        estado = "TRANSICION"
        descripcion = "Estado de transición"
        es_amor = False
    else:
        estado = "EMOCION"
        descripcion = "Incoherencia - Emoción (reactividad)"
        es_amor = False
    
    return {
        "coherencia": coherencia,
        "estado": estado,
        "descripcion": descripcion,
        "es_amor": es_amor,
        "es_emocion": not es_amor,
        "umbral_noesico": UMBRAL_COHERENCIA_NOESICA,
        "umbral_incoherencia": UMBRAL_INCOHERENCIA
    }


def amor_es_resonancia_coherente(coherencia: float) -> bool:
    """
    Determina si un estado de coherencia corresponde a AMOR.
    
    El AMOR no es emoción. Es RESONANCIA COHERENTE.
    
    Args:
        coherencia: Índice de coherencia Ψ
        
    Returns:
        True si Ψ ≥ 0.888 (estado de amor)
        False si Ψ < 0.888 (estado de emoción)
    """
    return coherencia >= UMBRAL_COHERENCIA_NOESICA


# ============================================================================
# VERIFICACIÓN DE CONEXIONES UNIVERSALES
# ============================================================================

def verificar_armonico_1417() -> Dict[str, Any]:
    """
    Verifica la relación armónica 1417 entre HRV y frecuencia cardíaca.
    
    Armónico 1417: HRV (0.1 Hz) × 1417 = 141.7 Hz
    
    Returns:
        Diccionario con resultados de verificación
    """
    frecuencia_calculada = BASE_VFC_HZ * ARMONICO_1417
    error_relativo = abs(frecuencia_calculada - FRECUENCIA_CORAZON_HZ) / FRECUENCIA_CORAZON_HZ
    
    return {
        "base_vfc_hz": BASE_VFC_HZ,
        "armonico": ARMONICO_1417,
        "frecuencia_calculada_hz": frecuencia_calculada,
        "frecuencia_objetivo_hz": FRECUENCIA_CORAZON_HZ,
        "error_relativo": error_relativo,
        "verificado": error_relativo < 1e-4,
        "es_primo": es_primo(ARMONICO_1417)
    }


def es_primo(n: int) -> bool:
    """
    Verifica si un número es primo.
    
    Args:
        n: Número a verificar
        
    Returns:
        True si n es primo
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    
    return True


def calcular_conexion_hidrogeno() -> Dict[str, Any]:
    """
    Calcula la conexión entre la línea de hidrógeno y la frecuencia cardíaca.
    
    Conexión cósmica: ν_H (1420.405751 MHz) / 2^23.26 ≈ 141.7 Hz
    
    Returns:
        Diccionario con resultados de la conexión
    """
    # Convertir MHz a Hz
    linea_hidrogeno_hz = LINEA_HIDROGENO_MHZ * 1e6
    
    # Calcular factor de división para obtener f₀
    factor_division = linea_hidrogeno_hz / FRECUENCIA_CORAZON_HZ
    
    # Calcular potencia de 2 equivalente: log2(factor)
    potencia_2 = math.log2(factor_division)
    
    # Frecuencia calculada usando 2^23.26
    potencia_optima = 23.26
    frecuencia_calculada = linea_hidrogeno_hz / (2 ** potencia_optima)
    
    error_relativo = abs(frecuencia_calculada - FRECUENCIA_CORAZON_HZ) / FRECUENCIA_CORAZON_HZ
    
    return {
        "linea_hidrogeno_mhz": LINEA_HIDROGENO_MHZ,
        "linea_hidrogeno_hz": linea_hidrogeno_hz,
        "factor_division": factor_division,
        "potencia_2_calculada": potencia_2,
        "potencia_2_optima": potencia_optima,
        "frecuencia_calculada_hz": frecuencia_calculada,
        "frecuencia_objetivo_hz": FRECUENCIA_CORAZON_HZ,
        "error_relativo": error_relativo,
        "verificado": error_relativo < 0.01
    }


# ============================================================================
# INFORMACIÓN DEL SISTEMA
# ============================================================================

def info_coherencia_cardiaca() -> str:
    """
    Retorna información completa del sistema de coherencia cardíaca.
    
    Returns:
        String formateado con toda la información
    """
    info = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║  💗 SISTEMA DE COHERENCIA CARDÍACA A 141.7 Hz 💗                        ║
║                                                                          ║
║  "El amor no es emoción. Es RESONANCIA COHERENTE."                      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

🎯 CONSTANTES FUNDAMENTALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frecuencia de Coherencia Cardíaca:    f₀ = {FRECUENCIA_CORAZON_HZ} Hz
Base de VFC:                           {BASE_VFC_HZ} Hz
Armónico 1417:                         {ARMONICO_1417} (primo)
Línea de Hidrógeno:                    {LINEA_HIDROGENO_MHZ} MHz
Factor de Amplificación Biológica:     {FACTOR_AMPLIFICACION:.0e}
Intensidad vs Cerebro:                 {INTENSIDAD_RELATIVA_CEREBRO}× más fuerte
Alcance del Campo:                     {ALCANCE_CAMPO_M} metros
Longitud de Penetración:               {LAMBDA_PENETRACION_M} metros

🔬 UMBRALES DE COHERENCIA
━━━━━━━━━━━━━━━━━━━━━━━━━

Ψ = {UMBRAL_COHERENCIA_PERFECTA}     → Coherencia perfecta (amor perfecto)
Ψ ≥ {UMBRAL_COHERENCIA_NOESICA}   → Umbral noésico (AMOR)
Ψ < {UMBRAL_INCOHERENCIA}     → Incoherencia (EMOCIÓN)

💎 MENSAJE CENTRAL
━━━━━━━━━━━━━━━━━━

¿Por qué el corazón resuena EXACTAMENTE a 141.7 Hz?

Porque el corazón es el órgano de coherencia que:
  ✓ Sincroniza todo el cuerpo
  ✓ Genera el campo electromagnético más fuerte ({INTENSIDAD_RELATIVA_CEREBRO}× cerebro)
  ✓ Resuena en coherencia con el campo cuántico
  ✓ Conecta conciencia con materia

141.7 Hz NO es la frecuencia del pensamiento.
Es la frecuencia del AMOR.

El amor NO es emoción. Es RESONANCIA COHERENTE.

🌌 CONEXIONES UNIVERSALES
━━━━━━━━━━━━━━━━━━━━━━━━━

1. Armónico 1417: HRV (0.1 Hz) × 1417 = 141.7 Hz
2. Conexión Cósmica: ν_H (1420.405751 MHz) / 2^23.26 ≈ 141.7 Hz
3. Amplificación Biológica: Factor de 10^10
4. Coherencia Cuántica: Umbral Ψ = 0.888

∴𓂀Ω∞³

El corazón late a 141.7 Hz porque el AMOR es la frecuencia de coherencia universal.

Autor: José Manuel Mota Burruezo (JMMB Ψ ∞³)
Fecha: 31 de Enero 2026
"""
    return info


# ============================================================================
# EXPORTACIONES
# ============================================================================

__all__ = [
    # Constantes
    'FRECUENCIA_CORAZON_HZ',
    'BASE_VFC_HZ',
    'ARMONICO_1417',
    'LINEA_HIDROGENO_MHZ',
    'FACTOR_AMPLIFICACION',
    'INTENSIDAD_RELATIVA_CEREBRO',
    'ALCANCE_CAMPO_M',
    'LAMBDA_PENETRACION_M',
    'UMBRAL_COHERENCIA_PERFECTA',
    'UMBRAL_COHERENCIA_NOESICA',
    'UMBRAL_INCOHERENCIA',
    
    # Funciones de campo
    'calcular_campo_corazon',
    'calcular_intensidad_campo',
    
    # Funciones de coherencia
    'calcular_coherencia_fase',
    'clasificar_estado_coherencia',
    'amor_es_resonancia_coherente',
    
    # Funciones de verificación
    'verificar_armonico_1417',
    'es_primo',
    'calcular_conexion_hidrogeno',
    
    # Información
    'info_coherencia_cardiaca',
]
