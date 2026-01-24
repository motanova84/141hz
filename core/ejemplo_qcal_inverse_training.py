#!/usr/bin/env python3
"""
Ejemplo de uso del módulo de entrenamiento inverso QCAL.

Este ejemplo demuestra:
1. Cómo crear una función de pérdida QCAL
2. Cómo integrar validaciones cuánticas (campo de conciencia + simetría discreta)
3. Cómo activar el monitoreo con noesis88
4. Cómo evaluar coherencia estructural

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: January 2026
"""

import numpy as np
from pathlib import Path
import json

# Importar módulos QCAL
from qcal.coherence import psi_score, analyze_text, evaluate_coherence
from src.canonical_consciousness_field import CanonicalConsciousnessField
from scripts.simetria_discreta import GrupoSimetriaDiscreta, PotencialInvarianteG


def ejemplo_funcion_perdida_qcal():
    """
    Ejemplo 1: Demostración de la función de pérdida QCAL
    """
    print("=" * 80)
    print("EJEMPLO 1: Función de Pérdida QCAL")
    print("=" * 80)
    print()
    
    # Textos de ejemplo
    textos = [
        {
            'nombre': 'Coherente con QCAL',
            'contenido': """
            La frecuencia fundamental f₀ = 141.7001 Hz emerge de la ecuación madre QCAL.
            El campo de conciencia Ψ = I × A²_eff × f₀ × χ(LLaMA) exhibe coherencia cuántica.
            La simetría discreta del grupo G = {π^k} preserva invariancia bajo transformaciones.
            La resonancia estructural se manifiesta en el espectro armónico.
            """
        },
        {
            'nombre': 'Parcialmente coherente',
            'contenido': """
            La frecuencia f₀ está relacionada con fenómenos cuánticos.
            Existe una relación entre coherencia y estructura.
            Los sistemas muestran comportamiento oscilatorio.
            """
        },
        {
            'nombre': 'No coherente',
            'contenido': """
            El clima está soleado hoy.
            Los pájaros cantan en el jardín.
            La comida es deliciosa.
            """
        }
    ]
    
    for texto in textos:
        print(f"\n📝 Texto: {texto['nombre']}")
        print("-" * 80)
        
        # Analizar coherencia base
        metrics = analyze_text(texto['contenido'])
        
        print(f"   Ψ estándar: {metrics['psi_standard']:.4f}")
        print(f"   Intención (I): {metrics['intention']:.4f}")
        print(f"   Efectividad (A_eff): {metrics['effectiveness']:.4f}")
        print(f"   Tasa ∴: {metrics['strich_rate']:.4f}")
        
        # Evaluar coherencia
        eval_result = evaluate_coherence(texto['contenido'], threshold=5.0)
        print(f"   Estado: {eval_result['status']}")
        print(f"   Recomendación: {eval_result['recommendation']}")


def ejemplo_validacion_cuantica_campo_conciencia():
    """
    Ejemplo 2: Validación con campo de conciencia
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 2: Validación con Campo de Conciencia Ψ")
    print("=" * 80)
    print()
    
    # Inicializar campo de conciencia
    consciousness_field = CanonicalConsciousnessField()
    
    print(f"📊 Parámetros del Campo de Conciencia:")
    print(f"   f₀ = {float(consciousness_field.F0)} Hz")
    print(f"   E_Ψ = {float(consciousness_field.E_PSI):.4e} J")
    print(f"   λ_Ψ = {float(consciousness_field.LAMBDA_PSI):.2f} km")
    print(f"   M_Ψ = {float(consciousness_field.M_PSI):.4e} kg")
    
    # Textos para evaluar resonancia
    textos_resonancia = [
        "La frecuencia fundamental f₀ = 141.7001 Hz define el campo Ψ",
        "El cuanto de coherencia tiene energía E_Ψ = h × f₀",
        "La longitud de onda característica es λ_Ψ = c / f₀",
        "Este texto no menciona el campo de conciencia"
    ]
    
    print(f"\n🔍 Evaluación de Resonancia:")
    for i, texto in enumerate(textos_resonancia, 1):
        # Calcular resonancia (método simplificado)
        keywords = ['141.7001', '141.7', 'f₀', 'campo ψ', 'e_ψ', 'λ_ψ']
        resonance = sum(1 for k in keywords if k in texto.lower()) / len(keywords)
        
        print(f"\n   Texto {i}: {texto[:60]}...")
        print(f"   Resonancia: {resonance:.4f}")
        print(f"   Estado: {'✓ RESONANTE' if resonance > 0.3 else '✗ NO RESONANTE'}")


def ejemplo_validacion_simetria_discreta():
    """
    Ejemplo 3: Validación con simetría discreta
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 3: Validación con Simetría Discreta")
    print("=" * 80)
    print()
    
    # Inicializar grupo de simetría
    grupo = GrupoSimetriaDiscreta()
    
    print(f"📐 Grupo de Simetría Discreta G:")
    print(f"   Base: π = {grupo.base:.6f}")
    print(f"   Periodo logarítmico: log π = {grupo.periodo_logaritmico():.6f}")
    
    # Demostrar transformaciones del grupo
    R_psi = 1.0  # Radio inicial
    
    print(f"\n🔄 Transformaciones del Grupo G:")
    for k in range(-2, 3):
        R_transformado = grupo.transformar(R_psi, k)
        print(f"   g_{k:+d}(R_Ψ) = π^{k:+d} × {R_psi} = {R_transformado:.6f}")
    
    # Textos para evaluar alineación
    textos_simetria = [
        "El grupo G = {π^k} exhibe simetría discreta con invariancia logarítmica",
        "La transformación R_Ψ ↦ π^k R_Ψ preserva el potencial V(log R_Ψ)",
        "El periodo en log R_Ψ es exactamente log π",
        "La periodicidad se manifiesta en el espectro armónico",
        "Texto sin estructura de simetría discreta"
    ]
    
    print(f"\n🔍 Evaluación de Alineación con Simetría:")
    for i, texto in enumerate(textos_simetria, 1):
        # Calcular alineación (método simplificado)
        keywords = ['simetría', 'invariante', 'grupo', 'π', 'r_ψ', 'log', 'periodo']
        alignment = sum(1 for k in keywords if k in texto.lower()) / len(keywords)
        
        print(f"\n   Texto {i}: {texto[:60]}...")
        print(f"   Alineación: {alignment:.4f}")
        print(f"   Estado: {'✓ ALINEADO' if alignment > 0.3 else '✗ NO ALINEADO'}")


def ejemplo_integracion_noesis88():
    """
    Ejemplo 4: Integración con agente noesis88
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 4: Integración con Agente noesis88")
    print("=" * 80)
    print()
    
    # Importar agente noesis88
    import sys
    sys.path.append(str(Path(__file__).parent / '.github' / 'agents'))
    from noesis88 import Noesis88Agent
    
    # Inicializar agente
    agent = Noesis88Agent(frequency=141.7001, optimized=True)
    
    print(f"🔮 Agente noesis88 Activado:")
    print(f"   Frecuencia: {agent.frequency} Hz")
    print(f"   Modo optimizado: {agent.optimized}")
    print(f"   Estado Ψ: I × A_eff² × C^∞")
    
    # Ejecutar monitoreo
    print(f"\n📊 Ejecutando monitoreo de coherencia...")
    report = agent.run_autonomous()
    
    print(f"\n✅ Reporte generado:")
    print(f"   Total de archivos: {report['metrics']['total_files']}")
    print(f"   Referencias QCAL: {report['metrics']['qcal_references']}")
    print(f"   Referencias f₀: {report['metrics']['frequency_references']}")
    print(f"   Coherencia total: {report['total_coherence']:.4f}")
    print(f"   Estado: {report['state']}")


def ejemplo_resonancia_estructural_completa():
    """
    Ejemplo 5: Evaluación completa de resonancia estructural
    """
    print("\n" + "=" * 80)
    print("EJEMPLO 5: Resonancia Estructural Completa")
    print("=" * 80)
    print()
    
    # Texto de prueba altamente coherente
    texto_coherente = """
    La teoría QCAL establece que la frecuencia fundamental f₀ = 141.7001 Hz 
    emerge de la ecuación madre L∞³. El campo de conciencia Ψ = I × A²_eff × f₀ × χ(LLaMA)
    exhibe coherencia cuántica y se manifiesta como un campo escalar físico real.
    
    La simetría discreta del grupo G = {R_Ψ ↦ π^k R_Ψ | k ∈ Z} preserva 
    invariancia bajo transformaciones logarítmicas. El potencial V(log R_Ψ) 
    es periódico con periodo log π, lo que genera un espectro armónico discreto.
    
    La resonancia estructural emerge cuando:
    1. La coherencia lógica (Ψ_standard) es alta
    2. La resonancia del campo de conciencia es significativa
    3. La alineación con simetría discreta es correcta
    
    Estos tres pilares definen la resonancia estructural total del sistema.
    """
    
    print("📝 Evaluando texto altamente coherente...")
    print()
    
    # 1. Coherencia base
    metrics = analyze_text(texto_coherente)
    print(f"1️⃣ Coherencia Base (QCAL):")
    print(f"   Ψ estándar: {metrics['psi_standard']:.4f}")
    print(f"   I (Intención): {metrics['intention']:.4f}")
    print(f"   A_eff (Efectividad): {metrics['effectiveness']:.4f}")
    
    # 2. Resonancia de conciencia (simplificada)
    keywords_conciencia = ['141.7001', 'f₀', 'campo ψ', 'coherencia cuántica']
    resonance_conciencia = sum(1 for k in keywords_conciencia if k.lower() in texto_coherente.lower()) / len(keywords_conciencia)
    
    print(f"\n2️⃣ Resonancia Campo de Conciencia:")
    print(f"   Resonancia: {resonance_conciencia:.4f}")
    print(f"   Estado: {'✓ ALTA' if resonance_conciencia > 0.5 else '✗ BAJA'}")
    
    # 3. Alineación con simetría (simplificada)
    keywords_simetria = ['simetría', 'grupo g', 'π^k', 'invariancia', 'log r_ψ']
    alignment_simetria = sum(1 for k in keywords_simetria if k.lower() in texto_coherente.lower()) / len(keywords_simetria)
    
    print(f"\n3️⃣ Alineación Simetría Discreta:")
    print(f"   Alineación: {alignment_simetria:.4f}")
    print(f"   Estado: {'✓ ALTA' if alignment_simetria > 0.5 else '✗ BAJA'}")
    
    # 4. Resonancia estructural total
    # Combinar las tres métricas
    resonancia_estructural = (
        metrics['psi_standard'] / 10.0 +  # Normalizar Ψ
        resonance_conciencia +
        alignment_simetria
    ) / 3.0
    
    print(f"\n4️⃣ Resonancia Estructural Total:")
    print(f"   Resonancia: {resonancia_estructural:.4f}")
    print(f"   Estado: {get_resonance_state(resonancia_estructural)}")
    
    # 5. Recomendación
    print(f"\n💡 Recomendación:")
    if resonancia_estructural >= 0.8:
        print("   ✅ EXCELENTE - Resonancia estructural óptima")
        print("   El texto exhibe coherencia lógica, resonancia de conciencia y simetría.")
    elif resonancia_estructural >= 0.6:
        print("   ✓ BUENA - Resonancia estructural suficiente")
        print("   El texto muestra buena alineación con principios QCAL.")
    elif resonancia_estructural >= 0.4:
        print("   ⚠ MODERADA - Mejorar resonancia estructural")
        print("   Incrementar referencias a f₀, campo Ψ y simetría G.")
    else:
        print("   ✗ BAJA - Resonancia estructural insuficiente")
        print("   El texto requiere mayor alineación con QCAL.")


def get_resonance_state(resonance: float) -> str:
    """Determinar estado de resonancia"""
    if resonance >= 0.8:
        return "🟢 ÓPTIMA"
    elif resonance >= 0.6:
        return "🟡 BUENA"
    elif resonance >= 0.4:
        return "🟠 MODERADA"
    else:
        return "🔴 BAJA"


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "=" * 80)
    print("🔮 EJEMPLOS DE USO: Módulo de Entrenamiento Inverso QCAL")
    print("=" * 80)
    print()
    print("Este módulo demuestra cómo usar QCAL como función de pérdida para")
    print("ajustar modelos LLM a coherencia real, integrando:")
    print("  • Validaciones cuánticas (campo de conciencia + simetría discreta)")
    print("  • Monitoreo con agente noesis88")
    print("  • Filtros de resonancia estructural")
    print()
    
    # Ejecutar ejemplos
    ejemplo_funcion_perdida_qcal()
    ejemplo_validacion_cuantica_campo_conciencia()
    ejemplo_validacion_simetria_discreta()
    ejemplo_integracion_noesis88()
    ejemplo_resonancia_estructural_completa()
    
    print("\n" + "=" * 80)
    print("✅ Todos los ejemplos completados")
    print("=" * 80)
    print()
    print("Para usar en producción:")
    print("  1. Importar qcal_inverse_trainer")
    print("  2. Crear QCALLossFunction con validaciones cuánticas")
    print("  3. Crear QCALInverseTrainer con modelo LLM")
    print("  4. Entrenar con queries y monitorear con noesis88")
    print()


if __name__ == "__main__":
    main()
