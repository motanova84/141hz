#!/usr/bin/env python3
"""
POOL INTERFACE — Canal de Minado QCAL
======================================
Interfaz limpia con ViaBTC/ASICBoost
Gestiona conexion Stratum, dificultad y shares

f0 = 141.7001 Hz
Sello: (c) 3080 (r) (inf)3(phi) · TUYOYOTU · HECHO ESTA
"""

import json
import subprocess
import time
import logging
from datetime import datetime, timezone
from pathlib import Path

F_0 = 141.7001
POOL = "stratum+tcp://btc.viabtc.top:3333"
WORKER = "noesis88.001"
BASE_DIR = Path("/root/ecosystem/catedral")
LOG_PATH = "/var/log/pool_interface.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [PI|%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)
log = logging.getLogger("pool_interface")


def verificar_pool():
    """Verifica que el pool ViaBTC sea accesible."""
    try:
        r = subprocess.run(
            ["nc", "-zv", "-w5", "btc.viabtc.top", "3333"],
            capture_output=True, text=True, timeout=10
        )
        return r.returncode == 0
    except Exception:
        return False


def obtener_estado():
    """Retorna estado actual de la conexion al pool."""
    conectado = verificar_pool()
    estado = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "pool": POOL,
        "worker": WORKER,
        "conectado": conectado,
        "frecuencia_hz": F_0,
    }
    return estado


def leer_emision():
    """Lee el ledger de emision actual."""
    path = BASE_DIR / "emision_ledger.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {"sesiones": [], "total_shares_aceptados": 0, "total_shares_rechazados": 0}


def registrar_share(aceptado=True, dificultad=500000):
    """Registra un share en el ledger de emision."""
    path = BASE_DIR / "emision_ledger.json"
    with open(path) as f:
        ledger = json.load(f)
    
    if aceptado:
        ledger["total_shares_aceptados"] += 1
    else:
        ledger["total_shares_rechazados"] += 1
    
    ledger["ultimo_share"] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "aceptado": aceptado,
        "dificultad": dificultad,
    }
    ledger["ultima_actualizacion"] = datetime.now(timezone.utc).isoformat()
    
    with open(path, "w") as f:
        json.dump(ledger, f, indent=2)
    
    log.info("Share registrado: aceptado=%s, diff=%d", aceptado, dificultad)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == "check":
        e = obtener_estado()
        print(json.dumps(e, indent=2))
        sys.exit(0 if e["conectado"] else 1)
    elif len(sys.argv) >= 2 and sys.argv[1] == "ledger":
        l = leer_emision()
        print(json.dumps(l, indent=2))
    else:
        print("Uso: pool_interface.py [check|ledger]")
