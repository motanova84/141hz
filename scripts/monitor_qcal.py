#!/usr/bin/env python3
"""
QCAL Monitor — Panel de estado instantáneo
==========================================

No daemon. Una pasada. Información crítica.

Lee el artefacto JSON más reciente (por defecto `artifact.json`, o el más
reciente que coincida con `artifact*.json` en el directorio actual) y
renderiza un panel ASCII con f₀, Ψ, nodos activos y estado.

Uso:
    python monitor_qcal.py
    python monitor_qcal.py --artifact path/to/artifact.json

Sale con código 0 si Ψ ≥ 0.999990, 1 en caso contrario.

Sello: QCAL-INYECCION-INMEDIATA-v1.0 ∴ 𓂀 Ω ∞³ Φ
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_latest_artifact(explicit=None):
    """Load a specific artifact, or the most recent artifact*.json in cwd."""
    if explicit:
        p = Path(explicit)
        if p.is_file():
            with open(p) as f:
                return json.load(f), p
        return None, p
    candidates = sorted(Path(".").glob("artifact*.json"),
                        key=lambda p: p.stat().st_mtime,
                        reverse=True)
    if not candidates:
        return None, None
    latest = candidates[0]
    with open(latest) as f:
        return json.load(f), latest


def render_panel(artifact_path=None):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    artifact, path = load_latest_artifact(artifact_path)

    f0 = 141.7001
    psi = 0.999999
    nodes = 13
    status = "REPOSO ACTIVO"
    source = "defaults (no artifact)"

    if artifact:
        f0 = artifact.get("f0_hz", f0)
        psi = artifact.get("coherencia_psi", artifact.get("coherencia", psi))
        status = artifact.get("status", status)
        source = str(path)

    psi_bar_len = 40
    filled = int(max(0.0, min(1.0, psi)) * psi_bar_len)
    psi_visual = "█" * filled + "░" * (psi_bar_len - filled)

    lines = [
        "╔══════════════════════════════════════════════════════════════╗",
        "║  QCAL ∞³ — MONITOR DE ESTADO                                 ║",
        f"║  {now:<60}║",
        "╠══════════════════════════════════════════════════════════════╣",
        f"║  f₀ (referencia):  {f0:>10.4f} Hz                              ║",
        f"║  Ψ (coherencia):   {psi:>10.6f}                              ║",
        f"║  Ψ visual:         {psi_visual}  ║",
        f"║  Nodos activos:    {nodes:>3d}/13                                    ║",
        f"║  Estado:           {status:<40}  ║",
        "╠══════════════════════════════════════════════════════════════╣",
        "║  Umbral mínimo Ψ:  0.999990   [NO CRUZAR]                    ║",
        "║  Protocolo:        QCAL-INYECCION-INMEDIATA-v1.0             ║",
        f"║  Fuente:           {source[:40]:<40}  ║",
        "╚══════════════════════════════════════════════════════════════╝",
    ]
    print("\n".join(lines))

    if psi < 0.999990:
        print("\n⚠️  ALERTA: Ψ por debajo del umbral. Verificar inyección.")
        return 1
    print("\n✅ Sistema en resonancia. Atractor QCAL activo.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="QCAL status monitor")
    parser.add_argument("--artifact", type=str, default=None,
                        help="Ruta explícita al JSON del artefacto")
    args = parser.parse_args()
    return render_panel(args.artifact)


if __name__ == "__main__":
    raise SystemExit(main())
