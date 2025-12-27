#!/usr/bin/env python3
"""
Test básico para verificar la funcionalidad del Dashboard Avanzado
"""

import sys
import os
import json

# Añadir el directorio dashboard al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_import_dashboard():
    """Test 1: Verificar que se puede importar el módulo"""
    print("🧪 TEST 1: Importar módulo dashboard")
    print("-" * 60)
    
    try:
        from dashboard import dashboard_avanzado
        print("   ✅ Módulo importado correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error al importar: {e}")
        return False

def test_dashboard_class():
    """Test 2: Verificar la clase DashboardAvanzado"""
    print("\n🧪 TEST 2: Clase DashboardAvanzado")
    print("-" * 60)
    
    try:
        from dashboard.dashboard_avanzado import DashboardAvanzado
        
        dashboard = DashboardAvanzado()
        
        # Verificar atributos iniciales
        assert hasattr(dashboard, 'metricas_tiempo_real'), "Falta atributo metricas_tiempo_real"
        assert hasattr(dashboard, 'estado_sistema'), "Falta atributo estado_sistema"
        assert hasattr(dashboard, 'ultima_actualizacion'), "Falta atributo ultima_actualizacion"
        
        assert dashboard.estado_sistema == "OPTIMO", "Estado inicial debe ser OPTIMO"
        
        print(f"   ✅ Estado inicial: {dashboard.estado_sistema}")
        print(f"   ✅ Atributos verificados correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_app():
    """Test 3: Verificar la aplicación Flask"""
    print("\n🧪 TEST 3: Aplicación Flask")
    print("-" * 60)
    
    try:
        from dashboard.dashboard_avanzado import app
        
        # Verificar que es una aplicación Flask
        assert app is not None, "App no puede ser None"
        assert hasattr(app, 'route'), "App debe tener método route"
        
        print("   ✅ Aplicación Flask creada correctamente")
        
        # Verificar rutas
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/api/stream', '/api/estado-completo']
        
        for route in expected_routes:
            if route in routes:
                print(f"   ✅ Ruta '{route}' registrada")
            else:
                print(f"   ❌ Ruta '{route}' NO encontrada")
                return False
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test 4: Verificar endpoints de la API"""
    print("\n🧪 TEST 4: Endpoints de la API")
    print("-" * 60)
    
    try:
        from dashboard.dashboard_avanzado import app
        
        # Crear cliente de prueba
        with app.test_client() as client:
            # Test endpoint principal
            response = client.get('/')
            assert response.status_code == 200, f"Código de estado incorrecto: {response.status_code}"
            print("   ✅ GET / - OK (200)")
            
            # Test endpoint estado completo
            response = client.get('/api/estado-completo')
            assert response.status_code == 200, f"Código de estado incorrecto: {response.status_code}"
            
            data = json.loads(response.data)
            assert 'sistema' in data, "Falta campo 'sistema'"
            assert 'version' in data, "Falta campo 'version'"
            assert 'metricas' in data, "Falta campo 'metricas'"
            
            print("   ✅ GET /api/estado-completo - OK (200)")
            print(f"   ✅ Sistema: {data['sistema']}")
            print(f"   ✅ Versión: {data['version']}")
            
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_exists():
    """Test 5: Verificar que existe el template HTML"""
    print("\n🧪 TEST 5: Template HTML")
    print("-" * 60)
    
    try:
        template_path = os.path.join(
            os.path.dirname(__file__), 
            'templates', 
            'dashboard_avanzado.html'
        )
        
        if os.path.exists(template_path):
            print(f"   ✅ Template encontrado: {template_path}")
            
            # Verificar que contiene elementos clave
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            checks = [
                ('Dashboard Avanzado GW250114', 'Título del dashboard'),
                ('EventSource', 'API de SSE'),
                ('/api/stream', 'Endpoint de stream'),
                ('/api/estado-completo', 'Endpoint de estado'),
                ('metric-card', 'Cards de métricas'),
                ('system-info', 'Información del sistema')
            ]
            
            for check_str, description in checks:
                if check_str in content:
                    print(f"   ✅ Contiene: {description}")
                else:
                    print(f"   ⚠️  No contiene: {description}")
            
            return True
        else:
            print(f"   ❌ Template no encontrado: {template_path}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Ejecutar todos los tests"""
    print("=" * 70)
    print("🔬 TESTS DEL DASHBOARD AVANZADO GW250114")
    print("=" * 70)
    print()
    
    tests = [
        ("Importar módulo", test_import_dashboard),
        ("Clase DashboardAvanzado", test_dashboard_class),
        ("Aplicación Flask", test_flask_app),
        ("Endpoints de la API", test_api_endpoints),
        ("Template HTML", test_template_exists)
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n❌ Error ejecutando test '{nombre}': {e}")
            resultados.append((nombre, False))
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DE TESTS")
    print("=" * 70)
    
    for nombre, resultado in resultados:
        status = "✅ PASADO" if resultado else "❌ FALLADO"
        print(f"{status}: {nombre}")
    
    exitosos = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    print(f"\n📈 Resultado: {exitosos}/{total} tests pasados")
    print("=" * 70)
    
    if exitosos == total:
        print("✅ TODOS LOS TESTS PASARON")
        return 0
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        return 1

if __name__ == "__main__":
    sys.exit(main())
