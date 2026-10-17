#!/usr/bin/env python3
"""
ICQ-SEC-001 v2.1.1 — FILTRO DE VETO POR INDUCCIÓN EN f₀
Correcciones post-auditoría:
  • lfilter_zi() en lugar de lfiltic()
  • Burn-in 100 ms
  • Baseline mínimo 30 bloques
  • Protección baseline_std = 0
"""
import numpy as np
from scipy import signal
from typing import Tuple, Dict
from collections import deque

class F0InductionVetoEngine:
    def __init__(
        self,
        f0_hz: float = 141.7001,
        band_halfwidth_hz: float = 0.1,
        butter_order: int = 4,
        sigma_threshold: float = 3.0,
        baseline_window_blocks: int = 100,
        burn_in_ms: float = 100.0
    ):
        self.f0 = f0_hz
        self.band_low = f0_hz - band_halfwidth_hz
        self.band_high = f0_hz + band_halfwidth_hz
        self.butter_order = butter_order
        self.sigma_threshold = sigma_threshold
        self.burn_in_samples = int(burn_in_ms)
        self.baseline_powers = deque(maxlen=baseline_window_blocks)
        self.baseline_mean = None
        self.baseline_std = None
        self.baseline_established = False
        self._redesign_filter(fs_target=1000.0)

    def _redesign_filter(self, fs_target: float):
        self.fs_emf = fs_target
        nyquist = fs_target / 2.0
        low_norm = self.band_low / nyquist
        high_norm = self.band_high / nyquist
        self.b_butter, self.a_butter = signal.butter(
            N=self.butter_order, Wn=[low_norm, high_norm], btype='band'
        )
        self.filter_state = signal.lfilter_zi(self.b_butter, self.a_butter)

    def establish_baseline(self, emf_trace: np.ndarray):
        power = self._compute_band_power(emf_trace)
        self.baseline_powers.append(power)
        if len(self.baseline_powers) >= 30:
            self.baseline_mean = float(np.mean(self.baseline_powers))
            self.baseline_std = float(np.std(self.baseline_powers, ddof=1))
            if self.baseline_std == 0 or np.isnan(self.baseline_std):
                self.baseline_std = 1e-12
            self.baseline_established = True

    def _compute_band_power(self, emf_trace: np.ndarray) -> float:
        filtered, next_state = signal.lfilter(
            self.b_butter, self.a_butter, emf_trace, zi=self.filter_state
        )
        self.filter_state = next_state
        if len(filtered) > self.burn_in_samples:
            filtered_stable = filtered[self.burn_in_samples:]
        else:
            filtered_stable = filtered
        return float(np.var(filtered_stable))

    def evaluate(self, emf_trace: np.ndarray) -> Tuple[bool, str, Dict]:
        power = self._compute_band_power(emf_trace)
        meta = {
            "f0_hz": self.f0, "band_low_hz": self.band_low, "band_high_hz": self.band_high,
            "measured_power": float(power), "baseline_mean": self.baseline_mean,
            "baseline_std": self.baseline_std, "baseline_established": self.baseline_established,
            "burn_in_samples": self.burn_in_samples
        }
        if not self.baseline_established:
            self.establish_baseline(emf_trace)
            return True, "F0_BASELINE_COLLECTION", meta
        z_power = (power - self.baseline_mean) / self.baseline_std
        meta["z_power"] = float(z_power)
        if z_power > self.sigma_threshold:
            return False, f"VETO_F0_INDUCTION_Z{z_power:.2f}", meta
        return True, "F0_PASS", meta

    def reset_filter_state(self):
        self.filter_state = signal.lfilter_zi(self.b_butter, self.a_butter)
