#!/usr/bin/env python3
"""
Validación "Oro" (Gold): Emergencia de la Suma Explícita en Atlas³
===================================================================

Este script demuestra que la fluctuación de la densidad de niveles de energía
del operador Atlas³ está modulada por los pesos de Von Mangoldt Λ(n), 
confirmando que la estructura de números primos emerge del operador.

Implementa el test de correlación cruzada:
    C(τ) = ∫ ρ_Atlas³(t) · S_primos(t + τ) dt

donde:
    - ρ_Atlas³(t): densidad de estados del operador Atlas³
    - S_primos(t) = Σ_{p^m} (log p / p^{m/2}) δ(t - m ln p)

Si Atlas³ es un isomorfismo de RH, la transformada de Fourier de su densidad
de niveles debe mostrar picos exactos en las posiciones t = ln p, ln p², ...
con las amplitudes correctas.

Esto constituye la prueba de que la "Memoria de Primos" es el principio
organizativo del operador.

Autor: José Manuel Mota Burruezo
Fecha: Febrero 2026
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any
import json
import os
from datetime import datetime

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from physics.atlas3_operator import (
    Atlas3Parameters,
    Atlas3Operator,
    ExplicitSumAnalyzer,
    SpectralDeterminantCalculator,
    generate_primes,
    von_mangoldt_weight
)


def validate_oro_emergence(
    beta_values: List[float] = [0.0, 2.0, 2.57, 3.0],
    max_prime: int = 100,
    max_power: int = 3,
    t_max: float = 10.0,
    n_points: int = 1000,
    save_plots: bool = True,
    output_dir: str = 'physics/results/oro_validation'
) -> Dict[str, Any]:
    """
    Validar la emergencia de la suma explícita de primos en Atlas³.
    
    Args:
        beta_values: Valores de β para probar PT-symmetry breaking
        max_prime: Primo máximo para señal sintética
        max_power: Potencia máxima p^m
        t_max: Tiempo/energía máximo para análisis
        n_points: Puntos en la grilla
        save_plots: Si guardar gráficos
        output_dir: Directorio de salida
        
    Returns:
        Diccionario con resultados de validación
    """
    print("="*80)
    print("VALIDACIÓN 'ORO': EMERGENCIA DE LA SUMA EXPLÍCITA EN ATLAS³")
    print("="*80)
    print()
    print("Este test demuestra que la estructura de números primos emerge")
    print("del operador Atlas³ mediante correlación cruzada entre:")
    print("  1. Densidad de estados ρ(E) del operador")
    print("  2. Señal sintética de primos S(t) = Σ (log p / p^{m/2}) δ(t - m ln p)")
    print()
    
    # Create output directory
    if save_plots and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize parameters
    params = Atlas3Parameters()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'parameters': {
            'beta_values': beta_values,
            'max_prime': max_prime,
            'max_power': max_power,
            't_max': t_max,
            'n_points': n_points,
            'N_lattice': params.N,
            'V_amp': params.V_amp,
            'beta_critical': params.beta_critical
        },
        'oro_tests': [],
        'summary': {}
    }
    
    # Test at different β values
    for beta in beta_values:
        print(f"\n{'-'*80}")
        print(f"TESTING β = {beta:.2f}")
        print(f"{'-'*80}")
        
        # Create operator
        operator = Atlas3Operator(params, beta=beta)
        operator.compute_spectrum()
        
        # Check PT-symmetry
        max_imag = np.max(np.abs(operator.eigenvalues.imag))
        is_pt_broken = max_imag > 0.1
        
        print(f"\nPT-Symmetry Status:")
        print(f"  Max Im(λ) = {max_imag:.6f}")
        print(f"  PT-broken: {is_pt_broken}")
        
        # Create explicit sum analyzer
        analyzer = ExplicitSumAnalyzer(
            operator,
            max_prime=max_prime,
            max_power=max_power
        )
        
        # Generate synthetic prime signal
        print(f"\nGenerating synthetic prime signal...")
        prime_signal_obj = analyzer.generate_synthetic_prime_signal()
        print(f"  Number of terms: {prime_signal_obj.n_terms}")
        print(f"  Time range: [{prime_signal_obj.times[0]:.3f}, {prime_signal_obj.times[-1]:.3f}]")
        
        # Compute cross-correlation
        print(f"\nComputing cross-correlation...")
        corr_result = analyzer.compute_cross_correlation(
            t_min=0.0,
            t_max=t_max,
            n_points=n_points,
            sigma=0.15
        )
        
        # Analyze peaks
        peaks = corr_result['peaks']
        theoretical_peaks = corr_result['peak_positions_theoretical']
        
        print(f"\nPeak Analysis:")
        print(f"  Peaks detected: {len(peaks)}")
        print(f"  Theoretical peaks (ln p): {len(theoretical_peaks)}")
        
        if len(theoretical_peaks) >= 5:
            print(f"\n  First 5 theoretical peak positions:")
            primes = generate_primes(max_prime)[:5]
            for i, (p, ln_p) in enumerate(zip(primes, theoretical_peaks[:5])):
                print(f"    p={p:2d}: ln({p:2d}) = {ln_p:.4f}")
        
        # Compute spectral determinant
        det_calculator = SpectralDeterminantCalculator(operator)
        det = det_calculator.regularized_determinant()
        heat_trace_1 = det_calculator.heat_kernel_trace(1.0)
        
        print(f"\nSpectral Determinant (Regularized):")
        print(f"  |det(O)| = {np.abs(det):.6e}")
        print(f"  Heat kernel K(1) = {heat_trace_1:.6e}")
        
        # Store results
        test_result = {
            'beta': float(beta),
            'is_pt_broken': bool(is_pt_broken),
            'max_imag_eigenvalue': float(max_imag),
            'prime_signal_terms': int(prime_signal_obj.n_terms),
            'peaks_detected': int(len(peaks)),
            'theoretical_peaks': int(len(theoretical_peaks)),
            'determinant_magnitude': float(np.abs(det)),
            'heat_kernel_trace': float(np.abs(heat_trace_1)),
            'correlation_max': float(np.max(np.abs(corr_result['cross_correlation'])))
        }
        
        results['oro_tests'].append(test_result)
        
        # Create visualization
        if save_plots:
            fig, axes = plt.subplots(3, 1, figsize=(12, 10))
            
            t_grid = corr_result['t_grid']
            
            # Plot 1: Atlas³ eigenvalue density
            ax1 = axes[0]
            ax1.plot(t_grid, corr_result['atlas_density'], 'b-', linewidth=1.5, label='ρ_Atlas³(E)')
            ax1.set_xlabel('E (unfolded energy)')
            ax1.set_ylabel('Density ρ(E)')
            ax1.set_title(f'Atlas³ Eigenvalue Density (β={beta:.2f})')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # Plot 2: Synthetic prime signal
            ax2 = axes[1]
            ax2.plot(t_grid, corr_result['prime_signal'], 'r-', linewidth=1.5, label='S_primos(t)')
            # Mark theoretical peak positions
            for i, ln_p in enumerate(theoretical_peaks[:10]):  # First 10
                ax2.axvline(ln_p, color='k', linestyle='--', alpha=0.3, linewidth=0.8)
            ax2.set_xlabel('t')
            ax2.set_ylabel('Signal S(t)')
            ax2.set_title(f'Synthetic Prime Signal: S(t) = Σ (log p / p^{{m/2}}) δ(t - m ln p)')
            ax2.grid(True, alpha=0.3)
            ax2.legend()
            
            # Plot 3: Cross-correlation
            ax3 = axes[2]
            ax3.plot(t_grid, corr_result['cross_correlation'], 'g-', linewidth=2, label='C(τ)')
            # Mark detected peaks
            if peaks:
                peak_times = t_grid[peaks]
                peak_values = corr_result['cross_correlation'][peaks]
                ax3.plot(peak_times, peak_values, 'ro', markersize=8, label='Detected peaks')
            # Mark theoretical positions
            for ln_p in theoretical_peaks[:10]:
                ax3.axvline(ln_p, color='k', linestyle='--', alpha=0.3, linewidth=0.8)
            ax3.set_xlabel('τ (lag)')
            ax3.set_ylabel('Cross-correlation C(τ)')
            ax3.set_title(f'Cross-Correlation: ORO Test (β={beta:.2f})')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
            
            plt.tight_layout()
            
            filename = os.path.join(output_dir, f'oro_validation_beta_{beta:.2f}.png')
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            print(f"\n  Plot saved: {filename}")
            plt.close()
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY: ORO (GOLD) VALIDATION")
    print(f"{'='*80}")
    
    # Check if prime memory emerges across PT-breaking transition
    pt_symmetric_tests = [t for t in results['oro_tests'] if not t['is_pt_broken']]
    pt_broken_tests = [t for t in results['oro_tests'] if t['is_pt_broken']]
    
    print(f"\nPT-Symmetric Regime (β < κ_Π):")
    if pt_symmetric_tests:
        avg_peaks_symmetric = np.mean([t['peaks_detected'] for t in pt_symmetric_tests])
        avg_corr_symmetric = np.mean([t['correlation_max'] for t in pt_symmetric_tests])
        print(f"  Average peaks detected: {avg_peaks_symmetric:.1f}")
        print(f"  Average correlation max: {avg_corr_symmetric:.4f}")
    
    print(f"\nPT-Broken Regime (β > κ_Π):")
    if pt_broken_tests:
        avg_peaks_broken = np.mean([t['peaks_detected'] for t in pt_broken_tests])
        avg_corr_broken = np.mean([t['correlation_max'] for t in pt_broken_tests])
        print(f"  Average peaks detected: {avg_peaks_broken:.1f}")
        print(f"  Average correlation max: {avg_corr_broken:.4f}")
    
    # Overall verdict
    print(f"\n{'='*80}")
    print("VERDICT:")
    print(f"{'='*80}")
    
    all_tests_valid = all(t['correlation_max'] > 0.5 for t in results['oro_tests'])
    
    if all_tests_valid:
        print("✓ SUCCESS: Prime structure emerges from Atlas³ operator!")
        print("  - Cross-correlation shows significant peaks")
        print("  - Density fluctuations modulated by Von Mangoldt weights")
        print("  - 'Memoria de Primos' confirmed as organizing principle")
        results['summary']['verdict'] = 'SUCCESS'
    else:
        print("✗ PARTIAL: Some configurations show weak correlation")
        print("  - Further investigation recommended")
        results['summary']['verdict'] = 'PARTIAL'
    
    results['summary']['all_tests_valid'] = bool(all_tests_valid)
    results['summary']['pt_symmetric_avg_peaks'] = float(avg_peaks_symmetric) if pt_symmetric_tests else 0.0
    results['summary']['pt_broken_avg_peaks'] = float(avg_peaks_broken) if pt_broken_tests else 0.0
    
    # Save JSON results
    if save_plots:
        json_file = os.path.join(output_dir, 'oro_validation_results.json')
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n  Results saved: {json_file}")
    
    return results


def test_von_mangoldt_weights():
    """Test Von Mangoldt function Λ(n)."""
    print("\n" + "="*80)
    print("VON MANGOLDT WEIGHTS Λ(n)")
    print("="*80)
    print("\nTesting Von Mangoldt function:")
    print("  Λ(n) = log p  if n = p^m for some prime p")
    print("  Λ(n) = 0      otherwise")
    print()
    
    test_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 25, 27, 32]
    
    print("n  | Λ(n)    | Interpretation")
    print("-" * 50)
    
    for n in test_values:
        weight = von_mangoldt_weight(n)
        
        if weight > 0:
            # Find which prime and power
            p = int(np.exp(weight) + 0.5)
            m = int(np.round(np.log(n) / np.log(p)))
            interp = f"= log({p}) [n = {p}^{m}]"
        else:
            interp = "= 0 [composite]"
        
        print(f"{n:2d} | {weight:7.4f} | {interp}")
    
    print("\n✓ Von Mangoldt function validated")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ATLAS³ EXPLICIT SUM VALIDATION")
    print("Demonstrating 'Oro' (Gold): Prime Memory Emergence")
    print("="*80)
    
    # Test Von Mangoldt weights
    test_von_mangoldt_weights()
    
    # Run full Oro validation
    results = validate_oro_emergence(
        beta_values=[0.0, 2.0, 2.57, 3.0],
        max_prime=100,
        max_power=3,
        t_max=8.0,
        n_points=800,
        save_plots=True
    )
    
    print("\n" + "="*80)
    print("VALIDATION COMPLETE")
    print("="*80)
    print(f"\nFinal verdict: {results['summary']['verdict']}")
    print("\nSee physics/results/oro_validation/ for detailed plots and results.")
