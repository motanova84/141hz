#!/usr/bin/env python3
"""
2. FALSABILIDAD EXPLÍCITA

No es "creeme", es "verifícalo tú mismo"

Define criterios claros y específicos que falsarían la hipótesis de 141.7001 Hz
como frecuencia fundamental del campo noésico.
"""

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.validador_pilares import guardar_json


def criterios_falsacion():
    """
    Define criterios explícitos de falsación científica.
    
    Returns:
        dict: Criterios de falsación verificables
    """
    print("=" * 70)
    print("2. FALSABILIDAD EXPLÍCITA")
    print("=" * 70)
    print()
    print("🔬 No es 'créeme', es 'verifícalo tú mismo'")
    print()
    print("python")
    print("# Criterios explícitos que falsarían la hipótesis")
    
    criterios = {
        'gravitacional': {
            'criterio': 'Ausencia en GWTC-3+',
            'descripcion': 'Si la frecuencia 141.7 Hz no aparece en ningún evento de GWTC-3 o catálogos posteriores',
            'metodo_verificacion': 'Análisis espectral de todos los eventos con SNR > 5',
            'umbral_falsacion': 'Ausencia en >10 eventos con masa total >50 M☉',
            'estado': 'VERIFICABLE'
        },
        'topologico': {
            'criterio': 'No detección en Bi₂Se₃ @ 4K',
            'descripcion': 'Si experimentos en aislantes topológicos Bi₂Se₃ a 4K no muestran resonancia',
            'metodo_verificacion': 'Espectroscopía de impedancia en banda 140-143 Hz',
            'umbral_falsacion': 'Ausencia de pico espectral con Q > 100 en ±1 Hz',
            'estado': 'PENDIENTE EXPERIMENTAL'
        },
        'cosmologico': {
            'criterio': 'Compatibilidad total con ΛCDM',
            'descripcion': 'Si efectos predichos son indistinguibles de ΛCDM estándar',
            'metodo_verificacion': 'Análisis Bayesiano comparativo de modelos cosmológicos',
            'umbral_falsacion': 'Bayes Factor BF < 1 favoreciendo ΛCDM puro',
            'estado': 'VERIFICABLE'
        },
        'neurociencia': {
            'criterio': 'Ausencia en EEG doble ciego',
            'descripcion': 'Si estudios EEG controlados no detectan componente 141.7 Hz',
            'metodo_verificacion': 'EEG de alta resolución (n>100) con protocolo doble ciego',
            'umbral_falsacion': 'p-value > 0.05 en todos los grupos experimentales',
            'estado': 'PENDIENTE EXPERIMENTAL'
        }
    }
    
    print("criterios_falsacion = {")
    for nombre, criterio in criterios.items():
        print(f"    '{nombre}': '{criterio['criterio']}',")
    print("}")
    print()
    
    print("✅ Detalles de Criterios de Falsación:")
    print()
    
    for nombre, criterio in criterios.items():
        print(f"🔬 {nombre.upper()}")
        print(f"   Criterio: {criterio['criterio']}")
        print(f"   Descripción: {criterio['descripcion']}")
        print(f"   Método: {criterio['metodo_verificacion']}")
        print(f"   Umbral: {criterio['umbral_falsacion']}")
        print(f"   Estado: {criterio['estado']}")
        print()
    
    resultado_falsabilidad = {
        'falsabilidad': 'EXPLÍCITA',
        'criterios': criterios,
        'principio': 'Hipótesis científica falsable según criterio de Popper',
        'verificacion': 'Independiente por cualquier laboratorio con equipamiento apropiado'
    }
    
    print("📋 Principio Científico:")
    print(f"   {resultado_falsabilidad['principio']}")
    print(f"   Verificación: {resultado_falsabilidad['verificacion']}")
    print()
    
    # Guardar resultados - Ahora se ejecuta dentro de la función
    output_dir = Path('results')
    output_dir.mkdir(parents=True, exist_ok=True)
    # Guardar resultados automáticamente
    output_dir = Path('results')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'criterios_falsacion.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado_falsabilidad, f, indent=2, ensure_ascii=False)
    
    return resultado_falsabilidad


if __name__ == '__main__':
    try:
        resultados = criterios_falsacion()

        print("📊 Resultados guardados en: results/criterios_falsacion.json")
        print()
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
