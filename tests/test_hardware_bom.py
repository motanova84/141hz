#!/usr/bin/env python3
"""
Tests for Hardware BOM Verification System

Tests the hardware verification module in simulation mode to ensure
all components are properly validated.

License: CERN-OHL-P v2
"""

import sys
import os
import subprocess
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hardware.verify_bom import (
    BOMVerifier, HardwareSimulator, F0_HZ, SI5351_I2C_ADDR,
    MAGNETOMETER_ADDR_1, GSR_PIN, LED_PIN
)


class TestHardwareSimulator(unittest.TestCase):
    """Test the hardware simulator."""
    
    def setUp(self):
        self.sim = HardwareSimulator()
    
    def test_i2c_scan(self):
        """Test I2C device scanning."""
        devices = self.sim.i2c_scan()
        self.assertIn(SI5351_I2C_ADDR, devices)
        self.assertIn(MAGNETOMETER_ADDR_1, devices)
    
    def test_analog_read(self):
        """Test analog pin reading."""
        value = self.sim.read_analog(GSR_PIN)
        self.assertGreaterEqual(value, 0)
        self.assertLessEqual(value, 1023)
        self.assertEqual(value, 512)  # Default simulated value
    
    def test_digital_write_read(self):
        """Test digital pin write and read."""
        self.sim.write_digital(LED_PIN, True)
        self.assertTrue(self.sim.read_digital(LED_PIN))
        
        self.sim.write_digital(LED_PIN, False)
        self.assertFalse(self.sim.read_digital(LED_PIN))
    
    def test_amplifier_burst(self):
        """Test amplifier burst simulation."""
        result = self.sim.test_amplifier_burst(1.0)
        self.assertEqual(result['frequency'], 1.0)
        self.assertLess(result['distortion'], 0.001)  # < 0.1%
        self.assertEqual(result['status'], 'PASS')


class TestBOMVerifier(unittest.TestCase):
    """Test the BOM verifier."""
    
    def setUp(self):
        self.verifier = BOMVerifier(simulate=True)
    
    def tearDown(self):
        self.verifier.close()
    
    def test_si5351_detection(self):
        """Test Si5351 clock generator detection."""
        result = self.verifier.test_i2c_si5351()
        self.assertTrue(result)
        self.assertTrue(self.verifier.results.get('si5351'))
    
    def test_magnetometer_detection(self):
        """Test magnetometer detection."""
        result = self.verifier.test_i2c_magnetometer()
        self.assertTrue(result)
        self.assertTrue(self.verifier.results.get('magnetometer'))
    
    def test_gsr_integrity(self):
        """Test GSR sensor integrity."""
        result = self.verifier.test_gsr_integrity()
        self.assertTrue(result)
        self.assertTrue(self.verifier.results.get('gsr_integrity'))
    
    def test_tpa3116_calibration(self):
        """Test TPA3116 amplifier calibration."""
        result = self.verifier.test_tpa3116_burst()
        self.assertTrue(result)
        self.assertTrue(self.verifier.results.get('tpa3116'))
    
    def test_led_coherence(self):
        """Test LED coherence."""
        result = self.verifier.test_led_coherence()
        self.assertTrue(result)
        self.assertEqual(self.verifier.results.get('led_coherence'), 1.0)
    
    def test_serial_delays(self):
        """Test serial delay configuration."""
        result = self.verifier.test_serial_delays()
        self.assertTrue(result)
        self.assertTrue(self.verifier.results.get('serial_delays'))
    
    def test_all_tests(self):
        """Test running all verification tests."""
        passed, total = self.verifier.run_all_tests()
        self.assertEqual(passed, 6)
        self.assertEqual(total, 6)
        self.assertEqual(passed, total)


class TestBOMVerifierCLI(unittest.TestCase):
    """Test the command-line interface."""
    
    def test_simulate_mode(self):
        """Test CLI in simulation mode."""
        result = subprocess.run(
            ['python3', 'hardware/verify_bom.py', '--simulate'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('VERIFICADO', result.stdout)
        self.assertIn('6/6 PASS', result.stdout)
        self.assertIn('CERN-OHL-P v2', result.stdout)
        self.assertIn('CodeQL vulnerabilities: 0', result.stdout)
        self.assertIn(f'{F0_HZ} Hz', result.stdout)
    
    def test_help_option(self):
        """Test CLI help option."""
        result = subprocess.run(
            ['python3', 'hardware/verify_bom.py', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('--simulate', result.stdout)
        self.assertIn('--port', result.stdout)
        self.assertIn('CERN-OHL-P v2', result.stdout)
    
    def test_port_required_without_simulate(self):
        """Test that port is required when not in simulate mode."""
        result = subprocess.run(
            ['python3', 'hardware/verify_bom.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--port', result.stderr)


class TestConstants(unittest.TestCase):
    """Test hardware constants."""
    
    def test_f0_frequency(self):
        """Test F0 frequency constant."""
        self.assertAlmostEqual(F0_HZ, 141.7001, places=4)
    
    def test_i2c_addresses(self):
        """Test I2C address constants."""
        self.assertEqual(SI5351_I2C_ADDR, 0x60)
        self.assertEqual(MAGNETOMETER_ADDR_1, 0x1E)
    
    def test_pin_numbers(self):
        """Test pin number constants."""
        self.assertEqual(GSR_PIN, 0)  # A0
        self.assertEqual(LED_PIN, 13)  # D13


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
