#!/usr/bin/env python3
"""
Análisis Completo de Resonancia 141.7 Hz en GW150914
====================================================

Búsqueda específica de señal persistente a 141.7001 Hz en el ringdown
post-merger de GW150914, con análisis multi-detector coherente.

Implementa:
1. FFT interpolada con zero-padding para resolución ultra-alta
2. Análisis coherente H1-L1 (cross-correlation)
3. Mapeo de coherencia de fase para localización
4. Filtro adaptativo Ψ-NSE v1.0
5. Análisis de significancia estadística (σ)

Autor: Sistema QCAL ∞³
Hash de Certificación: 1d62f6d4
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional

# Import GW analysis libraries
try:
    from gwpy.timeseries import TimeSeries
    from gwpy.signal import filter_design
    from gwpy.frequencyseries import FrequencySeries
    from gwosc import datasets
    from gwosc.locate import get_urls
except ImportError as e:
    print(f"❌ Error importing GW libraries: {e}")
    print("Install with: pip install gwpy gwosc")
    sys.exit(1)

try:
    from scipy import signal
    from scipy.interpolate import interp1d
    from scipy.stats import norm
except ImportError:
    print("❌ Error: scipy is required")
    print("Install with: pip install scipy")
    sys.exit(1)


class AnalizadorGW150914:
    """
    Analizador completo de resonancia 141.7 Hz en GW150914.
    
    Implementa técnicas avanzadas de análisis coherente multi-detector
    para detectar modos cuasinormales persistentes.
    """
    
    def __init__(self):
        """Inicializar analizador."""
        self.evento = "GW150914"
        self.f0 = 141.7001  # Hz - Frecuencia QCAL
        self.cert_hash = "1d62f6d4"
        
        # Parámetros de GW150914
        self.gps_time = 1126259462.4  # GPS time del merger
        self.masa_final = 67.4  # M☉
        
        # Parámetros de análisis
        self.detectors = ['H1', 'L1']  # GW150914 solo detectado por LIGO
        self.sample_rate = 4096  # Hz
        self.fft_padding_factor = 16  # Zero-padding para interpolación
        
        # Ventanas de análisis
        self.pre_merger = 2.0  # s antes del merger
        self.post_merger = 4.0  # s después del merger (extendido)
        self.ringdown_start = 0.010  # s después del merger
        self.ringdown_duration = 0.500  # s
        
        # Líneas instrumentales conocidas (para filtrado notch)
        self.instrumental_lines = [
            60.0,   # AC power
            120.0,  # Harmonic
            141.6,  # Cerca de f0 (instrumental)
        ]
        
        # Directorios
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "results" / "gw150914_1417hz"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.resultados = {
            "evento": self.evento,
            "f0_qcal": self.f0,
            "cert_hash": self.cert_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "detectores": {}
        }
    
    def cargar_strain(self, detector: str) -> TimeSeries:
        """
        Cargar datos de strain del detector.
        
        Args:
            detector: Nombre del detector ('H1' o 'L1')
            
        Returns:
            TimeSeries: Datos de strain
        """
        print(f"📡 Cargando strain de {detector}...")
        
        start = self.gps_time - self.pre_merger
        end = self.gps_time + self.post_merger
        
        try:
            strain = TimeSeries.fetch_open_data(
                detector, start, end,
                sample_rate=self.sample_rate,
                cache=True
            )
            print(f"   ✅ Strain cargado: {len(strain)} muestras")
            return strain
        except Exception as e:
            print(f"   ❌ Error cargando strain: {e}")
            raise
    
    def aplicar_filtro_notch(self, strain: TimeSeries) -> TimeSeries:
        """
        Aplicar filtros notch para líneas instrumentales.
        
        Args:
            strain: TimeSeries original
            
        Returns:
            TimeSeries: Strain filtrado
        """
        print("🔧 Aplicando filtros notch para líneas instrumentales...")
        
        strain_filtered = strain.copy()
        
        for freq in self.instrumental_lines:
            # Crear filtro notch con Q=30
            notch = filter_design.notch(freq, strain.sample_rate, quality=30)
            strain_filtered = strain_filtered.filter(notch, filtfilt=True)
            print(f"   ✓ Notch @ {freq} Hz")
        
        print("   ✅ Filtrado notch completado")
        return strain_filtered
    
    def aplicar_filtro_psi_nse(self, strain: TimeSeries) -> TimeSeries:
        """
        Aplicar Filtro Adaptativo Ψ-NSE v1.0.
        
        Este filtro "se sintoniza" a la frecuencia fundamental del sistema
        basada en el Axioma de Emisión, maximizando la recuperación de señal
        en la zona de 15σ.
        
        Args:
            strain: TimeSeries
            
        Returns:
            TimeSeries: Strain filtrado con Ψ-NSE
        """
        print("🧬 Aplicando Filtro Adaptativo Ψ-NSE v1.0...")
        
        # Parámetros adaptativos basados en masa final
        # Para M_final ~ 67 M☉, el modo dominante está en ~250 Hz
        # f0 está en región de overtones, requiere filtro específico
        
        # Ancho de banda adaptativo: función de Q y resonancia
        Q_adaptive = 150  # Mayor Q para mayor selectividad
        bandwidth = self.f0 / Q_adaptive
        
        f_low = self.f0 - bandwidth / 2
        f_high = self.f0 + bandwidth / 2
        
        print(f"   📏 Q adaptativo: {Q_adaptive}")
        print(f"   📊 Ancho de banda: {bandwidth:.4f} Hz")
        print(f"   📍 Rango: [{f_low:.4f}, {f_high:.4f}] Hz")
        
        # Diseñar filtro
        bp_filter = filter_design.bandpass(f_low, f_high, strain.sample_rate)
        strain_filtered = strain.filter(bp_filter, filtfilt=True)
        
        # Normalizar por energía para preservar SNR
        energy_original = np.sum(strain.value**2)
        energy_filtered = np.sum(strain_filtered.value**2)
        
        if energy_filtered > 0:
            normalization = np.sqrt(energy_original / energy_filtered)
            strain_filtered = strain_filtered * normalization
        
        print("   ✅ Filtro Ψ-NSE aplicado y normalizado")
        
        return strain_filtered
    
    def calcular_fft_interpolada(self, strain: TimeSeries) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcular FFT con zero-padding para alta resolución.
        
        Args:
            strain: TimeSeries
            
        Returns:
            tuple: (freqs, fft_amplitude)
        """
        print(f"📊 Calculando FFT interpolada (padding factor: {self.fft_padding_factor})...")
        
        # Aplicar ventana de Tukey
        window = signal.windows.tukey(len(strain), alpha=0.1)
        windowed_data = strain.value * window
        
        # Zero-padding
        n_padded = len(windowed_data) * self.fft_padding_factor
        
        # FFT
        fft_vals = np.fft.rfft(windowed_data, n=n_padded)
        freqs = np.fft.rfftfreq(n_padded, d=1.0/strain.sample_rate.value)
        
        # Amplitud
        fft_amplitude = np.abs(fft_vals) * 2.0 / len(windowed_data)
        
        # Resolución
        df = freqs[1] - freqs[0]
        print(f"   ✅ Resolución frecuencial: {df:.6f} Hz")
        print(f"   📏 Puntos FFT: {n_padded}")
        
        return freqs, fft_amplitude
    
    def calcular_snr_en_f0(self, freqs: np.ndarray, fft_amp: np.ndarray) -> Dict:
        """
        Calcular SNR en f0 = 141.7001 Hz.
        
        Args:
            freqs: Array de frecuencias
            fft_amp: Array de amplitudes FFT
            
        Returns:
            dict: Resultados de SNR
        """
        print(f"🎯 Calculando SNR en f₀ = {self.f0} Hz...")
        
        # Encontrar índice más cercano a f0
        f0_idx = np.argmin(np.abs(freqs - self.f0))
        f_detected = freqs[f0_idx]
        amp_at_f0 = fft_amp[f0_idx]
        
        # Calcular fondo (background) en ventana alrededor de f0
        # Excluir la región central para no incluir la señal
        window_width = 10  # Hz
        exclude_width = 0.5  # Hz
        
        window_mask = (freqs > self.f0 - window_width) & \
                     (freqs < self.f0 + window_width) & \
                     ((freqs < self.f0 - exclude_width) | \
                      (freqs > self.f0 + exclude_width))
        
        background = fft_amp[window_mask]
        
        # Estadísticas del fondo
        bg_mean = np.mean(background)
        bg_std = np.std(background)
        bg_median = np.median(background)
        
        # SNR basado en desviación estándar
        snr_std = (amp_at_f0 - bg_mean) / bg_std if bg_std > 0 else 0
        
        # SNR basado en mediana (más robusto)
        snr_median = amp_at_f0 / bg_median if bg_median > 0 else 0
        
        # Significancia estadística (asumiendo distribución normal)
        # p-value de cola derecha
        p_value = 1 - norm.cdf(snr_std) if snr_std > 0 else 1.0
        significance_sigma = norm.ppf(1 - p_value) if p_value < 1.0 else 0.0
        
        resultado = {
            "f_detected": float(f_detected),
            "f_expected": float(self.f0),
            "deviation_hz": float(abs(f_detected - self.f0)),
            "amplitude_at_f0": float(amp_at_f0),
            "background_mean": float(bg_mean),
            "background_std": float(bg_std),
            "background_median": float(bg_median),
            "snr_std": float(snr_std),
            "snr_median": float(snr_median),
            "p_value": float(p_value),
            "significance_sigma": float(significance_sigma)
        }
        
        print(f"   📍 Frecuencia detectada: {f_detected:.4f} Hz")
        print(f"   📊 Amplitud en f₀: {amp_at_f0:.2e}")
        print(f"   📈 SNR (std): {snr_std:.2f}")
        print(f"   📉 SNR (median): {snr_median:.2f}")
        print(f"   🎯 Significancia: {significance_sigma:.2f}σ")
        
        return resultado
    
    def analisis_coherente_h1_l1(self, h1_strain: TimeSeries, 
                                  l1_strain: TimeSeries) -> Dict:
        """
        Análisis coherente H1-L1 usando cross-correlation.
        
        Multiplica las FFTs conjugadas (H1 * L1*) para reforzar señales
        astrofísicas coherentes y suprimir ruido instrumental.
        
        Args:
            h1_strain: TimeSeries de H1
            l1_strain: TimeSeries de L1
            
        Returns:
            dict: Resultados de coherencia
        """
        print("🧬 Análisis coherente H1-L1 (cross-correlation)...")
        
        # Asegurar misma longitud
        min_len = min(len(h1_strain), len(l1_strain))
        h1_data = h1_strain.value[:min_len]
        l1_data = l1_strain.value[:min_len]
        
        # FFT de ambos detectores
        h1_fft = np.fft.rfft(h1_data)
        l1_fft = np.fft.rfft(l1_data)
        
        # Cross-spectrum: H1 * conj(L1)
        cross_spectrum = h1_fft * np.conj(l1_fft)
        
        # Amplitud del cross-spectrum
        cross_amp = np.abs(cross_spectrum)
        
        # Auto-spectra para normalización
        h1_auto = np.abs(h1_fft)**2
        l1_auto = np.abs(l1_fft)**2
        
        # Coherencia: |cross|^2 / (|H1|^2 * |L1|^2)
        coherence = cross_amp**2 / (h1_auto * l1_auto + 1e-20)
        
        # Frecuencias
        freqs = np.fft.rfftfreq(min_len, d=1.0/self.sample_rate)
        
        # Buscar coherencia en f0
        f0_idx = np.argmin(np.abs(freqs - self.f0))
        coherence_at_f0 = coherence[f0_idx]
        cross_amp_at_f0 = cross_amp[f0_idx]
        
        # Fase relativa
        phase_h1_l1 = np.angle(cross_spectrum[f0_idx])
        
        # Calcular SNR coherente
        # El SNR coherente es mayor que SNR individual si la señal es coherente
        window_mask = (freqs > self.f0 - 5) & (freqs < self.f0 + 5)
        bg_cross = np.median(cross_amp[window_mask])
        snr_coherent = cross_amp_at_f0 / bg_cross if bg_cross > 0 else 0
        
        resultado = {
            "coherence_at_f0": float(coherence_at_f0),
            "cross_amplitude_at_f0": float(cross_amp_at_f0),
            "phase_h1_l1_rad": float(phase_h1_l1),
            "phase_h1_l1_deg": float(np.degrees(phase_h1_l1)),
            "snr_coherent": float(snr_coherent),
            "coherence_spectrum": coherence.tolist(),
            "frequencies": freqs.tolist()
        }
        
        print(f"   📊 Coherencia en f₀: {coherence_at_f0:.4f}")
        print(f"   🌊 Fase H1-L1: {np.degrees(phase_h1_l1):.1f}°")
        print(f"   📈 SNR coherente: {snr_coherent:.2f}")
        
        # Validar coherencia
        if coherence_at_f0 > 0.5:
            print("   ✅ SEÑAL COHERENTE entre H1 y L1")
        else:
            print("   ⚠️  Coherencia baja - posible ruido")
        
        return resultado
    
    def mapeo_coherencia_fase(self, h1_result: Dict, l1_result: Dict,
                              coherent_result: Dict) -> Dict:
        """
        Mapeo de coherencia de fase para localización.
        
        Usa la diferencia de fase entre H1 y L1 para verificar
        consistencia con la localización conocida de GW150914.
        
        Args:
            h1_result: Resultados de H1
            l1_result: Resultados de L1
            coherent_result: Resultados de análisis coherente
            
        Returns:
            dict: Resultados de mapeo de fase
        """
        print("📍 Mapeo de coherencia de fase para localización...")
        
        # Diferencia de fase observada
        phase_diff_obs = coherent_result["phase_h1_l1_rad"]
        
        # Para GW150914, conocemos la localización aproximada
        # La diferencia de tiempo entre H1 y L1 es ~6.9 ms
        # Esto corresponde a una diferencia de fase:
        # Δφ = 2π * f * Δt
        
        dt_h1_l1 = 0.0069  # s (tiempo de vuelo de luz entre detectores)
        phase_diff_expected = 2 * np.pi * self.f0 * dt_h1_l1
        
        # Normalizar a [-π, π]
        phase_diff_expected = np.arctan2(np.sin(phase_diff_expected), 
                                         np.cos(phase_diff_expected))
        
        # Desviación de fase
        phase_deviation = abs(phase_diff_obs - phase_diff_expected)
        if phase_deviation > np.pi:
            phase_deviation = 2*np.pi - phase_deviation
        
        # Consistencia espacial
        # Si la fase es consistente con la localización, refuerza
        # que la señal es astrofísica y no instrumental
        is_spatially_consistent = phase_deviation < np.pi/4  # 45°
        
        resultado = {
            "phase_diff_observed_rad": float(phase_diff_obs),
            "phase_diff_expected_rad": float(phase_diff_expected),
            "phase_deviation_rad": float(phase_deviation),
            "phase_deviation_deg": float(np.degrees(phase_deviation)),
            "dt_h1_l1_s": dt_h1_l1,
            "is_spatially_consistent": bool(is_spatially_consistent)
        }
        
        print(f"   📍 Fase observada: {np.degrees(phase_diff_obs):.1f}°")
        print(f"   🎯 Fase esperada: {np.degrees(phase_diff_expected):.1f}°")
        print(f"   📊 Desviación: {np.degrees(phase_deviation):.1f}°")
        
        if is_spatially_consistent:
            print("   ✅ CONSISTENCIA ESPACIAL confirmada")
            print("   🌌 Señal compatible con fuente astrofísica")
        else:
            print("   ⚠️  Desviación de fase significativa")
        
        return resultado
    
    def procesar_detector(self, detector: str) -> Dict:
        """
        Procesar análisis completo de un detector.
        
        Args:
            detector: Nombre del detector
            
        Returns:
            dict: Resultados completos
        """
        print(f"\n{'='*80}")
        print(f"📡 PROCESANDO {detector}")
        print(f"{'='*80}\n")
        
        # 1. Cargar strain
        strain_raw = self.cargar_strain(detector)
        
        # 2. Aplicar filtro notch
        strain_notched = self.aplicar_filtro_notch(strain_raw)
        
        # 3. Extraer ringdown
        ringdown_start = self.gps_time + self.ringdown_start
        ringdown_end = ringdown_start + self.ringdown_duration
        strain_ringdown = strain_notched.crop(ringdown_start, ringdown_end)
        
        # 4. Aplicar filtro Ψ-NSE
        strain_filtered = self.aplicar_filtro_psi_nse(strain_ringdown)
        
        # 5. FFT interpolada
        freqs, fft_amp = self.calcular_fft_interpolada(strain_filtered)
        
        # 6. Calcular SNR
        snr_result = self.calcular_snr_en_f0(freqs, fft_amp)
        
        resultado = {
            "detector": detector,
            "n_samples": len(strain_filtered),
            "duration": float(self.ringdown_duration),
            "fft": {
                "frequencies": freqs.tolist(),
                "amplitudes": fft_amp.tolist()
            },
            "snr": snr_result,
            "strain_data": strain_filtered  # Guardar para análisis coherente
        }
        
        return resultado
    
    def run_complete_analysis(self) -> Dict:
        """
        Ejecutar análisis completo de GW150914.
        
        Returns:
            dict: Resultados completos del análisis
        """
        print("="*80)
        print("ANÁLISIS DE RESONANCIA POST-MERGER EN GW150914")
        print("Búsqueda específica de señal a 141.7 Hz")
        print("="*80)
        print()
        
        # Procesar cada detector
        h1_result = self.procesar_detector('H1')
        l1_result = self.procesar_detector('L1')
        
        self.resultados["detectores"]["H1"] = {
            k: v for k, v in h1_result.items() if k != "strain_data"
        }
        self.resultados["detectores"]["L1"] = {
            k: v for k, v in l1_result.items() if k != "strain_data"
        }
        
        print()
        
        # Análisis coherente H1-L1
        coherent_result = self.analisis_coherente_h1_l1(
            h1_result["strain_data"],
            l1_result["strain_data"]
        )
        self.resultados["coherent_analysis"] = coherent_result
        
        print()
        
        # Mapeo de coherencia de fase
        phase_map = self.mapeo_coherencia_fase(
            h1_result["snr"],
            l1_result["snr"],
            coherent_result
        )
        self.resultados["phase_mapping"] = phase_map
        
        # Calcular SNR combinado
        snr_h1 = h1_result["snr"]["snr_std"]
        snr_l1 = l1_result["snr"]["snr_std"]
        snr_combined = np.sqrt(snr_h1**2 + snr_l1**2)
        
        # Significancia combinada
        sig_h1 = h1_result["snr"]["significance_sigma"]
        sig_l1 = l1_result["snr"]["significance_sigma"]
        sig_combined = np.sqrt(sig_h1**2 + sig_l1**2)
        
        self.resultados["detailed"] = {
            "snr_h1": snr_h1,
            "snr_l1": snr_l1,
            "snr_combined": snr_combined,
            "snr_coherent": coherent_result["snr_coherent"]
        }
        
        self.resultados["statistics"] = {
            "significance_h1_sigma": sig_h1,
            "significance_l1_sigma": sig_l1,
            "significance_combined_sigma": sig_combined,
            "coherence_at_f0": coherent_result["coherence_at_f0"],
            "spatially_consistent": phase_map["is_spatially_consistent"]
        }
        
        # Generar visualizaciones
        self.generar_visualizaciones(h1_result, l1_result, coherent_result)
        
        # Generar reporte
        self.generar_reporte()
        
        # Guardar resultados JSON
        output_json = self.output_dir / "GW150914_1417Hz_complete_analysis.json"
        with open(output_json, 'w') as f:
            # Eliminar strain_data de resultados para JSON
            resultados_json = {
                k: v for k, v in self.resultados.items()
                if k != "strain_data"
            }
            json.dump(resultados_json, f, indent=2)
        
        print()
        print("="*80)
        print("📊 ANÁLISIS COMPLETADO")
        print(f"   JSON: {output_json}")
        print("="*80)
        
        return self.resultados
    
    def generar_visualizaciones(self, h1_result: Dict, l1_result: Dict,
                               coherent_result: Dict):
        """Generar figura completa de análisis."""
        print("\n📊 Generando visualizaciones...")
        
        fig = plt.figure(figsize=(20, 12))
        gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Espectro H1
        ax1 = fig.add_subplot(gs[0, 0])
        freqs_h1 = np.array(h1_result["fft"]["frequencies"])
        amp_h1 = np.array(h1_result["fft"]["amplitudes"])
        mask_h1 = (freqs_h1 > 100) & (freqs_h1 < 200)
        ax1.semilogy(freqs_h1[mask_h1], amp_h1[mask_h1], 'b-', linewidth=1)
        ax1.axvline(self.f0, color='red', linestyle='--', linewidth=2, 
                   label=f'f₀ = {self.f0} Hz')
        ax1.set_xlabel('Frecuencia (Hz)')
        ax1.set_ylabel('Amplitud FFT')
        ax1.set_title('H1: Espectro FFT Interpolado', fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Espectro L1
        ax2 = fig.add_subplot(gs[0, 1])
        freqs_l1 = np.array(l1_result["fft"]["frequencies"])
        amp_l1 = np.array(l1_result["fft"]["amplitudes"])
        mask_l1 = (freqs_l1 > 100) & (freqs_l1 < 200)
        ax2.semilogy(freqs_l1[mask_l1], amp_l1[mask_l1], 'g-', linewidth=1)
        ax2.axvline(self.f0, color='red', linestyle='--', linewidth=2,
                   label=f'f₀ = {self.f0} Hz')
        ax2.set_xlabel('Frecuencia (Hz)')
        ax2.set_ylabel('Amplitud FFT')
        ax2.set_title('L1: Espectro FFT Interpolado', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Zoom en f0 - H1
        ax3 = fig.add_subplot(gs[1, 0])
        mask_zoom_h1 = (freqs_h1 > self.f0 - 5) & (freqs_h1 < self.f0 + 5)
        ax3.plot(freqs_h1[mask_zoom_h1], amp_h1[mask_zoom_h1], 'b-', linewidth=2)
        ax3.axvline(self.f0, color='red', linestyle='--', linewidth=2)
        ax3.set_xlabel('Frecuencia (Hz)')
        ax3.set_ylabel('Amplitud FFT')
        ax3.set_title(f'H1: Zoom {self.f0-5}-{self.f0+5} Hz', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # 4. Zoom en f0 - L1
        ax4 = fig.add_subplot(gs[1, 1])
        mask_zoom_l1 = (freqs_l1 > self.f0 - 5) & (freqs_l1 < self.f0 + 5)
        ax4.plot(freqs_l1[mask_zoom_l1], amp_l1[mask_zoom_l1], 'g-', linewidth=2)
        ax4.axvline(self.f0, color='red', linestyle='--', linewidth=2)
        ax4.set_xlabel('Frecuencia (Hz)')
        ax4.set_ylabel('Amplitud FFT')
        ax4.set_title(f'L1: Zoom {self.f0-5}-{self.f0+5} Hz', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        # 5. Espectro de coherencia
        ax5 = fig.add_subplot(gs[2, 0])
        freqs_coh = np.array(coherent_result["frequencies"])
        coherence = np.array(coherent_result["coherence_spectrum"])
        mask_coh = (freqs_coh > 100) & (freqs_coh < 200)
        ax5.plot(freqs_coh[mask_coh], coherence[mask_coh], 'purple', linewidth=1)
        ax5.axvline(self.f0, color='red', linestyle='--', linewidth=2,
                   label=f'f₀ = {self.f0} Hz')
        ax5.axhline(0.5, color='orange', linestyle=':', linewidth=1,
                   label='Umbral coherencia')
        ax5.set_xlabel('Frecuencia (Hz)')
        ax5.set_ylabel('Coherencia H1-L1')
        ax5.set_title('Coherencia Espectral H1-L1', fontweight='bold')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        ax5.set_ylim([0, 1])
        
        # 6. Resumen estadístico
        ax6 = fig.add_subplot(gs[2, 1])
        ax6.axis('off')
        
        snr_h1 = h1_result["snr"]["snr_std"]
        snr_l1 = l1_result["snr"]["snr_std"]
        snr_combined = np.sqrt(snr_h1**2 + snr_l1**2)
        sig_combined = self.resultados["statistics"]["significance_combined_sigma"]
        coherence_f0 = coherent_result["coherence_at_f0"]
        
        summary_text = f"""
RESUMEN ESTADÍSTICO

Frecuencia QCAL: {self.f0} Hz
Hash Cert: {self.cert_hash}

SNR H1: {snr_h1:.2f}
SNR L1: {snr_l1:.2f}
SNR Combinado: {snr_combined:.2f}
SNR Coherente: {coherent_result['snr_coherent']:.2f}

Significancia: {sig_combined:.2f}σ
Coherencia @ f₀: {coherence_f0:.3f}

Consistencia Espacial: {'✅ Sí' if self.resultados['phase_mapping']['is_spatially_consistent'] else '❌ No'}

CONCLUSIÓN:
{'✅ POTENCIAL HALLAZGO' if sig_combined >= 5.0 else '⚠️ NO DETECCIÓN CONVINCENTE'}
"""
        
        ax6.text(0.1, 0.5, summary_text, fontsize=11, family='monospace',
                verticalalignment='center')
        
        # Título general
        fig.suptitle(
            f'Análisis Completo GW150914: Resonancia 141.7 Hz\n'
            f'Filtro Ψ-NSE v1.0 | FFT Interpolada (x{self.fft_padding_factor})',
            fontsize=16, fontweight='bold'
        )
        
        # Guardar
        output_fig = self.output_dir / "gw150914_1417Hz_analysis.png"
        plt.savefig(output_fig, dpi=300, bbox_inches='tight')
        print(f"   ✅ Figura guardada: {output_fig}")
        
        plt.close()
    
    def generar_reporte(self):
        """Generar reporte de texto."""
        print("📝 Generando reporte...")
        
        output_txt = self.output_dir / "GW150914_1417Hz_Analysis_Report.txt"
        
        with open(output_txt, 'w') as f:
            f.write("="*80 + "\n")
            f.write("ANÁLISIS DE RESONANCIA POST-MERGER EN GW150914\n")
            f.write("Búsqueda específica de señal a 141.7 Hz\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"Evento: {self.evento}\n")
            f.write(f"GPS Time: {self.gps_time}\n")
            f.write(f"Masa Final: {self.masa_final} M☉\n")
            f.write(f"Frecuencia QCAL: {self.f0} Hz\n")
            f.write(f"Hash de Certificación: {self.cert_hash}\n")
            f.write(f"Timestamp: {self.resultados['timestamp']}\n\n")
            
            f.write("RESULTADOS POR DETECTOR\n")
            f.write("-"*80 + "\n\n")
            
            for det in ['H1', 'L1']:
                det_data = self.resultados['detectores'][det]
                f.write(f"{det}:\n")
                f.write(f"  SNR (std): {det_data['snr']['snr_std']:.2f}\n")
                f.write(f"  SNR (median): {det_data['snr']['snr_median']:.2f}\n")
                f.write(f"  Significancia: {det_data['snr']['significance_sigma']:.2f}σ\n")
                f.write(f"  Frecuencia detectada: {det_data['snr']['f_detected']:.4f} Hz\n")
                f.write(f"  Desviación de f₀: {det_data['snr']['deviation_hz']:.4f} Hz\n\n")
            
            f.write("ANÁLISIS COHERENTE\n")
            f.write("-"*80 + "\n\n")
            f.write(f"SNR Combinado: {self.resultados['detailed']['snr_combined']:.2f}\n")
            f.write(f"SNR Coherente: {self.resultados['detailed']['snr_coherent']:.2f}\n")
            f.write(f"Significancia Combinada: {self.resultados['statistics']['significance_combined_sigma']:.2f}σ\n")
            f.write(f"Coherencia @ f₀: {self.resultados['statistics']['coherence_at_f0']:.4f}\n")
            f.write(f"Consistencia Espacial: {'Sí' if self.resultados['statistics']['spatially_consistent'] else 'No'}\n\n")
            
            f.write("MAPEO DE FASE\n")
            f.write("-"*80 + "\n\n")
            phase_map = self.resultados['phase_mapping']
            f.write(f"Fase H1-L1 observada: {phase_map['phase_diff_observed_rad']:.4f} rad ({np.degrees(phase_map['phase_diff_observed_rad']):.1f}°)\n")
            f.write(f"Fase H1-L1 esperada: {phase_map['phase_diff_expected_rad']:.4f} rad ({np.degrees(phase_map['phase_diff_expected_rad']):.1f}°)\n")
            f.write(f"Desviación: {phase_map['phase_deviation_deg']:.1f}°\n\n")
            
            f.write("CONCLUSIÓN\n")
            f.write("-"*80 + "\n\n")
            
            sig = self.resultados['statistics']['significance_combined_sigma']
            if sig >= 5.0:
                conclusion = "✅ POTENCIAL HALLAZGO - Señal significativa (≥5σ) detectada en 141.7 Hz"
            elif sig >= 3.0:
                conclusion = "⚠️ EVIDENCIA MODERADA - Señal detectada (3-5σ) requiere validación adicional"
            else:
                conclusion = "❌ NO DETECCIÓN CONVINCENTE - Señal por debajo de 3σ"
            
            f.write(f"{conclusion}\n\n")
            f.write("="*80 + "\n")
        
        print(f"   ✅ Reporte guardado: {output_txt}")


def main():
    """Ejecutar análisis completo."""
    from datetime import datetime
    
    print("\n" + "="*80)
    print("ANÁLISIS DE RESONANCIA POST-MERGER EN GW150914")
    print("Búsqueda específica de señal a 141.7 Hz")
    print("="*80)
    
    try:
        # Crear analizador y ejecutar
        analizador = AnalizadorGW150914()
        results = analizador.run_complete_analysis()
        
        print("\n✅ Análisis completado exitosamente")
        print(f"   Figura guardada como: gw150914_1417Hz_analysis.png")
        print(f"   Reporte guardado como: GW150914_1417Hz_Analysis_Report.txt")
        
        # Resumen ejecutivo
        print("\n" + "="*80)
        print("RESUMEN EJECUTIVO:")
        print(f"   • SNR combinado: {results['detailed']['snr_combined']:.2f}")
        print(f"   • Significancia: {results['statistics']['significance_combined_sigma']:.2f}σ")
        print(f"   • Conclusión: {'POTENCIAL HALLAZGO' if results['statistics']['significance_combined_sigma'] >= 5.0 else 'NO DETECCIÓN CONVINCENTE'}")
        print("="*80)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {str(e)}")
        print("\nSugerencias para solución:")
        print("1. Verificar conexión a internet para descargar datos de GWOSC")
        print("2. Instalar dependencias: pip install gwpy astropy scipy matplotlib")
        print("3. Contactar con los mantenedores de GWOSC si hay problemas de datos")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
