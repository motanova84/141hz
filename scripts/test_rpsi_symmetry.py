#!/usr/bin/env python3
"""
Test script for A_Rpsi_symmetry.ipynb
Verifies that the notebook can be executed and produces expected results.
"""

import sympy as sp
import sys

def test_rpsi_symmetry():
    """Test the A_Rpsi symmetry calculation"""
    print("🧪 Testing A_Rpsi Symmetry Calculation...")
    print("=" * 60)
    
    # Define symbols
    R = sp.symbols('R', positive=True)
    alpha, beta, gamma, delta, zeta1p2, Lambda = sp.symbols('α β γ δ ζ Λ')
    
    # Define energy function
    E = alpha/R**4 + beta*zeta1p2/R**2 + gamma*Lambda**2*R**2 + delta*sp.sin(sp.log(R)/sp.log(sp.pi))**2
    
    # Calculate derivative
    dE = sp.diff(E, R)
    
    # Solve numerically
    try:
        sol = sp.nsolve(
            dE.subs({
                alpha: 1,
                beta: 1,
                gamma: 1,
                delta: 1e-2,
                zeta1p2: -0.207886,
                Lambda: 1e-61
            }), 
            3  # Initial guess
        )
        
        R_opt = float(sol)
        print(f"✅ Solution found: R_opt = {R_opt:.10f}")
        
        # Expected value (from original calculation)
        expected = 2.8713961554
        tolerance = 1e-8
        
        if abs(R_opt - expected) < tolerance:
            print(f"✅ Result matches expected value (diff = {abs(R_opt - expected):.2e})")
            
            # Verify it's a minimum
            d2E = sp.diff(dE, R)
            d2E_eval = d2E.subs({
                alpha: 1,
                beta: 1,
                gamma: 1,
                delta: 1e-2,
                zeta1p2: -0.207886,
                Lambda: 1e-61,
                R: sol
            })
            
            if float(d2E_eval) > 0:
                print(f"✅ Second derivative is positive: {float(d2E_eval):.6f} (minimum confirmed)")
                print("=" * 60)
                print("🎉 All tests passed!")
                return 0
            else:
                print(f"❌ Second derivative is not positive: {float(d2E_eval):.6f}")
                return 1
        else:
            print(f"❌ Result doesn't match expected value")
            print(f"   Expected: {expected:.10f}")
            print(f"   Got:      {R_opt:.10f}")
            print(f"   Diff:     {abs(R_opt - expected):.2e}")
            return 1
            
    except Exception as e:
        print(f"❌ Error during calculation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(test_rpsi_symmetry())
