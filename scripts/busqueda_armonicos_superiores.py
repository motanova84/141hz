#!/usr/bin/env python3
"""
Búsqueda Experimental de Armónicos Superiores en LIGO
=======================================================
Análisis sistemático de armónicos de f₀ = 141.7001 Hz en datos de LIGO.

Armónicos buscados:
- Submúltiplos: f₀/2, f₀/3, f₀/4, f₀/5
- Múltiplos: 2f₀, 3f₀, 4f₀, 5f₀
- Armónicos áureos: f₀ × φ, f₀ × φ²
- Armónicos π: f₀ × π, f₀ × π²

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


class BuscadorArmonicosSuperiores:
    """Búsqueda experimental de armónicos superiores de 141.7001 Hz"""
    
    def __init__(self, f0=141.7001):
        """
        Inicializa el buscador de armónicos
        
        Args:
            f0: Frecuencia fundamental (Hz)
        """
        self.f0 = f0
        self.phi = (1 + np.sqrt(5)) / 2  # Número áureo
        self.armonicos = self._calcular_armonicos()
        
    def _calcular_armonicos(self):
        """Calcula todos los armónicos a buscar"""
        armonicos = {}
        
        # Submúltiplos (divisiones)
        for n in [2, 3, 4, 5]:
            armonicos[f'f0/{n}'] = {
                'frecuencia': self.f0 / n,
                'tipo': 'submúltiplo',
                'orden': n
            }
        
        # Múltiplos
        for n in [2, 3, 4, 5]:
            armonicos[f'{n}f0'] = {
                'frecuencia': self.f0 * n,
                'tipo': 'múltiplo',
                'orden': n
            }
        
        # Armónicos áureos
        armonicos['f0*phi'] = {
            'frecuencia': self.f0 * self.phi,
            'tipo': 'áureo',
            'orden': 1
        }
        armonicos['f0*phi^2'] = {
            'frecuencia': self.f0 * self.phi**2,
            'tipo': 'áureo',
            'orden': 2
        }
        
        # Armónicos π
        armonicos['f0*pi'] = {
            'frecuencia': self.f0 * np.pi,
            'tipo': 'pi',
            'orden': 1
        }
        armonicos['f0*pi^2'] = {
            'frecuencia': self.f0 * np.pi**2,
            'tipo': 'pi',
            'orden': 2
        }
        
        return armonicos
    
    def buscar_en_datos(self, datos, fs, detector='H1', banda_ancho=2.0):
        """
        Busca armónicos en datos de strain
        
        Args:
            datos: Array de datos de strain
            fs: Frecuencia de muestreo (Hz)
            detector: Nombre del detector
            banda_ancho: Ancho de banda para búsqueda (Hz)
            
        Returns:
            dict: Resultados de la búsqueda
        """
        print(f"\n🔍 BÚSQUEDA DE ARMÓNICOS SUPERIORES - {detector}")
        print("=" * 70)
        
        # Calcular espectro de potencia
        freqs, psd = signal.welch(datos, fs, nperseg=min(len(datos)//4, 4096))
        
        # Buscar cada armónico
        resultados = {}
        for nombre, info in self.armonicos.items():
            freq_target = info['frecuencia']
            
            # Verificar si está dentro del rango de LIGO (10-2000 Hz)
            if freq_target < 10 or freq_target > 2000:
                resultados[nombre] = {
                    'frecuencia_teorica': freq_target,
                    'detectable': False,
                    'razon': 'fuera_rango_ligo'
                }
                continue
            
            # Buscar pico en banda
            mask = (freqs >= freq_target - banda_ancho/2) & \
                   (freqs <= freq_target + banda_ancho/2)
            
            if not np.any(mask):
                resultados[nombre] = {
                    'frecuencia_teorica': freq_target,
                    'detectable': False,
                    'razon': 'banda_vacia'
                }
                continue
            
            # Encontrar pico máximo en banda
            psd_banda = psd[mask]
            freqs_banda = freqs[mask]
            idx_max = np.argmax(psd_banda)
            
            # Calcular SNR
            potencia_pico = psd_banda[idx_max]
            potencia_mediana = np.median(psd)
            snr = potencia_pico / potencia_mediana
            
            # Calcular diferencia de frecuencia
            freq_detectada = freqs_banda[idx_max]
            diff_freq = abs(freq_detectada - freq_target)
            
            resultados[nombre] = {
                'frecuencia_teorica': float(freq_target),
                'frecuencia_detectada': float(freq_detectada),
                'diferencia': float(diff_freq),
                'snr': float(snr),
                'potencia': float(potencia_pico),
                'tipo': info['tipo'],
                'orden': info['orden'],
                'detectable': True,
                'significativo': bool(snr > 3.0)
            }
            
            status = "✅" if snr > 5.0 else "⚠️ " if snr > 3.0 else "❌"
            print(f"{status} {nombre:12s}: {freq_detectada:8.2f} Hz " +
                  f"(teórico: {freq_target:8.2f} Hz), SNR = {snr:6.2f}")
        
        return resultados
    
    def analizar_evento(self, evento='GW150914', detectores=['H1', 'L1']):
        """
        Analiza armónicos en un evento específico
        
        Args:
            evento: Nombre del evento (e.g., 'GW150914')
            detectores: Lista de detectores a analizar
            
        Returns:
            dict: Resultados por detector
        """
        print(f"\n🌌 ANÁLISIS DE ARMÓNICOS SUPERIORES: {evento}")
        print("=" * 70)
        
        resultados_evento = {
            'evento': evento,
            'f0': self.f0,
            'detectores': {}
        }
        
        try:
            from gwpy.timeseries import TimeSeries
            from gwosc import datasets
            
            # Obtener tiempo GPS del evento
            try:
                gps = datasets.event_gps(evento)
                inicio = gps - 16
                fin = gps + 16
            except:
                print(f"⚠️  No se pudo obtener GPS para {evento}")
                return self._analisis_simulado(evento, detectores)
            
            # Analizar cada detector
            for detector in detectores:
                try:
                    print(f"\n📡 Descargando datos de {detector}...")
                    datos = TimeSeries.fetch_open_data(
                        detector, inicio, fin, sample_rate=4096
                    )
                    
                    # Preprocesamiento básico
                    datos = datos.highpass(20)
                    datos = datos.notch(60)
                    
                    # Buscar armónicos
                    resultados = self.buscar_en_datos(
                        datos.value, datos.sample_rate.value, detector
                    )
                    
                    resultados_evento['detectores'][detector] = resultados
                    
                except Exception as e:
                    print(f"❌ Error con {detector}: {e}")
                    resultados_evento['detectores'][detector] = {
                        'error': str(e)
                    }
            
        except ImportError:
            print("⚠️  gwpy/gwosc no disponible - usando datos simulados")
            return self._analisis_simulado(evento, detectores)
        
        return resultados_evento
    
    def _analisis_simulado(self, evento, detectores):
        """Análisis simulado para testing sin conectividad"""
        print("\n🧪 EJECUTANDO ANÁLISIS SIMULADO")
        
        resultados_evento = {
            'evento': evento,
            'f0': self.f0,
            'detectores': {},
            'simulado': True
        }
        
        # Generar datos sintéticos
        fs = 4096
        duration = 32
        t = np.linspace(0, duration, fs * duration)
        
        for detector in detectores:
            # Señal sintética con armónicos
            señal = np.zeros_like(t)
            for nombre, info in self.armonicos.items():
                if info['frecuencia'] < 10 or info['frecuencia'] > 2000:
                    continue
                # Amplitud decreciente con orden
                assert info['orden'] > 0, f"El armónico '{nombre}' tiene orden no positivo: {info['orden']}"
                amp = 1e-21 / info['orden']
                señal += amp * np.sin(2 * np.pi * info['frecuencia'] * t)
            
            # Agregar ruido
            ruido = np.random.normal(0, 5e-22, len(t))
            datos = señal + ruido
            
            # Buscar armónicos
            resultados = self.buscar_en_datos(datos, fs, detector)
            resultados_evento['detectores'][detector] = resultados
        
        return resultados_evento
    
    def generar_reporte(self, resultados_evento, output_dir='../results'):
        """
        Genera reporte completo de la búsqueda
        
        Args:
            resultados_evento: Resultados del análisis
            output_dir: Directorio para guardar resultados
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        evento = resultados_evento['evento']
        
        # Guardar JSON
        json_file = output_path / f'armonicos_superiores_{evento}.json'
        with open(json_file, 'w') as f:
            json.dump(resultados_evento, f, indent=2)
        print(f"\n💾 Resultados guardados en: {json_file}")
        
        # Generar estadísticas
        print("\n📊 ESTADÍSTICAS GENERALES:")
        print("=" * 70)
        
        total_armonicos = len(self.armonicos)
        detectables = 0
        significativos = 0
        
        for detector, resultados in resultados_evento['detectores'].items():
            if 'error' in resultados:
                continue
            
            det_count = sum(1 for r in resultados.values() 
                          if isinstance(r, dict) and r.get('detectable', False))
            sig_count = sum(1 for r in resultados.values() 
                          if isinstance(r, dict) and r.get('significativo', False))
            
            detectables += det_count
            significativos += sig_count
            
            print(f"\n{detector}:")
            print(f"  • Armónicos detectables: {det_count}/{total_armonicos}")
            print(f"  • Detecciones significativas (SNR > 3): {sig_count}")
            
            # Top 3 armónicos por SNR
            armonicos_validos = [(nombre, data) for nombre, data in resultados.items()
                               if isinstance(data, dict) and data.get('detectable', False)]
            armonicos_validos.sort(key=lambda x: x[1].get('snr', 0), reverse=True)
            
            print(f"\n  🏆 Top 3 armónicos detectados:")
            for i, (nombre, data) in enumerate(armonicos_validos[:3], 1):
                print(f"    {i}. {nombre}: {data['frecuencia_detectada']:.2f} Hz, " +
                      f"SNR = {data['snr']:.2f}")
        
        # Generar visualización
        self._generar_visualizacion(resultados_evento, output_path)
        
        return json_file
    
    def _generar_visualizacion(self, resultados_evento, output_path):
        """Genera visualización de resultados"""
        evento = resultados_evento['evento']
        detectores = [d for d in resultados_evento['detectores'].keys() 
                     if 'error' not in resultados_evento['detectores'][d]]
        
        if not detectores:
            print("⚠️  No hay datos para visualizar")
            return
        
        fig, axes = plt.subplots(len(detectores), 1, 
                                figsize=(12, 4 * len(detectores)))
        if len(detectores) == 1:
            axes = [axes]
        
        for ax, detector in zip(axes, detectores):
            resultados = resultados_evento['detectores'][detector]
            
            # Preparar datos para gráfico
            nombres = []
            frecuencias = []
            snrs = []
            tipos = []
            
            for nombre, data in resultados.items():
                if not isinstance(data, dict) or not data.get('detectable', False):
                    continue
                nombres.append(nombre)
                frecuencias.append(data['frecuencia_teorica'])
                snrs.append(data['snr'])
                tipos.append(data['tipo'])
            
            # Colores por tipo
            colores = {'submúltiplo': '#1f77b4', 'múltiplo': '#ff7f0e',
                      'áureo': '#2ca02c', 'pi': '#d62728'}
            colors = [colores[t] for t in tipos]
            
            # Gráfico de barras
            bars = ax.bar(range(len(nombres)), snrs, color=colors, alpha=0.7)
            ax.axhline(y=5.0, color='red', linestyle='--', 
                      label='Umbral significativo (SNR=5)', linewidth=2)
            ax.axhline(y=3.0, color='orange', linestyle=':', 
                      label='Umbral marginal (SNR=3)', linewidth=1.5)
            
            ax.set_xlabel('Armónico')
            ax.set_ylabel('SNR')
            ax.set_title(f'{detector} - {evento}: Búsqueda de Armónicos Superiores')
            ax.set_xticks(range(len(nombres)))
            ax.set_xticklabels(nombres, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        fig_file = output_path / f'armonicos_superiores_{evento}.png'
        plt.savefig(fig_file, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Visualización guardada en: {fig_file}")


def main():
    """Función principal"""
    print("🌌 BÚSQUEDA EXPERIMENTAL DE ARMÓNICOS SUPERIORES EN LIGO")
    print("=" * 70)
    print(f"Frecuencia fundamental: f₀ = 141.7001 Hz")
    print()
    
    # Crear buscador
    buscador = BuscadorArmonicosSuperiores()
    
    # Mostrar armónicos a buscar
    print("📋 ARMÓNICOS A BUSCAR:")
    print("-" * 70)
    for nombre, info in buscador.armonicos.items():
        print(f"  {nombre:12s}: {info['frecuencia']:8.2f} Hz ({info['tipo']})")
    
    # Analizar GW150914
    print("\n" + "=" * 70)
    resultados = buscador.analizar_evento('GW150914', ['H1', 'L1'])
    
    # Generar reporte
    buscador.generar_reporte(resultados)
    
    print("\n✅ BÚSQUEDA DE ARMÓNICOS SUPERIORES COMPLETADA")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
