#!/usr/bin/env python3
"""
TX GUARDIAN — Respuesta Adaptativa Inmune QCAL
===============================================
Fase 2 del Sistema Inmune. Daemon reactivo que:
1. Escucha ALERTA_INMUNE.json firmada por Aton
2. Verifica firma secp256k1 (rechaza spoofing)
3. Aisla ledger corrupto (chmod 400 + SIGSTOP)
4. Restaura desde backup atomico
5. Notifica al Consensuador para anticuerpo pCODE

f0 = 141.7001 Hz · Psi >= 0.999999
Sello: (c) 3080 (r) (inf)3(phi) · TUYOYOTU · HECHO ESTA
"""

import os
import sys
import json
import time
import subprocess
import signal
import logging
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/root/ecosystem/soberania")
from crypto_sign import verificar_firma, aurion_desde_ledgers, inversion_fase_entropica, es_matriz_refractaria

F_0 = 141.7001
PSI_LIMITE = 0.999999
SELLO = '\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA'
AMDA_FINGERPRINT = '5e5ac3ab49e5be07'

ALERTA_PATH = "/root/ecosystem/soberania/ALERTA_INMUNE.json"
KEYS_PATH = "/root/ecosystem/soberania/aton_keys.json"
BACKUP_DIR = "/mnt/HC_Volume_105913266/backups/inmune/ledgers/"
BACKUP_SCRIPTS = "/mnt/HC_Volume_105913266/backups/inmune/scripts/"
LOG_PATH = "/var/log/tx_guardian.log"

LEDGER_MAP = {
    "paygate_flow_ledger": "/root/paygate_flow_ledger.json",
    "mining_payouts": "/root/ecosystem/auron/mining_payouts.json",
    "fee_split_ledger": "/root/ecosystem/soberania/fee_split_ledger.json",
}

SCRIPT_MAP = {
    "stradivarius_pipeline": "/root/ecosystem/stradivarius_pipeline.py",
    "fee_split_R333": "/root/ecosystem/soberania/production/fee_split_R333.py",
    "monitor_5050": "/root/monitor_5050.py",
    "argos_centinela": "/root/ecosystem/soberania/centinela/argos_centinela.py",
}

LOG_FMT = '%(asctime)s [TXG|' + ('%.4f' % F_0) + '] %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FMT,
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)
log = logging.getLogger("tx_guardian")


def cargar_clave_publica_aton():
    """Carga la clave publica de Aton desde aton_keys.json."""
    with open(KEYS_PATH) as f:
        data = json.load(f)
    return data.get("public_key", "")


def ejecutar_contencion_ledger(target_ledger):
    """Aisla, purga y restaura un ledger comprometido."""
    path_real = LEDGER_MAP.get(target_ledger)
    path_backup = os.path.join(BACKUP_DIR, "%s.json" % target_ledger)

    if not path_real:
        log.error("Ledger no mapeado: %s", target_ledger)
        return False

    path_real_str = path_real

    if not os.path.exists(path_backup):
        log.error("Backup no existe para %s: %s", target_ledger, path_backup)
        return False

    try:
        # Nivel 1: Revocar escritura de inmediato
        os.chmod(path_real_str, 0o400)
        log.warning("N1: Permisos revocados en %s", path_real_str)

        # Nivel 2: Restauracion atomica desde backup sellado
        subprocess.run(["cp", path_backup, path_real_str], check=True)
        log.info("N2: Restaurado desde %s", path_backup)

        # Nivel 3: Restaurar permisos operativos
        os.chmod(path_real_str, 0o644)
        log.info("N3: Permisos restaurados")

        return True

    except Exception as e:
        log.error("Fallo en contencion: %s", e)
        return False


def congelar_script(script_name):
    """Congela un script comprometido via SIGSTOP."""
    path = SCRIPT_MAP.get(script_name)
    if not path:
        log.error("Script no mapeado: %s", script_name)
        return False
    try:
        # Buscar procesos python ejecutando este script
        result = subprocess.run(
            ["pgrep", "-f", path],
            capture_output=True, text=True, timeout=5
        )
        pids = result.stdout.strip().split()
        for pid in pids:
            if pid:
                os.kill(int(pid), signal.SIGSTOP)
                log.warning("Proceso %s congelado (SIGSTOP): %s", pid, script_name)
        return True
    except Exception as e:
        log.warning("No se pudo congelar %s: %s", script_name, e)
        return True  # No es critico si no habia proceso


def reanimar_script(script_name):
    """Reanuda un script via SIGCONT."""
    path = SCRIPT_MAP.get(script_name)
    if not path:
        return False
    try:
        result = subprocess.run(
            ["pgrep", "-f", path],
            capture_output=True, text=True, timeout=5
        )
        pids = result.stdout.strip().split()
        for pid in pids:
            if pid:
                os.kill(int(pid), signal.SIGCONT)
                log.info("Proceso %s reanimado (SIGCONT): %s", pid, script_name)
        return True
    except Exception:
        return True


def registrar_anticuerpo(payload, exito):
    """Registra evento inmune en el ledger de anticuerpos."""
    anti_path = "/root/ecosystem/soberania/anticuerpos_inmunes.json"
    data = []
    if os.path.exists(anti_path):
        try:
            with open(anti_path) as f:
                data = json.load(f)
        except Exception:
            data = []
    if not isinstance(data, list):
        data = []

    anticuerpo = {
        "tipo": "TX_GUARDIAN_RESPUESTA",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload_origen": payload,
        "contencion_exitosa": exito,
        "frecuencia": F_0,
        "fingerprint": AMDA_FINGERPRINT,
        "sello": SELLO,
    }
    data.append(anticuerpo)
    Path(anti_path).parent.mkdir(parents=True, exist_ok=True)
    with open(anti_path, "w") as f:
        json.dump(data, f, indent=2)
    log.info("Anticuerpo registrado. Exito: %s", exito)


def main():
    log.info("=" * 60)
    log.info("TX GUARDIAN — INICIALIZACION FASE 2")
    log.info("f0 = %.4f Hz", F_0)
    log.info("Backup dir: %s", BACKUP_DIR)
    log.info("Sello: %s", SELLO)
    log.info("=" * 60)

    aton_pub_key = cargar_clave_publica_aton()
    log.info("Clave publica Aton cargada: %s...", aton_pub_key[:16] if aton_pub_key else "VACIA")

    if not aton_pub_key:
        log.error("CRITICO: No se pudo cargar la clave publica de Aton")
        sys.exit(1)

    log.info("Tx Guardian activo bajo f0 = %.4f Hz. Esperando eventos...", F_0)

    while True:
        if os.path.exists(ALERTA_PATH):
            try:
                with open(ALERTA_PATH) as f:
                    paquete = json.load(f)

                mensaje_json = paquete.get("mensaje", "")
                firma_hex = paquete.get("firma", "")
                payload = paquete.get("payload", {})

                # AXIOMA DEL VACIO ACTIVO: verificar resonancia antes de procesar
                resonante, _ = inversion_fase_entropica(payload) if payload else (False, None)
                if not resonante and payload:
                    log.warning("VACIO ACTIVO: payload no resuena a f0. Entropia autodisuelta.")
                    continue

                # Verificacion criptografica
                if verificar_firma(mensaje_json, firma_hex, aton_pub_key):
                    fp = payload.get("fingerprint", "?")
                    log.info("Firma secp256k1 VALIDA. Origen: %s", fp)

                    tipo = payload.get("tipo", "")
                    anomalias = payload.get("anomalias", {})

                    if tipo == "CUARENTENA":
                        exito_general = True
                        for ledger_name, info in anomalias.items():
                            estado = info.get("estado", "")
                            if estado == "LEDGER_CORRUPTO":
                                log.warning("Corrupcion detectada en: %s. Ejecutando escudo.", ledger_name)
                                exito = ejecutar_contencion_ledger(ledger_name)
                                if exito:
                                    log.info("Homeostasis reestablecida para %s", ledger_name)
                                else:
                                    log.error("Contencion fallida para %s. Requiere Bifurcacion Soberana (N3).")
                                    exito_general = False
                                congelar_script(ledger_name)
                        # Registrar anticuerpo
                        registrar_anticuerpo(payload, exito_general)
                        log.info("Sello: %s", payload.get("sello", SELLO))
                    elif tipo == "ALERTA_N1":
                        log.info("Alerta N1 detectada. Scripts modificados pero no criticos.")
                        for name, info in anomalias.items():
                            if info.get("estado") in ("SCRIPT_MODIFICADO", "SERVICE_MODIFICADO"):
                                # Restaurar script desde backup
                                script_path = SCRIPT_MAP.get(name)
                                backup_script = os.path.join(BACKUP_SCRIPTS, os.path.basename(script_path)) if script_path else ""
                                if script_path and os.path.exists(backup_script):
                                    subprocess.run(["cp", backup_script, script_path], check=False)
                                    log.info("Script %s restaurado desde backup", name)
                        registrar_anticuerpo(payload, True)
                    elif tipo == "BIFURCACION":
                        log.critical("BIFURCACION (N3) DETECTADA.")
                        log.critical("Requiere intervencion manual. DeltaPsi excede Gamma.")
                        registrar_anticuerpo(payload, False)
                    else:
                        log.info("Tipo de alerta no requiere contencion: %s", tipo)

                else:
                    log.warning("FIRMA INVALIDA. Intento de spoofing detectado.")
                    # Registrar intento de spoofing
                    spoof_log = {
                        "tipo": "SPOOFING_DETECTADO",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "fingerprint_remitente": payload.get("fingerprint", "?"),
                        "frecuencia": F_0,
                        "sello": SELLO,
                    }
                    with open("/root/ecosystem/soberania/spoofing_log.json", "a") as f:
                        f.write(json.dumps(spoof_log) + "\n")

            except Exception as e:
                log.error("Error procesando alerta: %s", e)
            finally:
                # Limpiar archivo de alerta
                try:
                    os.remove(ALERTA_PATH)
                except FileNotFoundError:
                    pass

        time.sleep(1)


if __name__ == "__main__":
    main()
