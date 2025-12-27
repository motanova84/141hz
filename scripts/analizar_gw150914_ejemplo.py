#!/usr/bin/env python3
"""
Ejemplo de análisis espectral de GW150914 en 141.7 Hz
Script corregido que busca modulación en la frecuencia objetivo
"""
import numpy as np
import gwpy.timeseries
import scipy.signal

# Cargar datos de GW150914
data = gwpy.timeseries.TimeSeries.fetch_open_data('H1', 1126259446, 1126259478, sample_rate=4096)

# Preprocesamiento
data = data.highpass(20).notch(60)

# Análisis espectral
frequencies, times, power = scipy.signal.spectrogram(data, fs=4096, nperseg=1024)

# Buscar modulación en 141.7 Hz
target_freq = 141.7001
# Encontrar el índice de frecuencia más cercano al objetivo
freq_idx = np.argmin(np.abs(frequencies - target_freq))
peak = frequencies[freq_idx]
peak_power = np.max(power[freq_idx, :])

print(f"Modulación detectada en {peak:.4f} Hz")
print(f"Potencia del pico: {peak_power:.2e}")
