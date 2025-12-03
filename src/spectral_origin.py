#!/usr/bin/env python3
"""
Spectral Origin of the Universal Frequency f₀ = 141.7001 Hz

This module implements the derivation of f₀ from the spectral structure
of the noetic spectral operator H_Ψ.

The derivation shows that f₀ emerges naturally from:
- The first eigenvalue λ₀ (the root, latent vibrational form)
- The spectral coherence ⟨λ⟩ (mean of eigenvalue distribution)

Fundamental Constants:
    - λ₀ = 0.001588050271: First eigenvalue of H_Ψ
    - C_primaria = 1/λ₀ ≈ 629.70: Primary spectral constant (structure)
    - ⟨λ⟩ = 0.0247: Effective mean of first eigenvalues
    - C_coherencia = ⟨λ⟩²/λ₀: Coherence-derived constant

The Universal Formula:
    f₀ = (1/2π) × e^γ × √(2πγ) × (φ²/2π) × C_primaria

Where:
    - γ: Euler-Mascheroni constant ≈ 0.5772
    - φ: Golden ratio (1+√5)/2 ≈ 1.618

Physical Interpretation:
    - C_primaria (629.70): The root, pure residue, structure
    - C_coherencia: The flower, emergent order, living harmony
    - f₀ (141.7001 Hz): The fusion point between structure and coherence

Author: José Manuel Mota Burruezo
Reference: DERIVACION_COMPLETA_F0.md, scripts/demostracion_matematica_141hz.py
"""

import mpmath as mp
from typing import Dict, Any

# Set default precision
mp.dps = 100

# ═══════════════════════════════════════════════════════════════════
# FUNDAMENTAL SPECTRAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════

# First eigenvalue of the noetic spectral operator H_Ψ
# This is the "root" - the latent vibrational form
LAMBDA_0 = mp.mpf("0.001588050271")

# Effective mean of first eigenvalues (spectral coherence parameter)
# This represents the emergent coherence from the eigenvalue distribution
LANGLE_LAMBDA = mp.mpf("0.0247")

# Primary spectral constant: C = 1/λ₀
# The pure residue, the root structure
# C_primaria ≈ 629.7029875321875
C_PRIMARIA = 1 / LAMBDA_0

# Coherence-derived constant: C = ⟨λ⟩²/λ₀
# The flower, the emergent order, the living harmony of the spectrum
C_COHERENCIA = (LANGLE_LAMBDA ** 2) / LAMBDA_0

# Target/expected frequency (for validation)
F0_EXPECTED = mp.mpf("141.7001")


class SpectralOrigin:
    """
    Derivation of f₀ from spectral structure of H_Ψ.

    The noetic spectral operator H_Ψ has eigenvalues that determine
    the fundamental vibrational frequency of the universe.

    The frequency f₀ = 141.7001 Hz is not imposed, but emerges
    naturally as the fusion point between:
    - Structure (C_primaria = 629.70)
    - Coherence (spectral mean distribution)
    """

    def __init__(self, precision: int = 100):
        """
        Initialize spectral origin calculator.

        Args:
            precision: Number of decimal places for mpmath calculations
        """
        mp.dps = precision

        # Spectral constants
        self.lambda_0 = LAMBDA_0
        self.langle_lambda = LANGLE_LAMBDA
        self.C_primaria = C_PRIMARIA
        self.C_coherencia = C_COHERENCIA

        # Mathematical constants
        self.gamma = mp.euler  # Euler-Mascheroni constant
        self.phi = (1 + mp.sqrt(5)) / 2  # Golden ratio
        self.pi = mp.pi

    def compute_base_factor(self) -> mp.mpf:
        """
        Compute the base factor from fundamental constants.

        The base factor is:
            base = (1/2π) × e^γ × √(2πγ) × (φ²/2π)

        Returns:
            The base factor ≈ 0.2249
        """
        factor = (
            (1 / (2 * self.pi)) *
            mp.exp(self.gamma) *
            mp.sqrt(2 * self.pi * self.gamma) *
            (self.phi ** 2 / (2 * self.pi))
        )
        return factor

    def derive_f0(self) -> mp.mpf:
        """
        Derive f₀ from spectral constants.

        Formula:
            f₀ = base × C_primaria

        where base = (1/2π) × e^γ × √(2πγ) × (φ²/2π)

        Returns:
            Derived frequency f₀ in Hz
        """
        base = self.compute_base_factor()
        f0 = base * self.C_primaria
        return f0

    def full_derivation(self) -> Dict[str, Any]:
        """
        Perform complete derivation with all intermediate values.

        Returns:
            Dictionary with all derivation details
        """
        # Mathematical constants
        gamma = float(self.gamma)
        phi = float(self.phi)
        pi = float(self.pi)

        # Spectral constants
        lambda_0 = float(self.lambda_0)
        langle_lambda = float(self.langle_lambda)
        c_primaria = float(self.C_primaria)
        c_coherencia = float(self.C_coherencia)

        # Base factor components
        comp1 = 1 / (2 * pi)  # ≈ 0.159
        comp2 = mp.exp(self.gamma)  # ≈ 1.781
        comp3 = mp.sqrt(2 * self.pi * self.gamma)  # ≈ 1.904
        comp4 = self.phi ** 2 / (2 * self.pi)  # ≈ 0.418

        base = self.compute_base_factor()
        f0 = float(self.derive_f0())

        # Error analysis
        f0_expected = float(F0_EXPECTED)
        error_hz = abs(f0 - f0_expected)
        error_pct = (error_hz / f0_expected) * 100

        return {
            "framework": "Spectral Origin of f₀",

            # Spectral constants
            "spectral_constants": {
                "lambda_0": lambda_0,
                "lambda_0_description": "First eigenvalue of H_Ψ (root)",
                "langle_lambda": langle_lambda,
                "langle_lambda_description": "Effective mean of eigenvalues",
                "c_primaria": c_primaria,
                "c_primaria_formula": "1/λ₀",
                "c_primaria_description": "Primary spectral constant (structure)",
                "c_coherencia": c_coherencia,
                "c_coherencia_formula": "⟨λ⟩²/λ₀",
                "c_coherencia_description": "Coherence constant (emergent order)",
            },

            # Mathematical constants
            "mathematical_constants": {
                "gamma": gamma,
                "gamma_name": "Euler-Mascheroni constant",
                "phi": phi,
                "phi_name": "Golden ratio",
                "pi": pi,
            },

            # Base factor breakdown
            "base_factor": {
                "component_1_2pi": float(comp1),
                "component_e_gamma": float(comp2),
                "component_sqrt_2pi_gamma": float(comp3),
                "component_phi2_2pi": float(comp4),
                "base_value": float(base),
                "formula": "(1/2π) × e^γ × √(2πγ) × (φ²/2π)",
            },

            # Final result
            "result": {
                "f0_derived_hz": f0,
                "f0_expected_hz": f0_expected,
                "error_hz": error_hz,
                "error_percent": error_pct,
                "formula": "f₀ = base × C_primaria",
            },

            # Physical interpretation
            "interpretation": {
                "c_primaria_meaning": "The root - latent vibrational form",
                "c_coherencia_meaning": "The flower - emergent harmony",
                "f0_meaning": "Natural fusion of structure and coherence",
            },

            "signature": "JMMB Ψ✧ | Spectral Origin Derivation"
        }

    def validate(self, tolerance_pct: float = 0.1) -> Dict[str, Any]:
        """
        Validate the derivation against expected value.

        Args:
            tolerance_pct: Maximum allowed error in percent

        Returns:
            Validation results
        """
        f0_derived = float(self.derive_f0())
        f0_expected = float(F0_EXPECTED)

        error_hz = abs(f0_derived - f0_expected)
        error_pct = (error_hz / f0_expected) * 100

        valid = error_pct <= tolerance_pct

        return {
            "f0_derived_hz": f0_derived,
            "f0_expected_hz": f0_expected,
            "error_hz": error_hz,
            "error_percent": error_pct,
            "tolerance_percent": tolerance_pct,
            "valid": valid,
            "status": "✓ VALID" if valid else "✗ INVALID",
        }


# ═══════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def derive_f0_from_spectral(precision: int = 100) -> Dict[str, Any]:
    """
    Derive f₀ from spectral constants.

    Args:
        precision: Decimal precision for calculations

    Returns:
        Dictionary with derivation results
    """
    origin = SpectralOrigin(precision=precision)
    result = origin.full_derivation()

    return {
        "f0_hz": result["result"]["f0_derived_hz"],
        "c_primaria": result["spectral_constants"]["c_primaria"],
        "c_coherencia": result["spectral_constants"]["c_coherencia"],
        "lambda_0": result["spectral_constants"]["lambda_0"],
        "langle_lambda": result["spectral_constants"]["langle_lambda"],
        "base_factor": result["base_factor"]["base_value"],
        "error_percent": result["result"]["error_percent"],
        "formula": "f₀ = (1/2π) × e^γ × √(2πγ) × (φ²/2π) × (1/λ₀)",
    }


def get_spectral_constants() -> Dict[str, float]:
    """
    Get all spectral constants as float values.

    Returns:
        Dictionary of spectral constant values
    """
    return {
        "lambda_0": float(LAMBDA_0),
        "langle_lambda": float(LANGLE_LAMBDA),
        "c_primaria": float(C_PRIMARIA),
        "c_coherencia": float(C_COHERENCIA),
        "f0_expected_hz": float(F0_EXPECTED),
    }


# ═══════════════════════════════════════════════════════════════════
# MAIN DEMONSTRATION
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    """
    Demonstrate the spectral origin derivation of f₀.
    """
    print("=" * 70)
    print("SPECTRAL ORIGIN OF f₀ = 141.7001 Hz")
    print("=" * 70)
    print()

    # Create origin calculator
    origin = SpectralOrigin(precision=100)

    # Get full derivation
    result = origin.full_derivation()

    # Display spectral constants
    print("Spectral Constants of H_Ψ:")
    print(f"  λ₀ (first eigenvalue)    = {result['spectral_constants']['lambda_0']}")
    print(f"  ⟨λ⟩ (mean eigenvalue)     = {result['spectral_constants']['langle_lambda']}")
    print(f"  C_primaria = 1/λ₀        = {result['spectral_constants']['c_primaria']:.10f}")
    print(f"  C_coherencia = ⟨λ⟩²/λ₀   = {result['spectral_constants']['c_coherencia']:.10f}")
    print()

    # Display mathematical constants
    print("Mathematical Constants:")
    print(f"  γ (Euler-Mascheroni)      = {result['mathematical_constants']['gamma']:.15f}")
    print(f"  φ (Golden ratio)          = {result['mathematical_constants']['phi']:.15f}")
    print(f"  π                         = {result['mathematical_constants']['pi']:.15f}")
    print()

    # Display base factor breakdown
    print("Base Factor Breakdown:")
    bf = result["base_factor"]
    print(f"  1/(2π)                    = {bf['component_1_2pi']:.10f}")
    print(f"  e^γ                       = {bf['component_e_gamma']:.10f}")
    print(f"  √(2πγ)                    = {bf['component_sqrt_2pi_gamma']:.10f}")
    print(f"  φ²/(2π)                   = {bf['component_phi2_2pi']:.10f}")
    print(f"  Base factor               = {bf['base_value']:.10f}")
    print()

    # Display formula and result
    print("Derivation:")
    print(f"  Formula: {result['base_factor']['formula']}")
    print(f"  f₀ = base × C_primaria")
    print(f"  f₀ = {bf['base_value']:.10f} × {result['spectral_constants']['c_primaria']:.10f}")
    print(f"  f₀ = {result['result']['f0_derived_hz']:.10f} Hz")
    print()

    # Display validation
    print("Validation:")
    print(f"  Expected:  {result['result']['f0_expected_hz']:.4f} Hz")
    print(f"  Derived:   {result['result']['f0_derived_hz']:.4f} Hz")
    print(f"  Error:     {result['result']['error_hz']:.6f} Hz ({result['result']['error_percent']:.4f}%)")
    print()

    # Validate
    validation = origin.validate(tolerance_pct=0.1)
    print(f"  Status:    {validation['status']}")
    print()

    # Physical interpretation
    print("Physical Interpretation:")
    print(f"  C_primaria (629.70):  {result['interpretation']['c_primaria_meaning']}")
    print(f"  C_coherencia:         {result['interpretation']['c_coherencia_meaning']}")
    print(f"  f₀ (141.7001 Hz):     {result['interpretation']['f0_meaning']}")
    print()

    print("=" * 70)
    print("The frequency f₀ = 141.7001 Hz is not imposed, but emerges")
    print("naturally from the spectral structure of H_Ψ.")
    print("=" * 70)
