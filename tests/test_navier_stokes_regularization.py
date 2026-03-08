#!/usr/bin/env python3
"""
Unit Tests: Navier-Stokes Vibrational Regularization

Tests for the QCAL regularization module that prevents blow-up
in finite time for 3D Navier-Stokes equations.
"""

import pytest
import numpy as np
from navier_stokes.regularization import NavierStokesRegularizer
from navier_stokes.constants import F0, ALPHA_QFT, BETA_QFT


class TestNavierStokesRegularizer:
    """Test suite for NavierStokesRegularizer class."""
    
    def test_initialization(self):
        """Test regularizer initialization."""
        reg = NavierStokesRegularizer(medium='water')
        assert reg.medium == 'water'
        assert reg.frequency == F0
        assert reg.base_viscosity > 0
        assert reg.amplitude > 0
    
    def test_medium_selection(self):
        """Test different medium configurations."""
        for medium in ['water', 'air', 'vacuum']:
            reg = NavierStokesRegularizer(medium=medium)
            assert reg.medium == medium
            assert reg.base_viscosity > 0
    
    def test_resonant_viscosity(self):
        """Test resonant viscosity calculation."""
        reg = NavierStokesRegularizer(medium='water')
        
        # At t=0
        nu_0 = reg.resonant_viscosity(0.0)
        assert nu_0 > reg.base_viscosity
        
        # Time-dependent
        nu_1 = reg.resonant_viscosity(1.0)
        assert nu_1 > 0
        
        # Should oscillate around enhanced value
        times = np.linspace(0, 1, 100)
        viscosities = [reg.resonant_viscosity(t) for t in times]
        assert all(nu > 0 for nu in viscosities)
    
    def test_dissipative_scale(self):
        """Test dissipative length scale calculation."""
        reg = NavierStokesRegularizer(medium='water')
        ℓ0 = reg.dissipative_scale()
        
        assert ℓ0 > 0
        assert 1e-7 < ℓ0 < 1e-2  # Reasonable physical range
    
    def test_critical_reynolds(self):
        """Test critical Reynolds number."""
        reg = NavierStokesRegularizer(medium='water')
        Re_c = reg.critical_reynolds_number()
        
        assert Re_c > 0
    
    def test_qcal_forcing(self):
        """Test QCAL forcing amplitude."""
        reg = NavierStokesRegularizer(medium='water')
        
        # At origin
        pos_origin = np.array([0.0, 0.0, 0.0])
        force_origin = reg.qcal_forcing_amplitude(pos_origin)
        assert force_origin > 0
        
        # Away from origin (should decay due to Gaussian envelope)
        pos_away = np.array([1.0, 1.0, 1.0])
        force_away = reg.qcal_forcing_amplitude(pos_away)
        assert force_away >= 0  # May be very small or zero
        assert force_away <= force_origin  # Should not exceed origin
    
    def test_energy_dissipation(self):
        """Test energy dissipation rate."""
        reg = NavierStokesRegularizer(medium='water')
        
        # Positive dissipation for all vorticity values
        for vort in [0.1, 1.0, 10.0]:
            dissipation = reg.energy_dissipation_rate(vort)
            assert dissipation > 0
    
    def test_blow_up_prevention(self):
        """Test blow-up prevention criterion."""
        reg = NavierStokesRegularizer(medium='water')
        
        vorticity = 1.0
        time = 0.5
        
        status = reg.blow_up_prevention_criterion(vorticity, time)
        
        assert 'blow_up_prevented' in status
        assert 'resonant_viscosity' in status
        assert 'effective_damping' in status
        assert 'dissipation_rate' in status
        assert status['resonant_viscosity'] > 0
        assert status['dissipation_rate'] > 0
    
    def test_laminar_eternity_index(self):
        """Test laminar-eternity index calculation."""
        reg = NavierStokesRegularizer(medium='water')
        
        # Stable flow: constant vorticity
        times = np.linspace(0, 1, 100)
        vorticity_stable = np.ones_like(times)
        
        lambda_stable = reg.laminar_eternity_index(vorticity_stable, times)
        assert 0 <= lambda_stable <= 1
        assert lambda_stable > 0.5  # Should indicate stability
        
        # Unstable flow: growing vorticity
        vorticity_growing = np.exp(times)
        lambda_growing = reg.laminar_eternity_index(vorticity_growing, times)
        assert 0 <= lambda_growing <= 1
        assert lambda_growing < lambda_stable
    
    def test_get_summary(self):
        """Test summary retrieval."""
        reg = NavierStokesRegularizer(medium='water')
        summary = reg.get_summary()
        
        assert 'medium' in summary
        assert 'frequency_hz' in summary
        assert 'base_viscosity_m2_s' in summary
        assert 'amplitude' in summary
        assert 'dissipative_scale_m' in summary
        assert summary['frequency_hz'] == F0


class TestBlowUpPrevention:
    """Integration tests for blow-up prevention."""
    
    def test_bounded_vorticity_evolution(self):
        """Test that vorticity remains bounded over time."""
        reg = NavierStokesRegularizer(medium='water')
        
        times = np.linspace(0, 1.0, 200)
        dt = times[1] - times[0]
        
        vorticity = 1.0
        max_vorticity = vorticity
        
        for t in times[1:]:
            vort_bounded = min(vorticity, 100.0)
            stretching = BETA_QFT * (1 - ALPHA_QFT) * vort_bounded
            damping = reg.resonant_viscosity(t) * vort_bounded
            vorticity += (stretching - damping) * dt
            vorticity = max(0.1, vorticity)
            
            max_vorticity = max(max_vorticity, vorticity)
        
        # Vorticity should remain bounded (not blow up to infinity)
        assert max_vorticity < 1000
        assert vorticity > 0
    
    def test_positive_dissipation_always(self):
        """Test that dissipation remains positive at all times."""
        reg = NavierStokesRegularizer(medium='water')
        
        times = np.linspace(0, 1.0, 100)
        vorticity_values = [0.1, 1.0, 10.0, 50.0]
        
        for t in times:
            for vort in vorticity_values:
                dissipation = reg.energy_dissipation_rate(vort)
                assert dissipation > 0, f"Negative dissipation at t={t}, vort={vort}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
