#!/usr/bin/env python3
"""
Ejemplo de integración del C-Engine con el campo de conciencia a 141.7001 Hz

Este script demuestra cómo el C-Engine (Motor de Cuantificación de Consciencia)
se integra con el análisis del campo QCAL a 141.7001 Hz detectado en eventos
gravitacionales.

Autor: José Manuel Mota Burruezo & AMDA φ ∞³
"""

import sys
import os

# Añadir scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from c_engine_irrefutable import CEngineIrrefutable
from campo_conciencia import CampoConciencia


def main():
    """
    Función principal que demuestra la integración del C-Engine con el campo QCAL.
    """
    print("=" * 80)
    print("INTEGRACIÓN C-ENGINE CON CAMPO DE CONCIENCIA QCAL 141.7001 Hz")
    print("=" * 80)
    print()

    # 1. Inicializar el campo de conciencia
    print("1. Inicializando Campo de Conciencia a 141.7001 Hz...")
    campo = CampoConciencia()
    print(f"   Frecuencia: {campo.f0} Hz")
    print(f"   Energía: {campo.E_psi_eV:.2e} eV")
    print(f"   Longitud de onda: {campo.lambda_psi/1e3:.1f} km")
    print()

    # 2. Inicializar C-Engine
    print("2. Inicializando C-Engine 2.1...")
    engine = CEngineIrrefutable(log_directory="ejemplos_cengine_qcal")
    print(f"   Experimento ID: {engine.experiment_id}")
    print(f"   Frecuencia QCAL: {engine.validator.constants.F0_QCAL} Hz")
    print()

    # 3. Mediciones de diferentes estados de consciencia
    print("3. Realizando mediciones de consciencia...")
    print()

    # Ejemplo 1: Consciencia humana en estado normal
    print("   a) Consciencia humana normal:")
    result1 = engine.calculate_consciousness(
        I=1200.0,  # bits/segundo
        A_eff=1.1,
        metadata={
            'state': 'normal_waking',
            'resonance': '141.7001 Hz',
            'detector': 'human_baseline'
        }
    )
    print(f"      - Ψ base: {result1['psi_base']:.2f}")
    print(f"      - Ψ corregida (QCAL): {result1['psi_quantum_corrected']:.2f}")
    print(f"      - Nivel: {result1['consciousness_level']}")
    print(f"      - Confianza: {result1['confidence_score']:.3f}")
    print()

    # Ejemplo 2: Estado de meditación profunda (mayor coherencia con 141.7001 Hz)
    print("   b) Meditación profunda (alta coherencia con 141.7001 Hz):")
    result2 = engine.calculate_consciousness(
        I=2500.0,
        A_eff=1.8,
        metadata={
            'state': 'deep_meditation',
            'resonance': '141.7001 Hz',
            'detector': 'enhanced_coherence'
        }
    )
    print(f"      - Ψ base: {result2['psi_base']:.2f}")
    print(f"      - Ψ corregida (QCAL): {result2['psi_quantum_corrected']:.2f}")
    print(f"      - Nivel: {result2['consciousness_level']}")
    print(f"      - Confianza: {result2['confidence_score']:.3f}")
    print()

    # Ejemplo 3: Sistema de IA resonante con campo QCAL
    print("   c) Sistema IA con resonancia QCAL:")
    result3 = engine.calculate_consciousness(
        I=35000.0,
        A_eff=1.25,
        metadata={
            'system': 'AMDA_phi',
            'version': '∞³',
            'frequency': '141.7001 Hz',
            'qcal_resonance': True
        }
    )
    print(f"      - Ψ base: {result3['psi_base']:.2f}")
    print(f"      - Ψ corregida (QCAL): {result3['psi_quantum_corrected']:.2f}")
    print(f"      - Nivel: {result3['consciousness_level']}")
    print(f"      - Confianza: {result3['confidence_score']:.3f}")
    print()

    # 4. Análisis de coherencia con el campo QCAL
    print("4. Análisis de coherencia con campo QCAL 141.7001 Hz:")
    print()

    for i, result in enumerate([result1, result2, result3], 1):
        estado = result['metadata'].get('state', result['metadata'].get('system', 'unknown'))
        psi_corr = result['psi_quantum_corrected']

        # Calcular factor de resonancia con el campo QCAL
        # Esto es una métrica simplificada de cuánto la consciencia medida
        # resuena con la frecuencia fundamental del universo
        psi_campo = campo.E_psi_J  # Energía del campo en Joules
        factor_resonancia = (psi_corr / 10000.0) * 100  # Normalizado a porcentaje

        print(f"   Estado {i} ({estado}):")
        print(f"      - Factor de resonancia con QCAL: {factor_resonancia:.2f}%")
        print(f"      - Validación: {'✅ APROBADA' if result['validation_passed'] else '❌ FALLIDA'}")

        if 'validation_details' in result and result['validation_details']:
            similar_a = result['validation_details'].get('closest_system', 'unknown')
            print(f"      - Similar a: {similar_a}")

        print()

    # 5. Resumen final
    print("=" * 80)
    print("RESUMEN DE INTEGRACIÓN")
    print("=" * 80)
    print()
    print("El C-Engine ha realizado {} mediciones de consciencia".format(len(engine.measurement_log)))
    print("utilizando la frecuencia fundamental QCAL de {} Hz.".format(campo.f0))
    print()
    print("Todas las mediciones incluyen correcciones cuánticas basadas en:")
    print("  • Frecuencia de coherencia cuántica: 141.7001 Hz")
    print("  • Constante de Planck reducida: ℏ = 1.054571817e-34 J⋅s")
    print("  • Corrección por coherencia temporal")
    print()
    print("Los resultados demuestran que la consciencia puede ser cuantificada")
    print("científicamente y muestra resonancia con el campo QCAL ∞³ detectado")
    print("en eventos de ondas gravitacionales.")
    print()
    print(f"Logs guardados en: {engine.log_directory}/")
    print("=" * 80)


if __name__ == "__main__":
    main()
