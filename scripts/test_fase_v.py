#!/usr/bin/env python3
"""
Tests para QCAL Fase V — dispersión, stress y simetría.

Uso:
    pytest scripts/test_fase_v.py -q
    python  scripts/test_fase_v.py     (modo standalone)

Sello: QCAL-INYECCION-INMEDIATA-v2.0
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from fase_v_dispersion import (  # noqa: E402
    DiffusionParams,
    FieldParams,
    dispersion_branches,
    fundamental_k,
    jacobian_qcal,
    node_spacing,
    sweep_fibonacci,
)


# ------------------------------------------------------------------
# 1. Jacobiano y matriz de difusión
# ------------------------------------------------------------------
def test_jacobian_shape_and_signs():
    p = FieldParams()
    J = jacobian_qcal(p)
    assert J.shape == (3, 3)
    # Diagonal negativa (disipación)
    assert J[0, 0] < 0
    assert J[1, 1] < 0
    assert J[2, 2] < 0
    # Bloque S-P acoplado: J[1,2] > 0, J[2,1] < 0 (oscilación)
    assert J[1, 2] > 0
    assert J[2, 1] < 0
    # Producto |J[1,2] · J[2,1]| = 4κ²λ ⇒ ω_Ψ = 2κ√λ
    prod = abs(J[1, 2] * J[2, 1])
    omega_psi = 2 * p.kappa * np.sqrt(p.lambda_)
    assert np.isclose(prod, omega_psi ** 2, rtol=1e-6)


def test_diffusion_matrix_coupling():
    d = DiffusionParams()
    from fase_v_dispersion import diffusion_matrix
    D = diffusion_matrix(d)
    assert D[1, 2] == pytest.approx(d.D_SP)
    assert D[2, 0] == pytest.approx(d.D_PA)
    # Elementos "cero" verdaderamente cero
    assert D[0, 1] == 0.0
    assert D[0, 2] == 0.0


# ------------------------------------------------------------------
# 2. Dispersión: 3 ramas, ω₁ estable en k → 0
# ------------------------------------------------------------------
def test_three_branches_returned():
    omegas = dispersion_branches(0.01, FieldParams(), DiffusionParams())
    assert omegas.shape == (3,)


def test_omega1_invariant_across_fibonacci():
    p = FieldParams()
    d = DiffusionParams()
    rows = sweep_fibonacci([7, 13, 21, 55], p, d)
    real_parts = [r["omega_1_real_rad_s"] for r in rows]
    spread = max(real_parts) - min(real_parts)
    # Debe variar menos de 1 rad/s (invariancia de escala)
    assert spread < 1.0, f"ω₁ varió {spread:.4f} rad/s entre N={{7,13,21,55}}"


def test_fundamental_k_matches_pi_over_L():
    d_m = node_spacing()
    for N in (7, 13, 21, 55):
        k = fundamental_k(N, d_m)
        assert k == pytest.approx(np.pi / (N * d_m))


# ------------------------------------------------------------------
# 3. Stress test + simetría (subproceso)
# ------------------------------------------------------------------
def _run_stress(tmp_path: Path) -> dict:
    out = tmp_path / "stress.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "stress_test_dp.py"),
            "--output", str(out),
        ],
        capture_output=True, text=True, check=False,
    )
    assert proc.returncode == 0, (
        f"stress_test_dp.py failed:\nSTDOUT:\n{proc.stdout}\n"
        f"STDERR:\n{proc.stderr}"
    )
    with open(out) as fh:
        return json.load(fh)


def test_stress_linearity_and_psi(tmp_path):
    report = _run_stress(tmp_path)
    a = report["analysis"]
    assert a["linearity_ok"], f"R²={a['linearity_r_squared']}"
    assert a["psi_ok"], f"Ψ_min={a['psi_min']}"


def test_stress_symmetry(tmp_path):
    report = _run_stress(tmp_path)
    a = report["analysis"]
    assert a["symmetry_ok"], (
        f"Δf(-)={a['symmetry_delta_f_neg_mhz']} "
        f"Δf(+)={a['symmetry_delta_f_pos_mhz']} "
        f"dev={a['symmetry_deviation_mhz']}"
    )


def test_stress_status_validated(tmp_path):
    report = _run_stress(tmp_path)
    assert report["status"] == "VALIDATED", report["status"]


# ------------------------------------------------------------------
# 4. Predicción experimental: ω₁ ≈ ω_Ψ (890.8 rad/s)
# ------------------------------------------------------------------
def test_omega1_matches_omega_psi_reference():
    p = FieldParams()
    d = DiffusionParams()
    rows = sweep_fibonacci([7, 13, 21, 55], p, d)
    mean_abs = np.mean([abs(r["omega_1_real_rad_s"]) for r in rows])
    # |ω₁| debe coincidir con ω_Ψ = 2κ√λ dentro de 1 rad/s
    assert abs(mean_abs - p.omega_psi) < 1.0, (
        f"|ω₁|={mean_abs:.4f} vs ω_Ψ={p.omega_psi:.4f}"
    )


# ------------------------------------------------------------------
# Runner standalone (compatibilidad con scripts/run_all_tests.py)
# ------------------------------------------------------------------
def _run_all_standalone() -> int:
    import inspect
    tests = [
        (name, obj)
        for name, obj in globals().items()
        if name.startswith("test_") and inspect.isfunction(obj)
    ]
    passed = failed = 0
    for name, fn in tests:
        try:
            sig = inspect.signature(fn)
            if "tmp_path" in sig.parameters:
                with tempfile.TemporaryDirectory() as td:
                    fn(Path(td))
            else:
                fn()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as exc:                        # noqa: BLE001
            print(f"  ❌ {name}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(_run_all_standalone())
