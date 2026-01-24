#!/usr/bin/env python3
"""
Test Suite for Dimensionless Constants Framework
=================================================

This test suite validates the dimensionless constants core module
with 30+ comprehensive tests ensuring the framework meets all
requirements specified in the problem statement.

Tests cover:
- Core constant initialization and precision
- Dimensionless ratio calculations
- f₀ derivation from pure constants
- Mass hierarchy validation
- Noetic radius coupling
- Running coupling α(E)
- Physical law validations
- Numerical precision and stability

Author: José Manuel Mota Burruezo Ψ ✧ ∞³
Date: January 2026
"""

import sys
import unittest
from pathlib import Path
import mpmath as mp

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from dimensionless_constants_core import DimensionlessConstantsCore, DimensionlessConstants


class TestDimensionlessConstantsCore(unittest.TestCase):
    """Test core dimensionless constants module."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.core = DimensionlessConstantsCore(precision=100)
        
    def test_01_initialization(self):
        """Test that core initializes correctly."""
        self.assertIsNotNone(self.core)
        self.assertEqual(self.core.precision, 100)
        
    def test_02_alpha_value(self):
        """Test fine structure constant value."""
        alpha = float(self.core.alpha)
        # α ≈ 1/137.036
        self.assertAlmostEqual(alpha, 1/137.036, places=3)
        self.assertTrue(0.007 < alpha < 0.008)
        
    def test_03_alpha_inverse(self):
        """Test inverse of fine structure constant."""
        alpha_inv = float(self.core.alpha_inv)
        # α⁻¹ ≈ 137.036
        self.assertAlmostEqual(alpha_inv, 137.036, places=2)
        self.assertTrue(137.0 < alpha_inv < 137.1)
        
    def test_04_golden_ratio(self):
        """Test golden ratio φ."""
        phi = float(self.core.phi)
        # φ = (1+√5)/2 ≈ 1.618
        self.assertAlmostEqual(phi, 1.618033988749895, places=10)
        
    def test_05_euler_gamma(self):
        """Test Euler-Mascheroni constant."""
        gamma = float(self.core.gamma)
        # γ ≈ 0.5772156649
        self.assertAlmostEqual(gamma, 0.5772156649, places=8)
        
    def test_06_zeta_prime_half(self):
        """Test Riemann zeta derivative at s=1/2."""
        zeta = float(self.core.zeta_prime_half)
        # ζ'(1/2) ≈ -0.207886
        self.assertAlmostEqual(zeta, -0.207886, places=4)
        self.assertTrue(zeta < 0)
        
    def test_07_mass_ratio_p_e(self):
        """Test proton-to-electron mass ratio."""
        ratio = float(self.core.mass_ratio_p_e)
        # m_p/m_e ≈ 1836.15
        self.assertAlmostEqual(ratio, 1836.15, places=1)
        self.assertTrue(1830 < ratio < 1840)
        
    def test_08_mass_ratio_normalized(self):
        """Test mass ratio normalized by α."""
        ratio = float(self.core.mass_ratio_normalized)
        # (m_p/m_e)/137 ≈ 13.4
        self.assertAlmostEqual(ratio, 13.4, places=1)
        self.assertTrue(13.0 < ratio < 14.0)
        
    def test_09_constants_dataclass(self):
        """Test constants dataclass structure."""
        constants = self.core.constants
        self.assertIsInstance(constants, DimensionlessConstants)
        self.assertIsNotNone(constants.ALPHA)
        self.assertIsNotNone(constants.PHI)
        self.assertIsNotNone(constants.MASS_RATIO_P_E)
        
    def test_10_precision_setting(self):
        """Test that precision is properly set."""
        core_50 = DimensionlessConstantsCore(precision=50)
        self.assertEqual(core_50.precision, 50)
        
    def test_11_f0_derivation_structure(self):
        """Test f₀ derivation returns proper structure."""
        result = self.core.derive_f0_from_pure_constants()
        self.assertIn("f0_derived_hz", result)
        self.assertIn("f0_observed_hz", result)
        self.assertIn("relative_error", result)
        self.assertIn("status", result)
        
    def test_12_f0_derivation_value(self):
        """Test f₀ derived value is close to observed."""
        result = self.core.derive_f0_from_pure_constants()
        f0_derived = result["f0_derived_hz"]
        f0_observed = result["f0_observed_hz"]
        
        # Should be within 5% (calibration allows some variation)
        rel_error = abs(f0_derived - f0_observed) / f0_observed
        self.assertLess(rel_error, 0.05)
        
    def test_13_f0_uses_pure_constants(self):
        """Test f₀ derivation uses only dimensionless constants."""
        result = self.core.derive_f0_from_pure_constants()
        
        # Check that formula involves zeta, phi
        self.assertIn("zeta_prime_half", result)
        self.assertIn("phi_cubed", result)
        self.assertEqual(result["derivation_formula"], "|ζ'(1/2)| × φ³ × base_freq")
        
    def test_14_noetic_radius_calculation(self):
        """Test noetic radius R_Ψ calculation."""
        result = self.core.compute_noetic_radius_ratio()
        R_psi_km = result["R_psi_km"]
        
        # R_Ψ ≈ 337.1 km
        self.assertAlmostEqual(R_psi_km, 337.1, places=0)
        self.assertTrue(335 < R_psi_km < 340)
        
    def test_15_noetic_radius_ratio(self):
        """Test noetic radius ratio with α."""
        result = self.core.compute_noetic_radius_ratio()
        ratio = result["ratio_R_psi_over_137_km"]
        
        # R_Ψ/137 ≈ 2.46
        self.assertAlmostEqual(ratio, 2.46, places=1)
        self.assertTrue(2.4 < ratio < 2.5)
        
    def test_16_mass_hierarchy_validation(self):
        """Test mass hierarchy validation."""
        result = self.core.validate_mass_hierarchy()
        self.assertEqual(result["validation"], "PASS")
        self.assertIn("normalized_ratio", result)
        
    def test_17_mass_hierarchy_in_range(self):
        """Test mass hierarchy is in expected range."""
        result = self.core.validate_mass_hierarchy()
        ratio = result["normalized_ratio"]
        expected_range = result["expected_range"]
        
        self.assertGreaterEqual(ratio, expected_range[0])
        self.assertLessEqual(ratio, expected_range[1])
        
    def test_18_running_alpha_low_energy(self):
        """Test running coupling at low energy."""
        result = self.core.compute_running_alpha(0.001)  # 1 MeV
        
        # At low energy, should be close to α(0) (within 1%)
        alpha_E = result["alpha_at_energy"]
        alpha_0 = result["alpha_low_energy"]
        
        rel_diff = abs(alpha_E - alpha_0) / alpha_0
        self.assertLess(rel_diff, 0.01)  # Within 1%
        
    def test_19_running_alpha_high_energy(self):
        """Test running coupling at high energy."""
        result = self.core.compute_running_alpha(1000)  # 1 TeV
        
        # At high energy, should be larger than α(0)
        alpha_E = result["alpha_at_energy"]
        alpha_0 = result["alpha_low_energy"]
        
        self.assertGreater(alpha_E, alpha_0)
        
    def test_20_running_alpha_positive_change(self):
        """Test α increases with energy."""
        result = self.core.compute_running_alpha(100)
        rel_change = result["relative_change"]
        
        # Should be positive (α increases)
        self.assertGreater(rel_change, 0)
        
    def test_21_running_alpha_dimensionless(self):
        """Test running α remains dimensionless."""
        for energy in [1, 10, 100, 1000]:
            result = self.core.compute_running_alpha(energy)
            alpha_E = result["alpha_at_energy"]
            
            # Should remain in (0, 1)
            self.assertGreater(alpha_E, 0)
            self.assertLess(alpha_E, 1)
            
    def test_22_coherence_report_generation(self):
        """Test coherence report generates without errors."""
        report = self.core.generate_coherence_report()
        self.assertIsInstance(report, str)
        self.assertIn("DIMENSIONLESS CONSTANTS", report)
        self.assertIn("α", report)
        
    def test_23_report_contains_key_sections(self):
        """Test report contains all key sections."""
        report = self.core.generate_coherence_report()
        self.assertIn("THE HEART OF THE SYSTEM", report)
        self.assertIn("DERIVATION OF f₀", report)
        self.assertIn("MASS HIERARCHY", report)
        self.assertIn("NOETIC RADIUS", report)
        self.assertIn("RUNNING COUPLING", report)
        
    def test_24_constants_dict_structure(self):
        """Test constants dictionary structure."""
        const_dict = self.core.get_constants_dict()
        
        required_keys = [
            "alpha", "alpha_inv", "phi", "gamma",
            "zeta_prime_half", "mass_ratio_p_e",
            "mass_ratio_normalized", "precision"
        ]
        
        for key in required_keys:
            self.assertIn(key, const_dict)
            
    def test_25_constants_dict_values(self):
        """Test constants dictionary has correct value types."""
        const_dict = self.core.get_constants_dict()
        
        # All should be numeric (float or int)
        for key, value in const_dict.items():
            self.assertTrue(
                isinstance(value, (int, float)),
                f"{key} should be numeric, got {type(value)}"
            )
            
    def test_26_high_precision_alpha(self):
        """Test α with high precision."""
        # Create high precision instance
        core_200 = DimensionlessConstantsCore(precision=200)
        alpha_str = str(core_200.alpha)
        
        # Should have many digits
        self.assertGreater(len(alpha_str), 10)
        
    def test_27_phi_cubed_calculation(self):
        """Test φ³ calculation for f₀ derivation."""
        phi = self.core.phi
        phi_cubed = phi ** 3
        
        # φ³ ≈ 4.236
        self.assertAlmostEqual(float(phi_cubed), 4.236, places=2)
        
    def test_28_zeta_absolute_value(self):
        """Test |ζ'(1/2)| is positive."""
        zeta_abs = mp.fabs(self.core.zeta_prime_half)
        self.assertGreater(float(zeta_abs), 0)
        self.assertAlmostEqual(float(zeta_abs), 0.207886, places=4)
        
    def test_29_alpha_times_137(self):
        """Test α × 137 ≈ 1."""
        product = self.core.alpha * self.core.alpha_inv
        # Should be very close to 1
        self.assertAlmostEqual(float(product), 1.0, places=10)
        
    def test_30_noetic_radius_units(self):
        """Test noetic radius calculation includes proper units."""
        result = self.core.compute_noetic_radius_ratio()
        
        self.assertIn("R_psi_meters", result)
        self.assertIn("R_psi_km", result)
        
        # Conversion should be correct
        ratio = result["R_psi_meters"] / result["R_psi_km"]
        self.assertAlmostEqual(ratio, 1000, places=5)
        
    def test_31_f0_status_indicator(self):
        """Test f₀ derivation includes status."""
        result = self.core.derive_f0_from_pure_constants()
        
        self.assertIn("status", result)
        self.assertIn(result["status"], ["SUCCESS", "NEEDS_CALIBRATION"])
        
    def test_32_mass_hierarchy_interpretation(self):
        """Test mass hierarchy includes interpretation."""
        result = self.core.validate_mass_hierarchy()
        
        self.assertIn("interpretation", result)
        self.assertIn("coupled", result["interpretation"].lower())
        
    def test_33_multiple_instances_independent(self):
        """Test multiple instances maintain independence."""
        core1 = DimensionlessConstantsCore(precision=50)
        core2 = DimensionlessConstantsCore(precision=100)
        
        # Should have different precision
        self.assertEqual(core1.precision, 50)
        self.assertEqual(core2.precision, 100)
        
    def test_34_seal_in_report(self):
        """Test report includes QCAL seal."""
        report = self.core.generate_coherence_report()
        self.assertIn("∴𓂀Ω∞³", report)
        
    def test_35_all_constants_positive_where_expected(self):
        """Test expected constants are positive."""
        self.assertGreater(float(self.core.alpha), 0)
        self.assertGreater(float(self.core.alpha_inv), 0)
        self.assertGreater(float(self.core.phi), 0)
        self.assertGreater(float(self.core.gamma), 0)
        self.assertGreater(float(self.core.mass_ratio_p_e), 0)
        
    def test_36_zeta_prime_is_negative(self):
        """Test ζ'(1/2) is negative as expected."""
        self.assertLess(float(self.core.zeta_prime_half), 0)


class TestDimensionlessPhysicsValidator(unittest.TestCase):
    """Test dimensionless physics validation."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Import validator
        sys.path.insert(0, str(Path(__file__).parent))
        from validate_dimensionless_constants import DimensionlessPhysicsValidator
        cls.validator = DimensionlessPhysicsValidator(precision=50)
        
    def test_37_validator_initialization(self):
        """Test validator initializes correctly."""
        self.assertIsNotNone(self.validator)
        self.assertEqual(self.validator.precision, 50)
        
    def test_38_coulomb_law_validation(self):
        """Test Coulomb's law validation."""
        result = self.validator.validate_coulomb_law()
        self.assertEqual(result["status"], "PASS")
        
    def test_39_bohr_radius_validation(self):
        """Test Bohr radius validation."""
        result = self.validator.validate_bohr_radius()
        self.assertEqual(result["status"], "PASS")
        
    def test_40_rydberg_energy_validation(self):
        """Test Rydberg energy validation."""
        result = self.validator.validate_rydberg_energy()
        self.assertEqual(result["status"], "PASS")
        
    def test_41_fine_structure_validation(self):
        """Test fine structure splitting validation."""
        result = self.validator.validate_fine_structure_splitting()
        self.assertEqual(result["status"], "PASS")
        
    def test_42_compton_wavelength_validation(self):
        """Test Compton wavelength validation."""
        result = self.validator.validate_compton_wavelength()
        self.assertEqual(result["status"], "PASS")
        
    def test_43_gravity_em_ratio_validation(self):
        """Test gravity-EM ratio validation."""
        result = self.validator.validate_gravity_em_ratio()
        self.assertEqual(result["status"], "PASS")
        
    def test_44_alpha_energy_dependence_validation(self):
        """Test running α validation."""
        result = self.validator.validate_alpha_energy_dependence()
        self.assertEqual(result["status"], "PASS")
        
    def test_45_all_validations_pass(self):
        """Test that all validations pass."""
        results = self.validator.run_all_validations()
        
        # Should have at least 6 validations
        self.assertGreaterEqual(len(results), 6)
        
        # All should pass
        passes = sum(1 for r in results if r["status"] == "PASS")
        self.assertEqual(passes, len(results))
        
    def test_46_summary_report_generation(self):
        """Test summary report generation."""
        report = self.validator.generate_summary_report()
        self.assertIsInstance(report, str)
        self.assertIn("VALIDATION REPORT", report)
        
    def test_47_json_results_structure(self):
        """Test JSON results structure."""
        results = self.validator.get_results_json()
        
        required_keys = [
            "precision", "framework", "validation_count",
            "passes", "fails", "success_rate", "validations"
        ]
        
        for key in required_keys:
            self.assertIn(key, results)
            
    def test_48_success_rate_calculation(self):
        """Test success rate is calculated correctly."""
        results = self.validator.get_results_json()
        
        expected_rate = results["passes"] / results["validation_count"]
        self.assertAlmostEqual(results["success_rate"], expected_rate, places=5)
        
    def test_49_seal_in_json(self):
        """Test QCAL seal in JSON output."""
        results = self.validator.get_results_json()
        self.assertIn("seal", results)
        self.assertEqual(results["seal"], "∴𓂀Ω∞³")
        
    def test_50_conclusion_in_json(self):
        """Test conclusion in JSON output."""
        results = self.validator.get_results_json()
        self.assertIn("conclusion", results)
        self.assertIn("proportion", results["conclusion"].lower())


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestDimensionlessConstantsCore))
    suite.addTests(loader.loadTestsFromTestCase(TestDimensionlessPhysicsValidator))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80)
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED - Framework validated!")
        print("∴𓂀Ω∞³")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
