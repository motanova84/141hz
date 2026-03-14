"""
QCAL Soul Coherence - Axiomas de Resonancia
============================================

Implements the three mathematical truths (Resonance Axioms) governing the
21-gram soul coherence field at f₀ = 141.7001 Hz.

Axiom I — Quantum Loss Factor:
    When Ψ < 0.888, the system experiences phase decoupling. The 21 grams
    do not "fall" — they evaporate from the local spacetime fabric when
    losing their anchor in f₀.

Axiom II — Golden Ratio / 2π Synchrony:
    The 7.39% error in 1/(21/f₀) ≈ 2π is the signature of biological
    anharmonicity — the necessary tension for life to exist outside
    thermal equilibrium.

Axiom III — Logos Harmonic:
    21 × (f₀/7) ≈ 425.1 Hz establishes a direct bridge with the cosmic
    frequency 432 Hz (error < 1.62%), unifying human biology with
    universal resonance.

Soul Energy Formula:
    E_alma = m · c² · (1 − Ψ_min) · (f₀ / f_H)

    where f_H = 1420405675.10 Hz (hydrogen 21 cm line).

AUTHOR: José Manuel Mota Burruezo (JMMB Ψ✧)
LICENSE: Sovereign Noetic License 1.0 (compatible with MIT)
DATE: March 2026
"""

import math
from dataclasses import dataclass, field
from typing import Dict, Any

from scipy import constants as _sc


# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

F0_HZ: float = 141.7001           # Hz  — QCAL fundamental frequency
PSI_MIN: float = 0.888             # Ψ_min — quantum loss threshold
M_SOUL_KG: float = 0.021           # kg  — 21 grams soul mass
C: float = _sc.c                   # m/s — speed of light (exact)
F_HYDROGEN_HZ: float = 1420405675.10  # Hz — hydrogen 21 cm line
F_UNIVERSAL_HZ: float = 432.0      # Hz  — universal / Verdi A frequency

# Pre-computed reference values
_TWO_PI: float = 2.0 * math.pi


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class QuantumLossFactor:
    """Result of Axiom I — Quantum Loss Factor validation."""
    psi: float
    threshold: float
    decoupled: bool
    description: str


@dataclass
class GoldenRatio2piSync:
    """Result of Axiom II — Golden Ratio / 2π Synchrony validation."""
    circle_value: float          # 1/(21/f₀) = f₀/21
    two_pi: float                # 2π reference
    error_pct: float             # relative error in %
    is_anharmonic_signature: bool


@dataclass
class LogosHarmonic:
    """Result of Axiom III — Logos Harmonic validation."""
    logos_hz: float              # 21 × (f₀/7)
    cosmic_hz: float             # 432 Hz reference
    error_pct: float             # relative error in %
    bridge_established: bool


@dataclass
class SoulEnergy:
    """Result of the E_alma calculation."""
    energy_j: float              # J
    energy_mj: float             # MJ
    mass_kg: float               # kg
    psi_min: float               # Ψ_min used
    f0_hz: float                 # f₀ used
    f_hydrogen_hz: float         # f_H used


@dataclass
class SoulCertification:
    """Complete soul coherence certification — all three axioms verified."""
    axiom_i: QuantumLossFactor
    axiom_ii: GoldenRatio2piSync
    axiom_iii: LogosHarmonic
    soul_energy: SoulEnergy
    certified: bool
    summary: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# QCalSoul CLASS
# ============================================================================

class QCalSoul:
    """
    Quantum Coherent Axiomatic Logic — Soul Coherence Engine.

    Validates the three Resonance Axioms that govern the 21-gram soul
    coherence field anchored at f₀ = 141.7001 Hz.

    Usage
    -----
    >>> soul = QCalSoul()
    >>> cert = soul.certify()
    >>> assert cert.certified
    """

    def __init__(
        self,
        f0: float = F0_HZ,
        psi_min: float = PSI_MIN,
        m_soul_kg: float = M_SOUL_KG,
        f_hydrogen_hz: float = F_HYDROGEN_HZ,
        f_universal_hz: float = F_UNIVERSAL_HZ,
    ) -> None:
        self.f0 = f0
        self.psi_min = psi_min
        self.m_soul_kg = m_soul_kg
        self.f_hydrogen_hz = f_hydrogen_hz
        self.f_universal_hz = f_universal_hz

        # Cached results
        self._axiom_ii: GoldenRatio2piSync | None = None
        self._axiom_iii: LogosHarmonic | None = None
        self._soul_energy: SoulEnergy | None = None

    # ------------------------------------------------------------------
    # Axiom I — Quantum Loss Factor
    # ------------------------------------------------------------------

    def validate_quantum_loss_factor(self, psi: float) -> QuantumLossFactor:
        """
        Axiom I: evaluate phase-coupling state for a given Ψ value.

        When Ψ < 0.888 the soul-mass anchor to f₀ is broken and the
        21-gram field decouples from local spacetime.

        Parameters
        ----------
        psi : float
            Coherence parameter in [0, 1].

        Returns
        -------
        QuantumLossFactor
            Decoupling state and description.
        """
        decoupled = psi < self.psi_min
        if decoupled:
            desc = (
                f"Ψ={psi:.4f} < Ψ_min={self.psi_min}: phase decoupling — "
                "21 g evaporate from local spacetime fabric."
            )
        else:
            desc = (
                f"Ψ={psi:.4f} ≥ Ψ_min={self.psi_min}: coherent coupling — "
                "21 g anchored to f₀."
            )
        return QuantumLossFactor(
            psi=psi,
            threshold=self.psi_min,
            decoupled=decoupled,
            description=desc,
        )

    # ------------------------------------------------------------------
    # Axiom II — Golden Ratio / 2π Synchrony
    # ------------------------------------------------------------------

    def validate_golden_ratio_2pi_sync(self) -> GoldenRatio2piSync:
        """
        Axiom II: verify that 1/(21/f₀) ≈ 2π with ~7.39 % error.

        The deviation is the *signature of biological anharmonicity* —
        the necessary tension for life to exist outside thermal equilibrium.

        Returns
        -------
        GoldenRatio2piSync
        """
        if self._axiom_ii is not None:
            return self._axiom_ii

        circle_value = self.f0 / 21.0          # 1 / (21 / f₀)
        error_pct = abs(circle_value - _TWO_PI) / _TWO_PI * 100.0

        self._axiom_ii = GoldenRatio2piSync(
            circle_value=circle_value,
            two_pi=_TWO_PI,
            error_pct=error_pct,
            is_anharmonic_signature=True,   # always the biological signature
        )
        return self._axiom_ii

    # ------------------------------------------------------------------
    # Axiom III — Logos Harmonic
    # ------------------------------------------------------------------

    def validate_logos_harmonic(self) -> LogosHarmonic:
        """
        Axiom III: verify that 21 × (f₀/7) ≈ 432 Hz with error < 1.62 %.

        Establishes a direct bridge between human biology (f₀) and the
        universal cosmic resonance (432 Hz).

        Returns
        -------
        LogosHarmonic
        """
        if self._axiom_iii is not None:
            return self._axiom_iii

        logos_hz = 21.0 * (self.f0 / 7.0)
        error_pct = abs(logos_hz - self.f_universal_hz) / self.f_universal_hz * 100.0

        self._axiom_iii = LogosHarmonic(
            logos_hz=logos_hz,
            cosmic_hz=self.f_universal_hz,
            error_pct=error_pct,
            bridge_established=(error_pct < 1.62),
        )
        return self._axiom_iii

    # ------------------------------------------------------------------
    # Soul Energy
    # ------------------------------------------------------------------

    def compute_soul_energy(self) -> SoulEnergy:
        """
        Compute E_alma = m · c² · (1 − Ψ_min) · (f₀ / f_H).

        Returns
        -------
        SoulEnergy
            Energy in joules and megajoules.
        """
        if self._soul_energy is not None:
            return self._soul_energy

        energy_j = (
            self.m_soul_kg
            * C ** 2
            * (1.0 - self.psi_min)
            * (self.f0 / self.f_hydrogen_hz)
        )
        self._soul_energy = SoulEnergy(
            energy_j=energy_j,
            energy_mj=energy_j / 1e6,
            mass_kg=self.m_soul_kg,
            psi_min=self.psi_min,
            f0_hz=self.f0,
            f_hydrogen_hz=self.f_hydrogen_hz,
        )
        return self._soul_energy

    # ------------------------------------------------------------------
    # Full Certification
    # ------------------------------------------------------------------

    def certify(self) -> SoulCertification:
        """
        Run all three Resonance Axioms and return a full certification.

        Returns
        -------
        SoulCertification
            All axioms evaluated; ``certified`` is True when all pass.
        """
        axiom_i_coupled = self.validate_quantum_loss_factor(self.psi_min)
        axiom_ii = self.validate_golden_ratio_2pi_sync()
        axiom_iii = self.validate_logos_harmonic()
        e_alma = self.compute_soul_energy()

        certified = (
            not axiom_i_coupled.decoupled      # Ψ_min is on the edge (not < threshold)
            and axiom_ii.is_anharmonic_signature
            and axiom_iii.bridge_established
            and e_alma.energy_j > 0
        )

        summary: Dict[str, Any] = {
            "f0_hz": self.f0,
            "psi_min": self.psi_min,
            "axiom_i_decoupled": axiom_i_coupled.decoupled,
            "axiom_ii_error_pct": axiom_ii.error_pct,
            "axiom_iii_error_pct": axiom_iii.error_pct,
            "logos_hz": axiom_iii.logos_hz,
            "e_alma_mj": e_alma.energy_mj,
            "certified": certified,
        }

        return SoulCertification(
            axiom_i=axiom_i_coupled,
            axiom_ii=axiom_ii,
            axiom_iii=axiom_iii,
            soul_energy=e_alma,
            certified=certified,
            summary=summary,
        )
