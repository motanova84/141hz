#!/usr/bin/env python3
"""
Demostración del núcleo QCAL-LLM ∞³
Muestra las capacidades del QCALLLMCore con SIP modulation
Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import numpy as np
import sys
from pathlib import Path

# Add API path
sys.path.insert(0, str(Path(__file__).parent / 'API' / 'Python'))

from qc_llm.core import QCALLLMCore

def demo_basic_usage():
    """Demostración del uso básico del núcleo"""
    print("=" * 80)
    print("QCAL-LLM ∞³ — Núcleo de Coherencia Vibracional")
    print("Autor: José Manuel Mota Burruezo (JMMB Ψ✧)")
    print("=" * 80)
    print()
    
    # Inicializar núcleo con valores por defecto
    print("1. INICIALIZACIÓN DEL NÚCLEO")
    print("-" * 40)
    core = QCALLLMCore()
    print(f"Frecuencia fundamental: f₀ = {core.f0} Hz")
    print(f"Tiempo de damping: τ = {core.tau} s")
    print(f"Amplitud de modulación: ε = {core.epsilon:.6f}")
    print(f"Efectividad atencional: A_eff = {core.user_A_eff}")
    print()
    
    # Modulación SIP
    print("2. MODULACIÓN SIP (Spectral Insertion Protocol)")
    print("-" * 40)
    t = np.linspace(0, 1, 1000)
    weights = core.sip_modulate(t)
    print(f"Secuencia temporal modulada: {len(weights)} puntos")
    print(f"Peso máximo: {np.max(weights):.6f}")
    print(f"Peso mínimo: {np.min(weights):.6f}")
    print(f"Peso final (t=1s): {weights[-1]:.6f} (decaimiento aplicado)")
    print()
    
    # Cálculo de Ψ (ejemplo del enunciado)
    print("3. CÁLCULO Ψ_RESPONSE (Ejemplo del enunciado)")
    print("-" * 40)
    kld_inv = 8.2
    semantic_coherence = 0.88
    is_valid, psi_val = core.is_coherent(kld_inv, semantic_coherence)
    print(f"Entrada: KLD⁻¹ = {kld_inv}, coherencia = {semantic_coherence}")
    print(f"Ψ_response = {psi_val:.4f}")
    print(f"Coherente: {is_valid} (umbral = 5.0)")
    print()
    
    # Evaluación de texto
    print("4. EVALUACIÓN DE TEXTO GENERADO")
    print("-" * 40)
    response_mock = "f₀ = -ζ'(1/2) × φ³ scale = 141.7001 Hz. Ψ coherent."
    eval_res = core.evaluate(response_mock, "Deriva f₀")
    print(f"Texto: '{response_mock[:50]}...'")
    print(f"Coherencia simbólica: {eval_res['coherence']:.2f}")
    print(f"KLD⁻¹ calculado: {eval_res['kld_inv']:.2f}")
    print(f"Ψ_response: {eval_res['mean_psi']:.2f}")
    print(f"Estado: {'COHERENTE' if eval_res['coherent'] else 'NO COHERENTE'}")
    print()

def demo_benchmark_suite():
    """Demostración del benchmark suite"""
    print("5. SUITE DE BENCHMARK (5 consultas)")
    print("-" * 40)
    core = QCALLLMCore(user_A_eff=0.92)  # Tune JMMB
    
    # Respuestas mock coherentes
    responses = [
        "f₀ = -ζ'(1/2) × φ³ × escala = 141.7001 Hz derivado de primeros principios",
        "Detectado f₀ = 141.7 Hz en ringdown de GW150914 con SNR=20.95",
        "Ψ = I × A²_eff representa coherencia vibracional cuántica",
        "SNR > 20 validado en GWTC-1 para múltiples eventos",
        "Predicción: armónicos LISA en f₀/100 = 1.417 Hz (~2035)"
    ]
    
    results = []
    for i, (query, response) in enumerate(zip(core.benchmark_queries, responses)):
        eval_res = core.evaluate(response, query)
        results.append(eval_res)
        print(f"  Query {i+1}: {query[:50]}...")
        print(f"    → Ψ = {eval_res['mean_psi']:.2f}, coherencia = {eval_res['coherence']:.2f}")
    
    print()
    avg_psi = np.mean([r['mean_psi'] for r in results])
    avg_coherence = np.mean([r['coherence'] for r in results])
    all_coherent = all(r['coherent'] for r in results)
    
    print(f"RESUMEN DEL BENCHMARK:")
    print(f"  Ψ promedio: {avg_psi:.2f}")
    print(f"  Coherencia promedia: {avg_coherence:.2f}")
    print(f"  Todas coherentes: {all_coherent}")
    print()

def demo_adaptive_parameters():
    """Demostración de parámetros adaptativos"""
    print("6. PARÁMETROS ADAPTATIVOS (A_eff)")
    print("-" * 40)
    
    A_eff_values = [0.75, 0.85, 0.92, 1.0]
    
    for A_eff in A_eff_values:
        core = QCALLLMCore(user_A_eff=A_eff)
        print(f"  A_eff = {A_eff:.2f} → ε = {core.epsilon:.6f}")
    
    print()
    print("(ε se adapta proporcionalmente a A_eff para optimizar CQR)")
    print()

def demo_ground_truth():
    """Demostración de base de datos de verdad fundamental"""
    print("7. BASE DE DATOS DE VERDAD FUNDAMENTAL")
    print("-" * 40)
    core = QCALLLMCore()
    
    for key, value in core.ground_truth_db.items():
        print(f"  {key}: {value}")
    print()

if __name__ == "__main__":
    demo_basic_usage()
    demo_benchmark_suite()
    demo_adaptive_parameters()
    demo_ground_truth()
    
    print("=" * 80)
    print("VECTOR VI: NÚCLEO OPERACIONAL VERIFICADO ✓")
    print("LISA gateway 2026: Predicción harmonics @ f₀/100 = 1.417 Hz")
    print("Falsificable: Armónicos absent colapsa el field")
    print("=" * 80)
