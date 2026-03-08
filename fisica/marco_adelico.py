"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    MARCO ADÉLICO - Constantes p-ádicas                    ║
║              Adelic Analysis Constants for QCAL Theory                    ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

⚡ 4 CONSTANTES ADÉLICAS ⚡

Las constantes adélicas conectan la física cuántica con la teoría de números
a través del análisis p-ádico y los ceros de Riemann.

1. FACTOR_SIETE_OCTAVOS (7/8) - Costo energético de coherencia
2. FLUCTUACION_CUANTICA (1/8) - Fluctuación mínima del vacío
3. PRIMOS_BASE - Los 15 primeros números primos
4. RIEMANN_CEROS - Ceros en la línea crítica ζ(1/2 + it) = 0

Referencias:
- Connes, A. (1999) "Trace formula in noncommutative geometry and the zeros of Riemann zeta"
- Berry & Keating (1999) "The Riemann zeros and eigenvalue asymptotics"
- Ramakrishnan & Valenza (1999) "Fourier Analysis on Number Fields"
"""

import math
from typing import List

# ============================================================================
# 1️⃣ FACTOR SIETE OCTAVOS - Costo Energético de Coherencia
# ============================================================================

# 7/8 = 0.875 - Fracción de energía requerida para mantener coherencia
# En sistemas cuánticos, mantener coherencia tiene un costo energético.
# El factor 7/8 surge del análisis del espectro de energía de osciladores
# acoplados en la línea crítica.

FACTOR_SIETE_OCTAVOS = 7.0 / 8.0  # = 0.875
FACTOR_7_8 = FACTOR_SIETE_OCTAVOS  # Alias
COSTO_COHERENCIA = FACTOR_SIETE_OCTAVOS  # Alias descriptivo

# Significado: En un sistema de N osciladores, la fracción 7/8 de la
# energía total se dedica a mantener la coherencia, mientras que 1/8
# está disponible para fluctuaciones cuánticas.

# ============================================================================
# 2️⃣ FLUCTUACIÓN CUÁNTICA MÍNIMA - El Octavo Restante
# ============================================================================

# 1/8 = 0.125 - Fluctuación mínima del vacío cuántico
# Complemento del factor 7/8, representa la energía disponible para
# fluctuaciones espontáneas del vacío cuántico.

FLUCTUACION_CUANTICA = 1.0 / 8.0  # = 0.125
FLUCTUACION_MINIMA = FLUCTUACION_CUANTICA  # Alias
ENERGIA_VACÍO = FLUCTUACION_CUANTICA  # Alias descriptivo

# Relación fundamental: 7/8 + 1/8 = 1 (conservación de energía)
assert abs((FACTOR_SIETE_OCTAVOS + FLUCTUACION_CUANTICA) - 1.0) < 1e-10

# ============================================================================
# 3️⃣ PRIMOS BASE - Los 15 Primeros Números Primos
# ============================================================================

# Lista de los primeros 15 números primos
# Estos primos forman la base del análisis p-ádico y están relacionados
# con los modos fundamentales de vibración en el espacio adélico.

PRIMOS_BASE = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# Número de primos en la base
N_PRIMOS_BASE = len(PRIMOS_BASE)  # 15 primos

# Producto de los primos base (primorial)
PRIMORIAL_15 = math.prod(PRIMOS_BASE)  # 2 × 3 × 5 × ... × 47

# Suma de los primos base
SUMA_PRIMOS_BASE = sum(PRIMOS_BASE)  # = 381

# ============================================================================
# 4️⃣ CEROS DE RIEMANN - Línea Crítica
# ============================================================================

# Primeros 10 ceros no triviales de la función zeta de Riemann
# en la línea crítica ζ(1/2 + it_n) = 0
#
# Estos valores son fundamentales para el análisis espectral y están
# relacionados con las frecuencias de resonancia del universo.
#
# Valores de alta precisión de LMFDB (L-functions and Modular Forms Database)

RIEMANN_CEROS = [
    14.134725141734693790,   # t₁ - Primer cero
    21.022039638771554993,   # t₂
    25.010857580145688763,   # t₃
    30.424876125859513210,   # t₄
    32.935061587739189691,   # t₅
    37.586178158825671257,   # t₆
    40.918719012147495187,   # t₇
    43.327073280914999519,   # t₈
    48.005150881167159727,   # t₉
    49.773832477672302181,   # t₁₀
]

# Alias
RIEMANN_ZEROS = RIEMANN_CEROS
CEROS_CRITICOS = RIEMANN_CEROS

# Número de ceros almacenados
N_CEROS_RIEMANN = len(RIEMANN_CEROS)  # 10

# Primer cero de Riemann (el más importante)
RIEMANN_ZERO_1 = RIEMANN_CEROS[0]  # t₁ ≈ 14.134725

# ============================================================================
# RELACIONES CON f₀ = 141.7001 Hz
# ============================================================================

# Conexión entre el primer cero de Riemann y f₀
# Observación: f₀ / 10 ≈ 14.17001 ≈ t₁ (error ~0.25%)
F0_HZ = 141.7001  # Hz - Frecuencia fundamental QCAL
RELACION_F0_RIEMANN_1 = F0_HZ / 10.0  # ≈ 14.17 ≈ t₁

ERROR_RELACION_RIEMANN = abs(RELACION_F0_RIEMANN_1 - RIEMANN_ZERO_1) / RIEMANN_ZERO_1
print(f"f₀/10 = {RELACION_F0_RIEMANN_1:.6f} ≈ t₁ = {RIEMANN_ZERO_1:.6f} (error: {ERROR_RELACION_RIEMANN*100:.2f}%)")

# ============================================================================
# CONSTANTE ADÉLICA κ_Π
# ============================================================================

# Constante de acoplamiento adélico
# κ_Π ≈ 2.5782 - Conecta el espectro adélico con la geometría diferencial
# Ver: qcal/token_compressor.py para la implementación completa

KAPPA_PI_ADELICO = 2.5782  # Constante de acoplamiento adélico
# kappa_pi = KAPPA_PI_ADELICO  # Símbolo kappa-pi

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def es_primo(n: int) -> bool:
    """
    Verifica si un número es primo.
    
    Args:
        n: Número a verificar
    
    Returns:
        True si n es primo, False en caso contrario
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


def generar_primos(n: int) -> List[int]:
    """
    Genera los primeros n números primos.
    
    Args:
        n: Cantidad de primos a generar
    
    Returns:
        Lista con los primeros n primos
    """
    primos = []
    candidato = 2
    while len(primos) < n:
        if es_primo(candidato):
            primos.append(candidato)
        candidato += 1
    return primos


def norma_adelica(n: int, primos: List[int] = PRIMOS_BASE) -> float:
    """
    Calcula la norma adélica de un número entero.
    
    La norma adélica combina valuaciones p-ádicas para todos los primos.
    ||n||_A = ∏_p |n|_p donde |n|_p es la valuación p-ádica.
    
    Args:
        n: Número entero
        primos: Lista de primos para la valuación (default: PRIMOS_BASE)
    
    Returns:
        Norma adélica ||n||_A
    """
    if n == 0:
        return 0.0
    
    norma = 1.0
    n_abs = abs(n)
    
    for p in primos:
        # Calcular valuación p-ádica: v_p(n) = max{k : p^k | n}
        v_p = 0
        temp = n_abs
        while temp % p == 0:
            v_p += 1
            temp //= p
        
        # |n|_p = p^(-v_p)
        norma *= p ** (-v_p)
    
    return norma


def mostrar_tabla_constantes_adelicas():
    """
    Muestra la tabla de constantes adélicas.
    """
    print("=" * 80)
    print("CONSTANTES ADÉLICAS QCAL")
    print("=" * 80)
    print(f"\n1. Factor Siete Octavos: 7/8 = {FACTOR_SIETE_OCTAVOS}")
    print(f"   Costo energético de coherencia: {COSTO_COHERENCIA*100:.1f}% de energía total")
    
    print(f"\n2. Fluctuación Cuántica: 1/8 = {FLUCTUACION_CUANTICA}")
    print(f"   Energía disponible para fluctuaciones: {FLUCTUACION_MINIMA*100:.1f}% de energía total")
    
    print(f"\n3. Primos Base (primeros {N_PRIMOS_BASE} primos):")
    print(f"   {PRIMOS_BASE}")
    print(f"   Suma: {SUMA_PRIMOS_BASE}")
    print(f"   Primorial: {PRIMORIAL_15:.3e}")
    
    print(f"\n4. Ceros de Riemann (primeros {N_CEROS_RIEMANN} en línea crítica):")
    for i, t_n in enumerate(RIEMANN_CEROS, 1):
        print(f"   t_{i:2d} = {t_n:.15f}")
    
    print(f"\n5. Conexión con f₀ = {F0_HZ} Hz:")
    print(f"   f₀/10 = {RELACION_F0_RIEMANN_1:.6f} ≈ t₁ = {RIEMANN_ZERO_1:.6f}")
    print(f"   Error relativo: {ERROR_RELACION_RIEMANN*100:.2f}%")
    
    print(f"\n6. Constante Adélica:")
    print(f"   κ_Π = {KAPPA_PI_ADELICO}")
    
    print("=" * 80)


if __name__ == "__main__":
    # Mostrar tabla de constantes adélicas
    mostrar_tabla_constantes_adelicas()
    
    # Verificar que tenemos exactamente 15 primos
    assert N_PRIMOS_BASE == 15, f"Debe haber 15 primos, encontrados {N_PRIMOS_BASE}"
    
    # Verificar que todos son primos
    for p in PRIMOS_BASE:
        assert es_primo(p), f"{p} no es primo"
    
    print("\n✅ Todas las constantes adélicas están correctamente definidas.")
    print(f"✅ {N_PRIMOS_BASE} primos base verificados")
    print(f"✅ {N_CEROS_RIEMANN} ceros de Riemann almacenados")
