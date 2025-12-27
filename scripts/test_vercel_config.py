#!/usr/bin/env python3
"""
Test para validar la configuración de Vercel
Verifica que vercel.json contiene todas las configuraciones requeridas
"""

import json
import os
import sys

def test_vercel_config():
    """Valida la estructura y contenido de vercel.json"""
    
    # Ruta al archivo vercel.json
    config_path = os.path.join(os.path.dirname(__file__), '..', 'vercel.json')
    
    print("🔍 Validando configuración de Vercel...")
    
    # Verificar que el archivo existe
    if not os.path.exists(config_path):
        print("❌ ERROR: vercel.json no encontrado")
        return False
    
    # Cargar y parsear JSON
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✓ vercel.json es JSON válido")
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: JSON inválido - {e}")
        return False
    
    # Validar estructura principal
    required_keys = ['version', 'builds', 'routes', 'headers', 'crons', 'functions', 'regions', 'cleanUrls', 'trailingSlash']
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        print(f"❌ ERROR: Faltan claves requeridas: {missing_keys}")
        return False
    print(f"✓ Estructura principal completa ({len(required_keys)} claves)")
    
    # Validar version
    if config['version'] != 2:
        print(f"❌ ERROR: version debe ser 2, es {config['version']}")
        return False
    print("✓ Version correcta (2)")
    
    # Validar builds
    if not config['builds'] or not any(b['src'] == 'index.html' for b in config['builds']):
        print("❌ ERROR: Falta configuración de build para index.html")
        return False
    print("✓ Build configurado para index.html")
    
    # Validar rutas importantes
    required_routes = {
        '/validate': '/scripts/validar_gw150914.py',
        '/multievento': '/scripts/analisis_bayesiano_multievento.py'
    }
    
    routes = {r['src']: r['dest'] for r in config['routes'] if 'src' in r and 'dest' in r}
    for src, expected_dest in required_routes.items():
        if src not in routes:
            print(f"❌ ERROR: Falta ruta {src}")
            return False
        if routes[src] != expected_dest:
            print(f"❌ ERROR: Ruta {src} apunta a {routes[src]}, esperado {expected_dest}")
            return False
    print(f"✓ Rutas principales configuradas ({len(required_routes)})")
    
    # Validar headers personalizados
    required_headers = {
        'X-Powered-By': 'GWPy + Noesis Ψ',
        'X-Frequency': '141.7001 Hz',
        'X-Coherence': 'Verified'
    }
    
    if not config['headers']:
        print("❌ ERROR: No hay configuración de headers")
        return False
    
    headers = {h['key']: h['value'] for h in config['headers'][0]['headers']}
    for key, expected_value in required_headers.items():
        if key not in headers:
            print(f"❌ ERROR: Falta header {key}")
            return False
        if headers[key] != expected_value:
            print(f"❌ ERROR: Header {key} = '{headers[key]}', esperado '{expected_value}'")
            return False
    print(f"✓ Headers personalizados configurados ({len(required_headers)})")
    
    # Validar cron job
    if not config['crons']:
        print("❌ ERROR: No hay configuración de cron")
        return False
    
    cron = config['crons'][0]
    if cron['path'] != '/scripts/analisis_bayesiano_multievento.py':
        print(f"❌ ERROR: Cron path incorrecto: {cron['path']}")
        return False
    if cron['schedule'] != '0 */6 * * *':
        print(f"❌ ERROR: Cron schedule incorrecto: {cron['schedule']}")
        return False
    print("✓ Cron job configurado (cada 6 horas)")
    
    # Validar funciones serverless
    required_functions = [
        'scripts/analisis_bayesiano_multievento.py',
        'scripts/validar_gw150914.py'
    ]
    
    for func_path in required_functions:
        if func_path not in config['functions']:
            print(f"❌ ERROR: Falta configuración de función {func_path}")
            return False
        
        func_config = config['functions'][func_path]
        if 'memory' not in func_config or 'maxDuration' not in func_config:
            print(f"❌ ERROR: Función {func_path} sin configuración completa")
            return False
    print(f"✓ Funciones serverless configuradas ({len(required_functions)})")
    
    # Validar regiones
    required_regions = ['fra1', 'iad1', 'gru1']
    if not all(region in config['regions'] for region in required_regions):
        print(f"❌ ERROR: Faltan regiones. Esperadas: {required_regions}")
        return False
    print(f"✓ Regiones geográficas configuradas ({len(required_regions)})")
    
    # Validar configuración de URLs
    if config['cleanUrls'] != True:
        print("❌ ERROR: cleanUrls debe ser true")
        return False
    if config['trailingSlash'] != False:
        print("❌ ERROR: trailingSlash debe ser false")
        return False
    print("✓ Configuración de URLs correcta")
    
    # Verificar que los scripts referenciados existen
    scripts_dir = os.path.join(os.path.dirname(__file__))
    required_scripts = [
        'validar_gw150914.py',
        'analisis_bayesiano_multievento.py'
    ]
    
    for script in required_scripts:
        script_path = os.path.join(scripts_dir, script)
        if not os.path.exists(script_path):
            print(f"⚠️  ADVERTENCIA: Script referenciado no encontrado: {script}")
        else:
            print(f"✓ Script encontrado: {script}")
    
    print("\n✅ Todas las validaciones pasaron exitosamente!")
    return True

def test_index_html():
    """Valida que index.html existe"""
    
    index_path = os.path.join(os.path.dirname(__file__), '..', 'index.html')
    
    print("\n🔍 Validando index.html...")
    
    if not os.path.exists(index_path):
        print("❌ ERROR: index.html no encontrado")
        return False
    
    # Verificar que es un archivo HTML válido
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if not content.strip().startswith('<!DOCTYPE html>'):
        print("❌ ERROR: index.html no tiene DOCTYPE válido")
        return False
    
    # Verificar elementos importantes
    required_elements = ['141.7001 Hz', 'GW250114', 'Ψ']
    for element in required_elements:
        if element not in content:
            print(f"⚠️  ADVERTENCIA: Elemento '{element}' no encontrado en index.html")
    
    print("✓ index.html existe y es válido")
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("TEST: Configuración Vercel para GW250114-141Hz-Analysis")
    print("=" * 60)
    print()
    
    success = True
    
    # Ejecutar tests
    success = test_vercel_config() and success
    success = test_index_html() and success
    
    print("\n" + "=" * 60)
    if success:
        print("✅ TODOS LOS TESTS PASARON")
        print("=" * 60)
        sys.exit(0)
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("=" * 60)
        sys.exit(1)
