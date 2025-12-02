#!/usr/bin/env python3
"""
Validación Alternativa 1: Prueba de Coherencia Inter-Detector (No Clásica)
=============================================================================

Hipótesis: Si 141.7001 Hz es real, debe estar sincronizada entre H1 y L1,
incluso si Virgo no la ve.

Implementa:
- Cálculo de coherencia cruzada espectral usando scipy.signal.coherence
- Medición del pico de coherencia en 141.7 Hz (> 0.4)
- Comparación con bandas adyacentes para validar significancia
"""

import numpy as np
from scipy import signal
import warnings
warnings.filterwarnings('ignore')


def calcular_coherencia_inter_detector(data_h1, data_l1, fs=4096,
                                        f_target=141.7001,
                                        ventana_tiempo=0.5):
    """
    Calcula la coherencia cruzada espectral entre H1 y L1

    Parameters:
    -----------
    data_h1 : array-like
        Datos del detector H1 (strain)
    data_l1 : array-like
        Datos del detector L1 (strain)
    fs : float
        Frecuencia de muestreo (Hz)
    f_target : float
        Frecuencia objetivo (Hz)
    ventana_tiempo : float
        Ventana de tiempo alrededor del ringdown (segundos)

    Returns:
    --------
    dict : Diccionario con resultados de coherencia
        - coherencia_f0: coherencia en frecuencia objetivo
        - coherencia_media_banda: coherencia media en banda adyacente
        - significancia: ratio coherencia_f0 / coherencia_media_banda
        - frecuencias: array de frecuencias
        - coherencias: array de valores de coherencia
    """
    # Convertir a arrays numpy
    h1 = np.asarray(data_h1)
    l1 = np.asarray(data_l1)

    # Asegurar que ambos tienen la misma longitud
    min_len = min(len(h1), len(l1))
    h1 = h1[:min_len]
    l1 = l1[:min_len]

    # Calcular coherencia usando método de Welch
    nperseg = int(fs * ventana_tiempo)
    nperseg = min(nperseg, len(h1) // 4)

    freqs, coherence = signal.coherence(h1, l1, fs=fs,
                                        nperseg=nperseg,
                                        noverlap=nperseg//2)

    # Encontrar índice de frecuencia objetivo
    idx_target = np.argmin(np.abs(freqs - f_target))
    coherencia_f0 = coherence[idx_target]

    # Calcular coherencia en bandas adyacentes (excluyendo ±5 Hz alrededor de f0)
    banda_width = 30  # Hz para comparación
    banda_exclusion = 5  # Hz a excluir alrededor del pico

    idx_banda_inferior_start = np.argmin(np.abs(freqs - (f_target - banda_width)))
    idx_banda_inferior_end = np.argmin(np.abs(freqs - (f_target - banda_exclusion)))

    idx_banda_superior_start = np.argmin(np.abs(freqs - (f_target + banda_exclusion)))
    idx_banda_superior_end = np.argmin(np.abs(freqs - (f_target + banda_width)))

    # Coherencia en bandas adyacentes
    coherencia_banda_inferior = coherence[idx_banda_inferior_start:idx_banda_inferior_end]
    coherencia_banda_superior = coherence[idx_banda_superior_start:idx_banda_superior_end]

    coherencias_adyacentes = np.concatenate([coherencia_banda_inferior,
                                             coherencia_banda_superior])

    if len(coherencias_adyacentes) > 0:
        coherencia_media_banda = np.mean(coherencias_adyacentes)
        coherencia_std_banda = np.std(coherencias_adyacentes)
    else:
        coherencia_media_banda = 0.0
        coherencia_std_banda = 0.0

    # Calcular significancia
    if coherencia_media_banda > 0:
        significancia = coherencia_f0 / coherencia_media_banda
        sigma = (coherencia_f0 - coherencia_media_banda) / coherencia_std_banda if coherencia_std_banda > 0 else 0
    else:
        significancia = 0.0
        sigma = 0.0

    # Criterio de validación: coherencia > 0.4 y significancia > 1.5
    es_significativo = (coherencia_f0 > 0.4) and (significancia > 1.5)

    return {
        'coherencia_f0': float(coherencia_f0),
        'coherencia_media_banda': float(coherencia_media_banda),
        'coherencia_std_banda': float(coherencia_std_banda),
        'significancia': float(significancia),
        'sigma': float(sigma),
        'es_significativo': bool(es_significativo),
        'frecuencias': freqs,
        'coherencias': coherence,
        'freq_target': f_target,
        'umbral_coherencia': 0.4,
        'criterio_cumplido': es_significativo
    }


def analizar_coherencia_ventanas_temporales(data_h1, data_l1, fs=4096,
                                            f_target=141.7001,
                                            tiempo_total=2.0,
                                            ventana=0.5,
                                            overlap=0.25):
    """
    Analiza la coherencia en múltiples ventanas temporales

    Parameters:
    -----------
    data_h1, data_l1 : array-like
        Datos de los detectores
    fs : float
        Frecuencia de muestreo
    f_target : float
        Frecuencia objetivo
    tiempo_total : float
        Tiempo total a analizar (segundos)
    ventana : float
        Duración de cada ventana (segundos)
    overlap : float
        Superposición entre ventanas (segundos)

    Returns:
    --------
    dict : Resultados del análisis temporal
    """
    h1 = np.asarray(data_h1)
    l1 = np.asarray(data_l1)

    # Calcular número de muestras
    samples_ventana = int(ventana * fs)
    samples_overlap = int(overlap * fs)
    samples_paso = samples_ventana - samples_overlap

    # Limitar al tiempo total disponible
    samples_total = min(len(h1), len(l1), int(tiempo_total * fs))

    coherencias_temporales = []
    tiempos = []

    start = 0
    while start + samples_ventana <= samples_total:
        end = start + samples_ventana

        # Extraer ventana
        h1_window = h1[start:end]
        l1_window = l1[start:end]

        # Calcular coherencia en esta ventana
        resultado = calcular_coherencia_inter_detector(
            h1_window, l1_window, fs=fs, f_target=f_target,
            ventana_tiempo=ventana
        )

        coherencias_temporales.append(resultado['coherencia_f0'])
        tiempos.append(start / fs)

        start += samples_paso

    coherencias_temporales = np.array(coherencias_temporales)
    tiempos = np.array(tiempos)

    # Estadísticas de persistencia temporal
    coherencias_significativas = coherencias_temporales > 0.4
    persistencia_ratio = np.sum(coherencias_significativas) / len(coherencias_temporales)

    return {
        'coherencias_temporales': coherencias_temporales,
        'tiempos': tiempos,
        'coherencia_media': float(np.mean(coherencias_temporales)),
        'coherencia_max': float(np.max(coherencias_temporales)),
        'coherencia_min': float(np.min(coherencias_temporales)),
        'persistencia_ratio': float(persistencia_ratio),
        'ventanas_significativas': int(np.sum(coherencias_significativas)),
        'total_ventanas': len(coherencias_temporales)
    }


def validar_sincronizacion_h1_l1(data_h1, data_l1, fs=4096, f_target=141.7001):
    """
    Validación completa de sincronización entre H1 y L1 en 141.7001 Hz

    Parameters:
    -----------
    data_h1, data_l1 : array-like
        Datos de strain de los detectores
    fs : float
        Frecuencia de muestreo
    f_target : float
        Frecuencia objetivo

    Returns:
    --------
    dict : Resultados completos de validación
    """
    print("=" * 70)
    print("VALIDACIÓN ALTERNATIVA 1: COHERENCIA INTER-DETECTOR")
    print("=" * 70)
    print(f"Frecuencia objetivo: {f_target} Hz")
    print(f"Detectores: H1 y L1")
    print()

    # 1. Coherencia global
    print("1. Análisis de coherencia global...")
    resultado_global = calcular_coherencia_inter_detector(
        data_h1, data_l1, fs=fs, f_target=f_target
    )

    print(f"   Coherencia en {f_target} Hz: {resultado_global['coherencia_f0']:.4f}")
    print(f"   Coherencia en bandas adyacentes: {resultado_global['coherencia_media_banda']:.4f}")
    print(f"   Significancia: {resultado_global['significancia']:.2f}x")
    print(f"   Desviaciones sigma: {resultado_global['sigma']:.2f}σ")
    print(f"   Criterio cumplido (> 0.4): {resultado_global['es_significativo']}")
    print()

    # 2. Análisis temporal
    print("2. Análisis de persistencia temporal...")
    resultado_temporal = analizar_coherencia_ventanas_temporales(
        data_h1, data_l1, fs=fs, f_target=f_target
    )

    print(f"   Coherencia media temporal: {resultado_temporal['coherencia_media']:.4f}")
    print(f"   Coherencia máxima: {resultado_temporal['coherencia_max']:.4f}")
    print(f"   Persistencia (ventanas > 0.4): {resultado_temporal['persistencia_ratio']*100:.1f}%")
    print(f"   Ventanas significativas: {resultado_temporal['ventanas_significativas']}/{resultado_temporal['total_ventanas']}")
    print()

    # Conclusión
    print("=" * 70)
    print("CONCLUSIÓN:")
    print("=" * 70)

    validacion_exitosa = (
        resultado_global['es_significativo'] and
        resultado_temporal['persistencia_ratio'] > 0.5
    )

    if validacion_exitosa:
        print("✅ La frecuencia 141.7001 Hz muestra coherencia significativa entre H1 y L1")
        print("   - Coherencia > 0.4 en frecuencia objetivo")
        print("   - Persistencia temporal > 50%")
        print("   - Compatible con señal física real sincronizada")
    else:
        print("❌ La coherencia no cumple todos los criterios de validación")
        print("   - Posible artefacto instrumental o insuficiente SNR")

    print()

    return {
        'resultado_global': resultado_global,
        'resultado_temporal': resultado_temporal,
        'validacion_exitosa': validacion_exitosa,
        'frecuencia_objetivo': f_target,
        'detectores': ['H1', 'L1']
    }


if __name__ == '__main__':
    print("Script de validación de coherencia inter-detector")
    print("Genera datos sintéticos para demostración")
    print()

    # Generar datos sintéticos para prueba
    fs = 4096
    duration = 2.0
    t = np.linspace(0, duration, int(fs * duration))
    f0 = 141.7001

    # Simular señal coherente en ambos detectores con ruido
    signal_template = np.sin(2 * np.pi * f0 * t)

    # H1: señal con ruido
    noise_h1 = np.random.normal(0, 0.5, len(t))
    data_h1 = signal_template + noise_h1

    # L1: misma señal con ligero retraso y ruido (simular propagación)
    delay_samples = int(0.01 * fs)  # 10 ms de retraso
    signal_l1 = np.roll(signal_template, delay_samples)
    noise_l1 = np.random.normal(0, 0.5, len(t))
    data_l1 = signal_l1 + noise_l1

    # Ejecutar validación
    resultado = validar_sincronizacion_h1_l1(data_h1, data_l1, fs=fs, f_target=f0)

    print("\n✓ Validación completada")
    print(f"✓ Estado: {'APROBADA' if resultado['validacion_exitosa'] else 'FALLIDA'}")
