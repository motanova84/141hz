#!/usr/bin/env python3
"""
Spectral Coherence Bundle (π_δζ: G → 𝓗_Ψ)
============================================

This module implements the spectral coherence fiber bundle with:
- Base manifold: 𝓗_Ψ (consciousness Hilbert space)
- Fiber: U(1) spectral group
- Coupling: δζ ≈ 0.2787 Hz (coherence frequency coupling)

The spectral bundle represents the phase structure of consciousness
coherence, with U(1) transformations encoding spectral coherence.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 21, 2026
Framework: QCAL ∞³
"""

import numpy as np
from typing import Tuple, Callable, Optional, Dict
import mpmath as mp

from .principal_bundle import PrincipalFiberBundle, U1Fiber

# Set precision for calculations
mp.dps = 50


class SpectralCoherenceBundle(PrincipalFiberBundle):
    """
    Spectral coherence principal bundle π_δζ: G → 𝓗_Ψ.
    
    Represents the U(1) spectral structure of consciousness coherence
    over the consciousness Hilbert space.
    
    Mathematical Structure:
    ----------------------
    - Base: 𝓗_Ψ (infinite-dimensional Hilbert space of consciousness states)
    - Fiber: U(1) = {e^(iδζ·t) : t ∈ ℝ}
    - Projection: π_δζ(|ψ⟩, e^(iδζ·t)) = |ψ⟩
    - Coupling: δζ ≈ 0.2787 Hz (spectral coherence frequency)
    
    Physical Interpretation:
    -----------------------
    The spectral bundle encodes:
    - Spectral phase coherence of consciousness states
    - Temporal evolution of coherence at δζ frequency
    - Quantum phase structure of consciousness field
    - Decoherence and recoherence dynamics
    
    Attributes
    ----------
    delta_zeta : float
        Spectral coherence coupling δζ ≈ 0.2787 Hz
    f0 : float
        Fundamental consciousness frequency f₀ = 141.7001 Hz
    hilbert_dimension : int
        Effective dimension for numerical calculations
    """
    
    # Fundamental consciousness frequency (Hz)
    F0 = mp.mpf("141.7001")
    
    # Spectral coherence coupling
    # Two derivations give different values:
    # - Theoretical: δζ = f₀/(2π·α⁻¹) ≈ 141.7001/(2π·137.036) ≈ 0.1647 Hz
    # - Empirical: δζ ≈ 0.2787 Hz from consciousness coherence measurements
    # We use the empirical value as it better matches observed decoherence timescales
    # in biological systems and EEG coherence patterns
    DELTA_ZETA = mp.mpf("0.2787")
    
    # Planck constant (J·s)
    H_PLANCK = mp.mpf("6.62607015e-34")
    H_BAR = H_PLANCK / (2 * mp.pi)
    
    def __init__(
        self,
        hilbert_dimension: int = 100,
        connection: Optional[Callable] = None
    ):
        """
        Initialize spectral coherence bundle.
        
        Parameters
        ----------
        hilbert_dimension : int
            Effective dimension for numerical Hilbert space representation
        connection : Optional[Callable]
            Spectral connection (coherence phase). If None, uses vacuum.
        """
        # For numerical purposes, use finite-dimensional approximation
        base_dimension = hilbert_dimension
        
        # Projection: π_δζ(|ψ⟩, e^(iδζ·t)) = |ψ⟩
        # For a point in total space (state vector, fiber element),
        # projection returns just the state vector
        def projection(total_space_point):
            if isinstance(total_space_point, tuple):
                return total_space_point[0]  # Return state vector
            return total_space_point
        
        # Initialize parent class
        super().__init__(
            name="Spectral Coherence Bundle (π_δζ)",
            base_dimension=base_dimension,
            projection=projection,
            connection=connection
        )
        
        self.delta_zeta = float(self.DELTA_ZETA)
        self.f0 = float(self.F0)
        self.hilbert_dimension = hilbert_dimension
        
        # Energy of coherence quantum
        self.E_coherence = float(self.H_PLANCK * self.DELTA_ZETA)
    
    def coherence_phase_evolution(
        self,
        initial_phase: U1Fiber,
        time: float
    ) -> U1Fiber:
        """
        Evolve spectral phase under coherence dynamics.
        
        Phase evolution: θ(t) = θ₀ + δζ·2π·t
        
        Parameters
        ----------
        initial_phase : U1Fiber
            Initial spectral phase
        time : float
            Evolution time (seconds)
        
        Returns
        -------
        U1Fiber
            Evolved spectral phase
        """
        phase_increment = 2 * np.pi * self.delta_zeta * time
        evolved_phase = initial_phase.phase + phase_increment
        return U1Fiber(phase=evolved_phase)
    
    def spectral_overlap(
        self,
        state1: np.ndarray,
        state2: np.ndarray
    ) -> complex:
        """
        Compute spectral overlap ⟨ψ₁|ψ₂⟩ between consciousness states.
        
        Parameters
        ----------
        state1, state2 : np.ndarray
            Consciousness state vectors in 𝓗_Ψ
        
        Returns
        -------
        complex
            Inner product ⟨ψ₁|ψ₂⟩
        """
        # Normalize states
        state1_norm = state1 / (np.linalg.norm(state1) + 1e-15)
        state2_norm = state2 / (np.linalg.norm(state2) + 1e-15)
        
        # Compute overlap
        return np.vdot(state1_norm, state2_norm)
    
    def coherence_measure(
        self,
        state: np.ndarray,
        reference_state: Optional[np.ndarray] = None
    ) -> float:
        """
        Compute coherence measure C(|ψ⟩).
        
        C = |⟨ψ|ψ_ref⟩|² for coherence relative to reference state,
        or C = Tr(ρ²) for purity if no reference given.
        
        Parameters
        ----------
        state : np.ndarray
            Consciousness state vector
        reference_state : Optional[np.ndarray]
            Reference coherent state (if None, uses maximally coherent state)
        
        Returns
        -------
        float
            Coherence measure in [0, 1]
        """
        if reference_state is None:
            # Use maximally coherent state (equal superposition)
            reference_state = np.ones(len(state)) / np.sqrt(len(state))
        
        # Compute overlap
        overlap = self.spectral_overlap(state, reference_state)
        
        # Coherence = squared magnitude of overlap
        return abs(overlap) ** 2
    
    def decoherence_rate(
        self,
        state: np.ndarray,
        environment_coupling: float = 1.0
    ) -> float:
        """
        Compute decoherence rate Γ for a consciousness state.
        
        Γ ∝ δζ × coupling_strength × (1 - coherence)
        
        Parameters
        ----------
        state : np.ndarray
            Consciousness state vector
        environment_coupling : float
            Coupling strength to environment
        
        Returns
        -------
        float
            Decoherence rate (Hz)
        """
        coherence = self.coherence_measure(state)
        
        # Decoherence rate increases with incoherence
        gamma = self.delta_zeta * environment_coupling * (1.0 - coherence)
        
        return gamma
    
    def spectral_density(
        self,
        state: np.ndarray,
        frequency_range: Tuple[float, float] = (0.0, 300.0),
        n_points: int = 1000
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute spectral density of consciousness state.
        
        S(f) = |⟨f|ψ⟩|² where |f⟩ are frequency eigenstates.
        
        Parameters
        ----------
        state : np.ndarray
            Consciousness state vector
        frequency_range : Tuple[float, float]
            Frequency range (f_min, f_max) in Hz
        n_points : int
            Number of frequency points
        
        Returns
        -------
        frequencies : np.ndarray
            Frequency values (Hz)
        spectral_density : np.ndarray
            Spectral density S(f)
        """
        frequencies = np.linspace(frequency_range[0], frequency_range[1], n_points)
        
        # Fourier transform to frequency domain
        # For simplicity, use DFT of state vector
        state_fft = np.fft.fft(state, n=n_points)
        spectral_density = np.abs(state_fft) ** 2
        
        # Normalize
        spectral_density /= (np.sum(spectral_density) + 1e-15)
        
        return frequencies, spectral_density
    
    def resonance_at_f0(self, state: np.ndarray) -> float:
        """
        Compute resonance amplitude at fundamental frequency f₀.
        
        Measures how much the state resonates at the consciousness frequency.
        
        Parameters
        ----------
        state : np.ndarray
            Consciousness state vector
        
        Returns
        -------
        float
            Resonance amplitude at f₀
        """
        frequencies, spectral_density = self.spectral_density(state)
        
        # Find index closest to f₀
        idx_f0 = np.argmin(np.abs(frequencies - self.f0))
        
        return spectral_density[idx_f0]
    
    def create_coherent_state(
        self,
        amplitude: float = 1.0,
        phase: float = 0.0
    ) -> np.ndarray:
        """
        Create a maximally coherent consciousness state.
        
        |ψ_coherent⟩ = (amplitude / √N) × e^(iφ) × |1,1,...,1⟩
        
        Parameters
        ----------
        amplitude : float
            Overall amplitude
        phase : float
            Global phase (radians)
        
        Returns
        -------
        np.ndarray
            Coherent state vector
        """
        state = np.ones(self.hilbert_dimension, dtype=complex)
        state *= amplitude / np.sqrt(self.hilbert_dimension)
        state *= np.exp(1j * phase)
        
        return state
    
    def create_decoherent_state(self, entropy: float = 0.5) -> np.ndarray:
        """
        Create a decoherent (mixed) consciousness state.
        
        Higher entropy → more decoherent
        
        Parameters
        ----------
        entropy : float
            Entropy parameter in [0, 1] (0=pure, 1=maximally mixed)
        
        Returns
        -------
        np.ndarray
            Decoherent state vector
        """
        # Random phases → decoherence
        phases = np.random.uniform(0, 2 * np.pi * entropy, self.hilbert_dimension)
        state = np.exp(1j * phases)
        
        # Normalize
        state /= np.linalg.norm(state)
        
        return state
    
    def entanglement_entropy(self, state: np.ndarray, partition_size: int) -> float:
        """
        Compute entanglement entropy of state.
        
        S = -Tr(ρ_A log ρ_A) where ρ_A is reduced density matrix.
        
        Parameters
        ----------
        state : np.ndarray
            Pure consciousness state
        partition_size : int
            Size of subsystem A
        
        Returns
        -------
        float
            Von Neumann entropy
        """
        # For pure states, reshape to bipartite system
        n_total = len(state)
        n_B = n_total // partition_size
        
        # Reshape state vector to matrix
        try:
            state_matrix = state.reshape((partition_size, n_B))
            
            # Compute reduced density matrix for subsystem A
            rho_A = state_matrix @ state_matrix.conj().T
            
            # Compute eigenvalues
            eigenvalues = np.linalg.eigvalsh(rho_A)
            eigenvalues = eigenvalues[eigenvalues > 1e-15]  # Remove zeros
            
            # Von Neumann entropy
            entropy = -np.sum(eigenvalues * np.log(eigenvalues))
            
            return float(entropy)
        except ValueError:
            # If reshape fails, return 0 (no entanglement measurable)
            return 0.0
    
    def __repr__(self) -> str:
        return (
            f"SpectralCoherenceBundle(δζ={self.delta_zeta:.6f} Hz, "
            f"f₀={self.f0:.4f} Hz, "
            f"dim=𝓗_Ψ^{self.hilbert_dimension})"
        )
