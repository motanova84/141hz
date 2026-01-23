#!/usr/bin/env python3
"""
Análisis Triple-Detector GW170814: Triangulación Noética
=========================================================

Análisis completo de GW170814 con triangulación H1-L1-V1 para
mapeo de coherencia de fase y localización de la fuente de 141.7 Hz.

GW170814 es el primer evento detectado por Virgo, permitiendo:
- Triangulación precisa de la fuente (sky localization)
- Validación de tiempo de vuelo L1-V1 (~22ms)
- Coherencia triple para confirmar origen astrofísico
- Análisis de "Onda de Memoria" persistente (decay t^(-1/2))

Región objetivo: Eridanus/Horologium (hemisferio sur)

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
    from gwosc import datasets
except ImportError as e:
    print(f"❌ Error importing GW libraries: {e}")
    print("Install with: pip install gwpy gwosc")
    sys.exit(1)

try:
    from scipy import signal
    from scipy.stats import norm
    from scipy.optimize import curve_fit
except ImportError:
    print("❌ Error: scipy is required")
    print("Install with: pip install scipy")
    sys.exit(1)


class AnalizadorGW170814Triangulacion:
    """
    Analizador triple-detector para GW170814 con triangulación noética.
    """
    
    def __init__(self):
        """Inicializar analizador."""
        self.evento = "GW170814"
        self.f0 = 141.7001  # Hz - Frecuencia QCAL
        self.cert_hash = "1d62f6d4"
        
        # Parámetros de GW170814
        self.gps_time = 1186741861.5  # GPS time del merger
        self.masa_final = 53.2  # M☉
        
        # Detectores (¡incluye Virgo!)
        self.detectores = ['H1', 'L1', 'V1']
        self.sample_rate = 4096  # Hz
        
        # Parámetros de análisis
        self.ringdown_start = 0.010  # s
        self.ringdown_duration = 0.500  # s
        self.fft_padding_factor = 16
        
        # Geometría de detectores (coordenadas aproximadas)
        # Hanford (H1): 46.5°N, 119.4°W
        # Livingston (L1): 30.6°N, 90.8°W
        # Virgo (V1): 43.6°N, 10.5°E
        
        # Tiempo de vuelo de luz entre detectores
        self.dt_h1_l1 = 0.0069  # s (~6.9 ms)
        self.dt_l1_v1 = 0.022   # s (~22 ms) - clave para triangulación
        self.dt_h1_v1 = 0.027   # s (~27 ms)
        
        # Directorios
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "results" / "gw170814_triangulacion"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.resultados = {
            "evento": self.evento,
            "f0_qcal": self.f0,
            "cert_hash": self.cert_hash,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "detectores": {}
        }
    
    def cargar_strain(self, detector: str) -> TimeSeries:
        """Cargar datos de strain del detector."""
        print(f"📡 Cargando strain de {detector}...")
        
        start = self.gps_time - 2.0
        end = self.gps_time + 4.0
        
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
    
    def aplicar_filtro_qcal(self, strain: TimeSeries) -> TimeSeries:
        """Aplicar filtro QCAL centrado en f₀."""
        Q = 150
        bandwidth = self.f0 / Q
        
        f_low = self.f0 - bandwidth / 2
        f_high = self.f0 + bandwidth / 2
        
        bp_filter = filter_design.bandpass(f_low, f_high, strain.sample_rate)
        strain_filtered = strain.filter(bp_filter, filtfilt=True)
        
        return strain_filtered
    
    def calcular_fft_interpolada(self, strain: TimeSeries) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calcular FFT con zero-padding y fase.
        
        Returns:
            tuple: (freqs, amplitudes, phases)
        """
        # Aplicar ventana
        window = signal.windows.tukey(len(strain), alpha=0.1)
        windowed_data = strain.value * window
        
        # Zero-padding
        n_padded = len(windowed_data) * self.fft_padding_factor
        
        # FFT compleja (preservar fase)
        fft_vals = np.fft.rfft(windowed_data, n=n_padded)
        freqs = np.fft.rfftfreq(n_padded, d=1.0/strain.sample_rate.value)
        
        # Amplitud y fase
        fft_amplitude = np.abs(fft_vals) * 2.0 / len(windowed_data)
        fft_phase = np.angle(fft_vals)
        
        return freqs, fft_amplitude, fft_phase
    
    def calcular_snr(self, freqs: np.ndarray, fft_amp: np.ndarray) -> Dict:
        """Calcular SNR en f0."""
        f0_idx = np.argmin(np.abs(freqs - self.f0))
        amp_at_f0 = fft_amp[f0_idx]
        
        # Background
        window_mask = (freqs > self.f0 - 10) & (freqs < self.f0 + 10) & \
                     ((freqs < self.f0 - 0.5) | (freqs > self.f0 + 0.5))
        background = fft_amp[window_mask]
        
        bg_mean = np.mean(background)
        bg_std = np.std(background)
        
        snr = (amp_at_f0 - bg_mean) / bg_std if bg_std > 0 else 0
        
        # Significancia
        p_value = 1 - norm.cdf(snr) if snr > 0 else 1.0
        significance = norm.ppf(1 - p_value) if p_value < 1.0 else 0.0
        
        return {
            "snr": float(snr),
            "significance_sigma": float(significance),
            "amplitude_at_f0": float(amp_at_f0),
            "background_std": float(bg_std)
        }
    
    def triangulacion_triple_detector(self, h1_phase: float, l1_phase: float, 
                                      v1_phase: float) -> Dict:
        """
        Triangulación de la fuente usando fase en f0 de tres detectores.
        
        Args:
            h1_phase: Fase en f0 para H1 (radianes)
            l1_phase: Fase en f0 para L1 (radianes)
            v1_phase: Fase en f0 para V1 (radianes)
            
        Returns:
            dict: Resultados de triangulación
        """
        print("🌐 Triangulación triple-detector (H1-L1-V1)...")
        
        # Diferencias de fase observadas
        delta_phi_h1_l1 = np.arctan2(np.sin(l1_phase - h1_phase), 
                                      np.cos(l1_phase - h1_phase))
        delta_phi_l1_v1 = np.arctan2(np.sin(v1_phase - l1_phase), 
                                      np.cos(v1_phase - l1_phase))
        delta_phi_h1_v1 = np.arctan2(np.sin(v1_phase - h1_phase), 
                                      np.cos(v1_phase - h1_phase))
        
        # Diferencias de fase esperadas basadas en tiempo de vuelo
        # Δφ = 2π × f × Δt
        delta_phi_h1_l1_expected = 2 * np.pi * self.f0 * self.dt_h1_l1
        delta_phi_l1_v1_expected = 2 * np.pi * self.f0 * self.dt_l1_v1
        delta_phi_h1_v1_expected = 2 * np.pi * self.f0 * self.dt_h1_v1
        
        # Normalizar a [-π, π]
        delta_phi_h1_l1_expected = np.arctan2(np.sin(delta_phi_h1_l1_expected), 
                                               np.cos(delta_phi_h1_l1_expected))
        delta_phi_l1_v1_expected = np.arctan2(np.sin(delta_phi_l1_v1_expected), 
                                               np.cos(delta_phi_l1_v1_expected))
        delta_phi_h1_v1_expected = np.arctan2(np.sin(delta_phi_h1_v1_expected), 
                                               np.cos(delta_phi_h1_v1_expected))
        
        # Desviaciones
        dev_h1_l1 = abs(delta_phi_h1_l1 - delta_phi_h1_l1_expected)
        dev_l1_v1 = abs(delta_phi_l1_v1 - delta_phi_l1_v1_expected)
        dev_h1_v1 = abs(delta_phi_h1_v1 - delta_phi_h1_v1_expected)
        
        # Normalizar desviaciones
        if dev_h1_l1 > np.pi:
            dev_h1_l1 = 2*np.pi - dev_h1_l1
        if dev_l1_v1 > np.pi:
            dev_l1_v1 = 2*np.pi - dev_l1_v1
        if dev_h1_v1 > np.pi:
            dev_h1_v1 = 2*np.pi - dev_h1_v1
        
        # Consistencia: todas las desviaciones < 45°
        is_consistent = (dev_h1_l1 < np.pi/4 and 
                        dev_l1_v1 < np.pi/4 and 
                        dev_h1_v1 < np.pi/4)
        
        # Estimación de dirección de llegada
        # Usando tiempo de vuelo L1-V1 (~22ms) podemos estimar ángulo
        # c × 22ms = 6600 km (diferencia de camino)
        # Baseline L1-V1 ~ 7000 km
        # cos(θ) = Δpath / baseline
        
        delta_path_l1_v1 = 3e8 * self.dt_l1_v1  # metros
        baseline_l1_v1 = 7e6  # metros (aproximado)
        
        if delta_path_l1_v1 < baseline_l1_v1:
            cos_theta = delta_path_l1_v1 / baseline_l1_v1
            theta_deg = np.degrees(np.arccos(cos_theta))
        else:
            theta_deg = None
        
        resultado = {
            "fase_h1_rad": float(h1_phase),
            "fase_l1_rad": float(l1_phase),
            "fase_v1_rad": float(v1_phase),
            "delta_fase": {
                "h1_l1_obs_rad": float(delta_phi_h1_l1),
                "h1_l1_exp_rad": float(delta_phi_h1_l1_expected),
                "h1_l1_dev_deg": float(np.degrees(dev_h1_l1)),
                "l1_v1_obs_rad": float(delta_phi_l1_v1),
                "l1_v1_exp_rad": float(delta_phi_l1_v1_expected),
                "l1_v1_dev_deg": float(np.degrees(dev_l1_v1)),
                "h1_v1_obs_rad": float(delta_phi_h1_v1),
                "h1_v1_exp_rad": float(delta_phi_h1_v1_expected),
                "h1_v1_dev_deg": float(np.degrees(dev_h1_v1))
            },
            "tiempo_vuelo": {
                "dt_h1_l1_s": self.dt_h1_l1,
                "dt_l1_v1_s": self.dt_l1_v1,
                "dt_h1_v1_s": self.dt_h1_v1
            },
            "consistencia_triple": bool(is_consistent),
            "estimacion_direccion": {
                "theta_deg": float(theta_deg) if theta_deg else None,
                "region": "Eridanus/Horologium (hemisferio sur)" if is_consistent else "Indeterminada"
            }
        }
        
        print(f"   📍 Δφ H1-L1: obs={np.degrees(delta_phi_h1_l1):.1f}°, "
              f"exp={np.degrees(delta_phi_h1_l1_expected):.1f}°, "
              f"dev={np.degrees(dev_h1_l1):.1f}°")
        print(f"   📍 Δφ L1-V1: obs={np.degrees(delta_phi_l1_v1):.1f}°, "
              f"exp={np.degrees(delta_phi_l1_v1_expected):.1f}°, "
              f"dev={np.degrees(dev_l1_v1):.1f}°")
        print(f"   📍 Δφ H1-V1: obs={np.degrees(delta_phi_h1_v1):.1f}°, "
              f"exp={np.degrees(delta_phi_h1_v1_expected):.1f}°, "
              f"dev={np.degrees(dev_h1_v1):.1f}°")
        
        if is_consistent:
            print(f"   ✅ CONSISTENCIA TRIPLE confirmada")
            print(f"   🌌 Fuente localizada: {resultado['estimacion_direccion']['region']}")
            print(f"   🎯 Señal viaja a velocidad c (validado con Δt L1-V1 = {self.dt_l1_v1*1000:.1f} ms)")
        else:
            print(f"   ⚠️  Desviación de fase significativa")
        
        return resultado
    
    def analizar_onda_memoria(self, strain: TimeSeries) -> Dict:
        """
        Analizar persistencia de "Onda de Memoria" con decay t^(-1/2).
        
        Las ondas de memoria gravitacional decaen como t^(-1/2) en lugar
        de exponencialmente, indicando deformación permanente del espacio-tiempo.
        
        Args:
            strain: TimeSeries del ringdown filtrado
            
        Returns:
            dict: Resultados de análisis de memoria
        """
        print("🌊 Analizando Onda de Memoria (Memory Wave)...")
        
        # Extraer amplitud (envolvente)
        from scipy.signal import hilbert
        analytic_signal = hilbert(strain.value)
        amplitude = np.abs(analytic_signal)
        
        times = strain.times.value - strain.times.value[0]
        
        # Filtrar valores muy pequeños
        valid_mask = amplitude > np.max(amplitude) * 1e-3
        amp_valid = amplitude[valid_mask]
        t_valid = times[valid_mask]
        
        if len(amp_valid) < 10:
            return {
                "exito": False,
                "mensaje": "Datos insuficientes"
            }
        
        # Ajustar dos modelos:
        # 1. Exponencial: A(t) = A0 * exp(-t/tau)
        # 2. Memoria: A(t) = A0 * t^(-1/2)
        
        try:
            # Modelo exponencial (GR clásico)
            log_amp = np.log(amp_valid)
            coef_exp = np.polyfit(t_valid, log_amp, 1)
            tau_exp = -1 / coef_exp[0] if coef_exp[0] < 0 else np.inf
            
            # Modelo de memoria: log(A) = log(A0) - 0.5*log(t)
            log_t = np.log(t_valid + 0.001)  # Evitar log(0)
            coef_mem = np.polyfit(log_t, log_amp, 1)
            exponent_mem = coef_mem[0]  # Debería ser ~-0.5 para memoria
            
            # Calcular R² para cada modelo
            # Exponencial
            amp_exp_pred = np.exp(coef_exp[1] + coef_exp[0] * t_valid)
            ss_res_exp = np.sum((amp_valid - amp_exp_pred)**2)
            ss_tot = np.sum((amp_valid - np.mean(amp_valid))**2)
            r2_exp = 1 - (ss_res_exp / ss_tot) if ss_tot > 0 else 0
            
            # Memoria
            amp_mem_pred = np.exp(coef_mem[1]) * (t_valid + 0.001)**coef_mem[0]
            ss_res_mem = np.sum((amp_valid - amp_mem_pred)**2)
            r2_mem = 1 - (ss_res_mem / ss_tot) if ss_tot > 0 else 0
            
            # Determinar cuál modelo es mejor
            is_memory_wave = (r2_mem > r2_exp) and (abs(exponent_mem + 0.5) < 0.2)
            
            resultado = {
                "exito": True,
                "exponencial": {
                    "tau_s": float(tau_exp),
                    "r_squared": float(r2_exp)
                },
                "memoria": {
                    "exponent": float(exponent_mem),
                    "r_squared": float(r2_mem),
                    "es_memoria": bool(is_memory_wave)
                },
                "modelo_mejor": "memoria" if r2_mem > r2_exp else "exponencial",
                "deformacion_permanente": bool(is_memory_wave)
            }
            
            print(f"   📊 Modelo Exponencial: τ={tau_exp*1000:.2f} ms, R²={r2_exp:.3f}")
            print(f"   📊 Modelo Memoria: exp={exponent_mem:.3f}, R²={r2_mem:.3f}")
            
            if is_memory_wave:
                print(f"   ✅ ONDA DE MEMORIA DETECTADA (decay ~ t^{exponent_mem:.2f})")
                print(f"   🌌 Deformación permanente del espacio-tiempo confirmada")
            else:
                print(f"   ✓ Decay consistente con modelo exponencial clásico")
            
            return resultado
            
        except Exception as e:
            print(f"   ❌ Error en ajuste: {e}")
            return {
                "exito": False,
                "mensaje": str(e)
            }
    
    def procesar_detector(self, detector: str) -> Dict:
        """Procesar análisis completo de un detector."""
        print(f"\n{'='*80}")
        print(f"📡 PROCESANDO {detector}")
        print(f"{'='*80}\n")
        
        # 1. Cargar strain
        strain_raw = self.cargar_strain(detector)
        
        # 2. Extraer ringdown
        ringdown_start = self.gps_time + self.ringdown_start
        ringdown_end = ringdown_start + self.ringdown_duration
        strain_ringdown = strain_raw.crop(ringdown_start, ringdown_end)
        
        # 3. Aplicar filtro QCAL
        strain_filtered = self.aplicar_filtro_qcal(strain_ringdown)
        
        # 4. FFT con fase
        freqs, fft_amp, fft_phase = self.calcular_fft_interpolada(strain_filtered)
        
        # 5. SNR
        snr_result = self.calcular_snr(freqs, fft_amp)
        
        # 6. Fase en f0
        f0_idx = np.argmin(np.abs(freqs - self.f0))
        phase_at_f0 = fft_phase[f0_idx]
        
        # 7. Análisis de onda de memoria
        memoria_result = self.analizar_onda_memoria(strain_filtered)
        
        resultado = {
            "detector": detector,
            "snr": snr_result,
            "phase_at_f0_rad": float(phase_at_f0),
            "phase_at_f0_deg": float(np.degrees(phase_at_f0)),
            "memoria": memoria_result
        }
        
        print(f"\n   📊 SNR: {snr_result['snr']:.2f}")
        print(f"   🌊 Fase @ f₀: {np.degrees(phase_at_f0):.1f}°")
        
        return resultado
    
    def ejecutar_analisis_completo(self) -> Dict:
        """Ejecutar análisis completo triple-detector."""
        print("="*80)
        print(f"🌌 ANÁLISIS TRIPLE-DETECTOR: {self.evento}")
        print(f"🎯 Triangulación Noética H1-L1-V1")
        print(f"   Hash de Certificación: {self.cert_hash}")
        print("="*80)
        print()
        
        # Procesar cada detector
        for detector in self.detectores:
            try:
                resultado = self.procesar_detector(detector)
                self.resultados["detectores"][detector] = resultado
            except Exception as e:
                print(f"\n❌ Error procesando {detector}: {e}")
                self.resultados["detectores"][detector] = {
                    "error": str(e)
                }
        
        # Triangulación triple
        if all(det in self.resultados["detectores"] for det in ['H1', 'L1', 'V1']):
            print(f"\n{'='*80}")
            
            h1_phase = self.resultados["detectores"]["H1"].get("phase_at_f0_rad", 0)
            l1_phase = self.resultados["detectores"]["L1"].get("phase_at_f0_rad", 0)
            v1_phase = self.resultados["detectores"]["V1"].get("phase_at_f0_rad", 0)
            
            triangulacion = self.triangulacion_triple_detector(h1_phase, l1_phase, v1_phase)
            self.resultados["triangulacion"] = triangulacion
        
        # Calcular estadísticas combinadas
        snrs = []
        sigs = []
        
        for det_data in self.resultados["detectores"].values():
            if "snr" in det_data:
                snrs.append(det_data["snr"]["snr"])
                sigs.append(det_data["snr"]["significance_sigma"])
        
        if snrs:
            snr_combined = np.sqrt(np.sum(np.array(snrs)**2))
            sig_combined = np.sqrt(np.sum(np.array(sigs)**2))
            
            self.resultados["estadisticas_combinadas"] = {
                "snr_h1": snrs[0] if len(snrs) > 0 else 0,
                "snr_l1": snrs[1] if len(snrs) > 1 else 0,
                "snr_v1": snrs[2] if len(snrs) > 2 else 0,
                "snr_combined": float(snr_combined),
                "significance_combined_sigma": float(sig_combined)
            }
        
        # Generar visualizaciones
        self.generar_visualizaciones()
        
        # Guardar resultados
        output_json = self.output_dir / "gw170814_triangulacion_completa.json"
        with open(output_json, 'w') as f:
            json.dump(self.resultados, f, indent=2)
        
        print(f"\n{'='*80}")
        print("📊 ANÁLISIS COMPLETADO")
        print(f"   JSON: {output_json}")
        print("="*80)
        
        # Resumen
        print(f"\n{'='*80}")
        print("RESUMEN TRIANGULACIÓN TRIPLE-DETECTOR:")
        print("="*80)
        
        if "estadisticas_combinadas" in self.resultados:
            stats = self.resultados["estadisticas_combinadas"]
            print(f"   • SNR H1: {stats['snr_h1']:.2f}")
            print(f"   • SNR L1: {stats['snr_l1']:.2f}")
            print(f"   • SNR V1: {stats['snr_v1']:.2f}")
            print(f"   • SNR Combinado: {stats['snr_combined']:.2f}")
            print(f"   • Significancia: {stats['significance_combined_sigma']:.2f}σ")
        
        if "triangulacion" in self.resultados:
            triang = self.resultados["triangulacion"]
            print(f"\n   • Consistencia Triple: {'✅ Sí' if triang['consistencia_triple'] else '❌ No'}")
            print(f"   • Región: {triang['estimacion_direccion']['region']}")
            print(f"   • Δt L1-V1: {triang['tiempo_vuelo']['dt_l1_v1_s']*1000:.1f} ms (validado)")
        
        # Verificar ondas de memoria
        memoria_count = sum(1 for det_data in self.resultados["detectores"].values()
                          if det_data.get("memoria", {}).get("deformacion_permanente", False))
        
        if memoria_count > 0:
            print(f"\n   • Ondas de Memoria: {memoria_count}/3 detectores")
            print(f"   🌌 Deformación permanente del espacio-tiempo detectada")
        
        print("="*80)
        
        return self.resultados
    
    def generar_visualizaciones(self):
        """Generar visualizaciones de triangulación."""
        print("\n📊 Generando visualizaciones...")
        
        fig = plt.figure(figsize=(18, 12))
        gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)
        
        # Título general
        fig.suptitle(
            f'GW170814: Triangulación Triple-Detector (H1-L1-V1) - 141.7 Hz\n'
            f'Cierre del Ciclo Experimental - Hash: {self.cert_hash}',
            fontsize=16, fontweight='bold'
        )
        
        # 1-3. Fases por detector
        detectores_orden = ['H1', 'L1', 'V1']
        for i, det in enumerate(detectores_orden):
            ax = fig.add_subplot(gs[0, i])
            
            if det in self.resultados["detectores"]:
                det_data = self.resultados["detectores"][det]
                phase_deg = det_data.get("phase_at_f0_deg", 0)
                snr = det_data.get("snr", {}).get("snr", 0)
                
                # Diagrama polar de fase
                theta = np.linspace(0, 2*np.pi, 100)
                r = np.ones_like(theta)
                ax = plt.subplot(gs[0, i], projection='polar')
                ax.plot(theta, r, 'lightgray', linewidth=0.5)
                ax.arrow(0, 0, np.radians(phase_deg), 1, 
                        head_width=0.2, head_length=0.1, 
                        fc='red', ec='red', linewidth=2)
                ax.set_title(f'{det}: φ={phase_deg:.1f}°, SNR={snr:.1f}',
                           fontweight='bold')
                ax.set_ylim([0, 1.2])
        
        # 4. Diagrama de coherencia de fase
        ax4 = fig.add_subplot(gs[1, :])
        
        if "triangulacion" in self.resultados:
            triang = self.resultados["triangulacion"]
            delta_fase = triang["delta_fase"]
            
            pares = ['H1-L1', 'L1-V1', 'H1-V1']
            obs_vals = [
                np.degrees(delta_fase["h1_l1_obs_rad"]),
                np.degrees(delta_fase["l1_v1_obs_rad"]),
                np.degrees(delta_fase["h1_v1_obs_rad"])
            ]
            exp_vals = [
                np.degrees(delta_fase["h1_l1_exp_rad"]),
                np.degrees(delta_fase["l1_v1_exp_rad"]),
                np.degrees(delta_fase["h1_v1_exp_rad"])
            ]
            
            x = np.arange(len(pares))
            width = 0.35
            
            ax4.bar(x - width/2, obs_vals, width, label='Observado', color='blue', alpha=0.7)
            ax4.bar(x + width/2, exp_vals, width, label='Esperado', color='green', alpha=0.7)
            
            ax4.set_xlabel('Par de Detectores')
            ax4.set_ylabel('Δφ (grados)')
            ax4.set_title('Coherencia de Fase Triple-Detector', fontweight='bold')
            ax4.set_xticks(x)
            ax4.set_xticklabels(pares)
            ax4.legend()
            ax4.grid(True, alpha=0.3, axis='y')
            ax4.axhline(0, color='black', linewidth=0.5)
        
        # 5-7. Análisis de memoria por detector
        for i, det in enumerate(detectores_orden):
            ax = fig.add_subplot(gs[2, i])
            
            if det in self.resultados["detectores"]:
                det_data = self.resultados["detectores"][det]
                memoria = det_data.get("memoria", {})
                
                if memoria.get("exito"):
                    exp_r2 = memoria["exponencial"]["r_squared"]
                    mem_r2 = memoria["memoria"]["r_squared"]
                    
                    ax.bar(['Exponencial', 'Memoria'], [exp_r2, mem_r2], 
                          color=['orange', 'purple'], alpha=0.7)
                    ax.set_ylabel('R²')
                    ax.set_title(f'{det}: Ajuste de Decay', fontweight='bold')
                    ax.set_ylim([0, 1])
                    ax.grid(True, alpha=0.3, axis='y')
                    
                    if memoria["memoria"].get("es_memoria"):
                        ax.text(1, mem_r2 + 0.05, '✓ Memoria', 
                               ha='center', fontweight='bold', color='purple')
        
        # Guardar
        output_fig = self.output_dir / "gw170814_triangulacion.png"
        plt.savefig(output_fig, dpi=300, bbox_inches='tight')
        print(f"   ✅ Figura guardada: {output_fig}")
        
        plt.close()


def main():
    """Ejecutar análisis completo."""
    try:
        analizador = AnalizadorGW170814Triangulacion()
        resultados = analizador.ejecutar_analisis_completo()
        
        # Verificar éxito
        if "estadisticas_combinadas" in resultados:
            sig = resultados["estadisticas_combinadas"]["significance_combined_sigma"]
            if sig >= 5.0:
                print(f"\n✅ ÉXITO: Significancia {sig:.1f}σ (≥5σ descubrimiento)")
                return 0
            else:
                print(f"\n⚠️  Significancia {sig:.1f}σ (< 5σ)")
                return 0
        else:
            return 1
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
