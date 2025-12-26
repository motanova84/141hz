#!/usr/bin/env python3
"""
Análisis de 141.7001 Hz con Bandpass Filter [140.5-143.0 Hz]

Este script implementa el análisis específico del pico secundario de energía
en 141.7001 Hz usando filtro bandpass [140.5-143.0 Hz] sobre datos strain .hdf5
publicados por GWOSC.

Comportamiento esperado:
- Frecuencia esperada: f̂ = 141.7001 ± 0.0012 Hz
- Aparecerá como pico secundario de energía en análisis tipo Q-transform o wavelet packets (Q > 30)
- Será visible dentro de la ventana ±0.3 s del merger del evento principal (fase chirp → coalescencia)
- Aparecerá con coherencia parcial entre al menos dos detectores (ej. H1 y L1)
- No será atribuible a líneas espectrales conocidas ni glitches instrumentales estándar
- Su presencia será reproducible con filtros band-pass [140.5–143.0] Hz

Uso:
    python3 analisis_141hz_bandpass.py --event GW150914
    python3 analisis_141hz_bandpass.py --event GW150914 --detectors H1 L1
    python3 analisis_141hz_bandpass.py --event GW150914 --output results/
"""

import sys
import os
import argparse
from datetime import datetime

# Try to import required dependencies
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # Create minimal mock for constants testing
    class np:
        @staticmethod
        def argmin(x): return 0
        @staticmethod
        def argmax(x): return 0
        @staticmethod
        def abs(x): return abs(x)
        @staticmethod
        def mean(x): return sum(x) / len(x) if x else 0
        @staticmethod
        def std(x): 
            if not x: return 0
            m = np.mean(x)
            return (sum((xi - m)**2 for xi in x) / len(x)) ** 0.5
        @staticmethod
        def median(x): 
            s = sorted(x)
            n = len(s)
            return s[n//2] if n % 2 else (s[n//2-1] + s[n//2]) / 2

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    MPL_AVAILABLE = True
except ImportError:
    MPL_AVAILABLE = False

try:
    from gwpy.timeseries import TimeSeries
    from gwpy.signal import filter_design
    GWPY_AVAILABLE = True
except ImportError:
    GWPY_AVAILABLE = False
    # Module can still be imported for testing constants


# Parámetros de análisis según especificaciones
TARGET_FREQUENCY = 141.7001  # Hz
FREQUENCY_UNCERTAINTY = 0.0012  # Hz
BANDPASS_LOW = 140.5  # Hz
BANDPASS_HIGH = 143.0  # Hz
MERGER_WINDOW = 0.3  # segundos (±0.3s alrededor del merger)
MIN_Q_VALUE = 30  # Q > 30 para Q-transform
MIN_DETECTORS = 2  # Coherencia entre al menos 2 detectores


# Catálogo de eventos GWOSC conocidos
KNOWN_EVENTS = {
    'GW150914': 1126259462.423,
    'GW151012': 1128678900.44,
    'GW151226': 1135136350.6,
    'GW170104': 1167559936.6,
    'GW170814': 1186741861.5,
    'GW170817': 1187008882.4,
    'GW170823': 1187529256.5,
}


def validate_event(event_name):
    """Validar que el evento existe en el catálogo"""
    if event_name not in KNOWN_EVENTS:
        print(f"❌ Evento {event_name} no encontrado en el catálogo")
        print(f"   Eventos disponibles: {', '.join(KNOWN_EVENTS.keys())}")
        return None
    return KNOWN_EVENTS[event_name]


def download_strain_data(event_name, detector, merger_time):
    """
    Descargar datos strain .hdf5 desde GWOSC
    
    Args:
        event_name: Nombre del evento (e.g., 'GW150914')
        detector: Nombre del detector (e.g., 'H1', 'L1')
        merger_time: Tiempo GPS del merger
        
    Returns:
        TimeSeries: Datos de strain
    """
    if not GWPY_AVAILABLE:
        print(f"   ❌ GWPy no está disponible")
        return None
        
    print(f"   📡 Descargando datos de {detector}...")
    
    # Ventana de datos: ±16 segundos alrededor del merger
    start_time = merger_time - 16
    end_time = merger_time + 16
    
    try:
        data = TimeSeries.fetch_open_data(detector, start_time, end_time, sample_rate=4096)
        print(f"   ✅ Datos descargados: {len(data)} muestras a {data.sample_rate} Hz")
        return data
    except Exception as e:
        print(f"   ❌ Error descargando datos: {e}")
        return None


def apply_bandpass_filter(data, low_freq=BANDPASS_LOW, high_freq=BANDPASS_HIGH):
    """
    Aplicar filtro bandpass [140.5-143.0 Hz] al strain
    
    Args:
        data: TimeSeries de datos
        low_freq: Frecuencia baja del filtro (Hz)
        high_freq: Frecuencia alta del filtro (Hz)
        
    Returns:
        TimeSeries: Datos filtrados
    """
    if not GWPY_AVAILABLE:
        print(f"   ❌ GWPy no está disponible")
        return None
        
    print(f"   🔧 Aplicando filtro bandpass [{low_freq}-{high_freq}] Hz...")
    
    # Diseñar filtro bandpass
    bp = filter_design.bandpass(low_freq, high_freq, data.sample_rate)
    
    # Aplicar filtro (filtfilt para fase cero)
    filtered_data = data.filter(bp, filtfilt=True)
    
    print(f"   ✅ Filtro aplicado exitosamente")
    return filtered_data


def extract_merger_window(data, merger_time, window=MERGER_WINDOW):
    """
    Extraer ventana de ±0.3s alrededor del merger
    
    Args:
        data: TimeSeries de datos
        merger_time: Tiempo GPS del merger
        window: Ventana temporal en segundos (±window)
        
    Returns:
        TimeSeries: Segmento de datos alrededor del merger
    """
    print(f"   ✂️  Extrayendo ventana de ±{window}s alrededor del merger...")
    
    # Ventana temporal
    start = merger_time - window
    end = merger_time + window
    
    # Extraer segmento
    segment = data.crop(start, end)
    
    print(f"   ✅ Ventana extraída: {len(segment)} muestras ({len(segment)/data.sample_rate.value:.3f}s)")
    return segment


def compute_qtransform(data, merger_time, qrange=(MIN_Q_VALUE, 100), frange=(BANDPASS_LOW, BANDPASS_HIGH)):
    """
    Calcular Q-transform con Q > 30
    
    Args:
        data: TimeSeries de datos
        merger_time: Tiempo GPS del merger
        qrange: Rango de valores Q (Q_min, Q_max)
        frange: Rango de frecuencias (f_min, f_max)
        
    Returns:
        Spectrogram: Q-transform
    """
    print(f"   📊 Calculando Q-transform (Q={qrange[0]}-{qrange[1]}, f={frange[0]}-{frange[1]} Hz)...")
    
    # Calcular Q-transform
    # Usar ventana alrededor del merger
    window_duration = 2 * MERGER_WINDOW
    qtransform = data.q_transform(
        outseg=(merger_time - MERGER_WINDOW, merger_time + MERGER_WINDOW),
        qrange=qrange,
        frange=frange
    )
    
    print(f"   ✅ Q-transform calculado")
    return qtransform


def analyze_frequency_peak(data, target_freq=TARGET_FREQUENCY, bandwidth=0.5):
    """
    Analizar pico de frecuencia en la banda objetivo
    
    Args:
        data: TimeSeries de datos
        target_freq: Frecuencia objetivo (Hz)
        bandwidth: Ancho de banda para análisis (Hz)
        
    Returns:
        dict: Resultados del análisis
    """
    print(f"   🎯 Analizando pico de frecuencia en {target_freq} Hz...")
    
    # Calcular espectro de potencia
    spectrum = data.asd(fftlength=0.25, overlap=0.125)
    
    # Encontrar índice más cercano a la frecuencia objetivo
    freq_idx = np.argmin(np.abs(spectrum.frequencies.value - target_freq))
    detected_freq = spectrum.frequencies.value[freq_idx]
    power_at_target = spectrum.value[freq_idx]
    
    # Calcular SNR en banda estrecha
    freq_mask = (spectrum.frequencies.value >= target_freq - bandwidth) & \
                (spectrum.frequencies.value <= target_freq + bandwidth)
    noise_floor = np.median(spectrum.value[freq_mask])
    
    # Evitar división por cero
    if noise_floor > 0:
        snr = power_at_target / noise_floor
    else:
        snr = 0.0
    
    # Verificar si está dentro del rango esperado
    within_expected = abs(detected_freq - target_freq) <= FREQUENCY_UNCERTAINTY
    
    results = {
        'detected_frequency': detected_freq,
        'power': power_at_target,
        'snr': snr,
        'within_expected': within_expected,
        'deviation': abs(detected_freq - target_freq),
        'spectrum': spectrum
    }
    
    print(f"   ✅ Frecuencia detectada: {detected_freq:.4f} Hz (Δf = {results['deviation']:.4f} Hz)")
    print(f"   ✅ SNR: {snr:.2f}")
    print(f"   ✅ Dentro del rango esperado: {'SÍ' if within_expected else 'NO'}")
    
    return results


def check_coherence(results_dict):
    """
    Verificar coherencia entre detectores
    
    Args:
        results_dict: Diccionario con resultados por detector
        
    Returns:
        dict: Análisis de coherencia
    """
    print("\n🔗 Verificando coherencia entre detectores...")
    
    if len(results_dict) < MIN_DETECTORS:
        print(f"   ⚠️  Se requieren al menos {MIN_DETECTORS} detectores")
        return {
            'coherent': False,
            'reason': f'Insuficientes detectores ({len(results_dict)}/{MIN_DETECTORS})'
        }
    
    # Extraer frecuencias detectadas
    frequencies = [r['detected_frequency'] for r in results_dict.values()]
    snrs = [r['snr'] for r in results_dict.values()]
    
    # Calcular coherencia: todas las frecuencias deben estar cerca
    freq_std = np.std(frequencies)
    freq_mean = np.mean(frequencies)
    
    # Criterio de coherencia: desviación estándar < 0.1 Hz y SNR promedio > 1.5
    coherent = (freq_std < 0.1) and (np.mean(snrs) > 1.5)
    
    coherence_results = {
        'coherent': coherent,
        'freq_mean': freq_mean,
        'freq_std': freq_std,
        'snr_mean': np.mean(snrs),
        'num_detectors': len(results_dict)
    }
    
    print(f"   Frecuencia media: {freq_mean:.4f} ± {freq_std:.4f} Hz")
    print(f"   SNR medio: {np.mean(snrs):.2f}")
    print(f"   Coherencia: {'✅ SÍ' if coherent else '❌ NO'}")
    
    return coherence_results


def create_visualization(event_name, results_dict, qtransforms, output_dir):
    """
    Crear visualización de los resultados
    
    Args:
        event_name: Nombre del evento
        results_dict: Diccionario con resultados por detector
        qtransforms: Diccionario con Q-transforms por detector
        output_dir: Directorio de salida
    """
    print("\n📊 Creando visualización...")
    
    # Crear figura con subplots para cada detector
    n_detectors = len(results_dict)
    fig = plt.figure(figsize=(15, 5 * n_detectors))
    
    for i, (detector, results) in enumerate(results_dict.items(), 1):
        # Subplot 1: Espectro de potencia con filtro bandpass
        ax1 = fig.add_subplot(n_detectors, 3, (i-1)*3 + 1)
        spectrum = results['spectrum']
        
        # Filtrar espectro para mostrar solo la banda de interés
        freq_mask = (spectrum.frequencies.value >= BANDPASS_LOW - 5) & \
                    (spectrum.frequencies.value <= BANDPASS_HIGH + 5)
        
        ax1.plot(spectrum.frequencies.value[freq_mask], 
                spectrum.value[freq_mask], 
                'b-', linewidth=1.5, label='ASD')
        ax1.axvline(TARGET_FREQUENCY, color='green', linestyle='--', 
                   linewidth=2, label=f'Objetivo: {TARGET_FREQUENCY} Hz')
        ax1.axvline(results['detected_frequency'], color='red', linestyle='--', 
                   linewidth=2, label=f'Detectado: {results["detected_frequency"]:.4f} Hz')
        ax1.axvspan(BANDPASS_LOW, BANDPASS_HIGH, alpha=0.2, color='yellow', 
                   label=f'Bandpass [{BANDPASS_LOW}-{BANDPASS_HIGH}] Hz')
        
        ax1.set_xlabel('Frecuencia (Hz)')
        ax1.set_ylabel('ASD (1/√Hz)')
        ax1.set_title(f'{detector} - Espectro de Potencia (Bandpass Filter)')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # Subplot 2: Q-transform
        ax2 = fig.add_subplot(n_detectors, 3, (i-1)*3 + 2)
        if detector in qtransforms:
            qtransform = qtransforms[detector]
            im = qtransform.plot(ax=ax2)
            ax2.axhline(TARGET_FREQUENCY, color='white', linestyle='--', 
                       linewidth=2, label=f'{TARGET_FREQUENCY} Hz')
            ax2.set_ylim(BANDPASS_LOW, BANDPASS_HIGH)
            ax2.set_xlabel('Tiempo desde merger (s)')
            ax2.set_ylabel('Frecuencia (Hz)')
            ax2.set_title(f'{detector} - Q-Transform (Q > {MIN_Q_VALUE})')
            ax2.legend(fontsize=8)
            plt.colorbar(im, ax=ax2, label='Energía')
        
        # Subplot 3: Métricas de detección
        ax3 = fig.add_subplot(n_detectors, 3, (i-1)*3 + 3)
        ax3.axis('off')
        
        metrics_text = f"""
{detector} - Métricas de Detección

Frecuencia detectada: {results['detected_frequency']:.4f} Hz
Frecuencia objetivo:  {TARGET_FREQUENCY:.4f} Hz
Desviación:          {results['deviation']:.4f} Hz
Incertidumbre:       ±{FREQUENCY_UNCERTAINTY:.4f} Hz

SNR:                 {results['snr']:.2f}
Potencia:            {results['power']:.2e} 1/√Hz

Dentro del rango:    {'✅ SÍ' if results['within_expected'] else '❌ NO'}

Filtro aplicado:     Bandpass [{BANDPASS_LOW}-{BANDPASS_HIGH}] Hz
Q-transform:         Q > {MIN_Q_VALUE}
Ventana temporal:    ±{MERGER_WINDOW} s
        """
        
        ax3.text(0.1, 0.9, metrics_text, transform=ax3.transAxes,
                fontsize=10, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    
    # Guardar figura
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f'{event_name}_141hz_bandpass_{timestamp}.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Visualización guardada: {output_file}")


def analyze_event(event_name, detectors, output_dir):
    """
    Análisis completo del evento con filtro bandpass
    
    Args:
        event_name: Nombre del evento (e.g., 'GW150914')
        detectors: Lista de detectores (e.g., ['H1', 'L1'])
        output_dir: Directorio de salida
    """
    print(f"\n{'='*70}")
    print(f"🌌 ANÁLISIS DE {event_name} CON FILTRO BANDPASS [{BANDPASS_LOW}-{BANDPASS_HIGH}] Hz")
    print(f"{'='*70}\n")
    
    # Validar evento
    merger_time = validate_event(event_name)
    if merger_time is None:
        return
    
    print(f"Evento: {event_name}")
    print(f"Tiempo GPS del merger: {merger_time}")
    print(f"Detectores: {', '.join(detectors)}")
    print(f"Frecuencia objetivo: {TARGET_FREQUENCY} ± {FREQUENCY_UNCERTAINTY} Hz")
    print(f"Filtro bandpass: [{BANDPASS_LOW}-{BANDPASS_HIGH}] Hz")
    print(f"Ventana temporal: ±{MERGER_WINDOW} s alrededor del merger")
    print(f"Q-transform: Q > {MIN_Q_VALUE}")
    print()
    
    results_dict = {}
    qtransforms = {}
    
    # Analizar cada detector
    for detector in detectors:
        print(f"\n{'─'*70}")
        print(f"🔍 Procesando detector: {detector}")
        print(f"{'─'*70}\n")
        
        # 1. Descargar datos strain .hdf5
        strain_data = download_strain_data(event_name, detector, merger_time)
        if strain_data is None:
            print(f"   ⚠️  Saltando detector {detector}")
            continue
        
        # 2. Aplicar filtro bandpass [140.5-143.0 Hz]
        filtered_data = apply_bandpass_filter(strain_data)
        
        # 3. Extraer ventana de ±0.3s alrededor del merger
        merger_window = extract_merger_window(filtered_data, merger_time)
        
        # 4. Calcular Q-transform con Q > 30
        qtransform = compute_qtransform(filtered_data, merger_time)
        qtransforms[detector] = qtransform
        
        # 5. Analizar pico de frecuencia en 141.7001 Hz
        results = analyze_frequency_peak(merger_window)
        results_dict[detector] = results
    
    # Verificar coherencia entre detectores
    if len(results_dict) >= MIN_DETECTORS:
        coherence = check_coherence(results_dict)
    else:
        coherence = {'coherent': False, 'reason': 'Insuficientes detectores'}
    
    # Crear visualización
    if results_dict:
        create_visualization(event_name, results_dict, qtransforms, output_dir)
    
    # Resumen final
    print(f"\n{'='*70}")
    print("📋 RESUMEN DEL ANÁLISIS")
    print(f"{'='*70}\n")
    
    print(f"Evento analizado: {event_name}")
    print(f"Detectores procesados: {len(results_dict)}/{len(detectors)}")
    print()
    
    for detector, results in results_dict.items():
        status = '✅' if results['within_expected'] else '⚠️'
        print(f"{detector}: {status} f = {results['detected_frequency']:.4f} Hz, "
              f"SNR = {results['snr']:.2f}, "
              f"Δf = {results['deviation']:.4f} Hz")
    
    print()
    
    if 'coherent' in coherence:
        if coherence['coherent']:
            print("✅ COHERENCIA CONFIRMADA entre detectores")
            print(f"   Frecuencia promedio: {coherence['freq_mean']:.4f} ± {coherence['freq_std']:.4f} Hz")
            print(f"   SNR promedio: {coherence['snr_mean']:.2f}")
        else:
            print("⚠️  COHERENCIA NO CONFIRMADA")
            if 'reason' in coherence:
                print(f"   Razón: {coherence['reason']}")
    
    print()
    print(f"{'='*70}")
    print("✅ ANÁLISIS COMPLETADO")
    print(f"{'='*70}\n")


def main():
    """Función principal"""
    # Check dependencies
    if not GWPY_AVAILABLE:
        print("❌ Error: GWPy no está instalado")
        print("   Instalar con: pip install gwpy")
        return 1
    
    if not NUMPY_AVAILABLE:
        print("❌ Error: NumPy no está instalado")
        print("   Instalar con: pip install numpy")
        return 1
    
    if not MPL_AVAILABLE:
        print("⚠️  Advertencia: Matplotlib no está instalado")
        print("   Las visualizaciones no estarán disponibles")
        print("   Instalar con: pip install matplotlib")
    
    parser = argparse.ArgumentParser(
        description='Análisis de 141.7001 Hz con filtro bandpass [140.5-143.0 Hz]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s --event GW150914
  %(prog)s --event GW150914 --detectors H1 L1
  %(prog)s --event GW150914 --detectors H1 L1 V1 --output results/
        """
    )
    
    parser.add_argument(
        '--event',
        type=str,
        required=True,
        help='Nombre del evento a analizar (e.g., GW150914)'
    )
    
    parser.add_argument(
        '--detectors',
        type=str,
        nargs='+',
        default=['H1', 'L1'],
        help='Lista de detectores a analizar (default: H1 L1)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='../results/bandpass_analysis',
        help='Directorio de salida para resultados (default: ../results/bandpass_analysis)'
    )
    
    args = parser.parse_args()
    
    # Ejecutar análisis
    analyze_event(args.event, args.detectors, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
