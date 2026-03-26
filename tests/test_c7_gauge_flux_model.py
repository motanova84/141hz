"""
Tests for C₇ Gauge Flux Model - High Physics Route

Tests for the C7 gauge flux model that demonstrates the frequency shift
134.425 Hz → 141.7001 Hz as an eigenvalue of a flux-bound state.
"""

import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import pytest
import numpy as np
from physics.c7_gauge_flux_model import (
    C7GaugeFluxModel,
    demonstrate_gauge_flux_shift
)
from qcal.constants import F0_HZ


class TestC7GaugeFluxModel:
    """Tests for the C7GaugeFluxModel class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.model = C7GaugeFluxModel(n_nodes=7, coupling_J=1.0)
    
    def test_initialization(self):
        """Test model initialization."""
        assert self.model.n_nodes == 7
        assert self.model.J == 1.0
        assert self.model.f_target == F0_HZ
        assert self.model.f_bare == 134.425
        assert abs(self.model.delta_f - (F0_HZ - 134.425)) < 1e-6
    
    def test_energy_dispersion_phi_zero(self):
        """Test energy dispersion with zero flux."""
        # For Φ = 0, energies should be symmetric
        energies = [self.model.energy_dispersion(k, 0.0) for k in range(7)]
        
        # k=0 should give minimum energy: -2J cos(0) = -2J
        assert abs(energies[0] - (-2.0)) < 1e-10
        
        # Energies should be real
        for e in energies:
            assert isinstance(e, (int, float, np.number))
    
    def test_energy_dispersion_bounds(self):
        """Test that energies are bounded correctly."""
        # For any Φ and k, energy should be in [-2J, 2J]
        phi_values = np.linspace(0, 2*np.pi, 20)
        
        for phi in phi_values:
            for k in range(7):
                energy = self.model.energy_dispersion(k, phi)
                assert -2.1 <= energy <= 2.1  # Allow small numerical error
    
    def test_energy_dispersion_invalid_k(self):
        """Test that invalid k raises ValueError."""
        with pytest.raises(ValueError, match="Mode k must be"):
            self.model.energy_dispersion(-1, 0.0)
        
        with pytest.raises(ValueError, match="Mode k must be"):
            self.model.energy_dispersion(7, 0.0)
    
    def test_energy_spectrum_length(self):
        """Test that energy spectrum has correct length."""
        spectrum = self.model.energy_spectrum(0.0)
        assert len(spectrum) == 7
    
    def test_energy_spectrum_ordering(self):
        """Test that energy spectrum is computed correctly."""
        phi = 0.5
        spectrum = self.model.energy_spectrum(phi)
        
        # Compare with individual calculations
        for k in range(7):
            expected = self.model.energy_dispersion(k, phi)
            assert abs(spectrum[k] - expected) < 1e-10
    
    def test_frequency_from_flux_positive(self):
        """Test that frequency is always positive."""
        phi_values = np.linspace(0, np.pi, 20)
        
        for phi in phi_values:
            freq = self.model.frequency_from_flux(phi, self.model.f_bare)
            assert freq > 0, f"Frequency should be positive, got {freq}"
    
    def test_frequency_from_flux_monotonic(self):
        """Test that frequency increases with flux in [0, π/2]."""
        phi_values = np.linspace(0, np.pi/2, 50)
        frequencies = [
            self.model.frequency_from_flux(phi, self.model.f_bare)
            for phi in phi_values
        ]
        
        # Should be roughly increasing
        for i in range(len(frequencies) - 1):
            # Allow some numerical noise
            assert frequencies[i+1] >= frequencies[i] - 0.1
    
    def test_find_optimal_flux_convergence(self):
        """Test that optimization finds a flux close to target."""
        result = self.model.find_optimal_flux(
            target_frequency=F0_HZ,
            phi_range=(0.0, np.pi),
            n_points=1000
        )
        
        assert 'phi_optimal' in result
        assert 'frequency' in result
        assert 'error' in result
        assert 'theta_per_bond' in result
        
        # Error should be small (within 0.1 Hz for 1000 points)
        assert result['error'] < 0.1
        
        # Frequency should be close to target
        assert abs(result['frequency'] - F0_HZ) < 0.1
    
    def test_find_optimal_flux_theoretical_range(self):
        """Test that optimal flux reproduces the target frequency."""
        result = self.model.find_optimal_flux(
            target_frequency=F0_HZ,
            phi_range=(0.0, np.pi),
            n_points=1000
        )
        
        # The optimal flux should reproduce the target frequency closely
        assert abs(result['frequency'] - F0_HZ) < 0.1
        
        # Flux should be in a reasonable range [0, π]
        assert 0.0 <= result['phi_optimal'] <= np.pi
        
        # The error should be small
        assert result['error'] < 0.1
    
    def test_chiral_holonomy(self):
        """Test chiral holonomy calculation."""
        phi = 0.5
        holonomy = self.model.chiral_holonomy(phi)
        
        # Holonomy should equal flux
        assert abs(holonomy - phi) < 1e-10
    
    def test_chiral_torsion_per_bond(self):
        """Test chiral torsion per bond."""
        phi = 0.7
        torsion = self.model.chiral_torsion_per_bond(phi)
        
        # Should be phi/7
        expected = phi / 7.0
        assert abs(torsion - expected) < 1e-10
    
    def test_frustration_parameter(self):
        """Test magnetic frustration parameter."""
        # Full quantum: Φ = 2π → f = 1
        frustration_full = self.model.frustration_parameter(2 * np.pi)
        assert abs(frustration_full - 1.0) < 1e-10
        
        # Half quantum: Φ = π → f = 0.5
        frustration_half = self.model.frustration_parameter(np.pi)
        assert abs(frustration_half - 0.5) < 1e-10
        
        # Zero flux: Φ = 0 → f = 0
        frustration_zero = self.model.frustration_parameter(0.0)
        assert abs(frustration_zero) < 1e-10
    
    def test_validate_flux_hypothesis_structure(self):
        """Test validate_flux_hypothesis returns correct structure."""
        result = self.model.validate_flux_hypothesis(0.4, tolerance_hz=0.01)
        
        required_keys = [
            'is_valid', 'frequency', 'error_hz', 'error_percent',
            'holonomy', 'torsion_per_bond', 'frustration', 'phi_rad',
            'target_frequency', 'bare_frequency'
        ]
        
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
    
    def test_validate_flux_hypothesis_tolerance(self):
        """Test that validation respects tolerance."""
        # First find optimal flux
        opt_result = self.model.find_optimal_flux(n_points=1000)
        phi_opt = opt_result['phi_optimal']
        
        # Validate with strict tolerance
        validation = self.model.validate_flux_hypothesis(
            phi_opt,
            tolerance_hz=0.1
        )
        
        # Should pass validation
        assert validation['is_valid']
        assert validation['error_hz'] < 0.1
    
    def test_demonstrate_function(self):
        """Test the demonstrate_gauge_flux_shift function."""
        results = demonstrate_gauge_flux_shift()
        
        assert 'model' in results
        assert 'optimization' in results
        assert 'validation' in results
        assert 'conclusion' in results
        
        # Check model parameters
        assert results['model']['n_nodes'] == 7
        assert results['model']['f_target'] == F0_HZ
        assert results['model']['f_bare'] == 134.425
        
        # Check optimization succeeded
        assert results['optimization']['error'] < 0.1
        
        # Check conclusion has required fields
        assert 'phi_sweet_spot_rad' in results['conclusion']
        assert 'chiral_torsion_per_bond_rad' in results['conclusion']
        assert 'message' in results['conclusion']


class TestPhysicalConsistency:
    """Tests for physical consistency of the model."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.model = C7GaugeFluxModel(n_nodes=7, coupling_J=1.0)
    
    def test_flux_periodicity(self):
        """Test that energies have expected periodicity."""
        k = 3
        phi0 = 0.5
        
        # For a discrete cycle C7, the period is 14π (not 2π)
        # because phase = (2πk + Φ)/7
        # For it to repeat, we need (2πk + Φ + ΔΦ)/7 = (2πk + Φ)/7 + 2π
        # So ΔΦ = 14π
        
        e0 = self.model.energy_dispersion(k, phi0)
        e_14pi = self.model.energy_dispersion(k, phi0 + 14*np.pi)
        
        # Should be equal (up to numerical precision)
        assert abs(e0 - e_14pi) < 1e-8
    
    def test_time_reversal_symmetry_breaking(self):
        """Test that flux breaks time-reversal symmetry."""
        # For Φ ≠ 0, the spectrum should not be symmetric under k → -k
        phi = 0.4
        
        # Compare k=1 and k=-1 (mod 7) = k=6
        e1 = self.model.energy_dispersion(1, phi)
        e6 = self.model.energy_dispersion(6, phi)
        
        # For Φ=0, these would be equal. For Φ≠0, they should differ
        if phi != 0:
            # Allow small tolerance for numerical precision
            # but they should be measurably different
            assert abs(e1 - e6) > 1e-6
    
    def test_zero_flux_limit(self):
        """Test that Φ=0 gives expected symmetric spectrum."""
        spectrum = self.model.energy_spectrum(0.0)
        
        # k=0 should give minimum energy
        assert spectrum[0] < spectrum[1]
        
        # Spectrum should be symmetric: ε(k) = ε(7-k)
        for k in range(1, 4):
            assert abs(spectrum[k] - spectrum[7-k]) < 1e-10
    
    def test_energy_gap_increases_with_flux(self):
        """Test that energy gap increases with flux in [0, π/2]."""
        phi_values = np.linspace(0, np.pi/2, 20)
        gaps = []
        
        for phi in phi_values:
            e0 = self.model.energy_dispersion(0, phi)
            e1 = self.model.energy_dispersion(1, phi)
            gap = abs(e1 - e0)
            gaps.append(gap)
        
        # Gap should generally increase (monotonic in smooth model)
        # Check that final gap > initial gap
        assert gaps[-1] > gaps[0]
    
    def test_torsion_sign_convention(self):
        """Test that torsion has correct sign."""
        phi = 0.5
        torsion = self.model.chiral_torsion_per_bond(phi)
        
        # For positive flux, torsion should be positive
        if phi > 0:
            assert torsion > 0
        elif phi < 0:
            assert torsion < 0
        else:
            assert abs(torsion) < 1e-10


class TestNumericalStability:
    """Tests for numerical stability."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.model = C7GaugeFluxModel(n_nodes=7, coupling_J=1.0)
    
    def test_large_flux_values(self):
        """Test that model handles large flux values."""
        # Test with flux = 100π (should wrap around)
        phi_large = 100 * np.pi
        
        # Should not raise error
        energy = self.model.energy_dispersion(0, phi_large)
        assert np.isfinite(energy)
        assert -2.1 <= energy <= 2.1
    
    def test_negative_flux(self):
        """Test that model handles negative flux."""
        phi_neg = -0.5
        
        # Should work without error
        spectrum = self.model.energy_spectrum(phi_neg)
        assert len(spectrum) == 7
        assert all(np.isfinite(spectrum))
    
    def test_very_small_flux(self):
        """Test numerical precision for very small flux."""
        phi_tiny = 1e-10
        
        # Should be close to zero-flux case
        e0_zero = self.model.energy_dispersion(0, 0.0)
        e0_tiny = self.model.energy_dispersion(0, phi_tiny)
        
        assert abs(e0_zero - e0_tiny) < 1e-8
    
    def test_high_resolution_optimization(self):
        """Test optimization with very high resolution."""
        result = self.model.find_optimal_flux(n_points=10000)
        
        # Should converge to very small error
        assert result['error'] < 0.01
        assert np.isfinite(result['phi_optimal'])
        assert 0 <= result['phi_optimal'] <= 2*np.pi


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
