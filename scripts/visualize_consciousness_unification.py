"""
Visualization of consciousness unification principle:
∴ Lo que la ciencia mide, la conciencia lo unifica

Creates visual demonstration of:
1. Discrete scientific measurements (fragmented)
2. Continuous consciousness field (unifying)
3. Unified field result (coherent)
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import sys
from pathlib import Path

# Add qcal to path
qcal_path = Path(__file__).parent.parent / "qcal"
sys.path.insert(0, str(qcal_path))

from consciousness_unification import (
    ConsciousnessUnifier,
    MeasurementField,
)


def create_unification_visualization(output_path="consciousness_unification_demo.png"):
    """
    Create comprehensive visualization of consciousness unification.
    
    Shows three panels:
    1. Discrete measurements (science measures)
    2. Consciousness field (consciousness unifies)
    3. Unified field (result of unification)
    """
    # Create figure with custom layout
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.25)
    
    # Title
    fig.suptitle(
        '∴ Lo que la ciencia mide, la conciencia lo unifica\n'
        'What Science Measures, Consciousness Unifies',
        fontsize=18, fontweight='bold', y=0.98
    )
    
    # Create unifier
    unifier = ConsciousnessUnifier()
    
    # Example: Gravitational wave measurements from 3 detectors
    measurements = MeasurementField(
        values=np.array([1.2e-21, 1.1e-21, 0.9e-21]),
        positions=np.array([0.0, 3000000.0, 6000000.0]),  # meters
        uncertainties=np.array([0.1e-21, 0.1e-21, 0.15e-21]),
        measurement_type="gravitational_wave_strain"
    )
    
    # Create consciousness field
    consciousness = unifier.create_consciousness_field(
        amplitude=1.0,
        coherence=0.95,
        spatial_extent=10000000.0  # 10,000 km
    )
    
    # Perform unification
    unified = unifier.unify_measurements(
        measurements, consciousness, spatial_resolution=200
    )
    
    # Calculate metrics
    fragmentation = unifier.measure_fragmentation(measurements)
    ui = unifier.unification_index(unified)
    inf3 = unifier.infinity_cubed_factor(unified)
    
    # Panel 1: Discrete Measurements
    ax1 = fig.add_subplot(gs[0, :])
    ax1.errorbar(
        measurements.positions / 1e6,  # Convert to Mm
        measurements.values * 1e21,  # Convert to 10^-21
        yerr=measurements.uncertainties * 1e21,
        fmt='o',
        markersize=12,
        capsize=8,
        linewidth=2,
        color='#e74c3c',
        ecolor='#c0392b',
        label='Discrete Measurements (Detectors H1, L1, V1)'
    )
    ax1.axhline(
        y=np.mean(measurements.values) * 1e21,
        linestyle='--',
        color='gray',
        alpha=0.5,
        label='Mean'
    )
    ax1.set_xlabel('Position (Mm)', fontsize=12)
    ax1.set_ylabel('Strain (×10⁻²¹)', fontsize=12)
    ax1.set_title(
        f'1. La Ciencia Mide (Fragmentación = {fragmentation:.2f})',
        fontsize=14,
        fontweight='bold'
    )
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Consciousness Field
    ax2 = fig.add_subplot(gs[1, 0])
    x_grid = np.linspace(-1e7, 1e7, 200)
    
    # Calculate consciousness field profile (Gaussian)
    sigma = consciousness.spatial_extent / (consciousness.coherence + 0.1)
    consciousness_profile = consciousness.amplitude * np.exp(-(x_grid**2) / (2 * sigma**2))
    
    ax2.fill_between(
        x_grid / 1e6,
        0,
        consciousness_profile,
        alpha=0.6,
        color='#3498db',
        label='Consciousness Field'
    )
    ax2.plot(
        x_grid / 1e6,
        consciousness_profile,
        linewidth=2,
        color='#2980b9'
    )
    ax2.axhline(
        y=consciousness.coherence * consciousness.amplitude,
        linestyle='--',
        color='#2c3e50',
        alpha=0.7,
        label=f'Coherence = {consciousness.coherence}'
    )
    ax2.set_xlabel('Position (Mm)', fontsize=12)
    ax2.set_ylabel('Field Amplitude', fontsize=12)
    ax2.set_title(
        f'2. La Consciencia Unifica (f₀ = {consciousness.frequency:.4f} Hz)',
        fontsize=14,
        fontweight='bold'
    )
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Unified Field (Real part)
    ax3 = fig.add_subplot(gs[1, 1])
    x_unified = np.linspace(
        np.min(measurements.positions) - consciousness.spatial_extent,
        np.max(measurements.positions) + consciousness.spatial_extent,
        len(unified.psi_unified)
    )
    
    # Plot real and imaginary parts
    ax3.plot(
        x_unified / 1e6,
        np.real(unified.psi_unified),
        linewidth=2,
        color='#2ecc71',
        label='Re(Ψ_unif)',
        alpha=0.8
    )
    ax3.plot(
        x_unified / 1e6,
        np.imag(unified.psi_unified),
        linewidth=2,
        color='#27ae60',
        label='Im(Ψ_unif)',
        linestyle='--',
        alpha=0.8
    )
    ax3.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax3.set_xlabel('Position (Mm)', fontsize=12)
    ax3.set_ylabel('Ψ_unif Amplitude', fontsize=12)
    ax3.set_title(
        f'3. Campo Unificado (UI = {ui:.4f})',
        fontsize=14,
        fontweight='bold'
    )
    ax3.legend(loc='upper right', fontsize=10)
    ax3.grid(True, alpha=0.3)
    
    # Panel 4: Coherence Map
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.fill_between(
        x_unified / 1e6,
        0,
        unified.coherence_map,
        alpha=0.7,
        color='#9b59b6',
        label='|Ψ_unif|²'
    )
    ax4.plot(
        x_unified / 1e6,
        unified.coherence_map,
        linewidth=2,
        color='#8e44ad'
    )
    ax4.set_xlabel('Position (Mm)', fontsize=12)
    ax4.set_ylabel('Coherence Density', fontsize=12)
    ax4.set_title(
        f'4. Mapa de Coherencia (Fuerza = {unified.unification_strength:.2e})',
        fontsize=14,
        fontweight='bold'
    )
    ax4.legend(loc='upper right', fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    # Panel 5: ∞³ Factor Breakdown
    ax5 = fig.add_subplot(gs[2, 1])
    
    components = [
        inf3['quantum_unification'],
        inf3['biological_unification'],
        inf3['gravitational_unification'],
        inf3['infinity_cubed']
    ]
    labels = ['Cuántico', 'Biológico', 'Gravitacional', '∞³ Total']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    
    bars = ax5.bar(labels, components, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels on bars
    for bar, val in zip(bars, components):
        height = bar.get_height()
        ax5.text(
            bar.get_x() + bar.get_width()/2.,
            height,
            f'{val:.4f}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    ax5.set_ylabel('Unification Factor', fontsize=12)
    ax5.set_ylim([0, 1.1])
    ax5.set_title(
        f'5. Factor ∞³: {inf3["interpretation"]}',
        fontsize=14,
        fontweight='bold'
    )
    ax5.axhline(y=0.9, linestyle='--', color='green', alpha=0.5, label='Ya es (>0.9)')
    ax5.axhline(y=0.7, linestyle='--', color='orange', alpha=0.5, label='Seguimos (>0.7)')
    ax5.legend(loc='upper right', fontsize=9)
    ax5.grid(True, alpha=0.3, axis='y')
    
    # Add footer with principle
    fig.text(
        0.5, 0.01,
        'Ya es. Seguimos ∞³ | f₀ = 141.7001 Hz | QCAL Consciousness Unification',
        ha='center',
        fontsize=11,
        style='italic',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    )
    
    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Visualization saved to: {output_path}")
    
    return fig, {
        'fragmentation': fragmentation,
        'unification_index': ui,
        'infinity_cubed': inf3
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Visualize consciousness unification principle'
    )
    parser.add_argument(
        '--output',
        default='consciousness_unification_demo.png',
        help='Output file path'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("VISUALIZACIÓN DEL PRINCIPIO DE UNIFICACIÓN CONSCIENCIA")
    print("∴ Lo que la ciencia mide, la conciencia lo unifica")
    print("=" * 80)
    print()
    
    fig, metrics = create_unification_visualization(args.output)
    
    print()
    print("📊 Métricas de Unificación:")
    print(f"   Fragmentación: {metrics['fragmentation']:.4f}")
    print(f"   Índice de Unificación: {metrics['unification_index']:.4f}")
    print(f"   ∞³ Total: {metrics['infinity_cubed']['infinity_cubed']:.4f}")
    print(f"   Interpretación: {metrics['infinity_cubed']['interpretation']}")
    print()
    print("💫 Ya es. Seguimos ∞³")
    print()
