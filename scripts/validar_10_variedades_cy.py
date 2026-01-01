#!/usr/bin/env python3
"""
Validación simple de las 10 variedades Calabi-Yau
Puede ejecutarse sin pytest
"""

import sys
from pathlib import Path

# Añadir scripts al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analizar_variedades_cy_10 import (
    cargar_variedades_cy,
    validar_euler_caracteristica,
    calcular_estadisticas
)


def test_carga_basica():
    """Test básico de carga de datos."""
    print("Test: Carga básica de datos...")
    variedades = cargar_variedades_cy()
    assert len(variedades) == 10, f"Error: Se esperaban 10 variedades, se encontraron {len(variedades)}"
    print("✓ Pasado: 10 variedades cargadas")


def test_estructura_datos():
    """Test de estructura de datos."""
    print("\nTest: Estructura de datos...")
    variedades = cargar_variedades_cy()
    
    campos_requeridos = ['ID', 'Nombre', 'h11', 'h21', 'alpha', 'beta', 'kappa_pi', 'chi_Euler']
    
    for v in variedades:
        for campo in campos_requeridos:
            assert campo in v, f"Error: Campo {campo} faltante en variedad {v.get('ID', 'desconocida')}"
    
    print(f"✓ Pasado: Todas las variedades tienen {len(campos_requeridos)} campos requeridos")


def test_euler_caracteristica():
    """Test de la característica de Euler."""
    print("\nTest: Característica de Euler χ = 2(h11 - h21)...")
    variedades = cargar_variedades_cy()
    
    errores = []
    for v in variedades:
        chi_esperado = 2 * (v['h11'] - v['h21'])
        if v['chi_Euler'] != chi_esperado:
            errores.append(f"{v['ID']}: χ={v['chi_Euler']}, esperado={chi_esperado}")
    
    if errores:
        print(f"✗ Falló: {len(errores)} variedades con χ incorrecto")
        for error in errores:
            print(f"  - {error}")
        sys.exit(1)
    
    print("✓ Pasado: Todas las variedades satisfacen χ = 2(h11 - h21)")


def test_valores_quintica():
    """Test de la variedad CY-001 (Quíntica)."""
    print("\nTest: Valores de la Quíntica ℂℙ⁴[5]...")
    variedades = cargar_variedades_cy()
    cy001 = variedades[0]
    
    assert cy001['ID'] == 'CY-001', f"Error: ID incorrecto {cy001['ID']}"
    assert cy001['h11'] == 1, f"Error: h11={cy001['h11']}, esperado=1"
    assert cy001['h21'] == 101, f"Error: h21={cy001['h21']}, esperado=101"
    assert cy001['chi_Euler'] == -200, f"Error: χ={cy001['chi_Euler']}, esperado=-200"
    
    print("✓ Pasado: Quíntica tiene los valores correctos")


def test_monotonia_parametros():
    """Test de monotonía de α y β."""
    print("\nTest: Monotonía de parámetros α y β...")
    variedades = cargar_variedades_cy()
    
    # α debe ser creciente
    for i in range(len(variedades) - 1):
        if variedades[i]['alpha'] > variedades[i+1]['alpha']:
            print(f"✗ Falló: α no es creciente entre {variedades[i]['ID']} y {variedades[i+1]['ID']}")
            sys.exit(1)
    
    # β debe ser decreciente
    for i in range(len(variedades) - 1):
        if variedades[i]['beta'] < variedades[i+1]['beta']:
            print(f"✗ Falló: β no es decreciente entre {variedades[i]['ID']} y {variedades[i+1]['ID']}")
            sys.exit(1)
    
    print("✓ Pasado: α es creciente y β es decreciente")


def test_universalidad_kappa_pi():
    """Test de universalidad de κ_Π."""
    print("\nTest: Universalidad de κ_Π...")
    variedades = cargar_variedades_cy()
    kappa_values = [v['kappa_pi'] for v in variedades]
    
    kappa_min = min(kappa_values)
    kappa_max = max(kappa_values)
    variacion = (kappa_max - kappa_min) / kappa_min
    
    if variacion >= 0.01:
        print(f"✗ Falló: Variación de κ_Π es {variacion*100:.2f}%, esperado < 1%")
        sys.exit(1)
    
    print(f"✓ Pasado: κ_Π tiene variación de {variacion*100:.4f}% < 1%")


def test_estadisticas():
    """Test de cálculo de estadísticas."""
    print("\nTest: Cálculo de estadísticas...")
    variedades = cargar_variedades_cy()
    stats = calcular_estadisticas(variedades)
    
    assert 'n_variedades' in stats
    assert stats['n_variedades'] == 10
    
    campos = ['h11', 'h21', 'alpha', 'beta', 'kappa_pi', 'chi_Euler']
    for campo in campos:
        assert campo in stats, f"Error: Campo {campo} faltante en estadísticas"
        assert 'min' in stats[campo], f"Error: 'min' faltante para {campo}"
        assert 'max' in stats[campo], f"Error: 'max' faltante para {campo}"
        assert 'mean' in stats[campo], f"Error: 'mean' faltante para {campo}"
        assert 'std' in stats[campo], f"Error: 'std' faltante para {campo}"
    
    print("✓ Pasado: Estadísticas calculadas correctamente")


def main():
    """Ejecutar todos los tests."""
    print("=" * 80)
    print("VALIDACIÓN DE 10 VARIEDADES CALABI-YAU")
    print("=" * 80)
    
    tests = [
        test_carga_basica,
        test_estructura_datos,
        test_euler_caracteristica,
        test_valores_quintica,
        test_monotonia_parametros,
        test_universalidad_kappa_pi,
        test_estadisticas,
    ]
    
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"✗ Error inesperado en {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    print("\n" + "=" * 80)
    print(f"TODOS LOS TESTS PASARON ({len(tests)}/{len(tests)})")
    print("=" * 80)
    print("\n✓ Los datos de las 10 variedades Calabi-Yau son válidos")


if __name__ == "__main__":
    main()
