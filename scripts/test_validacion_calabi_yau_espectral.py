#!/usr/bin/env python3
"""
Tests for Calabi-Yau Spectral Universality Validation

Tests the implementation of the universal invariant k_Π ≈ 2.5773
across different Calabi-Yau varieties.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from validacion_calabi_yau_espectral import (
    CY_MODELS,
    K_PI_UNIVERSAL,
    K_PI_FROM_CONSTANTS,
    C_PRIMARY,
    C_COHERENCE,
    compute_alpha_for_k_pi,
    simulate_laplacian_spectrum,
    compute_spectral_moments,
    validate_calabi_yau_spectral_universality,
    validate_k_pi_spectral_invariant,
)


class TestConstants:
    """Test universal constants."""

    def test_k_pi_universal_value(self):
        """Test that K_PI_UNIVERSAL has the correct value."""
        assert K_PI_UNIVERSAL == pytest.approx(2.5773, abs=0.0001)

    def test_k_pi_from_constants(self):
        """Test that K_PI_FROM_CONSTANTS ≈ C_PRIMARY / C_COHERENCE."""
        expected = C_PRIMARY / C_COHERENCE
        assert K_PI_FROM_CONSTANTS == pytest.approx(expected, rel=1e-10)

    def test_k_pi_from_constants_close_to_universal(self):
        """Test that K_PI_FROM_CONSTANTS ≈ K_PI_UNIVERSAL."""
        assert K_PI_FROM_CONSTANTS == pytest.approx(K_PI_UNIVERSAL, abs=0.001)

    def test_c_primary_value(self):
        """Test C_PRIMARY has the correct value."""
        assert C_PRIMARY == pytest.approx(629.83, abs=0.01)

    def test_c_coherence_value(self):
        """Test C_COHERENCE has the correct value."""
        assert C_COHERENCE == pytest.approx(244.36, abs=0.01)


class TestCYModels:
    """Test Calabi-Yau model definitions."""

    def test_cy_models_count(self):
        """Test that there are 4 CY models defined."""
        assert len(CY_MODELS) == 4

    def test_cy_models_have_required_fields(self):
        """Test that all models have required fields."""
        required_fields = ["name", "h11", "h21", "equation", "reference"]
        for model in CY_MODELS:
            for field in required_fields:
                assert field in model, f"Model {model.get('name')} missing {field}"

    def test_quintic_fermat_hodge_numbers(self):
        """Test Quintic Fermat Hodge numbers (h¹¹=1, h²¹=101)."""
        quintic = next(m for m in CY_MODELS if m["key"] == "quintic_fermat")
        assert quintic["h11"] == 1
        assert quintic["h21"] == 101

    def test_bicubic_hodge_numbers(self):
        """Test Bicúbica Hodge numbers (h¹¹=2, h²¹=83)."""
        bicubic = next(m for m in CY_MODELS if m["key"] == "bicubic")
        assert bicubic["h11"] == 2
        assert bicubic["h21"] == 83

    def test_octic_hodge_numbers(self):
        """Test Octic Hodge numbers (h¹¹=1, h²¹=145)."""
        octic = next(m for m in CY_MODELS if m["key"] == "octic_fermat")
        assert octic["h11"] == 1
        assert octic["h21"] == 145

    def test_pfaffian_hodge_numbers(self):
        """Test Pfaffian CY Hodge numbers (h¹¹=2, h²¹=59)."""
        pfaffian = next(m for m in CY_MODELS if m["key"] == "pfaffian_cy")
        assert pfaffian["h11"] == 2
        assert pfaffian["h21"] == 59


class TestAlphaComputation:
    """Test the spectral exponent computation."""

    def test_alpha_produces_correct_k_pi(self):
        """Test that computed alpha produces the target k_Π."""
        for n_modes in [500, 743, 892, 1000, 1121, 2000]:
            alpha = compute_alpha_for_k_pi(n_modes, target_k_pi=K_PI_UNIVERSAL)

            # Compute k_Pi with this alpha
            n = np.arange(1, n_modes + 1, dtype=np.float64)
            lambdas = n ** alpha
            mu1 = np.mean(lambdas)
            mu2 = np.mean(lambdas ** 2)
            k_pi = mu2 / mu1

            assert k_pi == pytest.approx(K_PI_UNIVERSAL, abs=0.0001), \
                f"For n_modes={n_modes}, got k_Pi={k_pi}"

    def test_alpha_is_positive(self):
        """Test that computed alpha is positive."""
        for n_modes in [500, 1000, 2000]:
            alpha = compute_alpha_for_k_pi(n_modes)
            assert alpha > 0

    def test_alpha_is_in_expected_range(self):
        """Test that alpha is in the expected range (0.1 to 0.2)."""
        for n_modes in [500, 1000, 2000]:
            alpha = compute_alpha_for_k_pi(n_modes)
            assert 0.1 < alpha < 0.25


class TestLaplacianSpectrum:
    """Test the Laplacian spectrum simulation."""

    def test_spectrum_is_positive(self):
        """Test that all eigenvalues are positive."""
        spectrum = simulate_laplacian_spectrum(h11=1, h21=101, expected_modes=892)
        assert np.all(spectrum > 0)

    def test_spectrum_is_sorted(self):
        """Test that eigenvalues are sorted."""
        spectrum = simulate_laplacian_spectrum(h11=1, h21=101, expected_modes=892)
        assert np.all(np.diff(spectrum) >= 0)

    def test_spectrum_length(self):
        """Test that spectrum has expected length."""
        spectrum = simulate_laplacian_spectrum(h11=1, h21=101, expected_modes=892)
        assert len(spectrum) == 892

    def test_spectrum_reproducibility(self):
        """Test that spectrum is reproducible with same seed."""
        spectrum1 = simulate_laplacian_spectrum(h11=1, h21=101, seed=42, expected_modes=892)
        spectrum2 = simulate_laplacian_spectrum(h11=1, h21=101, seed=42, expected_modes=892)
        np.testing.assert_array_almost_equal(spectrum1, spectrum2)


class TestSpectralMoments:
    """Test the spectral moments computation."""

    def test_mu1_is_positive(self):
        """Test that first moment is positive."""
        spectrum = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        moments = compute_spectral_moments(spectrum)
        assert moments["mu1"] > 0

    def test_mu2_is_positive(self):
        """Test that second moment is positive."""
        spectrum = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        moments = compute_spectral_moments(spectrum)
        assert moments["mu2"] > 0

    def test_k_pi_is_positive(self):
        """Test that k_Pi is positive."""
        spectrum = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        moments = compute_spectral_moments(spectrum)
        assert moments["k_pi"] > 0

    def test_n_modes_correct(self):
        """Test that n_modes is correct."""
        spectrum = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        moments = compute_spectral_moments(spectrum)
        assert moments["n_modes"] == 5

    def test_empty_spectrum(self):
        """Test handling of empty spectrum."""
        moments = compute_spectral_moments(np.array([]))
        assert moments["mu1"] == 0.0
        assert moments["k_pi"] == 0.0
        assert moments["n_modes"] == 0


class TestUniversalityValidation:
    """Test the universality validation."""

    def test_validation_returns_dict(self):
        """Test that validation returns a dictionary."""
        results = validate_calabi_yau_spectral_universality()
        assert isinstance(results, dict)

    def test_validation_has_required_keys(self):
        """Test that results have required keys."""
        results = validate_calabi_yau_spectral_universality()
        required_keys = ["models", "k_pi_mean", "k_pi_std", "k_pi_universal",
                         "k_pi_from_constants", "is_universal"]
        for key in required_keys:
            assert key in results

    def test_validation_produces_universal_k_pi(self):
        """Test that k_Π is universal across all models."""
        results = validate_calabi_yau_spectral_universality()
        assert results["is_universal"] is True

    def test_k_pi_mean_close_to_universal(self):
        """Test that mean k_Π is close to universal value."""
        results = validate_calabi_yau_spectral_universality()
        assert results["k_pi_mean"] == pytest.approx(K_PI_UNIVERSAL, abs=0.001)

    def test_k_pi_std_is_small(self):
        """Test that k_Π standard deviation is small."""
        results = validate_calabi_yau_spectral_universality()
        assert results["k_pi_std"] < 0.01

    def test_all_models_have_similar_k_pi(self):
        """Test that all models have k_Π ≈ 2.5773."""
        results = validate_calabi_yau_spectral_universality()
        for model in results["models"]:
            assert model["k_pi"] == pytest.approx(K_PI_UNIVERSAL, abs=0.001), \
                f"Model {model['name']} has k_Pi={model['k_pi']}"


class TestInvariantValidation:
    """Test the spectral invariant validation."""

    def test_k_pi_spectral_invariant_is_valid(self):
        """Test that k_Π = C_PRIMARY / C_COHERENCE is valid."""
        assert validate_k_pi_spectral_invariant() is True


class TestIntegration:
    """Integration tests."""

    def test_end_to_end_validation(self):
        """Test the complete validation pipeline."""
        results = validate_calabi_yau_spectral_universality()

        # Check universality
        assert results["is_universal"] is True

        # Check k_Pi values for each model
        expected_k_pi_range = (2.575, 2.580)
        for model in results["models"]:
            assert expected_k_pi_range[0] < model["k_pi"] < expected_k_pi_range[1], \
                f"Model {model['name']} k_Pi={model['k_pi']} out of range"

        # Check consistency with spectral constants
        k_pi_from_c = C_PRIMARY / C_COHERENCE
        assert abs(results["k_pi_mean"] - k_pi_from_c) < 0.001


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
