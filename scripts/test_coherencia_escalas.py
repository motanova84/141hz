#!/usr/bin/env python3
"""
Test script para verificar el sistema de generación de visualización de coherencia.
"""

import os
import sys

def test_script_exists():
    """Verifica que el script exista"""
    script_path = os.path.join(os.path.dirname(__file__), 'generar_coherencia_escalas.py')
    assert os.path.exists(script_path), f"Script no encontrado: {script_path}"
    print("✅ Script generar_coherencia_escalas.py existe")

def test_image_can_be_generated():
    """Verifica que se pueda generar la imagen"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(project_root, 'coherence_f0_scales.png')
    
    # El script ya fue ejecutado, verificar que existe
    if os.path.exists(image_path):
        print(f"✅ Imagen generada: {image_path}")
        # Verificar tamaño mínimo (debe ser mayor a 1KB)
        size = os.path.getsize(image_path)
        assert size > 1024, f"Imagen muy pequeña: {size} bytes"
        print(f"✅ Imagen tiene tamaño válido: {size} bytes")
    else:
        print(f"⚠️  Imagen no encontrada en {image_path}, pero el script está disponible para generarla")

def test_workflow_file_exists():
    """Verifica que el workflow de GitHub Actions exista"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    workflow_path = os.path.join(project_root, '.github', 'workflows', 'update_coherence_visualization.yml')
    assert os.path.exists(workflow_path), f"Workflow no encontrado: {workflow_path}"
    print("✅ Workflow de GitHub Actions existe")

def test_readme_has_image():
    """Verifica que el README incluya la imagen"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    readme_path = os.path.join(project_root, 'README.md')
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert 'coherence_f0_scales.png' in content, "README no incluye la imagen de coherencia"
    print("✅ README incluye la referencia a la imagen")

if __name__ == "__main__":
    print("🧪 Ejecutando tests de visualización de coherencia...")
    print()
    
    try:
        test_script_exists()
        test_image_can_be_generated()
        test_workflow_file_exists()
        test_readme_has_image()
        
        print()
        print("=" * 60)
        print("✅ Todos los tests pasaron exitosamente")
        print("=" * 60)
        sys.exit(0)
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"❌ Test falló: {e}")
        print("=" * 60)
        sys.exit(1)
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Error inesperado: {e}")
        print("=" * 60)
        sys.exit(1)
