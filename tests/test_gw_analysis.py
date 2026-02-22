#!/usr/bin/env python3
"""
Tests for gw_analysis.py
========================

Test suite for the GW spectral filter analysis script.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gw_analysis import SpectralFilterAnalyzer, get_event_list


class TestSpectralFilterAnalyzer:
    """Test cases for SpectralFilterAnalyzer class."""
    
    def test_initialization(self):
        """Test analyzer initialization with default parameters."""
        analyzer = SpectralFilterAnalyzer()
        
        assert analyzer.center_freq == 141.7001
        assert analyzer.bandwidth == 0.0032
        assert analyzer.run == "O4"
        assert analyzer.f0_qcal == 141.7001
        assert analyzer.kappa_pi == 2.5773
    
    def test_custom_parameters(self):
        """Test analyzer with custom parameters."""
        analyzer = SpectralFilterAnalyzer(
            center_freq=142.0,
            bandwidth=0.005,
            run="O3",
            min_events=10
        )
        
        assert analyzer.center_freq == 142.0
        assert analyzer.bandwidth == 0.005
        assert analyzer.run == "O3"
        assert analyzer.min_events == 10
    
    def test_bandpass_filter_design(self):
        """Test bandpass filter design."""
        analyzer = SpectralFilterAnalyzer()
        b, a = analyzer.design_bandpass_filter()
        
        # Check filter coefficients are returned
        assert len(b) > 0
        assert len(a) > 0
        assert len(b) == len(a)
    
    def test_simulated_strain_generation(self):
        """Test simulated strain data generation."""
        analyzer = SpectralFilterAnalyzer()
        strain = analyzer._generate_simulated_strain("GW150914")
        
        # Check output shape
        expected_samples = 32 * analyzer.sample_rate
        assert len(strain) == expected_samples
        
        # Check values are reasonable
        assert np.max(np.abs(strain)) < 1e-19  # Should be strain-level
    
    def test_snr_computation(self):
        """Test SNR computation."""
        analyzer = SpectralFilterAnalyzer()
        
        # Create test signals
        strain = np.random.normal(0, 1e-21, 10000)
        filtered = np.random.normal(0, 2e-21, 10000)
        
        snr = analyzer.compute_snr_in_band(strain, filtered)
        
        # SNR should be positive
        assert snr >= 0
    
    def test_analyze_event_simulated(self):
        """Test single event analysis with simulated data."""
        analyzer = SpectralFilterAnalyzer()
        result = analyzer.analyze_event("GW150914", detector="H1", simulated=True)
        
        # Check result structure
        assert "event" in result
        assert "detector" in result
        assert "snr" in result
        assert "peak_freq" in result
        assert "detected" in result
        
        # Check values
        assert result["event"] == "GW150914"
        assert result["detector"] == "H1"
        assert isinstance(result["detected"], bool)
    
    def test_multi_event_search(self):
        """Test multi-event subdominant search."""
        analyzer = SpectralFilterAnalyzer(min_events=5)
        event_list = get_event_list("O4")[:5]  # Use first 5 events
        
        stats = analyzer.search_multi_event_subdominant(
            event_list=event_list,
            detector="H1",
            simulated=True
        )
        
        # Check statistics
        assert "total_events" in stats
        assert stats["total_events"] == 5
        assert "detection_rate" in stats
        assert 0 <= stats["detection_rate"] <= 1
        assert "mean_snr" in stats
        assert "consistency" in stats
    
    def test_certificate_generation(self):
        """Test analysis certificate generation."""
        analyzer = SpectralFilterAnalyzer()
        
        # Run minimal analysis
        event_list = get_event_list("O4")[:3]
        analyzer.search_multi_event_subdominant(
            event_list=event_list,
            simulated=True
        )
        
        # Generate certificate
        certificate = analyzer.generate_certificate()
        
        # Check certificate structure
        assert "certificate_id" in certificate
        assert "hash" in certificate
        assert "data" in certificate
        assert "signature" in certificate
        assert len(certificate["hash"]) == 64  # SHA-256 hex
    
    def test_export_results(self):
        """Test results export."""
        analyzer = SpectralFilterAnalyzer()
        
        # Run minimal analysis
        event_list = get_event_list("O4")[:2]
        analyzer.search_multi_event_subdominant(
            event_list=event_list,
            simulated=True
        )
        
        # Export
        output_path = analyzer.export_results("test_output.json")
        
        # Check file exists
        assert output_path.exists()
        
        # Clean up
        output_path.unlink()


class TestEventLists:
    """Test event list generation."""
    
    def test_o4_event_list(self):
        """Test O4 event list generation."""
        events = get_event_list("O4")
        
        assert len(events) > 0
        assert all("GWO4Event" in e for e in events)
    
    def test_o3_event_list(self):
        """Test O3 event list generation."""
        events = get_event_list("O3")
        
        assert len(events) > 0
        # Should contain some real O3 events
        assert any("GW19" in e for e in events)
    
    def test_default_event_list(self):
        """Test default (unknown) event list."""
        events = get_event_list("UNKNOWN")
        
        # Should default to O4
        assert len(events) > 0


class TestSimulationMode:
    """Tests for explicit simulation/real-data mode in SpectralFilterAnalyzer."""

    def test_default_is_simulation(self):
        """Default analyzer must run in simulation mode."""
        analyzer = SpectralFilterAnalyzer()
        assert analyzer.simulation_mode is True

    def test_simulation_mode_in_config(self):
        """simulation_mode must be recorded in results config."""
        analyzer = SpectralFilterAnalyzer(simulation_mode=True)
        assert analyzer.results["config"]["simulation_mode"] is True

    def test_real_data_mode_in_config(self):
        """simulation_mode=False must be recorded in results config."""
        analyzer = SpectralFilterAnalyzer(simulation_mode=False)
        assert analyzer.results["config"]["simulation_mode"] is False

    def test_analyze_event_uses_simulation_by_default(self):
        """analyze_event must use simulation when simulation_mode=True."""
        analyzer = SpectralFilterAnalyzer(simulation_mode=True)
        result = analyzer.analyze_event("GW150914", detector="H1")
        # Should succeed and return valid result
        assert "snr" in result
        assert isinstance(result["detected"], bool)

    def test_simulation_mode_false_with_no_gwpy(self):
        """With simulation_mode=False and no gwpy, falls back to simulation."""
        import gw_analysis as gw_mod
        original = gw_mod.GWPY_AVAILABLE
        try:
            gw_mod.GWPY_AVAILABLE = False
            analyzer = SpectralFilterAnalyzer(simulation_mode=False)
            # analyze_event should still work via fallback
            result = analyzer.analyze_event("GW150914", detector="H1")
            assert "snr" in result
        finally:
            gw_mod.GWPY_AVAILABLE = original


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
