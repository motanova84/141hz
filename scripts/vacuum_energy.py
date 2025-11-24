#!/usr/bin/env python3
"""
Vacuum Energy Optimization Module
Implements vacuum energy calculations for cosmological analysis
"""
import numpy as np
from scipy.optimize import minimize_scalar


# Physical constants for vacuum energy calculation
alpha = 1.0  # Planck energy term coefficient
beta = 1.0   # Zeta prime coupling coefficient
gamma = 1.0  # Cosmological constant coupling
delta = 1.0  # Oscillatory term amplitude
zeta_prime = -0.5  # Riemann zeta derivative parameter
Lambda = 1e-3  # Cosmological constant (normalized)
pi_val = np.pi  # Pi constant


def E_vac_log(log_r):
    """
    Calculate vacuum energy as a function of log(R/ℓ_P)
    
    This function implements a multi-term vacuum energy model that includes:
    - Planck-scale corrections (1/R^4 term)
    - Quantum corrections via zeta function (1/R^2 term)
    - Cosmological constant contribution (R^2 term)
    - Oscillatory quantum corrections (sin^2 term)
    
    Parameters
    ----------
    log_r : float
        Logarithm (base 10) of the radius in Planck length units: log10(R/ℓ_P)
    
    Returns
    -------
    float
        Total vacuum energy E_vac at the given radius scale
    
    Notes
    -----
    The energy has four contributions:
    1. term1: alpha / R^4  - Planck-scale quantum corrections
    2. term2: beta * zeta_prime / R^2  - Renormalization corrections
    3. term3: gamma * Lambda^2 * R^2  - Cosmological constant energy
    4. term4: delta * sin^2(log(R)/log(pi))  - Oscillatory quantum effects
    
    The minimum of this function represents the equilibrium radius scale
    where vacuum energy is minimized.
    """
    # Ensure log_r is a float for numpy operations
    log_r = float(log_r)
    R = 10**log_r  # R / ℓ_P (radius in Planck length units)
    
    # Term 1: Planck-scale corrections (dominant at small R)
    term1 = alpha / R**4
    
    # Term 2: Quantum corrections via zeta function derivative
    term2 = beta * zeta_prime / R**2
    
    # Term 3: Cosmological constant contribution (dominant at large R)
    term3 = gamma * Lambda**2 * R**2
    
    # Term 4: Oscillatory quantum corrections
    term4 = delta * np.sin(np.log(R) / np.log(pi_val))**2
    
    return term1 + term2 + term3 + term4


def optimize_vacuum_energy(bounds=(40, 50), method='bounded'):
    """
    Find the radius that minimizes vacuum energy
    
    Parameters
    ----------
    bounds : tuple of float, optional
        Bounds for log10(R/ℓ_P) optimization range, default (40, 50)
    method : str, optional
        Optimization method for minimize_scalar, default 'bounded'
    
    Returns
    -------
    result : OptimizeResult
        Optimization result containing:
        - x: optimal log10(R/ℓ_P)
        - fun: minimum vacuum energy
        - success: whether optimization succeeded
        - message: description of convergence
    
    Examples
    --------
    >>> result = optimize_vacuum_energy(bounds=(40, 50))
    >>> print(f"Optimal log(R): {result.x:.4f}")
    >>> print(f"Minimum energy: {result.fun:.6e}")
    """
    res = minimize_scalar(E_vac_log, bounds=bounds, method=method)
    return res


def analyze_vacuum_energy(log_r_range=None):
    """
    Analyze vacuum energy across a range of radius scales
    
    Parameters
    ----------
    log_r_range : array-like, optional
        Range of log10(R/ℓ_P) values to evaluate. If None, uses (40, 50)
    
    Returns
    -------
    dict
        Dictionary containing:
        - log_r_values: array of log10(R) values
        - energy_values: corresponding vacuum energies
        - optimum: optimization result at minimum
        - analysis: dictionary with detailed term contributions at optimum
    """
    if log_r_range is None:
        log_r_range = np.linspace(40, 50, 1000)
    
    # Calculate energy across range
    energy_values = np.array([E_vac_log(log_r) for log_r in log_r_range])
    
    # Find optimum
    optimum = optimize_vacuum_energy(bounds=(log_r_range[0], log_r_range[-1]))
    
    # Calculate individual term contributions at optimum
    R_opt = 10**optimum.x
    analysis = {
        'log_r_opt': optimum.x,
        'R_opt': R_opt,
        'E_min': optimum.fun,
        'term1_planck': alpha / R_opt**4,
        'term2_quantum': beta * zeta_prime / R_opt**2,
        'term3_lambda': gamma * Lambda**2 * R_opt**2,
        'term4_oscillatory': delta * np.sin(np.log(R_opt) / np.log(pi_val))**2
    }
    
    return {
        'log_r_values': log_r_range,
        'energy_values': energy_values,
        'optimum': optimum,
        'analysis': analysis
    }


def main():
    """Main execution function for demonstration"""
    print("=" * 70)
    print("VACUUM ENERGY OPTIMIZATION")
    print("=" * 70)
    print()
    
    print("Physical Parameters:")
    print(f"  alpha (Planck term):        {alpha}")
    print(f"  beta (quantum coupling):    {beta}")
    print(f"  gamma (Lambda coupling):    {gamma}")
    print(f"  delta (oscillatory):        {delta}")
    print(f"  zeta_prime:                 {zeta_prime}")
    print(f"  Lambda (cosmological):      {Lambda}")
    print(f"  pi_val:                     {pi_val:.6f}")
    print()
    
    # Optimize vacuum energy
    print("Optimizing vacuum energy in range log(R) ∈ [40, 50]...")
    res = optimize_vacuum_energy(bounds=(40, 50))
    
    print()
    print("Optimization Results:")
    print(f"  Optimal log(R/ℓ_P):         {res.x:.6f}")
    print(f"  Optimal R/ℓ_P:              10^{res.x:.2f}")
    print(f"  Minimum energy:             {res.fun:.6e}")
    print(f"  Optimization success:       {res.success}")
    print(f"  Message:                    {res.message}")
    print()
    
    # Detailed analysis
    print("Detailed Analysis at Optimum:")
    analysis = analyze_vacuum_energy()
    details = analysis['analysis']
    
    R_opt = details['R_opt']
    print(f"  Radius (Planck units):      {R_opt:.6e}")
    print(f"  Total energy:               {details['E_min']:.6e}")
    print()
    print("  Energy Contributions:")
    print(f"    Planck term (α/R⁴):       {details['term1_planck']:.6e}")
    print(f"    Quantum term (βζ'/R²):    {details['term2_quantum']:.6e}")
    print(f"    Lambda term (γΛ²R²):      {details['term3_lambda']:.6e}")
    print(f"    Oscillatory (δsin²):      {details['term4_oscillatory']:.6e}")
    print()
    
    # Calculate relative contributions
    total = abs(details['E_min'])
    if total > 0:
        print("  Relative Contributions (%):")
        print(f"    Planck term:              {abs(details['term1_planck'])/total*100:.2f}%")
        print(f"    Quantum term:             {abs(details['term2_quantum'])/total*100:.2f}%")
        print(f"    Lambda term:              {abs(details['term3_lambda'])/total*100:.2f}%")
        print(f"    Oscillatory:              {abs(details['term4_oscillatory'])/total*100:.2f}%")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
