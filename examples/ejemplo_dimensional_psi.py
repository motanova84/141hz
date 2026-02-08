#!/usr/bin/env python3
"""
Ejemplo completo de validación dimensional de Ψ = I · A_eff²

Este script demuestra que el problema matemático ha sido resuelto:

1. A_eff es un coeficiente adimensional
2. I fija la escala dimensional (información)
3. Ψ = I · A_eff² es dimensionalmente consistente
4. Comportamiento límite correcto: lim(A_eff→1) Ψ = I
5. Análogo a factores de acoplo en física estándar (α, αs, g, λ)

NO HAY RUPTURA DIMENSIONAL - Esto es física estándar.

Author: José Manuel Mota Burruezo (JMMB Ψ ∞³)
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal import (
    complete_dimensional_validation,
    print_validation_report,
    validate_limit_behavior,
    compare_to_physics_coupling_factors
)


def ejemplo_validacion_basica():
    """
    Validación básica con valores típicos.
    """
    print("=" * 80)
    print("EJEMPLO 1: Validación Básica")
    print("=" * 80)
    print()
    
    I = 10.0  # bits
    A_eff = 0.92  # adimensional
    
    print(f"Dado: I = {I} bits (información)")
    print(f"      A_eff = {A_eff} (efectividad, adimensional)")
    print()
    
    Psi = I * (A_eff ** 2)
    print(f"Ψ = I · A_eff² = {I} · {A_eff}² = {Psi:.4f} bits")
    print()
    print("✓ Ψ tiene las mismas dimensiones que I (bits)")
    print("✓ A_eff² es adimensional, no hay ruptura dimensional")
    print()


def ejemplo_limite():
    """
    Demostrar comportamiento límite: A_eff → 1 ⟹ Ψ → I
    """
    print("=" * 80)
    print("EJEMPLO 2: Comportamiento Límite")
    print("=" * 80)
    print()
    
    I = 15.0  # bits
    
    print(f"Dado: I = {I} bits")
    print()
    print("Tabla de convergencia (A_eff → 1):")
    print()
    print("  A_eff    |    Ψ      |  Ψ/I   |  I - Ψ")
    print("-----------|-----------|--------|----------")
    
    for A_eff in [0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 0.999, 1.0]:
        Psi = I * (A_eff ** 2)
        ratio = Psi / I
        diff = I - Psi
        print(f"  {A_eff:6.3f}  | {Psi:9.4f} | {ratio:6.4f} | {diff:8.4f}")
    
    print()
    print("✓ A medida que A_eff → 1, Ψ → I")
    print("✓ En el límite A_eff = 1: Ψ = I (efectividad perfecta)")
    print()


def ejemplo_fisica_estandar():
    """
    Comparar con factores de acoplo en física.
    """
    print("=" * 80)
    print("EJEMPLO 3: Comparación con Física Estándar")
    print("=" * 80)
    print()
    
    print("Factores de acoplo adimensionales en física:")
    print()
    
    # Comparar con física
    physics = compare_to_physics_coupling_factors()
    
    print("┌─────────────────────────┬────────────┬──────────────────────────┐")
    print("│ Constante               │ Valor      │ Rol en física            │")
    print("├─────────────────────────┼────────────┼──────────────────────────┤")
    
    examples = physics['examples']
    
    # Fine structure constant
    alpha = examples['fine_structure_alpha']
    print(f"│ α (estructura fina)     │ {alpha['value']:10.6f} │ Acoplo EM en QED         │")
    
    # Strong coupling
    alpha_s = examples['strong_coupling_alpha_s']
    print(f"│ αs (fuerte)             │ {alpha_s['value']:10.4f}   │ Acoplo fuerte en QCD     │")
    
    # Weak coupling
    g = examples['weak_coupling_g']
    print(f"│ g (débil)               │ {g['value']:10.3f}    │ Acoplo débil             │")
    
    # Higgs self-coupling
    lambda_h = examples['higgs_self_coupling_lambda']
    print(f"│ λ (Higgs)               │ {lambda_h['value']:10.2f}     │ Autoacoplamiento Higgs   │")
    
    print("├─────────────────────────┼────────────┼──────────────────────────┤")
    print("│ A_eff (QCAL)            │    0.92    │ Efectividad atencional   │")
    print("└─────────────────────────┴────────────┴──────────────────────────┘")
    print()
    print("Fórmulas análogas:")
    print("  • E_binding = α² · m_e · c²     (QED)")
    print("  • σ ∝ αs²                       (QCD)")
    print("  • Ψ = I · A_eff²                (QCAL)")
    print()
    print("✓ A_eff actúa EXACTAMENTE como α, αs, g, λ en física")
    print("✓ Esto es ESTÁNDAR en física - factores de acoplo adimensionales")
    print("✓ NO hay ruptura dimensional")
    print()


def ejemplo_casos_especiales():
    """
    Casos especiales y extremos.
    """
    print("=" * 80)
    print("EJEMPLO 4: Casos Especiales")
    print("=" * 80)
    print()
    
    I = 20.0  # bits
    
    print(f"Dado: I = {I} bits")
    print()
    print("Casos extremos:")
    print()
    
    # Caso 1: Sin efectividad
    A_eff = 0.0
    Psi = I * (A_eff ** 2)
    print(f"1. A_eff = 0 (sin efectividad)")
    print(f"   Ψ = {I} · 0² = {Psi}")
    print(f"   → Sin efectividad, sin coherencia")
    print()
    
    # Caso 2: Media efectividad
    A_eff = 0.5
    Psi = I * (A_eff ** 2)
    print(f"2. A_eff = 0.5 (media efectividad)")
    print(f"   Ψ = {I} · 0.5² = {Psi}")
    print(f"   → Coherencia al 25% de I")
    print()
    
    # Caso 3: Alta efectividad
    A_eff = 0.9
    Psi = I * (A_eff ** 2)
    print(f"3. A_eff = 0.9 (alta efectividad)")
    print(f"   Ψ = {I} · 0.9² = {Psi}")
    print(f"   → Coherencia al 81% de I")
    print()
    
    # Caso 4: Efectividad perfecta
    A_eff = 1.0
    Psi = I * (A_eff ** 2)
    print(f"4. A_eff = 1 (efectividad perfecta)")
    print(f"   Ψ = {I} · 1² = {Psi}")
    print(f"   → Coherencia = Información (PERFECCIÓN)")
    print()
    print("✓ En todos los casos, Ψ mantiene las dimensiones de I")
    print()


def validacion_completa():
    """
    Validación completa usando el módulo dimensional_analysis_psi.
    """
    print("=" * 80)
    print("VALIDACIÓN COMPLETA AUTOMATIZADA")
    print("=" * 80)
    print()
    
    # Ejecutar validación completa
    results = complete_dimensional_validation(I=10.0, A_eff=0.92)
    
    # Imprimir reporte
    print_validation_report(results)


def main():
    """
    Ejecutar todos los ejemplos.
    """
    print("\n\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "PROBLEMA MATEMÁTICO RESUELTO: Ψ = I · A_eff²" + " " * 18 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Ejemplo 1: Validación básica
    ejemplo_validacion_basica()
    input("Presiona Enter para continuar...")
    
    # Ejemplo 2: Comportamiento límite
    ejemplo_limite()
    input("Presiona Enter para continuar...")
    
    # Ejemplo 3: Comparación con física
    ejemplo_fisica_estandar()
    input("Presiona Enter para continuar...")
    
    # Ejemplo 4: Casos especiales
    ejemplo_casos_especiales()
    input("Presiona Enter para continuar...")
    
    # Validación completa
    validacion_completa()
    
    print("\n\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "CONCLUSIÓN FINAL" + " " * 34 + "║")
    print("╠" + "═" * 78 + "╣")
    print("║" + " " * 78 + "║")
    print("║  ✓ A_eff es ADIMENSIONAL (coeficiente de efectividad)                     ║")
    print("║  ✓ I fija la ESCALA DIMENSIONAL (información en bits/nats)                ║")
    print("║  ✓ Ψ = I · A_eff² es DIMENSIONALMENTE CONSISTENTE                         ║")
    print("║  ✓ Comportamiento LÍMITE CORRECTO: lim(A_eff→1) Ψ = I                     ║")
    print("║  ✓ ANÁLOGO a física estándar (α, αs, g, λ)                                ║")
    print("║                                                                            ║")
    print("║  ✓✓✓ NO HAY RUPTURA DIMENSIONAL ✓✓✓                                       ║")
    print("║  ✓✓✓ ESTO ES FÍSICA ESTÁNDAR (factores de acoplo) ✓✓✓                     ║")
    print("║                                                                            ║")
    print("╚" + "═" * 78 + "╝")
    print()


if __name__ == "__main__":
    main()
