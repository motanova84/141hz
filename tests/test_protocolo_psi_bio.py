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
    BioPulseSignal,
    CoherenceMetrics,
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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
