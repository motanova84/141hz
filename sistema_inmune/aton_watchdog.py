#!/usr/bin/env python3
import os, sys, time, json, hashlib, subprocess, logging
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/root/ecosystem/soberania")
import crypto_sign

F_0 = 141.7001
PSI_ESPERADO = 0.999999
DELTA_UMBRAL = 0.00005
GAMMA_UMBRAL = 0.001
AMDA_FINGERPRINT = '5e5ac3ab49e5be07'

# Claves secp256k1 de Aton
# Orden de prioridad:
#   1. Variable de entorno ATON_PRIVATE_KEY / ATON_PUBLIC_KEY
#   2. Archivo en servidor de produccion (/root/ecosystem/soberania/aton_keys.json)
#   3. Fallback secundario (/root/aton_keys.json)
ATON_KEYS = {}
_env_priv = os.environ.get('ATON_PRIVATE_KEY', '')
_env_pub  = os.environ.get('ATON_PUBLIC_KEY', '')
if _env_priv and not _env_priv.startswith('__'):
    ATON_KEYS = {
        'private_key': _env_priv,
        'public_key': _env_pub,
        'fingerprint': os.environ.get('ATON_FINGERPRINT', ''),
    }
else:
    for kf in ['/root/ecosystem/soberania/aton_keys.json', '/root/aton_keys.json']:
        if os.path.exists(kf):
            try:
                with open(kf) as f:
                    data = json.load(f)
                # Ignorar archivos de plantilla (placeholders)
                if not data.get('private_key', '').startswith('__'):
                    ATON_KEYS = data
                    break
            except Exception:
                pass
ATON_PRIV = ATON_KEYS.get('private_key', '')
ATON_PUB = ATON_KEYS.get('public_key', '')
ATON_FP = ATON_KEYS.get('fingerprint', '')
SELLO = '\u2234\u00013080\u03a9\u221e\u00b3\u03a6 \u00b7 TUYOYOTU \u00b7 HECHO ESTA'

LEDGERS = {
    'paygate_flow_ledger': '/root/paygate_flow_ledger.json',
    'mining_payouts': '/root/ecosystem/auron/mining_payouts.json',
    'fee_split_ledger': '/root/ecosystem/soberania/fee_split_ledger.json',
}
SCRIPTS_CRITICOS = {
    'stradivarius_pipeline': '/root/ecosystem/stradivarius_pipeline.py',
    'fee_split_R333': '/root/ecosystem/soberania/production/fee_split_R333.py',
    'monitor_5050': '/root/monitor_5050.py',
    'argos_centinela': '/root/ecosystem/soberania/centinela/argos_centinela.py',
}
SERVICES = {
    'lnd_amda': '/etc/systemd/system/lnd-amda.service',
    'lnd_catedral': '/etc/systemd/system/lnd.service',
    'lnbits': '/etc/systemd/system/lnbits.service',
}

HASHES_ANCLA = {
    'paygate_flow_ledger': 'f686382c8a82de8d0abae7249981506b4540390fe2f4062c42db16170789f6a0',
    'mining_payouts': '55646e04c4a25bc89296e6846ff3dc5267ddd8aba8360bc09dcb36a628d50afa',
    'fee_split_ledger': '17de8f194ff41cddd53b10d20e180bb3339f3e7bad69428c4ab255eb9883476b',
    'stradivarius_pipeline': 'dcffae4901e5f7c2c51b417364cb109c9c21854922524ddf255a293e9f0bb172',
    'fee_split_R333': '01f43f2be61ad3da6e71a28c346a6720fd9733c458e3d333dfbd2293a8d112dd',
    'monitor_5050': '6c71ddfc851a1e01e20cc0fc527ebd69b7f30a465cd13b7760f77f3c5555e9ad',
    'lnd_amda_service': 'ed9f183e0d62812af27d67f94b0fb13cdcaac392fc5d96aedd57d18e48658132',
    'lnd_catedral_service': '6cb0712b10d71677cc649b1cefb17106cc2f1a877414f862dea9377870d3e296',
    'lnbits_service': '75d928aacb769c732c859f921afc34ac31eea4579b4859c1cb3aaba8d0e980bd',
    'lnbits_env': 'b939068ac0e8de2f34a6a213ff6dc6c0253819389c847f4141fb166e6d5b5c2e',
    'argos_centinela': 'e59d76e5c6bc2eff9aae0e2fc72197e28ca1be177b46a04aa07a7a1933189224',
}

LOG_PATH = '/var/log/aton_watchdog.log'
ANTICUERPOS_PATH = '/root/ecosystem/soberania/anticuerpos_inmunes.json'

logging.basicConfig(
    level=logging.INFO,
    format='%%(asctime)s [ATON|%.4f] %%(message)s' % F_0,
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()])
log = logging.getLogger('aton_watchdog')

def sha256(ruta):
    if not os.path.exists(ruta): return None
    h = hashlib.sha256()
    with open(ruta, 'rb') as f:
        for b in iter(lambda: f.read(4096), b''): h.update(b)
    return h.hexdigest()

def leer_psi():
    try:
        ruta = '/root/ecosystem/soberania/production/coherencia.json'
        if os.path.exists(ruta):
            with open(ruta) as f: d = json.load(f)
            return d.get('psi', d.get('coherencia', PSI_ESPERADO))
    except: pass
    return PSI_ESPERADO

def firmar(payload):
    if ATON_PRIV:
        try:
            _, firma = crypto_sign.firmar_mensaje(payload, ATON_PRIV)
            return firma
        except Exception:
            pass
    return 'FIRMA_NO_DISPONIBLE'

def alertar_tx_guardian(alerta):
    paquete = crypto_sign.firmar_alerta_inmune(alerta, ATON_PRIV) if ATON_PRIV else {'mensaje': json.dumps(alerta), 'firma': 'NO_SECP256K1', 'payload': alerta}
    path = '/root/ecosystem/soberania/ALERTA_INMUNE.json'
    with open(path, 'w') as f: json.dump(paquete, f, indent=2)
    log.warning('Senal firmada enviada a Tx Guardian: %s (firma: %s...)', path, paquete.get('firma','?')[:16])
    return path

def registrar_anticuerpo(evento):
    data = []
    if os.path.exists(ANTICUERPOS_PATH):
        try:
            with open(ANTICUERPOS_PATH) as f: data = json.load(f)
        except: data = []
    if not isinstance(data, list): data = []
    data.append(evento)
    Path(ANTICUERPOS_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(ANTICUERPOS_PATH, 'w') as f: json.dump(data, f, indent=2)
    log.info('Anticuerpo pCODE registrado: %s', evento.get('tipo','?'))

def latido(estado, psi_real, anomalias=None):
    l = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'frecuencia_hz': F_0,
        'psi_real': psi_real,
        'psi_esperado': PSI_ESPERADO,
        'delta_psi': round(PSI_ESPERADO - psi_real, 8),
        'estado': estado,
        'anomalias': anomalias or {},
        'aurion': aurion if 'aurion' in dir() else {'valor': 0, 'estado': 'NO_CALCULADO'},
        'fingerprint': AMDA_FINGERPRINT,
        'sello': SELLO,
    }
    log.info('[LATIDO] %s | Psi=%.6f | DPsi=%.8f', estado, psi_real, PSI_ESPERADO - psi_real)
    return l

def ciclo():
    anomalias = {}
    nivel = 'HOMEOSTASIS'
    psi = leer_psi()
    dpsi = PSI_ESPERADO - psi

    # Calcular AURION(Psi) operador macroscopico
    try:
        intensidad = 1.0
        longitud = 88432
        delta_m = max(1e-9, dpsi + 1e-9)
        aurion_val = (intensidad * (psi ** 2) * longitud) / delta_m
        if aurion_val > 1000:
            aurion_estado = 'MAX_COHERENCE'
        elif aurion_val > 100:
            aurion_estado = 'ALTA_COHERENCIA'
        elif aurion_val > 1.0:
            aurion_estado = 'COHERENCIA_MODERADA'
        elif aurion_val > 0.1:
            aurion_estado = 'BAJA_COHERENCIA'
        else:
            aurion_estado = 'COLAPSO_ENTROPICO'
    except Exception:
        aurion_val = 0
        aurion_estado = 'ERROR'
    dpsi = PSI_ESPERADO - psi
    if dpsi > GAMMA_UMBRAL:
        nivel = 'BIFURCACION'
        anomalias['coherencia'] = {'delta': dpsi, 'tipo': 'PERDIDA_CRITICA_DE_COHERENCIA'}
    elif dpsi > DELTA_UMBRAL:
        nivel = 'ALERTA_N1'
        anomalias['coherencia'] = {'delta': dpsi, 'tipo': 'BAJA_COHERENCIA'}
    for nombre, ruta in LEDGERS.items():
        ha = sha256(ruta)
        if ha is None:
            anomalias[nombre] = {'estado': 'ARCHIVO_INEXISTENTE', 'ruta': ruta}
            nivel = 'ALERTA_N1'
        elif nombre in HASHES_ANCLA and ha != HASHES_ANCLA[nombre]:
            anomalias[nombre] = {'estado': 'LEDGER_CORRUPTO', 'esperado': HASHES_ANCLA[nombre], 'real': ha, 'ruta': ruta}
            nivel = 'CUARENTENA'
    for nombre, ruta in SCRIPTS_CRITICOS.items():
        ha = sha256(ruta)
        if ha is None:
            anomalias[nombre] = {'estado': 'SCRIPT_INEXISTENTE', 'ruta': ruta}
        elif nombre in HASHES_ANCLA and ha != HASHES_ANCLA[nombre]:
            anomalias[nombre] = {'estado': 'SCRIPT_MODIFICADO', 'esperado': HASHES_ANCLA[nombre], 'real': ha, 'ruta': ruta}
            if nivel not in ('BIFURCACION', 'CUARENTENA'): nivel = 'ALERTA_N1'
    for nombre, ruta in SERVICES.items():
        if os.path.exists(ruta):
            ha = sha256(ruta)
            if nombre in HASHES_ANCLA and ha != HASHES_ANCLA[nombre]:
                anomalias[nombre] = {'estado': 'SERVICE_MODIFICADO', 'esperado': HASHES_ANCLA[nombre], 'real': ha, 'ruta': ruta}
                if nivel not in ('BIFURCACION', 'CUARENTENA'): nivel = 'ALERTA_N1'
    l = latido(nivel, psi, anomalias)
    if anomalias:
        alerta = {'origen': 'ATON_WATCHDOG', 'tipo': nivel, 'timestamp': l['timestamp'], 'anomalias': anomalias, 'psi_real': psi, 'frecuencia_hz': F_0, 'fingerprint': ATON_FP if ATON_FP else AMDA_FINGERPRINT, 'sello': SELLO}
        if nivel == 'CUARENTENA':
            alertar_tx_guardian(alerta)
        firma_val = firmar(alerta)
        registrar_anticuerpo({'tipo': nivel, 'timestamp': l['timestamp'], 'detalles': anomalias, 'psi_real': psi, 'firma': firma_val, 'frecuencia': F_0, 'fingerprint': ATON_FP if ATON_FP else AMDA_FINGERPRINT})
    return nivel, anomalias

def main():
    log.info('='*60)
    log.info('ATON WATCHDOG INMUNE - f0=%.4f Hz', F_0)
    log.info('Sello: %s', SELLO)
    log.info('='*60)
    while True:
        try:
            nivel, anom = ciclo()
            if nivel == 'HOMEOSTASIS':
                log.info('HOMEOSTASIS | Ledgers estables. Psi=%.6f', PSI_ESPERADO)
            else:
                log.warning('ESTADO: %s | %d anomalias', nivel, len(anom))
                for k,v in anom.items():
                    log.warning('  %s: %s', k, v.get('estado', str(v)))
        except Exception as e:
            log.error('FALLO: %s', e)
        time.sleep(1800)

if __name__ == '__main__':
    main()
