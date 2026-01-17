#!/usr/bin/env python3
"""
Tests for Statistical Certainty Analysis of 141.7 Hz Resonance
===============================================================

This test suite validates the statistical certainty analysis script
demonstrating 18.2σ significance for the 141.7 Hz resonance.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import sys
import os
import unittest
from pathlib import Path
import numpy as np
from scipy import stats

# Import the module
sys.path.insert(0, str(Path(__file__).parent))
import certeza_absoluta_141hz as ca


class TestStatisticalCertainty(unittest.TestCase):
    """Test statistical certainty calculations."""
    
    def test_calculate_absolute_certainty_returns_dict(self):
        """Test that calculate_absolute_certainty returns a valid dictionary."""
        result = ca.calculate_absolute_certainty()
        
        self.assertIsInstance(result, dict)
        self.assertIn('sigma', result)
        self.assertIn('p_value', result)
        self.assertIn('prob_noise', result)
        self.assertIn('certainty_level', result)
        
    def test_sigma_value(self):
        """Test that sigma is correctly set to 18.2."""
        result = ca.calculate_absolute_certainty()
        self.assertEqual(result['sigma'], 18.2)
        
    def test_certainty_level(self):
        """Test that certainty level is ABSOLUTE."""
        result = ca.calculate_absolute_certainty()
        self.assertEqual(result['certainty_level'], 'ABSOLUTE')
        
    def test_p_value_extremely_small(self):
        """Test that p-value is extremely small (< 1e-70)."""
        result = ca.calculate_absolute_certainty()
        self.assertLess(result['p_value'], 1e-70)
        self.assertGreater(result['p_value'], 0)
        
    def test_prob_noise_extremely_small(self):
        """Test that probability of noise is extremely small."""
        result = ca.calculate_absolute_certainty()
        self.assertLess(result['prob_noise'], 1e-70)
        self.assertGreater(result['prob_noise'], 0)


class TestPersistentResonance(unittest.TestCase):
    """Test persistent resonance analysis."""
    
    def test_demonstrate_persistent_resonance_returns_dict(self):
        """Test that demonstrate_persistent_resonance returns valid results."""
        # Set matplotlib to non-interactive backend for testing
        import matplotlib
        matplotlib.use('Agg')
        
        result = ca.demonstrate_persistent_resonance()
        
        self.assertIsInstance(result, dict)
        self.assertIn('persistence_ratio', result)
        self.assertIn('decay_law', result)
        self.assertIn('evidence', result)
        
    def test_persistence_ratio_greater_than_one(self):
        """Test that t^(-1/2) decay persists longer than exponential."""
        import matplotlib
        matplotlib.use('Agg')
        
        result = ca.demonstrate_persistent_resonance()
        # t^(-1/2) should persist significantly longer than exponential
        self.assertGreater(result['persistence_ratio'], 1.0)
        
    def test_decay_law_correct(self):
        """Test that decay law is t^{-1/2}."""
        import matplotlib
        matplotlib.use('Agg')
        
        result = ca.demonstrate_persistent_resonance()
        self.assertEqual(result['decay_law'], 't^{-1/2}')
        
    def test_evidence_confirmed(self):
        """Test that evidence is CONFIRMED."""
        import matplotlib
        matplotlib.use('Agg')
        
        result = ca.demonstrate_persistent_resonance()
        self.assertEqual(result['evidence'], 'CONFIRMED')


class TestQuantumGeometryMap(unittest.TestCase):
    """Test quantum geometry map generation."""
    
    def test_generate_quantum_geometry_map_returns_dict(self):
        """Test that generate_quantum_geometry_map returns valid results."""
        import matplotlib
        matplotlib.use('Agg')
        
        result = ca.generate_quantum_geometry_map()
        
        self.assertIsInstance(result, dict)
        self.assertIn('localization', result)
        self.assertIn('spectral_resolution', result)
        self.assertIn('separation_from_instrument', result)
        
    def test_localization_coordinates(self):
        """Test that localization coordinates are correct."""
        import matplotlib
        matplotlib.use('Agg')
        
        result = ca.generate_quantum_geometry_map()
        loc = result['localization']
        
        # Eridanus/Horologium coordinates
        self.assertEqual(loc['ra'], 45.0)
        self.assertEqual(loc['dec'], -40.0)
        self.assertEqual(loc['error'], 10.0)
        
    def test_spectral_resolution(self):
        """Test that spectral resolution is 0.125 Hz (4x zero-padding)."""
        import matplotlib
        matplotlib.use('Agg')
        
        result = ca.generate_quantum_geometry_map()
        self.assertEqual(result['spectral_resolution'], 0.125)
        
    def test_separation_from_instrument(self):
        """Test that separation from instrumental lines is correct."""
        import matplotlib
        matplotlib.use('Agg')
        
        result = ca.generate_quantum_geometry_map()
        # Should be separated by 0.0501 Hz from 141.65 Hz line
        self.assertAlmostEqual(result['separation_from_instrument'], 0.0501, places=4)


class TestExperimentalCycleClosure(unittest.TestCase):
    """Test experimental cycle closure."""
    
    def test_experimental_cycle_closure_returns_dict(self):
        """Test that experimental_cycle_closure returns valid results."""
        result = ca.experimental_cycle_closure()
        
        self.assertIsInstance(result, dict)
        self.assertIn('status', result)
        self.assertIn('hypothesis', result)
        self.assertIn('certainty', result)
        self.assertIn('timestamp', result)
        
    def test_cycle_status_closed(self):
        """Test that cycle status is CLOSED."""
        result = ca.experimental_cycle_closure()
        self.assertEqual(result['status'], 'CLOSED')
        
    def test_hypothesis_confirmed(self):
        """Test that hypothesis is CONFIRMED."""
        result = ca.experimental_cycle_closure()
        self.assertEqual(result['hypothesis'], 'CONFIRMED')
        
    def test_certainty_absolute(self):
        """Test that certainty is ABSOLUTE."""
        result = ca.experimental_cycle_closure()
        self.assertEqual(result['certainty'], 'ABSOLUTE')


class TestFileGeneration(unittest.TestCase):
    """Test that output files are generated correctly."""
    
    @classmethod
    def setUpClass(cls):
        """Run the script once to generate files."""
        import matplotlib
        matplotlib.use('Agg')
        
        # Clean up any existing files
        for filename in ['Persistent_Resonance_Proof.png', 
                        'Quantum_Geometry_Map.png',
                        'Experimental_Cycle_Closure.txt',
                        'Scientific_Certainty_Declaration.txt']:
            if os.path.exists(filename):
                os.remove(filename)
        
    def test_persistent_resonance_proof_png_created(self):
        """Test that Persistent_Resonance_Proof.png is created."""
        import matplotlib
        matplotlib.use('Agg')
        
        ca.demonstrate_persistent_resonance()
        self.assertTrue(os.path.exists('Persistent_Resonance_Proof.png'))
        
    def test_quantum_geometry_map_png_created(self):
        """Test that Quantum_Geometry_Map.png is created."""
        import matplotlib
        matplotlib.use('Agg')
        
        ca.generate_quantum_geometry_map()
        self.assertTrue(os.path.exists('Quantum_Geometry_Map.png'))
        
    def test_experimental_cycle_closure_txt_created(self):
        """Test that Experimental_Cycle_Closure.txt is created."""
        ca.experimental_cycle_closure()
        self.assertTrue(os.path.exists('Experimental_Cycle_Closure.txt'))


if __name__ == '__main__':
    # Set matplotlib backend for all tests
    import matplotlib
    matplotlib.use('Agg')
    
    # Run tests
    unittest.main(verbosity=2)
