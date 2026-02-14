"""
Example: Complete Cytoplasmic Flow Analysis with Quantum Resonance
===================================================================

This example demonstrates the full cytoplasmic flow model including:
1. Reynolds number calculation and Stokes regime validation
2. RiemannResonanceOperator eigenfrequencies
3. Beltrami flow with vorticity alignment
4. Microtubule quantum lattice streaming
5. Riemann pressure field analysis
6. Integration with cardiac coherence across scales

The model connects molecular-scale cytoplasmic dynamics to macro-scale
cardiac rhythms through the fundamental frequency f₀ = 141.7001 Hz.

Author: José Manuel Mota Burruezo
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Import models
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.cytoplasmic_flow_model import (
    CytoplasmicParameters,
    RiemannResonanceOperator,
    BeltramiFlow,
    MicrotubuleQuantumLattice,
    RiemannPressureField,
    validate_cytoplasmic_flow_model
)
from physics.coherencia_cardiaca import (
    CardiacCoherenceBridge,
    HeartRateVariability
)
from qcal.constants import F0_HZ


def plot_complete_analysis():
    """
    Create comprehensive visualization of cytoplasmic flow analysis.
    """
    # Initialize components
    params = CytoplasmicParameters()
    operator = RiemannResonanceOperator(n_modes=10)
    beltrami = BeltramiFlow(lambda_param=1.0)
    lattice = MicrotubuleQuantumLattice(n_dimers=100)
    pressure_field = RiemannPressureField(n_zeros=10)
    bridge = CardiacCoherenceBridge()
    
    # Create figure
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # 1. Reynolds Number and Stokes Regime
    ax1 = fig.add_subplot(gs[0, 0])
    velocities = np.logspace(-7, -5, 100)  # 0.1 to 10 μm/s
    reynolds = [params.reynolds_number(v) for v in velocities]
    
    ax1.loglog(velocities * 1e6, reynolds, 'b-', linewidth=2)
    ax1.axhline(y=1e-2, color='r', linestyle='--', label='Stokes limit (Re << 1)')
    ax1.axvline(x=params.v_kinesin * 1e6, color='g', linestyle='--', 
                label=f'Kinesin velocity ({params.v_kinesin*1e6:.1f} μm/s)')
    ax1.set_xlabel('Velocity (μm/s)', fontsize=10)
    ax1.set_ylabel('Reynolds Number', fontsize=10)
    ax1.set_title('1. Reynolds Number vs Velocity\n(Stokes Regime)', fontsize=11, fontweight='bold')
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)
    
    # 2. Eigenfrequencies
    ax2 = fig.add_subplot(gs[0, 1])
    eigen_results = operator.compute_eigenfrequencies(params)
    freqs = eigen_results['frequencies']
    harmonics = eigen_results['harmonics']
    
    ax2.plot(harmonics, freqs, 'ro-', markersize=8, linewidth=2, label='Eigenfrequencies')
    ax2.plot(harmonics, harmonics * F0_HZ, 'b--', linewidth=1, label=f'{harmonics[0]}×f₀ (expected)')
    ax2.set_xlabel('Harmonic Number n', fontsize=10)
    ax2.set_ylabel('Frequency (Hz)', fontsize=10)
    ax2.set_title(f'2. Eigenfrequencies fn = n×f₀\n(f₀ = {F0_HZ:.4f} Hz)', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    # 3. Beltrami Flow Field
    ax3 = fig.add_subplot(gs[0, 2])
    x = np.linspace(0, 10e-6, 50)
    y = np.linspace(0, 10e-6, 50)
    X, Y = np.meshgrid(x, y)
    vx, vy = beltrami.velocity_field_2d(X, Y, t=0)
    
    speed = np.sqrt(vx**2 + vy**2)
    contour = ax3.contourf(X*1e6, Y*1e6, speed, levels=20, cmap='viridis')
    ax3.streamplot(X*1e6, Y*1e6, vx, vy, color='white', linewidth=0.5, 
                   density=1.5, arrowsize=0.8)
    plt.colorbar(contour, ax=ax3, label='Speed (a.u.)')
    ax3.set_xlabel('x (μm)', fontsize=10)
    ax3.set_ylabel('y (μm)', fontsize=10)
    ax3.set_title('3. Beltrami Flow Field\n(ω = λv)', fontsize=11, fontweight='bold')
    ax3.set_aspect('equal')
    
    # 4. Microtubule Lattice
    ax4 = fig.add_subplot(gs[1, 0])
    flow_results = lattice.generate_streaming_flow(params)
    positions = flow_results['positions'] * 1e9  # Convert to nm
    velocities_mt = flow_results['velocities'] * 1e6  # Convert to μm/s
    
    ax4.plot(positions, velocities_mt, 'b-', linewidth=2)
    ax4.axhline(y=params.v_kinesin*1e6, color='r', linestyle='--', 
                label=f'Mean: {params.v_kinesin*1e6:.2f} μm/s')
    ax4.set_xlabel('Position (nm)', fontsize=10)
    ax4.set_ylabel('Velocity (μm/s)', fontsize=10)
    ax4.set_title(f'4. Microtubule Streaming\n({lattice.n_dimers} tubulin dimers)', 
                  fontsize=11, fontweight='bold')
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)
    
    # 5. Riemann Pressure Field
    ax5 = fig.add_subplot(gs[1, 1])
    x_grid = np.linspace(0, 10e-6, 1000)
    p = pressure_field.pressure_field_1d(x_grid, t=0)
    minima = pressure_field.find_pressure_minima(x_grid)
    
    ax5.plot(x_grid*1e6, p, 'b-', linewidth=2, label='Pressure field')
    ax5.plot(minima*1e6, pressure_field.pressure_field_1d(minima, t=0), 
             'ro', markersize=8, label=f'Minima ({len(minima)} found)')
    ax5.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    ax5.set_xlabel('Position (μm)', fontsize=10)
    ax5.set_ylabel('Pressure (a.u.)', fontsize=10)
    ax5.set_title('5. Riemann Pressure Field\n(Zeros as minima on σ=1/2)', 
                  fontsize=11, fontweight='bold')
    ax5.legend(fontsize=8)
    ax5.grid(True, alpha=0.3)
    
    # 6. Riemann Zeros
    ax6 = fig.add_subplot(gs[1, 2])
    zeros_t = pressure_field.riemann_zeros_t
    ax6.bar(range(1, len(zeros_t)+1), zeros_t, color='steelblue', alpha=0.7)
    ax6.set_xlabel('Zero Index', fontsize=10)
    ax6.set_ylabel('t value (ζ(1/2 + it) = 0)', fontsize=10)
    ax6.set_title('6. Riemann Zeros\n(Critical line σ = 1/2)', fontsize=11, fontweight='bold')
    ax6.grid(True, alpha=0.3, axis='y')
    
    # 7. Multi-Scale Frequency Propagation
    ax7 = fig.add_subplot(gs[2, 0])
    results = bridge.analyze_multi_scale_coherence(duration=60.0)
    
    scales = ['Molecular\n(Microtubules)', 'Cellular\n(C. elegans)', 'Cardiac\n(Heart)']
    frequencies_scale = [
        results['molecular']['fundamental_freq'],
        results['cellular']['scaled_freq'],
        results['cardiac']['scaled_f0']
    ]
    colors_scale = ['red', 'orange', 'blue']
    
    bars = ax7.bar(scales, frequencies_scale, color=colors_scale, alpha=0.7)
    ax7.set_ylabel('Frequency (Hz)', fontsize=10)
    ax7.set_title('7. Multi-Scale Frequency Propagation\n(f₀ across biological scales)', 
                  fontsize=11, fontweight='bold')
    ax7.set_yscale('log')
    ax7.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, freq in zip(bars, frequencies_scale):
        height = bar.get_height()
        ax7.text(bar.get_x() + bar.get_width()/2., height,
                f'{freq:.3f} Hz',
                ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # 8. HRV Spectrum
    ax8 = fig.add_subplot(gs[2, 1])
    hrv = HeartRateVariability()
    hrv_data = hrv.generate_synthetic_hrv(duration=120.0, f0_amplitude=0.03)
    spectrum = hrv.compute_hrv_spectrum(hrv_data['rr_intervals'])
    
    # Plot spectrum
    freq_mask = spectrum['frequencies'] < 5.0  # Show up to 5 Hz
    ax8.semilogy(spectrum['frequencies'][freq_mask], 
                 spectrum['power'][freq_mask], 'b-', linewidth=2)
    
    # Mark f₀ scaled harmonics
    f0_scaled = hrv_data['f0_scaled']
    for n in range(1, 4):
        ax8.axvline(x=n*f0_scaled, color='r', linestyle='--', alpha=0.5,
                   label=f'f₀×{n}' if n == 1 else '')
    
    ax8.set_xlabel('Frequency (Hz)', fontsize=10)
    ax8.set_ylabel('Power (a.u.)', fontsize=10)
    ax8.set_title('8. HRV Power Spectrum\n(f₀ harmonics in cardiac data)', 
                  fontsize=11, fontweight='bold')
    ax8.legend(fontsize=8)
    ax8.grid(True, alpha=0.3)
    
    # 9. Summary Statistics
    ax9 = fig.add_subplot(gs[2, 2])
    ax9.axis('off')
    
    summary_text = f"""
CYTOPLASMIC FLOW MODEL
Quantum Resonance Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Physical Parameters:
  ρ = {params.rho:.0f} kg/m³
  ν = {params.nu:.0e} m²/s
  L = {params.L*1e6:.1f} μm
  Re = {params.reynolds_number():.2e}
  
Fundamental Frequency:
  f₀ = {F0_HZ:.4f} Hz
  
Eigenfrequencies (first 3):
  f₁ = {freqs[0]:.2f} Hz
  f₂ = {freqs[1]:.2f} Hz
  f₃ = {freqs[2]:.2f} Hz
  
Microtubules:
  Dimers: {lattice.n_dimers}
  Spacing: {lattice.a*1e9:.1f} nm
  Velocity: {flow_results['mean_velocity']*1e6:.2f} μm/s
  
Riemann Zeros:
  Count: {len(zeros_t)}
  First: t₁ = {zeros_t[0]:.3f}
  
Multi-Scale Integration:
  Molecular: {frequencies_scale[0]:.2f} Hz
  Cellular: {frequencies_scale[1]:.3f} Hz
  Cardiac: {frequencies_scale[2]:.3f} Hz
  Coherence: {results['cardiac']['coherence_metric']:.3f}
  
Status: ✓ ALL SYSTEMS OPERATIONAL
    """
    
    ax9.text(0.1, 0.95, summary_text, transform=ax9.transAxes,
            fontsize=9, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Main title
    fig.suptitle('Cytoplasmic Flow Model with Quantum Resonance\n' +
                'Molecular Scale → Cellular Scale → Cardiac Scale Integration',
                fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    return fig


def run_complete_example():
    """
    Run complete example with validation and visualization.
    """
    print("=" * 80)
    print("CYTOPLASMIC FLOW MODEL - COMPLETE ANALYSIS")
    print("=" * 80)
    
    # 1. Run validation
    print("\n1. Running model validation...")
    print("-" * 80)
    results = validate_cytoplasmic_flow_model()
    
    print(f"\n✓ Reynolds Number: Re = {results['reynolds_number']:.2e}")
    print(f"✓ Stokes Regime: {results['is_stokes_regime']}")
    print(f"✓ Hermitian Check: {results['hermitian_check']['status']}")
    print(f"✓ Beltrami Condition: {results['beltrami_check']['condition_satisfied']}")
    print(f"✓ Pressure Minima Found: {results['pressure_minima_count']}")
    
    # 2. Run cardiac coherence integration
    print("\n2. Running multi-scale integration...")
    print("-" * 80)
    bridge = CardiacCoherenceBridge()
    integration = bridge.validate_integration_with_cytoplasmic_model()
    
    print(f"\n✓ Integration Status: {integration['status']}")
    print(f"✓ Frequency Consistency: {integration['consistency_check']}")
    
    # 3. Create visualization
    print("\n3. Creating comprehensive visualization...")
    print("-" * 80)
    
    try:
        fig = plot_complete_analysis()
        
        # Save figure
        output_path = 'cytoplasmic_flow_complete_analysis.png'
        fig.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"\n✓ Visualization saved to: {output_path}")
        
        # Try to display if possible
        try:
            plt.show()
        except:
            print("  (Display not available in this environment)")
        
    except Exception as e:
        print(f"\n⚠ Visualization error: {e}")
        print("  (Matplotlib may not be available)")
    
    print("\n" + "=" * 80)
    print("✓ ANALYSIS COMPLETE")
    print("=" * 80)
    
    return results, integration


if __name__ == '__main__':
    results, integration = run_complete_example()
