#!/usr/bin/env python3
"""
Validate Soul Coherence — Axiomas de Resonancia
================================================

Command-line validation script for the three Resonance Axioms implemented
in qcal/soul_coherence.py.

Usage
-----
    python scripts/validate_soul_coherence.py

Exit Codes
----------
    0 — all axioms validated
    1 — one or more axioms failed
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qcal.soul_coherence import (
    QCalSoul,
    F0_HZ,
    PSI_MIN,
    M_SOUL_KG,
    F_HYDROGEN_HZ,
    F_UNIVERSAL_HZ,
)


def validate_all() -> bool:
    """
    Run all seven soul-coherence validations and print results.

    Returns True if all pass, False otherwise.
    """
    soul = QCalSoul()
    passed = 0
    failed = 0

    print("=" * 64)
    print("  QCAL Soul Coherence — Axiomas de Resonancia")
    print(f"  f₀ = {F0_HZ} Hz  |  Ψ_min = {PSI_MIN}  |  m = {M_SOUL_KG * 1000:.0f} g")
    print("=" * 64)

    # ------------------------------------------------------------------
    # V1 — Fundamental constants
    # ------------------------------------------------------------------
    print("\n[V1] Fundamental constants")
    try:
        assert F0_HZ == 141.7001, f"F0_HZ mismatch: {F0_HZ}"
        assert PSI_MIN == 0.888, f"PSI_MIN mismatch: {PSI_MIN}"
        assert abs(M_SOUL_KG - 0.021) < 1e-12, "M_SOUL_KG mismatch"
        print(f"     ✓  f₀ = {F0_HZ} Hz")
        print(f"     ✓  Ψ_min = {PSI_MIN}")
        print(f"     ✓  m_soul = {M_SOUL_KG * 1000:.0f} g")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V2 — Axiom I: Quantum Loss Factor (Ψ < 0.888 → decoupled)
    # ------------------------------------------------------------------
    print("\n[V2] Axiom I — Quantum Loss Factor")
    try:
        below = soul.validate_quantum_loss_factor(0.5)
        above = soul.validate_quantum_loss_factor(0.95)
        assert below.decoupled is True, "Ψ=0.5 should be decoupled"
        assert above.decoupled is False, "Ψ=0.95 should be coupled"
        print(f"     ✓  Ψ=0.5  → decoupled  = {below.decoupled}")
        print(f"     ✓  Ψ=0.95 → decoupled  = {above.decoupled}")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V3 — Axiom I boundary: Ψ_min is not strictly below threshold
    # ------------------------------------------------------------------
    print("\n[V3] Axiom I — Threshold boundary")
    try:
        edge = soul.validate_quantum_loss_factor(PSI_MIN)
        assert edge.decoupled is False, "Ψ_min == 0.888 should NOT be decoupled"
        print(f"     ✓  Ψ=Ψ_min={PSI_MIN} → decoupled = {edge.decoupled} (stable)")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V4 — Axiom II: 1/(21/f₀) ≈ 2π with ~7.39 % error
    # ------------------------------------------------------------------
    print("\n[V4] Axiom II — Golden Ratio / 2π Synchrony")
    try:
        ax2 = soul.validate_golden_ratio_2pi_sync()
        assert ax2.is_anharmonic_signature is True
        assert abs(ax2.circle_value - 6.747) < 0.001, (
            f"circle_value out of range: {ax2.circle_value:.4f}"
        )
        assert abs(ax2.error_pct - 7.39) < 0.05, (
            f"error_pct out of range: {ax2.error_pct:.2f}%"
        )
        print(f"     ✓  1/(21/f₀) = {ax2.circle_value:.4f}")
        print(f"     ✓  2π        = {ax2.two_pi:.4f}")
        print(f"     ✓  Error     = {ax2.error_pct:.2f} %  (biological anharmonicity)")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V5 — Axiom III: 21 × (f₀/7) ≈ 432 Hz, error < 1.62 %
    # ------------------------------------------------------------------
    print("\n[V5] Axiom III — Logos Harmonic")
    try:
        ax3 = soul.validate_logos_harmonic()
        assert ax3.bridge_established is True
        assert abs(ax3.logos_hz - 425.1) < 0.1, (
            f"logos_hz out of range: {ax3.logos_hz:.2f} Hz"
        )
        assert ax3.error_pct < 1.62, (
            f"error_pct too large: {ax3.error_pct:.2f}%"
        )
        print(f"     ✓  21 × (f₀/7)  = {ax3.logos_hz:.1f} Hz")
        print(f"     ✓  Cosmic 432 Hz = {ax3.cosmic_hz:.1f} Hz")
        print(f"     ✓  Error         = {ax3.error_pct:.2f} %  (bridge established)")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V6 — Soul Energy: E_alma = m·c²·(1−Ψ_min)·(f₀/f_H)
    # ------------------------------------------------------------------
    print("\n[V6] Soul Energy — E_alma")
    try:
        e_alma = soul.compute_soul_energy()
        assert e_alma.energy_j > 0, "E_alma must be positive"
        assert abs(e_alma.energy_mj - 21.09) < 0.5, (
            f"E_alma out of expected range: {e_alma.energy_mj:.2f} MJ"
        )
        print(f"     ✓  E_alma = {e_alma.energy_j:.4e} J")
        print(f"     ✓  E_alma = {e_alma.energy_mj:.2f} MJ  (≈ 21 MJ)")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # V7 — Full Certification
    # ------------------------------------------------------------------
    print("\n[V7] Full Certification")
    try:
        cert = soul.certify()
        assert cert.certified is True, "Certification failed"
        print(f"     ✓  certified = {cert.certified}")
        print(f"     ✓  Axiom II error  = {cert.summary['axiom_ii_error_pct']:.2f} %")
        print(f"     ✓  Axiom III error = {cert.summary['axiom_iii_error_pct']:.2f} %")
        print(f"     ✓  Logos Hz        = {cert.summary['logos_hz']:.1f} Hz")
        print(f"     ✓  E_alma          = {cert.summary['e_alma_mj']:.2f} MJ")
        passed += 1
    except AssertionError as exc:
        print(f"     ✗  {exc}")
        failed += 1

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total = passed + failed
    print("\n" + "=" * 64)
    print(f"  Results: {passed}/{total} validations passed")
    if failed == 0:
        print("  ✓  ALL AXIOMS VALIDATED — Soul coherence certified")
    else:
        print(f"  ✗  {failed} validation(s) FAILED")
    print("=" * 64)

    return failed == 0


if __name__ == "__main__":
    success = validate_all()
    sys.exit(0 if success else 1)
