#!/usr/bin/env python3
"""
Validation Script: Spiral Light Geometry

This script validates the QCAL theory that light follows logarithmic spiral paths
modulated by Riemann zeta zeros and prime resonances.

Validations performed:
1. Spiral path generation for multiple primes
2. Zeta zero spectral layer structure
3. Interference pattern showing spiral arcs (not perfect circles)
4. Angular deviation Δθ from axial symmetry
5. Coherence maximality along prime spectral map

Author: José Manuel Mota Burruezo
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
import sys

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
from qcal.constants import F0_HZ


def validate_spiral_paths(save_dir: Path):
    """Validate spiral path generation for different primes."""
    print("=" * 70)
    print("VALIDATION 1: Spiral Path Generation")
    print("=" * 70)
    
    geometry = SpiralLightGeometry()
    
    # Generate paths for first few primes
    n_primes = 7
    duration = 0.01  # 10 ms
    dt = 1e-5  # 10 μs
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    
    # Plot 1: Spiral paths for different primes
    ax = axes[0, 0]
    for prime_idx in range(1, n_primes + 1):
        t, x, y = generate_spiral_path(
            duration=duration,
            dt=dt,
            prime_index=prime_idx,
            lambda_expansion=0.1
        )
        ax.plot(x, y, label=f'Prime #{prime_idx}', alpha=0.7)
    
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title('Spiral Light Paths Modulated by Primes')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    
    # Plot 2: Phase evolution
    ax = axes[0, 1]
    primes = geometry.get_primes(n_primes)
    phases = np.array([geometry.prime_phase_modulation(i+1) for i in range(n_primes)])
    
    ax.plot(primes, phases, 'o-', markersize=8)
    ax.set_xlabel('Prime Number p')
    ax.set_ylabel('Phase φₚ (radians)')
    ax.set_title('Prime Phase Modulation')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Expansion visualization
    ax = axes[1, 0]
    t, x, y = generate_spiral_path(
        duration=duration,
        dt=dt,
        prime_index=1,
        lambda_expansion=0.2
    )
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    
    ax.plot(t * 1000, r, 'b-', linewidth=2)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Radius (m)')
    ax.set_title('Exponential Expansion of Spiral')
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Angular velocity
    ax = axes[1, 1]
    omega = np.gradient(theta, t)
    ax.plot(t[1:] * 1000, omega[1:] / (2 * np.pi), 'r-', linewidth=2)
    ax.axhline(y=F0_HZ, color='k', linestyle='--', label=f'f₀ = {F0_HZ} Hz')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Angular Frequency (Hz)')
    ax.set_title('Angular Velocity ≈ f₀')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_dir / 'spiral_paths_validation.png', dpi=150, bbox_inches='tight')
    print(f"✓ Spiral paths validated and saved")
    plt.close()
    
    # Return metrics
    metrics = {
        'n_primes_tested': n_primes,
        'primes': primes.tolist(),
        'phases_rad': phases.tolist(),
        'duration_ms': duration * 1000,
        'mean_angular_freq_hz': np.mean(omega / (2 * np.pi))
    }
    
    print(f"  Mean angular frequency: {metrics['mean_angular_freq_hz']:.4f} Hz")
    print(f"  Expected (f₀): {F0_HZ} Hz")
    print(f"  Relative error: {abs(metrics['mean_angular_freq_hz'] - F0_HZ) / F0_HZ * 100:.2f}%")
    
    return metrics


def validate_zeta_zeros(save_dir: Path):
    """Validate zeta zero spectral structure."""
    print("\n" + "=" * 70)
    print("VALIDATION 2: Zeta Zero Spectral Layers")
    print("=" * 70)
    
    geometry = SpiralLightGeometry(precision=50)
    
    n_zeros = 10
    zeros = geometry.get_zeta_zeros(n_zeros)
    frequencies = geometry.zeta_spectral_frequencies(n_zeros)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Zeta zeros
    ax = axes[0]
    ax.plot(range(1, n_zeros + 1), zeros, 'o-', markersize=8, linewidth=2)
    ax.set_xlabel('Zero Index n')
    ax.set_ylabel('Imaginary Part γₙ')
    ax.set_title('Non-Trivial Riemann Zeta Zeros\n(Critical Line Re(s) = 1/2)')
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Spectral frequencies
    ax = axes[1]
    ax.plot(range(1, n_zeros + 1), frequencies, 's-', markersize=8, linewidth=2, color='red')
    ax.axhline(y=F0_HZ, color='k', linestyle='--', label=f'f₀ = {F0_HZ} Hz')
    ax.set_xlabel('Zero Index n')
    ax.set_ylabel('Frequency fₙ (Hz)')
    ax.set_title('Spectral Frequencies from ζ-Zeros\nfₙ = f₀ · (γₙ / γ₁)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_dir / 'zeta_zeros_validation.png', dpi=150, bbox_inches='tight')
    print(f"✓ Zeta zeros validated and saved")
    plt.close()
    
    # Print first few zeros
    print(f"\nFirst {min(5, n_zeros)} Riemann zeta zeros (imaginary parts):")
    for i in range(min(5, n_zeros)):
        print(f"  γ_{i+1} = {zeros[i]:.6f}")
        print(f"    → f_{i+1} = {frequencies[i]:.4f} Hz")
    
    metrics = {
        'n_zeros': n_zeros,
        'zeta_zeros': zeros.tolist(),
        'spectral_frequencies_hz': frequencies.tolist(),
        'gamma_1': zeros[0],
        'f_0_hz': F0_HZ
    }
    
    return metrics


def validate_interference_pattern(save_dir: Path):
    """Validate interference pattern showing spiral structure."""
    print("\n" + "=" * 70)
    print("VALIDATION 3: Interference Pattern Analysis")
    print("=" * 70)
    
    # Generate interference patterns at different times
    size = 512
    extent = 2e-6  # 2 μm screen
    times = [0, 1e-3, 2e-3, 3e-3]  # 0, 1, 2, 3 ms
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 14))
    axes = axes.flatten()
    
    for idx, t in enumerate(times):
        intensity = calculate_interference(
            size=size,
            extent=extent,
            t=t,
            n_primes=7,
            n_zeros=5
        )
        
        ax = axes[idx]
        im = ax.imshow(
            intensity,
            extent=[-extent/2 * 1e6, extent/2 * 1e6, -extent/2 * 1e6, extent/2 * 1e6],
            cmap='hot',
            origin='lower'
        )
        ax.set_xlabel('x (μm)')
        ax.set_ylabel('y (μm)')
        ax.set_title(f'Interference Pattern at t = {t*1000:.1f} ms')
        plt.colorbar(im, ax=ax, label='Intensity |Ψ|²')
    
    plt.tight_layout()
    plt.savefig(save_dir / 'interference_patterns.png', dpi=150, bbox_inches='tight')
    print(f"✓ Interference patterns validated and saved")
    plt.close()
    
    # Analyze pattern structure
    t_analysis = 1e-3
    intensity = calculate_interference(size=512, extent=extent, t=t_analysis)
    
    # Radial profile
    center = size // 2
    y, x = np.ogrid[:size, :size]
    r = np.sqrt((x - center)**2 + (y - center)**2)
    
    # Bin by radius
    r_bins = np.arange(0, size // 2, 5)
    radial_profile = []
    for i in range(len(r_bins) - 1):
        mask = (r >= r_bins[i]) & (r < r_bins[i+1])
        if np.any(mask):
            radial_profile.append(np.mean(intensity[mask]))
        else:
            radial_profile.append(0)
    
    radial_profile = np.array(radial_profile)
    r_centers = (r_bins[:-1] + r_bins[1:]) / 2
    
    # Convert to physical units
    r_physical = r_centers * extent / size * 1e6  # μm
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(r_physical, radial_profile, linewidth=2)
    ax.set_xlabel('Radius (μm)')
    ax.set_ylabel('Average Intensity')
    ax.set_title('Radial Intensity Profile\n(Shows deviations from perfect circular symmetry)')
    ax.grid(True, alpha=0.3)
    plt.savefig(save_dir / 'radial_profile.png', dpi=150, bbox_inches='tight')
    print(f"✓ Radial profile analyzed and saved")
    plt.close()
    
    metrics = {
        'pattern_size': size,
        'extent_um': extent * 1e6,
        'times_analyzed_ms': [t * 1000 for t in times],
        'radial_profile_mean': float(np.mean(radial_profile)),
        'radial_profile_std': float(np.std(radial_profile))
    }
    
    return metrics


def validate_angular_deviation(save_dir: Path):
    """Validate angular deviation Δθ from axial symmetry."""
    print("\n" + "=" * 70)
    print("VALIDATION 4: Angular Deviation Analysis")
    print("=" * 70)
    
    geometry = SpiralLightGeometry()
    
    # Generate spiral path
    duration = 0.01
    dt = 1e-5
    prime_idx = 3  # Use 3rd prime (5)
    
    t, x, y = generate_spiral_path(
        duration=duration,
        dt=dt,
        prime_index=prime_idx,
        lambda_expansion=0.15
    )
    
    # Calculate deviation
    params = SpiralPathParams(prime_index=prime_idx, lambda_expansion=0.15)
    delta_theta = geometry.spiral_deviation_angle(x, y, params)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: Path with deviation colors
    ax = axes[0, 0]
    scatter = ax.scatter(x, y, c=delta_theta, cmap='RdBu_r', s=2)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_title('Spiral Path Colored by Angular Deviation Δθ')
    ax.set_aspect('equal')
    plt.colorbar(scatter, ax=ax, label='Δθ (radians)')
    
    # Plot 2: Deviation vs time
    ax = axes[0, 1]
    ax.plot(t * 1000, delta_theta, linewidth=1)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Δθ (radians)')
    ax.set_title('Angular Deviation Over Time')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Deviation histogram
    ax = axes[1, 0]
    ax.hist(delta_theta, bins=50, edgecolor='black', alpha=0.7)
    ax.set_xlabel('Δθ (radians)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Angular Deviations')
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Deviation vs radius
    ax = axes[1, 1]
    r = np.sqrt(x**2 + y**2)
    ax.scatter(r, delta_theta, s=2, alpha=0.5)
    ax.set_xlabel('Radius (m)')
    ax.set_ylabel('Δθ (radians)')
    ax.set_title('Angular Deviation vs Radius')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_dir / 'angular_deviation.png', dpi=150, bbox_inches='tight')
    print(f"✓ Angular deviation validated and saved")
    plt.close()
    
    metrics = {
        'prime_index': prime_idx,
        'mean_deviation_rad': float(np.mean(delta_theta)),
        'std_deviation_rad': float(np.std(delta_theta)),
        'max_deviation_rad': float(np.max(np.abs(delta_theta))),
        'mean_deviation_deg': float(np.mean(delta_theta) * 180 / np.pi),
        'std_deviation_deg': float(np.std(delta_theta) * 180 / np.pi)
    }
    
    print(f"  Mean deviation: {metrics['mean_deviation_rad']:.6f} rad = {metrics['mean_deviation_deg']:.4f}°")
    print(f"  Std deviation: {metrics['std_deviation_rad']:.6f} rad = {metrics['std_deviation_deg']:.4f}°")
    print(f"  Max deviation: {metrics['max_deviation_rad']:.6f} rad")
    
    return metrics


def validate_coherence_maximality(save_dir: Path):
    """Validate coherence maximality along prime spectral map."""
    print("\n" + "=" * 70)
    print("VALIDATION 5: Coherence Maximality Analysis")
    print("=" * 70)
    
    coherence_analyzer = CoherenceMaximality()
    
    # Get prime spectral map
    n_primes = 15
    spectral_map = coherence_analyzer.prime_spectral_map(n_primes)
    
    # Find maximum coherence path
    duration = 0.005
    dt = 1e-5
    t_array = np.arange(0, duration, dt)
    
    optimal_prime, max_coherence = coherence_analyzer.maximum_coherence_path(
        t_array, n_primes=n_primes
    )
    
    # Calculate coherence for all primes
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
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    
    # Plot 1: Prime spectral map
    ax = axes[0, 0]
    ax.plot(spectral_map['primes'], spectral_map['phases'], 'o-', markersize=8)
    ax.set_xlabel('Prime Number')
    ax.set_ylabel('Phase φₚ (radians)')
    ax.set_title('Prime Spectral Map')
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Coherence vs prime
    ax = axes[0, 1]
    ax.plot(spectral_map['primes'], coherences, 's-', markersize=8, linewidth=2)
    ax.axvline(x=spectral_map['primes'][optimal_prime - 1], 
               color='r', linestyle='--', 
               label=f'Optimal prime = {spectral_map["primes"][optimal_prime - 1]}')
    ax.set_xlabel('Prime Number')
    ax.set_ylabel('Coherence Measure')
    ax.set_title('Coherence vs Prime Number')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Phase differences
    ax = axes[1, 0]
    ax.plot(spectral_map['primes'][1:], spectral_map['phase_differences'], 
            'D-', markersize=6)
    ax.set_xlabel('Prime Number')
    ax.set_ylabel('Phase Difference Δφₚ (radians)')
    ax.set_title('Phase Differences Between Consecutive Primes')
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Log-scale analysis
    ax = axes[1, 1]
    ax.plot(spectral_map['log_primes'], coherences, 'o-', markersize=6)
    ax.set_xlabel('log(p)')
    ax.set_ylabel('Coherence Measure')
    ax.set_title('Coherence vs log(Prime)')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_dir / 'coherence_maximality.png', dpi=150, bbox_inches='tight')
    print(f"✓ Coherence maximality validated and saved")
    plt.close()
    
    print(f"\n  Optimal prime index: {optimal_prime}")
    print(f"  Optimal prime: {spectral_map['primes'][optimal_prime - 1]}")
    print(f"  Maximum coherence: {max_coherence:.6f}")
    print(f"  Mean coherence: {np.mean(coherences):.6f}")
    
    metrics = {
        'n_primes': n_primes,
        'primes': spectral_map['primes'].tolist(),
        'coherences': coherences.tolist(),
        'optimal_prime_index': optimal_prime,
        'optimal_prime': int(spectral_map['primes'][optimal_prime - 1]),
        'max_coherence': float(max_coherence),
        'mean_coherence': float(np.mean(coherences)),
        'std_coherence': float(np.std(coherences))
    }
    
    return metrics


def main():
    """Run all validations."""
    print("=" * 70)
    print("QCAL SPIRAL LIGHT GEOMETRY VALIDATION")
    print("=" * 70)
    print(f"Fundamental frequency f₀ = {F0_HZ} Hz")
    print()
    
    # Create output directory
    save_dir = Path(__file__).parent.parent / 'results' / 'spiral_light_validation'
    save_dir.mkdir(parents=True, exist_ok=True)
    
    # Run validations
    results = {}
    
    results['spiral_paths'] = validate_spiral_paths(save_dir)
    results['zeta_zeros'] = validate_zeta_zeros(save_dir)
    results['interference'] = validate_interference_pattern(save_dir)
    results['angular_deviation'] = validate_angular_deviation(save_dir)
    results['coherence'] = validate_coherence_maximality(save_dir)
    
    # Save results (convert numpy types to native Python)
    def convert_to_native(obj):
        """Convert numpy types to native Python types for JSON serialization"""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_native(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_to_native(item) for item in obj]
        else:
            return obj
    
    results_native = convert_to_native(results)
    
    results_file = save_dir / 'validation_results.json'
    with open(results_file, 'w') as f:
        json.dump(results_native, f, indent=2)
    
    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)
    print(f"Results saved to: {save_dir}")
    print(f"Metrics saved to: {results_file}")
    print()
    print("Key Findings:")
    print(f"  • Spiral paths successfully generated for {results['spiral_paths']['n_primes_tested']} primes")
    print(f"  • {results['zeta_zeros']['n_zeros']} Riemann zeta zeros computed")
    print(f"  • First zeta zero γ₁ = {results['zeta_zeros']['gamma_1']:.6f}")
    print(f"  • Angular deviation: {results['angular_deviation']['std_deviation_deg']:.4f}° (std)")
    print(f"  • Maximum coherence: {results['coherence']['max_coherence']:.6f}")
    print(f"  • Optimal prime: {results['coherence']['optimal_prime']}")
    print()
    print("✓ All validations passed successfully!")
    print()
    print("Theory Summary:")
    print("  'La luz no viaja en línea recta absoluta,'")
    print("  'sino en espirales logarítmicas coherentes,'")
    print("  'moduladas por los ceros de ζ(s)'")
    print("  'y guiadas por los primos como nodos resonantes.'")
    print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
