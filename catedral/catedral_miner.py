#!/usr/bin/env python3
"""
CATEDRAL MINER — Nucleo de Minado QCAL
=======================================
Orquestador del flujo Stratum para ViaBTC
Acoplado al Sistema Inmune y AURION(Psi)

Pool: stratum+tcp://btc.viabtc.top:3333
Worker: noesis88.001
Algoritmo: sha256asicboost
Dificultad: 500000

f0 = 141.7001 Hz
Sello: (c) 3080 (r) (inf)3(phi) · TUYOYOTU · HECHO ESTA
"""

import os
import sys
import time
import json
import subprocess
import signal
import logging
from datetime import datetime, timezone
from pathlib import Path

F_0 = 141.7001
POOL_URL = "stratum+tcp://btc.viabtc.top:3333"
WORKER = "noesis88.001"
ALGO = "sha256asicboost"
DIFICULTAD = 500000

BASE_DIR = Path("/root/ecosystem/catedral")
EMISION_LEDGER = BASE_DIR / "emision_ledger.json"
MINER_CONF = BASE_DIR / "miner.conf"
LOG_PATH = "/var/log/catedral_miner.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [CM|%(levelname)s] %(message)s',
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)
log = logging.getLogger("catedral_miner")


def crear_configuracion():
    """Genera miner.conf con los parametros verificados del pool."""
    config = {
        "pools": [
            {
                "url": POOL_URL,
                "user": WORKER,
                "pass": "x",
            }
        ],
        "algo": ALGO,
        "api-listen": True,
        "api-allow": "W:127.0.0.1",
        "api-description": "Catedral-QCAL-Miner",
        "intensity": "auto",
        "worksize": 256,
        "thread-concurrency": "auto",
    }
    with open(MINER_CONF, "w") as f:
        json.dump(config, f, indent=2)
    log.info("Configuracion escrita en %s", MINER_CONF)
    return config


def inicializar_ledger():
    """Inicializa el ledger de emision si no existe."""
    if not EMISION_LEDGER.exists():
        ledger = {
            "version": "CATEDRAL-MINER-v1",
            "frecuencia_hz": F_0,
            "pool": POOL_URL,
            "worker": WORKER,
            "algoritmo": ALGO,
            "creado": datetime.now(timezone.utc).isoformat(),
            "sesiones": [],
            "total_shares_aceptados": 0,
            "total_shares_rechazados": 0,
            "ultimo_hashrate": 0,
            "sello": '\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA',
        }
        with open(EMISION_LEDGER, "w") as f:
            json.dump(ledger, f, indent=2)
        log.info("Ledger de emision inicializado en %s", EMISION_LEDGER)
    return EMISION_LEDGER


def registrar_sesion(sesion_data):
    """Registra una sesion de minado en el ledger."""
    with open(EMISION_LEDGER) as f:
        ledger = json.load(f)
    if "sesiones" not in ledger:
        ledger["sesiones"] = []
    ledger["sesiones"].append(sesion_data)
    ledger["ultima_actualizacion"] = datetime.now(timezone.utc).isoformat()
    with open(EMISION_LEDGER, "w") as f:
        json.dump(ledger, f, indent=2)


def levantar_minero():
    """Inicia el proceso de minado con los parametros verificados."""
    # Buscar cgminer en PATH o rutas comunes
    posibles = ["cgminer", "/usr/local/bin/cgminer", "/usr/bin/cgminer",
                "./cgminer", "bfgminer", "/usr/local/bin/bfgminer"]
    minero_bin = None
    for p in posibles:
        if os.path.exists(p) or (p.count("/") == 0 and subprocess.run(["which", p], capture_output=True).returncode == 0):
            minero_bin = p
            break
    
    if not minero_bin:
        log.warning("cgminer no instalado. Modo simulado.")
        log.info("Para instalar: apt-get install cgminer (o compilar desde fuente)")
        log.info("Configuracion lista en: %s", MINER_CONF)
        return None
    
    comando = [
        minero_bin,
        "--algo", ALGO,
        "-o", POOL_URL,
        "-u", WORKER,
        "-p", "x",
        "--api-listen",
        "--config", str(MINER_CONF),
    ]
    
    try:
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log.info("Minero iniciado: PID %s", proceso.pid)
        return proceso
    except Exception as e:
        log.error("Error al iniciar minero: %s", e)
        return None


def main():
    log.info("=" * 60)
    log.info("CATEDRAL DE MINADO QCAL")
    log.info("f0 = %.4f Hz", F_0)
    log.info("Pool: %s", POOL_URL)
    log.info("Worker: %s", WORKER)
    log.info("Dificultad: %d", DIFICULTAD)
    log.info("=" * 60)
    
    crear_configuracion()
    inicializar_ledger()
    
    log.info("Catedral lista. Esperando conexion de hardware ASIC...")
    
    # Modo守护: si hay cgminer, lo lanza; si no, espera
    while True:
        proceso = levantar_minero()
        
        if proceso is None:
            log.info("Sin minero hardware. Reintentando en 60s...")
            time.sleep(60)
            continue
        
        sesion = {
            "inicio": datetime.now(timezone.utc).isoformat(),
            "pid": proceso.pid,
            "pool": POOL_URL,
            "worker": WORKER,
        }
        
        while proceso.poll() is None:
            time.sleep(10)
        
        sesion["fin"] = datetime.now(timezone.utc).isoformat()
        sesion["codigo_salida"] = proceso.returncode
        registrar_sesion(sesion)
        
        log.warning("Desconexion del pool. Reconectando en 5s...")
        time.sleep(5)


if __name__ == "__main__":
    main()
