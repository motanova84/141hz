#!/usr/bin/env python3
"""
Pipeline de Análisis EOV - Ecuación del Origen Vibracional
===========================================================

Pipeline completo para aplicar la EOV al análisis de ondas gravitacionales,
integrando con el framework existente del repositorio.

Autor: José Manuel Mota Burruezo (JMMB Ψ✧)
Fecha: 2025-10-12
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Tuple

# Importar módulo EOV
try:
    from ecuacion_origen_vibracional import (
        termino_oscilatorio,
        detectar_firma_eov,
        generar_señal_eov,
        calcular_espectrograma_eov,
        campo_noético_temporal,
        F_0,
        OMEGA_0
    )
except ImportError:
    print("⚠️  No se pudo importar el módulo EOV")
    sys.exit(1)

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Directorios
SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
DATA_DIR = REPO_DIR / "data" / "raw"
RESULTS_DIR = REPO_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "figures"

# Crear directorios si no existen
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Parámetros de análisis
F_TARGET = 141.7001  # Hz
DETECTORES = ['H1', 'L1', 'V1']
SAMPLE_RATE = 4096  # Hz

# ============================================================================
# FUNCIONES DE ANÁLISIS
# ============================================================================

def analizar_datos_con_eov(data: np.ndarray, 
                           sample_rate: float,
                           detector: str = "H1") -> Dict:
    """
    Analiza datos de ondas gravitacionales buscando firma EOV.
    
    Parámetros
    ----------
    data : array
        Serie temporal de strain
    sample_rate : float
        Frecuencia de muestreo (Hz)
    detector : str
        Nombre del detector
    
    Retorna
    -------
    dict
        Resultados del análisis EOV
    """
    print(f"🔬 Analizando {detector} con modelo EOV...")
    
    # Crear vector de tiempo
    tiempo = np.arange(len(data)) / sample_rate
    
    # Detectar firma EOV
    freq, snr, power = detectar_firma_eov(tiempo, data, sample_rate)
    
    # Análisis espectral detallado
    freqs = np.fft.rfftfreq(len(data), 1/sample_rate)
    fft_val = np.fft.rfft(data)
    espectro = np.abs(fft_val)**2
    
    # Buscar pico en banda
    mask = (freqs >= F_TARGET - 5) & (freqs <= F_TARGET + 5)
    idx_peak = np.argmax(espectro[mask])
    freq_peak = freqs[mask][idx_peak]
    
    # Calcular campo noético efectivo
    # Inferir |Ψ|² de la amplitud detectada
    R_est = 1e-20  # Escalar de Ricci estimado
    amplitud_strain = np.sqrt(power)
    
    # De h ~ (G/c⁴) × R × |Ψ|², estimar |Ψ|²
    Psi_sq_est = amplitud_strain * (6.67430e-11 / 299792458**4) / R_est
    
    resultados = {
        'detector': detector,
        'frecuencia_detectada': freq,
        'snr': snr,
        'potencia': power,
        'diferencia_f0': abs(freq - F_TARGET),
        'Psi_squared_estimado': Psi_sq_est,
        'espectro': (freqs, espectro),
        'validacion_eov': abs(freq - F_TARGET) < 0.5
    }
    
    print(f"   Frecuencia: {freq:.4f} Hz (Δf = {abs(freq - F_TARGET):.4f} Hz)")
    print(f"   SNR: {snr:.2f}")
    print(f"   |Ψ|² estimado: {Psi_sq_est:.2e}")
    print(f"   Validación EOV: {'✅ CONFIRMADA' if resultados['validacion_eov'] else '❌ NO DETECTADA'}")
    
    return resultados


def comparar_modelos(data: np.ndarray,
                     sample_rate: float,
                     tiempo_merger: float = 0.0) -> Dict:
    """
    Compara modelo con y sin EOV.
    
    Parámetros
    ----------
    data : array
        Datos observados
    sample_rate : float
        Frecuencia de muestreo
    tiempo_merger : float
        Tiempo de fusión
    
    Retorna
    -------
    dict
        Comparación de modelos
    """
    print("\n📊 Comparando modelos con y sin EOV...")
    
    tiempo = np.arange(len(data)) / sample_rate
    
    # Modelo sin EOV (solo modo dominante ~250 Hz)
    # Aproximación: seno amortiguado simple
    def modelo_sin_eov(t, A=1e-21, tau=0.01, f=250, phi=0):
        return A * np.exp(-t/tau) * np.cos(2*np.pi*f*t + phi)
    
    # Modelo con EOV (modo dominante + componente 141.7 Hz)
    def modelo_con_eov(t, A1=1e-21, A2=1e-23):
        h1 = A1 * np.exp(-t/0.01) * np.cos(2*np.pi*250*t)
        h2 = generar_señal_eov(t, amplitud=A2)
        return h1 + h2
    
    # Calcular χ² para ambos modelos
    h_sin = modelo_sin_eov(tiempo)
    h_con = modelo_con_eov(tiempo)
    
    chi2_sin = np.sum((data - h_sin)**2)
    chi2_con = np.sum((data - h_con)**2)
    
    # Bayes Factor (aproximado)
    delta_chi2 = chi2_sin - chi2_con
    bayes_factor = np.exp(delta_chi2 / 2)
    
    print(f"   χ² sin EOV: {chi2_sin:.2e}")
    print(f"   χ² con EOV: {chi2_con:.2e}")
    print(f"   Δχ²: {delta_chi2:.2e}")
    print(f"   Bayes Factor: {bayes_factor:.2f}")
    
    if bayes_factor > 3:
        print("   ✅ Evidencia moderada a favor de EOV")
    elif bayes_factor > 10:
        print("   ✅✅ Evidencia fuerte a favor de EOV")
    else:
        print("   ⚠️  Evidencia insuficiente")
    
    return {
        'chi2_sin_eov': chi2_sin,
        'chi2_con_eov': chi2_con,
        'delta_chi2': delta_chi2,
        'bayes_factor': bayes_factor,
        'modelos': (h_sin, h_con)
    }


def generar_predicciones_eov(duracion: float = 1.0,
                             sample_rate: float = 4096) -> Tuple[np.ndarray, np.ndarray]:
    """
    Genera predicciones teóricas del modelo EOV.
    
    Parámetros
    ----------
    duracion : float
        Duración de la señal (s)
    sample_rate : float
        Frecuencia de muestreo (Hz)
    
    Retorna
    -------
    tiempo, señal : arrays
        Predicción temporal de EOV
    """
    print("\n🔮 Generando predicciones EOV...")
    
    tiempo = np.linspace(0, duracion, int(duracion * sample_rate))
    
    # Parámetros físicos esperados
    R = 1e-20  # Curvatura típica cerca de BH
    Psi_0 = 1.0
    tau = 0.05  # Decaimiento típico de ringdown
    
    señal = generar_señal_eov(
        tiempo,
        R=R,
        Psi_0=Psi_0,
        tau_decay=tau,
        amplitud=1e-21
    )
    
    print(f"   Duración: {duracion} s")
    print(f"   Amplitud máxima: {np.max(np.abs(señal)):.2e}")
    print(f"   Frecuencia: {F_TARGET} Hz")
    
    return tiempo, señal


# ============================================================================
# VISUALIZACIÓN
# ============================================================================

def visualizar_analisis_eov(resultados: List[Dict],
                            output_path: Path):
    """
    Genera visualización completa del análisis EOV.
    
    Parámetros
    ----------
    resultados : list
        Lista de resultados por detector
    output_path : Path
        Ruta de salida para figura
    """
    print(f"\n📈 Generando visualización en {output_path}...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Análisis de Firma EOV - 141.7001 Hz', 
                 fontsize=16, fontweight='bold')
    
    # Panel 1: Espectros de todos los detectores
    ax1 = axes[0, 0]
    for res in resultados:
        freqs, espectro = res['espectro']
        mask = (freqs >= 100) & (freqs <= 200)
        ax1.semilogy(freqs[mask], espectro[mask], 
                    label=f"{res['detector']} (SNR={res['snr']:.1f})",
                    alpha=0.7, linewidth=1.5)
    
    ax1.axvline(F_TARGET, color='red', linestyle='--', 
               linewidth=2, label=f'f₀ = {F_TARGET} Hz')
    ax1.set_xlabel('Frecuencia (Hz)', fontsize=11)
    ax1.set_ylabel('Potencia Espectral', fontsize=11)
    ax1.set_title('Espectros Multi-detector', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Panel 2: Zoom en banda EOV
    ax2 = axes[0, 1]
    for res in resultados:
        freqs, espectro = res['espectro']
        mask = (freqs >= F_TARGET - 2) & (freqs <= F_TARGET + 2)
        ax2.plot(freqs[mask], espectro[mask], 
                label=res['detector'], linewidth=2)
    
    ax2.axvline(F_TARGET, color='red', linestyle='--', linewidth=2)
    ax2.set_xlabel('Frecuencia (Hz)', fontsize=11)
    ax2.set_ylabel('Potencia Espectral', fontsize=11)
    ax2.set_title(f'Zoom en {F_TARGET} Hz ± 2 Hz', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Panel 3: Señal teórica EOV
    ax3 = axes[1, 0]
    t_pred, h_pred = generar_predicciones_eov(duracion=0.5)
    ax3.plot(t_pred * 1000, h_pred * 1e21, color='purple', linewidth=1.5)
    ax3.set_xlabel('Tiempo (ms)', fontsize=11)
    ax3.set_ylabel('Strain (×10⁻²¹)', fontsize=11)
    ax3.set_title('Predicción Teórica EOV', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Panel 4: Tabla de resultados
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Crear tabla
    tabla_data = []
    for res in resultados:
        estado = "✅" if res['validacion_eov'] else "❌"
        tabla_data.append([
            res['detector'],
            f"{res['frecuencia_detectada']:.2f}",
            f"{res['snr']:.2f}",
            f"{res['diferencia_f0']:.3f}",
            estado
        ])
    
    tabla = ax4.table(cellText=tabla_data,
                     colLabels=['Detector', 'f (Hz)', 'SNR', 'Δf (Hz)', 'EOV'],
                     cellLoc='center',
                     loc='center',
                     bbox=[0, 0.3, 1, 0.6])
    
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 2)
    
    # Estilo de la tabla
    for i in range(len(tabla_data) + 1):
        if i == 0:
            for j in range(5):
                tabla[(i, j)].set_facecolor('#4CAF50')
                tabla[(i, j)].set_text_props(weight='bold', color='white')
        else:
            color = '#E8F5E9' if i % 2 == 0 else '#FFFFFF'
            for j in range(5):
                tabla[(i, j)].set_facecolor(color)
    
    ax4.text(0.5, 0.1, 
            '🌌 Ecuación del Origen Vibracional (EOV)\n' + 
            'G_μν + Λg_μν = (8πG/c⁴)(T_μν + T_μν^Ψ) + ζ(∇²)|Ψ|² + R cos(2πf₀t)|Ψ|²',
            ha='center', va='center', fontsize=9, style='italic',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✅ Figura guardada: {output_path}")
    
    return fig


# ============================================================================
# PIPELINE PRINCIPAL
# ============================================================================

def ejecutar_pipeline_eov(datos_sinteticos: bool = True):
    """
    Ejecuta el pipeline completo de análisis EOV.
    
    Parámetros
    ----------
    datos_sinteticos : bool
        Si True, usa datos sintéticos; si False, intenta cargar datos reales
    """
    print("=" * 70)
    print("🌌 PIPELINE DE ANÁLISIS EOV")
    print("   Ecuación del Origen Vibracional - QCAL ∞³")
    print("=" * 70)
    
    # Generar o cargar datos
    if datos_sinteticos:
        print("\n📊 Generando datos sintéticos para demostración...")
        
        # Simular datos de 3 detectores
        duracion = 1.0
        t = np.linspace(0, duracion, int(duracion * SAMPLE_RATE))
        
        # Modo dominante + EOV + ruido
        datos = {}
        for detector in ['H1', 'L1', 'V1']:
            # Modo dominante (250 Hz)
            h_dom = 1e-21 * np.exp(-t/0.01) * np.cos(2*np.pi*250*t)
            
            # Componente EOV
            h_eov = generar_señal_eov(t, amplitud=5e-23)
            
            # Ruido blanco
            ruido = np.random.normal(0, 1e-23, len(t))
            
            # Señal total
            datos[detector] = h_dom + h_eov + ruido
        
        print(f"   ✅ Datos sintéticos generados ({len(t)} puntos)")
    
    else:
        print("\n📡 Intentando cargar datos reales de LIGO/Virgo...")
        print("   ⚠️  Función no implementada - usar datos sintéticos")
        return
    
    # Análisis EOV por detector
    resultados = []
    print("\n" + "=" * 70)
    print("🔬 ANÁLISIS POR DETECTOR")
    print("=" * 70)
    
    for detector in ['H1', 'L1', 'V1']:
        if detector in datos:
            res = analizar_datos_con_eov(datos[detector], SAMPLE_RATE, detector)
            resultados.append(res)
            print()
    
    # Comparación de modelos
    print("=" * 70)
    print("📊 COMPARACIÓN DE MODELOS")
    print("=" * 70)
    comparacion = comparar_modelos(datos['H1'], SAMPLE_RATE)
    
    # Visualización
    print("\n" + "=" * 70)
    print("📈 GENERACIÓN DE VISUALIZACIONES")
    print("=" * 70)
    output_fig = FIGURES_DIR / "analisis_eov_completo.png"
    fig = visualizar_analisis_eov(resultados, output_fig)
    
    # Reporte final
    print("\n" + "=" * 70)
    print("📋 REPORTE FINAL")
    print("=" * 70)
    
    detectados = sum(1 for r in resultados if r['validacion_eov'])
    print(f"\n🎯 Detecciones EOV: {detectados}/{len(resultados)} detectores")
    print(f"🎼 Frecuencia objetivo: {F_TARGET} Hz")
    
    if detectados >= 2:
        print("\n✅✅ VALIDACIÓN MULTI-DETECTOR CONFIRMADA")
        print("   La firma EOV está presente en múltiples detectores")
        print("   Coincidencia consistente con predicción teórica")
    elif detectados == 1:
        print("\n✅ DETECCIÓN EN UN DETECTOR")
        print("   Se requiere confirmación multi-sitio")
    else:
        print("\n⚠️  NO SE DETECTÓ FIRMA EOV CLARA")
        print("   Posibles causas: ruido, amplitud débil, o ausencia de señal")
    
    print("\n✨ Resonancia del origen - QCAL ∞³")
    print("=" * 70)
    
    return resultados


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Punto de entrada principal."""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Pipeline de análisis EOV para ondas gravitacionales'
    )
    parser.add_argument(
        '--real-data',
        action='store_true',
        help='Usar datos reales en lugar de sintéticos'
    )
    
    args = parser.parse_args()
    
    # Ejecutar pipeline
    resultados = ejecutar_pipeline_eov(datos_sinteticos=not args.real_data)
    
    return 0 if resultados else 1


if __name__ == "__main__":
    sys.exit(main())
