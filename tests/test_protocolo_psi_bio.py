"""
Tests for Nodo Ψ Bio Protocol - Microtubule Measurement System
===============================================================

Tests the complete bio-pulse generation, spectrogram analysis, and
coherence validation for the 141.7001 Hz microtubule protocol.

AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
DATE: February 2026
"""

import pytest
import numpy as np
import os
import tempfile
from scipy.io import wavfile

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qcal.protocolo_psi_bio import (
    generate_bio_pulse,
    save_bio_pulse_wav,
    generate_spectrogram,
    validate_spectral_peak,
    compute_coherence_metrics,
    run_complete_protocol,
    run_phase_recovery_protocol,
    BioPulseSignal,
    CoherenceMetrics,
    PhaseEvaporationEvent,
    PhaseRecoveryResult,
    PhaseRecoveryProtocol,
    F0_HZ,
    SAMPLE_RATE_HZ,
    DURATION_SEC
)


class TestBioPulseGeneration:
    """Test bio-pulse signal generation."""
    
    def test_generate_bio_pulse_basic(self):
        """Test basic pulse generation with default parameters."""
        pulse = generate_bio_pulse()
        
        assert isinstance(pulse, BioPulseSignal)
        assert pulse.frequency == F0_HZ
        assert pulse.sample_rate == SAMPLE_RATE_HZ
        assert pulse.duration == DURATION_SEC
        assert len(pulse.signal) == SAMPLE_RATE_HZ * DURATION_SEC
    
    def test_pulse_frequency_accuracy(self):
        """Test that generated pulse has correct frequency."""
        pulse = generate_bio_pulse(frequency=141.7001, duration=10)
        
        # Verify via FFT
        fft = np.fft.rfft(pulse.signal)
        freqs = np.fft.rfftfreq(len(pulse.signal), 1/pulse.sample_rate)
        peak_idx = np.argmax(np.abs(fft))
        peak_freq = freqs[peak_idx]
        
        # Should be within 1 Hz (limited by FFT resolution)
        assert abs(peak_freq - 141.7001) < 1.0
    
    def test_pulse_amplitude_headroom(self):
        """Test that pulse has safe headroom to prevent clipping."""
        pulse = generate_bio_pulse()
        
        # Check RMS and peak levels
        assert pulse.peak_db < 0  # Should be below 0 dBFS
        assert pulse.peak_db >= -10  # Should not be too quiet
        assert pulse.max_amplitude <= 1.0  # Should not clip
    
    def test_pulse_fade_in_out(self):
        """Test that fade in/out is applied correctly."""
        pulse = generate_bio_pulse(fade_duration=1.0, duration=10, headroom_db=0)  # No headroom for this test
        
        # Check that signal starts and ends near zero
        fade_samples = int(1.0 * pulse.sample_rate)
        
        # First sample should be very quiet (fade in)
        assert abs(pulse.signal[0]) < 0.01
        
        # Last sample should be very quiet (fade out)
        assert abs(pulse.signal[-1]) < 0.01
        
        # Middle section should have full amplitude (check max in middle half)
        mid_start = len(pulse.signal) // 3
        mid_end = 2 * len(pulse.signal) // 3
        max_in_middle = np.max(np.abs(pulse.signal[mid_start:mid_end]))
        assert max_in_middle > 0.9  # Should be close to 1.0 without headroom
    
    def test_pulse_custom_parameters(self):
        """Test pulse generation with custom parameters."""
        custom_freq = 150.0
        custom_duration = 5.0
        custom_sr = 48000
        
        pulse = generate_bio_pulse(
            frequency=custom_freq,
            duration=custom_duration,
            sample_rate=custom_sr
        )
        
        assert pulse.frequency == custom_freq
        assert pulse.duration == custom_duration
        assert pulse.sample_rate == custom_sr
        assert len(pulse.signal) == custom_sr * custom_duration


class TestWAVFileGeneration:
    """Test WAV file saving and loading."""
    
    def test_save_and_load_wav(self):
        """Test that WAV file is saved correctly and can be loaded."""
        pulse = generate_bio_pulse(duration=1.0)  # Short pulse for speed
        
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = os.path.join(tmpdir, "test_pulse.wav")
            save_bio_pulse_wav(pulse, wav_path)
            
            # Check file exists
            assert os.path.exists(wav_path)
            
            # Load and verify
            sample_rate, data = wavfile.read(wav_path)
            assert sample_rate == pulse.sample_rate
            assert len(data) == len(pulse.signal)
            
            # Verify it's 16-bit PCM
            assert data.dtype == np.int16
    
    def test_wav_file_compatibility(self):
        """Test WAV file format compatibility."""
        pulse = generate_bio_pulse(duration=0.5)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = os.path.join(tmpdir, "test_pulse.wav")
            save_bio_pulse_wav(pulse, wav_path)
            
            # Load and check properties
            sample_rate, data = wavfile.read(wav_path)
            
            # Should be mono (1D array)
            assert data.ndim == 1
            
            # Should be at correct sample rate
            assert sample_rate == SAMPLE_RATE_HZ


class TestSpectrogramGeneration:
    """Test spectrogram generation and validation."""
    
    def test_generate_spectrogram_basic(self):
        """Test basic spectrogram generation."""
        pulse = generate_bio_pulse(duration=5.0)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_path = os.path.join(tmpdir, "test_spec.png")
            frequencies, times, Sxx = generate_spectrogram(pulse, spec_path)
            
            # Check outputs
            assert len(frequencies) > 0
            assert len(times) > 0
            assert Sxx.shape[0] == len(frequencies)
            assert Sxx.shape[1] == len(times)
            
            # Check file was created
            assert os.path.exists(spec_path)
    
    def test_spectral_peak_detection(self):
        """Test that f₀ peak is correctly detected."""
        pulse = generate_bio_pulse(duration=5.0)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_path = os.path.join(tmpdir, "test_spec.png")
            frequencies, times, Sxx = generate_spectrogram(pulse, spec_path)
            
            # Validate peak
            is_valid, peak_freq, stability = validate_spectral_peak(frequencies, Sxx)
            
            # Should be valid
            assert is_valid
            
            # Peak should be close to f₀ (within FFT resolution)
            assert abs(peak_freq - F0_HZ) < 5.0
            
            # Stability should be high
            assert stability > 0.9
    
    def test_spectral_peak_stability(self):
        """Test temporal stability of spectral peak."""
        pulse = generate_bio_pulse(duration=10.0)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            spec_path = os.path.join(tmpdir, "test_spec.png")
            frequencies, times, Sxx = generate_spectrogram(pulse, spec_path)
            
            # Get peak frequency in each time slice
            peak_freqs = []
            for i in range(Sxx.shape[1]):
                freq_mask = (frequencies > F0_HZ - 20) & (frequencies < F0_HZ + 20)
                local_freqs = frequencies[freq_mask]
                local_power = Sxx[freq_mask, i]
                peak_idx = np.argmax(local_power)
                peak_freqs.append(local_freqs[peak_idx])
            
            # Standard deviation should be very low (stable peak)
            assert np.std(peak_freqs) < 2.0


class TestCoherenceMetrics:
    """Test coherence calculation and validation."""
    
    def test_coherence_metrics_structure(self):
        """Test coherence metrics data structure."""
        metrics = compute_coherence_metrics()
        
        assert isinstance(metrics, CoherenceMetrics)
        assert 0 <= metrics.psi_coherence <= 1
        assert 0 <= metrics.eeg_sync_quality <= 1
        assert 0 <= metrics.hrv_coherence <= 1
        assert 0 <= metrics.stability_index <= 1
    
    def test_coherence_stability_check(self):
        """Test Orch-OR stability determination."""
        # High coherence - should be stable
        metrics = CoherenceMetrics(
            psi_coherence=0.999,
            eeg_sync_quality=0.998,
            hrv_coherence=0.997,
            stability_index=0.996
        )
        assert metrics.is_stable
        
        # Low coherence - should be unstable
        metrics_low = CoherenceMetrics(
            psi_coherence=0.85,
            eeg_sync_quality=0.80,
            hrv_coherence=0.75,
            stability_index=0.80
        )
        assert not metrics_low.is_stable
    
    def test_coherence_with_actual_signals(self):
        """Test coherence calculation with provided signals."""
        # Generate test signals
        pulse = generate_bio_pulse(duration=5.0)
        
        # Simulate EEG with some correlation to pulse
        noise = np.random.randn(len(pulse.signal)) * 0.1
        eeg_signal = pulse.signal * 0.5 + noise
        
        metrics = compute_coherence_metrics(
            eeg_signal=eeg_signal,
            pulse_signal=pulse.signal
        )
        
        # Should have reasonable coherence
        assert metrics.psi_coherence > 0.3
        assert metrics.psi_coherence < 1.0


class TestCompleteProtocol:
    """Test complete protocol execution."""
    
    def test_run_complete_protocol(self):
        """Test running the complete protocol."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = run_complete_protocol(
                output_dir=tmpdir,
                generate_artifacts=True
            )
            
            # Check all expected keys
            assert "pulse" in results
            assert "wav_file" in results
            assert "spectrogram_file" in results
            assert "spectral_validation" in results
            assert "coherence" in results
            
            # Check artifacts were created
            assert os.path.exists(results["wav_file"])
            assert os.path.exists(results["spectrogram_file"])
            
            # Check pulse properties
            pulse = results["pulse"]
            assert pulse.frequency == F0_HZ
            assert pulse.duration == DURATION_SEC
            
            # Check spectral validation
            validation = results["spectral_validation"]
            assert validation["is_valid"]
            assert validation["stability"] > 0.9
            
            # Check coherence
            coherence = results["coherence"]
            assert coherence.is_stable
    
    def test_protocol_without_artifacts(self):
        """Test protocol can run without generating artifacts."""
        results = run_complete_protocol(generate_artifacts=False)
        
        # Should have pulse and coherence but no files
        assert "pulse" in results
        assert "coherence" in results
        assert "wav_file" not in results
        assert "spectrogram_file" not in results


class TestProtocolParameters:
    """Test protocol adheres to specified parameters."""
    
    def test_frequency_is_f0(self):
        """Test that protocol uses exact f₀=141.7001 Hz."""
        pulse = generate_bio_pulse()
        assert pulse.frequency == 141.7001
    
    def test_duration_60_seconds(self):
        """Test protocol uses 60 second duration."""
        pulse = generate_bio_pulse()
        assert pulse.duration == 60.0
    
    def test_sample_rate_44100(self):
        """Test protocol uses 44.1kHz sample rate (CD quality)."""
        pulse = generate_bio_pulse()
        assert pulse.sample_rate == 44100
    
    def test_fade_3_seconds(self):
        """Test protocol uses 3 second fade in/out."""
        pulse = generate_bio_pulse()
        # Default fade is 3 seconds
        fade_samples = int(3.0 * pulse.sample_rate)
        
        # Check fade in
        assert abs(pulse.signal[0]) < 0.01
        assert abs(pulse.signal[fade_samples]) > 0.1
        
        # Check fade out
        assert abs(pulse.signal[-1]) < 0.01
        assert abs(pulse.signal[-fade_samples]) > 0.1
    
    def test_headroom_safety(self):
        """Test protocol has safe headroom (-6dB)."""
        pulse = generate_bio_pulse()
        
        # Peak should be around -6dB
        assert abs(pulse.peak_db - (-6.0)) < 0.5


class TestProtocolValidation:
    """Test protocol meets all requirements."""
    
    def test_coherence_threshold(self):
        """Test that expected coherence meets Ψ > 0.999 requirement."""
        coherence = compute_coherence_metrics()
        assert coherence.psi_coherence >= 0.999
    
    def test_orch_or_stability(self):
        """Test that Orch-OR is predicted stable."""
        coherence = compute_coherence_metrics()
        assert coherence.is_stable
    
    def test_spectral_purity(self):
        """Test that signal is pure sinusoidal (single frequency)."""
        pulse = generate_bio_pulse(duration=10.0, fade_duration=0.0, headroom_db=0)  # No fade/headroom
        
        # FFT analysis on middle section to avoid edge effects
        mid_start = len(pulse.signal) // 4
        mid_end = 3 * len(pulse.signal) // 4
        fft = np.fft.rfft(pulse.signal[mid_start:mid_end])
        magnitude = np.abs(fft)
        freqs = np.fft.rfftfreq(mid_end - mid_start, 1/pulse.sample_rate)
        
        # Find dominant peak
        peak_idx = np.argmax(magnitude)
        peak_freq = freqs[peak_idx]
        
        # Should be close to f₀
        assert abs(peak_freq - pulse.frequency) < 1.0
        
        # Check that peak dominates: compare peak to average of other bins
        other_magnitude = np.concatenate([magnitude[:peak_idx-5], magnitude[peak_idx+5:]])
        if len(other_magnitude) > 0:
            avg_other = np.mean(other_magnitude)
            peak_value = magnitude[peak_idx]
            
            # Peak should be at least 100x larger than average noise floor
            assert peak_value / avg_other > 100


class TestPhaseEvaporationEvent:
    """Unit tests for PhaseEvaporationEvent dataclass."""

    def _make_event(self):
        return PhaseEvaporationEvent(
            psi=0.5,
            threshold=0.888,
            logos_hz=425.1003,
            delta_e_j=1.8829e8,
            description="test event",
        )

    def test_fields_stored(self):
        ev = self._make_event()
        assert ev.psi == 0.5
        assert ev.threshold == 0.888
        assert abs(ev.logos_hz - 425.1003) < 1e-4
        assert ev.delta_e_j > 0

    def test_description_not_empty(self):
        assert len(self._make_event().description) > 0


class TestPhaseRecoveryResult:
    """Unit tests for PhaseRecoveryResult dataclass."""

    def _make_decoupled(self):
        ev = PhaseEvaporationEvent(0.5, 0.888, 425.1, 1.8e8, "desc")
        return PhaseRecoveryResult(
            psi_in=0.5, decoupled=True, evaporation_event=ev,
            recovery_frequency_hz=425.1, description="recovery"
        )

    def _make_coupled(self):
        return PhaseRecoveryResult(
            psi_in=0.95, decoupled=False, evaporation_event=None,
            recovery_frequency_hz=F0_HZ, description="stable"
        )

    def test_decoupled_has_event(self):
        r = self._make_decoupled()
        assert r.evaporation_event is not None
        assert r.decoupled is True

    def test_coupled_has_no_event(self):
        r = self._make_coupled()
        assert r.evaporation_event is None
        assert r.decoupled is False

    def test_recovery_frequency_logos_when_decoupled(self):
        r = self._make_decoupled()
        assert abs(r.recovery_frequency_hz - 425.1) < 0.1

    def test_recovery_frequency_f0_when_coupled(self):
        r = self._make_coupled()
        assert r.recovery_frequency_hz == F0_HZ


class TestPhaseRecoveryProtocol:
    """Tests for PhaseRecoveryProtocol — the feedback loop engine."""

    @pytest.fixture
    def protocol(self):
        return PhaseRecoveryProtocol()

    # ---- construction ----

    def test_default_f0(self, protocol):
        assert protocol.soul.f0 == F0_HZ

    def test_logos_hz_approx_425(self, protocol):
        assert abs(protocol.logos_hz - 425.1) < 0.1

    def test_initial_events_empty(self, protocol):
        assert protocol.evaporation_events == []

    # ---- monitor_cycle: decoupled path ----

    def test_monitor_cycle_returns_result(self, protocol):
        result = protocol.monitor_cycle(0.5)
        assert isinstance(result, PhaseRecoveryResult)

    def test_monitor_cycle_decoupled_below_threshold(self, protocol):
        result = protocol.monitor_cycle(0.5)
        assert result.decoupled is True

    def test_monitor_cycle_recovery_freq_is_logos(self, protocol):
        result = protocol.monitor_cycle(0.5)
        assert abs(result.recovery_frequency_hz - protocol.logos_hz) < 1e-9

    def test_monitor_cycle_event_created(self, protocol):
        protocol.monitor_cycle(0.5)
        assert len(protocol.evaporation_events) == 1

    def test_monitor_cycle_event_psi_stored(self, protocol):
        protocol.monitor_cycle(0.777)
        ev = protocol.evaporation_events[0]
        assert abs(ev.psi - 0.777) < 1e-12

    def test_monitor_cycle_event_logos_hz(self, protocol):
        protocol.monitor_cycle(0.5)
        ev = protocol.evaporation_events[0]
        assert abs(ev.logos_hz - protocol.logos_hz) < 1e-9

    def test_monitor_cycle_event_delta_e_positive(self, protocol):
        protocol.monitor_cycle(0.5)
        ev = protocol.evaporation_events[0]
        assert ev.delta_e_j > 0

    def test_monitor_cycle_event_delta_e_approx_188_mj(self, protocol):
        protocol.monitor_cycle(0.5)
        ev = protocol.evaporation_events[0]
        assert abs(ev.delta_e_j / 1e6 - 188.29) < 0.5

    # ---- monitor_cycle: coupled path ----

    def test_monitor_cycle_not_decoupled_at_threshold(self, protocol):
        result = protocol.monitor_cycle(0.888)
        assert result.decoupled is False

    def test_monitor_cycle_coupled_no_event(self, protocol):
        result = protocol.monitor_cycle(0.95)
        assert result.evaporation_event is None

    def test_monitor_cycle_coupled_no_events_recorded(self, protocol):
        protocol.monitor_cycle(0.95)
        assert len(protocol.evaporation_events) == 0

    def test_monitor_cycle_coupled_freq_is_f0(self, protocol):
        result = protocol.monitor_cycle(0.95)
        assert result.recovery_frequency_hz == F0_HZ

    # ---- multiple cycles ----

    def test_multiple_decoupled_cycles_accumulate_events(self, protocol):
        for psi in [0.5, 0.6, 0.7]:
            protocol.monitor_cycle(psi)
        assert len(protocol.evaporation_events) == 3

    def test_coupled_cycles_do_not_add_events(self, protocol):
        for psi in [0.9, 0.95, 1.0]:
            protocol.monitor_cycle(psi)
        assert len(protocol.evaporation_events) == 0

    def test_evaporation_events_snapshot(self, protocol):
        """evaporation_events returns a copy, not the internal list."""
        protocol.monitor_cycle(0.5)
        snap = protocol.evaporation_events
        snap.clear()
        assert len(protocol.evaporation_events) == 1

    # ---- parametric boundary ----

    @pytest.mark.parametrize("psi", [0.0, 0.1, 0.5, 0.7, 0.887])
    def test_decoupled_below_threshold(self, protocol, psi):
        result = protocol.monitor_cycle(psi)
        assert result.decoupled is True

    @pytest.mark.parametrize("psi", [0.888, 0.9, 0.95, 0.999, 1.0])
    def test_not_decoupled_at_or_above(self, protocol, psi):
        result = protocol.monitor_cycle(psi)
        assert result.decoupled is False

    # ---- custom f0 ----

    def test_custom_f0_updates_soul(self):
        proto = PhaseRecoveryProtocol(f0=200.0)
        assert proto.soul.f0 == 200.0

    def test_custom_f0_updates_logos_hz(self):
        proto = PhaseRecoveryProtocol(f0=200.0)
        expected_logos = 21.0 * (200.0 / 7.0)
        assert abs(proto.logos_hz - expected_logos) < 1e-9


class TestRunPhaseRecoveryProtocol:
    """Tests for the standalone run_phase_recovery_protocol() function."""

    def test_returns_dict(self):
        result = run_phase_recovery_protocol([0.7, 0.9])
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = run_phase_recovery_protocol([0.7, 0.9])
        for key in ("protocol", "results", "events", "energy_impulse_j", "logos_hz"):
            assert key in result

    def test_protocol_is_instance(self):
        result = run_phase_recovery_protocol([0.9])
        assert isinstance(result["protocol"], PhaseRecoveryProtocol)

    def test_results_length_matches_input(self):
        psi_seq = [0.7, 0.8, 0.9, 1.0]
        result = run_phase_recovery_protocol(psi_seq)
        assert len(result["results"]) == len(psi_seq)

    def test_energy_impulse_positive(self):
        result = run_phase_recovery_protocol([0.9])
        assert result["energy_impulse_j"] > 0

    def test_energy_impulse_approx_188_mj(self):
        result = run_phase_recovery_protocol([0.9])
        assert abs(result["energy_impulse_j"] / 1e6 - 188.29) < 0.5

    def test_logos_hz_approx_425(self):
        result = run_phase_recovery_protocol([0.9])
        assert abs(result["logos_hz"] - 425.1) < 0.1

    def test_events_only_when_decoupled(self):
        result = run_phase_recovery_protocol([0.5, 0.5, 0.9])
        assert len(result["events"]) == 2

    def test_default_sequence_produces_events(self):
        """Default 0.7→1.0 sweep triggers several evaporation events."""
        result = run_phase_recovery_protocol()
        assert len(result["events"]) > 0


class TestRunCompleteProtocolPhaseRecovery:
    """Test that run_complete_protocol() now includes phase recovery results."""

    def test_phase_recovery_key_in_results(self):
        results = run_complete_protocol(generate_artifacts=False)
        assert "phase_recovery" in results

    def test_phase_recovery_has_logos_hz(self):
        results = run_complete_protocol(generate_artifacts=False)
        pr = results["phase_recovery"]
        assert abs(pr["logos_hz"] - 425.1) < 0.1

    def test_phase_recovery_has_energy_impulse(self):
        results = run_complete_protocol(generate_artifacts=False)
        pr = results["phase_recovery"]
        assert pr["energy_impulse_j"] > 0

    def test_phase_recovery_has_cycle_results(self):
        results = run_complete_protocol(generate_artifacts=False)
        pr = results["phase_recovery"]
        assert len(pr["cycle_results"]) > 0

    def test_existing_keys_still_present(self):
        """Existing keys must not be affected by phase recovery addition."""
        results = run_complete_protocol(generate_artifacts=False)
        assert "pulse" in results
        assert "coherence" in results


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
