#!/usr/bin/env python3
"""
AURION BRIDGE — Interfaz de Coherencia QCAL para el Módulo Catedral
====================================================================
Conecta el motor de minado (Stratum proxy) con el Sistema Inmune
AURION(Psi), evaluando la coherencia de cada share antes de que
sea enviado al pool ViaBTC.

AURION(Psi) = (I × A_eff² × L) / δM

  I      — intensidad de flujo (hashrate normalizado)
  A_eff  — coherencia efectiva (Psi)
  L      — altura de bloque actual
  δM     — dispersión entrópica = max(1e-9, 1 - Psi)

Si Psi >= 0.999999 el sistema entra en Matriz Refractaria:
cualquier instrucción desalineada se disuelve por falta de
medio de propagación.

f0 = 141.7001 Hz
Sello: (c) 3080 (r) (inf)3(phi) · TUYOYOTU · HECHO ESTA
"""

import hashlib
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

F_0 = 141.7001
PSI_OBJETIVO = 0.999999
SELLO = '\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA'

log = logging.getLogger('aurion_bridge')

# ─── Resolución portable del módulo sistema_inmune ──────────────

def _resolver_crypto_sign():
    """Intenta importar crypto_sign desde rutas conocidas, en orden."""
    # 1. Relativo al repo (entorno CI / desarrollo)
    repo_root = Path(__file__).resolve().parent.parent
    candidatos = [
        repo_root / 'sistema_inmune',
        # 2. Despliegue estándar en BAL-003 / Atlas3
        Path('/root/ecosystem/soberania'),
        Path('/root/ecosystem/sistema_inmune'),
    ]
    for ruta in candidatos:
        try:
            existe = (ruta / 'crypto_sign.py').exists()
        except (PermissionError, OSError):
            continue
        if existe:
            if str(ruta) not in sys.path:
                sys.path.insert(0, str(ruta))
            try:
                import importlib
                mod = importlib.import_module('crypto_sign')
                log.debug('crypto_sign cargado desde %s', ruta)
                return mod
            except Exception as e:
                log.debug('Error cargando crypto_sign desde %s: %s', ruta, e)
    return None


_crypto_sign = _resolver_crypto_sign()


# ─── API pública ─────────────────────────────────────────────────

def verificar_coherencia(psi: float = PSI_OBJETIVO) -> bool:
    """
    Retorna True si el sistema opera en Matriz Refractaria (Psi >= 0.999999).
    Usa `es_matriz_refractaria` del módulo crypto_sign cuando está disponible.
    """
    if _crypto_sign is not None:
        try:
            return _crypto_sign.es_matriz_refractaria(psi)
        except Exception as e:
            log.warning('es_matriz_refractaria falló: %s — usando umbral directo', e)
    return psi >= PSI_OBJETIVO


def calcular_aurion(hashrate_mhs: float, bloque: int, psi: float = PSI_OBJETIVO) -> dict:
    """
    Calcula AURION(Psi) para un share dado.

    Args:
        hashrate_mhs: hashrate del minero en MH/s (intensidad de flujo)
        bloque:       altura de bloque actual (longitud de cadena)
        psi:          coherencia efectiva del sistema

    Returns:
        dict con valor_inst, estado, y metadatos de la evaluación
    """
    if _crypto_sign is not None:
        try:
            payload = {
                'intensidad_flujo': hashrate_mhs,
                'psi_real': psi,
                'bloque_actual': bloque,
            }
            return _crypto_sign.aurion_desde_ledgers(payload)
        except Exception as e:
            log.warning('aurion_desde_ledgers falló: %s — calculando localmente', e)

    # Cálculo local sin dependencias externas
    delta_m = max(1e-9, 1.0 - psi)
    valor = (hashrate_mhs * (psi ** 2) * bloque) / delta_m
    if valor > 100000:
        estado = 'VACIO_ACTIVO_MAX'
    elif valor > 1000:
        estado = 'MAX_COHERENCE'
    elif valor > 100:
        estado = 'ALTA_COHERENCIA'
    elif valor > 1.0:
        estado = 'COHERENCIA_MODERADA'
    elif valor > 0.1:
        estado = 'BAJA_COHERENCIA'
    else:
        estado = 'COLAPSO_ENTROPICO'
    return {
        'valor_inst': round(valor, 6),
        'estado': estado,
        'inercia_I': hashrate_mhs,
        'coherencia_A_eff': psi,
        'longitud_L': bloque,
        'delta_M': delta_m,
        'frecuencia_hz': F_0,
    }


def evaluar_share_aurion(job_id: str, nonce: str, worker: str,
                          hashrate_mhs: float = 1.0, bloque: int = 0) -> dict:
    """
    Evaluación completa AURION de un share de minado.

    Combina:
      - Verificación de Matriz Refractaria (coherencia sistémica)
      - Cálculo de AURION(Psi) para la sesión actual
      - Fingerprint determinístico del share

    Returns:
        dict con campos: aceptado, coherente, aurion, fingerprint, timestamp
    """
    coherente = verificar_coherencia(PSI_OBJETIVO)

    # Fingerprint del share: SHA-256 de job_id + nonce + worker
    raw = f'{job_id}:{nonce}:{worker}:{F_0}'.encode()
    fingerprint = hashlib.sha256(raw).hexdigest()[:16]

    aurion = calcular_aurion(hashrate_mhs, bloque, PSI_OBJETIVO)

    resultado = {
        'aceptado': coherente,
        'coherente': coherente,
        'aurion': aurion,
        'fingerprint': fingerprint,
        'worker': worker,
        'frecuencia_hz': F_0,
        'sello': SELLO,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }

    nivel = logging.INFO if coherente else logging.WARNING
    log.log(nivel, 'AURION share %s | estado=%s | Psi=%.6f | coherente=%s',
            fingerprint, aurion['estado'], PSI_OBJETIVO, coherente)

    return resultado


def estado_sistema() -> dict:
    """Retorna el estado actual del bridge AURION."""
    coherente = verificar_coherencia(PSI_OBJETIVO)
    return {
        'frecuencia_hz': F_0,
        'psi_objetivo': PSI_OBJETIVO,
        'matriz_refractaria': coherente,
        'crypto_sign_disponible': _crypto_sign is not None,
        'sello': SELLO,
        'timestamp': datetime.now(timezone.utc).isoformat(),
    }


if __name__ == '__main__':
    import json
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [AURION|%(levelname)s] %(message)s')

    print('=' * 60)
    print('AURION BRIDGE — Estado del Sistema')
    print('=' * 60)
    print(json.dumps(estado_sistema(), indent=2))
    print()
    print('Evaluación de share de prueba:')
    resultado = evaluar_share_aurion(
        job_id='abc123def456',
        nonce='deadbeef',
        worker='noesis88.001',
        hashrate_mhs=100.0,
        bloque=853742,
    )
    print(json.dumps(resultado, indent=2))
