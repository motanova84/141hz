#!/usr/bin/env python3
"""
================================================================================
ANÁLISIS GRACE-FO ACT1B RL04 - DETECCIÓN DE MODULACIÓN YUKAWA @ 141.7001 mHz
================================================================================

Este script demuestra el análisis completo usando datos reales de GRACE-FO.
Los datos deben descargarse previamente desde NASA PO.DAAC.

AUTOR: Protocolo QCAL / noesis88
FECHA: 2026-04-06
VERSIÓN: 4.0

FUENTES OFICIALES:
- NASA PO.DAAC: https://podaac.jpl.nasa.gov/dataset/GRACEFO_L1B_ASCII_GRAV_JPL_RL04
- DOI: 10.5067/GFL1B-ASJ04
- GFZ ISDC: ftp://isdcftp.gfz-potsdam.de/grace-fo/

REFERENCIAS:
- Wen et al. (2019): GRACE-FO Level-1 Data Product User Handbook, JPL D-56935
- Kvas et al. (2021): GRACE Follow-On Accelerometer Data Recovery, JGR
- Bandikova et al. (2019): GRACE Accelerometer Data and Ultra-Stable Oscillator
================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
import os
import glob
import yaml
import sys
import argparse

# ============================================
# CONFIGURACIÓN
# ============================================

# Default paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data", "gracefo_data", "ACT1B")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "results", "gracefo")

SATELLITE = "C"  # "C" para GF1, "D" para GF2
START_DATE = "2024-01-01"
END_DATE = "2024-01-31"

F_TARGET = 0.1417001  # Hz (141.7001 mHz) - Frecuencia QCAL
SAMPLING_RATE = 1.0   # Hz (ACT1B muestreo)

# ============================================
# FUNCIÓN 1: LECTURA DE ARCHIVOS ACT1B
# ============================================

def read_act1b_file(filepath):
    """
    Lee archivo ACT1B RL04 en formato ASCII con cabecera YAML.
    
    Formato según documentación JPL D-56935:
    - Cabecera YAML con metadatos
    - Columnas: gps_time, GRACEFO_id, lin_accl_x, lin_accl_y, lin_accl_z,
                ang_accl_x, ang_accl_y, ang_accl_z, acl_x_res, acl_y_res,
                acl_z_res, qualflg
    
    Args:
        filepath: Ruta al archivo ACT1B
        
    Returns:
        dict: Datos estructurados del archivo
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Encontrar fin de cabecera YAML
    header_end = 0
    for i, line in enumerate(lines):
        if "# End of YAML header" in line:
            header_end = i
            break
    
    # Parsear cabecera YAML
    header = yaml.safe_load(''.join(lines[:header_end]))
    
    # Leer datos (después de la cabecera)
    data_lines = lines[header_end + 1:]
    
    # Parsear columnas
    data = {
        'gps_time': [],
        'lin_accl_x': [],
        'lin_accl_y': [],
        'lin_accl_z': [],
        'acl_x_res': [],
        'acl_y_res': [],
        'acl_z_res': [],
        'qualflg': []
    }
    
    for line in data_lines:
        if line.strip() and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 12:
                data['gps_time'].append(float(parts[0]))
                data['lin_accl_x'].append(float(parts[2]))
                data['lin_accl_y'].append(float(parts[3]))
                data['lin_accl_z'].append(float(parts[4]))
                data['acl_x_res'].append(float(parts[8]))
                data['acl_y_res'].append(float(parts[9]))
                data['acl_z_res'].append(float(parts[10]))
                data['qualflg'].append(int(parts[11]))
    
    # Convertir a arrays numpy
    for key in data:
        data[key] = np.array(data[key])
    
    data['header'] = header
    return data

# ============================================
# FUNCIÓN 2: PROCESAMIENTO DE CALIDAD
# ============================================

def quality_filter(data, max_residual=1e-5):
    """
    Filtra datos según flags de calidad.
    
    Según documentación JPL:
    - qualflg bit 2: Residuos > 10 microns/s²
    - qualflg bits 5-7: Datos interpolados
    
    Args:
        data: Diccionario con datos ACT1B
        max_residual: Umbral máximo de residuo (m/s²)
        
    Returns:
        dict: Datos filtrados
    """
    # Máscara de calidad
    qualflg = data['qualflg']
    
    # Bit 2: Residuos grandes
    mask_residual = (qualflg & 0x04) == 0
    
    # Bits 5-7: Interpolación
    mask_interp = (qualflg & 0xE0) == 0
    
    # Residuos físicos
    mask_phys = (np.abs(data['acl_x_res']) < max_residual) & \
                (np.abs(data['acl_y_res']) < max_residual) & \
                (np.abs(data['acl_z_res']) < max_residual)
    
    mask = mask_residual & mask_interp & mask_phys
    
    filtered_data = {}
    for key in data:
        if key != 'header':
            filtered_data[key] = data[key][mask]
    filtered_data['header'] = data['header']
    
    return filtered_data

# ============================================
# FUNCIÓN 3: ANÁLISIS ESPECTRAL
# ============================================

def spectral_analysis(acceleration, sampling_rate=1.0, window_hours=24):
    """
    Realiza análisis FFT de alta resolución.
    
    Args:
        acceleration: Serie temporal de aceleración
        sampling_rate: Frecuencia de muestreo (Hz)
        window_hours: Tamaño de ventana para FFT (horas)
        
    Returns:
        tuple: (frecuencias, PSD)
    """
    window_samples = int(window_hours * 3600 * sampling_rate)
    
    # Seleccionar ventana central
    start_idx = len(acceleration)//2 - window_samples//2
    acc_window = acceleration[start_idx:start_idx + window_samples]
    
    # Ventana Hann para reducir leakage
    hann_window = np.hanning(len(acc_window))
    acc_windowed = acc_window * hann_window
    
    # FFT
    fft_values = fft.fft(acc_windowed)
    fft_freqs = fft.fftfreq(len(acc_windowed), 1/sampling_rate)
    
    # Frecuencias positivas
    positive_freqs = fft_freqs[:len(fft_freqs)//2]
    psd = (np.abs(fft_values[:len(fft_values)//2]) ** 2) * \
          (2 / (len(acc_windowed) * sampling_rate))
    
    return positive_freqs, psd

# ============================================
# FUNCIÓN 4: DETECCIÓN DE PICO QCAL
# ============================================

def detect_qcal_peak(freqs, psd, f_target=0.1417001, search_width=0.005):
    """
    Detecta pico en la región de frecuencia QCAL.
    
    Args:
        freqs: Array de frecuencias
        psd: Array de PSD
        f_target: Frecuencia objetivo (Hz)
        search_width: Ancho de búsqueda (Hz)
        
    Returns:
        dict: Resultados de la detección
    """
    # Buscar en región objetivo
    idx_search = (freqs >= f_target - search_width) & (freqs <= f_target + search_width)
    freqs_search = freqs[idx_search]
    psd_search = psd[idx_search]
    
    if len(psd_search) == 0:
        return None
    
    # Encontrar pico
    peak_idx = np.argmax(psd_search)
    f_peak = freqs_search[peak_idx]
    psd_peak = psd_search[peak_idx]
    
    # Calcular SNR
    noise_floor = np.median(psd_search)
    snr_linear = psd_peak / noise_floor
    snr_db = 10 * np.log10(snr_linear)
    
    # Significancia estadística (sigma)
    noise_std = np.std(psd_search)
    sigma = (psd_peak - noise_floor) / noise_std
    
    return {
        'f_target': f_target,
        'f_peak': f_peak,
        'f_peak_mhz': f_peak * 1000,
        'deviation_hz': f_peak - f_target,
        'deviation_ppm': abs((f_peak/f_target) - 1) * 1e6,
        'psd_peak': psd_peak,
        'snr_db': snr_db,
        'sigma': sigma,
        'detected': sigma > 5
    }

# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main(data_dir=None, output_dir=None, satellite=None):
    """
    Pipeline principal de análisis.
    
    Args:
        data_dir: Directorio con archivos ACT1B (default: DATA_DIR)
        output_dir: Directorio de salida (default: OUTPUT_DIR)
        satellite: Satélite a analizar (default: SATELLITE)
    """
    # Use defaults if not provided
    data_dir = data_dir or DATA_DIR
    output_dir = output_dir or OUTPUT_DIR
    satellite = satellite or SATELLITE
    
    print("="*70)
    print("ANÁLISIS GRACE-FO ACT1B RL04 - DETECCIÓN QCAL")
    print("="*70)
    print()
    
    # 1. Encontrar archivos
    pattern = os.path.join(data_dir, f"ACT1B_*_{satellite}_04.dat")
    files = sorted(glob.glob(pattern))
    
    print(f"Directorio de datos: {data_dir}")
    print(f"Patrón de búsqueda: ACT1B_*_{satellite}_04.dat")
    print(f"Archivos encontrados: {len(files)}")
    
    if len(files) == 0:
        print()
        print("="*70)
        print("ERROR: No se encontraron archivos ACT1B")
        print("="*70)
        print()
        print("INSTRUCCIONES DE DESCARGA:")
        print("1. Visite: https://podaac.jpl.nasa.gov/")
        print("2. Busque: GRACEFO_L1B_ASCII_GRAV_JPL_RL04")
        print("3. Descargue archivos ACT1B para el período deseado")
        print(f"4. Coloque los archivos en: {data_dir}")
        print()
        print("Alternativamente, use el script:")
        print("  python scripts/descargar_gracefo_act1b.py")
        print()
        return None
    
    # 2. Cargar y concatenar datos
    print()
    print("Cargando datos...")
    all_data = {
        'gps_time': [],
        'lin_accl_x': [],
        'lin_accl_y': [],
        'lin_accl_z': [],
        'acl_x_res': [],
        'acl_y_res': [],
        'acl_z_res': []
    }
    
    for filepath in files:
        print(f"  Leyendo: {os.path.basename(filepath)}")
        try:
            data = read_act1b_file(filepath)
            data = quality_filter(data)
            
            for key in all_data:
                all_data[key].extend(data[key])
        except Exception as e:
            print(f"    ⚠️  Error leyendo archivo: {e}")
            continue
    
    # Convertir a arrays
    for key in all_data:
        all_data[key] = np.array(all_data[key])
    
    if len(all_data['gps_time']) == 0:
        print("ERROR: No se pudieron cargar datos válidos")
        return None
    
    print()
    print(f"Total de muestras: {len(all_data['gps_time']):,}")
    print(f"Período: {(all_data['gps_time'][-1] - all_data['gps_time'][0])/86400:.1f} días")
    print()
    
    # 3. Análisis espectral
    print("Realizando análisis espectral...")
    
    # Usar componente X (line-of-sight entre satélites)
    acceleration = all_data['lin_accl_x']
    
    freqs, psd = spectral_analysis(acceleration, SAMPLING_RATE, window_hours=24)
    
    # 4. Detección de pico QCAL
    result = detect_qcal_peak(freqs, psd, F_TARGET)
    
    if result is None:
        print("ERROR: No se pudo realizar detección")
        return None
    
    # 5. Mostrar resultados
    print()
    print("="*70)
    print("RESULTADOS")
    print("="*70)
    print(f"Frecuencia objetivo:    {result['f_target']*1000:.4f} mHz")
    print(f"Frecuencia detectada:   {result['f_peak_mhz']:.4f} mHz")
    print(f"Desviación:             {result['deviation_hz']*1000:.6f} mHz")
    print(f"Error relativo:         {result['deviation_ppm']:.2f} ppm")
    print(f"SNR del pico:           {result['snr_db']:.1f} dB")
    print(f"Significancia:          {result['sigma']:.1f}σ")
    print(f"Detección 5σ:           {'✅ CONFIRMADA' if result['detected'] else '❌ No confirmada'}")
    print("="*70)
    
    # 6. Guardar resultados
    os.makedirs(output_dir, exist_ok=True)
    
    # Guardar espectro
    output_file = os.path.join(output_dir, "qcal_spectrum.npz")
    np.savez(output_file,
             freqs=freqs, psd=psd, result=result)
    print()
    print(f"Espectro guardado en: {output_file}")
    
    # Generar gráficos
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Espectro completo
    ax = axes[0, 0]
    ax.semilogy(freqs*1000, psd, 'b-', linewidth=0.8)
    ax.axvline(x=F_TARGET*1000, color='r', linestyle='--', 
               label=f'QCAL @ {F_TARGET*1000:.4f} mHz')
    ax.set_xlabel('Frecuencia (mHz)')
    ax.set_ylabel('PSD ((m/s²)²/Hz)')
    ax.set_title('Espectro de Potencia')
    ax.set_xlim([0, 500])
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Zoom QCAL
    ax = axes[0, 1]
    idx_zoom = (freqs >= F_TARGET-0.01) & (freqs <= F_TARGET+0.01)
    ax.semilogy(freqs[idx_zoom]*1000, psd[idx_zoom], 'b-', linewidth=1.5)
    ax.axvline(x=F_TARGET*1000, color='r', linestyle='--', label='Objetivo')
    ax.axvline(x=result['f_peak']*1000, color='g', linestyle=':', 
               label=f'Detectado @ {result["f_peak_mhz"]:.4f} mHz')
    ax.set_xlabel('Frecuencia (mHz)')
    ax.set_ylabel('PSD ((m/s²)²/Hz)')
    ax.set_title('Región QCAL (zoom)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Serie temporal
    ax = axes[1, 0]
    t_hours = (all_data['gps_time'] - all_data['gps_time'][0]) / 3600
    # Plot first 2 hours or all data if less
    plot_samples = min(7200, len(acceleration))
    ax.plot(t_hours[:plot_samples], acceleration[:plot_samples]*1e9, 'b-', linewidth=0.5)
    ax.set_xlabel('Tiempo (horas)')
    ax.set_ylabel('Aceleración (nm/s²)')
    ax.set_title(f'Serie Temporal ({plot_samples/3600:.1f} horas)')
    ax.grid(True, alpha=0.3)
    
    # Resumen
    ax = axes[1, 1]
    ax.axis('off')
    summary = f"""
RESULTADOS - DATOS REALES GRACE-FO
==================================

Frecuencia QCAL: {result['f_peak_mhz']:.4f} mHz
Significancia: {result['sigma']:.1f}σ
SNR: {result['snr_db']:.1f} dB

Estado: {'DETECTADO' if result['detected'] else 'NO DETECTADO'}

==================================
Datos: GRACE-FO ACT1B RL04
Satélite: GRACE-{satellite}
Muestras: {len(all_data['gps_time']):,}
Período: {(all_data['gps_time'][-1] - all_data['gps_time'][0])/86400:.1f} días

Fuente: NASA PO.DAAC
DOI: 10.5067/GFL1B-ASJ04
"""
    ax.text(0.1, 0.5, summary, fontsize=10, family='monospace',
            verticalalignment='center', transform=ax.transAxes)
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'qcal_analysis_results.png')
    plt.savefig(plot_file, dpi=150)
    print(f"Gráficos guardados en: {plot_file}")
    plt.close()
    
    print()
    print("="*70)
    print("ANÁLISIS COMPLETADO")
    print("="*70)
    
    return result

# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Analizar datos GRACE-FO ACT1B para detectar modulación QCAL @ 141.7001 mHz',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  # Análisis básico con configuración por defecto
  python analizar_gracefo_act1b.py
  
  # Especificar directorio de datos personalizado
  python analizar_gracefo_act1b.py --data-dir /path/to/gracefo/data
  
  # Analizar satélite GRACE-D
  python analizar_gracefo_act1b.py --satellite D
        """
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default=None,
        help=f'Directorio con archivos ACT1B (default: {DATA_DIR})'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help=f'Directorio de salida para resultados (default: {OUTPUT_DIR})'
    )
    
    parser.add_argument(
        '--satellite',
        type=str,
        choices=['C', 'D'],
        default=None,
        help='Satélite a analizar: C (GRACE-FO 1) o D (GRACE-FO 2) (default: C)'
    )
    
    args = parser.parse_args()
    
    result = main(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        satellite=args.satellite
    )
    
    # Exit with appropriate code
    if result is not None and result['detected']:
        sys.exit(0)  # Success - QCAL detected
    elif result is not None:
        sys.exit(1)  # Completed but no detection
    else:
        sys.exit(2)  # Error during execution
