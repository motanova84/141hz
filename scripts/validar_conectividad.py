#!/usr/bin/env python3
"""
Validador de conectividad GWOSC - Paso a paso según problema statement
Prueba que el usuario está conectado a GWOSC y puede acceder a los datos
"""
import gwpy.timeseries as ts
from gwosc.datasets import find_datasets
from gwosc import datasets
import sys
import traceback

def validar_conectividad_gwosc():
    """
    Valida que la conexión a GWOSC funciona correctamente
    Implementa el test mencionado en el problema statement:
    
    import gwpy.timeseries as ts
    from gwosc.datasets import find_datasets
    print(find_datasets(type="event", detector="H1"))
    """
    print("🌐 Validando conectividad a GWOSC...")
    print("="*50)
    
    try:
        # Test 1: Conectividad básica a GWOSC API
        print("📡 Test 1: Conectividad básica a GWOSC API")
        eventos = find_datasets(type="event", detector="H1")
        print(f"   ✅ Conexión exitosa: {len(eventos)} eventos encontrados")
        
        # Test 2: Verificar que GW150914 está disponible
        print("\n📊 Test 2: Verificar disponibilidad de GW150914")
        gw150914_disponible = "GW150914" in eventos
        if gw150914_disponible:
            print("   ✅ GW150914 disponible para análisis")
        else:
            print("   ❌ GW150914 no encontrado en la lista de eventos")
            return False
        
        # Test 3: Obtener información detallada de GW150914
        print("\n🔍 Test 3: Información detallada de GW150914")
        try:
            event_info = datasets.event_gps("GW150914")
            print(f"   ✅ GPS time GW150914: {event_info}")
            
            # Verificar que es el tiempo correcto esperado
            expected_gps = 1126259462.423  # Tiempo conocido de GW150914
            if abs(event_info - expected_gps) < 1:  # Tolerancia de 1 segundo
                print("   ✅ Tiempo GPS verificado correctamente")
            else:
                print(f"   ⚠️  Tiempo GPS inesperado (esperado ~{expected_gps})")
        except Exception as e:
            print(f"   ❌ Error obteniendo info de GW150914: {e}")
            return False
            
        # Test 4: Test de descarga pequeña (solo 1 segundo para rapidez)
        print("\n🔄 Test 4: Test de descarga de datos")
        try:
            # Intentar descargar 1 segundo de datos de H1 alrededor de GW150914
            gps_center = 1126259462
            data_test = ts.TimeSeries.fetch_open_data(
                'H1', gps_center-0.5, gps_center+0.5, 
                sample_rate=1024  # Baja resolución para test rápido
            )
            print(f"   ✅ Descarga de test exitosa: {len(data_test)} muestras")
            print(f"   📊 Sample rate: {data_test.sample_rate} Hz")
            
        except Exception as e:
            print(f"   ❌ Error en descarga de test: {e}")
            return False
            
        print("\n🚀 VALIDACIÓN EXITOSA")
        print("   Todas las pruebas de conectividad pasaron correctamente")
        print("   El sistema está listo para análisis reproducible")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR DE CONECTIVIDAD: {e}")
        print("\n🔧 Posibles soluciones:")
        print("   1. Verificar conexión a internet")
        print("   2. Actualizar gwpy: pip install --upgrade gwpy>=3.0.0")
        print("   3. Verificar que gwosc funciona: pip install --upgrade gwosc")
        print("   4. Si está en Windows, considerar usar Docker o WSL")
        return False

def main():
    """Ejecutor principal del validador"""
    print("🌌 GW250114 - 141.7001 Hz Analysis")
    print("📋 Validador de Conectividad GWOSC")
    print("🎯 Basado en el problema statement de validación paso a paso")
    print()
    
    exito = validar_conectividad_gwosc()
    
    if exito:
        print("\n✅ SISTEMA PREPARADO")
        print("   Puede continuar con el análisis de GW150914 (control)")
        print("   Ejecute: python scripts/validar_gw150914.py")
        sys.exit(0)
    else:
        print("\n❌ SISTEMA NO PREPARADO")
        print("   Resuelva los problemas de conectividad antes de continuar")
        sys.exit(1)

if __name__ == "__main__":
    main()
