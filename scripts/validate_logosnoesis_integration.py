#!/usr/bin/env python3
"""
Validación de Integración LogosNoesis — Fase #260
==================================================

Este script verifica que la integración del framework LogosNoesis
esté correctamente implementada y documentada.

AUTOR: José Manuel Mota Burruezo (JMMB Ψ✧)
FECHA: 2026-03-16
"""

import json
import os
import sys
from pathlib import Path


def check_file_exists(filepath: str, description: str) -> bool:
    """Verifica que un archivo exista."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NO ENCONTRADO: {filepath}")
        return False


def check_file_contains(filepath: str, search_term: str, description: str) -> bool:
    """Verifica que un archivo contenga un término específico."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_term in content:
                print(f"✅ {description}: '{search_term}' encontrado en {filepath}")
                return True
            else:
                print(f"❌ {description}: '{search_term}' NO encontrado en {filepath}")
                return False
    except Exception as e:
        print(f"❌ Error al leer {filepath}: {e}")
        return False


def validate_json_structure(filepath: str, key_path: list, description: str) -> bool:
    """Verifica que una estructura JSON contenga una clave específica."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            current = data
            for key in key_path:
                if key in current:
                    current = current[key]
                else:
                    print(f"❌ {description}: clave '{key}' no encontrada en {filepath}")
                    return False
            print(f"✅ {description}: estructura JSON válida en {filepath}")
            return True
    except Exception as e:
        print(f"❌ Error al validar JSON {filepath}: {e}")
        return False


def main():
    """Ejecuta todas las validaciones."""
    print("=" * 70)
    print("VALIDACIÓN DE INTEGRACIÓN LOGOSNOESIS — FASE #260")
    print("=" * 70)
    print()

    checks = []

    # 1. Verificar que existe LOGOSNOESIS_README.md
    print("1. Documentación Principal")
    print("-" * 70)
    checks.append(check_file_exists(
        "LOGOSNOESIS_README.md",
        "Documentación LogosNoesis"
    ))
    checks.append(check_file_contains(
        "LOGOSNOESIS_README.md",
        "Fase #260",
        "Referencia a Fase #260"
    ))
    checks.append(check_file_contains(
        "LOGOSNOESIS_README.md",
        "**Logos**",
        "Definición de Logos"
    ))
    checks.append(check_file_contains(
        "LOGOSNOESIS_README.md",
        "**Noesis**",
        "Definición de Noesis"
    ))
    checks.append(check_file_contains(
        "LOGOSNOESIS_README.md",
        "QCALStringCore",
        "Referencia a QCALStringCore"
    ))
    print()

    # 2. Verificar actualización de .qcal-context.json
    print("2. Contexto QCAL (.qcal-context.json)")
    print("-" * 70)
    checks.append(check_file_exists(
        ".qcal-context.json",
        "Archivo de contexto QCAL"
    ))
    checks.append(validate_json_structure(
        ".qcal-context.json",
        ["logosnoesis_framework"],
        "Sección logosnoesis_framework"
    ))
    checks.append(validate_json_structure(
        ".qcal-context.json",
        ["logosnoesis_framework", "phase_260"],
        "Detalles de Fase #260"
    ))
    checks.append(validate_json_structure(
        ".qcal-context.json",
        ["logosnoesis_framework", "logos_components"],
        "Componentes Logos"
    ))
    checks.append(validate_json_structure(
        ".qcal-context.json",
        ["logosnoesis_framework", "noesis_components"],
        "Componentes Noesis"
    ))
    checks.append(validate_json_structure(
        ".qcal-context.json",
        ["key_modules", "qcal_string_core"],
        "Módulo qcal_string_core en key_modules"
    ))
    print()

    # 3. Verificar actualización de CROSS_REPOSITORY_INTEGRATION.md
    print("3. Integración Cross-Repositorio")
    print("-" * 70)
    checks.append(check_file_exists(
        "CROSS_REPOSITORY_INTEGRATION.md",
        "Documentación de integración"
    ))
    checks.append(check_file_contains(
        "CROSS_REPOSITORY_INTEGRATION.md",
        "LogosNoesis",
        "Referencia a LogosNoesis"
    ))
    checks.append(check_file_contains(
        "CROSS_REPOSITORY_INTEGRATION.md",
        "Logos+Noesis",
        "Clasificación Logos+Noesis"
    ))
    print()

    # 4. Verificar actualización de qcal/qcal_string_core.py
    print("4. Módulo Principal (qcal/qcal_string_core.py)")
    print("-" * 70)
    checks.append(check_file_exists(
        "qcal/qcal_string_core.py",
        "Módulo qcal_string_core"
    ))
    checks.append(check_file_contains(
        "qcal/qcal_string_core.py",
        "Framework LogosNoesis",
        "Referencia al framework"
    ))
    checks.append(check_file_contains(
        "qcal/qcal_string_core.py",
        "LOGOSNOESIS_README.md",
        "Enlace a documentación"
    ))
    checks.append(check_file_contains(
        "qcal/qcal_string_core.py",
        "Fase #260",
        "Identificación de Fase #260"
    ))
    print()

    # 5. Verificar módulo funcional
    print("5. Verificación Funcional")
    print("-" * 70)
    try:
        sys.path.insert(0, os.getcwd())
        from qcal.qcal_string_core import QCALStringCore
        
        # Crear instancia
        core = QCALStringCore(N=32, seed=42, f0=141.7001)
        
        # Verificar certificado
        cert = core.certify()
        
        # Validaciones
        if cert["certificate"] == "QED-CUERDAS-VERIFIED":
            print(f"✅ Certificado correcto: {cert['certificate']}")
            checks.append(True)
        else:
            print(f"❌ Certificado incorrecto: {cert['certificate']}")
            checks.append(False)
            
        if cert["seal"] == "∴𓂀Ω∞³Φ":
            print(f"✅ Sello correcto: {cert['seal']}")
            checks.append(True)
        else:
            print(f"❌ Sello incorrecto: {cert['seal']}")
            checks.append(False)
            
        expected_peak = 14.134725141734695 * 141.7001  # γ₁ × f₀
        if abs(cert["resonance_peak_hz"] - expected_peak) < 0.01:
            print(f"✅ Pico de resonancia: {cert['resonance_peak_hz']:.2f} Hz ≈ {expected_peak:.2f} Hz")
            checks.append(True)
        else:
            print(f"❌ Pico de resonancia incorrecto: {cert['resonance_peak_hz']:.2f} Hz")
            checks.append(False)
            
        print(f"✅ Módulo QCALStringCore funcional")
        checks.append(True)
        
    except Exception as e:
        print(f"❌ Error al importar o ejecutar QCALStringCore: {e}")
        checks.append(False)
    
    print()

    # Resumen
    print("=" * 70)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 70)
    total = len(checks)
    passed = sum(checks)
    failed = total - passed
    
    print(f"Total de verificaciones: {total}")
    print(f"✅ Exitosas: {passed}")
    print(f"❌ Fallidas: {failed}")
    print(f"Porcentaje de éxito: {100 * passed / total:.1f}%")
    print()
    
    if failed == 0:
        print("🎉 ¡TODAS LAS VALIDACIONES PASARON!")
        print("   La integración LogosNoesis está correctamente implementada.")
        return 0
    else:
        print("⚠️  Algunas validaciones fallaron. Revise los errores arriba.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
