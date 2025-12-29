#!/usr/bin/env python3
"""
Test script para analizar_igets_gravimetro.py

Valida la lógica del análisis sin descargar datos reales.
Genera datos sintéticos con señal a 141.7 Hz.
"""

import numpy as np
import sys
import os
import tempfile
from scipy.signal import welch

# Añadir el directorio scripts al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))


def generar_datos_sinteticos(duracion=3600, fs=1.0, f_signal=141.7,
                             amplitud_signal=1.0, ruido_std=5.0):
    """
    Genera datos sintéticos de gravímetro con señal a frecuencia específica.

    Args:
        duracion (float): Duración en segundos
        fs (float): Frecuencia de muestreo [Hz]
        f_signal (float): Frecuencia de la señal [Hz]
        amplitud_signal (float): Amplitud de la señal [µGal]
        ruido_std (float): Desviación estándar del ruido [µGal]

    Returns:
        tuple: (tiempo, gravedad)
    """
    n_samples = int(duracion * fs)
    t = np.arange(n_samples) / fs

    # Componente de señal
    signal = amplitud_signal * np.sin(2 * np.pi * f_signal * t)

    # Componente de ruido
    noise = ruido_std * np.random.randn(n_samples)

    # Tendencia lenta
    trend = 100 * np.sin(2 * np.pi * 0.001 * t)

    # Combinar
    g = signal + noise + trend + 1000.0  # offset

    return t, g


def test_filtrado_tendencia():
    """Test: Filtrado de tendencia elimina valor medio."""
    print("\n[TEST] Filtrado de tendencia...")

    g = np.array([100, 105, 95, 110, 90, 100])
    g_filtered = g - np.mean(g)

    assert abs(np.mean(g_filtered)) < 1e-10, "Filtrado debe eliminar media"
    print("✓ Filtrado de tendencia: OK")
    return True


def test_analisis_espectral_sintetico():
    """Test: Análisis espectral detecta señal sintética."""
    print("\n[TEST] Análisis espectral con datos sintéticos...")

    # Generar datos con señal a 141.7 Hz
    f_signal = 141.7
    fs = 1000.0  # 1000 Hz de muestreo (necesario para detectar 141.7 Hz)
    duracion = 100  # 100 segundos para buena resolución

    t, g = generar_datos_sinteticos(duracion=duracion, fs=fs,
                                    f_signal=f_signal,
                                    amplitud_signal=2.0, ruido_std=1.0)

    # Filtrar tendencia
    g_filtered = g - np.mean(g)

    # Análisis espectral
    f, Pxx = welch(g_filtered, fs, nperseg=2048, scaling='density')

    # Buscar pico cerca de 141.7 Hz
    band = (f > 140) & (f < 143)
    idx_max = np.argmax(Pxx[band])
    f_peak = f[band][idx_max]

    print(f"  Frecuencia del pico detectado: {f_peak:.2f} Hz")
    print(f"  Frecuencia esperada: {f_signal} Hz")

    # Verificar que el pico está cerca de la señal inyectada
    assert abs(f_peak - f_signal) < 0.5, \
        f"Pico debe estar cerca de {f_signal} Hz"

    print("✓ Análisis espectral: OK")
    return True


def test_calculo_snr():
    """Test: Cálculo de SNR detecta señal sobre ruido."""
    print("\n[TEST] Cálculo de SNR...")

    # Generar datos con buena SNR
    f_signal = 141.7
    fs = 1000.0  # 1000 Hz de muestreo (necesario para detectar 141.7 Hz)
    duracion = 100

    t, g = generar_datos_sinteticos(duracion=duracion, fs=fs,
                                    f_signal=f_signal,
                                    amplitud_signal=5.0,  # señal fuerte
                                    ruido_std=1.0)

    # Análisis
    g_filtered = g - np.mean(g)
    f, Pxx = welch(g_filtered, fs, nperseg=2048, scaling='density')

    # Banda de señal (±0.5 Hz alrededor de 141.7 Hz)
    signal_band = (f > 141.2) & (f < 142.2)

    # Banda de ruido (130-140 Hz, lejos de la señal)
    noise_band = (f > 130) & (f < 140)

    # Calcular SNR
    signal_power = np.mean(Pxx[signal_band])
    noise_power = np.mean(Pxx[noise_band])
    snr = signal_power / noise_power

    print(f"  SNR calculado: {snr:.2f}")
    print(f"  Potencia señal: {signal_power:.2e}")
    print(f"  Potencia ruido: {noise_power:.2e}")

    # Con amplitud_signal=5 y ruido_std=1, esperamos SNR > 1
    assert snr > 1.0, "SNR debe ser > 1 con señal fuerte"

    print("✓ Cálculo de SNR: OK")
    return True


def test_script_con_datos_sinteticos():
    """Test: Script completo con archivo de datos sintéticos."""
    print("\n[TEST] Script completo con datos sintéticos...")

    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generar datos sintéticos
        t, g = generar_datos_sinteticos(duracion=100, fs=1000.0,
                                        f_signal=141.7,
                                        amplitud_signal=3.0,
                                        ruido_std=2.0)

        # Guardar en formato IGETS (dos columnas: tiempo, gravedad)
        data = np.column_stack([t, g])
        fname = os.path.join(tmpdir, "test_data.txt")
        np.savetxt(fname, data, fmt='%.6f')

        print(f"  Archivo de prueba creado: {fname}")
        print(f"  Puntos de datos: {len(t)}")

        # Importar funciones del script principal
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "igets_script",
            "/home/runner/work/141hz/141hz/scripts/analizar_igets_gravimetro.py"
        )
        igets_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(igets_module)

        # Leer datos
        t_read, g_read, fs = igets_module.leer_datos_gravimetro(fname)

        # Verificar lectura
        assert len(t_read) == len(t), "Datos leídos correctamente"
        assert abs(fs - 1000.0) < 1.0, "Frecuencia de muestreo correcta"

        # Filtrar
        g_filtered = igets_module.filtrar_tendencia(g_read)

        # Análisis espectral
        f, Pxx = igets_module.analisis_espectral(g_filtered, fs, nperseg=1024)

        # Calcular SNR
        snr = igets_module.calcular_snr(f, Pxx, f_signal=141.7)

        print(f"  SNR obtenido: {snr:.2f}")

        # Visualizar (sin mostrar)
        import matplotlib
        matplotlib.use('Agg')  # Backend no-interactivo

        output_plot = os.path.join(tmpdir, "test_spectrum.png")
        igets_module.visualizar_espectro(f, Pxx, f_signal=141.7,
                                         output_file=output_plot)

        assert os.path.exists(output_plot), "Gráfico debe generarse"
        print(f"  Gráfico generado: {output_plot}")

    print("✓ Script completo: OK")
    return True


def main():
    """Ejecuta todos los tests."""
    print("=" * 70)
    print("TEST SUITE: analizar_igets_gravimetro.py")
    print("=" * 70)

    tests = [
        test_filtrado_tendencia,
        test_analisis_espectral_sintetico,
        test_calculo_snr,
        test_script_con_datos_sinteticos,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__}: FAILED")
            print(f"  Error: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"RESULTADOS: {passed} tests passed, {failed} tests failed")
    print("=" * 70)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
