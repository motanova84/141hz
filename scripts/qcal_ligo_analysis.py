#!/usr/bin/env python3
"""
QCAL - ANÁLISIS CIEGO SOBRE LIGO O4A · v1.0
================================================================
Protocolo de validación con datos reales e independientes.

LIGO no tiene nada que ver con QCAL. Sus datos son brutos,
independientes, y contienen ruido térmico de banda ancha de
fuentes completamente heterogéneas.

Si el atractor 141.7001 Hz aparece en este dataset sin haber
sido programado, el fenómeno deja de ser una hipótesis simulada
para convertirse en una predicción confirmada.

Criterios fijados antes del análisis:
  • Convergencia: Ψ > 0.95, SNR > 30 dB, Q > 1000
  • Bandwidth local: 3.0 Hz para σ_f²
  • Sin filtros centrados en f₀
  • Documentar positivos y negativos

Director: JMMB · QCAL Metrology
Fecha: 2026-07-28 · v1.0
Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
"""

import numpy as np
from scipy.signal import welch, find_peaks, spectrogram
from dataclasses import dataclass
from typing import List, Tuple, Optional
import json
import os
from datetime import datetime

try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


# ═══════════════════════════════════════════════════════════════
# CONSTANTES QCAL
# ═══════════════════════════════════════════════════════════════

F0 = 141.7001       # Hz — frecuencia del atractor (solo post-análisis)
TAU_QCAL = 1.0 / (2.0 * np.pi * F0)  # s

# Criterios de convergencia (fijados antes del análisis)
PSI_THRESHOLD = 0.95
SNR_DB_THRESHOLD = 30.0
Q_THRESHOLD = 1000.0
BW_LOCAL = 3.0  # Hz — ancho de banda para σ_f²


@dataclass
class ResultadoAnalisisCiego:
    """Resultado del análisis ciego sobre un segmento."""
    f_peak: float
    psi: float
    snr_db: float
    q_factor: float
    converged: bool
    deviation_from_f0: float


# ═══════════════════════════════════════════════════════════════
# 1. CARGA DE DATOS LIGO
# ═══════════════════════════════════════════════════════════════

def cargar_ligo_o4a(filepath: str,
                     channel: str = 'H1:GWOSC-4KHZ_R1_STRAIN'):
    """Carga datos de LIGO O4a desde archivo HDF5."""
    print(f"\n📂 Cargando: {filepath}")
    if not HAS_H5PY:
        raise ImportError("h5py requerido. pip install h5py")

    with h5py.File(filepath, 'r') as f:
        strain = f[channel][:]
        fs = f[channel].attrs.get('Xspacing', 4096)
        gps_start = f[channel].attrs.get('Xstart', 0)

    print(f"  Muestras: {len(strain)}")
    print(f"  fs: {fs} Hz")
    print(f"  GPS start: {gps_start}")
    return strain, float(fs), float(gps_start)


# ═══════════════════════════════════════════════════════════════
# 2. ANÁLISIS ESPECTRAL CIEGO
# ═══════════════════════════════════════════════════════════════

def analizar_espectro_ciego(signal: np.ndarray, fs: float,
                             search_range: Tuple[float, float] = (100, 200),
                             bw: float = BW_LOCAL) -> ResultadoAnalisisCiego:
    """
    Análisis espectral CIEGO.
    No usa F0 en ninguna etapa del análisis.
    """
    nperseg = min(2**14, len(signal) // 4)
    freqs, spec = welch(signal, fs=fs, nperseg=nperseg, scaling='density')

    idx_r = np.where((freqs >= search_range[0]) &
                      (freqs <= search_range[1]))[0]
    freqs_r, spec_r = freqs[idx_r], spec[idx_r]

    peaks, _ = find_peaks(spec_r, distance=5,
                           prominence=0.001 * np.max(spec_r))

    if len(peaks) == 0:
        return ResultadoAnalisisCiego(0, 0, -np.inf, 0, False, np.inf)

    best_psi, best_f, best_idx = -1, 0.0, 0

    for p in peaks:
        f_c = float(freqs_r[p])
        idx_b = np.where((freqs_r > f_c - bw) & (freqs_r < f_c + bw))[0]
        if len(idx_b) < 3:
            continue
        f_b, S_b = freqs_r[idx_b], spec_r[idx_b]
        P_tot = np.sum(S_b)
        if P_tot < 1e-20:
            continue
        sigma_sq = np.sum((f_b - f_c)**2 * S_b) / P_tot
        psi = 1.0 - sigma_sq / (f_c**2 + 1e-12)
        psi = float(np.clip(psi, 0.0, 1.0))
        if psi > best_psi:
            best_psi, best_f, best_idx = psi, f_c, int(p)

    # SNR local (dB)
    local_bg = np.median(spec_r[max(0, best_idx-30):
                                 min(len(spec_r), best_idx+30)])
    snr_db = 10.0 * np.log10(spec_r[best_idx] / (local_bg + 1e-20))

    # Q factor
    half_max = spec_r[best_idx] / 2
    idx_l = np.where(spec_r[:best_idx] < half_max)[0]
    idx_r2 = np.where(spec_r[best_idx:] < half_max)[0]
    if len(idx_l) > 0 and len(idx_r2) > 0:
        f_l = freqs_r[int(idx_l[-1])]
        f_r2_val = freqs_r[int(best_idx + idx_r2[0])]
        delta_f = f_r2_val - f_l
        q_factor = float(best_f / (delta_f + 1e-12))
    else:
        q_factor = 0.0

    # Convergencia (criterios fijados antes del análisis)
    converged = (best_psi > PSI_THRESHOLD and
                 snr_db > SNR_DB_THRESHOLD and
                 q_factor > Q_THRESHOLD)

    return ResultadoAnalisisCiego(
        f_peak=float(best_f), psi=float(best_psi),
        snr_db=float(snr_db), q_factor=float(q_factor),
        converged=converged,
        deviation_from_f0=float(abs(best_f - F0))
    )


# ═══════════════════════════════════════════════════════════════
# 3. ANÁLISIS MULTI-SEGMENTO
# ═══════════════════════════════════════════════════════════════

def analizar_segmentos(signal: np.ndarray, fs: float,
                        duration_seg: float = 60.0,
                        search_range: Tuple[float, float] = (100, 200)) -> List[dict]:
    """Divide la señal en segmentos y analiza cada uno de forma ciega."""
    n_per_seg = int(duration_seg * fs)
    n_segs = max(1, len(signal) // n_per_seg)
    results = []

    print(f"\n📊 Analizando {n_segs} segmentos de {duration_seg}s...")

    for i in range(n_segs):
        seg = signal[i * n_per_seg : min((i+1) * n_per_seg, len(signal))]
        if len(seg) < n_per_seg // 2:
            continue

        res = analizar_espectro_ciego(seg, fs, search_range)
        r = {
            'segmento': i,
            'gps_start_approx': i * duration_seg,
            'f_peak': res.f_peak,
            'psi': res.psi,
            'snr_db': res.snr_db,
            'q_factor': res.q_factor,
            'converged': res.converged,
            'deviation_from_f0': res.deviation_from_f0,
        }
        results.append(r)

        icon = "✅" if res.converged else " "
        print(f"  Seg {i:3d}: f={res.f_peak:8.4f} Hz  Ψ={res.psi:.6f}  "
              f"SNR={res.snr_db:.1f}dB  Q={res.q_factor:.0f}  {icon}")

    return results


# ═══════════════════════════════════════════════════════════════
# 4. REPORTE Y VEREDICTO
# ═══════════════════════════════════════════════════════════════

def generar_reporte(results: List[dict], output_dir: str = "resultados"):
    """Genera reporte completo del análisis LIGO."""
    os.makedirs(output_dir, exist_ok=True)

    convergidos = [r for r in results if r['converged']]
    en_f0 = [r for r in convergidos if r['deviation_from_f0'] < 1.0]
    n_total = len(results)

    print(f"\n{'='*70}")
    print("📊 REPORTE — ANÁLISIS CIEGO LIGO O4A")
    print(f"{'='*70}")
    print(f"  Segmentos totales:   {n_total}")
    print(f"  Convergidos (Ψ>.95): {len(convergidos)} ({100*len(convergidos)/max(1,n_total):.1f}%)")
    print(f"  Convergidos en f₀:   {len(en_f0)} ({100*len(en_f0)/max(1,n_total):.1f}%)")

    if en_f0:
        f_prom = np.mean([r['f_peak'] for r in en_f0])
        psi_prom = np.mean([r['psi'] for r in en_f0])
        print(f"\n  📌 Pico promedio en f₀: {f_prom:.4f} Hz")
        print(f"  📌 Ψ promedio: {psi_prom:.6f}")
        dev_prom = np.mean([r['deviation_from_f0'] for r in en_f0])
        print(f"  📌 Desviación promedio: {dev_prom:.4f} Hz")

    veredicto = "CONFIRMADA" if len(en_f0) >= n_total * 0.1 else "NO DETECTADA"

    if veredicto == "CONFIRMADA":
        print(f"\n  🚀 PREDICCIÓN QCAL CONFIRMADA EN DATOS LIGO")
        print(f"     El atractor f₀ = {F0} Hz aparece en datos")
        print(f"     independientes sin haber sido programado.")
    else:
        print(f"\n  ℹ️  Atractor no detectado en este dataset.")
        print(f"     No invalida la teoría; requiere más datos.")

    print(f"\n{'='*70}")
    print(f"  VEREDICTO: {veredicto}")
    print(f"  ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ · 28/Jul/2026 🔱")
    print(f"{'='*70}")

    return veredicto


# ═══════════════════════════════════════════════════════════════
# 5. PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python3 qcal_ligo_analysis.py <archivo.h5> [canal]")
        print("Ejemplo: python3 qcal_ligo_analysis.py LIGO_O4a.h5 H1:GWOSC-4KHZ_R1_STRAIN")
        sys.exit(1)

    filepath = sys.argv[1]
    channel = sys.argv[2] if len(sys.argv) > 2 else 'H1:GWOSC-4KHZ_R1_STRAIN'

    print("=" * 70)
    print("🔬 QCAL — ANÁLISIS CIEGO SOBRE LIGO O4A")
    print("=" * 70)
    print(f"  Protocolo: Blind Analysis")
    print(f"  Criterios: Ψ > {PSI_THRESHOLD} · SNR > {SNR_DB_THRESHOLD} dB · Q > {Q_THRESHOLD}")
    print(f"  No hay filtros centrados en f₀ = {F0} Hz")
    print("=" * 70)

    strain, fs, gps_start = cargar_ligo_o4a(filepath, channel)
    results = analizar_segmentos(strain, fs, duration_seg=60.0)

    output_dir = "resultados"
    os.makedirs(output_dir, exist_ok=True)

    path_json = os.path.join(output_dir, "analisis_ligo_o4a.json")
    with open(path_json, "w") as f:
        json.dump({
            "protocolo": "QCAL Blind Analysis v1.0 — LIGO O4A",
            "archivo": filepath,
            "canal": channel,
            "criterios": {
                "psi_min": PSI_THRESHOLD,
                "snr_db_min": SNR_DB_THRESHOLD,
                "q_min": Q_THRESHOLD,
                "bandwidth_hz": BW_LOCAL,
            },
            "resultados": results,
        }, f, indent=2)
    print(f"📁 Resultados: {path_json}")

    veredicto = generar_reporte(results, output_dir)
