#!/usr/bin/env python3
"""
Test suite for QNM vs QCAL validation script
"""

import pytest
import json
import sys
from pathlib import Path

# Add physics directory to path for imports
physics_dir = Path(__file__).parent.parent / "physics"
sys.path.insert(0, str(physics_dir))

# Import the validator
from validate_qnm_vs_qcal import QNMvsQCALValidator


class TestQNMvsQCALValidator:
    """Test cases for QNM vs QCAL validator"""

    def setup_method(self):
        """Setup test fixtures"""
        self.validator = QNMvsQCALValidator(precision=30)

    def test_initialization(self):
        """Test validator initialization"""
        assert self.validator.f0_qcal == 141.7001
        assert self.validator.f_qnm_typical == 250.0
        assert self.validator.tau_qnm == 0.1
        assert self.validator.n_bootstrap == 1_000_000
        assert self.validator.sigma_threshold == 111
        assert self.validator.sigma_null == 999

    def test_scale_error_calculation(self):
        """Test scale error analysis"""
        results = self.validator.calculate_scale_error()

        # Check expected keys
        assert 'f_qcal_observed' in results
        assert 'f_qnm_typical' in results
        assert 'scale_ratio_typical' in results
        assert 'orders_of_magnitude' in results

        # Check values are reasonable
        assert results['f_qcal_observed'] == 141.7001
        assert results['f_qnm_typical'] == 250.0

        # Scale ratio should be > 1 (QNM frequency is higher)
        assert results['scale_ratio_typical'] > 1.0

        # Should be about 1.76x higher (250/141.7 ≈ 1.76)
        assert 1.7 < results['scale_ratio_typical'] < 1.8

        # Orders of magnitude should be less than 1 (same order)
        assert 0 < results['orders_of_magnitude'] < 1

    def test_persistence_comparison(self):
        """Test persistence analysis"""
        results = self.validator.compare_persistence(t_max=5.0, n_points=1000)

        # Check expected keys
        assert 'decay_law_qnm' in results
        assert 'decay_law_qcal' in results
        assert 'persistence_ratio' in results
        assert 'energy_qnm' in results
        assert 'energy_qcal' in results

        # Check decay laws
        assert results['decay_law_qnm'] == 'exponential'
        assert results['decay_law_qcal'] == 'power_law_t_minus_half'

        # QCAL should have more persistent energy
        assert results['energy_qcal'] > results['energy_qnm']
        assert results['persistence_ratio'] > 1.0

        # Check plot was created
        plot_file = self.validator.output_dir / 'qnm_vs_qcal_persistence.png'
        assert plot_file.exists()

    def test_statistical_significance(self):
        """Test statistical significance validation"""
        results = self.validator.validate_statistical_significance()

        # Check expected keys
        assert 'sigma_vs_threshold' in results
        assert 'sigma_vs_null' in results
        assert 'p_value_vs_threshold' in results
        assert 'p_value_vs_null' in results
        assert 'sigma_111_valid' in results
        assert 'sigma_999_valid' in results

        # Check sigma values are correct
        # (0.999 - 0.888) / 0.001 = 111
        assert abs(results['sigma_vs_threshold'] - 111.0) < 1.0

        # (0.999 - 0.0) / 0.001 = 999
        assert abs(results['sigma_vs_null'] - 999.0) < 1.0

        # Check validation flags
        assert results['sigma_111_valid'] is True
        assert results['sigma_999_valid'] is True

        # Check p-values are extremely small
        assert results['p_value_vs_threshold'] < 1e-20
        assert results['p_value_vs_null'] < 1e-100

        # Check classification
        assert results['classification'] == 'ABSOLUTE_CERTAINTY'

    def test_comprehensive_report_generation(self):
        """Test comprehensive report generation"""
        results = self.validator.generate_comprehensive_report()

        # Check top-level structure
        assert 'metadata' in results
        assert 'scale_error_analysis' in results
        assert 'persistence_analysis' in results
        assert 'statistical_significance' in results
        assert 'summary' in results

        # Check metadata
        assert results['metadata']['event'] == 'GW250114'
        assert results['metadata']['analysis_type'] == 'QNM_vs_QCAL_comparison'
        assert results['metadata']['fundamental_frequency_hz'] == 141.7001

        # Check summary
        assert 'qnm_prediction_range_hz' in results['summary']
        assert 'qcal_observation_hz' in results['summary']
        assert 'statistical_certainty_sigma' in results['summary']

        # Check JSON file was created
        json_file = self.validator.output_dir / 'qnm_vs_qcal_comprehensive_analysis.json'
        assert json_file.exists()

        # Verify JSON is valid
        with open(json_file, 'r') as f:
            loaded_data = json.load(f)
        assert loaded_data == results

    def test_output_directory_creation(self):
        """Test that output directory is created"""
        assert self.validator.output_dir.exists()
        assert self.validator.output_dir.is_dir()
        assert str(self.validator.output_dir).endswith('qnm_vs_qcal')

    def test_frequency_ranges(self):
        """Test QNM frequency range is physically reasonable"""
        # For 10-60 solar mass black holes
        assert 100 < self.validator.f_qnm_min < 300  # 60 M☉
        assert 1000 < self.validator.f_qnm_max < 1500  # 10 M☉
        assert self.validator.f_qnm_min < self.validator.f_qnm_typical < self.validator.f_qnm_max

    def test_bootstrap_sample_size(self):
        """Test bootstrap has sufficient samples"""
        # Should be 10^6 as specified in problem statement
        assert self.validator.n_bootstrap == 1_000_000

    def test_significance_thresholds(self):
        """Test significance thresholds match problem statement"""
        # Should have 111σ and 999σ as mentioned
        assert self.validator.sigma_threshold == 111
        assert self.validator.sigma_null == 999

        # Standard discovery threshold
        assert self.validator.sigma_discovery == 5


def test_main_execution():
    """Test main function executes without errors"""
    from validate_qnm_vs_qcal import main

    # Should return 0 on success
    result = main()
    assert result == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
