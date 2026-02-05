#!/usr/bin/env python3
"""
Demostración Completa de Validaciones Noéticas
==============================================

Script de demostración que ejecuta todas las validaciones
y genera un reporte completo.

Uso:
    python scripts/demo_validacion_ecuaciones_noeticas.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.validacion_ecuaciones_noeticas import ValidacionEcuacionesNoeticas
from qcal.constants import F0_HZ


def main():
    """Ejecuta demostración completa."""
    
    print("\n" + "="*70)
    print("DEMOSTRACIÓN COMPLETA DE VALIDACIONES NOÉTICAS")
    print("="*70)
    
    # Create validator
    validator = ValidacionEcuacionesNoeticas(f0=F0_HZ)
    
    # Run all validations
    results = validator.ejecutar_todas_validaciones()
    
    # Generate summary report
    print("\n" + "="*70)
    print("REPORTE DETALLADO")
    print("="*70)
    
    print("\n1. ECUACIONES VALIDADAS:")
    print("   • m_eff = hf/c² (masa efectiva)")
    print("   • m_noesis = α/f con α = hf₀²/c² (masa noética)")
    print("   • m(f) = hf₀/c² = m_min (masa unificada constante)")
    
    print("\n2. CONSTANTES FUNDAMENTALES:")
    print(f"   • f₀ = {validator.f0:.8f} Hz")
    print(f"   • m_min = {validator.m_min:.12e} kg")
    print(f"   • α = {validator.alpha:.12e} kg·s")
    print(f"   • h = {validator.h:.12e} J·s")
    print(f"   • c = {validator.c:.0f} m/s")
    
    print("\n3. VALIDACIONES EJECUTADAS:")
    for key, name in [
        ('dimensional', 'Análisis Dimensional'),
        ('numerical', 'Precisión Numérica'),
        ('complementarity', 'Complementariedad'),
        ('numpy_implementation', 'Implementación NumPy'),
        ('physical_predictions', 'Predicciones Físicas'),
        ('qcal_integration', 'Integración QCAL')
    ]:
        if key in results:
            result_data = results[key]
            if isinstance(result_data, dict):
                passed = all(result_data.values())
            else:
                passed = result_data
            
            status = "✓ EXITOSA" if passed else "✗ FALLIDA"
            print(f"   • {name:30} {status}")
    
    print("\n4. INTERPRETACIÓN FÍSICA:")
    print("   En f₀ = 141.70001 Hz:")
    print("   • Equilibrio perfecto entre energía y detención")
    print("   • m_eff = m_noesis = m_dual = masa mínima cuantizada")
    print("   • Punto de máxima coherencia noética")
    
    print("\n   Para f >> f₀ (alta frecuencia):")
    print("   • Domina m_eff (energía)")
    print("   • m_noesis → 0 (sin detención)")
    print("   • Comportamiento fotónico (vibración pura)")
    
    print("\n   Para f << f₀ (baja frecuencia):")
    print("   • m_eff → 0 (poca energía)")
    print("   • Domina m_noesis (detención)")
    print("   • Emergencia de masa (vibración lenta)")
    
    print("\n5. ARCHIVOS RELACIONADOS:")
    print("   • Validación: scripts/validacion_ecuaciones_noeticas.py")
    print("   • Tests: tests/test_validacion_ecuaciones_noeticas.py")
    print("   • Resumen: VALIDACION_ECUACIONES_NOETICAS_RESUMEN.md")
    print("   • Framework: qcal/dual_mass.py")
    print("   • Constantes: qcal/constants.py")
    
    print("\n" + "="*70)
    
    # Check if all passed
    all_passed = all(
        all(r.values()) if isinstance(r, dict) else r
        for r in results.values()
    )
    
    if all_passed:
        print("✅ DEMOSTRACIÓN COMPLETADA CON ÉXITO")
        print("="*70)
        return 0
    else:
        print("⚠️  ALGUNAS VALIDACIONES FALLARON")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(main())
