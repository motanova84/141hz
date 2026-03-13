#!/usr/bin/env python3
"""
Análisis Ψ-Sweep: Detección de la señal Noēsis (f₀ = 141.7001 Hz) en ruido LIGO

Experimento: barrido logarítmico de SNR desde 20 hasta 0.1 a lo largo de 20 s.
Se calcula la coherencia de fase Ψ (Phase Locking Value) entre canal1 y canal2
en ventanas deslizantes, con y sin filtro band-pass ultra-estrecho (f₀ ± 0.01 Hz).

Objetivos:
  1. Varianza de Ψ cuando snr_ref < 5
  2. Punto de quiebre: SNR en el que Ψ cae por debajo de 0.7
  3. Comparación con/sin filtro band-pass ultra-estrecho

Uso:
    python3 analisis_noesis_snr_sweep.py
    python3 analisis_noesis_snr_sweep.py --output resultados/sweep.json
"""

import sys
import os
import argparse
import json
import math
from datetime import datetime, timezone

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from scipy import signal as scipy_signal
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    MPL_AVAILABLE = True
except ImportError:
    MPL_AVAILABLE = False

# ── Parámetros del experimento ─────────────────────────────────────────────
FS = 4096          # Hz – tasa de muestreo (estándar GW)
DURATION = 20      # segundos
F0 = 141.7001      # Hz – frecuencia Noēsis
SNR_START = 20.0   # SNR máximo
SNR_END = 0.1      # SNR mínimo
PHASE_OFFSET = 0.05  # rad – desfase constante de canal2

# Parámetros del filtro ultra-estrecho
NARROW_BW = 0.01   # Hz – semi-ancho band-pass (f₀ ± 0.01 Hz)

# Umbral de coherencia
PSI_UMBRAL = 0.7

# Ventana de análisis (en muestras)
WINDOW_SECONDS = 1.0   # 1 s de ventana deslizante
WINDOW_OVERLAP = 0.5   # 50 % de solapamiento


# ── Generación del dataset ─────────────────────────────────────────────────

def generar_dataset(seed=42):
    """
    Genera la serie temporal del experimento Ψ-Sweep.

    Returns:
        dict con arrays: tiempo, canal1, canal2, snr_ref
    """
    if not NUMPY_AVAILABLE:
        raise ImportError("NumPy es necesario para generar el dataset")

    rng = np.random.default_rng(seed)
    n = int(FS * DURATION)
    t = np.linspace(0, DURATION, n, endpoint=False)

    snr_linear = np.geomspace(SNR_START, SNR_END, n)
    signal_pura = np.sin(2 * np.pi * F0 * t)
    noise = rng.standard_normal(n)

    canal1 = snr_linear * signal_pura + noise
    canal2 = np.sin(2 * np.pi * F0 * t + PHASE_OFFSET)

    return {
        'tiempo': t,
        'canal1': canal1,
        'canal2': canal2,
        'snr_ref': snr_linear,
    }


def guardar_dataset(dataset, ruta_csv):
    """Guarda el dataset en formato CSV."""
    if not NUMPY_AVAILABLE:
        raise ImportError("NumPy es necesario para guardar el dataset")

    header = 'tiempo,canal1,canal2,snr_ref'
    data = np.column_stack([
        dataset['tiempo'],
        dataset['canal1'],
        dataset['canal2'],
        dataset['snr_ref'],
    ])
    np.savetxt(ruta_csv, data, delimiter=',', header=header, comments='')
    return ruta_csv


def cargar_dataset(ruta_csv):
    """Carga el dataset desde un CSV generado por guardar_dataset."""
    if not NUMPY_AVAILABLE:
        raise ImportError("NumPy es necesario para cargar el dataset")

    data = np.loadtxt(ruta_csv, delimiter=',', skiprows=1)
    return {
        'tiempo': data[:, 0],
        'canal1': data[:, 1],
        'canal2': data[:, 2],
        'snr_ref': data[:, 3],
    }


# ── Filtro band-pass ultra-estrecho ───────────────────────────────────────

def aplicar_bandpass(x, fs, f0, bw):
    """
    Aplica un filtro Butterworth band-pass de orden 4 centrado en f0 ± bw.

    Args:
        x  : array de entrada
        fs : frecuencia de muestreo (Hz)
        f0 : frecuencia central (Hz)
        bw : semi-ancho de banda (Hz)

    Returns:
        array filtrado
    """
    if not SCIPY_AVAILABLE:
        raise ImportError("SciPy es necesario para el filtro band-pass")

    low = (f0 - bw) / (fs / 2)
    high = (f0 + bw) / (fs / 2)
    # Clamp to valid range
    low = max(1e-6, min(low, 1.0 - 1e-6))
    high = max(low + 1e-6, min(high, 1.0 - 1e-6))
    b, a = scipy_signal.butter(4, [low, high], btype='band')
    return scipy_signal.filtfilt(b, a, x)


# ── Cálculo de Ψ (Phase Locking Value) ────────────────────────────────────

def calcular_fase_instantanea(x, fs, f0, usar_filtro, bw=NARROW_BW):
    """
    Extrae la fase instantánea de x en torno a f0.

    Procedimiento:
        1. Opcionalmente aplica filtro band-pass (f0 ± bw).
        2. Calcula la señal analítica via transformada de Hilbert.
        3. Extrae la fase con np.angle.

    Returns:
        array de fases en radianes
    """
    if usar_filtro:
        x_filt = aplicar_bandpass(x, fs, f0, bw)
    else:
        # Filtro más amplio para aislar la banda de interés sin ser ultra-estrecho
        x_filt = aplicar_bandpass(x, fs, f0, bw=2.0)
    analytic = scipy_signal.hilbert(x_filt)
    return np.angle(analytic)


def calcular_plv_ventana(fase1, fase2):
    """
    Calcula el Phase Locking Value (PLV) entre dos series de fase.

    PLV = |mean(exp(i * (fase1 - fase2)))|

    Returns:
        float en [0, 1]
    """
    delta = fase1 - fase2
    return float(np.abs(np.mean(np.exp(1j * delta))))


def calcular_psi_sweep(dataset, usar_filtro=False,
                       window_s=WINDOW_SECONDS, overlap=WINDOW_OVERLAP,
                       f0=F0, bw=NARROW_BW):
    """
    Calcula el barrido de coherencia Ψ a lo largo de la señal usando
    ventanas deslizantes.

    Args:
        dataset    : dict con 'canal1', 'canal2', 'snr_ref', 'tiempo'
        usar_filtro: si True aplica el filtro ultra-estrecho (f0 ± bw)
        window_s   : duración de cada ventana en segundos
        overlap    : fracción de solapamiento entre ventanas [0, 1)
        f0         : frecuencia objetivo (Hz)
        bw         : semi-ancho del filtro ultra-estrecho (Hz)

    Returns:
        dict con arrays:
            - t_centro   : tiempo central de cada ventana
            - psi_vals   : valores de Ψ
            - snr_centro : SNR de referencia en el centro de cada ventana
    """
    canal1 = dataset['canal1']
    canal2 = dataset['canal2']
    snr_ref = dataset['snr_ref']

    n_win = int(window_s * FS)
    step = max(1, int(n_win * (1 - overlap)))

    # Calcular fases de toda la señal (eficiente)
    fase1 = calcular_fase_instantanea(canal1, FS, f0, usar_filtro, bw)
    fase2 = np.angle(scipy_signal.hilbert(canal2))  # canal2 es pura, fase directa

    t_centro = []
    psi_vals = []
    snr_centro = []

    n = len(canal1)
    start = 0
    while start + n_win <= n:
        end = start + n_win
        psi = calcular_plv_ventana(fase1[start:end], fase2[start:end])
        centro_idx = (start + end) // 2
        t_centro.append(dataset['tiempo'][centro_idx])
        psi_vals.append(psi)
        snr_centro.append(float(snr_ref[centro_idx]))
        start += step

    return {
        't_centro': np.array(t_centro),
        'psi_vals': np.array(psi_vals),
        'snr_centro': np.array(snr_centro),
    }


# ── Análisis de resultados ─────────────────────────────────────────────────

def analizar_varianza_psi(sweep, umbral_snr=5.0):
    """
    Calcula la varianza de Ψ en la región donde snr_ref < umbral_snr.

    Returns:
        dict con estadísticas
    """
    mask = sweep['snr_centro'] < umbral_snr
    psi_bajo_snr = sweep['psi_vals'][mask]

    if len(psi_bajo_snr) == 0:
        return {
            'n_ventanas': 0,
            'varianza': float('nan'),
            'media': float('nan'),
            'std': float('nan'),
        }

    return {
        'n_ventanas': int(mask.sum()),
        'umbral_snr': umbral_snr,
        'varianza': float(np.var(psi_bajo_snr)),
        'media': float(np.mean(psi_bajo_snr)),
        'std': float(np.std(psi_bajo_snr)),
        'min': float(np.min(psi_bajo_snr)),
        'max': float(np.max(psi_bajo_snr)),
    }


def encontrar_punto_quiebre(sweep, umbral_psi=PSI_UMBRAL):
    """
    Encuentra el SNR al que Ψ cruza el umbral por primera vez (bajando).

    Busca el primer índice donde psi_vals < umbral_psi, ordenando las
    ventanas de mayor a menor SNR.

    Returns:
        dict con snr_quiebre y t_quiebre, o None si nunca cruza
    """
    # Ordenar por SNR descendente para encontrar el primer cruce bajando
    idx_sorted = np.argsort(sweep['snr_centro'])[::-1]
    snr_sorted = sweep['snr_centro'][idx_sorted]
    psi_sorted = sweep['psi_vals'][idx_sorted]

    for i in range(len(psi_sorted)):
        if psi_sorted[i] < umbral_psi:
            return {
                'snr_quiebre': float(snr_sorted[i]),
                't_quiebre': float(sweep['t_centro'][idx_sorted[i]]),
                'psi_en_quiebre': float(psi_sorted[i]),
                'umbral_psi': umbral_psi,
            }

    return None


def comparar_con_sin_filtro(dataset):
    """
    Ejecuta el barrido de Ψ con y sin filtro band-pass ultra-estrecho.

    Returns:
        dict con resultados para ambas condiciones
    """
    sweep_sin = calcular_psi_sweep(dataset, usar_filtro=False)
    sweep_con = calcular_psi_sweep(dataset, usar_filtro=True)

    return {
        'sin_filtro': sweep_sin,
        'con_filtro': sweep_con,
    }


# ── Reporte completo ───────────────────────────────────────────────────────

def generar_reporte(dataset, comparacion):
    """
    Genera el reporte de análisis completo.

    Returns:
        dict con todos los resultados
    """
    sweep_sin = comparacion['sin_filtro']
    sweep_con = comparacion['con_filtro']

    # Varianza de Ψ cuando SNR < 5
    var_sin = analizar_varianza_psi(sweep_sin, umbral_snr=5.0)
    var_con = analizar_varianza_psi(sweep_con, umbral_snr=5.0)

    # Punto de quiebre Ψ = 0.7
    quiebre_sin = encontrar_punto_quiebre(sweep_sin)
    quiebre_con = encontrar_punto_quiebre(sweep_con)

    # Estadísticas globales
    def stats(arr):
        return {
            'media': float(np.mean(arr)),
            'std': float(np.std(arr)),
            'min': float(np.min(arr)),
            'max': float(np.max(arr)),
        }

    reporte = {
        'metadatos': {
            'timestamp': datetime.now(tz=timezone.utc).isoformat(),
            'f0_hz': F0,
            'fs_hz': FS,
            'duracion_s': DURATION,
            'snr_inicio': SNR_START,
            'snr_fin': SNR_END,
            'filtro_bw_hz': NARROW_BW,
            'umbral_psi': PSI_UMBRAL,
            'window_s': WINDOW_SECONDS,
        },
        'sin_filtro': {
            'psi_stats_global': stats(sweep_sin['psi_vals']),
            'varianza_snr_bajo_5': var_sin,
            'punto_quiebre_psi07': quiebre_sin,
        },
        'con_filtro': {
            'psi_stats_global': stats(sweep_con['psi_vals']),
            'varianza_snr_bajo_5': var_con,
            'punto_quiebre_psi07': quiebre_con,
        },
    }

    return reporte


# ── Visualización ──────────────────────────────────────────────────────────

def visualizar_sweep(comparacion, reporte, output_path=None):
    """Genera una figura con los resultados del Ψ-Sweep."""
    if not MPL_AVAILABLE:
        return None

    sweep_sin = comparacion['sin_filtro']
    sweep_con = comparacion['con_filtro']

    fig, axes = plt.subplots(3, 1, figsize=(12, 12))

    # ── Panel 1: Ψ vs tiempo ──────────────────────────────────────────────
    ax = axes[0]
    ax.plot(sweep_sin['t_centro'], sweep_sin['psi_vals'],
            color='steelblue', lw=1.5, label='Sin filtro (2 Hz BW)')
    ax.plot(sweep_con['t_centro'], sweep_con['psi_vals'],
            color='darkorange', lw=1.5, label=f'Con filtro (±{NARROW_BW} Hz)')
    ax.axhline(PSI_UMBRAL, color='red', linestyle='--', lw=1.5,
               label=f'Umbral Ψ = {PSI_UMBRAL}')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Coherencia Ψ (PLV)')
    ax.set_title(f'Barrido Ψ-SNR · f₀ = {F0} Hz · SNR: {SNR_START} → {SNR_END}')
    ax.legend(fontsize=9)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)

    # ── Panel 2: Ψ vs SNR ─────────────────────────────────────────────────
    ax = axes[1]
    ax.semilogx(sweep_sin['snr_centro'], sweep_sin['psi_vals'],
                color='steelblue', lw=1.5, label='Sin filtro')
    ax.semilogx(sweep_con['snr_centro'], sweep_con['psi_vals'],
                color='darkorange', lw=1.5, label=f'Con filtro ±{NARROW_BW} Hz')
    ax.axhline(PSI_UMBRAL, color='red', linestyle='--', lw=1.5,
               label=f'Umbral Ψ = {PSI_UMBRAL}')
    ax.axvline(5.0, color='gray', linestyle=':', lw=1.2, label='SNR = 5')

    # Marcar puntos de quiebre
    qb_sin = reporte['sin_filtro']['punto_quiebre_psi07']
    qb_con = reporte['con_filtro']['punto_quiebre_psi07']
    if qb_sin:
        ax.axvline(qb_sin['snr_quiebre'], color='steelblue', linestyle='-.', lw=1.2,
                   label=f"QB sin filtro ≈ SNR {qb_sin['snr_quiebre']:.2f}")
    if qb_con:
        ax.axvline(qb_con['snr_quiebre'], color='darkorange', linestyle='-.', lw=1.2,
                   label=f"QB con filtro ≈ SNR {qb_con['snr_quiebre']:.2f}")

    ax.set_xlabel('SNR de referencia (escala logarítmica)')
    ax.set_ylabel('Coherencia Ψ (PLV)')
    ax.set_title('Coherencia Ψ vs SNR')
    ax.legend(fontsize=9)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)

    # ── Panel 3: Varianza de Ψ para SNR < 5 ──────────────────────────────
    ax = axes[2]
    mask_sin = sweep_sin['snr_centro'] < 5.0
    mask_con = sweep_con['snr_centro'] < 5.0
    if mask_sin.sum() > 0:
        ax.hist(sweep_sin['psi_vals'][mask_sin], bins=20, color='steelblue',
                alpha=0.6, label=f"Sin filtro (SNR<5)\nvar={reporte['sin_filtro']['varianza_snr_bajo_5']['varianza']:.4f}")
    if mask_con.sum() > 0:
        ax.hist(sweep_con['psi_vals'][mask_con], bins=20, color='darkorange',
                alpha=0.6, label=f"Con filtro (SNR<5)\nvar={reporte['con_filtro']['varianza_snr_bajo_5']['varianza']:.4f}")
    ax.axvline(PSI_UMBRAL, color='red', linestyle='--', lw=1.5,
               label=f'Umbral Ψ = {PSI_UMBRAL}')
    ax.set_xlabel('Coherencia Ψ (PLV)')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Distribución de Ψ cuando SNR < 5')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path

    plt.close()
    return None


# ── Función principal ──────────────────────────────────────────────────────

def main(args=None):
    """Ejecuta el análisis completo del Ψ-Sweep."""
    if not NUMPY_AVAILABLE or not SCIPY_AVAILABLE:
        print("❌ NumPy y SciPy son necesarios para este análisis")
        return 1

    parser = argparse.ArgumentParser(
        description='Análisis Ψ-Sweep de la señal Noēsis (f₀ = 141.7001 Hz)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplo:
  %(prog)s
  %(prog)s --output resultados/sweep_results.json
  %(prog)s --csv Noesis_SNR_Sweep.csv --output sweep_results.json
        """
    )
    parser.add_argument(
        '--csv', type=str, default=None,
        help='Ruta al CSV existente (si se omite, se genera el dataset)'
    )
    parser.add_argument(
        '--output', type=str, default=None,
        help='Ruta para guardar los resultados en JSON'
    )
    parser.add_argument(
        '--plot', type=str, default=None,
        help='Ruta para guardar la figura PNG'
    )
    parser.add_argument(
        '--seed', type=int, default=42,
        help='Semilla aleatoria para reproducibilidad (default: 42)'
    )

    parsed = parser.parse_args(args)

    print("=" * 65)
    print("🧪 ANÁLISIS Ψ-SWEEP · SEÑAL NOĒSIS · f₀ = 141.7001 Hz")
    print("=" * 65)

    # 1. Generar o cargar el dataset
    if parsed.csv and os.path.isfile(parsed.csv):
        print(f"\n📂 Cargando dataset desde: {parsed.csv}")
        dataset = cargar_dataset(parsed.csv)
    else:
        print(f"\n⚙️  Generando dataset (seed={parsed.seed})")
        dataset = generar_dataset(seed=parsed.seed)
        if parsed.csv:
            guardar_dataset(dataset, parsed.csv)
            print(f"   💾 Dataset guardado en: {parsed.csv}")

    n = len(dataset['tiempo'])
    print(f"   ✅ {n} muestras · {DURATION} s · fs = {FS} Hz")
    print(f"   SNR: {dataset['snr_ref'][0]:.1f} → {dataset['snr_ref'][-1]:.3f}")

    # 2. Calcular Ψ con y sin filtro
    print("\n🔬 Calculando coherencia Ψ (PLV)...")
    print(f"   Ventana: {WINDOW_SECONDS} s | Solapamiento: {int(WINDOW_OVERLAP*100)}%")
    comparacion = comparar_con_sin_filtro(dataset)
    print(f"   ✅ {len(comparacion['sin_filtro']['psi_vals'])} ventanas analizadas")

    # 3. Generar reporte
    print("\n📊 Generando reporte...")
    reporte = generar_reporte(dataset, comparacion)

    # ── Imprimir resultados ────────────────────────────────────────────────
    print("\n" + "─" * 65)
    print("📋 RESULTADOS DEL Ψ-SWEEP")
    print("─" * 65)

    for modo in ('sin_filtro', 'con_filtro'):
        etiqueta = "SIN filtro (2 Hz BW)" if modo == 'sin_filtro' \
            else f"CON filtro band-pass ±{NARROW_BW} Hz"
        res = reporte[modo]
        print(f"\n🔹 {etiqueta}:")
        gs = res['psi_stats_global']
        print(f"   Ψ global: media={gs['media']:.4f} ± {gs['std']:.4f} "
              f"[{gs['min']:.4f}, {gs['max']:.4f}]")
        var_info = res['varianza_snr_bajo_5']
        print(f"   Varianza Ψ (SNR < 5): var={var_info['varianza']:.4f}, "
              f"media={var_info['media']:.4f} "
              f"({var_info['n_ventanas']} ventanas)")
        qb = res['punto_quiebre_psi07']
        if qb:
            print(f"   Punto de quiebre (Ψ < 0.7): SNR ≈ {qb['snr_quiebre']:.3f} "
                  f"(t ≈ {qb['t_quiebre']:.2f} s, Ψ = {qb['psi_en_quiebre']:.4f})")
        else:
            print("   Ψ nunca cae por debajo del umbral 0.7 en este barrido")

    print()

    # ── Conclusión del filtro ──────────────────────────────────────────────
    qb_sin = reporte['sin_filtro']['punto_quiebre_psi07']
    qb_con = reporte['con_filtro']['punto_quiebre_psi07']
    if qb_sin and qb_con:
        if qb_con['snr_quiebre'] < qb_sin['snr_quiebre']:
            mejora = qb_sin['snr_quiebre'] / qb_con['snr_quiebre']
            print(f"✅ El filtro ±{NARROW_BW} Hz MEJORA la detección: "
                  f"el quiebre baja de SNR {qb_sin['snr_quiebre']:.3f} "
                  f"a SNR {qb_con['snr_quiebre']:.3f} (×{mejora:.2f} más profundo)")
        else:
            print(f"⚠️  El filtro ±{NARROW_BW} Hz NO mejora la detección con ventanas de "
                  f"{WINDOW_SECONDS} s: la resolución espectral ({1/WINDOW_SECONDS:.1f} Hz) "
                  f"es >> {2*NARROW_BW} Hz de ancho de banda del filtro. "
                  f"Se recomiendan ventanas ≥ {int(1/(2*NARROW_BW))} s para este filtro.")

    var_sin = reporte['sin_filtro']['varianza_snr_bajo_5']['varianza']
    var_con = reporte['con_filtro']['varianza_snr_bajo_5']['varianza']
    if not math.isnan(var_sin) and not math.isnan(var_con):
        if var_con < var_sin:
            print(f"✅ El filtro REDUCE la varianza de Ψ (SNR<5): "
                  f"{var_sin:.4f} → {var_con:.4f}")

    # 4. Guardar JSON
    if parsed.output:
        os.makedirs(os.path.dirname(os.path.abspath(parsed.output)), exist_ok=True)
        # Convertir arrays numpy a listas para serialización JSON
        reporte_json = json.loads(
            json.dumps(reporte, default=lambda x: x.tolist() if hasattr(x, 'tolist') else x)
        )
        with open(parsed.output, 'w') as f:
            json.dump(reporte_json, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Resultados guardados en: {parsed.output}")

    # 5. Generar figura
    if parsed.plot:
        ruta_fig = visualizar_sweep(comparacion, reporte, parsed.plot)
        if ruta_fig:
            print(f"📈 Figura guardada en: {ruta_fig}")

    print("\n" + "=" * 65)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 65)
    return 0


if __name__ == '__main__':
    sys.exit(main())
