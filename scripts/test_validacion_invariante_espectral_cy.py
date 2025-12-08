#!/usr/bin/env python3
"""
Tests for Calabi-Yau Spectral Invariant k_Π Validation

This test module validates the implementation of the universal spectral
invariant k_Π = μ₂/μ₁ = 2.5773 in Calabi-Yau threefolds.

The tests verify:
1. Correctness of spectral moment calculations
2. Universality of k_Π across different CY models
3. Independence of k_Π from h^{2,1}
4. Reproducibility of results

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import sys
from pathlib import Path

# Add scripts directory to path for local imports
sys.path.insert(0, str(Path(__file__).parent))

import pytest  # noqa: E402
import numpy as np  # noqa: E402

from validacion_invariante_espectral_cy import (  # noqa: E402
    CalabiYauSpectralInvariant,
    CalabiYauModel,
    SpectralResult,
    K_PI_TARGET,
    K_PI_TOLERANCE,
    F0_HZ
)


class TestCalabiYauModel:
    """Tests for the CalabiYauModel dataclass."""

    def test_valid_model_creation(self):
        """Test creating a valid CY model."""
        model = CalabiYauModel(
            name="Test Quintic",
            h21=101,
            model_type="Symmetric"
        )
        assert model.name == "Test Quintic"
        assert model.h21 == 101
        assert model.model_type == "Symmetric"

    def test_model_with_description(self):
        """Test model with description."""
        model = CalabiYauModel(
            name="Test",
            h21=50,
            model_type="CICY",
            description="Test description"
        )
        assert model.description == "Test description"

    def test_invalid_h21_raises_error(self):
        """Test that negative h^{2,1} raises ValueError."""
        with pytest.raises(ValueError, match="h.*must be non-negative"):
            CalabiYauModel(name="Invalid", h21=-1, model_type="Test")


class TestSpectralMoments:
    """Tests for spectral moment calculations."""

    def test_moment_calculation(self):
        """Test that μ₁ and μ₂ are computed correctly."""
        validator = CalabiYauSpectralInvariant()

        # Create a simple test spectrum
        eigenvalues = np.array([1.0, 2.0, 3.0, 4.0, 5.0])

        moments = validator.compute_spectral_moments(eigenvalues)

        # μ₁ = mean = 3.0
        assert moments['mu1'] == pytest.approx(3.0, abs=1e-10)

        # μ₂ = mean of squares = (1 + 4 + 9 + 16 + 25)/5 = 11.0
        assert moments['mu2'] == pytest.approx(11.0, abs=1e-10)

        # k_Π = μ₂/μ₁ = 11/3 ≈ 3.6667
        assert moments['k_pi'] == pytest.approx(11.0 / 3.0, abs=1e-10)

    def test_moment_dictionary_keys(self):
        """Test that all required keys are in moment dictionary."""
        validator = CalabiYauSpectralInvariant()
        eigenvalues = np.array([1.0, 2.0, 3.0])

        moments = validator.compute_spectral_moments(eigenvalues)

        assert 'mu1' in moments
        assert 'mu2' in moments
        assert 'k_pi' in moments
        assert 'variance' in moments
        assert 'n_eigenvalues' in moments
        assert 'lambda_min' in moments
        assert 'lambda_max' in moments


class TestSpectralInvariant:
    """Tests for the universal spectral invariant k_Π."""

    @pytest.fixture
    def validator(self):
        """Create a validator instance."""
        return CalabiYauSpectralInvariant()

    def test_k_pi_target_value(self):
        """Test that k_Π target is 2.5773."""
        assert K_PI_TARGET == pytest.approx(2.5773, abs=0.0001)

    def test_f0_value(self):
        """Test that f₀ is 141.7001 Hz."""
        assert F0_HZ == pytest.approx(141.7001, abs=0.0001)

    def test_validate_single_model(self, validator):
        """Test validation of a single CY model."""
        model = CalabiYauModel(
            name="Test Model",
            h21=100,
            model_type="Test"
        )

        result = validator.validate_model(model)

        assert isinstance(result, SpectralResult)
        assert result.model == "Test Model"
        assert result.h21 == 100
        assert result.n_modes > 0
        # k_Π should be close to 2.5773
        assert abs(result.k_pi - K_PI_TARGET) < K_PI_TOLERANCE

    def test_all_models_have_valid_k_pi(self, validator):
        """Test that all standard models have valid k_Π."""
        results = validator.validate_all_models()

        for result in results:
            assert result.valid, f"Model {result.model} has k_Π = {result.k_pi}"

    def test_k_pi_universal_across_models(self, validator):
        """Test that k_Π is approximately the same across all models."""
        results = validator.validate_all_models()
        stats = validator.compute_statistics(results)

        # Mean should be close to target
        assert abs(stats['k_pi_mean'] - K_PI_TARGET) < K_PI_TOLERANCE * 2

        # Standard deviation should be small (< 5%)
        assert stats['k_pi_std'] < 0.05 * K_PI_TARGET

    def test_k_pi_independent_of_h21(self, validator):
        """Test that k_Π is independent of h^{2,1}."""
        results = validator.validate_all_models()
        stats = validator.compute_statistics(results)

        # Slope vs h^{2,1} should be approximately zero
        # Allow for small numerical variation
        assert abs(stats['slope_vs_h21']) < 0.01


class TestReproducibility:
    """Tests for reproducibility of results."""

    def test_results_are_reproducible(self):
        """Test that running validation twice gives same results."""
        validator1 = CalabiYauSpectralInvariant()
        validator2 = CalabiYauSpectralInvariant()

        results1 = validator1.validate_all_models()
        results2 = validator2.validate_all_models()

        for r1, r2 in zip(results1, results2):
            assert r1.model == r2.model
            assert r1.k_pi == pytest.approx(r2.k_pi, abs=1e-10)
            assert r1.n_modes == r2.n_modes

    def test_model_dependent_seed_is_consistent(self):
        """Test that different models have different but consistent spectra."""
        validator = CalabiYauSpectralInvariant()

        model1 = CalabiYauModel(name="Model A", h21=100, model_type="Test")
        model2 = CalabiYauModel(name="Model B", h21=100, model_type="Test")

        result1 = validator.validate_model(model1)
        result2 = validator.validate_model(model2)

        # Different models should have different k_Π (due to random seed)
        # but both should be within tolerance
        assert result1.valid
        assert result2.valid

        # Run again - should get same results
        result1_again = validator.validate_model(model1)
        assert result1.k_pi == pytest.approx(result1_again.k_pi, abs=1e-10)


class TestExport:
    """Tests for export functionality."""

    def test_to_dict_structure(self):
        """Test structure of exported dictionary."""
        validator = CalabiYauSpectralInvariant()
        data = validator.to_dict()

        assert 'framework' in data
        assert 'invariant' in data
        assert 'target_value' in data
        assert 'tolerance' in data
        assert 'results' in data
        assert 'statistics' in data
        assert 'qcal_connection' in data

    def test_to_dict_values(self):
        """Test values in exported dictionary."""
        validator = CalabiYauSpectralInvariant()
        data = validator.to_dict()

        assert data['target_value'] == K_PI_TARGET
        assert data['tolerance'] == K_PI_TOLERANCE
        assert len(data['results']) == 5  # 5 standard models

    def test_results_structure(self):
        """Test structure of individual results in export."""
        validator = CalabiYauSpectralInvariant()
        data = validator.to_dict()

        for result in data['results']:
            assert 'model' in result
            assert 'h21' in result
            assert 'k_pi' in result
            assert 'n_modes' in result
            assert 'model_type' in result
            assert 'mu1' in result
            assert 'mu2' in result
            assert 'valid' in result


class TestStatistics:
    """Tests for statistical analysis."""

    def test_statistics_structure(self):
        """Test structure of statistics dictionary."""
        validator = CalabiYauSpectralInvariant()
        results = validator.validate_all_models()
        stats = validator.compute_statistics(results)

        assert 'n_models' in stats
        assert 'k_pi_mean' in stats
        assert 'k_pi_std' in stats
        assert 'k_pi_min' in stats
        assert 'k_pi_max' in stats
        assert 'slope_vs_h21' in stats
        assert 'all_valid' in stats

    def test_statistics_values(self):
        """Test statistical values are reasonable."""
        validator = CalabiYauSpectralInvariant()
        results = validator.validate_all_models()
        stats = validator.compute_statistics(results)

        assert stats['n_models'] == 5
        assert stats['k_pi_min'] <= stats['k_pi_mean'] <= stats['k_pi_max']
        assert stats['k_pi_std'] >= 0
        assert isinstance(stats['all_valid'], bool)


class TestGenerateReport:
    """Tests for report generation."""

    def test_report_is_string(self):
        """Test that report is a string."""
        validator = CalabiYauSpectralInvariant()
        report = validator.generate_report()

        assert isinstance(report, str)

    def test_report_contains_key_sections(self):
        """Test that report contains required sections."""
        validator = CalabiYauSpectralInvariant()
        report = validator.generate_report()

        assert "UNIVERSAL SPECTRAL INVARIANT" in report
        assert "Abstract" in report
        assert "Results Table" in report
        assert "Statistical Summary" in report
        assert "Conclusion" in report
        assert "QCAL Framework Connection" in report

    def test_report_contains_model_names(self):
        """Test that report contains all model names."""
        validator = CalabiYauSpectralInvariant()
        report = validator.generate_report()

        assert "Quintic Fermat" in report
        assert "Bicubic" in report
        assert "Octic" in report
        assert "Random Seed 42" in report
        assert "Pfaffian CY" in report


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
