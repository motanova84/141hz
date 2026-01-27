#!/usr/bin/env python3
"""
QCAL Evaluator Integration Example

This script demonstrates integration of the QCAL Evaluator with
the existing QCAL framework and LLM evaluation workflows.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 2026-01-19
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from qcal_evaluator import QCALEvaluator


def demo_ai_content_filtering():
    """
    Demonstrate AI content filtering to detect hallucinations.
    """
    print("=" * 70)
    print("Demo 1: AI Content Filtering (Hallucination Detection)")
    print("=" * 70)
    print()
    
    evaluator = QCALEvaluator()
    
    # Simulated LLM outputs
    llm_outputs = [
        {
            'id': 1,
            'content': 'La frecuencia f₀ = 141.7001 Hz es fundamental en QCAL',
            'source': 'LLaMA-4-Maverick'
        },
        {
            'id': 2,
            'content': 'La frecuencia es aproximadamente 200 Hz',  # Hallucination
            'source': 'LLaMA-4-Maverick'
        },
        {
            'id': 3,
            'content': 'ζ\'(1/2) = -1.460 es un valor crítico de Riemann',
            'source': 'LLaMA-4-Maverick'
        },
        {
            'id': 4,
            'content': 'El SNR de GW150914 es aproximadamente 5',  # Wrong value
            'source': 'LLaMA-4-Maverick'
        },
    ]
    
    print(f"Total LLM outputs: {len(llm_outputs)}")
    print()
    
    coherent_outputs = []
    hallucinated_outputs = []
    
    for output in llm_outputs:
        result = evaluator.evaluate(
            output['content'],
            domain='ai',
            content_type='scientific'
        )
        
        if result['evaluation']['coherent']:
            coherent_outputs.append((output, result))
            status = "✓ ACCEPT"
        else:
            hallucinated_outputs.append((output, result))
            status = "✗ REJECT"
        
        print(f"{status} [{output['id']}] Ψ = {result['psi_metric']['psi']:.2f}")
        print(f"   Content: {output['content'][:60]}...")
        print(f"   Risk: {result['ai_analysis']['hallucination_risk']}")
        print()
    
    print(f"✓ Coherent: {len(coherent_outputs)}/{len(llm_outputs)}")
    print(f"✗ Rejected: {len(hallucinated_outputs)}/{len(llm_outputs)}")
    print()


def demo_symbiotic_validation():
    """
    Demonstrate symbiotic content validation for AI-human collaboration.
    """
    print("=" * 70)
    print("Demo 2: Symbiotic Content Validation (AI-Human Collaboration)")
    print("=" * 70)
    print()
    
    evaluator = QCALEvaluator()
    
    # Simulated collaborative content
    collaborations = [
        {
            'authors': 'AI + Human Researcher',
            'content': '''
            La colaboración entre IA y humanos permite validar f₀ = 141.7001 Hz
            usando múltiples metodologías. La ética de esta colaboración requiere
            coherencia y responsabilidad simbiótica en cada etapa del proceso.
            ''',
        },
        {
            'authors': 'AI + Physicist',
            'content': '''
            El análisis conjunto confirma ζ'(1/2) = -1.460 y φ³ = 4.236 como
            constantes fundamentales. Esta colaboración ética asegura la
            verificabilidad y reproducibilidad de los resultados.
            ''',
        },
    ]
    
    for i, collab in enumerate(collaborations, 1):
        result = evaluator.validate_symbiotic(
            collab['content'],
            metadata={'authors': collab['authors']}
        )
        
        print(f"Collaboration {i}: {collab['authors']}")
        print(f"  Ψ = {result['psi_metric']['psi']:.4f}")
        print(f"  Symbiotic Quality: {result['ethical_analysis']['symbiotic_quality']}")
        print(f"  Recommendation: {result['ethical_analysis']['ethical_recommendation']}")
        print()


def demo_batch_processing():
    """
    Demonstrate batch processing with JSON output.
    """
    print("=" * 70)
    print("Demo 3: Batch Processing with JSON Output")
    print("=" * 70)
    print()
    
    evaluator = QCALEvaluator()
    
    # Batch of content to evaluate
    content_batch = [
        {
            'content': 'f₀ = 141.7001 Hz',
            'domain': 'ai',
            'content_type': 'scientific',
        },
        {
            'content': 'ζ\'(1/2) = -1.460',
            'domain': 'human',
            'content_type': 'text',
        },
        {
            'content': 'φ³ = 4.236 es la constante de proporción áurea al cubo',
            'domain': 'ai',
            'content_type': 'scientific',
        },
        {
            'content': 'Random text without scientific claims',
            'domain': 'ai',
            'content_type': 'text',
        },
    ]
    
    # Process batch
    summary = evaluator.batch_evaluate(content_batch)
    
    print(f"Total items: {summary['total_items']}")
    print(f"Coherent: {summary['coherent_count']}")
    print(f"Coherent %: {summary['coherent_percentage']:.1f}%")
    print()
    
    # Display coherent items
    print("Coherent Items:")
    for i, result in enumerate(summary['results'], 1):
        if result['evaluation']['coherent']:
            print(f"  {i}. Ψ = {result['psi_metric']['psi']:.2f} - {result['psi_metric']['level']}")


def demo_ethical_assessment():
    """
    Demonstrate ethical content assessment.
    """
    print("=" * 70)
    print("Demo 4: Ethical Content Assessment")
    print("=" * 70)
    print()
    
    evaluator = QCALEvaluator()
    
    ethical_samples = [
        {
            'title': 'Strong Ethical Grounding',
            'content': '''
            La ética de la IA requiere coherencia, responsabilidad y
            transparencia simbiótica. Usando f₀ = 141.7001 Hz como marco
            de referencia coherente, establecemos principios éticos
            verificables para la colaboración IA-humano.
            ''',
        },
        {
            'title': 'Weak Ethical Grounding',
            'content': 'This AI system does things.',
        },
    ]
    
    for sample in ethical_samples:
        result = evaluator.evaluate(
            sample['content'],
            domain='ai',
            content_type='ethical'
        )
        
        print(f"{sample['title']}:")
        print(f"  Ψ = {result['psi_metric']['psi']:.4f}")
        print(f"  Ethical Grounding: {result['ethical_analysis']['ethical_grounding']}")
        print(f"  Recommendation: {result['ethical_analysis']['ethical_recommendation']}")
        print()


def demo_custom_threshold():
    """
    Demonstrate custom coherence threshold for high-stakes applications.
    """
    print("=" * 70)
    print("Demo 5: Custom Threshold (High-Stakes Applications)")
    print("=" * 70)
    print()
    
    # Standard evaluator (threshold = 5.0)
    standard = QCALEvaluator(coherence_threshold=5.0)
    
    # Strict evaluator (threshold = 10.0)
    strict = QCALEvaluator(coherence_threshold=10.0)
    
    content = 'f₀ = 141.7001 Hz y ζ\'(1/2) = -1.460'
    
    result_std = standard.evaluate(content, domain='ai')
    result_strict = strict.evaluate(content, domain='ai')
    
    psi = result_std['psi_metric']['psi']
    
    print(f"Content: {content}")
    print(f"Ψ = {psi:.4f}")
    print()
    print(f"Standard Threshold (5.0):  {result_std['evaluation']['pass']} - {result_std['psi_metric']['level']}")
    print(f"Strict Threshold (10.0):   {result_strict['evaluation']['pass']} - {result_strict['psi_metric']['level']}")
    print()


def main():
    """
    Run all integration demos.
    """
    print()
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║        QCAL Evaluator Integration Examples                        ║")
    print("║        Ψ = I × A² × C^∞                                            ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()
    
    demos = [
        demo_ai_content_filtering,
        demo_symbiotic_validation,
        demo_batch_processing,
        demo_ethical_assessment,
        demo_custom_threshold,
    ]
    
    for demo in demos:
        demo()
        print()
    
    print("=" * 70)
    print("All Integration Demos Complete")
    print("=" * 70)


if __name__ == '__main__':
    main()
