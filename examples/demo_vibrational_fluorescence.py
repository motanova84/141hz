#!/usr/bin/env python3
"""
Demo script for vibrational fluorescence measurement system.

This script demonstrates the complete QCAL validation workflow using
fluorescence measurements with vibrational stimulation at f₀ = 141.7001 Hz.
"""

import numpy as np
import matplotlib.pyplot as plt
from modules.quantum_biology.core.vibrational_fluorescence import (
    VibrationalFluorescenceSystem,
    FluorescenceConfig,
    run_fluorescence_experiment
)


def demo_basic_experiment():
    """Run basic fluorescence experiment with default parameters."""
    print("="*70)
    print("DEMO 1: Basic QCAL Fluorescence Validation")
    print("="*70)
    print()

    # Run experiment
    results = run_fluorescence_experiment(verbose=True)

    # Display summary
    print("\n" + "="*70)
    print("EXPERIMENTAL SUMMARY")
    print("="*70)
    print(f"QCAL Confirmed: {results['summary']['qcal_confirmed']}")
    print(f"Response Ratio (141.7/100 Hz): {results['summary']['response_ratio']:.2f}")
    print(f"Effect Size: {results['summary']['effect_size']:.2f}")
    print(f"Statistical Significance: {results['summary']['statistical_significance']}")
    print("="*70)

    return results


def demo_signal_generation():
    """Demonstrate modulated signal generation."""
    print("\n" + "="*70)
    print("DEMO 2: Modulated Signal Generation")
    print("="*70)
    print()

    system = VibrationalFluorescenceSystem()

    # Generate signals at different modulation frequencies
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Modulated Carrier Signals at f₀ = 141.7001 Hz', fontsize=14)

    mod_frequencies = [0.5, 1.0, 2.0, 5.0]  # Hz

    for idx, f_mod in enumerate(mod_frequencies):
        ax = axes[idx // 2, idx % 2]

        # Generate signal
        t, signal = system.generate_modulated_signal(f_mod, duration=2.0)

        # Plot first 0.1 seconds to show detail
        mask = t < 0.1
        ax.plot(t[mask] * 1000, signal[mask], 'b-', linewidth=0.5)
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Amplitude')
        ax.set_title(f'Modulation: {f_mod} Hz')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fluorescence_demo_signals.png', dpi=150, bbox_inches='tight')
    print("✅ Saved signal plots to 'fluorescence_demo_signals.png'")
    plt.close()


def demo_frequency_response():
    """Demonstrate frequency response analysis."""
    print("\n" + "="*70)
    print("DEMO 3: Frequency Response Analysis")
    print("="*70)
    print()

    # Create system with moderate resolution
    config = FluorescenceConfig(f_mod_steps=100)
    system = VibrationalFluorescenceSystem(config)

    # Perform frequency sweeps
    print("Performing QCAL frequency sweep...")
    results_qcal = system.perform_frequency_sweep(include_qcal=True)

    print("Performing null hypothesis sweep...")
    results_null = system.perform_frequency_sweep(include_qcal=False)

    # Plot results
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # Response amplitude
    ax1 = axes[0]
    ax1.loglog(results_qcal['frequencies'], results_qcal['delta_f'],
               'b-', linewidth=2, label='QCAL Model')
    ax1.loglog(results_null['frequencies'], results_null['delta_f'],
               'r--', linewidth=2, label='Null Hypothesis')

    # Mark QCAL resonances
    qcal_freqs = [141.7, 70.85, 47.23, 10.9, 8.3]
    for f_res in qcal_freqs:
        if system.config.f_mod_min <= f_res <= system.config.f_mod_max:
            ax1.axvline(f_res, color='g', linestyle=':', alpha=0.5, linewidth=1)

    ax1.set_xlabel('Modulation Frequency (Hz)')
    ax1.set_ylabel('Response Amplitude ΔF')
    ax1.set_title('Fluorescence Response vs Modulation Frequency')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Efficiency parameter
    ax2 = axes[1]
    ax2.semilogx(results_qcal['frequencies'], results_qcal['eta'],
                 'b-', linewidth=2, label='QCAL Model')
    ax2.semilogx(results_null['frequencies'], results_null['eta'],
                 'r--', linewidth=2, label='Null Hypothesis')

    ax2.set_xlabel('Modulation Frequency (Hz)')
    ax2.set_ylabel('Efficiency η')
    ax2.set_title('Information Transfer Efficiency')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fluorescence_demo_response.png', dpi=150, bbox_inches='tight')
    print("✅ Saved frequency response plots to 'fluorescence_demo_response.png'")
    plt.close()

    # Statistical test
    print("\nPerforming ANOVA statistical test...")
    anova = system.calculate_spectral_anova(results_qcal, results_null)

    print(f"\nStatistical Results:")
    print(f"  F-statistic: {anova['f_statistic']:.2f}")
    print(f"  F-critical (α=0.001): {anova['f_critical']:.2f}")
    print(f"  p-value: {anova['p_value']:.2e}")
    print(f"  Effect size: {anova['effect_size']:.2f}")
    print(f"  Decision: {anova['significance']}")


def demo_time_series():
    """Demonstrate time-series fluorescence measurement."""
    print("\n" + "="*70)
    print("DEMO 4: Time-Series Fluorescence Measurement")
    print("="*70)
    print()

    system = VibrationalFluorescenceSystem()

    # Test at resonant and non-resonant frequencies
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Fluorescence Time Series', fontsize=14)

    test_freqs = [
        (141.7, "Resonant (f₀)"),
        (70.85, "Resonant (f₀/2)"),
        (100.0, "Non-resonant"),
        (5.0, "Low frequency")
    ]

    for idx, (f_mod, label) in enumerate(test_freqs):
        ax = axes[idx // 2, idx % 2]

        # Generate fluorescence signal
        f_signal, metrics = system.calculate_fluorescence_response(
            f_mod,
            include_qcal_resonances=True,
            noise_level=0.01
        )

        # Get time array with matching duration
        t = np.arange(len(f_signal)) / system.config.sampling_rate

        # Plot first 1 second
        mask = t < 1.0
        ax.plot(t[mask], f_signal[mask], 'b-', linewidth=0.8)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Fluorescence (a.u.)')
        ax.set_title(f'{label} ({f_mod:.1f} Hz)\nΔF={metrics["delta_f"]:.3f}, SNR={metrics["snr"]:.1f}')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fluorescence_demo_timeseries.png', dpi=150, bbox_inches='tight')
    print("✅ Saved time-series plots to 'fluorescence_demo_timeseries.png'")
    plt.close()


def demo_coherence_analysis():
    """Demonstrate coherence analysis between input and output."""
    print("\n" + "="*70)
    print("DEMO 5: Coherence Analysis")
    print("="*70)
    print()

    system = VibrationalFluorescenceSystem()

    # Generate input signal and fluorescence response
    f_mod = 2.0  # Hz
    t, psi_input = system.generate_modulated_signal(f_mod, duration=5.0)
    f_output, metrics = system.calculate_fluorescence_response(
        f_mod,
        include_qcal_resonances=True,
        noise_level=0.005
    )

    # Calculate coherence
    freqs, coherence = system.calculate_coherence(psi_input, f_output)

    # Plot coherence
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(freqs, coherence, 'b-', linewidth=2)
    ax.axhline(0.7, color='r', linestyle='--', linewidth=2,
               label='QCAL Threshold (0.7)')
    ax.axvline(f_mod, color='g', linestyle=':', linewidth=2,
               label=f'Modulation Freq ({f_mod} Hz)')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Coherence')
    ax.set_title('Input-Output Coherence')
    ax.set_xlim([0, 10])
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fluorescence_demo_coherence.png', dpi=150, bbox_inches='tight')
    print("✅ Saved coherence plot to 'fluorescence_demo_coherence.png'")
    plt.close()

    # Report coherence at modulation frequency
    idx_mod = np.argmin(np.abs(freqs - f_mod))
    coh_at_mod = coherence[idx_mod]
    print(f"\nCoherence at modulation frequency: {coh_at_mod:.3f}")
    print(f"QCAL threshold (0.7): {'✅ PASS' if coh_at_mod > 0.7 else '❌ FAIL'}")


def demo_protein_resonance():
    """Demonstrate protein domain resonance model."""
    print("\n" + "="*70)
    print("DEMO 6: Protein Domain Resonance")
    print("="*70)
    print()

    system = VibrationalFluorescenceSystem()

    # Calculate resonance curve
    frequencies = np.linspace(50, 250, 500)
    responses = []

    for f in frequencies:
        omega = 2 * np.pi * f
        response = system.calculate_protein_resonance(omega)
        responses.append(abs(response))

    responses = np.array(responses)

    # Plot resonance
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(frequencies, responses, 'b-', linewidth=2)
    ax.axvline(system.config.f0, color='r', linestyle='--', linewidth=2,
               label=f'f₀ = {system.config.f0:.1f} Hz')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('|Response Amplitude|')
    ax.set_title('Protein Domain Resonance (Coupled Oscillator Model)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('fluorescence_demo_resonance.png', dpi=150, bbox_inches='tight')
    print("✅ Saved resonance plot to 'fluorescence_demo_resonance.png'")
    plt.close()

    # Report peak location
    peak_freq = frequencies[np.argmax(responses)]
    print(f"\nResonance peak at: {peak_freq:.2f} Hz")
    print(f"Expected (f₀): {system.config.f0:.2f} Hz")
    print(f"Deviation: {abs(peak_freq - system.config.f0):.2f} Hz")


def main():
    """Run all demonstration scripts."""
    print("\n" + "🧬 " * 35)
    print("VIBRATIONAL FLUORESCENCE MEASUREMENT SYSTEM")
    print("QCAL Validation Framework - Demo Suite")
    print("🧬 " * 35 + "\n")

    # Set random seed for reproducibility
    np.random.seed(42)

    # Run demos
    try:
        # Demo 1: Basic experiment
        results = demo_basic_experiment()

        # Demo 2: Signal generation
        demo_signal_generation()

        # Demo 3: Frequency response
        demo_frequency_response()

        # Demo 4: Time series
        demo_time_series()

        # Demo 5: Coherence analysis
        demo_coherence_analysis()

        # Demo 6: Protein resonance
        demo_protein_resonance()

        print("\n" + "="*70)
        print("🎉 ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nGenerated plots:")
        print("  • fluorescence_demo_signals.png")
        print("  • fluorescence_demo_response.png")
        print("  • fluorescence_demo_timeseries.png")
        print("  • fluorescence_demo_coherence.png")
        print("  • fluorescence_demo_resonance.png")
        print("\nFor more information, see:")
        print("  modules/quantum_biology/VIBRATIONAL_FLUORESCENCE_README.md")
        print("="*70)

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
