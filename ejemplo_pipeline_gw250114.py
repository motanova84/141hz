#!/usr/bin/env python3
"""
Ejemplo de uso del pipeline GW250114 QCAL
=========================================

Este script demuestra cómo usar el pipeline de análisis GW250114
para detectar resonancia en 141.7 Hz y calcular la métrica QCAL.
"""

import sys
import os

# Añadir directorio de scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from pipeline_gw250114_qcal import main_pipeline


def ejemplo_basico():
    """Ejemplo básico con datos simulados."""
    print("=" * 80)
    print("EJEMPLO 1: Análisis con datos simulados")
    print("=" * 80)
    print()
    
    # Ejecutar pipeline con datos simulados
    results = main_pipeline(
        filename=None,  # None = datos simulados
        fs=4096,
        output_dir='results/gw250114_ejemplo1'
    )
    
    # Mostrar resultados clave
    print("\n📊 RESULTADOS CLAVE:")
    print(f"  Frecuencia detectada: {results['detection']['frequency_detected']:.3f} Hz")
    print(f"  Resonancia confirmada: {results['detection']['resonance_detected']}")
    print(f"  SNR: {results['detection']['snr']:.2f}")
    print(f"  Ψ_max: {results['qcal_metric']['Psi_max']:.6f}")
    print(f"  Ψ_mean: {results['qcal_metric']['Psi_mean']:.6f}")
    print(f"  Coherencia noética: {results['noetic_field']['coherence_level']}")
    print(f"  Λ(C^∞): {results['noetic_field']['Lambda_C_inf']:.6f}")
    
    return results


def ejemplo_datos_reales():
    """Ejemplo con archivo de datos reales (si está disponible)."""
    print("\n" + "=" * 80)
    print("EJEMPLO 2: Análisis con datos reales")
    print("=" * 80)
    print()
    
    # Buscar archivo de datos
    posibles_archivos = [
        'data/GW250114_H1_strain.txt',
        'data/GW250114_strain.txt',
        'GW250114_strain.txt'
    ]
    
    archivo_encontrado = None
    for archivo in posibles_archivos:
        if os.path.exists(archivo):
            archivo_encontrado = archivo
            break
    
    if archivo_encontrado:
        print(f"📁 Archivo encontrado: {archivo_encontrado}")
        
        # Ejecutar pipeline con datos reales
        results = main_pipeline(
            filename=archivo_encontrado,
            fs=4096,
            output_dir='results/gw250114_ejemplo2'
        )
        
        return results
    else:
        print("⚠️  No se encontró archivo de datos reales")
        print("   Archivos buscados:")
        for archivo in posibles_archivos:
            print(f"   - {archivo}")
        print()
        print("   Para usar datos reales:")
        print("   1. Descargar GW250114 strain data")
        print("   2. Guardar en uno de los paths anteriores")
        print("   3. Ejecutar este script nuevamente")
        
        return None


def ejemplo_comparacion():
    """Ejemplo de comparación entre detectores H1 y L1."""
    print("\n" + "=" * 80)
    print("EJEMPLO 3: Comparación H1 vs L1")
    print("=" * 80)
    print()
    
    from pipeline_gw250114_qcal import (
        generate_simulated_gw250114_data,
        bandpass_filter,
        normalize_strain,
        spectral_analysis,
        qcal_metric,
        noetic_field_projection
    )
    
    # Generar datos simulados para ambos detectores
    print("📥 Generando datos simulados para H1 y L1...")
    t, strain_h1, strain_l1 = generate_simulated_gw250114_data(fs=4096, duration=32)
    
    # Procesar H1
    print("\n🔬 Procesando H1...")
    h1_filt = bandpass_filter(strain_h1, 4096, 130, 150)
    h1_norm = normalize_strain(h1_filt)
    f, t_spec, mag_h1, bp_h1 = spectral_analysis(h1_norm, 4096, 141.7, 0.15)
    psi_h1 = qcal_metric(bp_h1)
    field_h1 = noetic_field_projection(psi_h1, t_spec)
    
    # Procesar L1
    print("🔬 Procesando L1...")
    l1_filt = bandpass_filter(strain_l1, 4096, 130, 150)
    l1_norm = normalize_strain(l1_filt)
    f, t_spec, mag_l1, bp_l1 = spectral_analysis(l1_norm, 4096, 141.7, 0.15)
    psi_l1 = qcal_metric(bp_l1)
    field_l1 = noetic_field_projection(psi_l1, t_spec)
    
    # Comparar resultados
    print("\n📊 COMPARACIÓN H1 vs L1:")
    print(f"  H1 Ψ_max: {max(psi_h1):.6f}  |  L1 Ψ_max: {max(psi_l1):.6f}")
    print(f"  H1 Φ_mean: {field_h1['Phi_mean']:.6f}  |  L1 Φ_mean: {field_l1['Phi_mean']:.6f}")
    print(f"  H1 Coherencia: {field_h1['coherence_level']}  |  L1 Coherencia: {field_l1['coherence_level']}")
    print(f"  H1 Λ(C^∞): {field_h1['Lambda_C_inf']:.6f}  |  L1 Λ(C^∞): {field_l1['Lambda_C_inf']:.6f}")
    
    # Coherencia cruzada
    import numpy as np
    correlacion = np.corrcoef(psi_h1, psi_l1)[0, 1]
    print(f"\n🔗 Correlación H1-L1: {correlacion:.4f}")
    
    if correlacion > 0.5:
        print("   ✅ Alta coherencia entre detectores - señal consistente")
    elif correlacion > 0.2:
        print("   ⚠️  Coherencia moderada - verificar datos")
    else:
        print("   ❌ Baja coherencia - posible ruido o artefactos")


def main():
    """Función principal - ejecutar todos los ejemplos."""
    print("\n🌌 EJEMPLOS DE USO - Pipeline GW250114 QCAL\n")
    
    # Ejemplo 1: Datos simulados
    try:
        ejemplo_basico()
    except Exception as e:
        print(f"❌ Error en ejemplo básico: {e}")
        import traceback
        traceback.print_exc()
    
    # Ejemplo 2: Datos reales (si están disponibles)
    try:
        ejemplo_datos_reales()
    except Exception as e:
        print(f"❌ Error en ejemplo datos reales: {e}")
        import traceback
        traceback.print_exc()
    
    # Ejemplo 3: Comparación de detectores
    try:
        ejemplo_comparacion()
    except Exception as e:
        print(f"❌ Error en ejemplo comparación: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ Ejemplos completados")
    print("=" * 80)
    print("\n📁 Resultados guardados en:")
    print("   - results/gw250114_ejemplo1/")
    print("   - results/gw250114_ejemplo2/ (si hay datos reales)")
    print()


if __name__ == "__main__":
    main()
