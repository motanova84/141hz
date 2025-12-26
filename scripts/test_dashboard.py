#!/usr/bin/env python3
"""
Tests para el Dashboard de Estado GW250114
Verifica funcionalidad de endpoints y comportamiento
"""
import json
import os
import sys
import tempfile
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dashboard.estado_gw250114 import app


def test_estado_endpoint_sin_resultados():
    """Test endpoint /estado-gw250114 cuando no hay resultados"""
    print("Test 1: Estado sin resultados...")
    
    with app.test_client() as client:
        response = client.get('/estado-gw250114')
        
        assert response.status_code == 200, "Status code debe ser 200"
        assert response.content_type == 'application/json', "Content-Type debe ser JSON"
        
        data = response.get_json()
        assert data['evento'] == 'GW250114', "Evento debe ser GW250114"
        assert 'ultima_verificacion' in data, "Debe incluir ultima_verificacion"
        assert 'timestamp' in data, "Debe incluir timestamp"
        
        print("  ✅ Endpoint responde correctamente sin resultados")
        return True


def test_estado_endpoint_con_resultados():
    """Test endpoint /estado-gw250114 cuando hay resultados"""
    print("Test 2: Estado con resultados...")
    
    # Verificar que existe el archivo de resultados
    results_file = 'resultados/analisis_GW250114.json'
    if not os.path.exists(results_file):
        print("  ⚠️  Archivo de resultados no encontrado, saltando test")
        return True
    
    with app.test_client() as client:
        response = client.get('/estado-gw250114')
        
        assert response.status_code == 200, "Status code debe ser 200"
        
        data = response.get_json()
        assert data['disponible'], "disponible debe ser True"
        assert data['estado'] == 'ANALIZADO', "estado debe ser ANALIZADO"
        assert 'resultados' in data, "Debe incluir resultados"
        
        print("  ✅ Endpoint responde correctamente con resultados")
        return True


def test_monitor_endpoint():
    """Test endpoint /monitor-gw HTML"""
    print("Test 3: Página de monitoreo...")
    
    with app.test_client() as client:
        response = client.get('/monitor-gw')
        
        assert response.status_code == 200, "Status code debe ser 200"
        assert 'text/html' in response.content_type, "Content-Type debe ser HTML"
        
        html = response.get_data(as_text=True)
        
        # Verificar elementos clave del HTML
        assert 'Monitor GW250114' in html, "Debe contener título"
        assert 'actualizarEstado' in html, "Debe contener función JavaScript"
        assert '.estado' in html, "Debe contener estilos CSS"
        assert '/estado-gw250114' in html, "Debe referenciar endpoint API"
        
        print("  ✅ Página de monitoreo se genera correctamente")
        return True


def test_json_structure():
    """Test estructura del JSON de respuesta"""
    print("Test 4: Estructura JSON...")
    
    with app.test_client() as client:
        response = client.get('/estado-gw250114')
        data = response.get_json()
        
        # Campos requeridos
        required_fields = [
            'evento', 'ultima_verificacion', 'disponible', 
            'estado', 'mensaje', 'eventos_similares', 'timestamp'
        ]
        
        for field in required_fields:
            assert field in data, f"Campo {field} debe estar presente"
        
        # Tipos de datos
        assert isinstance(data['evento'], str), "evento debe ser string"
        assert isinstance(data['disponible'], bool), "disponible debe ser boolean"
        assert isinstance(data['timestamp'], (int, float)), "timestamp debe ser numérico"
        assert isinstance(data['eventos_similares'], list), "eventos_similares debe ser lista"
        
        print("  ✅ Estructura JSON correcta")
        return True


def test_multiple_requests():
    """Test múltiples peticiones consecutivas"""
    print("Test 5: Múltiples peticiones...")
    
    with app.test_client() as client:
        for i in range(5):
            response = client.get('/estado-gw250114')
            assert response.status_code == 200, f"Request {i+1} falló"
        
        print("  ✅ Múltiples peticiones funcionan correctamente")
        return True


def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n🧪 TESTS DEL DASHBOARD GW250114")
    print("=" * 50)
    
    tests = [
        test_estado_endpoint_sin_resultados,
        test_estado_endpoint_con_resultados,
        test_monitor_endpoint,
        test_json_structure,
        test_multiple_requests
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"  ❌ FALLO: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed} pasados, {failed} fallidos")
    
    if failed == 0:
        print("✅ Todos los tests pasaron exitosamente")
        return 0
    else:
        print("❌ Algunos tests fallaron")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
