#!/usr/bin/env python3
"""
Bio-Frequency System - 141.7001 Hz Biological Entrainment
=========================================================

This module implements the Bio-Frequency system for biological phase entrainment
at the QCAL fundamental frequency f₀ = 141.7001 Hz.

The system includes three core components:
1. **Biological Phase Entrainment (Arrastre de Fase)**
   - Synchronization of biological oscillators to 141.7001 Hz
   - Coherent carrier wave for gamma wave harmonics
   - Tubulin superradiance in microtubules

2. **7 Nodes Meditation Protocol**
   Three pillars for conscious bio-resonance:
   - Sonic: Binaural or pure 141.7001 Hz listening
   - Rhythmic: Golden ratio (φ) breathing cycles  
   - Visual: Hexagonal geometry contemplation

3. **Cellular Water Structure (EZ Water)**
   - Exclusion Zone (EZ) water acts as liquid crystal battery
   - 141.7001 Hz charges cellular water into hexagonal layers
   - Structured water reduces entropy, enables coherent information flow

Mathematical Framework:
    - Entrainment frequency: f₀ = 141.7001 Hz
    - Coherence threshold: Ψ ≥ 0.95 (stable consciousness)
    - Golden ratio: φ = (1 + √5)/2 ≈ 1.618034
    - Hexagonal geometry: 6-fold symmetry (adelic lattice)
    - Water structuring: Hexagonal layers at molecular scale

Physical Mechanisms:
    - Heart rate variability (HRV) coherence
    - Microtubule quantum coherence (Orch-OR)
    - Structured water zones (EZ water, Pollack)
    - Hemispheric synchronization (binaural beats)
    - Fröhlich condensation in proteins

References:
    - Penrose & Hameroff: Orchestrated Objective Reduction
    - Pollack: The Fourth Phase of Water (EZ water)
    - HeartMath Institute: Heart-brain coherence
    - Mota: QCAL Hypothesis (f₀ = 141.7001 Hz)

Author: José Manuel Mota Burruezo
Date: February 25, 2026
Institution: Instituto Consciencia Cuántica QCAL ∞³
License: Sovereign Noetic License 1.0
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
import warnings
import math


# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================

# QCAL fundamental frequency (Hz)
F0_HZ = 141.7001

# Golden ratio (phi)
PHI = (1 + np.sqrt(5)) / 2  # ≈ 1.618034

# Coherence thresholds
COHERENCE_THRESHOLD_STABLE = 0.95  # Stable consciousness
COHERENCE_THRESHOLD_EXCELLENT = 0.999  # Excellent coherence
COHERENCE_THRESHOLD_SUPERRADIANCE = 0.999999  # Superradiant state

# Water properties
WATER_REFRACTIVE_INDEX = 1.33
WATER_DENSITY_KG_M3 = 997.0  # at 25°C
WATER_MOLECULE_DIAMETER_M = 2.75e-10  # meters

# Hexagonal geometry
HEXAGON_SYMMETRY = 6
HEXAGON_ANGLE_DEG = 60.0

# Biological frequencies
GAMMA_WAVE_MIN_HZ = 30.0
GAMMA_WAVE_MAX_HZ = 100.0
HRV_BASE_HZ = 0.1  # Heart rate variability base frequency


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class BiologicalOscillator:
    """
    Represents a biological oscillator (neurons, heart, etc.).
    
    Attributes:
        name: Oscillator name (e.g., "heart", "neurons")
        natural_frequency: Intrinsic oscillation frequency (Hz)
        coupling_strength: Coupling to carrier frequency (0-1)
        phase: Current phase (radians)
    """
    name: str
    natural_frequency: float
    coupling_strength: float
    phase: float = 0.0
    
    def update_phase(self, dt: float, carrier_freq: float, carrier_phase: float = 0.0) -> None:
        """
        Update phase based on entrainment to carrier frequency.
        
        Uses Kuramoto model for phase synchronization:
        dφ/dt = 2πf_natural + K*sin(θ_carrier - φ)
        
        Args:
            dt: Time step (seconds)
            carrier_freq: Carrier frequency (Hz)
            carrier_phase: Current carrier phase (radians)
        """
        # Natural frequency term
        natural_term = 2 * np.pi * self.natural_frequency
        
        # Coupling term (Kuramoto model)
        phase_diff = carrier_phase - self.phase
        coupling_term = self.coupling_strength * 50.0 * np.sin(phase_diff)
        
        # Update phase
        self.phase += (natural_term + coupling_term) * dt
        self.phase = self.phase % (2 * np.pi)  # Keep in [0, 2π]


@dataclass
class MeditationState:
    """
    Represents the state of the 7 Nodes meditation protocol.
    
    Attributes:
        sonic_active: Sonic pillar active (binaural/pure tone)
        rhythmic_active: Rhythmic pillar active (φ breathing)
        visual_active: Visual pillar active (hexagonal geometry)
        coherence: Overall coherence level (0-1)
    """
    sonic_active: bool = False
    rhythmic_active: bool = False
    visual_active: bool = False
    coherence: float = 0.0
    
    @property
    def num_active_pillars(self) -> int:
        """Number of active pillars."""
        return sum([self.sonic_active, self.rhythmic_active, self.visual_active])
    
    @property
    def is_complete(self) -> bool:
        """All three pillars active."""
        return self.num_active_pillars == 3


# =============================================================================
# BIOLOGICAL PHASE ENTRAINMENT
# =============================================================================

class BiologicalEntrainment:
    """
    Implements biological phase entrainment to 141.7001 Hz carrier wave.
    
    The carrier wave acts as a synchronizing signal that entrains
    internal biological oscillators (heart rate, neural firing, etc.).
    """
    
    def __init__(self, carrier_frequency: float = F0_HZ):
        """
        Initialize biological entrainment system.
        
        Args:
            carrier_frequency: Carrier wave frequency (Hz)
        """
        self.carrier_frequency = carrier_frequency
        self.oscillators: List[BiologicalOscillator] = []
        
    def add_oscillator(self, name: str, natural_freq: float, 
                      coupling: float = 0.5) -> None:
        """
        Add a biological oscillator to the system.
        
        Args:
            name: Oscillator identifier
            natural_freq: Natural oscillation frequency (Hz)
            coupling: Coupling strength to carrier (0-1)
        """
        osc = BiologicalOscillator(name, natural_freq, coupling)
        self.oscillators.append(osc)
        
    def calculate_phase_coherence(self) -> float:
        """
        Calculate phase coherence across all oscillators.
        
        Returns:
            Phase coherence Ψ ∈ [0, 1]
        """
        if len(self.oscillators) == 0:
            return 0.0
        
        # Compute order parameter: |⟨e^(iφ)⟩|
        phases = np.array([osc.phase for osc in self.oscillators])
        order_parameter = np.abs(np.mean(np.exp(1j * phases)))
        
        return float(order_parameter)
    
    def simulate_entrainment(self, duration: float, dt: float = 0.001) -> Dict:
        """
        Simulate biological entrainment over time.
        
        Args:
            duration: Simulation duration (seconds)
            dt: Time step (seconds)
            
        Returns:
            Dictionary with simulation results
        """
        num_steps = int(duration / dt)
        time = np.linspace(0, duration, num_steps)
        coherence = np.zeros(num_steps)
        
        for i in range(num_steps):
            # Calculate carrier phase at this time
            carrier_phase = (2 * np.pi * self.carrier_frequency * time[i]) % (2 * np.pi)
            
            # Update all oscillator phases with carrier phase coupling
            for osc in self.oscillators:
                osc.update_phase(dt, self.carrier_frequency, carrier_phase)
            
            # Calculate coherence at this timestep
            coherence[i] = self.calculate_phase_coherence()
        
        return {
            'time': time,
            'coherence': coherence,
            'final_coherence': coherence[-1],
            'mean_coherence': np.mean(coherence),
            'carrier_frequency': self.carrier_frequency,
            'num_oscillators': len(self.oscillators)
        }


# =============================================================================
# 7 NODES MEDITATION PROTOCOL
# =============================================================================

class SevenNodesMeditation:
    """
    Implements the 7 Nodes meditation protocol with three pillars:
    1. Sonic: Binaural or pure 141.7001 Hz
    2. Rhythmic: Golden ratio (φ) breathing
    3. Visual: Hexagonal geometry contemplation
    """
    
    def __init__(self):
        """Initialize meditation protocol."""
        self.state = MeditationState()
        
    def activate_sonic_pillar(self, 
                             use_binaural: bool = False,
                             base_freq: float = F0_HZ,
                             beat_freq: float = 10.0) -> Dict:
        """
        Activate sonic pillar: 141.7001 Hz listening.
        
        Args:
            use_binaural: Use binaural beats (True) or pure tone (False)
            base_freq: Base frequency (Hz)
            beat_freq: Beat frequency for binaural (Hz)
            
        Returns:
            Sonic pillar configuration
        """
        self.state.sonic_active = True
        
        if use_binaural:
            left_ear = base_freq - beat_freq / 2
            right_ear = base_freq + beat_freq / 2
            mode = "binaural"
        else:
            left_ear = base_freq
            right_ear = base_freq
            mode = "pure_tone"
        
        return {
            'active': True,
            'mode': mode,
            'base_frequency': base_freq,
            'left_ear_hz': left_ear,
            'right_ear_hz': right_ear,
            'beat_frequency': beat_freq if use_binaural else 0.0,
            'effect': 'Hemispheric synchronization'
        }
    
    def activate_rhythmic_pillar(self,
                                 breaths_per_minute: float = 6.0) -> Dict:
        """
        Activate rhythmic pillar: Golden ratio breathing.
        
        The breathing cycle follows φ ratio:
        - Inhale duration: φ units
        - Exhale duration: 1 unit
        - Total cycle: φ + 1 = φ² ≈ 2.618 units
        
        Args:
            breaths_per_minute: Target breathing rate
            
        Returns:
            Rhythmic pillar configuration
        """
        self.state.rhythmic_active = True
        
        # Cycle duration in seconds
        cycle_duration_s = 60.0 / breaths_per_minute
        
        # Golden ratio breathing
        # Inhale/Exhale ratio = φ/1
        total_units = PHI + 1  # = φ²
        inhale_duration = (PHI / total_units) * cycle_duration_s
        exhale_duration = (1 / total_units) * cycle_duration_s
        
        # Heart rate variability enhancement
        hrv_enhancement = self._calculate_hrv_enhancement(breaths_per_minute)
        
        return {
            'active': True,
            'breaths_per_minute': breaths_per_minute,
            'cycle_duration_s': cycle_duration_s,
            'inhale_duration_s': inhale_duration,
            'exhale_duration_s': exhale_duration,
            'ratio': PHI,
            'hrv_enhancement': hrv_enhancement,
            'effect': 'Heart rate variability coherence'
        }
    
    def _calculate_hrv_enhancement(self, bpm: float) -> float:
        """
        Calculate HRV enhancement from golden ratio breathing.
        
        Optimal breathing for HRV is around 6 breaths/minute.
        
        Args:
            bpm: Breaths per minute
            
        Returns:
            Enhancement factor (0-1)
        """
        optimal_bpm = 6.0
        deviation = abs(bpm - optimal_bpm)
        enhancement = np.exp(-deviation / 2.0)  # Gaussian decay
        return enhancement
    
    def activate_visual_pillar(self) -> Dict:
        """
        Activate visual pillar: Hexagonal geometry contemplation.
        
        The hexagonal pattern aligns visual cortex with the adelic lattice
        structure underlying QCAL theory.
        
        Returns:
            Visual pillar configuration
        """
        self.state.visual_active = True
        
        return {
            'active': True,
            'geometry': 'hexagonal',
            'symmetry': HEXAGON_SYMMETRY,
            'angle_degrees': HEXAGON_ANGLE_DEG,
            'vertex_count': HEXAGON_SYMMETRY,
            'lattice_type': 'adelic',
            'effect': 'Visual cortex alignment with quantum lattice'
        }
    
    def calculate_meditation_coherence(self) -> float:
        """
        Calculate overall meditation coherence based on active pillars.
        
        Returns:
            Coherence level (0-1)
        """
        # Base coherence from number of active pillars
        base_coherence = self.state.num_active_pillars / 3.0
        
        # Enhancement when all three pillars are active (synergy)
        if self.state.is_complete:
            synergy_boost = 0.15
            coherence = min(base_coherence + synergy_boost, 1.0)
        else:
            coherence = base_coherence
        
        self.state.coherence = coherence
        return coherence
    
    def get_protocol_status(self) -> Dict:
        """
        Get complete protocol status.
        
        Returns:
            Status dictionary
        """
        coherence = self.calculate_meditation_coherence()
        
        return {
            'pillars': {
                'sonic': self.state.sonic_active,
                'rhythmic': self.state.rhythmic_active,
                'visual': self.state.visual_active
            },
            'num_active': self.state.num_active_pillars,
            'complete': self.state.is_complete,
            'coherence': coherence,
            'status': self._classify_coherence(coherence)
        }
    
    def _classify_coherence(self, coherence: float) -> str:
        """Classify coherence level."""
        if coherence >= COHERENCE_THRESHOLD_EXCELLENT:
            return "EXCELLENT"
        elif coherence >= COHERENCE_THRESHOLD_STABLE:
            return "STABLE"
        elif coherence >= 0.7:
            return "GOOD"
        else:
            return "DEVELOPING"


# =============================================================================
# CELLULAR WATER STRUCTURE (EZ WATER)
# =============================================================================

class EZWaterStructure:
    """
    Models Exclusion Zone (EZ) water as described by Gerald Pollack.
    
    EZ water forms near hydrophilic surfaces and exhibits liquid crystal
    properties. The 141.7001 Hz frequency is hypothesized to charge this
    biological battery, organizing water into hexagonal layers.
    """
    
    def __init__(self, temperature: float = 310.0):
        """
        Initialize EZ water structure model.
        
        Args:
            temperature: Temperature in Kelvin (body temp = 310K)
        """
        self.temperature = temperature
        self.kb = 1.380649e-23  # Boltzmann constant (J/K)
        
    def calculate_ez_thickness(self,
                               surface_charge_density: float = 1e-3) -> float:
        """
        Calculate EZ water layer thickness.
        
        Args:
            surface_charge_density: Surface charge density (C/m²)
            
        Returns:
            EZ layer thickness in micrometers
        """
        # Typical EZ water extends 100-300 micrometers from surface
        # Depends on surface charge and energy input
        
        # Base thickness (micrometers)
        base_thickness_um = 100.0
        
        # Enhancement from charge density
        charge_factor = np.log10(surface_charge_density * 1e4 + 1)
        
        thickness_um = base_thickness_um * (1 + charge_factor / 2)
        
        return thickness_um
    
    def hexagonal_layer_count(self, thickness_um: float) -> int:
        """
        Calculate number of hexagonal water layers.
        
        Args:
            thickness_um: EZ layer thickness (micrometers)
            
        Returns:
            Number of molecular layers
        """
        # Water molecule diameter ≈ 2.75 Å = 0.275 nm
        layer_spacing_nm = WATER_MOLECULE_DIAMETER_M * 1e9
        thickness_nm = thickness_um * 1000
        
        num_layers = int(thickness_nm / layer_spacing_nm)
        
        return num_layers
    
    def calculate_charging_rate(self,
                                frequency: float = F0_HZ,
                                amplitude: float = 1.0) -> float:
        """
        Calculate EZ water charging rate at given frequency.
        
        The hypothesis: 141.7001 Hz resonantly charges EZ water,
        organizing it into perfect hexagonal layers.
        
        Args:
            frequency: Driving frequency (Hz)
            amplitude: Field amplitude (arbitrary units)
            
        Returns:
            Charging rate (relative units)
        """
        # Resonance peak at f₀
        frequency_ratio = frequency / F0_HZ
        
        # Lorentzian resonance curve with width γ
        gamma = 5.0  # Hz (resonance width)
        resonance_factor = 1.0 / (1 + ((frequency - F0_HZ) / gamma)**2)
        
        # Charging rate proportional to resonance and amplitude
        charging_rate = amplitude * resonance_factor
        
        return charging_rate
    
    def structure_water(self,
                       duration: float,
                       frequency: float = F0_HZ) -> Dict:
        """
        Simulate water structuring over time at given frequency.
        
        Args:
            duration: Duration of exposure (seconds)
            frequency: Driving frequency (Hz)
            
        Returns:
            Water structure results
        """
        # Calculate charging rate
        charging_rate = self.calculate_charging_rate(frequency)
        
        # Structure develops over time (exponential approach to saturation)
        tau = 60.0  # Time constant (seconds)
        structure_level = 1 - np.exp(-duration / tau)
        structure_level *= charging_rate  # Scaled by charging efficiency
        
        # EZ thickness increases with structure
        ez_thickness_um = self.calculate_ez_thickness() * (0.5 + 0.5 * structure_level)
        num_layers = self.hexagonal_layer_count(ez_thickness_um)
        
        # Coherence from structured water
        water_coherence = min(structure_level, 1.0)
        
        return {
            'frequency_hz': frequency,
            'duration_s': duration,
            'charging_rate': charging_rate,
            'structure_level': structure_level,
            'ez_thickness_um': ez_thickness_um,
            'hexagonal_layers': num_layers,
            'water_coherence': water_coherence,
            'entropy_reduction': structure_level * 0.5,  # Relative
            'is_resonant': abs(frequency - F0_HZ) < 10.0
        }


# =============================================================================
# INTEGRATED BIO-FREQUENCY SYSTEM
# =============================================================================

class BioFrequencySystem:
    """
    Complete Bio-Frequency system integrating:
    1. Biological phase entrainment
    2. 7 Nodes meditation protocol
    3. EZ water structure
    """
    
    def __init__(self, carrier_frequency: float = F0_HZ):
        """
        Initialize complete bio-frequency system.
        
        Args:
            carrier_frequency: Fundamental frequency (Hz)
        """
        self.carrier_frequency = carrier_frequency
        self.entrainment = BiologicalEntrainment(carrier_frequency)
        self.meditation = SevenNodesMeditation()
        self.ez_water = EZWaterStructure()
        
        # Add default biological oscillators
        self._initialize_default_oscillators()
        
    def _initialize_default_oscillators(self):
        """Add default biological oscillators."""
        # Microtubules naturally resonate at f₀ with slight variation
        # This represents different protofilaments in the microtubule network
        self.entrainment.add_oscillator("microtubule_1", F0_HZ, coupling=0.95)
        self.entrainment.add_oscillator("microtubule_2", F0_HZ * 1.001, coupling=0.95)
        self.entrainment.add_oscillator("microtubule_3", F0_HZ * 0.999, coupling=0.95)
        self.entrainment.add_oscillator("microtubule_4", F0_HZ * 1.002, coupling=0.95)
    
    def run_complete_protocol(self,
                             duration: float = 300.0,
                             use_binaural: bool = False) -> Dict:
        """
        Run complete bio-frequency protocol.
        
        Args:
            duration: Protocol duration (seconds)
            use_binaural: Use binaural beats for sonic pillar
            
        Returns:
            Complete protocol results
        """
        # Activate all three pillars
        sonic = self.meditation.activate_sonic_pillar(use_binaural=use_binaural)
        rhythmic = self.meditation.activate_rhythmic_pillar(breaths_per_minute=6.0)
        visual = self.meditation.activate_visual_pillar()
        
        # Simulate biological entrainment
        entrainment_results = self.entrainment.simulate_entrainment(
            duration=duration, dt=0.01
        )
        
        # Simulate water structuring
        water_results = self.ez_water.structure_water(
            duration=duration,
            frequency=self.carrier_frequency
        )
        
        # Calculate overall system coherence
        meditation_coherence = self.meditation.calculate_meditation_coherence()
        biological_coherence = entrainment_results['final_coherence']
        water_coherence = water_results['water_coherence']
        
        # Combined coherence (weighted average)
        overall_coherence = (
            0.4 * biological_coherence +
            0.3 * meditation_coherence +
            0.3 * water_coherence
        )
        
        return {
            'carrier_frequency': self.carrier_frequency,
            'duration': duration,
            'pillars': {
                'sonic': sonic,
                'rhythmic': rhythmic,
                'visual': visual
            },
            'entrainment': entrainment_results,
            'water_structure': water_results,
            'coherence': {
                'biological': biological_coherence,
                'meditation': meditation_coherence,
                'water': water_coherence,
                'overall': overall_coherence,
                'status': self._classify_overall_coherence(overall_coherence)
            },
            'consciousness_stable': overall_coherence >= COHERENCE_THRESHOLD_STABLE
        }
    
    def _classify_overall_coherence(self, coherence: float) -> str:
        """Classify overall system coherence."""
        if coherence >= COHERENCE_THRESHOLD_SUPERRADIANCE:
            return "SUPERRADIANT"
        elif coherence >= COHERENCE_THRESHOLD_EXCELLENT:
            return "EXCELLENT"
        elif coherence >= COHERENCE_THRESHOLD_STABLE:
            return "STABLE"
        elif coherence >= 0.7:
            return "GOOD"
        else:
            return "DEVELOPING"


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_default_system(frequency: float = F0_HZ) -> BioFrequencySystem:
    """
    Create a bio-frequency system with default configuration.
    
    Args:
        frequency: Carrier frequency (Hz)
        
    Returns:
        Configured BioFrequencySystem
    """
    return BioFrequencySystem(carrier_frequency=frequency)


def quick_protocol(duration: float = 300.0) -> Dict:
    """
    Run quick bio-frequency protocol with defaults.
    
    Args:
        duration: Protocol duration in seconds
        
    Returns:
        Protocol results
    """
    system = create_default_system()
    return system.run_complete_protocol(duration=duration)


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("Bio-Frequency System - 141.7001 Hz Biological Entrainment")
    print("=" * 80)
    print()
    
    # Create system
    print("Creating Bio-Frequency System...")
    system = create_default_system()
    print(f"  Carrier frequency: {system.carrier_frequency} Hz")
    print(f"  Biological oscillators: {len(system.entrainment.oscillators)}")
    print()
    
    # Run 5-minute protocol
    print("Running complete 5-minute protocol...")
    print("  [Sonic] Activating 141.7001 Hz pure tone")
    print("  [Rhythmic] Golden ratio breathing (6 breaths/min)")
    print("  [Visual] Hexagonal geometry contemplation")
    print()
    
    results = system.run_complete_protocol(duration=300.0, use_binaural=False)
    
    # Display results
    print("Protocol Results:")
    print("-" * 80)
    
    coherence = results['coherence']
    print(f"Overall Coherence: Ψ = {coherence['overall']:.6f}")
    print(f"  Status: {coherence['status']}")
    print(f"  Consciousness Stable: {results['consciousness_stable']}")
    print()
    
    print("Component Coherence:")
    print(f"  Biological entrainment: Ψ = {coherence['biological']:.6f}")
    print(f"  Meditation protocol:    Ψ = {coherence['meditation']:.6f}")
    print(f"  Water structure:        Ψ = {coherence['water']:.6f}")
    print()
    
    water = results['water_structure']
    print("EZ Water Structure:")
    print(f"  Charging rate: {water['charging_rate']:.4f}")
    print(f"  Structure level: {water['structure_level']:.4f}")
    print(f"  EZ thickness: {water['ez_thickness_um']:.2f} μm")
    print(f"  Hexagonal layers: {water['hexagonal_layers']}")
    print(f"  Entropy reduction: {water['entropy_reduction']:.4f}")
    print()
    
    print("=" * 80)
    print("Protocol complete. System coherence achieved.")
    print("∴𓂀Ω∞³")
    print("=" * 80)
