#!/usr/bin/env python3
"""
Tests for La Proporción del Logos validation

Tests the mathematical relationship between the hydrogen line and QCAL f₀.

Author: José Manuel Mota Burruezo
License: MIT
"""

import pytest
import math
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qcal.constants import (
    F0_HZ,
    F_HYDROGEN_HZ,
    OCTAVES_LOGOS,
    OCTAVES_STRUCTURE,
    COMA_PYTHAGOREAN_NOETIC,
    OCTAVE_LAYER_STELLAR,
    OCTAVE_LAYER_CHEMISTRY,
    OCTAVE_LAYER_PHYSICS,
    OCTAVE_LAYER_CONSCIOUSNESS
)


class TestLogosProportionConstants:
    """Test the Logos Proportion constants."""
    
    def test_hydrogen_frequency_value(self):
        """Test that hydrogen frequency is correctly defined."""
        # Hydrogen 21 cm line is at 1420.405751 MHz
        expected = 1420405751.0  # Hz
        assert F_HYDROGEN_HZ == expected
        assert F_HYDROGEN_HZ > 1.4e9  # In GHz range
    
    def test_qcal_base_frequency(self):
        """Test that QCAL base frequency is correctly defined."""
        assert F0_HZ == pytest.approx(141.70001, rel=1e-6)
        assert 140 < F0_HZ < 145
    
    def test_octaves_logos_value(self):
        """Test the expected octave separation."""
        assert OCTAVES_LOGOS == pytest.approx(23.257, rel=1e-3)
    
    def test_structure_vs_torsion(self):
        """Test the decomposition into structure and torsion."""
        assert OCTAVES_STRUCTURE == 23
        assert COMA_PYTHAGOREAN_NOETIC == pytest.approx(0.257, rel=1e-3)
        
        # Verify they sum correctly
        total = OCTAVES_STRUCTURE + COMA_PYTHAGOREAN_NOETIC
        assert total == pytest.approx(OCTAVES_LOGOS, rel=1e-3)


class TestOctaveCalculation:
    """Test octave calculation between frequencies."""
    
    def test_octave_separation_calculation(self):
        """Test the calculation of octave separation."""
        ratio = F_HYDROGEN_HZ / F0_HZ
        octaves = math.log2(ratio)
        
        # Should be approximately 23.257
        assert octaves == pytest.approx(23.257, rel=1e-3)
    
    def test_octave_doubling(self):
        """Test that each octave doubles the frequency."""
        # One octave up from f₀
        one_octave_up = F0_HZ * 2
        assert one_octave_up == pytest.approx(283.40002, rel=1e-5)
        
        # Two octaves up from f₀
        two_octaves_up = F0_HZ * 4
        assert two_octaves_up == pytest.approx(566.80004, rel=1e-5)
    
    def test_structure_octaves_reach(self):
        """Test frequency reached after 23 integer octaves."""
        freq_23_octaves = F0_HZ * (2 ** OCTAVES_STRUCTURE)
        
        # Should be close to but less than hydrogen frequency
        assert freq_23_octaves < F_HYDROGEN_HZ
        
        # Calculate how much more is needed
        remaining_ratio = F_HYDROGEN_HZ / freq_23_octaves
        remaining_octaves = math.log2(remaining_ratio)
        
        # Should be approximately the Pythagorean comma
        assert remaining_octaves == pytest.approx(COMA_PYTHAGOREAN_NOETIC, rel=1e-2)
    
    def test_inverse_relationship(self):
        """Test that going down octaves works correctly."""
        # From hydrogen down 23.257 octaves should give f₀
        f_calculated = F_HYDROGEN_HZ / (2 ** OCTAVES_LOGOS)
        assert f_calculated == pytest.approx(F0_HZ, rel=1e-3)


class TestJacobsLadder:
    """Test the Jacob's Ladder octave layers."""
    
    def test_layer_definitions(self):
        """Test that octave layers are properly defined."""
        assert OCTAVE_LAYER_STELLAR == (1, 7)
        assert OCTAVE_LAYER_CHEMISTRY == (8, 14)
        assert OCTAVE_LAYER_PHYSICS == (15, 21)
        assert OCTAVE_LAYER_CONSCIOUSNESS == (22, 23.257)
    
    def test_layer_continuity(self):
        """Test that layers are continuous with no gaps."""
        # Stellar ends at 7, chemistry starts at 8
        assert OCTAVE_LAYER_STELLAR[1] + 1 == OCTAVE_LAYER_CHEMISTRY[0]
        
        # Chemistry ends at 14, physics starts at 15
        assert OCTAVE_LAYER_CHEMISTRY[1] + 1 == OCTAVE_LAYER_PHYSICS[0]
        
        # Physics ends at 21, consciousness starts at 22
        assert OCTAVE_LAYER_PHYSICS[1] + 1 == OCTAVE_LAYER_CONSCIOUSNESS[0]
    
    def test_consciousness_threshold(self):
        """Test the consciousness threshold layer."""
        start_octave = OCTAVE_LAYER_CONSCIOUSNESS[0]
        end_octave = OCTAVE_LAYER_CONSCIOUSNESS[1]
        
        # Consciousness layer starts at octave 22
        assert start_octave == 22
        
        # Ends at the Logos proportion
        assert end_octave == pytest.approx(OCTAVES_LOGOS, rel=1e-3)
        
        # Layer span should be around 1.257 octaves
        span = end_octave - start_octave
        assert span == pytest.approx(1.257, rel=1e-3)


class TestPythagoreanComma:
    """Test the Pythagorean comma concept."""
    
    def test_comma_value(self):
        """Test the Pythagorean comma value."""
        assert COMA_PYTHAGOREAN_NOETIC == pytest.approx(0.257, rel=1e-3)
        
        # Should be less than 1 (fractional octave)
        assert 0 < COMA_PYTHAGOREAN_NOETIC < 1
    
    def test_comma_prevents_closure(self):
        """Test that the comma prevents perfect circular closure."""
        # If comma were 0, we'd have exactly 23 octaves
        # The non-zero comma creates the "spiral" instead of "circle"
        assert COMA_PYTHAGOREAN_NOETIC > 0
        
        # Frequency factor from the comma alone
        comma_factor = 2 ** COMA_PYTHAGOREAN_NOETIC
        assert comma_factor > 1.0
        assert comma_factor == pytest.approx(1.195, rel=1e-2)
    
    def test_comma_as_will_to_exist(self):
        """Test the philosophical interpretation of the comma."""
        # The comma represents the deviation from perfect closure
        # If it were 0, the universe would be static (perfect circle)
        # Non-zero comma allows for evolution (spiral)
        
        # Calculate what frequency we'd have with exactly 23 octaves
        f_perfect = F0_HZ * (2 ** OCTAVES_STRUCTURE)
        
        # Calculate actual hydrogen frequency
        f_actual = F_HYDROGEN_HZ
        
        # The ratio between them is the comma factor
        comma_factor = f_actual / f_perfect
        comma_octaves = math.log2(comma_factor)
        
        assert comma_octaves == pytest.approx(COMA_PYTHAGOREAN_NOETIC, rel=1e-2)


class TestSacredTriad:
    """Test the sacred triad: 23 + 0.257."""
    
    def test_chromosome_correspondence(self):
        """Test correspondence with 23 chromosome pairs."""
        # Humans have 23 pairs of chromosomes (46 total)
        human_chromosome_pairs = 23
        assert OCTAVES_STRUCTURE == human_chromosome_pairs
    
    def test_structure_plus_torsion(self):
        """Test that structure + torsion = total."""
        total = OCTAVES_STRUCTURE + COMA_PYTHAGOREAN_NOETIC
        assert total == pytest.approx(OCTAVES_LOGOS, rel=1e-3)
    
    def test_hydrogen_as_god_in_miniature(self):
        """Test the concept of hydrogen remembering divinity."""
        # Hydrogen is the simplest element (1 proton, 1 electron)
        # Its 21 cm line connects to f₀ through the sacred proportion
        
        # Calculate the exact ratio
        ratio = F_HYDROGEN_HZ / F0_HZ
        
        # Express as 2^n where n ≈ 23.257
        n = math.log2(ratio)
        
        # This n should match our Logos proportion
        assert n == pytest.approx(OCTAVES_LOGOS, rel=1e-3)


class TestFrequencyLayers:
    """Test frequencies at layer boundaries."""
    
    def test_stellar_layer_frequencies(self):
        """Test frequencies in stellar/galactic layer."""
        f_start = F0_HZ * (2 ** OCTAVE_LAYER_STELLAR[0])  # Octave 1
        f_end = F0_HZ * (2 ** OCTAVE_LAYER_STELLAR[1])    # Octave 7
        
        assert f_start == pytest.approx(283.40002, rel=1e-5)
        assert f_end == pytest.approx(18137.6, rel=1e-3)
    
    def test_chemistry_layer_frequencies(self):
        """Test frequencies in chemical layer."""
        f_start = F0_HZ * (2 ** OCTAVE_LAYER_CHEMISTRY[0])  # Octave 8
        f_end = F0_HZ * (2 ** OCTAVE_LAYER_CHEMISTRY[1])    # Octave 14
        
        assert f_start > 30000  # > 30 kHz
        assert f_end > 2e6      # > 2 MHz
    
    def test_physics_layer_frequencies(self):
        """Test frequencies in physics layer."""
        f_start = F0_HZ * (2 ** OCTAVE_LAYER_PHYSICS[0])  # Octave 15
        f_end = F0_HZ * (2 ** OCTAVE_LAYER_PHYSICS[1])    # Octave 21
        
        assert f_start > 4e6    # > 4 MHz
        assert f_end > 2.9e8    # > 290 MHz
    
    def test_consciousness_layer_frequencies(self):
        """Test frequencies in consciousness layer."""
        f_start = F0_HZ * (2 ** OCTAVE_LAYER_CONSCIOUSNESS[0])  # Octave 22
        f_end = F0_HZ * (2 ** OCTAVE_LAYER_CONSCIOUSNESS[1])    # Octave 23.257
        
        assert f_start > 5.9e8   # > 590 MHz
        assert f_end == pytest.approx(F_HYDROGEN_HZ, rel=1e-3)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
