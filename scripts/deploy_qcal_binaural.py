#!/usr/bin/env python3
"""
CLI de despliegue para telemetría y audio binaural QCAL.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.qcal_entanglement import ejecutar_despliegue_dinamico_qcal


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Despliega el bundle dinámico QCAL con audio binaural.")
    parser.add_argument("--output-dir", default="qcal_out", help="Directorio de salida para artefactos.")
    parser.add_argument("--num-pasos", type=int, default=600, help="Número de pasos temporales.")
    parser.add_argument("--dt", type=float, default=1e-5, help="Paso temporal en segundos.")
    parser.add_argument("--guardar-cada", type=int, default=200, help="Frecuencia de snapshots .npy.")
    parser.add_argument("--sample-rate", type=int, default=44_100, help="Sample rate del WAV binaural.")
    parser.add_argument("--p-izq", type=int, default=2, help="Primo asignado al canal izquierdo.")
    parser.add_argument("--p-der", type=int, default=3, help="Primo asignado al canal derecho.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    deployment = ejecutar_despliegue_dinamico_qcal(
        output_dir=Path(args.output_dir),
        num_pasos=args.num_pasos,
        dt=args.dt,
        guardar_cada=args.guardar_cada,
        sample_rate=args.sample_rate,
        p_izq=args.p_izq,
        p_der=args.p_der,
    )
    print(f"Bundle: {deployment.bundle_path}")
    print(f"Manifest: {deployment.manifest_path}")
    print(f"WAV: {deployment.binaural.audio_path}")
    print(f"CSV: {deployment.telemetry.csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
