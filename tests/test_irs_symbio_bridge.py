#!/usr/bin/env python3
"""
Comprehensive test suite for IRS SYMBIO-BRIDGE modules.

Tests:
- physics/irs_symbio_bridge.py (C₇ topological system and Kerr ellipticity)
- physics/irs_interferometer.py (Sagnac interferometer and QND topology)
"""

import sys
import os
from pathlib import Path

# Add repository root to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import pytest
import numpy as np
import math

from physics.irs_symbio_bridge import (
    C7TopologicalSystem,
    KerrEllipticityCalculator,
    create_default_c7_system,
    calculate_expected_ellipticity,
    verify_theoretical_constants,
    PHI_GAUGE_FRACTIONAL,
    Q_FACTOR_DEFAULT,
    N_NODES_C7,
    N_FERMIONS,
    H_SIGMA_CONFORMAL
)

from physics.irs_interferometer import (
    SagnacInterferometer,
    QNDMeasurementTopology,
    LockInHomodyneDetector,
    IRSInstrument,
    create_default_irs_instrument,
    ARM_LENGTH_M,
    FINESSE_DEFAULT
)

from qcal.constants import F0_HZ


# ============================================================================
# TEST SUITE: C7 TOPOLOGICAL SYSTEM
# ============================================================================

class TestC7TopologicalSystem:
    """Test suite for C7TopologicalSystem class."""
    
    def test_initialization_default(self):
        """Test default initialization."""
        c7 = C7TopologicalSystem()
        assert c7.n_nodes == 7
        assert c7.n_fermions == 3
        assert c7.phi_gauge == PHI_GAUGE_FRACTIONAL
        assert c7.h_sigma == H_SIGMA_CONFORMAL
        assert c7.parity_broken is True  # 3 fermions (odd) breaks parity
    
    def test_initialization_invalid_nodes(self):
        """Test that initialization fails with wrong number of nodes."""
        with pytest.raises(ValueError, match="exactamente 7 nodos"):
            C7TopologicalSystem(n_nodes=5)
    
    def test_initialization_invalid_fermions(self):
        """Test that initialization fails with invalid fermion count."""
        with pytest.raises(ValueError, match="debe ser positivo"):
            C7TopologicalSystem(n_fermions=0)
    
    def test_calculate_k7_asymmetry_constant(self):
        """Test K₇ calculation."""
        c7 = C7TopologicalSystem()
        k7 = c7.calculate_k7_asymmetry_constant()
        
        # K₇ = sin(6π/7) × sin(π/28) / sin(π/8) ≈ 0.1269
        expected = 0.1269
        assert abs(k7 - expected) / expected < 0.01  # < 1% error
    
    def test_calculate_geometric_coupling(self):
        """Test geometric coupling factor calculation."""
        c7 = C7TopologicalSystem()
        eta_geo = c7.calculate_geometric_coupling()
        
        # η_geo ≈ 0.1848 (topological factor)
        expected = 0.1848
        assert abs(eta_geo - expected) < 1e-6  # Exact value
    
    def test_get_system_properties(self):
        """Test system properties dictionary."""
        c7 = C7TopologicalSystem()
        props = c7.get_system_properties()
        
        assert 'n_nodes' in props
        assert 'k7_asymmetry' in props
        assert 'geometric_coupling' in props
        assert 'parity_broken' in props
        assert props['f0_hz'] == F0_HZ
        assert props['phi_gauge_pi'] == pytest.approx(1.0/8.0)
    
    def test_theta_0_heptagon(self):
        """Test fundamental heptagonal angle."""
        c7 = C7TopologicalSystem()
        # θ₀ = 2π/7
        expected = 2.0 * math.pi / 7.0
        assert c7.theta_0 == pytest.approx(expected)


# ============================================================================
# TEST SUITE: KERR ELLIPTICITY CALCULATOR
# ============================================================================

class TestKerrEllipticityCalculator:
    """Test suite for KerrEllipticityCalculator class."""
    
    def test_initialization(self):
        """Test initialization."""
        c7 = create_default_c7_system()
        kerr_calc = KerrEllipticityCalculator(c7, Q_FACTOR_DEFAULT)
        assert kerr_calc.q_factor == Q_FACTOR_DEFAULT
    
    def test_initialization_invalid_q(self):
        """Test that initialization fails with invalid Q."""
        c7 = create_default_c7_system()
        with pytest.raises(ValueError, match="positivo"):
            KerrEllipticityCalculator(c7, q_factor=-1)
    
    def test_calculate_kerr_ellipticity_max(self):
        """Test maximum Kerr ellipticity calculation."""
        c7 = create_default_c7_system()
        kerr_calc = KerrEllipticityCalculator(c7, Q_FACTOR_DEFAULT)
        result = kerr_calc.calculate_kerr_ellipticity_max()
        
        # Expected: ≈ 23.5° for Q = 1000
        expected_deg = 23.5
        epsilon_k_deg = result['epsilon_k_max_deg']
        
        assert abs(epsilon_k_deg - expected_deg) / expected_deg < 0.05  # < 5% error
        assert result['q_factor'] == Q_FACTOR_DEFAULT
        assert 'epsilon_k_max_rad' in result
        assert 'epsilon_k_max_mrad' in result
    
    def test_spectral_sweep(self):
        """Test spectral sweep around f₀."""
        c7 = create_default_c7_system()
        kerr_calc = KerrEllipticityCalculator(c7, Q_FACTOR_DEFAULT)
        
        frequencies, ellipticities = kerr_calc.spectral_sweep(n_points=100)
        
        assert len(frequencies) == 100
        assert len(ellipticities) == 100
        
        # Peak should be at f₀
        max_idx = np.argmax(ellipticities)
        peak_freq = frequencies[max_idx]
        assert abs(peak_freq - F0_HZ) < 1e-4
    
    def test_check_falsification_criterion_confirmed(self):
        """Test falsification criterion with positive detection."""
        c7 = create_default_c7_system()
        kerr_calc = KerrEllipticityCalculator(c7, Q_FACTOR_DEFAULT)
        
        # Get expected value
        result = kerr_calc.calculate_kerr_ellipticity_max()
        measured = result['epsilon_k_max_rad'] * 0.9  # 90% of maximum
        
        falsification = kerr_calc.check_falsification_criterion(
            measured_ellipticity=measured,
            frequency=F0_HZ,
            sensitivity_rad=1e-4
        )
        
        assert falsification['falsification_status'] == "MODELO CONFIRMADO"
        assert falsification['detection_confirmed'] is True
        assert falsification['in_spectral_window'] is True
    
    def test_check_falsification_criterion_refuted(self):
        """Test falsification criterion with no detection."""
        c7 = create_default_c7_system()
        kerr_calc = KerrEllipticityCalculator(c7, Q_FACTOR_DEFAULT)
        
        # Measure too low ellipticity
        measured = 1e-5  # 0.01 mrad (way below expected)
        
        falsification = kerr_calc.check_falsification_criterion(
            measured_ellipticity=measured,
            frequency=F0_HZ,
            sensitivity_rad=1e-4
        )
        
        assert falsification['falsification_status'] == "MODELO REFUTADO"
        assert falsification['detection_confirmed'] is False


# ============================================================================
# TEST SUITE: SAGNAC INTERFEROMETER
# ============================================================================

class TestSagnacInterferometer:
    """Test suite for SagnacInterferometer class."""
    
    def test_initialization(self):
        """Test initialization."""
        sagnac = SagnacInterferometer()
        assert sagnac.arm_length == ARM_LENGTH_M
        assert sagnac.finesse == FINESSE_DEFAULT
    
    def test_initialization_invalid_params(self):
        """Test that initialization fails with invalid parameters."""
        with pytest.raises(ValueError):
            SagnacInterferometer(arm_length=-1)
        with pytest.raises(ValueError):
            SagnacInterferometer(laser_wavelength=-1)
        with pytest.raises(ValueError):
            SagnacInterferometer(laser_power=-1)
        with pytest.raises(ValueError):
            SagnacInterferometer(finesse=-1)
    
    def test_derived_properties(self):
        """Test derived properties calculation."""
        sagnac = SagnacInterferometer()
        
        # FSR = c / (2L)
        expected_fsr = 299792458.0 / (2.0 * ARM_LENGTH_M)
        assert sagnac.fsr == pytest.approx(expected_fsr, rel=1e-6)
        
        # Linewidth = FSR / Finesse
        expected_linewidth = expected_fsr / FINESSE_DEFAULT
        assert sagnac.linewidth == pytest.approx(expected_linewidth, rel=1e-6)
    
    def test_calculate_photon_number(self):
        """Test photon number calculation."""
        sagnac = SagnacInterferometer()
        n_photons = sagnac.calculate_photon_number()
        
        # Should be a large number for 1 mW laser
        assert n_photons > 1e10
        assert isinstance(n_photons, float)
    
    def test_calculate_phase_sensitivity(self):
        """Test phase sensitivity calculation."""
        sagnac = SagnacInterferometer()
        delta_phi = sagnac.calculate_phase_sensitivity()
        
        # Shot noise limited: δφ ≈ 1/√N
        # Should be very small (sub-µrad)
        assert delta_phi < 1e-6  # < µrad
        assert delta_phi > 0
    
    def test_calculate_sagnac_phase_shift(self):
        """Test Sagnac phase shift calculation."""
        sagnac = SagnacInterferometer()
        
        # Earth rotation: Ω ≈ 7.27 × 10⁻⁵ rad/s
        omega_earth = 7.27e-5
        phase_shift = sagnac.calculate_sagnac_phase_shift(omega_earth)
        
        # Should be detectable (for a 4km × 4km loop, this is large)
        assert abs(phase_shift) > 0
        # Phase shift scales with area, so for 16 km² it's large
        assert abs(phase_shift) > 1  # > 1 rad for large interferometer
    
    def test_get_interferometer_properties(self):
        """Test properties dictionary."""
        sagnac = SagnacInterferometer()
        props = sagnac.get_interferometer_properties()
        
        assert 'arm_length_km' in props
        assert 'laser_wavelength_nm' in props
        assert 'fsr_hz' in props
        assert 'n_photons' in props
        assert 'phase_sensitivity_rad' in props


# ============================================================================
# TEST SUITE: QND MEASUREMENT TOPOLOGY
# ============================================================================

class TestQNDMeasurementTopology:
    """Test suite for QNDMeasurementTopology class."""
    
    def test_initialization(self):
        """Test initialization."""
        qnd = QNDMeasurementTopology()
        assert qnd.coupling_strength < 0.1  # Weak coupling
        assert qnd.decoherence_time > 0
    
    def test_initialization_invalid_coupling(self):
        """Test that initialization fails with invalid coupling."""
        with pytest.raises(ValueError):
            QNDMeasurementTopology(coupling_strength=0.5)  # Too strong
        with pytest.raises(ValueError):
            QNDMeasurementTopology(coupling_strength=-1)
    
    def test_calculate_measurement_backaction(self):
        """Test back-action calculation."""
        qnd = QNDMeasurementTopology(coupling_strength=1e-6)
        backaction = qnd.calculate_measurement_backaction(measurement_time=1.0)
        
        # For weak coupling, back-action should be tiny
        assert backaction < 1e-10
        assert backaction >= 0
    
    def test_calculate_qnd_fidelity(self):
        """Test QND fidelity calculation."""
        qnd = QNDMeasurementTopology(coupling_strength=1e-6)
        fidelity = qnd.calculate_qnd_fidelity(measurement_time=1.0)
        
        # Fidelity should be very close to 1
        assert fidelity > 0.99
        assert fidelity <= 1.0
    
    def test_is_measurement_qnd(self):
        """Test QND criterion check."""
        qnd = QNDMeasurementTopology(coupling_strength=1e-6)
        
        # Should be QND for short measurements
        assert qnd.is_measurement_qnd(measurement_time=1.0) is True
        
        # Might not be QND for very long measurements
        # (depends on decoherence time)
    
    def test_get_qnd_properties(self):
        """Test properties dictionary."""
        qnd = QNDMeasurementTopology()
        props = qnd.get_qnd_properties(measurement_time=1.0)
        
        assert 'coupling_strength' in props
        assert 'fidelity' in props
        assert 'is_qnd' in props
        assert 'qnd_quality' in props


# ============================================================================
# TEST SUITE: LOCK-IN HOMODYNE DETECTOR
# ============================================================================

class TestLockInHomodyneDetector:
    """Test suite for LockInHomodyneDetector class."""
    
    def test_initialization(self):
        """Test initialization."""
        lockin = LockInHomodyneDetector()
        assert lockin.reference_frequency == F0_HZ
        assert lockin.integration_time > 0
        assert lockin.bandwidth > 0
    
    def test_initialization_invalid_params(self):
        """Test that initialization fails with invalid parameters."""
        with pytest.raises(ValueError):
            LockInHomodyneDetector(reference_frequency=-1)
        with pytest.raises(ValueError):
            LockInHomodyneDetector(integration_time=-1)
        with pytest.raises(ValueError):
            LockInHomodyneDetector(bandwidth=-1)
    
    def test_derived_properties(self):
        """Test derived properties."""
        lockin = LockInHomodyneDetector(integration_time=10.0, bandwidth=0.01)
        
        # SNR improvement ≈ √(T × BW)
        expected_improvement = np.sqrt(10.0 * 0.01)
        assert lockin.snr_improvement == pytest.approx(expected_improvement)
        
        # Frequency resolution = 1/T
        expected_resolution = 1.0 / 10.0
        assert lockin.frequency_resolution == pytest.approx(expected_resolution)
    
    def test_calculate_signal_to_noise_ratio(self):
        """Test SNR calculation."""
        lockin = LockInHomodyneDetector()
        
        signal_amplitude = 1.0
        noise_spectral_density = 0.1
        
        snr = lockin.calculate_signal_to_noise_ratio(signal_amplitude, noise_spectral_density)
        
        assert snr > 0
        assert isinstance(snr, float)
    
    def test_demodulate_signal(self):
        """Test signal demodulation."""
        lockin = LockInHomodyneDetector(reference_frequency=F0_HZ, integration_time=1.0)
        
        # Generate test signal
        sample_rate = 1000.0
        duration = 1.0
        n_samples = int(duration * sample_rate)
        time = np.linspace(0, duration, n_samples)
        
        # Signal at f₀ with known amplitude and phase
        amplitude = 1.0
        phase = np.pi / 4
        signal = amplitude * np.sin(2.0 * math.pi * F0_HZ * time + phase)
        
        # Demodulate
        i_comp, q_comp = lockin.demodulate_signal(time, signal, phase_offset=0.0)
        
        # Check that components are reasonable
        assert isinstance(i_comp, float)
        assert isinstance(q_comp, float)
        
        # Amplitude should be recovered (within numerical error)
        recovered_amplitude = np.sqrt(i_comp**2 + q_comp**2)
        assert abs(recovered_amplitude - amplitude) < 0.1
    
    def test_calculate_phase_and_amplitude(self):
        """Test phase and amplitude calculation from I/Q."""
        lockin = LockInHomodyneDetector()
        
        i_comp = 1.0
        q_comp = 1.0
        
        amplitude, phase = lockin.calculate_phase_and_amplitude(i_comp, q_comp)
        
        expected_amplitude = np.sqrt(2.0)
        expected_phase = np.pi / 4
        
        assert amplitude == pytest.approx(expected_amplitude)
        assert phase == pytest.approx(expected_phase)
    
    def test_get_detector_properties(self):
        """Test properties dictionary."""
        lockin = LockInHomodyneDetector()
        props = lockin.get_detector_properties()
        
        assert 'reference_frequency_hz' in props
        assert 'integration_time_s' in props
        assert 'snr_improvement_factor' in props
        assert 'n_cycles' in props


# ============================================================================
# TEST SUITE: COMPLETE IRS INSTRUMENT
# ============================================================================

class TestIRSInstrument:
    """Test suite for IRSInstrument class."""
    
    def test_initialization(self):
        """Test initialization."""
        irs = IRSInstrument()
        assert irs.sagnac is not None
        assert irs.qnd is not None
        assert irs.lockin is not None
        assert irs.c7_system is not None
        assert irs.kerr_calculator is not None
    
    def test_calculate_expected_signal(self):
        """Test expected signal calculation."""
        irs = IRSInstrument()
        expected = irs.calculate_expected_signal()
        
        assert 'expected_ellipticity_rad' in expected
        assert 'snr_improved' in expected
        assert 'qnd_fidelity' in expected
        assert 'detection_feasible' in expected
        
        # Detection should be feasible
        assert bool(expected['detection_feasible']) is True
        assert bool(expected['qnd_maintained']) is True
        
        # SNR should be very high
        assert expected['snr_improved'] > 1000
    
    def test_simulate_measurement(self):
        """Test measurement simulation."""
        irs = IRSInstrument()
        measurement_data = irs.simulate_measurement(duration=10.0, noise_level=1e-8)
        
        assert 'time' in measurement_data
        assert 'signal_pure' in measurement_data
        assert 'signal_measured' in measurement_data
        assert 'noise' in measurement_data
        
        # Check that arrays have correct length
        n_samples = len(measurement_data['time'])
        assert len(measurement_data['signal_pure']) == n_samples
        assert len(measurement_data['signal_measured']) == n_samples
    
    def test_get_instrument_summary(self):
        """Test instrument summary."""
        irs = IRSInstrument()
        summary = irs.get_instrument_summary()
        
        assert 'interferometer' in summary
        assert 'qnd_topology' in summary
        assert 'lockin_detector' in summary
        assert 'c7_system' in summary
        assert 'expected_signal' in summary
    
    def test_create_default_instrument(self):
        """Test default instrument creation."""
        irs = create_default_irs_instrument()
        assert isinstance(irs, IRSInstrument)


# ============================================================================
# TEST SUITE: UTILITY FUNCTIONS
# ============================================================================

class TestUtilityFunctions:
    """Test suite for utility functions."""
    
    def test_create_default_c7_system(self):
        """Test default C7 system creation."""
        c7 = create_default_c7_system()
        assert isinstance(c7, C7TopologicalSystem)
        assert c7.n_nodes == 7
    
    def test_calculate_expected_ellipticity(self):
        """Test expected ellipticity calculation."""
        result = calculate_expected_ellipticity(q_factor=1000.0)
        
        assert 'epsilon_k_max_deg' in result
        assert 'epsilon_k_max_rad' in result
        assert 'epsilon_k_max_mrad' in result
        
        # Should be around 23.5°
        assert 20.0 < result['epsilon_k_max_deg'] < 30.0
    
    def test_verify_theoretical_constants(self):
        """Test theoretical constants verification."""
        verification = verify_theoretical_constants()
        
        assert 'k7_calculated' in verification
        assert 'k7_verified' in verification
        assert 'eta_geo_calculated' in verification
        assert 'eta_geo_verified' in verification
        
        # Both should be verified (within tolerance)
        assert verification['k7_verified'] is True
        assert verification['eta_geo_verified'] is True


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
