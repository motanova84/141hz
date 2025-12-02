#!/usr/bin/env python3
"""
Análisis Estadístico Avanzado - Implementación del Problem Statement
Implementa las tres funciones requeridas:
1. Análisis de significancia estadística con p_value = stats.norm.sf(SNR) < 10⁻⁶
2. Coherencia multisitio compute_coherence_h1_l1(f₀)
3. Exclusión de sistemáticos exclude_instrumental_artifacts(f₀)
"""
import numpy as np
from scipy import stats, signal
from gwpy.timeseries import TimeSeries
import warnings
warnings.filterwarnings('ignore')


def calculate_snr_at_frequency(data, f0, fs=4096, method='welch'):
    """
    Calcular SNR en una frecuencia específica
    
    Parameters:
    -----------
    data : array-like
        Datos de strain del detector
    f0 : float
        Frecuencia objetivo en Hz
    fs : float
        Frecuencia de muestreo
    method : str
        Método de análisis espectral ('welch' o 'fft')
    
    Returns:
    --------
    snr : float
        Signal-to-Noise Ratio en la frecuencia objetivo
    """
    if isinstance(data, TimeSeries):
        strain = data.value
        fs = data.sample_rate.value
    else:
        strain = np.asarray(data)
    
    if method == 'welch':
        # Usar método de Welch para espectro más robusto
        nperseg = min(len(strain) // 4, 2048)
        freqs, psd = signal.welch(strain, fs, nperseg=nperseg)
    else:
        # FFT directo
        freqs = np.fft.rfftfreq(len(strain), d=1/fs)
        fft_strain = np.fft.rfft(strain)
        psd = np.abs(fft_strain)**2 / len(strain)
    
    # Encontrar índice de frecuencia objetivo
    idx_target = np.argmin(np.abs(freqs - f0))
    
    # Potencia en frecuencia objetivo
    power_target = psd[idx_target]
    
    # Estimar ruido de fondo (mediana en banda alrededor de f0)
    banda_width = 30  # Hz
    idx_start = np.argmin(np.abs(freqs - (f0 - banda_width)))
    idx_end = np.argmin(np.abs(freqs - (f0 + banda_width)))
    
    # Excluir la región inmediata alrededor del pico
    exclude_width = 5
    background_indices = np.concatenate([
        np.arange(idx_start, max(idx_start, idx_target - exclude_width)),
        np.arange(min(len(freqs)-1, idx_target + exclude_width), idx_end)
    ])
    
    if len(background_indices) > 0:
        noise_floor = np.median(psd[background_indices])
    else:
        noise_floor = np.median(psd)
    
    # SNR como razón de potencias
    if noise_floor > 0:
        snr = power_target / noise_floor
    else:
        snr = 0.0
    
    return snr


def analisis_significancia_estadistica(data, f0=141.7001, fs=4096):
    """
    1. Análisis de significancia estadística
    Calcula p-value usando stats.norm.sf(SNR)
    Criterio: p_value < 10⁻⁶
    
    Parameters:
    -----------
    data : TimeSeries or array-like
        Datos del detector
    f0 : float
        Frecuencia objetivo (Hz)
    fs : float
        Frecuencia de muestreo (Hz)
    
    Returns:
    --------
    dict : Resultados del análisis
        - snr: Signal-to-Noise Ratio
        - p_value: Probabilidad de falso positivo
        - significativo: bool, True si p_value < 10⁻⁶
    """
    # Calcular SNR en la frecuencia objetivo
    snr = calculate_snr_at_frequency(data, f0, fs)
    
    # Calcular p-value usando survival function de distribución normal
    # Esto da la probabilidad de observar un SNR >= observado bajo hipótesis nula
    p_value = stats.norm.sf(snr)
    
    # Criterio de significancia
    significativo = p_value < 1e-6
    
    resultado = {
        'f0': f0,
        'snr': float(snr),
        'p_value': float(p_value),
        'significativo': bool(significativo),
        'criterio': 'p_value < 10⁻⁶'
    }
    
    return resultado


def compute_coherence_h1_l1(f0, data_h1, data_l1, fs=4096, bandwidth=10):
    """
    2. Coherencia multisitio
    Calcula coherencia entre H1 y L1 en la frecuencia f0
    
    Parameters:
    -----------
    f0 : float
        Frecuencia objetivo (Hz)
    data_h1 : TimeSeries or array-like
        Datos del detector H1
    data_l1 : TimeSeries or array-like
        Datos del detector L1
    fs : float
        Frecuencia de muestreo (Hz)
    bandwidth : float
        Ancho de banda para análisis de coherencia (Hz)
    
    Returns:
    --------
    dict : Resultados de coherencia
        - coherence_at_f0: Coherencia en f0
        - coherence_mean: Coherencia media en banda
        - coherence_std: Desviación estándar en banda
        - coherent: bool, True si coherencia significativa
    """
    # Convertir a arrays si son TimeSeries
    if isinstance(data_h1, TimeSeries):
        strain_h1 = data_h1.value
        fs = data_h1.sample_rate.value
    else:
        strain_h1 = np.asarray(data_h1)
    
    if isinstance(data_l1, TimeSeries):
        strain_l1 = data_l1.value
    else:
        strain_l1 = np.asarray(data_l1)
    
    # Asegurar misma longitud
    min_len = min(len(strain_h1), len(strain_l1))
    strain_h1 = strain_h1[:min_len]
    strain_l1 = strain_l1[:min_len]
    
    # Calcular coherencia usando scipy.signal.coherence
    nperseg = min(len(strain_h1) // 4, 2048)
    freqs, coherence = signal.coherence(
        strain_h1, strain_l1, 
        fs=fs, 
        nperseg=nperseg
    )
    
    # Encontrar coherencia en f0
    idx_f0 = np.argmin(np.abs(freqs - f0))
    coherence_at_f0 = coherence[idx_f0]
    
    # Calcular coherencia en banda alrededor de f0
    idx_start = np.argmin(np.abs(freqs - (f0 - bandwidth/2)))
    idx_end = np.argmin(np.abs(freqs - (f0 + bandwidth/2)))
    coherence_band = coherence[idx_start:idx_end]
    
    coherence_mean = np.mean(coherence_band)
    coherence_std = np.std(coherence_band)
    
    # Criterio de coherencia significativa
    # Coherencia > 0.5 indica correlación fuerte entre detectores
    coherent = coherence_at_f0 > 0.5
    
    resultado = {
        'f0': f0,
        'coherence_at_f0': float(coherence_at_f0),
        'coherence_mean': float(coherence_mean),
        'coherence_std': float(coherence_std),
        'coherent': coherent,
        'criterio': 'coherence > 0.5'
    }
    
    return resultado


def exclude_instrumental_artifacts(f0, data, fs=4096, detector='H1'):
    """
    3. Exclusión de sistemáticos
    Verifica que la frecuencia f0 no coincida con líneas instrumentales conocidas
    
    Parameters:
    -----------
    f0 : float
        Frecuencia objetivo (Hz)
    data : TimeSeries or array-like
        Datos del detector
    fs : float
        Frecuencia de muestreo (Hz)
    detector : str
        Nombre del detector ('H1' o 'L1')
    
    Returns:
    --------
    dict : Resultados del test de sistemáticos
        - is_clean: bool, True si f0 no es artefacto instrumental
        - nearest_line: Línea instrumental más cercana
        - distance: Distancia a línea instrumental más cercana
        - lines_checked: Lista de líneas instrumentales verificadas
    """
    # Líneas instrumentales conocidas en LIGO (Hz)
    instrumental_lines = {
        60: "Power line noise (red eléctrica)",
        120: "Armónico de 60 Hz",
        180: "2° armónico de 60 Hz",
        240: "3° armónico de 60 Hz",
        300: "Bombas de vacío",
        393: "Violín modes (suspensión)",
        500: "Calibración",
        1000: "Calibración"
    }
    
    # Agregar líneas específicas de cada detector
    if detector == 'H1':
        instrumental_lines.update({
            35.9: "Violín mode H1",
            72.0: "Violín mode H1 - 1st harmonic",
            108.0: "Violín mode H1 - 2nd harmonic"
        })
    elif detector == 'L1':
        instrumental_lines.update({
            36.7: "Violín mode L1",
            73.4: "Violín mode L1 - 1st harmonic",
            110.0: "Violín mode L1 - 2nd harmonic"
        })
    
    # Calcular distancias a todas las líneas instrumentales
    frequencies = np.array(list(instrumental_lines.keys()))
    distances = np.abs(frequencies - f0)
    
    # Encontrar línea más cercana
    nearest_idx = np.argmin(distances)
    nearest_freq = frequencies[nearest_idx]
    nearest_distance = distances[nearest_idx]
    nearest_description = instrumental_lines[nearest_freq]
    
    # Criterio de exclusión: f0 debe estar a más de 2 Hz de cualquier línea conocida
    # Este umbral es conservador para evitar falsos positivos
    tolerance = 2.0  # Hz
    is_clean = nearest_distance > tolerance
    
    # Análisis espectral para verificar estructura de líneas
    if isinstance(data, TimeSeries):
        strain = data.value
        fs = data.sample_rate.value
    else:
        strain = np.asarray(data)
    
    # Calcular espectro
    nperseg = min(len(strain) // 4, 2048)
    freqs_spec, psd = signal.welch(strain, fs, nperseg=nperseg)
    
    # Verificar si hay picos en líneas instrumentales
    lines_detected = []
    for freq_line in frequencies:
        idx_line = np.argmin(np.abs(freqs_spec - freq_line))
        power_line = psd[idx_line]
        
        # Comparar con mediana local
        idx_start = max(0, idx_line - 10)
        idx_end = min(len(psd), idx_line + 10)
        median_local = np.median(psd[idx_start:idx_end])
        
        if power_line > 3 * median_local:  # Pico significativo
            lines_detected.append({
                'frequency': freq_line,
                'description': instrumental_lines[freq_line],
                'snr': power_line / median_local
            })
    
    resultado = {
        'f0': f0,
        'is_clean': is_clean,
        'nearest_line': {
            'frequency': float(nearest_freq),
            'description': nearest_description,
            'distance': float(nearest_distance)
        },
        'tolerance': tolerance,
        'lines_detected': lines_detected,
        'lines_checked': list(instrumental_lines.keys()),
        'criterio': f'distance > {tolerance} Hz de líneas instrumentales'
    }
    
    return resultado


def ejecutar_analisis_completo(data_h1, data_l1, f0=141.7001, fs=4096):
    """
    Ejecutar análisis completo según problem statement
    
    Parameters:
    -----------
    data_h1 : TimeSeries or array-like
        Datos del detector H1
    data_l1 : TimeSeries or array-like
        Datos del detector L1
    f0 : float
        Frecuencia objetivo (Hz)
    fs : float
        Frecuencia de muestreo (Hz)
    
    Returns:
    --------
    dict : Resultados completos
    """
    print("=" * 70)
    print("🔬 ANÁLISIS ESTADÍSTICO AVANZADO")
    print("=" * 70)
    print(f"Frecuencia objetivo: {f0} Hz")
    print()
    
    # 1. Análisis de significancia estadística
    print("1️⃣  Análisis de significancia estadística")
    print("-" * 70)
    sig_h1 = analisis_significancia_estadistica(data_h1, f0, fs)
    sig_l1 = analisis_significancia_estadistica(data_l1, f0, fs)
    
    print(f"H1: SNR = {sig_h1['snr']:.2f}, p-value = {sig_h1['p_value']:.2e}")
    print(f"    {'✅ Significativo' if sig_h1['significativo'] else '❌ No significativo'} (criterio: p < 10⁻⁶)")
    print(f"L1: SNR = {sig_l1['snr']:.2f}, p-value = {sig_l1['p_value']:.2e}")
    print(f"    {'✅ Significativo' if sig_l1['significativo'] else '❌ No significativo'} (criterio: p < 10⁻⁶)")
    print()
    
    # 2. Coherencia multisitio
    print("2️⃣  Coherencia multisitio H1-L1")
    print("-" * 70)
    coherence = compute_coherence_h1_l1(f0, data_h1, data_l1, fs)
    
    print(f"Coherencia en {f0} Hz: {coherence['coherence_at_f0']:.3f}")
    print(f"Coherencia media en banda: {coherence['coherence_mean']:.3f} ± {coherence['coherence_std']:.3f}")
    print(f"    {'✅ Señal coherente' if coherence['coherent'] else '❌ No coherente'} (criterio: coherence > 0.5)")
    print()
    
    # 3. Exclusión de sistemáticos
    print("3️⃣  Exclusión de sistemáticos instrumentales")
    print("-" * 70)
    systematics_h1 = exclude_instrumental_artifacts(f0, data_h1, fs, 'H1')
    systematics_l1 = exclude_instrumental_artifacts(f0, data_l1, fs, 'L1')
    
    print(f"H1: Línea instrumental más cercana: {systematics_h1['nearest_line']['frequency']} Hz")
    print(f"    ({systematics_h1['nearest_line']['description']})")
    print(f"    Distancia: {systematics_h1['nearest_line']['distance']:.1f} Hz")
    print(f"    {'✅ Sin artefactos' if systematics_h1['is_clean'] else '❌ Posible artefacto'}")
    
    print(f"L1: Línea instrumental más cercana: {systematics_l1['nearest_line']['frequency']} Hz")
    print(f"    ({systematics_l1['nearest_line']['description']})")
    print(f"    Distancia: {systematics_l1['nearest_line']['distance']:.1f} Hz")
    print(f"    {'✅ Sin artefactos' if systematics_l1['is_clean'] else '❌ Posible artefacto'}")
    print()
    
    # Resumen
    print("=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    
    criterios_cumplidos = 0
    total_criterios = 4
    
    # Criterio 1: Significancia en al menos un detector
    sig_passed = sig_h1['significativo'] or sig_l1['significativo']
    if sig_passed:
        print("✅ Significancia estadística (p < 10⁻⁶)")
        criterios_cumplidos += 1
    else:
        print("❌ Significancia estadística NO cumplida")
    
    # Criterio 2: Coherencia multisitio
    if coherence['coherent']:
        print("✅ Coherencia multisitio (coherence > 0.5)")
        criterios_cumplidos += 1
    else:
        print("❌ Coherencia multisitio NO cumplida")
    
    # Criterio 3: Exclusión de sistemáticos H1
    if systematics_h1['is_clean']:
        print("✅ Exclusión de sistemáticos H1")
        criterios_cumplidos += 1
    else:
        print("❌ Exclusión de sistemáticos H1 NO cumplida")
    
    # Criterio 4: Exclusión de sistemáticos L1
    if systematics_l1['is_clean']:
        print("✅ Exclusión de sistemáticos L1")
        criterios_cumplidos += 1
    else:
        print("❌ Exclusión de sistemáticos L1 NO cumplida")
    
    print()
    print(f"📈 Criterios cumplidos: {criterios_cumplidos}/{total_criterios}")
    
    # Preparar resultados completos
    resultados = {
        'f0': f0,
        'significancia': {
            'h1': sig_h1,
            'l1': sig_l1,
            'passed': sig_passed
        },
        'coherencia': coherence,
        'sistemáticos': {
            'h1': systematics_h1,
            'l1': systematics_l1,
            'passed': systematics_h1['is_clean'] and systematics_l1['is_clean']
        },
        'criterios_cumplidos': criterios_cumplidos,
        'total_criterios': total_criterios,
        'validacion_exitosa': criterios_cumplidos >= 3  # Al menos 3 de 4
    }
    
    return resultados


# Ejemplo de uso y testing
if __name__ == "__main__":
    print("🧪 Testing módulo de análisis estadístico avanzado")
    print("Generando datos sintéticos...")
    
    # Generar datos sintéticos para testing
    fs = 4096
    duration = 2  # segundos
    t = np.linspace(0, duration, int(fs * duration))
    
    # Señal de prueba: modo en 141.7 Hz con algo de ruido
    f0 = 141.7001
    signal_h1 = 1e-21 * np.exp(-np.pi * f0 * t / 8.5) * np.sin(2 * np.pi * f0 * t)
    noise_h1 = np.random.normal(0, 2e-22, len(t))
    data_h1 = signal_h1 + noise_h1
    
    # L1 con señal correlacionada pero con fase y amplitud diferentes
    signal_l1 = 0.7e-21 * np.exp(-np.pi * f0 * t / 8.5) * np.sin(2 * np.pi * f0 * t + np.pi/4)
    noise_l1 = np.random.normal(0, 2e-22, len(t))
    data_l1 = signal_l1 + noise_l1
    
    # Ejecutar análisis completo
    resultados = ejecutar_analisis_completo(data_h1, data_l1, f0, fs)
    
    print()
    if resultados['validacion_exitosa']:
        print("✅ VALIDACIÓN EXITOSA")
    else:
        print("⚠️  VALIDACIÓN PARCIAL - Revisar criterios no cumplidos")
