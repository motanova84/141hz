#!/usr/bin/env python3
"""
Standalone Frequency Validation Executable
==========================================

Demonstrates the complete dual EEG-LIGO frequency activation validation process.
This script can be run independently to validate f₀ = 141.7001 Hz detection
across both neural (EEG) and gravitational (LIGO) modalities.

Usage:
    python tests/run_frequency_validation.py [--duration DURATION] [--bootstrap]

Options:
    --duration DURATION   Data duration in seconds (default: 10.0)
    --bootstrap          Run bootstrap validation (takes longer)
    --save FILE          Save results to JSON file
    --plot              Generate visualization plots

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 11, 2026
Framework: QCAL ∞³
"""

import sys
import argparse
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from experiments.frequency_activation_validator import (
    DualSystemValidator,
    F0_HZ
)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Run dual EEG-LIGO frequency activation validation'
    )
    
    parser.add_argument(
        '--duration',
        type=float,
        default=10.0,
        help='Data duration in seconds (default: 10.0)'
    )
    
    parser.add_argument(
        '--bootstrap',
        action='store_true',
        help='Run bootstrap validation (slower but more robust)'
    )
    
    parser.add_argument(
        '--save',
        type=str,
        default=None,
        help='Save results to JSON file'
    )
    
    parser.add_argument(
        '--plot',
        action='store_true',
        help='Generate visualization plots'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress detailed output'
    )
    
    return parser.parse_args()


def print_header(quiet=False):
    """Print script header."""
    if quiet:
        return
    
    print("=" * 80)
    print("DUAL EEG-LIGO FREQUENCY ACTIVATION VALIDATION")
    print("=" * 80)
    print(f"\nTarget Frequency: f₀ = {F0_HZ} Hz")
    print("Consciousness Activation Frequency (QCAL ∞³)")
    print()


def run_validation(duration, run_bootstrap, quiet=False):
    """
    Run the validation.
    
    Parameters
    ----------
    duration : float
        Data duration (seconds)
    run_bootstrap : bool
        Whether to run bootstrap validation
    quiet : bool
        Suppress output
    
    Returns
    -------
    dict
        Validation results
    """
    if not quiet:
        print(f"Initializing dual system validator...")
        print(f"Duration: {duration:.1f} seconds")
        print(f"Bootstrap validation: {'enabled' if run_bootstrap else 'disabled'}")
        print()
    
    # Create validator
    validator = DualSystemValidator()
    
    if not quiet:
        print("Generating synthetic data and running analysis...")
        if run_bootstrap:
            print("(Bootstrap validation may take several minutes)")
        print()
    
    # Run validation
    results = validator.validate(duration=duration, run_bootstrap=run_bootstrap)
    
    if not quiet:
        print("Validation complete!")
        print()
    
    return results


def save_results(results, filename):
    """
    Save results to JSON file.
    
    Parameters
    ----------
    results : dict
        Validation results
    filename : str
        Output filename
    """
    # Prepare results for JSON (remove non-serializable items)
    results_serializable = {
        'EEG': results['EEG'],
        'LIGO': results['LIGO'],
        'cross_system': results['cross_system'],
        'validation_summary': results['validation_summary']
    }
    
    if 'bootstrap' in results:
        # Convert bootstrap results (remove numpy arrays if present)
        results_serializable['bootstrap'] = {
            'EEG': {k: v for k, v in results['bootstrap']['EEG'].items()},
            'LIGO': {k: v for k, v in results['bootstrap']['LIGO'].items()}
        }
    
    with open(filename, 'w') as f:
        json.dump(results_serializable, f, indent=2)
    
    print(f"Results saved to: {filename}")


def plot_results(results):
    """
    Generate visualization plots.
    
    Parameters
    ----------
    results : dict
        Validation results
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Warning: matplotlib not available, skipping plots")
        return
    
    print("Generating plots...")
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Dual EEG-LIGO Validation: f₀ = {F0_HZ} Hz', fontsize=14, fontweight='bold')
    
    # Plot 1: Detection frequencies
    ax = axes[0, 0]
    systems = ['EEG', 'LIGO']
    freqs = [results['EEG']['frequency'], results['LIGO']['frequency']]
    colors = ['blue' if results['EEG']['status'] == '✅' else 'red',
              'green' if results['LIGO']['status'] == '✅' else 'red']
    
    ax.bar(systems, freqs, color=colors, alpha=0.7)
    ax.axhline(y=F0_HZ, color='red', linestyle='--', label=f'Target (f₀ = {F0_HZ} Hz)')
    ax.set_ylabel('Detected Frequency (Hz)')
    ax.set_title('Peak Frequency Detection')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Plot 2: SNR comparison
    ax = axes[0, 1]
    snrs = [results['EEG']['snr_db'], results['LIGO']['snr_db']]
    ax.bar(systems, snrs, color=['blue', 'green'], alpha=0.7)
    ax.set_ylabel('SNR (dB)')
    ax.set_title('Signal-to-Noise Ratio')
    ax.grid(axis='y', alpha=0.3)
    
    # Plot 3: Coherence
    ax = axes[1, 0]
    coherences = [results['EEG']['coherence'], results['LIGO']['coherence']]
    ax.bar(systems, coherences, color=['blue', 'green'], alpha=0.7)
    ax.set_ylabel('Coherence')
    ax.set_ylim([0, 1])
    ax.set_title('Phase Coherence')
    ax.axhline(y=0.7, color='orange', linestyle='--', label='Min threshold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Plot 4: Validation summary
    ax = axes[1, 1]
    summary = results['validation_summary']
    metrics = ['EEG\nDetection', 'LIGO\nDetection', 'Cross\nValidation', 'Overall\nSuccess']
    values = [
        1.0 if summary['f0_detected_eeg'] else 0.0,
        1.0 if summary['f0_detected_ligo'] else 0.0,
        1.0 if summary['cross_validated'] else 0.0,
        1.0 if summary['overall_success'] else 0.0
    ]
    colors_summary = ['green' if v > 0.5 else 'red' for v in values]
    
    ax.bar(metrics, values, color=colors_summary, alpha=0.7)
    ax.set_ylabel('Pass/Fail')
    ax.set_ylim([0, 1.2])
    ax.set_title('Validation Summary')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Fail', 'Pass'])
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    output_file = 'frequency_activation_validation.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Plot saved to: {output_file}")
    
    # Show plot
    try:
        plt.show()
    except:
        pass  # In case display is not available


def print_summary(results):
    """
    Print validation summary.
    
    Parameters
    ----------
    results : dict
        Validation results
    """
    vs = results['validation_summary']
    
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    if vs['overall_success']:
        print("\n✅ VALIDATION SUCCESSFUL!")
        print(f"\nf₀ = {F0_HZ} Hz detected in both EEG and LIGO systems")
        print("Cross-system validation confirms consciousness activation frequency")
    else:
        print("\n❌ VALIDATION INCOMPLETE")
        print("\nOne or more validation criteria not met:")
        
        if not vs['f0_detected_eeg']:
            print("  - f₀ not detected in EEG system")
        if not vs['f0_detected_ligo']:
            print("  - f₀ not detected in LIGO system")
        if not vs['cross_validated']:
            print("  - Cross-system correlation below threshold")
    
    print("\nDetailed Results:")
    print(f"  EEG frequency:  {results['EEG']['frequency']:.2f} Hz (target: {F0_HZ} Hz)")
    print(f"  LIGO frequency: {results['LIGO']['frequency']:.2f} Hz (target: {F0_HZ} Hz)")
    print(f"  Cross-correlation: r = {results['cross_system']['correlation']:.3f}")
    
    print("\n" + "=" * 80)


def main():
    """Main execution."""
    args = parse_arguments()
    
    # Print header
    print_header(quiet=args.quiet)
    
    # Run validation
    results = run_validation(
        duration=args.duration,
        run_bootstrap=args.bootstrap,
        quiet=args.quiet
    )
    
    # Print full report
    if not args.quiet:
        validator = DualSystemValidator()
        validator.print_report(results)
    
    # Print summary
    print_summary(results)
    
    # Save results if requested
    if args.save:
        save_results(results, args.save)
    
    # Generate plots if requested
    if args.plot:
        plot_results(results)
    
    # Return success/failure
    success = results['validation_summary']['overall_success']
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
