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
| `emision_ledger.json` | Ledger de emisión — contador de shares y sesiones |
| `miner.conf` | Configuración persistente del pool |

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

## Proxy Stratum (BAL-003)

Ya operativo via systemd:
```
/usr/bin/socat TCP-LISTEN:3333,reuseaddr,fork TCP:btc.viabtc.top:3333
```

Verificar:
```bash
systemctl status stratum-proxy
pool_interface.py check
```

f0 = 141.7001 Hz
Sello: (c) 3080 (r) (inf)3(phi) · TUYOYOTU · HECHO ESTA
