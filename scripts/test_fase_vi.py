#!/usr/bin/env python3
"""
Tests para QCAL Fase VI — cadena de 13 nodos y modo de escucha.

Uso:
    pytest scripts/test_fase_vi.py -q
    python  scripts/test_fase_vi.py

Sello: QCAL-INYECCION-INMEDIATA-v3.0
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

from experimento_cadena_13 import (  # noqa: E402
    ChainParams,
    envelope,
    fit_envelope,
    simulate_chain,
    K0_PRED,
    XI_PRED_M,
)
from fase_vi_escucha_ambiental import (  # noqa: E402
    BANDS,
    band_cross_correlation,
    CORR_HIGH,
    CORR_LOW,
)


# ------------------------------------------------------------------
# 1. Cadena — simetría de la envolvente y ajuste
# ------------------------------------------------------------------
def test_envelope_symmetric_in_r():
    for r in (0.1, 0.5, 1.0, 2.5):
        a = envelope(r, 10.0, 1.4, 29.8, 0.0)
        b = envelope(-r, 10.0, 1.4, 29.8, 0.0)
        assert np.isclose(a, b, rtol=1e-12)


def test_envelope_at_zero():
    val = envelope(0.0, 12.34, 1.4, 29.8, 0.1)
    assert np.isclose(val, 12.34 * np.cos(0.1), rtol=1e-12)


def test_chain_fit_recovers_xi_and_k0():
    params = ChainParams()
    sim = simulate_chain(params)
    fit = fit_envelope(sim["r_m"], sim["df_measured_mhz"])
    assert abs(fit["xi_fit_m"] - XI_PRED_M) < 0.15
    assert abs(fit["k0_fit_rad_per_m"] - K0_PRED) < 2.0
    assert fit["rmse_mhz"] < 0.10


# ------------------------------------------------------------------
# 2. Cross-correlación — señales ortogonales vs acopladas
# ------------------------------------------------------------------
def test_cross_correlation_orthogonal_noise():
    rng = np.random.default_rng(1)
    x = rng.normal(0.0, 1.0, size=4096)
    y = rng.normal(0.0, 1.0, size=4096)
    rho = band_cross_correlation(x, y, max_lag=100)
    assert 0.0 <= rho < 0.2


def test_cross_correlation_identical_series_is_one():
    rng = np.random.default_rng(2)
    x = rng.normal(0.0, 1.0, size=2048)
    rho = band_cross_correlation(x, x, max_lag=32)
    assert rho == pytest.approx(1.0, abs=1e-9)


def test_bands_have_expected_frequencies():
    freqs = {b.name: b.f_hz for b in BANDS}
    assert freqs["mains_50hz"] == 50.0
    assert freqs["schumann_7p83"] == pytest.approx(7.83)


def test_threshold_ordering():
    assert 0.0 < CORR_LOW < CORR_HIGH < 1.0


# ------------------------------------------------------------------
# 3. Ejecuciones extremo a extremo (subproceso)
# ------------------------------------------------------------------
def _run(cmd) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def test_chain_script_end_to_end(tmp_path):
    out = tmp_path / "cadena13.json"
    rc, so, se = _run([sys.executable,
                       str(SCRIPTS / "experimento_cadena_13.py"),
                       "--output", str(out)])
    assert rc == 0, f"stdout:\n{so}\nstderr:\n{se}"
    report = json.loads(out.read_text())
    assert report["status"] == "VALIDATED"
    assert report["validation"]["xi_ok"]
    assert report["validation"]["k0_ok"]
    assert report["validation"]["rmse_ok"]


def test_listening_closed_scenario(tmp_path):
    out = tmp_path / "closed.json"
    rc, so, se = _run([sys.executable,
                       str(SCRIPTS / "fase_vi_escucha_ambiental.py"),
                       "--hours", "2", "--coupling", "closed",
                       "--output", str(out)])
    assert rc == 0, f"stdout:\n{so}\nstderr:\n{se}"
    report = json.loads(out.read_text())
    assert report["verdict"] == "CLOSED_SYSTEM"
    assert report["global_max_correlation"] < CORR_LOW


def test_listening_open_scenario(tmp_path):
    out = tmp_path / "open.json"
    rc, so, se = _run([sys.executable,
                       str(SCRIPTS / "fase_vi_escucha_ambiental.py"),
                       "--hours", "2", "--coupling", "open",
                       "--output", str(out)])
    assert rc == 0, f"stdout:\n{so}\nstderr:\n{se}"
    report = json.loads(out.read_text())
    assert report["verdict"] == "OPEN_TRANSDUCER"
    assert report["open_hits"] >= 1


# ------------------------------------------------------------------
# Runner standalone
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
