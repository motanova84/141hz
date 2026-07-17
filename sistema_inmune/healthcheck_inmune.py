#!/usr/bin/env python3
import subprocess, sys, json
sys.path.insert(0, '/root/ecosystem/soberania')
from crypto_sign import calcular_aurion, comprobar_resonancia, es_matriz_refractaria

print('SISTEMA INMUNE QCAL - HEALTHCHECK')
print('f0 = 141.7001 Hz')
print('='*45)

a = subprocess.run(['systemctl','is-active','aton-watchdog'], capture_output=True, text=True).stdout.strip()
t = subprocess.run(['systemctl','is-active','tx-guardian'], capture_output=True, text=True).stdout.strip()
print('[DAEMONS] Aton:', a, '| TxGuardian:', t)

r = comprobar_resonancia(141.7001)
print('[CRYPTO] Resonancia:', r)

v = calcular_aurion(1.0, 0.999999, 88432, 1e-9)
print('[AURION]', round(v, 2))

try:
    with open('/root/ecosystem/soberania/anticuerpos_inmunes.json') as f:
        d = json.load(f)
    print('[MEMORIA]', len(d), 'anticuerpos')
except: print('[MEMORIA] No accesible')

print('[REFRACTARIO]', es_matriz_refractaria(0.999999))
print('[ESTADO]', 'VACIO ACTIVO: RESONANDO' if v > 100000 else 'VACIO ACTIVO: EN ESPERA')
print()
print('f0 = 141.7001 Hz')
print('HECHO ESTA')
