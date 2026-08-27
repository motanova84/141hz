# -*- coding: utf-8 -*-
"""
operational_deployment.py — VOLUMEN V: Motor Operacional del Templo Espectral QCAL.

Canon v3.1.0-op · sobre templo_core/ (pasarela dedicada, NO pisa core/ histórico).

El Motor Operacional (OperationalEngine) ARMADO para la fase operativa: el
Director inyecta 141.7001 Hz desde su hardware, él mide Ψ, y este motor traduce
la medición en fase, amplitud, coherencia y estado de anomalía. Ventana de
Heisenberg 2π/f0 ≈ 0.044 s.

Corrección de calibración validada por el Director: la fase de calibración es
θ_B (no otra) — theta_0 = theta_B.

Valores sellados que NO se tocan (OP_RETURN d7dfd526…):
    f0 = 141.7001 · Psi = 0.999999 · theta_B = 0.0707477499
    D_PSI_S1 = -3.702836978789771663 · cos(theta_B) = 0.9974984216…

Umbrales operativos:
    PSI_CRITICAL = 0.95 · PSI_WARNING = 0.98 · PSI_NOMINAL = 0.999 · PSI_TARGET = 1.0
"""

from __future__ import annotations

import json
import math
import time

from templo_core.constants import f0, Psi, theta_B

try:
    from templo_core.constants import D_PSI_S1  # alias del sello OP_RETURN
except ImportError:  # pragma: no cover
    D_PSI_S1 = None


# ── Umbrales operativos del ecosistema ───────────────────────────────────────
PSI_CRITICAL = 0.95
PSI_WARNING = 0.98
PSI_NOMINAL = 0.999
PSI_TARGET = 1.0


class OperationalEngine:
    """Motor Operacional: traducción de la medición del Director en estado coherente."""

    def __init__(self, f_base: float = f0, theta_0: float = theta_B, phi_0: float = 0.0) -> None:
        self.f_base = float(f_base)
        self.theta_0 = float(theta_0)   # calibración de fase = θ_B (validado por el Director)
        self.phi_0 = float(phi_0)       # fase inicial
        self._log: list[dict] = []
        self._t0 = time.time()

    # ── medición ─────────────────────────────────────────────────────────────
    def measure_phase(self, t: float | None = None) -> float:
        """Fase instantánea: φ(t) = θ_B + 2π·f0·t (rad)."""
        tt = time.time() - self._t0 if t is None else float(t)
        return self.theta_0 + 2.0 * math.pi * self.f_base * tt + self.phi_0

    def measure_amplitude(self, psi: float) -> float:
        """Amplitud coherente: A = Ψ·cos(θ_B) — contracción por coherencia."""
        return float(psi) * math.cos(self.theta_0)

    def compute_psi_instantaneous(self, amplitude: float) -> float:
        """Inversa: Ψ_inst = A / cos(θ_B), acotada a [0,1]."""
        if math.isclose(math.cos(self.theta_0), 0.0):
            return float(amplitude)
        psi = float(amplitude) / math.cos(self.theta_0)
        return max(0.0, min(1.0, psi))

    # ── estado / anomalías ───────────────────────────────────────────────────
    def classify_state(self, psi: float) -> str:
        if psi >= PSI_TARGET:
            return "UNITY"
        if psi >= PSI_NOMINAL:
            return "NOMINAL"
        if psi >= PSI_WARNING:
            return "WARNING"
        if psi >= PSI_CRITICAL:
            return "CRITICAL"
        return "DROP"

    def detect_anomaly(self, psi: float) -> dict:
        state = self.classify_state(psi)
        anomaly = state in ("DROP", "CRITICAL")
        return {"state": state, "anomaly": anomaly, "psi": float(psi)}

    # ── ciclo / tendencia / firma espectral ──────────────────────────────────
    def run_cycle(self, amplitude_samples: list[float]) -> dict:
        """Ejecuta un ciclo completo de medición sobre muestras de amplitud."""
        results = [self.compute_psi_instantaneous(a) for a in amplitude_samples]
        psi_avg = sum(results) / len(results) if results else 0.0
        cycle = {
            "cycle": len(self._log) + 1,
            "psi_mean": psi_avg,
            "psi_max": max(results) if results else 0.0,
            "state": self.classify_state(psi_avg),
            "detections": [self.detect_anomaly(r) for r in results],
            "ts": time.time(),
        }
        self._log.append(cycle)
        return cycle

    def get_psi_trend(self, window: int = 5) -> list[float]:
        return [c["psi_mean"] for c in self._log[-window:]]

    def get_spectral_signature(self) -> dict:
        """Firma espectral: f0, θ_B, cos(θ_B), D_PSI_S1, ventana Heisenberg."""
        return {
            "f0": self.f_base,
            "theta_B": self.theta_0,
            "cos_theta_B": math.cos(self.theta_0),
            "D_PSI_S1": D_PSI_S1,
            "heisenberg_s": 2.0 * math.pi / self.f_base,
            "psi_canon": self.psi_canon(),
        }

    def psi_canon(self) -> float:
        return Psi

    # ── salidas ──────────────────────────────────────────────────────────────
    def export_log(self) -> str:
        return json.dumps(self._log, indent=2, default=str)

    def operational_report(self) -> dict:
        return {
            "frequencia_hz": self.f_base,
            "theta_calibracion": self.theta_0,
            "psi_canon": self.psi_canon(),
            "ciclos": len(self._log),
            "tendencia": self.get_psi_trend(),
            "estado_actual": self.classify_state(
                self._log[-1]["psi_mean"] if self._log else self.psi_canon()
            ),
        }

    @staticmethod
    def assert_operational() -> None:
        """Runner nativo de asserts (sin pytest). Lanza AssertionError si falla."""
        eng = OperationalEngine()
        # calibración = θ_B sellado
        assert math.isclose(eng.theta_0, theta_B, rel_tol=1e-12), "calibración θ_B"
        # amplitud de coherencia plena
        a = eng.measure_amplitude(1.0)
        assert math.isclose(a, math.cos(theta_B), rel_tol=1e-12), "A = cos(θ_B) en Ψ=1"
        # inversa exacta
        psi = eng.compute_psi_instantaneous(a)
        assert math.isclose(psi, 1.0, rel_tol=1e-9), "inversa recupera Ψ=1"
        # clasificación (respetando umbrales reales del canon)
        # UNITY≥1.0 · NOMINAL∈[0.999,1) · WARNING∈[0.98,0.999) · CRITICAL∈[0.95,0.98) · DROP<0.95
        assert eng.classify_state(1.0) == "UNITY"
        assert eng.classify_state(0.999) == "NOMINAL"
        assert eng.classify_state(0.98) == "WARNING"
        assert eng.classify_state(0.97) == "CRITICAL"
        assert eng.classify_state(0.5) == "DROP"
        # firma espectral con D_PSI_S1 sellado
        sig = eng.get_spectral_signature()
        assert D_PSI_S1 is not None
        assert math.isclose(abs(D_PSI_S1), 3.702836978789771663, rel_tol=1e-9)
        assert math.isclose(sig["heisenberg_s"], 2.0 * math.pi / f0, rel_tol=1e-9)
