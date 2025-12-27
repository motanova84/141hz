#!/usr/bin/env python3
"""
Ejemplo de integración del verificador GW250114 con el pipeline existente
"""
import sys
from pathlib import Path

# Agregar directorio de scripts al path
sys.path.insert(0, str(Path(__file__).parent))

from verificador_gw250114 import VerificadorGW250114

def ejemplo_basico():
    """Ejemplo 1: Verificación básica de disponibilidad"""
    print("=" * 60)
    print("EJEMPLO 1: Verificación básica")
    print("=" * 60)
    
    verificador = VerificadorGW250114()
    
    # Verificar si GW250114 está disponible
    disponible = verificador.verificar_disponibilidad_evento()
    
    if disponible:
        print("✅ GW250114 disponible - iniciar análisis")
    else:
        print("⏳ GW250114 no disponible todavía")
    
    print()

def ejemplo_verificacion_eventos_similares():
    """Ejemplo 2: Buscar eventos similares o preliminares"""
    print("=" * 60)
    print("EJEMPLO 2: Búsqueda de eventos similares")
    print("=" * 60)
    
    verificador = VerificadorGW250114()
    
    # Buscar eventos que puedan ser GW250114 o versiones preliminares
    verificador.verificar_eventos_similares()
    
    print()

def ejemplo_analisis_evento():
    """Ejemplo 3: Análisis de un evento específico (si está disponible)"""
    print("=" * 60)
    print("EJEMPLO 3: Análisis de evento (ejemplo conceptual)")
    print("=" * 60)
    
    verificador = VerificadorGW250114()
    
    # Este código se ejecutaría si GW250114 estuviera disponible:
    print("📋 Si GW250114 estuviera disponible, se ejecutaría:")
    print("   1. Descarga de datos de detectores H1, L1, V1")
    print("   2. Análisis espectral en banda 140-143 Hz")
    print("   3. Búsqueda de pico en 141.7001 Hz")
    print("   4. Cálculo de SNR y significancia")
    print("   5. Generación de informe JSON")
    
    print()

def ejemplo_integracion_pipeline():
    """Ejemplo 4: Integración con pipeline de validación existente"""
    print("=" * 60)
    print("EJEMPLO 4: Integración con pipeline existente")
    print("=" * 60)
    
    print("📋 Flujo de integración:")
    print("   1. Pipeline ejecuta validación GW150914 (control)")
    print("   2. Si GW150914 pasa validación (BF > 10, p < 0.01):")
    print("      → Verificador busca GW250114 en catálogo")
    print("   3. Si GW250114 está disponible:")
    print("      → Descarga automática de datos")
    print("      → Aplicación de metodología validada")
    print("      → Generación de resultados")
    print("   4. Si GW250114 no disponible:")
    print("      → Búsqueda de eventos similares")
    print("      → Modo de monitoreo opcional")
    
    print()

def ejemplo_resumen_resultados():
    """Ejemplo 5: Interpretación de resultados"""
    print("=" * 60)
    print("EJEMPLO 5: Interpretación de resultados")
    print("=" * 60)
    
    verificador = VerificadorGW250114()
    
    # Ejemplo de resultados que se generarían
    resultados_ejemplo = {
        'H1': {
            'frecuencia_detectada': 141.7001,
            'snr': 7.5,
            'diferencia': 0.0001,
            'significativo': True,
            'potencia_pico': 1.2e-42
        },
        'L1': {
            'frecuencia_detectada': 141.75,
            'snr': 3.2,
            'diferencia': 0.0499,
            'significativo': False,
            'potencia_pico': 5.6e-43
        }
    }
    
    resumen = verificador.generar_resumen(resultados_ejemplo)
    
    print("📊 Ejemplo de resultados:")
    print(f"   Total detectores analizados: {resumen['total_detectores']}")
    print(f"   Detectores con señal significativa: {resumen['exitosos']}")
    print(f"   Tasa de éxito: {resumen['tasa_exito']*100:.1f}%")
    print(f"   Detectores significativos: {resumen['detectores_significativos']}")
    
    print("\n💡 Interpretación:")
    if resumen['exitosos'] >= 2:
        print("   ✅ Señal confirmada en múltiples detectores")
        print("   ✅ Alta confianza en detección")
    elif resumen['exitosos'] == 1:
        print("   ⚠️  Señal detectada en un solo detector")
        print("   ⚠️  Se requiere análisis adicional")
    else:
        print("   ❌ No se detectó señal significativa")
        print("   ❌ Posible falso positivo o señal débil")
    
    print()

def main():
    """Ejecutar todos los ejemplos"""
    print("\n🌌 EJEMPLOS DE USO - VERIFICADOR GW250114")
    print("=" * 60)
    print()
    
    ejemplos = [
        ejemplo_basico,
        ejemplo_verificacion_eventos_similares,
        ejemplo_analisis_evento,
        ejemplo_integracion_pipeline,
        ejemplo_resumen_resultados
    ]
    
    for ejemplo in ejemplos:
        try:
            ejemplo()
        except Exception as e:
            print(f"❌ Error en ejemplo {ejemplo.__name__}: {e}")
    
    print("=" * 60)
    print("📚 Para más información:")
    print("   - Ver: scripts/verificador_gw250114.py")
    print("   - Test: scripts/test_verificador_gw250114.py")
    print("   - Pipeline: scripts/pipeline_validacion.py")
    print("=" * 60)

if __name__ == "__main__":
    sys.exit(main())
