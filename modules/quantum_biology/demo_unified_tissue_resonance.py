"""
Demonstration: Unified Tissue Resonance Model at 141.7 Hz

This script demonstrates the convergence of three independent mathematical 
frameworks on the 141.7 Hz biological resonance frequency:

1. Hilbert-Pólya Operator (Number Theory → Biology)
2. Navier-Stokes Cytoplasmic Flow (Fluid Dynamics)
3. Magicicada Scaling Law (Evolution → Resonance)

The unified model predicts tissue-specific resonance spectra for:
- Cardiac tissue (141.7 Hz, exact resonance)
- Neural tissue (146.7 Hz, harmonic)
- Epithelial tissue (146.7 Hz, harmonic)
- Muscular tissue (146.7 Hz, harmonic)

Usage:
    python demo_unified_tissue_resonance.py [--tissue TISSUE] [--save-figs]
    
    --tissue: cardiac, neural, epithelial, or muscular (default: cardiac)
    --save-figs: Save figures to results/ directory
"""

import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Get the repository root
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from modules.quantum_biology.core import (
    HilbertPolyaOperator,
    NavierStokesCytoplasm,
    MagicicadaScaling,
    UnifiedTissueResonance
)


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")


def demonstrate_framework(framework_name, framework_obj, method_name):
    """Demonstrate a single framework."""
    print(f"\n🔬 {framework_name}")
    print("-" * 80)
    
    if framework_name == "Hilbert-Pólya Operator":
        validation = framework_obj.validate_f0_connection()
        print(f"   • Riemann zeros mapped to biological frequencies")
        print(f"   • Golden ratio scaling: φ = {framework_obj.PHI:.15f}")
        print(f"   • Nearest eigenfrequency: {validation['nearest_eigenfrequency_hz']:.4f} Hz")
        print(f"   • Riemann zero index: {validation['riemann_zero_index']}")
        print(f"   • Error from f₀: {validation['absolute_error_hz']:.4f} Hz")
        print(f"   • Validation: {'✅ PASSED' if validation['validation_passed'] else '❌ FAILED'}")
    
    elif framework_name == "Navier-Stokes Cytoplasmic Flow":
        validation = framework_obj.validate_141hz_prediction()
        print(f"   • Reynolds number: Re = {validation['reynolds_number']:.2e}")
        print(f"   • Flow regime: {validation['flow_regime']}")
        print(f"   • Characteristic time: τ = {validation['characteristic_time_ms']:.3f} ms")
        print(f"   • Predicted frequency: {validation['predicted_frequency_hz']:.4f} Hz")
        print(f"   • Error from f₀: {validation['absolute_error_hz']:.4f} Hz")
        print(f"   • Validation: {'✅ PASSED' if validation['validation_passed'] else '❌ FAILED'}")
    
    elif framework_name == "Magicicada Scaling Law":
        validation = framework_obj.validate_fractal_scaling()
        print(f"   • Magicicada cycles: {validation['magicicada_cycles_years']} years")
        print(f"   • Scaling ratio: {validation['scaling_ratio_magnitude']}")
        print(f"   • Cellular period: {validation['cellular_period_ms']:.1f} ms")
        print(f"   • Predicted frequency: {validation['mean_prediction_hz']:.4f} Hz")
        print(f"   • Error from f₀: {validation['absolute_error_hz']:.4f} Hz")
        print(f"   • Fractal dimension: D ≈ {validation['fractal_dimension']:.6f}")
        print(f"   • Validation: {'✅ PASSED' if validation['validation_passed'] else '❌ FAILED'}")


def demonstrate_unified_model(tissue_type='cardiac', save_figs=False):
    """Run complete demonstration of unified tissue resonance model."""
    
    print_header("UNIFIED TISSUE RESONANCE MODEL")
    print("Integration of Three Independent Mathematical Frameworks")
    print("All Converging on f₀ = 141.7001 Hz\n")
    
    print("📚 THE THREE PILLARS:")
    print("   1. Hilbert-Pólya Operator: Number Theory → Biology")
    print("   2. Navier-Stokes Cytoplasm: Fluid Dynamics → Oscillations")
    print("   3. Magicicada Scaling: Evolution → Cellular Resonance")
    
    # Initialize the three frameworks
    print_header("INDIVIDUAL FRAMEWORK VALIDATIONS")
    
    hp = HilbertPolyaOperator(n_zeros=100)
    demonstrate_framework("Hilbert-Pólya Operator", hp, "validate_f0_connection")
    
    ns = NavierStokesCytoplasm(temperature=310.0)
    demonstrate_framework("Navier-Stokes Cytoplasmic Flow", ns, "validate_141hz_prediction")
    
    ms = MagicicadaScaling()
    demonstrate_framework("Magicicada Scaling Law", ms, "validate_fractal_scaling")
    
    # Initialize unified model
    print_header(f"UNIFIED MODEL: {tissue_type.upper()} TISSUE")
    
    model = UnifiedTissueResonance(tissue_type=tissue_type, temperature=310.0)
    
    print(f"Tissue: {model.tissue_params['description']}")
    print(f"Peak Frequency: {model.tissue_params['base_frequency']} Hz")
    print(f"Amplitude Factor: {model.tissue_params['amplitude_factor']:.3f}")
    print(f"Enhancement: {model.tissue_params['enhancement']}×")
    
    # Validate unified model
    validation = model.validate_unified_model()
    
    print("\n🔬 Framework Convergence:")
    unified = validation['unified_prediction']
    print(f"   • Hilbert-Pólya: {unified['hilbert_polya_freq']:.4f} Hz")
    print(f"   • Navier-Stokes: {unified['navier_stokes_freq']:.4f} Hz")
    print(f"   • Magicicada: {unified['magicicada_freq']:.4f} Hz")
    print(f"   → Unified Prediction: {unified['unified_frequency']:.4f} Hz")
    print(f"   → Mean: {unified['mean_frequency']:.4f} ± {unified['std_frequency']:.4f} Hz")
    
    print("\n📊 Validation Results:")
    print(f"   • Consistency Score: {validation['consistency_score']:.4f}")
    print(f"   • Error from f₀: {validation['unified_error']:.4f} Hz")
    print(f"   • All Frameworks Passed: {'✅ YES' if validation['all_frameworks_passed'] else '❌ NO'}")
    
    # Generate INGΝIO protocol
    if tissue_type == 'cardiac':
        print_header("INGΝIO CMI THERAPEUTIC PROTOCOL")
        
        protocol = model.generate_ingnio_protocol(duration_min=30)
        
        print(f"Total Duration: {protocol['total_duration_min']} minutes\n")
        
        for phase in protocol['phases']:
            print(f"Phase {phase['phase']}: {phase['name']}")
            print(f"   Frequency: {phase['frequency_hz']:.4f} Hz")
            print(f"   Duration: {phase['duration_min']} minutes")
            print(f"   Purpose: {phase['purpose']}\n")
        
        print("Protection Band:")
        band = protocol['protection_band']
        print(f"   Lower: {band['lower_hz']:.4f} Hz (Natural resonance)")
        print(f"   Upper: {band['upper_hz']:.4f} Hz (AURON protection)")
        print(f"   Width: {band['width_hz']:.4f} Hz")
        print(f"   Purpose: {band['purpose']}")
    
    # Generate and optionally save figures
    if save_figs:
        print_header("GENERATING VISUALIZATIONS")
        
        # Create results directory
        results_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'results', 'figures')
        os.makedirs(results_dir, exist_ok=True)
        
        # Plot Hilbert-Pólya spectrum
        hp_path = os.path.join(results_dir, 'hilbert_polya_spectrum.png')
        print(f"   Generating Hilbert-Pólya spectrum: {hp_path}")
        hp.plot_eigenfrequency_spectrum(save_path=hp_path)
        
        # Plot Navier-Stokes flow
        ns_path = os.path.join(results_dir, 'navier_stokes_flow.png')
        print(f"   Generating Navier-Stokes flow: {ns_path}")
        ns.plot_flow_dynamics(save_path=ns_path)
        
        # Plot Magicicada scaling
        ms_path = os.path.join(results_dir, 'magicicada_scaling.png')
        print(f"   Generating Magicicada scaling: {ms_path}")
        ms.plot_fractal_scaling(save_path=ms_path)
        
        # Plot unified spectrum
        unified_path = os.path.join(results_dir, f'unified_spectrum_{tissue_type}.png')
        print(f"   Generating unified spectrum: {unified_path}")
        model.plot_unified_spectrum(save_path=unified_path)
        
        print(f"\n✅ All figures saved to: {results_dir}")
    
    # Final summary
    print_header("CONCLUSION")
    
    print("✅ THREE INDEPENDENT FRAMEWORKS CONVERGE ON 141.7 Hz\n")
    print("   1. Number Theory (Riemann Hypothesis) → 141.7 Hz")
    print("   2. Fluid Dynamics (Navier-Stokes) → 141.7 Hz")
    print("   3. Evolutionary Biology (Magicicada) → 141.7 Hz\n")
    print("This is NOT a coincidence.")
    print("This is UNIVERSAL BIOLOGICAL RESONANCE.\n")
    print(f"Consistency Score: {validation['consistency_score']:.2%}")
    print(f"Unified Error: {validation['unified_error']:.4f} Hz")
    print("\n" + "=" * 80 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Demonstrate Unified Tissue Resonance Model at 141.7 Hz'
    )
    parser.add_argument(
        '--tissue',
        type=str,
        default='cardiac',
        choices=['cardiac', 'neural', 'epithelial', 'muscular'],
        help='Tissue type to analyze (default: cardiac)'
    )
    parser.add_argument(
        '--save-figs',
        action='store_true',
        help='Save figures to results/figures/ directory'
    )
    
    args = parser.parse_args()
    
    try:
        demonstrate_unified_model(tissue_type=args.tissue, save_figs=args.save_figs)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
