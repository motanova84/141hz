#!/usr/bin/env python3
"""
Vacuum Energy Visualization
Creates plots showing the energy landscape and term contributions
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vacuum_energy import (
    E_vac_log, optimize_vacuum_energy, analyze_vacuum_energy,
    alpha, beta, gamma, delta, zeta_prime, Lambda, pi_val
)


def plot_energy_landscape(log_r_range=None, output_file=None):
    """
    Plot the vacuum energy landscape
    
    Parameters
    ----------
    log_r_range : array-like, optional
        Range of log(R) values to plot
    output_file : str, optional
        Path to save the figure
    """
    if log_r_range is None:
        log_r_range = np.linspace(40, 50, 1000)
    
    # Calculate energies
    energies = np.array([E_vac_log(log_r) for log_r in log_r_range])
    
    # Find optimum
    result = optimize_vacuum_energy(bounds=(log_r_range[0], log_r_range[-1]))
    
    # Create figure
    fig = plt.figure(figsize=(12, 8))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Plot 1: Full energy landscape (log scale)
    ax1 = fig.add_subplot(gs[0, :])
    ax1.semilogy(log_r_range, energies, 'b-', linewidth=2, label='Total Energy')
    ax1.axvline(result.x, color='r', linestyle='--', linewidth=2, 
                label=f'Minimum at log(R) = {result.x:.4f}')
    ax1.axhline(result.fun, color='r', linestyle=':', alpha=0.5)
    ax1.set_xlabel('log₁₀(R/ℓ_P)', fontsize=12)
    ax1.set_ylabel('Vacuum Energy', fontsize=12)
    ax1.set_title('Vacuum Energy Landscape', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Add text box with optimization results
    textstr = f'Minimum Energy: {result.fun:.4e}\nOptimal log(R): {result.x:.6f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax1.text(0.02, 0.98, textstr, transform=ax1.transAxes, fontsize=10,
             verticalalignment='top', bbox=props)
    
    # Plot 2: Individual terms
    ax2 = fig.add_subplot(gs[1, 0])
    
    R_values = 10**log_r_range
    term1 = alpha / R_values**4
    term2 = beta * zeta_prime / R_values**2
    term3 = gamma * Lambda**2 * R_values**2
    term4 = delta * np.sin(np.log(R_values) / np.log(pi_val))**2
    
    # Filter out extremely small values to avoid numerical issues
    min_val = 1e-200
    term1_plot = np.maximum(np.abs(term1), min_val)
    term2_plot = np.maximum(np.abs(term2), min_val)
    term3_plot = np.maximum(term3, min_val)
    term4_plot = np.maximum(term4, min_val)
    
    # Only plot non-negligible terms
    ax2.semilogy(log_r_range, term1_plot, 'g-', label='|Planck term|', alpha=0.7)
    ax2.semilogy(log_r_range, term2_plot, 'orange', label='|Quantum term|', alpha=0.7)
    ax2.semilogy(log_r_range, term3_plot, 'purple', label='Lambda term', alpha=0.7)
    ax2.semilogy(log_r_range, term4_plot, 'cyan', label='Oscillatory term', alpha=0.7)
    
    ax2.set_xlabel('log₁₀(R/ℓ_P)', fontsize=11)
    ax2.set_ylabel('Energy Contribution', fontsize=11)
    ax2.set_title('Individual Energy Terms (Absolute Values)', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Contributions at optimum
    ax3 = fig.add_subplot(gs[1, 1])
    
    R_opt = 10**result.x
    contributions = {
        'Planck': alpha / R_opt**4,
        'Quantum': beta * zeta_prime / R_opt**2,
        'Lambda': gamma * Lambda**2 * R_opt**2,
        'Oscillatory': delta * np.sin(np.log(R_opt) / np.log(pi_val))**2
    }
    
    # Calculate absolute contributions for pie chart
    abs_contributions = {k: abs(v) for k, v in contributions.items()}
    total_abs = sum(abs_contributions.values())
    
    # Show all contributions with relative percentages
    if total_abs > 0:
        # Calculate percentages
        percentages = {k: (v / total_abs * 100) for k, v in abs_contributions.items()}
        
        # Only show contributions > 0.01% to avoid clutter
        threshold = 0.01
        significant = {k: v for k, v in abs_contributions.items() 
                      if (v / total_abs * 100) > threshold}
        
        if significant:
            colors = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']
            wedges, texts, autotexts = ax3.pie(
                significant.values(),
                labels=significant.keys(),
                autopct='%1.1f%%',
                colors=colors[:len(significant)],
                startangle=90
            )
            
            # Make percentage text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
        else:
            # Show as bar chart if pie chart is not appropriate
            ax3.clear()
            names = list(abs_contributions.keys())
            values = list(abs_contributions.values())
            colors_bar = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3']
            ax3.bar(names, values, color=colors_bar)
            ax3.set_ylabel('Absolute Contribution', fontsize=10)
            ax3.set_yscale('log')
            ax3.tick_params(axis='x', rotation=45)
    else:
        ax3.text(0.5, 0.5, 'All terms negligible', ha='center', va='center')
    
    ax3.set_title('Relative Contributions at Optimum', fontsize=12, fontweight='bold')
    
    # Overall title
    fig.suptitle('Vacuum Energy Analysis', fontsize=16, fontweight='bold', y=0.98)
    
    # Save or show
    if output_file:
        try:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        except (ValueError, RuntimeWarning):
            # Fallback if tight layout causes issues
            plt.savefig(output_file, dpi=300)
        print(f"✅ Figure saved to: {output_file}")
    else:
        plt.show()
    
    plt.close()


def plot_term_comparison(output_file=None):
    """
    Create a detailed comparison of energy terms across scales
    
    Parameters
    ----------
    output_file : str, optional
        Path to save the figure
    """
    log_r_range = np.linspace(35, 55, 2000)
    R_values = 10**log_r_range
    
    # Calculate terms
    term1 = alpha / R_values**4
    term2 = np.abs(beta * zeta_prime / R_values**2)
    term3 = gamma * Lambda**2 * R_values**2
    term4 = delta * np.sin(np.log(R_values) / np.log(pi_val))**2
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot with different styles
    ax.loglog(log_r_range, term1, 'g-', linewidth=2, label='Planck term (α/R⁴)')
    ax.loglog(log_r_range, term2, 'orange', linewidth=2, label='|Quantum term| (|βζ\'/R²|)')
    ax.loglog(log_r_range, term3, 'purple', linewidth=2, label='Lambda term (γΛ²R²)')
    ax.loglog(log_r_range, term4, 'cyan', linewidth=1.5, label='Oscillatory term', alpha=0.7)
    
    # Add shaded regions to show dominance
    ax.axvspan(35, 40, alpha=0.1, color='green', label='Planck-dominated')
    ax.axvspan(50, 55, alpha=0.1, color='purple', label='Lambda-dominated')
    
    # Find crossover points
    idx_cross = np.where(np.diff(np.sign(np.log10(term1) - np.log10(term3))))[0]
    if len(idx_cross) > 0:
        cross_log_r = log_r_range[idx_cross[0]]
        ax.axvline(cross_log_r, color='red', linestyle='--', alpha=0.5,
                   label=f'Crossover: log(R) ≈ {cross_log_r:.1f}')
    
    ax.set_xlabel('log₁₀(R/ℓ_P)', fontsize=13)
    ax.set_ylabel('Energy Contribution (log scale)', fontsize=13)
    ax.set_title('Energy Term Comparison Across Scales', fontsize=15, fontweight='bold')
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, which='both', alpha=0.3)
    
    # Add text annotations
    textstr = (f'Parameters:\n'
               f'α = {alpha}, β = {beta}\n'
               f'γ = {gamma}, δ = {delta}\n'
               f'ζ\' = {zeta_prime}, Λ = {Lambda}')
    props = dict(boxstyle='round', facecolor='lightblue', alpha=0.5)
    ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='bottom', horizontalalignment='right', bbox=props)
    
    plt.tight_layout()
    
    if output_file:
        try:
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
        except (ValueError, RuntimeWarning):
            # Fallback if tight layout causes issues
            plt.savefig(output_file, dpi=300)
        print(f"✅ Figure saved to: {output_file}")
    else:
        plt.show()
    
    plt.close()


def main():
    """Main execution function"""
    print("=" * 70)
    print("VACUUM ENERGY VISUALIZATION")
    print("=" * 70)
    print()
    
    # Create results directory if it doesn't exist
    results_dir = Path(__file__).parent.parent / 'results' / 'figures'
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate plots
    print("Generating vacuum energy landscape plot...")
    plot_energy_landscape(
        output_file=str(results_dir / 'vacuum_energy_landscape.png')
    )
    
    print("\nGenerating energy term comparison plot...")
    plot_term_comparison(
        output_file=str(results_dir / 'vacuum_energy_terms_comparison.png')
    )
    
    print()
    print("=" * 70)
    print("✅ Visualization complete!")
    print(f"📁 Figures saved to: {results_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
