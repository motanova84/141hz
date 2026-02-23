#!/usr/bin/env python3
"""
Test suite for validate_tres_puertas.py

Validates the Three Doors implementation for Riemann Hypothesis
spectral validation.
"""

import json
import os
import sys
import unittest
from pathlib import Path
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import validate_tres_puertas as vtp
except ImportError:
    print("❌ Error: Cannot import validate_tres_puertas")
    sys.exit(1)

try:
    import mpmath as mp
except ImportError:
    print("❌ Error: mpmath is required for tests")
    sys.exit(1)


class TestPuertaUno(unittest.TestCase):
    """Test cases for Puerta 1 (ξ(s) as Spectral Function)."""

    def setUp(self):
        """Set up test fixtures."""
        self.puerta1 = vtp.PuertaUno(precision=30)

    def test_odlyzko_zeros_loaded(self):
        """Test that Odlyzko reference zeros are loaded correctly."""
        zeros = self.puerta1.odlyzko_zeros
        
        self.assertEqual(len(zeros), 5)
        
        # First zero should be approximately 14.1347251417346937904572519836
        first_zero = float(zeros[0])
        self.assertAlmostEqual(first_zero, 14.134725, places=5)
        
        # Zeros should be in ascending order
        for i in range(len(zeros) - 1):
            self.assertLess(zeros[i], zeros[i + 1])

    def test_xi_riemann_at_zero(self):
        """Test that ξ(s) is close to zero at known zero."""
        # First Riemann zero at t ≈ 14.134725
        s = mp.mpc(0.5, 14.134725)
        xi_val = self.puerta1._xi_riemann(s)
        
        # Should be very close to zero
        self.assertLess(abs(xi_val), 1e-3)

    def test_pt_symmetry_structure(self):
        """Test that PT symmetry validation returns correct structure."""
        zeros = [mp.mpf(14.134725), mp.mpf(21.022040)]
        results = self.puerta1.validate_pt_symmetry(zeros)
        
        self.assertIn("symmetry_validated", results)
        self.assertIn("max_error", results)
        self.assertIn("errors", results)
        self.assertIsInstance(results["symmetry_validated"], bool)

    def test_comparison_structure(self):
        """Test that Odlyzko comparison returns correct structure."""
        computed = [mp.mpf(14.134725), mp.mpf(21.022040)]
        results = self.puerta1.compare_with_odlyzko(computed)
        
        self.assertIn("comparisons", results)
        self.assertIn("max_difference", results)
        self.assertIn("precision_validated", results)
        self.assertEqual(len(results["comparisons"]), 2)


class TestPuertaDos(unittest.TestCase):
    """Test cases for Puerta 2 (Trace and Prime Sum)."""

    def setUp(self):
        """Set up test fixtures."""
        self.puerta2 = vtp.PuertaDos(n_zeros=100)

    def test_zeros_loaded(self):
        """Test that Riemann zeros are loaded correctly."""
        zeros = self.puerta2.zeros
        
        self.assertEqual(len(zeros), 100)
        
        # First zero should be approximately 14.134725
        self.assertAlmostEqual(zeros[0], 14.134725, places=5)
        
        # Zeros should be in ascending order
        for i in range(len(zeros) - 1):
            self.assertLess(zeros[i], zeros[i + 1])

    def test_spacing_statistics(self):
        """Test spacing statistics computation."""
        results = self.puerta2.compute_spacing_statistics()
        
        self.assertIn("variance", results)
        self.assertIn("variance_theoretical", results)
        self.assertIn("consistent_with_gue", results)
        
        # Variance should be positive
        self.assertGreater(results["variance"], 0)
        
        # Theoretical variance should be 0.18
        self.assertAlmostEqual(results["variance_theoretical"], 0.18, places=2)

    def test_rigidity_computation(self):
        """Test rigidity computation."""
        results = self.puerta2.compute_rigidity()
        
        self.assertIn("rigidity", results)
        self.assertIn("L", results)
        self.assertIn("consistent_with_gue", results)
        
        # Rigidity should be positive
        self.assertGreater(results["rigidity"], 0)

    def test_von_mangoldt_connection(self):
        """Test von Mangoldt formula connection."""
        results = self.puerta2.von_mangoldt_connection()
        
        self.assertIn("mean_density", results)
        self.assertIn("theoretical_density", results)
        self.assertIn("connection_validated", results)
        
        # Densities should be positive
        self.assertGreater(results["mean_density"], 0)
        self.assertGreater(results["theoretical_density"], 0)


class TestPuertaTres(unittest.TestCase):
    """Test cases for Puerta 3 (Emanating Code)."""

    def setUp(self):
        """Set up test fixtures."""
        self.puerta3 = vtp.PuertaTres()

    def test_frequency_validation(self):
        """Test frequency resonance validation."""
        results = self.puerta3.validate_frequency_resonance()
        
        self.assertIn("f0_hz", results)
        self.assertIn("expected", results)
        self.assertIn("validated", results)
        
        # f0 should be 141.7001
        self.assertAlmostEqual(results["f0_hz"], 141.7001, places=4)

    def test_curvature_validation(self):
        """Test curvature validation."""
        results = self.puerta3.validate_curvature()
        
        self.assertIn("kappa_pi", results)
        self.assertIn("expected", results)
        self.assertIn("validated", results)
        
        # κ_Π should be approximately 2.5782
        self.assertAlmostEqual(results["kappa_pi"], 2.5782, places=3)

    def test_coherence_computation(self):
        """Test coherence computation."""
        results = self.puerta3.compute_coherence()
        
        self.assertIn("psi", results)
        self.assertIn("manifested", results)
        
        # Coherence should be 1.0 for full manifestation
        self.assertAlmostEqual(results["psi"], 1.0, places=6)

    def test_seal_generation(self):
        """Test seal generation."""
        seal = self.puerta3.generate_seal()
        
        self.assertIsInstance(seal, str)
        self.assertEqual(seal, "∴𓂀Ω∞³Φ")


class TestTresPuertasValidator(unittest.TestCase):
    """Test cases for complete Three Doors validator."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = vtp.TresPuertasValidator(precision=30)

    def test_validator_initialization(self):
        """Test validator initialization."""
        self.assertIsNotNone(self.validator.puerta1)
        self.assertIsNotNone(self.validator.puerta2)
        self.assertIsNotNone(self.validator.puerta3)
        self.assertEqual(self.validator.precision, 30)

    def test_execute_all_structure(self):
        """Test that execute_all returns correct structure."""
        results = self.validator.execute_all()
        
        self.assertIn("timestamp", results)
        self.assertIn("precision", results)
        self.assertIn("puerta_1", results)
        self.assertIn("puerta_2", results)
        self.assertIn("puerta_3", results)
        self.assertIn("status", results)
        
        # Each puerta should have a status
        self.assertIn("status", results["puerta_1"])
        self.assertIn("status", results["puerta_2"])
        self.assertIn("status", results["puerta_3"])

    def test_certificate_generation(self):
        """Test certificate generation."""
        # Execute validation first
        self.validator.execute_all()
        
        # Generate certificate
        certificate = self.validator.generate_certificate()
        
        self.assertIsInstance(certificate, str)
        self.assertIn("REGISTRO DE MANIFESTACIÓN", certificate)
        self.assertIn("QCAL∞³", certificate)
        self.assertIn("∴𓂀Ω∞³Φ", certificate)
        self.assertIn("141.7001", certificate)
        self.assertIn("2.5782", certificate)

    def test_global_status_computation(self):
        """Test global status computation."""
        r1 = {"status": "MANIFESTADO"}
        r2 = {"status": "MANIFESTADO"}
        r3 = {"status": "MANIFESTADO"}
        
        status = self.validator._compute_global_status(r1, r2, r3)
        self.assertEqual(status, "MANIFESTACIÓN ANALÍTICA COMPLETA")
        
        # Test partial manifestation
        r1["status"] = "PARCIAL"
        status = self.validator._compute_global_status(r1, r2, r3)
        self.assertEqual(status, "MANIFESTACIÓN PARCIAL")


class TestConstants(unittest.TestCase):
    """Test QCAL constants used in validation."""

    def test_f0_value(self):
        """Test F0_HZ constant."""
        self.assertAlmostEqual(vtp.F0_HZ, 141.7001, places=4)

    def test_kappa_pi_value(self):
        """Test KAPPA_PI constant."""
        self.assertAlmostEqual(vtp.KAPPA_PI, 2.5782, places=4)

    def test_phi_value(self):
        """Test PHI (golden ratio) constant."""
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(vtp.PHI, expected_phi, places=10)


if __name__ == "__main__":
    unittest.main()
