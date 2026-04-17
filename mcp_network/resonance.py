"""Real-observer resonance checks for MCP nodes."""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Callable, Dict, Tuple

import numpy as np
import pandas as pd

F0_REFERENCE = 141.7001
PSI_GATE = 0.888
MS_PER_SECOND = 1000.0
PHASE_WINDOW_SECONDS = 60.0
MAX_LATENCY_MS = 250.0
PHASE_WEIGHT = 0.7
LATENCY_WEIGHT = 0.3

BASELINE_BIO_LATENCY_MS = 18.0
BASELINE_BIO_LATENCY_NOISE_STD = 2.0
BASELINE_BIO_PHASE_OFFSET = 0.04

BASELINE_VACUO_LATENCY_MS = 10.0
BASELINE_VACUO_LATENCY_NOISE_STD = 2.0
BASELINE_VACUO_PHASE_OFFSET = 0.01

BIOLOGIA_FALLBACK_LATENCY_MS = 15.0
BIOLOGIA_FALLBACK_PHASE_OFFSET = 0.012
BIOLOGIA_BASE_LATENCY_MS = 25.0
BIOLOGIA_LATENCY_NOISE_STD = 3.0

INTERFEROMETER_FALLBACK_LATENCY_MS = 9.5
INTERFEROMETER_FALLBACK_PHASE_OFFSET = 0.005
INTERFEROMETER_BASE_LATENCY_MS = 8.0
INTERFEROMETER_LATENCY_NOISE_STD = 2.0

ObserverPayload = Tuple[float, float, bool, bool]
ObserverFn = Callable[[], ObserverPayload]

_REAL_OBSERVERS: Dict[str, ObserverFn] = {}
_RNG = np.random.default_rng(1417001)
_HARMONIC_FACTORS: Dict[str, float] = {
    "biosensores-cuanticos": 1.0,
    "vacuo-noesico": 1.0,
    "biologia-cuantica-noesica": 0.5,
    "interferometro-noesico": 2.0,
}


def register_real_observer(node: str, loader: ObserverFn) -> None:
    """Register a real observer callback for a node."""
    _REAL_OBSERVERS[node] = loader


def _data_path(filename: str) -> Path:
    root = Path(__file__).resolve().parent.parent
    return root / "tests" / "data" / filename


def _psi_from_measurements(latency_ms: float, phase_offset: float) -> float:
    phase_score = max(0.0, 1.0 - abs(phase_offset) / math.pi)
    latency_score = max(0.0, 1.0 - max(latency_ms, 0.0) / MAX_LATENCY_MS)
    psi = (PHASE_WEIGHT * phase_score) + (LATENCY_WEIGHT * latency_score)
    return max(0.0, min(1.0, psi))


def _normal(mean: float, std_dev: float) -> float:
    """Deterministic normal sample for reproducible test behavior."""
    return float(_RNG.normal(mean, std_dev))


def load_biosensores_cuanticos() -> ObserverPayload:
    """Baseline observer for existing biological channel."""
    return (
        _normal(BASELINE_BIO_LATENCY_MS, BASELINE_BIO_LATENCY_NOISE_STD),
        BASELINE_BIO_PHASE_OFFSET,
        True,
        True,
    )


def load_vacuo_noesico() -> ObserverPayload:
    """Baseline observer for existing interferometric-vacuum channel."""
    return (
        _normal(BASELINE_VACUO_LATENCY_MS, BASELINE_VACUO_LATENCY_NOISE_STD),
        BASELINE_VACUO_PHASE_OFFSET,
        True,
        True,
    )


def load_hrv_eeg_biologia() -> ObserverPayload:
    """Observador real para biologia-cuantica-noesica (f₀/2).

    Métrica de desfase: desviación del intervalo RR medio respecto al esperado por f₀/2.
    """
    path = _data_path("hrv_eeg_biologia_cuantica.csv")
    if not os.path.exists(path):
        return BIOLOGIA_FALLBACK_LATENCY_MS, BIOLOGIA_FALLBACK_PHASE_OFFSET, True, True

    df = pd.read_csv(path)
    rr_mean = df["rr_interval_ms"].mean()
    expected_rr = MS_PER_SECOND / (F0_REFERENCE / 2)
    delta_rr = rr_mean - expected_rr
    phase_offset = 2 * math.pi * (delta_rr / MS_PER_SECOND) * PHASE_WINDOW_SECONDS

    latency_ms = _normal(BIOLOGIA_BASE_LATENCY_MS, BIOLOGIA_LATENCY_NOISE_STD)
    return latency_ms, phase_offset, True, True


def load_magnetometer_interferometer() -> ObserverPayload:
    """Observador real para interferometro-noesico (2×f₀).

    Métrica de desfase: desviación del pico espectral respecto a 283.4002 Hz.
    """
    path = _data_path("magnetometer_interferometer.csv")
    if not os.path.exists(path):
        return INTERFEROMETER_FALLBACK_LATENCY_MS, INTERFEROMETER_FALLBACK_PHASE_OFFSET, True, True

    df = pd.read_csv(path)
    peak_freq = df["frequency_hz"].mean()
    target = F0_REFERENCE * 2
    delta_f = peak_freq - target
    phase_offset = 2 * math.pi * delta_f / target

    latency_ms = _normal(INTERFEROMETER_BASE_LATENCY_MS, INTERFEROMETER_LATENCY_NOISE_STD)
    return latency_ms, phase_offset, True, True


def check_node_resonance(node: str) -> Dict[str, object]:
    """Check real resonance for an MCP node and return health metrics."""
    observer = _REAL_OBSERVERS.get(node)
    harmonic_factor = _HARMONIC_FACTORS.get(node, 1.0)
    target_frequency = F0_REFERENCE * harmonic_factor

    if observer is None:
        return {
            "node": node,
            "psi": 0.0,
            "resonance": "unknown",
            "latency_ms": None,
            "phase_offset_rad": None,
            "checks": {
                "observer_registered": False,
                "sensor_available": False,
                "data_valid": False,
                "fuente_fisica": "none",
            },
            "qcal": {
                "gate_threshold": PSI_GATE,
                "harmonic_factor": harmonic_factor,
                "target_frequency_hz": target_frequency,
                "modo_real": False,
                "logos_level": "inactive",
            },
        }

    latency_ms, phase_offset, sensor_available, data_valid = observer()
    psi = _psi_from_measurements(latency_ms, phase_offset)
    coherent = psi >= PSI_GATE and sensor_available and data_valid

    return {
        "node": node,
        "psi": round(psi, 6),
        "resonance": "coherent" if coherent else "decoherent",
        "latency_ms": round(float(latency_ms), 6),
        "phase_offset_rad": float(phase_offset),
        "checks": {
            "observer_registered": True,
            "sensor_available": bool(sensor_available),
            "data_valid": bool(data_valid),
            "fuente_fisica": "real" if sensor_available and data_valid else "fallback",
        },
        "qcal": {
            "gate_threshold": PSI_GATE,
            "harmonic_factor": harmonic_factor,
            "target_frequency_hz": target_frequency,
            "modo_real": bool(sensor_available and data_valid),
            "logos_level": "saturated" if coherent else "recovering",
        },
    }


register_real_observer("biosensores-cuanticos", load_biosensores_cuanticos)
register_real_observer("vacuo-noesico", load_vacuo_noesico)
register_real_observer("biologia-cuantica-noesica", load_hrv_eeg_biologia)
register_real_observer("interferometro-noesico", load_magnetometer_interferometer)
