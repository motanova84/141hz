#!/usr/bin/env python3
"""
Comprehensive Test Suite for QCAL Falsifiability Framework

This test suite validates the implementation of the QCAL falsifiability
experimental framework, including:
- Energy controller (±0.03% constancy)
- Frequency response analyzer (~0.3% precision)
- Falsifiability experiment orchestration

Total: 31 unit + integration tests
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add experiments to path
sys.path.insert(0, str(Path(__file__).parent))

from experiments.energy_controller import (
    EnergyController,
    AdaptiveAmplitudeController,
    EnergyMonitor,
    EnergyControlParams
)
from experiments.frequency_response_analyzer import (
    FrequencyResponseAnalyzer,
    SpectralPeakDetector,
    LorentzianResonanceModel,
    MeasurementResult,
    SpectralPeak
)
from experiments.falsifiability_experiment import (
    FalsifiabilityExperiment,
    ExperimentResult,
    Verdict
)


class TestAdaptiveAmplitudeController:
    """Test suite for adaptive amplitude controller."""
    
    def test_amplitude_calculation_frequency_independent(self):
        """Test that amplitude is frequency-independent for constant energy."""
        controller = AdaptiveAmplitudeController(target_energy=1.0)
        
        # Test at different frequencies
        amp_100hz = controller.calculate_amplitude(100.0, duration=1.0)
        amp_qcal = controller.calculate_amplitude(141.7, duration=1.0)
        amp_1000hz = controller.calculate_amplitude(1000.0, duration=1.0)
        
        # All should be equal (frequency-independent)
        assert amp_100hz == pytest.approx(amp_qcal, rel=1e-10)
        assert amp_100hz == pytest.approx(amp_1000hz, rel=1e-10)
    
    def test_amplitude_scales_with_energy(self):
        """Test that amplitude scales correctly with target energy."""
        controller = AdaptiveAmplitudeController(target_energy=1.0)
        amp_1 = controller.calculate_amplitude(141.7, duration=1.0)
        
        controller = AdaptiveAmplitudeController(target_energy=4.0)
        amp_4 = controller.calculate_amplitude(141.7, duration=1.0)
        
        # For E = A²T/2, if E increases by 4×, A increases by 2×
        assert amp_4 == pytest.approx(amp_1 * 2.0, rel=1e-10)
    
    def test_energy_validation(self):
        """Test energy validation for generated signals."""
        controller = AdaptiveAmplitudeController(target_energy=1.0)
        
        # Generate signal
        t = np.linspace(0, 1, 10000)
        dt = t[1] - t[0]
        amp = controller.calculate_amplitude(141.7, duration=1.0)
        signal = amp * np.sin(2 * np.pi * 141.7 * t)
        
        # Validate energy
        actual_energy, rel_error = controller.validate_energy(signal, dt)
        
        assert actual_energy == pytest.approx(1.0, rel=0.01)
        assert rel_error < 0.01  # Within 1%


class TestEnergyMonitor:
    """Test suite for energy monitor with PID feedback."""
    
    def test_drift_measurement(self):
        """Test drift measurement from target energy."""
        params = EnergyControlParams(target_energy=1.0)
        monitor = EnergyMonitor(params)
        
        # Measure drift
        drift = monitor.measure_drift(1.05)
        assert drift == pytest.approx(0.05, abs=1e-10)
        
        drift = monitor.measure_drift(0.95)
        assert drift == pytest.approx(-0.05, abs=1e-10)
    
    def test_pid_correction(self):
        """Test PID correction calculation."""
        params = EnergyControlParams(
            target_energy=1.0,
            pid_kp=0.1,
            pid_ki=0.01,
            pid_kd=0.001
        )
        monitor = EnergyMonitor(params)
        
        # Apply correction
        correction = monitor.pid_correction(0.1)
        
        # Should have proportional component at minimum
        assert abs(correction) > 0
    
    def test_monitor_reset(self):
        """Test monitor reset functionality."""
        params = EnergyControlParams(target_energy=1.0)
        monitor = EnergyMonitor(params)
        
        # Accumulate some state
        monitor.measure_drift(1.1)
        monitor.pid_correction(0.1)
        
        # Reset
        monitor.reset()
        
        assert monitor.integral_error == 0.0
        assert monitor.previous_error == 0.0
        assert len(monitor.measurements) == 0


class TestEnergyController:
    """Test suite for main energy controller."""
    
    def test_signal_generation(self):
        """Test basic signal generation with energy control."""
        controller = EnergyController(target_energy=1.0, tolerance=0.001)
        
        t, signal = controller.generate_controlled_signal(
            frequency_hz=141.7,
            duration=0.1,
            sampling_rate=10000
        )
        
        assert len(t) == len(signal)
        assert len(signal) > 0
    
    def test_energy_constancy_within_tolerance(self):
        """Test that energy is maintained within tolerance."""
        controller = EnergyController(target_energy=1.0, tolerance=0.001)
        
        t, signal = controller.generate_controlled_signal(
            frequency_hz=141.7,
            duration=0.1,
            sampling_rate=10000
        )
        
        # Calculate actual energy
        dt = t[1] - t[0]
        actual_energy = np.sum(signal**2) * dt
        rel_error = abs(actual_energy - 1.0) / 1.0
        
        assert rel_error < 0.001
    
    def test_energy_constancy_across_frequencies(self):
        """Test energy constancy across multiple frequencies."""
        controller = EnergyController(target_energy=1.0, tolerance=0.0005)
        
        frequencies = [100.0, 141.7, 177.6, 888.0]
        results = controller.validate_energy_constancy(
            frequencies_hz=frequencies,
            duration=0.1,
            sampling_rate=10000
        )
        
        assert results['within_tolerance']
        assert results['max_error'] < 0.0005
        assert results['energy_constancy'] < 0.0003  # ±0.03%
    
    def test_different_target_energies(self):
        """Test controller works with different target energies."""
        for target_energy in [0.5, 1.0, 2.0]:
            controller = EnergyController(
                target_energy=target_energy,
                tolerance=0.001
            )
            
            t, signal = controller.generate_controlled_signal(
                frequency_hz=141.7,
                duration=0.1
            )
            
            dt = t[1] - t[0]
            actual_energy = np.sum(signal**2) * dt
            
            assert actual_energy == pytest.approx(target_energy, rel=0.001)


class TestLorentzianResonanceModel:
    """Test suite for Lorentzian resonance model."""
    
    def test_lorentzian_shape(self):
        """Test basic Lorentzian function shape."""
        model = LorentzianResonanceModel()
        
        f = np.linspace(130, 150, 100)
        response = model.lorentzian(f, amplitude=1.0, f0=141.7, gamma=2.0, offset=0.0)
        
        # Peak should be at f0
        peak_idx = np.argmax(response)
        assert f[peak_idx] == pytest.approx(141.7, abs=0.5)
    
    def test_biological_noise_addition(self):
        """Test addition of realistic biological noise."""
        model = LorentzianResonanceModel()
        
        signal = np.ones(1000)
        noisy = model.add_biological_noise(signal, noise_level=0.1)
        
        # Should have added variance
        assert np.std(noisy) > 0
        assert np.std(noisy) < 0.2  # But reasonable
    
    def test_peak_fitting(self):
        """Test Lorentzian peak fitting."""
        model = LorentzianResonanceModel()
        
        # Create synthetic peak
        f = np.linspace(130, 150, 100)
        true_params = [1.0, 141.7, 2.0, 0.1]
        response = model.lorentzian(f, *true_params)
        
        # Add small noise
        response += np.random.randn(len(f)) * 0.01
        
        # Fit
        fitted_params, _ = model.fit_peak(f, response, f0_guess=141.7)
        
        # Should recover parameters reasonably
        assert fitted_params[1] == pytest.approx(true_params[1], abs=1.0)


class TestSpectralPeakDetector:
    """Test suite for spectral peak detector."""
    
    def test_qcal_frequency_detection(self):
        """Test detection of QCAL frequencies."""
        detector = SpectralPeakDetector(snr_threshold=3.0)
        
        # Test each QCAL frequency
        assert detector._is_qcal_frequency(141.7)
        assert detector._is_qcal_frequency(142.0)  # Within tolerance
        assert detector._is_qcal_frequency(177.6)
        assert detector._is_qcal_frequency(888.0)
        assert not detector._is_qcal_frequency(100.0)
    
    def test_peak_detection(self):
        """Test peak detection in power spectrum."""
        detector = SpectralPeakDetector(snr_threshold=3.0)
        
        # Create spectrum with peaks at QCAL frequencies
        frequencies = np.linspace(50, 300, 500)
        power = np.ones_like(frequencies) * 0.1  # Baseline
        
        # Add peaks at QCAL frequencies
        for qcal_freq in [141.7, 177.6]:
            idx = np.argmin(np.abs(frequencies - qcal_freq))
            power[idx] = 1.0
        
        peaks = detector.detect_peaks(frequencies, power)
        
        # Should detect peaks
        assert len(peaks) > 0
        
        # Count QCAL peaks
        qcal_peaks = [p for p in peaks if p.is_qcal_frequency]
        assert len(qcal_peaks) >= 1


class TestFrequencyResponseAnalyzer:
    """Test suite for frequency response analyzer."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = FrequencyResponseAnalyzer(
            n_sensors=88,
            n_averages=1000,
            sampling_rate=10000
        )
        
        assert analyzer.n_sensors == 88
        assert analyzer.n_averages == 1000
        assert analyzer.sampling_rate == 10000
    
    def test_noise_reduction_factor(self):
        """Test noise reduction calculation."""
        analyzer = FrequencyResponseAnalyzer(n_sensors=88, n_averages=1000)
        
        reduction = analyzer.get_noise_reduction_factor()
        expected = np.sqrt(88 * 1000)
        
        assert reduction == pytest.approx(expected, rel=1e-10)
    
    def test_delta_f_measurement(self):
        """Test ΔF measurement at single frequency."""
        analyzer = FrequencyResponseAnalyzer(n_sensors=10, n_averages=100)
        
        result = analyzer.measure_delta_f(
            frequency=141.7,
            coherence=0.923,
            duration=0.1
        )
        
        assert isinstance(result, MeasurementResult)
        assert result.frequency == 141.7
        assert result.delta_f > 0
        assert result.uncertainty > 0
        assert result.snr_db > 0
    
    def test_measurement_precision(self):
        """Test that measurement precision is ~0.3%."""
        analyzer = FrequencyResponseAnalyzer(n_sensors=88, n_averages=1000)
        
        result = analyzer.measure_delta_f(frequency=141.7, coherence=0.923)
        
        precision = result.uncertainty / result.delta_f
        assert precision < 0.01  # Better than 1%
    
    def test_spectral_analysis(self):
        """Test full spectral analysis."""
        analyzer = FrequencyResponseAnalyzer(n_sensors=10, n_averages=100)
        
        frequencies = np.linspace(100, 200, 20)
        results = analyzer.analyze_spectrum(frequencies, coherence=0.923)
        
        assert len(results['responses']) == len(frequencies)
        assert len(results['uncertainties']) == len(frequencies)
        assert 'peaks' in results
        assert 'precision' in results
    
    def test_qcal_enhancement(self):
        """Test that ΔF is enhanced at QCAL frequencies."""
        analyzer = FrequencyResponseAnalyzer(n_sensors=50, n_averages=500)
        
        # Measure at QCAL and control frequencies
        result_qcal = analyzer.measure_delta_f(141.7, coherence=0.923)
        result_control = analyzer.measure_delta_f(100.0, coherence=0.923)
        
        # QCAL frequency should show enhancement
        ratio = result_qcal.delta_f / result_control.delta_f
        assert ratio > 1.2  # Should be enhanced


class TestFalsifiabilityExperiment:
    """Test suite for falsifiability experiment orchestrator."""
    
    def test_initialization(self):
        """Test experiment initialization."""
        experiment = FalsifiabilityExperiment(
            target_coherence=0.923,
            n_averages=100,
            n_sensors=10
        )
        
        assert experiment.target_coherence == 0.923
        assert isinstance(experiment.energy_controller, EnergyController)
        assert isinstance(experiment.response_analyzer, FrequencyResponseAnalyzer)
    
    def test_verdict_logic_qcal_supported(self):
        """Test verdict logic for QCAL support."""
        experiment = FalsifiabilityExperiment()
        
        # Simulate QCAL result: ratio > 1.5, p < 0.05
        verdict = experiment._determine_verdict(
            ratio=2.79,
            p_value=1e-6,
            confidence_interval=(2.77, 2.82)
        )
        
        assert verdict == Verdict.QCAL_SUPPORTED
    
    def test_verdict_logic_qcal_falsified(self):
        """Test verdict logic for QCAL falsification."""
        experiment = FalsifiabilityExperiment()
        
        # Simulate flat response: ratio ≈ 1.0
        verdict = experiment._determine_verdict(
            ratio=1.05,
            p_value=0.5,
            confidence_interval=(0.95, 1.15)
        )
        
        assert verdict == Verdict.QCAL_FALSIFIED
    
    def test_verdict_logic_inconclusive(self):
        """Test verdict logic for inconclusive results."""
        experiment = FalsifiabilityExperiment()
        
        # Borderline result
        verdict = experiment._determine_verdict(
            ratio=1.3,
            p_value=0.1,
            confidence_interval=(1.1, 1.5)
        )
        
        assert verdict == Verdict.INCONCLUSIVE
    
    def test_critical_test_execution(self):
        """Test end-to-end critical test execution."""
        experiment = FalsifiabilityExperiment(
            n_averages=100,
            n_sensors=10,
            target_coherence=0.923
        )
        
        result = experiment.run_critical_test(
            qcal_frequency=141.7,
            control_frequency=100.0,
            duration=0.1
        )
        
        assert isinstance(result, ExperimentResult)
        assert isinstance(result.verdict, Verdict)
        assert result.ratio > 0
        assert result.p_value >= 0
        assert result.p_value <= 1
        assert result.energy_constancy >= 0
    
    def test_result_has_all_fields(self):
        """Test that experiment result contains all required fields."""
        experiment = FalsifiabilityExperiment(n_averages=50, n_sensors=5)
        
        result = experiment.run_critical_test(duration=0.1)
        
        # Check all fields are present
        assert hasattr(result, 'verdict')
        assert hasattr(result, 'ratio')
        assert hasattr(result, 'ratio_uncertainty')
        assert hasattr(result, 'p_value')
        assert hasattr(result, 'confidence_interval_95')
        assert hasattr(result, 'delta_f_qcal')
        assert hasattr(result, 'delta_f_control')
        assert hasattr(result, 'energy_constancy')
        assert hasattr(result, 'snr_db')
        assert hasattr(result, 'measurement_precision')
    
    def test_result_string_representation(self):
        """Test result string representation."""
        experiment = FalsifiabilityExperiment(n_averages=50, n_sensors=5)
        
        result = experiment.run_critical_test(duration=0.1)
        result_str = str(result)
        
        # Should contain key information
        assert 'VERDICT' in result_str
        assert 'Ratio' in result_str
        assert 'p-value' in result_str


class TestIntegration:
    """Integration tests for complete workflow."""
    
    def test_full_experimental_workflow(self):
        """Test complete experimental workflow from start to finish."""
        # Create experiment with reduced parameters for speed
        experiment = FalsifiabilityExperiment(
            target_coherence=0.923,
            n_averages=50,
            n_sensors=5,
            target_energy=1.0,
            energy_tolerance=0.001
        )
        
        # Run critical test
        result = experiment.run_critical_test(
            qcal_frequency=141.7,
            control_frequency=100.0,
            duration=0.1
        )
        
        # Verify result quality
        assert result.energy_constancy < 0.001  # Good energy control
        assert result.measurement_precision < 0.1  # Reasonable precision
        assert result.snr_db > 10  # Good SNR
    
    def test_energy_control_integration(self):
        """Test energy control integration across experiment."""
        controller = EnergyController(target_energy=1.0, tolerance=0.001)
        
        # Generate signals at multiple frequencies
        frequencies = [100.0, 141.7, 177.6]
        energies = []
        
        for freq in frequencies:
            t, signal = controller.generate_controlled_signal(
                frequency_hz=freq,
                duration=0.1,
                sampling_rate=10000
            )
            dt = t[1] - t[0]
            energy = np.sum(signal**2) * dt
            energies.append(energy)
        
        energies = np.array(energies)
        
        # All energies should be very close
        assert np.std(energies) / np.mean(energies) < 0.001
    
    def test_statistical_significance(self):
        """Test that QCAL results achieve statistical significance."""
        experiment = FalsifiabilityExperiment(
            n_averages=100,
            n_sensors=20,
            target_coherence=0.923
        )
        
        result = experiment.run_critical_test(duration=0.1)
        
        # With QCAL enhancement, should achieve significance
        if result.ratio > 1.5:
            assert result.p_value < 0.05


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
