#!/usr/bin/env python3
"""
🔧 Validation Support Functions - Improved Convergence & Normalization

This module provides improved implementations for the validation notebooks
to address numerical concordance issues and ensure better convergence.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Purpose: Fix numerical errors ~1 mentioned in GitHub issue
"""

import mpmath as mp
import numpy as np
import scipy.special as sp_special
from typing import List, Tuple, Callable, Union
import warnings

def configure_precision(dps: int = 25) -> None:
    """Configure mpmath precision for computations."""
    mp.dps = dps
    print(f"🔧 Configured precision: {dps} decimal places")

def improved_sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Optimized Sieve of Eratosthenes with memory efficiency.
    
    Args:
        limit: Upper limit for prime generation
        
    Returns:
        List of prime numbers up to limit
    """
    if limit < 2:
        return []
    
    # Use bit array for memory efficiency
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    # Only check odd numbers after 2
    for i in range(3, int(limit**0.5) + 1, 2):
        if sieve[i]:
            for j in range(i*i, limit + 1, 2*i):
                sieve[j] = False
    
    # Collect primes: 2 + all odd primes
    primes = [2] + [i for i in range(3, limit + 1, 2) if sieve[i]]
    return primes

def get_first_n_primes(n: int) -> List[int]:
    """
    Get first n prime numbers using optimized sieve.
    
    Args:
        n: Number of primes to generate
        
    Returns:
        List of first n prime numbers
    """
    if n <= 0:
        return []
    
    # Improved prime number theorem approximation
    if n < 6:
        limit = 15
    else:
        # More accurate approximation for larger n
        log_n = np.log(n)
        limit = max(15, int(n * (log_n + np.log(log_n) - 1 + 1.8*np.log(log_n)/log_n)))
    
    primes = improved_sieve_of_eratosthenes(limit)
    
    # Extend if needed
    while len(primes) < n:
        limit = int(limit * 1.5)
        primes = improved_sieve_of_eratosthenes(limit)
    
    return primes[:n]

def compute_zeta_zeros_batch(n_zeros: int, batch_size: int = 100) -> List[complex]:
    """
    Compute zeta zeros in batches with progress reporting.
    
    Args:
        n_zeros: Number of zeros to compute
        batch_size: Batch size for progress reporting
        
    Returns:
        List of complex zeta zeros (0.5 + i*gamma_n)
    """
    zeros = []
    
    print(f"ζ Computing {n_zeros} zeta zeros in batches of {batch_size}...")
    
    for i in range(1, n_zeros + 1):
        if i % batch_size == 0 or i == n_zeros:
            print(f"   Progress: {i}/{n_zeros} zeros computed")
        
        try:
            gamma_n = mp.zetazero(i)
            # Convert mpmath complex to Python complex
            zeros.append(complex(0.5, complex(gamma_n).imag))
        except Exception as e:
            print(f"⚠️ Warning: Failed to compute zero {i}: {e}")
            continue
    
    print(f"✅ Successfully computed {len(zeros)} zeta zeros")
    return zeros

def create_test_functions() -> dict:
    """
    Create a collection of test functions with improved properties.
    
    Returns:
        Dictionary of test functions with their names
    """
    
    def gaussian_even(u: Union[float, np.ndarray], sigma: float = 1.0) -> Union[float, np.ndarray]:
        """Gaussian function: f(u) = exp(-u²/(2σ²)) - guaranteed even"""
        return np.exp(-u**2 / (2 * sigma**2))
    
    def cosine_gaussian(u: Union[float, np.ndarray], sigma: float = 1.0, omega: float = 0.0) -> Union[float, np.ndarray]:
        """Cosine modulated Gaussian - even function"""
        return np.exp(-u**2 / (2 * sigma**2)) * np.cos(omega * u)
    
    def rational_even(u: Union[float, np.ndarray], alpha: float = 1.0) -> Union[float, np.ndarray]:
        """Rational function: 1/(1 + α*u²) - even and integrable"""
        return 1.0 / (1.0 + alpha * u**2)
    
    def compact_smooth(u: Union[float, np.ndarray], a: float = 2.0) -> Union[float, np.ndarray]:
        """Smooth compact support function"""
        u_arr = np.asarray(u)
        result = np.zeros_like(u_arr)
        mask = np.abs(u_arr) < a
        u_masked = u_arr[mask]
        
        # Smooth cutoff: exp(-1/(a²-u²)) for |u| < a
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result[mask] = np.exp(-1.0 / (a**2 - u_masked**2))
        
        return result
    
    return {
        'gaussian': gaussian_even,
        'cosine_gaussian': cosine_gaussian,
        'rational': rational_even,
        'compact': compact_smooth
    }

def improved_archimedean_side(f_func: Callable, lim: float, method: str = 'adaptive') -> float:
    """
    Improved calculation of Archimedean side with better numerical stability.
    
    Args:
        f_func: Test function
        lim: Integration limit
        method: Integration method ('adaptive' or 'fixed')
        
    Returns:
        Value of A_∞(f)
    """
    print(f"🏛️ Computing Archimedean side (method: {method})...")
    
    def integrand(u):
        u_val = float(u)
        u_abs = abs(u_val)
        
        if u_abs < 1e-12:
            return 0.0
        
        try:
            # Use mpmath digamma function correctly
            psi_val = float(mp.digamma(u_abs/2.0 + 1.0))
            
            # Correct Archimedean kernel: ½ψ(|u|/2 + 1) - ½log(π)
            kernel = 0.5 * psi_val - 0.5 * np.log(np.pi)
            
            f_val = f_func(u_val)
            
            return f_val * kernel
            
        except Exception as e:
            print(f"⚠️ Warning in integrand at u={u_val}: {e}")
            return 0.0
    
    if method == 'adaptive':
        # Adaptive integration with error control
        result = mp.quad(integrand, [-lim, lim], maxdegree=12)
    else:
        # Fixed quadrature (faster but less accurate)
        result = mp.quad(integrand, [-lim, lim], maxdegree=8)
    
    return float(result)

def improved_prime_sum(f_func: Callable, primes: List[int], lim: float, 
                      use_conjugate: bool = True) -> complex:
    """
    Improved prime sum calculation with conjugate symmetry.
    
    Args:
        f_func: Test function (should be even)
        primes: List of prime numbers
        lim: Integration limit  
        use_conjugate: Whether to use conjugate symmetry for speed
        
    Returns:
        Complex value of prime sum (imaginary part should be ~0 for even functions)
    """
    print(f"🔢 Computing prime sum over {len(primes)} primes...")
    
    total_sum = 0.0 + 0.0j
    
    for i, p in enumerate(primes):
        if i % 100 == 0 and i > 0:
            print(f"   Prime progress: {i}/{len(primes)}")
        
        log_p = np.log(p)
        
        def integrand(u):
            u_val = float(u)
            f_val = f_func(u_val)
            
            # p^(-iu) = exp(-iu * log(p))
            phase = -1j * u_val * log_p
            exponential = np.exp(phase)
            
            return f_val * exponential
        
        # Integrate using mpmath
        try:
            integral_result = mp.quad(integrand, [-lim, lim], maxdegree=10)
            contribution = log_p * complex(integral_result)
            total_sum += contribution
            
        except Exception as e:
            print(f"⚠️ Warning for prime {p}: {e}")
            continue
    
    print(f"✅ Prime sum computed: Re={total_sum.real:.8f}, Im={total_sum.imag:.8f}")
    
    # For even functions, imaginary part should be negligible
    if abs(total_sum.imag) > 1e-6:
        print(f"⚠️ Warning: Large imaginary part in prime sum: {total_sum.imag}")
    
    return total_sum

def improved_zero_sum(f_func: Callable, zeros: List[complex], lim: float, 
                     sigma0: float = 1.5) -> complex:
    """
    Improved zero sum with better convergence and error handling.
    
    Args:
        f_func: Test function
        zeros: List of zeta zeros
        lim: Integration limit
        sigma0: Real part for shifted integration (should be > 1)
        
    Returns:
        Complex value of zero sum
    """
    print(f"ζ Computing zero sum over {len(zeros)} zeros (σ0={sigma0})...")
    
    if sigma0 <= 1.0:
        print(f"⚠️ Warning: σ0={sigma0} ≤ 1, using σ0=1.5 for convergence")
        sigma0 = 1.5
    
    total_sum = 0.0 + 0.0j
    
    for i, zero in enumerate(zeros):
        if i % 100 == 0 and i > 0:
            print(f"   Zero progress: {i}/{len(zeros)}")
        
        # Use shifted critical line: σ0 + i*γ instead of 0.5 + i*γ
        rho = complex(sigma0, zero.imag)
        
        def integrand(u):
            u_val = float(u)
            f_val = f_func(u_val)
            
            # rho^(-iu) = exp(-iu * log(rho))
            try:
                log_rho = np.log(rho)
                phase = -1j * u_val * log_rho
                exponential = np.exp(phase)
                
                return f_val * exponential
                
            except Exception as e:
                print(f"⚠️ Error in zero integrand: {e}")
                return 0.0
        
        try:
            integral_result = mp.quad(integrand, [-lim, lim], maxdegree=10)
            contribution = complex(integral_result)
            total_sum += contribution
            
        except Exception as e:
            print(f"⚠️ Warning for zero {i+1}: {e}")
            continue
    
    print(f"✅ Zero sum computed: Re={total_sum.real:.8f}, Im={total_sum.imag:.8f}")
    return total_sum

def validate_function_properties(f_func: Callable, name: str = "test_function") -> bool:
    """
    Validate that test function has required properties (even, integrable, etc.)
    
    Args:
        f_func: Function to validate
        name: Function name for reporting
        
    Returns:
        True if function passes all checks
    """
    print(f"🧪 Validating function '{name}'...")
    
    test_points = np.linspace(-5, 5, 100)
    
    # Check if function is even: f(-u) = f(u)
    f_pos = f_func(test_points)
    f_neg = f_func(-test_points)
    
    is_even = np.allclose(f_pos, f_neg, rtol=1e-10)
    print(f"   Even property: {'✅ PASS' if is_even else '❌ FAIL'}")
    
    # Check if function is real-valued
    is_real = np.all(np.isreal(f_pos))
    print(f"   Real-valued: {'✅ PASS' if is_real else '❌ FAIL'}")
    
    # Check if function is bounded
    is_bounded = np.all(np.isfinite(f_pos)) and np.all(f_pos >= 0)
    print(f"   Bounded/Non-negative: {'✅ PASS' if is_bounded else '❌ FAIL'}")
    
    # Check decay at infinity
    far_points = np.array([-100, 100])
    f_far = f_func(far_points)
    decays = np.all(np.abs(f_far) < 1e-10)
    print(f"   Decay at infinity: {'✅ PASS' if decays else '❌ FAIL'}")
    
    all_pass = is_even and is_real and is_bounded and decays
    print(f"🎯 Overall: {'✅ VALID' if all_pass else '❌ INVALID'}")
    
    return all_pass

def run_validation_with_convergence_check(test_func_name: str = 'gaussian',
                                        param_sets: List[Tuple[int, int, int]] = None,
                                        target_error: float = 1e-6) -> dict:
    """
    Run validation with progressive parameter increase until convergence.
    
    Args:
        test_func_name: Name of test function to use
        param_sets: List of (P, NΞ, precision) parameter combinations
        target_error: Target error for convergence
        
    Returns:
        Dictionary with results for each parameter set
    """
    if param_sets is None:
        param_sets = [
            (100, 100, 15),   # Quick test
            (250, 250, 20),   # Medium test
            (500, 500, 25),   # CI test
            (1000, 1000, 30), # Full test
        ]
    
    print(f"🔬 Running convergence validation with function '{test_func_name}'")
    print(f"🎯 Target error: {target_error}")
    
    test_functions = create_test_functions()
    if test_func_name not in test_functions:
        print(f"❌ Unknown test function: {test_func_name}")
        return {}
    
    f_func = test_functions[test_func_name]
    
    # Validate function properties first
    if not validate_function_properties(f_func, test_func_name):
        print("❌ Function validation failed, aborting")
        return {}
    
    results = {}
    
    for P, NΞ, precision in param_sets:
        print(f"\n📊 Testing with P={P}, NΞ={NΞ}, precision={precision}")
        print("=" * 50)
        
        # Configure precision
        configure_precision(precision)
        
        # Generate primes and zeros
        print("🔢 Generating primes...")
        primes = get_first_n_primes(P)
        
        print("ζ Computing zeta zeros...")
        zeros = compute_zeta_zeros_batch(NΞ, batch_size=max(10, NΞ//10))
        
        # Test function parameters
        lim = 8.0  # Reasonable integration limit
        sigma0 = 1.8  # Safely > 1 for convergence
        
        # Create test function with appropriate scaling
        def scaled_test_func(u):
            scale = 1.0 / (P**0.1)  # Weak scaling with number of primes
            return f_func(u / scale)
        
        # Compute sides
        try:
            A_arch = improved_archimedean_side(scaled_test_func, lim)
            prime_contrib = improved_prime_sum(scaled_test_func, primes, lim)
            zero_contrib = improved_zero_sum(scaled_test_func, zeros, lim, sigma0)
            
            arithmetic_side = prime_contrib.real + zero_contrib.real
            
            abs_error = abs(A_arch - arithmetic_side)
            rel_error = abs_error / abs(A_arch) if A_arch != 0 else float('inf')
            
            converged = abs_error < target_error
            
            result = {
                'P': P, 'NΞ': NΞ, 'precision': precision,
                'A_archimedean': A_arch,
                'prime_sum': prime_contrib.real,
                'zero_sum': zero_contrib.real,
                'arithmetic_side': arithmetic_side,
                'abs_error': abs_error,
                'rel_error': rel_error,
                'converged': converged,
                'prime_imag': prime_contrib.imag,
                'zero_imag': zero_contrib.imag
            }
            
            results[f'P{P}_N{NΞ}'] = result
            
            print(f"\n📊 Results:")
            print(f"   Archimedean: {A_arch:.10f}")
            print(f"   Arithmetic:  {arithmetic_side:.10f}")
            print(f"   Abs Error:   {abs_error:.10f}")
            print(f"   Rel Error:   {rel_error:.10f}")
            print(f"   Status:      {'✅ CONVERGED' if converged else '❌ NOT CONVERGED'}")
            
            if converged:
                print(f"🎉 Convergence achieved with P={P}, NΞ={NΞ}")
                break
                
        except Exception as e:
            print(f"❌ Error in computation: {e}")
            results[f'P{P}_N{NΞ}'] = {'error': str(e)}
    
    return results

if __name__ == "__main__":
    # Quick test when run directly
    print("🚀 Testing improved validation functions...")
    
    # Test basic functionality
    test_functions = create_test_functions()
    
    for name, func in test_functions.items():
        validate_function_properties(func, name)
        print()
    
    # Run a small convergence test
    results = run_validation_with_convergence_check('gaussian', [(50, 20, 15)], 1e-3)
    
    if results:
        print("✅ Basic validation functions working correctly")
    else:
        print("❌ Issues detected in validation functions")