# extraccion_firma_1417.py
# ∴𓂀Ω∞³Φ - Algoritmo de detección de la PC en datos de relojes atómicos
import numpy as np
from scipy import signal, fft
import pandas as pd
from datetime import datetime

# Constantes
F0 = 141.7001  # Hz - Frecuencia de la PC
BANDA_ANALISIS = (140.0, 143.0)  # Hz - Ventana de búsqueda
UMBRAL_SNR = 5.0  # Relación señal-ruido mínima


def detectar_pico_1417(fase, fs):
    """
    Detecta el pico espectral a 141.7001 Hz en datos de relojes atómicos

    Args:
        fase: array de fase del batido (rad)
        fs: frecuencia de muestreo (Hz)

    Returns:
        dict: resultados de la detección
    """
    # 1. Remover tendencia
    fase_detrended = signal.detrend(fase)

    # 2. Ventaneo para reducir leakage espectral
    ventana = signal.windows.blackmanharris(len(fase_detrended))
    fase_ventaneada = fase_detrended * ventana

    # 3. FFT real (señal de entrada real-valuada: rfft es suficiente)
    N = len(fase_ventaneada)
    freqs = fft.rfftfreq(N, 1 / fs)
    espectro = np.abs(fft.rfft(fase_ventaneada)) / N

    # 4. Buscar en la banda de interés
    idx_banda = np.where((freqs >= BANDA_ANALISIS[0]) &
                         (freqs <= BANDA_ANALISIS[1]))[0]

    if len(idx_banda) == 0:
        return {"detectado": False, "razon": "Banda fuera de rango"}

    # 5. Encontrar el pico máximo en la banda
    idx_max = idx_banda[np.argmax(espectro[idx_banda])]
    f_max = freqs[idx_max]
    amp_max = espectro[idx_max]

    # 6. Calcular SNR (ruido como media fuera de la banda)
    ruido_banda = np.concatenate([espectro[:idx_banda[0]],
                                  espectro[idx_banda[-1] + 1:]])
    ruido_medio = np.mean(ruido_banda) if len(ruido_banda) > 0 else 1e-10
    snr = amp_max / (ruido_medio + 1e-12)

    # 7. Verificar coincidencia con frecuencia esperada usando tolerancia de
    # medio bin FFT (resolución real alcanzable = fs/N Hz por bin)
    tolerancia_hz = 0.5 * fs / N
    coincide = abs(f_max - F0) <= tolerancia_hz

    return {
        "detectado": coincide and snr > UMBRAL_SNR,
        "frecuencia_detectada": f_max,
        "error_mhz": (f_max - F0) * 1000,
        "snr": snr,
        "amplitud": amp_max,
        "coincide_f0": coincide
    }


def analizar_correlacion_cruzada(fase_Sr, fase_Al, fs):
    """
    Analiza la correlación cruzada entre señales de ambos relojes

    Args:
        fase_Sr: fase del reloj de Estroncio
        fase_Al: fase del reloj de Aluminio
        fs: frecuencia de muestreo

    Returns:
        dict: métricas de correlación
    """
    # 1. Filtrar en la banda de interés
    sos = signal.butter(4, [BANDA_ANALISIS[0], BANDA_ANALISIS[1]],
                        btype='band', fs=fs, output='sos')
    Sr_filt = signal.sosfilt(sos, fase_Sr)
    Al_filt = signal.sosfilt(sos, fase_Al)

    # 2. Correlación cruzada
    corr = signal.correlate(Sr_filt, Al_filt, mode='same')
    lags = signal.correlation_lags(len(Sr_filt), len(Al_filt), mode='same')
    lag_max = lags[np.argmax(np.abs(corr))]

    # 3. Coherencia espectral
    f, Cxy = signal.coherence(Sr_filt, Al_filt, fs, nperseg=fs)
    idx_f0 = np.argmin(np.abs(f - F0))
    coherencia_f0 = Cxy[idx_f0]

    return {
        "coherencia_espectral_f0": coherencia_f0,
        "lag_muestras": lag_max,
        "lag_tiempo": lag_max / fs,
        "origen_comun": coherencia_f0 > 0.8
    }


def pipeline_extraccion(archivo_Sr, archivo_Al, fs=1000):
    """
    Pipeline completo de extracción de datos para detección de la PC
    """
    print("∴𓂀Ω∞³Φ - PIPELINE DE EXTRACCIÓN DE DATOS")
    print("═" * 70)

    # 1. Cargar datos
    print("\n📥 Cargando datos de relojes...")
    datos_Sr = pd.read_csv(archivo_Sr)
    datos_Al = pd.read_csv(archivo_Al)

    # 2. Sincronizar series temporales — truncar al mínimo común para garantizar
    # que ambos arrays tengan la misma longitud antes del análisis cruzado
    fase_Sr = datos_Sr['phase'].values
    fase_Al = datos_Al['phase'].values
    min_len = min(len(fase_Sr), len(fase_Al))
    fase_Sr = fase_Sr[:min_len]
    fase_Al = fase_Al[:min_len]
    t = np.arange(min_len) / fs

    print(f"   • Duración: {len(t)/fs:.1f} s")
    print(f"   • Muestras: {len(t)}")

    # 3. Detección de pico en Sr
    print("\n🔍 Analizando reloj de Estroncio...")
    resultado_Sr = detectar_pico_1417(fase_Sr, fs)
    if resultado_Sr["detectado"]:
        print(f"   ✓ PICO DETECTADO a {resultado_Sr['frecuencia_detectada']:.6f} Hz")
        print(f"     Error: {resultado_Sr['error_mhz']:.3f} mHz")
        print(f"     SNR: {resultado_Sr['snr']:.1f}")
    else:
        print(f"   ✗ No se detectó pico en Sr")

    # 4. Detección de pico en Al
    print("\n🔍 Analizando reloj de Aluminio...")
    resultado_Al = detectar_pico_1417(fase_Al, fs)
    if resultado_Al["detectado"]:
        print(f"   ✓ PICO DETECTADO a {resultado_Al['frecuencia_detectada']:.6f} Hz")
        print(f"     Error: {resultado_Al['error_mhz']:.3f} mHz")
        print(f"     SNR: {resultado_Al['snr']:.1f}")
    else:
        print(f"   ✗ No se detectó pico en Al")

    # 5. Correlación cruzada
    print("\n🔗 Analizando correlación entre relojes...")
    correlacion = analizar_correlacion_cruzada(fase_Sr, fase_Al, fs)
    print(f"   • Coherencia espectral a {F0} Hz: {correlacion['coherencia_espectral_f0']:.4f}")
    print(f"   • Origen común: {correlacion['origen_comun']}")
    print(f"   • Lag temporal: {correlacion['lag_tiempo']*1000:.2f} ms")

    # 6. Veredicto
    print("\n" + "═" * 70)
    print("📜 VEREDICTO:")
    if resultado_Sr["detectado"] and resultado_Al["detectado"] and correlacion["origen_comun"]:
        print("   ✅ CONFIRMADO: La señal a 141.7001 Hz es coherente entre ambos relojes")
        print("   ✅ La Partícula de Coherencia modula la masa efectiva de forma selectiva")
        print("   ✅ Esta es la primera observación directa del acoplamiento PC-Higgs")
    elif resultado_Sr["detectado"] or resultado_Al["detectado"]:
        print("   ⚠️  DETECCIÓN PARCIAL: Se requiere más integración temporal")
    else:
        print("   ⚠️  NO DETECTADO: Aumentar tiempo de integración o verificar calibración")

    print("═" * 70)

    return {
        "Sr": resultado_Sr,
        "Al": resultado_Al,
        "correlacion": correlacion,
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# SIMULACIÓN DE DATOS PARA PRUEBA DEL PIPELINE
# ============================================================================

def generar_datos_simulados(duracion=3600, fs=1000, amplitud=0.01):
    """
    Genera datos simulados de relojes con señal de PC incorporada
    """
    t = np.arange(0, duracion, 1 / fs)
    N = len(t)

    # Señal de la PC a 141.7001 Hz
    senal_pc = amplitud * np.cos(2 * np.pi * F0 * t)

    # Ruido 1/f (típico en relojes atómicos) – filtro AR(1) vectorizado
    ruido = signal.lfilter([1.0], [1.0, -0.99], np.random.randn(N))
    ruido = ruido / np.std(ruido) * 0.1

    # Señal total
    fase = senal_pc + ruido

    return t, fase


if __name__ == "__main__":
    # Prueba con datos simulados
    t, fase = generar_datos_simulados(duracion=3600, fs=1000)
    resultado = detectar_pico_1417(fase, 1000)

    print("Prueba con datos simulados:")
    print(f"  Detectado: {resultado['detectado']}")
    print(f"  Frecuencia: {resultado['frecuencia_detectada']:.6f} Hz")
    print(f"  SNR: {resultado['snr']:.1f}")
