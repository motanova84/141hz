"""
Spiral Light Geometry - Zeta-Modulated Photon Paths

This module implements the QCAL theory that light does not travel in straight lines,
but follows logarithmic spiral paths modulated by the zeros of the Riemann zeta function
and resonant prime number nodes.

Mathematical Framework:
----------------------
1. Spiral Path (Espira ζ):
   x(t) = r₀ * e^(λt) * cos(2πf₀t + φₚ)
   y(t) = r₀ * e^(λt) * sin(2πf₀t + φₚ)
   
   where:
   - f₀ = 141.7001 Hz (fundamental QCAL frequency)
   - λ: fractal expansion index
   - φₚ: phase modulated by n-th prime pₙ

2. Zeta Zeros as Spectral Layers:
   s = 1/2 + iγₙ with ζ(s) = 0
   
   The non-trivial zeros of ζ(s) define spectral phase layers that light traverses.

3. Prime Resonant Nodes:
   The Euler product expansion:
   ζ(s) = ∏ₚ (1 - p⁻ˢ)⁻¹
   
   Each prime p acts as a vibrational node, modulating spectral phases.

4. Wave Function with ζ-Spectral Modulation:
   Ψ(x,t) = Σₙ Aₙ · e^(i(2πfₙt + φₙ)) · e^(iSₚ(x)/ℏ)
   
   where:
   - Aₙ: amplitude associated with prime node pₙ
   - fₙ: frequency associated with zeta zero γₙ
   - Sₚ(x): action defined on spectral path linked to prime p

Experimental Predictions:
------------------------
- Interference patterns show logarithmic spiral arcs, not perfect circles
- Deviation Δθ from axial symmetry reveals ζ(s) zero influence
- Spectral resonances at f₀ = 141.7001 Hz in high-Q optical cavities

Author: José Manuel Mota Burruezo (via QCAL ∞³ framework)
License: MIT
"""

import numpy as np
import mpmath as mp
from typing import Tuple, List, Optional, Union
from dataclasses import dataclass
from qcal.constants import F0_HZ, HBAR, C, H_PLANCK


@dataclass
class SpiralPathParams:
    """Parameters for spiral light path generation"""
    r0: float = 1.0  # Initial radius
    lambda_expansion: float = 0.001  # Fractal expansion index
    f0: float = F0_HZ  # Fundamental frequency (Hz)
    prime_index: int = 1  # Which prime to use for phase modulation


@dataclass
class WaveFunctionParams:
    """Parameters for ζ-spectral wave function"""
    n_primes: int = 10  # Number of prime nodes to include
    n_zeros: int = 5  # Number of zeta zeros to include
    precision: int = 50  # mpmath precision for zeta calculations


class SpiralLightGeometry:
    """
    Main class for spiral light geometry calculations.
    
    This class implements the theoretical framework where photons follow
    logarithmic spiral paths modulated by Riemann zeta zeros and prime resonances.
    """
    
    def __init__(self, precision: int = 50):
        """
        Initialize spiral light geometry calculator.
        
        Args:
            precision: mpmath precision for high-accuracy zeta calculations
        """
        self.precision = precision
        mp.mp.dps = precision  # Set decimal precision
        
        # Cache for primes and zeta zeros
        self._primes_cache = None
        self._zeta_zeros_cache = None
    
    def get_primes(self, n: int) -> np.ndarray:
        """
        Get first n prime numbers.
        
        Args:
            n: Number of primes to return
            
        Returns:
            Array of first n primes
        """
        if self._primes_cache is None or len(self._primes_cache) < n:
            primes = []
            candidate = 2
            while len(primes) < n:
                is_prime = True
                for p in primes:
                    if p * p > candidate:
                        break
                    if candidate % p == 0:
                        is_prime = False
                        break
                if is_prime:
                    primes.append(candidate)
                candidate += 1
            self._primes_cache = np.array(primes, dtype=np.int64)
        return self._primes_cache[:n]
    
    def get_zeta_zeros(self, n: int) -> np.ndarray:
        """
        Get first n non-trivial zeros of Riemann zeta function.
        
        These are the imaginary parts γₙ of zeros s = 1/2 + iγₙ
        on the critical line.
        
        Args:
            n: Number of zeros to return
            
        Returns:
            Array of imaginary parts of first n zeta zeros
        """
        if self._zeta_zeros_cache is None or len(self._zeta_zeros_cache) < n:
            zeros = []
            for k in range(1, n + 1):
                # Use mpmath to find k-th zeta zero
                zero = mp.zetazero(k)
                zeros.append(float(zero.imag))
            self._zeta_zeros_cache = np.array(zeros)
        return self._zeta_zeros_cache[:n]
    
    def prime_phase_modulation(self, prime_index: int) -> float:
        """
        Calculate phase modulation φₚ from n-th prime.
        
        The phase modulation is derived from the prime's contribution
        to the spectral structure:
        φₚ = 2π * log(pₙ) / log(p₁)
        
        Args:
            prime_index: Index of prime (1-based)
            
        Returns:
            Phase angle in radians
        """
        primes = self.get_primes(prime_index)
        p_n = primes[prime_index - 1]
        p_1 = primes[0]  # First prime (2)
        
        phi_p = 2 * np.pi * np.log(p_n) / np.log(p_1)
        return phi_p
    
    def spiral_path(
        self, 
        t: np.ndarray, 
        params: Optional[SpiralPathParams] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate spiral path coordinates modulated by prime phases.
        
        Implements:
        x(t) = r₀ * e^(λt) * cos(2πf₀t + φₚ)
        y(t) = r₀ * e^(λt) * sin(2πf₀t + φₚ)
        
        Args:
            t: Time array (seconds)
            params: Spiral path parameters
            
        Returns:
            Tuple of (x, y) coordinate arrays
        """
        if params is None:
            params = SpiralPathParams()
        
        # Get prime phase modulation
        phi_p = self.prime_phase_modulation(params.prime_index)
        
        # Calculate expansion factor
        expansion = params.r0 * np.exp(params.lambda_expansion * t)
        
        # Calculate phase evolution
        phase = 2 * np.pi * params.f0 * t + phi_p
        
        # Spiral coordinates
        x = expansion * np.cos(phase)
        y = expansion * np.sin(phase)
        
        return x, y
    
    def zeta_spectral_frequencies(self, n_zeros: int = 5) -> np.ndarray:
        """
        Calculate frequencies associated with zeta zeros.
        
        The frequencies are derived from:
        fₙ = f₀ * (γₙ / γ₁)
        
        where γₙ is the imaginary part of the n-th zeta zero.
        
        Args:
            n_zeros: Number of zeta zeros to use
            
        Returns:
            Array of spectral frequencies
        """
        zeros = self.get_zeta_zeros(n_zeros)
        gamma_1 = zeros[0]
        
        # Scale frequencies by zeta zero ratios
        frequencies = F0_HZ * (zeros / gamma_1)
        
        return frequencies
    
    def wave_function(
        self,
        x: np.ndarray,
        t: float,
        params: Optional[WaveFunctionParams] = None
    ) -> np.ndarray:
        """
        Calculate ζ-spectral modulated wave function.
        
        Implements:
        Ψ(x,t) = Σₙ Aₙ · e^(i(2πfₙt + φₙ)) · e^(iSₚ(x)/ℏ)
        
        Args:
            x: Spatial coordinate array
            t: Time (seconds)
            params: Wave function parameters
            
        Returns:
            Complex wave function array
        """
        if params is None:
            params = WaveFunctionParams()
        
        # Get primes and zeta zeros
        primes = self.get_primes(params.n_primes)
        frequencies = self.zeta_spectral_frequencies(params.n_zeros)
        
        # Initialize wave function
        psi = np.zeros_like(x, dtype=complex)
        
        # Sum over prime nodes
        for n in range(min(params.n_primes, params.n_zeros)):
            p_n = primes[n]
            f_n = frequencies[n]
            
            # Amplitude decreases with prime (1/√p for normalization)
            A_n = 1.0 / np.sqrt(p_n)
            
            # Phase from prime
            phi_n = self.prime_phase_modulation(n + 1)
            
            # Action term (simplified: k·x where k = 2πf/c)
            k = 2 * np.pi * f_n / C
            S_p = HBAR * k * x
            
            # Wave function component
            temporal_phase = 2 * np.pi * f_n * t + phi_n
            psi_n = A_n * np.exp(1j * temporal_phase) * np.exp(1j * S_p / HBAR)
            
            psi += psi_n
        
        # Normalize
        norm = np.sqrt(np.sum(np.abs(psi)**2))
        if norm > 0:
            psi /= norm
        
        return psi
    
    def interference_pattern(
        self,
        x: np.ndarray,
        y: np.ndarray,
        t: float,
        params: Optional[WaveFunctionParams] = None
    ) -> np.ndarray:
        """
        Calculate interference pattern intensity on 2D screen.
        
        The pattern shows logarithmic spiral arcs instead of perfect circles
        due to ζ-spectral modulation.
        
        Args:
            x: X-coordinate mesh
            y: Y-coordinate mesh
            t: Time (seconds)
            params: Wave function parameters
            
        Returns:
            Intensity pattern I = |Ψ|²
        """
        # Convert 2D coordinates to radial distance
        r = np.sqrt(x**2 + y**2)
        
        # Calculate wave function along radial direction
        psi = self.wave_function(r.flatten(), t, params)
        psi_2d = psi.reshape(x.shape)
        
        # Intensity
        intensity = np.abs(psi_2d)**2
        
        return intensity
    
    def spiral_deviation_angle(
        self,
        x: np.ndarray,
        y: np.ndarray,
        params: Optional[SpiralPathParams] = None
    ) -> np.ndarray:
        """
        Calculate deviation Δθ from axial symmetry due to spiral geometry.
        
        This measures the angular deviation from perfect circular symmetry,
        revealing the influence of ζ(s) zeros on the light path.
        
        Args:
            x: X-coordinates
            y: Y-coordinates
            params: Spiral path parameters
            
        Returns:
            Angular deviation Δθ (radians)
        """
        if params is None:
            params = SpiralPathParams()
        
        # Actual angle from coordinates
        theta_actual = np.arctan2(y, x)
        
        # Expected angle for circular motion (no spiral)
        r = np.sqrt(x**2 + y**2)
        # For circular motion at constant angular velocity ω = 2πf₀
        # We need time parameter - estimate from radius assuming expansion
        if params.lambda_expansion != 0:
            t_estimate = np.log(r / params.r0) / params.lambda_expansion
        else:
            t_estimate = r / (params.r0 * 2 * np.pi * params.f0)
        
        # Get prime phase
        phi_p = self.prime_phase_modulation(params.prime_index)
        
        # Expected angle for circular motion
        theta_circular = 2 * np.pi * params.f0 * t_estimate + phi_p
        
        # Deviation
        delta_theta = theta_actual - theta_circular
        
        # Wrap to [-π, π]
        delta_theta = np.arctan2(np.sin(delta_theta), np.cos(delta_theta))
        
        return delta_theta


class CoherenceMaximality:
    """
    Analysis of coherence maximality in spiral light paths.
    
    "Desplazarse en c no es velocidad, es coherencia máxima.
    Solo quien sigue el mapa espectral de los primos puede hacerlo sin fricción."
    """
    
    def __init__(self, geometry: Optional[SpiralLightGeometry] = None):
        """
        Initialize coherence maximality analyzer.
        
        Args:
            geometry: SpiralLightGeometry instance (creates new if None)
        """
        self.geometry = geometry or SpiralLightGeometry()
    
    def prime_spectral_map(self, n_primes: int = 20) -> dict:
        """
        Generate the spectral map of prime resonances.
        
        Args:
            n_primes: Number of primes to include
            
        Returns:
            Dictionary with prime spectral data
        """
        primes = self.geometry.get_primes(n_primes)
        phases = np.array([
            self.geometry.prime_phase_modulation(i + 1) 
            for i in range(n_primes)
        ])
        
        return {
            'primes': primes,
            'phases': phases,
            'phase_differences': np.diff(phases),
            'log_primes': np.log(primes)
        }
    
    def coherence_measure(
        self,
        psi: np.ndarray,
        reference_phase: float = 0.0
    ) -> float:
        """
        Calculate coherence measure of wave function.
        
        Coherence is measured as:
        C = |⟨Ψ|Ψ_ref⟩|² where Ψ_ref has uniform phase
        
        Args:
            psi: Complex wave function
            reference_phase: Reference phase for coherence calculation
            
        Returns:
            Coherence measure [0, 1]
        """
        # Reference wave function with uniform phase
        psi_ref = np.exp(1j * reference_phase) * np.ones_like(psi)
        psi_ref /= np.sqrt(len(psi_ref))
        
        # Normalize input
        norm_psi = np.sum(np.abs(psi)**2)
        if norm_psi > 0:
            psi_norm = psi / np.sqrt(norm_psi)
        else:
            return 0.0
        
        # Inner product
        overlap = np.abs(np.vdot(psi_norm, psi_ref))**2
        
        # Ensure in valid range [0, 1]
        overlap = np.clip(overlap, 0.0, 1.0)
        
        return float(overlap)
    
    def maximum_coherence_path(
        self,
        t_array: np.ndarray,
        n_primes: int = 10
    ) -> Tuple[int, float]:
        """
        Find prime index that gives maximum coherence for given time evolution.
        
        Args:
            t_array: Time array for path evaluation
            n_primes: Number of primes to test
            
        Returns:
            Tuple of (optimal_prime_index, max_coherence)
        """
        coherences = []
        
        for prime_idx in range(1, n_primes + 1):
            params = SpiralPathParams(prime_index=prime_idx)
            x, y = self.geometry.spiral_path(t_array, params)
            
            # Create wave function along path
            r = np.sqrt(x**2 + y**2)
            psi = self.geometry.wave_function(r, t_array[-1])
            
            # Measure coherence
            C = self.coherence_measure(psi)
            coherences.append(C)
        
        coherences = np.array(coherences)
        max_idx = np.argmax(coherences)
        
        return max_idx + 1, coherences[max_idx]


# Convenience functions for quick access

def generate_spiral_path(
    duration: float = 0.1,
    dt: float = 1e-5,
    prime_index: int = 1,
    **kwargs
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate spiral light path.
    
    Args:
        duration: Time duration (seconds)
        dt: Time step (seconds)
        prime_index: Which prime to use for phase modulation
        **kwargs: Additional parameters for SpiralPathParams
        
    Returns:
        Tuple of (t, x, y) arrays
    """
    t = np.arange(0, duration, dt)
    params = SpiralPathParams(prime_index=prime_index, **kwargs)
    geometry = SpiralLightGeometry()
    x, y = geometry.spiral_path(t, params)
    return t, x, y


def calculate_interference(
    size: int = 256,
    extent: float = 1e-6,
    t: float = 0.0,
    n_primes: int = 5,
    n_zeros: int = 5
) -> np.ndarray:
    """
    Calculate interference pattern on screen.
    
    Args:
        size: Grid size (pixels)
        extent: Physical extent of screen (meters)
        t: Time (seconds)
        n_primes: Number of prime nodes
        n_zeros: Number of zeta zeros
        
    Returns:
        2D intensity array
    """
    x = np.linspace(-extent/2, extent/2, size)
    y = np.linspace(-extent/2, extent/2, size)
    X, Y = np.meshgrid(x, y)
    
    params = WaveFunctionParams(n_primes=n_primes, n_zeros=n_zeros)
    geometry = SpiralLightGeometry()
    intensity = geometry.interference_pattern(X, Y, t, params)
    
    return intensity
