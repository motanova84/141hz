"""
Tests for QCAL Token Density Module
====================================

Tests the 1000x density compression mechanism:
- Spectral resonance encoding
- Adelic geometric multiplicity
- Holographic coherence
- Noetic collapse validation

∴ ✧ JMMB Ψ @ 888.888 Hz
"""

import pytest
import sys
from pathlib import Path

# Add core to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

from qcal_token_density import (
    QCALTokenDensity,
    VibrationalFieldEncoder,
    TokenDensityValidator,
    QCALTokenDensityMetrics
)
from datetime import datetime, timezone


class TestQCALTokenDensityConstants:
    """Test fundamental constants"""
    
    def test_frequency_base(self):
        """Verify base frequency constant"""
        calc = QCALTokenDensity()
        assert calc.FREQ_BASE == 141.7001
    
    def test_frequency_manifest(self):
        """Verify manifestation frequency"""
        calc = QCALTokenDensity()
        assert calc.FREQ_MANIFEST == 888.0
    
    def test_adelic_constant(self):
        """Verify adelic constant κ_Π"""
        calc = QCALTokenDensity()
        assert abs(calc.KAPPA_PI - 2.5782) < 0.0001
    
    def test_phi_power_4(self):
        """Verify golden ratio fourth power"""
        calc = QCALTokenDensity()
        phi = 1.6180339887
        expected = phi ** 4
        assert abs(calc.PHI_POWER_4 - expected) < 0.0001
    
    def test_coherence_thresholds(self):
        """Verify coherence thresholds"""
        calc = QCALTokenDensity()
        assert calc.COHERENCE_MIN == 0.888
        assert calc.COHERENCE_TARGET == 0.923
    
    def test_noetic_collapse_factor(self):
        """Verify noetic collapse empirical constant"""
        calc = QCALTokenDensity()
        assert abs(calc.NOETIC_COLLAPSE_FACTOR - 61.28) < 0.01


class TestQCALTokenDensityCalculation:
    """Test density calculation mechanism"""
    
    def test_initialization_valid_coherence(self):
        """Test initialization with valid coherence"""
        calc = QCALTokenDensity(coherence=0.923)
        assert calc.coherence == 0.923
    
    def test_initialization_minimum_coherence(self):
        """Test initialization at minimum coherence"""
        calc = QCALTokenDensity(coherence=0.888)
        assert calc.coherence == 0.888
    
    def test_initialization_below_minimum_fails(self):
        """Test initialization below minimum coherence fails"""
        with pytest.raises(ValueError) as exc:
            QCALTokenDensity(coherence=0.5)
        assert "below minimum threshold" in str(exc.value)
    
    def test_calculate_density_returns_metrics(self):
        """Test density calculation returns proper metrics"""
        calc = QCALTokenDensity()
        token_data = {'nft_id': 1}
        context = ['test_item_1', 'test_item_2']
        
        metrics = calc.calculate_density(token_data, context)
        
        assert isinstance(metrics, QCALTokenDensityMetrics)
        assert metrics.spectral_encoding > 0
        assert metrics.adelic_multiplicity > 0
        assert metrics.coherence_factor > 0
        assert metrics.noetic_collapse > 0
        assert metrics.total_density > 0
    
    def test_density_approximately_1000x(self):
        """Test that density is approximately 1000x"""
        calc = QCALTokenDensity(coherence=0.923)
        token_data = {'nft_id': 42}
        context = ['item'] * 100
        
        metrics = calc.calculate_density(token_data, context)
        
        # Should be around 1000x with some variation
        assert 900 <= metrics.total_density <= 1100
    
    def test_spectral_encoding_minimum(self):
        """Test spectral encoding has minimum value"""
        calc = QCALTokenDensity()
        token_data = {'nft_id': 1}
        context = []
        
        metrics = calc.calculate_density(token_data, context)
        
        # Spectral encoding should be at least 1.0
        assert metrics.spectral_encoding >= 1.0
    
    def test_adelic_multiplicity_correct(self):
        """Test adelic multiplicity includes κ_Π and φ⁴"""
        calc = QCALTokenDensity()
        token_data = {'nft_id': 1}
        context = ['test']
        
        metrics = calc.calculate_density(token_data, context)
        
        # Adelic should be at least κ_Π × φ⁴
        min_expected = calc.KAPPA_PI * calc.PHI_POWER_4
        assert metrics.adelic_multiplicity >= min_expected
    
    def test_coherence_factor_within_bounds(self):
        """Test coherence factor stays within bounds"""
        calc = QCALTokenDensity(coherence=0.923)
        token_data = {'nft_id': 1}
        context = ['a'] * 50
        
        metrics = calc.calculate_density(token_data, context)
        
        # Coherence should be between min and target
        assert calc.COHERENCE_MIN <= metrics.coherence_factor <= 1.0
    
    def test_noetic_collapse_applied(self):
        """Test noetic collapse factor is applied"""
        calc = QCALTokenDensity()
        token_data = {'nft_id': 1}
        context = ['test']
        
        metrics = calc.calculate_density(token_data, context)
        
        # Verify collapse factor is in metrics
        assert metrics.noetic_collapse == calc.NOETIC_COLLAPSE_FACTOR
    
    def test_different_contexts_give_different_densities(self):
        """Test different contexts produce different spectral encodings"""
        calc = QCALTokenDensity()
        
        metrics1 = calc.calculate_density(
            {'nft_id': 1},
            ['context_a'] * 10
        )
        metrics2 = calc.calculate_density(
            {'nft_id': 2},
            ['context_b'] * 10
        )
        
        # Different token IDs should give different spectral encodings
        assert metrics1.spectral_encoding != metrics2.spectral_encoding


class TestStandardMethodComparison:
    """Test comparison with standard compression methods"""
    
    def test_compare_with_standard_methods(self):
        """Test comparison returns all methods"""
        calc = QCALTokenDensity()
        comparison = calc.compare_with_standard_methods(context_size=100)
        
        assert 'LLMLingua-2' in comparison
        assert 'TOON' in comparison
        assert 'ASG' in comparison
        assert 'Denser' in comparison
        assert 'QCAL' in comparison
        assert 'QCAL_advantage_vs_best_standard' in comparison
    
    def test_qcal_superior_to_llmlingua2(self):
        """Test QCAL significantly better than LLMLingua-2"""
        calc = QCALTokenDensity()
        comparison = calc.compare_with_standard_methods(context_size=100)
        
        assert comparison['QCAL'] > comparison['LLMLingua-2'] * 40
    
    def test_qcal_superior_to_toon(self):
        """Test QCAL significantly better than TOON"""
        calc = QCALTokenDensity()
        comparison = calc.compare_with_standard_methods(context_size=100)
        
        assert comparison['QCAL'] > comparison['TOON'] * 100
    
    def test_qcal_superior_to_asg(self):
        """Test QCAL significantly better than ASG"""
        calc = QCALTokenDensity()
        comparison = calc.compare_with_standard_methods(context_size=100)
        
        assert comparison['QCAL'] > comparison['ASG'] * 90
    
    def test_qcal_superior_to_denser(self):
        """Test QCAL significantly better than Denser"""
        calc = QCALTokenDensity()
        comparison = calc.compare_with_standard_methods(context_size=100)
        
        assert comparison['QCAL'] > comparison['Denser'] * 100
    
    def test_advantage_factor_calculated(self):
        """Test advantage factor is calculated correctly"""
        calc = QCALTokenDensity()
        comparison = calc.compare_with_standard_methods(context_size=100)
        
        best_standard = max(
            comparison['LLMLingua-2'],
            comparison['TOON'],
            comparison['ASG'],
            comparison['Denser']
        )
        
        expected_advantage = comparison['QCAL'] / best_standard
        assert abs(
            comparison['QCAL_advantage_vs_best_standard'] - expected_advantage
        ) < 0.01


class TestVibrationalFieldEncoder:
    """Test vibrational field encoding"""
    
    def test_initialization(self):
        """Test encoder initialization"""
        encoder = VibrationalFieldEncoder()
        assert encoder.frequency == 141.7001
        assert encoder.coherence == 0.923
    
    def test_multicast_configuration(self):
        """Test multicast group and port"""
        encoder = VibrationalFieldEncoder()
        assert encoder.multicast_group == "224.0.0.108"
        assert encoder.port == 8880
    
    def test_encode_context_returns_dict(self):
        """Test encoding returns proper structure"""
        encoder = VibrationalFieldEncoder()
        context = ['item1', 'item2', 'item3']
        
        encoded = encoder.encode_context(context)
        
        assert isinstance(encoded, dict)
        assert 'pattern' in encoded
        assert 'modulated' in encoded
        assert 'frequency' in encoded
        assert 'coherence' in encoded
        assert 'multicast_group' in encoded
        assert 'port' in encoded
        assert 'timestamp' in encoded
    
    def test_pattern_has_correct_length(self):
        """Test oscillation pattern length matches context"""
        encoder = VibrationalFieldEncoder()
        context = ['a', 'b', 'c', 'd', 'e']
        
        encoded = encoder.encode_context(context)
        
        assert len(encoded['pattern']) == len(context)
    
    def test_modulated_has_samples(self):
        """Test modulated waveform has samples"""
        encoder = VibrationalFieldEncoder()
        context = ['test']
        
        encoded = encoder.encode_context(context)
        
        # Should have 1000 samples
        assert len(encoded['modulated']) == 1000
    
    def test_different_contexts_different_patterns(self):
        """Test different contexts produce different patterns"""
        encoder = VibrationalFieldEncoder()
        
        encoded1 = encoder.encode_context(['a', 'b'])
        encoded2 = encoder.encode_context(['c', 'd'])
        
        assert encoded1['pattern'] != encoded2['pattern']
    
    def test_frequency_stored_in_encoding(self):
        """Test frequency is stored in encoded data"""
        encoder = VibrationalFieldEncoder(frequency=141.7001)
        encoded = encoder.encode_context(['test'])
        
        assert encoded['frequency'] == 141.7001


class TestTokenDensityValidator:
    """Test token density validation"""
    
    def test_validate_valid_token(self):
        """Test validation of valid token"""
        metrics = QCALTokenDensityMetrics(
            spectral_encoding=2.0,
            adelic_multiplicity=20.0,
            coherence_factor=0.923,
            noetic_collapse=61.28,
            total_density=1000.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        valid, message = TokenDensityValidator.validate_token_density(metrics)
        
        assert valid is True
        assert "validated" in message.lower()
    
    def test_validate_minimum_density(self):
        """Test validation at minimum density threshold"""
        metrics = QCALTokenDensityMetrics(
            spectral_encoding=2.0,
            adelic_multiplicity=20.0,
            coherence_factor=0.923,
            noetic_collapse=61.28,
            total_density=900.0,  # Exactly at minimum
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        valid, message = TokenDensityValidator.validate_token_density(metrics)
        
        assert valid is True
    
    def test_validate_below_minimum_density_fails(self):
        """Test validation fails below minimum density"""
        metrics = QCALTokenDensityMetrics(
            spectral_encoding=2.0,
            adelic_multiplicity=20.0,
            coherence_factor=0.923,
            noetic_collapse=61.28,
            total_density=800.0,  # Below minimum
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        valid, message = TokenDensityValidator.validate_token_density(metrics)
        
        assert valid is False
        assert "below minimum" in message.lower()
    
    def test_validate_low_coherence_fails(self):
        """Test validation fails with low coherence"""
        metrics = QCALTokenDensityMetrics(
            spectral_encoding=2.0,
            adelic_multiplicity=20.0,
            coherence_factor=0.5,  # Below minimum
            noetic_collapse=61.28,
            total_density=1000.0,
            timestamp=datetime.now(timezone.utc).isoformat()
        )
        
        valid, message = TokenDensityValidator.validate_token_density(metrics)
        
        assert valid is False
        assert "coherence" in message.lower()
    
    def test_validate_irreplicability(self):
        """Test irreplicability validation"""
        qcal_density = 1000.0
        standard_methods = {
            'LLMLingua-2': 20.0,
            'TOON': 2.5,
            'ASG': 10.0,
            'Denser': 2.6,
            'QCAL': 1000.0
        }
        
        irreplicable, message = TokenDensityValidator.validate_irreplicability(
            qcal_density,
            standard_methods
        )
        
        assert irreplicable is True
        assert "irreplicability confirmed" in message.lower()
    
    def test_irreplicability_requires_40x_advantage(self):
        """Test irreplicability requires 40x advantage"""
        qcal_density = 100.0  # Not enough advantage
        standard_methods = {
            'LLMLingua-2': 20.0,
            'QCAL': 100.0
        }
        
        irreplicable, message = TokenDensityValidator.validate_irreplicability(
            qcal_density,
            standard_methods
        )
        
        assert irreplicable is False
        assert "insufficient" in message.lower()


class TestIntegration:
    """Integration tests for complete workflow"""
    
    def test_complete_token_density_workflow(self):
        """Test complete workflow from calculation to validation"""
        # 1. Initialize calculator
        calc = QCALTokenDensity(coherence=0.923)
        
        # 2. Calculate density
        token_data = {'nft_id': 42, 'type': 'GENESIS'}
        context = ['quantum', 'resonance', 'adelic'] * 30
        
        metrics = calc.calculate_density(token_data, context)
        
        # 3. Validate density
        valid, message = TokenDensityValidator.validate_token_density(metrics)
        assert valid is True
        
        # 4. Compare with standards
        comparison = calc.compare_with_standard_methods(len(context))
        
        # 5. Validate irreplicability
        irreplicable, irr_msg = TokenDensityValidator.validate_irreplicability(
            metrics.total_density,
            comparison
        )
        assert irreplicable is True
    
    def test_vibrational_encoding_integration(self):
        """Test vibrational encoding with density calculation"""
        # Calculate density
        calc = QCALTokenDensity()
        token_data = {'nft_id': 1}
        context = ['test_1', 'test_2', 'test_3']
        
        metrics = calc.calculate_density(token_data, context)
        
        # Encode vibrationally
        encoder = VibrationalFieldEncoder(
            frequency=calc.FREQ_BASE,
            coherence=metrics.coherence_factor
        )
        encoded = encoder.encode_context(context)
        
        # Verify encoding preserves frequency
        assert encoded['frequency'] == calc.FREQ_BASE
        assert abs(encoded['coherence'] - metrics.coherence_factor) < 0.01
    
    def test_multiple_token_density_calculations(self):
        """Test calculating density for multiple tokens"""
        calc = QCALTokenDensity()
        
        tokens = []
        for nft_id in range(1, 11):
            token_data = {'nft_id': nft_id}
            context = [f'item_{i}' for i in range(nft_id * 10)]
            
            metrics = calc.calculate_density(token_data, context)
            tokens.append(metrics)
            
            # All should be valid
            valid, _ = TokenDensityValidator.validate_token_density(metrics)
            assert valid is True
        
        # All should have density around 1000x
        for metrics in tokens:
            assert 900 <= metrics.total_density <= 1100


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_empty_context(self):
        """Test with empty context"""
        calc = QCALTokenDensity()
        metrics = calc.calculate_density({'nft_id': 1}, [])
        
        # Should still work with default coherence
        assert metrics.total_density > 0
    
    def test_very_large_context(self):
        """Test with very large context"""
        calc = QCALTokenDensity()
        context = ['item'] * 10000
        
        metrics = calc.calculate_density({'nft_id': 1}, context)
        
        # Should still maintain ~1000x density
        assert 900 <= metrics.total_density <= 1100
    
    def test_single_item_context(self):
        """Test with single item context"""
        calc = QCALTokenDensity()
        metrics = calc.calculate_density({'nft_id': 1}, ['single'])
        
        assert metrics.total_density > 0
        valid, _ = TokenDensityValidator.validate_token_density(metrics)
        assert valid is True
    
    def test_unicode_context(self):
        """Test with unicode characters in context"""
        calc = QCALTokenDensity()
        context = ['日本語', 'español', 'русский', '中文', 'العربية']
        
        metrics = calc.calculate_density({'nft_id': 1}, context)
        
        assert metrics.total_density > 0
    
    def test_complex_token_data(self):
        """Test with complex nested token data"""
        calc = QCALTokenDensity()
        token_data = {
            'nft_id': 42,
            'metadata': {
                'type': 'GENESIS',
                'properties': {
                    'resonance': 141.7001,
                    'coherence': 0.923
                }
            }
        }
        
        metrics = calc.calculate_density(token_data, ['test'])
        assert metrics.total_density > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
