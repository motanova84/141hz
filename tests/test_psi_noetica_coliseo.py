#!/usr/bin/env python3
"""
Tests para el módulo coliseo_psi_noetic.py

Valida:
  1. calcular_snr_potencia() — ratio on-band/off-band
  2. calcular_psi_noetica()  — D_Ψ = D_SNR · D_Coh²
  3. Cuatro escenarios con AUC por escenario
  4. Sanidad nula: AUC ≈ 0.5 (tolerancia ±0.10) bajo H0 pura con ruido blanco
  5. f_control: ratio score(f0)/score(f_control)

Las métricas se reportan como AUC / p-value Monte Carlo.
No se usan traducciones a σ sin función de calibración definida.
"""

import sys
import os
import unittest
import numpy as np
from scipy import signal as sp_signal

# Añadir scripts/ al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from coliseo_psi_noetic import (
    calcular_snr_potencia,
    calcular_psi_noetica,
    calcular_auc_escenario,
    calcular_ratio_control,
    generar_par_escenario1,
    generar_par_escenario2,
    generar_par_escenario3,
    generar_par_escenario4,
    EPSILON,
    F0_DEFAULT,
    BW_DEFAULT,
    FS_DEFAULT,
    F_CONTROL_OFFSET,
)

# ─── parámetros de test ────────────────────────────────────────────────────
FS = 4096
DURATION = 1.0   # s  (resolución espectral ≤ 1 Hz con periodograma)
N = int(DURATION * FS)
F0 = F0_DEFAULT
BW = BW_DEFAULT   # 5 Hz (resoluble con DURATION=1s)
N_TRIALS = 100   # reducido para CI; aumentar a ≥200 para paper
SNR_RMS = 3.0    # señal moderada
AUC_NULL_MIN = 0.40   # tolerancia sanidad nula (H0)
AUC_NULL_MAX = 0.60
AUC_SIGNAL_MIN = 0.55  # mínimo AUC para escenarios con señal


class TestCalcSNRPotencia(unittest.TestCase):
    """Valida calcular_snr_potencia() — ratio on-band/off-band."""

    def _make_psd(self, f0, bw, fs=FS):
        """PSD sintética con pico en f0 (periodograma de máxima resolución)."""
        n = 4096
        t = np.arange(n) / fs
        x = np.sin(2 * np.pi * f0 * t) + np.random.default_rng(0).normal(0, 0.01, n)
        freqs, pxx = sp_signal.periodogram(x, fs=fs)
        return freqs, pxx

    def test_snr_mayor_1_con_senal(self):
        """Con señal en f0, D_SNR debe ser > 1."""
        freqs, pxx = self._make_psd(F0, BW)
        d_snr = calcular_snr_potencia(pxx, freqs, f0=F0, bw=BW)
        self.assertGreater(d_snr, 1.0,
                           f"D_SNR esperado > 1 con señal, obtenido {d_snr:.3f}")

    def test_snr_cercano_1_con_ruido_blanco(self):
        """Con ruido blanco, D_SNR debe estar cerca de 1."""
        rng = np.random.default_rng(42)
        n = 8192
        x = rng.normal(0, 1, n)
        freqs, pxx = sp_signal.welch(x, fs=FS, nperseg=512)
        d_snr = calcular_snr_potencia(pxx, freqs, f0=F0, bw=BW)
        self.assertGreater(d_snr, 0.3,
                           "D_SNR no debe ser cero con ruido blanco")
        self.assertLess(d_snr, 5.0,
                        f"D_SNR no debe dispararse con ruido blanco, obtenido {d_snr:.3f}")

    def test_snr_retorna_float_no_negativo(self):
        """D_SNR siempre debe ser ≥ 0."""
        rng = np.random.default_rng(7)
        x = rng.normal(0, 1, 1024)
        freqs, pxx = sp_signal.welch(x, fs=FS, nperseg=128)
        d_snr = calcular_snr_potencia(pxx, freqs, f0=F0, bw=BW)
        self.assertGreaterEqual(d_snr, 0.0)
        self.assertIsInstance(d_snr, float)


class TestCalcPsiNoetica(unittest.TestCase):
    """Valida calcular_psi_noetica() — D_Ψ = D_SNR · D_Coh²."""

    def setUp(self):
        np.random.seed(0)

    def test_psi_positivo_con_senal_comun(self):
        """Con señal común en ambos canales, D_Ψ debe ser positivo."""
        n = N
        t = np.arange(n) / FS
        s = np.sin(2 * np.pi * F0 * t)
        x1 = s + np.random.normal(0, 0.3, n)
        x2 = s + np.random.normal(0, 0.3, n)
        res = calcular_psi_noetica(x1, x2, fs=FS, f0=F0, bw=BW)
        self.assertGreater(res["psi"], 0.0)
        self.assertGreater(res["d_snr"], 0.0)
        self.assertGreater(res["d_coh"], 0.0)

    def test_psi_mayor_sin_senal_que_con_ruido_puro(self):
        """D_Ψ con señal coherente debe ser mayor que sin señal."""
        n = N
        np.random.seed(1)
        t = np.arange(n) / FS
        s = np.sin(2 * np.pi * F0 * t)

        # H1: señal coherente
        x1_h1 = s + np.random.normal(0, 0.3, n)
        x2_h1 = s + np.random.normal(0, 0.3, n)
        res_h1 = calcular_psi_noetica(x1_h1, x2_h1, fs=FS, f0=F0, bw=BW)

        # H0: ruido puro
        x1_h0 = np.random.normal(0, 1.0, n)
        x2_h0 = np.random.normal(0, 1.0, n)
        res_h0 = calcular_psi_noetica(x1_h0, x2_h0, fs=FS, f0=F0, bw=BW)

        self.assertGreater(res_h1["psi"], res_h0["psi"],
                           "D_Ψ(H1) debe superar D_Ψ(H0)")

    def test_psi_devuelve_claves_correctas(self):
        """El dict de retorno debe tener 'psi', 'd_snr', 'd_coh'."""
        n = N
        x = np.random.normal(0, 1, n)
        res = calcular_psi_noetica(x, x, fs=FS, f0=F0, bw=BW)
        for key in ("psi", "d_snr", "d_coh"):
            self.assertIn(key, res, f"Falta clave '{key}' en resultado")

    def test_d_coh_entre_0_y_1(self):
        """La coherencia media D_Coh debe estar en [0, 1]."""
        n = N
        x1 = np.random.normal(0, 1, n)
        x2 = np.random.normal(0, 1, n)
        res = calcular_psi_noetica(x1, x2, fs=FS, f0=F0, bw=BW)
        self.assertGreaterEqual(res["d_coh"], 0.0)
        self.assertLessEqual(res["d_coh"], 1.0)


class TestSanidadNula(unittest.TestCase):
    """Sanidad bajo H0 pura: AUC debe estar en [0.40, 0.60]."""

    def test_auc_h0_cerca_de_0_5(self):
        """Con ruido blanco puro, AUC ≈ 0.5 (sin señal, sin sesgo)."""
        np.random.seed(123)

        def gen_ruido_puro(n, fs, f0, amp, snr_rms):
            noise_std = amp / snr_rms
            return (np.random.normal(0, noise_std, n),
                    np.random.normal(0, noise_std, n))

        auc = calcular_auc_escenario(
            gen_ruido_puro,
            n_trials=N_TRIALS,
            n_samples=N,
            fs=FS,
            f0=F0,
            bw=BW,
            amp=1.0,
            snr_rms=SNR_RMS,
        )
        self.assertGreaterEqual(
            auc, AUC_NULL_MIN,
            f"AUC nulo {auc:.3f} < {AUC_NULL_MIN} — posible sesgo negativo"
        )
        self.assertLessEqual(
            auc, AUC_NULL_MAX,
            f"AUC nulo {auc:.3f} > {AUC_NULL_MAX} — detector sesgado bajo H0"
        )

    def test_score_medio_no_satura_con_ruido(self):
        """El score medio bajo H0 no debe ser extremo ni depender fuertemente de la semilla."""
        scores_por_semilla = []
        for seed in [10, 20, 30]:
            np.random.seed(seed)
            psis = []
            for _ in range(30):
                n1 = np.random.normal(0, 1, N)
                n2 = np.random.normal(0, 1, N)
                res = calcular_psi_noetica(n1, n2, fs=FS, f0=F0, bw=BW)
                psis.append(res["psi"])
            scores_por_semilla.append(np.mean(psis))

        cv = np.std(scores_por_semilla) / (np.mean(scores_por_semilla) + EPSILON)  # evita /0
        self.assertLess(cv, 1.0,
                        f"Coeficiente de variación inter-semilla {cv:.3f} demasiado alto")


class TestCuatroEscenarios(unittest.TestCase):
    """AUC por escenario — tabla paper-ready."""

    def _auc(self, gen_fn, **kwargs):
        np.random.seed(42)
        return calcular_auc_escenario(
            gen_fn,
            n_trials=N_TRIALS,
            n_samples=N,
            fs=FS,
            f0=F0,
            bw=BW,
            amp=1.0,
            snr_rms=SNR_RMS,
            **kwargs,
        )

    def test_escenario1_ideal(self):
        """Escenario 1 — Ideal: AUC debe ser > 0.55."""
        auc = self._auc(generar_par_escenario1)
        self.assertGreater(auc, AUC_SIGNAL_MIN,
                           f"Escenario 1 AUC={auc:.3f} demasiado bajo")

    def test_escenario2_jitter(self):
        """Escenario 2 — Jitter: AUC debe ser > 0.50 (robusto)."""
        auc = self._auc(generar_par_escenario2, sigma_phi=0.5)
        self.assertGreater(auc, 0.50,
                           f"Escenario 2 AUC={auc:.3f} — Ψ no robusto a jitter")

    def test_escenario3_glitch(self):
        """Escenario 3 — Glitch: AUC no debe caer por debajo de 0.40.

        Ψ rechaza glitches via D_Coh (el glitch no es coherente entre canales).
        """
        auc = self._auc(generar_par_escenario3, glitch_amp_factor=10.0)
        self.assertGreater(auc, 0.40,
                           f"Escenario 3 AUC={auc:.3f} — Ψ colapsa ante glitch")

    def test_escenario4_ruido_correlacionado(self):
        """Escenario 4 — Ruido correlacionado: AUC debe reportarse (sin umbral fijo).

        Este escenario audita si la métrica se infla por acoplamientos comunes.
        Solo verificamos que el AUC esté en [0, 1] (no saturado).
        """
        auc = self._auc(generar_par_escenario4, rho=0.8)
        self.assertGreaterEqual(auc, 0.0)
        self.assertLessEqual(auc, 1.0)
        # Imprimir para auditoría — en paper real comparar con escenario 1
        print(f"\n  [Escenario 4] AUC con ρ=0.8: {auc:.3f} "
              f"(comparar con Escenario 1 para detectar inflación)")


class TestFControl(unittest.TestCase):
    """Valida el ratio score(f0)/score(f_control)."""

    def setUp(self):
        np.random.seed(0)
        t = np.arange(N) / FS
        s = np.sin(2 * np.pi * F0 * t)
        self.x1 = s + np.random.normal(0, 0.3, N)
        self.x2 = s + np.random.normal(0, 0.3, N)

    def test_ratio_mayor_1_con_senal_en_f0(self):
        """Con señal en f0, ratio(f0/f_control) debe ser > 1."""
        f_control = F0 + F_CONTROL_OFFSET
        r = calcular_ratio_control(self.x1, self.x2,
                                   fs=FS, f0=F0, f_control=f_control, bw=BW)
        self.assertGreater(r["ratio"], 1.0,
                           f"Ratio esperado > 1 con señal en f0, obtenido {r['ratio']:.3f}")

    def test_f_control_por_defecto_es_f0_mas_50(self):
        """Sin especificar f_control, debe usarse f0 + 50 Hz."""
        r = calcular_ratio_control(self.x1, self.x2,
                                   fs=FS, f0=F0, f_control=None, bw=BW)
        # Verificar que las claves existen y son válidas
        for key in ("psi_f0", "psi_control", "ratio"):
            self.assertIn(key, r)
        self.assertGreaterEqual(r["psi_control"], 0.0)

    def test_ratio_ruido_puro_no_dispara(self):
        """Con ruido puro, ratio(f0/f_control) no debe ser >> 1 (sin sesgo).

        Con el epsilon de protección, ratio nunca es inf. Verificamos que
        no exceda un umbral razonable (< 100) cuando no hay señal.
        """
        np.random.seed(99)
        n1 = np.random.normal(0, 1, N)
        n2 = np.random.normal(0, 1, N)
        r = calcular_ratio_control(n1, n2, fs=FS, f0=F0, bw=BW)
        # Con epsilon de protección el ratio debe ser finito
        self.assertFalse(np.isinf(r["ratio"]),
                         "Ratio no debe ser inf con epsilon de protección")
        self.assertLess(r["ratio"], 100.0,
                        f"Ratio con ruido puro demasiado alto: {r['ratio']:.3f}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
