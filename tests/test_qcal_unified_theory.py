#!/usr/bin/env python3
"""
Test suite for QCAL Unified Theory module integration.

Verifies that the unified theory classes are properly exposed
through the qcal package and work correctly.
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestQCALUnifiedTheoryIntegration(unittest.TestCase):
    """Test QCAL module unified theory integration."""
    
    def test_import_from_qcal(self):
        """Test that UnifiedTheory can be imported from qcal package."""
        try:
            from qcal import UnifiedTheory
        except ImportError as e:
            self.fail(f"Failed to import UnifiedTheory from qcal: {e}")
    
    def test_import_all_components(self):
        """Test that all unified theory components can be imported."""
        from qcal import (
            UnifiedTheoryConstants,
            RiemannZetaComponent,
            CalabiYauComponent,
            FrequencyComponent,
            ConsciousnessComponent,
            GravityComponent,
            SpectrumComponent,
            CondensedMatterComponent,
            UnifiedTheory
        )
    
    def test_unified_theory_initialization(self):
        """Test UnifiedTheory class initialization."""
        from qcal import UnifiedTheory
        
        theory = UnifiedTheory()
        self.assertEqual(theory.f0, 141.7001)
        self.assertIsNotNone(theory.constants)
        self.assertIsNotNone(theory.zeta)
        self.assertIsNotNone(theory.calabi_yau)
        self.assertIsNotNone(theory.frequency)
        self.assertIsNotNone(theory.consciousness)
        self.assertIsNotNone(theory.gravity)
        self.assertIsNotNone(theory.spectrum)
        self.assertIsNotNone(theory.condensed_matter)
    
    def test_unified_theory_constants(self):
        """Test UnifiedTheoryConstants class."""
        from qcal import UnifiedTheoryConstants
        
        constants = UnifiedTheoryConstants()
        self.assertEqual(constants.f0, 141.7001)
        self.assertIsNotNone(constants.omega_0)
        self.assertIsNotNone(constants.lambda_psi)
        self.assertIsNotNone(constants.R_psi)
        
        # Check derived values are calculated
        import math
        expected_omega = 2 * math.pi * 141.7001
        self.assertAlmostEqual(constants.omega_0, expected_omega, places=4)
    
    def test_riemann_component(self):
        """Test RiemannZetaComponent."""
        from qcal import RiemannZetaComponent
        
        zeta = RiemannZetaComponent()
        
        # Test first overtone
        f1 = zeta.riemann_overtone_frequency(1)
        expected_f1 = 14.134725 * 141.7001
        self.assertAlmostEqual(f1, expected_f1, places=2)
        
        # Test get all overtones
        overtones = zeta.get_all_overtones()
        self.assertEqual(len(overtones), 20)
        self.assertEqual(overtones[0]["n"], 1)
    
    def test_gravity_component(self):
        """Test GravityComponent."""
        from qcal import GravityComponent
        
        gravity = GravityComponent()
        
        # Test Yukawa correction
        r = 384400e3  # Earth-Moon distance
        correction = gravity.yukawa_correction(r)
        self.assertIn("lambda_yukawa_km", correction)
        self.assertGreater(correction["lambda_yukawa_km"], 300)
        self.assertLess(correction["lambda_yukawa_km"], 400)
        
        # Test GW prediction
        gw_pred = gravity.gravitational_wave_prediction()
        self.assertEqual(gw_pred["frequency_Hz"], 141.7001)
        self.assertIn("LIGO Hanford", gw_pred["detectors"])
    
    def test_consciousness_component(self):
        """Test ConsciousnessComponent."""
        from qcal import ConsciousnessComponent
        
        consciousness = ConsciousnessComponent()
        
        # Test information integration
        integration = consciousness.information_integration(A_eff=0.95)
        self.assertEqual(integration["A_eff"], 0.95)
        self.assertEqual(integration["coherence_level"], "maximum")
        
        # Test decoherence time extension
        deco = consciousness.decoherence_time_extension()
        self.assertGreater(deco["enhancement_factor"], 1.0)
        self.assertTrue(deco["falsifiable"])
    
    def test_cyclic_relationship(self):
        """Test cyclic relationship structure."""
        from qcal import UnifiedTheory
        
        theory = UnifiedTheory()
        cycle = theory.cyclic_relationship()
        
        self.assertIn("cycle", cycle)
        self.assertIn("connections", cycle)
        self.assertEqual(len(cycle["cycle"]), 7)  # 6 components + closing loop
        self.assertEqual(cycle["cycle"][0], "Number (ζ)")
        self.assertEqual(cycle["cycle"][-1], "Number (ζ)")
    
    def test_falsifiable_predictions(self):
        """Test that all falsifiable predictions are present."""
        from qcal import UnifiedTheory
        
        theory = UnifiedTheory()
        predictions = theory.all_falsifiable_predictions()
        
        self.assertIn("gravitational_waves", predictions)
        self.assertIn("yukawa_correction", predictions)
        self.assertIn("quantum_coherence", predictions)
        self.assertIn("condensed_matter", predictions)
        self.assertIn("riemann_overtones", predictions)
    
    def test_generate_report(self):
        """Test report generation."""
        from qcal import UnifiedTheory
        
        theory = UnifiedTheory()
        report = theory.generate_report()
        
        self.assertIn("title", report)
        self.assertIn("version", report)
        self.assertIn("fundamental_frequency", report)
        self.assertIn("cyclic_relationship", report)
        self.assertIn("falsifiable_predictions", report)
        self.assertEqual(report["fundamental_frequency"]["value_Hz"], 141.7001)
    
    def test_qcal_constants_available(self):
        """Test that fundamental constants are available from qcal."""
        import qcal
        
        self.assertEqual(qcal.F0, 141.7001)
        self.assertAlmostEqual(qcal.PHI, 1.618033988749895, places=10)
        self.assertTrue(hasattr(qcal, 'KAPPA_PI'))
        self.assertTrue(hasattr(qcal, 'PSI_RESONANCE'))


class TestUnifiedTheoryAvailabilityFlag(unittest.TestCase):
    """Test that the availability flag is properly set."""
    
    def test_unified_theory_available_flag(self):
        """Test UNIFIED_THEORY_AVAILABLE flag."""
        import qcal
        
        self.assertTrue(hasattr(qcal, 'UNIFIED_THEORY_AVAILABLE'))
        self.assertTrue(qcal.UNIFIED_THEORY_AVAILABLE)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
