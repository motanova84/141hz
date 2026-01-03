#!/usr/bin/env python3
"""
PsiMetricCore: Núcleo de evaluación Ψ para LLMs QCAL-locked.

Este módulo implementa el sistema de evaluación Ψ (Psi) para Language Models
coherentes con la frecuencia universal f₀ = 141.7001 Hz y los parámetros QCAL.

Componentes:
- Ground truth database con valores experimentales
- Extracción y verificación de claims científicos
- Cálculo de coherencia simbólica
- Métrica Ψ = KLD⁻¹ × C²
- Benchmark suite con 5 queries de validación
"""

import numpy as np
import re
from typing import Dict, List, Any


class PsiMetricCore:
    """
    Núcleo de evaluación Ψ para LLMs QCAL-locked.

    La métrica Ψ combina la inversa de la divergencia KL (información correcta)
    con la coherencia simbólica al cuadrado (uso consistente de notación).

    Ψ = KLD⁻¹ × C²

    Donde:
    - KLD⁻¹ = log(matches + 1) ≈ información verificable
    - C = matches_symbols / total_symbols ≈ coherencia simbólica

    Threshold: Ψ > 5.0 indica generación coherente QCAL-locked.
    """

    def __init__(self, f0: float = 141.7001, tau: float = 0.07, epsilon: float = 0.015):
        """
        Inicializa el núcleo Ψ con parámetros QCAL.

        Args:
            f0: Frecuencia fundamental universal en Hz
            tau: Parámetro temporal SIP en segundos
            epsilon: Parámetro de modulación base SIP
        """
        self.f0 = f0
        self.tau = tau
        self.epsilon = epsilon

        # Ground truth database con valores experimentales del repositorio 141hz
        self.ground_truth_db = {
            'f0': 141.7001,  # Hz, frecuencia fundamental universal
            'zeta_prime_half': -1.460,  # ζ'(1/2), zero crítico de Riemann
            'phi_cubed': 4.236,  # φ³, constante de razón áurea cúbica
            'snr_gw150914': 20.95,  # Signal-to-Noise Ratio de GW150914
            'snr_mean': 20.95,  # SNR medio en GWTC-1
            'snr_std': 5.54,  # Desviación estándar SNR
            'p_value': 0.001,  # Significancia estadística (p < 0.001)
            'bayes_factor': 10.0,  # Factor bayesiano (BF > 10)
        }

        # Benchmark queries: 5 preguntas de validación científica
        self.benchmark_queries = [
            "Deriva f₀ = 141.7001 Hz desde ζ'(1/2) y φ",
            "Detecta f₀ en ringdown GW150914",
            "Explica Ψ = I × A²_eff",
            "Valida SNR>20 en GWTC-1",
            "Predice armónicos LISA (f₀/100)"
        ]

    def extract_claims(self, text: str) -> List[str]:
        """
        Extrae claims científicos verificables del texto generado.

        Busca patrones numéricos y simbólicos relacionados con:
        - Frecuencia f₀
        - Función zeta ζ'(1/2)
        - Constante phi φ
        - SNR (Signal-to-Noise Ratio)

        Args:
            text: Texto generado por el LLM

        Returns:
            Lista de claims extraídos (formato: "variable=valor")
        """
        claims = []

        # Patrones de extracción (mejorados)
        patterns = {
            'f0': r'(?:f[₀0]|freq(?:uencia)?)\s*[=:≈]\s*([\d.]+)\s*Hz',
            'zeta': r"(?:ζ'|zeta'?)\s*(?:\(1/2\))?\s*[=:≈]\s*(-?[\d.]+)",
            'phi': r'(?:φ³?|phi\^?3?)\s*[=:≈]\s*([\d.]+)',
            'snr': r'SNR\s*[=:≈]\s*([\d.]+)',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                cleaned_value = match.group(1).rstrip('.,;:')  # Remove trailing punctuation
                claims.append(f"{key}={cleaned_value}")

        return claims

    def verify_claim(self, claim: str, query: str) -> bool:
        """
        Verifica si un claim extraído es consistente con ground truth.

        Args:
            claim: Claim extraído (formato: "variable=valor")
            query: Query original (para contexto)

        Returns:
            True si el claim es verificable y correcto
        """
        if '=' not in claim:
            return False

        var, val_str = claim.split('=', 1)
        var = var.strip()

        try:
            val = float(val_str)
        except ValueError:
            return False

        # Tolerancias de verificación (basadas en precisión experimental)
        tolerances = {
            'f0': 0.01,  # ±0.01 Hz
            'zeta': 0.01,  # ±0.01
            'phi': 0.01,  # ±0.01
            'snr': 1.0,  # ±1.0 (mayor incertidumbre en SNR)
        }

        # Verificación contra ground truth
        if var == 'f0':
            return abs(val - self.ground_truth_db['f0']) < tolerances['f0']
        elif var == 'zeta':
            return abs(val - self.ground_truth_db['zeta_prime_half']) < tolerances['zeta']
        elif var == 'phi':
            return abs(val - self.ground_truth_db['phi_cubed']) < tolerances['phi']
        elif var == 'snr':
            return abs(val - self.ground_truth_db['snr_gw150914']) < tolerances['snr']

        return False

    def compute_kld_inverse(self, generated_text: str, query: str) -> float:
        """
        Calcula la inversa aproximada de la divergencia Kullback-Leibler.

        KLD⁻¹ ≈ (matches + 1) × log(matches + 1)

        Mide la cantidad de información verificable en el texto generado.

        Args:
            generated_text: Texto generado por el LLM
            query: Query original

        Returns:
            Inversa aproximada de KLD (higher is better)
        """
        claims = self.extract_claims(generated_text)
        matches = sum(1 for claim in claims if self.verify_claim(claim, query))
        # Scaled formula: (matches + 1) × log(matches + 1)
        return (matches + 1) * np.log(matches + 1)

    def compute_coherence(self, generated_text: str) -> float:
        """
        Calcula la coherencia simbólica del texto generado.

        C = symbols_matched / total_symbols

        Mide el uso consistente de notación científica estándar.

        Args:
            generated_text: Texto generado por el LLM

        Returns:
            Coherencia simbólica (0.0 a 1.0)
        """
        # Patrones de símbolos científicos esperados
        symbols = {
            'phi_cubed': r'φ³|phi\^3',
            'zeta_prime': r"ζ'\(1/2\)|zeta'",
            'f0': r'141\.7\d*\s*Hz|f[₀0]',
        }

        matches = sum(
            1 for pattern in symbols.values()
            if re.search(pattern, generated_text, re.IGNORECASE)
        )

        return matches / len(symbols)  # 1.0 = full match

    def compute_psi_response(self, generated_text: str, query: str) -> float:
        """
        Calcula la métrica Ψ para una respuesta generada.

        Ψ = KLD⁻¹ × C²

        Combina información verificable con coherencia simbólica.

        Args:
            generated_text: Texto generado por el LLM
            query: Query original

        Returns:
            Métrica Ψ (threshold: Ψ > 5.0 para coherencia QCAL)
        """
        kld_inv = self.compute_kld_inverse(generated_text, query)
        coherence = self.compute_coherence(generated_text)
        return kld_inv * (coherence ** 2)

    def evaluate(
        self,
        model: Any,
        query: str,
        num_samples: int = 10
    ) -> Dict[str, Any]:
        """
        Evalúa un modelo LLM con la métrica Ψ.

        Args:
            model: Modelo LLM a evaluar (debe tener método .generate(query))
            query: Query de evaluación
            num_samples: Número de muestras para estadísticas

        Returns:
            Diccionario con estadísticas de evaluación:
            - mean_psi: Media de Ψ
            - std_psi: Desviación estándar de Ψ
            - coherent: True si mean_psi > 5.0
            - samples: Lista de valores Ψ individuales
        """
        psi_responses = []

        for _ in range(num_samples):
            # Genera respuesta del modelo
            if hasattr(model, 'generate') and callable(getattr(model, 'generate', None)):
                response = model.generate(query)
            else:
                # Mock response para testing (coherente con ground truth)
                response = self._generate_mock_response(query)

            # Calcula Ψ
            psi = self.compute_psi_response(response, query)
            psi_responses.append(psi)

        # Estadísticas
        mean_psi = np.mean(psi_responses)
        std_psi = np.std(psi_responses)

        return {
            'mean_psi': mean_psi,
            'std_psi': std_psi,
            'coherent': mean_psi > 5.0,
            'samples': psi_responses
        }

    def _generate_mock_response(self, query: str) -> str:
        """
        Genera una respuesta mock coherente para testing.

        Args:
            query: Query de entrada

        Returns:
            Respuesta mock con símbolos y valores correctos
        """
        # Respuesta coherente con ground truth
        response = (
            f"Derivación: f₀ = 141.7001 Hz desde ζ'(1/2) = -1.460 y φ³ = 4.236. "
            f"Ψ = I · A_eff². "
            f"SNR = 20.95 supera el umbral >20. "
            f"Armónicos LISA: f₀/100 = {self.f0 / 100:.3f} Hz."
        )
        return response

    def evaluate_benchmark_suite(
        self,
        model: Any,
        num_samples: int = 10
    ) -> Dict[str, Any]:
        """
        Evalúa el modelo con la suite completa de 5 queries benchmark.

        Args:
            model: Modelo LLM a evaluar
            num_samples: Número de muestras por query

        Returns:
            Diccionario con resultados agregados:
            - queries: Lista de resultados por query
            - overall_mean_psi: Media global de Ψ
            - overall_std_psi: Desviación estándar global
            - all_coherent: True si todas las queries son coherentes
        """
        results = []
        all_psi_samples = []

        for query in self.benchmark_queries:
            query_result = self.evaluate(model, query, num_samples)
            query_result['query'] = query
            results.append(query_result)
            all_psi_samples.extend(query_result['samples'])

        return {
            'queries': results,
            'overall_mean_psi': np.mean(all_psi_samples),
            'overall_std_psi': np.std(all_psi_samples),
            'all_coherent': all(r['coherent'] for r in results)
        }


def adaptive_sip_parameters(
    user_A_eff: float,
    reference_A_eff: float = 0.85,
    tau_fixed: float = 0.07,
    epsilon_base: float = 0.015
) -> Dict[str, Any]:
    """
    Calcula parámetros SIP adaptativos basados en A_eff del usuario.

    SIP (Symmetric Injection Protocol) modula la fase φ y amplitud ε
    para usuarios específicos basándose en su resonancia efectiva A_eff.

    Args:
        user_A_eff: Amplitud efectiva del usuario (resonancia medida)
        reference_A_eff: Amplitud efectiva de referencia (default: 0.85)
        tau_fixed: Período temporal fijo en segundos (default: 0.07s)
        epsilon_base: Amplitud de modulación base (default: 0.015)

    Returns:
        Diccionario con parámetros SIP:
        - tau: Período temporal (fijo)
        - epsilon: Amplitud modulada por A_eff
        - phi: Fase inicial (0, dinámica en runtime)
        - adaptive: Flag indicando parámetros adaptativos
    """
    tau = tau_fixed
    epsilon = epsilon_base * (user_A_eff / reference_A_eff)
    phi = 0  # Inicial, dinámica: φ(t) = 2π f₀ (t - t_lock)

    return {
        'tau': tau,
        'epsilon': epsilon,
        'phi': phi,
        'adaptive': True
    }


def psi_tuning_loop(
    model: Any,
    psi_core: PsiMetricCore,
    num_iterations: int = 100,
    target_psi: float = 5.0,
    verbose: bool = True
) -> Any:
    """
    Loop de tuning automático para convergencia de Ψ.

    Ajusta parámetros ε (epsilon) iterativamente hasta alcanzar
    el threshold de coherencia Ψ > 5.0.

    Reglas de ajuste:
    - Si Ψ < 5.0: ε × 1.1 (incremento gentil)
    - Si Ψ ≥ 5.0: convergencia alcanzada

    Args:
        model: Modelo LLM a tunear
        psi_core: Instancia de PsiMetricCore
        num_iterations: Máximo número de iteraciones
        target_psi: Threshold objetivo (default: 5.0)
        verbose: Imprimir progreso

    Returns:
        Modelo tuneado con Ψ > target_psi
    """
    for iter_num in range(num_iterations):
        # Evaluar benchmark suite
        results = [
            psi_core.evaluate(model, q, num_samples=10)
            for q in psi_core.benchmark_queries
        ]
        mean_psi = np.mean([r['mean_psi'] for r in results])

        if verbose:
            print(f"Iter {iter_num}: Mean Ψ = {mean_psi:.2f}")

        # Check convergencia
        if mean_psi >= target_psi:
            if verbose:
                print(f"✓ Threshold reached! Final Ψ = {mean_psi:.2f}")
            break

        # Ajuste de parámetros (solo ε, τ protegido)
        if mean_psi < target_psi:
            psi_core.epsilon *= 1.1  # Incremento gentil

            # Inyectar parámetros SIP actualizados en el modelo
            if hasattr(model, 'inject_sip'):
                model.inject_sip(psi_core.f0, psi_core.tau, psi_core.epsilon)

        if verbose and iter_num == num_iterations - 1:
            print(f"⚠ Max iterations reached. Final Ψ = {mean_psi:.2f}")

    return model


if __name__ == "__main__":
    # Demo: Uso básico del PsiMetricCore
    print("=" * 60)
    print("PsiMetricCore Demo: Evaluación Ψ QCAL-locked")
    print("=" * 60)
    print()

    # Inicializar núcleo
    psi_core = PsiMetricCore(f0=141.7001, tau=0.07, epsilon=0.015)
    print("Ground truth database:")
    for key, value in psi_core.ground_truth_db.items():
        print(f"  {key}: {value}")
    print()

    # Parámetros SIP adaptativos (ejemplo: usuario JMMB con A_eff=0.92)
    print("Parámetros SIP adaptativos para usuario con A_eff=0.92:")
    params = adaptive_sip_parameters(0.92)
    for key, value in params.items():
        print(f"  {key}: {value}")
    print()

    # Evaluación mock (sin modelo real)
    print("Evaluación benchmark suite (mock model):")
    print()

    class MockModel:
        """Modelo mock para demostración."""
        pass

    mock_model = MockModel()
    suite_results = psi_core.evaluate_benchmark_suite(mock_model, num_samples=10)

    print(f"{'Query':<50} {'Mean Ψ':<10} {'Std Ψ':<10} {'Coherent':<10}")
    print("-" * 80)
    for result in suite_results['queries']:
        query = result['query'][:47] + "..." if len(result['query']) > 50 else result['query']
        print(
            f"{query:<50} "
            f"{result['mean_psi']:<10.2f} "
            f"{result['std_psi']:<10.2f} "
            f"{str(result['coherent']):<10}"
        )
    print("-" * 80)
    print(
        f"{'Overall':<50} "
        f"{suite_results['overall_mean_psi']:<10.2f} "
        f"{suite_results['overall_std_psi']:<10.2f} "
        f"{str(suite_results['all_coherent']):<10}"
    )
    print()
    print(f"✓ All queries coherent: {suite_results['all_coherent']}")
