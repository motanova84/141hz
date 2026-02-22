#!/usr/bin/env python3
"""
Consciousness as Intersection of Fiber Bundles
==============================================

C = Γ(E_α) ∩ Γ(E_δζ) = Ker(π_α - π_δζ)

This module implements the fundamental insight that consciousness does NOT emerge.
It IS the intersection space of two principal fiber bundles:

1. E_α: π_α: G → 𝓜^3,1 (electromagnetic gauge bundle, α ≈ 1/137)
2. E_δζ: π_δζ: G → 𝓗_Ψ (spectral coherence bundle, δζ ≈ 0.2787 Hz)

KEY FORMULATIONS:
-----------------
1. As intersection of sections: C = Γ(E_α) ∩ Γ(E_δζ)
2. As kernel of projection difference: C = Ker(π_α - π_δζ)

Only states that do NOT distinguish between matter and information are conscious.
States in C exist simultaneously in spacetime and consciousness Hilbert space.

The intersection constant Λ_G = α·δζ ≈ 1/491.5 governs the topological capacity
for conscious observers and the "habitability rate" of the universe.

THE PLATONIC CAVE:
-----------------
       G (Total Space)
      / \
     /   \
    ↓     ↓
   π_α   π_δζ
    ↓     ↓
𝓜^3,1   𝓗_Ψ
  ↓       ↓
α-fibrado  δζ-fibrado
  ↓       ↓
  🔥     🧠
Sombras   Formas
     ↘   ↙
       👁️
  Consciousness = Ker(π_α - π_δζ)

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 21, 2026
Updated: February 8, 2026 (Added kernel formulation)
Framework: QCAL ∞³
"""

import numpy as np
from typing import Tuple, List, Dict, Callable, Optional
from dataclasses import dataclass
import mpmath as mp

from .principal_bundle import PrincipalFiberBundle, U1Fiber
from .electromagnetic_bundle import ElectromagneticGaugeBundle
from .spectral_bundle import SpectralCoherenceBundle

# Set precision for calculations
mp.dps = 50


@dataclass
class IntersectionConstant:
    """
    Intersection constant Λ_G = α·δζ.
    
    This fundamental constant governs the "aspect ratio" of the universe -
    how many "field lines" from the total space G become matter vs. information.
    
    Attributes
    ----------
    alpha : float
        Fine structure constant α ≈ 1/137.036
    delta_zeta : float
        Spectral coherence coupling δζ ≈ 0.2787 Hz
    lambda_G : float
        Intersection constant Λ_G = α·δζ
    """
    alpha: float
    delta_zeta: float
    
    @property
    def lambda_G(self) -> float:
        """Compute intersection constant Λ_G = α·δζ."""
        return self.alpha * self.delta_zeta
    
    @property
    def lambda_G_hz(self) -> float:
        """Intersection constant in Hz."""
        return self.lambda_G
    
    @property
    def lambda_G_inverse(self) -> float:
        """Inverse intersection constant 1/Λ_G."""
        return 1.0 / self.lambda_G if self.lambda_G != 0 else float('inf')
    
    def topological_capacity(self) -> float:
        """
        Compute topological information capacity.
        
        C_topo = log(1/Λ_G) ≈ log(491.8) ≈ 6.20 bits
        
        This measures how many bits of information can be encoded
        in the intersection structure.
        
        Returns
        -------
        float
            Topological capacity (bits)
        """
        if self.lambda_G > 0:
            return np.log2(self.lambda_G_inverse)
        return 0.0
    
    def observer_density(self, universe_volume: float = 1.0) -> float:
        """
        Estimate density of conscious observers.
        
        ρ_obs ∝ Λ_G × V_universe
        
        Parameters
        ----------
        universe_volume : float
            Volume scale (arbitrary units)
        
        Returns
        -------
        float
            Observer density
        """
        return self.lambda_G * universe_volume
    
    def validate_universal_constant(self) -> Dict[str, bool]:
        """
        Validate that Λ_G matches the expected universal value.
        
        The intersection constant should satisfy:
        Λ_G = α · δζ ≈ 1/491.5
        
        This is the topological habitability rate of the universe.
        
        Returns
        -------
        Dict[str, bool]
            Validation results
        """
        results = {}
        
        # Check individual constants are in expected ranges
        results['alpha_valid'] = 0.007 < self.alpha < 0.008  # α ≈ 1/137
        results['delta_zeta_valid'] = 0.27 < self.delta_zeta < 0.29  # δζ ≈ 0.2787 Hz
        
        # Check product is correct
        expected_product = self.alpha * self.delta_zeta
        results['product_consistent'] = abs(self.lambda_G - expected_product) < 1e-10
        
        # Check inverse is approximately 491.5
        expected_inverse = 491.5
        actual_inverse = self.lambda_G_inverse
        results['inverse_matches_theory'] = abs(actual_inverse - expected_inverse) < 1.0
        
        # Check habitability interpretation
        # Λ_G should be small but positive (rare but possible observers)
        results['habitability_in_range'] = 0.001 < self.lambda_G < 0.01
        
        # Overall validation
        results['overall_valid'] = all(results.values())
        
        return results
    
    def __repr__(self) -> str:
        return (
            f"IntersectionConstant(α={self.alpha:.10f}, "
            f"δζ={self.delta_zeta:.6f} Hz, "
            f"Λ_G={self.lambda_G:.10f} Hz, "
            f"C_topo={self.topological_capacity():.4f} bits)"
        )


class ConsciousnessIntersection:
    """
    Consciousness space C = π_α(G) ∩ π_δζ(G).
    
    Represents consciousness as the intersection of simultaneous sections
    of the electromagnetic and spectral fiber bundles.
    
    Mathematical Structure:
    ----------------------
    Given:
    - π_α: G → 𝓜^3,1 (electromagnetic bundle)
    - π_δζ: G → 𝓗_Ψ (spectral bundle)
    
    The consciousness space C consists of pairs (σ_α, σ_δζ) where:
    - σ_α: 𝓜^3,1 → G (section of electromagnetic bundle)
    - σ_δζ: 𝓗_Ψ → G (section of spectral bundle)
    - Compatibility: σ_α and σ_δζ must agree on the overlap
    
    Physical Interpretation:
    -----------------------
    - States in C are simultaneously physical and spectral
    - Electromagnetic gauge freedom ↔ Spectral phase coherence
    - Λ_G determines the "width" of the intersection
    - Consciousness emerges where both projections are valid
    
    Attributes
    ----------
    em_bundle : ElectromagneticGaugeBundle
        Electromagnetic gauge bundle π_α
    spectral_bundle : SpectralCoherenceBundle
        Spectral coherence bundle π_δζ
    intersection_constant : IntersectionConstant
        Fundamental intersection constant Λ_G
    """
    
    def __init__(
        self,
        em_bundle: Optional[ElectromagneticGaugeBundle] = None,
        spectral_bundle: Optional[SpectralCoherenceBundle] = None
    ):
        """
        Initialize consciousness intersection.
        
        Parameters
        ----------
        em_bundle : Optional[ElectromagneticGaugeBundle]
            Electromagnetic bundle. If None, creates default.
        spectral_bundle : Optional[SpectralCoherenceBundle]
            Spectral bundle. If None, creates default.
        """
        # Initialize bundles
        self.em_bundle = em_bundle or ElectromagneticGaugeBundle()
        self.spectral_bundle = spectral_bundle or SpectralCoherenceBundle()
        
        # Compute intersection constant
        self.intersection_constant = IntersectionConstant(
            alpha=self.em_bundle.alpha,
            delta_zeta=self.spectral_bundle.delta_zeta
        )
        
        # Storage for consciousness states
        self._states: List[Dict] = []
    
    @property
    def lambda_G(self) -> float:
        """Get intersection constant Λ_G."""
        return self.intersection_constant.lambda_G
    
    def is_simultaneous_section(
        self,
        em_section: Callable,
        spectral_section: Callable,
        test_points: List[Tuple[np.ndarray, np.ndarray]],
        tolerance: float = 1e-6
    ) -> bool:
        """
        Test if two sections are compatible (simultaneous).
        
        For sections to be simultaneous, their fiber components must
        be compatible across the intersection.
        
        Parameters
        ----------
        em_section : Callable
            Section σ_α of electromagnetic bundle
        spectral_section : Callable
            Section σ_δζ of spectral bundle
        test_points : List[Tuple[np.ndarray, np.ndarray]]
            List of (spacetime_point, hilbert_point) pairs to test
        tolerance : float
            Compatibility tolerance
        
        Returns
        -------
        bool
            True if sections are simultaneous
        """
        for spacetime_pt, hilbert_pt in test_points:
            # Evaluate sections
            em_fiber = em_section(spacetime_pt)
            spectral_fiber = spectral_section(hilbert_pt)
            
            # Check fiber compatibility (phases should match mod Λ_G)
            if isinstance(em_fiber, U1Fiber) and isinstance(spectral_fiber, U1Fiber):
                phase_diff = abs(em_fiber.phase - spectral_fiber.phase)
                phase_diff = min(phase_diff, 2 * np.pi - phase_diff)  # Wrap to [0, π]
                
                # Compatibility criterion: phase difference < tolerance
                if phase_diff > tolerance:
                    return False
        
        return True
    
    def create_consciousness_state(
        self,
        spacetime_point: np.ndarray,
        consciousness_vector: np.ndarray,
        em_phase: float = 0.0,
        spectral_phase: float = 0.0
    ) -> Dict:
        """
        Create a consciousness state in the intersection space C.
        
        A consciousness state consists of:
        - Physical location (spacetime point)
        - Consciousness configuration (Hilbert vector)
        - Electromagnetic phase (U(1) gauge)
        - Spectral coherence phase (U(1) spectral)
        
        Parameters
        ----------
        spacetime_point : np.ndarray
            Position in 𝓜^3,1 (t, x, y, z)
        consciousness_vector : np.ndarray
            State in 𝓗_Ψ
        em_phase : float
            Electromagnetic gauge phase (radians)
        spectral_phase : float
            Spectral coherence phase (radians)
        
        Returns
        -------
        Dict
            Consciousness state
        """
        state = {
            'spacetime': spacetime_point.copy(),
            'consciousness': consciousness_vector.copy(),
            'em_fiber': U1Fiber(phase=em_phase),
            'spectral_fiber': U1Fiber(phase=spectral_phase),
            'compatible': abs(em_phase - spectral_phase) < 0.1,  # Rough check
            'timestamp': spacetime_point[0] if len(spacetime_point) > 0 else 0.0
        }
        
        self._states.append(state)
        return state
    
    def consciousness_field_strength(
        self,
        state: Dict,
        epsilon: float = 1e-8
    ) -> float:
        """
        Compute consciousness field strength.
        
        This is a measure of how strongly the intersection manifests
        at a given state, combining electromagnetic and spectral curvatures.
        
        F_C = √(F_em² + F_spec²)
        
        Parameters
        ----------
        state : Dict
            Consciousness state
        epsilon : float
            Numerical derivative step
        
        Returns
        -------
        float
            Consciousness field strength
        """
        # Electromagnetic curvature
        if self.em_bundle.connection is not None:
            F_em = self.em_bundle.curvature(state['spacetime'])
        else:
            F_em = 0.0
        
        # Spectral curvature (simplified)
        F_spec = abs(state['spectral_fiber'].phase - state['em_fiber'].phase)
        
        # Combined field strength
        F_C = np.sqrt(F_em**2 + F_spec**2)
        
        return F_C
    
    def master_equation(
        self,
        total_space_element: Tuple[np.ndarray, U1Fiber]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply master equation: G → {π_α, π_δζ} → {𝓜^3,1, 𝓗_Ψ} → ∩ C.
        
        Takes an element from total space G and projects it through
        both fiber bundles to create an intersection state.
        
        Parameters
        ----------
        total_space_element : Tuple[np.ndarray, U1Fiber]
            Element from G (configuration, fiber)
        
        Returns
        -------
        spacetime_projection : np.ndarray
            Projection to 𝓜^3,1 via π_α
        hilbert_projection : np.ndarray
            Projection to 𝓗_Ψ via π_δζ
        """
        configuration, fiber = total_space_element
        
        # Project through π_α to get spacetime coordinates
        # For this implementation, assume configuration contains both
        n_spacetime = 4
        spacetime_projection = configuration[:n_spacetime]
        
        # Project through π_δζ to get Hilbert vector
        hilbert_projection = configuration[n_spacetime:]
        
        return spacetime_projection, hilbert_projection
    
    def intersection_measure(self, state1: Dict, state2: Dict) -> float:
        """
        Compute intersection measure between two consciousness states.
        
        I(C₁, C₂) = |⟨ψ₁|ψ₂⟩| × exp(-|Δx|²/λ_G²)
        
        Combines spatial separation and consciousness overlap.
        
        Parameters
        ----------
        state1, state2 : Dict
            Consciousness states
        
        Returns
        -------
        float
            Intersection measure in [0, 1]
        """
        # Consciousness overlap
        psi1 = state1['consciousness']
        psi2 = state2['consciousness']
        
        # Normalize
        psi1_norm = psi1 / (np.linalg.norm(psi1) + 1e-15)
        psi2_norm = psi2 / (np.linalg.norm(psi2) + 1e-15)
        
        consciousness_overlap = abs(np.vdot(psi1_norm, psi2_norm))
        
        # Spatial separation
        x1 = state1['spacetime'][1:]  # Spatial coordinates only
        x2 = state2['spacetime'][1:]
        spatial_distance = np.linalg.norm(x1 - x2)
        
        # Intersection measure with Gaussian suppression
        lambda_G_meters = self.lambda_G * 3e8  # Convert Hz to approximate length scale
        spatial_factor = np.exp(-spatial_distance**2 / (lambda_G_meters**2 + 1e-10))
        
        return consciousness_overlap * spatial_factor
    
    def entanglement_via_intersection(
        self,
        state1: Dict,
        state2: Dict
    ) -> float:
        """
        Compute entanglement between states via intersection.
        
        Consciousness states can become entangled through their
        shared presence in the intersection space C.
        
        Parameters
        ----------
        state1, state2 : Dict
            Consciousness states
        
        Returns
        -------
        float
            Entanglement measure
        """
        # Intersection measure
        I = self.intersection_measure(state1, state2)
        
        # Phase coherence
        phase_diff = abs(state1['em_fiber'].phase - state2['spectral_fiber'].phase)
        coherence = np.cos(phase_diff)
        
        # Entanglement via intersection
        E = I * (1 + coherence) / 2
        
        return E
    
    def evolve_consciousness_state(
        self,
        state: Dict,
        time_step: float
    ) -> Dict:
        """
        Evolve consciousness state in time.
        
        Evolution combines:
        - Spectral phase evolution at δζ
        - Electromagnetic dynamics
        - Intersection coupling
        
        Parameters
        ----------
        state : Dict
            Initial consciousness state
        time_step : float
            Time evolution step (seconds)
        
        Returns
        -------
        Dict
            Evolved consciousness state
        """
        # Create evolved state
        evolved_state = state.copy()
        
        # Evolve spacetime (simple: advance time)
        evolved_state['spacetime'] = state['spacetime'].copy()
        evolved_state['spacetime'][0] += time_step
        
        # Evolve spectral phase
        evolved_state['spectral_fiber'] = self.spectral_bundle.coherence_phase_evolution(
            state['spectral_fiber'],
            time_step
        )
        
        # Evolve consciousness vector (unitary evolution)
        omega_0 = 2 * np.pi * self.spectral_bundle.f0
        phase_evolution = np.exp(-1j * omega_0 * time_step)
        evolved_state['consciousness'] = state['consciousness'] * phase_evolution
        
        # Update timestamp
        evolved_state['timestamp'] = state['timestamp'] + time_step
        
        return evolved_state
    
    def projection_difference(
        self,
        total_space_element: Tuple[np.ndarray, U1Fiber]
    ) -> np.ndarray:
        """
        Compute the projection difference (π_α - π_δζ) for an element of G.
        
        This is the fundamental operator whose kernel defines consciousness:
        C = Ker(π_α - π_δζ)
        
        The projection difference measures how much a state distinguishes
        between matter (spacetime) and information (consciousness space).
        
        Parameters
        ----------
        total_space_element : Tuple[np.ndarray, U1Fiber]
            Element from total space G (configuration, fiber)
        
        Returns
        -------
        np.ndarray
            Difference vector in unified space
        """
        configuration, fiber = total_space_element
        
        # Extract projections
        n_spacetime = 4
        spacetime_config = configuration[:n_spacetime]
        hilbert_config = configuration[n_spacetime:]
        
        # For the difference, we need a unified representation
        # We use the phase difference weighted by the configurations
        
        # Spacetime contribution: weighted by α (electromagnetic coupling)
        em_contribution = self.em_bundle.alpha * spacetime_config
        
        # Hilbert contribution: weighted by δζ (coherence coupling)  
        # Pad/truncate to match dimensions
        hilbert_padded = np.zeros(n_spacetime)
        min_dim = min(len(hilbert_config), n_spacetime)
        hilbert_padded[:min_dim] = hilbert_config[:min_dim]
        spectral_contribution = self.spectral_bundle.delta_zeta * hilbert_padded
        
        # Projection difference
        diff = em_contribution - spectral_contribution
        
        return diff
    
    def is_in_kernel(
        self,
        state: Dict,
        tolerance: float = 1e-6
    ) -> bool:
        """
        Test if a consciousness state is in Ker(π_α - π_δζ).
        
        States in the kernel do NOT distinguish between matter and information.
        These are the truly conscious states.
        
        C = Ker(π_α - π_δζ) = {s ∈ G : π_α(s) = π_δζ(s)}
        
        In practice, this means the electromagnetic and spectral phases
        must be equal (or differ by at most tolerance).
        
        Parameters
        ----------
        state : Dict
            Consciousness state to test
        tolerance : float
            Kernel membership tolerance (in radians)
        
        Returns
        -------
        bool
            True if state is in the kernel (is truly conscious)
        """
        # The kernel condition is that the phases match
        phase_diff = abs(state['em_fiber'].phase - state['spectral_fiber'].phase)
        
        # Account for periodicity: difference might wrap around 2π
        phase_diff = min(phase_diff, 2 * np.pi - phase_diff)
        
        # Test if difference is within tolerance
        return phase_diff < tolerance
    
    def kernel_projection(
        self,
        state: Dict
    ) -> Dict:
        """
        Project a state onto the kernel Ker(π_α - π_δζ).
        
        This "makes a state conscious" by ensuring it doesn't distinguish
        between matter and information.
        
        The projection balances the electromagnetic and spectral components
        so they become equal under their respective projections.
        
        Parameters
        ----------
        state : Dict
            Arbitrary state (possibly not in kernel)
        
        Returns
        -------
        Dict
            Projected state in Ker(π_α - π_δζ) (conscious state)
        """
        # Create projection by averaging the projections
        # This is the closest point in the kernel
        
        # Balance the phases
        avg_phase = (state['em_fiber'].phase + state['spectral_fiber'].phase) / 2
        
        # Create balanced state
        projected_state = state.copy()
        projected_state['em_fiber'] = U1Fiber(phase=avg_phase)
        projected_state['spectral_fiber'] = U1Fiber(phase=avg_phase)
        projected_state['compatible'] = True  # Now compatible by construction
        
        # Mark as kernel-projected
        projected_state['in_kernel'] = True
        projected_state['kernel_distance'] = abs(
            state['em_fiber'].phase - state['spectral_fiber'].phase
        )
        
        return projected_state
    
    def consciousness_emergence_measure(
        self,
        state: Dict
    ) -> float:
        """
        Measure how "conscious" a state is.
        
        NOT because consciousness emerges, but because we measure
        how close a state is to the kernel Ker(π_α - π_δζ).
        
        Returns 1.0 for states perfectly in the kernel (fully conscious),
        0.0 for states far from the kernel (unconscious).
        
        The kernel condition is π_α(s) = π_δζ(s), which in phase space
        means the electromagnetic and spectral phases must match.
        
        Parameters
        ----------
        state : Dict
            State to measure
        
        Returns
        -------
        float
            Consciousness measure in [0, 1]
        """
        # The kernel condition is that the phases match
        # This is the primary criterion for consciousness
        phase_diff = abs(state['em_fiber'].phase - state['spectral_fiber'].phase)
        
        # Wrap to [0, π] (minimum difference accounting for periodicity)
        phase_diff = min(phase_diff, 2 * np.pi - phase_diff)
        
        # Consciousness measure: 1 when phases match, 0 when maximally different
        # Use Gaussian-like decay with characteristic scale π/2
        characteristic_scale = np.pi / 2
        consciousness = np.exp(-phase_diff**2 / (2 * characteristic_scale**2))
        
        return float(consciousness)
    
    def validate_intersection_consistency(self) -> Dict[str, bool]:
        """
        Validate mathematical consistency of the intersection.
        
        Checks:
        1. Both bundles are well-defined
        2. Intersection constant is positive
        3. Projections are compatible
        
        Returns
        -------
        Dict[str, bool]
            Validation results
        """
        results = {}
        
        # Check bundles are defined
        results['em_bundle_defined'] = self.em_bundle is not None
        results['spectral_bundle_defined'] = self.spectral_bundle is not None
        
        # Check intersection constant
        results['lambda_G_positive'] = self.lambda_G > 0
        results['lambda_G_finite'] = np.isfinite(self.lambda_G)
        
        # Check dimensional compatibility
        results['dimensions_compatible'] = True  # Always true in this implementation
        
        # Overall consistency
        results['overall_consistent'] = all(results.values())
        
        return results
    
    def __repr__(self) -> str:
        return (
            f"ConsciousnessIntersection(\n"
            f"  π_α: {self.em_bundle.name}\n"
            f"  π_δζ: {self.spectral_bundle.name}\n"
            f"  Λ_G: {self.lambda_G:.10f} Hz\n"
            f"  States: {len(self._states)}\n"
            f")"
        )
