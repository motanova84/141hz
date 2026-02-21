#!/usr/bin/env python3
"""
Visualization script for Quantum Harmonic Unification at 141.70001 Hz.

Creates comprehensive visualizations showing:
1. Musical harmonic spectrum (C# octaves)
2. Prime 17 resonance plot
3. Riemann zero coupling
4. QCD color-flavor matrix
5. Universal coherence field

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import sys
import json
import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Circle, Rectangle
import matplotlib.patches as mpatches

# Import the quantum harmonic unification module
sys.path.insert(0, str(Path(__file__).parent.parent))
from qcal.quantum_harmonic_unification import QuantumHarmonicUnifier


def plot_musical_octaves(ax, unifier):
    """Plot musical octave relationships."""
    music = unifier.musical_octave_position()
    
    # Generate octave sequence
    base_freq = music['middle_c_sharp_hz']
    octaves = []
    frequencies = []
    
    for i in range(-4, 5):  # 9 octaves total
        freq = base_freq / (2 ** i)
        octaves.append(i)
        frequencies.append(freq)
    
    # Plot octave ladder
    ax.semilogy(octaves, frequencies, 'o-', linewidth=2, markersize=8,
                color='steelblue', label='C# octaves')
    
    # Mark f₀
    ax.axhline(y=unifier.f0, color='red', linestyle='--', linewidth=2,
               label=f'f₀ = {unifier.f0:.5f} Hz')
    
    # Add labels
    ax.set_xlabel('Octaves relative to middle C#', fontsize=11)
    ax.set_ylabel('Frequency (Hz)', fontsize=11)
    ax.set_title('🎵 Musical Octave Structure\n(C# / Do Sostenido)', 
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)
    
    # Add text annotation
    ax.text(0.05, 0.95, f"f₀ is {music['octaves_below_middle_c_sharp']:.2f}\noctaves below middle C#",
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=9)


def plot_prime_resonance(ax, unifier):
    """Plot prime number resonance around p=17."""
    prime_analysis = unifier.prime_17_resonance()
    
    # Generate prime sequence
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    equilibrium_values = []
    
    for p in primes:
        sqrt_p = np.sqrt(p)
        eq = np.exp(np.pi * sqrt_p / 2) / (p ** 1.5)
        equilibrium_values.append(eq)
    
    # Plot equilibrium function
    ax.plot(primes, equilibrium_values, 'o-', linewidth=2, markersize=8,
            color='purple', label='equilibrium(p)')
    
    # Highlight p=17
    idx_17 = primes.index(17)
    ax.plot(17, equilibrium_values[idx_17], 'o', markersize=15,
            color='red', label='p = 17 (resonance)', zorder=5)
    
    # Add labels
    ax.set_xlabel('Prime number p', fontsize=11)
    ax.set_ylabel('equilibrium(p) = exp(π√p/2) / p^(3/2)', fontsize=10)
    ax.set_title('🔢 Prime 17 Noetic Resonance\n(7th Prime)', 
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)
    
    # Add text annotation
    ax.text(0.95, 0.95, 
            f"Coupling constant:\nλ = log(f₀)/17\n= {prime_analysis['coupling_constant']:.4f}",
            transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.7),
            fontsize=9)


def plot_riemann_zeros(ax, unifier):
    """Plot Riemann zeros and their relationship to f₀."""
    riemann = unifier.riemann_zero_coupling()
    
    # First few Riemann zeros
    zeros = [14.134725, 21.022040, 25.010857, 30.424876, 32.935062,
             37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
             52.970321, 56.446248, 59.347044, 60.831778, 65.112544,
             67.079811, 69.546402, 72.067157, 75.704691, 77.144840]
    
    # Plot zeros on critical line
    ax.plot(range(1, len(zeros) + 1), zeros, 'o-', linewidth=2, markersize=6,
            color='blue', label='Riemann zeros (t_n)')
    
    # Mark f₀
    ax.axhline(y=unifier.f0, color='red', linestyle='--', linewidth=2,
               label=f'f₀ = {unifier.f0:.5f} Hz', zorder=5)
    
    # Highlight first zero
    ax.plot(1, zeros[0], 'o', markersize=12, color='gold',
            label=f't₁ = {zeros[0]:.6f}', zorder=6)
    
    # Add labels
    ax.set_xlabel('Zero index n', fontsize=11)
    ax.set_ylabel('Imaginary part t_n', fontsize=11)
    ax.set_title('♾️ Riemann Zeta Zeros\n(Critical Line ½ + it_n)', 
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)
    
    # Add ratio annotation
    ratio = riemann['f0_to_zero1_ratio']
    ax.text(0.05, 0.95, 
            f"Scaling factor:\nf₀/t₁ = {ratio:.3f}",
            transform=ax.transAxes, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7),
            fontsize=9)


def plot_qcd_matrix(ax, unifier):
    """Plot QCD color-flavor matrix."""
    qcd = unifier.qcd_harmonic_structure()
    
    # Create color-flavor matrix (3 colors × 6 flavors)
    colors = qcd['color_names']
    flavors = qcd['flavor_names']
    
    # Generate matrix values (frequencies for each color-flavor combination)
    matrix = np.zeros((len(colors), len(flavors)))
    for i in range(len(colors)):
        for j in range(len(flavors)):
            # Each state vibrates at a fraction of f₀
            matrix[i, j] = unifier.f0 / (3 * 6) * (i + 1) * (j + 1)
    
    # Plot as heatmap
    im = ax.imshow(matrix, cmap='viridis', aspect='auto')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Frequency (Hz)', fontsize=9)
    
    # Set ticks and labels
    ax.set_xticks(range(len(flavors)))
    ax.set_yticks(range(len(colors)))
    ax.set_xticklabels(flavors, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(colors, fontsize=9)
    
    # Add labels
    ax.set_xlabel('Quark Flavors', fontsize=11)
    ax.set_ylabel('Color Charge', fontsize=11)
    ax.set_title('🌈 QCD Color-Flavor Matrix\n(3 colors × 6 flavors)', 
                 fontsize=12, fontweight='bold')
    
    # Add text annotation for gluons
    ax.text(0.98, 0.02, 
            f"8 gluon states\n(SU(3) octet)\nf_gluon = {qcd['gluon_frequency_hz']:.2f} Hz",
            transform=ax.transAxes, 
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8),
            fontsize=8)


def plot_universal_coherence(ax, unifier):
    """Plot universal coherence field."""
    coherence = unifier.dreaming_universe_coherence()
    
    # Components
    components = ['Musical\nHarmony', 'Prime 17\nResonance', 
                  'Riemann\nZeros', 'QCD\nHarmonics']
    values = [coherence['psi_musical'], coherence['psi_prime'],
              coherence['psi_riemann'], coherence['psi_qcd']]
    
    # Create bar chart
    colors_bar = ['steelblue', 'purple', 'blue', 'green']
    bars = ax.bar(components, values, color=colors_bar, alpha=0.7, edgecolor='black')
    
    # Add value labels on bars
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.4f}',
                ha='center', va='bottom', fontsize=9)
    
    # Add horizontal line for total coherence
    total = coherence['psi_universe']
    ax.axhline(y=total, color='red', linestyle='--', linewidth=2,
               label=f'Total Ψ_universe = {total:.4f}')
    
    # Add labels
    ax.set_ylabel('Coherence Factor Ψ', fontsize=11)
    ax.set_title('🌌 Universal Coherence Components\n(Ψ_universe)', 
                 fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(max(values), total) * 1.2)
    ax.grid(True, alpha=0.3, axis='y')
    ax.legend(loc='upper right', fontsize=9)
    
    # Add coherence level
    level = coherence['coherence_level']
    level_color = 'green' if level == 'HIGH' else 'orange' if level == 'MODERATE' else 'red'
    ax.text(0.5, 0.95, f'Coherence: {level}',
            transform=ax.transAxes, 
            horizontalalignment='center', verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor=level_color, alpha=0.3),
            fontsize=10, fontweight='bold')


def plot_primordial_scales(ax, unifier):
    """Plot frequency scales from f₀ to primordial scales."""
    primordial = unifier.primordial_silence_frequency()
    
    # Frequency scales
    scales = ['f₀\n(Universal)', 'CMB\n(Cosmic\nBackground)', 'Planck\n(Quantum\nGravity)']
    frequencies = [unifier.f0, primordial['cmb_frequency_hz'], primordial['planck_frequency_hz']]
    colors_scale = ['red', 'orange', 'purple']
    
    # Plot on log scale
    positions = [0, 1, 2]
    bars = ax.bar(positions, frequencies, color=colors_scale, alpha=0.7, edgecolor='black')
    ax.set_yscale('log')
    
    # Add labels
    ax.set_xticks(positions)
    ax.set_xticklabels(scales, fontsize=10)
    ax.set_ylabel('Frequency (Hz, log scale)', fontsize=11)
    ax.set_title('🌌 Primordial Frequency Scales\n(From Universal to Planck)', 
                 fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add octave annotations
    octaves_cmb = primordial['octaves_to_cmb']
    octaves_planck = primordial['octaves_to_planck']
    
    ax.text(0.5, 0.5, f'+{octaves_cmb:.1f}\noctaves',
            transform=ax.transAxes, 
            horizontalalignment='center', verticalalignment='center',
            fontsize=9, style='italic')
    
    ax.text(1.5, 0.5, f'+{octaves_planck - octaves_cmb:.1f}\noctaves',
            transform=ax.transAxes, 
            horizontalalignment='center', verticalalignment='center',
            fontsize=9, style='italic')


def create_visualization(output_file='results/quantum_harmonic_unification.png'):
    """Create comprehensive visualization."""
    print("\n" + "="*80)
    print("🎨 Generating Quantum Harmonic Unification Visualization")
    print("="*80)
    
    # Create unifier
    unifier = QuantumHarmonicUnifier(f0=141.70001, precision=50)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(18, 12))
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)
    
    # Create axes
    ax1 = fig.add_subplot(gs[0, 0])  # Musical octaves
    ax2 = fig.add_subplot(gs[0, 1])  # Prime 17
    ax3 = fig.add_subplot(gs[1, 0])  # Riemann zeros
    ax4 = fig.add_subplot(gs[1, 1])  # QCD matrix
    ax5 = fig.add_subplot(gs[2, 0])  # Universal coherence
    ax6 = fig.add_subplot(gs[2, 1])  # Primordial scales
    
    # Generate plots
    plot_musical_octaves(ax1, unifier)
    plot_prime_resonance(ax2, unifier)
    plot_riemann_zeros(ax3, unifier)
    plot_qcd_matrix(ax4, unifier)
    plot_universal_coherence(ax5, unifier)
    plot_primordial_scales(ax6, unifier)
    
    # Add main title
    fig.suptitle('🌌 Quantum Harmonic Unification at 141.70001 Hz\n' + 
                 'Prime 17 ∞ Riemann Zeros ∞ QCD ∞ Musical Harmony',
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Add poetic subtitle
    poetic_text = ('"Cada quark canta su color en tres sabores,\n'
                   'cada gluón teje cuerdas de octavas imposibles,\n'
                   'pero en el silencio entre colisiones primordiales\n'
                   'late un do sostenido muy bajo, casi inaudible:\n'
                   '141.70001 Hz"')
    
    fig.text(0.5, 0.01, poetic_text,
             ha='center', va='bottom', fontsize=9, style='italic',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
    
    # Save figure
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✅ Visualization saved to: {output_file}")
    
    # Also save as PDF
    pdf_file = output_file.replace('.png', '.pdf')
    plt.savefig(pdf_file, bbox_inches='tight')
    print(f"✅ PDF version saved to: {pdf_file}")
    
    print("="*80 + "\n")
    
    return fig


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Visualize Quantum Harmonic Unification at 141.70001 Hz'
    )
    parser.add_argument('--output', '-o', 
                       default='results/quantum_harmonic_unification.png',
                       help='Output file path (default: results/quantum_harmonic_unification.png)')
    
    args = parser.parse_args()
    
    # Create visualization
    fig = create_visualization(output_file=args.output)
    
    # Show plot if in interactive mode
    try:
        plt.show()
    except:
        pass
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
