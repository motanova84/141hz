#!/usr/bin/env python3
"""
Generador de Variedades Calabi-Yau con h11 + h21 = 13
======================================================

Este script genera variedades Calabi-Yau con la restricción:
    h^{1,1} + h^{2,1} = 13

Para cada variedad se calcula:
    - ID único: CY_{h11}_{h21}
    - Números de Hodge: h^{1,1} y h^{2,1}
    - Característica de Euler: χ = 2(h^{1,1} - h^{2,1})
    - Invariante κ_Π = log(13) ≈ 2.564949

La restricción h11 + h21 = 13 define una familia especial de CY varieties
relacionadas con el número primo 13 y su logaritmo natural.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: Enero 2026
"""

import json
import math
import sys
from pathlib import Path


def generar_cy_kappa_25773(target_N: int = 13) -> list:
    """
    Genera variedades Calabi-Yau con h11 + h21 = target_N.
    
    Parameters:
        target_N: Suma objetivo de números de Hodge (default: 13)
        
    Returns:
        Lista de diccionarios con datos de cada variedad CY
    """
    cy_varieties = []
    
    # Para h11 + h21 = 13, generamos todas las combinaciones posibles
    # h11 va de 1 a 12 (h21 = 13 - h11)
    for h11 in range(1, target_N):
        h21 = target_N - h11
        
        # Característica de Euler: χ = 2(h^{1,1} - h^{2,1})
        chi_euler = 2 * (h11 - h21)
        
        # Invariante κ_Π = log(h11 + h21) = log(13)
        kappa_pi = round(math.log(h11 + h21), 6)
        
        # Crear entrada para esta variedad
        cy_variety = {
            "ID": f"CY_{h11}_{h21}",
            "h11": h11,
            "h21": h21,
            "chi_Euler": chi_euler,
            "kappa_pi": kappa_pi
        }
        
        cy_varieties.append(cy_variety)
    
    return cy_varieties


def main():
    """Función principal."""
    print("=" * 80)
    print("GENERACIÓN DE VARIEDADES CALABI-YAU CON h^{1,1} + h^{2,1} = 13")
    print("=" * 80)
    print()
    
    # Generar variedades CY con restricción h11 + h21 = 13
    target_N = 13
    cy_varieties = generar_cy_kappa_25773(target_N=target_N)
    
    print(f"✅ Generadas {len(cy_varieties)} variedades Calabi-Yau")
    print(f"   Restricción: h^{{1,1}} + h^{{2,1}} = {target_N}")
    print(f"   κ_Π = log({target_N}) ≈ {math.log(target_N):.6f}")
    print()
    
    # Mostrar resumen
    print("Resumen de variedades generadas:")
    print("-" * 80)
    print(f"{'ID':<12} {'h^{1,1}':<8} {'h^{2,1}':<8} {'χ':<8} {'κ_Π':<12}")
    print("-" * 80)
    
    for cy in cy_varieties:
        print(f"{cy['ID']:<12} {cy['h11']:<8} {cy['h21']:<8} "
              f"{cy['chi_Euler']:<8} {cy['kappa_pi']:<12.6f}")
    
    print("-" * 80)
    print()
    
    # Determinar ruta de salida
    base_dir = Path(__file__).parent.parent
    
    # Intentar guardar en data/ si existe, sino en resultados/
    data_dir = base_dir / "data"
    resultados_dir = base_dir / "resultados"
    
    if data_dir.exists():
        output_dir = data_dir
    elif resultados_dir.exists():
        output_dir = resultados_dir
    else:
        # Crear directorio resultados si no existe
        resultados_dir.mkdir(exist_ok=True)
        output_dir = resultados_dir
    
    # Guardar JSON
    json_path = output_dir / "cy_kappa_25773_log13.json"
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cy_varieties, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Archivo JSON generado exitosamente:")
    print(f"   {json_path}")
    print()
    
    # Mostrar ejemplo de entrada
    print("Ejemplo de entrada del JSON:")
    print("-" * 80)
    if cy_varieties:
        example = cy_varieties[len(cy_varieties) // 2]  # Mostrar uno del medio
        print(json.dumps(example, indent=2, ensure_ascii=False))
    print()
    
    # Información adicional
    print("=" * 80)
    print("INFORMACIÓN SOBRE κ_Π")
    print("=" * 80)
    print()
    print(f"  • h^{{1,1}} + h^{{2,1}} = {target_N}")
    print(f"  • χ = 2(h^{{1,1}} - h^{{2,1}})")
    print(f"  • κ_Π = log({target_N}) ≈ {math.log(target_N):.6f}")
    print()
    print("  Todas las variedades en esta familia tienen el mismo κ_Π")
    print("  ya que todas satisfacen h^{1,1} + h^{2,1} = 13.")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
