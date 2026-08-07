# CATEDRAL DE MINADO QCAL — Arquitectura Híbrida

## Topología Distribuida

```
[Atlas3 (Mac mini local)] ───(hashes)───> [BAL-003 (Nuremberg)] ───(Stratum proxy)───> [ViaBTC Pool]
      CPU/ASICs locales                      socat :3333 → btc.viabtc.top:3333           btc.viabtc.top:3333
      Ejecuta hashes                         Filtro inmune + Tx Guardian                 noesis88.001
      Conexión a localhost:3333              IP estática 195.201.219.237                 Dificultad 500000
```

## Componentes

| Capa | Nodo | Función |
|------|------|---------|
| **Cómputo** | Atlas3 (Mac mini) | Genera hashes SHA256AsicBoost |
| **Proxy** | BAL-003 (Nuremberg) | Reenvía Stratum, filtra tráfico |
| **Pool** | ViaBTC | Acepta shares, paga recompensas |

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `catedral_miner.py` | Orquestador del flujo Stratum (en BAL-003 o Atlas3) |
| `pool_interface.py` | Interfaz con ViaBTC — verifica pool, registra shares |
| `qcal_stradivarius.py` | Proxy Stratum con filtro espectral p-ádico + AURION(Psi) |
| `aurion_bridge.py` | Interfaz portable al motor de coherencia AURION(Psi) |
| `qcal_hash_daemon.cpp` | Daemon C++ de verificación de fase armónica (SHA256) |
| `emision_ledger.json` | Ledger de emisión — contador de shares y sesiones |
| `miner.conf` | Configuración persistente del pool |

## Filtro AURION

Cada share pasa por dos capas de validación antes de llegar al pool:

1. **Métrica p-ádica** — verifica que el espacio de fase del nonce sea armónico con f₀  
   `(int(job_id[:16], 16) + int(nonce[:8], 16)) % 7 == 0`

2. **Coherencia AURION(Psi)** — evalúa el sistema en Matriz Refractaria  
   `AURION(Psi) = (I × A_eff² × L) / δM`  
   Si Psi ≥ 0.999999 → Matriz Refractaria activa → share sellado y enviado  
   Si Psi < 0.999999 → share en cuarentena (Vacío Activo)

El módulo `aurion_bridge.py` resuelve automáticamente la ruta de `sistema_inmune/crypto_sign.py`
tanto en entorno de repositorio (CI/desarrollo) como en despliegue en servidor.

## Conexión desde Atlas3

```bash
# cgminer apunta al proxy local en BAL-003
./cgminer --algo sha256asicboost \
  -o stratum+tcp://localhost:3333 \
  -u noesis88.001 \
  -p x

# O si prefieres UDP tunnel:
# socat TCP-LISTEN:3333,fork TCP:195.201.219.237:3333
```

## Proxy Stratum / Stradivarius (BAL-003)

Proxy Python con filtro QCAL:
```bash
python3 qcal_stradivarius.py
```

O via socat simple (sin filtro):
```
/usr/bin/socat TCP-LISTEN:3333,reuseaddr,fork TCP:btc.viabtc.top:3333
```

Verificar:
```bash
systemctl status stratum-proxy
python3 pool_interface.py check
python3 aurion_bridge.py
```

## Daemon Hash C++

```bash
# Compilar
g++ -O2 -o qcal_hash_daemon qcal_hash_daemon.cpp

# Verificar un share
./qcal_hash_daemon <block_header_hex> <nonce> [worker]
```

f0 = 141.7001 Hz  
Sello: (c) 3080 (r) (inf)3(phi) · TUYOYOTU · HECHO ESTA

