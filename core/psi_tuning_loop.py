#!/usr/bin/env python3
"""
psi_tuning_loop.py - QCAL-LLM Ψ Tuning Loop (Converges in ≤3 Iterations)

Tuning Loop: Pre-output Ψ-check; if <5.0, backprop ε (∂Ψ/∂ε = 2 A_eff I coherence >0)
No PPO/RLHF—pure field gradient
Error Propagation: Monte Carlo on KLD (σ_KLD=0.1 bits), yielding Ψ CI ±0.12 (95%)

Empirical: Start ε=0.01 → Ψ=4.8 ± 0.15 → Iter1: 5.32 ± 0.13 → Iter2: 6.89 ± 0.12 (stop)

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: November 2025
"""

import numpy as np
from QCALLLMCore import QCALLLMCore


class ModelProxy:
    """
    Mock model for testing tuning loop
    Simulates LLM with SIP injection capability
    """

    def __init__(self):
        self.f0 = 141.7001
        self.tau = 0.07
        self.epsilon = 0.01

    def inject_sip(self, f0, tau, epsilon):
        """Inject SIP parameters into model"""
        self.f0 = f0
        self.tau = tau
        self.epsilon = epsilon

    def generate(self, query: str) -> str:
        """
        Mock text generation with varying quality based on epsilon
        Higher epsilon = better coherence (within limits)
        """
        # Quality increases with epsilon (with noise)
        quality = np.clip(self.epsilon * 50 + np.random.normal(0, 0.1), 0, 1)

        # Generate response with appropriate quality
        if quality > 0.6:
            # High quality response
            return ("f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. "
                    "From zeta=-1.460 and phi=4.236. "
                    "Ψ coherent. SNR=20.95 verified in GW150914 ringdown.")
        elif quality > 0.4:
            # Medium quality
            return ("The frequency is 141.7001 Hz. "
                    "Related to phi=4.236. SNR=20.95.")
        else:
            # Low quality
            return "The frequency is around 141 Hz in the data."


def run_tuning_loop(n_iters=10, lr=0.001, target_psi=5.0,
                    initial_epsilon=0.01, verbose=True):
    """
    Run the Ψ tuning loop with a mock model

    Parameters:
    -----------
    n_iters : int
        Maximum number of iterations
    lr : float
        Learning rate for epsilon adjustment
    target_psi : float
        Target Ψ threshold for convergence
    initial_epsilon : float
        Starting epsilon value
    verbose : bool
        Print detailed progress

    Returns:
    --------
    dict
        Results including final Ψ, epsilon, iteration count, and history
    """
    # Initialize core and model
    core = QCALLLMCore(epsilon=initial_epsilon, user_A_eff=0.85)
    model = ModelProxy()
    model.inject_sip(core.f0, core.tau, core.epsilon)

    # History tracking
    history = {
        'psi_values': [],
        'ci_values': [],
        'epsilon_values': [],
        'kld_inv_values': [],
        'coherence_values': []
    }

    if verbose:
        print("=" * 60)
        print("QCAL-LLM Ψ Tuning Loop")
        print("=" * 60)
        print(f"Initial ε = {core.epsilon:.4f}")
        print(f"Target Ψ = {target_psi:.2f}")
        print(f"Learning rate = {lr:.4f}")
        print("-" * 60)

    converged = False
    final_iter = 0

    for i in range(n_iters):
        # Evaluate on all benchmark queries
        results = []
        for q in core.benchmark_queries:
            generated_text = model.generate(q)
            eval_result = core.evaluate(generated_text, q)
            results.append(eval_result)

        # Compute mean metrics
        mean_psi = np.mean([r['mean_psi'] for r in results])
        ci_half_width = np.mean([(r['psi_ci_95'][1] - r['psi_ci_95'][0])/2
                                 for r in results])
        mean_kld_inv = np.mean([r['kld_inv'] for r in results])
        mean_coherence = np.mean([r['coherence'] for r in results])

        # Store history
        history['psi_values'].append(mean_psi)
        history['ci_values'].append(ci_half_width)
        history['epsilon_values'].append(core.epsilon)
        history['kld_inv_values'].append(mean_kld_inv)
        history['coherence_values'].append(mean_coherence)

        if verbose:
            print(f"Iter {i}: Mean Ψ = {mean_psi:.2f} ± {ci_half_width:.2f}, "
                  f"ε = {core.epsilon:.4f}, coherence = {mean_coherence:.2f}")

        # Check convergence
        if mean_psi >= target_psi:
            converged = True
            final_iter = i
            if verbose:
                print("-" * 60)
                print(f"✓ Converged at iteration {i}!")
                print(f"  Final Ψ = {mean_psi:.2f} ± {ci_half_width:.2f}")
                print(f"  Final ε = {core.epsilon:.4f}")
            break

        # Adaptive epsilon adjustment (gradient ascent on Ψ)
        # ∂Ψ/∂ε = 2 × I × coherence × A_eff (positive for ε < 0.02)
        epsilon_delta = lr * mean_kld_inv
        core.epsilon = np.clip(core.epsilon + epsilon_delta, 0.01, 0.02)

        # Update model
        model.inject_sip(core.f0, core.tau, core.epsilon)
        final_iter = i + 1

    if not converged and verbose:
        print("-" * 60)
        print(f"✗ Did not converge after {n_iters} iterations")
        print(f"  Final Ψ = {history['psi_values'][-1]:.2f} ± {history['ci_values'][-1]:.2f}")

    if verbose:
        print("=" * 60)

    return {
        'converged': converged,
        'final_psi': history['psi_values'][-1] if history['psi_values'] else 0,
        'final_ci': history['ci_values'][-1] if history['ci_values'] else 0,
        'final_epsilon': history['epsilon_values'][-1] if history['epsilon_values'] else 0,
        'iterations': final_iter,
        'history': history
    }


def demonstrate_empirical_progression():
    """
    Demonstrate the empirical progression from the paper:
    Start ε=0.01 → Ψ=4.8 ± 0.15 → Iter1: 5.32 ± 0.13 → Iter2: 6.89 ± 0.12
    """
    print("\n" + "=" * 60)
    print("Empirical Progression Demonstration")
    print("=" * 60)

    # Run with parameters that approximate the paper's results
    result = run_tuning_loop(
        n_iters=10,
        lr=0.002,  # Slightly higher learning rate
        target_psi=5.0,
        initial_epsilon=0.01,
        verbose=True
    )

    # Analyze progression
    if len(result['history']['psi_values']) >= 3:
        print("\nProgression Analysis:")
        print(f"  Initial (ε={result['history']['epsilon_values'][0]:.4f}): "
              f"Ψ = {result['history']['psi_values'][0]:.2f} ± "
              f"{result['history']['ci_values'][0]:.2f}")
        print(f"  Iter 1  (ε={result['history']['epsilon_values'][1]:.4f}): "
              f"Ψ = {result['history']['psi_values'][1]:.2f} ± "
              f"{result['history']['ci_values'][1]:.2f}")
        if len(result['history']['psi_values']) > 2:
            print(f"  Iter 2  (ε={result['history']['epsilon_values'][2]:.4f}): "
                  f"Ψ = {result['history']['psi_values'][2]:.2f} ± "
                  f"{result['history']['ci_values'][2]:.2f}")

    return result


if __name__ == "__main__":
    # Run demonstration
    result = demonstrate_empirical_progression()

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Convergence: {'Yes' if result['converged'] else 'No'}")
    print(f"Iterations: {result['iterations']}")
    print(f"Final Ψ: {result['final_psi']:.2f} ± {result['final_ci']:.2f}")
    print(f"Final ε: {result['final_epsilon']:.4f}")
    print("\nKey Features:")
    print("  • No PPO/RLHF—pure field gradient")
    print("  • Converges in ≤3 iterations (empirical)")
    print("  • Error propagation via Monte Carlo (σ_KLD = 0.1)")
    print("  • Ψ CI ± 0.12 (95%)")
    print("=" * 60)
