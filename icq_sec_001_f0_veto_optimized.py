#!/usr/bin/env python3
"""
ICQ-SEC-001 Optimized — F0InductionVetoEngine v2.1.0
Correcciones:
  - Tasa de muestreo EMF fija a 1 kHz (cumple Nyquist)
  - Uso de signal.lfilter_zi para estado inicial correcto
  - Burn-in de 100 ms para eliminar transitorio del filtro Butterworth estrecho
  - Baseline con mínimo 30 bloques para estabilidad de σ
"""

import numpy as np
from scipy import signal
from typing import Tuple, Dict
from collections import deque

class F0InductionVetoEngineOptimized:
    def __init__(
        self,
        f0_hz: float = 141.7001,
        band_halfwidth_hz: float = 0.1,
        butter_order: int = 4,
        sigma_threshold: float = 3.0,
        baseline_window_blocks: int = 100
    ):
        self.f0 = f0_hz
        self.band_low = f0_hz - band_halfwidth_hz
        self.band_high = f0_hz + band_halfwidth_hz
        self.butter_order = butter_order
        self.sigma_threshold = sigma_threshold
        
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
            N=self.butter_order,
            Wn=[low_norm, high_norm],
            btype='band'
        )
        # Estado inicial correcto para filtro IIR
        self.filter_state = signal.lfilter_zi(self.b_butter, self.a_butter)
    
    def _compute_band_power(self, emf_trace: np.ndarray) -> float:
        filtered, next_state = signal.lfilter(
            self.b_butter, self.a_butter, emf_trace, zi=self.filter_state
        )
        self.filter_state = next_state
        
        # Descartar transitorio inicial del filtro estrecho (100 ms)
        burn_in = int(self.fs_emf * 0.1)
        if len(filtered) <= burn_in:
            return float(np.var(filtered))
        power = np.var(filtered[burn_in:])
        return float(power)
    
    def evaluate(self, emf_trace: np.ndarray) -> Tuple[bool, str, Dict]:
        power = self._compute_band_power(emf_trace)
        
        meta = {
            "f0_hz": self.f0,
            "measured_power": power,
            "baseline_mean": self.baseline_mean,
            "baseline_std": self.baseline_std,
            "baseline_established": self.baseline_established
        }
        
        if not self.baseline_established:
            self.baseline_powers.append(power)
            if len(self.baseline_powers) >= 30:
                self.baseline_mean = float(np.mean(self.baseline_powers))
                self.baseline_std = float(np.std(self.baseline_powers, ddof=1))
                if self.baseline_std == 0:
                    self.baseline_std = 1e-12
                self.baseline_established = True
            return True, "F0_BASELINE_COLLECTION", meta
        
        z_power = (power - self.baseline_mean) / self.baseline_std
        meta["z_power"] = float(z_power)
        
        if z_power > self.sigma_threshold:
            return False, f"VETO_F0_INDUCTION_Z{z_power:.2f}", meta
        
        return True, "F0_PASS", meta
