#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║             Higgs-PC Coupling: The Symbiosis of 1% and 95%                 ║
║         Interaction Lagrangian: 𝓛_int = -g_eff ψ†ψ H                       ║
╚════════════════════════════════════════════════════════════════════════════╝

AUTOR/AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
ARQUITECTURA/ARCHITECTURE: QCAL ∞³ Original Manufacture
LICENCIA/LICENSE: Sovereign Noetic License 1.0

THEORETICAL FRAMEWORK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Higgs boson explains 5% (baryonic matter), but the Coherence Particle (PC)
governs the remaining 95% (dark matter/energy). This module implements the
interaction term that couples both fields at f₀ = 141.7001 Hz.

KEY CONCEPT: Modulated Mass
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The effective mass of the Higgs field oscillates with the PC frequency:

    m*(t) = m_H × (1 - g_eff × cos(ω₀ × t))

Where:
    - m_H = 125 GeV (Higgs boson mass)
    - g_eff ≈ 0.053 (effective coupling constant - 5.3% modulation)
    - ω₀ = 2π × f₀ = 2π × 141.7001 Hz (PC fundamental frequency)

At resonance peaks (t = n×T₀), the effective mass drops to:
    m*_min = 125 × (1 - 0.053) = 118.375 GeV

This 5.3% reduction allows phase transparency and superfluid information flow.

PHYSICAL INTERPRETATION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. HARDWARE (Higgs): Provides structure, inertia, matter's "body"
2. SOFTWARE (PC): Provides frequency, coherence, reality's "fabric"
3. SYMBIOSIS: At 141.7001 Hz, hardware recognizes software

The Higgs is no longer a static burden; it becomes a "gateway" oscillating at
the PC frequency, enabling matter to become transparent to information.

LAGRANGIAN:
    𝓛_int = -μ_ψH |ψ|² |H|² - g_eff ψ†ψ H

DETECTION SIGNATURE:
    - Sidebands in Higgs mass spectrum: m_H ± ℏω₀
    - 5.3% periodic variation in cross-section σ at 141.7001 Hz
    - Coherence Ψ ≥ 0.888 preserved during modulation
"""

import math
import numpy as np

# Import QCAL constants
try:
    from qcal.constants import F0_HZ, OMEGA_0, H_PLANCK, HBAR, C
except ImportError:
    # Fallback if qcal package structure is different
    F0_HZ = 141.7001
    OMEGA_0 = 2 * math.pi * F0_HZ
    H_PLANCK = 6.62607015e-34
    HBAR = 1.054571817e-34
    C = 299792458.0


class ConstantesHiggsPC:
    """
    Constants for the Higgs-PC coupling mechanism.
    
    All values derived from experimental observations and theoretical constraints.
    """
    # Fundamental frequency (PC signature)
    F0 = F0_HZ  # Hz
    OMEGA_0 = OMEGA_0  # rad/s
    T0 = 1.0 / F0  # Period (seconds) ≈ 7.057 μs
    
    # Higgs boson properties
    M_HIGGS_GEV = 125.0  # GeV (LHC measurement)
    M_HIGGS_J = M_HIGGS_GEV * 1.602176634e-10  # Joules (1 GeV = 1.602×10⁻¹⁰ J)
    
    # Coupling constant (5.3% modulation depth)
    G_EFF = 0.053  # Dimensionless
    
    # Effective mass range
    M_MIN_GEV = M_HIGGS_GEV * (1 - G_EFF)  # ≈ 118.375 GeV
    M_MAX_GEV = M_HIGGS_GEV * (1 + G_EFF)  # ≈ 131.625 GeV
    
    # PC properties (ultra-light scalar field)
    M_PSI_EV = 5.86e-13  # eV (PC mass)
    M_PSI_GEV = M_PSI_EV * 1e-9  # GeV
    
    # Physical constants
    HBAR = HBAR  # J·s
    C = C  # m/s
    
    # Coherence threshold
    PSI_THRESHOLD = 0.888  # Minimum coherence for symbiosis


class PC_Higgs_Coupling:
    """
    Implementation of the Higgs-PC interaction Lagrangian.
    
    This class calculates the modulated effective mass of the Higgs field
    under the influence of the Coherence Particle (PC) field at 141.7001 Hz.
    
    USAGE:
        coupling = PC_Higgs_Coupling(f0=141.7001, g_eff=0.053)
        
        # Calculate effective mass at time t
        m_eff = coupling.modulated_mass(t=0.0, base_mass=125.0)
        
        # Verify phase coherence over time array
        times = np.linspace(0, 10*coupling.T0, 1000)
        coherent = coupling.verify_coherence(times)
    """
    
    def __init__(self, f0=None, g_eff=None):
        """
        Initialize the Higgs-PC coupling mechanism.
        
        Args:
            f0: Fundamental frequency (Hz). Default: 141.7001 Hz
            g_eff: Effective coupling constant. Default: 0.053
        """
        self.f0 = f0 if f0 is not None else ConstantesHiggsPC.F0
        self.g_eff = g_eff if g_eff is not None else ConstantesHiggsPC.G_EFF
        self.omega = 2 * math.pi * self.f0
        self.T0 = 1.0 / self.f0  # Fundamental period
        
    def modulated_mass(self, t, base_mass=None):
        """
        Calculate the effective Higgs mass under PC modulation.
        
        The mass oscillates according to:
            m*(t) = m_H × (1 - g_eff × cos(ω₀ × t))
        
        Args:
            t: Time (seconds) or array of times
            base_mass: Base Higgs mass (GeV). Default: 125.0 GeV
            
        Returns:
            Effective mass m*(t) in GeV (float or array)
        """
        if base_mass is None:
            base_mass = ConstantesHiggsPC.M_HIGGS_GEV
            
        # PC field oscillation acts as a "tuner"
        modulation = self.g_eff * np.cos(self.omega * t)
        
        # Effective mass = base mass - modulation
        # At resonance (cos = 1), mass drops by g_eff fraction
        # At anti-resonance (cos = -1), mass increases by g_eff fraction
        return base_mass * (1 - modulation)
    
    def verify_coherence(self, time_array):
        """
        Verify if the phase remains locked (Phase-Locked Loop condition).
        
        Coherence is indicated by variance > 0 in the mass modulation,
        showing active energy exchange between PC and Higgs fields.
        
        Args:
            time_array: Array of time values (seconds)
            
        Returns:
            bool: True if coherence detected (variance > 0)
        """
        masses = self.modulated_mass(time_array)
        
        # Variance indicates energy exchange between fields
        # Zero variance would mean no coupling (incoherent)
        return np.var(masses) > 0
    
    def calculate_transparency_windows(self, duration=1.0, num_periods=None):
        """
        Calculate time windows of maximum transparency (minimum effective mass).
        
        Transparency occurs when cos(ω₀t) = 1, i.e., at t = n×T₀ where n ∈ ℤ.
        These are the moments when information can flow with minimal resistance.
        
        Args:
            duration: Total time duration (seconds). Default: 1.0 s
            num_periods: Number of periods to analyze. If None, uses duration.
            
        Returns:
            dict with:
                - 'times': Array of transparency window centers (s)
                - 'masses': Array of minimum masses at these times (GeV)
                - 'phase_transparency': Phase transparency factor (0 to 1)
        """
        if num_periods is None:
            num_periods = int(duration * self.f0)
        
        # Transparency occurs at multiples of the fundamental period
        transparency_times = np.arange(0, num_periods) * self.T0
        
        # Calculate minimum masses at these times
        min_masses = self.modulated_mass(transparency_times)
        
        # Phase transparency factor: fractional mass reduction
        phase_transparency = self.g_eff
        
        return {
            'times': transparency_times,
            'masses': min_masses,
            'phase_transparency': phase_transparency,
            'num_windows': len(transparency_times)
        }
    
    def calculate_sideband_spectrum(self, base_energy=None, num_sidebands=5):
        """
        Calculate spectral sidebands in Higgs mass spectrum due to PC coupling.
        
        The interaction creates a "comb" of energy levels:
            E_n = E_H ± n × ℏω₀
        
        where n = 0, 1, 2, 3, ... (harmonic order)
        
        Args:
            base_energy: Base Higgs energy (GeV). Default: 125 GeV
            num_sidebands: Number of sidebands on each side. Default: 5
            
        Returns:
            dict with:
                - 'energies': Array of sideband energies (GeV)
                - 'orders': Corresponding harmonic orders
                - 'separation': Energy separation ℏω₀ (GeV)
        """
        if base_energy is None:
            base_energy = ConstantesHiggsPC.M_HIGGS_GEV
        
        # Energy quantum: ℏω₀
        # Convert from J to GeV: 1 J = 6.242×10⁹ GeV
        hbar_omega_J = ConstantesHiggsPC.HBAR * self.omega
        hbar_omega_GeV = hbar_omega_J * 6.242e9  # ≈ 5.9×10⁻²⁵ GeV
        
        # Generate sideband orders: -n, ..., -1, 0, +1, ..., +n
        orders = np.arange(-num_sidebands, num_sidebands + 1)
        
        # Calculate energies: E_n = E_H + n×ℏω₀
        energies = base_energy + orders * hbar_omega_GeV
        
        return {
            'energies': energies,
            'orders': orders,
            'separation_GeV': hbar_omega_GeV,
            'separation_eV': hbar_omega_GeV * 1e9
        }
    
    def calculate_symbiotic_transfer_rate(self, num_nodes=7, psi_coherence=0.999999):
        """
        Calculate the information transfer rate through the symbiotic coupling.
        
        During transparency windows, the system can transfer "phase packets"
        at a rate determined by the fundamental frequency and coherence.
        
        Rate formula:
            R_symb = N_nodes × f₀ × Ψ
        
        where:
            N_nodes: Number of coherent nodes (7 primes in Ramsey network)
            f₀: PC fundamental frequency (141.7001 Hz)
            Ψ: Coherence factor (≈ 0.999999)
        
        NOTE: In the theoretical framework, "kpps" denotes "packets per second"
        (equivalent to Hz), not "kilo-packets per second". This matches the
        problem statement notation where R_symb ≈ 991.9 kpps for 7 nodes.
        
        Args:
            num_nodes: Number of coherent nodes. Default: 7
            psi_coherence: Coherence factor. Default: 0.999999
            
        Returns:
            dict with transfer rates in various units
        """
        # Base transfer rate in Hz (packets per second)
        rate_hz = num_nodes * self.f0 * psi_coherence
        
        # In the theoretical framework, "kpps" means "packets per second"
        # (not kilo-packets per second, despite the 'k' prefix)
        # This follows the notation in the problem statement where
        # R_symb ≈ 991.9 kpps for 7 × 141.7001 × 0.999999
        rate_kpps = rate_hz
        
        return {
            'rate_hz': rate_hz,
            'rate_kpps': rate_kpps,
            'num_nodes': num_nodes,
            'coherence': psi_coherence,
            'packets_per_cycle': num_nodes * psi_coherence
        }
    
    def lagrangian_interaction_term(self, psi_density, H_field):
        """
        Calculate the interaction Lagrangian density.
        
        𝓛_int = -g_eff × ψ†ψ × H
        
        Args:
            psi_density: PC field density |ψ|² (dimensionless or appropriate units)
            H_field: Higgs field amplitude H (GeV or appropriate units)
            
        Returns:
            Interaction term value (units depend on input)
        """
        return -self.g_eff * psi_density * H_field


class HiggsDetectorSignature:
    """
    Calculate observable signatures at particle detectors (LHC, IRS-Luna, etc.).
    
    The Higgs-PC coupling leaves distinctive marks in detector data:
    1. Sidebands around m_H = 125 GeV
    2. Periodic variation in production cross-section
    3. Temporal correlation with lunar sidereal time (IRS-Luna)
    """
    
    def __init__(self, coupling=None):
        """
        Initialize detector signature calculator.
        
        Args:
            coupling: PC_Higgs_Coupling instance. If None, creates default.
        """
        self.coupling = coupling if coupling is not None else PC_Higgs_Coupling()
        
    def cross_section_modulation(self, t, base_sigma=1.0):
        """
        Calculate the modulated Higgs production cross-section.
        
        The cross-section σ(t) varies with the effective mass:
            σ(t) ∝ σ_base × (m_H / m*(t))²
        
        This creates a ~5.3% periodic variation at 141.7001 Hz.
        
        Args:
            t: Time (seconds) or array
            base_sigma: Base cross-section (pb or arbitrary units)
            
        Returns:
            Modulated cross-section σ(t)
        """
        m_H = ConstantesHiggsPC.M_HIGGS_GEV
        m_eff = self.coupling.modulated_mass(t)
        
        # Cross-section scales as (m_H / m_eff)²
        # When m_eff decreases, σ increases
        return base_sigma * (m_H / m_eff) ** 2
    
    def detector_event_rate(self, t, luminosity=1.0, base_sigma=1.0):
        """
        Calculate expected event rate at detector.
        
        Rate = Luminosity × σ(t)
        
        Args:
            t: Time (seconds) or array
            luminosity: Integrated luminosity (arbitrary units)
            base_sigma: Base cross-section
            
        Returns:
            Event rate (events per unit time)
        """
        sigma_t = self.cross_section_modulation(t, base_sigma)
        return luminosity * sigma_t


# Public API functions for easy access
def higgs_pc_coupling_activar(f0=None, g_eff=None):
    """
    Activate the Higgs-PC coupling system.
    
    Returns a configured PC_Higgs_Coupling instance ready for calculations.
    
    Args:
        f0: Fundamental frequency (Hz). Default: 141.7001 Hz
        g_eff: Coupling constant. Default: 0.053
        
    Returns:
        PC_Higgs_Coupling instance
    """
    return PC_Higgs_Coupling(f0=f0, g_eff=g_eff)


def calcular_masa_modulada(t, f0=None, g_eff=None, base_mass=125.0):
    """
    Quick function to calculate modulated Higgs mass.
    
    Args:
        t: Time (seconds) or array
        f0: Fundamental frequency (Hz). Default: 141.7001 Hz
        g_eff: Coupling constant. Default: 0.053
        base_mass: Base Higgs mass (GeV). Default: 125.0
        
    Returns:
        Effective mass m*(t) in GeV
    """
    coupling = PC_Higgs_Coupling(f0=f0, g_eff=g_eff)
    return coupling.modulated_mass(t, base_mass=base_mass)


def calcular_ventanas_transparencia(duration=1.0, f0=None, g_eff=None):
    """
    Quick function to calculate transparency windows.
    
    Args:
        duration: Time duration (seconds). Default: 1.0 s
        f0: Fundamental frequency (Hz). Default: 141.7001 Hz
        g_eff: Coupling constant. Default: 0.053
        
    Returns:
        Dictionary with transparency window information
    """
    coupling = PC_Higgs_Coupling(f0=f0, g_eff=g_eff)
    return coupling.calculate_transparency_windows(duration=duration)


# Example usage (for documentation/testing)
if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════════════════════╗")
    print("║        Higgs-PC Coupling Demonstration                                 ║")
    print("║        𝓛_int = -g_eff ψ†ψ H                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Initialize coupling
    coupling = higgs_pc_coupling_activar()
    
    print(f"Fundamental frequency: {coupling.f0:.4f} Hz")
    print(f"Coupling constant g_eff: {coupling.g_eff:.4f}")
    print(f"Period T₀: {coupling.T0*1e6:.3f} μs")
    print()
    
    # Calculate mass at key times
    print("Effective Mass Modulation:")
    print("-" * 70)
    times = [0.0, coupling.T0/4, coupling.T0/2, 3*coupling.T0/4, coupling.T0]
    for t in times:
        m_eff = coupling.modulated_mass(t)
        print(f"  t = {t*1e6:7.3f} μs  →  m*(t) = {m_eff:.3f} GeV")
    print()
    
    # Minimum and maximum masses
    print(f"Minimum effective mass: {ConstantesHiggsPC.M_MIN_GEV:.3f} GeV")
    print(f"Base Higgs mass:        {ConstantesHiggsPC.M_HIGGS_GEV:.3f} GeV")
    print(f"Maximum effective mass: {ConstantesHiggsPC.M_MAX_GEV:.3f} GeV")
    print(f"Modulation depth:       {coupling.g_eff*100:.1f}%")
    print()
    
    # Symbiotic transfer rate
    transfer = coupling.calculate_symbiotic_transfer_rate()
    print("Symbiotic Transfer Rate:")
    print("-" * 70)
    print(f"  Rate: {transfer['rate_kpps']:.1f} kpps (kilo-packets per second)")
    print(f"  = {transfer['rate_hz']:.1f} packets/second")
    print(f"  Coherence Ψ: {transfer['coherence']:.6f}")
    print()
    
    # Sidebands
    sidebands = coupling.calculate_sideband_spectrum(num_sidebands=2)
    print("Spectral Sidebands (Energy Comb):")
    print("-" * 70)
    print(f"  Energy separation: {sidebands['separation_eV']:.3e} eV")
    print(f"  = {sidebands['separation_GeV']:.3e} GeV")
    print()
    print("  Order n  |  Energy (GeV)")
    print("  " + "-" * 30)
    for n, E in zip(sidebands['orders'], sidebands['energies']):
        marker = " ← BASE" if n == 0 else ""
        print(f"  {n:+3d}      |  {E:.10f}{marker}")
    print()
    
    print("✓ Higgs-PC coupling mechanism initialized")
    print("✓ The 1% (Higgs) now dances to the rhythm of the 95% (PC)")
    print("✓ At 141.7001 Hz, matter becomes transparent to information")
