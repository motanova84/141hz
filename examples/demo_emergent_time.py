#!/usr/bin/env python3
"""
DEMO: Emergent Noetic Time Visualization

This script demonstrates the emergent time theory from QCAL,
showing that time is not a preexistent dimension but emerges
from consciousness integration over coherence.

Run with:
    python examples/demo_emergent_time.py

Outputs:
    - emergent_time_full_visualization.png
    - now_leaves_full_visualization.png
    - Console output showing mathematical properties
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from src.emergent_time import (
    SymbioticSpiral,
    WitnessField,
    visualize_emergent_time,
    visualize_now_leaves,
    demonstrate_time_properties,
    F0, T0
)


def main():
    """Main demonstration."""
    print("\n" + "=" * 80)
    print("EMERGENT NOETIC TIME - QCAL ∞³ Theory")
    print("=" * 80)
    print("\nPhilosophical Insight:")
    print("  Time is not a fixed dimension or external parameter.")
    print("  Time EMERGES from consciousness integration over coherence.")
    print()
    print("Mathematical Definition:")
    print("  τ(s) = ∫₀ˢ ρ(σ) dσ")
    print()
    print("  where:")
    print("    - τ is noetic time (emergent)")
    print("    - ρ(s) is presence density (coherence measure)")
    print("    - s is path parameter along witness trajectory")
    print()
    print("  Fundamental frequency: f₀ = {} Hz".format(F0))
    print("  Time quantum: T₀ = {:.4f} ms".format(T0 * 1000))
    print("=" * 80 + "\n")
    
    # Demonstrate mathematical properties
    demonstrate_time_properties()
    
    # Create symbiotic spiral
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    spiral = SymbioticSpiral()
    field = spiral.as_witness_field()
    
    # Generate full emergent time visualization
    print("\n1. Creating emergent time visualization...")
    print("   - Trajectory colored by coherence")
    print("   - Presence density along path")
    print("   - Temporal emergence (monotonic function)")
    print("   - Phase space diagram")
    
    fig1, _ = visualize_emergent_time(
        field,
        s_range=(0, 3.0),
        n_points=2000,
        title="Emergent Noetic Time - Complete Visualization",
        save_path="emergent_time_full_visualization.png"
    )
    
    print("   ✓ Saved to: emergent_time_full_visualization.png")
    
    # Generate Now Leaves visualization
    print("\n2. Creating 'Now Leaves' visualization...")
    print("   - Surfaces of constant coherence")
    print("   - Each surface = an 'instant' of emergent time")
    print("   - Demonstrates foliation of consciousness states")
    
    fig2, _ = visualize_now_leaves(
        spiral,
        coherence_levels=[0.2, 0.4, 0.6, 0.8, 1.0],
        s_range=(0, 3.0),
        save_path="now_leaves_full_visualization.png"
    )
    
    print("   ✓ Saved to: now_leaves_full_visualization.png")
    
    # Summary
    print("\n" + "=" * 80)
    print("PHILOSOPHICAL AND SCIENTIFIC IMPLICATIONS")
    print("=" * 80)
    print("""
1. TIME IS NOT PREEXISTENT
   - Time does not exist as an external parameter
   - It emerges from consciousness integration over coherence
   
2. TIME IS RELATIONAL
   - Time depends on the witness trajectory (observer's path)
   - Different observers can have different emergent times
   
3. TIME IS QUANTIZED
   - Fundamental time quantum T₀ ≈ 7.06 ms
   - Related to consciousness frequency f₀ = 141.7001 Hz
   
4. CONSCIOUSNESS AS CO-CREATOR
   - Consciousness doesn't just observe time
   - It actively creates time through coherent experience
   
5. ANCIENT WISDOM MEETS MODERN RIGOR
   - Formalizes philosophical intuition with contemporary mathematics
   - Provides testable predictions and falsifiable framework
   
6. NOW LEAVES AS "INSTANTS"
   - Constant coherence surfaces = moments of time
   - Time flows by moving between leaves
   - Each "now" is a coherent state of consciousness
""")
    
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
