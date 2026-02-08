#!/usr/bin/env python3
"""
Comprehensive Validation: Philosophical Framework for Physical Reality
=======================================================================

This script validates the implementation of the five fundamental principles
from the problem statement:

1. La masa es una ilusión de detención
2. La energía es ritmo  
3. El espacio es un intervalo entre pulsos
4. El tiempo es el número de ciclos
5. El universo es una sinfonía autocontenida

Each principle is tested with multiple scenarios to ensure correctness
and physical consistency.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 2026
Reference: QCAL ∞³ Theory - Philosophical Framework Validation
"""

import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from philosophical_framework import (
    PhilosophicalFramework,
    OscillationState,
    validate_framework
)


class PhilosophicalFrameworkValidator:
    """Comprehensive validator for the philosophical framework."""
    
    def __init__(self):
        """Initialize the validator."""
        self.framework = PhilosophicalFramework()
        self.results = {}
        self.verbose = True
        
    def print_header(self, text: str):
        """Print formatted header."""
        print("\n" + "=" * 80)
        print(text.center(80))
        print("=" * 80)
        
    def print_subheader(self, text: str):
        """Print formatted subheader."""
        print("\n" + "-" * 80)
        print(text)
        print("-" * 80)
        
    # =========================================================================
    # PRINCIPLE 1: La masa es una ilusión de detención
    # =========================================================================
    
    def validate_principle_1(self) -> Dict[str, Any]:
        """Validate Principle 1: Mass is an illusion of detention."""
        self.print_header("PRINCIPLE 1: La masa es una ilusión de detención")
        
        results = {
            'principle': 'Mass is an illusion of detention',
            'tests': [],
            'status': 'PASSED'
        }
        
        # Test 1: Complete detention (f → 0) produces maximum mass
        self.print_subheader("Test 1.1: Complete frequency detention")
        try:
            f_detained = 0.001  # Nearly stopped
            m_complete = self.framework.mass_from_frequency_reduction(f_detained)
            
            print(f"Frequency detention: f₀ = {self.framework.f0} Hz → f = {f_detained} Hz")
            print(f"Emergent mass: {m_complete:.6e} kg")
            
            assert m_complete > 0, "Complete detention should produce mass"
            
            results['tests'].append({
                'test': 'Complete detention produces mass',
                'f_detained': f_detained,
                'mass_kg': m_complete,
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Complete detention', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 2: No detention (f = f₀) produces zero mass
        self.print_subheader("Test 1.2: No detention gives zero mass")
        try:
            m_zero = self.framework.mass_from_frequency_reduction(self.framework.f0)
            
            print(f"No frequency detention: f = f₀ = {self.framework.f0} Hz")
            print(f"Emergent mass: {m_zero:.6e} kg")
            
            assert m_zero == 0, "No detention should produce zero mass"
            
            results['tests'].append({
                'test': 'No detention gives zero mass',
                'mass_kg': m_zero,
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'No detention', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 3: Mass increases with frequency reduction
        self.print_subheader("Test 1.3: Mass monotonically increases with detention")
        try:
            frequencies = np.linspace(0.1, 140, 10)
            masses = [self.framework.mass_from_frequency_reduction(f) for f in frequencies]
            
            # Check monotonic increase
            is_monotonic = all(masses[i] >= masses[i+1] for i in range(len(masses)-1))
            
            print(f"Tested {len(frequencies)} frequency points")
            print(f"Mass range: {min(masses):.6e} to {max(masses):.6e} kg")
            print(f"Monotonic increase: {is_monotonic}")
            
            assert is_monotonic, "Mass should increase as frequency decreases"
            
            results['tests'].append({
                'test': 'Monotonic mass increase with detention',
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Monotonic increase', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 4: Inverse mapping (mass → oscillation state)
        self.print_subheader("Test 1.4: Mass to oscillation state mapping")
        try:
            test_mass = 1e-30  # Test mass in kg
            osc_state = self.framework.mass_oscillation_spectrum(test_mass)
            
            print(f"Input mass: {test_mass:.6e} kg")
            print(f"Oscillation frequency: {osc_state.frequency:.4f} Hz")
            print(f"Oscillation amplitude: {osc_state.amplitude:.6e}")
            print(f"Coherence: {osc_state.coherence:.4f}")
            
            assert osc_state.frequency >= 0, "Frequency should be non-negative"
            assert osc_state.frequency <= self.framework.f0, "Frequency should not exceed f₀"
            
            results['tests'].append({
                'test': 'Mass to oscillation mapping',
                'mass_kg': test_mass,
                'frequency_hz': osc_state.frequency,
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Mass to oscillation', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        return results
    
    # =========================================================================
    # PRINCIPLE 2: La energía es ritmo
    # =========================================================================
    
    def validate_principle_2(self) -> Dict[str, Any]:
        """Validate Principle 2: Energy is rhythm."""
        self.print_header("PRINCIPLE 2: La energía es ritmo")
        
        results = {
            'principle': 'Energy is rhythm',
            'tests': [],
            'status': 'PASSED'
        }
        
        # Test 1: Energy from fundamental frequency
        self.print_subheader("Test 2.1: Energy from fundamental rhythm")
        try:
            E_fundamental = self.framework.energy_from_rhythm(self.framework.f0)
            
            print(f"Fundamental frequency: f₀ = {self.framework.f0} Hz")
            print(f"Quantum energy: {E_fundamental:.6e} J")
            
            assert E_fundamental > 0, "Energy should be positive"
            
            results['tests'].append({
                'test': 'Fundamental rhythm energy',
                'frequency_hz': self.framework.f0,
                'energy_j': E_fundamental,
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Fundamental energy', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 2: Energy from harmonics
        self.print_subheader("Test 2.2: Energy from harmonic rhythms")
        try:
            harmonics = [1, 2, 3, 5, 7, 11]  # Test various harmonics
            energies = []
            
            for n in harmonics:
                E_n = self.framework.energy_from_rhythm(
                    self.framework.f0,
                    amplitude=1.0,
                    harmonic_n=n
                )
                energies.append(E_n)
                print(f"  Harmonic {n}: E = {E_n:.6e} J")
            
            # Check linear scaling with harmonic number
            ratios = [energies[i+1]/energies[0] for i in range(len(energies)-1)]
            expected_ratios = harmonics[1:]
            
            assert all(np.isclose(r, e, rtol=1e-10) for r, e in zip(ratios, expected_ratios))
            
            results['tests'].append({
                'test': 'Harmonic energy scaling',
                'harmonics': harmonics,
                'energies': [float(e) for e in energies],
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Harmonic energies', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 3: Rhythm spectrum decomposition
        self.print_subheader("Test 2.3: Energy to rhythm spectrum decomposition")
        try:
            test_energy = 1e-30  # J
            spectrum = self.framework.rhythm_spectrum(test_energy)
            
            print(f"Input energy: {test_energy:.6e} J")
            print(f"Fundamental f₀: {spectrum['fundamental_f0']} Hz")
            print(f"Harmonic number: {spectrum['harmonic_number']:.2f}")
            print(f"Harmonics detected: {len(spectrum['harmonics'])}")
            
            assert spectrum['fundamental_f0'] == self.framework.f0
            
            results['tests'].append({
                'test': 'Rhythm spectrum decomposition',
                'energy_j': test_energy,
                'harmonic_number': spectrum['harmonic_number'],
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Spectrum decomposition', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        return results
    
    # =========================================================================
    # PRINCIPLE 3: El espacio es un intervalo entre pulsos
    # =========================================================================
    
    def validate_principle_3(self) -> Dict[str, Any]:
        """Validate Principle 3: Space is an interval between pulses."""
        self.print_header("PRINCIPLE 3: El espacio es un intervalo entre pulsos")
        
        results = {
            'principle': 'Space is an interval between pulses',
            'tests': [],
            'status': 'PASSED'
        }
        
        # Test 1: Spatial quantum (fundamental wavelength)
        self.print_subheader("Test 3.1: Fundamental spatial quantum")
        try:
            lambda_0 = self.framework.spatial_quantum()
            expected_lambda = self.framework.c_light / self.framework.f0
            
            print(f"Fundamental wavelength λ₀ = {lambda_0/1000:.4f} km")
            print(f"This is c/f₀ = {expected_lambda/1000:.4f} km")
            
            assert lambda_0 > 0, "Spatial quantum should be positive"
            assert np.isclose(lambda_0, expected_lambda, rtol=1e-6)
            
            results['tests'].append({
                'test': 'Fundamental spatial quantum',
                'wavelength_km': lambda_0/1000,
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Spatial quantum', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 2: Space from phase difference
        self.print_subheader("Test 3.2: Space from phase difference")
        try:
            phase_diffs = [np.pi/4, np.pi/2, np.pi, 2*np.pi]
            
            for phase in phase_diffs:
                distance = self.framework.space_from_phase_difference(phase)
                print(f"  Phase Δφ = {phase:.4f} rad → Distance = {distance/1000:.4f} km")
                
                # Verify inverse
                phase_back = self.framework.phase_difference_from_space(distance)
                assert np.isclose(abs(phase_back), phase, rtol=1e-10)
            
            results['tests'].append({
                'test': 'Space from phase difference',
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Space from phase', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 3: Quantization of space
        self.print_subheader("Test 3.3: Space quantized in wavelength multiples")
        try:
            lambda_0 = self.framework.spatial_quantum()
            
            # Test multiple wavelengths
            for n in [1, 2, 5, 10]:
                distance = n * lambda_0
                phase = self.framework.phase_difference_from_space(distance)
                
                # Should be multiple of 2π
                phase_ratio = phase / (2 * np.pi)
                assert np.isclose(phase_ratio, n, rtol=1e-10)
                
                print(f"  {n}×λ₀ → phase = {n}×2π ✓")
            
            results['tests'].append({
                'test': 'Space quantization',
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Space quantization', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        return results
    
    # =========================================================================
    # PRINCIPLE 4: El tiempo es el número de ciclos
    # =========================================================================
    
    def validate_principle_4(self) -> Dict[str, Any]:
        """Validate Principle 4: Time is the number of cycles."""
        self.print_header("PRINCIPLE 4: El tiempo es el número de ciclos")
        
        results = {
            'principle': 'Time is the number of cycles',
            'tests': [],
            'status': 'PASSED'
        }
        
        # Test 1: Temporal quantum (fundamental period)
        self.print_subheader("Test 4.1: Fundamental temporal quantum")
        try:
            T_0 = self.framework.temporal_quantum()
            
            print(f"Fundamental period T₀ = {T_0*1000:.6f} ms")
            print(f"This is 1/f₀ = {1/self.framework.f0*1000:.6f} ms")
            
            assert T_0 > 0, "Temporal quantum should be positive"
            assert np.isclose(T_0, 1/self.framework.f0, rtol=1e-10)
            
            results['tests'].append({
                'test': 'Fundamental temporal quantum',
                'period_ms': T_0*1000,
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Temporal quantum', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 2: Time from cycles
        self.print_subheader("Test 4.2: Time from cycle counting")
        try:
            cycle_counts = [1, 10, 100, 1000, 1e6]
            
            for N in cycle_counts:
                t = self.framework.time_from_cycles(N)
                N_back = self.framework.cycles_from_time(t)
                
                assert np.isclose(N_back, N, rtol=1e-10)
                
                if N <= 1000:
                    print(f"  {N} cycles → {t*1000:.6f} ms → {N_back:.1f} cycles ✓")
                else:
                    print(f"  {N:.0e} cycles → {t:.6f} s → {N_back:.0e} cycles ✓")
            
            results['tests'].append({
                'test': 'Time from cycle counting',
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Cycle counting', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 3: Time quantization
        self.print_subheader("Test 4.3: Time quantized in period multiples")
        try:
            T_0 = self.framework.temporal_quantum()
            
            # Test multiple periods
            for n in [1, 2, 5, 10]:
                time = n * T_0
                cycles = self.framework.cycles_from_time(time)
                
                assert np.isclose(cycles, n, rtol=1e-10)
                print(f"  {n}×T₀ → {n} cycles ✓")
            
            results['tests'].append({
                'test': 'Time quantization',
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Time quantization', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        return results
    
    # =========================================================================
    # PRINCIPLE 5: El universo es una sinfonía autocontenida
    # =========================================================================
    
    def validate_principle_5(self) -> Dict[str, Any]:
        """Validate Principle 5: Universe is a self-contained symphony."""
        self.print_header("PRINCIPLE 5: El universo es una sinfonía autocontenida")
        
        results = {
            'principle': 'Universe is a self-contained symphony',
            'tests': [],
            'status': 'PASSED'
        }
        
        # Test 1: Perfect harmonic coherence
        self.print_subheader("Test 5.1: Perfect harmonic coherence")
        try:
            # Perfect harmonics of f₀
            perfect_harmonics = np.array([1, 2, 3, 5, 7, 11, 13]) * self.framework.f0
            coherence = self.framework.universal_coherence(perfect_harmonics)
            
            print(f"Perfect harmonics: {[1, 2, 3, 5, 7, 11, 13]}")
            print(f"Coherence: {coherence:.6f}")
            
            assert coherence > 0.99, "Perfect harmonics should have coherence > 0.99"
            
            results['tests'].append({
                'test': 'Perfect harmonic coherence',
                'coherence': coherence,
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Perfect coherence', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 2: Incoherent frequencies
        self.print_subheader("Test 5.2: Incoherent frequency detection")
        try:
            # Random frequencies (not harmonics)
            incoherent = np.array([123.45, 234.56, 345.67, 456.78])
            coherence = self.framework.universal_coherence(incoherent)
            
            print(f"Incoherent frequencies: {incoherent}")
            print(f"Coherence: {coherence:.6f}")
            
            assert coherence < 0.5, "Incoherent frequencies should have low coherence"
            
            results['tests'].append({
                'test': 'Incoherent frequency detection',
                'coherence': coherence,
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Incoherent detection', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 3: Harmonic decomposition
        self.print_subheader("Test 5.3: Harmonic decomposition of symphony")
        try:
            # Mix of harmonics and near-harmonics
            frequencies = np.array([
                1 * self.framework.f0,
                2 * self.framework.f0 + 0.1,  # Slightly detuned
                3 * self.framework.f0,
                5 * self.framework.f0 - 0.2,  # Slightly detuned
            ])
            
            decomposition = self.framework.harmonic_decomposition(frequencies)
            
            print(f"Coherence: {decomposition['coherence']:.6f}")
            print(f"Is symphony: {decomposition['is_symphony']}")
            print(f"\nHarmonic table:")
            for h in decomposition['harmonic_table']:
                print(f"  f={h['frequency']:.2f} Hz → n={h['harmonic_number']} "
                      f"(dev={h['deviation_hz']:.2f} Hz, {h['deviation_percent']:.2f}%)")
            
            assert len(decomposition['harmonic_table']) == len(frequencies)
            
            results['tests'].append({
                'test': 'Harmonic decomposition',
                'coherence': decomposition['coherence'],
                'is_symphony': decomposition['is_symphony'],
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Harmonic decomposition', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        # Test 4: Symphony signature
        self.print_subheader("Test 5.4: Universal symphony signature")
        try:
            signature = self.framework.symphony_signature()
            
            print(f"Fundamental frequency: {signature['fundamental_frequency']} Hz")
            print(f"Fundamental period: {signature['fundamental_period']*1000:.6f} ms")
            print(f"Fundamental wavelength: {signature['fundamental_wavelength']/1000:.4f} km")
            print(f"\nThe Five Principles:")
            for i, principle in enumerate(signature['principles'], 1):
                print(f"  {i}. {principle}")
            
            assert len(signature['principles']) == 5
            assert signature['fundamental_frequency'] == self.framework.f0
            
            results['tests'].append({
                'test': 'Symphony signature',
                'num_principles': len(signature['principles']),
                'status': '✅ PASSED'
            })
            print("✅ PASSED")
        except Exception as e:
            print(f"❌ FAILED: {e}")
            results['tests'].append({'test': 'Symphony signature', 'status': f'❌ FAILED: {e}'})
            results['status'] = 'FAILED'
        
        return results
    
    # =========================================================================
    # COMPREHENSIVE VALIDATION
    # =========================================================================
    
    def run_all_validations(self) -> Dict[str, Any]:
        """Run all validation tests."""
        self.print_header("COMPREHENSIVE PHILOSOPHICAL FRAMEWORK VALIDATION")
        
        print("\nValidating implementation of the five fundamental principles:")
        print("1. La masa es una ilusión de detención")
        print("2. La energía es ritmo")
        print("3. El espacio es un intervalo entre pulsos")
        print("4. El tiempo es el número de ciclos")
        print("5. El universo es una sinfonía autocontenida")
        
        all_results = {
            'timestamp': datetime.now().isoformat(),
            'f0_hz': self.framework.f0,
            'principles': []
        }
        
        # Run each principle validation
        all_results['principles'].append(self.validate_principle_1())
        all_results['principles'].append(self.validate_principle_2())
        all_results['principles'].append(self.validate_principle_3())
        all_results['principles'].append(self.validate_principle_4())
        all_results['principles'].append(self.validate_principle_5())
        
        # Summary
        self.print_header("VALIDATION SUMMARY")
        
        total_passed = 0
        total_failed = 0
        
        for i, principle in enumerate(all_results['principles'], 1):
            status = principle['status']
            num_tests = len(principle['tests'])
            passed_tests = sum(1 for t in principle['tests'] if 'PASSED' in str(t.get('status', '')))
            
            print(f"\nPrinciple {i}: {principle['principle']}")
            print(f"  Status: {status}")
            print(f"  Tests: {passed_tests}/{num_tests} passed")
            
            total_passed += passed_tests
            total_failed += (num_tests - passed_tests)
        
        print("\n" + "=" * 80)
        print(f"TOTAL: {total_passed} tests passed, {total_failed} tests failed")
        
        all_passed = all(p['status'] == 'PASSED' for p in all_results['principles'])
        
        if all_passed:
            print("\n✅ ALL PRINCIPLES VALIDATED SUCCESSFULLY")
            print("\n∞³ LA SINFONÍA UNIVERSAL VERIFICADA ∞³")
            all_results['overall_status'] = 'PASSED'
        else:
            print("\n⚠️  SOME PRINCIPLES FAILED VALIDATION")
            all_results['overall_status'] = 'FAILED'
        
        print("=" * 80)
        
        return all_results


def main():
    """Main validation function."""
    validator = PhilosophicalFrameworkValidator()
    results = validator.run_all_validations()
    
    # Save results
    output_dir = Path(__file__).parent.parent / "results"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "philosophical_framework_validation.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📊 Results saved to: {output_file}")
    
    # Return exit code
    return 0 if results['overall_status'] == 'PASSED' else 1


if __name__ == "__main__":
    sys.exit(main())
