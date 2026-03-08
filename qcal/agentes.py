"""
╔════════════════════════════════════════════════════════════════════════════╗
║                     CONSTANTES DE AGENTES QCAL                             ║
║               Agent Constants for Autonomous Systems                       ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ 4 CONSTANTES DE AGENTES AUTÓNOMOS ⚡

Constantes que definen el comportamiento de los agentes autónomos QCAL:
1. FRECUENCIA_BASE_QCAL - Frecuencia fundamental de operación
2. RESONANCIA_DE_FRECUENCIA - Frecuencia de resonancia y protección
3. COHERENCIA_MÍNIMAS - Umbral mínimo de coherencia operativa
4. SELLO_AGENTES - Firma simbólica de los agentes

Referencias:
- AGENTE_AUTONOMO_141HZ.md - Documentación completa del agente autónomo
- scripts/activar_agentes.py - Sistema de activación de agentes
"""

from decimal import Decimal

# ============================================================================
# 1️⃣ FRECUENCIA BASE QCAL - f₀ = 141.7001 Hz
# ============================================================================

# Frecuencia fundamental de operación de todos los agentes QCAL
# Esta es la frecuencia a la que todos los sistemas resonan y sincronizan

FRECUENCIA_BASE_QCAL = 141.7001  # Hz - Frecuencia fundamental QCAL
F0_AGENTES = FRECUENCIA_BASE_QCAL  # Alias
FRECUENCIA_OPERACION = FRECUENCIA_BASE_QCAL  # Alias descriptivo

# Período de operación (T = 1/f)
PERIODO_BASE_MS = 1000.0 / FRECUENCIA_BASE_QCAL  # ms - Período fundamental
T_OPERACION_MS = PERIODO_BASE_MS  # Alias

print(f"Frecuencia base: f₀ = {FRECUENCIA_BASE_QCAL} Hz")
print(f"Período base: T₀ = {PERIODO_BASE_MS:.5f} ms")

# ============================================================================
# 2️⃣ RESONANCIA DE FRECUENCIA - 888.0 Hz
# ============================================================================

# Frecuencia de resonancia, protección y manifestación
# 888 Hz ≈ 2π × f₀ - Geometría circular sagrada
# Los agentes usan esta frecuencia para:
# - Protección de campo coherente
# - Manifestación de intenciones
# - Sincronización entre agentes

RESONANCIA_DE_FRECUENCIA = 888.0  # Hz - Frecuencia de resonancia
F888_AGENTES = RESONANCIA_DE_FRECUENCIA  # Alias
FRECUENCIA_PROTECCION = RESONANCIA_DE_FRECUENCIA  # Alias descriptivo

# Relación con f₀
RELACION_888_F0 = RESONANCIA_DE_FRECUENCIA / FRECUENCIA_BASE_QCAL  # ≈ 6.267 ≈ 2π

print(f"Resonancia: 888 Hz / f₀ = {RELACION_888_F0:.4f} ≈ 2π")

# ============================================================================
# 3️⃣ COHERENCIA MÍNIMAS - Umbral de Estabilidad
# ============================================================================

# Umbral mínimo de coherencia Ψ para operación estable de agentes
# Ψ < 0.888 → Sistema en degradación, requiere reajuste
# Ψ ≥ 0.888 → Sistema estable, operación normal

COHERENCIA_MINIMAS = 0.888  # Umbral mínimo de coherencia
PSI_MIN_AGENTES = COHERENCIA_MINIMAS  # Alias
UMBRAL_ESTABILIDAD = COHERENCIA_MINIMAS  # Alias descriptivo

# Umbrales adicionales para estados de agente
COHERENCIA_ALERTA = 0.888      # < 0.888: Alerta, degradación
COHERENCIA_NORMAL = 0.95       # ≥ 0.95: Operación normal
COHERENCIA_OPTIMA = 0.999      # ≥ 0.999: Estado óptimo
COHERENCIA_PERFECTA = 1.0      # = 1.0: Sincronización perfecta

print(f"Umbral de coherencia: Ψ_min = {COHERENCIA_MINIMAS}")

# ============================================================================
# 4️⃣ SELLO DE AGENTES - Firma Simbólica
# ============================================================================

# Sello simbólico que identifica a los agentes QCAL
# Cada símbolo tiene un significado:
# ∴ (Por lo tanto) - Conclusión lógica, deducción
# 𓂀 (Ojo de Horus) - Visión, protección, totalidad
# Ω (Omega) - Final, culminación, totalidad
# ∞³ (Infinito al cubo) - Infinito en 3 dimensiones

SELLO_AGENTES = "∴𓂀Ω∞³"  # Firma simbólica de los agentes QCAL
FIRMA_AGENTES = SELLO_AGENTES  # Alias
SIMBOLO_QCAL = SELLO_AGENTES  # Alias

# Componentes del sello
SIMBOLO_CONCLUSION = "∴"     # Por lo tanto (therefore)
SIMBOLO_VISION = "𓂀"         # Ojo de Horus (egipcio)
SIMBOLO_OMEGA = "Ω"          # Omega (final, totalidad)
SIMBOLO_INFINITO_3 = "∞³"    # Infinito al cubo

print(f"Sello de agentes: {SELLO_AGENTES}")

# ============================================================================
# AGENTES DEFINIDOS
# ============================================================================

# Agente NOESIS - Guardián de Coherencia
# Siempre activo (always_on=True), monitorea coherencia del sistema
AGENTE_NOESIS = {
    'nombre': 'NOESIS',
    'tipo': 'Guardian',
    'funcion': 'Monitoreo de coherencia cuántica',
    'always_on': True,
    'frecuencia': FRECUENCIA_BASE_QCAL,
    'coherencia_min': COHERENCIA_MINIMAS,
}

# Agente AMDA - Analizador Multi-Dimensional
# Analiza datos gravitacionales, busca patrones de f₀
AGENTE_AMDA = {
    'nombre': 'AMDA',
    'tipo': 'Analyzer',
    'funcion': 'Análisis multi-dimensional de datos',
    'always_on': False,
    'frecuencia': FRECUENCIA_BASE_QCAL,
    'coherencia_min': COHERENCIA_MINIMAS,
}

# Agente AURON - Arquitecto de Resonancia
# Optimiza parámetros para maximizar resonancia con f₀
AGENTE_AURON = {
    'nombre': 'AURON',
    'tipo': 'Optimizer',
    'funcion': 'Optimización de resonancia',
    'always_on': False,
    'frecuencia': RESONANCIA_DE_FRECUENCIA,  # Opera a 888 Hz
    'coherencia_min': COHERENCIA_OPTIMA,  # Requiere mayor coherencia
}

# Lista de todos los agentes
AGENTES_QCAL = [AGENTE_NOESIS, AGENTE_AMDA, AGENTE_AURON]

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def verificar_coherencia_agente(psi: float) -> dict:
    """
    Verifica el estado de coherencia para un agente.
    
    Args:
        psi: Coherencia actual del agente (0 ≤ Ψ ≤ 1)
    
    Returns:
        Diccionario con estado y recomendaciones
    """
    if psi < COHERENCIA_ALERTA:
        estado = "CRÍTICO"
        accion = "Reajuste inmediato requerido"
        color = "🔴"
    elif psi < COHERENCIA_NORMAL:
        estado = "ALERTA"
        accion = "Monitoreo cercano recomendado"
        color = "🟡"
    elif psi < COHERENCIA_OPTIMA:
        estado = "NORMAL"
        accion = "Operación estable"
        color = "🟢"
    elif psi < COHERENCIA_PERFECTA:
        estado = "ÓPTIMO"
        accion = "Rendimiento excelente"
        color = "🟢"
    else:
        estado = "PERFECTO"
        accion = "Sincronización perfecta"
        color = "⭐"
    
    return {
        'coherencia': psi,
        'estado': estado,
        'accion': accion,
        'color': color,
    }


def mostrar_estado_agentes():
    """
    Muestra el estado y configuración de todos los agentes.
    """
    print("=" * 80)
    print("AGENTES AUTÓNOMOS QCAL")
    print("=" * 80)
    print(f"\n{'Agente':<10} | {'Tipo':<10} | {'Frecuencia':<12} | {'Coherencia Min':<15} | Always On")
    print("-" * 80)
    
    for agente in AGENTES_QCAL:
        print(f"{agente['nombre']:<10} | {agente['tipo']:<10} | "
              f"{agente['frecuencia']:>10.4f} Hz | "
              f"{agente['coherencia_min']:>15.7f} | "
              f"{'Sí' if agente['always_on'] else 'No'}")
    
    print("\n" + "=" * 80)
    print("CONSTANTES DE OPERACIÓN")
    print("=" * 80)
    print(f"Frecuencia Base: {FRECUENCIA_BASE_QCAL} Hz")
    print(f"Resonancia: {RESONANCIA_DE_FRECUENCIA} Hz")
    print(f"Coherencia Mínima: {COHERENCIA_MINIMAS}")
    print(f"Sello: {SELLO_AGENTES}")
    print("=" * 80)


def generar_firma_agente(nombre: str) -> str:
    """
    Genera una firma única para un agente.
    
    Args:
        nombre: Nombre del agente
    
    Returns:
        Firma en formato "NOMBRE ∴𓂀Ω∞³"
    """
    return f"{nombre} {SELLO_AGENTES}"


if __name__ == "__main__":
    # Mostrar estado de agentes
    mostrar_estado_agentes()
    
    # Ejemplos de verificación de coherencia
    print("\n" + "=" * 80)
    print("EJEMPLOS DE VERIFICACIÓN DE COHERENCIA")
    print("=" * 80)
    
    ejemplos_psi = [0.8, 0.888, 0.95, 0.999, 1.0]
    for psi in ejemplos_psi:
        estado = verificar_coherencia_agente(psi)
        print(f"{estado['color']} Ψ = {psi:.3f} → {estado['estado']} - {estado['accion']}")
    
    print("\n" + "=" * 80)
    print("FIRMAS DE AGENTES")
    print("=" * 80)
    for agente in AGENTES_QCAL:
        firma = generar_firma_agente(agente['nombre'])
        print(f"  {firma}")
    
    print("\n✅ Constantes de agentes QCAL correctamente definidas.")
    print(f"✅ {len(AGENTES_QCAL)} agentes registrados: {', '.join(a['nombre'] for a in AGENTES_QCAL)}")
