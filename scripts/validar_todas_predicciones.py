#!/usr/bin/env python3
"""
Script Principal: Validación de las 4 Predicciones Falsables QCAL ∞³
========================================================================

Este script ejecuta todas las validaciones de las predicciones falsables
del marco QCAL ∞³ presentadas en el paper.

Predicciones:
    1. Corrección Yukawa (λ_Ψ ≈ 337 km)
    2. Pico Espectral en BEC (k₀ ≈ 890 m⁻¹)
    3. Canal Invisible del Higgs (modulación azimutal)
    4. Modulación Gravitacional (f₀ = 141.7001 Hz)

Autor: José Manuel Mota Burruezo (JMMB Ψ ✧)
Fecha: Diciembre 2025
"""

import sys
import os
import subprocess
from pathlib import Path


def print_header():
    """Imprime encabezado del programa."""
    print("="*80)
    print("VALIDACIÓN DE PREDICCIONES FALSABLES DEL MARCO QCAL ∞³")
    print("Del Campo Ψ a la Verificación Experimental Multiescala")
    print("="*80)
    print()
    print("Autor: José Manuel Mota Burruezo (JMMB Ψ ✧)")
    print("Instituto de Conciencia Cuántica (ICQ)")
    print("ORCID: 0009-0002-1923-0773")
    print()
    print("Este script valida 4 predicciones cuantitativas y falsables:")
    print("  1. Corrección Yukawa a corto alcance del campo gravitacional")
    print("  2. Pico espectral en superfluidos (BEC) a k₀ ≈ 890 m⁻¹")
    print("  3. Canal invisible modulado en el Higgs")
    print("  4. Modulación gravitacional persistente a 141.7001 Hz")
    print()
    print("="*80)
    print()


def ejecutar_validacion(script_name, descripcion):
    """
    Ejecuta un script de validación individual.
    
    Args:
        script_name: Nombre del script a ejecutar
        descripcion: Descripción de la predicción
    
    Returns:
        bool: True si exitoso, False si falla
    """
    print("\n" + "="*80)
    print(f"EJECUTANDO: {descripcion}")
    print("="*80)
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ ERROR: Script no encontrado: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {descripcion} - COMPLETADO")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {descripcion} - FALLÓ")
        print(f"Código de salida: {e.returncode}")
        return False
    
    except Exception as e:
        print(f"\n❌ {descripcion} - ERROR")
        print(f"Excepción: {str(e)}")
        return False


def generar_reporte_final(resultados):
    """
    Genera reporte final de todas las validaciones.
    
    Args:
        resultados: Lista de tuplas (nombre, exito)
    """
    print("\n\n" + "="*80)
    print("REPORTE FINAL DE VALIDACIÓN")
    print("="*80)
    
    total = len(resultados)
    exitosos = sum(1 for _, exito in resultados if exito)
    
    print(f"\nPredicciones validadas: {exitosos}/{total}")
    print()
    
    for nombre, exito in resultados:
        estado = "✅ EXITOSA" if exito else "❌ FALLÓ"
        print(f"  {estado} - {nombre}")
    
    print()
    print("="*80)
    
    if exitosos == total:
        print("🎉 TODAS LAS VALIDACIONES COMPLETADAS EXITOSAMENTE")
        print()
        print("Próximos pasos:")
        print("  1. Revisar gráficas generadas (*.png)")
        print("  2. Consultar paper completo: papers/PREDICCIONES_FALSABLES_QCAL_INFINITO3.md")
        print("  3. Implementar protocolos experimentales propuestos")
    elif exitosos > 0:
        print("⚠️  ALGUNAS VALIDACIONES FALLARON")
        print()
        print("Acción requerida:")
        print("  - Revisar logs de errores arriba")
        print("  - Verificar dependencias instaladas")
    else:
        print("❌ TODAS LAS VALIDACIONES FALLARON")
        print()
        print("Acción requerida:")
        print("  - Verificar que todas las dependencias estén instaladas")
        print("  - Ejecutar: pip install -r requirements.txt")
    
    print("="*80)
    
    return exitosos == total


def main():
    """Función principal."""
    print_header()
    
    # Scripts a ejecutar
    validaciones = [
        (
            "validar_prediccion_yukawa.py",
            "Predicción 1: Corrección Yukawa"
        ),
        (
            "validar_prediccion_bec.py",
            "Predicción 2: Pico Espectral en BEC"
        ),
        (
            "validar_prediccion_higgs.py",
            "Predicción 3: Canal Invisible del Higgs"
        ),
        (
            "validar_prediccion_modulacion_gravitacional.py",
            "Predicción 4: Modulación Gravitacional"
        ),
    ]
    
    # Ejecutar cada validación
    resultados = []
    
    for script, descripcion in validaciones:
        exito = ejecutar_validacion(script, descripcion)
        resultados.append((descripcion, exito))
    
    # Generar reporte final
    exito_total = generar_reporte_final(resultados)
    
    # Retornar código apropiado
    return 0 if exito_total else 1


if __name__ == "__main__":
    sys.exit(main())
