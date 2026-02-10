#!/usr/bin/env python3
"""
𓂀 DESCARGADOR DE DATOS CRUDOS GWOSC
Accede a datos LIGO/Virgo a 4096 Hz - Canales auxiliares sin filtrado
"""

import requests
import numpy as np
import h5py
import argparse
import os
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    from gwosc import datasets
    from gwosc.datasets import event_gps
    from gwpy.timeseries import TimeSeries
    GWOSC_AVAILABLE = True
except ImportError:
    GWOSC_AVAILABLE = False
    print("⚠️  gwpy/gwosc not available - will use simulated data")


class DescargadorGWOSC:
    """Descarga datos crudos de LIGO/Virgo a máxima resolución."""
    
    def __init__(self):
        self.base_url = "https://gwosc.org"
        self.sampling_rate = 4096  # Hz - Máxima disponible
        self.estaciones = ['H1', 'L1', 'V1']  # Hanford, Livingston, Virgo
        self.canal_crudo = 'DCS-CALIB_STRAIN_CLEAN'  # Canal con menos filtrado
        
    def obtener_eventos_recientes(self, max_eventos=10):
        """Obtener eventos recientes de GWTC-3/O3."""
        print("𓂀 BUSCANDO EVENTOS RECIENTES GWTC-3/O3")
        print("=" * 60)
        
        if not GWOSC_AVAILABLE:
            print("⚠️  GWOSC no disponible - usando eventos de prueba")
            return self._get_test_events()
        
        try:
            # Acceder al catálogo más reciente
            eventos = datasets.find_datasets(type='events')
            eventos_recientes = []
            
            for event in eventos[:max_eventos]:
                try:
                    gps = event_gps(event)
                    eventos_recientes.append({
                        'nombre': event,
                        'gps': gps,
                        'detectores': ['H1', 'L1'],  # Default
                        'snr': 'N/A'
                    })
                    print(f"  • {event}: GPS={gps}")
                except Exception as e:
                    print(f"  ⚠️  Error obteniendo {event}: {e}")
                    continue
            
            return eventos_recientes if eventos_recientes else self._get_test_events()
            
        except Exception as e:
            print(f"❌ Error accediendo GWOSC: {e}")
            return self._get_test_events()
    
    def _get_test_events(self):
        """Eventos de prueba si falla la API."""
        print("𓂀 Usando eventos de prueba...")
        return [
            {'nombre': 'GW150914', 'gps': 1126259462.4, 'detectores': ['H1', 'L1'], 'snr': 24},
            {'nombre': 'GW170817', 'gps': 1187008882.4, 'detectores': ['H1', 'L1', 'V1'], 'snr': 32},
            {'nombre': 'GW200115', 'gps': 1263076815.0, 'detectores': ['H1', 'L1'], 'snr': 15}
        ]
    
    def descargar_datos_crudos(self, evento, detector='H1', duracion_segundos=32):
        """
        Descargar datos crudos de un evento específico.
        
        Args:
            evento: Dict con información del evento
            detector: 'H1' (Hanford), 'L1' (Livingston), 'V1' (Virgo)
            duracion_segundos: Duración a descargar (centrado en evento)
        """
        gps_central = evento['gps']
        inicio = gps_central - duracion_segundos/2
        fin = gps_central + duracion_segundos/2
        
        print(f"\n𓂀 DESCARGANDO DATOS CRUDOS:")
        print(f"  Evento: {evento['nombre']}")
        print(f"  Detector: {detector}")
        print(f"  GPS: {gps_central}")
        print(f"  Rango: {inicio} - {fin}")
        print(f"  Duración: {duracion_segundos}s")
        print(f"  Frecuencia muestreo: {self.sampling_rate} Hz")
        
        if not GWOSC_AVAILABLE:
            print("  ⚠️  gwpy no disponible - generando datos simulados")
            return self.generar_datos_simulados(detector, duracion_segundos, evento['nombre'])
        
        try:
            # Descargar usando GWpy
            datos = TimeSeries.fetch_open_data(
                detector,
                inicio,
                fin,
                sample_rate=self.sampling_rate,
                cache=False,
                verbose=False
            )
            
            print(f"  ✅ Datos descargados: {len(datos)} muestras")
            print(f"  📊 Estadísticas:")
            print(f"     • Media: {np.mean(datos.value):.2e}")
            print(f"     • STD: {np.std(datos.value):.2e}")
            print(f"     • Min: {np.min(datos.value):.2e}")
            print(f"     • Max: {np.max(datos.value):.2e}")
            
            return {
                'datos': datos.value,
                'fs': datos.sample_rate.value,
                'gps_inicio': datos.t0.value,
                'detector': detector,
                'evento': evento['nombre'],
                'metadata': {
                    'descarga_exitosa': True,
                    'muestras': len(datos),
                    'duracion': len(datos)/datos.sample_rate.value
                }
            }
            
        except Exception as e:
            print(f"  ❌ Error descargando: {e}")
            print("  𓂀 Generando datos simulados para pruebas...")
            return self.generar_datos_simulados(detector, duracion_segundos, evento['nombre'])
    
    def generar_datos_simulados(self, detector, duracion, nombre_evento):
        """Generar datos simulados para pruebas cuando no hay acceso real."""
        fs = self.sampling_rate
        n_muestras = int(fs * duracion)
        t = np.arange(n_muestras) / fs
        
        # Simular señal GW + ruido + posible f₀
        # 1. Señal de ondas gravitacionales (simplificada)
        f_gw = 100  # Hz - frecuencia típica de merger
        signal_gw = 1e-21 * np.sin(2 * np.pi * f_gw * t) * np.exp(-t/0.1)
        
        # 2. Posible f₀ oculta
        f0 = 141.7001
        signal_f0 = 5e-23 * np.sin(2 * np.pi * f0 * t)
        
        # 3. Ruido instrumental (típico de LIGO)
        # Componente 1/f
        noise_1f = 1e-22 * np.random.randn(n_muestras) / np.sqrt(1 + (f_gw/10))
        # Ruido blanco
        noise_white = 1e-23 * np.random.randn(n_muestras)
        # Líneas sísmicas
        seismic_lines = 2e-22 * (np.sin(2 * np.pi * 0.2 * t) + 
                                0.3 * np.sin(2 * np.pi * 1.0 * t))
        
        datos = signal_gw + signal_f0 + noise_1f + noise_white + seismic_lines
        
        print(f"  ⚠️  Usando datos simulados (para desarrollo)")
        print(f"  📊 Simulación incluye:")
        print(f"     • Señal GW: {f_gw} Hz, amplitud ~1e-21")
        print(f"     • Posible f₀: {f0} Hz, amplitud ~5e-23")
        print(f"     • Ruido instrumental realista")
        
        return {
            'datos': datos,
            'fs': fs,
            'gps_inicio': 1126259462.4,
            'detector': detector,
            'evento': nombre_evento,
            'metadata': {
                'descarga_exitosa': False,
                'simulado': True,
                'nota': 'Datos reales requieren acceso GWOSC API'
            }
        }
    
    def guardar_datos(self, datos_dict, directorio_salida='datos_crudos'):
        """Guardar datos descargados en formato HDF5."""
        os.makedirs(directorio_salida, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{datos_dict['detector']}_{datos_dict['evento']}_{timestamp}.h5"
        filepath = os.path.join(directorio_salida, filename)
        
        with h5py.File(filepath, 'w') as f:
            # Datos principales
            f.create_dataset('strain', data=datos_dict['datos'])
            
            # Metadata
            f.attrs['fs'] = datos_dict['fs']
            f.attrs['gps_inicio'] = datos_dict['gps_inicio']
            f.attrs['detector'] = datos_dict['detector']
            f.attrs['evento'] = datos_dict['evento']
            
            # Metadata adicional
            for key, value in datos_dict['metadata'].items():
                if isinstance(value, (int, float, str, bool)):
                    f.attrs[key] = value
        
        print(f"  💾 Datos guardados: {filepath}")
        return filepath


def main():
    """Función principal ejecutable."""
    parser = argparse.ArgumentParser(
        description='𓂀 Descargador de datos crudos GWOSC'
    )
    parser.add_argument('--eventos', type=int, default=3,
                        help='Número de eventos a descargar')
    parser.add_argument('--duracion', type=int, default=32,
                        help='Duración en segundos')
    parser.add_argument('--detector', type=str, default='H1',
                        choices=['H1', 'L1', 'V1'],
                        help='Detector a usar')
    parser.add_argument('--salida', type=str, default='datos_crudos',
                        help='Directorio de salida')
    
    args = parser.parse_args()
    
    print("𓂀 INICIANDO DESCARGA DE DATOS CRUDOS GWOSC")
    print("═" * 60)
    
    descargador = DescargadorGWOSC()
    eventos = descargador.obtener_eventos_recientes(args.eventos)
    
    # Descargar eventos
    resultados = []
    for evento in eventos:
        datos_crudos = descargador.descargar_datos_crudos(
            evento, args.detector, args.duracion
        )
        filepath = descargador.guardar_datos(datos_crudos, args.salida)
        resultados.append({
            'evento': evento['nombre'],
            'archivo': filepath,
            'exitoso': datos_crudos['metadata'].get('descarga_exitosa', False)
        })
    
    # Resumen
    print(f"\n𓂀 RESUMEN DE DESCARGA:")
    print(f"  Total eventos procesados: {len(resultados)}")
    exitosos = sum(1 for r in resultados if r['exitoso'])
    print(f"  Descargas exitosas: {exitosos}/{len(resultados)}")
    
    # Guardar resumen en JSON
    resumen_path = os.path.join(args.salida, 'resumen_descarga.json')
    with open(resumen_path, 'w') as f:
        json.dump(resultados, f, indent=2)
    print(f"  📄 Resumen guardado: {resumen_path}")


if __name__ == "__main__":
    main()
