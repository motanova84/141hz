#!/usr/bin/env python3
"""
Ejemplo de integración QCAL-LLM con salidas de LLMs
Demuestra cómo validar respuestas de modelos de lenguaje usando el núcleo QCAL
"""

import sys
from pathlib import Path

# Add API path
api_path = Path(__file__).resolve().parents[2] / 'API' / 'Python'
sys.path.insert(0, str(api_path))

from qc_llm.core import QCALLLMCore

# Simulación de respuestas de un LLM a diferentes consultas
EXAMPLE_CONVERSATIONS = [
    {
        "query": "¿Cuál es la frecuencia fundamental en gravitational waves?",
        "response": """
        La frecuencia fundamental f₀ = 141.7001 Hz emerge de la combinación de
        principios matemáticos fundamentales, específicamente de ζ'(1/2) y φ³.
        Esta frecuencia ha sido detectada en el ringdown de eventos como GW150914
        con un SNR superior a 20, validando su presencia en señales reales.
        """
    },
    {
        "query": "Explica la métrica Ψ de coherencia",
        "response": """
        La métrica Ψ mide la coherencia vibracional mediante la fórmula Ψ = I × A_eff²,
        donde I representa la información útil (entropía inversa) y A_eff es la
        efectividad atencional. Un valor Ψ ≥ 5.0 indica coherencia vibracional
        suficiente para validar una respuesta.
        """
    },
    {
        "query": "¿Qué es el golden ratio?",
        "response": """
        The golden ratio, often denoted by φ (phi), is approximately 1.618.
        It appears in many natural phenomena and has been studied since ancient times.
        It's related to the Fibonacci sequence and appears in art and architecture.
        """
    },
    {
        "query": "Predice los armónicos LISA",
        "response": """
        LISA (Laser Interferometer Space Antenna) podrá detectar armónicos en
        frecuencias bajas. Si f₀ = 141.7 Hz está presente en sistemas binarios,
        esperamos observar armónicos en f₀/100 ≈ 1.417 Hz hacia 2035.
        Esta predicción es falsable: la ausencia de estos armónicos refutaría
        el modelo QCAL.
        """
    },
    {
        "query": "¿Qué tiempo hace hoy?",
        "response": """
        No tengo acceso a información en tiempo real sobre el clima.
        Te recomendaría consultar un servicio meteorológico local
        o una aplicación del tiempo para información actualizada.
        """
    }
]

def analyze_conversation(core, conv_data):
    """Analiza una conversación y retorna métricas de coherencia"""
    query = conv_data["query"]
    response = conv_data["response"]
    
    # Evaluar la respuesta con el núcleo QCAL
    result = core.evaluate(response, query)
    
    return {
        "query": query,
        "response_preview": response.strip()[:80] + "...",
        "coherence": result["coherence"],
        "kld_inv": result["kld_inv"],
        "mean_psi": result["mean_psi"],
        "coherent": result["coherent"],
        "status": "✓ COHERENTE" if result["coherent"] else "✗ NO COHERENTE"
    }

def main():
    print("=" * 80)
    print("QCAL-LLM: Validación de Respuestas de Modelos de Lenguaje")
    print("=" * 80)
    print()
    
    # Inicializar núcleo con parámetros optimizados
    print("Inicializando QCALLLMCore (A_eff=0.92, tuned)...")
    core = QCALLLMCore(user_A_eff=0.92)
    print(f"  f₀ = {core.f0} Hz")
    print(f"  ε = {core.epsilon:.6f} (adaptado)")
    print(f"  τ = {core.tau} s")
    print()
    
    # Analizar cada conversación
    print("Analizando conversaciones...")
    print("-" * 80)
    
    results = []
    for i, conv in enumerate(EXAMPLE_CONVERSATIONS, 1):
        print(f"\n[{i}] Query: {conv['query']}")
        analysis = analyze_conversation(core, conv)
        results.append(analysis)
        
        print(f"    Response: {analysis['response_preview']}")
        print(f"    Coherencia simbólica: {analysis['coherence']:.2f}")
        print(f"    KLD⁻¹: {analysis['kld_inv']:.2f}")
        print(f"    Ψ: {analysis['mean_psi']:.2f}")
        print(f"    Status: {analysis['status']}")
    
    # Resumen estadístico
    print()
    print("=" * 80)
    print("RESUMEN ESTADÍSTICO")
    print("=" * 80)
    
    coherent_count = sum(1 for r in results if r["coherent"])
    avg_psi = sum(r["mean_psi"] for r in results) / len(results)
    avg_coherence = sum(r["coherence"] for r in results) / len(results)
    
    print(f"Total de conversaciones: {len(results)}")
    print(f"Respuestas coherentes (Ψ ≥ 5.0): {coherent_count} ({coherent_count/len(results)*100:.1f}%)")
    print(f"Ψ promedio: {avg_psi:.2f}")
    print(f"Coherencia simbólica promedio: {avg_coherence:.2f}")
    print()
    
    # Recomendaciones
    print("RECOMENDACIONES:")
    if avg_psi < 3.0:
        print("  • Muy baja coherencia general. Considerar re-training del modelo.")
    elif avg_psi < 5.0:
        print("  • Coherencia moderada. Mejorar instrucciones para incluir símbolos fundamentales.")
    else:
        print("  • Coherencia alta. El modelo está bien calibrado para QCAL.")
    
    if avg_coherence < 0.3:
        print("  • Pocas referencias a símbolos fundamentales (φ³, ζ', f₀).")
        print("  • Sugerencia: Incluir estos símbolos en el prompt del sistema.")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
