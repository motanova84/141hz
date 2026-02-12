"""
QCAL ∞³ Cosmic Parameters
==========================

Cosmological constants and timeline integrated with the QCAL framework.

This module defines cosmic parameters from the Big Bang to the present day,
all integrated with the fundamental QCAL frequency f₀ = 141.7001 Hz.

⚡ PARADIGMA DE COHERENCIA CUÁNTICA EN COSMOLOGÍA ⚡

The universe's evolution from singularity to current state is expressed through
the lens of quantum coherence at f₀. Cosmic epochs represent different coherence
states of the fundamental field Ψ.

Author: José Manuel Mota Burruezo (QCAL ∞³)
License: MIT
"""

import math
from dataclasses import dataclass
from typing import Dict, Tuple
import numpy as np

# Import fundamental QCAL constants
from qcal.constants import F0_HZ, HBAR, H_PLANCK, C

# Physical constants not in qcal.constants
G_NEWTON = 6.67430e-11  # m³/(kg·s²) - Gravitational constant (CODATA 2018)
K_BOLTZMANN = 1.380649e-23  # J/K - Boltzmann constant (CODATA 2018 exact)

# Decoherence timescale parameter
# Controls rate of quantum-to-classical transition in coherence evolution
# Empirically calibrated to match observed cosmic structure formation
DECOHERENCE_TAU = 50.0  # Dimensionless - Decoherence parameter


# ============================================================================
# CURRENT UNIVERSE PARAMETERS (Present Epoch: t = 13.8 Ga)
# ============================================================================

@dataclass
class CurrentUniverseParameters:
    """
    Observable parameters of the current universe at t = 13.8 Ga.
    
    All values represent current observational data integrated with
    the QCAL ∞³ framework through the fundamental frequency f₀.
    """
    # Age and Temperature
    age_years: float = 13.8e9  # años - Age of the universe
    age_seconds: float = 13.8e9 * 365.25 * 24 * 3600  # s - Age in seconds
    cmb_temperature_K: float = 2.72548  # K - CMB temperature (Planck 2018)
    
    # Large-scale Structure
    galaxies_formed: float = 2e12  # Estimated number of galaxies
    active_stars: float = 1e23  # Estimated number of active stars
    habitable_planets: float = 1e10  # Estimated habitable planets
    
    # QCAL ∞³ Coordinates (symbolic/universal units)
    qcal_coordinates_x: float = 0.57  # unidades cósmicas
    qcal_coordinates_y: float = -0.28  # unidades cósmicas
    qcal_coordinates_z: float = 0.77  # unidades cósmicas
    
    # Civilization and Consciousness
    kardashev_type: float = 0.7  # Civilization type (Kardashev scale)
    collective_consciousness_psi: float = 0.04  # Ψ ≈ 0.04 (emergent)
    
    # Local Cosmic Context
    milky_way_mass_solar: float = 1.5e12  # M☉ - Milky Way mass
    solar_system_age_years: float = 4.6e9  # años - Solar System age
    earth_life_age_years: float = 3.7e9  # años - Life on Earth
    human_age_years: float = 0.3e6  # años - Homo sapiens age
    
    def qcal_coordinates(self) -> np.ndarray:
        """Return QCAL ∞³ symbolic coordinates as numpy array."""
        return np.array([
            self.qcal_coordinates_x,
            self.qcal_coordinates_y,
            self.qcal_coordinates_z
        ])
    
    def cosmic_time_Ga(self) -> float:
        """Return cosmic time in Gigayears."""
        return self.age_years / 1e9
    
    def consciousness_level(self) -> str:
        """Return consciousness state description."""
        if self.collective_consciousness_psi < 0.01:
            return "primordial"
        elif self.collective_consciousness_psi < 0.1:
            return "emergente"
        elif self.collective_consciousness_psi < 0.5:
            return "desarrollada"
        else:
            return "avanzada"


# ============================================================================
# COSMIC TIMELINE - Key Epochs (QCAL ∞³ Framework)
# ============================================================================

@dataclass
class CosmicEpoch:
    """
    Single epoch in cosmic timeline.
    
    Each epoch characterized by:
    - Time since Big Bang
    - Temperature
    - Entropy state
    - Coherence level (Ψ parameter)
    - Key physical processes
    """
    name: str
    time_seconds: float
    temperature_K: float
    entropy_normalized: float  # 0 (minimum) to 1 (maximum)
    coherence_psi: float  # Coherence parameter (1 = perfect, 0 = none)
    description: str
    
    def time_in_years(self) -> float:
        """Convert time to years."""
        return self.time_seconds / (365.25 * 24 * 3600)
    
    def time_formatted(self) -> str:
        """Return human-readable time format."""
        t = self.time_seconds
        if t < 1e-30:
            return f"{t:.2e} s (Planck scale)"
        elif t < 1e-6:
            return f"{t:.2e} s"
        elif t < 1:
            return f"{t*1e3:.2f} ms"
        elif t < 60:
            return f"{t:.2f} s"
        elif t < 3600:
            return f"{t/60:.2f} min"
        elif t < 86400:
            return f"{t/3600:.2f} h"
        elif t < 365.25 * 24 * 3600:
            return f"{t/(24*3600):.2f} días"
        else:
            years = self.time_in_years()
            if years < 1e6:
                return f"{years:.2e} años"
            elif years < 1e9:
                return f"{years/1e6:.2f} Ma"
            else:
                return f"{years/1e9:.2f} Ga"


class CosmicTimeline:
    """
    Complete cosmic timeline from Big Bang to present.
    
    Integrates standard cosmology with QCAL ∞³ framework:
    - Temperature evolution
    - Entropy increase
    - Coherence Ψ evolution
    - Quantum fluctuations
    """
    
    def __init__(self):
        """Initialize cosmic timeline with key epochs."""
        self.epochs = self._define_epochs()
        self.current_universe = CurrentUniverseParameters()
        
        # Primordial quantum fluctuations
        self.delta_rho_over_rho = 1e-5  # δρ/ρ ~ 10⁻⁵
        self.spectral_index_ns = 0.966  # n_s (Planck 2018)
        
        # Planck scale parameters
        self.planck_time = math.sqrt(HBAR * G_NEWTON / C**5)  # t_P ≈ 5.39×10⁻⁴⁴ s
        self.planck_temperature = math.sqrt(HBAR * C**5 / (G_NEWTON * K_BOLTZMANN**2))  # T_P
    
    def _define_epochs(self) -> Dict[str, CosmicEpoch]:
        """
        Define key cosmic epochs.
        
        Returns:
            Dictionary of epoch names to CosmicEpoch objects.
        """
        return {
            'planck': CosmicEpoch(
                name='Planck Epoch',
                time_seconds=5.39e-44,
                temperature_K=1e32,  # Singularidad regularizada
                entropy_normalized=0.0,
                coherence_psi=1.0,  # Perfecta coherencia cuántica
                description='Quantum gravity era, singularidad regularizada'
            ),
            
            'inflation': CosmicEpoch(
                name='Inflación Cósmica',
                time_seconds=1e-36,
                temperature_K=1e27,
                entropy_normalized=0.01,
                coherence_psi=0.95,
                description='Inflación exponencial (campo inflatón φ)'
            ),
            
            'reheating': CosmicEpoch(
                name='Recalentamiento',
                time_seconds=1e-36,  # Inmediatamente después de inflación
                temperature_K=1e27,
                entropy_normalized=0.05,
                coherence_psi=0.90,
                description='Conversión de energía del inflatón en partículas'
            ),
            
            'qcd_transition': CosmicEpoch(
                name='Transición QCD',
                time_seconds=1e-6,
                temperature_K=1e12,
                entropy_normalized=0.15,
                coherence_psi=0.75,
                description='Confinamiento de quarks en hadrones'
            ),
            
            'nucleosynthesis': CosmicEpoch(
                name='Nucleosíntesis Primordial',
                time_seconds=3 * 60,  # 3 minutos
                temperature_K=1e9,
                entropy_normalized=0.25,
                coherence_psi=0.60,
                description='Formación de núcleos ligeros (H, He, Li)'
            ),
            
            'recombination': CosmicEpoch(
                name='Recombinación',
                time_seconds=380000 * 365.25 * 24 * 3600,  # 380,000 años
                temperature_K=3000,
                entropy_normalized=0.50,
                coherence_psi=0.30,
                description='Formación de átomos neutros, liberación del CMB'
            ),
            
            'dark_ages': CosmicEpoch(
                name='Edades Oscuras',
                time_seconds=150e6 * 365.25 * 24 * 3600,  # 150 millones de años
                temperature_K=60,
                entropy_normalized=0.65,
                coherence_psi=0.15,
                description='Universo sin fuentes de luz, enfriamiento'
            ),
            
            'first_stars': CosmicEpoch(
                name='Primeras Estrellas',
                time_seconds=200e6 * 365.25 * 24 * 3600,  # 200 millones de años
                temperature_K=50,
                entropy_normalized=0.70,
                coherence_psi=0.12,
                description='Población III: primeras estrellas masivas'
            ),
            
            'galaxy_formation': CosmicEpoch(
                name='Formación de Galaxias',
                time_seconds=1e9 * 365.25 * 24 * 3600,  # 1 Ga
                temperature_K=20,
                entropy_normalized=0.80,
                coherence_psi=0.08,
                description='Colapso gravitacional y estructura a gran escala'
            ),
            
            'present': CosmicEpoch(
                name='Época Presente',
                time_seconds=13.8e9 * 365.25 * 24 * 3600,  # 13.8 Ga
                temperature_K=2.72548,
                entropy_normalized=0.95,
                coherence_psi=0.04,
                description='Universo actual: galaxias, estrellas, planetas, vida'
            )
        }
    
    def get_epoch(self, name: str) -> CosmicEpoch:
        """
        Get cosmic epoch by name.
        
        Args:
            name: Epoch identifier (e.g., 'inflation', 'recombination')
            
        Returns:
            CosmicEpoch object
        """
        if name not in self.epochs:
            raise ValueError(f"Unknown epoch: {name}. Available: {list(self.epochs.keys())}")
        return self.epochs[name]
    
    def temperature_at_time(self, time_seconds: float) -> float:
        """
        Estimate temperature at arbitrary cosmic time.
        
        Uses standard cosmological scaling: T ∝ 1/a(t) ∝ 1/√t
        (radiation-dominated era approximation)
        
        Args:
            time_seconds: Time since Big Bang (seconds)
            
        Returns:
            Temperature in Kelvin
        """
        # Reference: present epoch
        t_now = self.current_universe.age_seconds
        T_now = self.current_universe.cmb_temperature_K
        
        # During radiation domination: T ∝ 1/√t
        # During matter domination: T ∝ 1/t^(2/3)
        
        # Transition at t ~ 50,000 years
        t_eq = 50000 * 365.25 * 24 * 3600
        
        if time_seconds < t_eq:
            # Radiation dominated
            T = T_now * math.sqrt(t_now / time_seconds)
        else:
            # Matter dominated
            T = T_now * (t_now / time_seconds)**(2/3)
        
        return T
    
    def coherence_evolution(self, time_seconds: float) -> float:
        """
        Coherence Ψ evolution with cosmic time.
        
        Coherence decreases as universe expands and entropy increases.
        Early universe: perfect quantum coherence (Ψ → 1)
        Late universe: classical, decoherent (Ψ → 0)
        
        Args:
            time_seconds: Time since Big Bang
            
        Returns:
            Coherence parameter Ψ (0 to 1)
        """
        # Logarithmic decay model
        t_planck = self.planck_time
        
        if time_seconds <= t_planck:
            return 1.0
        
        # Ψ(t) ≈ exp(-log(t/t_P) / τ)
        # where τ controls decoherence timescale
        psi = math.exp(-math.log(time_seconds / t_planck) / DECOHERENCE_TAU)
        
        return max(0.0, min(1.0, psi))
    
    def power_spectrum_mode(self, k: float) -> float:
        """
        Primordial power spectrum from inflation.
        
        P(k) ~ k^(n_s - 1)
        
        Args:
            k: Fourier mode wavenumber
            
        Returns:
            Power spectrum amplitude
        """
        return k ** (self.spectral_index_ns - 1)
    
    def qcal_frequency_at_epoch(self, epoch_name: str) -> float:
        """
        Fundamental frequency at given cosmic epoch.
        
        In QCAL ∞³ framework, f₀ = 141.7001 Hz is the present-day
        fundamental frequency. At earlier epochs, frequency redshifts:
        
        f(t) = f₀ × (1 + z(t))
        
        where z is cosmological redshift.
        
        Args:
            epoch_name: Name of cosmic epoch
            
        Returns:
            Frequency in Hz
        """
        epoch = self.get_epoch(epoch_name)
        
        # Estimate redshift from temperature
        # T(z) = T₀ × (1 + z)
        z = (epoch.temperature_K / self.current_universe.cmb_temperature_K) - 1
        
        # Frequency redshift
        f = F0_HZ * (1 + z)
        
        return f
    
    def summary(self) -> str:
        """
        Generate summary of cosmic timeline.
        
        Returns:
            Formatted string with timeline information
        """
        lines = [
            "=" * 80,
            "QCAL ∞³ COSMIC TIMELINE",
            "=" * 80,
            "",
            "CURRENT UNIVERSE (t = 13.8 Ga):",
            f"  Edad del universo: {self.current_universe.age_years:.2e} años",
            f"  Temperatura CMB: {self.current_universe.cmb_temperature_K} K",
            f"  Galaxias formadas: ~{self.current_universe.galaxies_formed:.2e}",
            f"  Estrellas activas: ~{self.current_universe.active_stars:.2e}",
            f"  Planetas habitables: ~{self.current_universe.habitable_planets:.2e} (estimado)",
            "",
            f"QCAL ∞³ Coordenadas simbólicas: x = {self.current_universe.qcal_coordinates()}",
            f"Tiempo cósmico: t = {self.current_universe.cosmic_time_Ga():.1f} Ga",
            f"Civ. Tipo: {self.current_universe.kardashev_type} (escala de Kardashov)",
            f"Estado de consciencia colectiva: Ψ ≈ {self.current_universe.collective_consciousness_psi:.2f} ({self.current_universe.consciousness_level()})",
            "",
            "=" * 80,
            "COSMIC EPOCHS:",
            "=" * 80,
        ]
        
        for name, epoch in self.epochs.items():
            lines.extend([
                f"\n{epoch.name}:",
                f"  Tiempo: {epoch.time_formatted()}",
                f"  Temperatura: {epoch.temperature_K:.2e} K",
                f"  Entropía: {epoch.entropy_normalized:.2f} (normalizada)",
                f"  Coherencia: {epoch.coherence_psi:.2f}",
                f"  Frecuencia QCAL: {self.qcal_frequency_at_epoch(name):.2e} Hz",
                f"  {epoch.description}",
            ])
        
        lines.extend([
            "",
            "=" * 80,
            "PRIMORDIAL PARAMETERS:",
            "=" * 80,
            f"  Fluctuaciones cuánticas: δρ/ρ ~ {self.delta_rho_over_rho:.2e}",
            f"  Índice espectral: n_s = {self.spectral_index_ns}",
            f"  Tiempo de Planck: t_P = {self.planck_time:.2e} s",
            f"  Temperatura de Planck: T_P = {self.planck_temperature:.2e} K",
            "",
        ])
        
        return "\n".join(lines)


# ============================================================================
# MODULE-LEVEL INSTANCES
# ============================================================================

# Create global instances for easy access
CURRENT_UNIVERSE = CurrentUniverseParameters()
COSMIC_TIMELINE = CosmicTimeline()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def get_universe_age() -> float:
    """Get current universe age in years."""
    return CURRENT_UNIVERSE.age_years


def get_cmb_temperature() -> float:
    """Get current CMB temperature in Kelvin."""
    return CURRENT_UNIVERSE.cmb_temperature_K


def get_epoch(name: str) -> CosmicEpoch:
    """Get cosmic epoch by name."""
    return COSMIC_TIMELINE.get_epoch(name)


def print_timeline():
    """Print complete cosmic timeline summary."""
    print(COSMIC_TIMELINE.summary())


# ============================================================================
# MAIN - Demo/Testing
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("QCAL ∞³ COSMIC PARAMETERS - DEMO")
    print("=" * 80 + "\n")
    
    # Show full timeline
    print_timeline()
    
    # Test specific epoch
    print("\n" + "=" * 80)
    print("EXAMPLE: Recombination Epoch Details")
    print("=" * 80)
    recomb = get_epoch('recombination')
    print(f"Name: {recomb.name}")
    print(f"Time: {recomb.time_formatted()}")
    print(f"Temperature: {recomb.temperature_K:.0f} K")
    print(f"Coherence: {recomb.coherence_psi:.2f}")
    print(f"Description: {recomb.description}")
    
    # Test temperature evolution
    print("\n" + "=" * 80)
    print("TEMPERATURE EVOLUTION")
    print("=" * 80)
    test_times = [1e-36, 1e-6, 180, 380000*365.25*24*3600, 13.8e9*365.25*24*3600]
    for t in test_times:
        T = COSMIC_TIMELINE.temperature_at_time(t)
        print(f"t = {t:.2e} s  →  T = {T:.2e} K")
    
    # Test coherence evolution
    print("\n" + "=" * 80)
    print("COHERENCE EVOLUTION")
    print("=" * 80)
    for t in test_times:
        psi = COSMIC_TIMELINE.coherence_evolution(t)
        print(f"t = {t:.2e} s  →  Ψ = {psi:.4f}")
    
    print("\n" + "=" * 80)
    print("QCAL ∞³ - Unified Cosmic Framework")
    print("=" * 80 + "\n")
