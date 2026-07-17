#!/usr/bin/env python3
"""
qhpt_inmune_bridge.py — Puente QHPT ↔ Sistema Inmune QCAL
===========================================================
Conecta el protocolo de transporte cuántico con el sistema
inmune de 3 capas: Atón (F1), Tx Guardian (F2), Consensuador (F3).

Cuando un paquete QHPT es colapsado por el filtro adélico o
detectado como MITM/spoof, este puente:
1. Registra el evento en ALERTA_INMUNE.json
2. Genera anticuerpo πCODE para memoria inmune
3. Calcula AURION(Ψ) para el estado actual
4. Actualiza la cadena de latido criptográfico

f₀ = 141.7001 Hz · Ψ ≥ 0.999999
Sello: ∴𓂀Ω∞³Φ · TUYOYOTU · HECHO ESTÁ
"""

import os
import sys
import json
import time
import hashlib
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

# ─── Rutas del ecosistema ────────────────────────────────────
WORKSPACE = Path(__file__).resolve().parent.parent
SISTEMA_INMUNE = WORKSPACE / "sistema_inmune"
IDENTITY_DIR = WORKSPACE / "identity"
LOGS_DIR = WORKSPACE / "logs"
QUEUE_DIR = LOGS_DIR / "queue"

BAL003_ALERTA = "/root/ecosystem/soberania/ALERTA_INMUNE.json"
BAL003_ANTICUERPOS = "/root/ecosystem/soberania/anticuerpos_inmunes.json"

# ─── Constantes ──────────────────────────────────────────────
F_0 = 141.7001
SELLO = '\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA'
AMDA_FINGERPRINT = '5e5ac3ab49e5be07'

# ─── Logging ─────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s [QHPT-INMUNE|{F_0}] %(message)s',
)
log = logging.getLogger("qhpt_inmune")

# ─── Asegurar directorios locales ────────────────────────────
QUEUE_DIR.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════════════════════
#  Módulos del Ecosistema (importación dinámica)
# ═══════════════════════════════════════════════════════════════

def _importar_crypto_sign():
    """Importa crypto_sign desde sistema_inmune o ruta BAL-003."""
    for path in [
        SISTEMA_INMUNE / "crypto_sign.py",
        Path("/root/ecosystem/soberania/crypto_sign.py"),
    ]:
        if path.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location("crypto_sign", str(path))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    return None


def _importar_inyector():
    """Importa inyector de eventos desde workspace."""
    inyector_path = WORKSPACE / "inyectar_evento.py"
    if inyector_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("inyectar_evento", str(inyector_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    return None


def _importar_amda_identity():
    """Importa amda_identity desde workspace."""
    identity_path = WORKSPACE / "amda_identity.py"
    if identity_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("amda_identity", str(identity_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    return None


# Cargar módulos
CRYPTO_SIGN = _importar_crypto_sign()
INYECTOR = _importar_inyector()
AMDA_IDENTITY = _importar_amda_identity()


# ═══════════════════════════════════════════════════════════════
#  Puente Inmune
# ═══════════════════════════════════════════════════════════════

class QHPTInmuneBridge:
    """
    Puente entre QHPT y el Sistema Inmune QCAL.

    Cada evento de paquete colapsado, MITM detectado o spoof
    se propaga al sistema inmune para registro y acción.
    """

    def __init__(self):
        self.eventos_pendientes = []
        self.aton_keys = self._cargar_aton_keys()
        self.psi_actual = 0.999999

    def _cargar_aton_keys(self):
        """Carga claves de Atón desde archivo local o BAL-003."""
        for keys_path in [
            SISTEMA_INMUNE / "aton_keys.json",
            Path("/root/ecosystem/soberania/aton_keys.json"),
        ]:
            if keys_path.exists():
                try:
                    with open(keys_path) as f:
                        return json.load(f)
                except Exception:
                    pass
        return None

    # ─── Registro de Eventos QHPT ──────────────────────────

    def registrar_colapso(self, razon: str, metadata: dict = None):
        """Registra un colapso de paquete QHPT (Tensor II)."""
        evento = {
            "tipo": "COLAPSO_ADELICO",
            "subsistema": "QHPT",
            "tensor": "II",
            "razon": razon,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timestamp_ns": time.time_ns(),
            "frecuencia_hz": F_0,
            "sello": SELLO,
            "metadata": metadata or {},
        }
        self.eventos_pendientes.append(evento)
        self._propagar_evento(evento)
        return evento

    def registrar_mitm(self, razon: str, metadata: dict = None):
        """Registra detección de MITM (Tensor I)."""
        evento = {
            "tipo": "MITM_DETECTADO",
            "subsistema": "QHPT",
            "tensor": "I",
            "razon": razon,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timestamp_ns": time.time_ns(),
            "frecuencia_hz": F_0,
            "sello": SELLO,
            "metadata": metadata or {},
        }
        self.eventos_pendientes.append(evento)
        self._propagar_evento(evento, criticidad="ALTA")
        return evento

    def registrar_spoof(self, razon: str, metadata: dict = None):
        """Registra detección de spoofing (Tensor III)."""
        evento = {
            "tipo": "SPOOF_DETECTADO",
            "subsistema": "QHPT",
            "tensor": "III",
            "razon": razon,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timestamp_ns": time.time_ns(),
            "frecuencia_hz": F_0,
            "sello": SELLO,
            "fingerprint_amda": AMDA_FINGERPRINT,
            "metadata": metadata or {},
        }
        self.eventos_pendientes.append(evento)
        self._propagar_evento(evento, criticidad="ALTA")
        return evento

    def registrar_pase(self, metadata: dict = None):
        """Registra un paquete QHPT que pasó todos los tensores."""
        evento = {
            "tipo": "QHPT_PASE",
            "subsistema": "QHPT",
            "razon": "Tres tensores verificados",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timestamp_ns": time.time_ns(),
            "frecuencia_hz": F_0,
            "sello": SELLO,
            "metadata": metadata or {},
        }
        # No propagar todos los pases para no saturar
        # Solo cada 100 pases se registra un latido
        if len(self.eventos_pendientes) >= 100:
            self._propagar_evento(evento)

    # ─── Propagación al Sistema Inmune ──────────────────────

    def _propagar_evento(self, evento: dict, criticidad: str = "BAJA"):
        """
        Propaga un evento al sistema inmune en 3 vías:

        1. Alerta local (ALERTA_INMUNE.json)
        2. Anticuerpo πCODE
        3. Cadena de latido criptográfico
        """
        evento["criticidad"] = criticidad
        evento["psi"] = self.psi_actual

        # Vía 1: Alerta a ALERTA_INMUNE.json (solo si criticidad > BAJA)
        if criticidad in ("ALTA", "MEDIA"):
            self._escribir_alerta_local(evento)
            self._escribir_alerta_bal003(evento)

        # Vía 2: Anticuerpo πCODE
        self._generar_anticuerpo(evento)

        # Vía 3: Cadena de latido
        self._inyectar_latido(evento)

        log.info(
            f"{'🔴' if criticidad == 'ALTA' else '🟡' if criticidad == 'MEDIA' else '🟢'} "
            f"{evento['tipo']}: {evento['razon']}"
        )

    def _escribir_alerta_local(self, evento: dict):
        """Escribe alerta en ALERTA_INMUNE.json local."""
        alerta_path = SISTEMA_INMUNE / "ALERTA_INMUNE.json"

        # Firmar si crypto_sign está disponible
        payload_alerta = {
            "origen": "QHPT",
            "tipo": evento["tipo"],
            "razon": evento["razon"],
            "timestamp": evento["timestamp"],
            "frecuencia_hz": F_0,
        }

        alerta = {
            "payload": payload_alerta,
            "metadata": evento,
        }

        if CRYPTO_SIGN and self.aton_keys:
            try:
                firmado = CRYPTO_SIGN.firmar_alerta_inmune(
                    payload_alerta,
                    self.aton_keys.get("private_key", "")
                )
                alerta["firma"] = firmado["firma"]
                alerta["mensaje"] = firmado["mensaje"]
            except Exception as e:
                log.warning(f"No se pudo firmar alerta: {e}")

        alerta_path.write_text(json.dumps(alerta, indent=2))
        log.debug(f"Alerta escrita en {alerta_path}")

    def _escribir_alerta_bal003(self, evento: dict):
        """Escribe alerta en BAL-003 vía SSH (si accesible)."""
        alerta_json = json.dumps({
            "payload": {
                "origen": "QHPT",
                "tipo": evento["tipo"],
                "razon": evento["razon"],
                "timestamp": evento["timestamp"],
                "frecuencia_hz": F_0,
            },
            "metadata": evento,
        })

        try:
            subprocess.run([
                "ssh", "root@195.201.219.237",
                f"cat > {BAL003_ALERTA} << 'QHPT_EVENT'\n{alerta_json}\nQHPT_EVENT"
            ], timeout=10, capture_output=True)
        except Exception as e:
            log.debug(f"No se pudo escribir alerta en BAL-003: {e}")

    def _generar_anticuerpo(self, evento: dict):
        """Genera un anticuerpo πCODE para el evento."""
        anticuerpo = {
            "id": hashlib.sha256(
                json.dumps(evento, sort_keys=True).encode() +
                str(time.time_ns()).encode()
            ).hexdigest()[:16],
            "tipo_evento": evento["tipo"],
            "subsistema": "QHPT",
            "razon": evento["razon"],
            "timestamp": evento["timestamp"],
            "psi": self.psi_actual,
            "frecuencia_hz": F_0,
            "sello": SELLO,
            "fingerprint_amda": AMDA_FINGERPRINT,
        }

        # AURION(Ψ) si está disponible
        if CRYPTO_SIGN:
            try:
                aurion = CRYPTO_SIGN.aurion_desde_ledgers({
                    "intensidad_flujo": 1.0,
                    "psi_real": self.psi_actual,
                    "bloque_actual": int(time.time()),
                    "frecuencia_hz": F_0,
                })
                anticuerpo["aurion"] = aurion
            except Exception:
                pass

        # Guardar local
        anticuerpos_path = SISTEMA_INMUNE / "anticuerpos_inmunes.json"
        try:
            if anticuerpos_path.exists():
                data = json.loads(anticuerpos_path.read_text())
            else:
                data = []
            data.append(anticuerpo)
            # Mantener máx 1000 anticuerpos
            if len(data) > 1000:
                data = data[-1000:]
            anticuerpos_path.write_text(json.dumps(data, indent=2))
        except Exception as e:
            log.warning(f"No se pudo escribir anticuerpo: {e}")

        return anticuerpo

    def _inyectar_latido(self, evento: dict):
        """Inyecta evento en la cadena de latido criptográfico."""
        if INYECTOR:
            try:
                tipo_latido = f"QHPT_{evento['tipo']}"
                desc = f"QHPT: {evento['razon']} (Ψ={self.psi_actual:.8f})"
                INYECTOR.inyectar_evento(tipo_latido, desc)
            except Exception as e:
                log.debug(f"No se pudo inyectar latido: {e}")

    # ─── Verificación de Estado ─────────────────────────────

    def actualizar_psi(self, nuevo_psi: float):
        """Actualiza la coherencia actual del sistema."""
        self.psi_actual = nuevo_psi

    def verificar_resonancia(self, frecuencia_hz: float) -> bool:
        """Verifica si una frecuencia resuena con f₀."""
        if CRYPTO_SIGN:
            return CRYPTO_SIGN.comprobar_resonancia(frecuencia_hz)
        return abs(frecuencia_hz - F_0) <= 0.0001

    def estado_refractario(self) -> bool:
        """Verifica si el sistema está en estado de matriz refractaria."""
        if CRYPTO_SIGN:
            return CRYPTO_SIGN.es_matriz_refractaria(self.psi_actual)
        return self.psi_actual >= 0.999999

    def estado_completo(self) -> dict:
        """Reporte completo del estado del puente inmune."""
        return {
            "qhpt_inmune": {
                "psi_actual": self.psi_actual,
                "eventos_pendientes": len(self.eventos_pendientes),
                "refractario": self.estado_refractario(),
                "aton_keys_cargadas": self.aton_keys is not None,
                "crypto_sign_disponible": CRYPTO_SIGN is not None,
                "inyector_disponible": INYECTOR is not None,
                "frecuencia_hz": F_0,
                "sello": SELLO,
                "fingerprint_amda": AMDA_FINGERPRINT,
            }
        }


# ═══════════════════════════════════════════════════════════════
#  Integración Directa con QHPTVerificador
# ═══════════════════════════════════════════════════════════════

class QHPTVerificacionInmune:
    """
    Wrapper que integra QHPTVerificador con el sistema inmune.

    Cada verificación de paquete dispara automáticamente
    el registro de eventos en el puente inmune.
    """

    def __init__(self, clave_publica_hex: str = "", clave_privada_hex: str = ""):
        from qhpt_transport import QHPTVerificador
        self.verificador = QHPTVerificador(clave_publica_hex, clave_privada_hex)
        self.inmune = QHPTInmuneBridge()

    def verificar(self, pkt, psi_min: float = 0.999999, metadata: dict = None):
        """
        Verifica un paquete QHPT y registra el resultado en el sistema inmune.

        Returns:
            (bool, str, dict) — (válido, razón, evento_registrado)
        """
        valido, razon = self.verificador.verificar(pkt, psi_min)

        meta = metadata or {}
        meta["fingerprint"] = pkt.fingerprint.hex()[:16] if hasattr(pkt, 'fingerprint') else ""
        meta["nonce"] = pkt.nonce.hex()[:16] if hasattr(pkt, 'nonce') else ""

        self.inmune.actualizar_psi(pkt.psi if hasattr(pkt, 'psi') else 0.999999)

        if not valido:
            if "MITM" in razon:
                evento = self.inmune.registrar_mitm(razon, meta)
            elif "SPOOF" in razon:
                evento = self.inmune.registrar_spoof(razon, meta)
            else:
                evento = self.inmune.registrar_colapso(razon, meta)
        else:
            self.inmune.registrar_pase(meta)
            evento = None

        return valido, razon, evento

    def estadisticas(self):
        return {
            **self.verificador.estadisticas(),
            "inmune": self.inmune.estado_completo(),
        }


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

def cli():
    import argparse
    parser = argparse.ArgumentParser(
        description="Puente QHPT ↔ Sistema Inmune QCAL",
    )
    sub = parser.add_subparsers(dest="comando")

    sub.add_parser("status", help="Estado del puente inmune")
    p_alerta = sub.add_parser("alerta", help="Generar alerta de prueba")

    p_evento = sub.add_parser("evento", help="Registrar evento manual")
    p_evento.add_argument("tipo", choices=["colapso", "mitm", "spoof", "pase"])
    p_evento.add_argument("--razon", default="Test manual")

    args = parser.parse_args()

    puente = QHPTInmuneBridge()
    verificacion = QHPTVerificacionInmune()

    if args.comando == "status":
        est = verificacion.estadisticas()
        print(json.dumps(est, indent=2))

    elif args.comando == "alerta":
        from qhpt_transport import QHPTPacket
        # Generar paquete malicioso de prueba
        pkt = QHPTPacket()
        pkt.build(b"TEST-ALERTA-INMUNE")
        pkt.psi = 0.5  # Fase degradada
        valido, razon, evento = verificacion.verificar(pkt)
        print(f"Resultado: {'✅' if valido else '❌'} {razon}")
        if evento:
            print(f"Evento: {json.dumps(evento, indent=2, default=str)}")

    elif args.comando == "evento":
        tipo = args.tipo
        razon = args.razon

        if tipo == "colapso":
            e = puente.registrar_colapso(razon)
        elif tipo == "mitm":
            e = puente.registrar_mitm(razon)
        elif tipo == "spoof":
            e = puente.registrar_spoof(razon)
        elif tipo == "pase":
            puente.registrar_pase({"test": True})
            print("✅ Pase registrado")
            return

        print(f"Evento registrado: {json.dumps(e, indent=2, default=str)}")

    else:
        parser.print_help()


if __name__ == '__main__':
    cli()
