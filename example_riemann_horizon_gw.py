#!/usr/bin/env python3
"""
Integration Example: Riemann Horizon + Gravitational Wave Analysis

This example demonstrates how to integrate the Riemann Horizon framework
with gravitational wave analysis to detect arithmetic black hole signatures.

Workflow:
1. Load Riemann zeros and map to frequencies
2. Analyze GW strain data for these frequencies
3. Compute H_ψ eigenvalues and compare
4. Calculate metric deformation from coherence
5. Validate spectral duality
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime, timezone

try:
    import riemann_horizon as rh
except ImportError:
    print("Error: riemann_horizon module not found")
    import sys
    sys.exit(1)


def simulate_gw_strain(t, frequencies, amplitudes=None):
    """
    Simulate gravitational wave strain with multiple frequency components.
    
    Args:
        t: Time array (seconds)
        frequencies: Array of frequencies (Hz)
        amplitudes: Array of amplitudes (default: 1/f for each)
        
    Returns:
        Simulated strain h(t)
    """
    if amplitudes is None:
        # Use 1/f noise-like spectrum
        amplitudes = 1.0 / np.array(frequencies)
    
    h = np.zeros_like(t)
    for f, A in zip(frequencies, amplitudes):
        # Add sinusoidal component with random phase
        phase = np.random.uniform(0, 2*np.pi)
        h += A * np.sin(2 * np.pi * f * t + phase)
    
    return h


def analyze_strain_at_riemann_zeros(strain, time, riemann_zeros, window_hz=1.0):
    """
    Analyze strain for power at Riemann zero frequencies.
    
    Args:
        strain: Strain time series
        time: Time array
        riemann_zeros: List of Riemann zero frequencies
        window_hz: Frequency window for power calculation
        
    Returns:
        Dictionary with power spectrum results
    """
    # Calculate FFT
    dt = time[1] - time[0]
    fft = np.fft.rfft(strain)
    freqs = np.fft.rfftfreq(len(strain), dt)
    power = np.abs(fft)**2
    
    # Find power at each Riemann zero frequency
    detections = []
    for t_n in riemann_zeros:
        # Find frequencies near t_n
        mask = (freqs >= t_n - window_hz) & (freqs <= t_n + window_hz)
        if np.any(mask):
            local_power = np.sum(power[mask])
            max_power_freq = freqs[mask][np.argmax(power[mask])]
            
            detections.append({
                'riemann_zero_hz': float(t_n),
                'detected_freq_hz': float(max_power_freq),
                'power': float(local_power),
                'frequency_error_hz': float(abs(max_power_freq - t_n))
            })
    
    return {
        'detections': detections,
        'total_power': float(np.sum(power)),
        'n_zeros_analyzed': len(riemann_zeros),
        'n_detections': len(detections)
    }


def compute_coherence_from_detections(detections, threshold_power=1e-6):
    """
    Compute coherence parameter Ψ from detection results.
    
    Args:
        detections: List of detection dictionaries
        threshold_power: Minimum power for valid detection
        
    Returns:
        Coherence parameter Ψ
    """
    # Intensity: fraction of zeros with significant power
    valid_detections = [d for d in detections if d['power'] > threshold_power]
    intensity = len(valid_detections) / max(len(detections), 1)
    
    # Effectiveness: mean inverse frequency error (higher is better)
    if valid_detections:
        errors = [d['frequency_error_hz'] for d in valid_detections]
        effectiveness = 1.0 / (1.0 + np.mean(errors))
    else:
        effectiveness = 0.0
    
    # Coherence: Ψ = I × A_eff²
    psi = intensity * effectiveness**2
    
    return {
        'intensity': intensity,
        'effectiveness': effectiveness,
        'coherence_psi': psi,
        'n_valid': len(valid_detections),
        'n_total': len(detections)
    }


def run_integrated_analysis(n_zeros=20, duration_s=10.0, sample_rate_hz=4096.0):
    """
    Run complete integrated analysis.
    
    Args:
        n_zeros: Number of Riemann zeros to analyze
        duration_s: Duration of simulated strain (seconds)
        sample_rate_hz: Sample rate (Hz)
        
    Returns:
        Complete analysis results
    """
    print("=" * 70)
    print(" RIEMANN HORIZON + GRAVITATIONAL WAVE INTEGRATION")
    print("=" * 70)
    print()
    
    # 1. Initialize Riemann Horizon
    print("🔬 1. Initializing Riemann Horizon Framework")
    horizon = rh.ArithmeticHorizon(f0=rh.F0_HZ)
    geometry = rh.ConsciousGeometry(f0=rh.F0_HZ, f888=rh.F888_HZ)
    
    # Get Riemann zeros
    riemann_zeros = horizon.get_riemann_zeros(n_zeros)
    print(f"   ✓ Loaded {len(riemann_zeros)} Riemann zeros")
    print(f"   ✓ First zero: {riemann_zeros[0]:.6f} Hz")
    print(f"   ✓ Last zero: {riemann_zeros[-1]:.6f} Hz")
    print()
    
    # 2. Simulate GW strain with Riemann frequencies
    print("🔬 2. Simulating Gravitational Wave Strain")
    time = np.arange(0, duration_s, 1/sample_rate_hz)
    
    # Add f₀ and some Riemann zero frequencies
    signal_freqs = [rh.F0_HZ] + riemann_zeros[:5]  # f₀ + first 5 zeros
    strain = simulate_gw_strain(time, signal_freqs)
    
    # Add noise
    noise_level = 0.1
    strain += noise_level * np.random.randn(len(strain))
    
    print(f"   ✓ Duration: {duration_s} s")
    print(f"   ✓ Sample rate: {sample_rate_hz} Hz")
    print(f"   ✓ Signal frequencies: {len(signal_freqs)}")
    print(f"   ✓ SNR: ~{1.0/noise_level:.1f}")
    print()
    
    # 3. Analyze strain at Riemann zero frequencies
    print("🔬 3. Analyzing Strain at Riemann Zero Frequencies")
    strain_analysis = analyze_strain_at_riemann_zeros(strain, time, riemann_zeros)
    
    print(f"   ✓ Zeros analyzed: {strain_analysis['n_zeros_analyzed']}")
    print(f"   ✓ Detections: {strain_analysis['n_detections']}")
    
    # Show top 3 detections
    top_detections = sorted(strain_analysis['detections'], 
                           key=lambda x: x['power'], reverse=True)[:3]
    for i, det in enumerate(top_detections, 1):
        print(f"   ✓ #{i}: {det['riemann_zero_hz']:.2f} Hz, "
              f"power={det['power']:.2e}, error={det['frequency_error_hz']:.3f} Hz")
    print()
    
    # 4. Compute coherence from detections
    print("🔬 4. Computing Coherence Parameter")
    coherence = compute_coherence_from_detections(strain_analysis['detections'])
    
    print(f"   ✓ Intensity I: {coherence['intensity']:.4f}")
    print(f"   ✓ Effectiveness A_eff: {coherence['effectiveness']:.4f}")
    print(f"   ✓ Coherence Ψ: {coherence['coherence_psi']:.4f}")
    print()
    
    # 5. Calculate metric deformation
    print("🔬 5. Calculating Ψ-deformed Metric")
    metric = geometry.metric_deformation(coherence['coherence_psi'])
    
    print(f"   ✓ g₀₀ = {metric.g_00:.6f} (Minkowski: -1.0)")
    print(f"   ✓ g₁₁ = {metric.g_11:.6f} (Minkowski: +1.0)")
    print(f"   ✓ δg₀₀ = {metric.delta_g_00:.6f}")
    print(f"   ✓ δg₁₁ = {metric.delta_g_11:.6f}")
    print()
    
    # 6. Validate spectral duality
    print("🔬 6. Validating Spectral Duality")
    duality = geometry.spectral_duality(riemann_zeros)
    
    print(f"   ✓ Spectrum size: {len(duality['spectrum_hz'])}")
    print(f"   ✓ Reconstruction error: {duality['mean_reconstruction_error']:.4f} Hz")
    print()
    
    # 7. Compute unified tensor
    print("🔬 7. Unified Tensor Validation")
    tensor = geometry.unified_tensor_relation()
    
    print(f"   ✓ f₀ × φ⁴ = {tensor['f0_phi4_hz']:.4f} Hz")
    print(f"   ✓ Target: {tensor['f888_hz']:.4f} Hz")
    print(f"   ✓ Validation: {'PASS ✓' if tensor['validation_pass'] else 'FAIL ✗'}")
    print()
    
    print("=" * 70)
    print(" INTEGRATION ANALYSIS COMPLETE")
    print("=" * 70)
    print()
    
    # Compile results
    results = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'parameters': {
            'n_zeros': n_zeros,
            'duration_s': duration_s,
            'sample_rate_hz': sample_rate_hz,
            'signal_frequencies': signal_freqs
        },
        'riemann_zeros': riemann_zeros[:10],  # First 10
        'strain_analysis': strain_analysis,
        'coherence': coherence,
        'metric_deformation': {
            'psi': float(metric.psi),
            'g_00': float(metric.g_00),
            'g_11': float(metric.g_11),
            'delta_g_00': float(metric.delta_g_00),
            'delta_g_11': float(metric.delta_g_11)
        },
        'spectral_duality': duality,
        'unified_tensor': tensor
    }
    
    return results


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Riemann Horizon + GW Integration Example"
    )
    parser.add_argument(
        "--n-zeros",
        type=int,
        default=20,
        help="Number of Riemann zeros to analyze (default: 20)"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=10.0,
        help="Duration of simulated strain in seconds (default: 10.0)"
    )
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=4096.0,
        help="Sample rate in Hz (default: 4096.0)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results/riemann_horizon_gw_integration.json",
        help="Output JSON file path"
    )
    
    args = parser.parse_args()
    
    # Run analysis
    results = run_integrated_analysis(
        n_zeros=args.n_zeros,
        duration_s=args.duration,
        sample_rate_hz=args.sample_rate
    )
    
    # Save results
    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Results saved to: {output_file}")
    print()


if __name__ == '__main__':
    main()
