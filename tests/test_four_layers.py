#!/usr/bin/env python3
"""
Unit tests for the four-layer QCAL architecture.

Tests all components of the four layers to ensure correctness.
"""

import unittest
import sys
import os
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from four_layers import (
    # CAPA 1
    RiemannOperatorSpectrum,
    NumberTheoryDerivation,
    AdelicGeometry,
    PiCodeAlgebra,
    # CAPA 2
    GW250114RingdownAnalysis,
    SpacetimeResonance,
    CoherencePsiObservable,
    FundamentalPulses,
    # CAPA 3
    NativeFrequencyHardware,
    CoherentRegisters,
    PhaseMemory,
    ResonanceProcessor,
    # CAPA 4
    NodeSynchronization,
    PiCodeValue,
    DistributedRecognition,
    SymbioticEconomy,
    NodeType,
)


class TestCapa1MathematicalFoundations(unittest.TestCase):
    """Test mathematical foundations layer."""
    
    def test_riemann_spectrum_fundamental_frequency(self):
        """Test fundamental frequency derivation from Riemann operator."""
        spectrum = RiemannOperatorSpectrum(precision=50)
        freq_data = spectrum.fundamental_frequency()
        
        # Should derive frequency close to measured value
        f0_derived = float(freq_data['f0_complete'])
        f0_measured = float(freq_data['f0_measured'])
        
        self.assertAlmostEqual(f0_derived, f0_measured, delta=5.0)
        self.assertGreater(f0_derived, 100.0)
        self.assertLess(f0_derived, 200.0)
    
    def test_adelic_coherence_threshold(self):
        """Test adelic coherence threshold."""
        adelic = AdelicGeometry()
        threshold = float(adelic.coherence_threshold())
        
        self.assertAlmostEqual(threshold, 0.888, places=3)
    
    def test_adelic_coherence_at_f0(self):
        """Test global coherence at f₀."""
        adelic = AdelicGeometry()
        psi = float(adelic.global_coherence(141.7001))
        threshold = float(adelic.coherence_threshold())
        
        # Should meet or exceed threshold
        self.assertGreaterEqual(psi, threshold)
    
    def test_picode_encode_decode(self):
        """Test πCODE encoding and decoding."""
        picode = PiCodeAlgebra()
        original = 10.0
        
        encoded = picode.encode(original)
        decoded = picode.decode(encoded)
        
        # Should be reasonably close (golden ratio decomposition)
        self.assertIsInstance(encoded, np.ndarray)
        self.assertGreater(decoded, 0.0)
    
    def test_number_theory_golden_ratio(self):
        """Test golden ratio properties."""
        number_theory = NumberTheoryDerivation()
        phi = float(number_theory.phi)
        
        # φ = (1 + √5) / 2 ≈ 1.618034
        self.assertAlmostEqual(phi, 1.618034, places=5)
        
        # φ² = φ + 1
        self.assertAlmostEqual(phi**2, phi + 1, places=5)


class TestCapa2QuantumPhysics(unittest.TestCase):
    """Test quantum physics layer."""
    
    def test_ringdown_generation(self):
        """Test ringdown waveform generation."""
        gw = GW250114RingdownAnalysis()
        t, h = gw.generate_ringdown(duration=0.5)
        
        self.assertEqual(len(t), len(h))
        self.assertGreater(len(t), 1000)
        self.assertIsInstance(h, np.ndarray)
    
    def test_141hz_detection(self):
        """Test 141.7 Hz resonance detection."""
        gw = GW250114RingdownAnalysis()
        t, h = gw.generate_ringdown(duration=0.5)
        detection = gw.detect_141hz_resonance(h)
        
        self.assertIn('detected', detection)
        self.assertIn('frequency', detection)
        self.assertIn('snr', detection)
        
        if detection['detected']:
            self.assertGreater(detection['snr'], 0)
    
    def test_spacetime_wavelength(self):
        """Test spacetime wavelength calculation."""
        spacetime = SpacetimeResonance()
        wavelength = float(spacetime.geometric_wavelength())
        
        # λ = c / f ≈ 2.1e6 m
        expected = 299792458 / 141.7001
        self.assertAlmostEqual(wavelength, expected, delta=1000)
    
    def test_coherence_eigenstates(self):
        """Test coherence operator eigenstates."""
        coh_obs = CoherencePsiObservable()
        eigenvalues, eigenvectors = coh_obs.coherence_eigenstates(dim=5)
        
        self.assertEqual(len(eigenvalues), 5)
        self.assertEqual(eigenvectors.shape, (5, 5))
        
        # Eigenvalues should be real and positive
        for eig in eigenvalues:
            self.assertGreater(eig, 0)
    
    def test_pulse_period(self):
        """Test fundamental pulse period derivation."""
        pulses = FundamentalPulses()
        T_derived = float(pulses.derive_pulse_period())
        
        # Should be positive
        self.assertGreater(T_derived, 0)


class TestCapa3ComputationalArchitecture(unittest.TestCase):
    """Test computational architecture layer."""
    
    def test_hardware_tick(self):
        """Test hardware clock ticking."""
        hw = NativeFrequencyHardware()
        initial_count = hw.cycle_count
        
        hw.tick()
        
        # Cycle count should increment
        self.assertEqual(hw.cycle_count, initial_count + 1)
        self.assertEqual(hw.cycle_count, 1)
    
    def test_hardware_synchronization(self):
        """Test hardware unit synchronization."""
        hw1 = NativeFrequencyHardware()
        hw2 = NativeFrequencyHardware()
        
        # Tick both the same amount
        for _ in range(10):
            hw1.tick()
            hw2.tick()
        
        # Should be synchronized
        self.assertTrue(hw1.is_synchronized(hw2, tolerance=0.01))
    
    def test_coherent_registers_write_read(self):
        """Test coherent register write and read."""
        regs = CoherentRegisters(num_registers=4)
        
        regs.write(0, amplitude=1.0, phase=np.pi/4)
        amp, phase = regs.read(0)
        
        self.assertAlmostEqual(amp, 1.0, places=5)
        self.assertAlmostEqual(phase, np.pi/4, places=5)
    
    def test_coherent_registers_superposition(self):
        """Test quantum superposition operation."""
        regs = CoherentRegisters(num_registers=4)
        
        regs.write(0, amplitude=1.0, phase=0.0)
        regs.write(1, amplitude=1.0, phase=0.0)
        regs.superpose(0, 1, 2)
        
        amp, phase = regs.read(2)
        
        # Superposition should have amplitude
        self.assertGreater(amp, 0)
    
    def test_phase_memory_byte_encoding(self):
        """Test phase memory byte encoding/decoding."""
        memory = PhaseMemory(capacity=100)
        
        test_value = 42
        memory.encode_byte(0, test_value)
        decoded = memory.decode_byte(0)
        
        # Should be exact or within 1 (rounding)
        self.assertAlmostEqual(decoded, test_value, delta=1)
    
    def test_resonance_processor_operations(self):
        """Test resonance processor operations."""
        proc = ResonanceProcessor()
        
        proc.registers.write(0, 1.0, 0.0)
        proc.registers.write(1, 1.0, np.pi/4)
        proc.resonance_add(0, 1, 2)
        
        amp, phase = proc.registers.read(2)
        
        # Should have result
        self.assertGreater(amp, 0)
        self.assertGreater(phase, 0)


class TestCapa4OntologicalNetwork(unittest.TestCase):
    """Test ontological network layer."""
    
    def test_node_registration(self):
        """Test node registration."""
        sync = NodeSynchronization()
        node = sync.register_node("test_node", NodeType.OBSERVER)
        
        self.assertEqual(node.node_id, "test_node")
        self.assertEqual(node.node_type, NodeType.OBSERVER)
        self.assertIn("test_node", sync.nodes)
    
    def test_node_coherence_measurement(self):
        """Test coherence measurement between nodes."""
        sync = NodeSynchronization()
        sync.register_node("node1", NodeType.CONTRIBUTOR)
        sync.register_node("node2", NodeType.VALIDATOR)
        
        sync.evolve_network(steps=10)
        
        coherence = sync.measure_coherence("node1", "node2")
        
        self.assertGreaterEqual(coherence, 0.0)
        self.assertLessEqual(coherence, 1.0)
    
    def test_picode_minting(self):
        """Test πCODE minting from coherence."""
        picode = PiCodeValue()
        
        # Mint with high coherence
        amount = picode.mint_picode("alice", coherence=0.95)
        balance = picode.get_balance("alice")
        
        self.assertGreater(amount, 0)
        self.assertEqual(balance, amount)
        self.assertGreater(picode.total_supply, 0)
    
    def test_picode_transfer(self):
        """Test πCODE transfer with coherence proof."""
        picode = PiCodeValue()
        
        # Mint initial balance
        picode.mint_picode("alice", 0.95)
        picode.mint_picode("bob", 0.92)
        
        initial_alice = picode.get_balance("alice")
        initial_bob = picode.get_balance("bob")
        
        # Transfer with valid coherence proof
        tx = picode.transfer("alice", "bob", 0.5, coherence_proof=0.92)
        
        self.assertIsNotNone(tx)
        self.assertEqual(picode.get_balance("alice"), initial_alice - 0.5)
        self.assertEqual(picode.get_balance("bob"), initial_bob + 0.5)
    
    def test_distributed_recognition(self):
        """Test distributed recognition without consensus."""
        recognition = DistributedRecognition(min_recognizers=2)
        
        # Submit contribution
        event = recognition.submit_contribution("alice", {"data": "test"})
        
        # Add recognizers
        recognition.recognize_contribution(event.event_id, "bob", 0.92)
        recognition.recognize_contribution(event.event_id, "charlie", 0.91)
        
        # Should be recognized
        self.assertTrue(recognition.is_recognized(event.event_id))
    
    def test_symbiotic_economy(self):
        """Test symbiotic economy value creation."""
        economy = SymbioticEconomy()
        picode = PiCodeValue()
        
        # Initiate symbiosis (correct parameter order)
        success = economy.initiate_symbiosis("alice", "bob", initial_coherence=0.92)
        self.assertTrue(success)
        
        # Interact symbiotically
        v1, v2 = economy.symbiotic_interaction("alice", "bob", picode)
        
        # Both should gain value
        self.assertGreater(v1, 0)
        self.assertGreater(v2, 0)


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestCapa1MathematicalFoundations))
    suite.addTests(loader.loadTestsFromTestCase(TestCapa2QuantumPhysics))
    suite.addTests(loader.loadTestsFromTestCase(TestCapa3ComputationalArchitecture))
    suite.addTests(loader.loadTestsFromTestCase(TestCapa4OntologicalNetwork))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
