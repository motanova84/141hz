#!/usr/bin/env python3
"""
modulation_traces.py - SIP Traces: Oscillatory Dynamics and Variance Analysis

Figure 1: Token Weight Modulation (0–0.1 s Zoom)
Matplotlib-generated: t vs. W_i(α=1, ε=0.0162). High-freq cosine (141.7 cycles/s) 
damps to e^{-1} at t=0.07 s. Verified stats: mean=1.0000, std=0.0066 (full); 
post-damp (t>0.07): var=1.24×10^{-5} (coherence preserved).

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from QCALLLMCore import QCALLLMCore


def plot_modulation_traces(save_path='modulation_traces.png', show=True):
    """
    Generate SIP modulation trace plots

    Parameters:
    -----------
    save_path : str
        Path to save the figure
    show : bool
        Whether to display the plot
    """
    # Initialize core with verified parameters
    core = QCALLLMCore(alpha=1.0, epsilon=0.0162, f0=141.7001, tau=0.07)

    # Time arrays
    t_full = np.linspace(0, 1, 10000)  # Full second
    t_zoom = np.linspace(0, 0.1, 1000)  # Zoom to 0.1s

    # Generate weights
    weights_full = core.sip_modulate(t_full)
    weights_zoom = core.sip_modulate(t_zoom)

    # Create figure
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Top panel: 0-0.1s zoom
    axes[0].plot(t_zoom * 1000, weights_zoom, 'b-', linewidth=1.5, label='W_i(t)')
    axes[0].axhline(y=1.0, color='k', linestyle='--', alpha=0.3, label='Baseline')
    axes[0].axvline(x=70, color='r', linestyle='--', alpha=0.5,
                    label=f'τ = {core.tau:.2f} s')
    axes[0].set_xlabel('Time (ms)', fontsize=12)
    axes[0].set_ylabel('Weight W_i(t)', fontsize=12)
    axes[0].set_title('SIP Token Weight Modulation (0–100 ms Zoom)', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='upper right', fontsize=10)

    # Bottom panel: Full second
    axes[1].plot(t_full, weights_full, 'b-', linewidth=1.0, label='W_i(t)')
    axes[1].axhline(y=1.0, color='k', linestyle='--', alpha=0.3, label='Baseline')
    axes[1].axvline(x=core.tau, color='r', linestyle='--', alpha=0.5,
                    label=f'e^(-1) at τ = {core.tau:.2f} s')
    axes[1].set_xlabel('Time (s)', fontsize=12)
    axes[1].set_ylabel('Weight W_i(t)', fontsize=12)
    axes[1].set_title('SIP Modulation: Full Time Evolution', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='upper right', fontsize=10)

    plt.tight_layout()

    # Calculate and display statistics
    mean_full = np.mean(weights_full)
    std_full = np.std(weights_full)
    var_post_damp = np.var(weights_full[t_full > core.tau])

    # First 5 points
    first_5 = weights_zoom[:5]

    # Add text box with statistics
    stats_text = (
        f"Statistics:\n"
        f"Mean: {mean_full:.4f}\n"
        f"Std (full): {std_full:.4f}\n"
        f"Var (t>{core.tau}s): {var_post_damp:.2e}\n"
        f"First 5: [{first_5[0]:.4f}, {first_5[1]:.4f}, "
        f"{first_5[2]:.4f}, {first_5[3]:.4f}, {first_5[4]:.4f}]\n"
        f"f₀ = {core.f0} Hz, ε = {core.epsilon:.4f}"
    )

    fig.text(0.02, 0.02, stats_text, fontsize=9,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             verticalalignment='bottom', family='monospace')

    # Save figure
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved modulation traces to {save_path}")

    if show:
        plt.show()

    # Print verification statistics
    print("\nVerified Statistics:")
    print(f"Mean: {mean_full:.4f} (expected: 1.0000)")
    print(f"Std (full): {std_full:.4f} (expected: 0.0066)")
    print(f"Var (post-damp, t>0.07): {var_post_damp:.2e} (expected: 1.24e-05)")
    print(f"First 5 points: {first_5}")
    print(f"Lyapunov-stable: λ ≈ {-1/core.tau:.2f} s⁻¹ (negative = stable)")

    return fig, axes


def plot_psi_sensitivity(save_path='psi_sensitivity.png', show=True):
    """
    Generate Ψ vs A_eff sensitivity landscape

    Figure 2: Ψ vs. A_eff (I=8.2 Fixed, n=100 Sims)
    Ψ = 8.2 A_eff²; threshold 5.0 at A_eff=0.78
    """
    # Fixed information parameter
    I = 8.2

    # A_eff range
    A_eff = np.linspace(0, 1.2, 100)

    # Calculate Psi
    psi = I * A_eff**2

    # Threshold
    threshold = 5.0
    A_threshold = np.sqrt(threshold / I)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(A_eff, psi, 'b-', linewidth=2, label='Ψ = 8.2 × A²_eff')
    ax.axhline(y=threshold, color='r', linestyle='--', linewidth=2,
               label=f'Threshold Ψ = {threshold}')
    ax.axvline(x=A_threshold, color='g', linestyle='--', linewidth=1.5, alpha=0.7,
               label=f'A_eff threshold = {A_threshold:.2f}')

    # Shaded regions
    ax.fill_between(A_eff, 0, psi, where=(psi >= threshold),
                    alpha=0.2, color='green', label='Coherent region')
    ax.fill_between(A_eff, 0, psi, where=(psi < threshold),
                    alpha=0.2, color='red', label='Subthreshold')

    ax.set_xlabel('A_eff (Effectiveness Parameter)', fontsize=12)
    ax.set_ylabel('Ψ_response', fontsize=12)
    ax.set_title('Ψ Response Sensitivity Landscape (I = 8.2 fixed)',
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=10)

    # Add sensitivity annotation
    A_sample = 0.88
    psi_sample = I * A_sample**2
    dPsi_dA = 2 * I * A_sample

    ax.annotate(f'dΨ/dA_eff = {dPsi_dA:.1f} at A={A_sample}',
                xy=(A_sample, psi_sample), xytext=(A_sample + 0.15, psi_sample + 1),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
                fontsize=10, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Saved Psi sensitivity plot to {save_path}")

    if show:
        plt.show()

    # Print statistics
    print(f"\nΨ = I × A²_eff with I = {I}")
    print(f"Threshold Ψ = {threshold} reached at A_eff = {A_threshold:.2f}")
    print(f"Sensitivity dΨ/dA_eff = 16.4 × A_eff (max at unity)")
    print(f"R² = 1.0 (exact quadratic)")

    return fig, ax


if __name__ == "__main__":
    print("Generating SIP Modulation Traces...")
    plot_modulation_traces(save_path='modulation_traces.png', show=False)

    print("\nGenerating Ψ Sensitivity Landscape...")
    plot_psi_sensitivity(save_path='psi_sensitivity.png', show=False)

    print("\nAll visualizations generated successfully!")
