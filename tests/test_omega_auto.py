#!/usr/bin/env python3
"""
Test suite for Omega ∞³ Auto-Validation Engine
==============================================

Tests for omega_auto.py module covering:
- PSD computation
- SNR calculation
- Data integrity hashing
- NFT metadata generation
- Validation workflows

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
License: MIT
"""

import unittest
import json
import sys
import os
import numpy as np
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from omega_auto import (
    omega_psd,
    omega_snr,
    compute_ipfs_hash,
    generate_nft_metadata,
    omega_validate_simulation,
    omega_validate,
    F0_TARGET,
    DF_TOLERANCE,
    SNR_THRESHOLD
)


class TestOmegaPSD(unittest.TestCase):
    """Test PSD computation."""
    
    def test_psd_basic(self):
        """Test basic PSD computation."""
        # Generate synthetic signal
        fs = 4096
        duration = 4
        t = np.linspace(0, duration, fs * duration)
        signal = np.sin(2 * np.pi * 100 * t) + 0.1 * np.random.randn(len(t))
        
        freqs, psd = omega_psd(signal, fs)
        
        self.assertEqual(len(freqs), len(psd))
        self.assertGreater(len(freqs), 0)
        self.assertTrue(np.all(psd >= 0))
    
    def test_psd_frequency_resolution(self):
        """Test frequency resolution of PSD."""
        fs = 4096
        duration = 8
        t = np.linspace(0, duration, fs * duration)
        signal = np.sin(2 * np.pi * F0_TARGET * t)
        
        freqs, psd = omega_psd(signal, fs)
        
        # Check that target frequency is in range
        self.assertGreater(np.max(freqs), F0_TARGET)
        self.assertLess(np.min(freqs), F0_TARGET)


class TestOmegaSNR(unittest.TestCase):
    """Test SNR calculation."""
    
    def test_snr_calculation(self):
        """Test SNR calculation with known signal."""
        # Create frequency array and PSD with peak at target
        freqs = np.linspace(0, 500, 10000)
        psd = np.ones_like(freqs) * 0.1
        
        # Add signal at target frequency
        mask = np.abs(freqs - F0_TARGET) < 0.1
        psd[mask] = 10.0
        
        snr = omega_snr(freqs, psd, F0_TARGET, DF_TOLERANCE)
        
        self.assertGreater(snr, SNR_THRESHOLD)
        self.assertIsInstance(snr, float)
    
    def test_snr_no_signal(self):
        """Test SNR with pure noise."""
        freqs = np.linspace(0, 500, 10000)
        psd = np.ones_like(freqs) * 0.1
        
        snr = omega_snr(freqs, psd, F0_TARGET, DF_TOLERANCE)
        
        # SNR should be close to 1 for uniform noise
        self.assertLess(snr, 2.0)
        self.assertGreater(snr, 0.5)


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and hashing."""
    
    def test_ipfs_hash_generation(self):
        """Test IPFS hash generation."""
        data = {"event": "GW150914", "snr": {"H1": 18.5, "L1": 17.2}}
        hash1 = compute_ipfs_hash(data)
        hash2 = compute_ipfs_hash(data)
        
        # Same data should give same hash
        self.assertEqual(hash1, hash2)
        self.assertTrue(hash1.startswith("Qm"))
        self.assertEqual(len(hash1), 46)  # Qm + 44 hex chars
    
    def test_ipfs_hash_uniqueness(self):
        """Test that different data gives different hashes."""
        data1 = {"event": "GW150914", "snr": 18.5}
        data2 = {"event": "GW151226", "snr": 22.3}
        
        hash1 = compute_ipfs_hash(data1)
        hash2 = compute_ipfs_hash(data2)
        
        self.assertNotEqual(hash1, hash2)


class TestNFTMetadata(unittest.TestCase):
    """Test NFT metadata generation."""
    
    def test_nft_metadata_structure(self):
        """Test NFT metadata has correct structure."""
        event = "GW150914"
        results = {
            "event": event,
            "snr": {"H1": 18.5, "L1": 17.2},
            "ipfs_hash": "QmTest123"
        }
        
        metadata = generate_nft_metadata(event, results)
        
        # Check schema.org structure
        self.assertEqual(metadata["@context"], "https://schema.org")
        self.assertEqual(metadata["@type"], "ScholarlyArticle")
        self.assertIn("Omega-Validation-141Hz", metadata["name"])
        
        # Check measurements
        self.assertIn("variableMeasured", metadata)
        self.assertIsInstance(metadata["variableMeasured"], list)
        
        # Check for f0 measurement
        f0_found = False
        for measurement in metadata["variableMeasured"]:
            if measurement["name"] == "f0":
                self.assertEqual(measurement["value"], F0_TARGET)
                self.assertEqual(measurement["unitText"], "Hz")
                f0_found = True
        self.assertTrue(f0_found)
    
    def test_nft_metadata_snr_values(self):
        """Test SNR values are included in NFT metadata."""
        results = {
            "event": "GW150914",
            "snr": {"H1": 18.5, "L1": 17.2},
            "ipfs_hash": "QmTest123"
        }
        
        metadata = generate_nft_metadata("GW150914", results)
        
        # Check SNR measurements
        snr_h1_found = False
        snr_l1_found = False
        for measurement in metadata["variableMeasured"]:
            if measurement["name"] == "snr_h1":
                self.assertEqual(measurement["value"], 18.5)
                snr_h1_found = True
            if measurement["name"] == "snr_l1":
                self.assertEqual(measurement["value"], 17.2)
                snr_l1_found = True
        
        self.assertTrue(snr_h1_found)
        self.assertTrue(snr_l1_found)


class TestOmegaValidation(unittest.TestCase):
    """Test omega validation workflows."""
    
    def test_simulation_mode(self):
        """Test validation in simulation mode."""
        event = "GW150914"
        results = omega_validate_simulation(event)
        
        self.assertEqual(results["event"], event)
        self.assertIn("snr", results)
        self.assertIn("H1", results["snr"])
        self.assertIn("L1", results["snr"])
        self.assertIn("coherent", results)
        self.assertIn("ipfs_hash", results)
        self.assertEqual(results["mode"], "simulation")
    
    def test_simulation_reproducibility(self):
        """Test that simulation is reproducible."""
        event = "GW150914"
        results1 = omega_validate_simulation(event)
        results2 = omega_validate_simulation(event)
        
        # Same event should give same results
        self.assertEqual(results1["snr"]["H1"], results2["snr"]["H1"])
        self.assertEqual(results1["snr"]["L1"], results2["snr"]["L1"])
    
    def test_omega_validate_default(self):
        """Test main omega_validate function."""
        event = "GW150914"
        results = omega_validate(event, use_real_data=False)
        
        # Check all required fields
        self.assertIn("event", results)
        self.assertIn("snr", results)
        self.assertIn("coherent", results)
        self.assertIn("ipfs_hash", results)
        self.assertIn("nft_metadata", results)
        self.assertIn("timestamp", results)
        
        # Check timestamp format
        timestamp = datetime.fromisoformat(results["timestamp"])
        self.assertIsInstance(timestamp, datetime)
    
    def test_omega_validate_coherence(self):
        """Test coherence detection."""
        event = "GW150914"
        results = omega_validate_simulation(event)
        
        # Coherence should be boolean
        self.assertIsInstance(results["coherent"], bool)
        
        # Coherence logic: |H1 - L1| < 5.0
        snr_h1 = results["snr"]["H1"]
        snr_l1 = results["snr"]["L1"]
        expected_coherent = abs(snr_h1 - snr_l1) < 5.0
        self.assertEqual(results["coherent"], expected_coherent)


class TestConstants(unittest.TestCase):
    """Test module constants."""
    
    def test_f0_target(self):
        """Test F0_TARGET constant."""
        self.assertEqual(F0_TARGET, 141.7001)
    
    def test_df_tolerance(self):
        """Test DF_TOLERANCE constant."""
        self.assertEqual(DF_TOLERANCE, 0.5)
    
    def test_snr_threshold(self):
        """Test SNR_THRESHOLD constant."""
        self.assertEqual(SNR_THRESHOLD, 5.0)


def run_tests():
    """Run all tests and return results."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
