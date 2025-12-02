#!/usr/bin/env python3
"""
Análisis de Resonancia Cruzada Virgo/KAGRA
==========================================
Análisis de coherencia y resonancia cruzada entre detectores para f₀ = 141.7001 Hz.

Detectores analizados:
- H1 (LIGO Hanford)
- L1 (LIGO Livingston)
- V1 (Virgo)
- K1 (KAGRA)

Métricas:
- SNR individual por detector
- Coherencia cruzada entre pares de detectores
- Fase relativa entre señales
- Consistencia de frecuencia entre detectores

Autor: José Manuel Mota Burruezo
Instituto Conciencia Cuántica
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


class AnalizadorResonanciaCruzada:
    """Análisis de resonancia cruzada entre múltiples detectores"""
    
    def __init__(self, f0=141.7001, banda_ancho=2.0):
        """
        Inicializa el analizador de resonancia cruzada
        
        Args:
            f0: Frecuencia fundamental (Hz)
            banda_ancho: Ancho de banda para análisis (Hz)
        """
        self.f0 = f0
        self.banda_ancho = banda_ancho
        self.detectores_disponibles = ['H1', 'L1', 'V1', 'K1']
        
    def analizar_detector(self, datos, fs, detector):
        """
        Analiza un detector individual
        
        Args:
            datos: Array de datos de strain
            fs: Frecuencia de muestreo (Hz)
            detector: Nombre del detector
            
        Returns:
            dict: Resultados del análisis
        """
        # Filtrar en banda de interés
        banda_inf = self.f0 - self.banda_ancho / 2
        banda_sup = self.f0 + self.banda_ancho / 2
        
        # Diseñar filtro
        sos = signal.butter(4, [banda_inf, banda_sup], 'bandpass', 
                           fs=fs, output='sos')
        datos_filtrados = signal.sosfilt(sos, datos)
        
        # Calcular espectro
        freqs, psd = signal.welch(datos, fs, nperseg=min(len(datos)//4, 4096))
        
        # Buscar pico en banda
        mask = (freqs >= banda_inf) & (freqs <= banda_sup)
        psd_banda = psd[mask]
        freqs_banda = freqs[mask]
        
        idx_max = np.argmax(psd_banda)
        freq_detectada = freqs_banda[idx_max]
        potencia_pico = psd_banda[idx_max]
        
        # Calcular SNR
        potencia_mediana = np.median(psd)
        snr = potencia_pico / potencia_mediana
        
        # Calcular amplitud y fase de la señal filtrada
        analytic_signal = signal.hilbert(datos_filtrados)
        amplitud = np.abs(analytic_signal)
        fase = np.angle(analytic_signal)
        
        # Amplitud máxima
        amp_max = np.max(amplitud)
        std_noise = np.std(datos_filtrados)
        snr_temporal = amp_max / std_noise if std_noise > 0 else 0
        
        return {
            'detector': detector,
            'frecuencia_detectada': float(freq_detectada),
            'diferencia_f0': float(abs(freq_detectada - self.f0)),
            'snr_espectral': float(snr),
            'snr_temporal': float(snr_temporal),
            'potencia': float(potencia_pico),
            'amplitud_max': float(amp_max),
            'datos_filtrados': datos_filtrados,
            'fase': fase,
            'freqs': freqs,
            'psd': psd
        }
    
    def calcular_coherencia(self, datos1, datos2, fs, det1, det2):
        """
        Calcula coherencia entre dos detectores
        
        Args:
            datos1, datos2: Arrays de datos de strain
            fs: Frecuencia de muestreo (Hz)
            det1, det2: Nombres de los detectores
            
        Returns:
            dict: Métricas de coherencia
        """
        # Asegurar misma longitud
        min_len = min(len(datos1), len(datos2))
        datos1 = datos1[:min_len]
        datos2 = datos2[:min_len]
        
        # Calcular coherencia
        freqs, coherence = signal.coherence(datos1, datos2, fs, 
                                            nperseg=min(min_len//4, 4096))
        
        # Coherencia en banda de interés
        mask = (freqs >= self.f0 - self.banda_ancho/2) & \
               (freqs <= self.f0 + self.banda_ancho/2)
        
        if not np.any(mask):
            return {
                'par': f'{det1}-{det2}',
                'coherencia_banda': 0.0,
                'coherencia_f0': 0.0,
                'error': 'banda_vacia'
            }
        
        coherence_banda = coherence[mask]
        freqs_banda = freqs[mask]
        
        # Coherencia promedio en banda
        coherencia_media = np.mean(coherence_banda)
        
        # Coherencia en f0
        idx_f0 = np.argmin(np.abs(freqs_banda - self.f0))
        coherencia_f0 = coherence_banda[idx_f0]
        
        # Calcular fase relativa usando cross-spectrum
        freqs_csd, csd = signal.csd(datos1, datos2, fs,
                                     nperseg=min(min_len//4, 4096))
        mask_csd = (freqs_csd >= self.f0 - 0.5) & (freqs_csd <= self.f0 + 0.5)
        
        if np.any(mask_csd):
            csd_f0 = csd[mask_csd]
            fase_relativa = np.angle(np.mean(csd_f0))
        else:
            fase_relativa = 0.0
        
        return {
            'par': f'{det1}-{det2}',
            'coherencia_banda': float(coherencia_media),
            'coherencia_f0': float(coherencia_f0),
            'fase_relativa': float(fase_relativa),
            'fase_relativa_deg': float(np.degrees(fase_relativa)),
            'freqs': freqs,
            'coherence': coherence
        }
    
    def analizar_evento(self, evento='GW150914', detectores=None):
        """
        Analiza resonancia cruzada en un evento
        
        Args:
            evento: Nombre del evento
            detectores: Lista de detectores (None = todos disponibles)
            
        Returns:
            dict: Resultados completos del análisis
        """
        if detectores is None:
            detectores = ['H1', 'L1', 'V1']  # V1 disponible en O2+
        
        print(f"\n🌌 ANÁLISIS DE RESONANCIA CRUZADA: {evento}")
        print("=" * 70)
        print(f"Detectores: {', '.join(detectores)}")
        print(f"Frecuencia objetivo: {self.f0} Hz")
        print()
        
        resultados = {
            'evento': evento,
            'f0': self.f0,
            'banda_ancho': self.banda_ancho,
            'detectores': {},
            'coherencias': []
        }
        
        try:
            from gwpy.timeseries import TimeSeries
            from gwosc import datasets
            
            # Obtener tiempo GPS
            try:
                gps = datasets.event_gps(evento)
                inicio = gps - 16
                fin = gps + 16
                print(f"📍 GPS: {gps} (±16s)")
            except:
                print(f"⚠️  No se pudo obtener GPS para {evento}")
                return self._analisis_simulado(evento, detectores)
            
            # Descargar y analizar cada detector
            datos_detectores = {}
            
            for detector in detectores:
                try:
                    print(f"\n📡 Analizando {detector}...")
                    
                    # Descargar datos
                    datos = TimeSeries.fetch_open_data(
                        detector, inicio, fin, sample_rate=4096
                    )
                    
                    # Preprocesamiento
                    datos = datos.highpass(20)
                    datos = datos.notch(60)
                    
                    # Analizar
                    resultado = self.analizar_detector(
                        datos.value, datos.sample_rate.value, detector
                    )
                    
                    resultados['detectores'][detector] = {
                        k: v for k, v in resultado.items()
                        if k not in ['datos_filtrados', 'fase', 'freqs', 'psd']
                    }
                    
                    # Guardar datos para coherencia
                    datos_detectores[detector] = {
                        'datos': datos.value,
                        'fs': datos.sample_rate.value
                    }
                    
                    print(f"  ✅ {detector}: f = {resultado['frecuencia_detectada']:.2f} Hz, " +
                          f"SNR = {resultado['snr_espectral']:.2f}")
                    
                except Exception as e:
                    print(f"  ❌ Error con {detector}: {e}")
                    resultados['detectores'][detector] = {'error': str(e)}
            
            # Calcular coherencias entre todos los pares
            print(f"\n🔗 ANÁLISIS DE COHERENCIA CRUZADA:")
            print("-" * 70)
            
            detectores_ok = [d for d in datos_detectores.keys()]
            for i, det1 in enumerate(detectores_ok):
                for det2 in detectores_ok[i+1:]:
                    try:
                        coherencia = self.calcular_coherencia(
                            datos_detectores[det1]['datos'],
                            datos_detectores[det2]['datos'],
                            datos_detectores[det1]['fs'],
                            det1, det2
                        )
                        
                        # Remover arrays grandes para JSON
                        coherencia_json = {
                            k: v for k, v in coherencia.items()
                            if k not in ['freqs', 'coherence']
                        }
                        resultados['coherencias'].append(coherencia_json)
                        
                        print(f"  {det1}-{det2}: " +
                              f"Coh(f₀) = {coherencia['coherencia_f0']:.3f}, " +
                              f"Coh(banda) = {coherencia['coherencia_banda']:.3f}, " +
                              f"Δφ = {coherencia['fase_relativa_deg']:.1f}°")
                    
                    except Exception as e:
                        print(f"  ⚠️  Error calculando {det1}-{det2}: {e}")
            
        except ImportError:
            print("⚠️  gwpy/gwosc no disponible - usando datos simulados")
            return self._analisis_simulado(evento, detectores)
        
        return resultados
    
    def _analisis_simulado(self, evento, detectores):
        """Análisis simulado para testing"""
        print("\n🧪 EJECUTANDO ANÁLISIS SIMULADO")
        
        resultados = {
            'evento': evento,
            'f0': self.f0,
            'banda_ancho': self.banda_ancho,
            'detectores': {},
            'coherencias': [],
            'simulado': True
        }
        
        # Generar datos sintéticos
        fs = 4096
        duration = 32
        t = np.linspace(0, duration, fs * duration)
        
        # Fase común para coherencia
        fase_base = np.random.uniform(0, 2*np.pi)
        
        datos_detectores = {}
        
        for detector in detectores:
            # Señal coherente con fase ligeramente diferente
            fase_det = fase_base + np.random.normal(0, 0.1)
            señal = 1e-21 * np.sin(2 * np.pi * self.f0 * t + fase_det)
            
            # Ruido diferente por detector
            ruido = np.random.normal(0, 3e-22, len(t))
            datos = señal + ruido
            
            # Analizar
            resultado = self.analizar_detector(datos, fs, detector)
            resultados['detectores'][detector] = {
                k: v for k, v in resultado.items()
                if k not in ['datos_filtrados', 'fase', 'freqs', 'psd']
            }
            
            datos_detectores[detector] = {'datos': datos, 'fs': fs}
        
        # Calcular coherencias sintéticas
        detectores_ok = list(datos_detectores.keys())
        for i, det1 in enumerate(detectores_ok):
            for det2 in detectores_ok[i+1:]:
                coherencia = self.calcular_coherencia(
                    datos_detectores[det1]['datos'],
                    datos_detectores[det2]['datos'],
                    fs, det1, det2
                )
                
                coherencia_json = {
                    k: v for k, v in coherencia.items()
                    if k not in ['freqs', 'coherence']
                }
                resultados['coherencias'].append(coherencia_json)
        
        return resultados
    
    def generar_reporte(self, resultados, output_dir='../results'):
        """
        Genera reporte completo
        
        Args:
            resultados: Resultados del análisis
            output_dir: Directorio de salida
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        evento = resultados['evento']
        
        # Guardar JSON
        json_file = output_path / f'resonancia_cruzada_{evento}.json'
        with open(json_file, 'w') as f:
            json.dump(resultados, f, indent=2)
        print(f"\n💾 Resultados guardados en: {json_file}")
        
        # Estadísticas
        print("\n📊 ESTADÍSTICAS DE RESONANCIA CRUZADA:")
        print("=" * 70)
        
        detectores_ok = [d for d, r in resultados['detectores'].items()
                        if 'error' not in r]
        
        print(f"\nDetectores analizados: {len(detectores_ok)}")
        print("\nFrecuencias detectadas:")
        for det in detectores_ok:
            res = resultados['detectores'][det]
            print(f"  {det}: {res['frecuencia_detectada']:.4f} Hz " +
                  f"(Δf = {res['diferencia_f0']:.4f} Hz, SNR = {res['snr_espectral']:.2f})")
        
        if resultados['coherencias']:
            print("\nCoherencia entre detectores:")
            for coh in resultados['coherencias']:
                print(f"  {coh['par']}: Coh(f₀) = {coh['coherencia_f0']:.3f}, " +
                      f"Δφ = {coh['fase_relativa_deg']:.1f}°")
            
            # Coherencia promedio
            coh_media = np.mean([c['coherencia_f0'] for c in resultados['coherencias']])
            print(f"\nCoherencia promedio: {coh_media:.3f}")
            
            if coh_media > 0.7:
                print("✅ Alta coherencia multi-detector - señal coherente")
            elif coh_media > 0.4:
                print("⚠️  Coherencia moderada - revisar análisis")
            else:
                print("❌ Baja coherencia - posible artefacto o ruido")
        
        # Generar visualización
        self._generar_visualizacion(resultados, output_path)
        
        return json_file
    
    def _generar_visualizacion(self, resultados, output_path):
        """Genera visualización de resultados"""
        evento = resultados['evento']
        detectores = [d for d, r in resultados['detectores'].items()
                     if 'error' not in r]
        
        if not detectores:
            print("⚠️  No hay datos para visualizar")
            return
        
        # Crear figura con subplots
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # 1. SNR por detector
        ax1 = fig.add_subplot(gs[0, :])
        snrs = [resultados['detectores'][d]['snr_espectral'] for d in detectores]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'][:len(detectores)]
        bars = ax1.bar(detectores, snrs, color=colors, alpha=0.7)
        ax1.axhline(y=5.0, color='red', linestyle='--', label='Umbral (SNR=5)', linewidth=2)
        ax1.set_ylabel('SNR Espectral')
        ax1.set_title(f'{evento}: SNR en f₀ = {self.f0} Hz por Detector')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Frecuencias detectadas
        ax2 = fig.add_subplot(gs[1, 0])
        freqs = [resultados['detectores'][d]['frecuencia_detectada'] for d in detectores]
        ax2.scatter(detectores, freqs, s=100, c=colors, alpha=0.7)
        ax2.axhline(y=self.f0, color='magenta', linestyle='--', 
                   label=f'f₀ = {self.f0} Hz', linewidth=2)
        ax2.set_ylabel('Frecuencia (Hz)')
        ax2.set_title('Frecuencias Detectadas')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Matriz de coherencia
        if resultados['coherencias']:
            ax3 = fig.add_subplot(gs[1, 1])
            n_det = len(detectores)
            coh_matrix = np.ones((n_det, n_det))
            
            for coh in resultados['coherencias']:
                par = coh['par'].split('-')
                if len(par) == 2 and par[0] in detectores and par[1] in detectores:
                    i = detectores.index(par[0])
                    j = detectores.index(par[1])
                    coh_matrix[i, j] = coh['coherencia_f0']
                    coh_matrix[j, i] = coh['coherencia_f0']
            
            im = ax3.imshow(coh_matrix, cmap='RdYlGn', vmin=0, vmax=1, aspect='auto')
            ax3.set_xticks(range(n_det))
            ax3.set_yticks(range(n_det))
            ax3.set_xticklabels(detectores)
            ax3.set_yticklabels(detectores)
            ax3.set_title('Matriz de Coherencia en f₀')
            plt.colorbar(im, ax=ax3, label='Coherencia')
            
            # Añadir valores
            for i in range(n_det):
                for j in range(n_det):
                    if i != j:
                        text = ax3.text(j, i, f'{coh_matrix[i, j]:.2f}',
                                      ha="center", va="center", color="black", fontsize=10)
        
        # 4. Diferencias de fase
        if resultados['coherencias']:
            ax4 = fig.add_subplot(gs[2, :])
            pares = [c['par'] for c in resultados['coherencias']]
            fases = [c['fase_relativa_deg'] for c in resultados['coherencias']]
            ax4.bar(pares, fases, color='purple', alpha=0.6)
            ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)
            ax4.set_ylabel('Diferencia de Fase (grados)')
            ax4.set_xlabel('Par de Detectores')
            ax4.set_title('Diferencias de Fase entre Detectores')
            ax4.set_xticklabels(pares, rotation=45, ha='right')
            ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'Análisis de Resonancia Cruzada: {evento}', 
                    fontsize=14, fontweight='bold')
        
        fig_file = output_path / f'resonancia_cruzada_{evento}.png'
        plt.savefig(fig_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Visualización guardada en: {fig_file}")


def main():
    """Función principal"""
    print("🌌 ANÁLISIS DE RESONANCIA CRUZADA VIRGO/KAGRA")
    print("=" * 70)
    print("Búsqueda de coherencia multi-detector en f₀ = 141.7001 Hz")
    print()
    
    # Crear analizador
    analizador = AnalizadorResonanciaCruzada()
    
    # Analizar GW150914 (solo H1, L1 - antes de Virgo)
    print("\n📍 Analizando GW150914 (O1 - sin Virgo)...")
    resultados_gw150914 = analizador.analizar_evento('GW150914', ['H1', 'L1'])
    analizador.generar_reporte(resultados_gw150914)
    
    # Analizar GW170814 (primer evento con Virgo)
    print("\n" + "=" * 70)
    print("\n📍 Analizando GW170814 (primer evento tri-detector)...")
    resultados_gw170814 = analizador.analizar_evento('GW170814', ['H1', 'L1', 'V1'])
    analizador.generar_reporte(resultados_gw170814)
    
    print("\n✅ ANÁLISIS DE RESONANCIA CRUZADA COMPLETADO")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
