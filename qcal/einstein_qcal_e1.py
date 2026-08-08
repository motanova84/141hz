"""
Operational QCAL-E1 contract for the Einstein-QCAL interferometric prediction.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import math
from typing import Any

import numpy as np

from qcal.constants import C, CAVITY_LINEWIDTH_HZ, F0_HZ
from qcal.einstein_qcal import ALPHA_ADELIC, CoherenceState, PSI_RESONANCE, omega_coupling


class QCALE1Verdict(str, Enum):
    """Allowed verdicts for the operational QCAL-E1 contract."""

    SUPPORTED = "SUPPORTED"
    FALSIFIED = "FALSIFIED"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass(frozen=True)
class QCALE1Contract:
    """Parameter-free operational contract for the Einstein-QCAL prediction."""

    prediction_id: str = "QCAL-E1"
    title: str = "Interferometric phase anomaly at 141.7001 Hz"
    central_frequency_hz: float = F0_HZ
    tolerance_hz: float = 1e-4
    line_width_hz: float = CAVITY_LINEWIDTH_HZ
    alpha_adelic: float = ALPHA_ADELIC
    resonance_threshold_psi: float = PSI_RESONANCE
    spectral_window_hz: tuple[float, float] = (100.0, 200.0)
    minimum_detector_sensitivity_hz_sqrt: float = 1e-24
    frequency_resolution_hz: float = 1e-4
    forbid_post_hoc_free_parameters: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QCALE1Measurement:
    """Auditable input for a QCAL-E1 evaluation."""

    psi_obs: float
    cavity_length_m: float = 4000.0
    f_observer_hz: float = F0_HZ
    detector_sensitivity_hz_sqrt: float = 1e-24
    detected_peak_frequency_hz: float | None = None
    detected_peak_power: float | None = None
    observed_phase_shift_rad: float | None = None
    measured_line_width_hz: float | None = None
    phase_velocity_sensitive: bool = True
    scale_linearity_r2: float | None = None
    scale_slope: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class QCALE1Evaluation:
    """Structured evaluation result for the operational contract."""

    contract: dict[str, Any]
    measurement: dict[str, Any]
    observables: dict[str, Any]
    criteria: dict[str, bool]
    verdict: str
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_qcal_e1_contract() -> QCALE1Contract:
    """Return the canonical QCAL-E1 contract."""

    return QCALE1Contract()


def lorentzian_weight(frequency_hz: float, contract: QCALE1Contract) -> float:
    """Normalized Lorentzian profile centered at the exact contract frequency."""

    if contract.line_width_hz <= 0.0:
        raise ValueError("line_width_hz must be positive")
    detuning = frequency_hz - contract.central_frequency_hz
    return 1.0 / (1.0 + 4.0 * (detuning / contract.line_width_hz) ** 2)


def _operational_delta_n(state: CoherenceState) -> float:
    """Leading-order refractive-index excess used by the operational contract."""

    modulation = (1.0 + math.cos(math.pi * F0_HZ / state.f_observer) ** 2) / 2.0
    return ALPHA_ADELIC * (1.0 - state.psi) * modulation


def predicted_phase_shift_rad(
    state: CoherenceState,
    cavity_length_m: float,
    contract: QCALE1Contract,
    frequency_hz: float | None = None,
) -> float:
    """Phase-delay prediction for the operational interferometric contract."""

    probe_frequency_hz = contract.central_frequency_hz if frequency_hz is None else frequency_hz
    delta_n = _operational_delta_n(state)
    phase_prefactor = 2.0 * math.pi * probe_frequency_hz * cavity_length_m / C
    return phase_prefactor * delta_n * lorentzian_weight(probe_frequency_hz, contract)


def model_spectrum(
    state: CoherenceState,
    cavity_length_m: float,
    contract: QCALE1Contract,
    frequencies_hz: list[float] | None = None,
) -> list[dict[str, float]]:
    """Return a compact auditable phase-response spectrum."""

    if frequencies_hz is None:
        frequencies_hz = [
            contract.central_frequency_hz - 5.0 * contract.tolerance_hz,
            contract.central_frequency_hz - contract.tolerance_hz,
            contract.central_frequency_hz,
            contract.central_frequency_hz + contract.tolerance_hz,
            contract.central_frequency_hz + 5.0 * contract.tolerance_hz,
        ]

    spectrum = []
    for frequency_hz in frequencies_hz:
        spectrum.append(
            {
                "frequency_hz": float(frequency_hz),
                "lorentzian_weight": float(lorentzian_weight(frequency_hz, contract)),
                "predicted_phase_shift_rad": float(
                    predicted_phase_shift_rad(
                        state=state,
                        cavity_length_m=cavity_length_m,
                        contract=contract,
                        frequency_hz=frequency_hz,
                    )
                ),
            }
        )
    return spectrum


def compute_scaling_metrics(
    cavity_length_m: float,
    contract: QCALE1Contract,
    psi_values: list[float] | None = None,
) -> dict[str, Any]:
    """Check the linear operational scaling against the spectral-gap function."""

    if psi_values is None:
        psi_values = [0.999996, 0.999997, 0.999998, 0.999999]

    gap_values = []
    phase_values = []
    for psi in psi_values:
        state = CoherenceState(psi=psi, f_observer=contract.central_frequency_hz)
        gap_values.append(state.spectral_gap)
        phase_values.append(
            predicted_phase_shift_rad(
                state=state,
                cavity_length_m=cavity_length_m,
                contract=contract,
                frequency_hz=contract.central_frequency_hz,
            )
        )

    x = np.asarray(gap_values, dtype=float)
    y = np.asarray(phase_values, dtype=float)
    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope * x + intercept
    ss_res = float(np.sum((y - y_fit) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 if ss_tot == 0.0 else 1.0 - ss_res / ss_tot

    return {
        "psi_values": [float(value) for value in psi_values],
        "delta_gap_rad_s": [float(value) for value in gap_values],
        "predicted_phase_shift_rad": [float(value) for value in phase_values],
        "linear_fit_slope": float(slope),
        "linear_fit_intercept": float(intercept),
        "linear_fit_r2": float(r2),
    }


def evaluate_qcal_e1(
    measurement: QCALE1Measurement,
    contract: QCALE1Contract | None = None,
) -> QCALE1Evaluation:
    """Evaluate the operational contract and return an auditable verdict."""

    contract = build_qcal_e1_contract() if contract is None else contract
    state = CoherenceState(psi=measurement.psi_obs, f_observer=measurement.f_observer_hz)

    operational_delta_n = _operational_delta_n(state)
    omega = omega_coupling(state)
    exact_n = 1.0 / omega
    predicted_peak_phase = predicted_phase_shift_rad(
        state=state,
        cavity_length_m=measurement.cavity_length_m,
        contract=contract,
        frequency_hz=contract.central_frequency_hz,
    )
    scaling = compute_scaling_metrics(measurement.cavity_length_m, contract)

    frequency_match = (
        measurement.detected_peak_frequency_hz is not None
        and abs(measurement.detected_peak_frequency_hz - contract.central_frequency_hz) <= contract.tolerance_hz
    )
    peak_present = (
        measurement.detected_peak_frequency_hz is not None
        and measurement.detected_peak_power is not None
        and measurement.detected_peak_power > 0.0
    )
    incoherent_regime = measurement.psi_obs < contract.resonance_threshold_psi
    sensitivity_adequate = measurement.detector_sensitivity_hz_sqrt <= contract.minimum_detector_sensitivity_hz_sqrt
    c_eff_sensitive_to_psi = measurement.phase_velocity_sensitive and operational_delta_n > 0.0
    scaling_r2 = measurement.scale_linearity_r2 if measurement.scale_linearity_r2 is not None else scaling["linear_fit_r2"]
    scaling_slope = measurement.scale_slope if measurement.scale_slope is not None else scaling["linear_fit_slope"]
    scaling_consistent = scaling_r2 >= 0.99 and scaling_slope > 0.0

    criteria = {
        "incoherent_regime": incoherent_regime,
        "sensitivity_adequate": sensitivity_adequate,
        "peak_present": peak_present,
        "frequency_match": frequency_match,
        "c_eff_sensitive_to_psi": c_eff_sensitive_to_psi,
        "scaling_consistent": scaling_consistent,
    }

    reasons: list[str] = []
    verdict = QCALE1Verdict.INCONCLUSIVE

    if incoherent_regime and sensitivity_adequate and not peak_present:
        verdict = QCALE1Verdict.FALSIFIED
        reasons.append("No peak detected at 141.7001 Hz under controlled incoherence and adequate sensitivity.")
    elif peak_present and not frequency_match:
        verdict = QCALE1Verdict.FALSIFIED
        reasons.append("Detected peak falls outside the ±0.0001 Hz anchoring tolerance.")
    elif (1.0 - measurement.psi_obs) > 0.0 and not c_eff_sensitive_to_psi:
        verdict = QCALE1Verdict.FALSIFIED
        reasons.append("Phase velocity remains insensitive to coherence despite ΔΨ > 0.")
    elif peak_present and frequency_match and c_eff_sensitive_to_psi and scaling_consistent:
        verdict = QCALE1Verdict.SUPPORTED
        reasons.append("Exact-frequency line, coherence-sensitive phase delay, and linear gap scaling all hold.")
    else:
        reasons.append("Current inputs do not satisfy either the falsification or confirmation thresholds.")

    observables = {
        "omega": float(omega),
        "n_refraction_exact": float(exact_n),
        "delta_n_operational": float(operational_delta_n),
        "c_eff_m_s": float(C * omega),
        "delta_gap_rad_s": float(state.spectral_gap),
        "predicted_peak_phase_shift_rad": float(predicted_peak_phase),
        "measured_line_width_hz": (
            float(measurement.measured_line_width_hz)
            if measurement.measured_line_width_hz is not None
            else float(contract.line_width_hz)
        ),
        "spectrum_model": model_spectrum(state, measurement.cavity_length_m, contract),
        "scaling_model": scaling,
    }

    return QCALE1Evaluation(
        contract=contract.to_dict(),
        measurement=measurement.to_dict(),
        observables=observables,
        criteria=criteria,
        verdict=verdict.value,
        reasons=reasons,
    )
