#!/usr/bin/env python3
"""
Comparación de Sensibilidad: LIGO vs KAGRA en 141.7 Hz
=======================================================

Analiza y compara las curvas de sensibilidad teóricas y observadas de:
- LIGO Hanford (H1)
- LIGO Livingston (L1)
- KAGRA (K1)

Objetivo: Determinar si KAGRA tiene suficiente sensibilidad en 141.7 Hz
para detectar la señal observada en LIGO.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Noise model constants for LIGO and KAGRA
# Based on published design sensitivities
LIGO_SEISMIC_AMP = 1e-23
LIGO_SEISMIC_FREQ = 10
LIGO_THERMAL_AMP = 4e-24
LIGO_THERMAL_FREQ = 150
LIGO_QUANTUM_AMP = 1.5e-23
LIGO_QUANTUM_FREQ = 200

KAGRA_SEISMIC_AMP = 2e-23  # Higher seismic noise (Japan location)
KAGRA_SEISMIC_FREQ = 10
KAGRA_THERMAL_AMP = 2e-24  # Lower thermal noise (cryogenic)
KAGRA_THERMAL_FREQ = 150
KAGRA_QUANTUM_AMP = 1.5e-23
KAGRA_QUANTUM_FREQ = 200


def obtener_sensibilidad_teorica():
    """
    Obtener curvas de sensibilidad teóricas de LIGO y KAGRA

    Basado en diseños publicados y curvas de ruido esperadas

    Returns:
        dict: Sensibilidades para cada detector
    """
    # Frecuencias de análisis (Hz)
    freqs = np.logspace(1, 3, 1000)  # 10 Hz a 1000 Hz

    # Parámetros de diseño simplificados
    # Estos son aproximaciones basadas en papers publicados

    # LIGO (Advanced LIGO design sensitivity)
    # Ruido cuántico + térmico + sísmico
    def ligo_asd(f):
        """Amplitude Spectral Density de LIGO (aproximada)"""
        # Noise sources
        seismic = LIGO_SEISMIC_AMP * (LIGO_SEISMIC_FREQ / f) ** 2
        thermal = LIGO_THERMAL_AMP / np.sqrt(1 + (f / LIGO_THERMAL_FREQ) ** 2)
        quantum = LIGO_QUANTUM_AMP * np.sqrt(1 + (f / LIGO_QUANTUM_FREQ) ** 2)

        # Total noise (suma cuadrática)
        return np.sqrt(seismic**2 + thermal**2 + quantum**2)

    # KAGRA (Design sensitivity con criogenia)
    def kagra_asd(f):
        """Amplitude Spectral Density de KAGRA (aproximada)"""
        # KAGRA tiene mejor ruido térmico (criogénico) pero peor seísmico (Japón)
        seismic = KAGRA_SEISMIC_AMP * (KAGRA_SEISMIC_FREQ / f) ** 2
        thermal = KAGRA_THERMAL_AMP / np.sqrt(1 + (f / KAGRA_THERMAL_FREQ) ** 2)
        quantum = KAGRA_QUANTUM_AMP * np.sqrt(1 + (f / KAGRA_QUANTUM_FREQ) ** 2)

        # Total noise
        return np.sqrt(seismic**2 + thermal**2 + quantum**2)
    
    # Calcular ASD para todas las frecuencias
    ligo_h1_asd = ligo_asd(freqs)
    ligo_l1_asd = ligo_asd(freqs) * 1.1  # L1 típicamente ~10% peor que H1
    kagra_asd_vals = kagra_asd(freqs)

    return {
        'freqs': freqs,
        'H1': ligo_h1_asd,
        'L1': ligo_l1_asd,
        'K1': kagra_asd_vals
    }


def analizar_141hz_especificamente(sensibilidades):
    """
    Análisis específico en 141.7 Hz

    Args:
        sensibilidades: Diccionario con curvas de sensibilidad
    """
    target_freq = 141.7
    
    # Encontrar índice más cercano a 141.7 Hz
    idx = np.argmin(np.abs(sensibilidades['freqs'] - target_freq))
    freq_exact = sensibilidades['freqs'][idx]
    
    # Extraer sensibilidades en 141.7 Hz
    asd_h1 = sensibilidades['H1'][idx]
    asd_l1 = sensibilidades['L1'][idx]
    asd_k1 = sensibilidades['K1'][idx]
    
    print("\n" + "="*70)
    print(f"📊 ANÁLISIS EN {target_freq} Hz")
    print("="*70)
    print()
    print(f"Frecuencia exacta analizada: {freq_exact:.2f} Hz")
    print()
    print("Sensibilidad (Amplitude Spectral Density):")
    print(f"  H1 (LIGO Hanford):    {asd_h1:.2e} Hz^(-1/2)")
    print(f"  L1 (LIGO Livingston): {asd_l1:.2e} Hz^(-1/2)")
    print(f"  K1 (KAGRA):           {asd_k1:.2e} Hz^(-1/2)")
    print()
    
    # Comparar ratios
    ratio_k1_h1 = asd_k1 / asd_h1
    ratio_k1_l1 = asd_k1 / asd_l1
    
    print("Ratios de sensibilidad (K1/LIGO):")
    print(f"  K1/H1: {ratio_k1_h1:.2f}x")
    print(f"  K1/L1: {ratio_k1_l1:.2f}x")
    print()
    
    # Interpretación
    print("🔍 INTERPRETACIÓN:")
    if ratio_k1_h1 < 3:
        print(f"  ✅ KAGRA tiene sensibilidad comparable a LIGO en {target_freq} Hz")
        print(f"     (diferencia < 3x)")
        print(f"  ✅ KAGRA PUEDE detectar la señal si es física universal")
    else:
        print(f"  ⚠️  KAGRA es {ratio_k1_h1:.1f}x menos sensible que H1")
        print(f"     Puede ser más difícil detectar señales débiles")
        print(f"  📊 SNR esperado en KAGRA: ~{1/ratio_k1_h1:.2f}x del SNR en H1")
    
    print()
    
    return {
        'freq': freq_exact,
        'asd_h1': asd_h1,
        'asd_l1': asd_l1,
        'asd_k1': asd_k1,
        'ratio_k1_h1': ratio_k1_h1,
        'ratio_k1_l1': ratio_k1_l1
    }


def generar_visualizacion(sensibilidades, analisis_141hz, output_dir=None):
    """
    Generar gráfico comparativo de sensibilidades
    
    Args:
        sensibilidades: Diccionario con curvas de sensibilidad
        analisis_141hz: Resultados del análisis en 141.7 Hz
        output_dir: Directorio de salida
    """
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)
        output_dir = os.path.join(repo_root, 'results', 'figures')
    
    os.makedirs(output_dir, exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Panel 1: Curvas completas de sensibilidad
    ax1.loglog(sensibilidades['freqs'], sensibilidades['H1'], 
               'b-', linewidth=2, label='LIGO H1', alpha=0.8)
    ax1.loglog(sensibilidades['freqs'], sensibilidades['L1'], 
               'g-', linewidth=2, label='LIGO L1', alpha=0.8)
    ax1.loglog(sensibilidades['freqs'], sensibilidades['K1'], 
               'r-', linewidth=2, label='KAGRA K1', alpha=0.8)
    
    # Marcar 141.7 Hz
    ax1.axvline(141.7, color='orange', linestyle='--', linewidth=2, 
                label='141.7 Hz', alpha=0.7)
    
    ax1.set_xlabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Amplitude Spectral Density (Hz$^{-1/2}$)', 
                   fontsize=12, fontweight='bold')
    ax1.set_title('Curvas de Sensibilidad: LIGO vs KAGRA', 
                  fontsize=14, fontweight='bold')
    ax1.legend(fontsize=11, loc='upper right')
    ax1.grid(True, alpha=0.3, which='both')
    ax1.set_xlim(10, 1000)
    
    # Panel 2: Zoom en banda de interés (100-200 Hz)
    mask = (sensibilidades['freqs'] >= 100) & (sensibilidades['freqs'] <= 200)
    freqs_zoom = sensibilidades['freqs'][mask]
    
    ax2.semilogy(freqs_zoom, sensibilidades['H1'][mask], 
                 'b-', linewidth=2.5, label='LIGO H1', alpha=0.8)
    ax2.semilogy(freqs_zoom, sensibilidades['L1'][mask], 
                 'g-', linewidth=2.5, label='LIGO L1', alpha=0.8)
    ax2.semilogy(freqs_zoom, sensibilidades['K1'][mask], 
                 'r-', linewidth=2.5, label='KAGRA K1', alpha=0.8)
    
    # Marcar 141.7 Hz con más detalle
    ax2.axvline(141.7, color='orange', linestyle='--', linewidth=2.5, 
                label='141.7 Hz', alpha=0.7)
    
    # Marcar puntos específicos en 141.7 Hz
    ax2.plot(analisis_141hz['freq'], analisis_141hz['asd_h1'], 
             'bo', markersize=10, label=f"H1 @ 141.7 Hz")
    ax2.plot(analisis_141hz['freq'], analisis_141hz['asd_l1'], 
             'go', markersize=10, label=f"L1 @ 141.7 Hz")
    ax2.plot(analisis_141hz['freq'], analisis_141hz['asd_k1'], 
             'ro', markersize=10, label=f"K1 @ 141.7 Hz")
    
    ax2.set_xlabel('Frecuencia (Hz)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Amplitude Spectral Density (Hz$^{-1/2}$)', 
                   fontsize=12, fontweight='bold')
    ax2.set_title('Zoom: Banda 100-200 Hz (141.7 Hz destacado)', 
                  fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10, loc='upper right', ncol=2)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(100, 200)
    
    plt.tight_layout()
    
    output_file = os.path.join(output_dir, 'ligo_vs_kagra_sensibilidad_141hz.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Visualización guardada: {output_file}")
    
    return output_file


def guardar_informe(analisis_141hz, output_dir=None):
    """
    Guardar informe textual del análisis
    
    Args:
        analisis_141hz: Resultados del análisis en 141.7 Hz
        output_dir: Directorio de salida
    """
    if output_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)
        output_dir = os.path.join(repo_root, 'results')
    
    os.makedirs(output_dir, exist_ok=True)
    
    informe_file = os.path.join(output_dir, 'comparacion_ligo_kagra_141hz.txt')
    
    with open(informe_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("COMPARACIÓN DE SENSIBILIDAD: LIGO vs KAGRA en 141.7 Hz\n")
        f.write("="*70 + "\n\n")
        
        f.write("OBJETIVO:\n")
        f.write("Determinar si KAGRA tiene suficiente sensibilidad para detectar\n")
        f.write("la señal de 141.7 Hz observada en LIGO.\n\n")
        
        f.write("RESULTADOS EN 141.7 Hz:\n")
        f.write(f"  Frecuencia analizada: {analisis_141hz['freq']:.2f} Hz\n\n")
        
        f.write("  Sensibilidad (ASD):\n")
        f.write(f"    H1 (LIGO Hanford):    {analisis_141hz['asd_h1']:.2e} Hz^(-1/2)\n")
        f.write(f"    L1 (LIGO Livingston): {analisis_141hz['asd_l1']:.2e} Hz^(-1/2)\n")
        f.write(f"    K1 (KAGRA):           {analisis_141hz['asd_k1']:.2e} Hz^(-1/2)\n\n")
        
        f.write("  Ratios K1/LIGO:\n")
        f.write(f"    K1/H1: {analisis_141hz['ratio_k1_h1']:.2f}x\n")
        f.write(f"    K1/L1: {analisis_141hz['ratio_k1_l1']:.2f}x\n\n")
        
        f.write("INTERPRETACIÓN:\n")
        if analisis_141hz['ratio_k1_h1'] < 3:
            f.write("  ✅ KAGRA tiene sensibilidad COMPARABLE a LIGO\n")
            f.write("     (diferencia < 3x)\n\n")
            f.write("  CONCLUSIÓN:\n")
            f.write("  Si 141.7 Hz es una señal física universal, KAGRA DEBE detectarla\n")
            f.write("  en eventos de fusión BBH con SNR suficiente.\n\n")
            f.write("  Si KAGRA NO detecta 141.7 Hz → evidencia de artefacto LIGO\n")
            f.write("  Si KAGRA SÍ detecta 141.7 Hz → evidencia de señal física\n")
        else:
            f.write(f"  ⚠️  KAGRA es {analisis_141hz['ratio_k1_h1']:.1f}x menos sensible\n")
            f.write("     Puede ser más difícil detectar señales débiles\n\n")
            f.write(f"  SNR esperado en KAGRA: ~{1/analisis_141hz['ratio_k1_h1']:.2f}x del SNR en H1\n\n")
            f.write("  CONCLUSIÓN:\n")
            f.write("  Señales detectables en LIGO pueden ser marginales en KAGRA.\n")
            f.write("  Se requieren eventos con SNR alto en LIGO para validación en KAGRA.\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("NOTAS TÉCNICAS:\n")
        f.write("- Sensibilidades basadas en diseños publicados (aproximadas)\n")
        f.write("- Sensibilidad real puede variar según condiciones operacionales\n")
        f.write("- KAGRA: ventaja térmica (criogénico), desventaja sísmica (Japón)\n")
        f.write("- Análisis completo requiere curvas ASD reales de cada run\n")
        f.write("="*70 + "\n")
    
    print(f"📄 Informe guardado: {informe_file}")
    
    return informe_file


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("🔬 COMPARACIÓN LIGO vs KAGRA: Sensibilidad en 141.7 Hz")
    print("="*70)
    print()
    
    print("📊 Calculando curvas de sensibilidad teóricas...")
    sensibilidades = obtener_sensibilidad_teorica()
    print("   ✅ Curvas calculadas")
    
    print("\n🎯 Analizando específicamente 141.7 Hz...")
    analisis_141hz = analizar_141hz_especificamente(sensibilidades)
    
    print("\n📈 Generando visualización...")
    output_file = generar_visualizacion(sensibilidades, analisis_141hz)
    
    print("\n📝 Guardando informe...")
    informe_file = guardar_informe(analisis_141hz)
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)
    print()
    print("📁 Archivos generados:")
    print(f"   - Visualización: {output_file}")
    print(f"   - Informe: {informe_file}")
    print()
    print("🎯 CONCLUSIÓN CLAVE:")
    if analisis_141hz['ratio_k1_h1'] < 3:
        print("   ✅ KAGRA puede detectar 141.7 Hz si es señal física universal")
        print("   ✅ Ausencia en KAGRA → evidencia de artefacto LIGO")
        print("   ✅ Presencia en KAGRA → evidencia de señal física real")
    else:
        print("   ⚠️  KAGRA menos sensible: requiere eventos fuertes para validación")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
