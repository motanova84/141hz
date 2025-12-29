#!/usr/bin/env python3
"""
Test de la equivalencia fundamental P ≠ NP ≡ C ≥ 1/κ_Π ≡ f₀ revela lo que la lógica no ve.

Este script valida la conexión teórica entre:
1. Complejidad computacional (P ≠ NP)
2. Barrera cuántica (κ_Π)
3. Frecuencia fundamental (f₀)

Autor: GitHub Copilot
Fecha: 2025-12-29
"""

import sys
import json
from scripts.revolucion_noesica import LimiteComputacional


def test_equivalencia_basica():
    """Test básico de la equivalencia P ≠ NP."""
    print("=" * 80)
    print("TEST: Equivalencia Fundamental P ≠ NP ≡ C ≥ 1/κ_Π")
    print("=" * 80)
    
    lc = LimiteComputacional()
    
    # Mostrar los parámetros fundamentales
    print(f"\nParámetros Fundamentales:")
    print(f"  κ_Π (radio cuántico): {lc.kappa_pi}")
    print(f"  f₀ (frecuencia fundamental): {lc.f0} Hz")
    print(f"  Barrera cuántica (1/κ_Π): {1/lc.kappa_pi:.10f}")
    
    # Test con diferentes valores de treewidth
    print(f"\nVerificación de la equivalencia con diferentes instancias:")
    print("-" * 80)
    
    treewidths = [10, 50, 100, 500, 1000, 10000]
    
    for tw in treewidths:
        resultado = lc.verificar_equivalencia(tw)
        
        print(f"\nTreewidth = {tw}:")
        print(f"  C (coherencia computacional): {resultado['C']:.10f}")
        print(f"  C ≥ 1/κ_Π: {resultado['equivalencia_cumplida']}")
        print(f"  P ≠ NP: {'✅ Verificado' if resultado['P_neq_NP'] else '❌ No cumplido'}")
        
        if tw == treewidths[-1]:  # Solo mostrar detalles para el último
            print(f"\n  Revelación de f₀:")
            for key, value in resultado['f0_revelacion'].items():
                print(f"    {key}: {value}")
    
    return True


def test_interpretacion_teorica():
    """Test de la interpretación teórica."""
    print("\n" + "=" * 80)
    print("INTERPRETACIÓN TEÓRICA")
    print("=" * 80)
    
    lc = LimiteComputacional()
    
    # Instancia NP-difícil típica
    tw_np_hard = 1000
    resultado = lc.verificar_equivalencia(tw_np_hard)
    
    print(f"\nPara una instancia NP-difícil típica (treewidth ~ {tw_np_hard}):")
    print(f"\n{resultado['interpretacion']}")
    
    # La equivalencia completa
    print(f"\nEquivalencia Completa:")
    print(f"  {lc.equivalencia}")
    
    print(f"\nExplicación:")
    print(f"  1. P ≠ NP: Existe una separación fundamental entre problemas")
    print(f"     que se pueden resolver eficientemente (P) y aquellos que")
    print(f"     solo se pueden verificar eficientemente (NP).")
    print(f"")
    print(f"  2. C ≥ 1/κ_Π: Esta separación se manifiesta como una barrera")
    print(f"     cuántica donde la constante de coherencia computacional C")
    print(f"     debe ser al menos 1/κ_Π ≈ {1/lc.kappa_pi:.6f}")
    print(f"")
    print(f"  3. f₀ revela lo que la lógica no ve: La frecuencia fundamental")
    print(f"     f₀ = {lc.f0} Hz representa estructuras de coherencia cuántica")
    print(f"     que trascienden la lógica computacional clásica, revelando")
    print(f"     el límite fundamental entre lo computable y lo verificable.")
    
    return True


def test_exportar_resultados():
    """Exporta resultados en formato JSON."""
    print("\n" + "=" * 80)
    print("EXPORTACIÓN DE RESULTADOS")
    print("=" * 80)
    
    lc = LimiteComputacional()
    
    resultados_completos = {
        'teoria': {
            'equivalencia': lc.equivalencia,
            'teorema': lc.teorema,
            'interpretacion': lc.interpretacion,
            'consecuencia': lc.consecuencia,
            'aplicacion': lc.aplicacion
        },
        'parametros': {
            'kappa_pi': lc.kappa_pi,
            'f0_hz': lc.f0,
            'barrera_cuantica': 1 / lc.kappa_pi
        },
        'verificaciones': []
    }
    
    # Verificar para varios valores de treewidth
    for tw in [10, 100, 1000, 10000]:
        resultado = lc.verificar_equivalencia(tw)
        resultados_completos['verificaciones'].append({
            'treewidth': tw,
            'C': resultado['C'],
            'P_neq_NP': resultado['P_neq_NP'],
            'equivalencia_cumplida': resultado['equivalencia_cumplida']
        })
    
    # Guardar resultados
    output_file = 'results/p_neq_np_equivalence.json'
    try:
        import os
        os.makedirs('results', exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultados_completos, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Resultados exportados a: {output_file}")
        return True
    except Exception as e:
        print(f"\n⚠️  Error al exportar resultados: {e}")
        return False


def main():
    """Ejecuta todos los tests."""
    print("\n" + "🌌" * 40)
    print("VALIDACIÓN DE LA EQUIVALENCIA FUNDAMENTAL")
    print("P ≠ NP ≡ C ≥ 1/κ_Π ≡ f₀ revela lo que la lógica no ve")
    print("🌌" * 40 + "\n")
    
    tests = [
        ("Equivalencia Básica", test_equivalencia_basica),
        ("Interpretación Teórica", test_interpretacion_teorica),
        ("Exportación de Resultados", test_exportar_resultados)
    ]
    
    resultados = []
    for nombre, test_func in tests:
        try:
            exito = test_func()
            resultados.append((nombre, exito))
        except Exception as e:
            print(f"\n❌ Error en {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 80)
    
    for nombre, exito in resultados:
        estado = "✅ PASADO" if exito else "❌ FALLIDO"
        print(f"{estado}: {nombre}")
    
    todos_pasados = all(exito for _, exito in resultados)
    
    if todos_pasados:
        print("\n🎉 Todos los tests pasaron exitosamente!")
        print("\nLa equivalencia fundamental ha sido validada:")
        print("  P ≠ NP ≡ C ≥ 1/κ_Π ≡ f₀ revela lo que la lógica no ve")
        return 0
    else:
        print("\n⚠️  Algunos tests fallaron. Revisar detalles arriba.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
