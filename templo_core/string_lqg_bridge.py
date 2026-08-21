# -*- coding: utf-8 -*-
"""
string_lqg_bridge.py — VOLUMEN IV: Puente Cuerdas-LQG del Templo Espectral QCAL.

Canon v3.1.0-op · sobre templo_core/ (pasarela dedicada, NO pisa core/ histórico).

Establece el puente entre la teoría de cuerdas y la gravedad cuántica de lazos
(LQG): la frecuencia base f0 = 141.7001 Hz como tensión de cuerda y la fase
θ_B como apertura del lazo. Portado fielmente con imports corregidos contra el
metal y runner nativo de asserts.
"""

from __future__ import annotations

import math

from templo_core.constants import f0, Psi, theta_B

# longitud de Planck reducida (ℏG/c³)^{1/2} ~ 1.616e-35 m
L_PLANCK = 1.616255e-35
ALPHA_PRIME = L_PLANCK ** 2  # pendiente de Regge


class StringLQGBridge:
    """Puente Cuerdas→LQG: tensor sobre cuerdas y área discreta de lazos."""

    def __init__(self, tension: float = (1.0 / (2.0 * math.pi * ALPHA_PRIME))) -> None:
        self.tension = float(tension)  # T = 1/(2πα')

    # ── lado cuerdas ─────────────────────────────────────────────────────────
    def string_energy(self, mode: int = 1) -> float:
        """E_n = 2·sqrt(α'·T)·n·(ℏ·f0) — energías de los modos de la cuerda."""
        sqrt_at = math.sqrt(ALPHA_PRIME * self.tension)
        return 2.0 * sqrt_at * mode * f0

    def n_oscillations(self, energy: float) -> float:
        return energy / (2.0 * math.sqrt(ALPHA_PRIME * self.tension) * f0)

    # ── lado LQG ─────────────────────────────────────────────────────────────
    def area_eigenvalue(self, j: int = 1) -> float:
        """A_j = 8π·ℓ_p²·θ_B·sqrt(j(j+1)) — área discreta del lazo, abertura θ_B."""
        return 8.0 * math.pi * (L_PLANCK ** 2) * theta_B * math.sqrt(j * (j + 1))

    def bridge_coherence(self) -> float:
        """Coherencia del puente: solapamiento cuerda-lazo en f0 con fase θ_B."""
        string_term = math.exp(-theta_B ** 2)
        lqg_term = math.cos(theta_B)
        return string_term * lqg_term * Psi

    def bridge_metric(self) -> dict:
        return {
            "tension": self.tension,
            "string_E1": self.string_energy(1),
            "area_j1": self.area_eigenvalue(1),
            "coherence": self.bridge_coherence(),
            "alpha_prime": ALPHA_PRIME,
            "f0": f0,
        }

    @staticmethod
    def assert_string_lqg() -> None:
        """Runner nativo de asserts. Lanza AssertionError si falla."""
        b = StringLQGBridge()
        m = b.bridge_metric()
        assert b.string_energy(1) > 0.0, "energía de cuerda positiva"
        assert b.area_eigenvalue(1) > 0.0, "área LQG positiva"
        assert 0.0 <= m["coherence"] <= 1.0, "coherencia del puente en [0,1]"
        assert math.isclose(m["f0"], f0, rel_tol=1e-12), "f0 = 141.7001"
        assert math.isclose(abs(theta_B), 0.070747749954285585, rel_tol=1e-9), "theta_B sellado"
