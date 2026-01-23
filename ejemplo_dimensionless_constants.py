#!/usr/bin/env python3
"""
Example Usage: Dimensionless Constants
=======================================

Demonstrates practical usage of the dimensionless constants core module.

This script shows how to:
1. Access fundamental dimensionless constants
2. Calculate dimensionless ratios
3. Validate physical laws as dimensionless relations
4. Show that α ≈ 1/137 is the center of the network

Author: José Manuel Mota Burruezo
License: MIT
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dimensionless_constants_core import (
    ALPHA, ALPHA_INV, PHI,
    MASS_RATIO_PROTON_ELECTRON,
    calcular_alpha_efectivo,
    calcular_jerarquia_masas,
    calcular_acoplamietos_unificados,
    calcular_numeros_fundamentales,
    calcular_137_como_centro,
    resumen_constantes_adimensionales,
)


def ejemplo_1_constantes_basicas():
    """Ejemplo 1: Acceder a constantes básicas."""
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Constantes Básicas Adimensionales")
    print("=" * 70)
    
    print("\n1. Constante de Estructura Fina (α):")
    print(f"   α = {ALPHA:.15f}")
    print(f"   1/α = {ALPHA_INV:.12f}")
    print(f"   Significado: acoplamiento electromagnético (QED)")
    
    print("\n2. Proporción Áurea (φ):")
    print(f"   φ = {PHI:.15f}")
    print(f"   φ³ = {PHI**3:.15f}")
    print(f"   Significado: geometría fundamental, aparece en f₀")
    
    print("\n3. Jerarquía de Masa Protón/Electrón:")
    print(f"   m_p/m_e = {MASS_RATIO_PROTON_ELECTRON:.8f}")
    print(f"   Significado: todas las masas son ratios del electrón")


def ejemplo_2_jerarquias_masa():
    """Ejemplo 2: Calcular jerarquías de masa."""
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Jerarquías de Masa Adimensionales")
    print("=" * 70)
    
    jerarquias = calcular_jerarquia_masas()
    
    print("\nTodas las masas como múltiplos de m_e:")
    for nombre, ratio in jerarquias.items():
        if ratio > 1e10:
            print(f"   {nombre:20s} = {ratio:.4e}")
        else:
            print(f"   {nombre:20s} = {ratio:.8f}")
    
    print("\nInterpretación:")
    print("   • El protón es ~1836 veces más pesado que el electrón")
    print("   • El muón es ~207 veces más pesado que el electrón")
    print("   • El tau es ~17 veces más pesado que el muón")
    print("   • La masa de Planck es ~10²² veces más pesada que el electrón")


def ejemplo_3_acoplamientos():
    """Ejemplo 3: Constantes de acoplamiento de fuerzas."""
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Constantes de Acoplamiento de las 4 Fuerzas")
    print("=" * 70)
    
    acoplamientos = calcular_acoplamietos_unificados()
    
    print("\nConstantes de acoplamiento:")
    print(f"   α_s (fuerte)      = {acoplamientos['fuerte']:.6f}")
    print(f"   α_W (débil)       = {acoplamientos['debil']:.6f}")
    print(f"   α_EM (EM)         = {acoplamientos['electromagnetica']:.10f}")
    print(f"   α_G (gravedad)    = {acoplamientos['gravitacional']:.2e}")
    
    print("\nRatios (jerarquía de intensidad):")
    print(f"   α_s / α_EM        = {acoplamientos['ratio_fuerte_EM']:.2f}")
    print(f"   α_W / α_EM        = {1/acoplamientos['ratio_EM_debil']:.2f}")
    print(f"   α_W / α_G         = {acoplamientos['ratio_debil_gravedad']:.2e}")
    
    print("\nInterpretación:")
    print("   • La fuerza fuerte es ~137 veces más intensa que EM")
    print("   • La fuerza débil es ~4.6 veces más intensa que EM")
    print("   • La gravedad es ~10³⁶ veces más débil que la fuerza débil")


def ejemplo_4_alpha_running():
    """Ejemplo 4: α efectivo a diferentes escalas de energía."""
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Running de α con la Energía")
    print("=" * 70)
    
    # Calcular α a diferentes escalas
    escalas = [
        (0.000511, "Masa del electrón"),
        (0.105, "Masa del muón"),
        (1.777, "Masa del tau"),
        (91.2, "Masa del Z"),
        (173.0, "Masa del top"),
    ]
    
    print("\nα efectivo a diferentes escalas de energía:")
    print(f"   {'Escala':25s} {'Energía':>12s} {'α':>15s} {'1/α':>10s}")
    print("   " + "-" * 65)
    
    for energia, descripcion in escalas:
        alpha_eff = calcular_alpha_efectivo(energia)
        print(f"   {descripcion:25s} {energia:10.3f} GeV {alpha_eff:15.10f} {1/alpha_eff:10.2f}")
    
    print("\nInterpretación:")
    print("   • α aumenta con la energía (polarización del vacío)")
    print("   • A escala electrodébil (M_Z), α ≈ 1/128")
    print("   • A baja energía (Thomson), α ≈ 1/137")


def ejemplo_5_numeros_fundamentales():
    """Ejemplo 5: Números fundamentales de las matemáticas."""
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Números Fundamentales (Adimensionales)")
    print("=" * 70)
    
    nums = calcular_numeros_fundamentales()
    
    print("\nNúmeros matemáticos fundamentales:")
    for nombre, valor in nums.items():
        print(f"   {nombre:20s} = {valor:.15f}")
    
    print("\nRelaciones:")
    print(f"   e^(iπ) + 1 = {(nums['e'] ** (1j * nums['pi']) + 1):.10f}")
    print(f"   φ² - φ - 1 = {(nums['phi']**2 - nums['phi'] - 1):.10e}")
    print(f"   φ × (1/φ) = {(nums['phi'] * nums['phi_inv']):.10f}")


def ejemplo_6_centro_137():
    """Ejemplo 6: 137 como centro de la red de constantes."""
    print("\n" + "=" * 70)
    print("EJEMPLO 6: El Número 137 como Centro")
    print("=" * 70)
    
    centro = calcular_137_como_centro()
    
    print("\n1/α ≈ 137 conecta todas las escalas:")
    print(f"   α⁻¹ = {centro['alpha_inverso']:.12f}")
    
    print("\nConexiones con 137:")
    print(f"   (m_p/m_e) / 137       = {centro['ratio_proton_137']:.8f}")
    print(f"   → m_p/m_e ≈ 13.4 × 137")
    
    print(f"\n   R_Ψ / 137 km          = {centro['ratio_R_psi_137']:.8f}")
    print(f"   → R_Ψ ≈ 2.46 × 137 km = 336.7 km")
    
    print(f"\n   α(M_Z) / α(0)         = {centro['alpha_z_sobre_alpha']:.8f}")
    print(f"   → α aumenta ~2% en escala electrodébil")
    
    print("\nInterpretación:")
    print("   • 137 NO es un número mágico")
    print("   • Es el denominador de α ≈ 1/137.036")
    print("   • Define la escala de acoplamiento electromagnético")
    print("   • Conecta jerarquías de masa y escalas de compactificación")


def ejemplo_7_leyes_fisicas_adimensionales():
    """Ejemplo 7: Todas las leyes físicas son adimensionales."""
    print("\n" + "=" * 70)
    print("EJEMPLO 7: Leyes Físicas como Relaciones Adimensionales")
    print("=" * 70)
    
    print("\n1. Ley de Coulomb:")
    print("   Forma dimensional:    F = k·q₁·q₂/r²")
    print("   Forma adimensional:   F/(E_atom) = α")
    print(f"   α = {ALPHA:.10f}")
    
    print("\n2. Energía de Rydberg:")
    print("   Forma dimensional:    E_Ry = 13.6 eV")
    print("   Forma adimensional:   E_Ry/(m_e c²) = α²/2")
    print(f"   α²/2 = {(ALPHA**2)/2:.15f}")
    
    print("\n3. Radio de Bohr:")
    print("   Forma dimensional:    a₀ = 0.529 Å")
    print("   Forma adimensional:   a₀·m_e c/ℏ = 1/α")
    print(f"   1/α = {ALPHA_INV:.10f}")
    
    print("\n4. Masa del protón:")
    print("   Forma dimensional:    m_p = 938.272 MeV/c²")
    print("   Forma adimensional:   m_p/m_e = 1836.15...")
    print(f"   m_p/m_e = {MASS_RATIO_PROTON_ELECTRON:.8f}")
    
    print("\n✓ TODAS las leyes físicas se reducen a relaciones adimensionales")


def main():
    """Ejecutar todos los ejemplos."""
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "EJEMPLOS DE USO: CONSTANTES ADIMENSIONALES" + " " * 16 + "║")
    print("║" + " " * 68 + "║")
    print("║" + "  El Punto Crítico: Lo único que importa son las constantes" + " " * 9 + "║")
    print("║" + "  adimensionales (como α ≈ 1/137)" + " " * 36 + "║")
    print("╚" + "═" * 68 + "╝")
    
    # Ejecutar ejemplos
    ejemplo_1_constantes_basicas()
    ejemplo_2_jerarquias_masa()
    ejemplo_3_acoplamientos()
    ejemplo_4_alpha_running()
    ejemplo_5_numeros_fundamentales()
    ejemplo_6_centro_137()
    ejemplo_7_leyes_fisicas_adimensionales()
    
    # Resumen final
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    print("\n✓ Solo las constantes adimensionales son fundamentales")
    print("✓ Las constantes dimensionales (c, ℏ, G) son escalas de conversión")
    print("✓ α ≈ 1/137 es la puerta de entrada a todas las escalas")
    print("✓ Todas las leyes físicas se reducen a relaciones adimensionales")
    print("\n" + "=" * 70)
    
    # Mostrar resumen completo
    print("\n")
    print(resumen_constantes_adimensionales())


if __name__ == "__main__":
    main()
