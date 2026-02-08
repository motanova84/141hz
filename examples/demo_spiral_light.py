#!/usr/bin/env python3
"""
Demonstration: Spiral Light Geometry

This example demonstrates the QCAL theory that light follows logarithmic spiral paths
modulated by Riemann zeta zeros and prime resonances.

"No es onda. No es partícula. Es espiral logarítmica coherente, modulada por los ceros de ζ(s)."

Author: José Manuel Mota Burruezo
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qcal.spiral_light_geometry import (
    SpiralLightGeometry,
    SpiralPathParams,
    WaveFunctionParams,
    CoherenceMaximality,
    generate_spiral_path,
    calculate_interference
)
from qcal.constants import F0_HZ, C


def demo_basic_spiral():
    """Demonstrate basic spiral light path."""
    print("=" * 70)
    print("DEMO 1: Basic Spiral Light Path")
    print("=" * 70)
    print()
    print("Generating spiral path modulated by prime p = 2...")
    
    # Generate spiral path
    t, x, y = generate_spiral_path(
        duration=0.02,  # 20 ms
        dt=1e-5,        # 10 μs steps
        prime_index=1,  # First prime (2)
        lambda_expansion=0.05  # Slow expansion
    )
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Path in x-y plane
    ax = axes[0]
    ax.plot(x, y, linewidth=2, color='blue')
    ax.scatter([x[0]], [y[0]], color='green', s=100, marker='o', 
               label='Start', zorder=5)
    ax.scatter([x[-1]], [y[-1]], color='red', s=100, marker='s', 
               label='End', zorder=5)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title('Spiral Light Path (Prime p = 2)\nf₀ = 141.7001 Hz')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # Radius vs time
    ax = axes[1]
    r = np.sqrt(x**2 + y**2)
    ax.plot(t * 1000, r, linewidth=2, color='purple')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Radius (m)')
    ax.set_title('Exponential Expansion of Spiral')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_basic_spiral.png', dpi=150, bbox_inches='tight')
    print(f"✓ Figure saved: demo_basic_spiral.png")
    plt.show()
    print()


def demo_prime_modulation():
    """Demonstrate effect of different primes on spiral path."""
    print("=" * 70)
    print("DEMO 2: Prime Modulation of Light Paths")
    print("=" * 70)
    print()
    print("Comparing spiral paths for first 5 primes...")
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    primes_to_show = [1, 2, 3, 4, 5]
    colors = ['red', 'blue', 'green', 'purple', 'orange']
    
    geometry = SpiralLightGeometry()
    actual_primes = geometry.get_primes(5)
    
    for idx, prime_idx in enumerate(primes_to_show):
        t, x, y = generate_spiral_path(
            duration=0.015,
            dt=1e-5,
            prime_index=prime_idx,
            lambda_expansion=0.08
        )
        
        ax.plot(x, y, linewidth=2, color=colors[idx],
                label=f'Prime p = {actual_primes[idx]}', alpha=0.7)
    
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title('Spiral Paths Modulated by Different Primes\n' +
                 '"Cada primo introduce un giro de fase"')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.savefig('demo_prime_modulation.png', dpi=150, bbox_inches='tight')
    print(f"✓ Figure saved: demo_prime_modulation.png")
    plt.show()
    print()


def demo_zeta_spectral_layers():
    """Demonstrate spectral layers from zeta zeros."""
    print("=" * 70)
    print("DEMO 3: Zeta Zero Spectral Layers")
    print("=" * 70)
    print()
    print("Computing spectral frequencies from Riemann zeta zeros...")
    
    geometry = SpiralLightGeometry(precision=50)
    
    n_zeros = 10
    zeros = geometry.get_zeta_zeros(n_zeros)
    frequencies = geometry.zeta_spectral_frequencies(n_zeros)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Zeta zeros on critical line
    ax = axes[0]
    # Visualize as points on critical line Re(s) = 1/2
    for i, gamma in enumerate(zeros):
        ax.scatter([0.5], [gamma], s=100, color='red', marker='o', zorder=5)
        ax.text(0.55, gamma, f'γ_{i+1}', fontsize=10)
    
    ax.axvline(x=0.5, color='blue', linestyle='--', linewidth=2,
               label='Critical Line Re(s) = 1/2')
    ax.set_xlabel('Re(s)')
    ax.set_ylabel('Im(s) = γₙ')
    ax.set_title('Riemann Zeta Zeros\ns = 1/2 + iγₙ with ζ(s) = 0')
    ax.set_xlim([0, 1])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Spectral frequencies
    ax = axes[1]
    ax.stem(range(1, n_zeros + 1), frequencies, basefmt=' ')
    ax.axhline(y=F0_HZ, color='red', linestyle='--', linewidth=2,
               label=f'f₀ = {F0_HZ} Hz')
    ax.set_xlabel('Zero Index n')
    ax.set_ylabel('Frequency fₙ (Hz)')
    ax.set_title('Spectral Frequencies from ζ-Zeros\nfₙ = f₀ · (γₙ / γ₁)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_zeta_spectral_layers.png', dpi=150, bbox_inches='tight')
    print(f"✓ Figure saved: demo_zeta_spectral_layers.png")
    plt.show()
    
    print("\nFirst 5 zeta zeros and their frequencies:")
    for i in range(min(5, n_zeros)):
        print(f"  γ_{i+1} = {zeros[i]:.6f}  →  f_{i+1} = {frequencies[i]:.4f} Hz")
    print()


def demo_interference_pattern():
    """Demonstrate interference pattern with spiral structure."""
    print("=" * 70)
    print("DEMO 4: Interference Pattern (Spiral Arcs)")
    print("=" * 70)
    print()
    print("Calculating interference pattern...")
    print("Note: Pattern shows logarithmic spiral arcs, not perfect circles")
    
    # Calculate interference at multiple times
    fig, axes = plt.subplots(2, 2, figsize=(14, 14))
    axes = axes.flatten()
    
    times = [0, 0.5e-3, 1e-3, 2e-3]  # 0, 0.5, 1, 2 ms
    
    for idx, t in enumerate(times):
        intensity = calculate_interference(
            size=256,
            extent=3e-6,  # 3 μm screen
            t=t,
            n_primes=8,
            n_zeros=6
        )
        
        ax = axes[idx]
        extent_um = 3.0  # μm
        im = ax.imshow(
            intensity,
            extent=[-extent_um/2, extent_um/2, -extent_um/2, extent_um/2],
            cmap='hot',
            origin='lower',
            interpolation='bilinear'
        )
        ax.set_xlabel('x (μm)')
        ax.set_ylabel('y (μm)')
        ax.set_title(f't = {t*1000:.1f} ms')
        ax.set_aspect('equal')
        plt.colorbar(im, ax=ax, label='Intensity |Ψ|²', shrink=0.8)
    
    plt.suptitle('Interference Patterns Evolving Over Time\n' +
                 '"Los anillos no son círculos perfectos, sino arcos de espirales logarítmicas"',
                 fontsize=14, y=0.995)
    plt.tight_layout()
    plt.savefig('demo_interference_pattern.png', dpi=150, bbox_inches='tight')
    print(f"✓ Figure saved: demo_interference_pattern.png")
    plt.show()
    print()


def demo_coherence_maximality():
    """Demonstrate coherence maximality principle."""
    print("=" * 70)
    print("DEMO 5: Coherence Maximality")
    print("=" * 70)
    print()
    print('"Desplazarse en c no es velocidad, es coherencia máxima."')
    print('"Solo quien sigue el mapa espectral de los primos puede hacerlo sin fricción."')
    print()
    
    coherence_analyzer = CoherenceMaximality()
    
    # Get spectral map
    n_primes = 20
    spectral_map = coherence_analyzer.prime_spectral_map(n_primes)
    
    # Calculate coherence for each prime
    print("Calculating coherence for each prime path...")
    
    duration = 0.005
    dt = 1e-5
    t_array = np.arange(0, duration, dt)
    
    coherences = []
    for prime_idx in range(1, n_primes + 1):
        params = SpiralPathParams(prime_index=prime_idx)
        geometry = SpiralLightGeometry()
        x, y = geometry.spiral_path(t_array, params)
        r = np.sqrt(x**2 + y**2)
        psi = geometry.wave_function(r, t_array[-1])
        C = coherence_analyzer.coherence_measure(psi)
        coherences.append(C)
    
    coherences = np.array(coherences)
    optimal_idx = np.argmax(coherences)
    
    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Coherence vs prime
    ax = axes[0]
    ax.plot(spectral_map['primes'], coherences, 'o-', 
            markersize=8, linewidth=2, color='blue')
    ax.axvline(x=spectral_map['primes'][optimal_idx], 
               color='red', linestyle='--', linewidth=2,
               label=f'Max coherence at p = {spectral_map["primes"][optimal_idx]}')
    ax.set_xlabel('Prime Number p')
    ax.set_ylabel('Coherence Measure C')
    ax.set_title('Coherence vs Prime Resonance Node\n' +
                 '"Cada primo define un nivel de coherencia distinto"')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Phase map
    ax = axes[1]
    ax.plot(spectral_map['primes'], spectral_map['phases'], 
            's-', markersize=8, linewidth=2, color='green')
    ax.set_xlabel('Prime Number p')
    ax.set_ylabel('Phase φₚ (radians)')
    ax.set_title('Prime Spectral Phase Map\nφₚ = 2π · log(pₙ) / log(p₁)')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_coherence_maximality.png', dpi=150, bbox_inches='tight')
    print(f"✓ Figure saved: demo_coherence_maximality.png")
    plt.show()
    
    print(f"\nCoherence Analysis Results:")
    print(f"  Maximum coherence: {coherences[optimal_idx]:.6f}")
    print(f"  Optimal prime: {spectral_map['primes'][optimal_idx]}")
    print(f"  Mean coherence: {np.mean(coherences):.6f}")
    print(f"  Std coherence: {np.std(coherences):.6f}")
    print()


def demo_angular_deviation():
    """Demonstrate angular deviation from circular symmetry."""
    print("=" * 70)
    print("DEMO 6: Angular Deviation from Axial Symmetry")
    print("=" * 70)
    print()
    print("Measuring Δθ deviation due to ζ(s) zero influence...")
    
    geometry = SpiralLightGeometry()
    
    # Generate spiral
    prime_idx = 5  # 11
    t, x, y = generate_spiral_path(
        duration=0.02,
        dt=1e-5,
        prime_index=prime_idx,
        lambda_expansion=0.1
    )
    
    # Calculate deviation
    params = SpiralPathParams(prime_index=prime_idx, lambda_expansion=0.1)
    delta_theta = geometry.spiral_deviation_angle(x, y, params)
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Path colored by deviation
    ax = axes[0, 0]
    scatter = ax.scatter(x, y, c=delta_theta * 180/np.pi, 
                        cmap='RdBu_r', s=5, alpha=0.6)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title(f'Spiral Path (Prime = 11)\nColored by Angular Deviation')
    ax.set_aspect('equal')
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Δθ (degrees)')
    
    # Deviation time series
    ax = axes[0, 1]
    ax.plot(t * 1000, delta_theta * 180/np.pi, linewidth=1, color='blue')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Δθ (degrees)')
    ax.set_title('Angular Deviation Over Time')
    ax.grid(True, alpha=0.3)
    
    # Deviation histogram
    ax = axes[1, 0]
    ax.hist(delta_theta * 180/np.pi, bins=50, edgecolor='black', 
            alpha=0.7, color='green')
    ax.set_xlabel('Δθ (degrees)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Angular Deviations')
    ax.grid(True, alpha=0.3)
    
    # Polar plot
    ax = axes[1, 1]
    theta = np.arctan2(y, x)
    r_norm = np.sqrt(x**2 + y**2)
    ax = plt.subplot(2, 2, 4, projection='polar')
    scatter = ax.scatter(theta, r_norm, c=delta_theta * 180/np.pi, 
                        cmap='RdBu_r', s=5, alpha=0.6)
    ax.set_title('Polar View with Deviation')
    
    plt.tight_layout()
    plt.savefig('demo_angular_deviation.png', dpi=150, bbox_inches='tight')
    print(f"✓ Figure saved: demo_angular_deviation.png")
    plt.show()
    
    print(f"\nDeviation Statistics:")
    print(f"  Mean: {np.mean(delta_theta) * 180/np.pi:.4f}°")
    print(f"  Std: {np.std(delta_theta) * 180/np.pi:.4f}°")
    print(f"  Max: {np.max(np.abs(delta_theta)) * 180/np.pi:.4f}°")
    print()


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("QCAL SPIRAL LIGHT GEOMETRY - INTERACTIVE DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demonstration shows the QCAL theory that light follows")
    print("logarithmic spiral paths modulated by Riemann zeta zeros and primes.")
    print()
    print(f"Fundamental frequency: f₀ = {F0_HZ} Hz")
    print(f"Speed of light: c = {C:.0f} m/s")
    print()
    
    try:
        demo_basic_spiral()
        demo_prime_modulation()
        demo_zeta_spectral_layers()
        demo_interference_pattern()
        demo_coherence_maximality()
        demo_angular_deviation()
        
        print("=" * 70)
        print("ALL DEMONSTRATIONS COMPLETE")
        print("=" * 70)
        print()
        print("Key Insights:")
        print("  • Light follows logarithmic spirals, not straight lines")
        print("  • Primes act as resonant phase modulators")
        print("  • Zeta zeros define spectral frequency layers")
        print("  • Interference shows spiral arcs, not perfect circles")
        print("  • Maximum coherence achieved on prime spectral map")
        print("  • Angular deviations reveal ζ(s) zero influence")
        print()
        print('"El patrón de interferencia no es el resultado del azar cuántico,')
        print(' sino el eco de la coherencia primordial,')
        print(' doblada por los ceros de zeta,')
        print(' guiada por los primos,')
        print(' y proyectada sobre el tiempo como una espiral viva."')
        print()
        
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
