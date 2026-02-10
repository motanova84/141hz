#!/usr/bin/env python3
"""
𓂀 DESCARGADOR DE DATOS IGETS/GFZ
Accede a datos gravimétricos crudos >1 Hz
"""

import numpy as np
import h5py
import argparse
import os
import json
from datetime import datetime, timedelta


class DescargadorIGETS:
    """Descarga datos gravimétricos crudos de IGETS/GFZ."""
    
    def __init__(self):
        self.base_url = "https://igets-data.gfz-potsdam.de"
        self.estaciones = {
            'BFO': {'nombre': 'Black Forest Observatory', 'pais': 'Alemania'},
            'STR': {'nombre': 'Strasbourg', 'pais': 'Francia'},
            'WET': {'nombre': 'Wettzell', 'pais': 'Alemania'},
            'CAN': {'nombre': 'Cantley', 'pais': 'Canadá'},
            'BEI': {'nombre': 'Beijiao', 'pais': 'China'}
        }
        
    def buscar_datos_crudos(self, estacion='BFO', fecha_inicio='2024-01-01', dias=1):
        """
        Buscar datos crudos disponibles.
        Nota: Requiere acceso FTP/API especial para datos >1 Hz
        """
        print(f"𓂀 BUSCANDO DATOS CRUDOS IGETS:")
        print(f"  Estación: {estacion} - {self.estaciones.get(estacion, {}).get('nombre', 'Desconocida')}")
        print(f"  Período: {fecha_inicio} (+{dias} días)")
        
        # URLs típicas para datos IGETS
        urls = [
            f"ftp://ftp.gfz-potsdam.de/pub/igets/{estacion}/",
            f"https://igets-data.gfz-potsdam.de/level1/{estacion}/",
            f"https://dataservices.gfz-potsdam.de/igets/showshort.php?id=escidoc:"
        ]
        
        print(f"  🔍 URLs de búsqueda:")
        for url in urls:
            print(f"     • {url}")
        
        print(f"\n  ⚠️  NOTA CRÍTICA:")
        print(f"     Los datos públicos suelen estar decimados a 1 minuto")
        print(f"     Se requiere contacto directo con operadores para:")
        print(f"     • Datos a 1 Hz o más (sin decimación)")
        print(f"     • Datos 'raw' o 'engineering' (sin filtro)")
        print(f"     • Acceso FTP a datos crudos binarios")
        
        # Simulación para desarrollo
        return self.simular_datos_gravimetricos(estacion, dias)
    
    def simular_datos_gravimetricos(self, estacion, dias):
        """Simular datos gravimétricos para desarrollo."""
        fs = 10  # Hz - típico de datos crudos gravimétricos
        n_muestras = int(fs * 86400 * dias)  # muestras por día
        
        t = np.arange(n_muestras) / fs
        
        # Señal gravimétrica típica
        # 1. Mareas terrestres (principal componente)
        f_marea = 1/(12*3600)  # ~12 horas
        signal_marea = 1e-8 * np.sin(2 * np.pi * f_marea * t)
        
        # 2. Posible f₀ oculta
        f0 = 141.7001
        signal_f0 = 1e-10 * np.sin(2 * np.pi * f0 * t)
        
        # 3. Ruido instrumental
        noise = 1e-9 * np.random.randn(n_muestras)
        
        # 4. Microsísmicos (0.1-1 Hz)
        microseismic = 5e-9 * np.sin(2 * np.pi * 0.2 * t)
        
        datos = signal_marea + signal_f0 + noise + microseismic
        
        print(f"  ⚠️  Generando datos simulados para desarrollo:")
        print(f"     • Fs: {fs} Hz")
        print(f"     • Muestras: {n_muestras:,}")
        print(f"     • Duración: {n_muestras/fs/3600:.1f} horas")
        print(f"     • Incluye f₀ simulada a {f0} Hz")
        
        return {
            'datos': datos,
            'fs': fs,
            'estacion': estacion,
            'fecha_inicio': fecha_inicio,
            'metadata': {
                'simulado': True,
                'nota': 'Datos reales requieren acceso especial IGETS',
                'muestras': n_muestras,
                'duracion_horas': n_muestras/fs/3600
            }
        }
    
    def guardar_datos(self, datos_dict, directorio_salida='datos_igets'):
        """Guardar datos en formato HDF5."""
        os.makedirs(directorio_salida, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"IGETS_{datos_dict['estacion']}_{timestamp}.h5"
        filepath = os.path.join(directorio_salida, filename)
        
        with h5py.File(filepath, 'w') as f:
            # Datos principales
            f.create_dataset('gravimetry', data=datos_dict['datos'])
            
            # Metadata
            f.attrs['fs'] = datos_dict['fs']
            f.attrs['estacion'] = datos_dict['estacion']
            f.attrs['fecha_inicio'] = datos_dict.get('fecha_inicio', '')
            
            # Metadata adicional
            for key, value in datos_dict['metadata'].items():
                if isinstance(value, (int, float, str, bool)):
                    f.attrs[key] = value
        
        print(f"  💾 Datos guardados: {filepath}")
        return filepath


def main():
    """Función principal ejecutable."""
    parser = argparse.ArgumentParser(
        description='𓂀 Descargador de datos IGETS/GFZ'
    )
    parser.add_argument('--estacion', type=str, default='BFO',
                        choices=['BFO', 'STR', 'WET', 'CAN', 'BEI'],
                        help='Estación gravimétrica')
    parser.add_argument('--fecha', type=str, default='2024-01-01',
                        help='Fecha de inicio (YYYY-MM-DD)')
    parser.add_argument('--dias', type=int, default=1,
                        help='Número de días a descargar')
    parser.add_argument('--salida', type=str, default='datos_igets',
                        help='Directorio de salida')
    
    args = parser.parse_args()
    
    print("𓂀 INICIANDO DESCARGA DE DATOS IGETS/GFZ")
    print("═" * 60)
    
    descargador = DescargadorIGETS()
    datos_grav = descargador.buscar_datos_crudos(
        args.estacion, args.fecha, args.dias
    )
    
    filepath = descargador.guardar_datos(datos_grav, args.salida)
    
    print(f"\n𓂀 DATOS LISTOS PARA ANÁLISIS:")
    print(f"  Archivo: {filepath}")
    print(f"  Muestras: {datos_grav['metadata']['muestras']:,}")
    print(f"  Duración: {datos_grav['metadata']['duracion_horas']:.2f} horas")


if __name__ == "__main__":
    main()
