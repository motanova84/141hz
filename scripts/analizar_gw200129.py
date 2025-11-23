#!/usr/bin/env python3
"""
Análisis de GW200129_065458 con PyCBC
Calcula las respuestas efectivas de detectores a 141.7 Hz

Este script analiza el evento GW200129_065458 y calcula las respuestas
efectivas (F_eff) de los detectores gravitacionales en la frecuencia 
objetivo de 141.7 Hz.

Detectores analizados:
- H1: LIGO Hanford
- L1: LIGO Livingston  
- V1: Virgo
- K1: KAGRA

Requiere:
    - pycbc >= 2.0.0
    - numpy >= 1.21.0

Uso:
    python scripts/analizar_gw200129.py
    
Salida:
    - Información del evento GW200129_065458
    - Respuestas efectivas de cada detector a 141.7 Hz
"""

import sys
import numpy as np

# Verificar que PyCBC está disponible
try:
    from pycbc.detector import Detector
    from pycbc.types import TimeSeries
except ImportError as e:
    print("❌ Error: PyCBC no está instalado o no se pudo importar")
    print(f"   Detalles: {e}")
    print("   Instalar con: pip install pycbc")
    sys.exit(1)


def calcular_respuesta_efectiva(detector_name, ra, dec, polarization, gps_time, freq):
    """
    Calcula la respuesta efectiva de un detector para una fuente específica.
    
    Args:
        detector_name: Nombre del detector ('H1', 'L1', 'V1', 'K1')
        ra: Ascensión recta de la fuente (radianes)
        dec: Declinación de la fuente (radianes)
        polarization: Ángulo de polarización (radianes)
        gps_time: Tiempo GPS del evento
        freq: Frecuencia objetivo (Hz)
    
    Returns:
        float: Respuesta efectiva F_eff del detector
    """
    try:
        # Crear objeto detector
        det = Detector(detector_name)
        
        # Calcular funciones de patrón de antena F+ y Fx
        fp, fc = det.antenna_pattern(ra, dec, polarization, gps_time)
        
        # Calcular respuesta efectiva combinada
        # F_eff = sqrt(F+^2 + Fx^2)
        f_eff = np.sqrt(fp**2 + fc**2)
        
        return f_eff
        
    except Exception as e:
        print(f"   ⚠️  Error calculando respuesta para {detector_name}: {e}")
        return 0.0


def analizar_gw200129():
    """
    Analiza el evento GW200129_065458 y calcula respuestas efectivas.
    """
    # Parámetros del evento GW200129_065458
    evento_nombre = "GW200129_065458"
    gps_time = 1264316116.4
    
    # Coordenadas del cielo para GW200129_065458
    # Basado en parámetros del catálogo GWOSC para GW200129_065458
    # RA: ~03h 25m (~51.25 deg = 0.894 rad)
    # Dec: ~-57.8 deg = -1.009 rad
    ra = 0.894  # Ascensión recta (radianes)
    dec = -1.009  # Declinación (radianes)
    polarization = 1.571  # Ángulo de polarización (radianes) ~90 grados
    
    # Frecuencia objetivo
    target_freq = 141.7  # Hz
    
    print(f"📍 Evento: {evento_nombre} — GPS: {gps_time}")
    print()
    
    # Lista de detectores a analizar
    detectores = ['H1', 'L1', 'V1', 'K1']
    
    print(f"🎯 Respuesta efectiva a {target_freq} Hz:")
    
    resultados = {}
    
    for det_name in detectores:
        try:
            # Calcular respuesta efectiva
            f_eff = calcular_respuesta_efectiva(
                det_name, ra, dec, polarization, gps_time, target_freq
            )
            
            resultados[det_name] = f_eff
            print(f"  {det_name}: F_eff = {f_eff:.4f}")
            
        except Exception as e:
            print(f"  {det_name}: Error - {e}")
            resultados[det_name] = 0.0
    
    return 0


def main():
    """Función principal"""
    try:
        return analizar_gw200129()
    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis interrumpido por el usuario")
        return 1
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
