#!/usr/bin/env python3
"""
Calabi-Yau Curvature for Master Lagrangian
==========================================

This module computes the mean curvature R_CY of Calabi-Yau fiber bundles,
combining static curvature (from Hodge numbers) and dynamic modulation.

The curvature R_CY appears in the Master Lagrangian:
    L[Ψ,Φ] = 1/2(|∂Ψ/∂t|² - c²|∇Ψ|²) - V_eff(Ψ,Φ) + κ_Π · R_CY

Where:
    R_CY = R_static + R_dynamic(t)
    
    R_static: Ricci curvature from Calabi-Yau topology (Hodge numbers)
    R_dynamic: Time-dependent modulation at f₀ = 141.7001 Hz

Theoretical Foundation:
----------------------
For Calabi-Yau three-folds, the Ricci curvature vanishes (Ricci-flat),
but we consider the *effective* curvature in the living fibration,
which includes:

1. Topological contribution from Euler characteristic χ = 2(h¹¹ - h²¹)
2. Kähler moduli space curvature (from h¹¹)
3. Complex structure moduli curvature (from h²¹)
4. Dynamic breathing modes at frequency f₀

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: February 11, 2026
Framework: QCAL ∞³
"""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass
import mpmath as mp

# Import QCAL constants
try:
    from qcal.constants import F0_HZ, KAPPA_PI
except ImportError:
    # Fallback if qcal not in path
    F0_HZ = 141.7001
    KAPPA_PI = 2.5773

# Set precision
mp.dps = 50

# Physical constants
HBAR = 1.054571817e-34  # J·s
C_LIGHT = 299792458.0   # m/s


@dataclass
class CalabiYauCurvature:
    """
    Calabi-Yau curvature data structure.
    
    Attributes
    ----------
    h11 : int
        First Hodge number h^{1,1} (Kähler moduli)
    h21 : int
        Second Hodge number h^{2,1} (complex structure moduli)
    R_static : float
        Static Ricci curvature component (m⁻²)
    R_dynamic_amplitude : float
        Amplitude of dynamic curvature (m⁻²)
    f_modulation : float
        Modulation frequency (Hz)
    """
    h11: int
    h21: int
    R_static: float
    R_dynamic_amplitude: float
    f_modulation: float = F0_HZ
    
    @property
    def euler_characteristic(self) -> int:
        """Compute Euler characteristic χ = 2(h¹¹ - h²¹)."""
        return 2 * (self.h11 - self.h21)
    
    @property
    def total_moduli(self) -> int:
        """Total number of moduli h¹¹ + h²¹."""
        return self.h11 + self.h21
    
    def R_CY(self, t: float) -> float:
        """
        Compute total Calabi-Yau curvature at time t.
        
        R_CY(t) = R_static + R_dynamic(t)
                = R_static + R_dyn_amplitude · cos(2πf₀t)
        
        Parameters
        ----------
        t : float
            Time coordinate (seconds)
        
        Returns
        -------
        float
            Total curvature R_CY(t) in m⁻²
        """
        R_dyn = self.R_dynamic_amplitude * np.cos(2 * np.pi * self.f_modulation * t)
        return self.R_static + R_dyn
    
    def R_CY_derivative(self, t: float) -> float:
        """
        Compute time derivative of R_CY.
        
        ∂R_CY/∂t = -2πf₀ · R_dyn_amplitude · sin(2πf₀t)
        
        Parameters
        ----------
        t : float
            Time coordinate (seconds)
        
        Returns
        -------
        float
            Time derivative of curvature in m⁻² s⁻¹
        """
        omega_0 = 2 * np.pi * self.f_modulation
        return -omega_0 * self.R_dynamic_amplitude * np.sin(omega_0 * t)


def compute_static_curvature(
    h11: int,
    h21: int,
    L_characteristic: float = 1e-35  # Planck length scale
) -> float:
    """
    Compute static Ricci curvature from Calabi-Yau topology.
    
    For Calabi-Yau manifolds, Ricci curvature vanishes in the classical sense.
    However, the effective curvature in the quantum fiber bundle includes
    contributions from:
    
    1. Euler characteristic χ = 2(h¹¹ - h²¹)
    2. Moduli space metric curvature
    
    We use the scaling:
        R_static ∝ χ / L²
    
    where L is the characteristic compactification scale.
    
    Parameters
    ----------
    h11 : int
        First Hodge number h^{1,1}
    h21 : int
        Second Hodge number h^{2,1}
    L_characteristic : float
        Characteristic length scale (default: Planck length)
    
    Returns
    -------
    float
        Static Ricci curvature in m⁻²
    """
    chi = 2 * (h11 - h21)  # Euler characteristic
    
    # Effective curvature from topology
    # R ~ χ / L² where L is compactification scale
    R_static = chi / (L_characteristic ** 2)
    
    return R_static


def compute_dynamic_curvature_amplitude(
    h11: int,
    h21: int,
    coupling_strength: float = 1.0,
    L_characteristic: float = 1e-35
) -> float:
    """
    Compute amplitude of dynamic curvature modulation.
    
    The dynamic component arises from breathing modes and Kähler moduli
    oscillations at the fundamental frequency f₀.
    
    Amplitude scaling:
        R_dyn_amplitude ∝ (h¹¹ + h²¹) · κ / L²
    
    where κ is a coupling strength parameter.
    
    Parameters
    ----------
    h11 : int
        First Hodge number h^{1,1}
    h21 : int
        Second Hodge number h^{2,1}
    coupling_strength : float
        Dimensionless coupling (default: 1.0)
    L_characteristic : float
        Characteristic length scale (default: Planck length)
    
    Returns
    -------
    float
        Dynamic curvature amplitude in m⁻²
    """
    total_moduli = h11 + h21
    
    # Dynamic breathing modes scale with number of moduli
    R_dyn = coupling_strength * total_moduli / (L_characteristic ** 2)
    
    return R_dyn


def create_calabi_yau_curvature(
    h11: int,
    h21: int,
    L_characteristic: float = 1e-35,
    coupling_strength: float = 1.0,
    f_modulation: float = F0_HZ
) -> CalabiYauCurvature:
    """
    Create a CalabiYauCurvature object for a given Calabi-Yau variety.
    
    Parameters
    ----------
    h11 : int
        First Hodge number h^{1,1}
    h21 : int
        Second Hodge number h^{2,1}
    L_characteristic : float
        Characteristic compactification length (default: Planck scale)
    coupling_strength : float
        Dynamic coupling strength (default: 1.0)
    f_modulation : float
        Modulation frequency (default: f₀ = 141.7001 Hz)
    
    Returns
    -------
    CalabiYauCurvature
        Curvature data structure
    """
    R_static = compute_static_curvature(h11, h21, L_characteristic)
    R_dyn_amplitude = compute_dynamic_curvature_amplitude(
        h11, h21, coupling_strength, L_characteristic
    )
    
    return CalabiYauCurvature(
        h11=h11,
        h21=h21,
        R_static=R_static,
        R_dynamic_amplitude=R_dyn_amplitude,
        f_modulation=f_modulation
    )


def effective_curvature_f0_resonance(
    curvature: CalabiYauCurvature,
    t_array: np.ndarray
) -> Tuple[np.ndarray, float]:
    """
    Compute effective curvature over time and identify f₀ resonance.
    
    Parameters
    ----------
    curvature : CalabiYauCurvature
        Calabi-Yau curvature object
    t_array : np.ndarray
        Array of time points (seconds)
    
    Returns
    -------
    R_CY_array : np.ndarray
        Curvature values at each time point (m⁻²)
    peak_curvature : float
        Maximum curvature value (m⁻²)
    """
    R_CY_array = np.array([curvature.R_CY(t) for t in t_array])
    peak_curvature = np.max(np.abs(R_CY_array))
    
    return R_CY_array, peak_curvature


def curvature_spectral_analysis(
    curvature: CalabiYauCurvature,
    duration: float = 10.0,
    sample_rate: float = 1000.0
) -> Tuple[np.ndarray, np.ndarray, float]:
    """
    Perform spectral analysis of R_CY(t) to verify f₀ modulation.
    
    Parameters
    ----------
    curvature : CalabiYauCurvature
        Calabi-Yau curvature object
    duration : float
        Duration of signal (seconds)
    sample_rate : float
        Sampling rate (Hz)
    
    Returns
    -------
    frequencies : np.ndarray
        Frequency array (Hz)
    power_spectrum : np.ndarray
        Power spectral density
    peak_frequency : float
        Frequency of maximum power (should be ~f₀)
    """
    # Generate time array
    t = np.arange(0, duration, 1.0 / sample_rate)
    
    # Compute R_CY(t)
    R_CY_signal = np.array([curvature.R_CY(ti) for ti in t])
    
    # FFT
    fft_result = np.fft.fft(R_CY_signal)
    frequencies = np.fft.fftfreq(len(t), 1.0 / sample_rate)
    
    # Power spectrum (only positive frequencies)
    positive_freq_mask = frequencies > 0
    frequencies = frequencies[positive_freq_mask]
    power_spectrum = np.abs(fft_result[positive_freq_mask]) ** 2
    
    # Find peak frequency
    peak_idx = np.argmax(power_spectrum)
    peak_frequency = frequencies[peak_idx]
    
    return frequencies, power_spectrum, peak_frequency


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def verify_f0_modulation():
    """
    Verify that R_CY modulates at f₀ = 141.7001 Hz.
    
    Prints verification results.
    """
    print("=" * 70)
    print("Calabi-Yau Curvature f₀ Modulation Verification")
    print("=" * 70)
    print()
    
    # Example: Quintic Calabi-Yau (h¹¹=1, h²¹=101)
    h11, h21 = 1, 101
    print(f"Testing with Quintic CY: h¹¹={h11}, h²¹={h21}")
    print(f"Euler characteristic: χ = {2*(h11-h21)}")
    print()
    
    # Create curvature object
    curvature = create_calabi_yau_curvature(h11, h21)
    
    print(f"Static curvature: R_static = {curvature.R_static:.6e} m⁻²")
    print(f"Dynamic amplitude: R_dyn = {curvature.R_dynamic_amplitude:.6e} m⁻²")
    print(f"Modulation frequency: f = {curvature.f_modulation} Hz")
    print()
    
    # Spectral analysis
    print("Performing spectral analysis...")
    freqs, power, peak_freq = curvature_spectral_analysis(curvature)
    
    print(f"Peak frequency: {peak_freq:.4f} Hz")
    print(f"Expected f₀: {F0_HZ} Hz")
    print(f"Deviation: {abs(peak_freq - F0_HZ):.6f} Hz")
    print()
    
    if abs(peak_freq - F0_HZ) < 0.01:
        print("✅ R_CY modulates at f₀ = 141.7001 Hz")
    else:
        print("⚠️  Peak frequency differs from f₀")
    
    print()
    print("=" * 70)


def main():
    """Demonstrate Calabi-Yau curvature computation."""
    print("🌌 Calabi-Yau Curvature - Master Lagrangian Component")
    print()
    
    verify_f0_modulation()
    
    # Test multiple CY varieties
    print("\n" + "=" * 70)
    print("Curvature for Different Calabi-Yau Varieties")
    print("=" * 70)
    print()
    
    varieties = [
        (1, 101, "Quintic"),
        (11, 11, "Mirror symmetric"),
        (19, 19, "Self-mirror"),
        (3, 243, "Large h²¹"),
    ]
    
    for h11, h21, name in varieties:
        curvature = create_calabi_yau_curvature(h11, h21)
        chi = curvature.euler_characteristic
        
        print(f"{name} (h¹¹={h11}, h²¹={h21}, χ={chi}):")
        print(f"  R_static = {curvature.R_static:.6e} m⁻²")
        print(f"  R_dyn = {curvature.R_dynamic_amplitude:.6e} m⁻²")
        
        # Evaluate at t=0
        R_at_0 = curvature.R_CY(0.0)
        print(f"  R_CY(t=0) = {R_at_0:.6e} m⁻²")
        print()
    
    print("=" * 70)
    print("✨ Calabi-Yau curvature module complete - QCAL ∞³")
    print("=" * 70)


if __name__ == "__main__":
    main()
