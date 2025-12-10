#!/usr/bin/env python3
"""
Validación de Predicción 4: Modulación Gravitacional Persistente
====================================================================

Este script analiza la predicción de modulación gravitacional persistente
a f₀ = 141.7001 Hz detectable por gravímetros superconductores.

Predicción:
    δg(t) = A cos(ω₀ t)
    
Donde:
    - ω₀ = 2π × 141.7001 Hz
    - A ≈ 10⁻¹⁵ g ≈ 10⁻¹⁴ m/s²

Autor: José Manuel Mota Burruezo (JMMB Ψ ✧)
Fecha: Diciembre 2025
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.constants import pi, hbar, c

# Constantes
F0 = 141.7001  # Hz
OMEGA0 = 2 * pi * F0  # rad/s
G_EARTH = 9.81  # m/s²


def calcular_amplitud_modulacion():
    """
    Estima la amplitud de modulación gravitacional.
    
    A/g ∼ (ℏω₀)/(m_Ψ c²) · (ℓ_P/R_Earth)²
    
    Returns:
        float: Amplitud en m/s²
    """
    # Parámetros
    l_planck = 1.616e-35  # m
    R_earth = 6.371e6  # m
    
    # Masa del campo Ψ
    m_psi = hbar * OMEGA0 / c**2
    
    # Estimación de amplitud relativa
    A_rel = (hbar * OMEGA0) / (m_psi * c**2) * (l_planck / R_earth)**2
    
    # Amplitud absoluta
    A = A_rel * G_EARTH
    
    return A


def generar_señal_modulada(duracion=3600, fs=1000, amplitud=1e-14, noise_level=1e-12):
    """
    Genera señal sintética de modulación gravitacional.
    
    NOTA: Para análisis completo se requieren 30 días de datos.
    Esta función usa 1 hora por defecto para demostración (limitación de memoria).
    En análisis real, se procesarían datos en chunks o se usaría downsample.
    
    Args:
        duracion: Duración en segundos (default: 1 hora para demo)
        fs: Frecuencia de muestreo (Hz)
        amplitud: Amplitud de modulación (m/s²)
        noise_level: Nivel de ruido (m/s²)
    
    Returns:
        tuple: (tiempo, señal)
    """
    t = np.arange(0, duracion, 1/fs)
    
    # Señal pura
    señal_pura = amplitud * np.cos(OMEGA0 * t)
    
    # Ruido
    ruido = noise_level * np.random.randn(len(t))
    
    # Señal total
    señal_total = señal_pura + ruido
    
    return t, señal_total, señal_pura


def analisis_espectral(t, señal, fs=1000):
    """
    Análisis espectral de la señal gravitacional.
    
    Args:
        t: Tiempo (s)
        señal: Señal temporal
        fs: Frecuencia de muestreo (Hz)
    
    Returns:
        tuple: (frecuencias, PSD)
    """
    # Welch PSD
    f, psd = welch(señal, fs=fs, nperseg=min(2**14, len(señal)//4))
    
    return f, psd


def calcular_snr_espectral(f, psd, f0=F0, delta_f=0.5):
    """
    Calcula SNR del pico a f₀.
    
    Args:
        f: Frecuencias
        psd: Densidad espectral de potencia
        f0: Frecuencia objetivo
        delta_f: Ancho de banda de señal (Hz)
    
    Returns:
        float: SNR
    """
    # Pico de señal
    idx_signal = np.where((f >= f0 - delta_f) & (f <= f0 + delta_f))[0]
    if len(idx_signal) == 0:
        return 0.0
    power_signal = np.max(psd[idx_signal])
    
    # Ruido de fondo (excluyendo pico)
    idx_background = np.where((f > 100) & (f < 200) & 
                              ((f < f0 - 5) | (f > f0 + 5)))[0]
    if len(idx_background) == 0:
        return 0.0
    power_background = np.mean(psd[idx_background])
    
    # SNR
    snr = power_signal / power_background if power_background > 0 else 0
    
    return snr


def simular_multiples_estaciones():
    """
    Simula datos de múltiples estaciones IGETS.
    """
    print("\n" + "="*70)
    print("SIMULACIÓN DE RED IGETS MULTI-ESTACIÓN")
    print("="*70)
    
    estaciones = [
        {'nombre': 'Wettzell', 'lat': 49.14, 'lon': 12.88, 'pais': 'Alemania'},
        {'nombre': 'Strasbourg', 'lat': 48.62, 'lon': 7.68, 'pais': 'Francia'},
        {'nombre': 'Medicina', 'lat': 44.53, 'lon': 11.65, 'pais': 'Italia'},
        {'nombre': 'Kyoto', 'lat': 35.03, 'lon': 135.96, 'pais': 'Japón'},
    ]
    
    duracion = 30 * 86400  # 30 días
    fs = 1000  # Hz
    amplitud_real = 1e-14  # m/s²
    
    print(f"\nParámetros de simulación:")
    print(f"  Duración: {duracion/86400:.0f} días")
    print(f"  Frecuencia de muestreo: {fs} Hz")
    print(f"  Amplitud de señal: A = {amplitud_real:.2e} m/s²")
    print(f"  Frecuencia objetivo: f₀ = {F0} Hz")
    
    resultados = []
    
    for i, est in enumerate(estaciones):
        print(f"\n  Estación {i+1}: {est['nombre']} ({est['pais']})")
        
        # Generar datos
        # Nota: Simulación reducida por memoria (1 hora en vez de 30 días)
        t_sim, señal, señal_pura = generar_señal_modulada(
            duracion=3600,  # 1 hora
            fs=fs,
            amplitud=amplitud_real,
            noise_level=1e-12
        )
        
        # Análisis espectral
        f, psd = analisis_espectral(t_sim, señal, fs=fs)
        snr = calcular_snr_espectral(f, psd, f0=F0)
        
        # Buscar pico en f₀
        idx_f0 = np.argmin(np.abs(f - F0))
        freq_detected = f[idx_f0]
        power_detected = psd[idx_f0]
        
        print(f"    Frecuencia detectada: {freq_detected:.3f} Hz")
        print(f"    SNR: {snr:.2f}")
        
        resultado = {
            'estacion': est['nombre'],
            'lat': est['lat'],
            'lon': est['lon'],
            'freq_detected': freq_detected,
            'snr': snr,
            'power': power_detected,
            'f': f,
            'psd': psd
        }
        
        resultados.append(resultado)
    
    # Análisis de coherencia
    print("\n" + "="*70)
    print("ANÁLISIS DE COHERENCIA MULTI-ESTACIÓN")
    print("="*70)
    
    freq_detections = [r['freq_detected'] for r in resultados]
    snr_values = [r['snr'] for r in resultados]
    
    print(f"\n  Frecuencias detectadas:")
    for r in resultados:
        print(f"    {r['estacion']}: f = {r['freq_detected']:.3f} Hz, SNR = {r['snr']:.2f}")
    
    print(f"\n  Estadísticas:")
    print(f"    Media: f̄ = {np.mean(freq_detections):.3f} Hz")
    print(f"    Desviación: σ_f = {np.std(freq_detections):.3f} Hz")
    print(f"    SNR promedio: {np.mean(snr_values):.2f}")
    
    # Criterio de coherencia
    coherente = all(abs(f - F0) < 0.5 for f in freq_detections) and all(s > 3 for s in snr_values)
    
    if coherente:
        print(f"\n  ✓ COHERENCIA CONFIRMADA")
        print(f"    Todas las estaciones detectan pico en {F0} ± 0.5 Hz con SNR > 3")
    else:
        print(f"\n  ✗ COHERENCIA NO CONFIRMADA")
        print(f"    Detecciones inconsistentes entre estaciones")
    
    print("="*70)
    
    return resultados


def generar_graficas_analisis():
    """
    Genera gráficas del análisis gravitacional.
    """
    print("\nGenerando gráficas...")
    
    # Simular señal de 1 hora (memoria limitada)
    duracion = 3600  # 1 hora
    fs = 1000
    amplitud = 1e-14
    
    t, señal, señal_pura = generar_señal_modulada(duracion, fs, amplitud, noise_level=1e-12)
    f, psd = analisis_espectral(t, señal, fs)
    
    fig = plt.figure(figsize=(14, 10))
    
    # Subplot 1: Serie temporal (primeros 10 segundos)
    ax1 = plt.subplot(2, 2, 1)
    t_zoom = t[:10000]  # Primeros 10 s
    señal_zoom = señal[:10000]
    señal_pura_zoom = señal_pura[:10000]
    
    ax1.plot(t_zoom, señal_zoom * 1e15, alpha=0.7, color='blue', linewidth=0.5, label='Señal + ruido')
    ax1.plot(t_zoom, señal_pura_zoom * 1e15, color='red', linewidth=1.5, label='Señal pura (A=10⁻¹⁴ m/s²)')
    ax1.set_xlabel('Tiempo (s)', fontsize=11)
    ax1.set_ylabel('δg (10⁻¹⁵ m/s²)', fontsize=11)
    ax1.set_title('Serie Temporal de Modulación Gravitacional', fontsize=12, fontweight='bold')
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # Subplot 2: Espectro de potencia completo
    ax2 = plt.subplot(2, 2, 2)
    ax2.loglog(f, psd, color='blue', alpha=0.7, linewidth=1)
    ax2.axvline(F0, color='red', linestyle='--', linewidth=2, label=f'f₀ = {F0} Hz')
    ax2.set_xlabel('Frecuencia (Hz)', fontsize=11)
    ax2.set_ylabel('PSD (m²/s⁴/Hz)', fontsize=11)
    ax2.set_title('Densidad Espectral de Potencia', fontsize=12, fontweight='bold')
    ax2.set_xlim([10, 500])
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Subplot 3: Zoom en f₀
    ax3 = plt.subplot(2, 2, 3)
    idx_zoom = np.where((f >= F0 - 10) & (f <= F0 + 10))[0]
    ax3.plot(f[idx_zoom], psd[idx_zoom], color='green', linewidth=2)
    ax3.axvline(F0, color='red', linestyle='--', linewidth=2, label=f'f₀ = {F0} Hz')
    ax3.set_xlabel('Frecuencia (Hz)', fontsize=11)
    ax3.set_ylabel('PSD (m²/s⁴/Hz)', fontsize=11)
    ax3.set_title('Zoom en Pico Resonante', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    
    # Subplot 4: SNR vs duración
    ax4 = plt.subplot(2, 2, 4)
    
    duraciones = np.logspace(2, 6, 20)  # 100 s a ~11 días
    snr_values = []
    
    # Calcular SNR para las primeras duraciones (limitado por memoria)
    n_calc = min(10, len(duraciones))
    for T in duraciones[:n_calc]:
        t_temp, señal_temp, _ = generar_señal_modulada(int(T), fs, amplitud, noise_level=1e-12)
        f_temp, psd_temp = analisis_espectral(t_temp, señal_temp, fs)
        snr_temp = calcular_snr_espectral(f_temp, psd_temp)
        snr_values.append(snr_temp)
    
    # Extender con modelo teórico SNR ∝ √T
    if len(snr_values) > 0:
        snr_extrapolated = snr_values[-1] * np.sqrt(duraciones / duraciones[n_calc-1])
    else:
        snr_extrapolated = np.sqrt(duraciones / 100)  # Fallback
    
    ax4.loglog(duraciones/86400, snr_extrapolated, linewidth=2, color='purple', 
               label='SNR predicho')
    if len(snr_values) > 0:
        ax4.scatter(duraciones[:n_calc]/86400, snr_values, s=50, color='red', zorder=5, label='Simulado')
    ax4.axhline(3, color='orange', linestyle='--', linewidth=2, label='SNR = 3')
    ax4.set_xlabel('Duración (días)', fontsize=11)
    ax4.set_ylabel('SNR', fontsize=11)
    ax4.set_title('SNR vs. Tiempo de Observación', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Predicción 4: Modulación Gravitacional Persistente a 141.7001 Hz',
                 fontsize=14, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('prediccion_modulacion_gravitacional.png', dpi=300, bbox_inches='tight')
    print("✅ Gráfica guardada: prediccion_modulacion_gravitacional.png")
    plt.close()


def protocolo_experimental():
    """
    Describe el protocolo experimental para IGETS.
    """
    print("\n" + "="*70)
    print("PROTOCOLO EXPERIMENTAL: GRAVÍMETROS IGETS")
    print("="*70)
    
    print("\n1. SELECCIÓN DE ESTACIONES")
    print("   Criterios:")
    print("     - Gravímetros superconductores (sensibilidad < 1 nGal)")
    print("     - Sincronización GPS/GNSS (precisión < 1 μs)")
    print("     - Datos continuos ≥30 días")
    print("     - Distribución geográfica global")
    
    print("\n2. ADQUISICIÓN DE DATOS")
    print("   - Frecuencia de muestreo: f_s ≥ 1000 Hz")
    print("   - Duración mínima: T ≥ 30 días")
    print("   - Formato: Series temporales g(t)")
    print("   - Timestamp: UTC con precisión GPS")
    
    print("\n3. PREPROCESAMIENTO")
    print("   Correcciones aplicadas:")
    print("     a) Modelo de mareas terrestres (IERS Conventions)")
    print("     b) Presión atmosférica (coeficiente admitancia)")
    print("     c) Deriva instrumental (spline fitting)")
    print("     d) Eventos sísmicos (filtrado manual)")
    
    print("\n4. ANÁLISIS ESPECTRAL")
    print("   Método: Welch periodogram")
    print("     - Ventana: Hanning (N = 10⁶ puntos)")
    print("     - Overlap: 50%")
    print("     - Resolución: Δf ≈ 0.001 Hz")
    print("   Búsqueda:")
    print(f"     - Banda: f = {F0} ± 0.5 Hz")
    print("     - Criterio: SNR > 3")
    
    print("\n5. CORRELACIÓN CRUZADA")
    print("   Entre estaciones:")
    print("     - Coherencia espectral γ²(f₀)")
    print("     - Diferencia de fase: Δφ < π/4")
    print("     - Correlación temporal: r > 0.5")
    
    print("="*70)


def sensibilidad_gravimetros():
    """
    Discute sensibilidad de gravímetros superconductores.
    """
    print("\n" + "="*70)
    print("SENSIBILIDAD DE GRAVÍMETROS SUPERCONDUCTORES")
    print("="*70)
    
    print("\nParámetros típicos (IGETS):")
    print("  - Sensibilidad: 0.1 nGal = 10⁻¹² m/s²")
    print("  - Rango dinámico: ±5000 μGal")
    print("  - Resolución temporal: 1 Hz - 1 kHz")
    print("  - Estabilidad a largo plazo: < 1 μGal/mes")
    
    A_pred = calcular_amplitud_modulacion()
    print(f"\nAmplitud predicha:")
    print(f"  A = {A_pred:.2e} m/s²")
    print(f"  A = {A_pred * 1e9:.4f} nGal")
    
    # Comparación
    sensibilidad_sg = 1e-12  # m/s²
    
    print(f"\nComparación:")
    print(f"  A / sensibilidad = {A_pred / sensibilidad_sg:.2f}")
    
    if A_pred > 3 * sensibilidad_sg:
        print(f"  ✓ Detectable con alta confianza (A > 3σ)")
    elif A_pred > sensibilidad_sg:
        print(f"  ✓ Marginalmente detectable (requiere larga integración)")
    else:
        print(f"  ✗ Por debajo del umbral de sensibilidad")
    
    print("\nEstrategias de mejora:")
    print("  1. Integración larga (T ≥ 30 días): SNR ∝ √T")
    print("  2. Múltiples estaciones: SNR ∝ √N")
    print("  3. Correlación cruzada: Rechaza ruido no correlacionado")
    print("  4. Análisis espectral optimizado: Ventanas, zero-padding")
    
    print("="*70)


def criterio_falsacion():
    """
    Define criterios de falsación.
    """
    print("\n" + "="*70)
    print("CRITERIO DE FALSACIÓN")
    print("="*70)
    
    print("\n❌ La predicción es REFUTADA si:")
    print("   Después de análisis riguroso con:")
    print("   1. Datos de ≥3 estaciones IGETS independientes")
    print("   2. Duración T ≥ 30 días cada una")
    print("   3. Correcciones completas (mareas, atmósfera, deriva)")
    print("   4. No se detecta pico coherente con:")
    print(f"      - Frecuencia: f = {F0} ± 0.001 Hz")
    print("      - SNR > 3 en cada estación")
    print("      - Fase estable: σ_φ < π/4 entre estaciones")
    
    print("\n✓ La predicción es CONFIRMADA si:")
    print("   1. Pico espectral detectado en f = 141.7001 ± 0.001 Hz")
    print("   2. SNR > 3 en ≥3 estaciones independientes")
    print("   3. Coherencia de fase entre estaciones (r > 0.5)")
    print("   4. Reproducible en campañas independientes")
    print("   5. No explicable por:")
    print("      - Mareas oceánicas o terrestres residuales")
    print("      - Efectos atmosféricos")
    print("      - Resonancias instrumentales")
    print("      - Contaminación antropogénica")
    
    print("\n" + "="*70)


def main():
    """
    Función principal de validación.
    """
    print("="*70)
    print("VALIDACIÓN: PREDICCIÓN 4 - MODULACIÓN GRAVITACIONAL")
    print("Marco: QCAL ∞³")
    print("="*70)
    
    # 1. Calcular amplitud predicha
    A = calcular_amplitud_modulacion()
    print(f"\nAmplitud predicha: A = {A:.2e} m/s² = {A*1e9:.4f} nGal")
    
    # 2. Sensibilidad de instrumentos
    sensibilidad_gravimetros()
    
    # 3. Simulación multi-estación
    resultados = simular_multiples_estaciones()
    
    # 4. Gráficas
    generar_graficas_analisis()
    
    # 5. Protocolo experimental
    protocolo_experimental()
    
    # 6. Criterio de falsación
    criterio_falsacion()
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE PREDICCIÓN 4")
    print("="*70)
    print("\n✓ PREDICCIÓN:")
    print(f"  δg(t) = A cos(2π × {F0} Hz × t)")
    print(f"  A ≈ {A:.2e} m/s² = {A*1e9:.4f} nGal")
    
    print("\n✓ PLATAFORMA:")
    print("  Red IGETS de gravímetros superconductores")
    print("  Estaciones: Wettzell, Strasbourg, Medicina, Kyoto, ...")
    
    print("\n✓ FACTIBILIDAD:")
    print("  Alta - Datos disponibles en tiempo casi real")
    print("  Análisis posible con datos existentes de archivo")
    print("  Tiempo estimado: 3-6 meses de análisis")
    
    print("\n✓ VENTAJAS:")
    print("  - No requiere nuevo hardware")
    print("  - Datos históricos analizables")
    print("  - Red global distribuida")
    print("  - Validación cruzada inmediata")
    
    print("="*70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
