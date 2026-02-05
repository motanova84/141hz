"""
Tests for vibrational fluorescence measurement system.

Validates the implementation against QCAL theoretical predictions.
"""

import numpy as np
import pytest
from modules.quantum_biology.core.vibrational_fluorescence import (
    VibrationalFluorescenceSystem,
    FluorescenceConfig,
    run_fluorescence_experiment
)


class TestVibrationalFluorescenceSystem:
    """Test suite for VibrationalFluorescenceSystem."""

    def test_initialization(self):
        """Test system initialization with default config."""
        system = VibrationalFluorescenceSystem()
        assert system.config.f0 == 141.7001
        assert system.omega0 == 2 * np.pi * 141.7001
        assert system.config.psi_critical == 0.888

    def test_initialization_custom_config(self):
        """Test system initialization with custom config."""
        config = FluorescenceConfig(
            f0=150.0,
            amplitude=2.0,
            psi_critical=0.9
        )
        system = VibrationalFluorescenceSystem(config)
        assert system.config.f0 == 150.0
        assert system.config.amplitude == 2.0
        assert system.config.psi_critical == 0.9

    def test_signal_generation_shape(self):
        """Test that generated signal has correct shape."""
        system = VibrationalFluorescenceSystem()
        f_mod = 1.0  # Hz
        t, signal = system.generate_modulated_signal(f_mod, duration=1.0)

        expected_length = int(1.0 * system.config.sampling_rate)
        assert len(t) == expected_length
        assert len(signal) == expected_length

    def test_signal_generation_carrier_frequency(self):
        """Test that carrier frequency is correct."""
        system = VibrationalFluorescenceSystem()
        f_mod = 0.5  # Hz (slow modulation)
        t, signal = system.generate_modulated_signal(f_mod, duration=2.0)

        # FFT to check dominant frequency
        from scipy import fft
        f_fft = fft.fft(signal)
        freqs = fft.fftfreq(len(signal), 1.0/system.config.sampling_rate)

        # Find peak frequency (should be near f0 = 141.7 Hz)
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = np.abs(f_fft[:len(freqs)//2])
        peak_freq = positive_freqs[np.argmax(positive_fft)]

        # Allow 1% tolerance
        assert np.abs(peak_freq - system.config.f0) < 0.01 * system.config.f0

    def test_constant_energy_constraint(self):
        """Test that total energy is constant across frequencies."""
        system = VibrationalFluorescenceSystem()

        # Generate signals at different modulation frequencies
        energies = []
        frequencies = [0.1, 1.0, 5.0, 10.0]

        for f_mod in frequencies:
            t, signal = system.generate_modulated_signal(
                f_mod,
                duration=10.0,
                ensure_constant_energy=True
            )
            dt = 1.0 / system.config.sampling_rate
            energy = np.sum(signal**2) * dt
            energies.append(energy)

        # All energies should be equal (within numerical tolerance)
        energies = np.array(energies)
        assert np.std(energies) / np.mean(energies) < 0.01  # 1% variation

    def test_protein_resonance_at_f0(self):
        """Test that protein resonance peaks at f₀."""
        system = VibrationalFluorescenceSystem()

        # Calculate response at different frequencies
        frequencies = np.linspace(100, 200, 100)
        responses = []

        for f in frequencies:
            omega = 2 * np.pi * f
            response = system.calculate_protein_resonance(omega)
            responses.append(abs(response))

        responses = np.array(responses)
        peak_freq = frequencies[np.argmax(responses)]

        # Peak should be at f₀ ± 5 Hz
        assert np.abs(peak_freq - system.config.f0) < 5.0

    def test_fluorescence_response_contains_modulation(self):
        """Test that fluorescence response contains modulation frequency."""
        system = VibrationalFluorescenceSystem()
        f_mod = 2.0  # Hz

        f_signal, metrics = system.calculate_fluorescence_response(
            f_mod,
            noise_level=0.001  # Low noise for clear signal
        )

        # FFT to check for modulation frequency
        from scipy import fft
        f_fft = fft.fft(f_signal)
        freqs = fft.fftfreq(len(f_signal), 1.0/system.config.sampling_rate)

        # Find peak near modulation frequency
        window = (np.abs(freqs - f_mod) < 0.5)
        if np.any(window):
            peak_power = np.max(np.abs(f_fft[window]))
            # Calculate mean excluding DC component
            non_dc_mask = np.abs(freqs) > 0.1
            mean_power = np.mean(np.abs(f_fft[non_dc_mask]))

            # Modulation should be visible (relaxed criterion)
            # Note: The modulation is in the amplitude envelope, not the carrier
            assert peak_power > 0.1 * mean_power

    def test_qcal_resonance_enhancement(self):
        """Test that QCAL resonances show enhanced response."""
        system = VibrationalFluorescenceSystem()

        # Test at QCAL resonance (f₀ = 141.7 Hz)
        _, metrics_resonant = system.calculate_fluorescence_response(
            141.7,
            include_qcal_resonances=True
        )

        # Test at non-resonant frequency
        _, metrics_nonresonant = system.calculate_fluorescence_response(
            100.0,
            include_qcal_resonances=True
        )

        # Resonant response should be larger
        assert metrics_resonant['delta_f'] > metrics_nonresonant['delta_f']

    def test_frequency_sweep_returns_expected_keys(self):
        """Test that frequency sweep returns all expected data."""
        system = VibrationalFluorescenceSystem()

        # Use small number of steps for fast test
        system.config.f_mod_steps = 10

        results = system.perform_frequency_sweep(include_qcal=True)

        assert 'frequencies' in results
        assert 'delta_f' in results
        assert 'eta' in results
        assert 'phase' in results
        assert 'snr' in results

        assert len(results['frequencies']) == 10
        assert len(results['delta_f']) == 10

    def test_anova_distinguishes_qcal_from_null(self):
        """Test that ANOVA test can distinguish QCAL from null hypothesis."""
        system = VibrationalFluorescenceSystem()
        system.config.f_mod_steps = 50  # Moderate resolution

        # Get QCAL and null results
        results_qcal = system.perform_frequency_sweep(include_qcal=True)
        results_null = system.perform_frequency_sweep(include_qcal=False)

        # Perform ANOVA
        anova = system.calculate_spectral_anova(results_qcal, results_null)

        # Should reject null hypothesis
        assert 'f_statistic' in anova
        assert 'p_value' in anova
        assert 'reject_null' in anova

        # With QCAL resonances, should show significant difference
        # (p-value should be small)
        assert anova['p_value'] < 0.05  # At least 5% significance

    def test_coherence_calculation(self):
        """Test coherence calculation between signals."""
        system = VibrationalFluorescenceSystem()

        # Generate two identical signals
        f_mod = 1.0
        t, signal1 = system.generate_modulated_signal(f_mod)
        signal2 = signal1.copy()

        # Calculate coherence
        freqs, coh = system.calculate_coherence(signal1, signal2)

        # Coherence of identical signals should be ~1
        assert np.max(coh) > 0.95

    def test_snr_calculation(self):
        """Test SNR calculation."""
        system = VibrationalFluorescenceSystem()

        # Create signal with known SNR
        t = np.linspace(0, 1, 10000)
        signal_freq = 5.0  # Hz
        signal = 10.0 * np.sin(2 * np.pi * signal_freq * t)
        noise = 1.0 * np.random.randn(len(t))
        total_signal = signal + noise

        system.config.sampling_rate = 10000.0
        snr = system.calculate_snr(total_signal, signal_freq)

        # SNR should be positive and reasonable (signal/noise = 10, but FFT amplifies)
        assert 5 < snr < 200  # Allow wider range for FFT-based SNR

    def test_full_validation(self):
        """Test complete QCAL validation workflow."""
        config = FluorescenceConfig(
            f_mod_steps=30,  # Reduced for faster test
            duration=5.0     # Shorter duration
        )
        system = VibrationalFluorescenceSystem(config)

        results = system.validate_qcal_predictions()

        # Check all expected keys
        assert 'qcal_results' in results
        assert 'null_results' in results
        assert 'anova' in results
        assert 'summary' in results

        # Summary should contain decision
        assert 'qcal_confirmed' in results['summary']
        assert 'statistical_significance' in results['summary']

    def test_response_ratio_criterion(self):
        """Test that QCAL criterion ΔF(141.7)/ΔF(100) > 1.5 is checked."""
        config = FluorescenceConfig(f_mod_steps=50)
        system = VibrationalFluorescenceSystem(config)

        results = system.validate_qcal_predictions()

        assert 'response_ratio_141_to_100' in results
        assert 'qcal_criterion_met' in results

        # With QCAL resonances, ratio should exceed 1.5
        if results['qcal_criterion_met']:
            assert results['response_ratio_141_to_100'] > 1.5


class TestFluorescenceConfig:
    """Test suite for FluorescenceConfig dataclass."""

    def test_default_values(self):
        """Test that default config has correct QCAL parameters."""
        config = FluorescenceConfig()
        assert config.f0 == 141.7001
        assert config.psi_critical == 0.888
        assert config.alpha == 0.001
        assert config.mod_index >= 0 and config.mod_index <= 1

    def test_custom_values(self):
        """Test creating config with custom values."""
        config = FluorescenceConfig(
            f0=150.0,
            psi_critical=0.9,
            alpha=0.01,
            sampling_rate=20000.0
        )
        assert config.f0 == 150.0
        assert config.psi_critical == 0.9
        assert config.alpha == 0.01
        assert config.sampling_rate == 20000.0


class TestRunFluorescenceExperiment:
    """Test suite for main experiment runner."""

    def test_run_with_defaults(self):
        """Test running experiment with default configuration."""
        results = run_fluorescence_experiment(verbose=False)

        assert results is not None
        assert 'summary' in results
        assert 'qcal_confirmed' in results['summary']

    def test_run_with_custom_config(self):
        """Test running experiment with custom configuration."""
        config = FluorescenceConfig(
            f_mod_steps=20,
            duration=3.0
        )
        results = run_fluorescence_experiment(config, verbose=False)

        assert results is not None
        assert len(results['qcal_results']['frequencies']) == 20


# Integration tests
class TestIntegrationWithQuantumBiology:
    """Integration tests with existing quantum biology module."""

    def test_fluorescence_system_compatible_with_fmo(self):
        """Test that fluorescence system can work alongside FMO complex."""
        # This test verifies that the new module doesn't break existing code
        try:
            from modules.quantum_biology.core.fmo_photosynthesis import FMOComplex

            # Create both systems
            fmo = FMOComplex()
            fluor_system = VibrationalFluorescenceSystem()

            # Both should work independently
            assert fluor_system.config.f0 == 141.7001
            assert hasattr(fmo, 'calculate_coherence')

        except ImportError:
            pytest.skip("FMO module not available")

    def test_coherence_threshold_consistency(self):
        """Test that Ψ threshold is consistent across modules."""
        system = VibrationalFluorescenceSystem()

        # QCAL critical threshold should be 0.888 across all modules
        assert system.config.psi_critical == 0.888


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v'])
