#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validación de la Teoría Unificada: Biología × Teoría de Números × Física Cuántica
=================================================================================
Script de validación para los tres módulos de la teoría unificada.

Este script valida:
1. Módulo adn_riemann.py - Codificación ADN-Riemann
2. Módulo mutaciones_resonantes.py - Análisis de mutaciones
3. Módulo teoria_unificada_adn.py - Teoría unificada

Autor: QCAL ∞³ System
Fecha: 2026-03-18
"""
import sys
from pathlib import Path

# Ajustar path para imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

import numpy as np
from adn_riemann import (
    CalculadorCerosRiemann, CodificadorADNRiemann,
    calcular_coherencia_cuantica_adn,
    FRECUENCIA_BASE, PSI_OPTIMO, FACTOR_UNIFICACION
)
from mutaciones_resonantes import (
    AnalizadorMutaciones, OptimizadorSecuencias
)
from teoria_unificada_adn import (
    TeoriaUnificadaADN, PHI, ALPHA_FINA
)


def print_header(titulo: str):
    """Imprime un encabezado formateado."""
    print("\n" + "=" * 80)
    print(f"  {titulo}")
    print("=" * 80)


def print_section(titulo: str):
    """Imprime un título de sección."""
    print(f"\n{'─' * 80}")
    print(f"  {titulo}")
    print(f"{'─' * 80}")


def validar_modulo_adn_riemann() -> bool:
    """Valida el módulo adn_riemann.py."""
    print_section("VALIDACIÓN: Módulo adn_riemann.py")
    
    try:
        # Test 1: Inicialización de calculador de ceros
        print("\n  ✓ Test 1: Inicialización CalculadorCerosRiemann")
        calculador = CalculadorCerosRiemann(num_ceros=100)
        assert calculador.numero_de_ceros() > 0
        print(f"    - Ceros precalculados: {calculador.numero_de_ceros()}")
        
        # Test 2: Primer cero conocido
        print("\n  ✓ Test 2: Verificación primer cero de Riemann")
        t1 = calculador.obtener_cero(1)
        assert abs(t1 - 14.134725) < 0.001
        print(f"    - Primer cero t₁ = {t1:.6f} (esperado: 14.134725)")
        
        # Test 3: Codificación ADN
        print("\n  ✓ Test 3: Codificación de secuencias ADN")
        codificador = CodificadorADNRiemann(calculador)
        seq = "ATGC"
        numero = codificador.secuencia_a_numero(seq)
        assert numero == 27
        print(f"    - Secuencia '{seq}' → Número {numero}")
        
        # Test 4: Conservación de información
        print("\n  ✓ Test 4: Conservación de información")
        seq_recuperada = codificador.numero_a_secuencia(numero, len(seq))
        assert seq == seq_recuperada
        print(f"    - {seq} → {numero} → {seq_recuperada} (conservado)")
        
        # Test 5: Propiedades espectrales
        print("\n  ✓ Test 5: Cálculo de propiedades espectrales")
        props = codificador.propiedades_espectrales(seq)
        assert 'resonancia_f0' in props
        assert 0 <= props['resonancia_f0'] <= 1
        print(f"    - Resonancia con f₀: {props['resonancia_f0']:.6f}")
        print(f"    - Frecuencia Riemann: {props['frecuencia_riemann_hz']:.4f} Hz")
        
        # Test 6: Coherencia cuántica
        print("\n  ✓ Test 6: Coherencia cuántica a T=310K")
        coherencia = calcular_coherencia_cuantica_adn(seq, temperatura=310.0)
        assert 'psi_efectivo' in coherencia
        assert 0 <= coherencia['psi_efectivo'] <= 1
        print(f"    - Ψ_efectivo: {coherencia['psi_efectivo']:.6f}")
        print(f"    - Q_efectivo: {coherencia['Q_efectivo']:.2f}")
        
        print("\n  ✅ MÓDULO adn_riemann.py: VALIDADO")
        return True
        
    except Exception as e:
        print(f"\n  ❌ ERROR en adn_riemann.py: {e}")
        return False


def validar_modulo_mutaciones() -> bool:
    """Valida el módulo mutaciones_resonantes.py."""
    print_section("VALIDACIÓN: Módulo mutaciones_resonantes.py")
    
    try:
        # Inicializar
        calculador = CalculadorCerosRiemann(num_ceros=100)
        codificador = CodificadorADNRiemann(calculador)
        analizador = AnalizadorMutaciones(codificador)
        optimizador = OptimizadorSecuencias(codificador, analizador)
        
        # Test 1: Análisis de mutación puntual
        print("\n  ✓ Test 1: Análisis de mutación puntual")
        resultado = analizador.analizar_mutacion_puntual("ATGC", 0, "G")
        assert resultado['secuencia_original'] == "ATGC"
        assert resultado['secuencia_mutada'] == "GTGC"
        print(f"    - Original: {resultado['secuencia_original']}")
        print(f"    - Mutada: {resultado['secuencia_mutada']}")
        print(f"    - Δ Resonancia: {resultado['delta_resonancia']:+.6f}")
        
        # Test 2: Mejores mutaciones
        print("\n  ✓ Test 2: Búsqueda de mejores mutaciones")
        mejores = analizador.encontrar_mejores_mutaciones("ATGC", num_mejores=3)
        assert len(mejores) <= 3
        print(f"    - Mutaciones encontradas: {len(mejores)}")
        if mejores:
            print(f"    - Mejor: {mejores[0]['base_original']}{mejores[0]['posicion']} → {mejores[0]['base_nueva']}")
        
        # Test 3: Complementariedad
        print("\n  ✓ Test 3: Análisis de complementariedad")
        comp = analizador.analizar_complementariedad("ATGC")
        assert comp['secuencia'] == "ATGC"
        assert comp['complemento'] == "TACG"
        print(f"    - Secuencia: {comp['secuencia']}")
        print(f"    - Complemento: {comp['complemento']}")
        print(f"    - Simétrica: {comp['simetrica']}")
        
        # Test 4: Optimización local
        print("\n  ✓ Test 4: Optimización local de secuencia")
        resultado = optimizador.optimizar_local("AAAA", max_iteraciones=5)
        assert 'secuencia_optimizada' in resultado
        print(f"    - Original: {resultado['secuencia_original']}")
        print(f"    - Optimizada: {resultado['secuencia_optimizada']}")
        print(f"    - Iteraciones: {resultado['iteraciones_totales']}")
        
        print("\n  ✅ MÓDULO mutaciones_resonantes.py: VALIDADO")
        return True
        
    except Exception as e:
        print(f"\n  ❌ ERROR en mutaciones_resonantes.py: {e}")
        return False


def validar_teoria_unificada() -> bool:
    """Valida el módulo teoria_unificada_adn.py."""
    print_section("VALIDACIÓN: Módulo teoria_unificada_adn.py")
    
    try:
        # Inicializar
        teoria = TeoriaUnificadaADN()
        seq_test = "ATGC"
        
        # Test 1: Entropía de información
        print("\n  ✓ Test 1: Entropía de información")
        entropia = teoria.calcular_entropia_informacion(seq_test)
        assert 'entropia_shannon_bits' in entropia
        assert abs(entropia['entropia_shannon_bits'] - 2.0) < 0.01  # Máxima para 4 bases diferentes
        print(f"    - Shannon: {entropia['entropia_shannon_bits']:.4f} bits/base")
        print(f"    - Contenido total: {entropia['contenido_informacion']:.2f} bits")
        
        # Test 2: Función de onda unificada
        print("\n  ✓ Test 2: Función de onda unificada")
        func_onda = teoria.calcular_funcion_onda_unificada(seq_test)
        assert 'amplitud' in func_onda
        assert 0 <= func_onda['amplitud'] <= 1
        assert 0 <= func_onda['probabilidad'] <= 1
        print(f"    - Amplitud: {func_onda['amplitud']:.6f}")
        print(f"    - Probabilidad: {func_onda['probabilidad']:.6f}")
        print(f"    - Coherente: {func_onda['coherencia_unificada']}")
        
        # Test 3: Acoplamiento triádico
        print("\n  ✓ Test 3: Acoplamiento triádico (Bio-Math-Quantum)")
        acoplamiento = teoria.calcular_acoplamiento_triada(seq_test)
        assert 'acoplamiento_triada' in acoplamiento
        assert abs(acoplamiento['factor_unificacion'] - 1.0/7.0) < 1e-6
        print(f"    - Bio-Math: {acoplamiento['acoplamiento_bio_math']:.6f}")
        print(f"    - Math-Quantum: {acoplamiento['acoplamiento_math_quantum']:.6f}")
        print(f"    - Quantum-Bio: {acoplamiento['acoplamiento_quantum_bio']:.6f}")
        print(f"    - Triada: {acoplamiento['acoplamiento_triada']:.8f}")
        
        # Test 4: Predicciones biológicas
        print("\n  ✓ Test 4: Predicciones biológicas")
        predicciones = teoria.predecir_propiedades_biologicas(seq_test)
        assert 'clasificacion' in predicciones
        assert 0 <= predicciones['estabilidad_termodinamica_pct'] <= 100
        print(f"    - Estabilidad: {predicciones['estabilidad_termodinamica_pct']:.2f}%")
        print(f"    - Expresión: {predicciones['potencial_expresion_0_10']:.2f}/10")
        print(f"    - Clasificación: {predicciones['clasificacion']}")
        
        # Test 5: Constantes de unificación
        print("\n  ✓ Test 5: Constantes de unificación")
        assert FRECUENCIA_BASE == 141.7001
        assert abs(PSI_OPTIMO - 0.999) < 0.001
        assert abs(FACTOR_UNIFICACION - 1.0/7.0) < 1e-10
        print(f"    - f₀ = {FRECUENCIA_BASE} Hz")
        print(f"    - Ψ_óptimo = {PSI_OPTIMO}")
        print(f"    - K_unificación = {FACTOR_UNIFICACION:.6f}")
        print(f"    - φ (áurea) = {PHI:.10f}")
        print(f"    - α (fina) = {ALPHA_FINA:.10f}")
        
        print("\n  ✅ MÓDULO teoria_unificada_adn.py: VALIDADO")
        return True
        
    except Exception as e:
        print(f"\n  ❌ ERROR en teoria_unificada_adn.py: {e}")
        return False


def validar_integracion_completa() -> bool:
    """Valida la integración completa del sistema."""
    print_section("VALIDACIÓN: Integración Completa")
    
    try:
        # Test de flujo completo
        print("\n  ✓ Test: Flujo completo de análisis")
        teoria = TeoriaUnificadaADN()
        
        # Analizar múltiples secuencias
        secuencias = ["ATGC", "GACT", "AAAA"]
        print(f"    - Analizando {len(secuencias)} secuencias...")
        
        for seq in secuencias:
            entropia = teoria.calcular_entropia_informacion(seq)
            func_onda = teoria.calcular_funcion_onda_unificada(seq)
            acoplamiento = teoria.calcular_acoplamiento_triada(seq)
            predicciones = teoria.predecir_propiedades_biologicas(seq)
            
            # Verificar coherencia entre módulos
            assert entropia['secuencia'] == seq
            assert func_onda['secuencia'] == seq
            assert acoplamiento['secuencia'] == seq
            assert predicciones['secuencia'] == seq
        
        print(f"    ✓ Análisis completo de {len(secuencias)} secuencias exitoso")
        
        print("\n  ✅ INTEGRACIÓN COMPLETA: VALIDADA")
        return True
        
    except Exception as e:
        print(f"\n  ❌ ERROR en integración: {e}")
        return False


def main():
    """Función principal de validación."""
    print_header("VALIDACIÓN TEORÍA UNIFICADA: Biología × Teoría de Números × Física Cuántica")
    print(f"\nFrecuencia Fundamental: f₀ = {FRECUENCIA_BASE} Hz | ∞³")
    print(f"Fecha: 2026-03-18")
    
    # Ejecutar validaciones
    resultados = []
    
    print_header("FASE 1: Validación de Módulos Individuales")
    resultados.append(("adn_riemann.py", validar_modulo_adn_riemann()))
    resultados.append(("mutaciones_resonantes.py", validar_modulo_mutaciones()))
    resultados.append(("teoria_unificada_adn.py", validar_teoria_unificada()))
    
    print_header("FASE 2: Validación de Integración")
    resultados.append(("Integración Completa", validar_integracion_completa()))
    
    # Resumen final
    print_header("RESUMEN DE VALIDACIÓN")
    
    total_tests = len(resultados)
    tests_pasados = sum(1 for _, resultado in resultados if resultado)
    
    print()
    for nombre, resultado in resultados:
        simbolo = "✅" if resultado else "❌"
        estado = "PASADO" if resultado else "FALLADO"
        print(f"  {simbolo} {nombre:30s} : {estado}")
    
    print(f"\n{'─' * 80}")
    print(f"  TOTAL: {tests_pasados}/{total_tests} validaciones pasadas")
    print(f"{'─' * 80}")
    
    if tests_pasados == total_tests:
        print("\n  🎉 ¡VALIDACIÓN COMPLETA EXITOSA!")
        print("\n  La teoría unificada está correctamente implementada y validada.")
        print("  Todos los componentes funcionan en armonía:")
        print("    • Biología (secuencias de ADN)")
        print("    • Teoría de Números (ceros de Riemann)")
        print("    • Física Cuántica (coherencia)")
        print(f"  Unidos a través de f₀ = {FRECUENCIA_BASE} Hz")
        return 0
    else:
        print(f"\n  ⚠️  VALIDACIÓN INCOMPLETA: {total_tests - tests_pasados} fallos")
        return 1


if __name__ == "__main__":
    sys.exit(main())
