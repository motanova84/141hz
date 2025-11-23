#!/usr/bin/env python3
"""
Script para generar datos simulados para prueba del análisis
"""
import numpy as np
import h5py
import os

def crear_datos_simulados():
    """Crear datos simulados que incluyan una señal en 141.7 Hz"""
    # Configuración de la simulación
    duration = 32  # segundos
    sample_rate = 4096  # Hz
    n_samples = int(duration * sample_rate)
    
    # Crear array de tiempo
    tiempo = np.linspace(0, duration, n_samples)
    gps_start = 1126259446  # GPS start time similar a GW150914
    
    # Generar ruido gaussiano
    noise_level = 1e-18
    strain = np.random.normal(0, noise_level, n_samples)
    
    # Agregar señal artificial en 141.7 Hz
    signal_freq = 141.7
    signal_amplitude = 2e-18  # Ligeramente mayor al ruido
    signal = signal_amplitude * np.sin(2 * np.pi * signal_freq * tiempo)
    
    # Modular la señal para que aparezca principalmente en el ringdown
    # Asumiendo que el merger está en el centro
    merger_time = duration / 2
    ringdown_envelope = np.exp(-(tiempo - merger_time)**2 / (2 * 2**2))  # Gaussiana centrada
    ringdown_envelope[tiempo < merger_time] = 0  # Solo después del merger
    
    # Aplicar envolvente
    signal = signal * ringdown_envelope
    
    # Combinar ruido y señal
    total_strain = strain + signal
    
    return tiempo, total_strain, gps_start, 1.0/sample_rate

def main():
    # Obtener rutas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(project_dir, 'data', 'raw')
    
    # Crear directorio si no existe
    os.makedirs(data_dir, exist_ok=True)
    
    print("Generando datos simulados para prueba...")
    
    # Generar datos simulados
    tiempo, strain, gps_start, dt = crear_datos_simulados()
    
    # Guardar en formato HDF5 compatible con gwpy
    filename = os.path.join(data_dir, 'H1-GW150914-32s.hdf5')
    
    with h5py.File(filename, 'w') as hdf:
        # Crear grupo strain
        strain_group = hdf.create_group('strain')
        
        # Guardar datos en el formato esperado por gwpy
        strain_group.create_dataset('Strain', data=strain)
        strain_group.create_dataset('Xstart', data=gps_start)
        strain_group.create_dataset('Xspacing', data=dt)
        
        # Agregar metadatos
        strain_group.attrs['name'] = 'H1:GWOSC-4KHZ_R1_STRAIN'
        strain_group.attrs['channel'] = 'H1:DCS-CALIB_STRAIN_C02'
        strain_group.attrs['epoch'] = gps_start
        strain_group.attrs['sample_rate'] = 1.0/dt
    
    print(f"Datos simulados guardados en: {filename}")
    print(f"  - Duración: {len(strain) * dt:.1f} segundos")
    print(f"  - Frecuencia de muestreo: {1.0/dt:.0f} Hz")
    print(f"  - Señal inyectada en: 141.7 Hz")
    print("¡Generación completada!")

if __name__ == "__main__":
    main()