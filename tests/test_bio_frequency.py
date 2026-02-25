#!/usr/bin/env python3
"""
Unit Tests for Bio-Frequency System
====================================

Comprehensive test suite for the Bio-Frequency module implementing
biological entrainment at 141.7001 Hz.

Author: José Manuel Mota Burruezo
Date: February 25, 2026
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.bio_frequency import (
    BiologicalOscillator,
    MeditationState,
    BiologicalEntrainment,
    SevenNodesMeditation,
    EZWaterStructure,
    BioFrequencySystem,
    F0_HZ,
    PHI,
    COHERENCE_THRESHOLD_STABLE,
    COHERENCE_THRESHOLD_EXCELLENT,
    HEXAGON_SYMMETRY
)


class TestBiologicalOscillator(unittest.TestCase):
    """Test BiologicalOscillator class."""
    
    def test_initialization(self):
        """Test oscillator initialization."""
        osc = BiologicalOscillator("test", 10.0, 0.5, 0.0)
        self.assertEqual(osc.name, "test")
        self.assertEqual(osc.natural_frequency, 10.0)
        self.assertEqual(osc.coupling_strength, 0.5)
        self.assertEqual(osc.phase, 0.0)
    
    def test_phase_update(self):
        """Test phase update mechanism."""
        osc = BiologicalOscillator("test", 10.0, 0.8, 0.0)
        initial_phase = osc.phase
        
        # Update phase
        osc.update_phase(dt=0.001, carrier_freq=10.0, carrier_phase=0.0)
        
        # Phase should have advanced
        self.assertNotEqual(osc.phase, initial_phase)
        
        # Phase should be in [0, 2π]
        self.assertGreaterEqual(osc.phase, 0.0)
        self.assertLess(osc.phase, 2 * np.pi)


class TestMeditationState(unittest.TestCase):
    """Test MeditationState class."""
    
    def test_initialization(self):
        """Test meditation state initialization."""
        state = MeditationState()
        self.assertFalse(state.sonic_active)
        self.assertFalse(state.rhythmic_active)
        self.assertFalse(state.visual_active)
        self.assertEqual(state.coherence, 0.0)
        self.assertEqual(state.num_active_pillars, 0)
        self.assertFalse(state.is_complete)
    
    def test_pillar_activation(self):
        """Test pillar activation tracking."""
        state = MeditationState()
        
        # Activate one pillar
        state.sonic_active = True
        self.assertEqual(state.num_active_pillars, 1)
        self.assertFalse(state.is_complete)
        
        # Activate all three
        state.rhythmic_active = True
        state.visual_active = True
        self.assertEqual(state.num_active_pillars, 3)
        self.assertTrue(state.is_complete)


class TestBiologicalEntrainment(unittest.TestCase):
    """Test BiologicalEntrainment class."""
    
    def test_initialization(self):
        """Test entrainment system initialization."""
        entrainment = BiologicalEntrainment(carrier_frequency=F0_HZ)
        self.assertEqual(entrainment.carrier_frequency, F0_HZ)
        self.assertEqual(len(entrainment.oscillators), 0)
    
    def test_add_oscillator(self):
        """Test adding oscillators."""
        entrainment = BiologicalEntrainment()
        entrainment.add_oscillator("test1", 100.0, 0.5)
        entrainment.add_oscillator("test2", 150.0, 0.7)
        
        self.assertEqual(len(entrainment.oscillators), 2)
        self.assertEqual(entrainment.oscillators[0].name, "test1")
        self.assertEqual(entrainment.oscillators[1].name, "test2")
    
    def test_phase_coherence_single_oscillator(self):
        """Test phase coherence with single oscillator."""
        entrainment = BiologicalEntrainment()
        entrainment.add_oscillator("test", F0_HZ, 0.9)
        
        coherence = entrainment.calculate_phase_coherence()
        
        # Single oscillator should have perfect coherence
        self.assertAlmostEqual(coherence, 1.0, places=6)
    
    def test_phase_coherence_synchronized(self):
        """Test phase coherence with synchronized oscillators."""
        entrainment = BiologicalEntrainment(carrier_frequency=F0_HZ)
        
        # Add oscillators at same frequency (should synchronize)
        entrainment.add_oscillator("osc1", F0_HZ, 0.95)
        entrainment.add_oscillator("osc2", F0_HZ, 0.95)
        
        results = entrainment.simulate_entrainment(duration=1.0, dt=0.001)
        
        # Should achieve high coherence
        self.assertGreater(results['final_coherence'], 0.95)
    
    def test_entrainment_simulation(self):
        """Test complete entrainment simulation."""
        entrainment = BiologicalEntrainment(carrier_frequency=F0_HZ)
        entrainment.add_oscillator("micro1", F0_HZ, 0.95)
        entrainment.add_oscillator("micro2", F0_HZ * 1.001, 0.95)
        
        results = entrainment.simulate_entrainment(duration=5.0, dt=0.001)
        
        # Check results structure
        self.assertIn('time', results)
        self.assertIn('coherence', results)
        self.assertIn('final_coherence', results)
        self.assertIn('mean_coherence', results)
        self.assertIn('carrier_frequency', results)
        self.assertIn('num_oscillators', results)
        
        # Check values
        self.assertEqual(results['carrier_frequency'], F0_HZ)
        self.assertEqual(results['num_oscillators'], 2)
        self.assertGreater(results['final_coherence'], 0.90)


class TestSevenNodesMeditation(unittest.TestCase):
    """Test SevenNodesMeditation class."""
    
    def test_initialization(self):
        """Test meditation protocol initialization."""
        meditation = SevenNodesMeditation()
        self.assertIsInstance(meditation.state, MeditationState)
        self.assertFalse(meditation.state.sonic_active)
    
    def test_sonic_pillar_pure_tone(self):
        """Test sonic pillar with pure tone."""
        meditation = SevenNodesMeditation()
        result = meditation.activate_sonic_pillar(use_binaural=False)
        
        self.assertTrue(result['active'])
        self.assertEqual(result['mode'], 'pure_tone')
        self.assertEqual(result['base_frequency'], F0_HZ)
        self.assertEqual(result['left_ear_hz'], F0_HZ)
        self.assertEqual(result['right_ear_hz'], F0_HZ)
        self.assertEqual(result['beat_frequency'], 0.0)
    
    def test_sonic_pillar_binaural(self):
        """Test sonic pillar with binaural beats."""
        meditation = SevenNodesMeditation()
        beat_freq = 10.0
        result = meditation.activate_sonic_pillar(use_binaural=True, beat_freq=beat_freq)
        
        self.assertTrue(result['active'])
        self.assertEqual(result['mode'], 'binaural')
        self.assertEqual(result['beat_frequency'], beat_freq)
        
        # Check frequency separation
        left = result['left_ear_hz']
        right = result['right_ear_hz']
        self.assertAlmostEqual(right - left, beat_freq, places=5)
    
    def test_rhythmic_pillar(self):
        """Test rhythmic pillar (golden ratio breathing)."""
        meditation = SevenNodesMeditation()
        result = meditation.activate_rhythmic_pillar(breaths_per_minute=6.0)
        
        self.assertTrue(result['active'])
        self.assertEqual(result['breaths_per_minute'], 6.0)
        self.assertAlmostEqual(result['ratio'], PHI, places=5)
        
        # Check breathing durations
        total = result['inhale_duration_s'] + result['exhale_duration_s']
        ratio = result['inhale_duration_s'] / result['exhale_duration_s']
        
        self.assertAlmostEqual(total, 10.0, places=5)  # 6 breaths/min = 10s/breath
        self.assertAlmostEqual(ratio, PHI, places=2)
    
    def test_visual_pillar(self):
        """Test visual pillar (hexagonal geometry)."""
        meditation = SevenNodesMeditation()
        result = meditation.activate_visual_pillar()
        
        self.assertTrue(result['active'])
        self.assertEqual(result['geometry'], 'hexagonal')
        self.assertEqual(result['symmetry'], HEXAGON_SYMMETRY)
        self.assertEqual(result['angle_degrees'], 60.0)
        self.assertEqual(result['lattice_type'], 'adelic')
    
    def test_meditation_coherence(self):
        """Test meditation coherence calculation."""
        meditation = SevenNodesMeditation()
        
        # No pillars active
        coherence = meditation.calculate_meditation_coherence()
        self.assertEqual(coherence, 0.0)
        
        # One pillar active
        meditation.activate_sonic_pillar()
        coherence = meditation.calculate_meditation_coherence()
        self.assertAlmostEqual(coherence, 1/3, places=5)
        
        # All three pillars active (with synergy boost)
        meditation.activate_rhythmic_pillar()
        meditation.activate_visual_pillar()
        coherence = meditation.calculate_meditation_coherence()
        self.assertGreaterEqual(coherence, 1.0)  # Synergy bonus brings to 1.0
    
    def test_protocol_status(self):
        """Test protocol status reporting."""
        meditation = SevenNodesMeditation()
        meditation.activate_sonic_pillar()
        meditation.activate_rhythmic_pillar()
        meditation.activate_visual_pillar()
        
        status = meditation.get_protocol_status()
        
        self.assertTrue(status['complete'])
        self.assertEqual(status['num_active'], 3)
        self.assertGreaterEqual(status['coherence'], 1.0)
        self.assertIn(status['status'], ['EXCELLENT', 'STABLE', 'GOOD'])


class TestEZWaterStructure(unittest.TestCase):
    """Test EZWaterStructure class."""
    
    def test_initialization(self):
        """Test EZ water initialization."""
        ez_water = EZWaterStructure(temperature=310.0)
        self.assertEqual(ez_water.temperature, 310.0)
    
    def test_ez_thickness(self):
        """Test EZ layer thickness calculation."""
        ez_water = EZWaterStructure()
        thickness = ez_water.calculate_ez_thickness(surface_charge_density=1e-3)
        
        # Typical EZ water is 100-300 micrometers
        self.assertGreater(thickness, 50.0)
        self.assertLess(thickness, 500.0)
    
    def test_hexagonal_layer_count(self):
        """Test hexagonal layer count calculation."""
        ez_water = EZWaterStructure()
        num_layers = ez_water.hexagonal_layer_count(thickness_um=100.0)
        
        # Should have many layers
        self.assertGreater(num_layers, 100)
        self.assertIsInstance(num_layers, int)
    
    def test_charging_rate_resonance(self):
        """Test charging rate at resonant frequency."""
        ez_water = EZWaterStructure()
        
        # At resonance (f₀)
        rate_resonant = ez_water.calculate_charging_rate(frequency=F0_HZ, amplitude=1.0)
        
        # Off resonance
        rate_off = ez_water.calculate_charging_rate(frequency=100.0, amplitude=1.0)
        
        # Resonant should be much higher
        self.assertGreater(rate_resonant, rate_off)
        self.assertGreater(rate_resonant, 0.8)
    
    def test_structure_water_at_resonance(self):
        """Test water structuring at resonant frequency."""
        ez_water = EZWaterStructure()
        result = ez_water.structure_water(duration=300.0, frequency=F0_HZ)
        
        self.assertEqual(result['frequency_hz'], F0_HZ)
        self.assertTrue(result['is_resonant'])
        self.assertGreater(result['charging_rate'], 0.8)
        self.assertGreater(result['structure_level'], 0.7)
        self.assertGreater(result['water_coherence'], 0.7)
    
    def test_structure_water_off_resonance(self):
        """Test water structuring off resonance."""
        ez_water = EZWaterStructure()
        result = ez_water.structure_water(duration=300.0, frequency=50.0)
        
        self.assertFalse(result['is_resonant'])
        self.assertLess(result['charging_rate'], 0.5)


class TestBioFrequencySystem(unittest.TestCase):
    """Test complete BioFrequencySystem."""
    
    def test_initialization(self):
        """Test system initialization."""
        system = BioFrequencySystem(carrier_frequency=F0_HZ)
        
        self.assertEqual(system.carrier_frequency, F0_HZ)
        self.assertIsInstance(system.entrainment, BiologicalEntrainment)
        self.assertIsInstance(system.meditation, SevenNodesMeditation)
        self.assertIsInstance(system.ez_water, EZWaterStructure)
        
        # Should have default oscillators
        self.assertGreater(len(system.entrainment.oscillators), 0)
    
    def test_default_oscillators(self):
        """Test default oscillator configuration."""
        system = BioFrequencySystem()
        
        # Should have microtubule oscillators
        self.assertEqual(len(system.entrainment.oscillators), 4)
        
        # Check they're near f₀
        for osc in system.entrainment.oscillators:
            self.assertAlmostEqual(osc.natural_frequency, F0_HZ, delta=0.5)
    
    def test_complete_protocol(self):
        """Test running complete protocol."""
        system = BioFrequencySystem()
        results = system.run_complete_protocol(duration=60.0, use_binaural=False)
        
        # Check structure
        self.assertIn('carrier_frequency', results)
        self.assertIn('duration', results)
        self.assertIn('pillars', results)
        self.assertIn('entrainment', results)
        self.assertIn('water_structure', results)
        self.assertIn('coherence', results)
        self.assertIn('consciousness_stable', results)
        
        # Check pillars activated
        self.assertTrue(results['pillars']['sonic']['active'])
        self.assertTrue(results['pillars']['rhythmic']['active'])
        self.assertTrue(results['pillars']['visual']['active'])
        
        # Check coherence (with more realistic thresholds for short duration)
        coherence = results['coherence']
        self.assertGreater(coherence['biological'], 0.85)
        self.assertGreater(coherence['meditation'], 0.7)
        self.assertGreater(coherence['water'], 0.5)  # Lower for short duration
        self.assertGreater(coherence['overall'], 0.75)
    
    def test_consciousness_stability(self):
        """Test consciousness stability threshold."""
        system = BioFrequencySystem()
        results = system.run_complete_protocol(duration=300.0)
        
        # With sufficient duration, should achieve stable consciousness
        self.assertGreaterEqual(results['coherence']['overall'], 0.85)


class TestConstants(unittest.TestCase):
    """Test fundamental constants."""
    
    def test_f0_value(self):
        """Test fundamental frequency value."""
        self.assertEqual(F0_HZ, 141.7001)
    
    def test_phi_value(self):
        """Test golden ratio value."""
        expected_phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(PHI, expected_phi, places=5)
        self.assertAlmostEqual(PHI, 1.618034, places=5)
    
    def test_coherence_thresholds(self):
        """Test coherence threshold values."""
        self.assertEqual(COHERENCE_THRESHOLD_STABLE, 0.95)
        self.assertEqual(COHERENCE_THRESHOLD_EXCELLENT, 0.999)
        self.assertLess(COHERENCE_THRESHOLD_STABLE, COHERENCE_THRESHOLD_EXCELLENT)
    
    def test_hexagon_symmetry(self):
        """Test hexagonal symmetry value."""
        self.assertEqual(HEXAGON_SYMMETRY, 6)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete system."""
    
    def test_full_protocol_workflow(self):
        """Test complete workflow from initialization to results."""
        # Create system
        system = BioFrequencySystem(carrier_frequency=F0_HZ)
        
        # Run protocol
        results = system.run_complete_protocol(duration=120.0, use_binaural=True)
        
        # Verify all components worked
        self.assertTrue(results['pillars']['sonic']['mode'] == 'binaural')
        self.assertGreater(results['entrainment']['final_coherence'], 0.85)
        self.assertGreater(results['water_structure']['structure_level'], 0.7)
        self.assertGreater(results['coherence']['overall'], 0.80)
    
    def test_parameter_consistency(self):
        """Test parameter consistency across components."""
        system = BioFrequencySystem(carrier_frequency=F0_HZ)
        results = system.run_complete_protocol(duration=100.0)
        
        # All components should use f₀
        self.assertEqual(results['carrier_frequency'], F0_HZ)
        self.assertEqual(results['entrainment']['carrier_frequency'], F0_HZ)
        self.assertEqual(results['water_structure']['frequency_hz'], F0_HZ)
        self.assertEqual(results['pillars']['sonic']['base_frequency'], F0_HZ)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
