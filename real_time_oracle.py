"""
Utilidades de ejecución en tiempo real para el oráculo gravitacional.
"""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from qcal_gravitational_oracle import GravitationalOracle, MATPLOTLIB_AVAILABLE, plt


class RealTimeGravitationalOracle:
    """Oráculo con buffer circular e historial incremental."""

    def __init__(self, f_target: float = 141.7001, buffer_duration: int = 32, update_interval: float = 2.0):
        self.f_target = float(f_target)
        self.buffer_duration = int(buffer_duration)
        self.update_interval = float(update_interval)
        self.sample_rate = 4096
        self.base_oracle = GravitationalOracle(f_target=self.f_target, verbose=False)
        self.history: List[Dict[str, Any]] = []
        self.ifos: List[str] = []
        self._buffers: Dict[str, np.ndarray] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._last_processed_at: Optional[float] = None

    @property
    def running(self) -> bool:
        return self._running

    def start_acquisition(self, ifos: Optional[Iterable[str]] = None) -> None:
        self.ifos = list(ifos or ["H1", "L1"])
        buffer_size = max(self.buffer_duration * self.sample_rate, self.sample_rate)
        self._buffers = {ifo: np.zeros(buffer_size, dtype=float) for ifo in self.ifos}
        self._running = True
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(target=self._synthetic_acquisition_loop, daemon=True)
            self._thread.start()

    def stop_acquisition(self) -> None:
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

    def ingest_samples(self, ifo: str, samples: np.ndarray) -> None:
        if ifo not in self._buffers:
            self.ifos.append(ifo)
            self._buffers[ifo] = np.zeros(max(self.buffer_duration * self.sample_rate, len(samples)), dtype=float)
        samples = np.asarray(samples, dtype=float)
        with self._lock:
            buffer = self._buffers[ifo]
            if len(samples) >= len(buffer):
                self._buffers[ifo] = samples[-len(buffer):]
            else:
                self._buffers[ifo] = np.concatenate([buffer[len(samples):], samples])

    def get_buffer_snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return {
                ifo: self.base_oracle._build_timeseries(values.copy(), sample_rate=self.sample_rate, name=f"{ifo}-realtime")
                for ifo, values in self._buffers.items()
            }

    def process_current_buffer(self, timestamp: Optional[float] = None) -> Optional[Dict[str, Any]]:
        if not self._buffers:
            return None
        snapshot = self.get_buffer_snapshot()
        metrics = self.base_oracle.calculate_spectral_metrics(snapshot, self.sample_rate)
        classification = self.base_oracle.classify_noise(metrics)
        result = {
            "timestamp": float(time.time() if timestamp is None else timestamp),
            "metrics": metrics,
            "classification": classification,
            "ifos": list(snapshot.keys()),
        }
        self.base_oracle.results = {
            "raw_data": snapshot,
            "metrics": metrics,
            "noise_classification": classification,
        }
        self.history.append(result)
        self._last_processed_at = result["timestamp"]
        return result

    def _synthetic_acquisition_loop(self) -> None:
        chunk_duration = min(max(self.update_interval, 0.25), 2.0)
        phase_map = {"H1": 0.0, "L1": np.pi / 12, "V1": np.pi / 8}
        while self._running:
            samples = max(int(self.sample_rate * chunk_duration), 64)
            t = np.arange(samples, dtype=float) / self.sample_rate
            for ifo in list(self.ifos):
                rng = np.random.default_rng(int((time.time() * 1e6) % (2 ** 32)))
                noise = rng.normal(0.0, 0.08, samples)
                signal_line = 0.02 * np.sin(2 * np.pi * self.f_target * t + phase_map.get(ifo, 0.0))
                self.ingest_samples(ifo, noise + signal_line)
            self.process_current_buffer()
            time.sleep(chunk_duration)


class RealTimeSimulator:
    """Inyector de datos sintéticos para pruebas de ejecución continua."""

    def __init__(self, oracle: RealTimeGravitationalOracle):
        self.oracle = oracle
        self._stop_event = threading.Event()

    def stop_simulation(self) -> None:
        self._stop_event.set()
        self.oracle.stop_acquisition()

    def start_simulation(self, duration: float = 60, injection_time: float = 20, injection_duration: float = 5) -> None:
        if not self.oracle.ifos:
            self.oracle.ifos = ["H1", "L1"]
        if not self.oracle._buffers:
            buffer_size = max(self.oracle.buffer_duration * self.oracle.sample_rate, self.oracle.sample_rate)
            self.oracle._buffers = {ifo: np.zeros(buffer_size, dtype=float) for ifo in self.oracle.ifos}
        self.oracle._running = True
        chunk_duration = min(max(self.oracle.update_interval, 0.25), 1.0)
        phase_map = {"H1": 0.0, "L1": np.pi / 10, "V1": np.pi / 6}
        elapsed = 0.0
        while elapsed < duration and not self._stop_event.is_set():
            samples = max(int(self.oracle.sample_rate * chunk_duration), 64)
            t = np.arange(samples, dtype=float) / self.oracle.sample_rate + elapsed
            injection_active = injection_time <= elapsed <= injection_time + injection_duration
            for ifo in self.oracle.ifos:
                rng = np.random.default_rng(int((elapsed * 1e6) + abs(hash(ifo)) % 1000))
                noise = rng.normal(0.0, 0.06, samples)
                amplitude = 0.02 if not injection_active else 0.12
                line = amplitude * np.sin(2 * np.pi * self.oracle.f_target * t + phase_map.get(ifo, 0.0))
                self.oracle.ingest_samples(ifo, noise + line)
            self.oracle.process_current_buffer(timestamp=elapsed)
            elapsed += chunk_duration
            time.sleep(min(chunk_duration, 0.05))
        self.oracle._running = False


class RealTimeVisualizer:
    """Visualizador simple para historial en tiempo real."""

    def __init__(self, oracle: RealTimeGravitationalOracle):
        self.oracle = oracle

    def run(self, max_frames: Optional[int] = None) -> None:
        if MATPLOTLIB_AVAILABLE:
            self._run_matplotlib(max_frames=max_frames)
            return
        self._run_text(max_frames=max_frames)

    def _run_text(self, max_frames: Optional[int] = None) -> None:
        frames = 0
        while self.oracle.running and (max_frames is None or frames < max_frames):
            if self.oracle.history:
                last = self.oracle.history[-1]
                print(
                    f"[RT] t={last['timestamp']:.2f}s coh={last['classification']['coherence']:.3f} "
                    f"snr={last['classification']['snr']:.2f} status={last['classification']['status']}"
                )
            time.sleep(max(self.oracle.update_interval, 0.1))
            frames += 1

    def _run_matplotlib(self, max_frames: Optional[int] = None) -> None:
        plt.ion()
        fig, axes = plt.subplots(2, 1, figsize=(10, 6))
        frames = 0
        while self.oracle.running and (max_frames is None or frames < max_frames):
            axes[0].clear()
            axes[1].clear()
            if self.oracle.history:
                times = [item["timestamp"] for item in self.oracle.history]
                coherences = [item["classification"]["coherence"] for item in self.oracle.history]
                snrs = [item["classification"]["snr"] for item in self.oracle.history]
                axes[0].plot(times, coherences, label="Coherencia")
                axes[0].axhline(self.oracle.base_oracle.umbral_coherencia_ruido, color="r", linestyle="--")
                axes[1].plot(times, snrs, label="SNR", color="tab:orange")
                axes[1].axhline(self.oracle.base_oracle.umbral_snr_minimo, color="r", linestyle="--")
                axes[0].legend()
                axes[1].legend()
            axes[0].set_ylabel("Coherencia")
            axes[1].set_ylabel("SNR [dB]")
            axes[1].set_xlabel("Tiempo [s]")
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(max(self.oracle.update_interval, 0.1))
            frames += 1
        plt.ioff()
        plt.close(fig)
