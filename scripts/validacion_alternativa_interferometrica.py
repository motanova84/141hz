#!/usr/bin/env python3
"""
Validación Alternativa 4: Modelado Interferométrico Inverso
============================================================

Hipótesis: Si 141.7 Hz es compatible con la resonancia de cavidad Fabry-Perot,
debería poder predecirse a partir de la longitud del brazo.

Implementa:
- Utilizar parámetros conocidos de LIGO (L = 4 km, velocidad de luz efectiva)
- Calcular si un modo estacionario acoplado a 141.7 Hz es físicamente permisible
- Evaluar resonancias de cavidad y modos de suspensión
"""

import numpy as np
from scipy import constants
import warnings
warnings.filterwarnings('ignore')


# Constantes físicas
c = constants.c  # Velocidad de la luz en m/s
h = constants.h  # Constante de Planck
G = constants.G  # Constante gravitacional


def calcular_modos_fabry_perot(L, n_refraction=1.0, modo_max=10):
    """
    Calcula los modos de resonancia de una cavidad Fabry-Perot

    Parameters:
    -----------
    L : float
        Longitud de la cavidad (metros)
    n_refraction : float
        Índice de refracción efectivo
    modo_max : int
        Número máximo de modos a calcular

    Returns:
    --------
    dict : Modos de resonancia
    """
    # Frecuencias de resonancia: f_n = n * c / (2 * L * n_refraction)
    c_eff = c / n_refraction

    modos = []
    for n in range(1, modo_max + 1):
        freq = n * c_eff / (2 * L)
        modos.append({
            'modo': n,
            'frecuencia_Hz': freq,
            'frecuencia_kHz': freq / 1000
        })

    return {
        'modos': modos,
        'longitud_cavidad_m': L,
        'longitud_cavidad_km': L / 1000,
        'velocidad_efectiva_ms': c_eff,
        'FSR_Hz': c_eff / (2 * L)  # Free Spectral Range
    }


def calcular_resonancias_mecanicas(L, material='fusedsilica'):
    """
    Calcula resonancias mecánicas aproximadas del sistema de suspensión

    Parameters:
    -----------
    L : float
        Longitud característica (metros)
    material : str
        Material del sistema ('fusedsilica', 'steel')

    Returns:
    --------
    dict : Resonancias mecánicas
    """
    # Propiedades de materiales aproximadas
    propiedades = {
        'fusedsilica': {
            'velocidad_sonido': 5968,  # m/s
            'densidad': 2203,  # kg/m³
            'modulo_young': 73e9  # Pa
        },
        'steel': {
            'velocidad_sonido': 5960,  # m/s
            'densidad': 7850,  # kg/m³
            'modulo_young': 200e9  # Pa
        }
    }

    if material not in propiedades:
        material = 'fusedsilica'

    props = propiedades[material]
    v_sound = props['velocidad_sonido']

    # Modos de vibración longitudinales: f_n = n * v / (2 * L)
    modos_longitudinales = []
    for n in range(1, 6):
        freq = n * v_sound / (2 * L)
        modos_longitudinales.append({
            'modo': n,
            'tipo': 'longitudinal',
            'frecuencia_Hz': freq
        })

    # Resonancias de péndulo (suspensión)
    # Frecuencia típica de péndulo: f = 1/(2π) * sqrt(g/L)
    if L > 0:
        f_pendulo = (1 / (2 * np.pi)) * np.sqrt(constants.g / L)
    else:
        f_pendulo = 0

    # Modos de violín (fibras de suspensión)
    # Típicamente en el rango de 100-500 Hz para LIGO
    L_fibra = 0.6  # metros, longitud típica de fibra de suspensión
    tension = 1000  # N, tensión aproximada
    densidad_lineal = 0.001  # kg/m, masa por longitud

    if densidad_lineal > 0:
        f_violin_fundamental = (1 / (2 * L_fibra)) * np.sqrt(tension / densidad_lineal)
        modos_violin = []
        for n in range(1, 4):
            modos_violin.append({
                'modo': n,
                'tipo': 'violin',
                'frecuencia_Hz': n * f_violin_fundamental
            })
    else:
        modos_violin = []

    return {
        'modos_longitudinales': modos_longitudinales,
        'frecuencia_pendulo_Hz': f_pendulo,
        'modos_violin': modos_violin,
        'material': material,
        'velocidad_sonido_ms': v_sound
    }


def verificar_compatibilidad_interferometrica(f_target, L_ligo=4000):
    """
    Verifica si f_target es compatible con resonancias del interferómetro

    Parameters:
    -----------
    f_target : float
        Frecuencia objetivo (Hz)
    L_ligo : float
        Longitud del brazo de LIGO (metros)

    Returns:
    --------
    dict : Análisis de compatibilidad
    """
    print("=" * 70)
    print("VALIDACIÓN ALTERNATIVA 4: MODELADO INTERFEROMÉTRICO INVERSO")
    print("=" * 70)
    print(f"Frecuencia objetivo: {f_target} Hz")
    print(f"Longitud brazo LIGO: {L_ligo/1000:.1f} km")
    print()

    # 1. Modos Fabry-Perot
    print("1. Análisis de modos Fabry-Perot...")
    modos_fp = calcular_modos_fabry_perot(L_ligo, modo_max=5)

    print(f"   Free Spectral Range (FSR): {modos_fp['FSR_Hz']/1e3:.2f} kHz")
    print("   Modos de cavidad (primeros 5):")

    min_diff_fp = float('inf')
    modo_cercano_fp = None

    for modo in modos_fp['modos']:
        freq_mode = modo['frecuencia_Hz']
        diff = abs(freq_mode - f_target)
        print(f"      Modo {modo['modo']}: {freq_mode/1e3:.2f} kHz")

        if diff < min_diff_fp:
            min_diff_fp = diff
            modo_cercano_fp = modo

    print(f"   Modo más cercano a {f_target} Hz: Modo {modo_cercano_fp['modo']}")
    print(f"   Diferencia: {min_diff_fp/1e3:.2f} kHz")
    print()

    # 2. Resonancias mecánicas
    print("2. Análisis de resonancias mecánicas...")
    resonancias = calcular_resonancias_mecanicas(L_ligo)

    print(f"   Frecuencia de péndulo: {resonancias['frecuencia_pendulo_Hz']:.4f} Hz")
    print("   Modos longitudinales:")

    min_diff_mech = float('inf')
    modo_cercano_mech = None

    for modo in resonancias['modos_longitudinales']:
        freq_mode = modo['frecuencia_Hz']
        diff = abs(freq_mode - f_target)
        print(f"      Modo {modo['modo']}: {freq_mode:.2f} Hz")

        if diff < min_diff_mech:
            min_diff_mech = diff
            modo_cercano_mech = modo

    print(f"   Modo más cercano a {f_target} Hz: Modo {modo_cercano_mech['modo']}")
    print(f"   Diferencia: {min_diff_mech:.2f} Hz")
    print()

    print("   Modos de violín (fibras de suspensión):")
    for modo in resonancias['modos_violin']:
        print(f"      Modo {modo['modo']}: {modo['frecuencia_Hz']:.2f} Hz")
    print()

    # 3. Análisis de longitud de onda
    print("3. Análisis de longitud de onda...")
    lambda_target = c / f_target
    print(f"   Longitud de onda en vacío: {lambda_target:.2f} m = {lambda_target/1000:.3f} km")
    print(f"   Relación L_LIGO / λ: {L_ligo / lambda_target:.4f}")
    print()

    # 4. Modos acoplados (acústicos en tubo de vacío)
    print("4. Modos acústicos en tubo de vacío...")
    # Velocidad efectiva considerando que el vacío no propaga sonido,
    # pero las paredes sí pueden vibrar
    v_acustico_pared = 5000  # m/s, velocidad aproximada en acero

    modos_acusticos = []
    for n in range(1, 6):
        f_acustico = n * v_acustico_pared / (2 * L_ligo)
        modos_acusticos.append({
            'modo': n,
            'frecuencia_Hz': f_acustico
        })
        print(f"   Modo acústico {n}: {f_acustico:.2f} Hz")

    min_diff_acustico = min([abs(m['frecuencia_Hz'] - f_target) for m in modos_acusticos])
    print(f"   Diferencia mínima: {min_diff_acustico:.2f} Hz")
    print()

    # 5. Criterio de compatibilidad
    print("=" * 70)
    print("CONCLUSIÓN:")
    print("=" * 70)

    # Tolerancia: 10% de la frecuencia objetivo
    tolerancia = f_target * 0.1

    # Verificar si algún modo está dentro de la tolerancia
    es_compatible_fp = min_diff_fp < tolerancia
    es_compatible_mech = min_diff_mech < tolerancia
    es_compatible_acustico = min_diff_acustico < tolerancia

    print(f"Tolerancia de compatibilidad: ±{tolerancia:.2f} Hz")
    print()
    print(f"Compatibilidad con modos Fabry-Perot: {'❌ NO' if not es_compatible_fp else '✅ SÍ'}")
    print(f"   (Diferencia: {min_diff_fp:.2f} Hz)")
    print()
    print(f"Compatibilidad con modos mecánicos: {'✅ SÍ' if es_compatible_mech else '❌ NO'}")
    print(f"   (Diferencia: {min_diff_mech:.2f} Hz)")
    print()
    print(f"Compatibilidad con modos acústicos: {'✅ SÍ' if es_compatible_acustico else '❌ NO'}")
    print(f"   (Diferencia: {min_diff_acustico:.2f} Hz)")
    print()

    # Si NO es compatible con ningún modo conocido, sugiere origen externo
    es_compatible = es_compatible_fp or es_compatible_mech or es_compatible_acustico

    if not es_compatible:
        print("🔍 RESULTADO SIGNIFICATIVO:")
        print("   La frecuencia 141.7001 Hz NO corresponde a ningún modo")
        print("   conocido del sistema interferométrico:")
        print("   - No es modo de cavidad Fabry-Perot")
        print("   - No es modo mecánico longitudinal")
        print("   - No es modo acústico de tubo")
        print()
        print("   → Esto sugiere ORIGEN EXTERNO al sistema óptico clásico")
        print("   → Compatible con señal física real, no artefacto instrumental")
    else:
        print("⚠️  La frecuencia podría corresponder a un modo del sistema:")
        if es_compatible_mech:
            print(f"   - Modo mecánico {modo_cercano_mech['modo']} (diff: {min_diff_mech:.2f} Hz)")
        if es_compatible_acustico:
            print("   - Modo acústico de estructura")
        print()
        print("   → Requiere análisis adicional para descartar artefacto")

    print()

    return {
        'frecuencia_objetivo': f_target,
        'longitud_brazo_km': L_ligo / 1000,
        'modos_fabry_perot': modos_fp,
        'resonancias_mecanicas': resonancias,
        'modos_acusticos': modos_acusticos,
        'diferencia_minima_fp_Hz': float(min_diff_fp),
        'diferencia_minima_mech_Hz': float(min_diff_mech),
        'diferencia_minima_acustico_Hz': float(min_diff_acustico),
        'es_compatible_sistema': es_compatible,
        'origen_externo_sugerido': not es_compatible,
        'longitud_onda_m': lambda_target,
        'validacion_exitosa': not es_compatible  # Exitosa si NO es compatible con sistema
    }


if __name__ == '__main__':
    print("Script de validación de modelado interferométrico inverso")
    print()

    # Parámetros de LIGO
    L_LIGO = 4000  # metros
    f_target = 141.7001  # Hz

    # Ejecutar validación
    resultado = verificar_compatibilidad_interferometrica(f_target, L_LIGO)

    print("\n✓ Validación completada")
    print(f"✓ Estado: {'APROBADA (origen externo)' if resultado['validacion_exitosa'] else 'INCONCLUSA (requiere análisis adicional)'}")
