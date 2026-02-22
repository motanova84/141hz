#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║      TEST SUITE - QUANTUM CHROMODYNAMIC POETRY (44+ Tests)                 ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)

Test suite completo para validar el módulo quantum_chromodynamic_poetry.
"""

import unittest
import sys
import math
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.quantum_chromodynamic_poetry import (
    QuantumChromodynamicPoetry,
    QuarkFlavor,
    QuarkColor,
    GluonType,
    Quark,
    Gluon,
    CosmicResonance,
    RIEMANN_ZEROS,
    OMEGA_17,
    F0_HZ,
    QUARK_MASSES_GEV,
    display_symphony_summary
)


class TestConstants(unittest.TestCase):
    """Tests for fundamental constants (5 tests)."""
    
    def test_f0_value(self):
        """Test fundamental frequency value."""
        self.assertAlmostEqual(F0_HZ, 141.70001, places=5)
    
    def test_omega_17_value(self):
        """Test prime 17 coupling constant."""
        expected = math.log(17)
        self.assertAlmostEqual(OMEGA_17, expected, places=6)
        self.assertAlmostEqual(OMEGA_17, 2.833, places=2)
    
    def test_riemann_zeros_count(self):
        """Test that exactly 10 Riemann zeros are defined."""
        self.assertEqual(len(RIEMANN_ZEROS), 10)
    
    def test_riemann_zero_values(self):
        """Test first and last Riemann zero values."""
        self.assertAlmostEqual(RIEMANN_ZEROS[0], 14.134725, places=6)  # γ₁
        self.assertAlmostEqual(RIEMANN_ZEROS[9], 49.773832, places=6)  # γ₁₀
    
    def test_quark_mass_count(self):
        """Test that all 6 quark flavors have masses defined."""
        self.assertEqual(len(QUARK_MASSES_GEV), 6)
        for flavor in QuarkFlavor:
            self.assertIn(flavor.value, QUARK_MASSES_GEV)


class TestQuarkCreation(unittest.TestCase):
    """Tests for quark creation and frequency calculations (10 tests)."""
    
    def setUp(self):
        """Initialize QCD poetry system."""
        self.qcd = QuantumChromodynamicPoetry()
    
    def test_create_single_quark(self):
        """Test creating a single quark."""
        quark = self.qcd.create_quark(QuarkFlavor.UP, QuarkColor.RED)
        self.assertIsInstance(quark, Quark)
        self.assertEqual(quark.flavor, QuarkFlavor.UP)
        self.assertEqual(quark.color, QuarkColor.RED)
    
    def test_quark_mass_assignment(self):
        """Test that quark mass is correctly assigned."""
        quark = self.qcd.create_quark(QuarkFlavor.CHARM, QuarkColor.BLUE)
        expected_mass = QUARK_MASSES_GEV['charm']
        self.assertAlmostEqual(quark.mass_gev, expected_mass, places=8)
    
    def test_quark_frequency_formula(self):
        """Test quark frequency formula: ω = log(m) + log(17)."""
        quark = self.qcd.create_quark(QuarkFlavor.TOP, QuarkColor.GREEN)
        expected_freq = math.log(quark.mass_gev) + OMEGA_17
        self.assertAlmostEqual(quark.frequency, expected_freq, places=8)
    
    def test_create_all_quarks_count(self):
        """Test that 18 quarks are created (6 flavors × 3 colors)."""
        quarks = self.qcd.create_all_quarks()
        self.assertEqual(len(quarks), 18)
    
    def test_create_all_quarks_unique_combinations(self):
        """Test that all flavor-color combinations are present."""
        quarks = self.qcd.create_all_quarks()
        combinations = {(q.flavor, q.color) for q in quarks}
        self.assertEqual(len(combinations), 18)
        
        # Verify all combinations exist
        for flavor in QuarkFlavor:
            for color in QuarkColor:
                self.assertIn((flavor, color), combinations)
    
    def test_quark_frequency_spectrum_structure(self):
        """Test quark frequency spectrum has correct structure."""
        spectrum = self.qcd.get_quark_frequency_spectrum()
        self.assertIn('by_flavor', spectrum)
        self.assertIn('by_color', spectrum)
        self.assertIn('all', spectrum)
        self.assertEqual(len(spectrum['all']), 18)
    
    def test_quark_spectrum_by_flavor(self):
        """Test quark spectrum grouping by flavor."""
        spectrum = self.qcd.get_quark_frequency_spectrum()
        for flavor in QuarkFlavor:
            self.assertIn(flavor.value, spectrum['by_flavor'])
            # Each flavor should have 3 quarks (3 colors)
            self.assertEqual(len(spectrum['by_flavor'][flavor.value]), 3)
    
    def test_quark_spectrum_by_color(self):
        """Test quark spectrum grouping by color."""
        spectrum = self.qcd.get_quark_frequency_spectrum()
        for color in QuarkColor:
            self.assertIn(color.value, spectrum['by_color'])
            # Each color should have 6 quarks (6 flavors)
            self.assertEqual(len(spectrum['by_color'][color.value]), 6)
    
    def test_up_quark_frequency_range(self):
        """Test up quark frequency is in expected range."""
        quark = self.qcd.create_quark(QuarkFlavor.UP, QuarkColor.RED)
        # log(0.00216) + log(17) ≈ -6.14 + 2.83 = -3.31
        self.assertLess(quark.frequency, 0)  # Should be negative
        self.assertGreater(quark.frequency, -10)
    
    def test_top_quark_frequency_range(self):
        """Test top quark frequency is in expected range."""
        quark = self.qcd.create_quark(QuarkFlavor.TOP, QuarkColor.BLUE)
        # log(172.69) + log(17) ≈ 5.15 + 2.83 = 7.98
        self.assertGreater(quark.frequency, 5)
        self.assertLess(quark.frequency, 10)


class TestGluonCreation(unittest.TestCase):
    """Tests for gluon creation and Riemann zero calculations (8 tests)."""
    
    def setUp(self):
        """Initialize QCD poetry system."""
        self.qcd = QuantumChromodynamicPoetry()
    
    def test_get_riemann_zero_exact_values(self):
        """Test exact Riemann zeros for n ≤ 10."""
        for n in range(1, 11):
            zero = self.qcd.get_riemann_zero(n)
            self.assertAlmostEqual(zero, RIEMANN_ZEROS[n - 1], places=6)
    
    def test_riemann_zero_asymptotic_approximation(self):
        """Test asymptotic approximation for n > 10."""
        n = 20
        zero = self.qcd.get_riemann_zero(n)
        expected = (2 * math.pi * n) / math.log(n)
        self.assertAlmostEqual(zero, expected, places=6)
    
    def test_riemann_zero_invalid_index(self):
        """Test that invalid Riemann zero indices raise errors."""
        with self.assertRaises(ValueError):
            self.qcd.get_riemann_zero(0)
        
        with self.assertRaises(ValueError):
            self.qcd.get_riemann_zero(-1)
    
    def test_create_single_gluon(self):
        """Test creating a single gluon."""
        gluon = self.qcd.create_gluon(GluonType.RB, 1)
        self.assertIsInstance(gluon, Gluon)
        self.assertEqual(gluon.gluon_type, GluonType.RB)
        self.assertEqual(gluon.riemann_zero_index, 1)
    
    def test_gluon_octave_calculation(self):
        """Test gluon octave is log₂(γₙ)."""
        gluon = self.qcd.create_gluon(GluonType.RG, 5)
        gamma_5 = RIEMANN_ZEROS[4]
        expected_octave = math.log2(gamma_5)
        self.assertAlmostEqual(gluon.octave, expected_octave, places=6)
    
    def test_gluon_frequency_calculation(self):
        """Test gluon frequency is f₀ × γₙ."""
        gluon = self.qcd.create_gluon(GluonType.BR, 3)
        gamma_3 = RIEMANN_ZEROS[2]
        expected_freq = F0_HZ * gamma_3
        self.assertAlmostEqual(gluon.frequency_hz, expected_freq, places=2)
    
    def test_create_gluon_octet_count(self):
        """Test that 8 gluons are created."""
        gluons = self.qcd.create_gluon_octet()
        self.assertEqual(len(gluons), 8)
    
    def test_gluon_spectrum_structure(self):
        """Test gluon frequency spectrum has correct structure."""
        spectrum = self.qcd.get_gluon_frequency_spectrum()
        self.assertIn('gluons', spectrum)
        self.assertIn('frequency_range_hz', spectrum)
        self.assertIn('octave_range', spectrum)
        self.assertEqual(len(spectrum['gluons']), 8)


class TestCosmicResonance(unittest.TestCase):
    """Tests for cosmic resonance calculations (10 tests)."""
    
    def setUp(self):
        """Initialize QCD poetry system."""
        self.qcd = QuantumChromodynamicPoetry()
    
    def test_love_between_prime_and_zero_structure(self):
        """Test cosmic resonance returns correct structure."""
        love = self.qcd.love_between_prime_and_zero(17, 1)
        self.assertIsInstance(love, CosmicResonance)
        self.assertEqual(love.prime, 17)
        self.assertEqual(love.riemann_zero_index, 1)
    
    def test_omega_prime_calculation(self):
        """Test omega_prime is log(p)."""
        love = self.qcd.love_between_prime_and_zero(13, 2)
        expected_omega = math.log(13)
        self.assertAlmostEqual(love.omega_prime, expected_omega, places=8)
    
    def test_resonance_intensity_range(self):
        """Test resonance intensity is in valid range [0, 1]."""
        love = self.qcd.love_between_prime_and_zero(17, 1)
        self.assertGreaterEqual(love.intensity, 0)
        self.assertLessEqual(love.intensity, 1)
    
    def test_resonance_intensity_formula(self):
        """Test intensity formula: I = |exp(iω_p·γₙ)| / (1 + |ω_p - γₙ|)."""
        love = self.qcd.love_between_prime_and_zero(17, 1)
        omega_p = math.log(17)
        gamma_1 = RIEMANN_ZEROS[0]
        
        # |exp(iω_p·γₙ)| = 1 for real ω_p and γₙ
        difference = abs(omega_p - gamma_1)
        expected_intensity = 1.0 / (1 + difference)
        
        self.assertAlmostEqual(love.intensity, expected_intensity, places=6)
    
    def test_beat_frequency_calculation(self):
        """Test beat frequency is |ω_p - γₙ| × f₀."""
        love = self.qcd.love_between_prime_and_zero(17, 1)
        omega_p = math.log(17)
        gamma_1 = RIEMANN_ZEROS[0]
        expected_beat = abs(omega_p - gamma_1) * F0_HZ
        self.assertAlmostEqual(love.beat_frequency_hz, expected_beat, places=2)
    
    def test_specific_resonance_17_1(self):
        """Test specific example: p=17, n=1."""
        love = self.qcd.love_between_prime_and_zero(17, 1)
        # Expected: intensity ≈ 0.081291, beat_freq ≈ 254.87 Hz (corrected)
        self.assertAlmostEqual(love.intensity, 0.081291, places=5)
        # Beat frequency calculation
        omega_17 = math.log(17)
        gamma_1 = 14.134725
        beat_expected = abs(omega_17 - gamma_1) * F0_HZ
        self.assertAlmostEqual(love.beat_frequency_hz, beat_expected, places=1)
    
    def test_non_prime_raises_error(self):
        """Test that non-prime numbers raise ValueError."""
        with self.assertRaises(ValueError):
            self.qcd.love_between_prime_and_zero(16, 1)
        
        with self.assertRaises(ValueError):
            self.qcd.love_between_prime_and_zero(100, 1)
    
    def test_resonance_matrix_shape(self):
        """Test resonance matrix has correct shape."""
        primes = [2, 3, 5]
        zero_indices = [1, 2, 3, 4]
        matrix = self.qcd.calculate_prime_zero_resonance_matrix(primes, zero_indices)
        
        self.assertEqual(len(matrix), 3)  # 3 primes
        for row in matrix:
            self.assertEqual(len(row), 4)  # 4 zeros
    
    def test_resonance_matrix_default_zeros(self):
        """Test resonance matrix uses first 10 zeros by default."""
        primes = [2, 3]
        matrix = self.qcd.calculate_prime_zero_resonance_matrix(primes)
        
        self.assertEqual(len(matrix), 2)
        for row in matrix:
            self.assertEqual(len(row), 10)  # Default: 10 zeros
    
    def test_resonance_symmetry(self):
        """Test resonance calculation is consistent."""
        love1 = self.qcd.love_between_prime_and_zero(11, 3)
        love2 = self.qcd.love_between_prime_and_zero(11, 3)
        self.assertAlmostEqual(love1.intensity, love2.intensity, places=8)


class TestPrimordialSilence(unittest.TestCase):
    """Tests for primordial silence frequency (5 tests)."""
    
    def setUp(self):
        """Initialize QCD poetry system."""
        self.qcd = QuantumChromodynamicPoetry()
    
    def test_primordial_silence_p17(self):
        """Test primordial silence frequency for p=17."""
        f_silence = self.qcd.primordial_silence_frequency(17)
        # f(17) = f₀ · exp(-1) ≈ 52.13 Hz
        expected = F0_HZ * math.exp(-1)
        self.assertAlmostEqual(f_silence, expected, places=2)
        self.assertAlmostEqual(f_silence, 52.13, places=1)
    
    def test_primordial_silence_formula(self):
        """Test general formula: f(p) = f₀ · exp(-log(p)/log(17))."""
        p = 23
        f_silence = self.qcd.primordial_silence_frequency(p)
        exponent = -math.log(p) / math.log(17)
        expected = F0_HZ * math.exp(exponent)
        self.assertAlmostEqual(f_silence, expected, places=6)
    
    def test_primordial_silence_decreasing(self):
        """Test that silence frequency decreases with larger primes."""
        f2 = self.qcd.primordial_silence_frequency(2)
        f3 = self.qcd.primordial_silence_frequency(3)
        f5 = self.qcd.primordial_silence_frequency(5)
        
        self.assertGreater(f2, f3)
        self.assertGreater(f3, f5)
    
    def test_primordial_silence_spectrum_count(self):
        """Test silence spectrum for first 20 primes."""
        spectrum = self.qcd.get_primordial_silence_spectrum()
        self.assertEqual(len(spectrum), 20)
    
    def test_primordial_silence_non_prime_error(self):
        """Test that non-primes raise ValueError."""
        with self.assertRaises(ValueError):
            self.qcd.primordial_silence_frequency(15)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling (6 tests)."""
    
    def setUp(self):
        """Initialize QCD poetry system."""
        self.qcd = QuantumChromodynamicPoetry()
    
    def test_custom_f0_initialization(self):
        """Test QCD system with custom f₀."""
        custom_f0 = 100.0
        qcd = QuantumChromodynamicPoetry(f0_hz=custom_f0)
        self.assertEqual(qcd.f0_hz, custom_f0)
        
        gluon = qcd.create_gluon(GluonType.RB, 1)
        expected_freq = custom_f0 * RIEMANN_ZEROS[0]
        self.assertAlmostEqual(gluon.frequency_hz, expected_freq, places=2)
    
    def test_is_prime_utility(self):
        """Test prime checking utility function."""
        qcd = QuantumChromodynamicPoetry()
        
        # Primes
        self.assertTrue(qcd._is_prime(2))
        self.assertTrue(qcd._is_prime(3))
        self.assertTrue(qcd._is_prime(17))
        self.assertTrue(qcd._is_prime(97))
        
        # Non-primes
        self.assertFalse(qcd._is_prime(1))
        self.assertFalse(qcd._is_prime(4))
        self.assertFalse(qcd._is_prime(100))
    
    def test_first_n_primes_utility(self):
        """Test first n primes utility function."""
        qcd = QuantumChromodynamicPoetry()
        
        primes = qcd._first_n_primes(5)
        self.assertEqual(primes, [2, 3, 5, 7, 11])
        
        primes = qcd._first_n_primes(10)
        self.assertEqual(len(primes), 10)
        self.assertEqual(primes[0], 2)
        self.assertEqual(primes[9], 29)
    
    def test_all_quark_flavors_have_masses(self):
        """Test that all QuarkFlavor enums have corresponding masses."""
        for flavor in QuarkFlavor:
            self.assertIn(flavor.value, QUARK_MASSES_GEV)
            mass = QUARK_MASSES_GEV[flavor.value]
            self.assertGreater(mass, 0)
    
    def test_all_gluon_types_count(self):
        """Test that GluonType enum has exactly 8 types."""
        gluon_types = list(GluonType)
        self.assertEqual(len(gluon_types), 8)
    
    def test_riemann_zeros_strictly_increasing(self):
        """Test that Riemann zeros are in strictly increasing order."""
        for i in range(len(RIEMANN_ZEROS) - 1):
            self.assertLess(RIEMANN_ZEROS[i], RIEMANN_ZEROS[i + 1])


class TestChromodynamicSymphony(unittest.TestCase):
    """Tests for complete symphony generation (5+ tests)."""
    
    def setUp(self):
        """Initialize QCD poetry system."""
        self.qcd = QuantumChromodynamicPoetry()
    
    def test_generate_symphony_structure(self):
        """Test symphony has all required components."""
        symphony = self.qcd.generate_chromodynamic_symphony()
        
        self.assertIn('quarks', symphony)
        self.assertIn('gluons', symphony)
        self.assertIn('cosmic_resonance', symphony)
        self.assertIn('primordial_silence', symphony)
        self.assertIn('metrics', symphony)
        self.assertIn('constants', symphony)
    
    def test_symphony_quark_count(self):
        """Test symphony includes all 18 quarks."""
        symphony = self.qcd.generate_chromodynamic_symphony()
        quarks = symphony['quarks']['particles']
        self.assertEqual(len(quarks), 18)
    
    def test_symphony_gluon_count(self):
        """Test symphony includes all 8 gluons."""
        symphony = self.qcd.generate_chromodynamic_symphony()
        gluons = symphony['gluons']['particles']
        self.assertEqual(len(gluons), 8)
    
    def test_symphony_resonance_matrix(self):
        """Test symphony resonance matrix is 10×10."""
        symphony = self.qcd.generate_chromodynamic_symphony()
        matrix = symphony['cosmic_resonance']['matrix']
        self.assertEqual(len(matrix), 10)  # 10 primes
        for row in matrix:
            self.assertEqual(len(row), 10)  # 10 zeros
    
    def test_symphony_metrics(self):
        """Test symphony metrics are computed correctly."""
        symphony = self.qcd.generate_chromodynamic_symphony()
        metrics = symphony['metrics']
        
        self.assertEqual(metrics['total_quarks'], 18)
        self.assertEqual(metrics['total_gluons'], 8)
        self.assertEqual(metrics['prime_count'], 10)
        self.assertEqual(metrics['riemann_zero_count'], 10)
    
    def test_display_symphony_summary(self):
        """Test that symphony summary can be displayed without errors."""
        symphony = self.qcd.generate_chromodynamic_symphony()
        try:
            display_symphony_summary(symphony)
        except Exception as e:
            self.fail(f"display_symphony_summary raised {type(e).__name__}: {e}")


def run_all_tests():
    """Run all tests and print summary."""
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║         QUANTUM CHROMODYNAMIC POETRY - Test Suite                         ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestQuarkCreation))
    suite.addTests(loader.loadTestsFromTestCase(TestGluonCreation))
    suite.addTests(loader.loadTestsFromTestCase(TestCosmicResonance))
    suite.addTests(loader.loadTestsFromTestCase(TestPrimordialSilence))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestChromodynamicSymphony))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                           Test Summary                                     ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"Total tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED")
    
    return result


if __name__ == "__main__":
    result = run_all_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
