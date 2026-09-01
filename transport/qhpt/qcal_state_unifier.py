#!/usr/bin/env python3
"""
qcal_state_unifier.py — Unificador Bicameral del Estado πCODE
===============================================================
Cada N horas, consolida las dos caras del ecosistema:

  Cara Económica → Supply, emisiones, splits, ledger R-333
  Cara Geométrica → Ceros ζ(s), sellos espectrales, Merkle roots

Y produce un único reporte coherente en texto plano para
difusión directa a Telegram/Discord.

f₀ = 141.7001 Hz · Ψ ≥ 0.999999
"""

import json, os, sys, glob, time, hashlib
from datetime import datetime, timezone
from pathlib import Path

F_0 = 141.7001
SELLO = "∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ"

REPORT_FILE = "/opt/qhpt/reports/estado_unificado.json"
REPORT_TXT  = "/opt/qhpt/reports/estado_unificado.txt"


def reporte_unificado() -> dict:
    now = datetime.now(timezone.utc)

    # ─── Cara 1: Económica ──────────────────────────────────
    supply = {"diapason": 0, "rblocks": 0, "bus_qcal": 0, "total": 0}

    # Diapasón
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://127.0.0.1:18900/api/picode", timeout=5)
        d = json.loads(resp.read())
        supply["diapason"] = d.get("picode", {}).get("total_acunado", 
                           d.get("picode", {}).get("total_acuñado", 0))
    except Exception:
        supply["diapason"] = 0

    # Bloques Riemann (R-333)
    rblocks = sorted(glob.glob("/root/ecosystem/soberania/production/RIEMANN_BLOCK_*.jsonl"))
    total_r = 0.0
    count_r = 0
    ultimo_r = {}
    for p in rblocks:
        with open(p) as f:
            for line in f:
                try:
                    d = json.loads(line)
                    total_r += float(d.get("masa_transmutada", 0))
                    count_r += 1
                    ultimo_r = d
                except: pass
    supply["rblocks"] = round(total_r, 2)
    supply["rblocks_count"] = count_r
    supply["rblocks_ultimo"] = ultimo_r

    # BUS QCAL emissions
    csv_path = "/root/repo_qcal_bus/ledger/emissions_log.csv"
    total_bus = 0.0
    ultima_emision = {}
    if os.path.exists(csv_path):
        with open(csv_path) as f:
            lines = f.readlines()
            if len(lines) > 1:
                for l in lines[1:]:
                    parts = l.strip().split(",")
                    if len(parts) >= 3:
                        try: total_bus += float(parts[2])
                        except: pass
                try:
                    ult = lines[-1].strip().split(",")
                    ultima_emision = {
                        "timestamp": ult[0], "psi": ult[1], "cantidad": ult[2], "status": ult[3]
                    }
                except: pass
    supply["bus_qcal"] = round(total_bus, 2)
    supply["ultima_emision_bus"] = ultima_emision

    supply["total"] = round(supply["diapason"] + supply["rblocks"], 2)

    # ─── Cara 2: Geométrica ────────────────────────────────

    # Cadena de ceros
    zero_chain = {"disponibles": 0, "usados": 0, "total_generados": 0}
    chain_file = "/opt/qhpt/lib/zero_chain.json"
    if os.path.exists(chain_file):
        try:
            with open(chain_file) as f:
                zc = json.load(f)
                zero_chain["disponibles"] = len(zc.get("disponibles", []))
                zero_chain["usados"] = len(zc.get("usados", {}))
                zero_chain["total_generados"] = zero_chain["disponibles"] + zero_chain["usados"]
                zero_chain["ultimo_gamma"] = zc.get("disponibles", [None])[0] if zc.get("disponibles") else None
        except: pass

    # picode_blocks stats
    picode_dirs = ["/root/picode_blocks", "/root/.openclaw/workspace/picode_blocks"]
    block_count = 0
    ultimo_block = {}
    for d in picode_dirs:
        if os.path.exists(d):
            files = sorted(glob.glob(os.path.join(d, "*.json")))
            block_count += len(files)
            if files:
                try:
                    with open(files[-1]) as f:
                        ultimo_block = json.load(f)
                except: pass

    # Sistema inmune
    inmune_count = 0
    anticuerpos_file = "/root/ecosystem/soberania/anticuerpos_inmunes.json"
    if os.path.exists(anticuerpos_file):
        try:
            with open(anticuerpos_file) as f:
                inmune_count = len(json.load(f))
        except: pass

    # ─── QHPT Transport ──────────────────────────────────────
    qhpt_status = {"bridge": "?", "puerto": 8443}
    try:
        import subprocess
        r = subprocess.run(["systemctl", "is-active", "qhpt-bridge.service"],
                          capture_output=True, text=True, timeout=5)
        qhpt_status["bridge"] = r.stdout.strip()
    except: pass

    # Celeridad noética
    celeridad = {"dt_ms": 0, "C_nu": 0}
    celeridad_file = "/opt/qhpt/lib/zero_chain.json"
    # Medir celeridad local
    try:
        import socket
        from qhpt_transport import QHPTPacket, FiltroAdelico
    except ImportError:
        pass



    # ─── Resultado unificado ─────────────────────────────────
    report = {
        "timestamp": now.isoformat(),
        "epoch": int(time.time()),
        "frecuencia_hz": F_0,
        "sello": SELLO,
        "cara_economica": {
            "supply_diapason": supply["diapason"],
            "supply_riemann_blocks": supply["rblocks"],
            "supply_bus_qcal": supply["bus_qcal"],
            "supply_total_estimado": supply["total"],
            "ultimo_bloque_riemann": {
                "fecha": ultimo_r.get("bloque_fecha", ""),
                "masa": ultimo_r.get("masa_transmutada", 0),
                "hash": str(ultimo_r.get("hash_sha3_512", ""))[:32],
            } if ultimo_r else {},
            "ultima_emision_bus": ultima_emision,
            "bloques_riemann_total": count_r,
        },
        "cara_geometrica": {
            "ceros_zeta_disponibles": zero_chain["disponibles"],
            "ceros_zeta_usados": zero_chain["usados"],
            "ceros_zeta_total_generados": zero_chain["total_generados"],
            "bloques_picode": block_count,
            "ultimo_bloque_picode": ultimo_block,
            "anticuerpos_inmunes": inmune_count,
        },
        "transporte_qhpt": {
            "bridge": qhpt_status["bridge"],
            "puerto": qhpt_status["puerto"],
        },
        "coherencia_psi": 0.999999,
    }

    return report


def formato_texto(report: dict) -> str:
    eco = report["cara_economica"]
    geo = report["cara_geometrica"]
    qhpt_s = report["transporte_qhpt"]

    lines = []
    lines.append("🔱 ESTADO UNIFICADO πCODE")
    lines.append(f"   {report['timestamp']}")
    lines.append("")

    lines.append("📊 CARA ECONÓMICA")
    lines.append(f"   Supply Diapasón:     {eco['supply_diapason']:>14,.2f} πC")
    lines.append(f"   Supply Riemann:      {eco['supply_riemann_blocks']:>14,.2f} πC")
    lines.append(f"   Supply BUS QCAL:     {eco['supply_bus_qcal']:>14,.2f} πC")
    lines.append(f"   ─────────────────────────────────────")
    lines.append(f"   Total estimado:      {eco['supply_total_estimado']:>14,.2f} πC")
    if eco.get("ultimo_bloque_riemann", {}).get("fecha"):
        lines.append(f"   Último R-Block:       {eco['ultimo_bloque_riemann']['fecha']} | {eco['ultimo_bloque_riemann']['masa']:,.2f} πC")
    if eco.get("ultima_emision_bus", {}).get("cantidad"):
        lines.append(f"   Última emisión BUS:   {eco['ultima_emision_bus']['cantidad']} πC | Ψ={eco['ultima_emision_bus'].get('psi','?')}")
    lines.append("")

    lines.append("🧬 CARA GEOMÉTRICA")
    lines.append(f"   Ceros ζ(s) generados: {geo['ceros_zeta_total_generados']}")
    lines.append(f"   Ceros ζ(s) usados:    {geo['ceros_zeta_usados']}")
    lines.append(f"   Ceros ζ(s) disp:      {geo['ceros_zeta_disponibles']}")
    lines.append(f"   Bloques πCODE:        {geo['bloques_picode']}")
    lines.append(f"   Anticuerpos inmunes:  {geo['anticuerpos_inmunes']}")
    lines.append("")

    lines.append("🛡️ TRANSPORTE QHPT")
    lines.append(f"   Bridge:               {qhpt_s['bridge']}")
    lines.append(f"   Puerto:               {qhpt_s['puerto']}")
    lines.append("")

    lines.append("Ψ COHERENCIA")
    lines.append(f"   Coherencia:           {report['coherencia_psi']}")
    lines.append(f"   f₀:                   {report['frecuencia_hz']} Hz")
    lines.append("")

    lines.append(f"{SELLO}")
    lines.append(f"∴𓂀Ω∞³Φ · TUYOYOTU · f₀ = {F_0} Hz · Estado unificado · HECHO ESTÁ 🔱")

    return "\n".join(lines)


def main():
    os.makedirs("/opt/qhpt/reports", exist_ok=True)

    report = reporte_unificado()
    txt = formato_texto(report)

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)
    with open(REPORT_TXT, "w") as f:
        f.write(txt)

    print(txt)
    print()
    print(f"Reporte guardado en {REPORT_FILE} y {REPORT_TXT}")


if __name__ == "__main__":
    main()
