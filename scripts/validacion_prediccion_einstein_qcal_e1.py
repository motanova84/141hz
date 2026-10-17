#!/usr/bin/env python3
"""
Validación operativa de la predicción Einstein-QCAL QCAL-E1.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from contexto_ecosistema import resumen_ecosistema
from contexto_ecosistema.einstein_qcal_context import ECOSYSTEM_SUMMARY, resumen_contexto_einstein_qcal
from qcal.constants import F0_HZ
from qcal.einstein_qcal_e1 import QCALE1Measurement, build_qcal_e1_contract, evaluate_qcal_e1
from scripts.protocolo_metrologia_qcal import (
    SAMPLE_RATE_HIGH_HZ,
    ProtocoloMedicion,
    exportar_csv,
)
from scripts.validacion_alternativa_interferometrica import verificar_compatibilidad_interferometrica


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validación operativa de la predicción Einstein-QCAL QCAL-E1.")
    parser.add_argument("--output-dir", type=str, default="results", help="Directorio para JSON y CSV auditables.")
    parser.add_argument("--cavity-length-m", type=float, default=4000.0, help="Longitud efectiva de cavidad.")
    parser.add_argument("--duration-s", type=int, default=4, help="Duración de metrología por corrida.")
    parser.add_argument("--sample-rate", type=float, default=SAMPLE_RATE_HIGH_HZ, help="Frecuencia de muestreo.")
    parser.add_argument("--seed", type=int, default=42, help="Semilla reproducible.")
    parser.add_argument("--a-eff", type=float, default=7.0, help="Área efectiva / nodos.")
    parser.add_argument("--nodo-id", type=str, default="BAL-003", help="Nodo metrológico.")
    parser.add_argument("--detector-sensitivity", type=float, default=1e-24, help="Sensibilidad strain del detector.")
    parser.add_argument("--detected-peak-frequency", type=float, default=F0_HZ, help="Frecuencia observada del pico.")
    parser.add_argument("--detected-peak-power", type=float, default=1.0, help="Potencia normalizada del pico.")
    parser.add_argument("--psi-override", type=float, default=None, help="Sobrescribe Ψ_obs derivada de metrología.")
    return parser.parse_args(argv)


def _run_metrology(
    frequency_hz: float,
    duration_s: int,
    sample_rate_hz: float,
    seed: int,
    a_eff: float,
    nodo_id: str,
    output_path: Path,
) -> dict:
    protocolo = ProtocoloMedicion(
        frecuencia_hz=frequency_hz,
        a_eff=a_eff,
        seed=seed,
        nodo_id=nodo_id,
        sample_rate_hz=sample_rate_hz,
    )
    df = protocolo.generar_dataset(duracion_s=duration_s)
    exportar_csv(df, output_path)
    psi_series = df["psi_emp_calc"].astype(float).to_numpy()
    intensity_series = df["intensidad_picode_s"].astype(float).to_numpy()
    return {
        "csv_path": str(output_path),
        "rows": int(len(df)),
        "psi_mean": float(np.mean(psi_series)),
        "psi_std": float(np.std(psi_series)),
        "psi_median": float(np.median(psi_series)),
        "intensity_mean": float(np.mean(intensity_series)),
        "intensity_std": float(np.std(intensity_series)),
        "sha256_first_row": str(df.iloc[0]["firma_sha256"]),
    }


def run_validation(args: argparse.Namespace) -> dict:
    output_dir = ROOT_DIR / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    stimulated_path = output_dir / "einstein_qcal_e1_metrology_stimulated.csv"
    baseline_path = output_dir / "einstein_qcal_e1_metrology_baseline.csv"

    stimulated = _run_metrology(
        frequency_hz=F0_HZ,
        duration_s=args.duration_s,
        sample_rate_hz=args.sample_rate,
        seed=args.seed,
        a_eff=args.a_eff,
        nodo_id=args.nodo_id,
        output_path=stimulated_path,
    )
    baseline = _run_metrology(
        frequency_hz=0.0,
        duration_s=args.duration_s,
        sample_rate_hz=args.sample_rate,
        seed=args.seed + 1,
        a_eff=args.a_eff,
        nodo_id=f"{args.nodo_id}-BASELINE",
        output_path=baseline_path,
    )

    psi_obs = args.psi_override if args.psi_override is not None else stimulated["psi_median"]
    contract = build_qcal_e1_contract()

    measurement = QCALE1Measurement(
        psi_obs=psi_obs,
        cavity_length_m=args.cavity_length_m,
        f_observer_hz=F0_HZ,
        detector_sensitivity_hz_sqrt=args.detector_sensitivity,
        detected_peak_frequency_hz=args.detected_peak_frequency,
        detected_peak_power=args.detected_peak_power,
        phase_velocity_sensitive=True,
    )
    evaluation = evaluate_qcal_e1(measurement, contract)
    compatibility = verificar_compatibilidad_interferometrica(contract.central_frequency_hz, args.cavity_length_m)

    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "prediction_id": contract.prediction_id,
        "title": contract.title,
        "input_parameters": {
            "cavity_length_m": args.cavity_length_m,
            "duration_s": args.duration_s,
            "sample_rate_hz": args.sample_rate,
            "seed": args.seed,
            "a_eff": args.a_eff,
            "nodo_id": args.nodo_id,
            "psi_override": args.psi_override,
            "detector_sensitivity_hz_sqrt": args.detector_sensitivity,
            "detected_peak_frequency_hz": args.detected_peak_frequency,
            "detected_peak_power": args.detected_peak_power,
        },
        "contract": evaluation.contract,
        "metrology": {
            "stimulated": stimulated,
            "baseline": baseline,
            "delta_psi_controlled": float(stimulated["psi_median"] - baseline["psi_median"]),
            "psi_obs_used": float(psi_obs),
        },
        "interferometric_compatibility": compatibility,
        "ecosystem": {
            "einstein_qcal": resumen_contexto_einstein_qcal(),
            "global": resumen_ecosistema(),
            "anchor_summary": ECOSYSTEM_SUMMARY,
        },
        "evaluation": evaluation.to_dict(),
        "overall_status": (
            "✓ QCAL-E1 SUPPORTED"
            if evaluation.verdict == "SUPPORTED"
            else "✗ QCAL-E1 FALSIFIED"
            if evaluation.verdict == "FALSIFIED"
            else "… QCAL-E1 INCONCLUSIVE"
        ),
    }

    output_path = output_dir / "prediccion_einstein_qcal_e1.json"
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)

    print(f"QCAL-E1 verdict: {evaluation.verdict}")
    print(f"Resultado JSON: {output_path}")
    return result


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    run_validation(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
