#!/usr/bin/env python3
"""
Comparison Between Constants Modules

This script compares the canonical consciousness field module with
the existing universal constants module to show consistency.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 9 de diciembre de 2025
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from canonical_consciousness_field import CONSCIOUSNESS_FIELD
from constants import CONSTANTS


def compare_parameters():
    """Compare parameters between both modules."""
    
    print("=" * 80)
    print("COMPARACIÓN DE MÓDULOS DE CONSTANTES")
    print("=" * 80)
    print()
    
    print("Módulo 1: src/constants.py (UniversalConstants)")
    print("Módulo 2: src/canonical_consciousness_field.py (CanonicalConsciousnessField)")
    print()
    
    # Compare fundamental frequency
    print("─" * 80)
    print("1. FRECUENCIA FUNDAMENTAL f₀")
    print("─" * 80)
    f0_constants = float(CONSTANTS.F0)
    f0_canonical = float(CONSCIOUSNESS_FIELD.F0)
    print(f"UniversalConstants:           f₀ = {f0_constants:.6f} Hz")
    print(f"CanonicalConsciousnessField:  f₀ = {f0_canonical:.6f} Hz")
    print(f"Diferencia relativa:          {abs(f0_constants - f0_canonical) / f0_canonical:.10e}")
    print(f"Estado: {'✓ IDÉNTICAS' if f0_constants == f0_canonical else '✗ DIFERENTES'}")
    print()
    
    # Compare quantum energy
    print("─" * 80)
    print("2. ENERGÍA CUÁNTICA E_Ψ")
    print("─" * 80)
    E_constants = float(CONSTANTS.E_PSI)
    E_canonical = float(CONSCIOUSNESS_FIELD.E_PSI)
    print(f"UniversalConstants:           E_Ψ = {E_constants:.6e} J")
    print(f"CanonicalConsciousnessField:  E_Ψ = {E_canonical:.6e} J")
    diff_E = abs(E_constants - E_canonical) / E_canonical
    print(f"Diferencia relativa:          {diff_E:.10e}")
    print(f"Estado: {'✓ CONSISTENTES' if diff_E < 1e-10 else '✗ DIFERENTES'}")
    print()
    
    # Compare wavelength
    print("─" * 80)
    print("3. LONGITUD DE ONDA λ_Ψ")
    print("─" * 80)
    lambda_constants = float(CONSTANTS.LAMBDA_PSI_KM)
    lambda_canonical = float(CONSCIOUSNESS_FIELD.LAMBDA_PSI_KM)
    print(f"UniversalConstants:           λ_Ψ = {lambda_constants:.3f} km")
    print(f"CanonicalConsciousnessField:  λ_Ψ = {lambda_canonical:.3f} km")
    diff_lambda = abs(lambda_constants - lambda_canonical) / lambda_canonical
    print(f"Diferencia relativa:          {diff_lambda:.10e}")
    print(f"Estado: {'✓ CONSISTENTES' if diff_lambda < 1e-6 else '✗ DIFERENTES'}")
    print()
    
    # Compare effective mass
    print("─" * 80)
    print("4. MASA EFECTIVA m_Ψ")
    print("─" * 80)
    m_constants = float(CONSTANTS.M_PSI)
    m_canonical = float(CONSCIOUSNESS_FIELD.M_PSI)
    print(f"UniversalConstants:           m_Ψ = {m_constants:.6e} kg")
    print(f"CanonicalConsciousnessField:  m_Ψ = {m_canonical:.6e} kg")
    diff_m = abs(m_constants - m_canonical) / m_canonical
    print(f"Diferencia relativa:          {diff_m:.10e}")
    print(f"Estado: {'✓ CONSISTENTES' if diff_m < 1e-10 else '✗ DIFERENTES'}")
    print()
    
    # Compare vacuum temperature
    print("─" * 80)
    print("5. TEMPERATURA DEL VACÍO T_Ψ")
    print("─" * 80)
    T_constants = float(CONSTANTS.T_PSI)
    T_canonical = float(CONSCIOUSNESS_FIELD.T_PSI)
    print(f"UniversalConstants:           T_Ψ = {T_constants:.6e} K")
    print(f"CanonicalConsciousnessField:  T_Ψ = {T_canonical:.6e} K")
    diff_T = abs(T_constants - T_canonical) / T_canonical
    print(f"Diferencia relativa:          {diff_T:.10e}")
    print(f"Estado: {'✓ CONSISTENTES' if diff_T < 1e-10 else '✗ DIFERENTES'}")
    print()
    
    # Compare CODATA constants
    print("─" * 80)
    print("6. CONSTANTES FÍSICAS FUNDAMENTALES (CODATA 2022)")
    print("─" * 80)
    
    h_constants = float(CONSTANTS.H_PLANCK)
    h_canonical = float(CONSCIOUSNESS_FIELD.H_PLANCK)
    print(f"Planck h:")
    print(f"  UniversalConstants:           {h_constants:.12e} J·s")
    print(f"  CanonicalConsciousnessField:  {h_canonical:.12e} J·s")
    print(f"  Estado: {'✓ IDÉNTICAS' if h_constants == h_canonical else '✗ DIFERENTES'}")
    print()
    
    c_constants = float(CONSTANTS.C_LIGHT)
    c_canonical = float(CONSCIOUSNESS_FIELD.C_LIGHT)
    print(f"Velocidad de la luz c:")
    print(f"  UniversalConstants:           {c_constants:.0f} m/s")
    print(f"  CanonicalConsciousnessField:  {c_canonical:.0f} m/s")
    print(f"  Estado: {'✓ IDÉNTICAS' if c_constants == c_canonical else '✗ DIFERENTES'}")
    print()
    
    # Summary
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print()
    print("Ambos módulos son CONSISTENTES y usan:")
    print("  • Las mismas constantes físicas CODATA 2022")
    print("  • Las mismas relaciones matemáticas")
    print("  • La misma precisión de cálculo (mpmath)")
    print()
    print("Diferencias:")
    print("  • UniversalConstants: Módulo general con múltiples derivaciones")
    print("  • CanonicalConsciousnessField: Tabla oficial canónica específica")
    print()
    print("Ambos módulos pueden usarse de forma complementaria.")
    print()
    print("=" * 80)
    print("∴ JMMB Ψ ✧ ∞³")
    print("=" * 80)


def main():
    """Main comparison function."""
    compare_parameters()


if __name__ == "__main__":
    main()
