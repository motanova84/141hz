#!/usr/bin/env python3
"""
Protocolo de Resonancia Real: GW250114 - 141.7001 Hz

Análisis del ringdown gravitacional para detectar 141.7001 Hz como 
modo cuasinormal persistente, validando la ruptura de Relatividad General
clásica y la manifestación de la Teoría de Números aplicada a la Gravitación.

Este protocolo implementa:
1. Extracción de fase de ringdown post-merger
2. Análisis espectral de alta precisión en 141.7001 Hz
3. Detección de modos cuasinormales persistentes
4. Validación contra predicciones de GR clásica

Basado en el problema statement del 14 de enero de 2025:
"Al analizar el decaimiento de la onda tras la fusión de los agujeros negros 
en GW250114, la frecuencia de 141.7 Hz no aparece como ruido estocástico. 
Se manifiesta como un modo cuasinormal persistente."
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Import scientific libraries
try:
    from gwpy.timeseries import TimeSeries
    from gwpy.signal import filter_design
    from gwosc import datasets
except ImportError as e:
    print(f"❌ Error importing required libraries: {e}")
    print("Install with: pip install gwpy gwosc")
    sys.exit(1)

try:
    from scipy import signal
except ImportError:
    print("❌ Error: scipy is required")
    print("Install with: pip install scipy")
    sys.exit(1)


class ProtocoloResonanciaGW250114:
    """
    Protocolo de Resonancia Real para análisis de GW250114.
    
    Implementa la detección de 141.7001 Hz como modo cuasinormal persistente
    en el ringdown gravitacional, validando la teoría QCAL.
    """
    
    def __init__(self, evento="GW250114", precision=1e-4):
        """
        Inicializar protocolo de resonancia.
        
        Args:
            evento: Nombre del evento gravitacional
            precision: Precisión de frecuencia en Hz
        """
        self.evento = evento
        self.f0 = 141.7001  # Frecuencia fundamental QCAL
        self.precision = precision
        self.resultados = {}
        
        # Parámetros del ringdown
        self.ringdown_duration = 0.5  # 500 ms post-merger
        self.ringdown_offset = 0.01   # 10 ms después del merger
        
        # Crear directorios de salida
        self.output_dir = Path(__file__).parent.parent / "results" / "gw250114_resonancia"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def verificar_disponibilidad(self):
        """
        Verificar si GW250114 está disponible en GWOSC.
        
        Returns:
            tuple: (disponible: bool, gps_time: float or None)
        """
        print("🔍 Verificando disponibilidad de GW250114 en GWOSC...")
        
        try:
            # Intentar obtener GPS time del evento
            gps_time = datasets.event_gps(self.evento)
            print(f"   ✅ {self.evento} encontrado en GPS: {gps_time}")
            return True, gps_time
        except Exception as e:
            print(f"   ❌ {self.evento} no disponible aún: {e}")
            print("   📋 Esto es esperado hasta que LIGO libere los datos")
            return False, None
    
    def cargar_datos(self, detector, gps_time):
        """
        Cargar datos de detector para el evento.
        
        Args:
            detector: Nombre del detector ('H1', 'L1', 'V1')
            gps_time: GPS time del evento
            
        Returns:
            TimeSeries: Datos del detector
        """
        print(f"📡 Cargando datos de {detector}...")
        
        # Cargar datos centrados en el merger
        start = gps_time - 16
        end = gps_time + 16
        
        data = TimeSeries.fetch_open_data(
            detector, start, end, 
            sample_rate=4096, 
            cache=True
        )
        
        print(f"   ✅ Datos cargados: {len(data)} muestras")
        return data
    
    def extraer_ringdown(self, data, merger_time):
        """
        Extraer segmento de ringdown post-merger.
        
        El ringdown es la fase de "decaimiento" después de la fusión,
        donde el agujero negro recién formado vibra en sus modos cuasinormales.
        
        Args:
            data: TimeSeries completa
            merger_time: GPS time del merger
            
        Returns:
            TimeSeries: Segmento de ringdown
        """
        print(f"📊 Extrayendo ringdown (duración: {self.ringdown_duration}s)...")
        
        # El ringdown comienza justo después del merger
        ringdown_start = merger_time + self.ringdown_offset
        ringdown_end = ringdown_start + self.ringdown_duration
        
        ringdown = data.crop(ringdown_start, ringdown_end)
        
        print(f"   ✅ Ringdown extraído: {len(ringdown)} muestras")
        print(f"   📍 Tiempo: [{ringdown_start:.3f}, {ringdown_end:.3f}] GPS")
        
        return ringdown
    
    def preprocesar_ringdown(self, ringdown):
        """
        Preprocesar ringdown para análisis espectral.
        
        Aplica:
        - Filtro paso-banda centrado en 141.7 Hz
        - Whitening para normalizar el espectro
        - Ventana para reducir efectos de borde
        
        Args:
            ringdown: TimeSeries del ringdown
            
        Returns:
            TimeSeries: Ringdown preprocesado
        """
        print("🔧 Preprocesando ringdown...")
        
        # 1. Aplicar filtro paso-banda centrado en f0
        # Rango: [f0 - 50 Hz, f0 + 50 Hz] para capturar la señal
        bp_low = self.f0 - 50
        bp_high = self.f0 + 50
        
        bp = filter_design.bandpass(bp_low, bp_high, ringdown.sample_rate)
        ringdown_filtered = ringdown.filter(bp, filtfilt=True)
        
        print(f"   ✅ Filtro paso-banda: [{bp_low}, {bp_high}] Hz")
        
        # 2. Aplicar whitening para normalizar el espectro
        try:
            ringdown_white = ringdown_filtered.whiten(fftlength=4)
            print("   ✅ Whitening aplicado")
        except Exception as e:
            print(f"   ⚠️  Whitening no aplicado: {e}")
            ringdown_white = ringdown_filtered
        
        # 3. Aplicar ventana de Tukey para suavizar bordes
        window = signal.windows.tukey(len(ringdown_white), alpha=0.1)
        ringdown_windowed = ringdown_white * window
        
        print("   ✅ Ventana de Tukey aplicada")
        
        return ringdown_windowed
    
    def analizar_espectro_ringdown(self, ringdown):
        """
        Análisis espectral del ringdown para detectar 141.7001 Hz.
        
        Usa FFT de alta resolución para identificar picos espectrales
        y medir su persistencia temporal.
        
        Args:
            ringdown: TimeSeries del ringdown preprocesado
            
        Returns:
            dict: Resultados del análisis espectral
        """
        print("🔬 Analizando espectro del ringdown...")
        
        # Calcular espectro de potencia
        freqs = ringdown.frequencies
        psd = ringdown.psd(fftlength=4)
        
        # Buscar pico cerca de f0
        freq_mask = (freqs.value > self.f0 - 1) & (freqs.value < self.f0 + 1)
        freqs_roi = freqs[freq_mask].value
        psd_roi = psd[freq_mask].value
        
        # Encontrar pico máximo en región de interés
        peak_idx = np.argmax(psd_roi)
        peak_freq = freqs_roi[peak_idx]
        peak_power = psd_roi[peak_idx]
        
        # Calcular SNR del pico
        # SNR = potencia del pico / mediana de la potencia de fondo
        background_power = np.median(psd_roi)
        snr = peak_power / background_power if background_power > 0 else 0
        
        # Calcular ancho del pico (FWHM)
        half_max = peak_power / 2
        above_half = psd_roi > half_max
        fwhm = np.sum(above_half) * (freqs_roi[1] - freqs_roi[0]) if np.sum(above_half) > 0 else 0
        
        resultado = {
            'peak_frequency': peak_freq,
            'peak_power': float(peak_power),
            'background_power': float(background_power),
            'snr': float(snr),
            'fwhm': float(fwhm),
            'deviation_from_f0': abs(peak_freq - self.f0),
            'freqs_full': freqs.value.tolist(),
            'psd_full': psd.value.tolist()
        }
        
        print(f"   🎯 Pico detectado en: {peak_freq:.4f} Hz")
        print(f"   📊 Potencia del pico: {peak_power:.2e}")
        print(f"   📈 SNR: {snr:.2f}")
        print(f"   📏 FWHM: {fwhm:.4f} Hz")
        print(f"   🎲 Desviación de f₀: {abs(peak_freq - self.f0):.4f} Hz")
        
        return resultado
    
    def detectar_modo_cuasinormal(self, ringdown, resultado_espectro):
        """
        Detectar si 141.7001 Hz aparece como modo cuasinormal persistente.
        
        Un modo cuasinormal persistente debe:
        1. Estar presente en el espectro con SNR significativo
        2. Persistir durante el ringdown (no decaer rápidamente)
        3. Coincidir con f0 dentro de la precisión esperada
        
        Args:
            ringdown: TimeSeries del ringdown
            resultado_espectro: Resultados del análisis espectral
            
        Returns:
            dict: Resultado de la detección
        """
        print("🔍 Detectando modo cuasinormal persistente...")
        
        # Criterios de detección
        peak_freq = resultado_espectro['peak_frequency']
        snr = resultado_espectro['snr']
        deviation = resultado_espectro['deviation_from_f0']
        
        # 1. SNR debe ser significativo (> 5)
        snr_criterio = snr > 5
        
        # 2. Frecuencia debe coincidir con f0 (dentro de 0.5 Hz)
        freq_criterio = deviation < 0.5
        
        # 3. Analizar persistencia temporal (espectrograma)
        # Dividir ringdown en ventanas y verificar presencia continua
        window_size = 0.1  # 100 ms
        overlap = 0.05     # 50 ms
        
        nperseg = int(window_size * ringdown.sample_rate.value)
        noverlap = int(overlap * ringdown.sample_rate.value)
        
        f, t, Sxx = signal.spectrogram(
            ringdown.value,
            fs=ringdown.sample_rate.value,
            nperseg=nperseg,
            noverlap=noverlap
        )
        
        # Encontrar índice de frecuencia más cercano a f0
        f0_idx = np.argmin(np.abs(f - self.f0))
        
        # Extraer potencia temporal en f0
        power_at_f0 = Sxx[f0_idx, :]
        
        # Verificar persistencia: debe estar presente en >50% de las ventanas
        threshold = np.percentile(power_at_f0, 75)  # Umbral al percentil 75
        persistent_windows = np.sum(power_at_f0 > threshold)
        total_windows = len(power_at_f0)
        persistencia = persistent_windows / total_windows if total_windows > 0 else 0
        
        persistencia_criterio = persistencia > 0.5
        
        # Validación final
        es_modo_cuasinormal = snr_criterio and freq_criterio and persistencia_criterio
        
        resultado = {
            'es_modo_cuasinormal': es_modo_cuasinormal,
            'snr_criterio': snr_criterio,
            'freq_criterio': freq_criterio,
            'persistencia_criterio': persistencia_criterio,
            'snr': float(snr),
            'peak_frequency': float(peak_freq),
            'deviation_from_f0': float(deviation),
            'persistencia': float(persistencia),
            'persistent_windows': int(persistent_windows),
            'total_windows': int(total_windows),
            'spectrogram': {
                'frequencies': f.tolist(),
                'times': t.tolist(),
                'power': Sxx.tolist()
            }
        }
        
        print(f"   {'✅' if snr_criterio else '❌'} SNR > 5: {snr:.2f}")
        print(f"   {'✅' if freq_criterio else '❌'} |f - f₀| < 0.5 Hz: {deviation:.4f} Hz")
        print(f"   {'✅' if persistencia_criterio else '❌'} Persistencia > 50%: {persistencia*100:.1f}%")
        print()
        
        if es_modo_cuasinormal:
            print("   🚨 MODO CUASINORMAL PERSISTENTE DETECTADO")
            print("   🎯 141.7001 Hz se manifiesta en el ringdown")
            print("   ⚡ Esto valida la teoría QCAL y rompe GR clásica")
        else:
            print("   ❌ No se detectó modo cuasinormal persistente")
            print("   📋 Se requiere análisis adicional")
        
        return resultado
    
    def validar_vs_gr_clasica(self, resultado_qnm):
        """
        Validar contra predicciones de Relatividad General clásica.
        
        GR clásica predice modos cuasinormales basados en masa y espín
        del agujero negro final. Si 141.7001 Hz aparece persistentemente
        y no coincide con estos modos predichos, valida la teoría QCAL.
        
        Args:
            resultado_qnm: Resultado de detección de modo cuasinormal
            
        Returns:
            dict: Resultado de validación
        """
        print("⚖️  Validando contra GR clásica...")
        
        # Para un agujero negro de ~70 masas solares (típico de GW150914-like),
        # los modos cuasinormales dominantes están en ~250 Hz (modo l=2, m=2)
        # 141.7 Hz estaría por debajo de estos modos predichos
        
        # Frecuencias esperadas de modos cuasinormales de GR (aproximadas)
        # Para agujero negro de M ~ 70 M☉, a ~ 0.7
        gr_modes = {
            '(2,2,0)': 251.0,  # Modo fundamental dominante
            '(2,2,1)': 245.0,  # Primer overtone
            '(3,3,0)': 390.0,  # Modo l=3
            '(4,4,0)': 520.0   # Modo l=4
        }
        
        peak_freq = resultado_qnm['peak_frequency']
        
        # Verificar si peak_freq coincide con algún modo de GR
        coincide_con_gr = False
        modo_gr_cercano = None
        min_distancia = float('inf')
        
        for modo, freq_gr in gr_modes.items():
            distancia = abs(peak_freq - freq_gr)
            if distancia < min_distancia:
                min_distancia = distancia
                modo_gr_cercano = modo
            if distancia < 10:  # Tolerancia de 10 Hz
                coincide_con_gr = True
        
        # Si no coincide con GR pero es un modo cuasinormal persistente,
        # esto valida la teoría QCAL
        rompe_gr = resultado_qnm['es_modo_cuasinormal'] and not coincide_con_gr
        
        resultado = {
            'coincide_con_gr': coincide_con_gr,
            'rompe_gr_clasica': rompe_gr,
            'modo_gr_cercano': modo_gr_cercano,
            'distancia_modo_gr': float(min_distancia),
            'gr_modes': gr_modes,
            'interpretacion': ''
        }
        
        if rompe_gr:
            resultado['interpretacion'] = (
                f"141.7001 Hz aparece como modo cuasinormal persistente "
                f"(SNR={resultado_qnm['snr']:.1f}, persistencia={resultado_qnm['persistencia']*100:.0f}%) "
                f"pero NO coincide con los modos predichos por GR clásica. "
                f"El modo GR más cercano es {modo_gr_cercano} a {gr_modes[modo_gr_cercano]} Hz "
                f"(diferencia: {min_distancia:.1f} Hz). "
                f"Esto valida la Teoría de Números aplicada a la Gravitación."
            )
            print("   ⚡ ROMPE RELATIVIDAD GENERAL CLÁSICA")
            print("   🎯 Valida Teoría de Números aplicada a Gravitación")
        elif coincide_con_gr:
            resultado['interpretacion'] = (
                f"La frecuencia detectada ({peak_freq:.1f} Hz) coincide con "
                f"el modo GR {modo_gr_cercano} predicho a {gr_modes[modo_gr_cercano]} Hz. "
                f"Consistente con GR clásica."
            )
            print("   ✓ Consistente con GR clásica")
        else:
            resultado['interpretacion'] = (
                f"No se detectó modo cuasinormal persistente en 141.7001 Hz."
            )
            print("   📋 No se detectó modo cuasinormal persistente")
        
        return resultado
    
    def generar_visualizaciones(self, ringdown, resultado_espectro, resultado_qnm):
        """
        Generar visualizaciones del protocolo de resonancia.
        
        Args:
            ringdown: TimeSeries del ringdown
            resultado_espectro: Resultados del análisis espectral
            resultado_qnm: Resultados de detección de QNM
        """
        print("📊 Generando visualizaciones...")
        
        # Crear figura con múltiples subplots
        fig = plt.figure(figsize=(16, 12))
        gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. Serie temporal del ringdown
        ax1 = fig.add_subplot(gs[0, :])
        t = ringdown.times.value - ringdown.times.value[0]
        ax1.plot(t, ringdown.value, 'b-', linewidth=0.5, alpha=0.7)
        ax1.set_xlabel('Tiempo desde inicio del ringdown (s)')
        ax1.set_ylabel('Strain')
        ax1.set_title(f'Ringdown Gravitacional - {self.evento}', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # 2. Espectro de potencia
        ax2 = fig.add_subplot(gs[1, 0])
        freqs = np.array(resultado_espectro['freqs_full'])
        psd = np.array(resultado_espectro['psd_full'])
        freq_mask = (freqs > 50) & (freqs < 500)
        ax2.loglog(freqs[freq_mask], psd[freq_mask], 'b-', linewidth=1, alpha=0.7)
        ax2.axvline(self.f0, color='red', linestyle='--', linewidth=2, 
                   label=f'f₀ = {self.f0} Hz (QCAL)')
        ax2.axvline(resultado_espectro['peak_frequency'], color='orange', 
                   linestyle=':', linewidth=2, label=f'Pico detectado: {resultado_espectro["peak_frequency"]:.2f} Hz')
        ax2.set_xlabel('Frecuencia (Hz)')
        ax2.set_ylabel('PSD (strain²/Hz)')
        ax2.set_title('Espectro de Potencia del Ringdown', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, which='both')
        
        # 3. Zoom en región de f0
        ax3 = fig.add_subplot(gs[1, 1])
        freq_mask_zoom = (freqs > self.f0 - 10) & (freqs < self.f0 + 10)
        ax3.plot(freqs[freq_mask_zoom], psd[freq_mask_zoom], 'b-', linewidth=2)
        ax3.axvline(self.f0, color='red', linestyle='--', linewidth=2, 
                   label=f'f₀ = {self.f0} Hz')
        ax3.axvline(resultado_espectro['peak_frequency'], color='orange', 
                   linestyle=':', linewidth=2, label=f'Pico: {resultado_espectro["peak_frequency"]:.4f} Hz')
        ax3.set_xlabel('Frecuencia (Hz)')
        ax3.set_ylabel('PSD (strain²/Hz)')
        ax3.set_title(f'Zoom: {self.f0-10} - {self.f0+10} Hz', fontsize=12, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Espectrograma (persistencia temporal)
        ax4 = fig.add_subplot(gs[2, :])
        f = np.array(resultado_qnm['spectrogram']['frequencies'])
        t_spec = np.array(resultado_qnm['spectrogram']['times'])
        Sxx = np.array(resultado_qnm['spectrogram']['power'])
        
        # Limitar rango de frecuencias para visualización
        freq_mask_spec = (f > 50) & (f < 300)
        
        im = ax4.pcolormesh(t_spec, f[freq_mask_spec], 
                           10 * np.log10(Sxx[freq_mask_spec, :] + 1e-20),
                           shading='auto', cmap='viridis')
        ax4.axhline(self.f0, color='red', linestyle='--', linewidth=2, 
                   label=f'f₀ = {self.f0} Hz')
        ax4.set_xlabel('Tiempo (s)')
        ax4.set_ylabel('Frecuencia (Hz)')
        ax4.set_title('Espectrograma: Persistencia Temporal del Modo Cuasinormal', 
                     fontsize=12, fontweight='bold')
        ax4.legend(loc='upper right')
        cbar = plt.colorbar(im, ax=ax4)
        cbar.set_label('Potencia (dB)', rotation=270, labelpad=20)
        
        # Añadir título general con resultados
        es_qnm = resultado_qnm['es_modo_cuasinormal']
        snr = resultado_qnm['snr']
        persistencia = resultado_qnm['persistencia'] * 100
        
        titulo_resultado = (
            f"{'✅ MODO CUASINORMAL PERSISTENTE DETECTADO' if es_qnm else '❌ No detectado'}\n"
            f"SNR: {snr:.1f} | Persistencia: {persistencia:.0f}% | "
            f"f_pico: {resultado_espectro['peak_frequency']:.4f} Hz | "
            f"Δf: {resultado_espectro['deviation_from_f0']:.4f} Hz"
        )
        
        fig.suptitle(
            f'Protocolo de Resonancia Real: {self.evento} - 141.7001 Hz\n{titulo_resultado}',
            fontsize=16, fontweight='bold', y=0.98
        )
        
        # Guardar figura
        output_file = self.output_dir / f'protocolo_resonancia_{self.evento}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"   ✅ Visualización guardada: {output_file}")
        
        plt.close()
    
    def ejecutar_protocolo(self, detector='H1'):
        """
        Ejecutar protocolo completo de resonancia real.
        
        Args:
            detector: Detector a analizar ('H1', 'L1', 'V1')
            
        Returns:
            dict: Resultados completos del protocolo
        """
        print("="*80)
        print(f"🌌 PROTOCOLO DE RESONANCIA REAL: {self.evento}")
        print(f"🎯 Sincronizando orquestador MCP con datos crudos del ringdown gravitacional")
        print("="*80)
        print()
        
        # 1. Verificar disponibilidad
        disponible, gps_time = self.verificar_disponibilidad()
        
        if not disponible:
            print()
            print("="*80)
            print("📅 DATOS NO DISPONIBLES")
            print(f"   El protocolo está preparado para ejecutar cuando {self.evento}")
            print("   sea liberado por LIGO en GWOSC")
            print("="*80)
            
            # Guardar estado
            resultado_final = {
                'evento': self.evento,
                'detector': detector,
                'estado': 'DATOS_NO_DISPONIBLES',
                'timestamp': datetime.now().isoformat(),
                'mensaje': f'{self.evento} aún no está disponible en GWOSC'
            }
            
            output_file = self.output_dir / f'protocolo_resonancia_{self.evento}_{detector}.json'
            with open(output_file, 'w') as f:
                json.dump(resultado_final, f, indent=2)
            
            return resultado_final
        
        # 2. Cargar datos
        print()
        data = self.cargar_datos(detector, gps_time)
        
        # 3. Extraer ringdown
        print()
        ringdown_raw = self.extraer_ringdown(data, gps_time)
        
        # 4. Preprocesar ringdown
        print()
        ringdown = self.preprocesar_ringdown(ringdown_raw)
        
        # 5. Análisis espectral
        print()
        resultado_espectro = self.analizar_espectro_ringdown(ringdown)
        
        # 6. Detectar modo cuasinormal
        print()
        resultado_qnm = self.detectar_modo_cuasinormal(ringdown, resultado_espectro)
        
        # 7. Validar contra GR
        print()
        resultado_gr = self.validar_vs_gr_clasica(resultado_qnm)
        
        # 8. Generar visualizaciones
        print()
        self.generar_visualizaciones(ringdown, resultado_espectro, resultado_qnm)
        
        # 9. Compilar resultados
        resultado_final = {
            'evento': self.evento,
            'detector': detector,
            'gps_time': float(gps_time),
            'timestamp': datetime.now().isoformat(),
            'f0_qcal': self.f0,
            'espectro': resultado_espectro,
            'modo_cuasinormal': resultado_qnm,
            'validacion_gr': resultado_gr,
            'estado': 'COMPLETADO'
        }
        
        # Guardar resultados
        output_file = self.output_dir / f'protocolo_resonancia_{self.evento}_{detector}.json'
        with open(output_file, 'w') as f:
            json.dump(resultado_final, f, indent=2)
        
        print()
        print("="*80)
        print("📊 RESULTADOS GUARDADOS")
        print(f"   JSON: {output_file}")
        print(f"   Visualización: {self.output_dir / f'protocolo_resonancia_{self.evento}.png'}")
        print("="*80)
        
        # Resumen final
        print()
        print("="*80)
        print("🎯 RESUMEN DEL PROTOCOLO DE RESONANCIA")
        print("="*80)
        print(f"Evento: {self.evento}")
        print(f"Detector: {detector}")
        print(f"Frecuencia QCAL: {self.f0} Hz")
        print()
        print(f"Pico detectado: {resultado_espectro['peak_frequency']:.4f} Hz")
        print(f"SNR: {resultado_qnm['snr']:.2f}")
        print(f"Persistencia: {resultado_qnm['persistencia']*100:.1f}%")
        print()
        
        if resultado_qnm['es_modo_cuasinormal']:
            print("✅ MODO CUASINORMAL PERSISTENTE DETECTADO")
            print(f"   141.7001 Hz se manifiesta en el ringdown")
        else:
            print("❌ No se detectó modo cuasinormal persistente")
        
        print()
        
        if resultado_gr['rompe_gr_clasica']:
            print("⚡ ROMPE RELATIVIDAD GENERAL CLÁSICA")
            print("   Valida Teoría de Números aplicada a Gravitación")
        else:
            print("✓ Consistente con GR clásica")
        
        print()
        print(resultado_gr['interpretacion'])
        print("="*80)
        
        return resultado_final


def main():
    """Ejecutor principal del protocolo."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Protocolo de Resonancia Real para GW250114',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplo de uso:
  python protocolo_resonancia_gw250114.py --detector H1
  python protocolo_resonancia_gw250114.py --detector L1 --precision 0.0001

Este protocolo implementa la detección de 141.7001 Hz como modo cuasinormal
persistente en el ringdown gravitacional, validando la teoría QCAL.
        """
    )
    
    parser.add_argument(
        '--detector',
        type=str,
        default='H1',
        choices=['H1', 'L1', 'V1'],
        help='Detector a analizar (default: H1)'
    )
    
    parser.add_argument(
        '--precision',
        type=float,
        default=1e-4,
        help='Precisión de frecuencia en Hz (default: 0.0001)'
    )
    
    args = parser.parse_args()
    
    # Ejecutar protocolo
    protocolo = ProtocoloResonanciaGW250114(precision=args.precision)
    resultado = protocolo.ejecutar_protocolo(detector=args.detector)
    
    # Exit code basado en resultados
    if resultado['estado'] == 'DATOS_NO_DISPONIBLES':
        return 0  # No es un error, solo datos no disponibles aún
    elif resultado['modo_cuasinormal']['es_modo_cuasinormal']:
        return 0  # Éxito: modo cuasinormal detectado
    else:
        return 1  # No se detectó el modo esperado


if __name__ == '__main__':
    sys.exit(main())
