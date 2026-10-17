import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import run_oracle


def test_parse_arguments_defaults():
    args = run_oracle.parse_arguments([])
    assert args.mode == "single"
    assert args.evento == "GW150914"
    assert args.plot is True
    assert args.interfaz == ["H1", "L1"]


def test_parse_arguments_no_plot():
    args = run_oracle.parse_arguments(["--mode", "simulate", "--no-plot", "--interfaz", "H1", "L1", "V1"])
    assert args.mode == "simulate"
    assert args.plot is False
    assert args.interfaz == ["H1", "L1", "V1"]


def test_save_results_serializes_numpy_and_timeseries(tmp_path):
    oracle = run_oracle.GravitationalOracle(verbose=False)
    results = oracle.analyze(evento="SERIAL_TEST", t_gps=1126259462.4, duracion=4, plot=False)
    output = tmp_path / "results.json"
    run_oracle.save_results(results, str(output))
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved["evento"] == "SERIAL_TEST"
    assert "metrics" in saved
    assert "raw_data" in saved


def test_save_realtime_history_extracts_summary(tmp_path):
    output = tmp_path / "history.json"
    history = [
        {
            "timestamp": 1.0,
            "classification": {
                "coherence": 0.8,
                "snr": 6.2,
                "phase": 12.0,
                "status": "LIMPIO",
            },
        }
    ]
    run_oracle.save_realtime_history(history, str(output))
    saved = json.loads(output.read_text(encoding="utf-8"))
    assert saved[0]["coherence"] == 0.8
    assert saved[0]["status"] == "LIMPIO"


def test_run_single_analysis_with_output(tmp_path):
    args = run_oracle.parse_arguments(["--mode", "single", "--evento", "TEST_SYNTHETIC", "--duracion", "4"])
    args.output = str(tmp_path / "single.json")
    results = run_oracle.run_single_analysis(args)
    assert results["evento"] == "TEST_SYNTHETIC"
    assert Path(args.output).exists()


def test_run_simulation_with_patched_visualizer(tmp_path, monkeypatch):
    calls = {"ran": False}

    def fake_run(self):
        calls["ran"] = True
        while self.oracle.running:
            if self.oracle.history:
                break

    monkeypatch.setattr(run_oracle.RealTimeVisualizer, "run", fake_run)
    args = run_oracle.parse_arguments(
        ["--mode", "simulate", "--simulate-duration", "1", "--inject-time", "0", "--output", str(tmp_path / "rt.json")]
    )
    history = run_oracle.run_simulation(args)
    assert calls["ran"] is True
    assert len(history) >= 1
    assert Path(args.output).exists()
