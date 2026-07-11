#!/usr/bin/env python3
"""
Tests para el Protocolo ΔP QCAL.

Compatible con:
  - pytest (para uso en CI moderno)
  - `python test_protocolo_perturbacion_dp.py` (para `scripts/run_all_tests.py`)

Falsabilidad: si ℱ_Ψ es correcto, las predicciones deben cumplirse.

Sello: QCAL-INYECCION-INMEDIATA-v1.0 ∴ 𓂀 Ω ∞³ Φ
"""

import sys
import tempfile
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from protocolo_perturbacion_dp import simulate_perturbation  # noqa: E402


class Args:
    """Mock args para invocar `simulate_perturbation` sin CLI."""

    def __init__(self, **kwargs):
        defaults = {
            "f0": 141.7001,
            "p_th": 1.0,
            "kappa": 445.4,
            "lambda_": 1.0,
            "mu": 0.5,
            "nu": 0.5,
            "rho": 445.4,
            "chi": 1e-3,
            "plot": False,
            "seed": 42,
            "delta_p": 0.0,
        }
        defaults.update(kwargs)
        for k, v in defaults.items():
            setattr(self, k, v)
        if "output" not in kwargs:
            tmp = tempfile.NamedTemporaryFile(
                suffix=".json", delete=False, prefix="qcal_test_")
            tmp.close()
            self.output = tmp.name


def test_prediction_symmetry():
    """Δf_predicho(+ΔP) = -Δf_predicho(-ΔP) bajo régimen lineal."""
    r_pos = simulate_perturbation(Args(delta_p=0.10, seed=42))
    r_neg = simulate_perturbation(Args(delta_p=-0.10, seed=42))
    assert abs(r_pos["delta_f_predicted_mhz"]
               + r_neg["delta_f_predicted_mhz"]) < 1e-9


def test_perturbation_scaling():
    """Δf_predicho ∝ ΔP: doblar ΔP debe doblar el shift."""
    r10 = simulate_perturbation(Args(delta_p=0.10, seed=1))
    r20 = simulate_perturbation(Args(delta_p=0.20, seed=1))
    ratio = r20["delta_f_predicted_mhz"] / r10["delta_f_predicted_mhz"]
    assert abs(ratio - 2.0) < 1e-9


def test_zero_perturbation():
    """ΔP = 0 → Δf_predicho = 0."""
    r = simulate_perturbation(Args(delta_p=0.0, seed=7))
    assert abs(r["delta_f_predicted_mhz"]) < 1e-10


def test_prediction_matches_theoretical_formula():
    """Δf = f₀ · χ · (ΔP/P_th) exactamente."""
    args = Args(delta_p=0.10, chi=1e-3, f0=141.7001, p_th=1.0, seed=99)
    r = simulate_perturbation(args)
    expected_hz = 141.7001 * 1e-3 * 0.10
    assert abs(r["delta_f_predicted_hz"] - expected_hz) < 1e-15


def test_prediction_near_14_17_mhz_default_params():
    """Con χ=1e-3, f₀=141.7001 Hz, ΔP=+10% ⇒ Δf ≈ 14.17 mHz (±0.01)."""
    r = simulate_perturbation(Args(delta_p=0.10, seed=123))
    assert abs(r["delta_f_predicted_mhz"] - 14.17001) < 0.01


def test_coherence_within_bounds():
    """0 ≤ Ψ ≤ 1 siempre."""
    for dp in [-0.20, -0.10, 0.0, 0.10, 0.20]:
        r = simulate_perturbation(Args(delta_p=dp, seed=17))
        assert 0.0 <= r["coherencia_psi"] <= 1.0


def test_artifact_schema():
    """El artefacto contiene las claves críticas para el workflow."""
    r = simulate_perturbation(Args(delta_p=0.10, seed=5))
    for key in ("timestamp", "f0_hz", "delta_p_ratio",
                "delta_f_predicted_mhz", "delta_f_measured_mhz",
                "coherencia_psi", "coherencia", "threshold_psi",
                "status", "parameters"):
        assert key in r, f"missing key: {key}"


def _run_all():
    """Runner standalone para `scripts/run_all_tests.py`."""
    tests = [v for k, v in globals().items()
             if k.startswith("test_") and callable(v)]
    failed = []
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
        except AssertionError as e:
            failed.append((t.__name__, f"AssertionError: {e}"))
            print(f"  ❌ {t.__name__}: {e}")
        except Exception as e:
            failed.append((t.__name__, f"{type(e).__name__}: {e}"))
            print(f"  ❌ {t.__name__}: {type(e).__name__}: {e}")
    print(f"\nQCAL ΔP tests: {len(tests) - len(failed)}/{len(tests)} pasados")
    return 0 if not failed else 1


if __name__ == "__main__":
    print("=" * 60)
    print("QCAL Protocolo ΔP — Test Suite (standalone)")
    print("=" * 60)
    sys.exit(_run_all())
