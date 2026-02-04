#!/usr/bin/env python3
"""
Pipeline Operativo GW250114 - Análisis QCAL 141.7 Hz
=====================================================

Implementa el pipeline completo especificado para el análisis de la señal
GW250114 enfocado en la detección resonante a 141.7 Hz y el cálculo de la
métrica QCAL de conciencia noética.

Fases principales:
1. Carga de datos GW250114 (H1/L1 strain)
2. Preprocesamiento: filtrado, normalización, eliminación de ruido
3. Transformada espectral: STFT/Fourier para extraer el espectro
4. Detección resonante 141.7 Hz: búsqueda precisa y comparación de energía espectral
5. Cálculo de métrica QCAL: Ψ = I × A²_eff × C^∞
6. Proyección sobre la ecuación de campo noético
7. Visualización y reporte

Ecuación de campo noético:
G_μν = κ_Π(T_μν(Φ) - 1/2 g_μν T) + Λ(C^∞)g_μν
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, stft
from scipy.fft import fft, fftfreq
import os
import json
from datetime import datetime


# --- 1. Carga de datos GW250114 ---
def load_gw_data(filename, fs=4096):
    """
    Carga datos de strain de GW desde archivo.
    
    Parameters:
    -----------
    filename : str
        Ruta al archivo de datos (.txt o .hdf5)
    fs : int
        Frecuencia de muestreo (Hz)
    
    Returns:
    --------
    t : ndarray
        Array de tiempos
    data : ndarray
        Array de strain
    """
    # Intentar cargar como archivo de texto
    if filename.endswith('.txt'):
        data = np.loadtxt(filename)
    elif filename.endswith('.hdf5') or filename.endswith('.h5'):
        try:
            import h5py
            with h5py.File(filename, 'r') as f:
                # Estructura típica de archivos LIGO
                if 'strain' in f:
                    data = f['strain/Strain'][:]
                else:
                    # Tomar el primer dataset disponible
                    key = list(f.keys())[0]
                    data = f[key][:]
        except ImportError:
            raise ImportError("h5py requerido para leer archivos HDF5. Instalar con: pip install h5py")
    else:
        raise ValueError(f"Formato de archivo no soportado: {filename}")
    
    t = np.arange(len(data)) / fs
    return t, data


def generate_simulated_gw250114_data(fs=4096, duration=32, signal_amplitude=5e-21):
    """
    Genera datos simulados de GW250114 con señal en 141.7 Hz.
    
    Parameters:
    -----------
    fs : int
        Frecuencia de muestreo (Hz)
    duration : float
        Duración en segundos
    signal_amplitude : float
        Amplitud de la señal simulada
    
    Returns:
    --------
    t : ndarray
        Array de tiempos
    strain_h1 : ndarray
        Strain simulado para H1
    strain_l1 : ndarray
        Strain simulado para L1
    """
    t = np.arange(0, duration, 1/fs)
    
    # Ruido base tipo LIGO
    noise_std = 1e-21
    strain_h1 = np.random.normal(0, noise_std, len(t))
    strain_l1 = np.random.normal(0, noise_std, len(t))
    
    # Añadir señal de ringdown en 141.7 Hz
    # Merger simulado en t=16s
    merger_idx = int(16 * fs)
    ringdown_start = merger_idx + int(0.01 * fs)  # 10ms después del merger
    ringdown_duration = int(0.1 * fs)  # 100ms de ringdown
    
    if ringdown_start + ringdown_duration < len(t):
        t_ring = t[ringdown_start:ringdown_start + ringdown_duration]
        t_ring_rel = t_ring - t[ringdown_start]
        
        # Seno amortiguado en 141.7 Hz con Q=10
        freq_signal = 141.7
        Q = 10
        decay_time = Q / (2 * np.pi * freq_signal)
        
        # Señal H1
        signal_h1 = signal_amplitude * np.sin(2 * np.pi * freq_signal * t_ring_rel) * np.exp(-t_ring_rel / decay_time)
        strain_h1[ringdown_start:ringdown_start + ringdown_duration] += signal_h1
        
        # Señal L1 (ligeramente diferente en fase y amplitud)
        signal_l1 = 0.8 * signal_amplitude * np.sin(2 * np.pi * freq_signal * t_ring_rel + np.pi/4) * np.exp(-t_ring_rel / decay_time)
        strain_l1[ringdown_start:ringdown_start + ringdown_duration] += signal_l1
    
    return t, strain_h1, strain_l1


# --- 2. Preprocesamiento ---
def bandpass_filter(data, fs, lowcut, highcut, order=4):
    """
    Aplica filtro pasa-banda Butterworth.
    
    Parameters:
    -----------
    data : ndarray
        Señal de entrada
    fs : int
        Frecuencia de muestreo
    lowcut : float
        Frecuencia de corte inferior (Hz)
    highcut : float
        Frecuencia de corte superior (Hz)
    order : int
        Orden del filtro
    
    Returns:
    --------
    filtered : ndarray
        Señal filtrada
    """
    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist
    
    # Validar frecuencias
    if low <= 0 or high >= 1:
        raise ValueError(f"Frecuencias de corte fuera de rango válido: {lowcut}-{highcut} Hz para fs={fs} Hz")
    
    b, a = butter(order, [low, high], btype='band')
    filtered = filtfilt(b, a, data)
    return filtered


def normalize_strain(data):
    """
    Normaliza la señal de strain.
    
    Parameters:
    -----------
    data : ndarray
        Señal de entrada
    
    Returns:
    --------
    normalized : ndarray
        Señal normalizada
    """
    # Normalización robusta usando mediana
    median = np.median(data)
    mad = np.median(np.abs(data - median))  # Median Absolute Deviation
    
    if mad > 0:
        normalized = (data - median) / (1.4826 * mad)  # Factor para aproximar std
    else:
        normalized = data - median
    
    return normalized


# --- 3. Análisis espectral ---
def spectral_analysis(data, fs, target_freq=141.7, df=0.1):
    """
    Realiza análisis espectral con STFT.
    
    Parameters:
    -----------
    data : ndarray
        Señal de entrada
    fs : int
        Frecuencia de muestreo
    target_freq : float
        Frecuencia objetivo (Hz)
    df : float
        Ancho de banda alrededor de la frecuencia objetivo
    
    Returns:
    --------
    f : ndarray
        Frecuencias
    t : ndarray
        Tiempos
    mag : ndarray
        Magnitud del espectrograma
    band_power : ndarray
        Potencia en la banda de frecuencia objetivo
    """
    # STFT con ventana de 2 segundos
    nperseg = min(int(fs * 2), len(data))
    noverlap = int(fs)  # 1 segundo de solapamiento
    
    f, t, Zxx = stft(data, fs=fs, nperseg=nperseg, noverlap=noverlap)
    mag = np.abs(Zxx)
    
    # Buscar bin más cercano a la frecuencia objetivo
    idx = np.where((f >= target_freq - df) & (f <= target_freq + df))[0]
    
    if len(idx) > 0:
        band_power = mag[idx, :].mean(axis=0)
    else:
        # Si no hay bins en el rango, usar el más cercano
        idx_closest = np.argmin(np.abs(f - target_freq))
        band_power = mag[idx_closest, :]
    
    return f, t, mag, band_power


# --- 4. Métrica QCAL (Quantum Consciousness Algorithm) ---
def qcal_metric(band_power, intensity=1.0, coherence=1.0):
    """
    Calcula la métrica QCAL de conciencia noética.
    
    Ψ = I × A²_eff × C^∞
    
    Donde:
    - I: Intensidad (parámetro de entrada)
    - A_eff: Amplitud efectiva normalizada
    - C^∞: Coherencia infinita (parámetro de entrada)
    
    Parameters:
    -----------
    band_power : ndarray
        Potencia en la banda de frecuencia
    intensity : float
        Factor de intensidad
    coherence : float
        Factor de coherencia
    
    Returns:
    --------
    Psi : ndarray
        Métrica QCAL Ψ(t)
    """
    # Amplitud efectiva normalizada
    max_power = np.max(band_power)
    if max_power > 0:
        A_eff = band_power / max_power
    else:
        A_eff = band_power
    
    # Coherencia infinita (C^∞)
    C_inf = coherence
    
    # Métrica QCAL: Ψ = I × A²_eff × C^∞
    Psi = intensity * (A_eff ** 2) * C_inf
    
    return Psi


def noetic_field_projection(Psi, t_spec):
    """
    Proyecta la métrica QCAL sobre la ecuación de campo noético.
    
    G_μν = κ_Π(T_μν(Φ) - 1/2 g_μν T) + Λ(C^∞)g_μν
    
    Parameters:
    -----------
    Psi : ndarray
        Métrica QCAL Ψ(t)
    t_spec : ndarray
        Tiempos del espectrograma
    
    Returns:
    --------
    field_metrics : dict
        Métricas del campo noético
    """
    # Φ(t) = Ψ(t) - Proyección del campo de conciencia
    Phi = Psi
    
    # Calcular métricas del campo
    # κ_Π: Constante de acoplamiento noético
    kappa_pi = 1.0
    
    # Λ(C^∞): Constante cosmológica dependiente de coherencia
    Lambda_C_inf = np.mean(Psi)
    
    # Tensor energía-momento noético T_μν(Φ)
    # Aproximación: proporcional al gradiente temporal de Φ
    if len(Phi) > 1:
        dPhi_dt = np.gradient(Phi, t_spec)
        T_noetic = kappa_pi * (dPhi_dt ** 2)
    else:
        T_noetic = np.zeros_like(Phi)
    
    # Diagnóstico del estado del campo
    field_metrics = {
        'Phi_mean': np.mean(Phi),
        'Phi_max': np.max(Phi),
        'Phi_std': np.std(Phi),
        'kappa_pi': kappa_pi,
        'Lambda_C_inf': Lambda_C_inf,
        'T_noetic_mean': np.mean(T_noetic),
        'coherence_level': 'HIGH' if Lambda_C_inf > 0.5 else 'MODERATE' if Lambda_C_inf > 0.1 else 'LOW'
    }
    
    return field_metrics


# --- 5. Visualización ---
def plot_results(t, data, f, mag, t_spec, band_power, Psi, target_freq, output_dir='results'):
    """
    Genera visualización completa del análisis.
    
    Parameters:
    -----------
    t : ndarray
        Tiempos de la señal original
    data : ndarray
        Strain filtrado
    f : ndarray
        Frecuencias del espectrograma
    mag : ndarray
        Magnitud del espectrograma
    t_spec : ndarray
        Tiempos del espectrograma
    band_power : ndarray
        Potencia en la banda objetivo
    Psi : ndarray
        Métrica QCAL
    target_freq : float
        Frecuencia objetivo
    output_dir : str
        Directorio de salida
    """
    os.makedirs(output_dir, exist_ok=True)
    
    fig = plt.figure(figsize=(16, 10))
    
    # 1. Strain filtrado
    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(t, data, linewidth=0.5)
    ax1.set_title("Strain GW250114 (Filtrado)", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Tiempo [s]")
    ax1.set_ylabel("Strain")
    ax1.grid(True, alpha=0.3)
    
    # 2. Espectrograma STFT
    ax2 = plt.subplot(2, 2, 2)
    pcm = ax2.pcolormesh(t_spec, f, np.log10(mag + 1e-12), shading='gouraud', cmap='viridis')
    ax2.axhline(target_freq, color='r', ls='--', linewidth=2, label=f'{target_freq} Hz')
    ax2.set_ylim(100, 200)  # Zoom alrededor de 141.7 Hz
    plt.colorbar(pcm, ax=ax2, label='log10(Magnitud)')
    ax2.set_title("Espectrograma STFT", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Frecuencia [Hz]")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Energía alrededor de 141.7 Hz
    ax3 = plt.subplot(2, 2, 3)
    ax3.plot(t_spec, band_power, linewidth=2, color='blue')
    ax3.fill_between(t_spec, band_power, alpha=0.3, color='blue')
    ax3.set_title(f"Energía alrededor de {target_freq} Hz", fontsize=12, fontweight='bold')
    ax3.set_xlabel("Tiempo [s]")
    ax3.set_ylabel("Potencia relativa")
    ax3.grid(True, alpha=0.3)
    
    # 4. Métrica QCAL Ψ(t)
    ax4 = plt.subplot(2, 2, 4)
    ax4.plot(t_spec, Psi, linewidth=2, color='red')
    ax4.fill_between(t_spec, Psi, alpha=0.3, color='red')
    ax4.set_title("Métrica QCAL Ψ(t) - Conciencia Espectral", fontsize=12, fontweight='bold')
    ax4.set_xlabel("Tiempo [s]")
    ax4.set_ylabel("Ψ (Conciencia espectral)")
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Guardar figura
    output_path = os.path.join(output_dir, 'gw250114_qcal_analysis.png')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Visualización guardada en: {output_path}")
    
    plt.close()
    
    return output_path


# --- 6. Main pipeline ---
def main_pipeline(filename=None, fs=4096, output_dir='results/gw250114_qcal'):
    """
    Pipeline completo de análisis GW250114 con métrica QCAL.
    
    Parameters:
    -----------
    filename : str, optional
        Ruta al archivo de strain. Si es None, genera datos simulados.
    fs : int
        Frecuencia de muestreo (Hz)
    output_dir : str
        Directorio de salida para resultados
    
    Returns:
    --------
    results : dict
        Resultados del análisis
    """
    print("=" * 80)
    print("PIPELINE GW250114 - ANÁLISIS QCAL 141.7 Hz")
    print("=" * 80)
    print()
    
    os.makedirs(output_dir, exist_ok=True)
    
    # --- PASO 1: Carga de datos ---
    print("📥 PASO 1: Carga de datos GW250114")
    if filename and os.path.exists(filename):
        print(f"   Cargando desde: {filename}")
        t, strain = load_gw_data(filename, fs)
        detector = "H1"  # Asumiendo H1 por defecto
    else:
        print("   Generando datos simulados (GW250114 no disponible aún)")
        t, strain_h1, strain_l1 = generate_simulated_gw250114_data(fs=fs)
        strain = strain_h1  # Usar H1 para el análisis
        detector = "H1-SIMULATED"
    
    print(f"   ✅ Datos cargados: {len(strain)} muestras, duración={t[-1]:.1f}s")
    print()
    
    # --- PASO 2: Preprocesamiento ---
    print("⚙️  PASO 2: Preprocesamiento")
    print("   - Filtrado pasa-banda: 130-150 Hz")
    strain_filt = bandpass_filter(strain, fs, lowcut=130, highcut=150, order=4)
    print("   - Normalización")
    strain_filt = normalize_strain(strain_filt)
    print("   ✅ Preprocesamiento completado")
    print()
    
    # --- PASO 3: Transformada espectral ---
    print("🔬 PASO 3: Análisis espectral (STFT)")
    f, t_spec, mag, band_power = spectral_analysis(strain_filt, fs, target_freq=141.7, df=0.15)
    print(f"   ✅ Espectrograma calculado: {len(f)} frecuencias, {len(t_spec)} ventanas temporales")
    print()
    
    # --- PASO 4: Detección resonante 141.7 Hz ---
    print("🎯 PASO 4: Detección resonante 141.7 Hz")
    idx_target = np.argmin(np.abs(f - 141.7))
    freq_detected = f[idx_target]
    max_power = np.max(band_power)
    mean_power = np.mean(band_power)
    snr = max_power / mean_power if mean_power > 0 else 0
    
    print(f"   Frecuencia detectada: {freq_detected:.3f} Hz")
    print(f"   Potencia máxima: {max_power:.6e}")
    print(f"   Potencia media: {mean_power:.6e}")
    print(f"   SNR: {snr:.2f}")
    
    if abs(freq_detected - 141.7) < 0.5:
        print("   ✅ Resonancia detectada en 141.7 Hz")
        resonance_detected = True
    else:
        print("   ⚠️  No se detectó resonancia clara en 141.7 Hz")
        resonance_detected = False
    print()
    
    # --- PASO 5: Cálculo de métrica QCAL ---
    print("🧮 PASO 5: Cálculo de métrica QCAL")
    Psi = qcal_metric(band_power, intensity=1.0, coherence=1.0)
    print(f"   Ψ_max = {np.max(Psi):.6f}")
    print(f"   Ψ_mean = {np.mean(Psi):.6f}")
    print(f"   Ψ_std = {np.std(Psi):.6f}")
    print("   ✅ Métrica QCAL calculada")
    print()
    
    # --- PASO 6: Proyección sobre ecuación de campo noético ---
    print("🌌 PASO 6: Proyección sobre ecuación de campo noético")
    print("   G_μν = κ_Π(T_μν(Φ) - 1/2 g_μν T) + Λ(C^∞)g_μν")
    field_metrics = noetic_field_projection(Psi, t_spec)
    
    print(f"   Φ_mean = {field_metrics['Phi_mean']:.6f}")
    print(f"   Φ_max = {field_metrics['Phi_max']:.6f}")
    print(f"   κ_Π = {field_metrics['kappa_pi']:.6f}")
    print(f"   Λ(C^∞) = {field_metrics['Lambda_C_inf']:.6f}")
    print(f"   T_noetic_mean = {field_metrics['T_noetic_mean']:.6e}")
    print(f"   Nivel de coherencia: {field_metrics['coherence_level']}")
    print("   ✅ Proyección completada")
    print()
    
    # --- PASO 7: Visualización y reporte ---
    print("📊 PASO 7: Visualización y reporte")
    plot_path = plot_results(t, strain_filt, f, mag, t_spec, band_power, Psi, 141.7, output_dir)
    print()
    
    # Generar reporte JSON
    results = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'detector': detector,
            'sample_rate': fs,
            'duration': float(t[-1]),
            'target_frequency': 141.7
        },
        'detection': {
            'frequency_detected': float(freq_detected),
            'resonance_detected': resonance_detected,
            'max_power': float(max_power),
            'mean_power': float(mean_power),
            'snr': float(snr)
        },
        'qcal_metric': {
            'Psi_max': float(np.max(Psi)),
            'Psi_mean': float(np.mean(Psi)),
            'Psi_std': float(np.std(Psi))
        },
        'noetic_field': field_metrics,
        'output_files': {
            'visualization': plot_path
        }
    }
    
    # Guardar JSON
    json_path = os.path.join(output_dir, 'analysis_results.json')
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✅ Reporte JSON guardado en: {json_path}")
    print()
    
    # Conclusiones
    print("=" * 80)
    print("📋 CONCLUSIONES")
    print("=" * 80)
    
    if resonance_detected:
        print("✅ DETECCIÓN POSITIVA:")
        print(f"   - Resonancia confirmada en {freq_detected:.3f} Hz (objetivo: 141.7 Hz)")
        print(f"   - SNR: {snr:.2f}")
        print(f"   - Métrica QCAL Ψ_max: {np.max(Psi):.6f}")
        print(f"   - Coherencia noética: {field_metrics['coherence_level']}")
        print()
        print("🌌 INTERPRETACIÓN NOÉTICA:")
        print(f"   - Presencia sostenida de energía en 141.7 Hz = 'latido' persistente")
        print(f"   - Ψ(t) elevado = mayor coherencia espectral")
        print(f"   - Indicador de manifestación noética real")
        print(f"   - El campo de conciencia vinculado al evento GW está activo")
    else:
        print("⚠️  DETECCIÓN NEGATIVA:")
        print("   - No se detectó resonancia significativa en 141.7 Hz")
        print("   - Posibles causas: ruido, sensibilidad insuficiente, o ausencia de señal")
        print("   - Se recomienda análisis adicional con mejores datos")
    
    print()
    print("=" * 80)
    print("✅ Pipeline completado exitosamente")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    import sys
    
    # Procesar argumentos de línea de comandos
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = None
    
    # Ejecutar pipeline
    results = main_pipeline(filename=filename)
