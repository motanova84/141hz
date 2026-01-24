#!/usr/bin/env python3
"""
Riemann Horizon Visualization

Generate visualizations of the Riemann Horizon framework including:
- Arithmetic horizon: Riemann zeros as singularities
- H_ψ potential and eigenvalues
- Metric deformation
- Spectral duality
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
from pathlib import Path

try:
    import riemann_horizon as rh
except ImportError:
    print("Error: riemann_horizon module not found")
    import sys
    sys.exit(1)


def plot_arithmetic_horizon(ax, n_zeros=50):
    """Plot Riemann zeros as arithmetic horizon."""
    horizon = rh.ArithmeticHorizon(f0=rh.F0_HZ)
    zeros = horizon.get_riemann_zeros(n_zeros)
    
    # Plot zeros
    indices = np.arange(1, len(zeros) + 1)
    ax.scatter(indices, zeros, c='blue', alpha=0.6, s=30, label='Riemann zeros t_n')
    
    # Plot ideal relationship t_n = n·f₀
    ideal_line = indices * rh.F0_HZ
    ax.plot(indices, ideal_line, 'r--', alpha=0.5, linewidth=2, label=f'n × f₀ (f₀={rh.F0_HZ} Hz)')
    
    ax.set_xlabel('Zero index n', fontsize=12)
    ax.set_ylabel('Imaginary part t_n (Hz)', fontsize=12)
    ax.set_title('Arithmetic Horizon: Zeros as Singularities', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add text annotation
    ax.text(0.05, 0.95, f'ζ(1/2 + it_n) = 0', 
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))


def plot_hpsi_potential(ax, x_min=0.1, x_max=10.0, n_points=500):
    """Plot H_ψ operator potential."""
    hpsi = rh.HpsiOperator(lambda_coupling=1.0, max_primes=20)
    x = np.linspace(x_min, x_max, n_points)
    V = hpsi.potential(x)
    
    ax.plot(x, V, 'green', linewidth=2)
    ax.set_xlabel('Position x', fontsize=12)
    ax.set_ylabel('Potential V(x)', fontsize=12)
    ax.set_title('H_ψ Potential: V(x) = λΣ cos(log p · log x) / p', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add formula
    formula = r'$V(x) = \lambda \sum_p \frac{\cos(\log p \cdot \log x)}{p}$'
    ax.text(0.5, 0.95, formula, 
            transform=ax.transAxes, fontsize=11, verticalalignment='top',
            ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))


def plot_eigenvalues_comparison(ax, n_states=10, grid_size=100):
    """Compare H_ψ eigenvalues with Riemann zeros."""
    horizon = rh.ArithmeticHorizon(f0=rh.F0_HZ)
    hpsi = rh.HpsiOperator(lambda_coupling=1.0, max_primes=20)
    
    x = np.linspace(0.1, 10.0, grid_size)
    riemann_zeros = horizon.get_riemann_zeros(n_states)
    eigenvalues, _ = hpsi.solve_eigensystem(x, n_states)
    
    indices = np.arange(1, n_states + 1)
    
    # Plot Riemann zeros
    ax.scatter(indices, riemann_zeros, c='blue', s=80, alpha=0.7, 
              marker='o', label='Riemann zeros t_n', zorder=3)
    
    # Plot eigenvalues (real part)
    eigenvalues_real = np.real(eigenvalues)
    ax.scatter(indices, eigenvalues_real, c='red', s=80, alpha=0.7, 
              marker='s', label='H_ψ eigenvalues (Re)', zorder=3)
    
    # Connect with lines
    for i, (z, ev) in enumerate(zip(riemann_zeros, eigenvalues_real)):
        ax.plot([i+1, i+1], [z, ev], 'gray', alpha=0.3, linewidth=1)
    
    ax.set_xlabel('State index n', fontsize=12)
    ax.set_ylabel('Energy / Frequency (Hz)', fontsize=12)
    ax.set_title('H_ψ ϕ_n = t_n ϕ_n ⇔ ζ(1/2 + it_n) = 0', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_metric_deformation(ax):
    """Plot metric deformation vs coherence parameter."""
    geometry = rh.ConsciousGeometry(f0=rh.F0_HZ, f888=rh.F888_HZ)
    
    # Range of coherence parameters
    psi_values = np.linspace(0, 10, 100)
    g_00_values = []
    g_11_values = []
    
    for psi in psi_values:
        metric = geometry.metric_deformation(psi)
        g_00_values.append(metric.g_00)
        g_11_values.append(metric.g_11)
    
    ax.plot(psi_values, g_00_values, 'b-', linewidth=2, label='g₀₀ (time)')
    ax.plot(psi_values, g_11_values, 'r-', linewidth=2, label='g₁₁ (space)')
    ax.axhline(y=-1, color='b', linestyle='--', alpha=0.3, label='Minkowski g₀₀')
    ax.axhline(y=1, color='r', linestyle='--', alpha=0.3, label='Minkowski g₁₁')
    
    ax.set_xlabel('Coherence parameter Ψ = I × A_eff²', fontsize=12)
    ax.set_ylabel('Metric components g_μν', fontsize=12)
    ax.set_title('Ψ-deformed Metric: g_μν(x) = g_μν(0) + δg_μν(Ψ)', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_unified_tensor(ax):
    """Visualize unified tensor relation."""
    geometry = rh.ConsciousGeometry(f0=rh.F0_HZ, f888=rh.F888_HZ)
    tensor = geometry.unified_tensor_relation()
    
    # Bar plot comparison
    labels = ['f₀ × φ⁴', '888 Hz target']
    values = [tensor['f0_phi4_hz'], tensor['f888_hz']]
    colors = ['purple', 'orange']
    
    bars = ax.bar(labels, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f} Hz',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Frequency (Hz)', fontsize=12)
    ax.set_title('Unified Tensor: Línea crítica ≡ 888 Hz (f₀ × φ⁴)', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add error annotation
    error_text = f"Relative error: {tensor['relative_error']:.2%}\nφ = {tensor['phi']:.6f}"
    ax.text(0.5, 0.95, error_text,
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))


def plot_spectral_duality(ax, n_zeros=20):
    """Plot spectral duality reconstruction."""
    horizon = rh.ArithmeticHorizon(f0=rh.F0_HZ)
    geometry = rh.ConsciousGeometry(f0=rh.F0_HZ, f888=rh.F888_HZ)
    
    riemann_zeros = horizon.get_riemann_zeros(n_zeros)
    duality = geometry.spectral_duality(riemann_zeros)
    
    indices = np.arange(1, len(duality['spectrum_hz']) + 1)
    
    # Plot original spectrum
    ax.scatter(indices, duality['spectrum_hz'], c='blue', s=60, alpha=0.7,
              marker='o', label='Riemann spectrum', zorder=3)
    
    # Plot reconstruction
    ax.scatter(indices, duality['reconstruction_hz'], c='red', s=60, alpha=0.7,
              marker='x', label='Harmonic reconstruction', zorder=3)
    
    # Connect with lines to show error
    for i, (orig, recon) in enumerate(zip(duality['spectrum_hz'], duality['reconstruction_hz'])):
        ax.plot([i+1, i+1], [orig, recon], 'gray', alpha=0.3, linewidth=1)
    
    ax.set_xlabel('State index n', fontsize=12)
    ax.set_ylabel('Frequency (Hz)', fontsize=12)
    ax.set_title('Spectral Duality: D_s ⊗ 1 + 1 ⊗ H_ψ', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add reconstruction error
    error_text = f"Mean error: {duality['mean_reconstruction_error']:.2f} Hz"
    ax.text(0.05, 0.95, error_text,
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.5))


def create_comprehensive_visualization(output_path='results/riemann_horizon_visualization.png'):
    """Create comprehensive visualization with all plots."""
    # Create figure with subplots
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Create subplots
    ax1 = fig.add_subplot(gs[0, 0])  # Arithmetic horizon
    ax2 = fig.add_subplot(gs[0, 1])  # H_ψ potential
    ax3 = fig.add_subplot(gs[1, 0])  # Eigenvalues comparison
    ax4 = fig.add_subplot(gs[1, 1])  # Metric deformation
    ax5 = fig.add_subplot(gs[2, 0])  # Unified tensor
    ax6 = fig.add_subplot(gs[2, 1])  # Spectral duality
    
    print("🎨 Generating visualizations...")
    
    # Generate each plot
    print("   📊 1/6 Arithmetic Horizon...")
    plot_arithmetic_horizon(ax1, n_zeros=50)
    
    print("   📊 2/6 H_ψ Potential...")
    plot_hpsi_potential(ax2)
    
    print("   📊 3/6 Eigenvalues Comparison...")
    plot_eigenvalues_comparison(ax3, n_states=10)
    
    print("   📊 4/6 Metric Deformation...")
    plot_metric_deformation(ax4)
    
    print("   📊 5/6 Unified Tensor...")
    plot_unified_tensor(ax5)
    
    print("   📊 6/6 Spectral Duality...")
    plot_spectral_duality(ax6, n_zeros=10)
    
    # Add main title
    fig.suptitle('Riemann Horizon: Arithmetic Black Holes & Vibrational Manifolds\n'
                 f'f₀ = {rh.F0_HZ} Hz | f₈₈₈ = {rh.F888_HZ} Hz | φ = {rh.PHI:.6f}',
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Save figure
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    plt.savefig(output_file, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"\n✅ Visualization saved to: {output_file}")
    
    return fig


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate Riemann Horizon visualizations"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/riemann_horizon_visualization.png",
        help="Output image file path"
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the plot interactively"
    )
    
    args = parser.parse_args()
    
    # Create visualization
    fig = create_comprehensive_visualization(args.output)
    
    # Show if requested
    if args.show:
        plt.show()
    
    plt.close()


if __name__ == '__main__':
    main()
