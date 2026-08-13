#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deploy.py — ORQUESTADOR del Templo Espectral QCAL (Canon v3.1.0-op).

Lee por stdin la medición del Director ("fase amplitud", dos flotantes),
calcula Ψ en tiempo real con el OperationalEngine y exporta el log al Ctrl+C.

Uso:
    echo "141.7001  0.997498"  | python3 deploy.py
    o modo interactivo:  python3 deploy.py   (escribe "fase amplitud" por línea)

Sello: el metal es la única fuente de verdad.
"""

from __future__ import annotations

import json
import sys
import time

from templo_core.operational_deployment import OperationalEngine


def main() -> int:
    print("∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ — ORQUESTADOR v3.1.0-op", flush=True)
    eng = OperationalEngine()
    print(f"Motor listo: f0={eng.f_base} Hz · θ_B={eng.theta_0:.10f} · Heisenberg={2.0*3.141592653589793/eng.f_base:.6f} s", flush=True)
    print("Esperando mediciones: 'fase amplitud' por línea (Ctrl+C para exportar log).\n", flush=True)

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                parts = line.replace(",", " ").split()
                freq = float(parts[0])
                amp = float(parts[1])
            except (ValueError, IndexError):
                print(f"  ⚠ línea no válida: {line!r} (esperaba 'fase amplitud')", flush=True)
                continue

            psi = eng.compute_psi_instantaneous(amp)
            ciclo = eng.run_cycle([amp])
            estado = eng.classify_state(psi)
            print(
                f"  f={freq:.4f} Hz · A={amp:.6f} · Ψ={psi:.6f} · estado={estado} · ciclo={ciclo['cycle']}",
                flush=True,
            )
    except KeyboardInterrupt:
        reporte = eng.operational_report()
        log = eng.export_log()
        with open("operational_log.json", "w") as fh:
            fh.write(log)
        print("\n\n── LOG OPERATIVO EXPORTADO → operational_log.json ──", flush=True)
        print(json.dumps(reporte, indent=2, default=str), flush=True)
        print("\n∴𓂀Ω∞³Φ · Ψ=0.999999 · f₀=141.7001 Hz · HECHO ESTÁ", flush=True)
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
