#!/usr/bin/env python3
"""
Análisis Poblacional GWTC-1: Resonancia 141.7 Hz
================================================

Ejecuta el análisis de resonancia en 141.7 Hz sobre múltiples eventos
de GWTC-1 para detectar consistencia estadística y validar el
"Fondo de Resonancia Universal".

Eventos analizados:
- GW150914 (M_final ~ 67.4 M☉)
- GW151226 (M_final ~ 21.8 M☉)
- GW170814 (M_final ~ 53.2 M☉) - Primer evento con Virgo

Si el SNR combinado escala con √N, habremos detectado el
Fondo de Resonancia Universal.

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
from typing import Dict, List, Tuple

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
    from scipy.stats import norm, linregress
except ImportError:
    print("❌ Error: scipy is required")
    print("Install with: pip install scipy")
    sys.exit(1)


class AnalizadorPoblacionalGWTC1:
    """
    Analizador poblacional de resonancia 141.7 Hz en GWTC-1.
    """
    
    def __init__(self):
        """Inicializar analizador poblacional."""
        self.f0 = 141.7001  # Hz - Frecuencia QCAL
        self.cert_hash = "1d62f6d4"
        
        # Eventos GWTC-1 a analizar
        self.eventos = {
            "GW150914": {
                "gps_time": 1126259462.4,
                "masa_final": 67.4,  # M☉
                "detectores": ['H1', 'L1']
            },
            "GW151226": {
                "gps_time": 1135136350.6,
                "masa_final": 21.8,
                "detectores": ['H1', 'L1']
            },
            "GW170814": {
                "gps_time": 1186741861.5,
                "masa_final": 53.2,
                "detectores": ['H1', 'L1', 'V1']  # Primer evento con Virgo
            }
        }
        
        # Parámetros de análisis
        self.sample_rate = 4096  # Hz
        self.ringdown_start = 0.010  # s
        self.ringdown_duration = 0.500  # s
        
        # Directorios
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "results" / "gwtc1_population"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.resultados = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "f0_qcal": self.f0,
            "cert_hash": self.cert_hash,
            "eventos_analizados": {},
            "estadisticas_poblacionales": {}
        }
    
    def analizar_evento(self, nombre: str, config: Dict) -> Dict:
        """
        Analizar un evento individual.
        
        Args:
            nombre: Nombre del evento
            config: Configuración del evento
            
        Returns:
            dict: Resultados del evento
        """
        print(f"\n{'='*80}")
        print(f"📡 ANALIZANDO {nombre}")
        print(f"   Masa final: {config['masa_final']} M☉")
        print(f"   Detectores: {', '.join(config['detectores'])}")
        print(f"{'='*80}\n")
        
        resultado_evento = {
            "nombre": nombre,
            "masa_final": config['masa_final'],
            "detectores": {},
            "snr_promedio": 0.0,
            "significancia_promedio": 0.0
        }
        
        snrs = []
        significancias = []
        
        for detector in config['detectores']:
            try:
                print(f"📊 Procesando {detector}...")
                
                # Cargar strain
                start = config['gps_time'] - 2.0
                end = config['gps_time'] + 4.0
                
                strain = TimeSeries.fetch_open_data(
                    detector, start, end,
                    sample_rate=self.sample_rate,
                    cache=True
                )
                
                # Extraer ringdown
                ringdown_start = config['gps_time'] + self.ringdown_start
                ringdown_end = ringdown_start + self.ringdown_duration
                ringdown = strain.crop(ringdown_start, ringdown_end)
                
                # Filtrar en f0
                Q = 150
                bandwidth = self.f0 / Q
                bp_filter = filter_design.bandpass(
                    self.f0 - bandwidth/2,
                    self.f0 + bandwidth/2,
                    ringdown.sample_rate
                )
                ringdown_filtered = ringdown.filter(bp_filter, filtfilt=True)
                
                # FFT
                window = signal.windows.tukey(len(ringdown_filtered), alpha=0.1)
                windowed = ringdown_filtered.value * window
                
                fft_vals = np.fft.rfft(windowed, n=len(windowed)*8)
                freqs = np.fft.rfftfreq(len(windowed)*8, d=1.0/self.sample_rate)
                fft_amp = np.abs(fft_vals) * 2.0 / len(windowed)
                
                # Calcular SNR en f0
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
                
                resultado_detector = {
                    "snr": float(snr),
                    "significance_sigma": float(significance),
                    "amplitude_at_f0": float(amp_at_f0),
                    "background_std": float(bg_std)
                }
                
                resultado_evento["detectores"][detector] = resultado_detector
                snrs.append(snr)
                significancias.append(significance)
                
                print(f"   ✅ SNR: {snr:.2f}, Significancia: {significance:.2f}σ")
                
            except Exception as e:
                print(f"   ❌ Error en {detector}: {e}")
                resultado_evento["detectores"][detector] = {
                    "error": str(e)
                }
        
        # Promedios
        if snrs:
            resultado_evento["snr_promedio"] = float(np.mean(snrs))
            resultado_evento["snr_combinado"] = float(np.sqrt(np.sum(np.array(snrs)**2)))
        
        if significancias:
            resultado_evento["significancia_promedio"] = float(np.mean(significancias))
            resultado_evento["significancia_combinada"] = float(np.sqrt(np.sum(np.array(significancias)**2)))
        
        print(f"\n   📊 SNR combinado: {resultado_evento.get('snr_combinado', 0):.2f}")
        print(f"   🎯 Significancia combinada: {resultado_evento.get('significancia_combinada', 0):.2f}σ")
        
        return resultado_evento
    
    def analizar_escalamiento(self) -> Dict:
        """
        Analizar escalamiento del SNR con √N.
        
        Si SNR_combined ~ √N, confirma Fondo de Resonancia Universal.
        
        Returns:
            dict: Resultados de escalamiento
        """
        print("\n" + "="*80)
        print("📈 ANÁLISIS DE ESCALAMIENTO CON √N")
        print("="*80 + "\n")
        
        # Extraer SNRs y número de detectores
        n_detectores = []
        snrs_combinados = []
        nombres_eventos = []
        
        for nombre, resultado in self.resultados["eventos_analizados"].items():
            n_det = len([d for d in resultado["detectores"].values() 
                        if "snr" in d])
            if n_det > 0 and "snr_combinado" in resultado:
                n_detectores.append(n_det)
                snrs_combinados.append(resultado["snr_combinado"])
                nombres_eventos.append(nombre)
        
        if len(n_detectores) < 2:
            print("⚠️  Datos insuficientes para análisis de escalamiento")
            return {
                "mensaje": "Datos insuficientes"
            }
        
        # Calcular escalamiento esperado
        sqrt_n = np.sqrt(n_detectores)
        
        # Regresión lineal: SNR vs √N
        slope, intercept, r_value, p_value, std_err = linregress(sqrt_n, snrs_combinados)
        
        # R² (coeficiente de determinación)
        r_squared = r_value**2
        
        resultado_escalamiento = {
            "n_eventos": len(n_detectores),
            "eventos": nombres_eventos,
            "n_detectores": n_detectores,
            "snrs_combinados": snrs_combinados,
            "sqrt_n": sqrt_n.tolist(),
            "regresion": {
                "slope": float(slope),
                "intercept": float(intercept),
                "r_squared": float(r_squared),
                "p_value": float(p_value)
            },
            "escalamiento_valido": r_squared > 0.8 and p_value < 0.05
        }
        
        print(f"   📊 Eventos analizados: {len(n_detectores)}")
        print(f"   📈 Pendiente: {slope:.2f}")
        print(f"   📉 R²: {r_squared:.3f}")
        print(f"   🎯 p-value: {p_value:.3e}")
        
        if resultado_escalamiento["escalamiento_valido"]:
            print("\n   ✅ ESCALAMIENTO CONFIRMADO (SNR ~ √N)")
            print("   🌌 FONDO DE RESONANCIA UNIVERSAL DETECTADO")
        else:
            print("\n   ❌ Escalamiento no confirmado")
        
        return resultado_escalamiento
    
    def ejecutar_analisis_poblacional(self) -> Dict:
        """
        Ejecutar análisis completo de población GWTC-1.
        
        Returns:
            dict: Resultados completos
        """
        print("="*80)
        print("🌌 ANÁLISIS POBLACIONAL GWTC-1: RESONANCIA 141.7 Hz")
        print(f"   Hash de Certificación: {self.cert_hash}")
        print("="*80)
        
        # Analizar cada evento
        for nombre, config in self.eventos.items():
            try:
                resultado = self.analizar_evento(nombre, config)
                self.resultados["eventos_analizados"][nombre] = resultado
            except Exception as e:
                print(f"\n❌ Error analizando {nombre}: {e}")
                self.resultados["eventos_analizados"][nombre] = {
                    "error": str(e)
                }
        
        # Análisis de escalamiento
        escalamiento = self.analizar_escalamiento()
        self.resultados["estadisticas_poblacionales"]["escalamiento"] = escalamiento
        
        # Calcular estadísticas globales
        snrs_todos = []
        sigs_todas = []
        
        for resultado in self.resultados["eventos_analizados"].values():
            if "snr_combinado" in resultado:
                snrs_todos.append(resultado["snr_combinado"])
            if "significancia_combinada" in resultado:
                sigs_todas.append(resultado["significancia_combinada"])
        
        if snrs_todos:
            self.resultados["estadisticas_poblacionales"]["snr_medio"] = float(np.mean(snrs_todos))
            self.resultados["estadisticas_poblacionales"]["snr_total_combinado"] = float(np.sqrt(np.sum(np.array(snrs_todos)**2)))
        
        if sigs_todas:
            self.resultados["estadisticas_poblacionales"]["significancia_media"] = float(np.mean(sigs_todas))
            self.resultados["estadisticas_poblacionales"]["significancia_total_combinada"] = float(np.sqrt(np.sum(np.array(sigs_todas)**2)))
        
        # Generar visualizaciones
        self.generar_visualizaciones()
        
        # Guardar resultados
        output_json = self.output_dir / "gwtc1_population_analysis.json"
        with open(output_json, 'w') as f:
            json.dump(self.resultados, f, indent=2)
        
        print("\n" + "="*80)
        print("📊 ANÁLISIS POBLACIONAL COMPLETADO")
        print(f"   JSON: {output_json}")
        print("="*80)
        
        # Resumen
        print("\n" + "="*80)
        print("RESUMEN POBLACIONAL:")
        print(f"   • Eventos analizados: {len(self.resultados['eventos_analizados'])}")
        if "snr_total_combinado" in self.resultados["estadisticas_poblacionales"]:
            print(f"   • SNR total combinado: {self.resultados['estadisticas_poblacionales']['snr_total_combinado']:.2f}")
        if "significancia_total_combinada" in self.resultados["estadisticas_poblacionales"]:
            print(f"   • Significancia total: {self.resultados['estadisticas_poblacionales']['significancia_total_combinada']:.2f}σ")
        
        if escalamiento.get("escalamiento_valido"):
            print(f"   • Escalamiento √N: ✅ CONFIRMADO (R²={escalamiento['regresion']['r_squared']:.3f})")
            print("\n   🌌 FONDO DE RESONANCIA UNIVERSAL DETECTADO")
        else:
            print("   • Escalamiento √N: ❌ No confirmado")
        
        print("="*80)
        
        return self.resultados
    
    def generar_visualizaciones(self):
        """Generar visualizaciones poblacionales."""
        print("\n📊 Generando visualizaciones poblacionales...")
        
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)
        
        # 1. SNR por evento
        ax1 = fig.add_subplot(gs[0, 0])
        nombres = []
        snrs = []
        for nombre, resultado in self.resultados["eventos_analizados"].items():
            if "snr_combinado" in resultado:
                nombres.append(nombre)
                snrs.append(resultado["snr_combinado"])
        
        if nombres:
            ax1.bar(nombres, snrs, color=['blue', 'green', 'purple'][:len(nombres)])
            ax1.axhline(5, color='red', linestyle='--', label='5σ umbral')
            ax1.set_ylabel('SNR Combinado')
            ax1.set_title('SNR por Evento', fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis='y')
        
        # 2. Significancia por evento
        ax2 = fig.add_subplot(gs[0, 1])
        sigs = []
        for nombre in nombres:
            resultado = self.resultados["eventos_analizados"][nombre]
            if "significancia_combinada" in resultado:
                sigs.append(resultado["significancia_combinada"])
        
        if sigs:
            ax2.bar(nombres, sigs, color=['blue', 'green', 'purple'][:len(nombres)])
            ax2.axhline(5, color='red', linestyle='--', label='5σ descubrimiento')
            ax2.axhline(3, color='orange', linestyle=':', label='3σ evidencia')
            ax2.set_ylabel('Significancia (σ)')
            ax2.set_title('Significancia por Evento', fontweight='bold')
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Escalamiento con √N
        ax3 = fig.add_subplot(gs[1, 0])
        
        escalamiento = self.resultados["estadisticas_poblacionales"].get("escalamiento", {})
        if "sqrt_n" in escalamiento:
            sqrt_n = np.array(escalamiento["sqrt_n"])
            snrs_obs = np.array(escalamiento["snrs_combinados"])
            
            # Plot datos observados
            ax3.scatter(sqrt_n, snrs_obs, s=100, color='blue', label='Observado', zorder=3)
            
            # Plot ajuste lineal
            slope = escalamiento["regresion"]["slope"]
            intercept = escalamiento["regresion"]["intercept"]
            sqrt_n_fit = np.linspace(sqrt_n.min()*0.9, sqrt_n.max()*1.1, 100)
            snr_fit = slope * sqrt_n_fit + intercept
            ax3.plot(sqrt_n_fit, snr_fit, 'r--', 
                    label=f'Ajuste: SNR = {slope:.2f}√N + {intercept:.2f}')
            
            # Etiquetar puntos
            for i, evento in enumerate(escalamiento["eventos"]):
                ax3.annotate(evento, (sqrt_n[i], snrs_obs[i]), 
                           xytext=(5, 5), textcoords='offset points')
            
            ax3.set_xlabel('√(Número de Detectores)')
            ax3.set_ylabel('SNR Combinado')
            ax3.set_title(f'Escalamiento con √N (R²={escalamiento["regresion"]["r_squared"]:.3f})', 
                         fontweight='bold')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        
        # 4. Tabla de resultados
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        
        tabla_text = "RESULTADOS POBLACIONALES\n\n"
        tabla_text += f"Frecuencia QCAL: {self.f0} Hz\n"
        tabla_text += f"Hash Cert: {self.cert_hash}\n\n"
        
        for nombre in nombres:
            resultado = self.resultados["eventos_analizados"][nombre]
            tabla_text += f"{nombre}:\n"
            tabla_text += f"  M_final: {resultado['masa_final']} M☉\n"
            tabla_text += f"  SNR: {resultado.get('snr_combinado', 0):.2f}\n"
            tabla_text += f"  Sig: {resultado.get('significancia_combinada', 0):.2f}σ\n\n"
        
        stats = self.resultados["estadisticas_poblacionales"]
        if "snr_total_combinado" in stats:
            tabla_text += f"SNR Total: {stats['snr_total_combinado']:.2f}\n"
        if "significancia_total_combinada" in stats:
            tabla_text += f"Sig Total: {stats['significancia_total_combinada']:.2f}σ\n"
        
        if escalamiento.get("escalamiento_valido"):
            tabla_text += "\n✅ Escalamiento √N confirmado"
        
        ax4.text(0.1, 0.5, tabla_text, fontsize=10, family='monospace',
                verticalalignment='center')
        
        # Título general
        fig.suptitle('Análisis Poblacional GWTC-1: Resonancia 141.7 Hz',
                    fontsize=16, fontweight='bold')
        
        # Guardar
        output_fig = self.output_dir / "gwtc1_population_analysis.png"
        plt.savefig(output_fig, dpi=300, bbox_inches='tight')
        print(f"   ✅ Figura guardada: {output_fig}")
        
        plt.close()


def main():
    """Ejecutar análisis poblacional."""
    try:
        analizador = AnalizadorPoblacionalGWTC1()
        resultados = analizador.ejecutar_analisis_poblacional()
        
        # Exit code basado en resultados
        escalamiento = resultados["estadisticas_poblacionales"].get("escalamiento", {})
        if escalamiento.get("escalamiento_valido"):
            print("\n✅ Éxito: Fondo de Resonancia Universal detectado")
            return 0
        else:
            print("\n⚠️  Advertencia: Escalamiento no confirmado")
            return 1
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
