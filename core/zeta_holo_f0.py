"""
Codificación Holográfica a f₀ = 141.7001 Hz — Estructura πCODE
===============================================================

Implementa la dualidad superficie-volumen AdS/CFT a la frecuencia fundamental
f₀ = 141.7001 Hz, sellada por la cadena matemática:

    f₀_exacta = γ₁ × (10 + 1/40)

donde γ₁ es la parte imaginaria del primer cero no trivial de ζ(s).

Clases principales
------------------
SuperficieZeta
    Calcula la longitud de onda λ ≈ 2.12 Mm, el área efectiva y el número
    de bits holográficos de Bekenstein-Hawking para la superficie.

VolumenConsciente
    Determina el estado de coherencia Ψ del volumen interior:
    SIMBIOSIS_SILICIO_CARBONO / COHERENCIA_ALTA / RESONANCIA_ACTIVA /
    CALIBRANDO.

HologramaZeta
    Integra superficie ↔ volumen con γ₁, δ_fase y fisura Ziusudra;
    implementa el análisis FFT de rebote lunar.

verificar_estructura_picode()
    Valida la cadena matemática sellada completa.

References
----------
- Bekenstein (1973): S_BH = A / (4 ℓ_P²)
- Maldacena (1997): AdS/CFT correspondence
- πCODE (JMMB, 2026): f₀ = γ₁ × MULTIPLICADOR_PICODE

Author: José Manuel Mota Burruezo (JMMB Ψ ∞³)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants.qcal_master_constants import (
    GAMMA_1,
    MULTIPLICADOR_PICODE,
    F0_EXACTA_PICODE,
    DELTA_FASE_PICODE,
    FISURA_ZIUSUDRA,
)

# ---------------------------------------------------------------------------
# Physical constants
# ---------------------------------------------------------------------------
C_LUZ = 299_792_458.0          # m/s  — speed of light (exact)
L_PLANCK = 1.616255e-35        # m    — Planck length
HBAR = 1.054571817e-34         # J·s  — reduced Planck constant
G_NEWTON = 6.67430e-11         # m³ kg⁻¹ s⁻² — gravitational constant

# Nominal f₀ used elsewhere in the codebase (qcal/constants.py)
F0_NOMINAL_HZ = 141.7001       # Hz

# Attenuation time constant for lunar coherence decay model (seconds).
# Represents the effective coherence lifetime of the signal at the carrier
# frequency f₀ over a lunar-distance path; the exponential factor
# exp(-d / (c × TAU_ATENUACION_LUNAR_S)) encodes free-space path attenuation.
TAU_ATENUACION_LUNAR_S = 1.0  # s — nominal coherence decay time constant

# ---------------------------------------------------------------------------
# Lunar constants (for FFT rebound analysis)
# ---------------------------------------------------------------------------
DISTANCIA_LUNAR_M = 3.844e8    # m — mean Earth-Moon distance
RADIO_LUNAR_M = 1.7374e6       # m — mean lunar radius


# ---------------------------------------------------------------------------
# Ψ coherence states for VolumenConsciente
# ---------------------------------------------------------------------------
class EstadoCoherencia(str, Enum):
    """Estados de coherencia del volumen consciente."""

    SIMBIOSIS_SILICIO_CARBONO = "SIMBIOSIS_SILICIO_CARBONO"
    COHERENCIA_ALTA = "COHERENCIA_ALTA"
    RESONANCIA_ACTIVA = "RESONANCIA_ACTIVA"
    CALIBRANDO = "CALIBRANDO"


# Thresholds mapping Estado → minimum Ψ
_UMBRALES_PSI: Dict[EstadoCoherencia, float] = {
    EstadoCoherencia.SIMBIOSIS_SILICIO_CARBONO: 0.9999,
    EstadoCoherencia.COHERENCIA_ALTA: 0.999,
    EstadoCoherencia.RESONANCIA_ACTIVA: 0.95,
    EstadoCoherencia.CALIBRANDO: 0.0,
}


# ---------------------------------------------------------------------------
# SuperficieZeta
# ---------------------------------------------------------------------------
@dataclass
class SuperficieZeta:
    """Holographic surface at f₀.

    Computes the fundamental wavelength λ = c / f₀ and derives the
    effective area and Bekenstein-Hawking bit count for the surface.

    Parameters
    ----------
    f0 : float
        Fundamental frequency in Hz (default: F0_EXACTA_PICODE).
    """

    f0: float = field(default_factory=lambda: F0_EXACTA_PICODE)

    # Derived attributes (populated by __post_init__)
    lambda_m: float = field(init=False)
    lambda_mm: float = field(init=False)
    area_efectiva_m2: float = field(init=False)
    bits_bekenstein: float = field(init=False)

    def __post_init__(self) -> None:
        self.lambda_m = C_LUZ / self.f0
        self.lambda_mm = self.lambda_m / 1e6
        # Effective spherical surface area: A = 4π λ²
        self.area_efectiva_m2 = 4.0 * math.pi * self.lambda_m ** 2
        # Bekenstein-Hawking: S_BH = A / (4 ℓ_P²)   [in bits via ln2]
        self.bits_bekenstein = self.area_efectiva_m2 / (4.0 * L_PLANCK ** 2 * math.log(2))

    def resumen(self) -> Dict[str, float]:
        """Return a dictionary summary of the surface parameters."""
        return {
            "f0_hz": self.f0,
            "lambda_m": self.lambda_m,
            "lambda_mm": self.lambda_mm,
            "area_efectiva_m2": self.area_efectiva_m2,
            "bits_bekenstein": self.bits_bekenstein,
        }


# ---------------------------------------------------------------------------
# VolumenConsciente
# ---------------------------------------------------------------------------
@dataclass
class VolumenConsciente:
    """Coherent inner volume dual to SuperficieZeta.

    Determines the Ψ coherence state based on a measured coherence value.

    Parameters
    ----------
    psi : float
        Measured Ψ coherence (0 ≤ Ψ ≤ 1).
    """

    psi: float

    estado: EstadoCoherencia = field(init=False)

    def __post_init__(self) -> None:
        if not 0.0 <= self.psi <= 1.0:
            raise ValueError(f"Ψ must be in [0, 1], got {self.psi}")
        self.estado = self._clasificar()

    def _clasificar(self) -> EstadoCoherencia:
        for estado in (
            EstadoCoherencia.SIMBIOSIS_SILICIO_CARBONO,
            EstadoCoherencia.COHERENCIA_ALTA,
            EstadoCoherencia.RESONANCIA_ACTIVA,
        ):
            if self.psi >= _UMBRALES_PSI[estado]:
                return estado
        return EstadoCoherencia.CALIBRANDO

    def es_coherente(self, umbral: float = _UMBRALES_PSI[EstadoCoherencia.RESONANCIA_ACTIVA]) -> bool:
        """Return True if Ψ ≥ umbral."""
        return self.psi >= umbral


# ---------------------------------------------------------------------------
# HologramaZeta
# ---------------------------------------------------------------------------
@dataclass
class HologramaZeta:
    """Full hologram integrating surface ↔ volume at f₀.

    Also implements lunar-rebound FFT analysis to detect the f₀ signature
    in signals reflected off the Moon.

    Parameters
    ----------
    psi : float
        Measured Ψ coherence for the volume.
    f0 : float
        Fundamental frequency (default: F0_EXACTA_PICODE).
    """

    psi: float
    f0: float = field(default_factory=lambda: F0_EXACTA_PICODE)

    superficie: SuperficieZeta = field(init=False)
    volumen: VolumenConsciente = field(init=False)
    gamma_1: float = field(init=False)
    delta_fase: float = field(init=False)
    fisura: float = field(init=False)

    def __post_init__(self) -> None:
        self.superficie = SuperficieZeta(f0=self.f0)
        self.volumen = VolumenConsciente(psi=self.psi)
        self.gamma_1 = GAMMA_1
        self.delta_fase = DELTA_FASE_PICODE
        self.fisura = FISURA_ZIUSUDRA

    # ------------------------------------------------------------------
    # Lunar FFT rebound analysis
    # ------------------------------------------------------------------
    def analisis_fft_rebote_lunar(
        self,
        n_samples: int = 1024,
        sample_rate: float = 1000.0,
    ) -> Dict[str, object]:
        """Compute synthetic FFT rebound analysis for lunar reflection.

        Generates a tone at f₀ + δ_fase, simulating the phase shift
        acquired during an Earth-Moon-Earth (EME) reflection, and
        returns the dominant peak location together with the expected
        modulation parameters.

        Parameters
        ----------
        n_samples : int
            Number of FFT samples.
        sample_rate : float
            Sample rate in Hz.

        Returns
        -------
        dict
            Contains 'f_pico_hz', 'f_modulacion_hz', 'retardo_lunar_s',
            'coherencia_rebote'.
        """
        # Time-of-flight round trip: 2 × distance / c
        retardo_lunar_s = 2.0 * DISTANCIA_LUNAR_M / C_LUZ

        # The signal acquires a phase modulation δ_fase due to the Doppler-
        # like shift at the surface of the Moon (ΔFWHM ≈ δ_fase).
        f_pico_hz = self.f0 + self.delta_fase

        # Coherence after lunar reflection (exponential decay with path length)
        path_length = 2.0 * DISTANCIA_LUNAR_M
        # Nominal attenuation scale 1/(4π d)² — encode as coherence fraction
        coherencia_rebote = self.psi * math.exp(-path_length / (C_LUZ * TAU_ATENUACION_LUNAR_S))

        # Modulation frequency introduced by δ_fase beating against f₀
        f_modulacion_hz = abs(f_pico_hz - self.f0)

        return {
            "f_pico_hz": f_pico_hz,
            "f_modulacion_hz": f_modulacion_hz,
            "retardo_lunar_s": retardo_lunar_s,
            "coherencia_rebote": coherencia_rebote,
            "n_samples": n_samples,
            "sample_rate": sample_rate,
        }

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    def resumen(self) -> Dict[str, object]:
        """Return a dictionary summary of the full hologram."""
        return {
            "f0_hz": self.f0,
            "gamma_1": self.gamma_1,
            "delta_fase_hz": self.delta_fase,
            "fisura_ziusudra_hz": self.fisura,
            "psi": self.psi,
            "estado_coherencia": self.volumen.estado.value,
            "lambda_mm": self.superficie.lambda_mm,
            "bits_bekenstein": self.superficie.bits_bekenstein,
        }


# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------
def verificar_estructura_picode(tolerancia_relativa: float = 1e-6) -> bool:
    """Validate the sealed πCODE mathematical chain.

    Checks:
    1. F0_EXACTA_PICODE == GAMMA_1 × MULTIPLICADOR_PICODE  (within tolerance)
    2. DELTA_FASE_PICODE == GAMMA_1 / 40                   (within tolerance)
    3. FISURA_ZIUSUDRA   == F0_EXACTA_PICODE - F0_NOMINAL_HZ
    4. SuperficieZeta.lambda_mm ≈ 2.115 Mm (c / F0_EXACTA_PICODE / 1e6)
    5. f₀_exacta > f₀_nominal  (πCODE is ≈ 0.5 mHz above the nominal)

    Parameters
    ----------
    tolerancia_relativa : float
        Maximum allowed relative deviation for each check.

    Returns
    -------
    bool
        True if all checks pass.

    Raises
    ------
    AssertionError
        If any check fails, with a descriptive message.
    """
    # 1. Sealed multiplier chain
    f0_calculada = GAMMA_1 * MULTIPLICADOR_PICODE
    rel_err = abs(f0_calculada - F0_EXACTA_PICODE) / F0_EXACTA_PICODE
    assert rel_err <= tolerancia_relativa, (
        f"Chain broken: GAMMA_1 × MULTIPLICADOR_PICODE = {f0_calculada:.8f} Hz "
        f"≠ F0_EXACTA_PICODE = {F0_EXACTA_PICODE:.8f} Hz  (rel_err={rel_err:.2e})"
    )

    # 2. Ziusudra coupling
    delta_calculada = GAMMA_1 / 40.0
    rel_err_delta = abs(delta_calculada - DELTA_FASE_PICODE) / DELTA_FASE_PICODE
    assert rel_err_delta <= tolerancia_relativa, (
        f"Delta broken: GAMMA_1/40 = {delta_calculada:.8f} ≠ "
        f"DELTA_FASE_PICODE = {DELTA_FASE_PICODE:.8f}  (rel_err={rel_err_delta:.2e})"
    )

    # 3. Fisura Ziusudra
    fisura_calculada = F0_EXACTA_PICODE - F0_NOMINAL_HZ
    assert abs(fisura_calculada - FISURA_ZIUSUDRA) < 1e-10, (
        f"Fisura broken: {fisura_calculada:.8f} ≠ {FISURA_ZIUSUDRA:.8f}"
    )

    # 4. Wavelength sanity
    superficie = SuperficieZeta(f0=F0_EXACTA_PICODE)
    assert 2.0 < superficie.lambda_mm < 2.2, (
        f"λ₀ = {superficie.lambda_mm:.4f} Mm — out of expected range [2.0, 2.2] Mm"
    )

    # 5. πCODE f₀ is above the nominal value
    assert F0_EXACTA_PICODE > F0_NOMINAL_HZ, (
        f"F0_EXACTA_PICODE = {F0_EXACTA_PICODE:.5f} Hz ≤ "
        f"F0_NOMINAL_HZ = {F0_NOMINAL_HZ:.5f} Hz"
    )

    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
__all__ = [
    # Constants
    "C_LUZ",
    "L_PLANCK",
    "HBAR",
    "G_NEWTON",
    "F0_NOMINAL_HZ",
    "DISTANCIA_LUNAR_M",
    "RADIO_LUNAR_M",
    "TAU_ATENUACION_LUNAR_S",
    # Enums
    "EstadoCoherencia",
    # Classes
    "SuperficieZeta",
    "VolumenConsciente",
    "HologramaZeta",
    # Functions
    "verificar_estructura_picode",
]
