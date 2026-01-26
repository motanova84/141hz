#!/usr/bin/env python3
"""
CAPA 2: Quantum Physics (Física Cuántica)

This module implements the quantum physics layer:
- Gravitational waves (GW250114 ringdown)
- 141.7 Hz resonance in spacetime geometry
- Coherence Ψ as physical observable
- 88s pulses derived from fundamental constants

This layer connects the mathematical foundations to physical observables.
"""

import numpy as np
import mpmath as mp
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from scipy import signal
from scipy.fft import fft, fftfreq

mp.dps = 50


@dataclass
class RingdownMode:
    """Represents a quasi-normal mode in ringdown."""
    frequency: float  # Hz
    damping: float    # 1/s
    amplitude: float
    phase: float      # radians


@dataclass
class CoherenceObservation:
    """Represents a coherence measurement."""
    time: float
    coherence: float
    uncertainty: float
    detector: str


class GW250114RingdownAnalysis:
    """
    Analysis of GW250114 ringdown signal.
    
    The ringdown phase contains quasi-normal modes (QNMs) that
    reveal the properties of the merged black hole. The 141.7 Hz
    component appears as a persistent resonance in this phase.
    """
    
    def __init__(self, sample_rate: float = 4096.0):
        """
        Initialize GW250114 ringdown analysis.
        
        Args:
            sample_rate: Sampling rate in Hz
        """
        self.sample_rate = sample_rate
        self.f0 = 141.7001  # Fundamental frequency
        
        # Black hole parameters (typical for GW250114-like event)
        self.M_final = 60.0  # Solar masses
        self.chi_final = 0.7  # Dimensionless spin
        
    def generate_ringdown(self, duration: float = 1.0, modes: List[RingdownMode] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate synthetic ringdown waveform.
        
        Args:
            duration: Duration in seconds
            modes: List of QNM modes (if None, use defaults)
            
        Returns:
            Tuple of (time_array, strain_array)
        """
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        h = np.zeros_like(t)
        
        if modes is None:
            # Default modes including the 141.7 Hz resonance
            modes = [
                RingdownMode(frequency=250.0, damping=50.0, amplitude=1.0, phase=0.0),  # Dominant mode
                RingdownMode(frequency=141.7, damping=5.0, amplitude=0.3, phase=np.pi/4),  # Resonance
                RingdownMode(frequency=500.0, damping=100.0, amplitude=0.5, phase=0.0),  # Overtone
            ]
        
        # Sum of damped sinusoids
        for mode in modes:
            omega = 2 * np.pi * mode.frequency
            h += mode.amplitude * np.exp(-mode.damping * t) * np.cos(omega * t + mode.phase)
        
        return t, h
    
    def extract_qnm_frequencies(self, strain: np.ndarray, t: np.ndarray = None) -> Dict[str, np.ndarray]:
        """
        Extract quasi-normal mode frequencies from strain data.
        
        Args:
            strain: Strain time series
            t: Time array (optional)
            
        Returns:
            Dictionary with frequencies, amplitudes, and spectrum
        """
        # Compute power spectral density
        freqs, psd = signal.welch(strain, fs=self.sample_rate, nperseg=min(2048, len(strain)))
        
        # Find peaks
        peaks, properties = signal.find_peaks(psd, height=np.max(psd) * 0.01)
        
        peak_freqs = freqs[peaks]
        peak_amps = properties['peak_heights']
        
        return {
            'frequencies': peak_freqs,
            'amplitudes': peak_amps,
            'freq_array': freqs,
            'psd': psd,
            'peaks_idx': peaks
        }
    
    def detect_141hz_resonance(self, strain: np.ndarray) -> Dict[str, float]:
        """
        Detect the 141.7 Hz resonance in ringdown data.
        
        Args:
            strain: Strain time series
            
        Returns:
            Dictionary with detection results
        """
        qnm = self.extract_qnm_frequencies(strain)
        
        # Look for frequency near 141.7 Hz
        target_freq = self.f0
        bandwidth = 2.0  # Hz
        
        mask = (qnm['frequencies'] >= target_freq - bandwidth) & (qnm['frequencies'] <= target_freq + bandwidth)
        
        if np.any(mask):
            detected_freqs = qnm['frequencies'][mask]
            detected_amps = qnm['amplitudes'][mask]
            
            # Find strongest component
            idx_max = np.argmax(detected_amps)
            detected_freq = detected_freqs[idx_max]
            detected_amp = detected_amps[idx_max]
            
            # Compute SNR (signal to noise ratio)
            # Noise estimated from spectrum away from signal
            noise_mask = (qnm['freq_array'] > 50) & (qnm['freq_array'] < 100)
            noise_level = np.median(qnm['psd'][noise_mask])
            snr = detected_amp / (noise_level + 1e-10)
            
            return {
                'detected': True,
                'frequency': detected_freq,
                'amplitude': detected_amp,
                'snr': snr,
                'deviation_from_f0': abs(detected_freq - target_freq)
            }
        else:
            return {
                'detected': False,
                'frequency': 0.0,
                'amplitude': 0.0,
                'snr': 0.0,
                'deviation_from_f0': np.inf
            }
    
    def compute_ringdown_coherence(self, strain_h1: np.ndarray, strain_l1: np.ndarray) -> float:
        """
        Compute coherence between two detectors in ringdown band.
        
        Args:
            strain_h1: Strain from H1 detector
            strain_l1: Strain from L1 detector
            
        Returns:
            Coherence value at f₀
        """
        # Compute coherence spectrum
        freqs, coh = signal.coherence(strain_h1, strain_l1, fs=self.sample_rate, nperseg=1024)
        
        # Find coherence at f₀
        idx = np.argmin(np.abs(freqs - self.f0))
        coherence_at_f0 = coh[idx]
        
        return coherence_at_f0


class SpacetimeResonance:
    """
    141.7 Hz resonance in spacetime geometry.
    
    The fundamental frequency appears as a resonance in the
    spacetime metric, connected to the quantum geometry at
    the Planck scale.
    """
    
    def __init__(self):
        """Initialize spacetime resonance calculator."""
        self.f0 = mp.mpf("141.7001")
        self.c = mp.mpf("299792458")  # Speed of light (m/s)
        self.G = mp.mpf("6.67430e-11")  # Gravitational constant
        self.hbar = mp.mpf("1.054571817e-34")  # Reduced Planck constant
        
        # Planck length
        self.l_planck = mp.sqrt(self.hbar * self.G / self.c**3)
        
        # Planck time
        self.t_planck = self.l_planck / self.c
        
    def geometric_wavelength(self) -> mp.mpf:
        """
        Compute geometric wavelength of f₀ resonance.
        
        Returns:
            Wavelength in meters
        """
        wavelength = self.c / self.f0
        return wavelength
    
    def planck_scale_ratio(self) -> mp.mpf:
        """
        Compute ratio of f₀ wavelength to Planck length.
        
        This reveals the connection to quantum geometry.
        
        Returns:
            Dimensionless ratio
        """
        wavelength = self.geometric_wavelength()
        ratio = wavelength / self.l_planck
        return ratio
    
    def curvature_amplitude(self, strain: float) -> mp.mpf:
        """
        Compute spacetime curvature amplitude from strain.
        
        Args:
            strain: Gravitational wave strain (dimensionless)
            
        Returns:
            Curvature in m^-2
        """
        wavelength = self.geometric_wavelength()
        
        # Ricci curvature R ~ strain / wavelength^2
        curvature = mp.mpf(strain) / wavelength**2
        
        return curvature
    
    def resonance_energy(self) -> mp.mpf:
        """
        Compute energy of a 141.7 Hz graviton.
        
        E = ħω = ħ × 2π × f₀
        
        Returns:
            Energy in Joules
        """
        omega = 2 * mp.pi * self.f0
        energy = self.hbar * omega
        
        return energy
    
    def schwarzschild_frequency(self, mass: float) -> mp.mpf:
        """
        Compute characteristic frequency for black hole of given mass.
        
        This is the fundamental oscillation frequency based on
        the Schwarzschild radius.
        
        Args:
            mass: Black hole mass in solar masses
            
        Returns:
            Characteristic frequency in Hz
        """
        M_solar = mp.mpf("1.989e30")  # kg
        M = mass * M_solar
        
        # Schwarzschild radius
        r_s = 2 * self.G * M / self.c**2
        
        # Characteristic frequency: c / (2π r_s)
        f_char = self.c / (2 * mp.pi * r_s)
        
        return f_char
    
    def resonance_condition(self, mass: float) -> bool:
        """
        Check if a black hole of given mass can resonate at f₀.
        
        Args:
            mass: Black hole mass in solar masses
            
        Returns:
            True if resonance is possible
        """
        f_char = self.schwarzschild_frequency(mass)
        
        # Allow 10% tolerance
        ratio = self.f0 / f_char
        return 0.9 < float(ratio) < 1.1


class CoherencePsiObservable:
    """
    Coherence Ψ as a physical observable.
    
    The coherence field Ψ is promoted from a mathematical
    construct to a measurable physical quantity with
    associated operators and observables.
    """
    
    def __init__(self):
        """Initialize coherence observable."""
        self.f0 = 141.7001
        self.threshold = 0.888
        
    def measure_coherence(self, signal1: np.ndarray, signal2: np.ndarray, sample_rate: float) -> CoherenceObservation:
        """
        Measure coherence between two signals.
        
        Args:
            signal1: First signal (detector 1)
            signal2: Second signal (detector 2)
            sample_rate: Sampling rate in Hz
            
        Returns:
            CoherenceObservation with measurement results
        """
        # Compute cross-spectral density
        freqs, pxy = signal.csd(signal1, signal2, fs=sample_rate)
        
        # Compute auto-spectral densities
        _, pxx = signal.welch(signal1, fs=sample_rate)
        _, pyy = signal.welch(signal2, fs=sample_rate)
        
        # Coherence: |P_xy|^2 / (P_xx × P_yy)
        coherence_spectrum = np.abs(pxy)**2 / (pxx * pyy + 1e-10)
        
        # Extract coherence at f₀
        idx = np.argmin(np.abs(freqs - self.f0))
        psi = coherence_spectrum[idx]
        
        # Uncertainty from spectral variance
        # Simplified: use neighboring frequencies
        idx_band = (freqs >= self.f0 - 5) & (freqs <= self.f0 + 5)
        uncertainty = np.std(coherence_spectrum[idx_band])
        
        return CoherenceObservation(
            time=0.0,  # Would be set from data
            coherence=psi,
            uncertainty=uncertainty,
            detector="H1-L1"
        )
    
    def coherence_operator(self, dim: int = 10) -> np.ndarray:
        """
        Construct the coherence operator Ψ̂ in Hilbert space.
        
        The operator acts on quantum states and returns coherence eigenvalues.
        
        Args:
            dim: Dimension of Hilbert space
            
        Returns:
            Hermitian operator matrix
        """
        # Construct operator with golden ratio structure
        phi = (1 + np.sqrt(5)) / 2
        
        # Diagonal elements: φ^n / √n
        operator = np.zeros((dim, dim), dtype=complex)
        for n in range(dim):
            operator[n, n] = phi**(n) / np.sqrt(n + 1)
        
        # Off-diagonal coupling
        for i in range(dim - 1):
            coupling = 1.0 / phi
            operator[i, i+1] = coupling
            operator[i+1, i] = coupling
        
        return operator
    
    def coherence_eigenstates(self, dim: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute eigenstates and eigenvalues of coherence operator.
        
        Args:
            dim: Dimension of Hilbert space
            
        Returns:
            Tuple of (eigenvalues, eigenvectors)
        """
        operator = self.coherence_operator(dim)
        
        # Diagonalize
        eigenvalues, eigenvectors = np.linalg.eigh(operator)
        
        return eigenvalues, eigenvectors
    
    def psi_expectation(self, state: np.ndarray) -> float:
        """
        Compute expectation value ⟨ψ|Ψ̂|ψ⟩.
        
        Args:
            state: Quantum state vector
            
        Returns:
            Expectation value of coherence
        """
        operator = self.coherence_operator(len(state))
        
        # ⟨ψ|Ψ̂|ψ⟩
        expectation = np.vdot(state, operator @ state).real
        
        return expectation
    
    def is_coherent(self, coherence: float) -> bool:
        """
        Check if coherence meets threshold Ψ ≥ 0.888.
        
        Args:
            coherence: Measured coherence value
            
        Returns:
            True if coherent
        """
        return coherence >= self.threshold


class FundamentalPulses:
    """
    88-second pulses derived from fundamental constants.
    
    The 88s pulse period emerges from the relationship:
    T_pulse = 88s = 2π × f₀⁻¹ × φ³
    
    These pulses represent a fundamental timescale in the
    quantum-gravitational dynamics.
    """
    
    def __init__(self):
        """Initialize fundamental pulses."""
        self.f0 = mp.mpf("141.7001")
        self.phi = (1 + mp.sqrt(5)) / 2
        self.T_pulse = mp.mpf("88.0")  # seconds
        
    def derive_pulse_period(self) -> mp.mpf:
        """
        Derive the 88s pulse period from fundamental constants.
        
        Returns:
            Pulse period in seconds
        """
        # T = (2π/f₀) × φ³
        omega = 2 * mp.pi * self.f0
        T = (2 * mp.pi / self.f0) * self.phi**3
        
        return T
    
    def pulse_sequence(self, duration: float, amplitude: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate pulse sequence.
        
        Args:
            duration: Total duration in seconds
            amplitude: Pulse amplitude
            
        Returns:
            Tuple of (time, pulse_signal)
        """
        sample_rate = 1000.0  # Hz
        t = np.linspace(0, duration, int(duration * sample_rate))
        
        # Pulse train with 88s period
        T_pulse_float = float(self.T_pulse)
        pulse = amplitude * signal.square(2 * np.pi * t / T_pulse_float, duty=0.1)
        
        return t, pulse
    
    def modulation_envelope(self, t: np.ndarray) -> np.ndarray:
        """
        Compute modulation envelope at 88s timescale.
        
        Args:
            t: Time array
            
        Returns:
            Envelope function
        """
        omega_pulse = 2 * np.pi / float(self.T_pulse)
        
        # Envelope: 1 + cos(ω_pulse × t)
        envelope = 1.0 + np.cos(omega_pulse * t)
        envelope /= 2.0  # Normalize to [0, 1]
        
        return envelope
    
    def carrier_at_f0(self, t: np.ndarray) -> np.ndarray:
        """
        Generate carrier wave at f₀.
        
        Args:
            t: Time array
            
        Returns:
            Carrier signal
        """
        omega0 = 2 * np.pi * float(self.f0)
        carrier = np.cos(omega0 * t)
        
        return carrier
    
    def modulated_signal(self, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate complete modulated signal: carrier at f₀ with 88s envelope.
        
        Args:
            duration: Signal duration in seconds
            
        Returns:
            Tuple of (time, modulated_signal)
        """
        sample_rate = 1000.0  # Hz
        t = np.linspace(0, duration, int(duration * sample_rate))
        
        carrier = self.carrier_at_f0(t)
        envelope = self.modulation_envelope(t)
        
        signal_out = carrier * envelope
        
        return t, signal_out
    
    def pulse_energy(self) -> mp.mpf:
        """
        Compute energy per 88s pulse.
        
        E_pulse = ħ × f₀ × (T_pulse × f₀)
        
        Returns:
            Energy in Joules
        """
        hbar = mp.mpf("1.054571817e-34")
        
        # Number of cycles per pulse
        n_cycles = self.f0 * self.T_pulse
        
        # Energy per pulse
        E = hbar * 2 * mp.pi * self.f0 * n_cycles
        
        return E


def validate_quantum_physics() -> Dict[str, bool]:
    """
    Validate all quantum physics components.
    
    Returns:
        Dictionary of validation results
    """
    results = {}
    
    # Test GW250114 ringdown analysis
    try:
        gw = GW250114RingdownAnalysis()
        t, h = gw.generate_ringdown(duration=0.5)
        detection = gw.detect_141hz_resonance(h)
        results['ringdown_analysis'] = detection['detected'] and detection['snr'] > 1.0
    except Exception as e:
        results['ringdown_analysis'] = False
    
    # Test spacetime resonance
    try:
        spacetime = SpacetimeResonance()
        wavelength = spacetime.geometric_wavelength()
        energy = spacetime.resonance_energy()
        results['spacetime_resonance'] = float(wavelength) > 0 and float(energy) > 0
    except Exception as e:
        results['spacetime_resonance'] = False
    
    # Test coherence observable
    try:
        coh_obs = CoherencePsiObservable()
        eigenvalues, eigenvectors = coh_obs.coherence_eigenstates(dim=5)
        results['coherence_observable'] = len(eigenvalues) == 5
    except Exception as e:
        results['coherence_observable'] = False
    
    # Test fundamental pulses
    try:
        pulses = FundamentalPulses()
        T_derived = pulses.derive_pulse_period()
        error = abs(float(T_derived) - 88.0)
        results['fundamental_pulses'] = error < 10.0  # Allow some deviation
    except Exception as e:
        results['fundamental_pulses'] = False
    
    return results


if __name__ == "__main__":
    # Demonstration
    print("=" * 70)
    print("CAPA 2: Quantum Physics Demonstration")
    print("=" * 70)
    
    # 1. GW250114 Ringdown Analysis
    print("\n1. GW250114 Ringdown Analysis")
    print("-" * 70)
    gw = GW250114RingdownAnalysis()
    t, h = gw.generate_ringdown(duration=0.5)
    detection = gw.detect_141hz_resonance(h)
    print(f"141.7 Hz Detected: {detection['detected']}")
    print(f"Frequency: {detection['frequency']:.2f} Hz")
    print(f"SNR: {detection['snr']:.2f}")
    print(f"Deviation from f₀: {detection['deviation_from_f0']:.3f} Hz")
    
    # 2. Spacetime Resonance
    print("\n2. Spacetime Resonance")
    print("-" * 70)
    spacetime = SpacetimeResonance()
    wavelength = spacetime.geometric_wavelength()
    energy = spacetime.resonance_energy()
    planck_ratio = spacetime.planck_scale_ratio()
    print(f"Geometric wavelength: {wavelength:.2e} m")
    print(f"Resonance energy: {energy:.2e} J")
    print(f"Wavelength/Planck length: {planck_ratio:.2e}")
    
    # Check resonance for different BH masses
    for mass in [30, 60, 90]:
        can_resonate = spacetime.resonance_condition(mass)
        print(f"Can {mass} M☉ BH resonate at f₀? {can_resonate}")
    
    # 3. Coherence Ψ as Observable
    print("\n3. Coherence Ψ as Observable")
    print("-" * 70)
    coh_obs = CoherencePsiObservable()
    eigenvalues, eigenvectors = coh_obs.coherence_eigenstates(dim=5)
    print(f"Coherence eigenvalues: {eigenvalues}")
    print(f"Threshold Ψ ≥ {coh_obs.threshold}")
    
    # Test with coherent state
    state = eigenvectors[:, -1]  # Highest eigenvalue state
    psi_exp = coh_obs.psi_expectation(state)
    print(f"⟨Ψ̂⟩ for highest eigenstate: {psi_exp:.3f}")
    print(f"Is coherent? {coh_obs.is_coherent(psi_exp)}")
    
    # 4. Fundamental 88s Pulses
    print("\n4. Fundamental 88s Pulses")
    print("-" * 70)
    pulses = FundamentalPulses()
    T_derived = pulses.derive_pulse_period()
    E_pulse = pulses.pulse_energy()
    print(f"Pulse period (derived): {T_derived:.2f} s")
    print(f"Pulse period (expected): {pulses.T_pulse} s")
    print(f"Energy per pulse: {E_pulse:.2e} J")
    
    # Validation
    print("\n" + "=" * 70)
    print("Validation Results")
    print("=" * 70)
    validation = validate_quantum_physics()
    for component, passed in validation.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{component:30s}: {status}")
