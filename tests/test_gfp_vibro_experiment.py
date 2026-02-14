#!/usr/bin/env python3
"""
Tests for gfp_vibro_experiment.py
==================================

Test suite for the GFP vibro-fluorescent experiment.
"""

import pytest
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gfp_vibro_experiment import GFPVibroExperiment


class TestGFPVibroExperiment:
    """Test cases for GFP vibro-fluorescent experiment."""
    
    def test_initialization(self):
        """Test experiment initialization."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        
        assert experiment.f_qcal == 141.7
        assert experiment.f_control == 100.0
        assert experiment.ratio_threshold == 1.5
        assert experiment.simulation_mode is True
    
    def test_simulated_measurement(self):
        """Test simulated fluorescence measurement."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        
        # Measure at QCAL frequency
        delta_f_qcal, snr_qcal = experiment._simulate_measurement(141.7, 10.0)
        
        # Measure at control frequency
        delta_f_control, snr_control = experiment._simulate_measurement(100.0, 10.0)
        
        # QCAL should have higher response
        assert delta_f_qcal > delta_f_control
        assert snr_qcal > snr_control
    
    def test_measure_fluorescence(self):
        """Test fluorescence measurement with repeats."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        result = experiment.measure_fluorescence(141.7, duration=10.0, n_repeats=3)
        
        # Check result structure
        assert "frequency" in result
        assert "n_repeats" in result
        assert "delta_f" in result
        assert "snr" in result
        
        # Check delta_f statistics
        assert "mean" in result["delta_f"]
        assert "std" in result["delta_f"]
        assert "values" in result["delta_f"]
        assert len(result["delta_f"]["values"]) == 3
    
    def test_comparison_experiment(self):
        """Test complete comparison experiment."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        results = experiment.run_comparison_experiment(duration=5.0, n_repeats=3)
        
        # Check results structure
        assert "config" in results
        assert "measurements" in results
        assert "analysis" in results
        
        # Check measurements
        assert "qcal_141.7hz" in results["measurements"]
        assert "control_100hz" in results["measurements"]
        
        # Check analysis
        analysis = results["analysis"]
        assert "delta_f_ratio" in analysis
        assert "snr_ratio" in analysis
        assert "statistical_test" in analysis
        assert "nft_support" in analysis
    
    def test_prediction_validation(self):
        """Test NFT prediction validation."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        results = experiment.run_comparison_experiment(duration=5.0, n_repeats=5)
        
        # Check ratio exceeds threshold
        ratio = results["analysis"]["delta_f_ratio"]["value"]
        threshold = results["analysis"]["delta_f_ratio"]["threshold"]
        
        # In simulation, should confirm prediction
        assert ratio > threshold
        assert results["analysis"]["delta_f_ratio"]["prediction_confirmed"]
        
        # Should have statistical significance
        assert results["analysis"]["statistical_test"]["p_value"] < 0.05
    
    def test_nft_support_confirmation(self):
        """Test NFT theory support confirmation."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        results = experiment.run_comparison_experiment(duration=10.0, n_repeats=5)
        
        # Should confirm NFT support
        assert results["analysis"]["nft_support"]["confirmed"]
        assert results["analysis"]["nft_support"]["confidence"] in ["high", "moderate"]
    
    def test_export_results(self):
        """Test results export."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        experiment.run_comparison_experiment(duration=5.0, n_repeats=3)
        
        # Export results
        output_path = experiment.export_results("test_gfp_results.json")
        
        try:
            # Check file exists and is valid JSON
            assert output_path.exists()
            
            with open(output_path) as f:
                data = json.load(f)
            
            assert "config" in data
            assert "measurements" in data
            assert "analysis" in data
            
        finally:
            # Clean up
            if output_path.exists():
                output_path.unlink()
    
    def test_protocol_generation(self):
        """Test protocol document generation."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        protocol_path = experiment.generate_protocol_document()
        
        try:
            # Check file exists
            assert protocol_path.exists()
            
            # Check content
            with open(protocol_path) as f:
                content = f.read()
            
            assert "GFP Vibro-Fluorescent Experimental Protocol" in content
            assert "141.7 Hz" in content
            assert "100 Hz" in content
            assert "Wet-Lab ∞" in content
            
        finally:
            # Clean up
            if protocol_path.exists():
                protocol_path.unlink()


class TestEnergyConstraint:
    """Test constant energy constraint."""
    
    def test_energy_conservation(self):
        """Test that energy is conserved between measurements."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        
        # This is a conceptual test - in real experiment,
        # energy would be controlled by adjusting amplitude
        assert experiment.energy_constraint == "constant"


class TestStatisticalAnalysis:
    """Test statistical analysis methods."""
    
    def test_t_test_execution(self):
        """Test that t-test is executed correctly."""
        experiment = GFPVibroExperiment(simulation_mode=True)
        results = experiment.run_comparison_experiment(duration=5.0, n_repeats=5)
        
        stats = results["analysis"]["statistical_test"]
        
        # Should have t-statistic and p-value
        assert "t_statistic" in stats
        assert "p_value" in stats
        assert "significant" in stats
        
        # p-value should be between 0 and 1
        assert 0 <= stats["p_value"] <= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
