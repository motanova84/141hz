#!/usr/bin/env python3
"""
Script para descargar datos de GWOSC para GW150914 (control)
"""
from gwpy.timeseries import TimeSeries
import os
import sys
import argparse

# Add parent directory to path to import user_confirmation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from user_confirmation import confirm_data_download, add_confirmation_args


def main(auto_yes=False):
    # Obtener la ruta base del proyecto (directorio padre del script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, 'data', 'raw')
    
    # Crear directorio de datos si no existe
    # Crear directorio de datos si no existe (ruta absoluta desde el script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data', 'raw')
    os.makedirs(data_dir, exist_ok=True)
    
    # Para GW150914 (control - datos reales disponibles)
    print("Descargando datos de control GW150914...")
    
    # Ask for user confirmation before downloading
    estimated_size_mb = 150.0  # Approximate size for 32s @ 4096 Hz for 2 detectors
    if not confirm_data_download(estimated_size_mb, auto_yes=auto_yes):
        print("Descarga cancelada por el usuario.")
        return
    
    try:
        # Datos de 32 segundos alrededor del merger
        gps_gw150914 = 1126259462  # Tiempo GPS del merger
        duration = 32  # segundos
        start = gps_gw150914 - 16
        end = gps_gw150914 + 16
        
        # Descargar datos de ambos detectores
        for detector in ['H1', 'L1']:
            print(f"Descargando {detector}...")
            data = TimeSeries.fetch_open_data(
                detector, start, end, sample_rate=4096, cache=True, verbose=True
            )
            # Guardar en formato HDF5
            filename = os.path.join(data_dir, f'{detector}-GW150914-32s.hdf5')
            data.write(filename, overwrite=True)
            print(f"Datos guardados en {filename}")
            
    except Exception as e:
        print(f"Error descargando datos: {e}")
        print("¿Estás conectado a internet?")
    
    print("¡Descarga completada!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Descarga datos de GWOSC para GW150914 (control)"
    )
    add_confirmation_args(parser)
    args = parser.parse_args()
    
    main(auto_yes=args.yes)
