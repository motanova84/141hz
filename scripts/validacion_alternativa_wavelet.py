#!/usr/bin/env python3
"""
Validación Alternativa 2: Persistencia Temporal + Análisis Wavelet
===================================================================

Hipótesis: Una señal real debe persistir más de un ciclo, incluso si débil.

Implementa:
- Aplicar wavelet transform (CWT) para aislar componentes a 141.7 Hz
- Medir duración en tiempo (ms) y consistencia de fase en cada evento
- Comparar con señales transitorias (ruido)
"""

import numpy as np
from scipy import signal as sp_signal
import pywt
import warnings
warnings.filterwarnings('ignore')


def analisis_wavelet_continuo(data, fs=4096, f_target=141.7001,
                               freq_range=(100, 200)):
    """
    Análisis de wavelet continuo (CWT) para aislar componente de frecuencia

    Parameters:
    -----------
    data : array-like
        Serie temporal de datos (strain)
    fs : float
        Frecuencia de muestreo (Hz)
    f_target : float
        Frecuencia objetivo (Hz)
    freq_range : tuple
        Rango de frecuencias a analizar (Hz)

    Returns:
    --------
    dict : Resultados del análisis wavelet
    """
    strain = np.asarray(data)

    # Definir escalas para CWT (convertir de frecuencia a escala)
    # scale = central_frequency / frequency
    wavelet = 'cmor1.5-1.0'  # Complex Morlet wavelet
    central_freq = pywt.central_frequency(wavelet)

    # Escalas correspondientes al rango de frecuencias
    frequencies = np.linspace(freq_range[0], freq_range[1], 200)
    scales = central_freq * fs / frequencies

    # Calcular CWT
    coefficients, freqs_cwt = pywt.cwt(strain, scales, wavelet,
                                        sampling_period=1/fs)

    # Encontrar índice de frecuencia objetivo
    idx_target = np.argmin(np.abs(freqs_cwt - f_target))
    freq_actual = freqs_cwt[idx_target]

    # Extraer componente de frecuencia objetivo
    componente_f0 = coefficients[idx_target, :]
    potencia_f0 = np.abs(componente_f0) ** 2
    fase_f0 = np.angle(componente_f0)

    # Calcular tiempo
    t = np.arange(len(strain)) / fs

    return {
        'coefficients': coefficients,
        'frequencies': freqs_cwt,
        'componente_f0': componente_f0,
        'potencia_f0': potencia_f0,
        'fase_f0': fase_f0,
        'tiempo': t,
        'freq_target': f_target,
        'freq_actual': freq_actual
    }


def medir_persistencia_temporal(potencia, tiempo, umbral_percentil=50):
    """
    Mide la persistencia temporal de una señal

    Parameters:
    -----------
    potencia : array-like
        Serie temporal de potencia
    tiempo : array-like
        Vector de tiempo correspondiente
    umbral_percentil : float
        Percentil para definir "señal significativa"

    Returns:
    --------
    dict : Métricas de persistencia
    """
    # Umbral de significancia
    umbral = np.percentile(potencia, umbral_percentil)

    # Identificar regiones por encima del umbral
    significativas = potencia > umbral

    # Calcular duración total de señal significativa
    dt = tiempo[1] - tiempo[0] if len(tiempo) > 1 else 0
    duracion_significativa = np.sum(significativas) * dt * 1000  # en ms
    duracion_total = (tiempo[-1] - tiempo[0]) * 1000  # en ms

    # Ratio de persistencia
    persistencia_ratio = np.sum(significativas) / len(significativas)

    # Encontrar regiones continuas
    diff_significativas = np.diff(np.concatenate([[0], significativas.astype(int), [0]]))
    starts = np.where(diff_significativas == 1)[0]
    ends = np.where(diff_significativas == -1)[0]

    # Duraciones de cada región
    if len(starts) > 0 and len(ends) > 0:
        duraciones_regiones = (ends - starts) * dt * 1000  # en ms
        num_regiones = len(starts)
        duracion_media_region = np.mean(duraciones_regiones)
        duracion_max_region = np.max(duraciones_regiones)
    else:
        duraciones_regiones = []
        num_regiones = 0
        duracion_media_region = 0
        duracion_max_region = 0

    return {
        'duracion_significativa_ms': float(duracion_significativa),
        'duracion_total_ms': float(duracion_total),
        'persistencia_ratio': float(persistencia_ratio),
        'num_regiones_continuas': int(num_regiones),
        'duracion_media_region_ms': float(duracion_media_region),
        'duracion_max_region_ms': float(duracion_max_region),
        'duraciones_regiones_ms': duraciones_regiones.tolist() if len(duraciones_regiones) > 0 else []
    }


def analizar_consistencia_fase(fase, tiempo, umbral_variacion=np.pi/4):
    """
    Analiza la consistencia de fase en el tiempo

    Parameters:
    -----------
    fase : array-like
        Serie temporal de fase (radianes)
    tiempo : array-like
        Vector de tiempo
    umbral_variacion : float
        Umbral de variación de fase considerada consistente (radianes)

    Returns:
    --------
    dict : Métricas de consistencia de fase
    """
    # Unwrap fase para evitar discontinuidades
    fase_unwrapped = np.unwrap(fase)

    # Calcular variación de fase
    variacion_fase = np.diff(fase_unwrapped)

    # Estadísticas de variación
    variacion_std = np.std(variacion_fase)
    variacion_media = np.mean(np.abs(variacion_fase))

    # Frecuencia instantánea (derivada de fase / 2π)
    dt = tiempo[1] - tiempo[0] if len(tiempo) > 1 else 1/4096
    freq_instantanea = np.abs(variacion_fase) / (2 * np.pi * dt)

    # Consistencia: proporción de variaciones pequeñas
    variaciones_consistentes = np.abs(variacion_fase) < umbral_variacion
    consistencia_ratio = np.sum(variaciones_consistentes) / len(variacion_fase)

    return {
        'variacion_fase_std': float(variacion_std),
        'variacion_fase_media': float(variacion_media),
        'frecuencia_instantanea_media': float(np.mean(freq_instantanea)),
        'frecuencia_instantanea_std': float(np.std(freq_instantanea)),
        'consistencia_ratio': float(consistencia_ratio),
        'fase_estable': bool(consistencia_ratio > 0.7)
    }


def validar_persistencia_wavelet(data, fs=4096, f_target=141.7001):
    """
    Validación completa de persistencia temporal usando wavelet

    Parameters:
    -----------
    data : array-like
        Datos de strain
    fs : float
        Frecuencia de muestreo
    f_target : float
        Frecuencia objetivo

    Returns:
    --------
    dict : Resultados completos de validación
    """
    print("=" * 70)
    print("VALIDACIÓN ALTERNATIVA 2: PERSISTENCIA TEMPORAL + WAVELET")
    print("=" * 70)
    print(f"Frecuencia objetivo: {f_target} Hz")
    print(f"Frecuencia de muestreo: {fs} Hz")
    print()

    # 1. Análisis wavelet
    print("1. Análisis wavelet continuo (CWT)...")
    resultado_cwt = analisis_wavelet_continuo(data, fs=fs, f_target=f_target)

    print(f"   Frecuencia analizada: {resultado_cwt['freq_actual']:.4f} Hz")
    print(f"   Duración total: {resultado_cwt['tiempo'][-1]*1000:.1f} ms")
    print()

    # 2. Persistencia temporal
    print("2. Análisis de persistencia temporal...")
    resultado_persistencia = medir_persistencia_temporal(
        resultado_cwt['potencia_f0'],
        resultado_cwt['tiempo']
    )

    print(f"   Duración significativa: {resultado_persistencia['duracion_significativa_ms']:.1f} ms")
    print(f"   Persistencia ratio: {resultado_persistencia['persistencia_ratio']*100:.1f}%")
    print(f"   Regiones continuas: {resultado_persistencia['num_regiones_continuas']}")
    print(f"   Duración máxima región: {resultado_persistencia['duracion_max_region_ms']:.1f} ms")
    print()

    # 3. Consistencia de fase
    print("3. Análisis de consistencia de fase...")
    resultado_fase = analizar_consistencia_fase(
        resultado_cwt['fase_f0'],
        resultado_cwt['tiempo']
    )

    print(f"   Frecuencia instantánea media: {resultado_fase['frecuencia_instantanea_media']:.2f} Hz")
    print(f"   Variación de fase (std): {resultado_fase['variacion_fase_std']:.4f} rad")
    print(f"   Consistencia de fase: {resultado_fase['consistencia_ratio']*100:.1f}%")
    print(f"   Fase estable: {resultado_fase['fase_estable']}")
    print()

    # Criterios de validación
    # Una señal real debe:
    # 1. Persistir al menos 10 ms (más de 1-2 ciclos a 141.7 Hz, período ~ 7 ms)
    # 2. Tener ratio de persistencia > 30%
    # 3. Tener consistencia de fase > 70%

    periodo_f0 = 1000 / f_target  # período en ms
    ciclos_minimos = 1.5
    duracion_minima = periodo_f0 * ciclos_minimos

    validacion_exitosa = (
        resultado_persistencia['duracion_max_region_ms'] > duracion_minima and
        resultado_persistencia['persistencia_ratio'] > 0.3 and
        resultado_fase['fase_estable']
    )

    # Conclusión
    print("=" * 70)
    print("CONCLUSIÓN:")
    print("=" * 70)
    print(f"Período de {f_target} Hz: {periodo_f0:.2f} ms")
    print(f"Duración mínima requerida: {duracion_minima:.2f} ms ({ciclos_minimos} ciclos)")
    print()

    if validacion_exitosa:
        print("✅ La frecuencia 141.7001 Hz muestra persistencia temporal significativa")
        print("   - Duración > umbral mínimo")
        print("   - Persistencia > 30%")
        print("   - Fase consistente (> 70%)")
        print("   - Compatible con señal física coherente")
    else:
        print("❌ La señal no cumple criterios de persistencia temporal")
        if resultado_persistencia['duracion_max_region_ms'] <= duracion_minima:
            dur_max = resultado_persistencia['duracion_max_region_ms']
            print(f"   - Duración insuficiente ({dur_max:.1f} < {duracion_minima:.1f} ms)")
        if resultado_persistencia['persistencia_ratio'] <= 0.3:
            print(f"   - Persistencia baja ({resultado_persistencia['persistencia_ratio']*100:.1f}%)")
        if not resultado_fase['fase_estable']:
            print(f"   - Fase inestable ({resultado_fase['consistencia_ratio']*100:.1f}%)")
        print("   - Posible artefacto transitorio o ruido")

    print()

    return {
        'resultado_cwt': {
            'freq_target': resultado_cwt['freq_target'],
            'freq_actual': resultado_cwt['freq_actual'],
            'potencia_maxima': float(np.max(resultado_cwt['potencia_f0']))
        },
        'resultado_persistencia': resultado_persistencia,
        'resultado_fase': resultado_fase,
        'validacion_exitosa': validacion_exitosa,
        'periodo_ms': periodo_f0,
        'duracion_minima_ms': duracion_minima
    }


if __name__ == '__main__':
    print("Script de validación de persistencia temporal con wavelet")
    print("Genera datos sintéticos para demostración")
    print()

    # Generar datos sintéticos para prueba
    fs = 4096
    duration = 1.0
    t = np.linspace(0, duration, int(fs * duration))
    f0 = 141.7001

    # Simular señal con envolvente (ringdown-like)
    tau = 0.15  # constante de tiempo de decaimiento (segundos)
    envelope = np.exp(-t / tau)
    signal_component = envelope * np.sin(2 * np.pi * f0 * t)

    # Añadir ruido
    noise = np.random.normal(0, 0.3, len(t))
    data = signal_component + noise

    # Ejecutar validación
    resultado = validar_persistencia_wavelet(data, fs=fs, f_target=f0)

    print("\n✓ Validación completada")
    print(f"✓ Estado: {'APROBADA' if resultado['validacion_exitosa'] else 'FALLIDA'}")
