#!/usr/bin/env python3
"""
demo_psi_formalization.py - Complete demonstration of Ψ formalization

Demonstrates the rigorous mathematical formalization of the QCAL Ψ operator,
including the operational definition of A_eff², the dimensional and
dimensionless forms, and the three experimentally falsifiable predictions.

Usage:
    python demo_psi_formalization.py
"""

import numpy as np
import math

from core.psi_formalization import (
    QCAL_BASE_FREQUENCY,
    PSI_TILDE_THRESHOLD,
    SPECTRAL_RATIO_THRESHOLD,
    C_LIGHT,
    compute_psi_from_timeseries,
    generate_coherent_signal,
    generate_incoherent_signal,
)
import core.psi_formalization as psi_mod


def _separator(title=""):
    line = "=" * 60
    if title:
        print(f"\n{line}")
        print(f"  {title}")
        print(line)
    else:
        print(line)


def demo_basic_metrics():
    _separator("Basic Ψ metrics (coherent signal)")

    _, a_t = generate_coherent_signal(
        duration=1.0, fs=1000.0, f0=QCAL_BASE_FREQUENCY,
        amplitude=1.0, noise_level=0.0, rng=np.random.default_rng(42)
    )

    m = compute_psi_from_timeseries(a_t, T=1.0, fs=1000.0, mass=1e-12)

    print(f"  A_eff²           = {m.A_eff_squared:.6f}")
    print(f"  Ψ̃  (dim.less)   = {m.psi_tilde:.6f}  [range: 0, π={math.pi:.4f}]")
    print(f"  Ψ   (Joules)     = {m.psi:.6e}")
    print(f"  is_coherent      = {m.is_coherent}  (threshold Ψ̃ ≥ {PSI_TILDE_THRESHOLD})")
    print(f"  f0_detected      = {m.f0_detected}  (threshold ratio ≥ {SPECTRAL_RATIO_THRESHOLD})")
    print(f"  dominant_freq    = {m.dominant_frequency:.4f} Hz  (expected {QCAL_BASE_FREQUENCY} Hz)")
    print(f"  spectral_ratio   = {m.spectral_ratio:.4f}")


def demo_incoherent_contrast():
    _separator("Contrast: incoherent (white noise) signal")

    _, a_t = generate_incoherent_signal(
        duration=1.0, fs=1000.0, amplitude=1.0,
        rng=np.random.default_rng(42)
    )

    m = compute_psi_from_timeseries(a_t, T=1.0, fs=1000.0, mass=1e-12)

    print(f"  A_eff²           = {m.A_eff_squared:.6f}")
    print(f"  Ψ̃  (dim.less)   = {m.psi_tilde:.6f}")
    print(f"  is_coherent      = {m.is_coherent}")
    print(f"  f0_detected      = {m.f0_detected}")
    print(f"  spectral_ratio   = {m.spectral_ratio:.4f}")


def demo_prediction_p1():
    _separator("P1 – Energy scaling: Ψ ∝ m")

    _, a_t = generate_coherent_signal(
        duration=1.0, fs=1000.0, f0=QCAL_BASE_FREQUENCY,
        amplitude=1.0, noise_level=0.0
    )
    masses = [1e-15, 1e-12, 1e-9, 1e-6]

    result = psi_mod.test_prediction_p1_energy_scaling(
        a_t, masses, T=1.0, fs=1000.0
    )

    print(f"  Prediction passed: {result['passed']}")
    print(f"  Relative deviation in Ψ/m: {result['relative_deviation']:.2e}")
    print("  Mass (kg)      Ψ (J)          Ψ/m (J/kg)")
    for m_val, psi_val, ratio in zip(
        result["masses"], result["psi_values"], result["psi_per_mass"]
    ):
        print(f"  {m_val:.2e}    {psi_val:.6e}   {ratio:.6e}")


def demo_prediction_p2():
    _separator("P2 – Coherence sensitivity")

    rng = np.random.default_rng(0)
    _, a_coh = generate_coherent_signal(
        duration=1.0, fs=1000.0, f0=QCAL_BASE_FREQUENCY,
        amplitude=1.0, noise_level=0.01, rng=rng
    )
    _, a_inc = generate_incoherent_signal(
        duration=1.0, fs=1000.0, amplitude=1.0,
        rng=np.random.default_rng(1)
    )

    result = psi_mod.test_prediction_p2_coherence_sensitivity(
        a_coh, a_inc, T=1.0, fs=1000.0
    )

    print(f"  Prediction passed       : {result['passed']}")
    print(f"  Coherent  f₀ detected   : {result['coherent_f0_detected']}")
    print(f"  Incoherent f₀ detected  : {result['incoherent_f0_detected']}")
    print(f"  Coherent  spectral ratio: {result['coherent_spectral_ratio']:.4f}")
    print(f"  Incoherent spectral ratio:{result['incoherent_spectral_ratio']:.4f}")
    print(f"  Coherent  Ψ̃            : {result['coherent_psi_tilde']:.4f}")
    print(f"  Incoherent Ψ̃           : {result['incoherent_psi_tilde']:.4f}")


def demo_prediction_p3():
    _separator("P3 – Spectral peak at f₀ = 141.7001 Hz")

    _, a_t = generate_coherent_signal(
        duration=1.0, fs=1000.0, f0=QCAL_BASE_FREQUENCY,
        amplitude=1.0, noise_level=0.01, rng=np.random.default_rng(7)
    )

    result = psi_mod.test_prediction_p3_spectral_peak(a_t, fs=1000.0)

    print(f"  Prediction passed     : {result['passed']}")
    print(f"  Dominant frequency    : {result['dominant_frequency']:.4f} Hz")
    print(f"  Expected f₀           : {result['f0_expected']:.4f} Hz")
    print(f"  Frequency error       : {result['frequency_error']:.4f} Hz")
    print(f"  Spectral ratio at f₀  : {result['spectral_ratio']:.4f}")
    print(f"  f₀ detected           : {result['f0_detected']}")


if __name__ == "__main__":
    print("\nΨ Formalization – Complete Demonstration")
    print("QCAL ∞³ | f₀ =", QCAL_BASE_FREQUENCY, "Hz")

    demo_basic_metrics()
    demo_incoherent_contrast()
    demo_prediction_p1()
    demo_prediction_p2()
    demo_prediction_p3()

    _separator()
    print("All demonstrations complete.\n")
