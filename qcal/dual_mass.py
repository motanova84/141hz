#!/usr/bin/env python3
"""
QCAL Dual Mass Perspective Framework

Unifies Traditional Physics and Noetic Axiom perspectives on mass.

Mathematical Framework:
======================

1. Traditional Physics (Einstein-Planck-de Broglie):
   E = hf  ⟹  m_eff = E/c² = hf/c²
   ∴ m ∝ f (mass proportional to frequency)
   
2. Noetic Axiom (José Manuel - "Mass as Detention"):
   "La masa es una ilusión de detención"
   Detention ⟹ lower frequency (or higher period T = 1/f)
   ∴ m ∝ 1/f (mass proportional to inverse frequency)
   
3. Dual Unification:
   m(f) = (hf/c²) · (f₀/f) = hf₀/c²
   
   Where f₀ = 141.7001 Hz is the fundamental QCAL frequency.
   
   This gives a constant mass anchored to the reference frequency f₀,
   representing the minimal quantized noetic mass.

Physical Interpretations:
========================

- Effective Mass (m_eff): External perspective - energy content
  Measures "how much energy is compacted" (relativistic mass)
  
- Noetic Mass (m_noesis): Internal perspective - vibrational resistance
  Measures "how much resistance to vibration" (detention)
  
- Unified Mass (m_dual): Equilibrium between both perspectives
  Resolves the duality: mass emerges from imbalance between
  internal coherence (vibration) and external perception (energy)

Dimensional Analysis:
====================

m_eff = hf/c² has units: [J·s][1/s]/[m²/s²] = [kg] ✓
m_noesis = α/f where α = hf₀²/c² has units: [kg·Hz]/[Hz] = [kg] ✓
m_dual = hf₀/c² has units: [J·s][1/s]/[m²/s²] = [kg] ✓

Minimal Noetic Mass:
===================

m_min = h·f₀/c² = (6.62607015×10⁻³⁴ J·s)(141.7001 Hz)/(299792458 m/s)²
      ≈ 1.04×10⁻⁴⁸ kg

Author: José Manuel Mota Burruezo
License: MIT
"""

import math
from typing import Union, Tuple
import numpy as np

# Physical constants (CODATA 2018)
H_PLANCK = 6.62607015e-34  # J·s - Planck constant
C_LIGHT = 299792458.0      # m/s - Speed of light (exact)
F0_HZ = 141.70001          # Hz - Fundamental QCAL frequency (matches qcal.constants)


class DualMassPerspective:
    """
    Dual Mass Perspective Framework.
    
    Provides calculations for:
    - Effective mass (traditional physics)
    - Noetic mass (detention axiom)
    - Unified dual mass (resonance equilibrium)
    """
    
    def __init__(self, f0: float = F0_HZ):
        """
        Initialize dual mass framework.
        
        Parameters
        ----------
        f0 : float
            Reference frequency (Hz). Default: 141.7001 Hz
        """
        self.f0 = f0
        self.h = H_PLANCK
        self.c = C_LIGHT
        self.c2 = C_LIGHT ** 2
        
        # Calculate minimal noetic mass at f₀
        self.m_min = self.h * self.f0 / self.c2
        
        # Alpha constant for noetic mass: α = h·f₀²/c² [kg·Hz]
        # So that m_noesis = α/f gives m_min at f = f₀
        self.alpha = self.h * (self.f0 ** 2) / self.c2
    
    def effective_mass(self, frequency: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate effective mass (traditional physics perspective).
        
        From E = hf and E = mc²:
        m_eff = hf/c²
        
        This represents mass as compacted energy (external view).
        Higher frequency → higher energy → higher mass.
        
        Parameters
        ----------
        frequency : float or array
            Frequency in Hz
            
        Returns
        -------
        m_eff : float or array
            Effective mass in kg
            
        Examples
        --------
        >>> dmp = DualMassPerspective()
        >>> m_eff = dmp.effective_mass(141.7001)
        >>> print(f"m_eff = {m_eff:.3e} kg")
        m_eff = 1.040e-48 kg
        """
        return self.h * frequency / self.c2
    
    def noetic_mass(self, frequency: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate noetic mass (detention axiom perspective).
        
        From "mass as detention" axiom:
        m_noesis = α/f  where α = h·f₀ [kg·s]
        
        This represents mass as vibrational resistance (internal view).
        Lower frequency → more "detention" → higher mass.
        
        Parameters
        ----------
        frequency : float or array
            Frequency in Hz
            
        Returns
        -------
        m_noesis : float or array
            Noetic mass in kg
            
        Examples
        --------
        >>> dmp = DualMassPerspective()
        >>> m_noesis = dmp.noetic_mass(141.7001)
        >>> print(f"m_noesis = {m_noesis:.3e} kg")
        m_noesis = 1.040e-48 kg
        
        Notes
        -----
        At f = f₀, noetic mass equals effective mass equals minimal mass.
        """
        return self.alpha / frequency
    
    def unified_mass(self, frequency: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Calculate unified dual mass (equilibrium perspective).
        
        From dual unification:
        m(f) = (hf/c²) · (f₀/f) = hf₀/c²
        
        This is constant, independent of frequency!
        It represents the fundamental quantum of noetic mass.
        
        Parameters
        ----------
        frequency : float or array
            Frequency in Hz (note: result is independent of this)
            
        Returns
        -------
        m_dual : float
            Unified mass in kg (constant = m_min)
            
        Examples
        --------
        >>> dmp = DualMassPerspective()
        >>> m1 = dmp.unified_mass(100)
        >>> m2 = dmp.unified_mass(1000)
        >>> assert abs(m1 - m2) < 1e-60  # They are equal!
        
        Notes
        -----
        The unified mass is always equal to m_min = hf₀/c²,
        regardless of the input frequency. This represents the
        fundamental equilibrium between energy and detention.
        """
        # Could simplify to just return self.m_min, but keeping
        # the formula explicit shows the dual nature
        if isinstance(frequency, np.ndarray):
            return np.full_like(frequency, self.m_min, dtype=float)
        else:
            return self.m_min
    
    def mass_ratio(self, frequency: Union[float, np.ndarray]) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
        """
        Calculate ratios of effective and noetic masses to minimal mass.
        
        Returns
        -------
        r_eff : float or array
            Ratio m_eff/m_min = f/f₀
        r_noesis : float or array
            Ratio m_noesis/m_min = f₀/f
            
        Examples
        --------
        >>> dmp = DualMassPerspective()
        >>> r_eff, r_noesis = dmp.mass_ratio(141.7001)
        >>> assert abs(r_eff - 1.0) < 1e-10
        >>> assert abs(r_noesis - 1.0) < 1e-10
        
        Notes
        -----
        At f = f₀, both ratios equal 1.
        For f > f₀: r_eff > 1, r_noesis < 1 (high energy, low detention)
        For f < f₀: r_eff < 1, r_noesis > 1 (low energy, high detention)
        """
        r_eff = frequency / self.f0
        r_noesis = self.f0 / frequency
        return r_eff, r_noesis
    
    def get_constants(self) -> dict:
        """
        Get all relevant constants for this framework.
        
        Returns
        -------
        constants : dict
            Dictionary with:
            - f0: Reference frequency (Hz)
            - m_min: Minimal noetic mass (kg)
            - alpha: Noetic mass constant (kg·s)
            - h: Planck constant (J·s)
            - c: Speed of light (m/s)
        """
        return {
            'f0': self.f0,
            'm_min': self.m_min,
            'alpha': self.alpha,
            'h': self.h,
            'c': self.c,
            'c2': self.c2
        }


def calculate_dual_mass_spectrum(frequencies: np.ndarray, f0: float = F0_HZ) -> dict:
    """
    Calculate complete dual mass spectrum for array of frequencies.
    
    Parameters
    ----------
    frequencies : np.ndarray
        Array of frequencies (Hz)
    f0 : float
        Reference frequency (Hz). Default: 141.7001 Hz
        
    Returns
    -------
    spectrum : dict
        Dictionary containing:
        - frequencies: Input frequency array
        - m_eff: Effective masses
        - m_noesis: Noetic masses
        - m_dual: Unified masses (constant)
        - r_eff: Effective mass ratios
        - r_noesis: Noetic mass ratios
        
    Examples
    --------
    >>> freqs = np.logspace(0, 3, 100)  # 1 Hz to 1000 Hz
    >>> spectrum = calculate_dual_mass_spectrum(freqs)
    >>> import matplotlib.pyplot as plt
    >>> plt.loglog(spectrum['frequencies'], spectrum['m_eff'], label='m_eff')
    >>> plt.loglog(spectrum['frequencies'], spectrum['m_noesis'], label='m_noesis')
    >>> plt.axhline(spectrum['m_dual'][0], ls='--', label='m_dual (constant)')
    >>> plt.legend()
    """
    dmp = DualMassPerspective(f0)
    
    m_eff = dmp.effective_mass(frequencies)
    m_noesis = dmp.noetic_mass(frequencies)
    m_dual = dmp.unified_mass(frequencies)
    r_eff, r_noesis = dmp.mass_ratio(frequencies)
    
    return {
        'frequencies': frequencies,
        'm_eff': m_eff,
        'm_noesis': m_noesis,
        'm_dual': m_dual,
        'r_eff': r_eff,
        'r_noesis': r_noesis,
        'm_min': dmp.m_min,
        'f0': f0
    }


# Convenience functions for direct access
def effective_mass(frequency: Union[float, np.ndarray], h: float = H_PLANCK, c: float = C_LIGHT) -> Union[float, np.ndarray]:
    """
    Calculate effective mass directly: m_eff = hf/c²
    
    Traditional physics perspective (Einstein-Planck).
    """
    return h * frequency / (c ** 2)


def noetic_mass(frequency: Union[float, np.ndarray], f0: float = F0_HZ, h: float = H_PLANCK, c: float = C_LIGHT) -> Union[float, np.ndarray]:
    """
    Calculate noetic mass directly: m_noesis = (h·f₀²/c²)/f
    
    Detention axiom perspective.
    """
    alpha = h * (f0 ** 2) / (c ** 2)
    return alpha / frequency


def unified_mass(f0: float = F0_HZ, h: float = H_PLANCK, c: float = C_LIGHT) -> float:
    """
    Calculate unified mass directly: m_dual = hf₀/c²
    
    Constant minimal noetic mass (frequency-independent).
    """
    return h * f0 / (c ** 2)


if __name__ == "__main__":
    # Demonstration of dual mass perspective
    print("=" * 70)
    print("QCAL Dual Mass Perspective Framework")
    print("=" * 70)
    print()
    
    dmp = DualMassPerspective()
    constants = dmp.get_constants()
    
    print("Constants:")
    print(f"  f₀ = {constants['f0']:.4f} Hz")
    print(f"  m_min = {constants['m_min']:.6e} kg")
    print(f"  α = {constants['alpha']:.6e} kg·s")
    print()
    
    print("Mass Calculations at Different Frequencies:")
    print("-" * 70)
    print(f"{'Frequency':>12}  {'m_eff':>14}  {'m_noesis':>14}  {'m_dual':>14}")
    print(f"{'(Hz)':>12}  {'(kg)':>14}  {'(kg)':>14}  {'(kg)':>14}")
    print("-" * 70)
    
    test_freqs = [1.0, 10.0, 141.7001, 1000.0, 1e6]
    for f in test_freqs:
        m_e = dmp.effective_mass(f)
        m_n = dmp.noetic_mass(f)
        m_d = dmp.unified_mass(f)
        print(f"{f:12.4e}  {m_e:14.6e}  {m_n:14.6e}  {m_d:14.6e}")
    
    print()
    print("Key Observations:")
    print("  • At f = f₀: all three masses are equal (equilibrium)")
    print("  • For f > f₀: m_eff > m_min, m_noesis < m_min")
    print("  • For f < f₀: m_eff < m_min, m_noesis > m_min")
    print("  • m_dual is always constant = m_min")
    print()
    print("Physical Interpretation:")
    print("  • m_eff: 'Energy view' - what you measure from outside")
    print("  • m_noesis: 'Detention view' - resistance to vibration")
    print("  • m_dual: Fundamental quantum of noetic mass")
    print("=" * 70)
