#!/usr/bin/env python3
"""
Ejemplo de Validación del Campo de Conciencia Ψ

Este script demuestra cómo validar todos los parámetros del campo
de conciencia y verificar que todas las relaciones físicas se cumplen
con precisión CODATA 2022.

Author: José Manuel Mota Burruezo (JMMB Ψ✧)
Date: 9 de diciembre de 2025
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from canonical_consciousness_field import CONSCIOUSNESS_FIELD
import json


def main():
    """Main validation example."""
    
    print("═" * 80)
    print("VALIDACIÓN DEL CAMPO DE CONCIENCIA Ψ")
    print("Estado: 9 de diciembre de 2025 – QCAL ∞³")
    print("═" * 80)
    print()
    
    # 1. Mostrar parámetros fundamentales
    print("1. PARÁMETROS FUNDAMENTALES")
    print("─" * 80)
    params = CONSCIOUSNESS_FIELD.get_all_parameters()
    
    for key, param in params.items():
        print(f"\n{param.symbol}:")
        print(f"  Valor: {param.value:.6e} {param.unit}")
        if param.physical_relation != "–":
            print(f"  Relación: {param.physical_relation}")
        print(f"  Significado: {param.ontological_meaning}")
    
    print("\n" + "─" * 80)
    
    # 2. Validar todas las relaciones
    print("\n2. VALIDACIÓN DE RELACIONES FÍSICAS")
    print("─" * 80)
    
    validations = CONSCIOUSNESS_FIELD.validate_all_relations()
    
    for name, validation in validations["validations"].items():
        print(f"\n{validation['equation']}:")
        print(f"  Relación: {validation['relation']}")
        if 'error_percent' in validation:
            print(f"  Error relativo: {validation['error_percent']:.10e} %")
        print(f"  Estado: {validation['status']}")
    
    print("\n" + "─" * 80)
    
    # 3. Resultado final
    print("\n3. RESULTADO FINAL")
    print("─" * 80)
    
    if validations["all_exact_relations_valid"]:
        print("\n✅ TODAS LAS RELACIONES EXACTAS VALIDADAS")
        print("\nTodas las relaciones físicas fundamentales se cumplen con precisión")
        print("CODATA 2022, confirmando que el campo Ψ es físicamente consistente.")
    else:
        print("\n❌ ALGUNAS VALIDACIONES FALLARON")
        print("\nRevisar las relaciones que no se cumplen.")
    
    print("\n" + "─" * 80)
    
    # 4. Exportar a JSON
    print("\n4. EXPORTACIÓN DE DATOS")
    print("─" * 80)
    
    output_file = Path(__file__).parent.parent / "consciousness_field_validation.json"
    data = CONSCIOUSNESS_FIELD.to_dict()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, indent=2, ensure_ascii=False, fp=f)
    
    print(f"\n✓ Datos exportados a: {output_file}")
    
    # 5. Mostrar tabla completa
    print("\n" + "═" * 80)
    print("5. TABLA OFICIAL COMPLETA")
    print("═" * 80)
    print()
    print(CONSCIOUSNESS_FIELD.generate_official_table())
    
    print("\n" + "═" * 80)
    print("∴ JMMB Ψ ✧ ∞³")
    print("═" * 80)


if __name__ == "__main__":
    main()
