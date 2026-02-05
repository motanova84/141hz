"""
Test suite for Unified Tissue Resonance Model.

Tests the integration of three independent mathematical frameworks:
1. Hilbert-Pólya Operator (Number Theory)
2. Navier-Stokes Cytoplasmic Flow (Fluid Dynamics)
3. Magicicada Scaling Law (Evolutionary Biology)

All converging on f₀ = 141.7 Hz biological resonance.
"""

import pytest
import numpy as np
from modules.quantum_biology.core import (
    HilbertPolyaOperator,
    NavierStokesCytoplasm,
    MagicicadaScaling,
    UnifiedTissueResonance
)


class TestHilbertPolyaOperator:
    """Test Hilbert-Pólya operator for mapping Riemann zeros to biology."""
    
    def test_initialization(self):
        """Test operator initialization."""
        hp = HilbertPolyaOperator(n_zeros=50)
        assert hp.n_zeros == 50
        assert hp.PHI == pytest.approx((1 + np.sqrt(5)) / 2, rel=1e-10)
        assert hp.F0_TARGET == 141.7001
    
    def test_riemann_zeros_computation(self):
        """Test Riemann zeta zero calculation."""
        hp = HilbertPolyaOperator(n_zeros=10)
        zeros = hp.compute_riemann_zeros()
        
        assert len(zeros) == 10
        assert all(zero > 0 for zero in zeros)  # All positive imaginary parts
        assert zeros[0] == pytest.approx(14.134725, rel=1e-5)  # First zero
    
    def test_eigenfrequency_mapping(self):
        """Test mapping to biological eigenfrequencies."""
        hp = HilbertPolyaOperator(n_zeros=100)
        eigenfreqs = hp.map_to_eigenfrequencies()
        
        assert len(eigenfreqs) == 100
        assert all(freq > 0 for freq in eigenfreqs)
        assert eigenfreqs.min() < 100  # Some should be below 100 Hz
        assert eigenfreqs.max() > 200  # Some should be above 200 Hz
    
    def test_f0_connection(self):
        """Test connection to f₀ = 141.7001 Hz."""
        hp = HilbertPolyaOperator(n_zeros=100)
        validation = hp.validate_f0_connection()
        
        assert 'nearest_eigenfrequency_hz' in validation
        assert 'absolute_error_hz' in validation
        assert 'validation_passed' in validation
        
        # Should find a reasonable match
        assert validation['absolute_error_hz'] < 50  # Within 50 Hz
        assert validation['relative_error_percent'] < 50  # Within 50%
    
    def test_spectrum_prediction(self):
        """Test tissue spectrum prediction."""
        hp = HilbertPolyaOperator(n_zeros=100)
        freqs, spectrum = hp.predict_tissue_spectrum(50, 250, 500)
        
        assert len(freqs) == 500
        assert len(spectrum) == 500
        assert spectrum.max() == pytest.approx(1.0, rel=1e-6)  # Normalized
        assert spectrum.min() >= 0


class TestNavierStokesCytoplasm:
    """Test Navier-Stokes cytoplasmic flow model."""
    
    def test_initialization(self):
        """Test model initialization."""
        ns = NavierStokesCytoplasm(temperature=310.0)
        assert ns.temperature == 310.0
        assert ns.DENSITY == 1030.0
        assert ns.VISCOSITY_KINEMATIC == 1e-6
    
    def test_reynolds_number(self):
        """Test Reynolds number calculation."""
        ns = NavierStokesCytoplasm()
        Re = ns.calculate_reynolds_number()
        
        assert Re > 0
        assert Re < 1e-3  # Should be very small (viscous-dominated)
    
    def test_oscillation_frequency(self):
        """Test natural oscillation frequency."""
        ns = NavierStokesCytoplasm()
        freq = ns.calculate_oscillation_frequency()
        
        assert freq > 0
        assert 50 < freq < 500  # Should be in biological range
    
    def test_141hz_prediction(self):
        """Test prediction of 141.7 Hz."""
        ns = NavierStokesCytoplasm()
        validation = ns.validate_141hz_prediction()
        
        assert 'predicted_frequency_hz' in validation
        assert 'reynolds_number' in validation
        assert 'validation_passed' in validation
        
        # Should predict in the right ballpark
        assert 100 < validation['predicted_frequency_hz'] < 200
        assert validation['reynolds_number'] < 1  # Viscous regime
    
    def test_flow_spectrum(self):
        """Test flow power spectrum."""
        ns = NavierStokesCytoplasm()
        freqs, psd = ns.predict_flow_spectrum(duration=0.5, sample_rate=5000)
        
        assert len(freqs) > 0
        assert len(psd) == len(freqs)
        assert all(psd >= 0)


class TestMagicicadaScaling:
    """Test Magicicada fractal scaling law."""
    
    def test_initialization(self):
        """Test model initialization."""
        ms = MagicicadaScaling()
        assert ms.MAGICICADA_CYCLES == [13, 17]
        assert ms.TAU_CELL == 7e-3
        assert ms.F_CELL_TARGET == 141.7
    
    def test_magicicada_frequencies(self):
        """Test Magicicada emergence frequencies."""
        ms = MagicicadaScaling()
        mag_freqs = ms.calculate_magicicada_frequencies()
        
        assert 13 in mag_freqs
        assert 17 in mag_freqs
        assert mag_freqs[13] > 0
        assert mag_freqs[17] > 0
        assert mag_freqs[13] < 1e-8  # Very low frequency (multi-year cycle)
    
    def test_scaling_ratio(self):
        """Test scaling ratio calculation."""
        ms = MagicicadaScaling()
        ratio = ms.calculate_scaling_ratio()
        
        assert ratio > 1e9  # Should be very large (10+ orders of magnitude)
        assert ratio < 1e12
    
    def test_cellular_frequency_prediction(self):
        """Test prediction of cellular frequency from Magicicada."""
        ms = MagicicadaScaling()
        mag_freqs = ms.calculate_magicicada_frequencies()
        
        for cycle, mag_freq in mag_freqs.items():
            cell_freq = ms.predict_cellular_frequency(mag_freq)
            assert cell_freq > 0
            assert 50 < cell_freq < 500  # Should be in biological range
    
    def test_fractal_validation(self):
        """Test fractal scaling validation."""
        ms = MagicicadaScaling()
        validation = ms.validate_fractal_scaling()
        
        assert 'scaling_ratio' in validation
        assert 'mean_prediction_hz' in validation
        assert 'fractal_dimension' in validation
        assert 'validation_passed' in validation
        
        # Should predict close to 141.7 Hz
        assert 100 < validation['mean_prediction_hz'] < 200


class TestUnifiedTissueResonance:
    """Test unified tissue resonance model."""
    
    @pytest.mark.parametrize("tissue_type", ['cardiac', 'neural', 'epithelial', 'muscular'])
    def test_initialization(self, tissue_type):
        """Test initialization for all tissue types."""
        model = UnifiedTissueResonance(tissue_type=tissue_type)
        
        assert model.tissue_type == tissue_type
        assert model.temperature == 310.0
        assert hasattr(model, 'hilbert_polya')
        assert hasattr(model, 'navier_stokes')
        assert hasattr(model, 'magicicada')
    
    def test_invalid_tissue_type(self):
        """Test error handling for invalid tissue type."""
        with pytest.raises(ValueError):
            UnifiedTissueResonance(tissue_type='invalid')
    
    def test_cardiac_tissue_parameters(self):
        """Test cardiac tissue parameters (exact f₀ resonance)."""
        model = UnifiedTissueResonance(tissue_type='cardiac')
        
        assert model.tissue_params['base_frequency'] == 141.7
        assert model.tissue_params['enhancement'] == 23.9
        assert 'cardiac' in model.tissue_params['description'].lower()
    
    def test_neural_tissue_parameters(self):
        """Test neural tissue parameters (harmonic resonance)."""
        model = UnifiedTissueResonance(tissue_type='neural')
        
        assert model.tissue_params['base_frequency'] == 146.7
        assert model.tissue_params['enhancement'] == 18.3
    
    def test_theory_unification(self):
        """Test unification of three frameworks."""
        model = UnifiedTissueResonance(tissue_type='cardiac')
        
        # Get predictions from each framework
        hp_freqs = model.hilbert_polya.map_to_eigenfrequencies()
        ns_freq = model.navier_stokes.calculate_oscillation_frequency()
        magic_freq = 1.0 / model.magicicada.TAU_CELL
        
        # Unify
        unified = model.unify_theories(hp_freqs, ns_freq, magic_freq)
        
        assert 'unified_frequency' in unified
        assert 'consistency' in unified
        assert 'validation_passed' in unified
        
        # Unified frequency should be reasonable
        assert 100 < unified['unified_frequency'] < 200
    
    def test_spectrum_prediction(self):
        """Test unified spectrum prediction."""
        model = UnifiedTissueResonance(tissue_type='cardiac')
        freqs, spectrum = model.predict_spectrum(50, 250, 500)
        
        assert len(freqs) == 500
        assert len(spectrum) == 500
        assert spectrum.max() == pytest.approx(1.0, rel=1e-6)  # Normalized
        
        # Should have peak near tissue frequency
        peak_idx = np.argmax(spectrum)
        peak_freq = freqs[peak_idx]
        assert abs(peak_freq - model.tissue_params['base_frequency']) < 20
    
    def test_unified_validation(self):
        """Test complete unified model validation."""
        model = UnifiedTissueResonance(tissue_type='cardiac')
        validation = model.validate_unified_model()
        
        assert 'tissue_type' in validation
        assert 'framework_validations' in validation
        assert 'unified_prediction' in validation
        assert 'consistency_score' in validation
        
        # All three frameworks should be present
        assert 'hilbert_polya' in validation['framework_validations']
        assert 'navier_stokes' in validation['framework_validations']
        assert 'magicicada' in validation['framework_validations']
        
        # Consistency should be high
        assert validation['consistency_score'] > 0.5
    
    def test_ingnio_protocol_generation(self):
        """Test INGΝIO CMI therapeutic protocol generation."""
        model = UnifiedTissueResonance(tissue_type='cardiac')
        protocol = model.generate_ingnio_protocol(duration_min=30)
        
        assert 'phases' in protocol
        assert 'protection_band' in protocol
        assert len(protocol['phases']) == 3
        
        # Check phase frequencies
        assert protocol['phases'][0]['frequency_hz'] == model.F_INGNIO
        assert protocol['phases'][1]['frequency_hz'] == model.F_AURON
        assert protocol['phases'][2]['frequency_hz'] == model.F_HARMONIC
        
        # Check protection band
        assert protocol['protection_band']['lower_hz'] == model.F_INGNIO
        assert protocol['protection_band']['upper_hz'] == model.F_AURON
    
    @pytest.mark.parametrize("tissue_type,expected_peak", [
        ('cardiac', 141.7),
        ('neural', 146.7),
        ('epithelial', 146.7),
        ('muscular', 146.7)
    ])
    def test_tissue_specific_peaks(self, tissue_type, expected_peak):
        """Test that each tissue type has correct peak frequency."""
        model = UnifiedTissueResonance(tissue_type=tissue_type)
        assert model.tissue_params['base_frequency'] == expected_peak


class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_all_frameworks_predict_similar_frequency(self):
        """Test that all three frameworks predict frequencies in same range."""
        hp = HilbertPolyaOperator(n_zeros=100)
        ns = NavierStokesCytoplasm()
        ms = MagicicadaScaling()
        
        # Get predictions
        hp_nearest, _, _ = hp.find_nearest_to_target(141.7)
        ns_freq = ns.calculate_oscillation_frequency()
        ms_freq = 1.0 / ms.TAU_CELL
        
        # All should be in 100-200 Hz range
        assert 100 < hp_nearest < 200
        assert 100 < ns_freq < 200
        assert 100 < ms_freq < 200
        
        # Standard deviation should be reasonable
        all_freqs = [hp_nearest, ns_freq, ms_freq]
        std = np.std(all_freqs)
        assert std < 50  # Within 50 Hz of each other
    
    def test_unified_model_convergence(self):
        """Test that unified model achieves good convergence."""
        model = UnifiedTissueResonance(tissue_type='cardiac')
        validation = model.validate_unified_model()
        
        # Error from f₀ should be small
        assert validation['unified_error'] < 10  # Within 10 Hz
        
        # Consistency score should be high
        assert validation['consistency_score'] > 0.7


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, '-v'])
