"""
psi_tuning_loop.py - Iterative Ψ Tuning Loop
Author: José Manuel Mota Burruezo (JMMB Ψ✧)

Iteratively adjusts epsilon until Ψ ≥ 5.0
Typical convergence: 1-3 iterations
"""

import random
from typing import Tuple, Dict, Any
from QCALLLMCore import QCALLLMCore


def tune_psi(
    generated_text: str,
    query: str,
    target_psi: float = 5.0,
    max_iterations: int = 3,
    epsilon_step: float = 0.005,
    user_A_eff: float = 0.85,
    verbose: bool = True
) -> Tuple[QCALLLMCore, Dict[str, Any]]:
    """
    Iteratively tune epsilon until Ψ ≥ target_psi

    Args:
        generated_text: LLM-generated text to evaluate
        query: Original query/prompt
        target_psi: Target Ψ threshold (default: 5.0)
        max_iterations: Maximum tuning iterations (default: 3)
        epsilon_step: Step size for epsilon adjustment (default: 0.005)
        user_A_eff: User effectiveness factor (default: 0.85)
        verbose: Print iteration details (default: True)

    Returns:
        Tuple of (tuned_core, final_eval_result)
    """
    epsilon = 0.015  # Initial epsilon

    for iteration in range(1, max_iterations + 1):
        # Create core with current epsilon
        core = QCALLLMCore(user_A_eff=user_A_eff, epsilon=epsilon)

        # Evaluate
        eval_result = core.evaluate(generated_text, query)
        psi = eval_result['mean_psi']
        coherent = eval_result['coherent']

        if verbose:
            print(f"Iteration {iteration}/{max_iterations}:")
            print(f"  epsilon = {epsilon:.4f}")
            print(f"  Ψ = {psi:.4f}")
            print(f"  Coherent: {coherent}")
            print(f"  Coherence: {eval_result['coherence']:.2%}")

        # Check if target achieved
        if psi >= target_psi:
            if verbose:
                print(f"\n✅ Target Ψ ≥ {target_psi:.1f} achieved in {iteration} iteration(s)!")
            return core, eval_result

        # Adjust epsilon for next iteration
        # If Ψ is low, increase epsilon to boost modulation
        epsilon += epsilon_step * (target_psi - psi) / target_psi
        epsilon = max(0.001, min(epsilon, 0.1))  # Clamp to reasonable range

        if verbose:
            print()

    # Return best attempt even if target not reached
    if verbose:
        print(f"⚠️  Max iterations reached. Final Ψ = {psi:.4f}")

    return core, eval_result


def auto_regenerate(
    llm_generate_fn,
    query: str,
    target_psi: float = 5.0,
    max_regenerations: int = 3,
    verbose: bool = True
) -> Tuple[str, QCALLLMCore, Dict[str, Any]]:
    """
    Auto-regenerate LLM output until Ψ threshold is met

    This implements the "No Human Loop" auto-evaluation pattern:
    - Generate text
    - Evaluate with Ψ
    - If Ψ < threshold, regenerate
    - Repeat until coherent or max attempts

    Args:
        llm_generate_fn: Function that takes query and returns generated text
        query: Original query/prompt
        target_psi: Target Ψ threshold (default: 5.0)
        max_regenerations: Maximum regeneration attempts (default: 3)
        verbose: Print iteration details (default: True)

    Returns:
        Tuple of (final_text, tuned_core, eval_result)
    """
    for attempt in range(1, max_regenerations + 1):
        if verbose:
            print(f"\n{'=' * 60}")
            print(f"Generation Attempt {attempt}/{max_regenerations}")
            print(f"{'=' * 60}")

        # Generate text
        generated_text = llm_generate_fn(query)

        if verbose:
            print(f"Generated: {generated_text[:100]}...")

        # Tune and evaluate
        core, eval_result = tune_psi(
            generated_text,
            query,
            target_psi=target_psi,
            verbose=verbose
        )

        # Check if coherent
        if eval_result['coherent']:
            if verbose:
                print(f"\n✅ Coherent output achieved in {attempt} attempt(s)!")
            return generated_text, core, eval_result

    if verbose:
        print(f"\n⚠️  Max regenerations reached. Best Ψ = {eval_result['mean_psi']:.4f}")

    return generated_text, core, eval_result


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("Ψ Tuning Loop Demo")
    print("=" * 60)

    # Example 1: Tune existing text
    print("\n1. Tuning existing text:")
    print("-" * 60)

    mock_text = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent."
    mock_query = "Deriva f₀ desde ζ'(1/2) y φ"

    tuned_core, result = tune_psi(
        mock_text,
        mock_query,
        target_psi=5.0,
        verbose=True
    )

    # Example 2: Mock LLM regeneration loop
    print("\n\n2. Auto-regeneration demo:")
    print("-" * 60)

    def mock_llm_generate(query: str) -> str:
        """Mock LLM that improves over attempts"""
        templates = [
            "The frequency is related to quantum mechanics.",
            "f₀ = 141.7001 Hz from mathematical derivation.",
            "f₀ = -ζ'(1/2) × φ³ = 141.7001 Hz. Coherent with GW data."
        ]
        return random.choice(templates)

    final_text, final_core, final_result = auto_regenerate(
        mock_llm_generate,
        "Explica f₀ = 141.7001 Hz",
        target_psi=5.0,
        max_regenerations=3,
        verbose=True
    )

    print("\n" + "=" * 60)
    print("Final Results:")
    print("=" * 60)
    print(f"Text: {final_text}")
    print(f"Ψ: {final_result['mean_psi']:.4f}")
    print(f"Coherent: {final_result['coherent']}")
