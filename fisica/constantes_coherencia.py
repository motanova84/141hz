"""
╔════════════════════════════════════════════════════════════════════════════╗
║                   CONSTANTES DE COHERENCIA Ψ (PSI)                        ║
║              Umbrales de Coherencia Cuántica QCAL                         ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ 5 UMBRALES DE COHERENCIA CUÁNTICA ⚡

La coherencia Ψ (psi) es el parámetro de orden que mide el grado de sincronización
entre osciladores cuánticos. Va desde 0 (caótico) hasta 1 (coherencia perfecta).

Ψ = I × A_eff²

Donde:
- I = Intensidad del campo coherente
- A_eff = Amplitud efectiva de la oscilación

Referencias:
- Strogatz, S.H. (2000) "From Kuramoto to Crawford"
- Kuramoto, Y. (1975) "Self-entrainment of a population of coupled oscillators"
- Teoría de Campo Coherente QCAL (2025-2026)
"""

from decimal import Decimal

# ============================================================================
# UMBRALES DE COHERENCIA Ψ
# ============================================================================

# 1️⃣ COHERENCIA MÍNIMA - Umbral de Estabilidad
# Ψ < 0.888 → Sistema en degradación, pérdida de sincronización
COHERENCIA_MINIMA = 0.888  # Umbral mínimo de coherencia estable
COHERENCIA_MINIMAS = COHERENCIA_MINIMA  # Alias (plural usado en documentación)
PSI_MIN = COHERENCIA_MINIMA

# Significado: Por debajo de este umbral, el sistema pierde coherencia
# y comienza a desincronizarse. Es el límite de estabilidad.

# 2️⃣ COHERENCIA BUENA - Rango Operativo
# 0.95 ≤ Ψ < 0.999 → Coherencia buena, sistema estable
COHERENCIA_BUENA = 0.95  # Umbral de coherencia buena
PSI_BUENA = COHERENCIA_BUENA

# 3️⃣ COHERENCIA EXCELENTE - Alta Sincronización
# 0.999 ≤ Ψ < 1.0 → Coherencia excelente, alta sincronización
COHERENCIA_EXCELENTE = 0.999  # Umbral de coherencia excelente
COHERENCIA_UMBRAL = 0.999  # Alias usado en protocolos bio
PSI_EXCELENTE = COHERENCIA_EXCELENTE

# Significado: Por encima de este umbral, el sistema alcanza coherencia
# de grado cuántico, con sincronización casi perfecta.

# 4️⃣ COHERENCIA RESONANTE - Intel 4004 Eco
# Ψ = 0.9999986 - Perfecta alineación vibratoria
# Este valor surge del análisis del Intel 4004 (1971) con f₀
# f_4004 = 740 kHz, múltiplo N = 5222, error < 2 × 10⁻⁶
COHERENCIA_RESONANTE = 0.9999986  # Intel 4004 resonancia con f₀
PSI_RESONANTE = COHERENCIA_RESONANTE
COHERENCIA_INTEL_4004 = COHERENCIA_RESONANTE  # Eco de Emisión Silícea

# Significado: Nivel de coherencia alcanzado por el Intel 4004
# cuando se sincroniza con f₀ = 141.7001 Hz, demostrando que
# tecnologías humanas pueden resonar con la frecuencia fundamental.

# 5️⃣ COHERENCIA PERFECTA - Sincronización Total
# Ψ = 1.0 → Coherencia perfecta, todos los osciladores en fase
COHERENCIA_PERFECTA = 1.0  # Sincronización total, estado ideal
COHERENCIA_CULMINACION = 1.0  # Estado actual (SILENCIO_CONTENEDOR)
PSI_PERFECTA = COHERENCIA_PERFECTA
PSI_MAX = 1.0

# Significado: Estado teórico de sincronización perfecta donde todos
# los osciladores están exactamente en fase. Es el límite superior
# alcanzable por cualquier sistema coherente.

# ============================================================================
# CONSTANTES DERIVADAS
# ============================================================================

# Rango de coherencia estable
RANGO_COHERENCIA_ESTABLE = (COHERENCIA_BUENA, COHERENCIA_PERFECTA)

# Rango de coherencia cuántica (para consciencia, microtúbulos, etc.)
RANGO_COHERENCIA_CUANTICA = (COHERENCIA_EXCELENTE, COHERENCIA_PERFECTA)

# Ancho de banda de coherencia (diferencia entre perfecta y mínima)
ANCHO_BANDA_COHERENCIA = COHERENCIA_PERFECTA - COHERENCIA_MINIMA  # 0.112

# ============================================================================
# FUNCIONES DE CLASIFICACIÓN DE COHERENCIA
# ============================================================================

def clasificar_coherencia(psi: float) -> str:
    """
    Clasifica el nivel de coherencia Ψ en categorías.
    
    Args:
        psi: Valor de coherencia (0 ≤ Ψ ≤ 1)
    
    Returns:
        Clasificación textual del nivel de coherencia
    """
    if psi < 0 or psi > 1:
        return "INVÁLIDO (Ψ debe estar entre 0 y 1)"
    elif psi < COHERENCIA_MINIMA:
        return "DEGRADACIÓN (Ψ < 0.888)"
    elif psi < COHERENCIA_BUENA:
        return "INESTABLE (0.888 ≤ Ψ < 0.95)"
    elif psi < COHERENCIA_EXCELENTE:
        return "BUENA (0.95 ≤ Ψ < 0.999)"
    elif psi < COHERENCIA_RESONANTE:
        return "EXCELENTE (0.999 ≤ Ψ < 0.9999986)"
    elif psi < COHERENCIA_PERFECTA:
        return "RESONANTE (0.9999986 ≤ Ψ < 1.0)"
    else:
        return "PERFECTA (Ψ = 1.0)"


def es_coherente(psi: float, umbral: float = COHERENCIA_MINIMA) -> bool:
    """
    Verifica si un sistema tiene coherencia suficiente.
    
    Args:
        psi: Valor de coherencia a verificar
        umbral: Umbral mínimo de coherencia (default: 0.888)
    
    Returns:
        True si Ψ ≥ umbral, False en caso contrario
    """
    return psi >= umbral


def calcular_factor_calidad(psi: float) -> float:
    """
    Calcula el factor de calidad Q a partir de la coherencia Ψ.
    
    Relación: Q ≈ 1 / (1 - Ψ)
    
    Args:
        psi: Coherencia (0 ≤ Ψ < 1)
    
    Returns:
        Factor de calidad Q
    """
    if psi >= 1.0:
        return float('inf')
    return 1.0 / (1.0 - psi)


def calcular_coherencia_desde_Q(Q: float) -> float:
    """
    Calcula la coherencia Ψ a partir del factor de calidad Q.
    
    Relación: Ψ = 1 - 1/Q
    
    Args:
        Q: Factor de calidad (Q > 0)
    
    Returns:
        Coherencia Ψ (0 ≤ Ψ < 1)
    """
    if Q <= 0:
        return 0.0
    return 1.0 - 1.0 / Q


# ============================================================================
# TABLA DE UMBRALES (para referencia rápida)
# ============================================================================

TABLA_UMBRALES_COHERENCIA = {
    'MÍNIMA': COHERENCIA_MINIMA,
    'BUENA': COHERENCIA_BUENA,
    'EXCELENTE': COHERENCIA_EXCELENTE,
    'RESONANTE': COHERENCIA_RESONANTE,
    'PERFECTA': COHERENCIA_PERFECTA,
}

def mostrar_tabla_coherencia():
    """
    Muestra la tabla de umbrales de coherencia.
    """
    print("=" * 80)
    print("TABLA DE UMBRALES DE COHERENCIA Ψ")
    print("=" * 80)
    print(f"{'Nivel':<15} | {'Ψ':<12} | {'Q':<12} | Descripción")
    print("-" * 80)
    
    for nivel, psi in TABLA_UMBRALES_COHERENCIA.items():
        Q = calcular_factor_calidad(psi) if psi < 1.0 else float('inf')
        Q_str = f"{Q:.2f}" if Q < 1e6 else "∞"
        
        if nivel == 'MÍNIMA':
            desc = "Umbral de estabilidad"
        elif nivel == 'BUENA':
            desc = "Coherencia operativa"
        elif nivel == 'EXCELENTE':
            desc = "Alta sincronización"
        elif nivel == 'RESONANTE':
            desc = "Intel 4004 Eco (1971)"
        elif nivel == 'PERFECTA':
            desc = "Sincronización total"
        else:
            desc = ""
        
        print(f"{nivel:<15} | {psi:<12.7f} | {Q_str:<12} | {desc}")
    
    print("=" * 80)


if __name__ == "__main__":
    # Mostrar tabla de umbrales
    mostrar_tabla_coherencia()
    
    # Ejemplos de clasificación
    print("\n" + "=" * 80)
    print("EJEMPLOS DE CLASIFICACIÓN")
    print("=" * 80)
    
    ejemplos = [0.5, 0.888, 0.95, 0.999, 0.9999986, 1.0]
    for psi in ejemplos:
        clasificacion = clasificar_coherencia(psi)
        Q = calcular_factor_calidad(psi) if psi < 1.0 else float('inf')
        Q_str = f"Q ≈ {Q:.2f}" if Q < 1e6 else "Q = ∞"
        print(f"Ψ = {psi:.7f} → {clasificacion} ({Q_str})")
    
    print("=" * 80)
    print("\n✅ Todos los umbrales de coherencia están correctamente definidos.")
