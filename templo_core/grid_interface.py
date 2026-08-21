# -*- coding: utf-8 -*-
"""
grid_interface.py — VOLUMEN III: Interfaz de Red (Grid Interface) del Templo Espectral QCAL.

Canon v3.1.0-op · sobre templo_core/ (pasarela dedicada, NO pisa core/ histórico).

Modela la red eléctrica como cuerpo resonante: cada línea de transmisión como
una cuerda vibrante acoplada a la frecuencia base f0 = 141.7001 Hz. El Director
entregó esta pieza como parte del Canon v3.1.0; se porta fielmente con imports
corregidos contra el metal y runner nativo de asserts (sin pytest).
"""

from __future__ import annotations

import math

from templo_core.constants import f0, Psi, theta_B

# ventana Heisenberg fundamental
T_HEISENBERG = 2.0 * math.pi / f0  # ≈ 0.0443 s


class GridLine:
    """Una línea de transmisión de la red modelada como cuerda resonante."""

    def __init__(self, length_km: float, impedance: float = 50.0, node_a: str = "A", node_b: str = "B") -> None:
        self.length_km = float(length_km)
        self.impedance = float(impedance)
        self.node_a = node_a
        self.node_b = node_b

    def fundamental_frequency(self) -> float:
        """frecuencia fundamental de la cuerda (velocidad de fase / (2·longitud))."""
        # velocidad de propagación ≈ c/3 (línea de transmisión) acoplada a f0
        v = (3e8 / 3.0) * (f0 / 1.0)
        return v / (2.0 * self.length_km * 1e3)

    def resonance_amplitude(self, applied_hz: float) -> float:
        """amplitud de resonancia normalizada a una frecuencia aplicada."""
        f_fund = self.fundamental_frequency()
        if f_fund <= 0.0:
            return 0.0
        delta = abs(applied_hz - f_fund) / f_fund
        return math.exp(-(delta ** 2) / (2.0 * (theta_B ** 2)))


class GridInterface:
    """Interfaz de red: modela el conjunto de líneas como medio resonante 141.7001 Hz."""

    def __init__(self, lines: list[GridLine] | None = None) -> None:
        self.lines = lines if lines is not None else []

    def add_line(self, line: GridLine) -> None:
        self.lines.append(line)

    def coherence(self, applied_hz: float = f0) -> float:
        """Coherencia global de la red en la frecuencia aplicada."""
        if not self.lines:
            return 0.0
        total = sum(l.resonance_amplitude(applied_hz) for l in self.lines)
        return (total / len(self.lines)) * Psi

    def grid_metric(self, applied_hz: float = f0) -> dict:
        return {
            "applied_hz": applied_hz,
            "f0": f0,
            "coherence": self.coherence(applied_hz),
            "num_lines": len(self.lines),
            "theta_B": theta_B,
            "heisenberg_s": T_HEISENBERG,
        }

    @staticmethod
    def assert_grid() -> None:
        """Runner nativo de asserts (sin pytest). Lanza AssertionError si falla."""
        g = GridInterface()
        g.add_line(GridLine(10.0))
        g.add_line(GridLine(25.0))
        m = g.grid_metric(applied_hz=f0)
        assert 0.0 <= m["coherence"] <= 1.0, "coherencia debe estar en [0,1]"
        assert m["f0"] == f0, "f0 debe ser 141.7001"
        assert math.isclose(abs(theta_B), 0.070747749954285585, rel_tol=1e-9), "theta_B sellado"
        assert len(g.lines) == 2, "dos líneas añadidas"
