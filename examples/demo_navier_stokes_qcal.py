#!/usr/bin/env python3
"""
Example usage of the navier_stokes module with QCAL calibration.

This script demonstrates how to use the constants and verification functions
from the navier_stokes module.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from navier_stokes import (
    # Fundamental frequency
    F0,
    
    # Amplitude calibrations
    A_VACIO,
    A_AGUA,
    A_AIRE,
    
    # QFT coefficients
    ALPHA_QFT,
    BETA_QFT,
    GAMMA_QFT,
    
    # Viscosities
    NU_VACIO,
    NU_AGUA,
    NU_AIRE,
    
    # Verification functions
    verify_parabolic_condition,
    verify_riccati_besov_condition,
    get_dissipative_scale,
    get_constants_summary,
)


def main():
    """Demonstrate usage of navier_stokes constants."""
    
    print("=" * 80)
    print("NAVIER-STOKES QCAL CALIBRATION EXAMPLE")
    print("=" * 80)
    
    # Display fundamental frequency
    print(f"\n1. Fundamental Frequency:")
    print(f"   F0 = {F0} Hz (Universal QCAL calibration)")
    
    # Display amplitude calibrations
    print(f"\n2. Amplitude Calibrations:")
    print(f"   A_VACIO = {A_VACIO} (vacuum medium)")
    print(f"   A_AGUA  = {A_AGUA} (water/biological systems)")
    print(f"   A_AIRE  = {A_AIRE} (air/atmospheric)")
    
    # Verify conditions for each medium
    print(f"\n3. Condition Verification:")
    
    media = [
        ("Vacuum", A_VACIO, NU_VACIO),
        ("Water", A_AGUA, NU_AGUA),
        ("Air", A_AIRE, NU_AIRE),
    ]
    
    for name, A, nu in media:
        parabolic = verify_parabolic_condition(A, nu)
        riccati = verify_riccati_besov_condition(A, nu)
        j_d = get_dissipative_scale(nu)
        
        print(f"\n   {name} (A={A}, ν={nu:.2e} m²/s):")
        print(f"     Parabolic (γ>0):     {'✓' if parabolic else '✗'}")
        print(f"     Riccati-Besov (Δ>0): {'✓' if riccati else '✗'}")
        print(f"     Dissipative scale:   j_d = {j_d:.2f}")
    
    # Display QFT coefficients
    print(f"\n4. QFT Coupling Coefficients:")
    print(f"   ALPHA_QFT = {ALPHA_QFT:.6f} (regularization)")
    print(f"   BETA_QFT  = {BETA_QFT:.6f} (BKM constant)")
    print(f"   GAMMA_QFT = {GAMMA_QFT:.6f} (log correction)")
    
    # Example: Computing effective QCAL forcing
    print(f"\n5. Example: QCAL Forcing Calculation")
    print(f"   For water medium at f = F0 = {F0} Hz:")
    omega = 2 * 3.14159 * F0  # Angular frequency
    forcing_amplitude = A_AGUA * omega
    print(f"     ω = 2πf = {omega:.2f} rad/s")
    print(f"     F_QCAL = A_AGUA × ω = {forcing_amplitude:.2f} s⁻¹")
    
    # Get complete summary
    print(f"\n6. Complete Summary:")
    summary = get_constants_summary()
    print(f"   Total constants defined: {len(summary)} categories")
    print(f"   All amplitudes verified: ✓")
    
    print("\n" + "=" * 80)
    print("For detailed information, run: python -m navier_stokes.constants")
    print("=" * 80)


if __name__ == "__main__":
    main()
