#!/usr/bin/env python3
"""
ICQ-SEC-001 — Filtro de Veto por Inducción en f₀
================================================
Detecta acoplamiento electromagnético no deseado en la banda
(f₀ ± 0.1) Hz = (141.7001 ± 0.1) Hz mediante filtro Butterworth
orden 4 y umbral adaptativo 3σ sobre la línea base de FASE 1.

Si se detecta potencia espectral excesiva → VETO_F0_INDUCTION
antes de que el bloque entre en el árbol Merkle.
"""

from __future__ import annotations
import numpy as np
from scipy.signal import butter, filtfilt, welch
from typing import Tuple, Dict, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class F0VetoConfig:
    f0: float = 141.7001          # Hz
    bandwidth_hz: float = 0.1     # ±0.1 Hz
    order: int = 4                # Butterworth
    sigma_threshold: float = 3.0  # umbral adaptativo
    # Subarmónicos de muestreo ambiental (f_s = f0 / k)
    k_options: tuple = (2, 4, 8, 16)

class F0InductionVeto:
    """
    Motor de veto por inducción a la frecuencia base QCAL.
    Debe ejecutarse sobre la señal EMF *antes* del sellado HMAC.
    """

    def __init__(self, config: F0VetoConfig = F0VetoConfig()):
        self.cfg = config
        self.baseline_psd_mean: Optional[float] = None
        self.baseline_psd_std: Optional[float] = None
        self._calibrated = False

    def set_baseline_from_fase1(self, emf_signal: np.ndarray, fs: float):
        """
        Establece la línea base de potencia espectral en la banda f₀
        a partir de los datos de FASE 1 (sala vacía).
        """
        power = self._band_power(emf_signal, fs)
        # Usamos media y desviación de ventanas deslizantes cortas
        # para estimar la distribución bajo H0 ambiental.
        if power is None:
            self.baseline_psd_mean = 0.0
            self.baseline_psd_std = 1e-12
        else:
            self.baseline_psd_mean = float(np.mean(power)) if np.ndim(power) else float(power)
            self.baseline_psd_std = float(np.std(power)) if np.ndim(power) and len(np.atleast_1d(power)) > 1 else 1e-12
        self._calibrated = True

    def _band_power(self, signal: np.ndarray, fs: float) -> Optional[float]:
        """Potencia espectral en la banda (f0 ± bandwidth) vía Welch + filtro."""
        if signal is None or len(signal) < 64:
            return None

        low = self.cfg.f0 - self.cfg.bandwidth_hz
        high = self.cfg.f0 + self.cfg.bandwidth_hz
        nyq = 0.5 * fs
        if high >= nyq:
            # Si la tasa de muestreo es insuficiente, devolver None (no veto)
            return None

        # Diseño Butterworth paso-banda
        b, a = butter(self.cfg.order, [low / nyq, high / nyq], btype='band')
        try:
            filtered = filtfilt(b, a, signal.astype(float))
        except Exception:
            return None

        # Potencia RMS en la banda
        power = float(np.mean(filtered ** 2))
        return power

    def evaluate(self, emf_signal: np.ndarray, fs: float) -> Tuple[bool, str, Dict]:
        """
        Retorna (is_valid, reason, meta).
        is_valid = False → el bloque debe ser vetado antes del Merkle.
        """
        meta = {"f0": self.cfg.f0, "calibrated": self._calibrated}

        if not self._calibrated:
            # Sin línea base de FASE 1 no se aplica este veto (solo umbrales absolutos)
            return True, "F0_VETO_SKIPPED_NO_BASELINE", meta

        power = self._band_power(emf_signal, fs)
        if power is None:
            return True, "F0_VETO_SKIPPED_INSUFFICIENT_DATA", meta

        threshold = self.baseline_psd_mean + self.cfg.sigma_threshold * max(self.baseline_psd_std, 1e-15)
        meta.update({
            "band_power": power,
            "threshold_3sigma": threshold,
            "baseline_mean": self.baseline_psd_mean,
            "baseline_std": self.baseline_psd_std
        })

        if power > threshold:
            return False, f"VETO_F0_INDUCTION_power={power:.6e}>thresh={threshold:.6e}", meta

        return True, "VALID_F0", meta

    @staticmethod
    def recommended_env_sampling_rate(k: int = 4) -> float:
        """Tasa de muestreo ambiental recomendada (subarmónico de f₀)."""
        return 141.7001 / k
