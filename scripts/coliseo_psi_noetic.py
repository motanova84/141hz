#!/usr/bin/env python3
"""
Coliseo PSI Noético - Definición canónica de D_Ψ y D_SNR

Implementa las métricas de detección coherente según el protocolo Oro:

    D_SNR = ∫(f0-bw to f0+bw) Pxx(f) df  /  ∫(f0+2bw to f0+4bw) Pxx(f) df
            (ratio on-band / off-band — SNR real, no potencia absoluta)

    D_Coh = coherencia media en banda [f0-bw, f0+bw]

    D_Ψ   = D_SNR · D_Coh²

Cuatro escenarios de validación:
    1. Ideal: señal común en ambos canales, ruido independiente
    2. Realista: señal común + desfase variable (jitter de fase)
    3. Glitch local: spike solo en canal 1
    4. Ruido parcialmente correlacionado: n2 = ρ·n1 + √(1-ρ²)·ε

Salida: AUC por escenario (no σ sin calibración).
Benchmark: ratio score(f0) / score(f_control), con f_control = f0 + 50 Hz por defecto.

Author: JMMB Ψ✧ / Copilot
"""

import argparse
import numpy as np
from scipy import signal
from scipy.signal import coherence as scipy_coherence

# ─────────────────────────── constantes ────────────────────────────────────
F0_DEFAULT = 141.7001   # Hz
BW_DEFAULT = 5.0        # Hz — semiancho de banda (≥1/T_min para ser resoluble)
FS_DEFAULT = 4096       # Hz
F_CONTROL_OFFSET = 50.0 # Hz — desplazamiento para frecuencia de control
EPSILON = 1e-30         # Epsilon universal para guards de división por cero

# Función trapz compatible con NumPy 1.x y 2.x
try:
    _trapz = np.trapezoid  # NumPy ≥2.0
except AttributeError:
    _trapz = np.trapz      # NumPy <2.0


# ═══════════════════════════════════════════════════════════════════════════
# Funciones métricas principales
# ═══════════════════════════════════════════════════════════════════════════

def _integrate_band(pxx, freqs, f_low, f_high):
    """Integra pxx entre f_low y f_high usando la regla del trapecio.

    Parámetros
    ----------
    pxx, freqs : array-like
        Densidad espectral y vector de frecuencias.
    f_low, f_high : float
        Límites de la banda (Hz).

    Retorna
    -------
    float
        Potencia integrada en la banda (unidades²).
    """
    mask = (freqs >= f_low) & (freqs <= f_high)
    if mask.sum() > 1:
        return float(_trapz(pxx[mask], freqs[mask]))
    df = freqs[1] - freqs[0]
    return float(pxx[mask].sum() * df)


def calcular_snr_potencia(pxx, freqs, f0=F0_DEFAULT, bw=BW_DEFAULT):
    """Ratio on-band / off-band de potencia espectral.

    D_SNR = ∫(f0-bw, f0+bw) Pxx(f) df  /  ∫(f0+2bw, f0+4bw) Pxx(f) df

    Parámetros
    ----------
    pxx : array-like
        Densidad espectral de potencia (unidades²/Hz).
    freqs : array-like
        Vector de frecuencias correspondiente a pxx (Hz).
    f0 : float
        Frecuencia central de interés (Hz).
    bw : float
        Semiancho de banda (Hz).

    Retorna
    -------
    float
        D_SNR ≥ 0. Valores > 1 indican exceso de potencia en banda.
    """
    freqs = np.asarray(freqs)
    pxx = np.asarray(pxx)

    # Se requiere al menos dos bins de frecuencia para estimar df de forma fiable.
    if len(freqs) < 2:
        # No hay resolución espectral suficiente para un cálculo significativo de SNR.
        # Se devuelve un valor especial (NaN) en lugar de asumir un df arbitrario.
        return float("nan")

    # Validar que ambas bandas tienen soporte en freqs; si no, SNR no calculable.
    mask_on = (freqs >= f0 - bw) & (freqs <= f0 + bw)
    mask_off = (freqs >= f0 + 2 * bw) & (freqs <= f0 + 4 * bw)
    if mask_on.sum() == 0 or mask_off.sum() == 0:
        return float("nan")

    power_on = _integrate_band(pxx, freqs, f0 - bw, f0 + bw)
    power_off = _integrate_band(pxx, freqs, f0 + 2 * bw, f0 + 4 * bw)

    if power_off <= 0:
        return 0.0

    return power_on / power_off


def _compute_psd(x, fs):
    """PSD de máxima resolución para señales cortas (periodograma)."""
    freqs, pxx = signal.periodogram(x, fs=fs, scaling='density')
    return freqs, pxx


def calcular_psi_noetica(x1, x2, fs=FS_DEFAULT, f0=F0_DEFAULT, bw=BW_DEFAULT):
    """Métrica noética D_Ψ = D_SNR · D_Coh².

    Parámetros
    ----------
    x1, x2 : array-like
        Series temporales de dos canales/nodos.
    fs : float
        Frecuencia de muestreo (Hz).
    f0 : float
        Frecuencia central (Hz).
    bw : float
        Semiancho de banda (Hz).

    Retorna
    -------
    dict con claves:
        psi   : D_Ψ = D_SNR · D_Coh²
        d_snr : ratio on-band / off-band (canal x1)
        d_coh : coherencia media en banda
    """
    x1 = np.asarray(x1, dtype=float)
    x2 = np.asarray(x2, dtype=float)

    n = len(x1)
    # Usar periodograma (máxima resolución espectral) para D_SNR
    freqs, pxx = _compute_psd(x1, fs)
    d_snr = calcular_snr_potencia(pxx, freqs, f0=f0, bw=bw)

    # Coherencia cruzada — nperseg = n//2, sin exceder la longitud de la señal
    nperseg = min(max(32, n // 2), n)
    f_coh, cxy = scipy_coherence(x1, x2, fs=fs, nperseg=nperseg)
    mask_band = (f_coh >= f0 - bw) & (f_coh <= f0 + bw)
    d_coh = float(np.mean(cxy[mask_band])) if mask_band.sum() > 0 else 0.0

    psi = d_snr * (d_coh ** 2)

    return {"psi": psi, "d_snr": d_snr, "d_coh": d_coh}


# ═══════════════════════════════════════════════════════════════════════════
# Generadores de datos sintéticos para los cuatro escenarios
# ═══════════════════════════════════════════════════════════════════════════

def _make_signal(n, fs, f0, amp=1.0, phi=0.0):
    t = np.arange(n) / fs
    return amp * np.sin(2 * np.pi * f0 * t + phi)


def generar_par_escenario1(n, fs, f0, amp, snr_rms):
    """Escenario 1 — Ideal: señal común, ruido independiente."""
    noise_std = amp / snr_rms if snr_rms > 0 else amp
    s = _make_signal(n, fs, f0, amp)
    x1 = s + np.random.normal(0, noise_std, n)
    x2 = s + np.random.normal(0, noise_std, n)
    return x1, x2


def generar_par_escenario2(n, fs, f0, amp, snr_rms, sigma_phi=0.5):
    """Escenario 2 — Realista: jitter de fase entre canales."""
    noise_std = amp / snr_rms if snr_rms > 0 else amp
    phi = np.random.normal(0, sigma_phi)
    x1 = _make_signal(n, fs, f0, amp, phi=0.0) + np.random.normal(0, noise_std, n)
    x2 = _make_signal(n, fs, f0, amp, phi=phi) + np.random.normal(0, noise_std, n)
    return x1, x2


def generar_par_escenario3(n, fs, f0, amp, snr_rms, glitch_amp_factor=10.0):
    """Escenario 3 — Glitch local: spike solo en canal 1."""
    noise_std = amp / snr_rms if snr_rms > 0 else amp
    s = _make_signal(n, fs, f0, amp)
    x1 = s + np.random.normal(0, noise_std, n)
    x2 = s + np.random.normal(0, noise_std, n)
    # Añadir glitch solo en x1
    glitch_idx = n // 2
    x1[glitch_idx] += glitch_amp_factor * amp
    return x1, x2


def generar_par_escenario4(n, fs, f0, amp, snr_rms, rho=0.8):
    """Escenario 4 — Ruido parcialmente correlacionado.

    n2 = ρ·n1 + √(1-ρ²)·ε  (el enemigo real: acoplamientos comunes).
    """
    noise_std = amp / snr_rms if snr_rms > 0 else amp
    s = _make_signal(n, fs, f0, amp)
    n1 = np.random.normal(0, noise_std, n)
    eps = np.random.normal(0, noise_std, n)
    n2 = rho * n1 + np.sqrt(1 - rho ** 2) * eps
    x1 = s + n1
    x2 = s + n2
    return x1, x2


# ═══════════════════════════════════════════════════════════════════════════
# Cálculo de AUC por escenario
# ═══════════════════════════════════════════════════════════════════════════

def calcular_auc_escenario(gen_fn, n_trials, n_samples, fs, f0, bw,
                           amp=1.0, snr_rms=3.0, **kwargs):
    """Calcula AUC comparando D_Ψ bajo H1 (señal+ruido) frente a H0 (solo ruido).

    Parámetros
    ----------
    gen_fn : callable
        Función generadora de par (x1, x2) bajo H1.
    n_trials : int
        Número de realizaciones por hipótesis.
    n_samples : int
        Número de muestras por realización.
    fs, f0, bw : float
        Parámetros espectrales.
    amp : float
        Amplitud de la señal (H1).
    snr_rms : float
        SNR_RMS de la señal respecto al ruido.
    **kwargs
        Argumentos extra para gen_fn.

    Retorna
    -------
    float
        AUC en [0, 1]. AUC ≈ 0.5 bajo H0 pura.
    """
    scores_h1 = []
    scores_h0 = []

    noise_std = amp / snr_rms if snr_rms > 0 else amp

    for _ in range(n_trials):
        # H1: señal presente
        x1, x2 = gen_fn(n_samples, fs, f0, amp, snr_rms, **kwargs)
        res = calcular_psi_noetica(x1, x2, fs=fs, f0=f0, bw=bw)
        scores_h1.append(res["psi"])

        # H0: solo ruido
        n1 = np.random.normal(0, noise_std, n_samples)
        n2 = np.random.normal(0, noise_std, n_samples)
        res0 = calcular_psi_noetica(n1, n2, fs=fs, f0=f0, bw=bw)
        scores_h0.append(res0["psi"])

    scores_h1 = np.array(scores_h1)
    scores_h0 = np.array(scores_h0)

    # AUC por integración trapezoidal sobre curva ROC empírica
    all_scores = np.concatenate([scores_h1, scores_h0])
    thresholds = np.sort(np.unique(all_scores))[::-1]

    tpr_list, fpr_list = [0.0], [0.0]
    for thr in thresholds:
        tpr = np.mean(scores_h1 >= thr)
        fpr = np.mean(scores_h0 >= thr)
        tpr_list.append(tpr)
        fpr_list.append(fpr)
    tpr_list.append(1.0)
    fpr_list.append(1.0)

    # AUC por integración trapezoidal sobre curva ROC empírica ordenada por FPR
    fpr_arr = np.array(fpr_list)
    tpr_arr = np.array(tpr_list)
    orden = np.argsort(fpr_arr)
    auc = float(_trapz(tpr_arr[orden], fpr_arr[orden]))
    return max(0.0, min(1.0, auc))


# ═══════════════════════════════════════════════════════════════════════════
# Benchmark con frecuencia de control
# ═══════════════════════════════════════════════════════════════════════════

def calcular_ratio_control(x1, x2, fs=FS_DEFAULT, f0=F0_DEFAULT,
                           f_control=None, bw=BW_DEFAULT):
    """Ratio score(f0) / score(f_control).

    Permite detectar si la métrica está inflada por acoplamientos comunes
    que afectarían también a la frecuencia de control.

    Parámetros
    ----------
    x1, x2 : array-like
        Series temporales.
    fs : float
        Frecuencia de muestreo (Hz).
    f0 : float
        Frecuencia objetivo (Hz).
    f_control : float or None
        Frecuencia de control (Hz). Por defecto f0 + 50 Hz.
    bw : float
        Semiancho de banda (Hz).

    Retorna
    -------
    dict
        psi_f0, psi_control, ratio (psi_f0 / psi_control).
    """
    if f_control is None:
        f_control = f0 + F_CONTROL_OFFSET

    res_f0 = calcular_psi_noetica(x1, x2, fs=fs, f0=f0, bw=bw)
    res_ctrl = calcular_psi_noetica(x1, x2, fs=fs, f0=f_control, bw=bw)

    psi_f0 = res_f0["psi"]
    psi_ctrl = res_ctrl["psi"]
    # EPSILON evita división por cero cuando no hay potencia en la banda de control
    ratio = psi_f0 / (psi_ctrl + EPSILON)

    return {"psi_f0": psi_f0, "psi_control": psi_ctrl, "ratio": ratio}


# ═══════════════════════════════════════════════════════════════════════════
# CLI principal
# ═══════════════════════════════════════════════════════════════════════════

def _build_parser():
    p = argparse.ArgumentParser(
        description="Coliseo PSI Noético — validación D_Ψ = D_SNR · D_Coh²"
    )
    p.add_argument("--f0", type=float, default=F0_DEFAULT,
                   help="Frecuencia objetivo en Hz (default: %(default)s)")
    p.add_argument("--f_control", type=float, default=None,
                   help="Frecuencia de control en Hz (default: f0+50)")
    p.add_argument("--bw", type=float, default=BW_DEFAULT,
                   help="Semiancho de banda en Hz (default: %(default)s)")
    p.add_argument("--fs", type=float, default=FS_DEFAULT,
                   help="Frecuencia de muestreo en Hz (default: %(default)s)")
    p.add_argument("--duration", type=float, default=0.2,
                   help="Duración de cada realización en s (default: %(default)s)")
    p.add_argument("--n_trials", type=int, default=200,
                   help="Número de realizaciones por escenario (default: %(default)s)")
    p.add_argument("--snr_rms", type=float, default=3.0,
                   help="SNR_RMS de la señal (default: %(default)s)")
    p.add_argument("--seed", type=int, default=42,
                   help="Semilla aleatoria (default: %(default)s)")
    p.add_argument("--benchmark", action="store_true",
                   help="Mostrar ratio score(f0)/score(f_control)")
    return p


def main():
    parser = _build_parser()
    args = parser.parse_args()

    np.random.seed(args.seed)

    f0 = args.f0
    f_control = args.f_control if args.f_control is not None else f0 + F_CONTROL_OFFSET
    bw = args.bw
    fs = int(args.fs)
    n_samples = int(args.duration * fs)
    n_trials = args.n_trials
    snr_rms = args.snr_rms

    escenarios = [
        ("Escenario 1 — Ideal",
         generar_par_escenario1, {}),
        ("Escenario 2 — Realista (jitter)",
         generar_par_escenario2, {"sigma_phi": 0.5}),
        ("Escenario 3 — Glitch local",
         generar_par_escenario3, {"glitch_amp_factor": 10.0}),
        ("Escenario 4 — Ruido parcialmente correlacionado",
         generar_par_escenario4, {"rho": 0.8}),
    ]

    print("=" * 64)
    print("COLISEO PSI NOÉTICO — D_Ψ = D_SNR · D_Coh²")
    print(f"f0={f0} Hz  bw=±{bw} Hz  fs={fs} Hz  n_trials={n_trials}")
    print("=" * 64)
    print(f"{'Escenario':<45}  {'AUC':>6}")
    print("-" * 64)

    resultados = {}
    for nombre, gen_fn, kwargs in escenarios:
        auc = calcular_auc_escenario(
            gen_fn, n_trials, n_samples, fs, f0, bw,
            amp=1.0, snr_rms=snr_rms, **kwargs
        )
        resultados[nombre] = auc
        print(f"{nombre:<45}  {auc:>6.3f}")

    print("-" * 64)

    if args.benchmark:
        print()
        print("BENCHMARK f0 vs f_control")
        print(f"f_control = {f_control:.2f} Hz")
        # Generar una realización típica (escenario 1, H1)
        x1, x2 = generar_par_escenario1(n_samples, fs, f0, amp=1.0, snr_rms=snr_rms)
        r = calcular_ratio_control(x1, x2, fs=fs, f0=f0, f_control=f_control, bw=bw)
        print(f"  D_Ψ(f0={f0:.2f} Hz)        = {r['psi_f0']:.4f}")
        print(f"  D_Ψ(f_ctrl={f_control:.2f} Hz) = {r['psi_control']:.4f}")
        print(f"  Ratio score(f0)/score(f_ctrl) = {r['ratio']:.3f}")

    return resultados


if __name__ == "__main__":
    main()
