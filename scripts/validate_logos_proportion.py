#!/usr/bin/env python3
"""
Validación de la Proporción del Logos: De la Galaxia al Átomo

Este script valida la relación logarítmica entre la línea del hidrógeno
(1,420,405,751 Hz) y la frecuencia fundamental QCAL (141.7001 Hz).

La ecuación fundamental:
    log₂(f_hydrogen / f₀) ≈ 23.257 octavas

Donde:
- 23 octavas representan la ESTRUCTURA (los 23 pares de cromosomas)
- 0.257 es la COMA PITAGÓRICA NOÉTICA (la torsión que permite la evolución)

Autor: José Manuel Mota Burruezo
Licencia: MIT
"""

import math
import mpmath as mp
import json
from typing import Dict, Tuple
import sys
import os

# Add parent directory to path to import qcal
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from qcal.constants import (
    F0_HZ,
    F_HYDROGEN_HZ,
    OCTAVES_LOGOS,
    OCTAVES_STRUCTURE,
    COMA_PYTHAGOREAN_NOETIC,
    OCTAVE_LAYER_STELLAR,
    OCTAVE_LAYER_CHEMISTRY,
    OCTAVE_LAYER_PHYSICS,
    OCTAVE_LAYER_CONSCIOUSNESS
)


def calculate_octave_separation(f_high: float, f_low: float, precision: int = 50) -> Dict:
    """
    Calcula la separación en octavas entre dos frecuencias.
    
    Args:
        f_high: Frecuencia alta (Hz)
        f_low: Frecuencia baja (Hz)
        precision: Precisión decimal para cálculo con mpmath
        
    Returns:
        Dict con octavas totales, parte entera, y coma pitagórica
    """
    # Set precision for arbitrary precision arithmetic
    mp.mp.dps = precision
    
    # Calculate ratio
    ratio = mp.mpf(f_high) / mp.mpf(f_low)
    
    # Calculate octaves: log₂(ratio)
    octaves_total = mp.log(ratio, 2)
    
    # Decompose into integer and fractional parts
    octaves_int = int(octaves_total)
    pythagorean_comma = float(octaves_total - octaves_int)
    
    return {
        'ratio': float(ratio),
        'octaves_total': float(octaves_total),
        'octaves_integer': octaves_int,
        'pythagorean_comma': pythagorean_comma,
        'frequency_high_hz': f_high,
        'frequency_low_hz': f_low
    }


def validate_logos_proportion() -> Dict:
    """
    Valida la Proporción del Logos entre hidrógeno cósmico y frecuencia vital.
    
    Returns:
        Dict con resultados de validación
    """
    print("=" * 80)
    print("VALIDACIÓN DE LA PROPORCIÓN DEL LOGOS")
    print("De la Galaxia al Átomo: El Puente Armónico Universal")
    print("=" * 80)
    print()
    
    # Calculate octave separation
    print("1. CÁLCULO DE SEPARACIÓN EN OCTAVAS")
    print("-" * 80)
    result = calculate_octave_separation(F_HYDROGEN_HZ, F0_HZ)
    
    print(f"Frecuencia Alta (Hidrógeno 21cm): {F_HYDROGEN_HZ:,.0f} Hz")
    print(f"Frecuencia Baja (QCAL f₀):        {F0_HZ:.5f} Hz")
    print(f"Ratio:                            {result['ratio']:.2e}")
    print()
    print(f"Octavas Totales:                  {result['octaves_total']:.6f}")
    print(f"Octavas Enteras (ESTRUCTURA):     {result['octaves_integer']}")
    print(f"Coma Pitagórica (TORSIÓN):        {result['pythagorean_comma']:.6f}")
    print()
    
    # Validate against expected values
    print("2. VALIDACIÓN CONTRA VALORES ESPERADOS")
    print("-" * 80)
    
    tolerance = 0.001  # 0.1% tolerance
    octaves_expected = OCTAVES_LOGOS
    
    error_total = abs(result['octaves_total'] - octaves_expected)
    error_percent = (error_total / octaves_expected) * 100
    
    print(f"Valor Esperado:     {octaves_expected:.6f} octavas")
    print(f"Valor Calculado:    {result['octaves_total']:.6f} octavas")
    print(f"Error Absoluto:     {error_total:.6f}")
    print(f"Error Relativo:     {error_percent:.4f}%")
    print()
    
    is_valid = error_total < tolerance
    
    if is_valid:
        print("✓ VALIDACIÓN EXITOSA: La Proporción del Logos es correcta")
    else:
        print("✗ ERROR: La proporción no coincide con el valor esperado")
    print()
    
    # Interpret the Pythagorean Comma
    print("3. INTERPRETACIÓN DE LA COMA PITAGÓRICA NOÉTICA")
    print("-" * 80)
    print(f"Valor: {result['pythagorean_comma']:.6f}")
    print()
    print("La Coma Pitagórica Noética (0.257) representa:")
    print("  • La desviación que impide el cierre perfecto del círculo")
    print("  • La apertura que permite la espiral evolutiva")
    print("  • La 'Voluntad de Existir' del universo")
    print("  • Si fuera 0 (exactamente 23 octavas), el universo sería estático")
    print()
    
    # Explain the Sacred Triad
    print("4. LA TRÍADA SAGRADA: 23 + 0.257")
    print("-" * 80)
    print(f"23 Octavas (ESTRUCTURA):")
    print(f"  • Los 23 pares de cromosomas humanos")
    print(f"  • El soporte de la vida biológica")
    print(f"  • La 'lira' sobre la que se toca la melodía cósmica")
    print()
    print(f"0.257 (TORSIÓN NOÉTICA):")
    print(f"  • La frecuencia de ajuste fino")
    print(f"  • 'La mano que pulsa la cuerda'")
    print(f"  • El hidrógeno recordando que es 'Dios en miniatura'")
    print()
    
    # Explain Jacob's Ladder
    print("5. ESCALERA DE JACOB: DESCENSO POR LAS OCTAVAS")
    print("-" * 80)
    print(f"Octavas 1-7:       Reino de las Estrellas y Galaxias (Energía Pura)")
    print(f"Octavas 8-14:      Reino de la Materia Estelar y Elementos (Química)")
    print(f"Octavas 15-21:     Reino de la Geometría Planetaria (Física)")
    print(f"Octavas 22-23.257: Umbral de la Consciencia (Biología → Pensamiento)")
    print()
    print("En el último tramo (22-23.257), la frecuencia 'aterriza' en el")
    print("hidrógeno de nuestras células. Es la distancia armónica necesaria")
    print("para que la luz se convierta en pensamiento sin quemar el soporte biológico.")
    print()
    
    # Calculate frequencies at each layer boundary
    print("6. FRECUENCIAS EN LOS LÍMITES DE CADA CAPA")
    print("-" * 80)
    
    boundaries = [1, 7, 8, 14, 15, 21, 22, 23.257]
    print(f"{'Octava':<10} {'Frecuencia (Hz)':<20} {'Dominio':<30}")
    print("-" * 80)
    
    for octave in boundaries:
        freq = F0_HZ * (2 ** octave)
        if octave <= 7:
            domain = "Estelar/Galáctico"
        elif octave <= 14:
            domain = "Químico/Elementos"
        elif octave <= 21:
            domain = "Físico/Planetario"
        else:
            domain = "Consciencia/Noético"
        
        print(f"{octave:<10.3f} {freq:<20,.0f} {domain:<30}")
    
    print()
    
    # Verification summary
    validation_result = {
        'is_valid': is_valid,
        'octaves_calculated': result['octaves_total'],
        'octaves_expected': octaves_expected,
        'error_absolute': error_total,
        'error_percent': error_percent,
        'pythagorean_comma': result['pythagorean_comma'],
        'structure_octaves': result['octaves_integer'],
        'hydrogen_frequency_hz': F_HYDROGEN_HZ,
        'qcal_frequency_hz': F0_HZ,
        'ratio': result['ratio'],
        'interpretation': {
            'structure': '23 chromosome pairs - biological support',
            'torsion': '0.257 Pythagorean comma - noetic adjustment',
            'meaning': 'Bridge between cosmic hydrogen and cellular consciousness'
        }
    }
    
    return validation_result


def save_results(results: Dict, filename: str = 'logos_proportion_validation.json'):
    """
    Guarda los resultados de validación a un archivo JSON.
    
    Args:
        results: Diccionario con resultados
        filename: Nombre del archivo de salida
    """
    output_path = os.path.join(os.path.dirname(__file__), '..', filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Resultados guardados en: {output_path}")
    print()


def main():
    """Función principal."""
    try:
        # Run validation
        results = validate_logos_proportion()
        
        # Save results
        save_results(results)
        
        # Final summary
        print("=" * 80)
        print("RESUMEN FINAL")
        print("=" * 80)
        if results['is_valid']:
            print("✓ La Proporción del Logos ha sido VALIDADA exitosamente")
            print()
            print(f"  log₂({F_HYDROGEN_HZ:,.0f} / {F0_HZ:.5f}) = {results['octaves_calculated']:.6f}")
            print(f"  = {results['structure_octaves']} + {results['pythagorean_comma']:.6f}")
            print()
            print("  El universo no salta en números enteros, sino en logaritmos de belleza.")
            print("  El número 23.257 es el puente exacto que conecta la radiofrecuencia")
            print("  más pura del cosmos con el latido de la vida.")
        else:
            print("✗ La validación ha fallado. Revisar cálculos.")
        print("=" * 80)
        
        return 0 if results['is_valid'] else 1
        
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
