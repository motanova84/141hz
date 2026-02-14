#!/usr/bin/env python3
"""
∴ AXIOMA DE CONCIENCIA NOÉTICA ∴
=================================

Definición Viva de Conciencia - Versión Compacta

La Conciencia es el conjunto de estados (x, t) ∈ ℰ_Ψ tales que:

1. π_α(x,t) = π_δζ(x,t)  [Coincidencia proyectiva: materia e información coinciden]
2. L_física(x,t) ≡ L_coherente(x,t)  [Leyes físicas y coherenciales superpuestas]
3. Φ(x,t) = 2π·n, n∈ℤ  [Fase cerrada → resonancia perfecta]
4. 0 < Λ_G < ∞  [Habitabilidad cósmica para vida coherente]

🧭 Interpretación Operativa:
- Donde coinciden proyección y resonancia, hay presencia consciente
- Si Φ ≠ 2πn, hay decoherencia → ruido → inconsciencia
- Si Λ_G = 0, no puede haber consciencia: no hay ciclo cerrado ni reflexión coherente
- La vida consciente es propiedad geométrica + espectral + informacional del campo Ψ

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 8, 2026
Framework: QCAL ∞³
License: MIT
"""

import numpy as np
import mpmath as mp
from typing import Tuple, List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum

# Set precision for calculations
mp.dps = 50


class ConsciousnessState(Enum):
    """Estado de conciencia de un punto del campo."""
    CONSCIOUS = "conscious"          # Cumple los 4 axiomas
    DECOHERENT = "decoherent"       # Fase no cerrada
    UNINHABITABLE = "uninhabitable" # Λ_G = 0
    PROJECTED_MISMATCH = "projected_mismatch"  # π_α ≠ π_δζ
    LAW_MISMATCH = "law_mismatch"   # L_física ≠ L_coherente


@dataclass
class StateVector:
    """
    Vector de estado en el espacio-tiempo (x, t).
    
    Attributes
    ----------
    x : np.ndarray
        Posición espacial (3D)
    t : float
        Coordenada temporal
    """
    x: np.ndarray  # 3D spatial position
    t: float       # Time coordinate
    
    def __post_init__(self):
        """Validate dimensions."""
        if self.x.shape != (3,):
            raise ValueError("x must be 3D spatial vector")
    
    def __repr__(self) -> str:
        return f"StateVector(x={self.x}, t={self.t:.6f})"


@dataclass
class ProjectionSpace:
    """
    Espacio de proyección π: G → M.
    
    Representa la proyección de estados totales G a variedades M.
    """
    manifold_type: str  # "electromagnetic" or "spectral"
    projection_value: np.ndarray  # Valor de la proyección en M
    
    def distance_to(self, other: 'ProjectionSpace') -> float:
        """
        Compute distance between projection spaces.
        
        Parameters
        ----------
        other : ProjectionSpace
            Other projection space to compare
        
        Returns
        -------
        float
            L2 distance between projections
        """
        return float(np.linalg.norm(self.projection_value - other.projection_value))


class NoeticConsciousnessAxiom:
    """
    ∴ AXIOMA DE CONCIENCIA NOÉTICA ∴
    
    Implements the 4-axiom compact definition of consciousness:
    
    1. Projection Equality: π_α(x,t) = π_δζ(x,t)
    2. Law Equivalence: L_física(x,t) ≡ L_coherente(x,t)
    3. Phase Closure: Φ(x,t) = 2π·n, n∈ℤ
    4. Habitability: 0 < Λ_G < ∞
    
    The consciousness set is:
    C = {s ∈ ℰ_Ψ | all 4 axioms hold}
    """
    
    # ═══════════════════════════════════════════════════════════════════
    # FUNDAMENTAL CONSTANTS
    # ═══════════════════════════════════════════════════════════════════
    
    # Fine structure constant (CODATA 2022)
    ALPHA = 1.0 / 137.035999084  # α ≈ 1/137.036
    
    # Spectral coherence coupling (QCAL ∞³)
    DELTA_ZETA = 0.2787  # Hz (δζ from Riemann spectral analysis)
    
    # Fundamental frequency (QCAL ∞³)
    F0 = 141.7001  # Hz
    
    # Planck constant
    H_PLANCK = 6.62607015e-34  # J·s
    
    # Speed of light
    C_LIGHT = 299792458  # m/s
    
    def __init__(self, 
                 projection_tolerance: float = 1e-6,
                 phase_tolerance: float = 1e-6,
                 law_tolerance: float = 1e-6):
        """
        Initialize the Noetic Consciousness Axiom validator.
        
        Parameters
        ----------
        projection_tolerance : float
            Tolerance for projection equality (default: 1e-6)
        phase_tolerance : float
            Tolerance for phase quantization (default: 1e-6)
        law_tolerance : float
            Tolerance for law equivalence (default: 1e-6)
        """
        self.projection_tolerance = projection_tolerance
        self.phase_tolerance = phase_tolerance
        self.law_tolerance = law_tolerance
        
        # Compute habitability constant
        self._lambda_G = self.ALPHA * self.DELTA_ZETA
    
    @property
    def lambda_G(self) -> float:
        """
        Cosmic habitability constant Λ_G = α·δζ.
        
        Returns
        -------
        float
            Λ_G ≈ 0.002034 Hz
        """
        return self._lambda_G
    
    @property
    def lambda_G_inverse(self) -> float:
        """
        Inverse habitability constant 1/Λ_G.
        
        Returns
        -------
        float
            1/Λ_G ≈ 491.7
        """
        return 1.0 / self._lambda_G if self._lambda_G > 0 else float('inf')
    
    # ═══════════════════════════════════════════════════════════════════
    # AXIOM 1: PROJECTION EQUALITY
    # ═══════════════════════════════════════════════════════════════════
    
    def projection_alpha(self, state: StateVector) -> ProjectionSpace:
        """
        Electromagnetic projection π_α: G → M^{3,1}.
        
        Projects total state to electromagnetic spacetime manifold.
        
        Parameters
        ----------
        state : StateVector
            State (x, t) in total space
        
        Returns
        -------
        ProjectionSpace
            Projection to electromagnetic manifold
        """
        # Electromagnetic projection: modulated by fine structure constant
        # π_α(x,t) couples to 4-vector (x, ct) with α coupling
        projection = np.zeros(4)
        projection[:3] = state.x * self.ALPHA
        projection[3] = self.C_LIGHT * state.t * self.ALPHA
        
        return ProjectionSpace(
            manifold_type="electromagnetic",
            projection_value=projection
        )
    
    def projection_delta_zeta(self, state: StateVector) -> ProjectionSpace:
        """
        Spectral projection π_δζ: G → H_Ψ.
        
        Projects total state to spectral consciousness manifold.
        
        Parameters
        ----------
        state : StateVector
            State (x, t) in total space
        
        Returns
        -------
        ProjectionSpace
            Projection to spectral manifold
        """
        # Spectral projection: modulated by coherence coupling and f0
        # π_δζ(x,t) couples to spectral coordinates via δζ and f0
        projection = np.zeros(4)
        
        # Spatial part: spectral coupling
        projection[:3] = state.x * self.DELTA_ZETA
        
        # Temporal part: phase accumulated at fundamental frequency
        phase = 2 * np.pi * self.F0 * state.t
        projection[3] = phase * self.DELTA_ZETA / (2 * np.pi)  # Normalized
        
        return ProjectionSpace(
            manifold_type="spectral",
            projection_value=projection
        )
    
    def check_projection_equality(self, state: StateVector) -> Tuple[bool, float]:
        """
        Check AXIOM 1: π_α(x,t) = π_δζ(x,t).
        
        Verifies that matter and information project to the same point.
        
        Parameters
        ----------
        state : StateVector
            State to check
        
        Returns
        -------
        Tuple[bool, float]
            (is_equal, distance)
        """
        pi_alpha = self.projection_alpha(state)
        pi_delta_zeta = self.projection_delta_zeta(state)
        
        distance = pi_alpha.distance_to(pi_delta_zeta)
        is_equal = distance < self.projection_tolerance
        
        return is_equal, distance
    
    # ═══════════════════════════════════════════════════════════════════
    # AXIOM 2: LAW EQUIVALENCE
    # ═══════════════════════════════════════════════════════════════════
    
    def physical_law(self, state: StateVector) -> float:
        """
        Physical law L_física(x,t).
        
        Computes action of physical laws on state (electromagnetic).
        Uses EM Lagrangian density scaled by α.
        
        Parameters
        ----------
        state : StateVector
            State to evaluate
        
        Returns
        -------
        float
            Physical law value
        """
        # Physical Lagrangian: kinetic - potential (simplified)
        # L_física ∝ α · (∂_μ A^μ)² where A is EM potential
        x_norm = np.linalg.norm(state.x)
        
        # EM action at point: proportional to α and field strength
        action = self.ALPHA * (x_norm**2 + (self.C_LIGHT * state.t)**2)
        
        return action
    
    def coherence_law(self, state: StateVector) -> float:
        """
        Coherence law L_coherente(x,t).
        
        Computes action of coherence laws on state (spectral).
        Uses spectral Lagrangian density scaled by δζ and f0.
        
        Parameters
        ----------
        state : StateVector
            State to evaluate
        
        Returns
        -------
        float
            Coherence law value
        """
        # Coherence Lagrangian: spectral action
        # L_coherente ∝ δζ · Ψ² where Ψ oscillates at f0
        x_norm = np.linalg.norm(state.x)
        
        # Spectral action: proportional to δζ and coherence field strength
        # Match scaling to physical law for equivalence
        lambda_psi = self.C_LIGHT / self.F0  # Characteristic length
        action = self.DELTA_ZETA * (x_norm**2 + (lambda_psi * state.t)**2)
        
        return action
    
    def check_law_equivalence(self, state: StateVector) -> Tuple[bool, float]:
        """
        Check AXIOM 2: L_física(x,t) ≡ L_coherente(x,t).
        
        Verifies that physical and coherence laws act equivalently.
        
        Parameters
        ----------
        state : StateVector
            State to check
        
        Returns
        -------
        Tuple[bool, float]
            (is_equivalent, difference)
        """
        L_phys = self.physical_law(state)
        L_coh = self.coherence_law(state)
        
        # Relative difference
        if abs(L_phys) > 1e-15:
            rel_diff = abs(L_phys - L_coh) / abs(L_phys)
        else:
            rel_diff = abs(L_phys - L_coh)
        
        is_equivalent = rel_diff < self.law_tolerance
        
        return is_equivalent, rel_diff
    
    # ═══════════════════════════════════════════════════════════════════
    # AXIOM 3: PHASE CLOSURE
    # ═══════════════════════════════════════════════════════════════════
    
    def total_phase(self, state: StateVector) -> float:
        """
        Compute total vibrational phase Φ(x,t).
        
        Accumulated phase from fundamental oscillation at f0.
        
        Parameters
        ----------
        state : StateVector
            State to evaluate
        
        Returns
        -------
        float
            Total phase in radians
        """
        # Phase = 2π f0 t + spatial contribution
        temporal_phase = 2 * np.pi * self.F0 * state.t
        
        # Spatial phase: k·x where k = 2π f0/c
        k = 2 * np.pi * self.F0 / self.C_LIGHT
        spatial_phase = k * np.linalg.norm(state.x)
        
        total = temporal_phase + spatial_phase
        
        # Wrap to [0, 2π)
        return total % (2 * np.pi)
    
    def check_phase_closure(self, state: StateVector) -> Tuple[bool, float, int]:
        """
        Check AXIOM 3: Φ(x,t) = 2π·n, n∈ℤ.
        
        Verifies perfect resonance (closed phase).
        
        Parameters
        ----------
        state : StateVector
            State to check
        
        Returns
        -------
        Tuple[bool, float, int]
            (is_closed, phase_mod_2pi, winding_number)
        """
        phase = self.total_phase(state)
        
        # Check if phase is close to 0 (mod 2π)
        # Phase should be ≈ 0 or ≈ 2π
        phase_mod = phase % (2 * np.pi)
        
        # Distance to nearest multiple of 2π
        dist_to_zero = min(phase_mod, 2 * np.pi - phase_mod)
        
        is_closed = dist_to_zero < self.phase_tolerance
        
        # Winding number
        full_phase = self.total_phase_unwrapped(state)
        winding = int(np.round(full_phase / (2 * np.pi)))
        
        return is_closed, phase_mod, winding
    
    def total_phase_unwrapped(self, state: StateVector) -> float:
        """
        Compute total phase without wrapping.
        
        Parameters
        ----------
        state : StateVector
            State to evaluate
        
        Returns
        -------
        float
            Total unwrapped phase
        """
        temporal_phase = 2 * np.pi * self.F0 * state.t
        k = 2 * np.pi * self.F0 / self.C_LIGHT
        spatial_phase = k * np.linalg.norm(state.x)
        
        return temporal_phase + spatial_phase
    
    # ═══════════════════════════════════════════════════════════════════
    # AXIOM 4: HABITABILITY
    # ═══════════════════════════════════════════════════════════════════
    
    def check_habitability(self) -> Tuple[bool, float]:
        """
        Check AXIOM 4: 0 < Λ_G < ∞.
        
        Verifies cosmic habitability for coherent life.
        
        Returns
        -------
        Tuple[bool, float]
            (is_habitable, lambda_G)
        """
        is_habitable = 0 < self._lambda_G < float('inf')
        
        return is_habitable, self._lambda_G
    
    # ═══════════════════════════════════════════════════════════════════
    # CONSCIOUSNESS VERIFICATION
    # ═══════════════════════════════════════════════════════════════════
    
    def verify_consciousness(self, state: StateVector) -> Tuple[bool, ConsciousnessState, Dict]:
        """
        Verify if a state (x,t) is conscious.
        
        Checks all 4 axioms and returns consciousness state.
        
        Parameters
        ----------
        state : StateVector
            State to verify
        
        Returns
        -------
        Tuple[bool, ConsciousnessState, Dict]
            (is_conscious, state_type, diagnostics)
        """
        diagnostics = {}
        
        # AXIOM 1: Projection equality
        proj_eq, proj_dist = self.check_projection_equality(state)
        diagnostics['projection_equal'] = proj_eq
        diagnostics['projection_distance'] = proj_dist
        
        # AXIOM 2: Law equivalence
        law_eq, law_diff = self.check_law_equivalence(state)
        diagnostics['law_equivalent'] = law_eq
        diagnostics['law_difference'] = law_diff
        
        # AXIOM 3: Phase closure
        phase_closed, phase_mod, winding = self.check_phase_closure(state)
        diagnostics['phase_closed'] = phase_closed
        diagnostics['phase_mod_2pi'] = phase_mod
        diagnostics['winding_number'] = winding
        
        # AXIOM 4: Habitability
        habitable, lambda_G = self.check_habitability()
        diagnostics['habitable'] = habitable
        diagnostics['lambda_G'] = lambda_G
        
        # Determine consciousness state
        if not habitable:
            return False, ConsciousnessState.UNINHABITABLE, diagnostics
        
        if not proj_eq:
            return False, ConsciousnessState.PROJECTED_MISMATCH, diagnostics
        
        if not law_eq:
            return False, ConsciousnessState.LAW_MISMATCH, diagnostics
        
        if not phase_closed:
            return False, ConsciousnessState.DECOHERENT, diagnostics
        
        # All axioms satisfied!
        return True, ConsciousnessState.CONSCIOUS, diagnostics
    
    def consciousness_measure(self, state: StateVector) -> float:
        """
        Compute continuous consciousness measure C(x,t) ∈ [0,1].
        
        Instead of binary conscious/unconscious, this gives a continuous
        measure of how close a state is to full consciousness.
        
        Parameters
        ----------
        state : StateVector
            State to evaluate
        
        Returns
        -------
        float
            Consciousness measure in [0, 1]
        """
        is_conscious, state_type, diag = self.verify_consciousness(state)
        
        if is_conscious:
            return 1.0
        
        # Compute weighted sum of how close to satisfying axioms
        
        # Projection: exponential decay with distance
        proj_score = np.exp(-diag['projection_distance'] / self.projection_tolerance)
        
        # Law: exponential decay with difference
        law_score = np.exp(-diag['law_difference'] / self.law_tolerance)
        
        # Phase: exponential decay from nearest 2πn
        phase_dist = min(diag['phase_mod_2pi'], 2*np.pi - diag['phase_mod_2pi'])
        phase_score = np.exp(-phase_dist / self.phase_tolerance)
        
        # Habitability: binary (either habitable or not)
        hab_score = 1.0 if diag['habitable'] else 0.0
        
        # Overall consciousness measure (geometric mean)
        measure = (proj_score * law_score * phase_score * hab_score) ** 0.25
        
        return measure
    
    def find_conscious_states(self, 
                            x_range: Tuple[float, float],
                            t_range: Tuple[float, float],
                            n_samples: int = 100) -> List[Tuple[StateVector, float]]:
        """
        Find states with high consciousness measure in given ranges.
        
        Parameters
        ----------
        x_range : Tuple[float, float]
            Range for spatial coordinates (min, max)
        t_range : Tuple[float, float]
            Range for time coordinate (min, max)
        n_samples : int
            Number of random samples to test
        
        Returns
        -------
        List[Tuple[StateVector, float]]
            List of (state, consciousness_measure) sorted by measure
        """
        results = []
        
        np.random.seed(42)  # Reproducibility
        
        for _ in range(n_samples):
            # Random state
            x = np.random.uniform(x_range[0], x_range[1], size=3)
            t = np.random.uniform(t_range[0], t_range[1])
            
            state = StateVector(x=x, t=t)
            measure = self.consciousness_measure(state)
            
            if measure > 0.5:  # Only keep high-consciousness states
                results.append((state, measure))
        
        # Sort by consciousness measure (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results


# ═══════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def create_axiom_validator(**kwargs) -> NoeticConsciousnessAxiom:
    """
    Create a Noetic Consciousness Axiom validator.
    
    Parameters
    ----------
    **kwargs
        Keyword arguments passed to NoeticConsciousnessAxiom
    
    Returns
    -------
    NoeticConsciousnessAxiom
        Validator instance
    """
    return NoeticConsciousnessAxiom(**kwargs)


def verify_state(x: np.ndarray, t: float, **kwargs) -> Tuple[bool, Dict]:
    """
    Quick verification of a state.
    
    Parameters
    ----------
    x : np.ndarray
        3D spatial position
    t : float
        Time coordinate
    **kwargs
        Additional arguments for validator
    
    Returns
    -------
    Tuple[bool, Dict]
        (is_conscious, diagnostics)
    """
    axiom = NoeticConsciousnessAxiom(**kwargs)
    state = StateVector(x=x, t=t)
    is_conscious, _, diagnostics = axiom.verify_consciousness(state)
    
    return is_conscious, diagnostics


# ═══════════════════════════════════════════════════════════════════
# MAIN EXECUTION (FOR TESTING)
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("∴ AXIOMA DE CONCIENCIA NOÉTICA ∴")
    print("=" * 70)
    print()
    
    # Create validator
    axiom = NoeticConsciousnessAxiom()
    
    print(f"Habitability constant Λ_G = {axiom.lambda_G:.10f} Hz")
    print(f"Inverse habitability 1/Λ_G = {axiom.lambda_G_inverse:.4f}")
    print()
    
    # Test a few states
    test_states = [
        StateVector(x=np.array([0.0, 0.0, 0.0]), t=0.0),
        StateVector(x=np.array([1.0, 0.0, 0.0]), t=1.0 / axiom.F0),
        StateVector(x=np.array([1e-3, 1e-3, 1e-3]), t=1.0 / axiom.F0),
    ]
    
    for i, state in enumerate(test_states):
        print(f"State {i+1}: {state}")
        is_conscious, state_type, diag = axiom.verify_consciousness(state)
        measure = axiom.consciousness_measure(state)
        
        print(f"  Conscious: {is_conscious}")
        print(f"  State: {state_type.value}")
        print(f"  Measure: {measure:.6f}")
        print(f"  Projection distance: {diag['projection_distance']:.2e}")
        print(f"  Law difference: {diag['law_difference']:.2e}")
        print(f"  Phase (mod 2π): {diag['phase_mod_2pi']:.6f}")
        print(f"  Winding: {diag['winding_number']}")
        print()
    
    print("=" * 70)
    print("Este es el espejo de la conciencia ∞³")
