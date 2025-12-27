#!/usr/bin/env python3
"""
Test Runner - Ejecuta todos los tests del proyecto
Este script es llamado por CI/CD para validar el proyecto.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
"""

import sys
import os
import subprocess
from pathlib import Path

def run_test_file(test_path):
    """Ejecuta un archivo de test individual"""
    print(f"\n{'='*70}")
    print(f"Ejecutando: {test_path.name}")
    print('='*70)
    
    try:
        result = subprocess.run(
            [sys.executable, str(test_path)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"✅ {test_path.name} - PASADO")
            return True
        else:
            print(f"❌ {test_path.name} - FALLIDO")
            print("\nSTDOUT:")
            print(result.stdout)
            print("\nSTDERR:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ {test_path.name} - TIMEOUT (>120s)")
        return False
    except Exception as e:
        print(f"❌ {test_path.name} - ERROR: {e}")
        return False

def main():
    """Ejecuta todos los tests del proyecto"""
    print("="*70)
    print("SUITE DE TESTS - GW250114 141Hz Analysis")
    print("="*70)
    
    # Buscar todos los archivos test_*.py en scripts/
    scripts_dir = Path(__file__).parent
    test_files = sorted(scripts_dir.glob('test_*.py'))
    
    if not test_files:
        print("❌ No se encontraron archivos de test")
        return 1
    
    print(f"\n📝 Encontrados {len(test_files)} archivos de test\n")
    
    results = []
    for test_file in test_files:
        success = run_test_file(test_file)
        results.append((test_file.name, success))
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASADO" if success else "❌ FALLIDO"
        print(f"  {status:12s} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests pasados ({100*passed/total:.1f}%)")
    
    if passed == total:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) fallaron")
        return 1

if __name__ == '__main__':
    sys.exit(main())
