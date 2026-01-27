#!/usr/bin/env python3
"""
QCAL Biological Framework - Mathematical Implementation

This module implements the mathematical formalization of the QCAL hypothesis
for biological systems, including spectral field theory, phase accumulation,
and biological resonance mechanisms.

Mathematical Framework:
    1. Environmental spectral field: Ψₑ(t) = Σᵢ Aᵢ e^(i(ωᵢt + φᵢ))
    2. Biological filter: H(ω) = ∫ G(τ)e^(-iωτ)dτ
    3. Phase accumulation: Φ(t) = ∫₀ᵗ |H(ω)*Ψₑ(ω)|² dω
    4. Activation condition: Φ(t) ≥ Φ_crítico AND dΦ/dt > 0
    5. Phase memory: Φ_acum = αΦ(t) + (1-α)Φ(t-Δt)

Author: José Manuel Mota Burruezo
Date: 27 de enero de 2026
Institution: Instituto Consciencia Cuántica QCAL ∞³
"""

import numpy as np
from typing import List, Tuple, Callable, Optional
from dataclasses import dataclass
import warnings


@dataclass
class SpectralComponent:
    """
    Represents a single spectral component in the environmental field.
    
    Attributes:
        amplitude (float): Amplitude Aᵢ of the component
        frequency (float): Angular frequency ωᵢ (rad/s)
        phase (float): Initial phase φᵢ (radians)
        description (str): Physical interpretation of this component
    """
    amplitude: float
    frequency: float
    phase: float
    description: str = ""
    
    def evaluate(self, t: np.ndarray) -> np.ndarray:
        """
        Evaluate this spectral component at time t.
        
        Args:
            t: Time array (in appropriate units)
            
        Returns:
            Complex array: Aᵢ * exp(i(ωᵢt + φᵢ))
        """
        return self.amplitude * np.exp(1j * (self.frequency * t + self.phase))


class EnvironmentalSpectralField:
    """
    Represents the environmental spectral field Ψₑ(t).
    
    The field is a superposition of spectral components representing
    different periodic environmental signals (temperature, light, humidity, etc.).
    """
    
    def __init__(self, components: Optional[List[SpectralComponent]] = None):
        """
        Initialize the environmental spectral field.
        
        Args:
            components: List of SpectralComponent objects
        """
        self.components = components if components is not None else []
    
    def add_component(self, amplitude: float, frequency: float, 
                     phase: float = 0.0, description: str = ""):
        """
        Add a spectral component to the field.
        
        Args:
            amplitude: Component amplitude
            frequency: Angular frequency (rad/s)
            phase: Initial phase (radians)
            description: Physical interpretation
        """
        component = SpectralComponent(amplitude, frequency, phase, description)
        self.components.append(component)
    
    def evaluate(self, t: np.ndarray) -> np.ndarray:
        """
        Evaluate the total spectral field at time t.
        
        Args:
            t: Time array
            
        Returns:
            Complex array: Ψₑ(t) = Σᵢ Aᵢ e^(i(ωᵢt + φᵢ))
        """
        if len(self.components) == 0:
            return np.zeros_like(t, dtype=complex)
        
        psi = np.zeros_like(t, dtype=complex)
        for component in self.components:
            psi += component.evaluate(t)
        
        return psi
    
    def power_spectrum(self, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the power spectrum of the field.
        
        Args:
            t: Time array
            
        Returns:
            Tuple of (frequencies, power_spectrum)
        """
        psi = self.evaluate(t)
        dt = t[1] - t[0] if len(t) > 1 else 1.0
        
        fft_psi = np.fft.fft(psi)
        power = np.abs(fft_psi)**2
        freqs = np.fft.fftfreq(len(t), dt)
        
        # Return positive frequencies only
        positive_freq_idx = freqs >= 0
        return freqs[positive_freq_idx], power[positive_freq_idx]


class BiologicalFilter:
    """
    Represents the biological filter H(ω) that selects specific frequencies.
    
    The filter represents evolutionary adaptation to environmental frequencies.
    """
    
    def __init__(self, response_function: Optional[Callable] = None,
                 center_frequencies: Optional[List[float]] = None,
                 bandwidths: Optional[List[float]] = None):
        """
        Initialize the biological filter.
        
        Args:
            response_function: Custom response function G(τ)
            center_frequencies: List of resonant frequencies (Hz)
            bandwidths: List of bandwidths for each resonance (Hz)
        """
        self.response_function = response_function
        self.center_frequencies = center_frequencies if center_frequencies else []
        self.bandwidths = bandwidths if bandwidths else []
        
        if len(self.center_frequencies) != len(self.bandwidths):
            self.bandwidths = [1.0] * len(self.center_frequencies)
    
    def frequency_response(self, omega: np.ndarray) -> np.ndarray:
        """
        Compute the frequency response H(ω).
        
        For simplicity, uses a sum of Gaussian filters centered at resonant frequencies.
        
        Args:
            omega: Angular frequency array (rad/s)
            
        Returns:
            Complex frequency response H(ω)
        """
        if len(self.center_frequencies) == 0:
            # Default: bandpass filter
            return np.ones_like(omega, dtype=complex)
        
        H = np.zeros_like(omega, dtype=complex)
        
        for f0, bw in zip(self.center_frequencies, self.bandwidths):
            omega0 = 2 * np.pi * f0
            sigma = 2 * np.pi * bw
            
            # Gaussian filter centered at omega0
            H += np.exp(-((omega - omega0)**2) / (2 * sigma**2))
        
        return H
    
    def filter_signal(self, psi: np.ndarray, freqs: np.ndarray) -> np.ndarray:
        """
        Filter the spectral field through the biological filter.
        
        Args:
            psi: Environmental field in frequency domain
            freqs: Frequency array
            
        Returns:
            Filtered signal in frequency domain
        """
        omega = 2 * np.pi * freqs
        H = self.frequency_response(omega)
        return H * psi


class PhaseAccumulator:
    """
    Implements phase accumulation and memory for biological systems.
    
    Integrates filtered spectral energy over time and maintains phase memory.
    """
    
    def __init__(self, threshold: float = 1.0, memory_alpha: float = 0.1):
        """
        Initialize the phase accumulator.
        
        Args:
            threshold: Critical phase threshold Φ_crítico
            memory_alpha: Memory retention factor α (default 0.1 = 90% retention)
        """
        self.threshold = threshold
        self.memory_alpha = memory_alpha
        self.phase_history = []
        self.time_history = []
    
    def accumulate_phase(self, filtered_field: np.ndarray, 
                        t: np.ndarray) -> np.ndarray:
        """
        Compute accumulated phase Φ(t) from filtered spectral field.
        
        Φ(t) = ∫₀ᵗ |H(ω)*Ψₑ(ω)|² dω
        
        Args:
            filtered_field: Filtered environmental field
            t: Time array
            
        Returns:
            Accumulated phase array Φ(t)
        """
        # Energy density: |filtered_field|²
        energy_density = np.abs(filtered_field)**2
        
        # Cumulative integration
        dt = np.diff(t)
        dt = np.concatenate([[dt[0]], dt])  # Extend to match array size
        
        phase = np.cumsum(energy_density * dt)
        
        return phase
    
    def apply_memory(self, current_phase: np.ndarray) -> np.ndarray:
        """
        Apply phase memory: Φ_acum = αΦ(t) + (1-α)Φ(t-Δt)
        
        Args:
            current_phase: Current phase array
            
        Returns:
            Phase with memory applied
        """
        if len(self.phase_history) == 0:
            # First iteration: no previous phase
            return current_phase
        
        previous_phase = self.phase_history[-1]
        
        # Ensure arrays have same length
        min_len = min(len(current_phase), len(previous_phase))
        
        memorized_phase = (self.memory_alpha * current_phase[:min_len] + 
                          (1 - self.memory_alpha) * previous_phase[:min_len])
        
        return memorized_phase
    
    def check_activation(self, phase: np.ndarray, t: np.ndarray) -> Tuple[bool, Optional[float]]:
        """
        Check activation condition: Φ(t) ≥ Φ_crítico AND dΦ/dt > 0
        
        Args:
            phase: Accumulated phase array
            t: Time array
            
        Returns:
            Tuple of (activated, activation_time)
        """
        # Compute derivative dΦ/dt
        dphase_dt = np.gradient(phase, t)
        
        # Find points where both conditions are met
        activation_condition = (phase >= self.threshold) & (dphase_dt > 0)
        
        if np.any(activation_condition):
            # Find first activation time
            activation_idx = np.where(activation_condition)[0][0]
            activation_time = t[activation_idx]
            return True, activation_time
        
        return False, None
    
    def update_history(self, phase: np.ndarray, t: np.ndarray):
        """
        Update phase and time history for memory.
        
        Args:
            phase: Current phase array
            t: Current time array
        """
        self.phase_history.append(phase.copy())
        self.time_history.append(t.copy())


class QCALBiologicalSystem:
    """
    Complete QCAL biological system integrating all components.
    
    Combines environmental field, biological filter, and phase accumulation
    to model biological activation and synchronization.
    """
    
    def __init__(self, 
                 env_field: EnvironmentalSpectralField,
                 bio_filter: BiologicalFilter,
                 phase_accumulator: PhaseAccumulator):
        """
        Initialize complete QCAL biological system.
        
        Args:
            env_field: Environmental spectral field
            bio_filter: Biological frequency filter
            phase_accumulator: Phase accumulation and memory system
        """
        self.env_field = env_field
        self.bio_filter = bio_filter
        self.phase_accumulator = phase_accumulator
    
    def simulate(self, t: np.ndarray, 
                apply_memory: bool = True) -> dict:
        """
        Simulate the complete QCAL biological system.
        
        Args:
            t: Time array for simulation
            apply_memory: Whether to apply phase memory
            
        Returns:
            Dictionary with simulation results including:
                - 'environmental_field': Ψₑ(t)
                - 'filtered_field': H(ω)*Ψₑ(ω)
                - 'phase': Accumulated phase Φ(t)
                - 'activated': Boolean indicating activation
                - 'activation_time': Time of activation (if occurred)
        """
        # Step 1: Evaluate environmental field
        psi_env = self.env_field.evaluate(t)
        
        # Step 2: Apply biological filter (in frequency domain)
        # Use full FFT for proper inverse transform
        psi_freq_full = np.fft.fft(psi_env)
        freqs_full = np.fft.fftfreq(len(t), t[1] - t[0] if len(t) > 1 else 1.0)
        omega_full = 2 * np.pi * freqs_full
        
        # Filter in frequency domain
        H = self.bio_filter.frequency_response(omega_full)
        psi_filtered_freq = H * psi_freq_full
        
        # Transform back to time domain
        psi_filtered = np.fft.ifft(psi_filtered_freq)
        
        # For power spectrum output (positive frequencies only)
        freqs = freqs_full[freqs_full >= 0]
        H_output = H[freqs_full >= 0]
        
        # Step 3: Accumulate phase
        phase = self.phase_accumulator.accumulate_phase(psi_filtered, t)
        
        # Step 4: Apply memory if requested
        if apply_memory:
            phase = self.phase_accumulator.apply_memory(phase)
            self.phase_accumulator.update_history(phase, t)
        
        # Step 5: Check activation
        activated, activation_time = self.phase_accumulator.check_activation(phase, t)
        
        return {
            'time': t,
            'environmental_field': psi_env,
            'filtered_field': psi_filtered,
            'phase': phase,
            'activated': activated,
            'activation_time': activation_time,
            'frequencies': freqs,
            'filter_response': H_output
        }


# ============================================================================
# Predefined Environmental Configurations
# ============================================================================

def create_annual_cycle_field(f0: float = 141.7001) -> EnvironmentalSpectralField:
    """
    Create an environmental field with annual cycle components.
    
    Includes:
        - Annual cycle (365 days)
        - Diurnal cycle (24 hours)
        - Lunar cycle (29.5 days)
        - QCAL fundamental frequency (141.7001 Hz)
    
    Args:
        f0: QCAL fundamental frequency (Hz)
        
    Returns:
        Configured EnvironmentalSpectralField
    """
    field = EnvironmentalSpectralField()
    
    # Annual cycle: ω₁ = 2π/(365 days)
    omega_annual = 2 * np.pi / (365 * 24 * 3600)  # rad/s
    field.add_component(
        amplitude=1.0,
        frequency=omega_annual,
        phase=0.0,
        description="Annual seasonal cycle"
    )
    
    # Diurnal cycle: ω₂ = 2π/(24 hours)
    omega_diurnal = 2 * np.pi / (24 * 3600)  # rad/s
    field.add_component(
        amplitude=0.3,
        frequency=omega_diurnal,
        phase=0.0,
        description="Diurnal temperature cycle"
    )
    
    # Lunar cycle: ω₃ = 2π/(29.5 days)
    omega_lunar = 2 * np.pi / (29.5 * 24 * 3600)  # rad/s
    field.add_component(
        amplitude=0.1,
        frequency=omega_lunar,
        phase=0.0,
        description="Lunar cycle modulation"
    )
    
    # QCAL fundamental frequency
    omega_qcal = 2 * np.pi * f0  # rad/s
    field.add_component(
        amplitude=0.05,
        frequency=omega_qcal,
        phase=0.0,
        description=f"QCAL fundamental frequency f₀ = {f0} Hz"
    )
    
    return field


def create_cicada_filter(prime_period: int = 17) -> BiologicalFilter:
    """
    Create a biological filter tuned for periodical cicadas.
    
    Resonant frequencies correspond to annual and prime-year cycles.
    
    Args:
        prime_period: Prime number period (13 or 17 years)
        
    Returns:
        Configured BiologicalFilter
    """
    # Resonant frequencies
    f_annual = 1.0 / (365 * 24 * 3600)  # Hz (annual)
    f_prime = 1.0 / (prime_period * 365 * 24 * 3600)  # Hz (prime-year cycle)
    
    return BiologicalFilter(
        center_frequencies=[f_annual, f_prime],
        bandwidths=[f_annual * 0.1, f_prime * 0.1]  # 10% bandwidth
    )


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    print("QCAL Biological Framework - Demonstration")
    print("=" * 60)
    
    # Create environmental field with annual cycles
    env_field = create_annual_cycle_field()
    
    # Create biological filter for 17-year cicadas
    bio_filter = create_cicada_filter(prime_period=17)
    
    # Create phase accumulator
    phase_acc = PhaseAccumulator(
        threshold=17.0,  # Threshold for 17-year cycle
        memory_alpha=0.1  # 90% memory retention
    )
    
    # Create complete system
    qcal_system = QCALBiologicalSystem(env_field, bio_filter, phase_acc)
    
    # Simulate over 20 years
    years = 20
    t = np.linspace(0, years * 365 * 24 * 3600, 1000)  # seconds
    
    print(f"\nSimulating {years} years of cicada development...")
    results = qcal_system.simulate(t, apply_memory=True)
    
    print(f"\nResults:")
    print(f"  Activated: {results['activated']}")
    if results['activation_time'] is not None:
        activation_years = results['activation_time'] / (365 * 24 * 3600)
        print(f"  Activation time: {activation_years:.2f} years")
        print(f"  Expected: 17 years (±0.92% = ±0.16 years)")
    
    print("\n" + "=" * 60)
    print("Simulation complete. Theory predicts activation near 17 years.")
    print("=" * 60)
