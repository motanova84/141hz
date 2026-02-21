#!/usr/bin/env python3
"""
Tests for Quantum Harmonic Unification module.

Tests the connections between:
- Musical harmonics (C# note)
- Prime number 17
- Riemann zeros
- QCD color-flavor structure
- Universal coherence

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import sys
import math
import importlib.util
from pathlib import Path

# Load module directly to avoid numpy dependency in qcal.__init__
module_path = Path(__file__).parent.parent / 'qcal' / 'quantum_harmonic_unification.py'
spec = importlib.util.spec_from_file_location('qhu', str(module_path))
qhu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qhu)

# Import from loaded module
QuantumHarmonicUnifier = qhu.QuantumHarmonicUnifier
F0_HZ = qhu.F0_HZ
PRIME_17 = qhu.PRIME_17
RIEMANN_ZERO_1 = qhu.RIEMANN_ZERO_1
QCD_COLORS = qhu.QCD_COLORS
QCD_FLAVORS = qhu.QCD_FLAVORS
QCD_GLUONS = qhu.QCD_GLUONS
C_SHARP_MIDDLE = qhu.C_SHARP_MIDDLE
PHI = qhu.PHI


class TestQuantumHarmonicUnifier:
    """Test suite for QuantumHarmonicUnifier class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.unifier = QuantumHarmonicUnifier(f0=F0_HZ, precision=50)
    
    def test_initialization(self):
        """Test proper initialization."""
        assert self.unifier.f0 == F0_HZ
        assert self.unifier.precision == 50
        print("✓ Initialization test passed")
    
    def test_musical_octave_position(self):
        """Test musical octave calculations."""
        music = self.unifier.musical_octave_position()
        
        # Check required keys
        assert 'f0_hz' in music
        assert 'note' in music
        assert 'octaves_below_middle_c_sharp' in music
        assert 'middle_c_sharp_hz' in music
        
        # Check values
        assert music['f0_hz'] == F0_HZ
        assert music['note'] == 'C# (do sostenido)'
        assert music['middle_c_sharp_hz'] == C_SHARP_MIDDLE
        
        # f₀ should be below middle C#
        assert music['octaves_below_middle_c_sharp'] > 0
        
        # Ratio should match
        expected_ratio = C_SHARP_MIDDLE / F0_HZ
        assert abs(music['ratio_to_middle'] - expected_ratio) < 0.01
        
        print(f"✓ Musical octave test passed: {music['octaves_below_middle_c_sharp']:.3f} octaves below middle C#")
    
    def test_prime_17_resonance(self):
        """Test prime 17 resonance calculations."""
        prime = self.unifier.prime_17_resonance()
        
        # Check required keys
        assert 'prime' in prime
        assert 'prime_position' in prime
        assert 'coupling_constant' in prime
        assert 'equilibrium_17' in prime
        
        # Check values
        assert prime['prime'] == PRIME_17
        assert prime['prime_position'] == 7  # 17 is the 7th prime
        
        # Coupling constant should be positive and reasonable
        assert 0.2 < prime['coupling_constant'] < 0.4
        
        # Equilibrium should be positive
        assert prime['equilibrium_17'] > 0
        
        # Resonance factor should be around 8-9
        assert 7 < prime['resonance_factor'] < 10
        
        print(f"✓ Prime 17 resonance test passed: coupling = {prime['coupling_constant']:.4f}")
    
    def test_riemann_zero_coupling(self):
        """Test Riemann zero coupling calculations."""
        riemann = self.unifier.riemann_zero_coupling()
        
        # Check required keys
        assert 'riemann_zero_1' in riemann
        assert 'f0_to_zero1_ratio' in riemann
        assert 'spectral_density_at_f0' in riemann
        
        # Check values
        assert riemann['riemann_zero_1'] == RIEMANN_ZERO_1
        
        # Ratio should be positive and around 10
        assert 8 < riemann['f0_to_zero1_ratio'] < 12
        
        # Distance should be positive (f₀ > first zero)
        assert riemann['distance_to_first_zero'] > 0
        
        # Spectral density should be reasonable
        assert riemann['spectral_density_at_f0'] > 0
        
        print(f"✓ Riemann zero coupling test passed: ratio = {riemann['f0_to_zero1_ratio']:.3f}")
    
    def test_qcd_harmonic_structure(self):
        """Test QCD harmonic structure calculations."""
        qcd = self.unifier.qcd_harmonic_structure()
        
        # Check required keys
        assert 'colors' in qcd
        assert 'flavors' in qcd
        assert 'gluons' in qcd
        assert 'qcd_dimension' in qcd
        assert 'color_frequency_hz' in qcd
        assert 'flavor_frequency_hz' in qcd
        assert 'gluon_frequency_hz' in qcd
        
        # Check QCD constants
        assert qcd['colors'] == QCD_COLORS  # 3
        assert qcd['flavors'] == QCD_FLAVORS  # 6
        assert qcd['gluons'] == QCD_GLUONS  # 8
        assert qcd['qcd_dimension'] == QCD_COLORS * QCD_FLAVORS  # 18
        
        # Check frequencies
        assert abs(qcd['color_frequency_hz'] - F0_HZ / QCD_COLORS) < 0.01
        assert abs(qcd['flavor_frequency_hz'] - F0_HZ / QCD_FLAVORS) < 0.01
        assert abs(qcd['gluon_frequency_hz'] - F0_HZ / QCD_GLUONS) < 0.01
        
        # Check names
        assert len(qcd['color_names']) == 3
        assert len(qcd['flavor_names']) == 6
        assert 'Red' in qcd['color_names']
        assert 'Up' in qcd['flavor_names']
        
        # QCD scale should be much higher than f₀
        assert qcd['octaves_to_qcd_scale'] > 60
        
        print(f"✓ QCD harmonics test passed: {qcd['qcd_dimension']} dimensional space")
    
    def test_primordial_silence_frequency(self):
        """Test primordial silence frequency calculations."""
        primordial = self.unifier.primordial_silence_frequency()
        
        # Check required keys
        assert 'planck_frequency_hz' in primordial
        assert 'cmb_frequency_hz' in primordial
        assert 'octaves_to_planck' in primordial
        assert 'octaves_to_cmb' in primordial
        
        # Planck frequency should be enormous
        assert primordial['planck_frequency_hz'] > 1e43
        
        # CMB frequency should be in GHz range
        assert primordial['cmb_frequency_hz'] > 1e9
        assert primordial['cmb_frequency_hz'] < 1e12
        
        # Octaves should be positive and large
        assert primordial['octaves_to_planck'] > 100
        assert primordial['octaves_to_cmb'] > 25  # CMB is about 28.6 octaves above f₀
        assert primordial['octaves_to_cmb'] < primordial['octaves_to_planck']
        
        print(f"✓ Primordial frequency test passed: {primordial['octaves_to_planck']:.1f} octaves to Planck")
    
    def test_dreaming_universe_coherence(self):
        """Test universal coherence calculation."""
        coherence = self.unifier.dreaming_universe_coherence()
        
        # Check required keys
        assert 'psi_musical' in coherence
        assert 'psi_prime' in coherence
        assert 'psi_riemann' in coherence
        assert 'psi_qcd' in coherence
        assert 'psi_universe' in coherence
        assert 'golden_coupling' in coherence
        assert 'coherence_level' in coherence
        
        # All psi values should be positive and <= 1
        assert 0 < coherence['psi_musical'] <= 1
        assert 0 < coherence['psi_prime'] <= 1
        assert 0 < coherence['psi_riemann'] <= 1
        assert 0 < coherence['psi_qcd'] <= 1
        assert 0 < coherence['psi_universe'] <= 1
        
        # Golden coupling should involve PHI
        expected_golden = coherence['psi_universe'] * PHI
        assert abs(coherence['golden_coupling'] - expected_golden) < 0.001
        
        # Coherence level should be a valid string
        assert coherence['coherence_level'] in ['HIGH', 'MODERATE', 'LOW']
        
        # Components should be present
        assert 'components' in coherence
        assert 'musical' in coherence['components']
        assert 'prime_17' in coherence['components']
        assert 'riemann' in coherence['components']
        assert 'qcd' in coherence['components']
        
        print(f"✓ Universal coherence test passed: Ψ = {coherence['psi_universe']:.6f}, level = {coherence['coherence_level']}")
    
    def test_full_report_generation(self):
        """Test full report generation."""
        report = self.unifier.generate_full_report()
        
        # Check main sections
        assert 'frequency_hz' in report
        assert 'timestamp' in report
        assert 'poetic_source' in report
        assert 'musical_analysis' in report
        assert 'prime_17_resonance' in report
        assert 'riemann_zeros' in report
        assert 'qcd_harmonics' in report
        assert 'primordial_silence' in report
        assert 'universal_coherence' in report
        assert 'summary' in report
        
        # Check frequency
        assert report['frequency_hz'] == F0_HZ
        
        # Check poetic source
        assert 'quark' in report['poetic_source'].lower()
        # Note: poetic_source is abbreviated, doesn't contain full poem
        
        # Summary should be a string
        assert isinstance(report['summary'], str)
        assert len(report['summary']) > 100
        
        print("✓ Full report generation test passed")
    
    def test_mathematical_consistency(self):
        """Test mathematical consistency between components."""
        music = self.unifier.musical_octave_position()
        prime = self.unifier.prime_17_resonance()
        riemann = self.unifier.riemann_zero_coupling()
        qcd = self.unifier.qcd_harmonic_structure()
        
        # Check that f₀ is consistent across all calculations
        assert music['f0_hz'] == F0_HZ
        assert abs(qcd['color_frequency_hz'] * QCD_COLORS - F0_HZ) < 0.01
        assert abs(qcd['flavor_frequency_hz'] * QCD_FLAVORS - F0_HZ) < 0.01
        assert abs(qcd['gluon_frequency_hz'] * QCD_GLUONS - F0_HZ) < 0.01
        
        # Check prime coupling is logarithmic
        expected_log = math.log(F0_HZ)
        assert abs(prime['log_f0'] - expected_log) < 0.001
        
        # Check Riemann ratio
        expected_ratio = F0_HZ / RIEMANN_ZERO_1
        assert abs(riemann['f0_to_zero1_ratio'] - expected_ratio) < 0.01
        
        print("✓ Mathematical consistency test passed")
    
    def test_physical_bounds(self):
        """Test that physical quantities are within reasonable bounds."""
        qcd = self.unifier.qcd_harmonic_structure()
        primordial = self.unifier.primordial_silence_frequency()
        
        # Energy at f₀ should be much smaller than typical particle energies
        # E = h × f₀ ≈ 9.4e-32 J ≈ 5.9e-13 eV (extremely small)
        assert qcd['E_f0_eV'] < 1e-10  # Much less than 1 eV
        
        # QCD scale should be around 200 MeV ≈ 4.8e22 Hz
        assert 1e22 < qcd['lambda_qcd_hz'] < 1e23
        
        # Planck frequency should be around 1.85e43 Hz
        assert 1e43 < primordial['planck_frequency_hz'] < 2e43
        
        # CMB frequency should be around 56.8 GHz
        assert 5e10 < primordial['cmb_frequency_hz'] < 6e10
        
        print("✓ Physical bounds test passed")


def run_tests():
    """Run all tests."""
    print("\n" + "="*80)
    print("🧪 Testing Quantum Harmonic Unification Module")
    print("="*80 + "\n")
    
    test_suite = TestQuantumHarmonicUnifier()
    test_suite.setup_method()
    
    tests = [
        test_suite.test_initialization,
        test_suite.test_musical_octave_position,
        test_suite.test_prime_17_resonance,
        test_suite.test_riemann_zero_coupling,
        test_suite.test_qcd_harmonic_structure,
        test_suite.test_primordial_silence_frequency,
        test_suite.test_dreaming_universe_coherence,
        test_suite.test_full_report_generation,
        test_suite.test_mathematical_consistency,
        test_suite.test_physical_bounds,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*80)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*80 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(run_tests())
