import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import qcal_gravitational_oracle as oracle_module
from qcal_gravitational_oracle import GravitationalOracle, SimpleTimeSeries


def _series(values: np.ndarray, sample_rate: float = 4096.0) -> SimpleTimeSeries:
    return SimpleTimeSeries(values, sample_rate=sample_rate, t0=0.0)


def test_fetch_ligo_data_falls_back_to_synthetic(monkeypatch):
    class FakeTimeSeries:
        @staticmethod
        def fetch_open_data(*args, **kwargs):
            raise RuntimeError("network unavailable")

    monkeypatch.setattr(oracle_module, "GWpyTimeSeries", FakeTimeSeries)
    oracle = GravitationalOracle(verbose=False)
    data = oracle.fetch_ligo_data(1126259462.4, duracion=4, ifos=["H1", "L1"])
    assert set(data) == {"H1", "L1"}
    assert all(len(series) == 4 * 4096 for series in data.values())
    assert all(np.std(series.value) > 0 for series in data.values())


def test_fetch_ligo_data_rejects_constant_series(monkeypatch):
    class FakeFetchedSeries(SimpleTimeSeries):
        pass

    class FakeTimeSeries:
        @staticmethod
        def fetch_open_data(*args, **kwargs):
            return FakeFetchedSeries(np.zeros(4096), sample_rate=4096.0, t0=0.0)

    monkeypatch.setattr(oracle_module, "GWpyTimeSeries", FakeTimeSeries)
    oracle = GravitationalOracle(verbose=False)
    data = oracle.fetch_ligo_data(1126259462.4, duracion=1, ifos=["H1"])
    assert np.std(data["H1"].value) > 0


def test_calculate_spectral_metrics_returns_expected_fields():
    oracle = GravitationalOracle(verbose=False)
    fs = 4096
    duration = 4
    t = np.arange(fs * duration) / fs
    base = 0.08 * np.sin(2 * np.pi * oracle.f_target * t)
    h1 = _series(base + 0.01 * np.sin(2 * np.pi * 80 * t), sample_rate=fs)
    l1 = _series(base + 0.01 * np.sin(2 * np.pi * 80 * t + np.pi / 8), sample_rate=fs)
    metrics = oracle.calculate_spectral_metrics({"H1": h1, "L1": l1}, fs)
    assert {"frequency", "psd_h1", "psd_l1", "coherence", "csd", "phase_deg", "idx_target", "snr_integrated", "fwhm", "fs", "nperseg"} <= set(metrics)
    assert metrics["nperseg"] > 0
    assert 0 <= metrics["idx_target"] < len(metrics["frequency"])
    assert np.isfinite(metrics["snr_integrated"])


def test_classify_noise_uses_thresholds():
    oracle = GravitationalOracle(verbose=False)
    metrics = {
        "idx_target": 0,
        "coherence": np.array([0.9]),
        "snr_integrated": 8.0,
        "phase_deg": np.array([10.0]),
    }
    result = oracle.classify_noise(metrics)
    assert result["status"].startswith("LIMPIO")
    assert result["details"] == {
        "coherence_check": True,
        "snr_check": True,
        "phase_check": True,
    }


def test_visualize_results_builds_six_axes():
    if not oracle_module.MATPLOTLIB_AVAILABLE:
        pytest.skip("matplotlib no disponible")
    oracle = GravitationalOracle(verbose=False)
    synthetic = oracle._generate_synthetic_data(4, 4096, ifo="H1")
    oracle.results["raw_data"] = {"H1": synthetic}
    metrics = oracle.calculate_spectral_metrics(
        {
            "H1": synthetic,
            "L1": oracle._generate_synthetic_data(4, 4096, ifo="L1"),
        },
        4096,
    )
    classification = oracle.classify_noise(metrics)
    fig = oracle.visualize_results(metrics, classification, "GW150914")
    assert len(fig.axes) == 6


def test_analyze_returns_structured_results(monkeypatch):
    oracle = GravitationalOracle(verbose=False)

    def fake_fetch(self, t_gps, duracion=32, ifos=None):
        return {
            ifo: self._generate_synthetic_data(duracion, 4096, ifo=ifo, t0=t_gps - duracion / 2)
            for ifo in (ifos or ["H1", "L1"])
        }

    monkeypatch.setattr(GravitationalOracle, "fetch_ligo_data", fake_fetch)
    results = oracle.analyze(evento="GW150914", t_gps=1126259462.4, duracion=4, plot=False)
    assert results["evento"] == "GW150914"
    assert "metrics" in results
    assert "noise_classification" in results
