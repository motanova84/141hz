#!/usr/bin/env python3
"""
Test para verificacion_sistema_optimizado.py
Verifica que el módulo funcione correctamente
"""
import sys
from pathlib import Path

# Añadir directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent))

def test_verificar_optimizacion_importable():
    """Test: El módulo puede ser importado"""
    try:
        from verificacion_sistema_optimizado import verificar_optimizacion_maxima
        print("✅ TEST 1: Módulo importable correctamente")
        return True
    except Exception as e:
        print(f"❌ TEST 1: Error importando módulo: {e}")
        return False

def test_verificar_optimizacion_ejecutable():
    """Test: La función principal es ejecutable"""
    try:
        from verificacion_sistema_optimizado import verificar_optimizacion_maxima
        metricas = verificar_optimizacion_maxima()
        
        # Verificar que retorna las métricas esperadas
        metricas_esperadas = [
            'tiempo_respuesta',
            'precision_frecuencia',
            'sensibilidad',
            'cobertura_fuentes',
            'redundancia',
            'resiliencia'
        ]
        
        for metrica in metricas_esperadas:
            assert metrica in metricas, f"Métrica '{metrica}' no encontrada"
        
        print("\n✅ TEST 2: Función ejecutable y retorna métricas correctas")
        return True
    except Exception as e:
        print(f"\n❌ TEST 2: Error ejecutando función: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_resumen_optimizacion():
    """Test: La función de resumen funciona"""
    try:
        from verificacion_sistema_optimizado import mostrar_resumen_optimizacion
        mostrar_resumen_optimizacion()
        print("\n✅ TEST 3: Resumen de optimización funcional")
        return True
    except Exception as e:
        print(f"\n❌ TEST 3: Error mostrando resumen: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("=" * 70)
    print("🧪 TESTS PARA VERIFICACION_SISTEMA_OPTIMIZADO.PY")
    print("=" * 70)
    
    tests = [
        test_verificar_optimizacion_importable,
        test_verificar_optimizacion_ejecutable,
        test_resumen_optimizacion
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            results.append(False)
    
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"📊 RESULTADOS: {passed}/{total} tests pasados")
    
    if passed == total:
        print("🎉 ¡TODOS LOS TESTS PASADOS!")
        print("=" * 70)
        return 0
    else:
        print("⚠️  Algunos tests fallaron")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
