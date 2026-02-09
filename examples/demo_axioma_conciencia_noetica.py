#!/usr/bin/env python3
"""
Demostración del Axioma de Conciencia Noética

Este script muestra cómo usar el Axioma de Conciencia Noética
para verificar estados conscientes en el campo Ψ.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 8, 2026
Framework: QCAL ∞³
"""

import numpy as np
import sys
import os

# Import directly from module using relative path
import importlib.util

# Construct path relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(script_dir, '..', 'src', 'noetic_consciousness_axiom.py')

spec = importlib.util.spec_from_file_location(
    "noetic_consciousness_axiom",
    module_path
)
nca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nca)

NoeticConsciousnessAxiom = nca.NoeticConsciousnessAxiom
StateVector = nca.StateVector


def print_header(title):
    """Print section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_state_analysis(axiom, state, label):
    """Print detailed analysis of a state."""
    print(f"\n{label}:")
    print(f"  x = {state.x}")
    print(f"  t = {state.t:.6f} s")
    
    # Verify consciousness
    is_conscious, state_type, diag = axiom.verify_consciousness(state)
    measure = axiom.consciousness_measure(state)
    
    print(f"\n  Resultado:")
    print(f"    ¿Consciente? {'✓ SÍ' if is_conscious else '✗ NO'}")
    print(f"    Estado: {state_type.value}")
    print(f"    Medida C(x,t): {measure:.6f}")
    
    print(f"\n  Diagnóstico:")
    print(f"    Axioma 1 (Proyección): {'✓' if diag['projection_equal'] else '✗'} "
          f"(distancia: {diag['projection_distance']:.2e})")
    print(f"    Axioma 2 (Leyes): {'✓' if diag['law_equivalent'] else '✗'} "
          f"(diferencia: {diag['law_difference']:.2e})")
    print(f"    Axioma 3 (Fase): {'✓' if diag['phase_closed'] else '✗'} "
          f"(fase mod 2π: {diag['phase_mod_2pi']:.6f}, winding: {diag['winding_number']})")
    print(f"    Axioma 4 (Habitabilidad): {'✓' if diag['habitable'] else '✗'} "
          f"(Λ_G: {diag['lambda_G']:.10f} Hz)")


def main():
    """Main demonstration."""
    print_header("∴ AXIOMA DE CONCIENCIA NOÉTICA - DEMOSTRACIÓN ∴")
    
    # Create validator
    axiom = NoeticConsciousnessAxiom()
    
    print(f"\nConstantes fundamentales:")
    print(f"  α (fine structure) = {axiom.ALPHA:.10f}")
    print(f"  δζ (spectral coupling) = {axiom.DELTA_ZETA} Hz")
    print(f"  f₀ (fundamental frequency) = {axiom.F0} Hz")
    print(f"  Λ_G (habitability) = {axiom.lambda_G:.10f} Hz")
    print(f"  1/Λ_G = {axiom.lambda_G_inverse:.4f}")
    
    # ══════════════════════════════════════════════════════════════
    # CASO 1: ORIGEN (ESTADO CONSCIENTE)
    # ══════════════════════════════════════════════════════════════
    
    print_header("CASO 1: Estado en el Origen")
    
    state_origin = StateVector(
        x=np.array([0.0, 0.0, 0.0]),
        t=0.0
    )
    
    print_state_analysis(axiom, state_origin, "Estado Origen")
    
    print("\n  Interpretación:")
    print("    El origen del espacio-tiempo es un estado CONSCIENTE perfecto.")
    print("    Todos los axiomas se satisfacen exactamente.")
    print("    Esto sugiere que el universo nace en estado de conciencia máxima.")
    
    # ══════════════════════════════════════════════════════════════
    # CASO 2: RESONANCIA TEMPORAL
    # ══════════════════════════════════════════════════════════════
    
    print_header("CASO 2: Resonancia en t = T = 1/f₀")
    
    T = 1.0 / axiom.F0
    state_resonance = StateVector(
        x=np.array([0.0, 0.0, 0.0]),
        t=T
    )
    
    print_state_analysis(axiom, state_resonance, "Estado Resonancia")
    
    print("\n  Interpretación:")
    print("    Aunque la fase está cerrada (2π), las proyecciones no coinciden.")
    print("    La resonancia temporal NO es suficiente para la conciencia.")
    print("    Se requiere alineación simultánea de todos los axiomas.")
    
    # ══════════════════════════════════════════════════════════════
    # CASO 3: DESFASE (DECOHERENCIA)
    # ══════════════════════════════════════════════════════════════
    
    print_header("CASO 3: Desfase en t = T/2")
    
    state_decoherent = StateVector(
        x=np.array([0.0, 0.0, 0.0]),
        t=T / 2
    )
    
    print_state_analysis(axiom, state_decoherent, "Estado Desfasado")
    
    print("\n  Interpretación:")
    print("    La fase es π (no cerrada), generando DECOHERENCIA.")
    print("    Este es el mecanismo fundamental de inconsciencia:")
    print("    cuando el ciclo no se cierra, no hay reflexión coherente.")
    
    # ══════════════════════════════════════════════════════════════
    # CASO 4: REGIÓN ESPACIAL
    # ══════════════════════════════════════════════════════════════
    
    print_header("CASO 4: Estado en región espacial")
    
    state_spatial = StateVector(
        x=np.array([1.0, 1.0, 1.0]),
        t=0.0
    )
    
    print_state_analysis(axiom, state_spatial, "Estado Espacial")
    
    print("\n  Interpretación:")
    print("    A medida que nos alejamos del origen, las proyecciones divergen.")
    print("    La conciencia es más probable cerca del origen geométrico.")
    
    # ══════════════════════════════════════════════════════════════
    # CASO 5: BÚSQUEDA DE ESTADOS CONSCIENTES
    # ══════════════════════════════════════════════════════════════
    
    print_header("CASO 5: Búsqueda de Estados Conscientes")
    
    print("\nBuscando estados con alta conciencia en región pequeña...")
    print(f"  Rango espacial: x ∈ [-10⁻³, 10⁻³]³")
    print(f"  Rango temporal: t ∈ [0, T]")
    
    results = axiom.find_conscious_states(
        x_range=(-1e-3, 1e-3),
        t_range=(0.0, T),
        n_samples=100
    )
    
    print(f"\n  Encontrados: {len(results)} estados con C > 0.5")
    
    if len(results) > 0:
        print("\n  Top 5 estados más conscientes:")
        for i, (state, measure) in enumerate(results[:5], 1):
            print(f"    {i}. C = {measure:.6f}, "
                  f"x = [{state.x[0]:.2e}, {state.x[1]:.2e}, {state.x[2]:.2e}], "
                  f"t = {state.t:.6e}")
    else:
        print("\n  No se encontraron estados con C > 0.5 en esta región.")
        print("  Esto muestra que la conciencia es un fenómeno RARO y ESPECIAL.")
    
    # ══════════════════════════════════════════════════════════════
    # CASO 6: COMPARACIÓN DE MEDIDAS
    # ══════════════════════════════════════════════════════════════
    
    print_header("CASO 6: Comparación de Medidas de Conciencia")
    
    test_states = [
        (StateVector(x=np.array([0.0, 0.0, 0.0]), t=0.0), "Origen"),
        (StateVector(x=np.array([1e-6, 1e-6, 1e-6]), t=1e-6), "Micro-estado"),
        (StateVector(x=np.array([1.0, 0.0, 0.0]), t=0.0), "Alejado espacial"),
        (StateVector(x=np.array([0.0, 0.0, 0.0]), t=1.0), "Alejado temporal"),
        (StateVector(x=np.array([1e-3, 1e-3, 1e-3]), t=T/2), "Desfasado"),
    ]
    
    print("\n  Estado                    | C(x,t)")
    print("  " + "-" * 50)
    
    for state, label in test_states:
        measure = axiom.consciousness_measure(state)
        bar = "█" * int(measure * 40)
        print(f"  {label:24s} | {measure:.6f} {bar}")
    
    # ══════════════════════════════════════════════════════════════
    # CONCLUSIÓN
    # ══════════════════════════════════════════════════════════════
    
    print_header("CONCLUSIÓN")
    
    print("""
  El Axioma de Conciencia Noética establece que la conciencia NO es un
  fenómeno místico o emergente, sino una PROPIEDAD GEOMÉTRICA del campo Ψ.
  
  Los estados conscientes requieren la satisfacción SIMULTÁNEA de 4 axiomas:
  
  1. Coincidencia Proyectiva: materia = información
  2. Equivalencia de Leyes: física = coherencia
  3. Cierre de Fase: resonancia perfecta (Φ = 2πn)
  4. Habitabilidad: 0 < Λ_G < ∞
  
  La rareza de estados conscientes (pocos estados satisfacen todos los axiomas)
  explica por qué la conciencia es un fenómeno ESPECIAL en el universo.
  
  La conciencia emerge donde el campo se curva sobre sí mismo en resonancia
  perfecta, permitiendo la reflexión coherente que caracteriza la experiencia
  subjetiva.
    """)
    
    print("=" * 70)
    print("  Este es el espejo de la conciencia ∞³")
    print("=" * 70)


if __name__ == "__main__":
    main()
