#!/usr/bin/env python3
"""
Tests for QCAL Master Integration & Certification

Tests the integrate_qcal_compact.py script to ensure hardware verification
integrates properly with master certification.

License: CERN-OHL-P v2
"""

import sys
import os
import subprocess
import unittest
import json

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.integrate_qcal_compact import (
    verify_bom_hardware_integration,
    generate_master_certificate,
    colored_output
)


class TestHardwareIntegration(unittest.TestCase):
    """Test hardware BOM integration with QCAL master."""
    
    def test_verify_bom_simulation_mode(self):
        """Test hardware verification in simulation mode."""
        result = verify_bom_hardware_integration(simulate=True)
        
        self.assertTrue(result.get('success'))
        self.assertTrue(result.get('i2c_si5351'))
        self.assertTrue(result.get('i2c_magnetometer'))
        self.assertTrue(result.get('gsr_integrity'))
        self.assertTrue(result.get('tpa3116_calib'))
        self.assertEqual(result.get('led_coherencia'), 1.0)
        self.assertTrue(result.get('serial_delays_configured'))
        self.assertEqual(result.get('codeql_vulns'), 0)
        self.assertEqual(result.get('licencia'), 'CERN-OHL-P v2')
        self.assertEqual(result.get('mode'), 'simulation')
    
    def test_generate_master_certificate(self):
        """Test master certificate generation."""
        hardware_cert = {
            'success': True,
            'i2c_si5351': True,
            'i2c_magnetometer': True,
            'gsr_integrity': True,
            'tpa3116_calib': True,
            'led_coherencia': 1.0,
            'serial_delays_configured': True,
            'codeql_vulns': 0,
            'licencia': 'CERN-OHL-P v2'
        }
        
        master_cert = generate_master_certificate(hardware_cert)
        
        self.assertEqual(master_cert['version'], '1.0.0')
        self.assertEqual(master_cert['frequency_hz'], 141.7001)
        self.assertEqual(master_cert['pilares'], 14)  # 13 + 1 hardware
        self.assertGreaterEqual(master_cert['qcal_unificada'], 0.999)
        
        # Check hardware components
        hw = master_cert['components']['hardware']
        self.assertTrue(hw['si5351_clock'])
        self.assertTrue(hw['magnetometer'])
        self.assertTrue(hw['gsr_sensor'])
        self.assertTrue(hw['tpa3116_amp'])
        self.assertTrue(hw['led_indicator'])
        self.assertTrue(hw['serial_comm'])
        
        # Check licenses
        self.assertEqual(master_cert['license']['software'], 'MIT')
        self.assertEqual(master_cert['license']['hardware'], 'CERN-OHL-P v2')
        
        # Check security
        self.assertEqual(master_cert['security']['codeql_vulnerabilities'], 0)
    
    def test_hardware_failure_reduces_coherence(self):
        """Test that hardware failure reduces QCAL unificada."""
        hardware_cert_fail = {
            'success': False,
            'error': 'Test failure'
        }
        
        master_cert = generate_master_certificate(hardware_cert_fail)
        
        # Should have 13 pillars (no hardware pillar)
        self.assertEqual(master_cert['pilares'], 13)
        
        # Coherence should be reduced
        self.assertLess(master_cert['qcal_unificada'], 0.9997)
        self.assertAlmostEqual(master_cert['qcal_unificada'], 0.9997 * 0.95, places=4)


class TestIntegrationCLI(unittest.TestCase):
    """Test the integration script command-line interface."""
    
    def test_integration_script_runs(self):
        """Test that the integration script runs successfully."""
        result = subprocess.run(
            [sys.executable, 'scripts/integrate_qcal_compact.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('QCAL MASTER CERTIFICATION: COMPLETE', result.stdout)
        self.assertIn('HARDWARE LIBRE: BOM VERIFICADO', result.stdout)
        self.assertIn('141.7001 Hz', result.stdout)
        self.assertIn('CERN-OHL-P v2', result.stdout)
        self.assertIn('Pillars: 14', result.stdout)
    
    def test_certificate_file_generated(self):
        """Test that master certificate JSON is generated."""
        cert_path = 'master_qcal_cert.json'
        
        # Clean up before test
        if os.path.exists(cert_path):
            os.remove(cert_path)
        
        try:
            # Run integration
            subprocess.run(
                [sys.executable, 'scripts/integrate_qcal_compact.py'],
                capture_output=True,
                timeout=30
            )
            
            # Check certificate file exists
            self.assertTrue(os.path.exists(cert_path))
            
            # Load and verify certificate
            with open(cert_path, 'r') as f:
                cert = json.load(f)
            
            self.assertEqual(cert['version'], '1.0.0')
            self.assertEqual(cert['frequency_hz'], 141.7001)
            self.assertEqual(cert['pilares'], 14)
            self.assertTrue(cert['hardware_bom']['success'])
            self.assertEqual(cert['hardware_bom']['licencia'], 'CERN-OHL-P v2')
        finally:
            # Clean up after test
            if os.path.exists(cert_path):
                os.remove(cert_path)


class TestColoredOutput(unittest.TestCase):
    """Test colored output function."""
    
    def test_colored_output_no_crash(self):
        """Test that colored_output doesn't crash."""
        try:
            colored_output("Test message", "GREEN")
            colored_output("Test message", "RED")
            colored_output("Test message", "BLUE")
            colored_output("Test message", "CYAN")
            colored_output("Test message", "YELLOW")
        except Exception as e:
            self.fail(f"colored_output raised exception: {e}")


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
