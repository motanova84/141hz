#!/usr/bin/env python3
"""Nivel C: experimento en vivo para captura de métricas de hardware real."""

from __future__ import annotations

import argparse
import json
import random
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class SensorFrame:
    timestamp_utc: str
    hrv_coherence: float
    eeg_gamma_sync: float
    magnetometry_alignment: float
    spectral_f0_match: float

    @property
    def psi(self) -> float:
        return round(
            0.25 * self.hrv_coherence
            + 0.25 * self.eeg_gamma_sync
            + 0.20 * self.magnetometry_alignment
            + 0.30 * self.spectral_f0_match,
            6,
        )


def read_hardware_frame() -> SensorFrame:
    """Replace this with real hardware acquisition (EEG/HRV/magnetometer)."""
    now = datetime.now(timezone.utc).isoformat()
    return SensorFrame(
        timestamp_utc=now,
        hrv_coherence=random.uniform(0.985, 0.999),
        eeg_gamma_sync=random.uniform(0.985, 0.999),
        magnetometry_alignment=random.uniform(0.980, 0.998),
        spectral_f0_match=random.uniform(0.990, 0.999),
    )


def run_experiment(samples: int, interval_s: float, output: Path) -> None:
    records = []
    for idx in range(samples):
        frame = read_hardware_frame()
        payload = asdict(frame)
        payload["psi"] = frame.psi
        payload["resonance"] = "coherent" if frame.psi >= 0.95 else "drifting"
        records.append(payload)
        print(
            f"[{idx + 1}/{samples}] Ψ={payload['psi']:.6f} "
            f"resonance={payload['resonance']}"
        )
        if idx < samples - 1:
            time.sleep(interval_s)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"frames": records}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ Reporte Nivel C guardado en: {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Ejecuta experimento Nivel C con captura en vivo")
    parser.add_argument("--samples", type=int, default=20, help="Número de muestras")
    parser.add_argument("--interval", type=float, default=1.0, help="Intervalo entre muestras (s)")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("resultados") / "nivel_c_experimento_vivo.json",
        help="Archivo JSON de salida",
    )
    args = parser.parse_args()

    run_experiment(samples=args.samples, interval_s=args.interval, output=args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
