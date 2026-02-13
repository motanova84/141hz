#!/usr/bin/env python3
"""
VALIDACIÓN: FASE III - GEOMETRÍA EMERGENTE
Validation of emergent geometry from consciousness coherence

This script validates the theoretical predictions:
1. Tensor symmetry G_μν = G_νμ
2. Optimal coherence at Ψ = 0.888: trace(G) < 10^-6
3. Boundary behaviors: Ψ→1 (flat), Ψ→0 (trap)
4. Master node coherence at 888 Hz
5. Gravity as coherence deficit mechanism

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.geometria_emergente import GeometriaEmergente, PSI_OPTIMAL, FREQUENCY_MASTER


class ValidadorGeometriaEmergente:
    """Validator for emergent geometry predictions."""
    
    def __init__(self, precision: int = 50):
        """Initialize validator with specified precision."""
        self.geo = GeometriaEmergente(precision=precision)
        self.results = {}
        
    def validate_tensor_symmetry(self) -> bool:
        """
        Validate that G_μν = G_νμ (tensor symmetry).
        
        Returns:
        --------
        bool
            True if tensor is symmetric within numerical tolerance
        """
        print("\n" + "=" * 80)
        print("VALIDATION 1: Tensor Symmetry G_μν = G_νμ")
        print("=" * 80)
        
        # Test at multiple coherence values
        psi_test = [0.1, 0.5, PSI_OPTIMAL, 0.95]
        all_symmetric = True
        
        for psi in psi_test:
            result = self.geo.einstein_tensor(psi)
            G = result['G_muv']
            
            # Check symmetry
            symmetric = np.allclose(G, G.T, rtol=1e-10, atol=1e-15)
            max_asymmetry = np.max(np.abs(G - G.T))
            
            print(f"Ψ = {psi:.3f}: Symmetric = {symmetric}, "
                  f"Max |G_μν - G_νμ| = {max_asymmetry:.2e}")
            
            all_symmetric = all_symmetric and symmetric
        
        self.results['symmetry'] = all_symmetric
        print(f"\n✓ RESULT: All tensors symmetric = {all_symmetric}")
        return all_symmetric
    
    def validate_optimal_coherence(self) -> bool:
        """
        Validate minimal fertile curvature at Ψ = 0.888.
        
        Requirement: trace(G) < 10^-6 at optimal coherence
        
        Returns:
        --------
        bool
            True if trace bound is satisfied
        """
        print("\n" + "=" * 80)
        print("VALIDATION 2: Optimal Coherence Ψ = 0.888")
        print("=" * 80)
        
        result = self.geo.einstein_tensor(PSI_OPTIMAL)
        trace_G = result['trace_G']
        
        print(f"Coherence: Ψ = {PSI_OPTIMAL}")
        print(f"Master frequency: f = {FREQUENCY_MASTER} Hz")
        print(f"Trace(G): {trace_G:.2e}")
        print(f"Requirement: |trace(G)| < 10^-6")
        
        satisfied = np.abs(trace_G) < 1e-6
        
        self.results['optimal_trace'] = {
            'trace': trace_G,
            'satisfied': satisfied
        }
        
        print(f"\n✓ RESULT: Requirement satisfied = {satisfied}")
        return satisfied
    
    def validate_boundary_behaviors(self) -> Dict[str, bool]:
        """
        Validate tensor behaviors at coherence boundaries.
        
        Requirements:
        - Ψ → 1: G_μν → 0 (flat unity)
        - Ψ → 0: G_μν → ∞ (gravitational trap)
        
        Returns:
        --------
        dict
            Validation results for each boundary
        """
        print("\n" + "=" * 80)
        print("VALIDATION 3: Boundary Behaviors")
        print("=" * 80)
        
        # Test Ψ → 1 (flat unity)
        print("\nBoundary 1: Ψ → 1 (Perfect Coherence → Flat Space)")
        print("-" * 80)
        psi_near_unity = [0.9, 0.95, 0.99, 0.999]
        norms_unity = []
        
        for psi in psi_near_unity:
            result = self.geo.einstein_tensor(psi)
            norm_G = np.linalg.norm(result['G_muv'])
            norms_unity.append(norm_G)
            print(f"Ψ = {psi:.3f}: ||G_μν|| = {norm_G:.2e}")
        
        # Check monotonic decrease toward zero
        decreasing_to_zero = all(norms_unity[i] > norms_unity[i+1] 
                                 for i in range(len(norms_unity)-1))
        near_zero = norms_unity[-1] < 1e-40
        
        print(f"Monotonic decrease: {decreasing_to_zero}")
        print(f"Near zero at Ψ=0.999: {near_zero}")
        
        # Test Ψ → 0 (gravitational trap)
        print("\nBoundary 2: Ψ → 0 (Zero Coherence → Gravitational Trap)")
        print("-" * 80)
        psi_near_zero = [0.1, 0.05, 0.01, 0.001]
        norms_trap = []
        
        for psi in psi_near_zero:
            result = self.geo.einstein_tensor(psi)
            norm_G = np.linalg.norm(result['G_muv'])
            norms_trap.append(norm_G)
            print(f"Ψ = {psi:.3f}: ||G_μν|| = {norm_G:.2e}")
        
        # Check monotonic increase toward infinity
        increasing_to_inf = all(norms_trap[i] < norms_trap[i+1] 
                               for i in range(len(norms_trap)-1))
        very_large = norms_trap[-1] > 1e30
        
        print(f"Monotonic increase: {increasing_to_inf}")
        print(f"Very large at Ψ=0.001: {very_large}")
        
        boundaries_valid = {
            'flat_unity': decreasing_to_zero and near_zero,
            'gravitational_trap': increasing_to_inf and very_large
        }
        
        self.results['boundaries'] = boundaries_valid
        
        print(f"\n✓ RESULT: Flat unity = {boundaries_valid['flat_unity']}, "
              f"Gravitational trap = {boundaries_valid['gravitational_trap']}")
        
        return boundaries_valid
    
    def validate_master_node(self) -> bool:
        """
        Validate master node coherence at 888 Hz.
        
        Checks:
        - Distributed coherence at Ψ = 0.888
        - Stable tensor configuration
        - Minimal fertile curvature
        
        Returns:
        --------
        bool
            True if master node is valid
        """
        print("\n" + "=" * 80)
        print("VALIDATION 4: Master Node @ 888 Hz")
        print("=" * 80)
        
        master = self.geo.compute_master_node_coherence()
        
        print(f"Coherence: Ψ = {master['psi']}")
        print(f"Frequency: f = {master['frequency']} Hz")
        print(f"State: {master['interpretation']['state']}")
        print(f"Curvature: {master['interpretation']['curvature']}")
        print(f"Gravity Source: {master['interpretation']['gravity_source']}")
        print(f"Trajectory Nature: {master['interpretation']['trajectory_nature']}")
        
        # Validation checks
        checks = {
            'correct_psi': np.abs(master['psi'] - PSI_OPTIMAL) < 1e-10,
            'correct_freq': np.abs(master['frequency'] - FREQUENCY_MASTER) < 1e-6,
            'symmetric': master['validation']['symmetric'],
            'trace_bound': master['validation']['trace_optimal']
        }
        
        all_valid = all(checks.values())
        
        print(f"\nValidation checks:")
        for key, value in checks.items():
            print(f"  {key}: {value}")
        
        self.results['master_node'] = checks
        
        print(f"\n✓ RESULT: Master node valid = {all_valid}")
        return all_valid
    
    def validate_coherence_deficit_mechanism(self) -> bool:
        """
        Validate that gravity emerges from coherence deficit.
        
        Theory: dG/dΨ < 0 (curvature increases as coherence decreases)
        
        Returns:
        --------
        bool
            True if mechanism is validated
        """
        print("\n" + "=" * 80)
        print("VALIDATION 5: Gravity as Coherence Deficit")
        print("=" * 80)
        
        # Compute gradient dG/dΨ numerically
        psi_values = np.linspace(0.1, 0.99, 20)
        norms = []
        
        for psi in psi_values:
            result = self.geo.einstein_tensor(psi)
            norm = np.linalg.norm(result['G_muv'])
            norms.append(norm)
        
        # Compute numerical derivative
        d_norm_d_psi = np.gradient(norms, psi_values)
        
        # Check that derivative is negative (gravity increases as coherence decreases)
        all_negative = np.all(d_norm_d_psi < 0)
        
        print(f"Coherence range: Ψ ∈ [{psi_values[0]:.2f}, {psi_values[-1]:.2f}]")
        print(f"d||G||/dΨ < 0 everywhere: {all_negative}")
        print(f"Mean gradient: {np.mean(d_norm_d_psi):.2e}")
        print(f"Interpretation: Gravity INCREASES as coherence DECREASES ✓")
        
        self.results['coherence_deficit'] = all_negative
        
        print(f"\n✓ RESULT: Coherence deficit mechanism validated = {all_negative}")
        return all_negative
    
    def generate_validation_report(self) -> Dict:
        """
        Generate comprehensive validation report.
        
        Returns:
        --------
        dict
            Complete validation results
        """
        print("\n" + "=" * 80)
        print("VALIDATION REPORT: FASE III - GEOMETRÍA EMERGENTE")
        print("=" * 80)
        
        # Count validations
        total_tests = 0
        passed_tests = 0
        
        for key, value in self.results.items():
            if isinstance(value, bool):
                total_tests += 1
                if value:
                    passed_tests += 1
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, bool):
                        total_tests += 1
                        if subvalue:
                            passed_tests += 1
        
        print(f"\nTests passed: {passed_tests}/{total_tests}")
        print(f"Success rate: {100*passed_tests/total_tests:.1f}%")
        
        # Overall assessment
        all_passed = (passed_tests == total_tests)
        
        if all_passed:
            print("\n✓✓✓ ALL VALIDATIONS PASSED ✓✓✓")
            print("\nFASE III ACTIVATED:")
            print("- Tensor gnosis stable at Ψ = 0.888")
            print("- Einstein-QCAL ∞³ bridge resolved")
            print("- Gravity as coherence deficit confirmed")
            print("- Master node 888 Hz operational")
            print("- Distributed coherence manifest")
        else:
            print("\n✗ SOME VALIDATIONS FAILED")
            print("Review failed tests above")
        
        return {
            'tests_passed': passed_tests,
            'tests_total': total_tests,
            'success_rate': passed_tests / total_tests,
            'all_passed': all_passed,
            'details': self.results
        }
    
    def visualize_coherence_landscape(self, save_path: str = None):
        """
        Visualize the coherence landscape G_μν(Ψ).
        
        Parameters:
        -----------
        save_path : str, optional
            Path to save figure
        """
        print("\n" + "=" * 80)
        print("VISUALIZATION: Coherence Landscape")
        print("=" * 80)
        
        # Scan coherence landscape
        psi_values = np.linspace(0.01, 0.999, 100)
        trace_G = []
        norm_G = []
        kappa_pi = []
        
        for psi in psi_values:
            result = self.geo.einstein_tensor(psi)
            trace_G.append(result['trace_G'])
            norm_G.append(np.linalg.norm(result['G_muv']))
            kappa_pi.append(result['kappa_pi'])
        
        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('FASE III: Geometría Emergente - Coherence Landscape', 
                     fontsize=16, fontweight='bold')
        
        # Plot 1: Trace(G) vs Ψ
        ax1 = axes[0, 0]
        ax1.semilogy(psi_values, np.abs(trace_G), 'b-', linewidth=2, label='|trace(G)|')
        ax1.axvline(PSI_OPTIMAL, color='r', linestyle='--', linewidth=2, 
                   label=f'Ψ = {PSI_OPTIMAL} (Master Node)')
        ax1.axhline(1e-6, color='g', linestyle=':', linewidth=2, label='Trace < 10⁻⁶')
        ax1.set_xlabel('Coherence Ψ', fontsize=12)
        ax1.set_ylabel('|trace(G)|', fontsize=12)
        ax1.set_title('Curvature Trace vs Coherence')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: ||G|| vs Ψ
        ax2 = axes[0, 1]
        ax2.semilogy(psi_values, norm_G, 'b-', linewidth=2, label='||G_μν||')
        ax2.axvline(PSI_OPTIMAL, color='r', linestyle='--', linewidth=2,
                   label=f'Ψ = {PSI_OPTIMAL}')
        ax2.set_xlabel('Coherence Ψ', fontsize=12)
        ax2.set_ylabel('||G_μν||', fontsize=12)
        ax2.set_title('Tensor Norm vs Coherence')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: κ_Π vs Ψ
        ax3 = axes[1, 0]
        ax3.semilogy(psi_values, kappa_pi, 'b-', linewidth=2, label='κ_Π(Ψ)')
        ax3.axvline(PSI_OPTIMAL, color='r', linestyle='--', linewidth=2,
                   label=f'Ψ = {PSI_OPTIMAL}')
        ax3.set_xlabel('Coherence Ψ', fontsize=12)
        ax3.set_ylabel('κ_Π (m/J)', fontsize=12)
        ax3.set_title('Gravitational Coupling vs Coherence')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Phase diagram
        ax4 = axes[1, 1]
        
        # Define regions
        psi_flat = psi_values[psi_values > 0.95]
        psi_fertile = psi_values[(psi_values >= 0.7) & (psi_values <= 0.95)]
        psi_trap = psi_values[psi_values < 0.7]
        
        ax4.axhspan(0.95, 1.0, alpha=0.3, color='green', label='Flat Unity')
        ax4.axhspan(0.7, 0.95, alpha=0.3, color='yellow', label='Fertile Curvature')
        ax4.axhspan(0.0, 0.7, alpha=0.3, color='red', label='Gravitational Trap')
        ax4.axhline(PSI_OPTIMAL, color='blue', linestyle='-', linewidth=3,
                   label=f'Master Node Ψ = {PSI_OPTIMAL}')
        
        ax4.set_ylim(0, 1)
        ax4.set_xlim(0, 1)
        ax4.set_ylabel('Coherence Ψ', fontsize=12)
        ax4.set_title('Coherence Phase Diagram')
        ax4.legend(loc='right')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Figure saved to: {save_path}")
        
        plt.show()
        
        return fig
    
    def run_full_validation(self, visualize: bool = True) -> Dict:
        """
        Run complete validation suite.
        
        Parameters:
        -----------
        visualize : bool
            Whether to generate visualization
            
        Returns:
        --------
        dict
            Complete validation report
        """
        print("\n" + "=" * 80)
        print("FASE III: GEOMETRÍA EMERGENTE - FULL VALIDATION SUITE")
        print("=" * 80)
        
        # Run all validations
        self.validate_tensor_symmetry()
        self.validate_optimal_coherence()
        self.validate_boundary_behaviors()
        self.validate_master_node()
        self.validate_coherence_deficit_mechanism()
        
        # Generate report
        report = self.generate_validation_report()
        
        # Visualize if requested
        if visualize:
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
            os.makedirs(output_dir, exist_ok=True)
            save_path = os.path.join(output_dir, 'geometria_emergente_validation.png')
            self.visualize_coherence_landscape(save_path)
        
        return report


def main():
    """Run validation suite."""
    validator = ValidadorGeometriaEmergente(precision=50)
    report = validator.run_full_validation(visualize=True)
    
    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print(f"Success rate: {100*report['success_rate']:.1f}%")
    
    return report


if __name__ == "__main__":
    main()
