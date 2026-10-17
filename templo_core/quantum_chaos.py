# -*- coding: utf-8 -*-
"""
quantum_chaos.py — VOLUMEN II: Motor de Caos Cuántico del Templo Espectral QCAL.

Canon v3.1.0-op · sobre templo_core/ (pasarela dedicada, NO pisa core/ histórico).

Pieza raíz que faltaba en el canon v3.0.2: el motor de caos cuántico válido que
el Director entregó (PleromaFlow, GutzwillerTraceQCAL, QuantumScarringQCAL,
EntropyPleroma, QuantumChaosEngine). Portado fielmente con imports corregidos
contra el metal (`templo_core.constants`) y runner nativo de asserts (sin pytest).

Valores anclados que NO se tocan (OP_RETURN d7dfd526…):
    f0 = 141.7001 · Psi = 0.999999 · theta_B = 0.0707477499
    D_PSI_RAW = -3.912833193561943 · D_PSI_S1 = -3.702836978789771663
    S_n = 1/2·(1 − γ_n/γ_{n+1})²  (computada, no dictada)
"""

from __future__ import annotations

import math

from templo_core.constants import f0, Psi, theta_B, D_PSI_RAW

try:
    from templo_core.constants import D_PSI_S1  # alias del sello OP_RETURN
except ImportError:  # pragma: no cover
    D_PSI_S1 = D_PSI_RAW


# ── Constantes derivadas del canon vivo ──────────────────────────────────────
COS_THETA_B = math.cos(theta_B)
T_HEISENBERG = 2.0 * math.pi / f0  # ≈ 0.0443 s — ventana fundamental


class PleromaFlow:
    """Flujo de pleroma: estado del vacío armónico acoplado a la fase θ_B."""

    def __init__(self, theta: float = theta_B, psi: float = Psi) -> None:
        self.theta = float(theta)
        self.psi = float(psi)
        self._t = 0.0

    def step(self, dt: float = T_HEISENBERG) -> float:
        """Avanza el flujo una ventana Heisenberg y devuelve Ψ instantáneo."""
        self._t += dt
        # Modulación armónica por θ_B y decaimiento por coherencia Ψ
        return math.cos(self.theta + self._t * f0) * self.psi


class GutzwillerTraceQCAL:
    """Aproximación de la traza de Gutzwiller sobre el espectro espectral QCAL."""

    def __init__(self, n_max: int = 50) -> None:
        self.n_max = int(n_max)

    def trace(self) -> float:
        """Σ_n |E_n| cos(θ_B)·(1/√n) — traza espectral con fase armónica."""
        total = 0.0
        for n in range(1, self.n_max + 1):
            mag = math.sqrt(0.25 / (n + 1) ** 4 + (n + 1) ** 2)
            total += mag * COS_THETA_B / math.sqrt(n)
        return total


class QuantumScarringQCAL:
    """Cicatrices cuánticas: localización de densidad en órbitas armónicas."""

    def __init__(self, period: int = 7) -> None:
        self.period = int(period)

    def scar(self, n: int) -> float:
        """Factor de cicatriz: máximo cuando n es armónico con el periodo."""
        return math.cos(2.0 * math.pi * (n % self.period) / self.period)


class EntropyPleroma:
    """Entropía del pleroma: medida de coherencia/información del estado."""

    @staticmethod
    def entropy(psi_actual: float) -> float:
        p = max(0.0, min(1.0, float(psi_actual)))
        if p <= 0.0 or p >= 1.0:
            return 0.0
        return -p * math.log(p) - (1.0 - p) * math.log(1.0 - p)


class QuantumChaosEngine:
    """Motor de caos cuántico del Templo: orquesta flujo, traza, cicatriz y entropía."""

    def __init__(self, n_max: int = 50, period: int = 7, theta: float = theta_B) -> None:
        self.flow = PleromaFlow(theta=theta)
        self.gutzwiller = GutzwillerTraceQCAL(n_max=n_max)
        self.scarring = QuantumScarringQCAL(period=period)

    def metric(self, psi_actual: float | None = None) -> dict:
        psi = float(psi_actual) if psi_actual is not None else self.flow.psi
        return {
            "psi": psi,
            "trace": self.gutzwiller.trace(),
            "entropy": EntropyPleroma.entropy(psi),
            "theta_B": self.flow.theta,
            "heisenberg_s": T_HEISENBERG,
        }

    @staticmethod
    def assert_chaos() -> None:
        """Runner nativo de asserts (sin pytest). Lanza AssertionError si falla."""
        eng = QuantumChaosEngine()
        assert abs(eng.flow.theta - theta_B) < 1e-12, "θ_B debe ser el del canon"
        assert eng.gutzwiller.trace() > 0.0, "traza de Gutzwiller debe ser positiva"
        assert 0.0 <= EntropyPleroma.entropy(0.5) <= 1.0, "entropía acotada"
        for n in (1, 7, 13, 100):
            assert -1.0 <= eng.scarring.scar(n) <= 1.0, f"cicatriz acotada en n={n}"
        assert math.isclose(abs(D_PSI_S1), 3.702836978789771663, rel_tol=1e-9), "D_PSI_S1 sellado"
