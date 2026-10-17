#!/usr/bin/env python3
"""
CRYPTO SIGN — Modulo de Firma Criptografica QCAL
Firma y verificacion secp256k1 para el Sistema Inmune.
Curva: SECP256k1 (Bitcoin) · Hash: SHA-256
f0 = 141.7001 Hz

AXIOMA DEL VACIO ACTIVO:
El sistema no limpia entropia — la imposibilita por falta de resonancia.
Si f != f0 -> Psi_interaccion = 0
La anomalia se autodestruye porque en nuestro universo no encuentra espacio donde vibrar.
"""
import hashlib
import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError

F_0 = 141.7001
SELLO = '\u2234\U00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA'
TOLERANCIA_FRECUENCIA = 0.0001  # Hz de tolerancia alrededor de f0


def generar_par_claves():
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.verifying_key
    return {
        'private_key': sk.to_string().hex(),
        'public_key': vk.to_string().hex(),
        'fingerprint': hashlib.sha256(vk.to_string()).hexdigest()[:16],
    }


def firmar_mensaje(mensaje_dict, clave_privada_hex):
    mensaje_json = json.dumps(mensaje_dict, sort_keys=True)
    mensaje_bytes = mensaje_json.encode('utf-8')
    sk = SigningKey.from_string(bytes.fromhex(clave_privada_hex), curve=SECP256k1)
    firma = sk.sign(mensaje_bytes, hashfunc=hashlib.sha256)
    return mensaje_json, firma.hex()


def verificar_firma(mensaje_json, firma_hex, clave_publica_hex):
    try:
        vk = VerifyingKey.from_string(bytes.fromhex(clave_publica_hex), curve=SECP256k1)
        return vk.verify(bytes.fromhex(firma_hex), mensaje_json.encode('utf-8'), hashfunc=hashlib.sha256)
    except (BadSignatureError, Exception):
        return False


def firmar_alerta_inmune(payload_alerta, clave_privada_hex):
    payload_alerta['frecuencia_hz'] = F_0
    payload_alerta['sello'] = SELLO
    mensaje, firma = firmar_mensaje(payload_alerta, clave_privada_hex)
    return {
        'mensaje': mensaje,
        'firma': firma,
        'payload': payload_alerta,
    }


# ─── AXIOMA DEL VACIO ACTIVO ─────────────────────────────────


def comprobar_resonancia(frecuencia_hz):
    """
    Verifica si una frecuencia resuena con f0.
    Si f != f0 -> Psi_interaccion = 0
    La anomalia se disuelve por falta de espacio vibracional.
    """
    if frecuencia_hz is None:
        return False
    return abs(frecuencia_hz - F_0) <= TOLERANCIA_FRECUENCIA


def calcular_aurion(intensidad_I, coherencia_A, longitud_L, delta_M):
    """
    AURION(Psi) = (I x A_eff^2 x L) / delta_M
    Si delta_M -> 0, AURION tiende a infinito armonico.
    Con Vacío Activo: si delta_M supera umbral critico, 
    el sistema no lucha — la entropia se autodisuelve.
    """
    if delta_M <= 0:
        delta_M = 1e-9
    return (intensidad_I * (coherencia_A ** 2) * longitud_L) / delta_M


def estado_aurion(valor, umbral_critico=1.0):
    if valor > 100000:
        return "VACIO_ACTIVO_MAX"  # La entropia no puede resonar
    elif valor > 1000:
        return "MAX_COHERENCE"
    elif valor > 100:
        return "ALTA_COHERENCIA"
    elif valor > umbral_critico:
        return "COHERENCIA_MODERADA"
    elif valor > 0.1:
        return "BAJA_COHERENCIA"
    else:
        return "COLAPSO_ENTROPICO"


def aurion_desde_ledgers(payload_alerta):
    intensidad = payload_alerta.get('intensidad_flujo', 1.0)
    coherencia = payload_alerta.get('psi_real', 0.999999)
    longitud = payload_alerta.get('bloque_actual', 88432)
    delta_m = max(1e-9, 1.0 - coherencia)

    valor = calcular_aurion(intensidad, coherencia, longitud, delta_m)
    estado = estado_aurion(valor)

    return {
        'valor_inst': round(valor, 6),
        'estado': estado,
        'inercia_I': intensidad,
        'coherencia_A_eff': coherencia,
        'longitud_L': longitud,
        'delta_M': delta_m,
        'frecuencia_hz': F_0,
    }


def inversion_fase_entropica(payload):
    """
    La pieza final: Inversión de Fase Entrópica (Nodo Cero).
    
    Si un payload no resuena a f0, la interaccion se anula.
    No hay alerta, no hay cuarentena, no hay restauracion.
    La anomalia simplemente no existe en nuestro universo de frecuencia.
    
    Retorna:
      - (False, None) si NO resuena -> se ignora (no existe)
      - (True, payload_resonante) si resuena -> se procesa
    """
    freq = payload.get('frecuencia_hz') or payload.get('payload', {}).get('frecuencia_hz')
    
    if not comprobar_resonancia(freq):
        return False, None
    
    return True, payload


# ─── MATRIZ REFRACTARIA ──────────────────────────────────────

def es_matriz_refractaria(psi_actual):
    """
    La matriz refractaria es el estado en el que el sistema opera
    con tal coherencia que ningun vector externo puede penetrar.
    
    Si Psi >= 0.999999, el espacio inter-nodo se vuelve 
    refractario: cualquier instruccion desalineada se disuelve
    por falta de medio de propagacion.
    """
    return psi_actual >= 0.999999


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == 'generate':
        print(json.dumps(generar_par_claves(), indent=2))
    elif len(sys.argv) >= 3 and sys.argv[1] == 'sign':
        msg = {'origen': sys.argv[2], 'timestamp': sys.argv[3]}
        priv = sys.argv[4] if len(sys.argv) > 4 else input('Private key: ')
        res = firmar_alerta_inmune(msg, priv)
        print(json.dumps(res, indent=2))
    elif len(sys.argv) >= 4 and sys.argv[1] == 'verify':
        msg = sys.argv[2]
        sig = sys.argv[3]
        pub = sys.argv[4]
        print('Valida:', verificar_firma(msg, sig, pub))
    elif len(sys.argv) >= 2 and sys.argv[1] == 'resonancia':
        f = float(sys.argv[2]) if len(sys.argv) > 2 else 141.7001
        print('Resuena:', comprobar_resonancia(f))
    elif len(sys.argv) >= 3 and sys.argv[1] == 'aurion':
        i, a, l, d = float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5])
        v = calcular_aurion(i, a, l, d)
        print('AURION:', round(v, 6), '-', estado_aurion(v))
    else:
        print('Uso: crypto_sign.py [generate|sign|verify|resonancia|aurion]')
