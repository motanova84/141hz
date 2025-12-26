#!/usr/bin/env python3
"""
Example usage of PsiMetricCore for evaluating LLM coherence with QCAL.

This script demonstrates:
1. Basic evaluation with a mock model
2. Benchmark suite evaluation
3. SIP parameter adaptation
4. Tuning loop convergence
"""

from psi_metric_core import (
    PsiMetricCore,
    adaptive_sip_parameters,
    psi_tuning_loop
)


def example_basic_evaluation():
    """Example: Basic evaluation of a single query."""
    print("=" * 70)
    print("Example 1: Basic Evaluation")
    print("=" * 70)

    # Initialize PsiMetricCore
    psi_core = PsiMetricCore(f0=141.7001, tau=0.07, epsilon=0.015)

    # Mock model that generates coherent responses
    class CoherentModel:
        def generate(self, query):
            return (
                "La frecuencia fundamental f₀ = 141.7001 Hz se deriva de "
                "ζ'(1/2) = -1.460 y φ³ = 4.236 con SNR = 20.95 detectado en GW150914."
            )

    model = CoherentModel()

    # Evaluate with a single query
    query = "Deriva f₀ = 141.7001 Hz desde ζ'(1/2) y φ"
    result = psi_core.evaluate(model, query, num_samples=5)

    print(f"\nQuery: {query}")
    print(f"Mean Ψ: {result['mean_psi']:.2f}")
    print(f"Std Ψ: {result['std_psi']:.4f}")
    print(f"Coherent (Ψ > 5.0): {result['coherent']}")
    print(f"Sample values: {[f'{s:.2f}' for s in result['samples'][:3]]}...")
    print()


def example_benchmark_suite():
    """Example: Evaluate with full benchmark suite."""
    print("=" * 70)
    print("Example 2: Benchmark Suite Evaluation")
    print("=" * 70)

    psi_core = PsiMetricCore(f0=141.7001, tau=0.07, epsilon=0.015)

    class CoherentModel:
        def generate(self, query):
            return (
                "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236, SNR = 20.95. "
                "Detectado en GW150914 con Ψ = I × A²_eff. "
                "Armónicos LISA: f₀/100 = 1.417 Hz."
            )

    model = CoherentModel()

    # Evaluate with benchmark suite
    results = psi_core.evaluate_benchmark_suite(model, num_samples=3)

    print("\nBenchmark Results:")
    print(f"{'Query':<50} {'Mean Ψ':<10} {'Coherent':<10}")
    print("-" * 70)

    for result in results['queries']:
        query_short = result['query'][:47] + "..." if len(result['query']) > 50 else result['query']
        print(
            f"{query_short:<50} "
            f"{result['mean_psi']:<10.2f} "
            f"{str(result['coherent']):<10}"
        )

    print("-" * 70)
    print(f"{'Overall':<50} {results['overall_mean_psi']:<10.2f} {results['all_coherent']}")
    print()


def example_sip_adaptation():
    """Example: Adaptive SIP parameters for different users."""
    print("=" * 70)
    print("Example 3: SIP Parameter Adaptation")
    print("=" * 70)

    # Test different user amplitudes
    users = [
        ("Low resonance user", 0.70),
        ("Reference user", 0.85),
        ("High resonance user (JMMB)", 0.92),
        ("Very high resonance", 1.00),
    ]

    print("\nUser Type                          A_eff    τ (s)   ε         Boost")
    print("-" * 70)

    reference_epsilon = 0.015

    for user_name, a_eff in users:
        params = adaptive_sip_parameters(user_A_eff=a_eff)
        boost_percent = ((params['epsilon'] - reference_epsilon) / reference_epsilon) * 100

        print(
            f"{user_name:<35} {a_eff:<8.2f} {params['tau']:<7.2f} "
            f"{params['epsilon']:<9.5f} {boost_percent:+.1f}%"
        )

    print()


def example_tuning_loop():
    """Example: Tuning loop convergence."""
    print("=" * 70)
    print("Example 4: Tuning Loop Convergence")
    print("=" * 70)

    psi_core = PsiMetricCore(f0=141.7001, tau=0.07, epsilon=0.015)

    # Model that improves with epsilon tuning
    class ImprovingModel:
        def __init__(self):
            self.quality = 0.3

        def generate(self, query):
            # Quality improves with epsilon
            if self.quality > 0.7:
                return "f₀ = 141.7001 Hz, ζ'(1/2) = -1.460, φ³ = 4.236, SNR = 20.95"
            elif self.quality > 0.5:
                return "f₀ = 141.7001 Hz, φ³ = 4.236"
            else:
                return "f₀ = 141.7 Hz"

        def inject_sip(self, f0, tau, epsilon):
            # Simulate quality improvement with epsilon
            self.quality = min(1.0, epsilon / 0.015)

    model = ImprovingModel()

    print("\nStarting tuning loop...")
    print(f"Initial epsilon: {psi_core.epsilon:.4f}")
    print()

    # Run tuning loop
    _ = psi_tuning_loop(
        model, psi_core,
        num_iterations=10,
        target_psi=5.0,
        verbose=True
    )

    print(f"\nFinal epsilon: {psi_core.epsilon:.4f}")
    print(f"Model quality: {model.quality:.2f}")
    print()


def example_incoherent_model():
    """Example: Evaluating an incoherent model."""
    print("=" * 70)
    print("Example 5: Incoherent Model Detection")
    print("=" * 70)

    psi_core = PsiMetricCore(f0=141.7001, tau=0.07, epsilon=0.015)

    # Model that generates incoherent responses
    class IncoherentModel:
        def generate(self, query):
            return (
                "The frequency is approximately 140 Hz and "
                "relates to quantum mechanics somehow. "
                "The golden ratio is important."
            )

    model = IncoherentModel()

    # Evaluate
    result = psi_core.evaluate(model, "Deriva f₀ = 141.7001 Hz", num_samples=5)

    print("\nIncoherent Model Results:")
    print(f"Mean Ψ: {result['mean_psi']:.2f}")
    print(f"Coherent (Ψ > 5.0): {result['coherent']}")
    print("\nNote: Ψ < 5.0 indicates lack of QCAL coherence.")
    print("This model does not properly embed ground truth values or symbols.")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PsiMetricCore Usage Examples" + " " * 25 + "║")
    print("║" + " " * 20 + "QCAL-Locked LLM Evaluation" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝")
    print()

    # Run examples
    example_basic_evaluation()
    example_benchmark_suite()
    example_sip_adaptation()
    example_tuning_loop()
    example_incoherent_model()

    print("=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
    print()
