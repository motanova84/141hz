#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validación de Soberanía QCAL ∞³
Sovereignty Validation Script

Este script verifica que todos los componentes del sistema de soberanía
estén correctamente implementados.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Get repository root (parent of scripts directory)
REPO_ROOT = Path(__file__).resolve().parent.parent

def validate_sovereignty():
    """Valida la implementación de soberanía."""
    print("=" * 80)
    print("VALIDACIÓN DE SOBERANÍA QCAL ∞³")
    print("=" * 80)
    print()
    
    errors = []
    warnings = []
    
    # 1. Verificar que existe LICENSE_SOBERANA
    print("1. Verificando LICENSE_SOBERANA...")
    license_path = REPO_ROOT / "LICENSE_SOBERANA"
    if license_path.exists():
        print("   ✓ LICENSE_SOBERANA encontrado")
        content = license_path.read_text(encoding='utf-8')
        if "José Manuel Mota Burruezo" in content:
            print("   ✓ Autoría correcta en LICENSE_SOBERANA")
        else:
            errors.append("Autoría no encontrada en LICENSE_SOBERANA")
        if "141.7001" in content:
            print("   ✓ Frecuencia f₀ correcta en LICENSE_SOBERANA")
        else:
            errors.append("Frecuencia f₀ no encontrada en LICENSE_SOBERANA")
    else:
        errors.append("LICENSE_SOBERANA no encontrado")
    print()
    
    # 2. Verificar core/soberania.py
    print("2. Verificando core/soberania.py...")
    try:
        from core.soberania import (
            verificar_patrimonio, 
            verificar_origen,
            validar_firma_espectral,
            generar_reporte_compliance,
            F0_HZ
        )
        print("   ✓ Módulo core/soberania.py importado correctamente")
        
        # Verificar constante
        if F0_HZ == 141.7001:
            print(f"   ✓ F0_HZ = {F0_HZ} Hz (correcto)")
        else:
            errors.append(f"F0_HZ incorrecto: {F0_HZ} (esperado: 141.7001)")
        
        # Verificar función verificar_patrimonio
        resultado = verificar_patrimonio()
        if "José Manuel Mota Burruezo" in resultado:
            print("   ✓ verificar_patrimonio() funciona correctamente")
        else:
            errors.append("verificar_patrimonio() no retorna autoría correcta")
        
        # Verificar función verificar_origen
        origen = verificar_origen()
        if origen.get("sovereign") == True:
            print("   ✓ verificar_origen() valida soberanía")
        else:
            errors.append("verificar_origen() no valida soberanía")
        
        # Verificar validación espectral
        if validar_firma_espectral(141.7001):
            print("   ✓ validar_firma_espectral() funciona correctamente")
        else:
            errors.append("validar_firma_espectral() falla para f₀")
        
        # Verificar reporte de compliance
        reporte = generar_reporte_compliance()
        if reporte.get("compliance_status") == "SOVEREIGN":
            print("   ✓ generar_reporte_compliance() genera estado SOVEREIGN")
        else:
            errors.append("generar_reporte_compliance() no genera estado SOVEREIGN")
    except ImportError as e:
        errors.append(f"No se puede importar core/soberania.py: {e}")
    print()
    
    # 3. Verificar AGENT_ACTIVATION_REPORT.json
    print("3. Verificando AGENT_ACTIVATION_REPORT.json...")
    report_path = REPO_ROOT / "AGENT_ACTIVATION_REPORT.json"
    if report_path.exists():
        print("   ✓ AGENT_ACTIVATION_REPORT.json encontrado")
        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            if report.get("sovereignty", {}).get("status") == "SOVEREIGN":
                print("   ✓ Estado de soberanía: SOVEREIGN")
            else:
                errors.append("Estado de soberanía incorrecto en AGENT_ACTIVATION_REPORT.json")
            
            if report.get("sovereignty", {}).get("author") == "José Manuel Mota Burruezo (JMMB Ψ✧)":
                print("   ✓ Autoría correcta en AGENT_ACTIVATION_REPORT.json")
            else:
                warnings.append("Autoría en AGENT_ACTIVATION_REPORT.json necesita verificación")
        except json.JSONDecodeError as e:
            errors.append(f"Error al parsear AGENT_ACTIVATION_REPORT.json: {e}")
    else:
        errors.append("AGENT_ACTIVATION_REPORT.json no encontrado")
    print()
    
    # 4. Verificar constantes en qcal/constants.py
    print("4. Verificando qcal/constants.py...")
    try:
        from qcal.constants import F0_HZ as QCAL_F0
        if QCAL_F0 == 141.7001:
            print(f"   ✓ qcal.constants.F0_HZ = {QCAL_F0} Hz (correcto)")
        else:
            errors.append(f"qcal.constants.F0_HZ incorrecto: {QCAL_F0} (esperado: 141.7001)")
    except ImportError as e:
        errors.append(f"No se puede importar qcal.constants: {e}")
    print()
    
    # 5. Verificar README.md
    print("5. Verificando README.md...")
    readme_path = REPO_ROOT / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding='utf-8')
        if "Sovereign" in content:
            print("   ✓ Badge de Sovereign License encontrado en README.md")
        else:
            warnings.append("Badge de Sovereign License no encontrado en README.md")
        if "LICENSE_SOBERANA" in content:
            print("   ✓ Referencia a LICENSE_SOBERANA en README.md")
        else:
            warnings.append("Referencia a LICENSE_SOBERANA no encontrada en README.md")
    else:
        errors.append("README.md no encontrado")
    print()
    
    # Resumen
    print("=" * 80)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 80)
    print()
    
    if errors:
        print(f"❌ ERRORES ({len(errors)}):")
        for error in errors:
            print(f"   - {error}")
        print()
    
    if warnings:
        print(f"⚠️  ADVERTENCIAS ({len(warnings)}):")
        for warning in warnings:
            print(f"   - {warning}")
        print()
    
    if not errors and not warnings:
        print("✓ TODAS LAS VALIDACIONES PASARON")
        print()
        print("El sistema de soberanía QCAL ∞³ está correctamente implementado.")
        print("Todos los badges deberían pasar a VERDE en el próximo escaneo.")
        return 0
    elif not errors:
        print("✓ VALIDACIÓN EXITOSA (con advertencias)")
        return 0
    else:
        print("❌ VALIDACIÓN FALLIDA")
        return 1

if __name__ == "__main__":
    sys.exit(validate_sovereignty())
