#!/usr/bin/env python3
"""
Frequency Response Analyzer for QCAL Falsifiability Experiments

This module measures ΔF(ω) with ~0.3% precision through multi-sensor averaging.
It detects spectral peaks at QCAL frequencies and models resonances with
Lorentzian profiles including biological noise.

Key features:
- Multi-sensor averaging: 88 sensors × 1000 averages → noise reduction ~297×
- Spectral peak detection at QCAL frequencies (141.7, 177.6, 888 Hz)
- Lorentzian resonance modeling with biological noise
- SNR > 40 dB for reliable measurements
"""

import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from scipy import signal
from scipy.optimize import curve_fit


@dataclass
class MeasurementResult:
    """Result of a frequency response measurement."""
    frequency: float
    delta_f: float
    uncertainty: float
    snr_db: float
    coherence: float
    spectral_power: float
    noise_floor: float


@dataclass
class SpectralPeak:
    """Detected spectral peak information."""
    frequency: float
    amplitude: float
    width: float
    snr: float
    is_qcal_frequency: bool


class LorentzianResonanceModel:
    """
    Lorentzian resonance model for biological responses.
    
    Models the frequency response as:
    L(f) = A / (1 + ((f - f0) / γ)²) + N(f)
    
    Where:
    - A: Peak amplitude
    - f0: Resonance frequency
    - γ: Linewidth (FWHM/2)
    - N(f): Biological noise component
    """
    
    @staticmethod
    def lorentzian(f: np.ndarray, amplitude: float, f0: float, gamma: float, offset: float) -> np.ndarray:
        """
        Lorentzian function.
        
        Args:
            f: Frequency array
            amplitude: Peak amplitude
            f0: Center frequency
            gamma: Half-width at half-maximum
            offset: Baseline offset
        
        Returns:
            Lorentzian profile
        """
        return amplitude / (1 + ((f - f0) / gamma)**2) + offset
    
    def fit_peak(
        self,
        frequencies: np.ndarray,
        response: np.ndarray,
        f0_guess: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Fit Lorentzian to spectral peak.
        
        Args:
            frequencies: Frequency array
            response: Measured response
            f0_guess: Initial guess for peak frequency
        
        Returns:
            (fitted_params, fitted_covariance)
        """
        # Initial guess: amplitude, f0, gamma, offset
        p0 = [np.max(response), f0_guess, 1.0, np.median(response)]
        
        # Bounds to ensure physical parameters
        bounds = (
            [0, f0_guess - 10, 0.1, 0],  # Lower bounds
            [np.inf, f0_guess + 10, 10, np.max(response)]  # Upper bounds
        )
        
        try:
            popt, pcov = curve_fit(
                self.lorentzian,
                frequencies,
                response,
                p0=p0,
                bounds=bounds,
                maxfev=5000
            )
            return popt, pcov
        except RuntimeError:
            # If fit fails, return guess values with high uncertainty
            return np.array(p0), np.eye(4) * 1e6
    
    def add_biological_noise(
        self,
        signal: np.ndarray,
        noise_level: float = 0.1,
        pink_noise_fraction: float = 0.5
    ) -> np.ndarray:
        """
        Add realistic biological noise (white + pink noise).
        
        Args:
            signal: Clean signal
            noise_level: Relative noise level
            pink_noise_fraction: Fraction of pink (1/f) noise
        
        Returns:
            Signal with biological noise
        """
        n = len(signal)
        
        # White noise component
        white_noise = np.random.randn(n) * noise_level * (1 - pink_noise_fraction)
        
        # Pink (1/f) noise component
        # Generate in frequency domain and transform
        freqs = np.fft.rfftfreq(n)
        freqs[0] = 1e-10  # Avoid division by zero
        pink_spectrum = 1.0 / np.sqrt(freqs)
        pink_spectrum[0] = 0  # No DC component
        
        # Random phase
        phase = np.exp(2j * np.pi * np.random.rand(len(pink_spectrum)))
        pink_fft = pink_spectrum * phase
        
        # Transform to time domain
        pink_noise_raw = np.fft.irfft(pink_fft, n)
        pink_noise = pink_noise_raw / np.std(pink_noise_raw) * noise_level * pink_noise_fraction
        
        return signal + white_noise + pink_noise


class SpectralPeakDetector:
    """
    Detector for spectral peaks at QCAL frequencies.
    
    QCAL predicts discrete spectral structure at specific frequencies:
    - 141.7 Hz: Primary resonance
    - 177.6 Hz: Secondary harmonic
    - 888 Hz: Higher harmonic
    """
    
    # QCAL predicted frequencies
    QCAL_FREQUENCIES = {
        141.7: {'name': 'Primary resonance', 'tolerance': 2.0},
        177.6: {'name': 'Secondary harmonic', 'tolerance': 2.0},
        888.0: {'name': 'Higher harmonic', 'tolerance': 5.0}
    }
    
    def __init__(self, snr_threshold: float = 3.0):
        """
        Initialize peak detector.
        
        Args:
            snr_threshold: Minimum SNR for valid peak detection
        """
        self.snr_threshold = snr_threshold
    
    def detect_peaks(
        self,
        frequencies: np.ndarray,
        power_spectrum: np.ndarray
    ) -> List[SpectralPeak]:
        """
        Detect spectral peaks in power spectrum.
        
        Args:
            frequencies: Frequency array
            power_spectrum: Power spectral density
        
        Returns:
            List of detected peaks
        """
        # Find peaks using scipy
        peak_indices, properties = signal.find_peaks(
            power_spectrum,
            height=np.median(power_spectrum) * 2,
            prominence=np.std(power_spectrum)
        )
        
        peaks = []
        noise_floor = np.median(power_spectrum)
        
        for idx in peak_indices:
            freq = frequencies[idx]
            amplitude = power_spectrum[idx]
            snr = amplitude / noise_floor if noise_floor > 0 else 0
            
            # Estimate width
            width = self._estimate_peak_width(frequencies, power_spectrum, idx)
            
            # Check if it's a QCAL frequency
            is_qcal = self._is_qcal_frequency(freq)
            
            if snr >= self.snr_threshold:
                peaks.append(SpectralPeak(
                    frequency=freq,
                    amplitude=amplitude,
                    width=width,
                    snr=snr,
                    is_qcal_frequency=is_qcal
                ))
        
        return peaks
    
    def _estimate_peak_width(
        self,
        frequencies: np.ndarray,
        power_spectrum: np.ndarray,
        peak_idx: int
    ) -> float:
        """Estimate FWHM of peak."""
        peak_height = power_spectrum[peak_idx]
        half_height = peak_height / 2
        
        # Find indices where spectrum crosses half height
        left_idx = peak_idx
        while left_idx > 0 and power_spectrum[left_idx] > half_height:
            left_idx -= 1
        
        right_idx = peak_idx
        while right_idx < len(power_spectrum) - 1 and power_spectrum[right_idx] > half_height:
            right_idx += 1
        
        width = frequencies[right_idx] - frequencies[left_idx]
        return width
    
    def _is_qcal_frequency(self, freq: float) -> bool:
        """Check if frequency matches QCAL prediction."""
        for qcal_freq, info in self.QCAL_FREQUENCIES.items():
            if abs(freq - qcal_freq) < info['tolerance']:
                return True
        return False


class FrequencyResponseAnalyzer:
    """
    High-precision frequency response analyzer.
    
    Measures ΔF(ω) with ~0.3% precision through:
    - Multi-sensor averaging (88 sensors)
    - Multiple measurements (1000 averages)
    - Noise reduction: √(88 × 1000) ≈ 297×
    
    Example:
        analyzer = FrequencyResponseAnalyzer(n_sensors=88, n_averages=1000)
        measurement = analyzer.measure_delta_f(frequency=141.7, coherence=0.923)
    """
    
    def __init__(
        self,
        n_sensors: int = 88,
        n_averages: int = 1000,
        sampling_rate: int = 10000
    ):
        """
        Initialize analyzer.
        
        Args:
            n_sensors: Number of independent sensors
            n_averages: Number of averages per sensor
            sampling_rate: Sampling rate in Hz
        """
        self.n_sensors = n_sensors
        self.n_averages = n_averages
        self.sampling_rate = sampling_rate
        self.peak_detector = SpectralPeakDetector()
        self.resonance_model = LorentzianResonanceModel()
    
    def measure_delta_f(
        self,
        frequency: float,
        coherence: float = 0.923,
        duration: float = 1.0,
        noise_level: float = 0.05
    ) -> MeasurementResult:
        """
        Measure ΔF at specific frequency with multi-sensor averaging.
        
        Args:
            frequency: Measurement frequency in Hz
            coherence: Expected coherence level (0-1)
            duration: Measurement duration
            noise_level: Biological noise level
        
        Returns:
            Measurement result with uncertainty
        """
        measurements = []
        
        # Multi-sensor, multi-average measurement
        for _ in range(self.n_sensors):
            sensor_measurements = []
            
            for _ in range(self.n_averages):
                # Simulate biological response
                # Response depends on coherence and proximity to QCAL frequencies
                response = self._simulate_biological_response(
                    frequency, coherence, duration, noise_level
                )
                sensor_measurements.append(response)
            
            # Average over measurements for this sensor
            measurements.append(np.mean(sensor_measurements))
        
        # Convert to numpy array
        measurements = np.array(measurements)
        
        # Calculate statistics
        delta_f = np.mean(measurements)
        uncertainty = np.std(measurements) / np.sqrt(len(measurements))
        
        # Calculate SNR
        signal_power = delta_f**2
        noise_power = uncertainty**2
        snr_linear = signal_power / noise_power if noise_power > 0 else 1e6
        snr_db = 10 * np.log10(snr_linear)
        
        # Estimate spectral power and noise floor
        spectral_power = delta_f
        noise_floor = noise_level
        
        return MeasurementResult(
            frequency=frequency,
            delta_f=delta_f,
            uncertainty=uncertainty,
            snr_db=snr_db,
            coherence=coherence,
            spectral_power=spectral_power,
            noise_floor=noise_floor
        )
    
    def _simulate_biological_response(
        self,
        frequency: float,
        coherence: float,
        duration: float,
        noise_level: float
    ) -> float:
        """
        Simulate biological response at given frequency.
        
        QCAL prediction: Discrete spectral structure (peaks at specific frequencies)
        Traditional biology: Flat response (energy-dependent only)
        
        Args:
            frequency: Stimulus frequency
            coherence: System coherence
            duration: Measurement duration
            noise_level: Noise level
        
        Returns:
            Response amplitude
        """
        # Base response (would be ~1.0 for traditional biology)
        base_response = 1.0
        
        # QCAL enhancement at resonance frequencies
        qcal_enhancement = 0.0
        for qcal_freq, info in SpectralPeakDetector.QCAL_FREQUENCIES.items():
            # Lorentzian enhancement
            gamma = 2.0  # Linewidth
            enhancement = coherence * 3.0 / (1 + ((frequency - qcal_freq) / gamma)**2)
            qcal_enhancement += enhancement
        
        # Total response
        response = base_response + qcal_enhancement
        
        # Add biological noise
        noise = np.random.randn() * noise_level * response
        
        return response + noise
    
    def analyze_spectrum(
        self,
        frequencies: np.ndarray,
        coherence: float = 0.923,
        duration: float = 1.0
    ) -> Dict[str, any]:
        """
        Analyze frequency response over a range of frequencies.
        
        Args:
            frequencies: Array of frequencies to test
            coherence: System coherence
            duration: Duration per measurement
        
        Returns:
            Spectral analysis results
        """
        responses = []
        uncertainties = []
        
        for freq in frequencies:
            result = self.measure_delta_f(freq, coherence, duration)
            responses.append(result.delta_f)
            uncertainties.append(result.uncertainty)
        
        responses = np.array(responses)
        uncertainties = np.array(uncertainties)
        
        # Detect peaks
        peaks = self.peak_detector.detect_peaks(frequencies, responses)
        
        # Calculate mean precision
        precision = np.mean(uncertainties / responses)
        
        return {
            'frequencies': frequencies,
            'responses': responses,
            'uncertainties': uncertainties,
            'peaks': peaks,
            'precision': precision,
            'n_qcal_peaks': sum(1 for p in peaks if p.is_qcal_frequency)
        }
    
    def get_noise_reduction_factor(self) -> float:
        """
        Calculate theoretical noise reduction from averaging.
        
        Returns:
            Noise reduction factor
        """
        return np.sqrt(self.n_sensors * self.n_averages)


def demonstrate_frequency_analyzer():
    """Demonstrate frequency response analyzer."""
    print("QCAL Frequency Response Analyzer Demonstration")
    print("=" * 60)
    
    # Create analyzer
    analyzer = FrequencyResponseAnalyzer(n_sensors=88, n_averages=1000)
    
    print(f"\nConfiguration:")
    print(f"  Sensors: {analyzer.n_sensors}")
    print(f"  Averages per sensor: {analyzer.n_averages}")
    print(f"  Noise reduction: {analyzer.get_noise_reduction_factor():.1f}×")
    
    # Measure at QCAL frequency
    print("\nTest 1: Measure ΔF at 141.7 Hz (QCAL resonance)")
    result = analyzer.measure_delta_f(frequency=141.7, coherence=0.923)
    print(f"  ΔF(141.7 Hz) = {result.delta_f:.3f} ± {result.uncertainty:.3f}")
    print(f"  SNR = {result.snr_db:.1f} dB")
    print(f"  Precision = {(result.uncertainty/result.delta_f)*100:.2f}%")
    
    # Measure at control frequency
    print("\nTest 2: Measure ΔF at 100 Hz (control)")
    result_control = analyzer.measure_delta_f(frequency=100.0, coherence=0.923)
    print(f"  ΔF(100 Hz) = {result_control.delta_f:.3f} ± {result_control.uncertainty:.3f}")
    print(f"  SNR = {result_control.snr_db:.1f} dB")
    
    # Calculate ratio
    ratio = result.delta_f / result_control.delta_f
    print(f"\nRatio ΔF(141.7)/ΔF(100) = {ratio:.2f}")
    
    # Analyze spectrum
    print("\nTest 3: Spectral analysis")
    frequencies = np.linspace(50, 300, 100)
    spectrum = analyzer.analyze_spectrum(frequencies, coherence=0.923)
    print(f"  Frequency range: {frequencies[0]:.1f} - {frequencies[-1]:.1f} Hz")
    print(f"  Peaks detected: {len(spectrum['peaks'])}")
    print(f"  QCAL peaks: {spectrum['n_qcal_peaks']}")
    print(f"  Mean precision: {spectrum['precision']*100:.2f}%")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_frequency_analyzer()
